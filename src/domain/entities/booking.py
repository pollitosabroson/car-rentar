from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class BookingStatus(str, Enum):
    """Booking status."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Booking(BaseModel):
    """Booking entity representing a car rental reservation."""

    id: UUID = Field(default_factory=uuid4)
    car_id: UUID
    customer_name: str = Field(min_length=1, max_length=100)
    customer_email: str = Field(min_length=1, max_length=100)
    start_date: date
    end_date: date
    total_cost: float = Field(gt=0)
    status: BookingStatus = Field(default=BookingStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    @field_validator("end_date")
    @classmethod
    def validate_end_date(cls, v: date, info) -> date:
        """Validate that end_date is after start_date."""
        if "start_date" in info.data and v <= info.data["start_date"]:
            raise ValueError("end_date must be after start_date")
        return v

    @field_validator("start_date")
    @classmethod
    def validate_start_date(cls, v: date) -> date:
        """Validate that start_date is not in the past."""
        if v < date.today():
            raise ValueError("start_date cannot be in the past")
        return v

    class Config:
        """Pydantic configuration."""

        use_enum_values = True
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
        }
