from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from src.domain.entities.booking import BookingStatus
from src.domain.entities.car import CarStatus


class CarCreateRequest(BaseModel):
    """Request schema for creating a car."""

    brand: str = Field(min_length=1, max_length=50)
    model: str = Field(min_length=1, max_length=50)
    year: int = Field(ge=1900, le=2100)
    license_plate: str = Field(min_length=1, max_length=20)
    daily_rate: float = Field(gt=0)


class CarUpdateStatusRequest(BaseModel):
    """Request schema for updating car status."""

    status: CarStatus


class CarResponse(BaseModel):
    """Response schema for car data."""

    id: UUID
    brand: str
    model: str
    year: int
    license_plate: str
    daily_rate: float
    status: CarStatus
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class BookingCreateRequest(BaseModel):
    """Request schema for creating a booking."""

    car_id: UUID
    customer_name: str = Field(min_length=1, max_length=100)
    customer_email: str = Field(min_length=1, max_length=100)
    start_date: date
    end_date: date


class BookingResponse(BaseModel):
    """Response schema for booking data."""

    id: UUID
    car_id: UUID
    customer_name: str
    customer_email: str
    start_date: date
    end_date: date
    total_cost: float
    status: BookingStatus
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        """Pydantic configuration."""

        from_attributes = True
