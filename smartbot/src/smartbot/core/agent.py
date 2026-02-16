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
        """
        Docstring for __init__

        :param: self
        :param provider: normally Echo (repeat message) or Ollama
        :type provider: LLMProvider
        :param memory: manages conversation's history
        :type memory: MemoryBackend
        """
        self._provider: LLMProvider = provider
        self._memory: MemoryBackend = memory

    def _normalize_history(self, history: list[Any]) -> list[dict[str, Any]]:
        """
        Normalize history into a list of serializable dictionaries.
        Supports both TypedDict and dataclass-based Message objects.

        :param: history
        :type history: list[Any]
        :raises TypeError
        :return: normalized
        :rtype: list[dict[str, Any]]
        """
        normalized: list[dict[str, Any]] = []

        for message in history:
            if isinstance(message, dict):
                normalized.append(message)
            elif hasattr(message, "to_dict"):
                normalized.append(message.to_dict())
            else:
                raise TypeError(
                    f"Unsupported message type in history: {type(message).__name__}"
                )

        return normalized

    def handle_message(self, user_input: str) -> str:
        """
        Process a user message and return assistant reply.

        :param self
        :param user_input: whatever the user writes
        :type user_input: str
        :return: assistant's response to user's request
        :rtype: str
        """

        logger.debug("Handling message from user")

        self._memory.add_message("user", user_input)

        history = self._memory.get_history()
        logger.debug("History length: %d", len(history))

        normalized_history = self._normalize_history(history)

        response = self._provider.generate_response(
            prompt=user_input,
            history=normalized_history,
        )

        logger.debug("Generated response")

        self._memory.add_message("assistant", response)

        return response
