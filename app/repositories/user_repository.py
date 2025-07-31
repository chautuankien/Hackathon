from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password
from app.core.exceptions import EmailAlreadyExistsException, UserNotFoundException


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user"""
        try:
            hashed_password = hash_password(user_data.password)
            db_user = User(
                email=user_data.email,
                password_hash=hashed_password,
                full_name=user_data.full_name,
            )
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except IntegrityError:
            self.db.rollback()
            raise EmailAlreadyExistsException()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise UserNotFoundException()
        return user

    def update_user(self, user_id: int, **kwargs) -> User:
        """Update user fields"""
        user = self.get_user_by_id(user_id)
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        """Soft delete user by setting is_active to False"""
        user = self.get_user_by_id(user_id)
        user.is_active = False
        self.db.commit()
        return True