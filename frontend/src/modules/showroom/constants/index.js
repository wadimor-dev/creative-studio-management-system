export const MOVEMENT_TYPE = {
  HANDOVER: 'HANDOVER',
  TRANSFER: 'TRANSFER',
  BORROW: 'BORROW',
  RETURN: 'RETURN',
  RELEASE: 'RELEASE',
  ADJUSTMENT: 'ADJUSTMENT',
};

export const MOVEMENT_STATUS = {
  COMPLETED: 'completed',
  PENDING: 'pending',
  CANCELLED: 'cancelled',
};

export const LOCATION_TYPE = {
  INTERNAL: 'internal',
  EXTERNAL: 'external',
};

export const BORROWING_STATUS = {
  PENDING: 'PENDING',
  BORROWED: 'BORROWED',
  RETURNED: 'RETURNED',
  CANCELLED: 'CANCELLED',
};

export const GUEST_RELEASE_STATUS = {
  PENDING: 'pending',
  APPROVED: 'approved',
};

export const OPNAME_STATUS = {
  DRAFT: 'draft',
  IN_PROGRESS: 'in_progress',
  COMPLETED: 'completed',
  APPROVED: 'approved',
};

export const RESTOCK_STATUS = {
  PENDING: 'PENDING',
  APPROVED: 'APPROVED',
  COMPLETED: 'COMPLETED',
  CANCELLED: 'CANCELLED',
};

export const MAINTENANCE_TYPE = {
  LAUNDRY: 'LAUNDRY',
  REPAIR: 'REPAIR',
  CLEANING: 'CLEANING',
  OTHER: 'OTHER',
};

export const MAINTENANCE_STATUS = {
  PENDING: 'PENDING',
  IN_PROGRESS: 'IN_PROGRESS',
  COMPLETED: 'COMPLETED',
};

export const RESERVATION_STATUS = {
  ACTIVE: 'ACTIVE',
  CANCELLED: 'CANCELLED',
  COMPLETED: 'COMPLETED',
};

export const TYPE_VARIANT = {
  [MOVEMENT_TYPE.HANDOVER]: 'success',
  [MOVEMENT_TYPE.TRANSFER]: 'info',
  [MOVEMENT_TYPE.BORROW]: 'warning',
  [MOVEMENT_TYPE.RETURN]: 'secondary',
  [MOVEMENT_TYPE.RELEASE]: 'danger',
  [MOVEMENT_TYPE.ADJUSTMENT]: 'primary',
};

export const STATUS_VARIANT = {
  [MOVEMENT_STATUS.COMPLETED]: 'success',
  [MOVEMENT_STATUS.PENDING]: 'warning',
  [MOVEMENT_STATUS.CANCELLED]: 'danger',
  [BORROWING_STATUS.BORROWED]: 'warning',
  [BORROWING_STATUS.RETURNED]: 'success',
  [BORROWING_STATUS.PENDING]: 'info',
  [OPNAME_STATUS.DRAFT]: 'secondary',
  [OPNAME_STATUS.IN_PROGRESS]: 'warning',
  [OPNAME_STATUS.COMPLETED]: 'success',
  [OPNAME_STATUS.APPROVED]: 'primary',
};

export const TYPE_LABEL = {
  [MOVEMENT_TYPE.HANDOVER]: 'Handover',
  [MOVEMENT_TYPE.TRANSFER]: 'Transfer',
  [MOVEMENT_TYPE.BORROW]: 'Pinjam',
  [MOVEMENT_TYPE.RETURN]: 'Kembali',
  [MOVEMENT_TYPE.RELEASE]: 'Release',
  [MOVEMENT_TYPE.ADJUSTMENT]: 'Penyesuaian',
};

export const STATUS_LABEL = {
  [MOVEMENT_STATUS.COMPLETED]: 'Selesai',
  [MOVEMENT_STATUS.PENDING]: 'Pending',
  [MOVEMENT_STATUS.CANCELLED]: 'Dibatalkan',
  [BORROWING_STATUS.BORROWED]: 'Dipinjam',
  [BORROWING_STATUS.RETURNED]: 'Dikembalikan',
  [BORROWING_STATUS.PENDING]: 'Menunggu Persetujuan',
  [BORROWING_STATUS.CANCELLED]: 'Dibatalkan',
  [OPNAME_STATUS.DRAFT]: 'Draft',
  [OPNAME_STATUS.IN_PROGRESS]: 'Berlangsung',
  [OPNAME_STATUS.COMPLETED]: 'Selesai',
  [OPNAME_STATUS.APPROVED]: 'Disetujui',
};

