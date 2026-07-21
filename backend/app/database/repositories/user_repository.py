"""
=========================================================
JARVIS User Repository
=========================================================

Provides database operations for the User model.

Author: Abhinay Kumar
Project: JARVIS
=========================================================
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models.user import User


class UserRepository:
    """
    Repository responsible only for database access.
    No business logic or transaction management.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_user(
        self,
        username: str,
        email: str,
        full_name: str,
        password_hash: str,
    ) -> User:
        """
        Create a new user.

        Transaction management is handled
        by the service layer.
        """

        user = User(
            username=username,
            email=email,
            full_name=full_name,
            password_hash=password_hash,
        )

        self.db.add(user)

        return user

    def get_by_id(
        self,
        user_id: int,
    ) -> User | None:
        """
        Return a user by ID.
        """

        stmt = select(User).where(
            User.id == user_id
        )

        result = self.db.execute(stmt)

        return result.scalar_one_or_none()

    def get_by_username(
        self,
        username: str,
    ) -> User | None:
        """
        Return a user by username.
        """

        stmt = select(User).where(
            User.username == username
        )

        result = self.db.execute(stmt)

        return result.scalar_one_or_none()

    def get_by_email(
        self,
        email: str,
    ) -> User | None:
        """
        Return a user by email.
        """

        stmt = select(User).where(
            User.email == email
        )

        result = self.db.execute(stmt)

        return result.scalar_one_or_none()

    def get_all(self) -> list[User]:
        """
        Return all users.
        """

        stmt = select(User)

        result = self.db.execute(stmt)

        return list(result.scalars().all())

    def update(self, user: User) -> User:
        """
        Return the modified user.

        Commit is handled by the service layer.
        """

        return user

    def delete(self, user: User) -> None:
        """
        Delete a user.

        Commit is handled by the service layer.
        """

        self.db.delete(user)