# Showroom Storage Location & QR Operations System

**Plan Version:** 3.4
**Status:** Implemented (Phase 1–10 Complete)
**Date:** 2026-07-19

---

## 1. Overview

This feature introduces a complete **physical storage management** and **QR-based operations** system for the Showroom module. QR codes become the entry point for **all** showroom operations — scanning a code triggers inventory checks, stock movements, and location lookups automatically.

### Key Design Decisions
- **Movement = Center of System**: Every operation produces a `showroom_movement` record; stock is always derived from movements.
- **Showroom starts AFTER goods leave Inventory** (handover boundary).
- **Two Entity Levels**: `showroom_locations` (business/zone) vs `showroom_storage_locations` (physical storage with self-referencing tree).
- **QR via Registry Pattern**: `showroom_qr_entities` table only, with pluggable resolvers per entity type.
- **Optimistic Locking**: `version` column on both stocks and storage locations.
- **Activity Logs**: Immutable, insert-only audit trail.

---

## 2. Architecture

### 2.1 Data Flow

```
┌─────────────────────────────────────────────────────────┐
│                     QR Code Scan                         │
│                  (token → resolve)                       │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                QR Entity Registry                        │
│         (storage, product, machine, room, printer)       │
│                                                          │
│  resolve_qr_token() → entity data → process action       │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│               QR Scan Service                            │
│                                                          │
│  CHECK_INVENTORY → return current stock at location      │
│  STOCK_IN → create movement + update stock (+qty)        │
│  STOCK_OUT → create movement + update stock (-qty)       │
│  CHECK_STOCK → return stock for product across locations │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              Optimistic Locking                          │
│                                                          │
│  SELECT FOR UPDATE → check version → update stock        │
│  → increment version → recalculate capacity              │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              Activity Log (Insert-Only)                   │
│                                                          │
│  action, entity_type, entity_id, actor_id, request_id    │
│  old_value, new_value (JSON snapshots)                    │
└─────────────────────────────────────────────────────────┘
```

### 2.2 New Database Tables

| Table | Purpose |
|---|---|
| `showroom_storage_locations` | Physical storage hierarchy (self-referencing tree) |
| `showroom_qr_entities` | QR code → entity mapping (generic, multi-type) |
| `showroom_activity_logs` | Immutable audit trail for all operations |
| `showroom_storage_snapshots` | Point-in-time stock snapshots per location |
| `showroom_daily_storage_summary` | Daily aggregated dashboard data |
| `showroom_permissions` | Granular permission codes |
| `showroom_roles` | Role definitions (system roles) |
| `showroom_role_permissions` | Role ↔ Permission mapping |
| `showroom_user_roles` | User ↔ Role assignment |

### 2.3 Updated Tables

| Table | Changes |
|---|---|
| `showroom_sample_stocks` | Added `storage_location_id` FK, `version` column |

---

## 3. Database Schema

### 3.1 `showroom_storage_locations`

| Column | Type | Description |
|---|---|---|
| `id` | INT PK | Auto-increment |
| `name` | VARCHAR(100) | Display name |
| `code` | VARCHAR(50) UNIQUE | Unique code (e.g. `SHW-A-01`) |
| `parent_id` | INT FK → self | Parent location (NULL = root) |
| `location_id` | INT FK → showroom_locations | Business location this belongs to |
| `storage_type` | VARCHAR(50) | `shelf`, `rack`, `cabinet`, `room`, `floor`, `zone` |
| `capacity_qty` | INT | Maximum capacity (NULL = unlimited) |
| `capacity_unit` | VARCHAR(20) | `PCS`, `BOX`, `HANGER`, `ROLL` |
| `capacity_note` | VARCHAR(255) | Human-readable capacity note |
| `used_capacity` | INT DEFAULT 0 | Current used capacity (recalculated from stock) |
| `path` | VARCHAR(500) | Cache path (auto-rebuilt from parent_id, never manual) |
| `description` | TEXT | Optional description |
| `is_active` | BOOLEAN DEFAULT 1 | Soft delete flag |
| `version` | INT DEFAULT 1 | Optimistic lock version |
| `created_at` | DATETIME | Creation timestamp |
| `updated_at` | DATETIME | Last update timestamp |

**Constraints:**
- Max depth: 2 levels (root → child → leaf)
- `path` is auto-rebuilt: never set manually
- `used_capacity` is auto-recalculated from `showroom_sample_stocks`

### 3.2 `showroom_qr_entities`