export const MAINTENANCE_TYPE_LABEL = {
  [MAINTENANCE_TYPE.LAUNDRY]: 'Laundry',
  [MAINTENANCE_TYPE.REPAIR]: 'Reparasi',
  [MAINTENANCE_TYPE.CLEANING]: 'Pembersihan',
  [MAINTENANCE_TYPE.OTHER]: 'Lainnya',
};

export const DOMAIN_TABS = [
  { id: 'sample', label: 'Sample Management' },
  { id: 'borrowing', label: 'Peminjaman' },
  { id: 'guest', label: 'Manajemen Tamu' },
  { id: 'stock-control', label: 'Kontrol Stok' },
  { id: 'reporting', label: 'Pelaporan' },
];

export const PURPOSE_OPTIONS = [
  { value: 'Display Baru', label: 'Display Baru' },
  { value: 'Cek Warna', label: 'Cek Warna' },
  { value: 'Shooting', label: 'Shooting' },
  { value: 'Foto Katalog', label: 'Foto Katalog' },
  { value: 'Pameran', label: 'Pameran' },
  { value: 'Lainnya', label: 'Lainnya' },
];

export const LOCATION_TYPE_OPTIONS = [
  { value: LOCATION_TYPE.INTERNAL, label: 'Internal' },
  { value: LOCATION_TYPE.EXTERNAL, label: 'Eksternal' },
];

export const BORROWING_STATUS_FILTER = [
  { value: 'all', label: 'Semua' },
  { value: BORROWING_STATUS.PENDING, label: 'Menunggu' },
  { value: BORROWING_STATUS.BORROWED, label: 'Dipinjam' },
  { value: BORROWING_STATUS.RETURNED, label: 'Dikembalikan' },
  { value: BORROWING_STATUS.CANCELLED, label: 'Dibatalkan' },
];

export const OPNAME_STATUS_FILTER = [
  { value: 'all', label: 'Semua' },
  { value: OPNAME_STATUS.DRAFT, label: 'Draft' },
  { value: OPNAME_STATUS.IN_PROGRESS, label: 'Berlangsung' },
  { value: OPNAME_STATUS.COMPLETED, label: 'Selesai' },
  { value: OPNAME_STATUS.APPROVED, label: 'Disetujui' },
];

export const RESTOCK_STATUS_FILTER = [
  { value: 'all', label: 'Semua' },
  { value: RESTOCK_STATUS.PENDING, label: 'Menunggu' },
  { value: RESTOCK_STATUS.APPROVED, label: 'Disetujui' },
  { value: RESTOCK_STATUS.COMPLETED, label: 'Selesai' },
];

export const LOCATION_OPTIONS = [
  { value: 'SHOWROOM', label: 'Showroom Utama' },
  { value: 'DISPLAY', label: 'Area Display' },
  { value: 'WAREHOUSE', label: 'Gudang' },
  { value: 'BACKSTAGE', label: 'Backstage' },
];

export const SUPPLIER_OPTIONS = [
  { value: 'Supplier A', label: 'Supplier A' },
  { value: 'Supplier B', label: 'Supplier B' },
  { value: 'Supplier C', label: 'Supplier C' },
];

export const PRODUCT_OPTIONS = [
  { value: 'Kain Batik Motif X', label: 'Kain Batik Motif X' },
  { value: 'Songket Palembang', label: 'Songket Palembang' },
  { value: 'Tenun Ikat Flores', label: 'Tenun Ikat Flores' },
  { value: 'Ulos Batak', label: 'Ulos Batak' },
  { value: 'Lurik Jogja', label: 'Lurik Jogja' },
];

export const REASON_OPTIONS = [
  { value: 'Habis Terjual', label: 'Habis Terjual' },
  { value: 'Dikembalikan', label: 'Dikembalikan' },
  { value: 'Rusak', label: 'Rusak' },
  { value: 'Lainnya', label: 'Lainnya' },
];
