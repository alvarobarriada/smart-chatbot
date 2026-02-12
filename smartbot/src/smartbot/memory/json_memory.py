import json
import logging
from functools import wraps
from pathlib import Path

from .base import MemoryBackend
from .models import Message, RoleType

# Configuración de Logging
logger = logging.getLogger(__name__)

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

class JsonMemoryError(Exception):
    """Excepción específica para errores de memoria."""

class JsonFileMemory(MemoryBackend):
    """
    Gestor de persistencia en archivo JSON con limite de ventana (Context Window).
    """

    def __init__(self, file_path: str = "history.json", max_messages: int = 10):
        self.file_path = Path(file_path)
        self.max_messages = max_messages
        self._messages: list[Message] = []

        # Programacion defensiva: Validar inputs en el constructor
        if max_messages < 1:
            raise ValueError("Max_messages debe ser al menos 1.")

        self._load_memory()

    def _load_memory(self) -> None:
        """Carga el historial existente si el archivo existe."""
        if not self.file_path.exists():
            logger.info(f"Archivo de memoria {self.file_path} no existe. Iniciando.")
            return

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                raw_data = json.load(file)

            # Programacion defensiva: Validar que lo que leemos es una lista
            if not isinstance(raw_data, list):
                logger.warning("El archivo de memoria esta corrupto (no es una lista).")
                self._messages = []
                return

            # Convertimos dicts a objetos Message (Type Safety)
            self._messages = [Message(**msg) for msg in raw_data]
            logger.debug(f"Cargados {len(self._messages)} mensajes: {self.file_path}")

        except (json.JSONDecodeError, TypeError) as e:
                logger.critical(f"Error critico cargando memoria: {e}")
                # Si el archivo esta corrupto, empezamos de cero
                self._messages = []

    def _save_memory(self) -> None:
        """Guarda el estado actual en disco."""
        try:
            data_to_save = [msg.to_dict() for msg in self._messages]

            with self.file_path.open("w", encoding="utf-8")as file:
                json.dump(data_to_save, file, indent=2, ensure_ascii=False)

        except OSError as e:
            # Excepción específica con contexto
            logger.error(f"No se pudo escribir: {self.file_path}. Permisos insuficien.")
            raise JsonMemoryError(f"Fallo al guardar historial: {e}") from e

    def add_message(self, role: RoleType, content: str) -> None:
       # Programacion defensiva: Guard clause para inputs vacios
       if not content or not content.strip():
           logger.warning("Intento de guardar mensaje vacio. Ignorado")
           return

       # Creamos el objeto inmutable
       new_msg = Message(role=role, content=content)

       self._messages.append(new_msg)
       self._prune_history()
       self._save_memory() # Guardamos cada vez que hay un cambio

    def _prune_history(self) -> None:
        """Mantiene la ventana deslizante."""
        if len(self._messages) > self.max_messages:
            removed_count = len(self._messages) - self.max_messages
            self._messages = self._messages[-self.max_messages:]
            logger.debug(f"Recortados {removed_count} mensajes antiguos.")


    def get_context(self) -> list[Message]:
        """
        Devuelve solo los ultimos 'max_messages' para no saturar al LLM.
        """
        # Slicing de listas: [inicio : fin]
        # Si max_messages es 5, tomamos los ultimos 5 (-5:)
        return self._messages.copy()

    def clear(self) -> None:
        self._messages = []
        try:
            self.file_path.unlink(missing_ok=True)
            logger.info("Memoria borrada y archivo eliminado.")
        except OSError as e:
            logger.error(f"Error al borrar archivo de memoria: {e}")
