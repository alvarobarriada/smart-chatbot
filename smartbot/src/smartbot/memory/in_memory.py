from typing import Any

from .base import MemoryBackend


class InMemoryBackend(MemoryBackend):
    """
    Guarda el historial en una lista de Python.
    Util para tests o sesiones efimeras.
    """

    def __init__(self):
        # La "base de datos" es una simple lista
        self._messages: list[dict[str, Any]] = []

    def add_message(self, role: str, content: str) -> None:
        message = {"role": role, "content": content}
        self._messages.append(message)

    def get_context(self) -> list[dict[str, Any]]:
        # Devolvemos una copia para evitar modificaciones accidentales fuera
        return self._messages.copy()

    def clear(self) -> None:
        self._messages = []