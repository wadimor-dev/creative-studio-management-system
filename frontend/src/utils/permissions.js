export const PERMISSIONS = {
  DASHBOARD: ['ADMIN', 'STAFF'],

  INVENTORY: ['ADMIN', 'CREATIVE', 'STAFF'],
  INVENTORY_ITEMS: ['ADMIN', 'CREATIVE', 'STAFF'],
  INVENTORY_TRANSACTIONS: ['ADMIN', 'CREATIVE', 'STAFF'],

  WORK: ['ADMIN', 'CREATIVE', 'STAFF'],

  PRODUCTS: ['ADMIN', 'STAFF', 'CREATIVE'],

  REPORTS: ['ADMIN'],

  USERS: ['ADMIN'],
};

export const hasPermission = (user, permission) => {
  if (!user?.role?.name) return false;

  return PERMISSIONS[permission]?.includes(user.role.name);
};