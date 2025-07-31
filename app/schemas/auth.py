from pydantic import BaseModel, EmailStr
from typing import Optional
from app.schemas.user import UserResponse


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class StandardResponse(BaseModel):
    status: str
    message: str
    data: Optional[dict] = None
    error_code: Optional[str] = None


class TokenValidationResponse(BaseModel):
    status: str
    data: UserResponse