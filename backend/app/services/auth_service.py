"""
=========================================================
JARVIS Authentication Service
=========================================================

Handles registration and login.

Author: Abhinay Kumar
Project: JARVIS
=========================================================
"""

from fastapi import HTTPException
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
from app.schemas.user import UserCreate
from app.services.base_service import BaseService


class AuthService(BaseService):

    def __init__(self, db: Session):
        super().__init__(db)
        self.repository = UserRepository(db)

    def register(self, user: UserCreate) -> User:

        if self.repository.get_by_username(user.username):
            raise HTTPException(400, "Username already exists.")

        if self.repository.get_by_email(user.email):
            raise HTTPException(400, "Email already exists.")

        db_user = self.repository.create_user(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            password_hash=hash_password(user.password),
        )

        self.commit()
        self.refresh(db_user)

        logger.info("User '%s' registered.", user.username)

        return db_user

    def login(self, credentials: LoginRequest):

        user = self.repository.get_by_username(
            credentials.username
        )

        if user is None:
            raise HTTPException(401, "Invalid username or password.")

        if not verify_password(
            credentials.password,
            user.password_hash,
        ):
            raise HTTPException(401, "Invalid username or password.")

        token = create_access_token(
            subject=user.username,
        )

        logger.info("User '%s' logged in.", user.username)

        return {
            "access_token": token,
            "token_type": "bearer",
        }