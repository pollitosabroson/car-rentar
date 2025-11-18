from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional
from uuid import UUID

from src.domain.entities.booking import Booking


class BookingRepository(ABC):
    """Port (interface) for booking repository operations."""

    @abstractmethod
    def save(self, booking: Booking) -> Booking:
        """Save a booking entity."""
        pass

    @abstractmethod
    def find_by_id(self, booking_id: UUID) -> Optional[Booking]:
        """Find a booking by its ID."""
        pass

    @abstractmethod
    def find_all(self) -> List[Booking]:
        """Get all bookings."""
        pass

    @abstractmethod
    def find_by_car_and_date_range(
        self, car_id: UUID, start_date: date, end_date: date
    ) -> List[Booking]:
        """Find bookings for a specific car within a date range."""
        pass

    @abstractmethod
    def update(self, booking: Booking) -> Optional[Booking]:
        """Update an existing booking."""
        pass

    @abstractmethod
    def delete(self, booking_id: UUID) -> bool:
        """Delete a booking by its ID."""
        pass
