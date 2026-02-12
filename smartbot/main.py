"""Command-line interface for SmartBot."""

from __future__ import annotations

from smartbot.core.agent import Agent
from smartbot.core.interfaces import MemoryError, ProviderError
from smartbot.memory.in_memory import InMemoryBackend
from smartbot.providers.echo_provider import EchoProvider
from smartbot.utils.logger import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)

def build_agent() -> Agent:
    """Create and configure the default Agent instance.

    :returns: Configured Agent using in-memory storage and echo provider.
    """
    return Agent(
        provider = EchoProvider(),
        memory = InMemoryBackend(),
    )


def main() -> None:
    """Run SmartBot interactive CLI."""
    agent = build_agent()

    logger.info("SmartBot CLI — type /exit to quit.")

    while True:
        try:
            user_input = input("> ").strip()
        except KeyboardInterrupt:
            logger.info("SmartBot CLI — Exiting the chatbot.\n")
            break

        if not user_input:
            continue

        if user_input == "/exit":
            break

        try:
            response = agent.handle_message(user_input)
        except ProviderError as exc:
            logger.error("Provider error: %s", exc)
            continue
        except MemoryError as exc:
            logger.error("Memory error: %s", exc)
            continue

        logger.info(response)


if __name__ == "__main__":
    main()
