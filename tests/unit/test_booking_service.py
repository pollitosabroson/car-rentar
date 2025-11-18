from datetime import date, timedelta
from unittest.mock import Mock
from uuid import uuid4

import pytest

from src.domain.entities.booking import BookingStatus
from src.domain.entities.car import Car, CarStatus
from src.domain.services.booking_service import BookingService


class TestBookingService:
    """Unit tests for BookingService."""

    @pytest.fixture
    def mock_booking_repository(self):
        """Create a mock booking repository."""
        return Mock()

    @pytest.fixture
    def mock_car_repository(self):
        """Create a mock car repository."""
        return Mock()

    @pytest.fixture
    def booking_service(self, mock_booking_repository, mock_car_repository):
        """Create a BookingService instance with mocked dependencies."""
        return BookingService(mock_booking_repository, mock_car_repository)

    @pytest.fixture
    def sample_car(self):
        """Create a sample car for testing."""
        return Car(
            id=uuid4(),
            brand="Toyota",
            model="Corolla",
            year=2023,
            license_plate="ABC-123",
            daily_rate=50.0,
            status=CarStatus.AVAILABLE,
        )

    def test_create_booking_success(
        self, booking_service, mock_car_repository, mock_booking_repository, sample_car
    ):
        """Test successful booking creation."""
        # Arrange
        start_date = date.today() + timedelta(days=1)
        end_date = date.today() + timedelta(days=3)

        mock_car_repository.find_by_id.return_value = sample_car
        mock_booking_repository.find_by_car_and_date_range.return_value = []

        # Mock save to return the booking passed to it
        def save_booking(booking):
            return booking

        mock_booking_repository.save.side_effect = save_booking

        # Act
        booking = booking_service.create_booking(
            car_id=sample_car.id,
            customer_name="John Doe",
            customer_email="john@example.com",
            start_date=start_date,
            end_date=end_date,
        )

        # Assert
        assert booking is not None
        assert booking.car_id == sample_car.id
        assert booking.customer_name == "John Doe"
        assert booking.total_cost == 100.0  # 2 days * 50.0
        mock_booking_repository.save.assert_called_once()

    def test_create_booking_car_not_found(
        self, booking_service, mock_car_repository, mock_booking_repository
    ):
        """Test booking creation fails when car doesn't exist."""
        # Arrange
        car_id = uuid4()
        start_date = date.today() + timedelta(days=1)
        end_date = date.today() + timedelta(days=3)

        mock_car_repository.find_by_id.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="Car not found"):
            booking_service.create_booking(
                car_id=car_id,
                customer_name="John Doe",
                customer_email="john@example.com",
                start_date=start_date,
                end_date=end_date,
            )

    def test_create_booking_car_not_available(
        self, booking_service, mock_car_repository, mock_booking_repository, sample_car
    ):
        """Test booking creation fails when car has conflicting bookings."""
        # Arrange
        sample_car.status = CarStatus.AVAILABLE
        start_date = date.today() + timedelta(days=1)
        end_date = date.today() + timedelta(days=3)

        mock_car_repository.find_by_id.return_value = sample_car

        # Simulate existing booking
        existing_booking = Mock(
            start_date=date.today() + timedelta(days=2),
            end_date=date.today() + timedelta(days=4),
            status=BookingStatus.CONFIRMED,
        )
        mock_booking_repository.find_by_car_and_date_range.return_value = [existing_booking]

        # Act & Assert
        with pytest.raises(ValueError, match="Car is not available"):
            booking_service.create_booking(
                car_id=sample_car.id,
                customer_name="John Doe",
                customer_email="john@example.com",
                start_date=start_date,
                end_date=end_date,
            )

    def test_list_available_cars_by_date(
        self, booking_service, mock_car_repository, mock_booking_repository
    ):
        """Test listing available cars for a specific date range."""
        # Arrange
        start_date = date.today() + timedelta(days=1)
        end_date = date.today() + timedelta(days=3)

        car1 = Car(
            id=uuid4(),
            brand="Toyota",
            model="Corolla",
            year=2023,
            license_plate="ABC-123",
            daily_rate=50.0,
            status=CarStatus.AVAILABLE,
        )
        car2 = Car(
            id=uuid4(),
            brand="Honda",
            model="Civic",
            year=2023,
            license_plate="XYZ-789",
            daily_rate=60.0,
            status=CarStatus.AVAILABLE,
        )
        car3 = Car(
            id=uuid4(),
            brand="Ford",
            model="Focus",
            year=2023,
            license_plate="DEF-456",
            daily_rate=55.0,
            status=CarStatus.RENTED,  # Not available
        )

        mock_car_repository.find_all.return_value = [car1, car2, car3]

        # Car2 has a conflicting booking
        def mock_find_by_car_and_date_range(car_id, start, end):
            if car_id == car2.id:
                return [
                    Mock(
                        start_date=start_date,
                        end_date=end_date,
                        status=BookingStatus.CONFIRMED,
                    )
                ]
            return []

        mock_booking_repository.find_by_car_and_date_range.side_effect = (
            mock_find_by_car_and_date_range
        )

        # Act
        available_cars = booking_service.list_available_cars_by_date(start_date, end_date)

        # Assert
        assert len(available_cars) == 1
        assert available_cars[0].id == car1.id
