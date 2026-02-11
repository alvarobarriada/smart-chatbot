import json
import os
from functools import wraps
from typing import Any

from .base import MemoryBackend

DEFAULT_HISTORY_FILE = "conversation_history.json"
DEFAULT_CONTEXT_WINDOW = 10
ALLOWED_ROLES = {"user", "assistant", "system"}

def enforce_valid_role(func):
    """
    Decorador que valida que el rol del mensaje sea correcto antes de guardarlo.
    """
    @wraps(func)
    def wrapper(self, role: str, content: str):
        if role not in ALLOWED_ROLES:
            raise ValueError(f"Rol invalido '{role}'. Permitidos: {ALLOWED_ROLES}")
        if not content.strip():
            raise ValueError("El contenido del mensaje no puede estar vacio.")
        return func(self, role, content)
    return wrapper

class JsonFileMemory(MemoryBackend):
    """
    Gestor de persistencia en archivo JSON con limite de ventana (Context Window).
    """

    def __init__(self, file_path: str = "history.json", max_messages: int = 10):
        self._file_path = file_path
        self._max_messages = max_messages
        self._messages: list[dict[str, Any]] = []
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        """Carga el historial existente si el archivo existe."""
        if os.path.exists(self._file_path):
            try:
                with open(self._file_path, encoding="utf-8") as file:
                    self._messages = json.load(file)
            except json.JSONDecodeError:
                # Si el archivo esta corrupto, empezamos de cero
                self._messages = []

    def _save_to_disk(self) -> None:
        """Guarda el estado actual en disco."""
        with open(self._file_path, "w", encoding="utf-8") as file:
            json.dump(self._messages, file, indent=2, ensure_ascii=False)

    def add_message(self, role: str, content: str) -> None:
       self._messages.append({"role": role, "content": content})
       self._save_to_disk() # Guardamos cada vez que hay un cambio

    def get_context(self) -> list[dict[str, Any]]:
        """
        Devuelve solo los ultimos 'max_messages' para no saturar al LLM.
        """
        # Slicing de listas: [inicio : fin]
        # Si max_messages es 5, tomamos los ultimos 5 (-5:)
        return self._messages[-self._max_messages:]

    def clear(self) -> None:
        self._messages = []
        if os.path.exists(self._file_path):
            os.remove(self._file_path)