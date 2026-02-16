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
        messages_history = [
            *history,
            prompt,
        ]

        try:
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
                timeout=60
            )

            response_llm.raise_for_status()

            data = response_llm.json()
            content = data["message"]["content"]

        except requests.exceptions.ConnectionError as error:
            raise RuntimeError(
                f"""Connection error: Could not connect to Ollama at {self.config.base_url}.
                Is it running?"""
                ) from error


        except requests.exceptions.HTTPError as error :
            error_details = response_llm.text
            raise RuntimeError(
                f"Ollama returned an HTTP error {response_llm.status_code}: {error_details}"
                ) from error

        except (ValueError, KeyError) as error:
            raise RuntimeError(
                f"Error processing Ollama's response. Unexpected structure: {error}"
                ) from error

        except requests.exceptions.RequestException as error:
            raise RuntimeError(f"Unexpected communication error with Ollama: {error}") from error

        assistant_message = Message(
            role="assistant",
            content=content,
            timestamp=datetime.now()
        )
        return assistant_message

    def validate_config(self) -> bool:
        try:
            test_request = requests.get(f"{self.config.base_url}/api/tags")
            return test_request.status_code == 200
        except requests.RequestException:
            return False