| Column | Type | Description |
|---|---|---|
| `id` | INT PK | Auto-increment |
| `entity_type` | VARCHAR(50) | `storage`, `product`, `machine`, `room`, `printer` |
| `entity_id` | INT | ID of the referenced entity |
| `token` | VARCHAR(100) UNIQUE | URL-safe token (20 chars) |
| `label` | VARCHAR(100) | Human-readable label |
| `storage_location_id` | INT FK → showroom_storage_locations | Optional: linked storage location |
| `is_active` | BOOLEAN DEFAULT 1 | Soft delete |
| `version` | INT DEFAULT 1 | Optimistic lock |
| `created_at` | DATETIME | Creation timestamp |
| `updated_at` | DATETIME | Last update timestamp |

### 3.3 `showroom_activity_logs`

| Column | Type | Description |
|---|---|---|
| `id` | INT PK | Auto-increment |
| `action` | VARCHAR(50) | Action code (e.g. `STORAGE_CREATE`, `QR_STOCK_IN`) |
| `entity_type` | VARCHAR(50) | Entity type affected |
| `entity_id` | INT | Entity ID affected |
| `actor_id` | INT FK → users | User who performed the action |
| `actor_type` | VARCHAR(20) DEFAULT 'USER' | `USER` or `SYSTEM` |
| `request_id` | VARCHAR(36) | UUID for request tracing |
| `idempotency_key` | VARCHAR(100) UNIQUE | Prevent duplicate operations |
| `detail` | TEXT | JSON detail |
| `old_value` | TEXT | JSON snapshot before change |
| `new_value` | TEXT | JSON snapshot after change |
| `created_at` | DATETIME | Creation timestamp |

### 3.4 `showroom_storage_snapshots`

| Column | Type | Description |
|---|---|---|
| `id` | INT PK | Auto-increment |
| `storage_location_id` | INT FK | Storage location |
| `product_id` | INT FK → products | Product |
| `sample_type` | VARCHAR(50) | `Display`, `Photography`, `Premium`, `Archive` |
| `quantity` | INT | Stock quantity at snapshot time |
| `snapshot_type` | VARCHAR(30) | `NIGHTLY`, `OPNAME_APPROVED`, `MIGRATION`, `MANUAL` |
| `created_at` | DATETIME | Snapshot timestamp |

### 3.5 `showroom_daily_storage_summary`

| Column | Type | Description |
|---|---|---|
| `id` | INT PK | Auto-increment |
| `summary_date` | DATE | Summary date |
| `total_items` | INT | Total items across all locations |
| `total_products` | INT | Total unique products |
| `total_locations` | INT | Total active locations |
| `total_movements` | INT | Total movements that day |
| `incoming` | INT | Total incoming quantity |
| `outgoing` | INT | Total outgoing quantity |
| `capacity_used_pct` | INT | Capacity utilization percentage |
| `created_at` | DATETIME | Creation timestamp |

### 3.6 Permission Tables

**`showroom_permissions`**

| code | name | description |
|---|---|---|
| `SHOWROOM_ADMIN` | Admin | Full access, bypasses all checks |
| `SHOWROOM_VIEWER` | Viewer | Read-only access |
| `SHOWROOM_OPERATOR` | Operator | Stock in/out, handover, scan |
| `SHOWROOM_SUPERVISOR` | Supervisor | Approve opname, adjust, transfer |

**`showroom_roles`** — 4 system roles: `SHOWROOM_ADMIN`, `SHOWROOM_VIEWER`, `SHOWROOM_OPERATOR`, `SHOWROOM_SUPERVISOR`

---

## 4. Backend API

All endpoints are prefixed with `/showroom-v2/` (mounted via the showroom V2 router).

### 4.1 Storage Endpoints (`/showroom-v2/storage`)

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `GET` | `/storage` | List storage locations (filter: `location_id`, `parent_id`) | User |
| `GET` | `/storage/tree` | Get hierarchical tree (filter: `location_id`) | User |
| `GET` | `/storage/{id}` | Get single storage location | User |
| `POST` | `/storage` | Create storage location | User |
| `PUT` | `/storage/{id}` | Update storage location | User |
| `DELETE` | `/storage/{id}` | Soft-delete storage location | User |
| `GET` | `/storage/qr/all` | List QR entities (filter: `entity_type`) | User |
| `GET` | `/storage/qr/{id}` | Get single QR entity | User |
| `POST` | `/storage/qr` | Create QR entity (auto-generates token) | User |
| `PUT` | `/storage/qr/{id}` | Update QR entity | User |
| `DELETE` | `/storage/qr/{id}` | Soft-delete QR entity | User |

