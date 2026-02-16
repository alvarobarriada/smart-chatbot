"""Core interfaces for SmartBot.

This module defines abstract base classes used by the Agent to interact
with language model Providers and Memory backends.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Literal

Role = Literal["user", "assistant", "system"]

@dataclass(frozen=True)
class Message:
    """
    Data Transfer Object (DTO) que representa un mensaje.
    Principio: Estructura de Datos (solo guarda datos, sin lógica).
    """
    role: Role
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        """Serializo el objeto para guardarlo en JSON."""
        return asdict(self)

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
    def add_message(self, message: Message) -> None:
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
