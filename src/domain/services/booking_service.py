from datetime import date
from typing import List
from uuid import UUID

from src.domain.entities.booking import Booking, BookingStatus
from src.domain.entities.car import Car, CarStatus
from src.domain.ports.booking_repository import BookingRepository
from src.domain.ports.car_repository import CarRepository


class BookingService:
    """Domain service containing business logic for booking operations."""

    def __init__(
        self, booking_repository: BookingRepository, car_repository: CarRepository
    ) -> None:
        self._booking_repository = booking_repository
        self._car_repository = car_repository

    def create_booking(
        self,
        car_id: UUID,
        customer_name: str,
        customer_email: str,
        start_date: date,
        end_date: date,
    ) -> Booking:
        """Create a new booking."""
        # Check if car exists
        car = self._car_repository.find_by_id(car_id)
        if not car:
            raise ValueError("Car not found")

        # Check if car is available for the requested dates
        if not self._is_car_available(car_id, start_date, end_date):
            raise ValueError("Car is not available for the selected dates")

        # Calculate total cost
        days = (end_date - start_date).days
        total_cost = days * car.daily_rate

        # Create booking
        booking = Booking(
            car_id=car_id,
            customer_name=customer_name,
            customer_email=customer_email,
            start_date=start_date,
            end_date=end_date,
            total_cost=total_cost,
        )

        return self._booking_repository.save(booking)

    def _is_car_available(self, car_id: UUID, start_date: date, end_date: date) -> bool:
        """Check if a car is available for the given date range."""
        # Get all bookings for this car in the date range
        existing_bookings = self._booking_repository.find_by_car_and_date_range(
            car_id, start_date, end_date
        )

        # Check for any confirmed or pending bookings that overlap
        for booking in existing_bookings:
            if booking.status in [BookingStatus.CONFIRMED, BookingStatus.PENDING]:
                # Check if dates overlap
                if self._dates_overlap(start_date, end_date, booking.start_date, booking.end_date):
                    return False

        return True

    def _dates_overlap(self, start1: date, end1: date, start2: date, end2: date) -> bool:
        """Check if two date ranges overlap."""
        return start1 < end2 and end1 > start2

    def list_available_cars_by_date(self, start_date: date, end_date: date) -> List[Car]:
        """List all cars available for a specific date range."""
        all_cars = self._car_repository.find_all()
        available_cars = []

        for car in all_cars:
            # Skip cars that are not in available status
            if car.status != CarStatus.AVAILABLE:
                continue

            # Check if car has no conflicting bookings
            if self._is_car_available(car.id, start_date, end_date):
                available_cars.append(car)

        return available_cars

    def get_booking(self, booking_id: UUID) -> Booking:
        """Get a booking by ID."""
        booking = self._booking_repository.find_by_id(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        return booking

    def cancel_booking(self, booking_id: UUID) -> Booking:
        """Cancel a booking."""
        booking = self.get_booking(booking_id)
        booking.status = BookingStatus.CANCELLED
        return self._booking_repository.update(booking)
