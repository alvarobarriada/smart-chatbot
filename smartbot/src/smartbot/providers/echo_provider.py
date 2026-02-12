from base import BaseProvider

class EchoProvider(BaseProvider):

    def generate_response(self, prompt: str, history: list[dict[str, str]]) -> str:
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
        return prompt

    def validate_config(self) -> bool:
        return True
