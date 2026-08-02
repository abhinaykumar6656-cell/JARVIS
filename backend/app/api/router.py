"""
=========================================================
JARVIS API Router
=========================================================

Registers all API endpoints.

Author: Abhinay Kumar
Project: JARVIS
=========================================================
"""

from fastapi import APIRouter

from app.api.admin import router as admin_router
from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.api.health import router as health_router
from app.api.system import router as system_router
from app.api.users import router as users_router

api_router = APIRouter()

# Authentication
api_router.include_router(auth_router)

# Chat
api_router.include_router(chat_router)

# Admin
api_router.include_router(admin_router)

# Health
api_router.include_router(health_router)

# System
api_router.include_router(system_router)

# Users
api_router.include_router(users_router)