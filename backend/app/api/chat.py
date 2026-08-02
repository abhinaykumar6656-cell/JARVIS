"""
=========================================================
JARVIS Chat API
=========================================================

AI Chat endpoints.

Author: Abhinay Kumar
Project: JARVIS
=========================================================
"""

from fastapi import APIRouter, Depends

from app.schemas.chat import ChatRequest
from app.schemas.chat import ChatResponse
from app.services.ai_service import AIService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


def get_ai_service() -> AIService:
    """
    Return AIService instance.
    """

    return AIService()


@router.post(
    "/",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    ai_service: AIService = Depends(get_ai_service),
):
    """
    Chat with JARVIS.
    """

    return ai_service.chat(request)