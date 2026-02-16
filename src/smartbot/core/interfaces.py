"""Core interfaces for SmartBot.

This module defines abstract base classes used by the Agent to interact
with language model Providers and Memory backends.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

Role = Literal["user", "assistant", "system"]

class Message(BaseModel):
    """
    Data Transfer Object (DTO) que representa un mensaje.
    Principio: Estructura de Datos (solo guarda datos, sin lógica).
    """
    role: Role
    content: str = Field(min_length=1)
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        frozen = True

    @field_validator('content')
    @classmethod
    def clean_content(cls, v: str) -> str:
        """Limpia espacios en blanco y valida que no quede vacío."""
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("El contenido no puede estar vacío (solo espacios)")
        return cleaned

    def to_dict(self) -> dict:
        """Serializo el objeto para guardarlo en JSON."""
        return self.model_dump()

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
