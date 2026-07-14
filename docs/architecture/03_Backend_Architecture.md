# Backend Architecture

## 1. Overview
The CSMS Backend is a high-performance RESTful API developed using **FastAPI** (Python). It handles complex business logic, authorization, database transactions, and data aggregation for the frontend.

## 2. Technology Stack Deep-Dive
- **Framework:** FastAPI (ASGI framework utilizing Python type hints)
- **ORM:** SQLAlchemy (Handles database abstraction and SQL generation)
- **Migrations:** Alembic (Tracks and applies database schema changes)
- **Data Validation:** Pydantic (Validates incoming request bodies and serializes outgoing responses based on Python classes)
- **Database:** MySQL
- **Authentication:** JWT (JSON Web Tokens) generated using `python-jose` and password hashing with `passlib` (bcrypt).

## 3. Architecture Pattern: N-Tier / Layered
The backend strictly follows a layered architectural pattern to ensure separation of concerns, testability, and maintainability:

1. **API Layer (`app/api`):** FastAPI router endpoints. Handles HTTP requests, extracts parameters, delegates work to services, and formats the HTTP response.
2. **Service Layer (`app/services`):** Contains the core business logic. It orchestrates data movement between the database and the API, enforcing business rules (e.g., "Cannot start a workflow if another is active").
3. **Repository Layer (`app/repositories`):** Abstracts direct database interaction. Uses SQLAlchemy sessions to perform CRUD operations.
4. **Data Access Layer (`app/models`):** SQLAlchemy declarative base classes mapping directly to MySQL tables.

## 4. Directory Structure (`app/`)

```
app/
├── api/           # API Routers (Endpoints organized by domain e.g., users, inventory)
├── common/        # Shared utilities and enumerations
├── config/        # Configuration loader (CORS, Environment variables via Pydantic Settings)
├── constants/     # Global constants, error codes, defaults
├── core/          # Core infrastructure (Security, Lifespan events, Config definitions)
├── database/      # SQLAlchemy Engine and Session maker setup
├── dependencies/  # FastAPI dependency injection functions (e.g., get_db, get_current_user)
├── exceptions/    # Custom application exceptions and global handlers
├── middleware/    # ASGI Middlewares (LoggingMiddleware, RequestIDMiddleware)
├── models/        # SQLAlchemy ORM Models (Table schemas)
├── permissions/   # PBAC definitions and RBAC mapping logic
├── repositories/  # Database access classes encapsulating SQLAlchemy queries
├── schemas/       # Pydantic models for Request (In) and Response (Out) validation
├── services/      # Business logic controllers orchestrating repositories
├── static/        # Static files (if any are served by backend)
├── utils/         # Helper scripts (password hashing, time formatting)
└── main.py        # FastAPI Application instantiation and router inclusion
```

## 5. Key Design Choices
- **Dependency Injection:** Heavily utilizes FastAPI's `Depends()` system to inject database sessions (`get_db`) and authentication states (`get_current_active_user`) directly into route handlers. This makes unit testing incredibly easy by allowing dependency overrides.
- **Middleware Integration:**
  - `RequestIDMiddleware`: Injects a unique trace ID into every incoming request header for tracking logs across the system.
  - `LoggingMiddleware`: Logs request processing times and endpoints.
- **Global Exception Handling:** Custom exception (`CSMSException`) is caught by a global exception handler in `main.py` which standardizes the JSON error response sent to the frontend.

## 6. Database Migrations
**Alembic** manages the database schema evolution. The `migrations/` folder tracks revisions. When a model in `app/models/` is modified, an Alembic autogenerate command is used to create a migration script, ensuring the production MySQL database remains in sync with the codebase.

## 7. Testing Strategy
- The `tests/` directory is partitioned by scopes: `unit`, `integration`, `repositories`, `services`, `api`, `security`, and `performance`.
- Built heavily on `pytest`.
- Uses fixture injection (`conftest.py`) to provide mock database sessions, test clients (`TestClient` from FastAPI), and authenticated user tokens to test cases.
