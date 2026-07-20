# ALUR KERJA MODUL SHOWROOM V2

## 1. KONSEP DASAR

Showroom dimulai **setelah barang keluar dari Inventory**. Setiap sample memiliki lokasi, tipe sample (Display/Photography/Premium/Archive), dan setiap perubahan menghasilkan **movement** (audit trail).

```
Inventory (Gudang Utama)
        │
        ▼ HANDOVER (event-driven)
┌─────────────────────────────────────────────────┐
│                   SHOWROOM                       │
│                                                  │
│  Showroom Utama ◄──► Display Area               │
│  (Display)           (Photography)               │
│       ▲                   ▲                      │
│       │    TRANSFER       │                      │
│       ▼                   ▼                      │
│  Guest Release        Borrowing                  │
│  (Draft→Approve)     (Langsung BORROWED)         │
│                                                  │
│  Stock Opname ◄─── Koreksi via Movement          │
│  Restock ◄──────── Auto/Manual Request           │
│  Maintenance ◄──── Cleaning/Repair/Retired       │
│                                                  │
│  Master Data ◄──── Konfigurasi semua referensi   │
└─────────────────────────────────────────────────┘
```

---

## 2. ALUR PERDOMAIN

### DOMAIN A: SAMPLE MANAGEMENT

#### A1. HANDOVER (Event-Driven Integration)
```
Inventory → Issue Sample → Event → Showroom menerima → Tambah stok
```
- **Input**: product_id, quantity, to_location_id, sample_type, purpose
- **Aksi**: Buat HANDOVER movement + update/create showroom_sample_stocks
- **Design**: Integration point — Mobile App/ERP lain bisa trigger tanpa ubah Showroom

#### A2. TRANSFER (Pindah Lokasi)
```
Showroom Utama ◄──► Display Area
```
- **Input**: product_id, from_location_id, to_location_id, quantity, sample_type, purpose
- **Aksi**: Buat TRANSFER movement + kurangi stok di source, tambah di dest

#### A3. BORROW (Pinjam Internal — LANGSUNG)
```
Showroom ──Borrow──► Peminjam (BORROWED langsung)
```
- **Input**: product_id, from_location_id, quantity, borrower_name, sample_type, purpose
- **Aksi**: Buat BORROW movement + kurangi stok + buat borrowing record (status: BORROWED)
- **TANPA APPROVAL** — Langsung BORROWED. Approval hanya memperlambat kerja.

#### A4. RETURN (Kembalikan)
```
BORROWED ──Return──► Stok kembali
```
- **Input**: borrowing_id, location_id
- **Aksi**: Buat RETURN movement + tambah stok + update borrowing status RETURNED

---

### DOMAIN B: BORROWING (Peminjaman)

Status flow:
```
BORROWED ──► RETURNED
    │
    └──► CANCELLED
```

- **Borrow**: Langsung BORROWED (tidak ada PENDING/APPROVE)
- **Extend**: Update expected_return_date
- **Cancel**: Kembalikan stok + buat RETURN movement + status CANCELLED

---

### DOMAIN C: GUEST MANAGEMENT (Manajemen Tamu)

Status flow:
```
DRAFT ──Approve──► APPROVED (stok berkurang)
    │
    └──Reject──► REJECTED (stok tidak berubah)
```

**KRITIS**: Stok hanya berubah SAAT APPROVE, bukan saat CREATE.

#### C1. CREATE RELEASE (Draft)
```
Input data → Status DRAFT → Stok TIDAK berubah
```

#### C2. APPROVE RELEASE
```
DRAFT → APPROVED → Buat RELEASE movement → Stok berkurang
```
- **Input**: release_id
- **Aksi**: Cek stok cukup → Buat movement → Kurangi stok → Set APPROVED

#### C3. REJECT RELEASE
```
DRAFT → REJECTED → Stok tidak berubah
```
- **Input**: release_id, reason

#### C4. RETURN FROM GUEST
```
APPROVED → RETURNED → Buat RETURN movement → Stok bertambah
```

---

### DOMAIN D: STOCK CONTROL

#### D1. STOCK OPname
```
Draft → In Progress → Completed (adjustment movements) → Approved
```
- Session → Input items → Hitung variance → Buat ADJUSTMENT movements → Approve

#### D2. RESTOCK REQUEST
```
Auto Suggest (stok < minimum) ATAU Manual Request (manager butuh tambah display)
→ PENDING → APPROVED → Handover dari inventory
```
- Source: `auto` atau `manual`
- Tidak terikat hanya stok < minimum

#### D3. MAINTENANCE
```
PENDING → IN_PROGRESS → COMPLETED
                │
                └── RETIRED (sample tidak layak)
```
- Types: CLEANING, REPAIR, LAUNDRY, RETIRED, OTHER
- **RETIRED**: Sample dihapus dari peredaran + buat RETIRED movement

---

### DOMAIN E: REPORTING

Dashboard KPI:
- **Total Sample**: Semua sample di showroom
- **At Showroom**: Sample yang ada di showroom (bukan borrowed/released)
- **Borrowed**: Sedang dipinjam
- **Released This Month**: Dirilis ke tamu bulan ini
- **Maintenance**: Sedang dalam perawatan
- **Retired**: Sample yang sudah tidak layak
- **Need Restock**: Request restok pending
- **Overdue Borrowing**: Peminjaman lewat waktu
- **Top Borrowed Product**: Produk paling sering dipinjam
- **Top Released Product**: Produk paling sering dirilis

