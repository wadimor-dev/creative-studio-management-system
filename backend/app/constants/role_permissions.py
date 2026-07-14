from app.constants.role import RoleType
from app.constants.permissions import Permission

ROLE_PERMISSIONS = {

    RoleType.ADMIN: {

        Permission.DASHBOARD_VIEW,

        Permission.INVENTORY_VIEW,
        Permission.INVENTORY_CREATE,
        Permission.INVENTORY_UPDATE,
        Permission.INVENTORY_DELETE,

        Permission.INVENTORY_TRANSACTION_VIEW,
        Permission.INVENTORY_TRANSACTION_CREATE,

        Permission.PRODUCT_VIEW,
        Permission.PRODUCT_CREATE,
        Permission.PRODUCT_UPDATE,
        Permission.PRODUCT_DELETE,

        Permission.USER_VIEW,
        Permission.USER_CREATE,
        Permission.USER_UPDATE,
        Permission.USER_DELETE,

        Permission.ROLE_VIEW,

        Permission.REPORT_VIEW,
    },

    RoleType.STAFF: {

        Permission.DASHBOARD_VIEW,

        Permission.INVENTORY_VIEW,
        Permission.INVENTORY_TRANSACTION_VIEW,
        Permission.INVENTORY_TRANSACTION_CREATE,

        Permission.PRODUCT_VIEW,
    },

    RoleType.CREATIVE: {

        Permission.DASHBOARD_VIEW,

        Permission.INVENTORY_VIEW,
        Permission.INVENTORY_CREATE,
        Permission.INVENTORY_UPDATE,
        Permission.INVENTORY_DELETE,

        Permission.PRODUCT_VIEW,

        Permission.USER_VIEW,

        Permission.REPORT_VIEW,
    },

}