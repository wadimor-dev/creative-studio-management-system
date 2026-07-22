export const ENDPOINTS = {
  AUTH: {
    LOGIN: '/auth/login',
    PROFILE: '/auth/me',
    REFRESH: '/auth/refresh',
  },
  DASHBOARD: {
    METRICS: '/dashboard',
  },
  WORK: '/work',
  INVENTORY: {
    ITEMS: '/inventory/items',
    TRANSACTIONS: '/inventory/transactions',
  },
  SCANNER: {
    LOCATION: '/inventory/scanner/location',
    IN: '/inventory/scanner/in',
    OUT: '/inventory/scanner/out',
  },
  CATEGORIES: '/categories',
  LOCATIONS: '/locations',
  PRODUCT_MASTER: '/product-master',
  PRODUCTS: '/products',
  PRODUCT_MOVEMENTS: '/product-movements',
  PRODUCT_STOCKS: '/product-stocks',
  REPORTS: '/reports',
  USERS: {
    LIST: '/users',
    PROFILE: '/users/profile'
  },
  EXPORT: '/export',
  SHOWROOM: {
    BASE: '/showroom',
    DASHBOARD: '/showroom/dashboard',
    STOCK: '/showroom/stock',
    TRANSFERS: '/showroom/transfers',
    STOCK_IN: '/showroom/stock-in',
    STOCK_OUT: '/showroom/stock-out',
    MOVEMENTS: '/showroom/movements',
    LOCATIONS: '/showroom/locations',
  },
  SHOWROOM_V2: {
    BASE: '/showroom-v2',
    DASHBOARD: '/showroom-v2/dashboard',
    SAMPLES: {
      STOCK: '/showroom-v2/samples/stock',
      HANDOVER: '/showroom-v2/samples/handover',
      TRANSFER: '/showroom-v2/samples/transfer',
      BORROW: '/showroom-v2/samples/borrow',
      RETURN: '/showroom-v2/samples/return',
      ADJUST: '/showroom-v2/samples/adjust',
      LOCATIONS: '/showroom-v2/samples/locations',
    },
    BORROWINGS: '/showroom-v2/borrowings',
    GUESTS: '/showroom-v2/guests',
    STOCK_CONTROL: {
      OPNAME: '/showroom-v2/stock-control/opname',
      RESTOCK: '/showroom-v2/stock-control/restock',
      MAINTENANCE: '/showroom-v2/stock-control/maintenance',
      RESERVATIONS: '/showroom-v2/stock-control/reservations',
    },
    REPORTS: {
      KPI: '/showroom-v2/reports/kpi',
      MOVEMENT_SUMMARY: '/showroom-v2/reports/movement-summary',
      STOCK_BY_LOCATION: '/showroom-v2/reports/stock-by-location',
      PRODUCT_HISTORY: '/showroom-v2/reports/product-history',
      BORROWING_SUMMARY: '/showroom-v2/reports/borrowing-summary',
      GUEST_SUMMARY: '/showroom-v2/reports/guest-summary',
    },
    MASTER_DATA: '/showroom-v2/master-data',
    SAMPLES_MOVEMENTS: '/showroom-v2/samples/movements',
    LOCATIONS_ALL: '/showroom-v2/samples/locations-all',
    PUBLIC: {
      SCAN: '/showroom-v2/public/scan',
    },
    STORAGE: {
      BASE: '/showroom-v2/storage',
      TREE: '/showroom-v2/storage/tree',
      QR: '/showroom-v2/storage/qr',
    },
    QR_SCAN: {
      RESOLVE: '/showroom-v2/qr/resolve',
      STORAGE: '/showroom-v2/qr/storage-scan',
      PRODUCT: '/showroom-v2/qr/product-scan',
    },
    DASHBOARD_V2: {
      SUMMARY: '/showroom-v2/dashboard',
      MOVEMENTS: '/showroom-v2/dashboard/movements',
      HEATMAP: '/showroom-v2/dashboard/heatmap',
      TRENDS: '/showroom-v2/dashboard/analytics/trends',
      TOP_PRODUCTS: '/showroom-v2/dashboard/analytics/top-products',
      BORROWING_ANALYTICS: '/showroom-v2/dashboard/analytics/borrowing',
      SNAPSHOT: '/showroom-v2/dashboard/snapshot',
      REBUILD_SUMMARY: '/showroom-v2/dashboard/rebuild-summary',
      SUMMARY_HISTORY: '/showroom-v2/dashboard/summary-history',
    },
    MANAGE: {
      BASE: '/showroom-v2/manage',
      REPORT: '/showroom-v2/manage/report',
      MOVEMENT_TYPES: '/showroom-v2/movement-types',
    },
    MOVEMENT_TYPES: {
      BASE: '/showroom-v2/movement-types',
    },
  },
};

export default ENDPOINTS;
