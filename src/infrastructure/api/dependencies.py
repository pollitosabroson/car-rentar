from src.config.settings import settings
from src.domain.services.booking_service import BookingService
from src.domain.services.car_service import CarService
from src.infrastructure.adapters.json_booking_repository import JsonBookingRepository
from src.infrastructure.adapters.json_car_repository import JsonCarRepository


def get_car_service() -> CarService:
    """Dependency injection for CarService."""
    repository = JsonCarRepository(settings.data_path)
    return CarService(repository)


def get_booking_service() -> BookingService:
    """Dependency injection for BookingService."""
    booking_repository = JsonBookingRepository(settings.data_path)
    car_repository = JsonCarRepository(settings.data_path)
    return BookingService(booking_repository, car_repository)
