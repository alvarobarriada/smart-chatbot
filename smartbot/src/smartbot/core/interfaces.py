"""Core interfaces for SmartBot.

This module defines abstract base classes used by the Agent to interact
with language model providers and memory backends.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Literal, TypedDict  # sugeridos por robustez en tipado (vs Set/Dict)

Role = Literal["user", "assistant", "system"]

class Message(TypedDict):
    """Represents a single chat message."""
    role: Role
    content: str
    timestamp: float


class ProviderError(RuntimeError):
    """Raised when a provider fails to generate a response."""


class MemoryError(RuntimeError):
    """Raised when a memory backend fails."""


class LLMProvider(ABC):
    """Abstract interface for language model providers."""

    @abstractmethod
    def generate_response(self, prompt: str, history: list[Message]) -> str:
        """Generate a reply from the assistant.

        :param prompt: Latest user message.
        :param history: Conversation history.
        :returns: Assistant reply.
        :raises ProviderError: If the provider fails.
        """
        raise NotImplementedError


class MemoryBackend(ABC):
    """Abstract interface for conversation memory backends."""

    @abstractmethod
    def add_message(self, role: Role, content: str) -> None:
        """Store a new message.

        :param role: Message role (user/assistant/system).
        :param content: Message content.
        """

    @abstractmethod
    def get_history(self) -> list[Message]:
        """Return stored conversation history.

        :returns: List of messages.
        """

    @abstractmethod
    def clear(self) -> None:
        """Remove all stored messages."""
