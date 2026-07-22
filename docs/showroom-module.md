# Showroom Module Documentation

## Overview

The Showroom module (`showroom_v2`) manages physical product samples in a showroom environment. It tracks stock movements (handover, transfer, borrow, return, release, maintenance, etc.), manages locations, storage racks, QR-based scanning, borrowing, guest releases, stock opname, restock requests, reservations, and reporting.

**Base URL:** `/api/v1/showroom-v2`  
**Auth:** All endpoints (except `/public/*`) require bearer JWT token via `get_current_user`.

---

## Backend Structure

```
backend/app/modules/showroom_v2/
├── routes/           → 13 route files, ~95 endpoints
│   ├── __init__.py   → Aggregates all sub-routers
│   ├── dashboard_v2.py
│   ├── dashboard.py
│   ├── sample.py     → Stock CRUD, handover, transfer, borrow, return, adjust, location CRUD
│   ├── borrowing.py  → Borrowing management (extend, cancel)
│   ├── guest.py      → Guest release (approve, reject, return)
│   ├── stock_control.py → Opname, restock, maintenance, reservations
│   ├── reporting.py  → KPIs, movement summary, stock by location, product history
│   ├── master_data.py → Generic master data CRUD (sample_type, maintenance_type, etc.)
│   ├── public.py     → Public scan (no auth), QR generation
│   ├── storage.py    → Storage locations CRUD, QR entities CRUD
│   ├── qr_scan.py    → QR token resolve, storage/product scan
│   ├── manage.py     → Management page (stock listing, add/remove with movement type)
│   └── movement_types.py → Movement type definitions CRUD
├── services/
│   ├── base.py       → Shared utilities (jakarta_now, validate_quantity, log_activity, get_or_create_stock, update_stock_with_optimistic_lock)
│   ├── sample_service.py
│   ├── borrowing_service.py
│   ├── guest_service.py
│   ├── stock_control_service.py
│   ├── reporting_service.py
│   ├── master_data_service.py
│   ├── storage_service.py
│   ├── qr_entity_service.py
│   ├── qr_scan_service.py
│   ├── dashboard_service.py
│   ├── analytics_service.py
│   └── snapshot_service.py
├── schemas/__init__.py → Pydantic models (LocationCreate/Update/Response, MovementResponse, BorrowingResponse, etc.)
```

---

## Database Models (19 showroom-specific tables)

### `showroom_locations`
| Column | Type | Notes |
|--------|------|-------|
| id | Integer | PK |
| code | String(50) | Unique, index |
| name | String(100) | |
| type | String(20) | `internal` or `external` |
| description | Text | Nullable |
| image_url | String(500) | Nullable |
| is_active | Boolean | Default true |
| created_at | DateTime | UTC+7 |
| updated_at | DateTime | UTC+7 |

Relationships: `stocks` (ShowroomSampleStock), `movements_from` (ShowroomMovement), `movements_to` (ShowroomMovement)

### `showroom_storage_locations`
Rak/laci/penyimpanan fisik di dalam suatu lokasi. Mendukung hierarki parent-child.  
Columns: `id`, `name`, `code`, `parent_id` (FK self), `location_id` (FK → showroom_locations), `storage_type` (`shelf`/`drawer`/`rack`/`cabinet`), `capacity_qty`, `capacity_unit`, `capacity_note`, `description`, `is_active`, `version` (optimistic lock), `created_at`, `updated_at`

### `showroom_sample_stock`
Stok sample di suatu lokasi.  
Columns: `id`, `product_id` (FK → products), `location_id` (FK → showroom_locations), `storage_location_id` (FK → showroom_storage_locations), `sample_type`, `quantity`, `is_active`, `version`, `created_at`, `updated_at`

### `showroom_movements`
Semua pergerakan produk. Setiap operasi (handover, transfer, borrow, dll) mencatat satu baris di sini.  
Columns: `id`, `movement_type` (String 50 — dari showroom_movement_types.code), `product_id`, `from_location_id` (FK → showroom_locations, nullable), `to_location_id` (FK → showroom_locations, nullable), `quantity`, `sample_type`, `purpose`, `user_id`, `date` (UTC+7), `notes`, `reference_type`, `reference_id`, `created_at`, `updated_at`

