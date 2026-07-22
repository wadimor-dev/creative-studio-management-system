export const PERMISSIONS = {
  DASHBOARD: ['ADMIN', 'STAFF'],

  INVENTORY: ['ADMIN', 'STAFF'],
  INVENTORY_ITEMS: ['ADMIN', 'STAFF'],
  INVENTORY_TRANSACTIONS: ['ADMIN', 'STAFF'],

  WORK: ['ADMIN', 'CREATIVE', 'STAFF'],

  PRODUCTS: ['ADMIN', 'STAFF'],

  REPORTS: ['ADMIN', 'CREATIVE'],

  USERS: ['ADMIN'],

  SHOWROOM: ['ADMIN'],
};

export const hasPermission = (user, permission) => {
  if (!user?.roles || !Array.isArray(user.roles)) return false;
  return user.roles.some(role => PERMISSIONS[permission]?.includes(role.name));
};
