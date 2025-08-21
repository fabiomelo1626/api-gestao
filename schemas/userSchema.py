from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: str
    fullname: Optional[str] = None 
    status: bool = True
    avatar: Optional[str] = None

class UserCreate(UserBase):
    model_config = {
        "from_attributes": True
    }
    
class ResetPasswordRequest(BaseModel):
    token: str
    nova_senha: str

class FirstPassword(BaseModel):
    username: str
    old_password: str
    new_password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }

class UpdatePassword(BaseModel):
    username: str
    new_password: str

class UserUpdate(BaseModel):
    username: str
    fullname: Optional[str] = None
    email: str
    avatar: Optional[str] = None