### `showroom_movement_types`
Definisi tipe pergerakan yang valid.  
Columns: `id`, `code` (String 50, unique), `name`, `direction` (IN/OUT), `is_active`, `notes` (keterangan penggunaan), `created_at`, `updated_at`

### `showroom_borrowings`
Peminjaman sample.  
Columns: `id`, `product_id`, `from_location_id`, `borrower_name`, `borrower_location_id` (FK → showroom_locations), `quantity`, `sample_type`, `purpose`, `borrow_date`, `expected_return_date`, `actual_return_date`, `borrowed_at`, `status` (active/returned/overdue/cancelled), `user_id`, `movement_id` (FK → showroom_movements), `return_movement_id`, `notes`, `created_at`, `updated_at`

### `showroom_guest_releases`
Release sample ke tamu.  
Columns: `id`, `product_id`, `location_id`, `quantity`, `sample_type`, `guest_name`, `guest_company`, `purpose`, `release_date`, `status` (draft/approved/rejected/returned), `user_id`, `approved_by`, `approved_at`, `rejected_by`, `rejected_at`, `movement_id`, `return_movement_id`, `return_date`, `notes`, `created_at`, `updated_at`

### `showroom_opname_sessions`
Sesi stock opname.  
Columns: `id`, `name`, `location_id`, `status` (in_progress/completed/approved), `created_by`, `approved_by`, `completed_at`, `approved_at`, `notes`, `created_at`

### `showroom_opname_items`
Item hasil opname.  
Columns: `id`, `session_id`, `product_id`, `location_id`, `sample_type`, `expected_quantity`, `actual_quantity`, `variance`, `adjustment_movement_id`, `notes`

### `showroom_restock_requests`
Permintaan restock.  
Columns: `id`, `product_id`, `location_id`, `sample_type`, `minimum_quantity`, `current_quantity`, `requested_quantity`, `source`, `status` (pending/approved/rejected), `requested_by`, `approved_by`, `movement_id`, `notes`, `created_at`, `updated_at`

### `showroom_maintenance`
Perawatan sample.  
Columns: `id`, `product_id`, `location_id`, `maintenance_type`, `status` (in_maintenance/completed), `quantity`, `sample_type`, `notes`, `created_by`, `completed_by`, `movement_id`, `return_movement_id`, `created_at`, `completed_at`

### `showroom_reservations`
Reservasi sample.  
Columns: `id`, `product_id`, `quantity`, `purpose`, `reserved_from`, `reserved_until`, `status` (active/expired/cancelled/fulfilled), `user_id`, `notes`, `created_at`, `updated_at`

### `showroom_qr_entities`
Entity QR codes.  
Columns: `id`, `entity_type` (storage_location/product/location), `entity_id`, `token` (UUID unique), `label`, `storage_location_id`, `is_active`, `version`, `created_at`, `updated_at`

### `showroom_barcode_scans`
Log scan QR.  
Columns: `id`, `barcode`, `scan_type` (storage/product), `result_id`, `result_type`, `user_id`, `location_id`, `movement_id`, `notes`, `scanned_at`

### `showroom_activity_logs`
Aktivitas log.  
Columns: `id`, `action`, `entity_type`, `entity_id`, `actor_type`, `user_id`, `request_id`, `idempotency_key`, `detail`, `old_value`, `new_value`, `created_at`

### `showroom_master_data`
Generic master data with type discriminator. Types: `sample_type`, `maintenance_type`, `purpose`, `borrow_reason`, `release_reason`, `location_type`.  
Columns: `id`, `type`, `name`, `value`, `description`, `is_active`, `sort_order`, `created_at`, `updated_at`

### `showroom_storage_snapshots`
Snapshot stok periodik.  
Columns: `id`, `storage_location_id`, `product_id`, `sample_type`, `quantity`, `snapshot_type`, `created_at`

### `showroom_daily_storage_summary`
Rangkuman harian.  
Columns: `id`, `summary_date`, `total_items`, `total_products`, `total_locations`, `total_movements`, `incoming`, `outgoing`, `capacity_used_pct`, `created_at`

### `showroom_movement_types`
See above.

---

## API Endpoints (95 total)

