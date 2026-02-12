"""Agent orchestrator for SmartBot."""

from __future__ import annotations

from smartbot.core.interfaces import LLMProvider, MemoryBackend


class Agent:
    """Coordinates provider and memory backends.

    The Agent is responsible for orchestrating the conversation flow
    without knowing concrete implementations.
    """

    def __init__(self, provider: LLMProvider, memory: MemoryBackend) -> None:
        """Initialize the Agent.

        :param provider: Language model provider implementation.
        :param memory: Conversation memory backend.
        """
        self._provider: LLMProvider = provider
        self._memory: MemoryBackend = memory


    def handle_message(self, user_input: str) -> str:
        """Process a user message and return assistant reply.

        :param user_input: Raw user input text.
        :returns: Assistant response.
        :raises ProviderError: If the provider fails to generate output.
        :raises MemoryError: If memory operations fail.
        """
        history = self._memory.get_history()

        response = self._provider.generate_response(
            prompt=user_input,
            history=history,
        )

        self._memory.add_message("user", user_input)
        self._memory.add_message("assistant", response)

        return response
