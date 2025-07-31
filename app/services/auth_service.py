from sqlalchemy.orm import Session
from datetime import timedelta
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import LoginRequest, TokenResponse, RefreshTokenResponse
from app.core.security import verify_password, create_access_token, create_refresh_token, verify_token
from app.core.exceptions import InvalidCredentialsException, UserNotActiveException, InvalidTokenException
from app.config import settings


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def register_user(self, user_data: UserCreate) -> UserResponse:
        """Register a new user"""
        db_user = self.user_repo.create_user(user_data)
        return UserResponse.from_orm(db_user)

    def login(self, login_data: LoginRequest) -> TokenResponse:
        """Authenticate user and return tokens"""
        # Get user by email
        user = self.user_repo.get_user_by_email(login_data.email)
        if not user:
            raise InvalidCredentialsException()

        # Verify password
        if not verify_password(login_data.password, user.password_hash):
            raise InvalidCredentialsException()

        # Check if user is active
        if not user.is_active:
            raise UserNotActiveException()

        # Create tokens
        token_data = {"sub": str(user.id), "email": user.email}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse.from_orm(user)
        )

    def validate_token(self, token: str) -> UserResponse:
        """Validate access token and return user info"""
        payload = verify_token(token, "access")
        user_id = int(payload.get("sub"))
        user = self.user_repo.get_user_by_id(user_id)
        
        if not user.is_active:
            raise UserNotActiveException()
        
        return UserResponse.from_orm(user)

    def refresh_access_token(self, refresh_token: str) -> RefreshTokenResponse:
        """Generate new access token using refresh token"""
        payload = verify_token(refresh_token, "refresh")
        user_id = int(payload.get("sub"))
        user = self.user_repo.get_user_by_id(user_id)
        
        if not user.is_active:
            raise UserNotActiveException()

        # Create new access token
        token_data = {"sub": str(user.id), "email": user.email}
        access_token = create_access_token(token_data)

        return RefreshTokenResponse(
            access_token=access_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )

    def get_current_user(self, token: str) -> UserResponse:
        """Get current user from token"""
        return self.validate_token(token)