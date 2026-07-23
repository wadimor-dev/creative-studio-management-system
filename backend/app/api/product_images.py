import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, Request
from app.dependencies.permission import RequirePermission
from app.constants.permissions import Permission
from app.core.exceptions import CSMSException
from app.common.responses import create_success_response

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOAD_DIR = os.path.join(BASE_DIR, "storage", "uploads", "products")
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif", "image/avif"}
MAX_FILE_SIZE = 20 * 1024 * 1024


@router.post("/upload-image", dependencies=[Depends(RequirePermission(Permission.PRODUCT_CREATE))])
async def upload_product_image(file: UploadFile = File(...), request: Request = None):
    if not file.content_type or file.content_type not in ALLOWED_CONTENT_TYPES:
        raise CSMSException(
            f"Invalid file type '{file.content_type}'. Allowed: image/jpeg, image/png, image/webp, image/gif, image/avif",
            status_code=400,
        )

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise CSMSException(f"File size exceeds 20MB limit", status_code=400)

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    filename = f"{uuid.uuid4()}.webp"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(contents)

    url = f"{request.base_url}uploads/products/{filename}"

    return create_success_response(data={"url": str(url)}, message="Image uploaded successfully")
