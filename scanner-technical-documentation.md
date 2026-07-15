Technical Documentation: Mobile Warehouse Scanner
Dokumen ini memuat panduan teknis mendalam mengenai arsitektur, teknologi, alur kerja (workflow), serta panduan pemecahan masalah (troubleshooting) untuk fitur Scanner Gudang Mobile pada Creative Studio Management System (CSMS).

1. Ikhtisar Sistem (System Overview)
Sistem Scanner dirancang sebagai antarmuka ramah-mobile bagi operator gudang untuk melakukan operasi keluar-masuk barang (inbound/outbound/transfer) serta audit fisik (stock opname) secara langsung di lapangan menggunakan gawai (smartphone/tablet) ataupun hardware barcode scanner.

Prinsip utamanya adalah Placement-First: Operator wajib me-scan kode lokasi rak (Placement) terlebih dahulu, baru kemudian memanipulasi stok produk di dalam rak tersebut guna meminimalisir kesalahan peletakan barang (human error).

2. Technology Stack
Frontend
React.js (Vite): Framework utama untuk UI interaktif.
Tailwind CSS: Untuk tata letak (layout) dan desain responsif (dioptimalkan untuk rasio layar HP).
html5-qrcode: Library inti untuk mengakses kamera (WebRTC) ponsel guna memindai QR Code & Barcode 1D/2D tanpa hardware tambahan.
Lucide React: Ikon SVG vektor yang bersih dan modern.
Axios: HTTP Client untuk interaksi dengan backend API.
Backend
FastAPI (Python): Framework asinkron berkinerja tinggi untuk routing dan validasi.
Pydantic: Digunakan untuk memvalidasi payload JSON (misal: validasi Enum Alasan Pergerakan Barang).
SQLAlchemy: ORM (Object Relational Mapper) untuk memanipulasi stok tabel database secara transaksional.
3. Architecture & Workflow
Alur Kerja Utama (Main Workflow)
Initial Scan (Placement): Frontend mengirim kode hasil pemindaian ke GET /api/v1/product-scanner/{code}. Backend meresolusi kode tersebut dan mengembalikan tipe "placement" beserta seluruh daftar stok riil (termasuk QTY) yang ada di rak tersebut.
Product Scan: Operator memindai barcode produk. Kode dikirim ke API yang sama. Jika dikenali sebagai tipe "product", frontend akan menempatkan produk tersebut ke baris paling atas daftar layar dengan stok yang merujuk pada placement saat ini.
Execution (Movement/Opname):
Jika menekan IN/OUT/MOVE, modal akan terbuka. Setelah Submit, payload dikirim ke POST /api/v1/product-movements.
Jika menekan Audit/Opname, modal berisi matriks stok akan terbuka. Setelah Submit, daftar kuantitas fisik dikirim ke POST /api/v1/product-opname.
TIP

Preservation of State: Saat melakukan submit stok, frontend akan secara otomatis memanggil ulang API placement untuk melakukan sinkronisasi dengan database. Agar daftar UI di layar HP tidak melompat-lompat akibat pembaruan ID database, sistem mempertahankan urutan (order) kartu produk pada state lokal React.

4. Frontend Architecture
Komponen Kunci
ScannerApp.jsx: Layar utama. Bertindak sebagai pengelola status (State Manager) untuk currentPlacement, scannedItems, dan jendela modal. Memuat form input manual dan plugin kamera.
Html5QrcodePlugin.jsx: Modul wrapper kustom yang mengeksekusi kelas dasar Html5Qrcode. Modul ini mengelola izin kamera browser, menyeleksi perangkat kamera (front/rear), dan menyuntikkan video tanpa memuat gaya CSS berantakan bawaan perpustakaan pihak ketiga.
scannerService.js: Kelas utilitas Axios yang membungkus semua interaksi HTTP (resolusi kode, eksekusi pergerakan, dan eksekusi opname).
State Management
currentPlacement: Menyimpan data rak yang sedang aktif. Jika null, sistem akan menolak pendaftaran pemindaian barcode produk.
scannedItems: Array objek produk. Diisi otomatis (auto-populate) dari database saat Rak dipindai, dan dimutakhirkan (append) saat barcode produk dipindai.
actionModal: Objek yang mengendalikan tipe pop-up saat ini (IN, OUT, MOVE, OPNAME).
5. Backend Architecture
Endpoint Utama
GET /api/v1/product-scanner/{code}

