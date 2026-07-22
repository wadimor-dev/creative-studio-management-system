# Rencana Refactor Authentication & Authorization System V2

**Status:** Draft — belum diimplementasi  
**Tujuan:** Hardcoded → Database-driven, Single Role → Multi Role, Stateless Refresh → DB Sessions

---

## Ringkasan Perubahan

| # | Poin | Perubahan | Dampak Backend | Dampak Frontend |
|---|------|-----------|----------------|-----------------|
| 1 | **Permissions di DB** | `ROLE_PERMISSIONS` → `permissions` + `role_permissions` tabel | ~20 files | Tidak ada |
| 2 | **Multi Role** | `users.role_id` FK → `user_roles` (many-to-many) | ~15 files | Role display components |
| 3 | **Role tidak di JWT** | `{role, sub, type, exp}` → `{sub, session_id, type, exp}` | ~15 files | Tidak ada |
| 4 | **sub=user_id** | `sub=username` → `sub=user_id` | ~10 files | Tidak ada |
| 5 | **Session DB** | Refresh token stateless → `user_sessions` tabel | auth_service, jwt, login/logout | refresh token logic |
| 6 | **Token Type Validation** | Validasi `type == "access"` di access token | 1 file (dependencies/auth.py) | Tidak ada |
| 7 | **Permission Namespace** | Naming convention, tidak ada refactor massal | 0 files (sudah dot-notation) | Tidak ada |
| 8 | **MANAGER role** | Tambah permission set untuk MANAGER | 1 file | Tidak ada |
| 9 | **Audit Global** | Standardisasi `audit_logs` dengan `module` field | ~5 files + migration | Tidak ada |
| 10 | **Ownership/Branch Checker** | Implementasi bertahap | ~5 files baru | Tidak ada |

---

## 1. Permissions di Database

### Saat Ini

```python
# constants/permissions.py (enum)
class Permission(str, Enum):
    PRODUCT_VIEW = "product.view"
    ...

# constants/role_permissions.py (hardcoded mapping)
ROLE_PERMISSIONS = {
    RoleType.ADMIN: { Permission.PRODUCT_VIEW, ... },
    RoleType.STAFF: { Permission.PRODUCT_VIEW },
}
```

### Target

```python
# Permission enum tetap ada sebagai source untuk seed
class Permission(str, Enum):
    PRODUCT_VIEW = "product.view"
```

Tapi mapping ada di database:

```
permissions              role_permissions           roles
+---------------+        +------------------+       +-----------+
| id (PK)       | <----+ | permission_id    |   +-> | id (PK)   |
| code (UNIQUE) |        | role_id          | --+   | name      |
| name          |        | PK(permission_id,|       | desc      |
| module        |        |     role_id)     |       +-----------+
| description   |        +------------------+
+---------------+
```

### Startup Sync

Di `main.py` atau `lifespan`:

```python
@app.on_event("startup")
async def sync_permissions():
    # Loop Permission enum
    #   if code not in DB → INSERT
    #   if code in DB → UPDATE name/description
    #   if code in DB but not in enum → jangan dihapus (custom permission)
```

Enum hanya menjadi **seed** — bukan sumber utama. Admin bisa tambah permission baru via halaman admin tanpa deploy.

### Migration

Migration baru `009_baru_permissions_tables`:

```python
def upgrade():
    op.create_table('permissions', ...)
    op.create_table('role_permissions', ...)
    # Seed data: INSERT Permission enum values ke permissions
    # Seed data: INSERT role_permissions dari ROLE_PERMISSIONS
```

Migration sebelumnya (`003c3d4e5f60`) membuat `showroom_permissions`, `showroom_roles`, `showroom_role_permissions`, `showroom_user_roles` — tabel itu sudah di-drop di `008f8a607185`. Jadi nama `permissions` dan `role_permissions` sekarang **available**.

**PENTING:** Tabel `showroom_roles` dulu dibuat untuk Showroom-specific role. Sekarang `roles` (tanpa prefix) adalah tabel global. Kita akan pakai `permissions` dan `role_permissions` (tanpa prefix) sebagai tabel global.

### Rename Existing `roles` Table

Tabel `roles` sekarang dipakai untuk role global. Ini OK — kita tambah kolom `is_system = Boolean(default=True)` untuk menandai role yang tidak bisa dihapus via UI.

Tabel `role_permissions` baru (role_id → permission_id) menggantikan `ROLE_PERMISSIONS` dict.

### Files yang Berubah

| File | Perubahan |
|------|-----------|
| `constants/permissions.py` | Tetap sebagai enum, tambah `module` annotation |
| `constants/role_permissions.py` | HAPUS — pindah ke startup sync |
| `constants/role.py` | TETAP (referensi role seed) |
| `models/role.py` | Tambah `is_system` column |
| `models/permission.py` | **BARU** — model `Permission` (tabel `permissions`) |
| `models/role_permission.py` | **BARU** — model `RolePermission` (tabel `role_permissions`) |
| `dependencies/permission.py` | Query DB bukan `ROLE_PERMISSIONS` dict |
| `core/lifespan.py` (atau main.py) | Startup sync: Permission enum → DB |
| `services/seed_service.py` atau `scripts/seed_permissions.py` | Sync logic |
| `routes/api/admin/permissions.py` | **BARU** — CRUD permissions untuk admin |
| `routes/api/admin/roles.py` | **BARU** — CRUD roles + role_permissions |
| `schemas/permission.py` | **BARU** |
| `schemas/role.py` | Update untuk role_permissions |
| `repositories/permission_repository.py` | **BARU** |
| `repositories/role_repository.py` | Update |

---

## 2. Multi Role (Many-to-Many Users ↔ Roles)

### Saat Ini

```python
class User(Base):
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    role = relationship("Role")
```

### Target

```python
user_roles
+------------------+
| user_id (FK)     | PK
| role_id (FK)     | PK
+------------------+
```

```python
class User(Base):
    # role_id dihapus
    roles = relationship("Role", secondary="user_roles")
```

### Migration

