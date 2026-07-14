from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.export import export_manager, RendererType, RenderContext
from app.repositories.item_repository import item_repo
from app.dependencies.permission import RequireRole
from app.constants.role import RoleType
from app.models.product_movement import ProductMovement
from sqlalchemy.orm import joinedload
from app.models.export_log import ExportLog
from app.services.report_engine import report_engine
from app.dependencies.auth import get_current_user
from app.models.user import User
import datetime

router = APIRouter()

def get_basic_context(orientation="P"):
    return RenderContext(orientation=orientation, page_size="A4")

@router.post("/items/excel", dependencies=[Depends(RequireRole([RoleType.ADMIN, RoleType.STAFF]))])
def export_items_excel(
    category_id: int | None = None,
    location_id: int | None = None,
    search: str | None = None,
    db: Session = Depends(get_db)
):
    from app.services.item_service import item_service
    items, _ = item_service.get_items(db, skip=0, limit=0, search=search, category_id=category_id, location_id=location_id)
    
    headers = ["ID", "SKU", "Name", "Stock Qty", "Status"]
    rows = [[item.id, item.sku, item.name, item.stock_qty, "Active" if item.is_active else "Inactive"] for item in items]
    
    dataset = {
        "metadata": {"report_type": "Inventory Items Report", "company": "Creative Studio"},
        "headers": headers,
        "rows": rows
    }
    
    stream = export_manager.export("excel", dataset, RendererType.TABLE, get_basic_context())
    
    filename = f"items_export_{datetime.date.today()}.xlsx"
    headers_res = {
        "Content-Disposition": f"inline; filename={filename}",
        "Access-Control-Expose-Headers": "Content-Disposition"
    }
    
    return StreamingResponse(
        stream, 
        headers=headers_res, 
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@router.post("/items/pdf", dependencies=[Depends(RequireRole([RoleType.ADMIN, RoleType.STAFF]))])
def export_items_pdf(
    category_id: int | None = None,
    location_id: int | None = None,
    search: str | None = None,
    db: Session = Depends(get_db)
):
    from app.services.item_service import item_service
    items, _ = item_service.get_items(db, skip=0, limit=0, search=search, category_id=category_id, location_id=location_id)
    
    headers = ["ID", "SKU", "Name", "Stock Qty", "Status"]
    rows = [[item.id, item.sku, item.name, item.stock_qty, "Active" if item.is_active else "Inactive"] for item in items]
    
    dataset = {
        "metadata": {"report_type": "Inventory Items Report", "company": "Creative Studio"},
        "headers": headers,
        "rows": rows
    }
    
    stream = export_manager.export("pdf", dataset, RendererType.TABLE, get_basic_context("P"))
    
    filename = f"items_export_{datetime.date.today()}.pdf"
    headers_res = {
        "Content-Disposition": f"inline; filename={filename}",
        "Access-Control-Expose-Headers": "Content-Disposition"
    }
    
    return StreamingResponse(stream, headers=headers_res, media_type="application/pdf")

@router.post("/product-movements/excel", dependencies=[Depends(RequireRole([RoleType.ADMIN, RoleType.STAFF]))])
def export_product_movements_excel(
    product_id: int | None = None,
    location_id: int | None = None,
    user_id: int | None = None,
    type_id: int | None = None,
    category_id: int | None = None,
    motif_id: int | None = None,
    sub_motif_id: int | None = None,
    color_id: int | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    db: Session = Depends(get_db)
):
    from app.models.product import Product
    query = db.query(ProductMovement).join(ProductMovement.product).options(
        joinedload(ProductMovement.product),
        joinedload(ProductMovement.source_location),
        joinedload(ProductMovement.destination_location),
        joinedload(ProductMovement.user)
    ).order_by(ProductMovement.date.desc())
    
    # ... basic filters
    if product_id: query = query.filter(ProductMovement.product_id == product_id)
    if user_id: query = query.filter(ProductMovement.user_id == user_id)
    if start_date: query = query.filter(ProductMovement.date >= start_date)
    if end_date: query = query.filter(ProductMovement.date <= f"{end_date} 23:59:59")
        
    movements = query.all()
    
    headers = ["Date", "Type", "SKU", "Product Name", "Qty", "Source", "Destination", "User", "Notes"]
    rows = []
    for m in movements:
        rows.append([
            m.date.strftime("%Y-%m-%d %H:%M"),
            m.type.value,
            m.product.sku if m.product else "-",
            m.product.display_name if m.product else "-",
            m.quantity,
            m.source_location.name if m.source_location else "-",
            m.destination_location.name if m.destination_location else "-",
            m.user.username if m.user else "-",
            m.notes or "-"
        ])
        
    dataset = {
        "metadata": {"report_type": "Product Movements Report", "company": "Creative Studio"},
        "headers": headers,
        "rows": rows
    }
    stream = export_manager.export("excel", dataset, RendererType.TABLE, get_basic_context("L"))
    
    filename = f"product_movements_{datetime.date.today()}.xlsx"
    headers_res = {
        "Content-Disposition": f"inline; filename={filename}",
        "Access-Control-Expose-Headers": "Content-Disposition"
    }
    
    return StreamingResponse(stream, headers=headers_res, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

@router.post("/product-movements/pdf", dependencies=[Depends(RequireRole([RoleType.ADMIN, RoleType.STAFF]))])
def export_product_movements_pdf(
    product_id: int | None = None,
    location_id: int | None = None,
    user_id: int | None = None,
    type_id: int | None = None,
    category_id: int | None = None,
    motif_id: int | None = None,
    sub_motif_id: int | None = None,
    color_id: int | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    db: Session = Depends(get_db)
):
    from app.models.product import Product
    query = db.query(ProductMovement).join(ProductMovement.product).options(
        joinedload(ProductMovement.product),
        joinedload(ProductMovement.source_location),
        joinedload(ProductMovement.destination_location),
        joinedload(ProductMovement.user)
    ).order_by(ProductMovement.date.desc())
    
    if product_id: query = query.filter(ProductMovement.product_id == product_id)
    if user_id: query = query.filter(ProductMovement.user_id == user_id)
    if start_date: query = query.filter(ProductMovement.date >= start_date)
    if end_date: query = query.filter(ProductMovement.date <= f"{end_date} 23:59:59")
        
    movements = query.all()
    
    headers = ["Date", "Type", "SKU", "Product Name", "Qty", "Source", "Destination", "User"]
    rows = []
    for m in movements:
        rows.append([
            m.date.strftime("%Y-%m-%d %H:%M"),
            m.type.value,
            m.product.sku if m.product else "-",
            m.product.display_name[:20] + "..." if m.product and len(m.product.display_name) > 20 else (m.product.display_name if m.product else "-"),
            m.quantity,
            m.source_location.name if m.source_location else "-",
            m.destination_location.name if m.destination_location else "-",
            m.user.username if m.user else "-"
        ])
        
    dataset = {
        "metadata": {"report_type": "Product Movements Report", "company": "Creative Studio"},
        "headers": headers,
        "rows": rows
    }
    stream = export_manager.export("pdf", dataset, RendererType.TABLE, get_basic_context("L"))
    
    filename = f"product_movements_{datetime.date.today()}.pdf"
    headers_res = {
        "Content-Disposition": f"inline; filename={filename}",
        "Access-Control-Expose-Headers": "Content-Disposition"
    }
    
    return StreamingResponse(stream, headers=headers_res, media_type="application/pdf")

@router.post("/reports/excel", dependencies=[Depends(RequireRole([RoleType.ADMIN]))])
def export_reports_excel(
    type: str = "daily",
    date: str | None = None,
    month: int | None = None,
    year: int | None = None,
    user_id: int | None = None,
    category_id: int | None = None,
    status: str | None = None,
    division: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    filters = {}
    if date: filters['date'] = date
    if month: filters['month'] = month
    if year: filters['year'] = year
    if user_id: filters['user_id'] = user_id
    if category_id: filters['category_id'] = category_id
    if status: filters['status'] = status
    if division: filters['division'] = division
    
    data = report_engine.get_report_data(db, report_type=type, skip=0, limit=10001, **filters)
    
    # We pass data directly to ExportManager
    data["metadata"]["generated_by"] = current_user.full_name or current_user.username
    context = RenderContext(orientation="L", page_size="A4")
    stream = export_manager.export("excel", data, RendererType.TABLE, context)
    
    log = ExportLog(user_id=current_user.id, type=type, format="EXCEL")
    db.add(log)
    db.commit()
    
    today_str = datetime.date.today().strftime("%Y%m%d")
    filename = f"activity_report_{type}_{today_str}.xlsx"
    headers_res = {
        "Content-Disposition": f"inline; filename={filename}",
        "Access-Control-Expose-Headers": "Content-Disposition"
    }
    
    return StreamingResponse(
        stream, 
        headers=headers_res, 
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@router.post("/reports/pdf", dependencies=[Depends(RequireRole([RoleType.ADMIN, RoleType.STAFF]))])
def export_reports_pdf(
    type: str = "daily",
    date: str | None = None,
    month: int | None = None,
    year: int | None = None,
    user_id: int | None = None,
    category_id: int | None = None,
    status: str | None = None,
    division: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    filters = {}
    if date: filters['date'] = date
    if month: filters['month'] = month
    if year: filters['year'] = year
    if user_id: filters['user_id'] = user_id
    if category_id: filters['category_id'] = category_id
    if status: filters['status'] = status
    if division: filters['division'] = division
    
    data = report_engine.get_report_data(db, report_type=type, skip=0, limit=2001, **filters)
    
    data["metadata"]["generated_by"] = current_user.full_name or current_user.username
    context = RenderContext(orientation="L", page_size="A4")
    stream = export_manager.export("pdf", data, RendererType.BLOCK, context)
    
    log = ExportLog(user_id=current_user.id, type=type, format="PDF")
    db.add(log)
    db.commit()
    
    today_str = datetime.date.today().strftime("%Y%m%d")
    filename = f"activity_report_{type}_{today_str}.pdf"
    headers_res = {
        "Content-Disposition": f"inline; filename={filename}",
        "Access-Control-Expose-Headers": "Content-Disposition"
    }
    
    return StreamingResponse(stream, headers=headers_res, media_type="application/pdf")

@router.post("/inventory-transactions/excel", dependencies=[Depends(RequireRole([RoleType.ADMIN, RoleType.STAFF]))])
def export_inventory_transactions_excel(
    item_id: int | None = None,
    user_id: int | None = None,
    category_id: int | None = None,
    location_id: int | None = None,
    type: str | None = None,
    db: Session = Depends(get_db)
):
    from app.services.inventory_service import inventory_service
    transactions, _ = inventory_service.get_transaction_history(
        db, skip=0, limit=10000, item_id=item_id, user_id=user_id,
        category_id=category_id, location_id=location_id, type=type
    )
    
    headers = ["Date", "Type", "Item SKU", "Item Name", "Qty", "Location", "User", "Remarks"]
    rows = []
    for tx in transactions:
        t_type = tx.type.value if hasattr(tx.type, 'value') else tx.type
        src = tx.source_location.name if tx.source_location else "-"
        dst = tx.destination_location.name if tx.destination_location else "-"
        loc = f"{src} -> {dst}" if src != "-" and dst != "-" else (src if src != "-" else dst)
        rows.append([
            tx.date.strftime("%Y-%m-%d %H:%M"),
            t_type,
            tx.item.sku if hasattr(tx.item, 'sku') else f"ITM-{tx.item_id}",
            tx.item.name if tx.item else "Unknown",
            tx.quantity,
            loc,
            tx.user.username if tx.user else "-",
            tx.notes or "-"
        ])
        
    dataset = {
        "metadata": {"report_type": "Inventory Transactions Report", "company": "Creative Studio"},
        "headers": headers,
        "rows": rows
    }
    stream = export_manager.export("excel", dataset, RendererType.TABLE, get_basic_context("L"))
    
    filename = f"inventory_transactions_{datetime.date.today()}.xlsx"
    headers_res = {
        "Content-Disposition": f"inline; filename={filename}",
        "Access-Control-Expose-Headers": "Content-Disposition"
    }
    return StreamingResponse(
        stream, 
        headers=headers_res, 
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@router.post("/inventory-transactions/pdf", dependencies=[Depends(RequireRole([RoleType.ADMIN, RoleType.STAFF]))])
def export_inventory_transactions_pdf(
    item_id: int | None = None,
    user_id: int | None = None,
    category_id: int | None = None,
    location_id: int | None = None,
    type: str | None = None,
    db: Session = Depends(get_db)
):
    from app.services.inventory_service import inventory_service
    transactions, _ = inventory_service.get_transaction_history(
        db, skip=0, limit=10000, item_id=item_id, user_id=user_id,
        category_id=category_id, location_id=location_id, type=type
    )
    
    headers = ["Date", "Type", "Item Name", "Qty", "Location", "User"]
    rows = []
    for tx in transactions:
        t_type = tx.type.value if hasattr(tx.type, 'value') else tx.type
        src = tx.source_location.name if tx.source_location else "-"
        dst = tx.destination_location.name if tx.destination_location else "-"
        loc = f"{src} -> {dst}" if src != "-" and dst != "-" else (src if src != "-" else dst)
        
        rows.append([
            tx.date.strftime("%Y-%m-%d %H:%M"),
            t_type,
            (tx.item.name[:20] + "...") if tx.item and len(tx.item.name) > 20 else (tx.item.name if tx.item else "Unknown"),
            tx.quantity,
            loc[:15] + "..." if len(loc) > 15 else loc,
            tx.user.username if tx.user else "-"
        ])
        
    dataset = {
        "metadata": {"report_type": "Inventory Transactions Report", "company": "Creative Studio"},
        "headers": headers,
        "rows": rows
    }
    stream = export_manager.export("pdf", dataset, RendererType.TABLE, get_basic_context("P"))
    
    filename = f"inventory_transactions_{datetime.date.today()}.pdf"
    headers_res = {
        "Content-Disposition": f"inline; filename={filename}",
        "Access-Control-Expose-Headers": "Content-Disposition"
    }
    return StreamingResponse(stream, headers=headers_res, media_type="application/pdf")
