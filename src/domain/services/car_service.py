from datetime import datetime
from typing import List, Optional
from uuid import UUID

from src.domain.entities.car import Car, CarStatus
from src.domain.ports.car_repository import CarRepository


class CarService:
    """Domain service containing business logic for car operations."""

    def __init__(self, car_repository: CarRepository) -> None:
        self._repository = car_repository

    def create_car(
        self,
        brand: str,
        model: str,
        year: int,
        license_plate: str,
        daily_rate: float,
    ) -> Car:
        """Create a new car."""
        car = Car(
            brand=brand,
            model=model,
            year=year,
            license_plate=license_plate,
            daily_rate=daily_rate,
        )
        return self._repository.save(car)

    def get_car(self, car_id: UUID) -> Optional[Car]:
        """Get a car by its ID."""
        return self._repository.find_by_id(car_id)

    def list_all_cars(self) -> List[Car]:
        """List all cars."""
        return self._repository.find_all()

    def list_available_cars(self) -> List[Car]:
        """List only available cars."""
        all_cars = self._repository.find_all()
        return [car for car in all_cars if car.status == CarStatus.AVAILABLE]

    def update_car_status(self, car_id: UUID, status: CarStatus) -> Optional[Car]:
        """Update the status of a car."""
        car = self._repository.find_by_id(car_id)
        if not car:
            return None

        car.status = status
        car.updated_at = datetime.utcnow()
        return self._repository.update(car)

    def delete_car(self, car_id: UUID) -> bool:
        """Delete a car."""
        return self._repository.delete(car_id)
