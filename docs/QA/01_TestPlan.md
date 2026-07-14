# Test Plan (WA-08)

## 1. Tujuan
Memastikan seluruh komponen dan alur dari Creative Studio Management System (CSMS) berfungsi sesuai desain arsitektur yang sudah di-*freeze*. 
Test ini bukan untuk mencoba fitur baru, melainkan menstabilkan rilis kandidat menuju ke *Production*.

## 2. Cakupan (Scope)
- **Modul**: Authentication, Users, Inventory, Work Activity, Assets, Dashboard, Reports, Export.
- **Tipe Tes**: 
  - Unit Test (Repositori, Service)
  - Integration Test (E2E alur pembuatan hingga laporan)
  - Data Integrity (Konsistensi Stok)
  - Security (Role based authorization, JWT)
  - Performance (Latency Benchmark)

## 3. Strategi
- `pytest` beserta `TestClient` akan digunakan sebagai *Test Runner* utama yang dijalankan di *Continuous Integration* sebelum perilisan.
- `Postman` dengan file `CSMS_API_Collection.json` digunakan untuk eksplorasi manual dan validasi endpoint tambahan.
- Tes regresi (pengulangan test suite) wajib dilakukan saat ditemukan dan diselesaikannya *bug*.

## 4. Kriteria Kelulusan (Pass Criteria)
- Seluruh *test cases* di-pass (hijau).
- Ekspor PDF & Excel bekerja tanpa *memory leak* dan mendukung pembatasan row data (2000 & 10000).
- Tidak ada *debug code* atau *log* yang tersisa di *production build*.
