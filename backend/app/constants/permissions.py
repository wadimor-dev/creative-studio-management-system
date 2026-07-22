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

    PRODUCT_MOVEMENT_VIEW = "product.movement.view"
    PRODUCT_MOVEMENT_CREATE = "product.movement.create"
    PRODUCT_MOVEMENT_UPDATE = "product.movement.update"
    PRODUCT_MOVEMENT_DELETE = "product.movement.delete"

    PRODUCT_MASTER_VIEW = "product.master.view"
    PRODUCT_MASTER_CREATE = "product.master.create"
    PRODUCT_MASTER_UPDATE = "product.master.update"
    PRODUCT_MASTER_DELETE = "product.master.delete"

    PRODUCT_EXPORT = "product.export"

    PRODUCT_STOCK_OPNAME = "product.stock.opname"

    CATEGORY_VIEW = "category.view"
    CATEGORY_CREATE = "category.create"
    CATEGORY_UPDATE = "category.update"
    CATEGORY_DELETE = "category.delete"

    LOCATION_VIEW = "location.view"
    LOCATION_CREATE = "location.create"
    LOCATION_UPDATE = "location.update"
    LOCATION_DELETE = "location.delete"

    WORK_VIEW = "work.view"
    WORK_CREATE = "work.create"
    WORK_START = "work.start"
    WORK_PAUSE = "work.pause"
    WORK_RESUME = "work.resume"
    WORK_CANCEL = "work.cancel"
    WORK_FINISH = "work.finish"

    WORK_EVIDENCE_UPLOAD = "work.evidence.upload"
    WORK_EVIDENCE_VIEW = "work.evidence.view"

    SHOWROOM_VIEW = "showroom.view"
    SHOWROOM_CREATE = "showroom.create"
    SHOWROOM_UPDATE = "showroom.update"

    EMPLOYEE_VIEW = "employee.view"
    EMPLOYEE_CREATE = "employee.create"
    EMPLOYEE_UPDATE = "employee.update"
    EMPLOYEE_DELETE = "employee.delete"
    EMPLOYEE_EXPORT = "employee.export"
    EMPLOYEE_IMPORT = "employee.import"
    EMPLOYEE_RESTORE = "employee.restore"
    EMPLOYEE_AUDIT = "employee.audit"
    EMPLOYEE_DOCUMENT = "employee.document"
    EMPLOYEE_HISTORY = "employee.history"
    EMPLOYEE_FAMILY = "employee.family"
    EMPLOYEE_CONTRACT = "employee.contract"
    EMPLOYEE_SALARY = "employee.salary"
    EMPLOYEE_ASSET = "employee.asset"
    EMPLOYEE_SKILL = "employee.skill"
    EMPLOYEE_CERTIFICATION = "employee.certification"
    EMPLOYEE_SHIFT = "employee.shift"

    ORGANIZATION_VIEW = "organization.view"
    ORGANIZATION_CREATE = "organization.create"
    ORGANIZATION_UPDATE = "organization.update"
    ORGANIZATION_DELETE = "organization.delete"

    JOB_LEVEL_VIEW = "job_level.view"
    JOB_LEVEL_CREATE = "job_level.create"
    JOB_LEVEL_UPDATE = "job_level.update"
    JOB_LEVEL_DELETE = "job_level.delete"

    BANK_VIEW = "bank.view"
    BANK_CREATE = "bank.create"
    BANK_UPDATE = "bank.update"
    BANK_DELETE = "bank.delete"

    ADMIN_OVERRIDE = "admin.override"
