from pydantic import BaseModel
from typing import Optional

class BaseFilter(BaseModel):
    search: Optional[str] = None
    sort_by: Optional[str] = "created_at"
    sort_order: Optional[str] = "desc"
