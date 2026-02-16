from datetime import datetime

import pytest
from pydantic import ValidationError

from smartbot.core.interfaces import (
    LLMProvider,
    MemoryBackend,
    MemoryError,
    Message,
    ProviderError,
)


def test_llmprovider_cannot_be_instantiated() -> None:
    """Ensure LLMProvider cannot be instantiated because it is abstract."""
    with pytest.raises(TypeError):
        LLMProvider() # type: ignore


def test_memorybackend_cannot_be_instantiated() -> None:
    """Ensure MemoryBackend cannot be instantiated because it is abstract."""
    with pytest.raises(TypeError):
        MemoryBackend()  # type: ignore

def test_provider_error_is_runtime_error() -> None:
    """Ensure ProviderError inherits from RuntimeError."""
    error: ProviderError = ProviderError("failure")

    assert isinstance(error, RuntimeError)
    assert str(error) == "failure"


def test_memory_error_is_runtime_error() -> None:
    """Ensure MemoryError inherits from RuntimeError."""
    error: MemoryError = MemoryError("failure")

    assert isinstance(error, RuntimeError)
    assert str(error) == "failure"


def test_message_creation_and_validation() -> None:
    """Ensure Message model validates content and sets timestamp automatically."""
    msg: Message = Message(role="user", content="  hello  ")

    assert msg.role == "user"
    assert msg.content == "hello"
    assert isinstance(msg.timestamp, datetime)


def test_message_rejects_empty_content() -> None:
    """Ensure Message raises ValueError when content is empty or whitespace."""
    with pytest.raises(ValueError):
        Message(role="user", content="   ")


def test_message_is_immutable() -> None:
    """Ensure Message model is immutable (frozen configuration)."""
    msg: Message = Message(role="assistant", content="hello")

    with pytest.raises(ValidationError):
        msg.content = "modified"
