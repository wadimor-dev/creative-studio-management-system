import os
import datetime
import subprocess
import zipfile
import shutil
from pathlib import Path

# Load settings to get DATABASE_URL if available, otherwise read from .env manually
try:
    from app.core.config import settings
    DB_URL = settings.DATABASE_URL
except ImportError:
    # Standalone mode fallback
    DB_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:@localhost/csms_db")

BACKUP_DIR = Path(__file__).resolve().parent.parent / "storage" / "backups"
UPLOADS_DIR = Path(__file__).resolve().parent.parent / "uploads"

def create_backup():
    """Create a backup of the MySQL database and the uploads folder."""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    db_backup_path = BACKUP_DIR / f"csms_db_backup_{timestamp}.sql"
    uploads_backup_path = BACKUP_DIR / f"csms_uploads_backup_{timestamp}.zip"
    
    print(f"[{datetime.datetime.now()}] Starting backup process...")

    # 1. Parse DB URL for mysqldump
    # Expected format: mysql+pymysql://user:password@host:port/dbname
    try:
        from urllib.parse import urlparse
        # SQLAlchemy URL parsing can be tricky if password has special chars, urlparse works for simple ones
        parsed = urlparse(DB_URL)
        
        db_user = parsed.username or "root"
        db_pass = parsed.password or ""
        db_host = parsed.hostname or "localhost"
        db_port = parsed.port or 3306
        db_name = parsed.path.lstrip("/")
        
        # Build mysqldump command
        cmd = [
            "mysqldump",
            f"--user={db_user}",
            f"--host={db_host}",
            f"--port={db_port}",
            "--single-transaction",
            "--routines",
            "--triggers",
        ]
        if db_pass:
            cmd.append(f"--password={db_pass}")
            
        cmd.append(db_name)
        
        print(f"[{datetime.datetime.now()}] Dumping database to {db_backup_path}...")
        with open(db_backup_path, "w") as f:
            subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, check=True)
            
    except Exception as e:
        print(f"[{datetime.datetime.now()}] Error dumping database: {e}")
        # Note: In production you might want to raise here to fail loudly
    
    # 2. Zip Uploads Folder
    print(f"[{datetime.datetime.now()}] Zipping uploads directory to {uploads_backup_path}...")
    try:
        if UPLOADS_DIR.exists():
            shutil.make_archive(str(uploads_backup_path).replace('.zip', ''), 'zip', str(UPLOADS_DIR))
        else:
            print(f"[{datetime.datetime.now()}] Uploads directory does not exist, skipping zip.")
    except Exception as e:
        print(f"[{datetime.datetime.now()}] Error zipping uploads: {e}")

    # 3. Cleanup Old Backups (Keep last 7 days)
    print(f"[{datetime.datetime.now()}] Cleaning up old backups...")
    retention_days = 7
    cutoff = datetime.datetime.now() - datetime.timedelta(days=retention_days)
    
    for file_path in BACKUP_DIR.glob("*"):
        if file_path.is_file():
            # Check modification time
            mtime = datetime.datetime.fromtimestamp(file_path.stat().st_mtime)
            if mtime < cutoff:
                try:
                    file_path.unlink()
                    print(f"Deleted old backup: {file_path.name}")
                except Exception as e:
                    print(f"Error deleting old backup {file_path.name}: {e}")

    print(f"[{datetime.datetime.now()}] Backup process completed successfully.")
    
    return {
        "database": str(db_backup_path) if db_backup_path.exists() else None,
        "uploads": str(uploads_backup_path) if uploads_backup_path.exists() else None,
        "timestamp": timestamp
    }

if __name__ == "__main__":
    create_backup()