### Dashboard V2 (`/dashboard`) — 12 endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | `/dashboard` | Summary dashboard KPI |
| GET | `/dashboard/borrowing-stats` | Borrowing statistics |
| GET | `/dashboard/guest-stats` | Guest release stats |
| GET | `/dashboard/overdue-borrowings` | Overdue borrowings list |
| GET | `/dashboard/movements` | Recent movements (limit) |
| GET | `/dashboard/heatmap` | Stock distribution heatmap |
| GET | `/dashboard/analytics/trends` | Movement trends (days) |
| GET | `/dashboard/analytics/top-products` | Top moved products (limit) |
| GET | `/dashboard/analytics/borrowing` | Borrowing analytics |
| POST | `/dashboard/snapshot` | Create manual snapshot |
| POST | `/dashboard/rebuild-summary` | Rebuild daily summary |
| GET | `/dashboard/summary-history` | Summary history (days) |

### Dashboard Legacy (`/dashboard/legacy`) — 4 endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | `/dashboard/legacy/` | Legacy KPI |
| GET | `/dashboard/legacy/borrowing-stats` | Legacy borrowing stats |
| GET | `/dashboard/legacy/guest-stats` | Legacy guest stats |
| GET | `/dashboard/legacy/overdue-borrowings` | Legacy overdue list |

### Samples (`/samples`) — 13 endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | `/samples/stock` | Stock summary (by location) |
| GET | `/samples/stock/{product_id}` | Stock for specific product |
| POST | `/samples/handover` | Handover inventory → showroom |
| POST | `/samples/transfer` | Transfer between locations |
| POST | `/samples/borrow` | Borrow sample |
| POST | `/samples/return/{borrowing_id}` | Return borrowed sample |
| POST | `/samples/adjust` | Adjust stock quantity |
| GET | `/samples/locations` | List active locations |
| GET | `/samples/movements` | Movement history (filtered) |
| GET | `/samples/locations-all` | All locations (incl inactive) |
| POST | `/samples/locations` | Create location |
| PUT | `/samples/locations/{location_id}` | Update location |
| DELETE | `/samples/locations/{location_id}` | Delete location |

### Borrowings (`/borrowings`) — 6 endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | `/borrowings/` | List (filter by status) |
| GET | `/borrowings/overdue` | Overdue list |
| GET | `/borrowings/stats` | Statistics |
| GET | `/borrowings/{borrowing_id}` | Get by ID |
| POST | `/borrowings/{borrowing_id}/extend` | Extend due date |
| POST | `/borrowings/{borrowing_id}/cancel` | Cancel borrowing |

### Guests (`/guests`) — 7 endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | `/guests/` | List (filter by status) |
| GET | `/guests/stats` | Statistics |
| GET | `/guests/{release_id}` | Get by ID |
| POST | `/guests/` | Create release (Draft) |
| POST | `/guests/{release_id}/approve` | Approve + reduce stock |
| POST | `/guests/{release_id}/reject` | Reject |
| POST | `/guests/{release_id}/return` | Return from guest |

### Stock Control (`/stock-control`) — 13 endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | `/stock-control/opname` | List opname sessions |
| POST | `/stock-control/opname` | Create session |
| POST | `/stock-control/opname/{session_id}/items` | Add item count |
| POST | `/stock-control/opname/{session_id}/complete` | Complete session |
| POST | `/stock-control/opname/{session_id}/approve` | Approve session |
| GET | `/stock-control/restock` | List restock requests |
| POST | `/stock-control/restock` | Create request |
| POST | `/stock-control/restock/{request_id}/approve` | Approve + fulfill |
| GET | `/stock-control/maintenance` | List maintenance |
| POST | `/stock-control/maintenance` | Create |
| POST | `/stock-control/maintenance/{maintenance_id}/complete` | Complete |
| GET | `/stock-control/reservations` | List reservations |
| POST | `/stock-control/reservations` | Create reservation |

### Reports (`/reports`) — 6 endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | `/reports/kpi` | KPI data |
| GET | `/reports/movement-summary` | Movement summary (days) |
| GET | `/reports/stock-by-location` | Stock by location |
| GET | `/reports/product-history/{product_id}` | Product movement history |
| GET | `/reports/borrowing-summary` | Borrowing summary |
| GET | `/reports/guest-summary` | Guest release summary |

