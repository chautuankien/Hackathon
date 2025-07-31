from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import (
    LoginRequest, TokenResponse, RefreshTokenRequest, RefreshTokenResponse,
    StandardResponse, TokenValidationResponse
)
from app.schemas.user import UserCreate, UserResponse
from app.core.exceptions import AuthException

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """Dependency to get auth service"""
    return AuthService(db)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
) -> UserResponse:
    """Dependency to get current user from token"""
    return auth_service.get_current_user(credentials.credentials)


@router.post("/register", response_model=StandardResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Register a new user"""
    try:
        user = auth_service.register_user(user_data)
        return StandardResponse(
            status="success",
            message="User registered successfully",
            data={
                "user_id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "created_at": user.created_at.isoformat()
            }
        )
    except HTTPException as e:
        return StandardResponse(
            status="error",
            message=e.detail,
            error_code="EMAIL_EXISTS" if e.status_code == 400 else "REGISTRATION_ERROR"
        )


@router.post("/login", response_model=StandardResponse)
async def login(
    login_data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """User login"""
    try:
        token_response = auth_service.login(login_data)
        return StandardResponse(
            status="success",
            message="Login successful",
            data=token_response.dict()
        )
    except AuthException as e:
        return StandardResponse(
            status="error",
            message=e.detail,
            error_code="INVALID_CREDENTIALS"
        )


@router.post("/refresh", response_model=StandardResponse)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Refresh access token"""
    try:
        token_response = auth_service.refresh_access_token(refresh_data.refresh_token)
        return StandardResponse(
            status="success",
            message="Token refreshed successfully",
            data=token_response.dict()
        )
    except AuthException as e:
        return StandardResponse(
            status="error",
            message=e.detail,
            error_code="TOKEN_EXPIRED" if "expired" in e.detail.lower() else "INVALID_TOKEN"
        )


@router.get("/me", response_model=TokenValidationResponse)
async def get_current_user_info(
    current_user: UserResponse = Depends(get_current_user)
):
    """Get current user information"""
    return TokenValidationResponse(
        status="success",
        data=current_user
    )


@router.post("/logout", response_model=StandardResponse)
async def logout(
    current_user: UserResponse = Depends(get_current_user)
):
    """User logout (currently just validates token)"""
    return StandardResponse(
        status="success",
        message="Logged out successfully"
    )


@router.get("/validate-token", response_model=TokenValidationResponse)
async def validate_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Validate token and return user info (for other services)"""
    try:
        user = auth_service.validate_token(credentials.credentials)
        return TokenValidationResponse(
            status="success",
            data=user
        )
    except AuthException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )