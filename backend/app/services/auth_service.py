"""
=========================================================
JARVIS Authentication Service
=========================================================

Handles user registration and login.

Author: Abhinay Kumar
Project: JARVIS
=========================================================
"""

from datetime import datetime, timezone

from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.database.models.user import User
from app.database.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest
from app.schemas.auth import Token
from app.schemas.user import UserCreate
from app.services.base_service import BaseService


class AuthService(BaseService):
    """
    Business logic for authentication.
    """

    def __init__(self, db: Session):
        super().__init__(db)
        self.repository = UserRepository(db)

    # ==========================================================
    # Register
    # ==========================================================

    def register(self, user: UserCreate) -> User:
        """
        Register a new user.
        """

        if self.repository.get_by_username(user.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists.",
            )

        if self.repository.get_by_email(user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists.",
            )

        try:
            db_user = self.repository.create_user(
                username=user.username,
                email=user.email,
                full_name=user.full_name,
                password_hash=hash_password(user.password),
            )

            self.commit()
            self.refresh(db_user)

            logger.info(
                "New user registered: %s",
                db_user.username,
            )

            return db_user

        except Exception:
            self.rollback()
            logger.exception("Registration failed.")
            raise

    # ==========================================================
    # Login
    # ==========================================================

    def login(
        self,
        credentials: LoginRequest,
    ) -> Token:
        """
        Authenticate a user and return a JWT.
        """

        user = self.repository.get_by_username(
            credentials.username,
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password.",
            )

        if not verify_password(
            credentials.password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password.",
            )

        user.last_login = datetime.now(timezone.utc)

        self.commit()
        self.refresh(user)

        token = create_access_token(
            data={
                "sub": user.username,
            }
        )

        logger.info(
            "User '%s' logged in.",
            user.username,
        )

        return Token(
            access_token=token,
            token_type="bearer",
        )

    # ==========================================================
    # Get User
    # ==========================================================

    def get_user_by_username(
        self,
        username: str,
    ) -> User | None:
        """
        Return a user by username.
        """

        return self.repository.get_by_username(
            username,
        )