### Master Data (`/master-data`) — 7 endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | `/master-data/` | List (by type, active_only) |
| GET | `/master-data/types` | Valid type keys |
| GET | `/master-data/{item_id}` | Get by ID |
| POST | `/master-data/` | Create |
| PUT | `/master-data/{item_id}` | Update |
| DELETE | `/master-data/{item_id}` | Delete |
| POST | `/master-data/seed` | Seed defaults |

### Public (`/public`) — 3 endpoints (NO AUTH)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/public/scan/{code}` | Location details + products |
| GET | `/public/scan/{code}/qr` | QR code PNG for location |
| GET | `/public/qr/{token}/image` | QR code PNG for any entity |

### Storage (`/storage`) — 12 endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | `/storage` | List storage locations |
| GET | `/storage/tree` | Hierarchy tree |
| GET | `/storage/qr` | List QR entities (alias) |
| GET | `/storage/qr/all` | List all QR entities |
| GET | `/storage/qr/{qr_id}` | Get QR entity |
| POST | `/storage/qr` | Create QR entity |
| PUT | `/storage/qr/{qr_id}` | Update QR entity |
| DELETE | `/storage/qr/{qr_id}` | Delete QR entity |
| GET | `/storage/{storage_id}` | Get storage by ID |
| POST | `/storage` | Create storage location |
| PUT | `/storage/{storage_id}` | Update storage location |
| DELETE | `/storage/{storage_id}` | Delete storage location |

### QR Scan (`/qr`) — 3 endpoints
| Method | Path | Description |
|--------|------|-------------|
| POST | `/qr/resolve` | Resolve QR token |
| POST | `/qr/storage-scan` | Process storage scan |
| POST | `/qr/product-scan` | Process product scan |

### Manage (`/manage`) — 4 endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | `/manage` | List products in management (paginated) |
| POST | `/manage/add` | Add/remove product with movement type |
| DELETE | `/manage/{stock_id}` | Remove product from management |
| GET | `/manage/report` | Movement report by period |

### Movement Types (`/movement-types`) — 5 endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | `/movement-types/` | List all (active_only filter) |
| GET | `/movement-types/{item_id}` | Get by ID |
| POST | `/movement-types/` | Create |
| PUT | `/movement-types/{item_id}` | Update |
| DELETE | `/movement-types/{item_id}` | Delete |

---

## All Response Format

```json
{
  "success": true,
  "data": { ... },
  "message": "optional message"
}
```

The `data` field can be an object, array, or null depending on the endpoint.

---

## Movement Types (Seeded in Database)

| Code | Direction | Description |
|------|-----------|-------------|
| HANDOVER | IN | Barang masuk ke showroom dari inventory / produksi |
| SHOWROOM_IN | IN | Barang masuk ke showroom dari lokasi lain |
| RETURN | IN | Barang dikembalikan setelah dipinjam |
| RESTOCK | IN | Penambahan stok baru (produksi, pembelian, hibah) |
| TRANSFER_IN | IN | Barang diterima dari lokasi ERP lain |
| MAINTENANCE_RETURN | IN | Barang kembali setelah selesai perawatan |
| ADJUSTMENT_IN | IN | Koreksi stok (+) hasil stock opname |
| ADJUSTMENT_OUT | OUT | Koreksi stok (-) hasil stock opname |
| SHOWROOM_OUT | OUT | Barang keluar ke gudang / luar showroom |
| BORROW | OUT | Barang dipinjam oleh pihak internal |
| TRANSFER_OUT | OUT | Barang dikirim ke cabang/showroom lain |
| TRANSFER | OUT | Barang dipindahkan antar lokasi showroom |
| RELEASE | OUT | Barang keluar permanen (hadiah, sponsor, dll) |
| RELEASE_REJECT | OUT | Barang release ditolak / dibatalkan |
| MAINTENANCE_OUT | OUT | Barang keluar untuk perawatan |
| RETIRED | OUT | Aset dinonaktifkan dari operasional |
| SCRAP | OUT | Barang dimusnahkan karena rusak berat |

---

## Frontend Structure

