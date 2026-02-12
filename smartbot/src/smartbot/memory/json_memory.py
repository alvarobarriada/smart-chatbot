import json
import time
from functools import wraps
from pathlib import Path

from smartbot.core.interfaces import MemoryBackend, Message, Role

ALLOWED_ROLES = {"user", "assistant", "system"}
DEFAULT_HISTORY_FILE = "conversation_history.json"
DEFAULT_CONTEXT_WINDOW = 10


def enforce_valid_role(func):
    """
    Decorador que valida que el rol del mensaje sea correcto antes de guardarlo.
    """

    @wraps(func)
    def wrapper(self, role: Role, content: str):
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

    def __init__(
        self,
        file_path: str = DEFAULT_HISTORY_FILE,
        max_messages: int = DEFAULT_CONTEXT_WINDOW,
    ):
        self._file_path = Path(file_path)
        self._max_messages = max_messages
        self._messages: list[Message] = []
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        """Carga el historial existente si el archivo existe."""
        if not self._file_path.exists():
            return

        try:
            with self._file_path.open(encoding="utf-8") as file:
                self._messages = json.load(file)
        except json.JSONDecodeError:
            # Si el archivo esta corrupto, empezamos de cero
            self._messages = []

    def _save_to_disk(self) -> None:
        """Guarda el estado actual en disco."""
        with self._file_path.open("w", encoding="utf-8") as file:
            json.dump(self._messages, file, indent=2, ensure_ascii=False)

    @enforce_valid_role
    def add_message(self, role: Role, content: str) -> None:
        message: Message = {
            "role": role,
            "content": content,
            "timestamp": time.time(),
        }
        self._messages.append(message)
        self._save_to_disk()

    def get_history(self) -> list[Message]:
        """
        Devuelve solo los ultimos 'max_messages' para no saturar al LLM.
        """
        return self._messages[-self._max_messages:]

    def clear(self) -> None:
        self._messages = []
        if self._file_path.exists():
            self._file_path.unlink()