**POST /storage — Request Body:**
```json
{
  "name": "Rak A-01",
  "code": "SHW-A-01",
  "parent_id": null,
  "location_id": 1,
  "storage_type": "shelf",
  "capacity_qty": 50,
  "capacity_unit": "PCS",
  "capacity_note": "Max 50 PCS produk display",
  "description": "Rak utama di area display"
}
```

**POST /storage/qr — Request Body:**
```json
{
  "entity_type": "storage",
  "entity_id": 1,
  "label": "QR Rak A-01"
}
```
> Token is auto-generated: `secrets.token_urlsafe(16)[:20]`

### 4.2 QR Scan Endpoints (`/showroom-v2/qr`)

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/qr/resolve` | Resolve QR token → return entity data |
| `POST` | `/qr/storage-scan` | Process storage QR scan (CHECK_INVENTORY / STOCK_IN / STOCK_OUT) |
| `POST` | `/qr/product-scan` | Process product QR scan (CHECK_STOCK) |

**POST /qr/resolve — Request Body:**
```json
{ "token": "aB3xK9mNpQ2rS5tU" }
```

**Response:**
```json
{
  "qr": {
    "id": 1,
    "token": "aB3xK9mNpQ2rS5tU",
    "entity_type": "storage",
    "entity_id": 1,
    "label": "QR Rak A-01"
  },
  "entity": {
    "id": 1,
    "name": "Rak A-01",
    "code": "SHW-A-01",
    "storage_type": "shelf",
    "capacity_qty": 50,
    "capacity_unit": "PCS",
    "used_capacity": 12,
    "path": "SHW-A-01",
    "location_id": 1
  }
}
```

**POST /qr/storage-scan — Request Body:**
```json
{
  "token": "aB3xK9mNpQ2rS5tU",
  "action": "STOCK_IN",
  "product_id": 5,
  "quantity": 10,
  "sample_type": "Display"
}
```

**Actions:**

| Action | Description | Required Fields |
|---|---|---|
| `CHECK_INVENTORY` | Returns all stock at this location | — |
| `STOCK_IN` | Adds stock to location | `product_id`, `quantity` |
| `STOCK_OUT` | Removes stock from location | `product_id`, `quantity` |

**POST /qr/product-scan — Request Body:**
```json
{
  "token": "xY7zW4vU8tR1qP0n",
  "action": "CHECK_STOCK"
}
```

### 4.3 Dashboard V2 Endpoints (`/showroom-v2/dashboard`)

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/dashboard` | Summary KPIs (total items, products, locations, movements) |
| `GET` | `/dashboard/movements` | Recent movements (limit param) |
| `GET` | `/dashboard/heatmap` | Stock heatmap data (product × location) |
| `GET` | `/dashboard/analytics/trends` | Movement trends over N days |
| `GET` | `/dashboard/analytics/top-products` | Top products by movement count |
| `GET` | `/dashboard/analytics/borrowing` | Borrowing analytics |
| `POST` | `/dashboard/snapshot` | Create manual snapshot |
| `POST` | `/dashboard/rebuild-summary` | Rebuild daily summary cache |
| `GET` | `/dashboard/summary-history` | Historical daily summaries |

---

## 5. Frontend

### 5.1 New Pages

| Page | Route | Description |
|---|---|---|
| `StorageManagement.jsx` | `/showroom/storage` | Tree view with CRUD, capacity indicators |
| `ScanStorage.jsx` | `/showroom/scan` | Mobile-first QR scan interface |
| `DashboardV2.jsx` | `/showroom/dashboard` | KPI cards, heatmap, analytics |

### 5.2 Storage Management (`/showroom/storage`)

**Features:**
- Hierarchical tree view with expand/collapse
- Create/edit/delete storage locations
- Capacity indicators (used/total with color coding)
- Parent-child relationship management
- Max depth validation (2 levels)
- Code uniqueness validation
- Auto-path rebuild on parent change

**Form Fields:**
| Field | Type | Required | Placeholder |
|---|---|---|---|
| Nama | text | Yes | Nama storage location |
| Kode | text | Yes | e.g. A-01-02 |
| Parent Location | SearchableSelect | No | — |
| Tipe | select | No | shelf |
| Kapasitas | number | No | Jumlah kapasitas |
| Unit | select | No | PCS |
| Catatan Kapasitas | text | No | Catatan kapasitas (opsional) |
| Deskripsi | textarea | No | Deskripsi storage (opsional) |

