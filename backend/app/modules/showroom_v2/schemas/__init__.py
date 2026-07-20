from typing import Optional, List, Union
from pydantic import BaseModel


class MasterDataCreate(BaseModel):
    type: str
    name: str
    value: str
    description: Optional[str] = None
    sort_order: Optional[int] = 0


class MasterDataUpdate(BaseModel):
    name: Optional[str] = None
    value: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None


class MasterDataResponse(BaseModel):
    id: int
    type: str
    name: str
    value: str
    description: Optional[str] = None
    is_active: bool
    sort_order: int

    class Config:
        from_attributes = True


class LocationCreate(BaseModel):
    code: str
    name: str
    type: str
    description: Optional[str] = None
    image_url: Optional[str] = None


class LocationUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class LocationResponse(BaseModel):
    id: int
    code: str
    name: str
    type: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True


class SampleStockResponse(BaseModel):
    product_id: int
    product_name: str
    sku: str
    sample_type: Optional[str] = None
    total_quantity: int
    locations: List[dict]


class SampleStockDetailResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    sku: str
    location_id: int
    location_name: str
    sample_type: Optional[str] = None
    quantity: int


class HandoverCreate(BaseModel):
    product_id: int
    quantity: int
    to_location_id: int
    storage_location_id: Optional[int] = None
    sample_type: Optional[str] = None
    purpose: str
    notes: Optional[str] = None


class TransferCreate(BaseModel):
    product_id: int
    from_location_id: int
    to_location_id: int
    from_storage_location_id: Optional[int] = None
    to_storage_location_id: Optional[int] = None
    quantity: int
    sample_type: Optional[str] = None
    purpose: str
    notes: Optional[str] = None


class BorrowCreate(BaseModel):
    product_id: int
    from_location_id: int
    quantity: int
    borrower_name: str
    borrower_location_id: Optional[int] = None
    sample_type: Optional[str] = None
    purpose: Optional[str] = None
    borrow_date: Optional[str] = None
    expected_return_date: Optional[str] = None
    notes: Optional[str] = None


class ReturnCreate(BaseModel):
    location_id: int
    notes: Optional[str] = None


class AdjustCreate(BaseModel):
    product_id: int
    location_id: int
    storage_location_id: Optional[int] = None
    adjustment: int
    sample_type: Optional[str] = None
    purpose: str
    notes: Optional[str] = None


class MovementResponse(BaseModel):
    id: int
    movement_type: str
    product: dict
    from_location: Optional[dict] = None
    to_location: Optional[dict] = None
    quantity: int
    sample_type: Optional[str] = None
    purpose: Optional[str] = None
    user: dict
    date: str
    notes: Optional[str] = None
    reference_type: Optional[str] = None
    reference_id: Optional[int] = None


class BorrowingResponse(BaseModel):
    id: int
    product: dict
    borrower_name: Optional[str] = None
    borrower_location: Optional[dict] = None
    from_location: Optional[dict] = None
    quantity: int
    sample_type: Optional[str] = None
    purpose: Optional[str] = None
    borrow_date: str
    expected_return_date: Optional[str] = None
    actual_return_date: Optional[str] = None
    borrowed_at: Optional[str] = None
    status: str
    user: dict
    notes: Optional[str] = None


class GuestReleaseCreate(BaseModel):
    product_id: int
    location_id: int
    quantity: int
    sample_type: Optional[str] = None
    guest_name: str
    guest_company: Optional[str] = None
    purpose: str
    release_date: str
    notes: Optional[str] = None


class GuestReleaseResponse(BaseModel):
    id: int
    product: dict
    location: Optional[dict] = None
    quantity: int
    sample_type: Optional[str] = None
    guest_name: str
    guest_company: Optional[str] = None
    purpose: Optional[str] = None
    release_date: str
    status: str
    user: dict
    approved_by: Optional[dict] = None
    approved_at: Optional[str] = None
    rejected_by: Optional[dict] = None
    rejected_at: Optional[str] = None
    movement: Optional[dict] = None
    notes: Optional[str] = None


class OpnameSessionCreate(BaseModel):
    name: str
    location_id: Optional[int] = None
    notes: Optional[str] = None


class OpnameSessionResponse(BaseModel):
    id: int
    name: str
    status: str
    location: Optional[dict] = None
    creator: dict
    approver: Optional[dict] = None
    notes: Optional[str] = None
    created_at: str
    completed_at: Optional[str] = None
    approved_at: Optional[str] = None


class OpnameItemCreate(BaseModel):
    product_id: int
    location_id: int
    actual_quantity: int
    sample_type: Optional[str] = None
    notes: Optional[str] = None


