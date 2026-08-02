"""
=========================================================
JARVIS Admin API
=========================================================

Administrator-only endpoints.

Author: Abhinay Kumar
Project: JARVIS
=========================================================
"""

from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_admin

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get("/dashboard")
def admin_dashboard(
    current_admin=Depends(get_current_admin),
):
    """
    Administrator dashboard.
    """

    return {
        "message": "Welcome Administrator!",
        "username": current_admin.username,
        "role": "Administrator",
        "system": "JARVIS",
    }