### 5.3 Scan Storage (`/showroom/scan`)

**Workflow:**
1. User enters/scans QR token
2. System resolves token → displays entity info
3. User selects action (CHECK_INVENTORY / STOCK_IN / STOCK_OUT)
4. For STOCK_IN/STOCK_OUT: user selects product + enters quantity
5. System processes operation → shows result

**Actions Available:**

| Action | When | What Happens |
|---|---|---|
| CHECK_INVENTORY | Storage QR scanned | Shows all items at this location |
| STOCK_IN | Storage QR + product selected | Adds stock, creates movement |
| STOCK_OUT | Storage QR + product selected | Removes stock, creates movement |
| CHECK_STOCK | Product QR scanned | Shows stock across all locations |

### 5.4 Dashboard V2 (`/showroom/dashboard`)

**Widgets:**
- **KPI Cards**: Total items, products, locations, movements
- **Heatmap**: Color-coded grid showing stock density (product × location)
- **Recent Movements**: Last N movements with type/quantity/user
- **Movement Trends**: Line chart over N days
- **Top Products**: Bar chart of most-moved products
- **Capacity Utilization**: Overall storage usage percentage

### 5.5 Updated Pages with Storage Selection

| Page | Form | Storage Field |
|---|---|---|
| SampleManagement | HandoverForm | `storage_location_id` (SearchableSelect) |
| SampleManagement | TransferForm | `from_storage_location_id`, `to_storage_location_id` |
| SampleManagement | AdjustForm | `storage_location_id` (SearchableSelect) |

> Storage SearchableSelect only appears when a business location is selected.

### 5.6 Offline Queue (`useOfflineQueue`)

**Purpose:** Handle operations when device is offline (e.g., mobile QR scanning in warehouse).

**States:**
| Status | Description |
|---|---|
| `PENDING` | Queued, waiting for connection |
| `SYNCING` | Currently being sent to server |
| `SUCCESS` | Successfully processed |
| `FAILED` | Failed after max retries |
| `CONFLICT` | Server returned 409 conflict |

**API:**
```javascript
const {
  queue,          // Array of queued items
  enqueue(item),  // Add item to queue
  remove(id),     // Remove item from queue
  retry(id),      // Retry failed item
  clearCompleted, // Remove all SUCCESS items
  processQueue,   // Manually trigger sync
  isSyncing,      // Boolean: currently syncing
  pendingCount,   // Number of PENDING items
  failedCount,    // Number of FAILED/CONFLICT items
} = useOfflineQueue();
```

**Storage:** localStorage (`csms_offline_queue`), auto-syncs on `online` event.

---

## 6. Backend Services

### 6.1 Storage Service (`StorageService`)

| Method | Description |
|---|---|
| `get_all(db, location_id, parent_id)` | List storage locations with filters |
| `get_tree(db, location_id)` | Build hierarchical tree structure |
| `get_by_id(db, storage_id)` | Get single location |
| `create(db, data, user_id)` | Create location + log activity |
| `update(db, storage_id, data, user_id)` | Update location + rebuild paths + log |
| `delete(db, storage_id, user_id)` | Soft-delete (check children/stock) + log |
| `_rebuild_path(db, location_id)` | Rebuild path cache from parent chain |
| `_rebuild_all_paths(db, location_id)` | Recursively rebuild child paths |
| `_recalculate_capacity(db, storage_location_id)` | Sum stock qty for this location |
| `_validate_depth(db, parent_id)` | Enforce max 2-level depth |

### 6.2 QR Entity Service (`QREntityService`)

| Method | Description |
|---|---|
| `get_all(db, entity_type)` | List QR entities |
| `get_by_id(db, qr_id)` | Get single QR entity |
| `create(db, data, user_id)` | Create QR entity with auto-generated token |
| `update(db, qr_id, data, user_id)` | Update QR entity |
| `delete(db, qr_id, user_id)` | Soft-delete QR entity |
| `resolve(db, token)` | Resolve token → entity data via Registry |

### 6.3 QR Scan Service (`QRScanService`)

| Method | Description |
|---|---|
| `process_storage_scan(db, qr_data, action, ...)` | Handle storage QR scan |
| `process_product_scan(db, qr_data, action, ...)` | Handle product QR scan |

### 6.4 Base Service (`base.py`)

| Method | Description |
|---|---|
| `log_activity(db, action, entity_type, ...)` | Insert activity log record |
| `acquire_stock_lock(db, stock_id)` | SELECT FOR UPDATE on stock row |
| `get_or_create_stock(db, product_id, location_id, ...)` | Get existing or create new stock record |
| `update_stock_with_optimistic_lock(db, stock_id, delta)` | Update with version check |

