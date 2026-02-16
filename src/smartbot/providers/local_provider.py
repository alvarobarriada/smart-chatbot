import requests

from smartbot.memory.models import Message

from .models import OllamaConfig


class OllamaProvider:
    def __init__(self, config: OllamaConfig) -> None:
        self.config = config

    def generate_response(self, prompt: str, history: list[Message]) -> Message:

        """
        Generates a response from the LLM by processing the current prompt and chat history.
        """

        # Añadimos el mensaje actual como dict serializable
        messages_history = [
            *history,
            {"role": "user", "content": prompt},
        ]

        response_llm = requests.post(
            f"{self.config.base_url}/api/chat",
            json={
                "model": self.config.model_name,
                "messages": messages_history,
                "stream": False,
                "options": {
                    "temperature": self.config.temperature,
                    "top_p": self.config.top_p,
                },
            },
        )
        response_llm.raise_for_status()

        return response_llm.json()["message"]["content"]


    def validate_config(self) -> bool:
        try:
            test_request = requests.get(f"{self.config.base_url}/api/tags")
            return test_request.status_code == 200
        except requests.RequestException:
            return False
