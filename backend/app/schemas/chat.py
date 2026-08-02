"""
=========================================================
JARVIS Chat Schemas
=========================================================

Schemas used for AI chat.

Author: Abhinay Kumar
Project: JARVIS
=========================================================
"""

from typing import List

from pydantic import BaseModel
from pydantic import Field


class ChatRequest(BaseModel):
    """
    Chat request schema.
    """

    message: str

    history: List[str] = Field(
        default_factory=list,
    )


class ChatResponse(BaseModel):
    """
    Chat response schema.
    """

    response: str