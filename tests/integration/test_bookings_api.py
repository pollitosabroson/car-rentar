from datetime import date, timedelta


class TestBookingsAPI:
    """Integration tests for bookings API endpoints."""

    def test_create_booking_success(self, client):
        """Test successful booking creation through API."""
        # First, create a car
        car_data = {
            "brand": "Toyota",
            "model": "Corolla",
            "year": 2023,
            "license_plate": "ABC-123",
            "daily_rate": 50.0,
        }
        car_response = client.post("/api/v1/cars", json=car_data)
        assert car_response.status_code == 201
        car_id = car_response.json()["id"]

        # Now create a booking
        booking_data = {
            "car_id": car_id,
            "customer_name": "John Doe",
            "customer_email": "john@example.com",
            "start_date": str(date.today() + timedelta(days=1)),
            "end_date": str(date.today() + timedelta(days=3)),
        }

        response = client.post("/api/v1/bookings", json=booking_data)

        assert response.status_code == 201
        data = response.json()
        assert data["car_id"] == car_id
        assert data["customer_name"] == "John Doe"
        assert data["total_cost"] == 100.0  # 2 days * 50.0
        assert data["status"] == "pending"

    def test_create_booking_car_not_found(self, client):
        """Test booking creation fails when car doesn't exist."""
        booking_data = {
            "car_id": "00000000-0000-0000-0000-000000000000",
            "customer_name": "John Doe",
            "customer_email": "john@example.com",
            "start_date": str(date.today() + timedelta(days=1)),
            "end_date": str(date.today() + timedelta(days=3)),
        }

        response = client.post("/api/v1/bookings", json=booking_data)

        assert response.status_code == 400
        assert "Car not found" in response.json()["detail"]

    def test_create_booking_conflicting_dates(self, client):
        """Test booking creation fails when dates conflict with existing booking."""
        # Create a car
        car_data = {
            "brand": "Toyota",
            "model": "Corolla",
            "year": 2023,
            "license_plate": "ABC-123",
            "daily_rate": 50.0,
        }
        car_response = client.post("/api/v1/cars", json=car_data)
        car_id = car_response.json()["id"]

        # Create first booking
        booking1_data = {
            "car_id": car_id,
            "customer_name": "John Doe",
            "customer_email": "john@example.com",
            "start_date": str(date.today() + timedelta(days=1)),
            "end_date": str(date.today() + timedelta(days=5)),
        }
        client.post("/api/v1/bookings", json=booking1_data)

        # Try to create conflicting booking
        booking2_data = {
            "car_id": car_id,
            "customer_name": "Jane Doe",
            "customer_email": "jane@example.com",
            "start_date": str(date.today() + timedelta(days=3)),
            "end_date": str(date.today() + timedelta(days=7)),
        }

        response = client.post("/api/v1/bookings", json=booking2_data)

        assert response.status_code == 400
        assert "not available" in response.json()["detail"]

    def test_get_booking(self, client):
        """Test retrieving a booking by ID."""
        # Create car and booking
        car_data = {
            "brand": "Toyota",
            "model": "Corolla",
            "year": 2023,
            "license_plate": "ABC-123",
            "daily_rate": 50.0,
        }
        car_response = client.post("/api/v1/cars", json=car_data)
        car_id = car_response.json()["id"]

        booking_data = {
            "car_id": car_id,
            "customer_name": "John Doe",
            "customer_email": "john@example.com",
            "start_date": str(date.today() + timedelta(days=1)),
            "end_date": str(date.today() + timedelta(days=3)),
        }
        create_response = client.post("/api/v1/bookings", json=booking_data)
        booking_id = create_response.json()["id"]

        # Get booking
        response = client.get(f"/api/v1/bookings/{booking_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == booking_id
        assert data["customer_name"] == "John Doe"

    def test_cancel_booking(self, client):
        """Test cancelling a booking."""
        # Create car and booking
        car_data = {
            "brand": "Toyota",
            "model": "Corolla",
            "year": 2023,
            "license_plate": "ABC-123",
            "daily_rate": 50.0,
        }
        car_response = client.post("/api/v1/cars", json=car_data)
        car_id = car_response.json()["id"]

        booking_data = {
            "car_id": car_id,
            "customer_name": "John Doe",
            "customer_email": "john@example.com",
            "start_date": str(date.today() + timedelta(days=1)),
            "end_date": str(date.today() + timedelta(days=3)),
        }
        create_response = client.post("/api/v1/bookings", json=booking_data)
        booking_id = create_response.json()["id"]

        # Cancel booking
        response = client.patch(f"/api/v1/bookings/{booking_id}/cancel")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "cancelled"
