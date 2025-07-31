from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_corporate: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class User(UserResponse):
    """Complete user model with all fields"""
    updated_at: datetime