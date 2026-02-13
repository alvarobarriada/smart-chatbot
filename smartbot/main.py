"""Command-line interface for SmartBot."""

from __future__ import annotations

from smartbot.core.agent import Agent
from smartbot.core.interfaces import MemoryError, ProviderError
from smartbot.memory.in_memory import InMemoryBackend
from smartbot.memory.json_memory import JsonFileMemory
from smartbot.providers.echo_provider import EchoProvider
from smartbot.providers.local_provider import OllamaProvider
from smartbot.providers.models import ChatBotConfig
from smartbot.providers.openai_provider import OpenaiProvider
from smartbot.utils.logger import get_logger, setup_logging
from smartbot.utils.yaml_loader import load_yaml_config

setup_logging()
logger = get_logger(__name__)

PROVIDER_REGISTRY = {
    "echo": EchoProvider,
    "ollama": OllamaProvider,
    "openai": OpenaiProvider,
}


def build_agent(config_path: str = "config.yaml") -> Agent:
    """Create and configure the Agent from YAML configuration.

    :param config_path: defaults to "config.yaml"
    :type config_path: str
    :raises: ValueError
    :return: agent
    :rtype: Agent
    """

    raw_config = load_yaml_config(config_path)
    parsed_config = ChatBotConfig(**raw_config)

    llm_config = parsed_config.llm

    provider_class = PROVIDER_REGISTRY.get(llm_config.provider)

    if provider_class is None:
        raise ValueError(f"Unsupported provider: {llm_config.provider}")

    provider = provider_class(config=llm_config)

    return Agent(
        provider=provider,
        memory = JsonFileMemory(file_path="history.json", max_messages=10)
        #memory=InMemoryBackend(),
    )


def main() -> None:
    agent = build_agent()

    logger.info("SmartBot CLI — type /exit to quit.")

    while True:
        try:
            user_input = input("> ").strip()
        except KeyboardInterrupt:
            logger.info("SmartBot CLI — Exiting the chatbot.")
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
