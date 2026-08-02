"""
=========================================================
JARVIS Users API
=========================================================

Protected user endpoints.

Author: Abhinay Kumar
Project: JARVIS
=========================================================
"""

from fastapi import APIRouter, Depends

from app.core.dependencies import (
    get_current_user,
    get_user_service,
)
from app.schemas.user import UserResponse
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "",
    response_model=list[UserResponse],
)
def get_users(
    current_user=Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    """
    Get all users.
    """

    return service.get_all_users()


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,
    current_user=Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    """
    Get a single user.
    """

    return service.get_user_by_id(user_id)