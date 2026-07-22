# Authentication & Authorization System (V1)

## Overview

Sistem auth menggunakan **JWT (HS256)** dengan dua tipe token: **access** (7 hari) dan **refresh** (30 hari). Role & permission dimapping **di code** (bukan di database) via file `constants/role_permissions.py`.

**Base URL auth:** `/api/v1/auth`  
**Header:** `Authorization: Bearer <token>`  
**Password hashing:** bcrypt via `passlib`

---

## Flow: Login → Protected Endpoint

```
POST /api/v1/auth/login
→ { access_token, refresh_token, token_type: "bearer" }

[Client menyimpan token]

GET /api/v1/<resource>   Authorization: Bearer <access_token>
→ [Dependency chain berjalan] → [Route handler]
```

### Dependency Chain

```
Request → OAuth2PasswordBearer (extract Bearer)
        → get_current_token_payload()   (decode JWT → TokenPayload)
          ├── Optional: RequirePermission(perm)  (check role→permissions, 403 if no)
          └── Optional: get_current_user()        (fetch User from DB by username)
```

---

## Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/api/v1/auth/login` | No | Login (form-encoded, OAuth2PasswordRequestForm) |
| `POST` | `/api/v1/auth/refresh` | No | Refresh token (body: `{ refresh_token }`) |
| `POST` | `/api/v1/auth/logout` | Yes | Logout (stateless) |
| `GET` | `/api/v1/auth/me` | Yes | Current user profile |

---

## Models

### `users` table
| Column | Type | Notes |
|--------|------|-------|
| id | Integer | PK |
| username | String(50) | Unique, index |
| email | String(100) | Unique, index |
| hashed_password | String(255) | bcrypt hash |
| full_name | String(100) | Nullable |
| is_active | Boolean | Default true |
| role_id | Integer | FK → roles.id |
| division_id | Integer | FK → divisions.id, nullable |

### `roles` table
| Column | Type | Notes |
|--------|------|-------|
| id | Integer | PK |
| name | String(50) | Unique, index (`ADMIN`, `STAFF`, `MANAGER`, `CREATIVE`) |
| description | String(255) | Nullable |

**Tidak ada** tabel `role_permissions` — mapping permssion ada di code.

---

## JWT Token

**Library:** `python-jose`  
**Algorithm:** `HS256`  
**Secret:** `settings.SECRET_KEY`

### Access Token
```json
{
  "sub": "username",
  "role": "ADMIN",
  "type": "access",
  "exp": <7 days from now>
}
```

### Refresh Token
```json
{
  "sub": "username",
  "role": "ADMIN",
  "type": "refresh",
  "exp": <30 days from now>
}
```

---

## Permission System

### Permission Definitions (`constants/permissions.py`)

```python
class Permission(str, Enum):
    DASHBOARD_VIEW = "dashboard.view"
    REPORT_VIEW = "report.view"
    REPORT_EXPORT = "report.export"
    USER_VIEW / CREATE / UPDATE / DELETE
    ROLE_VIEW
    INVENTORY_VIEW / CREATE / UPDATE / DELETE / EXPORT
    INVENTORY_TRANSACTION_VIEW / CREATE / EXPORT
    PRODUCT_VIEW / CREATE / UPDATE / DELETE / EXPORT / STOCK_OPNAME
    PRODUCT_MOVEMENT_VIEW / CREATE / UPDATE / DELETE
    PRODUCT_MASTER_VIEW / CREATE / UPDATE / DELETE
    CATEGORY_VIEW / CREATE / UPDATE / DELETE
    LOCATION_VIEW / CREATE / UPDATE / DELETE
    WORK_VIEW / CREATE / START / PAUSE / RESUME / CANCEL / FINISH
    WORK_EVIDENCE_UPLOAD / VIEW
    SHOWROOM_VIEW / CREATE / UPDATE
```

### Role → Permission Mapping (`constants/role_permissions.py`)

| Role | Granted Permissions |
|------|-------------------|
| **ADMIN** | **Semua** (50+ permissions) |
| **STAFF** | `DASHBOARD_VIEW`, `INVENTORY_VIEW`, `INVENTORY_TRANSACTION_VIEW/CREATE`, `PRODUCT_VIEW` |
| **CREATIVE** | Dashboard, inventory CRUD, product view, user view, report view, work full access, categories CRUD (~20 permissions) |
| **MANAGER** | **Tidak ada** — 0 permissions (kemungkinan belum selesai) |