```python
def upgrade():
    op.create_table('user_roles',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), primary_key=True),
        sa.Column('role_id', sa.Integer(), sa.ForeignKey('roles.id'), primary_key=True),
    )
    # Migrate existing data
    # INSERT INTO user_roles (user_id, role_id) SELECT id, role_id FROM users
    # Drop column role_id from users
    op.drop_column('users', 'role_id')
```

### Files yang Berubah

| File | Perubahan |
|------|-----------|
| `models/user.py` | Hapus `role_id` FK, tambah `roles = relationship(..., secondary="user_roles")` |
| `models/user_role.py` | **BARU** — model `UserRole` |
| `schemas/user.py` | `role_id: int` → `role_ids: list[int]` di UserCreate/UserUpdate |
| `schemas/user.py` | `role: Optional[RoleResponse]` → `roles: list[RoleResponse]` |
| `services/user_service.py` | Create/Update user: handle list of role_ids |
| `services/auth_service.py` | Login: ambil roles dari DB (bisa jadi lebih dari 1) |
| `repositories/user_repository.py` | Tidak perlu banyak berubah |
| `api/users.py` | Validasi role_ids input |
| `frontend/...` | User form: single role dropdown → multi-select/checkbox |
| `frontend/src/utils/permissions.js` | `user.role` → `user.roles` (plural, array) |

### Frontend Impact

`AuthContext.jsx`:
```js
// Sebelum
user.role.name  // single role

// Sesudah
user.roles      // array of Role objects
```

`permissions.js`:
```js
// Sebelum
export const hasPermission = (user, feature) => {
  return FEATURE_ROLES[feature]?.includes(user.role?.name);
};

// Sesudah
export const hasPermission = (user, feature) => {
  return user.roles?.some(role => 
    FEATURE_ROLES[feature]?.includes(role.name)
  );
};
```

---

## 3. Role Tidak Disimpan di JWT

### Saat Ini

```python
# jwt.py
to_encode = {
    "exp": expire,
    "sub": str(subject),    # username
    "role": role,           # "ADMIN"
    "type": "access"
}
```

### Target

```python
to_encode = {
    "exp": expire,
    "sub": str(user_id),    # user_id (integer)
    "session_id": session_uuid,
    "type": "access"        # Wajib validasi
}
```

### Alur Request dengan Role dari DB

```
Request → get_current_token_payload()
           → decode JWT → {sub, session_id, type, exp}
           → Validasi type == "access"
           → return TokenPayload(user_id, session_id)

Jika route butuh permission check:
           → RequirePermission("product.view")
              → get_user_permissions(db, user_id)
                 → JOIN user_roles → role_permissions → permissions
              → Cek apakah permission ada di set
              → return atau HTTP 403
```

### Perf Consideration

Setiap request → query DB untuk ambil permissions. Solusi:
1. **Per-request cache:** Simpan di `request.state.permissions` setelah query pertama
2. **Redis** (future): Cache user permissions dengan TTL 5 menit
3. Di FastAPI bisa pakai `request.scope` atau custom dependency

```python
# Di dependencies/permission.py
class RequirePermission:
    async def __call__(self, request: Request, db: Session = Depends(get_db), 
                       token_payload = Depends(get_current_token_payload)):
        # Cek request-scoped cache
        if not hasattr(request.state, 'permissions'):
            request.state.permissions = get_user_permissions(db, token_payload.sub)
        if self.permission not in request.state.permissions:
            raise HTTPException(403, "Permission denied")
```

### Files yang Berubah

| File | Perubahan |
|------|-----------|
| `core/jwt.py` | Hapus `role` dari payload, tambah `session_id` |
| `dependencies/auth.py` | `get_current_token_payload()` hapus role validation |
| `dependencies/permission.py` | `RequirePermission` query DB, bukan `ROLE_PERMISSIONS[token_payload.role]` |
| `schemas/auth.py` | `TokenPayload`: `sub` → int, `role` hapus, tambah `session_id` |
| `services/auth_service.py` | Hapus `role` dari create_access_token call |
| `services/user_service.py` | Tidak perlu role |
| Semua route yang pakai `token_payload.role` | Ganti logika |

---

## 4. sub = user_id (Bukan Username)

### Saat Ini

```python
# jwt.py
to_encode["sub"] = str(subject)  # username

# services/auth_service.py
access_token = create_access_token(subject=user.username, role=role_name)
```

### Target

```python
access_token = create_access_token(subject=user.id, session_id=session.uuid)
```

### Files yang Berubah

| File | Perubahan |
|------|-----------|
| `services/auth_service.py` | `subject=user.id` |
| `dependencies/auth.py` | `get_current_user()`: pakai `user_repo.get_by_id(db, token_payload.sub)` bukan `get_by_username` |
| `api/auth.py` | `get_current_user()` endpoint: pakai `user_repo.get_by_id(db, token_payload.sub)` |
| `api/users.py` | `get_profile()`: pakai `user_repo.get_by_id(db, token_payload.sub)` |
| Semua route yang pakai `token_payload.sub` sebagai username | Ganti lookup |

---

## 5. Session Database (Refresh Token)

### Saat Ini

- Refresh token adalah JWT stateless (30 hari expire)
- Logout hanya hapus token dari localStorage
- Token curian tetap valid sampai expire

### Target

```
user_sessions
+------------------+
| id (PK)          |
| user_id (FK)     |
| refresh_token    | hash dari refresh token
| device           |
| ip_address       |
| user_agent       |
| created_at       |
| expired_at       |
| last_used_at     |
| revoked_at       |
| is_revoked       | Boolean default false
+------------------+
```

### Alur Login Baru

```
POST /auth/login
  → AuthService.authenticate_user(db, form_data)
    → Verify password
    → Create session:
        session = UserSession(user_id=user.id, refresh_token=hash(token), 
                              ip=..., user_agent=..., expired_at=now+30days)
    → Create access_token(sub=user.id, session_id=session.id, type="access")
    → Create refresh_token_jwt(sub=user.id, session_id=session.id, type="refresh")
    → Return { access_token, refresh_token }
```

### Alur Refresh Baru

