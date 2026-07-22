from app.constants.role import RoleType
from app.constants.permissions import Permission

ROLE_PERMISSIONS = {

    RoleType.ADMIN: {
        Permission.ADMIN_OVERRIDE,
        Permission.DASHBOARD_VIEW,
        Permission.REPORT_VIEW,
        Permission.REPORT_EXPORT,
        Permission.USER_VIEW,
        Permission.USER_CREATE,
        Permission.USER_UPDATE,
        Permission.USER_DELETE,
        Permission.ROLE_VIEW,
        Permission.INVENTORY_VIEW,
        Permission.INVENTORY_CREATE,
        Permission.INVENTORY_UPDATE,
        Permission.INVENTORY_DELETE,
        Permission.INVENTORY_EXPORT,
        Permission.INVENTORY_TRANSACTION_VIEW,
        Permission.INVENTORY_TRANSACTION_CREATE,
        Permission.INVENTORY_TRANSACTION_EXPORT,
        Permission.PRODUCT_VIEW,
        Permission.PRODUCT_CREATE,
        Permission.PRODUCT_UPDATE,
        Permission.PRODUCT_DELETE,
        Permission.PRODUCT_MOVEMENT_VIEW,
        Permission.PRODUCT_MOVEMENT_CREATE,
        Permission.PRODUCT_MOVEMENT_UPDATE,
        Permission.PRODUCT_MOVEMENT_DELETE,
        Permission.PRODUCT_MASTER_VIEW,
        Permission.PRODUCT_MASTER_CREATE,
        Permission.PRODUCT_MASTER_UPDATE,
        Permission.PRODUCT_MASTER_DELETE,
        Permission.PRODUCT_EXPORT,
        Permission.PRODUCT_STOCK_OPNAME,
        Permission.CATEGORY_VIEW,
        Permission.CATEGORY_CREATE,
        Permission.CATEGORY_UPDATE,
        Permission.CATEGORY_DELETE,
        Permission.LOCATION_VIEW,
        Permission.LOCATION_CREATE,
        Permission.LOCATION_UPDATE,
        Permission.LOCATION_DELETE,
        Permission.WORK_VIEW,
        Permission.WORK_CREATE,
        Permission.WORK_START,
        Permission.WORK_PAUSE,
        Permission.WORK_RESUME,
        Permission.WORK_CANCEL,
        Permission.WORK_FINISH,
        Permission.WORK_EVIDENCE_UPLOAD,
        Permission.WORK_EVIDENCE_VIEW,
        Permission.SHOWROOM_VIEW,
        Permission.SHOWROOM_CREATE,
        Permission.SHOWROOM_UPDATE,
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

        Permission.INVENTORY_TRANSACTION_VIEW,
        Permission.INVENTORY_TRANSACTION_CREATE,

        Permission.PRODUCT_VIEW,

        Permission.USER_VIEW,

        Permission.REPORT_VIEW,

        Permission.WORK_VIEW,
        Permission.WORK_CREATE,
        Permission.WORK_START,
        Permission.WORK_PAUSE,
        Permission.WORK_RESUME,
        Permission.WORK_CANCEL,
        Permission.WORK_FINISH,

        Permission.WORK_EVIDENCE_UPLOAD,
        Permission.WORK_EVIDENCE_VIEW,

        Permission.CATEGORY_VIEW,
        Permission.CATEGORY_CREATE,
        Permission.CATEGORY_UPDATE,
        Permission.CATEGORY_DELETE,
    },

    RoleType.MANAGER: {
        Permission.DASHBOARD_VIEW,
        Permission.REPORT_VIEW,
        Permission.REPORT_EXPORT,
        Permission.INVENTORY_VIEW,
        Permission.INVENTORY_TRANSACTION_VIEW,
        Permission.PRODUCT_VIEW,
        Permission.PRODUCT_MOVEMENT_VIEW,
        Permission.SHOWROOM_VIEW,
        Permission.WORK_VIEW,
        Permission.CATEGORY_VIEW,
        Permission.LOCATION_VIEW,
    },

}