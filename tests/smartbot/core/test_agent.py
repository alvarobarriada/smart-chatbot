import pytest

from smartbot.core.agent import Agent
from smartbot.core.interfaces import LLMProvider, Message
from smartbot.memory.in_memory import InMemoryBackend


class FakeProvider(LLMProvider):
    """Test double that echoes the prompt content."""

    def generate_response(
        self,
        prompt: Message,
        history: list[Message],
    ) -> Message:
        return Message(role="assistant", content=f"echo: {prompt.content}")


def test_agent_full_flow() -> None:
    """Ensure Agent stores messages and returns provider response content."""
    memory: InMemoryBackend = InMemoryBackend()
    provider: FakeProvider = FakeProvider()
    agent: Agent = Agent(provider=provider, memory=memory)

    response: str = agent.handle_message("Hola")

    assert response == "echo: Hola"

    history: list[Message] = memory.get_history()

    assert len(history) == 2
    assert history[0].role == "user"
    assert history[0].content == "Hola"
    assert history[1].role == "assistant"
    assert history[1].content == "echo: Hola"


def test_agent_dependency_injection() -> None:
    """Ensure Agent keeps injected provider and memory references."""
    memory: InMemoryBackend = InMemoryBackend()
    provider: FakeProvider = FakeProvider()

    agent: Agent = Agent(provider=provider, memory=memory)

    assert agent._provider is provider
    assert agent._memory is memory


def test_agent_passes_correct_history_to_provider() -> None:
    """Ensure Agent passes full conversation history to provider."""
    memory: InMemoryBackend = InMemoryBackend()
    provider: FakeProvider = FakeProvider()
    agent: Agent = Agent(provider=provider, memory=memory)

    agent.handle_message("First")
    agent.handle_message("Second")

    history: list[Message] = memory.get_history()

    assert len(history) == 4
    assert history[0].content == "First"
    assert history[2].content == "Second"


def test_agent_handles_multiple_messages() -> None:
    """Ensure Agent accumulates conversation state across calls."""
    memory: InMemoryBackend = InMemoryBackend()
    provider: FakeProvider = FakeProvider()
    agent: Agent = Agent(provider=provider, memory=memory)

    responses: list[str] = [
        agent.handle_message("A"),
        agent.handle_message("B"),
    ]

    assert responses == ["echo: A", "echo: B"]
    assert len(memory.get_history()) == 4