```
POST /auth/refresh  { refresh_token }
  → AuthService.refresh_token(db, refresh_token)
    → Decode JWT → payload
    → Validasi type == "refresh"
    → Hash refresh_token dari request
    → Cari session: refresh_token_hash == hash
    → Cek: is_revoked? expired?
    → Rotate session:
        session.refresh_token = hash(new_token)
        session.last_used_at = now()
    → Create NEW access_token + refresh_token
    → Return { access_token, refresh_token }
```

### Alur Logout Baru

```
POST /auth/logout  Authorization: Bearer <access_token>
  → Decode access_token → { session_id, sub }
  → UserSession.where(id=session_id).update(is_revoked=True)
  → Return "Logout successful"
```

Logout juga bisa revoke ALL sessions user:
```
POST /auth/logout/all
  → UserSession.where(user_id=sub, is_revoked=False).update(is_revoked=True)
```

### Files yang Berubah

| File | Perubahan |
|------|-----------|
| `models/user_session.py` | **BARU** — model `UserSession` |
| `schemas/auth.py` | Update untuk session |
| `services/auth_service.py` | Implementasi session logic |
| `services/session_service.py` | **BARU** — create/revoke/validate session |
| `repositories/session_repository.py` | **BARU** |
| `dependencies/auth.py` | Optional: validasi session masih aktif |
| `api/auth.py` | Logout endpoint sekarang revoke session |
| `frontend/src/...` | Tambah refresh token logic di interceptor |

### Frontend Impact: Auto Refresh Token

`interceptors.js` perlu logic retry:

```js
// Saat ini: on 401 → clear token → redirect login
// Baru: on 401 → try refresh → retry original request
//        if refresh fails → clear session → redirect login
```

---

## 6. Token Type Validation

### Saat Ini

```python
# dependencies/auth.py
def get_current_token_payload(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    token_data = TokenPayload(**payload)
    # ❌ Tidak ada validasi type
    return token_data
```

### Target

```python
def get_current_token_payload(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid token type")
    token_data = TokenPayload(**payload)
    return token_data
```

Demikian juga di refresh endpoint:

```python
def refresh_token(db, refresh_token):
    payload = decode_access_token(refresh_token)
    if payload.get("type") != "refresh":
        raise CSMSException("Invalid token type", status_code=401)
```

### Files yang Berubah

| File | Perubahan |
|------|-----------|
| `dependencies/auth.py` | Tambah validasi `type == "access"` |
| `services/auth_service.py` | `refresh_token()` — validasi `type == "refresh"` (SUDAH ADA) |

Note: `auth_service.refresh_token()` sudah memvalidasi `type == "refresh"`. Yang belum adalah `get_current_token_payload()` untuk access token.

---

## 7. Permission Namespace

### Saat Ini

Sudah dot-notation: `"dashboard.view"`, `"product.view"`, `"showroom.view"`

### Target

Lebih granular dengan module prefix (+ `:` untuk action):

```
showroom.view                  → showroom:view
showroom.stock.read            → showroom:stock.read
showroom.stock.update          → showroom:stock.update
showroom.borrow.create         → showroom:borrow.create
showroom.borrow.return         → showroom:borrow.return
clinic.patient.read            → clinic:patient.read
hr.employee.read                → hr:employee.read
finance.invoice.approve         → finance:invoice.approve
```

**Format:** `module:entity.action`

Ini hanya **renaming** — tidak ada perubahan struktural. Dilakukan setelah poin 1-6 selesai agar tidak tumpang tindih.

---

## 8. MANAGER Role — Isi Permission

### Saat Ini

```python
ROLE_PERMISSIONS = {
    RoleType.MANAGER: set(),  # ❌ Kosong
}
```

### Target

```python
ROLE_PERMISSIONS = {
    RoleType.MANAGER: {
        Permission.DASHBOARD_VIEW,
        Permission.REPORT_VIEW,
        Permission.REPORT_EXPORT,
        Permission.INVENTORY_VIEW,
        Permission.INVENTORY_TRANSACTION_VIEW,
        Permission.PRODUCT_VIEW,
        Permission.PRODUCT_MOVEMENT_VIEW,
        Permission.SHOWROOM_VIEW,
        # Read-only untuk semua module
    },
}
```

Dengan poin 1 (DB-driven), MANAGER bisa diatur permission-nya via halaman admin.

---

## 9. Audit Log Global

### Saat Ini

Dua sistem audit berjalan paralel:

```
activity_logs (global)          showroom_activity_log (showroom-specific)
+---------------------+         +---------------------------+
| id                  |         | id                        |
| user_id             |         | actor_id                  |
| action_type         |         | action                    |
| description         |         | entity_type               |
| ip_address          |         | entity_id                 |
| user_agent          |         | actor_type                |
| created_at          |         | request_id                |
+---------------------+         | idempotency_key           |
                                | detail (≈description)     |
audit_logs (global)             | old_value                 |
+---------------------+         | new_value                 |
| id                  |         | created_at                |
| user_id             |         +---------------------------+
| table_name          |
| record_id           |
| action              |
| old_value (JSON)    |
| new_value (JSON)    |
| created_at          |
+---------------------+
```

### Target

Gabung menjadi satu sistem global dengan `module` field:

```
audit_logs (baru — unified)
+---------------------+
| id                  |
| user_id             |
| module              | "showroom", "inventory", "clinic", etc.
| entity_type         | "borrowing", "stock", "movement", etc. (≈ table_name atau entity_type)
| entity_id           |
| action              | CREATE, UPDATE, DELETE, LOGIN, EXPORT, APPROVE
| description         | Human-readable
| old_value (JSON)    |
| new_value (JSON)    |
| ip_address          |
| user_agent          |
| created_at          |
+---------------------+
```

### Migration

```python
def upgrade():
    # Migrasi showroom_activity_log → audit_logs
    # INSERT INTO audit_logs (module='showroom', entity_type, entity_id, action, ...)
    # SELECT dari showroom_activity_log
    
    # Migrasi activity_logs → audit_logs
    # INSERT INTO audit_logs (module='core', entity_type='activity', ...)
    
    # Migrasi audit_logs eksisting → audit_logs baru
    # INSERT INTO audit_logs (module='core', entity_type=table_name, ...)
    
    # Drop old tables
    op.drop_table('showroom_activity_log')
    op.drop_table('activity_logs')
    op.drop_table('audit_logs')
```

