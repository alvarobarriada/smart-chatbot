from smartbot.memory.models import Message

from .base import BaseProvider
from .models import EchoConfig, OllamaConfig, OpenAIConfig


class EchoProvider(BaseProvider):

    def generate_response(self, prompt: str, history: list[dict[str, str]]) -> Message:
        """Processes the user input and conversation history to generate a contextually
        aware response.

        :param prompt: The current text input or instruction from the user.
        :type prompt: str
        :param history: A list of previous message exchanges, where each dictionary typically
        contains 'role' and 'content' keys.
        :type history: list[dict[str, str]]

        :return: The generated text response.
        :rtype: str
        """
        return Message(role="assistant",content=prompt)

    def validate_config(self) -> bool:
        return True

    def __init__(self, config: OpenAIConfig | OllamaConfig | EchoConfig) -> None:
        self.config = config

