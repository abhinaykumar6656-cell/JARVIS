"""
=========================================================
JARVIS Authentication API
=========================================================

Authentication endpoints.

Author: Abhinay Kumar
Project: JARVIS
=========================================================
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.dependencies import get_auth_service
from app.core.dependencies import get_current_user
from app.core.dependencies import get_db
from app.schemas.auth import LoginRequest
from app.schemas.auth import Token
from app.schemas.user import UserCreate
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# ==========================================================
# Register
# ==========================================================

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Register a new user.
    """

    service = AuthService(db)

    return service.register(user)


# ==========================================================
# Login
# ==========================================================

@router.post(
    "/login",
    response_model=Token,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Authenticate a user and return a JWT access token.

    This endpoint accepts OAuth2 password form data,
    making it fully compatible with Swagger UI's
    Authorize button.
    """

    credentials = LoginRequest(
        username=form_data.username,
        password=form_data.password,
    )

    return auth_service.login(credentials)


# ==========================================================
# Current User
# ==========================================================

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user=Depends(get_current_user),
):
    """
    Return the currently authenticated user.
    """

    return current_user