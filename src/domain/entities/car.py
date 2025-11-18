from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class CarStatus(str, Enum):
    """Car availability status."""

    AVAILABLE = "available"
    RENTED = "rented"
    MAINTENANCE = "maintenance"


class Car(BaseModel):
    """Car entity representing a rental car in the domain."""

    id: UUID = Field(default_factory=uuid4)
    brand: str = Field(min_length=1, max_length=50)
    model: str = Field(min_length=1, max_length=50)
    year: int = Field(ge=1900, le=2100)
    license_plate: str = Field(min_length=1, max_length=20)
    daily_rate: float = Field(gt=0)
    status: CarStatus = Field(default=CarStatus.AVAILABLE)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Config:
        """Pydantic configuration."""

        use_enum_values = True
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat(),
        }
