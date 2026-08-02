"""
=========================================================
JARVIS Dependencies
=========================================================

Reusable FastAPI dependencies.

Author: Abhinay Kumar
Project: JARVIS
=========================================================
"""

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.core.security import oauth2_scheme
from app.database.session import get_db
from app.services import AuthService
from app.services import UserService


# ==========================================================
# Services
# ==========================================================

def get_user_service(
    db: Session = Depends(get_db),
) -> UserService:
    """
    Return a UserService instance.
    """

    return UserService(db)


def get_auth_service(
    db: Session = Depends(get_db),
) -> AuthService:
    """
    Return an AuthService instance.
    """

    return AuthService(db)


# ==========================================================
# Current User
# ==========================================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Validate JWT and return the authenticated user.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )

    try:
        payload = decode_access_token(token)

        username = payload.get("sub")

        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = auth_service.get_user_by_username(
        username
    )

    if user is None:
        raise credentials_exception

    return user


# ==========================================================
# Current Admin
# ==========================================================

def get_current_admin(
    current_user=Depends(get_current_user),
):
    """
    Validate that the current user
    is an active administrator.
    """

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user.",
        )

    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator privileges required.",
        )

    return current_user