"""Agent orchestrator for SmartBot."""

from __future__ import annotations

from typing import Any

from smartbot.core.interfaces import LLMProvider, MemoryBackend
from smartbot.utils.logger import get_logger

logger = get_logger(__name__)


class Agent:
    """Coordinates provider and memory backends.

    The Agent is responsible for orchestrating the conversation flow
    without knowing concrete implementations.
    """

    def __init__(self, provider: LLMProvider, memory: MemoryBackend) -> None:
        self._provider: LLMProvider = provider
        self._memory: MemoryBackend = memory

    def _normalize_history(self, history: list[Any]) -> list[dict[str, Any]]:
        """
        Normalize history into a list of serializable dictionaries.
        Supports both TypedDict and dataclass-based Message objects.
        """
        normalized: list[dict[str, Any]] = []

        for msg in history:
            if isinstance(msg, dict):
                normalized.append(msg)
            elif hasattr(msg, "to_dict"):
                normalized.append(msg.to_dict())
            else:
                raise TypeError(
                    f"Unsupported message type in history: {type(msg).__name__}"
                )

        return normalized

    def handle_message(self, user_input: str) -> str:
        """Process a user message and return assistant reply."""

        logger.debug("Handling message from user")

        # Guardar mensaje del usuario
        self._memory.add_message("user", user_input)

        history = self._memory.get_history()
        logger.debug("History length: %d", len(history))

        # Normalizar antes de enviar al provider
        normalized_history = self._normalize_history(history)

        response = self._provider.generate_response(
            prompt=user_input,
            history=normalized_history,
        )

        logger.debug("Generated response")

        # Guardar respuesta del asistente
        self._memory.add_message("assistant", response)

        return response
