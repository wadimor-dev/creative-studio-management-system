import os
from app.utils.file import UPLOAD_DIR

class StorageResolver:
    """Resolves abstract storage paths to concrete paths (e.g. absolute file paths)."""
    
    @staticmethod
    def resolve(storage_path: str) -> str | None:
        """
        Convert a relative storage_path into an absolute physical path for the renderer.
        If using cloud storage in the future, this method would download the file
        to a temp dir or return a presigned URL, without the Renderer needing to know.
        """
        if not storage_path:
            return None
            
        normalized = storage_path.replace("/", os.sep).lstrip(os.sep)
        
        # Prevent double 'uploads' path
        if normalized.startswith(os.path.join("uploads", "")):
            normalized = normalized[len("uploads" + os.sep):]
            
        abs_path = os.path.join(UPLOAD_DIR, normalized)
        
        if os.path.isfile(abs_path):
            return abs_path
            
        return None
