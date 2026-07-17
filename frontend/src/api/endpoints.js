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
};

export default ENDPOINTS;
