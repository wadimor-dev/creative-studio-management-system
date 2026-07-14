from enum import Enum

class Permission(str, Enum):

     DASHBOARD_VIEW = "dashboard.view"

    REPORT_VIEW = "report.view"
    REPORT_EXPORT = "report.export"

    USER_VIEW = "user.view"
    USER_CREATE = "user.create"
    USER_UPDATE = "user.update"
    USER_DELETE = "user.delete"

    ROLE_VIEW = "role.view"

    INVENTORY_VIEW = "inventory.view"
    INVENTORY_CREATE = "inventory.create"
    INVENTORY_UPDATE = "inventory.update"
    INVENTORY_DELETE = "inventory.delete"

    INVENTORY_EXPORT = "inventory.export"

    INVENTORY_TRANSACTION_VIEW = "inventory.transaction.view"
    INVENTORY_TRANSACTION_CREATE = "inventory.transaction.create"
    INVENTORY_TRANSACTION_EXPORT = "inventory.transaction.export"

    PRODUCT_VIEW = "product.view"
    PRODUCT_CREATE = "product.create"
    PRODUCT_UPDATE = "product.update"
    PRODUCT_DELETE = "product.delete"

    PRODUCT_EXPORT = "product.exportn