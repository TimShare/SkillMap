from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
import uuid


class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    is_public: bool = True


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_public: Optional[bool] = None


class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    name: str
    email: EmailStr
    is_public: bool
    is_active: bool
