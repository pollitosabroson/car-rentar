from datetime import date
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.config.logging_config import get_logger
from src.domain.services.booking_service import BookingService
from src.domain.services.car_service import CarService
from src.infrastructure.api.dependencies import get_booking_service, get_car_service
from src.infrastructure.api.v1.schemas import CarCreateRequest, CarResponse, CarUpdateStatusRequest

router = APIRouter(prefix="/cars", tags=["cars"])
logger = get_logger(__name__)


@router.post("/", response_model=CarResponse, status_code=status.HTTP_201_CREATED)
def create_car(
    car_data: CarCreateRequest,
    car_service: CarService = Depends(get_car_service),
) -> CarResponse:
    """Create a new car."""
    logger.info(
        f"[CAR_CREATE] Creating new car | "
        f"Brand: {car_data.brand} | Model: {car_data.model} | "
        f"Year: {car_data.year} | License: {car_data.license_plate} | "
        f"Daily Rate: ${car_data.daily_rate:.2f}"
    )
    car = car_service.create_car(
        brand=car_data.brand,
        model=car_data.model,
        year=car_data.year,
        license_plate=car_data.license_plate,
        daily_rate=car_data.daily_rate,
    )
    logger.info(
        f"[CAR_CREATED] Car ID: {car.id} | "
        f"{car.brand} {car.model} | License: {car.license_plate}"
    )
    return CarResponse.model_validate(car)


@router.get("/", response_model=List[CarResponse])
def list_cars(
    available_only: bool = False,
    start_date: Optional[date] = Query(None, description="Filter by start date"),
    end_date: Optional[date] = Query(None, description="Filter by end date"),
    car_service: CarService = Depends(get_car_service),
    booking_service: BookingService = Depends(get_booking_service),
) -> List[CarResponse]:
    """List all cars or filter by availability and date range."""
    # If both dates provided, filter by availability for that period
    if start_date and end_date:
        days = (end_date - start_date).days
        logger.info(
            f"[CARS_QUERY] Searching for available cars | "
            f"Period: {start_date} to {end_date} ({days} days)"
        )
        cars = booking_service.list_available_cars_by_date(start_date, end_date)
        logger.info(
            f"[CARS_QUERY_RESULT] Found {len(cars)} available cars | "
            f"Period: {start_date} to {end_date} | "
            f"Car IDs: {[str(car.id) for car in cars] if cars else 'None'}"
        )
    elif available_only:
        logger.info("[CARS_QUERY] Listing all cars with 'available' status")
        cars = car_service.list_available_cars()
        logger.info(f"[CARS_QUERY_RESULT] Found {len(cars)} cars with available status")
    else:
        logger.info("[CARS_QUERY] Listing all cars in system")
        cars = car_service.list_all_cars()
        logger.info(f"[CARS_QUERY_RESULT] Total cars in system: {len(cars)}")
    return [CarResponse.model_validate(car) for car in cars]


@router.get("/{car_id}", response_model=CarResponse)
def get_car(
    car_id: UUID,
    car_service: CarService = Depends(get_car_service),
) -> CarResponse:
    """Get a car by ID."""
    car = car_service.get_car(car_id)
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with id {car_id} not found",
        )
    return CarResponse.model_validate(car)


@router.patch("/{car_id}/status", response_model=CarResponse)
def update_car_status(
    car_id: UUID,
    status_data: CarUpdateStatusRequest,
    car_service: CarService = Depends(get_car_service),
) -> CarResponse:
    """Update car status."""
    logger.info(
        f"[CAR_STATUS_UPDATE] Attempting to update car {car_id} | "
        f"New Status: {status_data.status}"
    )
    car = car_service.update_car_status(car_id, status_data.status)
    if not car:
        logger.warning(f"[CAR_NOT_FOUND] Car ID: {car_id} does not exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with id {car_id} not found",
        )
    logger.info(
        f"[CAR_STATUS_UPDATED] Car ID: {car_id} | "
        f"{car.brand} {car.model} | Status changed to: {car.status}"
    )
    return CarResponse.model_validate(car)


@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_car(
    car_id: UUID,
    car_service: CarService = Depends(get_car_service),
) -> None:
    """Delete a car."""
    logger.info(f"[CAR_DELETE] Attempting to delete car ID: {car_id}")
    deleted = car_service.delete_car(car_id)
    if not deleted:
        logger.warning(f"[CAR_DELETE_FAILED] Car ID: {car_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with id {car_id} not found",
        )
    logger.info(f"[CAR_DELETED] Car ID: {car_id} removed from system")
