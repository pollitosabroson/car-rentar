from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.config.logging_config import get_logger
from src.domain.services.booking_service import BookingService
from src.infrastructure.api.dependencies import get_booking_service
from src.infrastructure.api.v1.schemas import BookingCreateRequest, BookingResponse

router = APIRouter(prefix="/bookings", tags=["bookings"])
logger = get_logger(__name__)


@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking_data: BookingCreateRequest,
    booking_service: BookingService = Depends(get_booking_service),
) -> BookingResponse:
    """Create a new booking."""
    try:
        logger.info(
            f"[BOOKING_ATTEMPT] Customer: {booking_data.customer_name} "
            f"({booking_data.customer_email}) | Car ID: {booking_data.car_id} | "
            f"Period: {booking_data.start_date} to {booking_data.end_date} | "
            f"Days: {(booking_data.end_date - booking_data.start_date).days}"
        )

        booking = booking_service.create_booking(
            car_id=booking_data.car_id,
            customer_name=booking_data.customer_name,
            customer_email=booking_data.customer_email,
            start_date=booking_data.start_date,
            end_date=booking_data.end_date,
        )

        logger.info(
            f"[BOOKING_SUCCESS] Booking ID: {booking.id} | "
            f"Customer: {booking.customer_name} | Car ID: {booking.car_id} | "
            f"Total Cost: ${booking.total_cost:.2f} | Status: {booking.status}"
        )

        return BookingResponse.model_validate(booking)

    except ValueError as e:
        logger.warning(
            f"[BOOKING_FAILED] Customer: {booking_data.customer_name} | "
            f"Car ID: {booking_data.car_id} | "
            f"Period: {booking_data.start_date} to {booking_data.end_date} | "
            f"Reason: {str(e)}"
        )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(
            f"[BOOKING_ERROR] Unexpected error for customer {booking_data.customer_name} | "
            f"Car ID: {booking_data.car_id} | Error: {str(e)}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create booking",
        )


@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(
    booking_id: UUID,
    booking_service: BookingService = Depends(get_booking_service),
) -> BookingResponse:
    """Get a booking by ID."""
    try:
        logger.info(f"[BOOKING_QUERY] Attempting to retrieve booking ID: {booking_id}")
        booking = booking_service.get_booking(booking_id)
        logger.info(
            f"[BOOKING_RETRIEVED] Booking ID: {booking_id} | "
            f"Customer: {booking.customer_name} | Status: {booking.status}"
        )
        return BookingResponse.model_validate(booking)
    except ValueError as e:
        logger.warning(f"[BOOKING_NOT_FOUND] Booking ID: {booking_id} | Reason: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.patch("/{booking_id}/cancel", response_model=BookingResponse)
def cancel_booking(
    booking_id: UUID,
    booking_service: BookingService = Depends(get_booking_service),
) -> BookingResponse:
    """Cancel a booking."""
    try:
        logger.info(f"[BOOKING_CANCEL_ATTEMPT] Attempting to cancel booking ID: {booking_id}")
        booking = booking_service.cancel_booking(booking_id)
        logger.info(
            f"[BOOKING_CANCELLED] Booking ID: {booking_id} | "
            f"Customer: {booking.customer_name} | Car ID: {booking.car_id} | "
            f"Period: {booking.start_date} to {booking.end_date}"
        )
        return BookingResponse.model_validate(booking)
    except ValueError as e:
        logger.warning(f"[BOOKING_CANCEL_FAILED] Booking ID: {booking_id} | Reason: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