File: app/api/product_scanner.py
Tujuan: Detektif kode. Mengecek secara berurutan apakah {code} tersebut merupakan kode unik Rak (ProductPlacement.code). Jika bukan, mengecek apakah itu kode SKU produk (Product.sku).
Return: JSON dengan field type (bernilai "placement" atau "product").
POST /api/v1/product-movements

File: app/api/product_movements.py -> app/services/movement_engine.py
Tujuan: Mesin penggerak (Movement Engine). Menerima spesifikasi arah pergerakan. Menggunakan blok Transaksi SQL untuk menambahkan/mengurangi tabel ProductPlacementStock, dan mencatat jejak sejarah di tabel ProductMovement.
POST /api/v1/product-opname

File: app/api/product_opname.py
Tujuan: Mesin Audit. Menerima array OpnameItem. Membandingkan actual_quantity dari payload dengan system quantity dari database.
Logika:
Jika actual > system, panggil Movement Engine untuk tipe IN dengan alasan STOCK_OPNAME.
Jika actual < system, panggil Movement Engine untuk tipe OUT dengan alasan STOCK_OPNAME.
6. Daftar Kode Error & Troubleshooting
Panduan ini ditujukan bagi Administrator Teknis jika menjumpai layar Error/Crash pada Scanner.

1. ReferenceError: [NamaKomponen] is not defined
WARNING

Error ini terjadi di level Frontend (React).

Penyebab: Terdapat typo pada impor pustaka/komponen, atau impor komponen secara tidak sengaja terhapus (misal: ikon dari lucide-react).
Solusi: Buka file ScannerApp.jsx dan pastikan nama variabel yang dilaporkan (misal MapPin, RefreshCw) tertulis jelas di blok impor baris paling atas.
2. HTTP 404 (Code not recognized)
Penyebab: Kode barcode yang di-scan tidak ditemukan di database tabel Rak (Placement) maupun tabel Produk (Product).
Solusi: Pastikan barcode dicetak melalui menu Barcode Center. Cek kembali apakah sku produk tersebut sudah terdaftar di sistem.
3. HTTP 422 Unprocessable Content
IMPORTANT

Error ini sering terjadi jika Payload (JSON) dari Frontend tidak sesuai aturan Pydantic di Backend.

Penyebab Utama di Scanner: Atribut reason (Alasan) yang dikirimkan saat menekan "Confirm IN/OUT" bukan bagian dari ProductMovementReason Enum (misal Frontend mengirim "INITIAL_STOCK", namun backend hanya menerima "RECEIVE_FROM_FACTORY").
Solusi: Samakan value string dropdown di ScannerApp.jsx dengan konfigurasi Enum pada file backend/app/models/product_movement.py.
4. HTTP 500 Internal Server Error (Crash Backend)
Penyebab: Backend mengalami Runtime Exception (seperti AttributeError atau ImportError) sebelum bisa membalas JSON.
Gejala: Aplikasi scanner frontend seolah-olah macet atau diam saja ketika melakukan scan, namun di terminal konsol backend muncul stack trace Python.
Contoh Kasus:
Mencari atribut product.name padahal nama kolom di SQLAlchemy adalah product.display_name.
Kesalahan alamat impor folder model.
Solusi: Buka terminal backend, perhatikan baris ke berapa yang menyebabkan crash, dan betulkan struktur OOP Python-nya.
5. NotAllowedError: Permission denied (Kamera Hitam)
Penyebab: Browser secara eksplisit memblokir akses webcam. Biasanya karena website diakses tanpa HTTPS (kecuali localhost), atau pengguna salah menekan "Block" pada notifikasi peramban.
Solusi: Operator wajib mengeklik ikon "Gembok" (Lock) pada URL Bar browser, pilih "Site Settings", dan izinkan "Camera". Kemudian muat ulang halaman (Refresh).