### Showroom `log_activity()` → Global Logger

```python
# showroom_v2/services/base.py
from app.services.logger_service import LoggerService

def log_activity(db, action, entity_type, entity_id, user_id, **kwargs):
    LoggerService.log_event(
        db=db, user_id=user_id, module="showroom",
        entity_type=entity_type, entity_id=entity_id,
        action=action, **kwargs
    )
```

---

## 10. Ownership & Branch Checker

### Saat Ini

```python
# core/security.py (DEAD CODE — tidak dipakai)
class OwnershipChecker:
    @staticmethod
    def is_owner(current_user_id, resource_owner_id):
        return str(current_user_id) == str(resource_owner_id)

class RoleChecker:
    @staticmethod
    def is_allowed(current_role, allowed_roles):
        return current_role in allowed_roles
```

### Arsitektur Tujuan (3 Layer)

```
┌─────────────────────────────────────────────────┐
│                  LAYER 1: IDENTITY              │
│  Users | Sessions | JWT | Authentication        │
├─────────────────────────────────────────────────┤
│                  LAYER 2: AUTHORIZATION          │
│  Roles | Permissions | UserRoles | RolePerms    │
├─────────────────────────────────────────────────┤
│                  LAYER 3: ACCESS CONTROL         │
│  ┌─────────────┐  ┌─────────────┐               │
│  │Permission   │  │Ownership    │               │
│  │Check        │  │Check        │               │
│  └─────────────┘  └─────────────┘               │
│  ┌─────────────┐  ┌─────────────┐               │
│  │Branch       │  │Department   │               │
│  │Check        │  │Check        │               │
│  └─────────────┘  └─────────────┘               │
│  ┌─────────────┐  ┌─────────────┐               │
│  │Module       │  │Future...    │               │
│  │Check        │  │             │               │
│  └─────────────┘  └─────────────┘               │
└─────────────────────────────────────────────────┘
```

### Layer 3 — Access Control Dependencies

```python
# dependencies/access_control.py

class RequirePermission:
    """Layer 3a: Cek apakah user punya permission tertentu"""
    def __init__(self, permission: str): ...

class OwnershipChecker:
    """Layer 3b: Cek apakah user adalah pemilik resource
    
    Contoh: Dokter A hanya bisa lihat Medical Record pasien sendiri.
    """
    def __init__(self, get_owner_id: Callable): ...

class BranchChecker:
    """Layer 3c: Cek apakah user dalam cabang yang sama dengan resource
    
    Contoh: Staff Cabang Solo hanya bisa akses inventory Cabang Solo.
    """
    def __init__(self, get_branch_id: Callable): ...

class DepartmentChecker:
    """Layer 3d: Cek apakah user dalam departemen yang sama"""
    def __init__(self, get_dept_id: Callable): ...

class ModuleChecker:
    """Layer 3e: Cek apakah user punya akses ke module tertentu
    
    Sederhana — cek apakah user punya minimal 1 permission di module itu.
    """
    def __init__(self, module: str): ...
```

### Contoh Penggunaan (Future)

```python
@router.get("/borrowings/{id}")
def get_borrowing(
    id: int,
    db: Session = Depends(get_db),
    _: None = Depends(RequirePermission("showroom:borrow.read")),
    # Staff hanya bisa lihat borrowing sendiri
    borrowing: ShowroomBorrowing = Depends(OwnershipChecker(
        lambda db, id: db.query(ShowroomBorrowing).get(id).created_by_id
    )),
):
    ...
```

### Implementasi Awal

Untuk tahap ini, implementasi **bertahap**:

1. **Phase 1** (sekarang): `RequirePermission` dari DB (poin 1)
2. **Phase 2** (setelah poin 1-9): `OwnershipChecker` untuk modul yang perlu
3. **Phase 3** (future): `BranchChecker`, `DepartmentChecker`, `ModuleChecker`

---

## Migration Strategy

### Database Migration Plan

1. **Migration A: `role_permissions` tables**
   - Buat `permissions` table
   - Buat `role_permissions` table  
   - Seed Permission enum values
   - Seed role_permissions dari ROLE_PERMISSIONS

2. **Migration B: `user_sessions` table**
   - Buat `user_sessions` table
   - Tidak ada data migration (session baru mulai dari 0)

3. **Migration C: `user_roles` table**
   - Buat `user_roles` table
   - Migrate data: INSERT INTO user_roles SELECT id, role_id FROM users
   - Drop `users.role_id`

4. **Migration D: Unified `audit_logs` table**
   - Buat `audit_logs_v2` table (dengan `module`, `entity_type`)
   - Migrate data dari `activity_logs`, `audit_logs`, `showroom_activity_log`
   - Drop old tables, rename new table

### Order Implementasi

```
Phase 1 (Backend Infrastructure):
  ├── Migration A: permissions + role_permissions tables
  ├── Model Permission, RolePermission
  ├── Startup sync Permission enum → DB
  ├── RequirePermission query DB (dengan per-request cache)
  └── CRUD routes: /admin/permissions, /admin/roles
  
Phase 2 (Multi Role + Sessions):
  ├── Migration B: user_sessions table
  ├── Migration C: user_roles table (many-to-many)
  ├── Update User model: hapus role_id, tambah roles relationship
  ├── Update UserService: handle role_ids list
  ├── Update AuthService: DB sessions, hapus role dari JWT, sub=user_id
  ├── Update JWT: {sub=user_id, session_id, type, exp}
  ├── Token type validation di get_current_token_payload
  └── Update /auth/login, /auth/refresh, /auth/logout

Phase 3 (Frontend):
  ├── AuthContext: user.roles (array) bukan user.role
  ├── permissions.js: hasPermission cek array roles
  ├── User form: single role → multi-select
  ├── Auth interceptor: tambah refresh logic (on 401 → refresh → retry)
  └── Sidebar: update role checking

Phase 4 (MANAGER + Audit):
  ├── Isi permission MANAGER
  ├── Migration D: unified audit_logs
  ├── Update LoggerService
  └── Hapus ShowroomActivityLog model

Phase 5 (Access Control):
  ├── OwnershipChecker
  ├── BranchChecker (basic)
  └── DepartmentChecker (basic)
```

