from app.models.role import Role
from app.models.category import Category
from app.models.unit import Unit
from app.models.location import Location
from app.models.user import User
from app.models.item import Item
from app.models.inventory_transaction import InventoryTransaction
from app.models.product_master import ProductType, ProductCategory, ProductMotif, ProductSubMotif, ProductColor
from app.models.product import Product
from app.models.product_movement import ProductMovement
from app.models.product_stock import ProductPlacementStock
from app.models.product_placement import PlacementType, ProductPlacement

# This ensures all models are imported when `app.models` is imported.
from app.models.item_stock import ItemStock
from app.models.division import Division
from app.models.work_category import WorkCategory
from app.models.work_activity import WorkActivity, WorkActivityStatus
from app.models.work_evidence import WorkEvidence

from app.models.work_asset import WorkAsset

from .export_log import ExportLog
from .activity_log import ActivityLog
from .audit_log import AuditLog

# Showroom Models
from app.models.showroom_master_data import ShowroomMasterData
from app.models.showroom_location import ShowroomLocation
from app.models.showroom_sample_stock import ShowroomSampleStock
from app.models.showroom_movement import ShowroomMovement, ShowroomMovementType
from app.models.showroom_borrowing import ShowroomBorrowing
from app.models.showroom_guest_release import ShowroomGuestRelease
from app.models.showroom_opname import ShowroomOpnameSession
from app.models.showroom_opname_item import ShowroomOpnameItem
from app.models.showroom_restock import ShowroomRestockRequest
from app.models.showroom_reservation import ShowroomReservation
from app.models.showroom_maintenance import ShowroomMaintenance
from app.models.showroom_barcode_scan import ShowroomBarcodeScan
from app.models.showroom_storage_location import ShowroomStorageLocation
from app.models.showroom_qr_entity import ShowroomQREntity
from app.models.showroom_activity_log import ShowroomActivityLog
from app.models.showroom_storage_snapshot import ShowroomStorageSnapshot
from app.models.showroom_daily_storage_summary import ShowroomDailyStorageSummary
from app.models.showroom_permission import ShowroomPermission, ShowroomRole, ShowroomUserRole
