from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.entities.car import Car


class CarRepository(ABC):
    """Port (interface) for car repository operations."""

    @abstractmethod
    def save(self, car: Car) -> Car:
        """Save a car entity."""
        pass

    @abstractmethod
    def find_by_id(self, car_id: UUID) -> Optional[Car]:
        """Find a car by its ID."""
        pass

    @abstractmethod
    def find_all(self) -> List[Car]:
        """Get all cars."""
        pass

    @abstractmethod
    def update(self, car: Car) -> Optional[Car]:
        """Update an existing car."""
        pass

    @abstractmethod
    def delete(self, car_id: UUID) -> bool:
        """Delete a car by its ID."""
        pass