class OpnameItemResponse(BaseModel):
    id: int
    product: dict
    location: dict
    sample_type: Optional[str] = None
    expected_quantity: int
    actual_quantity: Optional[int] = None
    variance: Optional[int] = None
    adjustment_movement_id: Optional[int] = None
    notes: Optional[str] = None


class RestockRequestCreate(BaseModel):
    product_id: int
    location_id: int
    sample_type: Optional[str] = None
    requested_quantity: int
    minimum_quantity: Optional[int] = None
    current_quantity: Optional[int] = None
    source: Optional[str] = "manual"
    notes: Optional[str] = None


class RestockRequestResponse(BaseModel):
    id: int
    product: dict
    location: dict
    sample_type: Optional[str] = None
    minimum_quantity: Optional[int] = None
    current_quantity: Optional[int] = None
    requested_quantity: int
    source: str
    status: str
    requester: dict
    approver: Optional[dict] = None
    notes: Optional[str] = None


class MaintenanceCreate(BaseModel):
    product_id: int
    location_id: Optional[int] = None
    maintenance_type: str
    quantity: int
    sample_type: Optional[str] = None
    notes: Optional[str] = None


class MaintenanceResponse(BaseModel):
    id: int
    product: dict
    location: Optional[dict] = None
    maintenance_type: str
    status: str
    quantity: int
    sample_type: Optional[str] = None
    notes: Optional[str] = None
    creator: dict
    completer: Optional[dict] = None
    movement: Optional[dict] = None
    created_at: str
    completed_at: Optional[str] = None


class ReservationCreate(BaseModel):
    product_id: int
    quantity: int
    purpose: Optional[str] = None
    reserved_from: str
    reserved_until: str
    notes: Optional[str] = None


class ReservationResponse(BaseModel):
    id: int
    product: dict
    quantity: int
    purpose: Optional[str] = None
    reserved_from: str
    reserved_until: str
    status: str
    notes: Optional[str] = None
    user: dict
    created_at: str
    updated_at: Optional[str] = None


class BarcodeScanLogResponse(BaseModel):
    id: int
    barcode: str
    scan_type: str
    result_id: Optional[int] = None
    result_type: Optional[str] = None
    user: dict
    location: Optional[dict] = None
    movement: Optional[dict] = None
    notes: Optional[str] = None
    scanned_at: str


class DashboardKPI(BaseModel):
    total_sample: int
    at_showroom: int
    borrowed: int
    released_this_month: int
    maintenance: int
    retired: int
    need_restock: int
    missing: int
    overdue_borrowing: int
    top_borrowed_product: Optional[dict] = None
    top_released_product: Optional[dict] = None
    stock_accuracy: Optional[float] = None


class StorageLocationCreate(BaseModel):
    name: str
    code: str
    parent_id: Optional[int] = None
    location_id: int
    storage_type: Optional[str] = "shelf"
    capacity_qty: Optional[int] = None
    capacity_unit: Optional[str] = "PCS"
    capacity_note: Optional[str] = None
    description: Optional[str] = None


class StorageLocationUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    parent_id: Optional[int] = None
    location_id: Optional[int] = None
    storage_type: Optional[str] = None
    capacity_qty: Optional[int] = None
    capacity_unit: Optional[str] = None
    capacity_note: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class StorageLocationResponse(BaseModel):
    id: int
    name: str
    code: str
    parent_id: Optional[int] = None
    location_id: int
    storage_type: str
    capacity_qty: Optional[int] = None
    capacity_unit: Optional[str] = None
    capacity_note: Optional[str] = None
    used_capacity: int
    path: Optional[str] = None
    description: Optional[str] = None
    is_active: bool
    version: int

    class Config:
        from_attributes = True


class QREntityCreate(BaseModel):
    entity_type: str
    entity_id: int
    label: Optional[str] = None
    storage_location_id: Optional[int] = None


class QREntityUpdate(BaseModel):
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None
    label: Optional[str] = None
    storage_location_id: Optional[int] = None
    is_active: Optional[bool] = None


class QREntityResponse(BaseModel):
    id: int
    entity_type: str
    entity_id: int
    token: str
    label: Optional[str] = None
    storage_location_id: Optional[int] = None
    is_active: bool
    version: int

    class Config:
        from_attributes = True


class QRScanRequest(BaseModel):
    token: str
    action: str
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    sample_type: Optional[str] = None


class ActivityLogResponse(BaseModel):
    id: int
    action: str
    entity_type: str
    entity_id: int
    actor_type: str
    detail: Optional[str] = None
    created_at: str

    class Config:
        from_attributes = True


class SuccessResponse(BaseModel):
    success: bool = True
    data: Optional[Union[dict, list]] = None
    message: Optional[str] = None
