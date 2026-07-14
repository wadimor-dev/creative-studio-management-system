# Login Credentials for Testing

The 401 Unauthorized error is now fixed. The backend authentication is working.

## Test Credentials

Use these credentials to log in to the frontend (http://localhost:5173):

**Username/Email:** `admin@studio.com`  
**Password:** `admin123`

This user has admin privileges.

## What Was Fixed

1. **ASGI Import Error** - Moved `main.py` into the `app` package
2. **CORS Configuration** - Fixed middleware order so CORS runs first
3. **Missing Dependencies** - Added `openpyxl` and `fpdf2` to requirements
4. **Bcrypt Compatibility** - Locked bcrypt to version <5.0 for passlib compatibility
5. **Test User Setup** - Created/updated admin user with known credentials

## How to Run

### Backend (FastAPI + Uvicorn)
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (Vite + React)
```bash
cd frontend
npm install
npm run dev
# Runs on http://localhost:5173
```

The backend API will be available at `http://localhost:8000/api/v1`

## API Endpoints

- **Login:** `POST /api/v1/auth/login` (expects form data with `username` and `password`)
- **Profile:** `GET /api/v1/auth/me` (requires Authorization header)
- **Refresh Token:** `POST /api/v1/auth/refresh`
- **Logout:** `POST /api/v1/auth/logout`

## Database

The app uses MySQL with the following configuration:
- **Host:** localhost
- **Database:** csms_db
- **User:** root
- **Password:** (empty)

Ensure MySQL is running and the database is created.

## Troubleshooting

If you get `ModuleNotFoundError` errors, ensure dependencies are installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

If you get bcrypt warnings, they can be safely ignored (functionality works fine).
