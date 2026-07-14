# CSMS Backend

Backend service for Creative Studio Management System.

---

# Technology

- Python 3.12+
- FastAPI
- SQLAlchemy
- Alembic
- MySQL
- JWT Authentication

---

# Folder Structure

```
app/

api/
common/
constants/
database/
dependencies/
exceptions/
middleware/
models/
permissions/
repositories/
schemas/
services/
utils/
```

---

# Running

## Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Mac/Linux

```bash
source venv/bin/activate
```

---

Install dependencies

```bash
pip install -r requirements.txt
```

---

Run

```bash
uvicorn app.main:app --reload
```

or

```bash
python run.py
```

---

# Environment

Create

```
.env
```

Example

```env
DATABASE_URL=mysql+pymysql://user:password@localhost/csms

SECRET_KEY=your-secret-key

ACCESS_TOKEN_EXPIRE_MINUTES=1440

ALGORITHM=HS256
```

---

# API Documentation

Swagger

```
/docs
```

ReDoc

```
/redoc
```

---

# Authentication

JWT Bearer Token

Authorization

```
Bearer <access_token>
```

---

# Permission System

The backend uses

Permission Based Access Control (PBAC) -> PROCEED DEV!

instead of direct role checking.

Example

```python
Depends(
    RequirePermission(
        Permission.INVENTORY_VIEW
    )
)
```

Permissions are mapped inside

```
ROLE_PERMISSIONS
```

---

# Main Modules

Dashboard

Inventory

Products

Reports

Users

Export

Authentication

---

# Coding Standard

Architecture

```
Router

↓

Service

↓

Repository

↓

Database
```

Business logic should remain inside Services.

Repositories should only access the database.

Routers should only receive requests and return responses.