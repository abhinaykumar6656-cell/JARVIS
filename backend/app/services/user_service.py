"""
=========================================================
JARVIS User Service
=========================================================

Contains all business logic related
to users.

Author: Abhinay Kumar
Project: JARVIS
=========================================================
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.core.security import hash_password
from app.database.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.services.base_service import BaseService


class UserService(BaseService):
    """
    Handles business logic for users.
    """

    def __init__(self, db: Session):
        super().__init__(db)
        self.repository = UserRepository(db)

    def create_user(self, user: UserCreate):
        """
        Create a new user.
        """

        logger.info(
            "Creating user '%s'",
            user.username,
        )

        if self.repository.get_by_username(user.username):
            logger.warning(
                "Duplicate username: %s",
                user.username,
            )

            raise HTTPException(
                status_code=400,
                detail="Username already exists.",
            )

        if self.repository.get_by_email(user.email):
            logger.warning(
                "Duplicate email: %s",
                user.email,
            )

            raise HTTPException(
                status_code=400,
                detail="Email already exists.",
            )

        try:
            new_user = self.repository.create_user(
                username=user.username,
                email=user.email,
                full_name=user.full_name,
                password_hash=hash_password(user.password),
            )

            self.commit()
            self.refresh(new_user)

            logger.info(
                "User '%s' created successfully.",
                user.username,
            )

            return new_user

        except Exception:
            self.rollback()

            logger.exception(
                "Database transaction failed."
            )

            raise

    def get_all_users(self):
        """
        Return all users.
        """

        logger.info("Fetching all users.")

        return self.repository.get_all()

    def get_user_by_id(self, user_id: int):
        """
        Return user by ID.
        """

        logger.info(
            "Fetching user id=%s",
            user_id,
        )

        user = self.repository.get_by_id(user_id)

        if user is None:
            logger.warning(
                "User %s not found.",
                user_id,
            )

            raise HTTPException(
                status_code=404,
                detail="User not found.",
            )

        return user