"""Agent orchestrator for SmartBot."""

from __future__ import annotations

from smartbot.core.interfaces import LLMProvider, MemoryBackend, Message
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

        user_message = Message(role="user", content=user_input)
        self._memory.add_message("user", user_input)

        history = self._memory.get_history()
        logger.debug("History length: %d", len(history))

        response = self._provider.generate_response(
            prompt=user_message,
            history=history,
        )

        logger.debug("Generated response")

        self._memory.add_message("assistant", response.content)

        return response.content
