"""
=========================================================
JARVIS Authentication Schemas
=========================================================

Schemas used for authentication APIs.

Author: Abhinay Kumar
Project: JARVIS
=========================================================
"""

from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"