---

## File Impact Summary

### Files to CREATE (13 files)

| # | File | Isi |
|---|------|-----|
| 1 | `models/permission.py` | `Permission` model (table `permissions`) |
| 2 | `models/role_permission.py` | `RolePermission` model (table `role_permissions`) |
| 3 | `models/user_role.py` | `UserRole` model (table `user_roles`) |
| 4 | `models/user_session.py` | `UserSession` model (table `user_sessions`) |
| 5 | `schemas/permission.py` | Pydantic schemas untuk Permission |
| 6 | `schemas/user_session.py` | Pydantic schemas untuk UserSession |
| 7 | `repositories/permission_repository.py` | DB queries untuk Permission |
| 8 | `repositories/session_repository.py` | DB queries untuk UserSession |
| 9 | `services/seed_service.py` | Startup sync Permission enum → DB |
| 10 | `services/session_service.py` | Create/validate/revoke sessions |
| 11 | `dependencies/access_control.py` | OwnershipChecker, BranchChecker, dll |
| 12 | `routes/api/admin/__init__.py` | Admin-only routes package |
| 13 | `routes/api/admin/permissions.py` | CRUD permissions |
| 14 | `routes/api/admin/roles.py` | CRUD roles + role_permissions assignment |

### Files to MODIFY (25+ files)

| File | Perubahan |
|------|-----------|
| `models/__init__.py` | Import model baru |
| `models/user.py` | Hapus `role_id`, tambah `roles` relationship |
| `models/role.py` | Tambah `is_system`, `permissions` relationship |
| `schemas/auth.py` | TokenPayload: sub → int, role hapus, session_id tambah |
| `schemas/user.py` | `role_id` → `role_ids: list[int]`, `role` → `roles` |
| `schemas/role.py` | Tambah `permissions: list[PermissionResponse]` |
| `core/jwt.py` | Hapus `role`, tambah `session_id` |
| `core/security.py` | HAPUS (pindah ke dependencies/access_control.py) |
| `dependencies/auth.py` | Validasi type, get_user pakai get_by_id |
| `dependencies/permission.py` | Query DB, per-request cache |
| `services/auth_service.py` | Sessions, multi-role, user_id |
| `services/user_service.py` | Handle role_ids list |
| `repositories/role_repository.py` | Tambah get_by_name, get_with_permissions |
| `repositories/user_repository.py` | Tambah get_by_id_with_roles |
| `constants/role_permissions.py` | HAPUS (pindah ke seed + DB) |
| `constants/permissions.py` | Tambah `module` annotation, tambah MANAGER perms |
| `constants/role.py` | Optional: tambah helper method |
| `main.py` | + lifespan startup sync, + admin router |
| `api/auth.py` | Session-based logout, profile pake user_id |
| `api/users.py` | Multi-role input/output |
| `services/logger_service.py` | Update untuk unified audit_logs |
| `modules/showroom_v2/services/base.py` | Pakai global logger |

### Files to DELETE (4 files)

| File | Alasan |
|------|--------|
| `constants/role_permissions.py` | Pindah ke DB |
| `core/security.py` | Dead code / pindah ke dependencies/access_control.py |
| `models/showroom_activity_log.py` | Migrasi ke unified audit_logs |
| `modules/showroom_v2/services/base.py` (log_activity) | Pindah ke global logger |

### Files with NO Changes (for reference)

| File | Alasan |
|------|--------|
| `modules/showroom_v2/routes/*.py` | Tidak perlu diubah — mereka pakai `get_current_user` yang akan otomatis menyesuaikan |
| `api/inventory.py`, `api/products.py`, dll | `RequirePermission()` API tetap sama, implementasi berubah di dependency |
| `api/work_activities.py` | Sama — dependency injection, tidak perlu ubah route files |
| `api/export.py` | Sama |
| `api/dashboard.py` | Sama |
| `api/reports.py` | Sama |
| Semua route showroom | Sama — mereka pakai `get_current_user` |
| Semua file schemas yang tidak related | Tidak perlu diubah |

---

## Risiko & Mitigasi

### Risiko 1: Semua user harus re-login
Karena `sub` berubah dari username → user_id dan format JWT berubah, semua token eksisting invalid.

**Mitigasi:** Komunikasikan ke user. Ini one-time event.

### Risiko 2: Performance — setiap request query DB untuk permissions
Jika ada 100 request/detik, ada 100 query permissions.

**Mitigasi:**
1. Per-request cache (query sekali per request)
2. Jika perlu: Redis cache dengan TTL 5 menit
3. SQL: `SELECT p.code FROM permissions p JOIN role_permissions rp ON p.id=rp.permission_id JOIN user_roles ur ON ur.role_id=rp.role_id WHERE ur.user_id=:user_id` — satu query join

### Risiko 3: Frontend masih pakai `user.role.name`
Banyak komponen yang akses `user.role.name`.

**Mitigasi:** Buat helper `getPrimaryRole()` atau update semua referensi. Bisa gradual.

### Risiko 4: Session table membesar
Setiap login = 1 row. User aktif login 1x/hari bisa punya 365 row/tahun.

**Mitigasi:**
1. Cleanup job: `DELETE FROM user_sessions WHERE expired_at < now() AND is_revoked = TRUE`
2. Index pada `user_id` dan `expired_at`

### Risiko 5: Migration `role_id` column drop
Ada foreign key constraints yang perlu dihandle.

**Mitigasi:**
1. Migration: CREATE `user_roles` → INSERT data → DROP foreign key → DROP column
2. Lakukan di luar jam kerja

---

## Frontend Changes Detail

### AuthContext.jsx

```jsx
// Sebelum
const user = response.data;  // { id, username, email, role: { id, name } }

// Sesudah  
const user = response.data;  // { id, username, email, roles: [{ id, name }] }
```

