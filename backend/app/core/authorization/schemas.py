from pydantic import BaseModel, ConfigDict
from typing import Optional


class PermissionResponse(BaseModel):
    id: int
    code: str
    name: str
    module: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class RolePermissionResponse(BaseModel):
    role_id: int
    permission_id: int

    model_config = ConfigDict(from_attributes=True)