---

### DOMAIN F: MASTER DATA

Semua referensi bisa dikonfigurasi:
- **Sample Type**: Display, Photography, Premium, Archive
- **Maintenance Type**: Cleaning, Repair, Laundry, Retired, Other
- **Purpose**: Display, Photography, Shooting, Exhibition, dll
- **Borrow Reason**: Internal Display, Photography, Client Preview
- **Release Reason**: Client Sampling, Exhibition, Marketing
- **Location Type**: Internal, External

---

## 3. PRINSIP PENTING

### Movement = Pusat Sistem
```
SEMUA operasi menghasilkan movement:
- Handover → HANDOVER movement
- Transfer → TRANSFER movement
- Borrow → BORROW movement
- Return → RETURN movement
- Guest Release → RELEASE movement
- Opname Adjustment → ADJUSTMENT movement
- Maintenance Out → MAINTENANCE_OUT movement
- Maintenance Return → MAINTENANCE_RETURN movement
- Retired → RETIRED movement
```

### Sample Stock = Derivat Movement
```
JANGAN pernah input stok manual.
Stock selalu UPDATE dari movement.
- Handover → stock bertambah
- Transfer → stock pindah
- Borrow → stock berkurang
- Return → stock bertambah
- Guest Release → stock berkurang
```

### Sample Type
```
Satu produk bisa punya banyak sample:
- Sarung Batik A → Display: 5 pcs
- Sarung Batik A → Photography: 2 pcs
- Sarung Batik A → Premium: 1 pcs
```

---

## 4. DATABASE

### Tabel Utama
| Tabel | Fungsi |
|-------|--------|
| showroom_master_data | Referensi konfigurable |
| showroom_locations | Lokasi showroom |
| showroom_sample_stocks | Stok sample (derivative dari movement) |
| showroom_movements | Audit trail semua pergerakan |
| showroom_borrowings | Peminjaman internal |
| showroom_guest_releases | Rilis ke tamu (draft→approve) |
| showroom_opname_sessions | Session opname |
| showroom_opname_items | Item opname |
| showroom_restock_requests | Request restok (auto/manual) |
| showroom_maintenance | Perawatan sample |
| showroom_reservations | Reservasi sample |
| showroom_barcode_scans | Log scan barcode |

---

## 5. ENDPOINTS

| Domain | Method | Endpoint | Fungsi |
|--------|--------|----------|--------|
| **Master Data** | GET | `/master-data` | Daftar master data |
| | GET | `/master-data/types` | Daftar tipe valid |
| | POST | `/master-data` | Buat master data |
| | PUT | `/master-data/{id}` | Update master data |
| | DELETE | `/master-data/{id}` | Hapus master data |
| | POST | `/master-data/seed` | Seed default values |
| **Sample** | GET | `/samples/stock` | Stok per lokasi/tipe |
| | POST | `/samples/handover` | Handover dari inventory |
| | POST | `/samples/transfer` | Pindah lokasi |
| | POST | `/samples/borrow` | Pinjam (langsung BORROWED) |
| | POST | `/samples/return/{id}` | Kembalikan sample |
| | POST | `/samples/adjust` | Adjust manual |
| | GET | `/samples/locations` | Daftar lokasi |
| | GET | `/samples/movements` | Histori pergerakan |
| **Borrowing** | GET | `/borrowings` | Daftar peminjaman |
| | GET | `/borrowings/overdue` | Peminjaman lewat waktu |
| | GET | `/borrowings/stats` | Statistik peminjaman |
| | POST | `/borrowings/{id}/extend` | Perpanjang |
| | POST | `/borrowings/{id}/cancel` | Batalkan |
| **Guest** | GET | `/guests` | Daftar rilis tamu |
| | GET | `/guests/stats` | Statistik |
| | POST | `/guests` | Buat draft rilis |
| | POST | `/guests/{id}/approve` | Setujui (stok berkurang) |
| | POST | `/guests/{id}/reject` | Tolak |
| | POST | `/guests/{id}/return` | Kembalikan dari tamu |
| **Stock Control** | GET/POST | `/stock-control/opname` | Opname sessions |
| | POST | `/stock-control/opname/{id}/items` | Input item |
| | POST | `/stock-control/opname/{id}/complete` | Selesaikan |
| | POST | `/stock-control/opname/{id}/approve` | Setujui |
| | GET/POST | `/stock-control/restock` | Restock requests |
| | POST | `/stock-control/restock/{id}/approve` | Setujui restok |
| | GET/POST | `/stock-control/maintenance` | Maintenance |
| | POST | `/stock-control/maintenance/{id}/complete` | Selesaikan |
| **Reports** | GET | `/reports/kpi` | Dashboard KPI |
| | GET | `/reports/movement-summary` | Ringkasan pergerakan |
| | GET | `/reports/stock-by-location` | Stok per lokasi |
| | GET | `/reports/borrowing-summary` | Ringkasan peminjaman |
| | GET | `/reports/guest-summary` | Ringkasan rilis tamu |
| | GET | `/reports/product-history/{id}` | Histori produk |
