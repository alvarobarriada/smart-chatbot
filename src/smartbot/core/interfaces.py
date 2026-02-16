"""Core interfaces for SmartBot.

This module defines abstract base classes used by the Agent to interact
with language model Providers and Memory backends.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

Role = Literal["user", "assistant", "system"]

class Message(BaseModel):
    """
    Data Transfer Object (DTO) that represents a Message.
    Principle: Data Strcuture (just saves data, no logic).
    """
    role: Role
    content: str = Field(min_length=1)
    timestamp: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(frozen=True)

    @field_validator('content')
    @classmethod
    def clean_content(cls, v: str) -> str:
        """Cleans the whitespaces and validates it isn't empty."""
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("The content can't be empty.")
        return cleaned

    def to_dict(self) -> dict:
        """Serializes the object to save it in JSON (without timestamp)."""
        return {
            "role": self.role,
            "content": self.content,
        }

class ProviderError(RuntimeError):
    """Raised when a provider fails to generate a response."""


class MemoryError(RuntimeError):
    """Raised when a memory backend fails."""


class LLMProvider(ABC):
    """Abstract interface for language model providers."""

    @abstractmethod
    def generate_response(self, prompt: Message, history: list[Message]) -> Message:
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
