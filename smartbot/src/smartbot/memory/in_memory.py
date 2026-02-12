import time

from smartbot.core.interfaces import MemoryBackend, Message, Role


class InMemoryBackend(MemoryBackend):
    """
    In-memory conversation storage.
    Useful for testing or ephemeral sessions.
    """

    def __init__(self) -> None:
        self._messages: list[Message] = []

    def add_message(self, role: Role, content: str) -> None:
        message: Message = {
            "role": role,
            "content": content,
            "timestamp": time.time(),
        }
        self._messages.append(message)

    def get_history(self) -> list[Message]:
        return self._messages.copy()

    def clear(self) -> None:
        self._messages.clear()