### Enforcement (`dependencies/permission.py`)

```python
class RequirePermission:
    def __init__(self, permission):
        self.permission = permission

    def __call__(self, token_payload: TokenPayload = Depends(get_current_token_payload)):
        permissions = ROLE_PERMISSIONS.get(token_payload.role, set())
        if self.permission not in permissions:
            raise HTTPException(status_code=403, detail="Permission denied")
```

Digunakan di route dengan `Depends`:

```python
@router.get("/")
def list_users(..., _: TokenPayload = Depends(RequirePermission(Permission.USER_VIEW))):
    ...
```

Atau jika perlu `token_payload` atau `user` di handler:

```python
@router.get("/me")
def get_me(token_payload: TokenPayload = Depends(get_current_token_payload)):
    ...

@router.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    ...
```

---

## Dimana Permission Digunakan

~91 lokasi di route files:

| Route File | Permissions |
|------------|-------------|
| `api/users.py` | `ROLE_VIEW`, `USER_VIEW/CREATE/UPDATE/DELETE` |
| `api/inventory.py` | `INVENTORY_VIEW/CREATE/UPDATE/DELETE`, `INVENTORY_TRANSACTION_VIEW/CREATE` |
| `api/products.py` | `PRODUCT_VIEW/CREATE/UPDATE/DELETE` |
| `api/categories.py` | `CATEGORY_VIEW/CREATE/UPDATE/DELETE` |
| `api/locations.py` | `LOCATION_VIEW/CREATE/UPDATE/DELETE` |
| `api/product_master.py` | `PRODUCT_MASTER_VIEW/CREATE/UPDATE/DELETE` |
| `api/work_activities.py` | `WORK_VIEW/CREATE/START/PAUSE/RESUME/CANCEL/FINISH`, `WORK_EVIDENCE_UPLOAD/VIEW` |
| `api/dashboard.py` | `DASHBOARD_VIEW` |
| `api/reports.py` | `REPORT_VIEW` |
| `api/export.py` | `INVENTORY_EXPORT`, `PRODUCT_EXPORT`, `REPORT_EXPORT`, `INVENTORY_TRANSACTION_EXPORT` |

---

## Key Dependencies

| File | Function |
|------|----------|
| `dependencies/auth.py` | `get_current_token_payload()`, `get_current_user()` |
| `dependencies/permission.py` | `RequirePermission` class |
| `core/jwt.py` | `create_access_token()`, `create_refresh_token()`, `decode_access_token()` |
| `core/password.py` | `verify_password()`, `get_password_hash()` |
| `core/security.py` | `RoleChecker`, `PermissionChecker`, `OwnershipChecker` — **tidak dipakai** (dead code) |
| `constants/role.py` | `RoleType` enum |
| `constants/permissions.py` | `Permission` enum (50+ permissions) |
| `constants/role_permissions.py` | `ROLE_PERMISSIONS` dict (role → set of permissions) |
| `services/auth_service.py` | `authenticate_user()`, `refresh_token()` |
| `repositories/user_repository.py` | `get_by_username()`, `get_by_email()` |

---

## Keamanan — Catatan Penting

1. **Token type tidak divalidasi** di `get_current_token_payload()` — refresh token bisa dipakai sebagai access token
2. **Logout stateless** — token tetap valid sampai expire (7/30 hari)
3. **Role MANAGER punya 0 permission** — kemungkinan belum selesai diimplementasikan
4. **`RoleChecker`/`PermissionChecker`/`OwnershipChecker`** di `core/security.py` adalah dead code — mekanisme permission sebenarnya ada di `dependencies/permission.py`
5. **Tidak ada row-level access control** — selain filter `current_user.id` di reports

---

## Seed Data

| Script | Fungsi |
|--------|--------|
| `scripts/seed_roles.py` | Buat 4 role: ADMIN, MANAGER, STAFF, CREATIVE |
| `scripts/seed_admin.py` | Buat user admin: `adminsuper` / `password123` |

Tidak ada auto-seeding di startup — seed harus dijalankan manual.

---

## Activity & Audit Log

| Tabel | Model | Isi |
|-------|-------|-----|
| `activity_logs` | `ActivityLog` | Business events: LOGIN, EXPORT, APPROVE, DELETE |
| `audit_logs` | `AuditLog` | Data mutation: CREATE, UPDATE, DELETE (dengan old/new JSON) |

Endpoint: `GET /api/v1/logs/activity` dan `GET /api/v1/logs/audit` (read-only, any authenticated user).
