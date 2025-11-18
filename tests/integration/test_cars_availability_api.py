from datetime import date, timedelta


class TestCarsAvailabilityAPI:
    """Integration tests for cars availability by date endpoint."""

    def test_list_available_cars_by_date_no_bookings(self, client):
        """Test listing available cars when there are no bookings."""
        # Create some cars
        cars_data = [
            {
                "brand": "Toyota",
                "model": "Corolla",
                "year": 2023,
                "license_plate": "ABC-123",
                "daily_rate": 50.0,
            },
            {
                "brand": "Honda",
                "model": "Civic",
                "year": 2023,
                "license_plate": "XYZ-789",
                "daily_rate": 60.0,
            },
        ]

        for car_data in cars_data:
            client.post("/api/v1/cars", json=car_data)

        # Query available cars
        start_date = date.today() + timedelta(days=1)
        end_date = date.today() + timedelta(days=3)

        response = client.get(f"/api/v1/cars?start_date={start_date}&end_date={end_date}")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2  # Both cars available

    def test_list_available_cars_excludes_booked_cars(self, client):
        """Test that booked cars are excluded from available cars list."""
        # Create cars
        car1_response = client.post(
            "/api/v1/cars",
            json={
                "brand": "Toyota",
                "model": "Corolla",
                "year": 2023,
                "license_plate": "ABC-123",
                "daily_rate": 50.0,
            },
        )
        car1_id = car1_response.json()["id"]

        car2_response = client.post(
            "/api/v1/cars",
            json={
                "brand": "Honda",
                "model": "Civic",
                "year": 2023,
                "license_plate": "XYZ-789",
                "daily_rate": 60.0,
            },
        )
        car2_id = car2_response.json()["id"]

        # Book car1
        booking_data = {
            "car_id": car1_id,
            "customer_name": "John Doe",
            "customer_email": "john@example.com",
            "start_date": str(date.today() + timedelta(days=1)),
            "end_date": str(date.today() + timedelta(days=5)),
        }
        client.post("/api/v1/bookings", json=booking_data)

        # Query available cars for overlapping period
        start_date = date.today() + timedelta(days=2)
        end_date = date.today() + timedelta(days=4)

        response = client.get(f"/api/v1/cars?start_date={start_date}&end_date={end_date}")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1  # Only car2 available
        assert data[0]["id"] == car2_id

    def test_list_available_cars_cancelled_bookings_dont_block(self, client):
        """Test that cancelled bookings don't block car availability."""
        # Create a car
        car_response = client.post(
            "/api/v1/cars",
            json={
                "brand": "Toyota",
                "model": "Corolla",
                "year": 2023,
                "license_plate": "ABC-123",
                "daily_rate": 50.0,
            },
        )
        car_id = car_response.json()["id"]

        # Book and cancel
        booking_data = {
            "car_id": car_id,
            "customer_name": "John Doe",
            "customer_email": "john@example.com",
            "start_date": str(date.today() + timedelta(days=1)),
            "end_date": str(date.today() + timedelta(days=5)),
        }
        booking_response = client.post("/api/v1/bookings", json=booking_data)
        booking_id = booking_response.json()["id"]

        client.patch(f"/api/v1/bookings/{booking_id}/cancel")

        # Query available cars
        start_date = date.today() + timedelta(days=2)
        end_date = date.today() + timedelta(days=4)

        response = client.get(f"/api/v1/cars?start_date={start_date}&end_date={end_date}")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1  # Car is available again
        assert data[0]["id"] == car_id
