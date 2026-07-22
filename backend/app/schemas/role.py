from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class RoleResponse(RoleBase):
    id: int
    is_system: bool = True

    model_config = ConfigDict(from_attributes=True)

class RoleWithPermissions(RoleResponse):
    permission_ids: List[int] = []
