"""Command-line interface for SmartBot."""

from __future__ import annotations

from smartbot.core.agent import Agent
from smartbot.core.interfaces import MemoryError, ProviderError
from smartbot.memory.in_memory import InMemory
from smartbot.providers.echo_provider import EchoProvider


def build_agent() -> Agent:
    """Create and configure the default Agent instance.

    :returns: Configured Agent using in-memory storage and echo provider.
    """
    return Agent(
        provider=EchoProvider(),
        memory=InMemory(),
    )


def main() -> None:
    """Run SmartBot interactive CLI."""
    agent = build_agent()

    print("SmartBot CLI — type /exit to quit.")

    while True:
        try:
            user_input = input("> ").strip()
        except KeyboardInterrupt:
            print("\nExiting the chatbot.\n")
            break

        if not user_input:
            continue

        if user_input == "/exit":
            break

        try:
            response = agent.handle_message(user_input)
        except ProviderError as exc:
            print(f"Provider error: {exc}")
            continue
        except MemoryError as exc:
            print(f"Memory error: {exc}")
            continue

        print(response)


if __name__ == "__main__":
    main()
