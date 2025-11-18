# 🚗 Car Rental API

A REST API for managing car rentals built with **FastAPI** following **Hexagonal Architecture (Ports & Adapters)** principles and **Test-Driven Development (TDD)**.

## 📋 Table of Contents

- [Design Choices](#design-choices)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Getting Started](#getting-started)
- [Running Tests](#running-tests)
- [API Documentation](#api-documentation)
- [Data Storage](#data-storage)
- [Logging](#logging)
- [Development Workflow](#development-workflow)

---

## 🎯 Design Choices

### Architecture: Hexagonal (Ports & Adapters)

**Why Hexagonal Architecture?**

1. **Separation of Concerns**: Business logic (domain) is completely isolated from infrastructure details
2. **Testability**: Pure domain logic can be tested without any infrastructure dependencies
3. **Flexibility**: Easy to swap implementations (e.g., JSON storage → PostgreSQL) without changing business logic
4. **Maintainability**: Clear boundaries between layers make the codebase easier to understand and modify

**Architecture Layers:**

```
┌─────────────────────────────────────────┐
│     Infrastructure Layer (Outside)      │
│  ┌─────────────────────────────────┐   │
│  │   API Layer (Primary Adapter)   │   │
│  │   - FastAPI Endpoints           │   │
│  │   - Request/Response Schemas    │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │      Domain Layer (Core)        │   │
│  │   - Entities (Car, Booking)     │   │
│  │   - Services (Business Logic)   │   │
│  │   - Ports (Interfaces)          │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  Adapters (Secondary Adapters)  │   │
│  │   - JSON Repository             │   │
│  │   - (Future: DB Repository)     │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

### Technology Stack

- **FastAPI**: High-performance async framework with automatic OpenAPI documentation
- **Pydantic**: Data validation and settings management
- **JSON Storage**: Simple file-based storage for MVP (easily replaceable)
- **Pytest**: Industry-standard testing framework
- **Docker**: Containerization for consistent environments

### TDD Approach

All features were developed following **Test-Driven Development**:

1. **RED** 🔴: Write failing tests first
2. **GREEN** 🟢: Write minimal code to pass tests
3. **REFACTOR** 🔵: Clean up and optimize

This ensures:
- High test coverage (84%+)
- Confidence in code changes
- Living documentation through tests

### Data Storage: JSON Files

**Why JSON for now?**

- **Simplicity**: No database setup required for development
- **Portability**: Easy to inspect and debug
- **Future-proof**: Thanks to Hexagonal Architecture, switching to PostgreSQL/MongoDB only requires:
  1. Creating a new repository adapter
  2. Implementing the same interface
  3. No changes to business logic!

---

## 📂 Project Structure

```
.
├── src/
│   ├── main.py                      # FastAPI application entry point
│   ├── config/
│   │   ├── settings.py              # Pydantic Settings
│   │   └── logging_config.py        # Logging configuration
│   ├── domain/                      # 🎯 CORE - Business Logic
│   │   ├── entities/
│   │   │   ├── car.py               # Car entity with validation
│   │   │   └── booking.py           # Booking entity with date validation
│   │   ├── services/
│   │   │   ├── car_service.py       # Car business logic
│   │   │   └── booking_service.py   # Booking business logic
│   │   └── ports/                   # Interfaces (Contracts)
│   │       ├── car_repository.py
│   │       └── booking_repository.py
│   └── infrastructure/              # 🔌 ADAPTERS
│       ├── adapters/
│       │   ├── json_car_repository.py      # JSON implementation
│       │   └── json_booking_repository.py  # JSON implementation
│       └── api/
│           ├── dependencies.py      # Dependency Injection
│           └── v1/                  # API version 1
│               ├── cars.py          # Car endpoints
│               ├── bookings.py      # Booking endpoints
│               └── schemas.py       # Request/Response models
├── tests/
│   ├── unit/                        # Domain logic tests (isolated)
│   │   └── test_booking_service.py
│   └── integration/                 # API endpoint tests
│       ├── test_bookings_api.py
│       └── test_cars_availability_api.py
├── data/                            # 💾 JSON storage directory
│   ├── cars.json                    # Car records
│   └── bookings.json                # Booking records
├── logs/                            # 📝 Application logs
│   └── app.log
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── pyproject.toml
```

---

## 🔧 Requirements

- **Docker** and **Docker Compose** (recommended)
- OR **Python 3.11+** (for local development without Docker)

---

## 🚀 Getting Started

### Option 1: Using Docker (Recommended)

1. **Clone the repository**

```bash
git clone <repository-url>
cd car-rentar
```

2. **Start the application**

```bash
docker-compose up --build -d
```

This will:
- Build the Docker image
- Start the API container
- Expose the API on `http://localhost:8000`

3. **Verify it's running**

```bash
curl http://localhost:8000/
```

Expected response:
```json
{
  "message": "Welcome to Car Rentar API",
  "version": "0.1.0",
  "docs": "/docs"
}
```

4. **View logs**

```bash
docker-compose logs -f api
```

5. **Stop the application**

```bash
docker-compose down
```

### Option 2: Local Development (Without Docker)

1. **Create a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Run the application**

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

4. **Access the API**

API: `http://localhost:8000`

---

## 🧪 Running Tests

### Using Docker (Recommended)

**Run all tests:**
```bash
docker-compose exec api pytest -v
```

**Run tests with coverage:**
```bash
docker-compose exec api pytest --cov=src --cov-report=term-missing
```

**Run specific test file:**
```bash
docker-compose exec api pytest tests/unit/test_booking_service.py -v
```

**Run integration tests only:**
```bash
docker-compose exec api pytest tests/integration/ -v
```

**Run unit tests only:**
```bash
docker-compose exec api pytest tests/unit/ -v
```

### Local Development

```bash
pytest -v
pytest --cov=src --cov-report=html  # Generates HTML coverage report
```

### Test Coverage

Current test coverage: **84%+**

- ✅ Unit tests for business logic (domain services)
- ✅ Integration tests for API endpoints
- ✅ Date availability logic
- ✅ Booking conflict detection
- ✅ Error handling

---

## 📚 API Documentation

Once the application is running, access the interactive API documentation:

### Swagger UI (Interactive)
**URL:** `http://localhost:8000/docs`

Features:
- Try out all endpoints
- See request/response schemas
- Test authentication flows

### ReDoc (Alternative)
**URL:** `http://localhost:8000/redoc`

### Available Endpoints

#### Cars

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/cars` | Create a new car |
| GET | `/api/v1/cars` | List all cars (with filters) |
| GET | `/api/v1/cars?start_date=2024-01-01&end_date=2024-01-05` | **List available cars for dates** |
| GET | `/api/v1/cars?available_only=true` | List cars with "available" status |
| GET | `/api/v1/cars/{car_id}` | Get car by ID |
| PATCH | `/api/v1/cars/{car_id}/status` | Update car status |
| DELETE | `/api/v1/cars/{car_id}` | Delete a car |

#### Bookings

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/bookings` | Create a booking |
| GET | `/api/v1/bookings/{booking_id}` | Get booking by ID |
| PATCH | `/api/v1/bookings/{booking_id}/cancel` | Cancel a booking |

### Example: Create a Car

```bash
curl -X POST http://localhost:8000/api/v1/cars \
  -H "Content-Type: application/json" \
  -d '{
    "brand": "Toyota",
    "model": "Corolla",
    "year": 2023,
    "license_plate": "ABC-1234",
    "daily_rate": 50.00
  }'
```

### Example: Create a Booking

```bash
curl -X POST http://localhost:8000/api/v1/bookings \
  -H "Content-Type: application/json" \
  -d '{
    "car_id": "<car-uuid>",
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "start_date": "2024-02-01",
    "end_date": "2024-02-05"
  }'
```

### Example: Query Available Cars by Date

```bash
curl "http://localhost:8000/api/v1/cars?start_date=2024-02-01&end_date=2024-02-05"
```

---

## 💾 Data Storage

### JSON Files Location

Data is stored in JSON files in the `data/` directory:

```
data/
├── cars.json       # All car records
└── bookings.json   # All booking records
```

### JSON Structure

**cars.json:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "brand": "Toyota",
    "model": "Corolla",
    "year": 2023,
    "license_plate": "ABC-1234",
    "daily_rate": 50.0,
    "status": "available",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": null
  }
]
```

**bookings.json:**
```json
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "car_id": "550e8400-e29b-41d4-a716-446655440000",
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "start_date": "2024-02-01",
    "end_date": "2024-02-05",
    "total_cost": 200.0,
    "status": "pending",
    "created_at": "2024-01-15T11:00:00",
    "updated_at": null
  }
]
```

### Data Persistence

- **Development**: Data persists in the local `data/` directory
- **Docker**: Data is stored inside the container (resets on `docker-compose down`)
  - To persist data, add a volume mount in `docker-compose.yml`

### Resetting Data

**Delete all data:**
```bash
rm data/*.json
```

Files will be recreated automatically on next API call.

---

## 📝 Logging

### Log Files

Logs are stored in:
```
logs/
└── app.log
```

### Log Format

```
2024-01-15 10:30:15,123 - src.infrastructure.api.v1.bookings - INFO - [BOOKING_ATTEMPT] Customer: John Doe (john@example.com) | Car ID: 550e8400... | Period: 2024-02-01 to 2024-02-05 | Days: 4
```

### Key Events Logged

#### Booking Events
- `[BOOKING_ATTEMPT]` - New booking request
- `[BOOKING_SUCCESS]` - Booking created successfully
- `[BOOKING_FAILED]` - Booking failed (with reason)
- `[BOOKING_CANCELLED]` - Booking cancelled
- `[BOOKING_ERROR]` - Unexpected errors

#### Car Availability Queries
- `[CARS_QUERY]` - Search for available cars
- `[CARS_QUERY_RESULT]` - Number of cars found

#### Car Management
- `[CAR_CREATE]` - New car added
- `[CAR_CREATED]` - Car successfully created
- `[CAR_STATUS_UPDATE]` - Status change attempt
- `[CAR_DELETED]` - Car removed

### View Logs

**Docker:**
```bash
docker-compose logs -f api
```

**Local file:**
```bash
tail -f logs/app.log
```

---

## 🛠️ Development Workflow

### Using Makefile (Shortcuts)

```bash
make help              # Show all available commands
make install           # Install dependencies
make pre-commit-install # Setup pre-commit hooks
make format            # Format code with black & isort
make lint              # Run linters (ruff, mypy)
make test              # Run tests
make docker-up         # Start Docker containers
make docker-down       # Stop Docker containers
make clean             # Clean cache files
```

### Code Quality

The project uses:
- **Black**: Code formatting
- **isort**: Import sorting
- **Ruff**: Fast Python linter
- **mypy**: Static type checking
- **pre-commit**: Git hooks for quality checks

---

## 🏗️ Future Improvements

1. **Database Migration**: Switch from JSON to PostgreSQL
   - Create `PostgreSQLCarRepository` implementing `CarRepository`
   - Update dependency injection
   - Zero changes to domain logic!

2. **Authentication**: Add JWT-based auth
3. **Rate Limiting**: Protect endpoints
4. **Caching**: Redis for availability queries
5. **Email Notifications**: Booking confirmations
6. **Payment Integration**: Process rental payments

---

## 📄 License

MIT

---

## 👨‍💻 Development Notes

For detailed development guidelines, see [AGENTS.md](./AGENTS.md) which includes:
- TDD workflow (Red → Green → Refactor)
- Git branching strategy
- Pre-commit setup
- Testing standards
