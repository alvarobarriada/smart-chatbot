from .base import MemoryBackend
from .models import Message, RoleType


class InMemoryBackend(MemoryBackend):
    """
    Guarda el historial en una lista de Python.
    Util para tests o sesiones efimeras.
    """

    def __init__(self):
        # La "base de datos" es una simple lista
        self._messages: list[Message] = []

    def add_message(self, role: RoleType, content: str) -> None:
        new_message = Message(role=role, content=content)
        self._messages.append(new_message)

    def get_context(self) -> list[Message]:
        # Devolvemos una copia para evitar modificaciones accidentales fuera
        return self._messages.copy()

    def clear(self) -> None:
        self._messages = []
