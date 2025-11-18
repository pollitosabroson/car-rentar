import json
from datetime import date
from pathlib import Path
from typing import List, Optional
from uuid import UUID

from src.domain.entities.booking import Booking
from src.domain.ports.booking_repository import BookingRepository


class JsonBookingRepository(BookingRepository):
    """JSON file-based implementation of BookingRepository."""

    def __init__(self, data_dir: Path) -> None:
        self._data_dir = data_dir
        self._file_path = data_dir / "bookings.json"
        self._ensure_data_dir()
        self._ensure_file()

    def _ensure_data_dir(self) -> None:
        """Ensure the data directory exists."""
        self._data_dir.mkdir(parents=True, exist_ok=True)

    def _ensure_file(self) -> None:
        """Ensure the JSON file exists."""
        if not self._file_path.exists():
            self._write_data([])

    def _read_data(self) -> List[dict]:
        """Read data from JSON file."""
        with open(self._file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_data(self, data: List[dict]) -> None:
        """Write data to JSON file."""
        with open(self._file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)

    def save(self, booking: Booking) -> Booking:
        """Save a booking entity."""
        data = self._read_data()
        booking_dict = booking.model_dump(mode="json")
        booking_dict["id"] = str(booking_dict["id"])
        booking_dict["car_id"] = str(booking_dict["car_id"])
        data.append(booking_dict)
        self._write_data(data)
        return booking

    def find_by_id(self, booking_id: UUID) -> Optional[Booking]:
        """Find a booking by its ID."""
        data = self._read_data()
        for booking_dict in data:
            if booking_dict["id"] == str(booking_id):
                return Booking(**booking_dict)
        return None

    def find_all(self) -> List[Booking]:
        """Get all bookings."""
        data = self._read_data()
        return [Booking(**booking_dict) for booking_dict in data]

    def find_by_car_and_date_range(
        self, car_id: UUID, start_date: date, end_date: date
    ) -> List[Booking]:
        """Find bookings for a specific car within a date range."""
        data = self._read_data()
        bookings = []

        for booking_dict in data:
            if booking_dict["car_id"] != str(car_id):
                continue

            booking = Booking(**booking_dict)

            # Check if booking dates overlap with the requested range
            if self._dates_overlap(start_date, end_date, booking.start_date, booking.end_date):
                bookings.append(booking)

        return bookings

    def _dates_overlap(self, start1: date, end1: date, start2: date, end2: date) -> bool:
        """Check if two date ranges overlap."""
        return start1 < end2 and end1 > start2

    def update(self, booking: Booking) -> Optional[Booking]:
        """Update an existing booking."""
        data = self._read_data()
        for i, booking_dict in enumerate(data):
            if booking_dict["id"] == str(booking.id):
                updated_dict = booking.model_dump(mode="json")
                updated_dict["id"] = str(updated_dict["id"])
                updated_dict["car_id"] = str(updated_dict["car_id"])
                data[i] = updated_dict
                self._write_data(data)
                return booking
        return None

    def delete(self, booking_id: UUID) -> bool:
        """Delete a booking by its ID."""
        data = self._read_data()
        original_length = len(data)
        data = [booking_dict for booking_dict in data if booking_dict["id"] != str(booking_id)]
        if len(data) < original_length:
            self._write_data(data)
            return True
        return False
