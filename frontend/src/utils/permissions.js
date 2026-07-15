export const PERMISSIONS = {
  DASHBOARD: ['ADMIN', 'STAFF'],

  INVENTORY: ['ADMIN', 'STAFF'],
  INVENTORY_ITEMS: ['ADMIN', 'STAFF'],
  INVENTORY_TRANSACTIONS: ['ADMIN', 'STAFF'],

  WORK: ['ADMIN', 'CREATIVE', 'STAFF'],

  PRODUCTS: ['ADMIN', 'STAFF'],

  REPORTS: ['ADMIN', 'CREATIVE'],

  USERS: ['ADMIN'],
};

export const hasPermission = (user, permission) => {
  if (!user?.role?.name) return false;

  return PERMISSIONS[permission]?.includes(user.role.name);
};