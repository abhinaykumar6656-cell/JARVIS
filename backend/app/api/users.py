"""
=========================================================
JARVIS User API
=========================================================

REST API endpoints for user management.

Author: Abhinay Kumar
Project: JARVIS
=========================================================
"""

from fastapi import APIRouter
from fastapi import Depends

from app.core.dependencies import get_user_service
from app.schemas import UserCreate
from app.schemas import UserResponse
from app.services import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=201,
    summary="Create User",
    description="Create a new user.",
)
def create_user(
    user: UserCreate,
    service: UserService = Depends(get_user_service),
):
    """
    Create a new user.
    """

    return service.create_user(user)


@router.get(
    "/",
    response_model=list[UserResponse],
    summary="List Users",
)
def get_all_users(
    service: UserService = Depends(get_user_service),
):
    """
    Return all users.
    """

    return service.get_all_users()


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get User by ID",
)
def get_user_by_id(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    """
    Return a user by ID.
    """

    return service.get_user_by_id(user_id)