### permissions.js

```js
// Sebelum — FEATURE_ROLES map
export const hasPermission = (user, feature) => {
  return FEATURE_ROLES[feature]?.includes(user.role?.name);
};

// Sesudah — FEATURE_ROLES tetap, tapi cek array roles
export const hasPermission = (user, feature) => {
  return user.roles?.some(role => 
    FEATURE_ROLES[feature]?.includes(role.name)
  );
};
```

### interceptors.js

```js
// Baru: refresh token logic on 401
let isRefreshing = false;
let failedQueue = [];

axiosInstance.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        }).then(token => {
          originalRequest.headers.Authorization = `Bearer ${token}`;
          return axiosInstance(originalRequest);
        });
      }
      
      originalRequest._retry = true;
      isRefreshing = true;
      
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post('/auth/refresh', { refresh_token: refreshToken });
        const newToken = response.data.access_token;
        localStorage.setItem('token', newToken);
        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        processQueue(null, newToken);
        return axiosInstance(originalRequest);
      } catch (err) {
        processQueue(err, null);
        localStorage.clear();
        window.location.href = '/login';
        return Promise.reject(err);
      } finally {
        isRefreshing = false;
      }
    }
    
    return Promise.reject(error);
  }
);
```

---

## Testing Checklist (Regression Test Scenarios)

Setiap scenario harus lulus setelah implementasi selesai. Checklist ini dipakai sebelum deploy.

### Authentication Flow

| # | Skenario | Langkah | Expected |
|---|----------|---------|----------|
| 1 | **Login Success** | POST `/auth/login` user valid | ✅ 200, return `{access_token, refresh_token}` |
| 2 | **Login Wrong Password** | POST `/auth/login` password salah | ❌ 401 "Incorrect username or password" |
| 3 | **Login Inactive User** | User `is_active=False` login | ❌ 400 "Inactive user" |
| 4 | **Login Non-existent User** | Username tidak ada | ❌ 401 "Incorrect username or password" |
| 5 | **Refresh Token Success** | POST `/auth/refresh` token valid | ✅ 200, return new token pair |
| 6 | **Refresh Invalid Token** | POST `/auth/refresh` token rusak | ❌ 401 |
| 7 | **Refresh Expired Token** | POST `/auth/refresh` token expired | ❌ 401 |
| 8 | **Refresh with Access Token** | POST `/auth/refresh` pakai access token | ❌ 401 "Invalid token type" |
| 9 | **Logout Revokes Session** | POST `/auth/logout`, lalu pakai refresh token lama | ❌ Session revoked |
| 10 | **Logout All Sessions** | POST `/auth/logout/all`, semua session user di-revoke | ✅ Semua session is_revoked=true |

### Permission Enforcement

| # | Skenario | Langkah | Expected |
|---|----------|---------|----------|
| 11 | **Valid Permission** | Admin akses endpoint `RequirePermission(PRODUCT_CREATE)` | ✅ 200 |
| 12 | **Invalid Permission** | Staff akses endpoint `RequirePermission(USER_CREATE)` | ❌ 403 "Permission denied" |
| 13 | **Dynamic Permission** | Tambah permission baru via DB → staff langsung bisa akses (tanpa deploy) | ✅ 200 |
| 14 | **Permission Removed** | Hapus permission dari role → akses langsung ditolak | ❌ 403 |
| 15 | **No Token** | Request tanpa `Authorization` header | ❌ 401 |

### Multi-Role

| # | Skenario | Langkah | Expected |
|---|----------|---------|----------|
| 16 | **User with 2 Roles** | User punya role ADMIN + STAFF → bisa akses kedua set permissions | ✅ Union permissions |
| 17 | **User with 0 Roles** | User tanpa role sama sekali → semua endpoint 403 | ❌ 403 |
| 18 | **Role Added** | User punya 1 role → admin assign role ke-2 → akses baru langsung aktif | ✅ Tanpa re-login |
| 19 | **Role Removed** | User kehilangan role → akses yang hilang langsung dicabut | ❌ 403 |

### User Profile

| # | Skenario | Langkah | Expected |
|---|----------|---------|----------|
| 20 | **GET /users/me** | Token valid → return user dengan roles (array) | ✅ `{ id, username, roles: [...] }` |
| 21 | **GET /users/profile** | Token valid → sama seperti /me | ✅ |
| 22 | **PUT /users/profile** | Update full_name, email | ✅ 200 |
| 23 | **User List (Admin)** | Admin GET `/users/` | ✅ Paginated, includes roles |
| 24 | **Create User** | POST `/users/` dengan `role_ids: [1, 2]` | ✅ 201, user punya 2 roles |
| 25 | **Update User Roles** | PUT `/users/{id}` dengan `role_ids` berbeda | ✅ Roles berubah |

### Token Validation

| # | Skenario | Langkah | Expected |
|---|----------|---------|----------|
| 26 | **Access Token di Refresh Endpoint** | POST `/auth/refresh` pakai access token | ❌ 401 |
| 27 | **Refresh Token di API Endpoint** | GET `/users/me` pakai refresh token | ❌ 401 |
| 28 | **Expired Access Token** | Token expired → akses endpoint | ❌ 401 |
| 29 | **Tampered Token** | Token diubah signature-nya | ❌ 401 |

### Session Management

| # | Skenario | Langkah | Expected |
|---|----------|---------|----------|
| 30 | **Double Login** | User login dari device A + B → 2 sessions | ✅ Kedua valid |
| 31 | **Revoke Single Session** | Logout device A → device B masih hidup | ✅ Device B tetap bisa akses |
| 32 | **Revoke All** | Logout all → kedua device tidak bisa akses | ❌ 401 |
| 33 | **Refresh Rotates Session** | Refresh token → `refresh_token_hash` di DB berubah | ✅ Hash baru |

### Role-Specific Access

