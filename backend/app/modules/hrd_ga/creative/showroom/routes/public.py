"""Public routes for showroom location QR scanning — no authentication required."""

import io
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.database.session import get_db
from app.models.showroom_location import ShowroomLocation
from app.models.showroom_sample_stock import ShowroomSampleStock
from app.models.product import Product

router = APIRouter()


@router.get("/scan/{code}")
def get_location_products(code: str, db: Session = Depends(get_db)):
    """Return location details and all products stored there."""
    location = db.query(ShowroomLocation).filter(ShowroomLocation.code == code).first()
    if not location:
        raise HTTPException(status_code=404, detail="Lokasi tidak ditemukan")

    stocks = db.query(ShowroomSampleStock).filter(
        ShowroomSampleStock.location_id == location.id
    ).all()

    products = []
    for stock in stocks:
        product = db.query(Product).filter(Product.id == stock.product_id).first()
        if product:
            products.append({
                "product_id": product.id,
                "product_name": product.display_name,
                "sku": getattr(product, "sku", None) or "",
                "quantity": stock.quantity,
                "sample_type": stock.sample_type,
            })

    return {
        "location": {
            "id": location.id,
            "code": location.code,
            "name": location.name,
            "type": location.type,
            "description": location.description,
            "image_url": location.image_url,
        },
        "products": products,
        "total_products": len(products),
        "total_quantity": sum(p["quantity"] for p in products),
    }


@router.get("/scan/{code}/qr")
def get_qr_code(code: str, db: Session = Depends(get_db)):
    """Generate and return a QR code PNG for the location."""
    import qrcode

    location = db.query(ShowroomLocation).filter(ShowroomLocation.code == code).first()
    if not location:
        raise HTTPException(status_code=404, detail="Lokasi tidak ditemukan")

    qr_url = f"https://csms.idekode.web.id/scan/{location.code}"

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(qr_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1e293b", back_color="white")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png", headers={
        "Content-Disposition": f'inline; filename="QR_{location.code}.png"',
    })


@router.get("/qr/{token}/image")
def get_qr_token_image(token: str, db: Session = Depends(get_db)):
    """Generate and return a QR code PNG for any active QR entity by token."""
    import qrcode

    from app.models.showroom_qr_entity import ShowroomQREntity
    qr = db.query(ShowroomQREntity).filter(
        ShowroomQREntity.token == token,
        ShowroomQREntity.is_active == True,
    ).first()
    if not qr:
        raise HTTPException(status_code=404, detail="QR token tidak ditemukan atau tidak aktif")

    qr_img = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr_img.add_data(token)
    qr_img.make(fit=True)
    img = qr_img.make_image(fill_color="#1e293b", back_color="white")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    label = qr.label or token
    return StreamingResponse(buf, media_type="image/png", headers={
        "Content-Disposition": f'inline; filename="QR_{label}.png"',
    })
