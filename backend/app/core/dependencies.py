"""
=========================================================
JARVIS Dependencies
=========================================================

Provides dependency injection helpers.

Author: Abhinay Kumar
Project: JARVIS
=========================================================
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services import UserService


def get_user_service(
    db: Session = Depends(get_db),
) -> UserService:
    """
    Return a UserService instance.
    """

    return UserService(db)