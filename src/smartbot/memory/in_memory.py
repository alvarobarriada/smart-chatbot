from smartbot.core.interfaces import MemoryBackend, Message, Role


class InMemoryBackend(MemoryBackend):
    """
    Volatile in-memory storage (RAM).
    Useful for testing or ephemeral sessions where persistence is not required.
    """
    def __init__(self) -> None:
        self._messages: list[Message] = []

    def add_message(self, role: Role, content: str) -> None:
        """Create and store a message in RAM."""
        # Pydantic automatically validates upon instantiation
        new_msg = Message(role=role, content=content)
        self._messages.append(new_msg)

    def get_history(self) -> list[Message]:
        """Return a copy of the history."""
        return self._messages.copy()

    def clear(self) -> None:
        """Clear the in-memory list."""
        self._messages.clear()
