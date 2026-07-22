Project: Wadimor ERP

Backend:
- FastAPI
- SQLAlchemy ORM
- Repository Pattern
- Service Layer

Frontend:
- React
- Vite

Architecture:

Controller
↓

Service

↓

Repository

↓

Database

Rules:

Never change architecture.

Never introduce new libraries unless requested.

Never rename APIs.

Never change response schema.

Reuse existing utility functions.

Always check existing code before generating new code.

Prefer modifying existing files over creating new files.

Never touch docs unless explicitly requested.

Never touch migrations unless asked.

Always use dependency injection.

Always keep business logic in services.

Never put business logic inside API routes.

Generate concise code.

Avoid duplication.

Keep functions small.