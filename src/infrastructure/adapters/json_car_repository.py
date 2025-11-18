import json
from pathlib import Path
from typing import List, Optional
from uuid import UUID

from src.domain.entities.car import Car
from src.domain.ports.car_repository import CarRepository


class JsonCarRepository(CarRepository):
    """JSON file-based implementation of CarRepository."""

    def __init__(self, data_dir: Path) -> None:
        self._data_dir = data_dir
        self._file_path = data_dir / "cars.json"
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

    def save(self, car: Car) -> Car:
        """Save a car entity."""
        data = self._read_data()
        car_dict = car.model_dump(mode="json")
        car_dict["id"] = str(car_dict["id"])
        data.append(car_dict)
        self._write_data(data)
        return car

    def find_by_id(self, car_id: UUID) -> Optional[Car]:
        """Find a car by its ID."""
        data = self._read_data()
        for car_dict in data:
            if car_dict["id"] == str(car_id):
                return Car(**car_dict)
        return None

    def find_all(self) -> List[Car]:
        """Get all cars."""
        data = self._read_data()
        return [Car(**car_dict) for car_dict in data]

    def update(self, car: Car) -> Optional[Car]:
        """Update an existing car."""
        data = self._read_data()
        for i, car_dict in enumerate(data):
            if car_dict["id"] == str(car.id):
                updated_dict = car.model_dump(mode="json")
                updated_dict["id"] = str(updated_dict["id"])
                data[i] = updated_dict
                self._write_data(data)
                return car
        return None

    def delete(self, car_id: UUID) -> bool:
        """Delete a car by its ID."""
        data = self._read_data()
        original_length = len(data)
        data = [car_dict for car_dict in data if car_dict["id"] != str(car_id)]
        if len(data) < original_length:
            self._write_data(data)
            return True
        return False
