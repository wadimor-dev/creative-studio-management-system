import os
import shutil
from fastapi import UploadFile
from app.exceptions.base import CSMSException
from app.core.config import settings

# Adjust the upload directory base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOAD_DIR = os.path.join(BASE_DIR, "storage", "uploads")
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

def get_file_extension(filename: str) -> str:
    return os.path.splitext(filename)[1].lower()

def validate_evidence_file(file: UploadFile):
    ext = get_file_extension(file.filename)
    if ext not in ALLOWED_EXTENSIONS:
        raise CSMSException(f"File extension {ext} not allowed. Allowed: {ALLOWED_EXTENSIONS}", status_code=400)
    
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise CSMSException(f"MIME type {file.content_type} not allowed. Allowed: {ALLOWED_MIME_TYPES}", status_code=400)
    
    # Check file size by seeking to the end
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        raise CSMSException(f"File size exceeds 5MB limit ({file_size} bytes)", status_code=400)
        
    return file_size

def save_evidence_file(file: UploadFile, activity_id: int, file_prefix: str) -> str:
    # Directory: storage/uploads/work_activity/{activity_id}/
    activity_dir = os.path.join(UPLOAD_DIR, "work_activity", str(activity_id))
    os.makedirs(activity_dir, exist_ok=True)
    
    # Generate unique filename: {prefix}_{original_filename}
    ext = get_file_extension(file.filename)
    # Sanitize original filename (remove path info)
    safe_name = os.path.basename(file.filename)
    import time
    timestamp = int(time.time())
    new_filename = f"{file_prefix}_{timestamp}_{safe_name}"
    
    file_path = os.path.join(activity_dir, new_filename)
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise CSMSException(f"Failed to save file: {str(e)}", status_code=500)
        
    # Return relative path for database
    return f"uploads/work_activity/{activity_id}/{new_filename}"
