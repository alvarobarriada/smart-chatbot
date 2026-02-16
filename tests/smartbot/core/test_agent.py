import pytest

from smartbot.core.agent import Agent
from smartbot.core.interfaces import LLMProvider, Message
from smartbot.memory.in_memory import InMemoryBackend


class FakeProvider(LLMProvider):
    def generate_response(
        self,
        prompt: str,
        history: list[Message],
    ) -> Message:
        return Message(role="assistant", content=f"echo: {prompt}")


def test_agent_flow():
    memory = InMemoryBackend()
    provider = FakeProvider()
    agent = Agent(provider=provider, memory=memory)

    response = agent.handle_message("Hola")

    assert response == "echo: Hola"

    history = memory.get_history()

    assert len(history) == 2
    assert history[0].role == "user"
    assert history[1].role == "assistant"


def test_agent_injection():
    memory = InMemoryBackend()
    provider = FakeProvider()

    agent = Agent(provider=provider, memory=memory)

    assert agent._provider is provider
    assert agent._memory is memory


# -----------------------------
# Cobertura de normalización
# -----------------------------

class DataclassLikeMessage:
    def __init__(self):
        self.role = "user"
        self.content = "hola"

    def to_dict(self):
        return {"role": self.role, "content": self.content}


def test_agent_normalizes_dataclass_messages():
    memory = InMemoryBackend()
    provider = FakeProvider()
    agent = Agent(provider=provider, memory=memory)

    memory._messages = [DataclassLikeMessage()]  # type: ignore

    response = agent.handle_message("Test")

    assert response == "echo: Test"


def test_agent_raises_on_invalid_message_type():
    memory = InMemoryBackend()
    provider = FakeProvider()
    agent = Agent(provider=provider, memory=memory)

    memory._messages = [object()]  # type: ignore

    with pytest.raises(TypeError):
        agent.handle_message("Test")