```
frontend/src/modules/showroom/
├── pages/               → 19 page components
│   ├── DashboardV2.jsx  → Main dashboard with KPIs, charts
│   ├── SampleManagement.jsx → Handover, transfer, borrow, return, adjust
│   ├── BorrowingPage.jsx → Borrowing list, extend, cancel
│   ├── GuestManagement.jsx → Guest releases CRUD
│   ├── StockControl.jsx → Opname, restock, maintenance, reservations
│   ├── LocationManagement.jsx → Location CRUD + QR codes
│   ├── StorageManagement.jsx → Storage locations tree CRUD
│   ├── ShowroomManagement.jsx → Management page (add/remove with movement type)
│   ├── ScanStorage.jsx  → QR code scanning interface
│   ├── QRGenerator.jsx  → QR code generation/bulk print
│   ├── Reporting.jsx    → Reports (KPI, movement, stock, borrowing, guest)
│   ├── MasterData.jsx   → Master data (sample_type, movement_type, location, etc.)
│   ├── Transfers.jsx    → (Legacy) Transfer list
│   ├── StockIn.jsx      → (Legacy) Stock in
│   ├── StockOut.jsx     → (Legacy) Stock out
│   ├── Stock.jsx        → (Legacy) Stock view
│   ├── Products.jsx     → (Legacy) Products
│   ├── Customers.jsx    → (Legacy) Customers
│   ├── Dashboard.jsx    → (Legacy) Dashboard
├── routes.jsx           → Route definitions (13 routes)
├── index.js             → Module index

frontend/src/layouts/
└── ShowroomLayout.jsx   → Sidebar navigation (12 nav items)

frontend/src/api/
└── services/showroomService.js → 75+ API methods
```

### Frontend Routes

| Path | Component | Description |
|------|-----------|-------------|
| `/showroom/dashboard` | DashboardV2 | Dashboard utama |
| `/showroom/samples` | SampleManagement | Manajemen sample (handover, transfer, borrow, return, adjust) |
| `/showroom/borrowings` | BorrowingPage | Daftar peminjaman |
| `/showroom/guests` | GuestManagement | Manajemen tamu |
| `/showroom/stock-control` | StockControl | Kontrol stok (opname, restock, maintenance, reservasi) |
| `/showroom/locations` | LocationManagement | Lokasi & QR Code |
| `/showroom/storage` | StorageManagement | Management penyimpanan |
| `/showroom/management` | ShowroomManagement | Management showroom (add/remove stock) |
| `/showroom/scan` | ScanStorage | Scan QR |
| `/showroom/qr-generator` | QRGenerator | Generator QR |
| `/showroom/reports` | Reporting | Pelaporan |
| `/showroom/master-data` | MasterData | Master data |

### Key Service Methods

```javascript
showroomService.getManageProducts(params)        // GET /manage
showroomService.addManageProduct(params)          // POST /manage/add
showroomService.removeManageProduct(id, params)   // DELETE /manage/{id}
showroomService.getManageReport(params)           // GET /manage/report

showroomService.getMovementTypes()                // GET /movement-types (mapped to {value, label, direction, notes})
showroomService.listMovementTypes(params)         // GET /movement-types (raw)
showroomService.createMovementType(data)          // POST /movement-types
showroomService.updateMovementType(id, data)      // PUT /movement-types/{id}
showroomService.deleteMovementType(id)            // DELETE /movement-types/{id}

showroomService.getLocations()                    // GET /samples/locations
showroomService.getAllLocations()                 // GET /samples/locations-all
showroomService.createLocation(data)              // POST /samples/locations
showroomService.updateLocation(id, data)          // PUT /samples/locations/{id}
showroomService.deleteLocation(id)                // DELETE /samples/locations/{id}

showroomService.getMasterData(params)             // GET /master-data
showroomService.createMasterData(data)            // POST /master-data
showroomService.updateMasterData(id, data)        // PUT /master-data/{id}
showroomService.deleteMasterData(id)              // DELETE /master-data/{id}
showroomService.seedMasterData()                  // POST /master-data/seed
```

---

## Database Migrations

```
alembic/versions/
├── 006f6a607183_create_movement_types_table.py       → showroom_movement_types table + seed
├── 007f7a607184_add_notes_to_movement_types.py        → notes column + seed descriptions
├── ... other migrations for showroom tables ...
```

---

## Tech Stack

- **Backend:** Python 3.14, FastAPI, SQLAlchemy 2.0, PyMySQL
- **Frontend:** React 19, Vite, Tailwind CSS, Lucide React icons
- **Database:** MySQL 8
- **Auth:** JWT bearer tokens
- **QR:** `qrcode[pil]` Python library
- **Migrations:** Alembic
