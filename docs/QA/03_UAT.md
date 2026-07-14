# User Acceptance Test (UAT) Checklist

## Skenario 1: Editor (Role: STAFF)
- [ ] Login ke sistem.
- [ ] Buka halaman `Work Activity Workspace`.
- [ ] Buat aktivitas baru "Edit Video Promosi".
- [ ] Ambil foto `BEFORE` (meja kerja).
- [ ] Klik tombol `START` (status berubah menjadi WORKING).
- [ ] Ambil foto `PROGRESS` di pertengahan jalan.
- [ ] Selesaikan pekerjaan, ambil foto `AFTER`.
- [ ] Klik `FINISH` (status berubah menjadi COMPLETED).

## Skenario 2: Photographer (Role: STAFF)
- [ ] Login ke sistem.
- [ ] Buka `Work Activity Workspace` dan buat aktivitas "Sesi Foto Model".
- [ ] Pinjam Aset (Kamera & Lensa) melalui tab `Assets`. Stok barang akan berkurang.
- [ ] Ambil foto `BEFORE` dan mulai pekerjaan (`START`).
- [ ] Setelah selesai, ambil foto `AFTER` dan selesaikan pekerjaan (`FINISH`).
- [ ] Verifikasi bahwa aset (Kamera & Lensa) secara otomatis kembali dan stok bertambah kembali normal.

## Skenario 3: Manager / Administrator
- [ ] Login ke sistem.
- [ ] Buka halaman `Dashboard`. Verifikasi metrik (Tugas selesai hari ini, jam kerja aktif, aset dipinjam) berjalan mulus.
- [ ] Buka halaman `Analytics & Reports`.
- [ ] Lakukan filter data (periode mingguan, spesifik karyawan).
- [ ] Buka bukti foto (Klik ikon Evidence) untuk memvalidasi *audit trail*.
- [ ] Klik tombol `Export as PDF` dan `Export as Excel`.
- [ ] Verifikasi bahwa dokumen PDF dan Excel memiliki header profesional, Summary, dan total baris sesuai dengan data di layar.
- [ ] Verifikasi di halaman `Inventory` bahwa stok akurat dan log peminjaman aset tampil di `Transaction History`.

---
**Tanda Tangan Penguji (UAT Sign-off):**

Tanggal : _______________  
Nama    : _______________  
Status  : [ ] LULUS / [ ] GAGAL