| # | Skenario | Langkah | Expected |
|---|----------|---------|----------|
| 34 | **ADMIN** | Akses semua endpoint | ✅ 200 semua |
| 35 | **STAFF** | Hanya dashboard, inventory view, product view | ✅ Sesuai definisi |
| 36 | **CREATIVE** | Dashboard, inventory CRUD, work full, categories CRUD | ✅ Sesuai definisi |
| 37 | **MANAGER** | Dashboard, reports, inventory view, product view, showroom view | ✅ Read-only untuk module bisnis |
| 38 | **MANAGER Cannot Create** | MANAGER akses USER_CREATE / PRODUCT_CREATE | ❌ 403 |

### Edge Cases

| # | Skenario | Langkah | Expected |
|---|----------|---------|----------|
| 39 | **Revoked Session Active** | Session di-revoke → akses endpoint → auto-redirect login | ✅ 401 |
| 40 | **Wrong sub Type** | Token dengan `sub="string"` padahal user_id integer | ❌ 401/404 |
| 41 | **Deleted User Token** | Token valid → user dihapus dari DB → akses endpoint | ❌ 404 "User not found" |
| 42 | **Blacklisted Permission** | Permission ada di DB, tidak di assign ke role manapun | ✅ Tidak bisa diakses |
| 43 | **Concurrent Login** | 2 request login bersamaan → 2 sessions terpisah | ✅ Kedua session valid |
| 44 | **Null Role_ids** | POST `/users/` dengan `role_ids: null` | ❌ 422 Validation error |

### Ownership Checker (Phase 5)

| # | Skenario | Langkah | Expected |
|---|----------|---------|----------|
| 45 | **Owner Access** | Dokter A lihat record milik sendiri | ✅ 200 |
| 46 | **Non-Owner Denied** | Dokter B lihat record Dokter A | ❌ 403 |
| 47 | **Admin Override** | Admin lihat record dokter manapun | ✅ 200 |

### Branch Checker (Phase 5)

| # | Skenario | Langkah | Expected |
|---|----------|---------|----------|
| 48 | **Same Branch** | Staff Cabang Solo akses inventory Cabang Solo | ✅ 200 |
| 49 | **Different Branch** | Staff Cabang Solo akses inventory Cabang Pekalongan | ❌ 403 |
| 50 | **Cross-Branch Admin** | Admin akses semua cabang | ✅ 200 |

### Unified Audit

| # | Skenario | Langkah | Expected |
|---|----------|---------|----------|
| 51 | **Activity Logged** | Login → `audit_logs` terisi dengan `module="core"`, `action="LOGIN"` | ✅ Row baru |
| 52 | **Audit Logged** | CRUD product → `audit_logs` terisi dengan old/new value | ✅ Row baru |
| 53 | **Showroom Activity** | Showroom movement → `audit_logs` terisi dengan `module="showroom"` | ✅ Row baru |
| 54 | **GET /logs/activity** | Endpoint logs return data dari unified audit_logs | ✅ Berfungsi |
| 55 | **GET /logs/audit** | Endpoint audit return data dari unified audit_logs | ✅ Berfungsi |

---

## Phase X — Core Platform Architecture

Pisahkan semua yang reusable dari modul bisnis ke `core/`.

### Struktur Direktori Target

```
backend/app/
│
├── core/                           # Reusable Platform Layer
│   ├── __init__.py
│   │
│   ├── auth/                       # Authentication
│   │   ├── __init__.py
│   │   ├── jwt.py                  # create_access_token, decode, refresh
│   │   ├── password.py             # bcrypt hashing
│   │   ├── session.py              # SessionService (create/validate/revoke)
│   │   └── dependencies.py         # get_current_token_payload, get_current_user
│   │
│   ├── authorization/              # Authorization
│   │   ├── __init__.py
│   │   ├── models.py               # Permission, Role, RolePermission models
│   │   ├── schemas.py              # PermissionResponse, dll
│   │   ├── repositories.py         # PermissionRepository, RoleRepository
│   │   ├── services.py             # Permission sync, role assignment
│   │   ├── dependencies.py         # RequirePermission, OwnershipChecker, dll
│   │   └── seed.py                 # Startup sync Permission enum → DB
│   │
│   ├── audit/                      # Audit & Activity Logging
│   │   ├── __init__.py
│   │   ├── models.py               # AuditLog (unified)
│   │   ├── schemas.py              # AuditLogResponse
│   │   ├── services.py             # LoggerService (log_activity, log_audit)
│   │   ├── repositories.py         # AuditLogRepository
│   │   └── routes.py               # GET /logs/activity, /logs/audit
│   │
│   ├── notification/               # (future) Email, WhatsApp, Push
│   │   └── __init__.py
│   │
│   ├── storage/                    # (future) File upload, S3, local
│   │   └── __init__.py
│   │
│   ├── qr/                         # (future) QR code generation
│   │   └── __init__.py
│   │
│   ├── file/                       # (future) File processing, images
│   │   └── __init__.py
│   │
│   ├── cache/                      # (future) Redis, per-request cache
│   │   └── __init__.py
│   │
│   ├── events/                     # (future) Event bus
│   │   └── __init__.py
│   │
│   └── security/                   # Security utilities
│       ├── __init__.py
│       ├── cors.py                 # CORS setup
│       ├── middleware.py           # RequestID, Logging middleware
│       └── encryption.py           # (future) Data encryption
│
├── modules/                        # Business Modules (tipis!)
│   ├── showroom/                   # Showroom Management
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── routes/
│   │   ├── services/
│   │   └── repositories/
│   │
│   ├── inventory/                  # (future) Inventory Management
│   │   └── ...
│   │
│   ├── hr/                         # (future) HR
│   │   └── ...
│   │
│   ├── finance/                    # (future) Finance
│   │   └── ...
│   │
│   ├── clinic/                     # (future) Clinic
│   │   └── ...
│   │
│   └── production/                 # (future) Production
│       └── ...
│
├── constants/                      # Tetap — enum & constants
│   ├── permissions.py              # Permission enum (seed source)
│   └── role.py                     # RoleType constants
│
├── models/                         # Tetap — SQLAlchemy models (import dari core)
├── schemas/                        # Tetap — Pydantic schemas
├── repositories/                   # Tetap — DB repositories
├── services/                       # Tetap — Business services
├── dependencies/                   # Tetap — FastAPI dependencies
├── api/                            # Tetap — Route files
│
├── database/                       # Tetap — DB session, Base
├── config/                         # Tetap — CORS, logging
├── exceptions/                     # Tetap — Error handlers
├── common/                         # Tetap — Responses, pagination
├── middleware/                      # Tetap — Middleware
└── main.py                         # Tetap
```

