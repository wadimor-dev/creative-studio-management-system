from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from app.schemas.role import RoleResponse

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role_id: int

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    role_id: Optional[int] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    role: Optional[RoleResponse] = None
    
    model_config = ConfigDict(from_attributes=True)

class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
