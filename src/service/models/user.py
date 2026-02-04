from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
import uuid


class UserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: Optional[uuid.UUID] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    hashed_password: Optional[str] = None
    is_public: Optional[bool] = None
    is_active: Optional[bool] = None

