export const ENDPOINTS = {
  AUTH: {
    LOGIN: '/auth/login',
    PROFILE: '/auth/me',
    REFRESH: '/auth/refresh',
  },
  DASHBOARD: {
    METRICS: '/dashboard',
  },
  INVENTORY: {
    ITEMS: '/inventory/items',
    TRANSACTIONS: '/inventory/transactions',
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
};

export default ENDPOINTS;