### 6.5 Permissions (`core/permissions.py`)

| Function | Description |
|---|---|
| `get_user_permissions(db, user_id)` | Fetch all permission codes for user |
| `has_permission(db, user_id, code)` | Check single permission (SHOWROOM_ADMIN bypasses) |
| `require_permission(code)` | Route decorator: 403 if missing |
| `require_any_permission(*codes)` | Route decorator: 403 if none match |

### 6.6 QR Resolvers (`core/qr_resolvers.py`)

| Function | Description |
|---|---|
| `register_resolver(entity_type, fn)` | Register resolver function for entity type |
| `resolve_qr_token(db, token)` | Look up QR + call resolver |

**Built-in Resolvers:**
- `storage` → returns `ShowroomStorageLocation` data
- `product` → returns `Product` data

**Adding a new entity type:**
```python
from app.modules.showroom_v2.core.qr_resolvers import register_resolver

def _resolve_machine(db, entity_type, entity_id):
    machine = db.query(Machine).filter(Machine.id == entity_id).first()
    if not machine:
        return None
    return {"id": machine.id, "name": machine.name, "status": machine.status}

register_resolver("machine", _resolve_machine)
```

---

## 7. Alembic Migrations

| Revision | Description |
|---|---|
| `001a1b2c3d4e` | Create `showroom_storage_locations` |
| `002b2c3d4e5f` | Create `showroom_qr_entities`, `showroom_activity_logs` |
| `003c3d4e5f60` | Create `showroom_permissions`, `showroom_roles`, `showroom_role_permissions`, `showroom_user_roles` |
| `003b3d4e5f61` | Create `showroom_storage_snapshots`, `showroom_daily_storage_summary` |
| `004d4e5f6071` | Add `version` + `storage_location_id` to `showroom_sample_stocks` |
| `005e5f607182` | Seed 4 roles + 12 permissions |

**Run all migrations:**
```bash
cd backend
alembic upgrade head
```

---

## 8. File Structure

### Backend (New Files)
```
backend/app/
├── models/
│   ├── showroom_storage_location.py
│   ├── showroom_qr_entity.py
│   ├── showroom_activity_log.py
│   ├── showroom_storage_snapshot.py
│   ├── showroom_daily_storage_summary.py
│   └── showroom_permission.py
├── modules/showroom_v2/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── permissions.py
│   │   └── qr_resolvers.py
│   ├── services/
│   │   ├── base.py (updated)
│   │   ├── storage_service.py
│   │   ├── qr_entity_service.py
│   │   ├── qr_scan_service.py
│   │   ├── dashboard_service.py
│   │   ├── analytics_service.py
│   │   └── snapshot_service.py
│   └── routes/
│       ├── __init__.py (updated)
│       ├── storage.py
│       ├── qr_scan.py
│       └── dashboard_v2.py
└── alembic/versions/
    ├── 001a1b2c3d4e_create_storage_locations.py
    ├── 002b2c3d4e5f_create_qr_entities_activity_logs.py
    ├── 003c3d4e5f60_create_permissions_roles.py
    ├── 003b3d4e5f61_create_snapshots_summary.py
    ├── 004d4e5f6071_add_stock_version_storage.py
    └── 005e5f607182_seed_permissions.py
```

### Frontend (New Files)
```
frontend/src/
├── modules/showroom/
│   ├── pages/
│   │   ├── StorageManagement.jsx
│   │   ├── ScanStorage.jsx
│   │   └── DashboardV2.jsx (updated)
│   ├── routes.jsx (updated)
│   └── helpers/index.js (updated)
├── hooks/
│   └── useOfflineQueue.js
├── layouts/
│   └── ShowroomLayout.jsx (updated)
└── api/
    ├── endpoints.js (updated)
    └── services/showroomService.js (updated)
```

---

## 9. Deployment Checklist

1. **Backend:**
   ```bash
   cd backend
   git pull origin main
   source venv/bin/activate
   alembic upgrade head
   ```

2. **Frontend:**
   ```bash
   cd frontend
   git pull origin main
   npm install
   npm run build
   ```

3. **Verify:**
   - Check `/showroom/storage` renders tree view
   - Check `/showroom/scan` accepts QR tokens
   - Check `/showroom/dashboard` shows heatmap + KPIs
   - Verify existing sample/borrowing/guest forms have storage fields
