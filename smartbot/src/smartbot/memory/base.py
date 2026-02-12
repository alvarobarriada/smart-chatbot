from abc import ABC, abstractmethod

from .models import Message, RoleType


class MemoryBackend(ABC):
    """
    Clase abstracta que define como debe comportarse cualquier memoria.
    Patron: Strategy / Interface
    """

    @abstractmethod
    def add_message(self, role: RoleType, content: str) -> None:
        """Guarda un mensaje nuevo (user o assistant)."""

    @abstractmethod
    def get_context(self) -> list[Message]:
        """Recupera el historial de mensajes para enviarlo al LLM."""

    @abstractmethod
    def clear(self) -> None:
        """Borra la memoria."""
