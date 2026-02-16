import json
import logging
from pathlib import Path

from pydantic import TypeAdapter, ValidationError

from smartbot.core.interfaces import MemoryBackend, MemoryError, Message, Role

DEFAULT_HISTORY_FILE = "conversation_history.json"
DEFAULT_CONTEXT_WINDOW = 10

logger = logging.getLogger(__name__)

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

        if max_messages < 1:
            raise ValueError("max_messages debe ser al menos 1.")

        self._load_memory()

    def _load_memory(self) -> None:
        """Carga el historial existente si el archivo existe."""
        if not self._file_path.exists():
            return

        try:
            json_content = self._file_path.read_text(encoding="utf-8")

            adapter = TypeAdapter(list[Message])
            self._messages = adapter.validate_json(json_content)

            logger.debug(f"Cargados {len(self._messages)} mensajes validados.")

        except (ValidationError, json.JSONDecodeError) as e:
            logger.error(f"Datos corruptos en {self._file_path}: {e}")
            self._messages = []

    def _save_memory(self) -> None:
        """Guarda el estado actual en disco."""
        try:
            adapter = TypeAdapter(list[Message])

            json_bytes = adapter.dump_json(self._messages, indent=2)

            self._file_path.write_bytes(json_bytes)

        except OSError as e:
            msg = f"No se pudo escribir en {self._file_path}"
            logger.error(msg)
            raise MemoryError(msg) from e

    def add_message(self, role: Role, content: str) -> None:
        try:
            new_msg = Message(role=role, content=content)

            self._messages.append(new_msg)
            self._prune_history()
            self._save_memory()

        except ValidationError as e:
            logger.error(f"Intento de guardar mensaje inválido: {e}")

    def _prune_history(self) -> None:
        if len(self._messages) > self._max_messages:
            self._messages = self._messages[-self._max_messages:]

    def get_history(self) -> list[Message]:
        """Devuelve los últimos N mensajes (Rolling Window)."""
        return self._messages[-self._max_messages:].copy()

    def clear(self) -> None:
        self._messages = []
        if self._file_path.exists():
            self._file_path.unlink()