### Prinsip

1. **`core/` TIDAK boleh import dari `modules/`** — core berdiri sendiri
2. **`modules/` import dari `core/`** — modul bisnis tipis, hanya business logic
3. **`core/auth/`** handle semua soal identity: JWT, sessions, login/logout/refresh
4. **`core/authorization/`** handle roles & permissions: DB storage, sync, access control
5. **`core/audit/`** handle semua logging: activity, audit trail
6. Setiap sub-package di `core/` punya `__init__.py` yang export public API

### Migration Path (dari struktur lama ke baru)

```
Structure Lama                    → Structure Baru
──────────────────────────────────────────────────────
core/jwt.py                       → core/auth/jwt.py (+ backward compat import)
core/password.py                  → core/auth/password.py
core/security.py                  → HAPUS (dead code)
dependencies/auth.py              → core/auth/dependencies.py
services/auth_service.py          → core/auth/session.py (sebagian)
                                    services/auth_service.py (tetap, panggil core)

constants/permissions.py          → Tetap (sebagai enum seed)
constants/role_permissions.py     → HAPUS
constants/role.py                 → Tetap

models/permission.py (baru)       → core/authorization/models.py
models/role_permission.py (baru)  → core/authorization/models.py
models/user_role.py (baru)        → core/authorization/models.py
models/user_session.py (baru)     → core/auth/models.py
models/role.py (lama)             → Tetap (import dari core/authorization)
models/user.py (lama)             → Tetap (import UserRole, Role)

dependencies/permission.py        → core/authorization/dependencies.py
dependencies/access_control.py    → core/authorization/dependencies.py

services/logger_service.py        → core/audit/services.py
models/activity_log.py            → core/audit/models.py
models/audit_log.py               → core/audit/models.py
models/showroom_activity_log.py   → HAPUS (migrasi ke core/audit)

api/auth.py                       → api/auth.py (tetap, panggil core/auth)
api/users.py                      → api/users.py (tetap)
api/logs.py                       → api/logs.py (tetap, panggil core/audit)
```

### Backward Compatibility

Setiap file di lokasi **lama** yang dipanggil oleh file lain akan tetap ada sebagai **wrapper**:

```python
# app/core/jwt.py (lama) → menjadi re-export
from app.core.auth.jwt import create_access_token, create_refresh_token, decode_access_token

# → Semua file yang import dari core/jwt.py TIDAK perlu diubah
```

Setelah semua file selesai direfactor, wrapper bisa dihapus di fase terpisah.

### Keuntungan

1. **Modul bisnis tipis** — showroom hanya urus showroom, tidak mikir auth
2. **Reusable** — clinic, hr, finance, production bisa pakai `core/auth/`, `core/authorization/`
3. **Testable** — `core/` bisa di-test tanpa modul bisnis
4. **Plugin-ready** — modul bisnis bisa ditambah/hapus tanpa ganggu core
5. **ERP-ready** — arsitektur ini scale untuk multi-module ERP

---

## Implementation Checklist (Final)

- [ ] **Phase 0: Plan** — Dokumen plan selesai & di-review ✅
- [ ] **Phase 1: Core Auth Infrastructure** (permissions DB + sessions + multi-role)
  - [ ] Buat direktori `core/auth/`, `core/authorization/`, `core/audit/`
  - [ ] Migration A: permissions + role_permissions tables
  - [ ] Migration B: user_sessions table
  - [ ] Migration C: user_roles table + drop users.role_id
  - [ ] Migration D: unified audit_logs table
  - [ ] Models: Permission, RolePermission, UserRole, UserSession, AuditLog
  - [ ] Schemas: Permission, UserSession, AuditLog
  - [ ] Repositories: Permission, Session
  - [ ] Services: SessionService, SeedService (permission sync)
  - [ ] JWT: core/auth/jwt.py (session-based, no role, sub=user_id)
  - [ ] Dependencies: core/auth/dependencies.py, core/authorization/dependencies.py
  - [ ] Routes: admin/permissions.py, admin/roles.py
  - [ ] Update User model: hapus role_id, tambah roles M2M
  - [ ] Update user schemas: role_id → role_ids, role → roles
  - [ ] Update user_service: handle multi-role
  - [ ] Update auth_service: sessions, user_id, no role in JWT
  - [ ] Update api/auth.py: session-based logout
  - [ ] Update api/users.py: multi-role input/output
  - [ ] Update main.py: lifespan sync, admin router
  - [ ] Token type validation
- [ ] **Phase 2: Frontend**
  - [ ] AuthContext: user.roles (array) bukan user.role
  - [ ] permissions.js: hasPermission cek array
  - [ ] ProtectedRoute: update permission check
  - [ ] interceptors.js: refresh token retry logic
  - [ ] Sidebar: update role checking
  - [ ] User form: multi-role select
- [ ] **Phase 3: MANAGER + Audit**
  - [ ] Isi permission MANAGER
  - [ ] LoggerService → core/audit/services.py
  - [ ] Hapus ShowroomActivityLog
  - [ ] Update showroom_v2/services/base.py: pakai global logger
- [ ] **Phase 4: Access Control**
  - [ ] OwnershipChecker
  - [ ] BranchChecker (basic)
  - [ ] DepartmentChecker (basic)
- [ ] **Phase 5: Core Restructure**
  - [ ] Pindahkan file ke core/*/
  - [ ] Buat backward-compat wrappers
  - [ ] Update imports
  - [ ] Hapus file lama
- [ ] **Quality Gate**
  - [ ] Backend build (python import check)
  - [ ] Frontend build (vite build)
  - [ ] Alembic migrations run (upgrade + downgrade)
  - [ ] Test semua 55 skenario dari testing checklist
