import os
from app.core.file.utils import UPLOAD_DIR


class StorageResolver:
    def resolve(self, storage_path: str) -> str | None:
        if not storage_path:
            return None

        normalized = storage_path.replace("/", os.sep).lstrip(os.sep)

        if normalized.startswith(os.path.join("uploads", "")):
            normalized = normalized[len("uploads" + os.sep):]

        abs_path = os.path.join(UPLOAD_DIR, normalized)

        if os.path.isfile(abs_path):
            return abs_path

        return None
