from datetime import datetime

import requests

from smartbot.core.interfaces import Message

from .models import OllamaConfig


class OllamaProvider:
    def __init__(self, config: OllamaConfig) -> None:
        self.config = config

    def generate_response(self, prompt: Message, history: list[Message]) -> Message:

        """
        Generates a response from the LLM by processing the current prompt and chat history.
        """

        # Añadimos el mensaje actual como dict serializable
        messages_history = [
            *history,
            prompt,
        ]

        response_llm = requests.post(
            f"{self.config.base_url}/api/chat",
            json={
                "model": self.config.model_name,
                "messages": [message.to_dict() for message in messages_history],
                "stream": False,
                "options": {
                    "temperature": self.config.temperature,
                    "top_p": self.config.top_p,
                },
            },
        )
        response_llm.raise_for_status()

        assistant_message = Message(
            role="assistant",
            content=response_llm.json()["message"]["content"],
            timestamp=datetime.now()
        )
        return assistant_message


    def validate_config(self) -> bool:
        try:
            test_request = requests.get(f"{self.config.base_url}/api/tags")
            return test_request.status_code == 200
        except requests.RequestException:
            return False
