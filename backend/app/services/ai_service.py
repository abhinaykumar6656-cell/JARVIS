"""
=========================================================
JARVIS AI Service
=========================================================

Handles AI conversations using Ollama.

Author: Abhinay Kumar
Project: JARVIS
=========================================================
"""

from typing import Final

import requests
from requests.exceptions import ConnectionError
from requests.exceptions import RequestException
from requests.exceptions import Timeout

from app.schemas.chat import ChatRequest
from app.schemas.chat import ChatResponse


class AIService:
    """
    Business logic for AI conversations.
    """

    OLLAMA_URL: Final = "http://127.0.0.1:11434/api/generate"

    MODEL: Final = "llama3.2"

    SYSTEM_PROMPT: Final = """
You are JARVIS.

You are an intelligent AI assistant created by Abhinay Kumar.

Rules:

- Always be friendly.
- Always be professional.
- Always answer naturally.
- Remember the conversation history provided.
- If the user already introduced themselves, use their name.
- Keep answers concise unless asked otherwise.
"""

    def __init__(self):
        """
        Initialize AI service.
        """
        pass

    def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        """
        Generate AI response using Ollama.
        """

        message = request.message.strip()

        if not message:
            return ChatResponse(
                response="Please enter a message."
            )

        history = ""

        if request.history:

            history = "\n".join(
                request.history
            )

        prompt = (
            f"{self.SYSTEM_PROMPT}\n\n"
            f"{history}\n\n"
            f"User: {message}\n"
            f"JARVIS:"
        )

        payload = {
            "model": self.MODEL,
            "prompt": prompt,
            "stream": False,
        }

        try:

            response = requests.post(
                self.OLLAMA_URL,
                json=payload,
                timeout=120,
            )

            response.raise_for_status()

            data = response.json()

            answer = data.get(
                "response",
                "No response received.",
            )

            return ChatResponse(
                response=answer.strip(),
            )

        except ConnectionError:

            return ChatResponse(
                response=(
                    "Unable to connect to Ollama. "
                    "Please make sure Ollama is running."
                )
            )

        except Timeout:

            return ChatResponse(
                response="Ollama request timed out."
            )

        except RequestException as exc:

            return ChatResponse(
                response=f"Ollama request failed: {exc}"
            )

        except Exception as exc:

            return ChatResponse(
                response=f"Unexpected error: {exc}"
            )