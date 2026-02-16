import pytest

from smartbot.core.interfaces import (
    LLMProvider,
    MemoryBackend,
    MemoryError,
    Message,
    ProviderError,
)


def test_llmprovider_cannot_be_instantiated():
    with pytest.raises(TypeError):
        LLMProvider()


def test_memorybackend_cannot_be_instantiated():
    with pytest.raises(TypeError):
        MemoryBackend()


class DummyLLM(LLMProvider):
    def generate_response(self, prompt: str, history):
        # Llamamos explícitamente al método base para ejecutar
        # el raise NotImplementedError
        return super().generate_response(prompt, history)


def test_llmprovider_generate_response_not_implemented():
    dummy = DummyLLM()

    with pytest.raises(NotImplementedError):
        dummy.generate_response("hi", [])


def test_provider_error_is_runtime_error():
    error = ProviderError("failure")
    assert isinstance(error, RuntimeError)
    assert str(error) == "failure"


def test_memory_error_is_runtime_error():
    error = MemoryError("failure")
    assert isinstance(error, RuntimeError)
    assert str(error) == "failure"


def test_message_typed_dict_structure():
    msg: Message = {
        "role": "user",
        "content": "hello",
        "timestamp": 123.456,
    }

    assert msg["role"] == "user"
    assert msg["content"] == "hello"
    assert isinstance(msg["timestamp"], float)
