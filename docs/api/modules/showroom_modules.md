Dokumentasi API Modul Showroom
Deskripsi
Modul showroom (showroom_v2) adalah modul yang digunakan untuk mengelola stok produk di showroom. Modul ini menyediakan berbagai endpoint API untuk mengakses dan mengelola data showroom, termasuk pengelolaan stok, pengiriman, peminjaman, pengembalian, dan lainnya.

Struktur Modul
Struktur modul showroom terdiri dari beberapa komponen utama, yaitu:

Routes: Komponen ini berisi definisi endpoint API untuk setiap fungsi yang tersedia di modul showroom.
Services: Komponen ini berisi implementasi logika bisnis untuk setiap fungsi yang tersedia di modul showroom.
Schemas: Komponen ini berisi definisi model data yang digunakan oleh modul showroom.
Endpoint API
Berikut ini adalah daftar endpoint API yang tersedia di modul showroom:

Endpoint CRUD
Endpoint	Metode	Deskripsi
/showroom_v2/samples	GET	Mengambil daftar sample
/showroom_v2/samples/{id}	GET	Mengambil detail sample berdasarkan ID
/showroom_v2/samples	POST	Menambahkan sample baru
/showroom_v2/samples/{id}	PUT	Memperbarui detail sample berdasarkan ID
/showroom_v2/samples/{id}	DELETE	Menghapus sample berdasarkan ID
Endpoint Handover
Endpoint	Metode	Deskripsi
/showroom_v2/samples/{id}/handover	POST	Melakukan handover sample berdasarkan ID
Endpoint Transfer
Endpoint	Metode	Deskripsi
/showroom_v2/transfers	POST	Menambahkan transfer baru
/showroom_v2/transfers/{id}	PUT	Memperbarui detail transfer berdasarkan ID
/showroom_v2/transfers/{id}	DELETE	Menghapus transfer berdasarkan ID
Endpoint Borrowing
Endpoint	Metode	Deskripsi
/showroom_v2/borrowings	POST	Menambahkan peminjaman baru
/showroom_v2/borrowings/{id}	PUT	Memperbarui detail peminjaman berdasarkan ID
/showroom_v2/borrowings/{id}	DELETE	Menghapus peminjaman berdasarkan ID
Endpoint Guest Release
Endpoint	Metode	Deskripsi
/showroom_v2/guests/{id}/release	POST	Menyelesaikan pengembalian tamu berdasarkan ID
Endpoint Stock Control
Endpoint	Metode	Deskripsi
/showroom_v2/stock-control/opname	POST	Menambahkan opname baru
/showroom_v2/stock-control/opname/{id}	PUT	Memperbarui detail opname berdasarkan ID
/showroom_v2/stock-control/opname/{id}	DELETE	Menghapus opname berdasarkan ID
/showroom_v2/stock-control/restock	POST	Menambahkan restock baru
/showroom_v2/stock-control/maintenance	POST	Menambahkan maintenance baru
/showroom_v2/stock-control/reservations	POST	Menambahkan reservasi baru
Endpoint Reporting
Endpoint	Metode	Deskripsi
/showroom_v2/reports/kpi	GET	Mengambil laporan KPI
/showroom_v2/reports/movement-summary	GET	Mengambil laporan ringkasan pergerakan stok
/showroom_v2/reports/stock-by-location	GET	Mengambil laporan stok berdasarkan lokasi
/showroom_v2/reports/product-history	GET	Mengambil laporan riwayat produk
Endpoint Master Data
Endpoint	Metode	Deskripsi
/showroom_v2/master-data/sample-types	GET	Mengambil daftar jenis sample
/showroom_v2/master-data/sample-types	POST	Menambahkan jenis sample baru
/showroom_v2/master-data/sample-types/{id}	PUT	Memperbarui jenis sample berdasarkan ID
/showroom_v2/master-data/sample-types/{id}	DELETE	Meng