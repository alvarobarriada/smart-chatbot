from smartbot.core.agent import Agent
from smartbot.core.interfaces import LLMProvider
from smartbot.memory.in_memory import InMemoryBackend


class FakeProvider(LLMProvider):
    def generate_response(self, prompt: str, history: list) -> str:
        return f"echo: {prompt}"


def test_agent_flow():
    memory = InMemoryBackend()
    provider = FakeProvider()
    agent = Agent(provider=provider, memory=memory)

    response = agent.handle_message("Hola")

    assert response == "echo: Hola"

    history = memory.get_history()

    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[1]["role"] == "assistant"


def test_agent_injection():
    memory = InMemoryBackend()
    provider = FakeProvider()

    agent = Agent(provider=provider, memory=memory)

    assert agent._provider is provider
    assert agent._memory is memory
