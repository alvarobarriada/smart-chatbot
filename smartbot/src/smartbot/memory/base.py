from abc import ABC, abstractmethod
from typing import Any


class MemoryBackend(ABC):
    """
    Clase abstracta que define como debe comportarse cualquier memoria.
    Patron: Strategy / Interface
    """

    @abstractmethod
    def add_message(self, role: str, content: str) -> None:
        """Guarda un mensaje nuevo (user o assistant)."""
        pass

    @abstractmethod
    def get_context(self) -> list[dict[str, Any]]:
        """Recupera el historial de mensajes para enviarlo al LLM."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Borra la memoria."""
        pass