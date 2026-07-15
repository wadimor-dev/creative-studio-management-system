from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
import os
from pathlib import Path

router = APIRouter()

BACKUP_DIR = Path(__file__).resolve().parent.parent.parent / "storage" / "backups"

@router.get("/backups", summary="List available backups")
def list_backups(current_user: User = Depends(get_current_user)):
    """List all available backup files."""
    if current_user.role.name not in ["ADMIN", "SUPERADMIN"]:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    if not BACKUP_DIR.exists():
        return {"data": []}
        
    backups = []
    for file_path in BACKUP_DIR.glob("*"):
        if file_path.is_file():
            stat = file_path.stat()
            backups.append({
                "filename": file_path.name,
                "size_bytes": stat.st_size,
                "created_at": stat.st_mtime * 1000 # JS timestamp
            })
            
    # Sort descending by creation time
    backups.sort(key=lambda x: x["created_at"], reverse=True)
    return {"data": backups}

@router.get("/backups/download/{filename}", summary="Download a backup file")
def download_backup(filename: str, current_user: User = Depends(get_current_user)):
    """Download a specific backup file."""
    if current_user.role.name not in ["ADMIN", "SUPERADMIN"]:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    file_path = BACKUP_DIR / filename
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Backup file not found")
        
    return FileResponse(path=file_path, filename=filename, media_type="application/octet-stream")

def run_backup_task():
    import sys
    scripts_dir = str(Path(__file__).resolve().parent.parent.parent / "scripts")
    if scripts_dir not in sys.path:
        sys.path.append(scripts_dir)
    try:
        from system_backup import create_backup
        create_backup()
    except Exception as e:
        print(f"Background backup task failed: {e}")

@router.post("/backups/trigger", summary="Trigger a manual backup")
def trigger_backup(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    """Trigger a manual backup to run in the background."""
    if current_user.role.name not in ["ADMIN", "SUPERADMIN"]:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    background_tasks.add_task(run_backup_task)
    
    # Log the activity
    from app.services.logger_service import logger_service
    from app.database.session import SessionLocal
    with SessionLocal() as db:
        logger_service.log_activity(
            db=db,
            user_id=current_user.id,
            action_type="SYSTEM_BACKUP",
            description="Triggered manual system backup"
        )
        
    return {"message": "Backup task started in the background"}
