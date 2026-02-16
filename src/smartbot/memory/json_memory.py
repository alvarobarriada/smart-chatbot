import json
import logging
from pathlib import Path

from pydantic import TypeAdapter, ValidationError

from smartbot.core.interfaces import MemoryBackend, MemoryError, Message, Role

# CLEAN CODE: Constants to avoid magic numbers
DEFAULT_HISTORY_FILE = "conversation_history.json"
DEFAULT_CONTEXT_WINDOW = 10
ENCODING = "utf-8"

logger = logging.getLogger(__name__)

class JsonFileMemory(MemoryBackend):
    """
    JSON file persistence manager with history rotation.

    Implements the Single Responsibility Principle by handling both I/O
    operations and state management for the conversation history.
    """
    def __init__(
        self,
        file_path: str = DEFAULT_HISTORY_FILE,
        max_messages: int = DEFAULT_CONTEXT_WINDOW,
    ):
        """
        Initialize the persistent memory backend.

        :param file_path: Path to the JSON file where history is stored.
        :param max_messages: Maximum number of messages to retain (sliding window).
        :raises ValueError: If max_messages is less than 1.
        """
        self._file_path = Path(file_path)
        self._max_messages = max_messages
        self._messages: list[Message] = []

        # DEFENSIVE PROGRAMMING: Validate inputs at startup
        if max_messages < 1:
            raise ValueError("max_messages debe ser al menos 1.")

        self._load_memory()

    def _load_memory(self) -> None:
        """Load and validate history from disk using Pydantic."""
        if not self._file_path.exists():
            logger.info(f"Memory file not found at {self._file_path}. Starting empty.")
            return

        try:
            json_content = self._file_path.read_text(encoding=ENCODING)

            adapter = TypeAdapter(list[Message])
            self._messages = adapter.validate_json(json_content)

            logger.debug(f"Loaded {len(self._messages)} messages.")

        except (ValidationError, json.JSONDecodeError) as error:
            logger.warning(f"Corrupt memory at {self._file_path}. Resetting history: {error}")
            self._messages = []

    def _save_memory(self) -> None:
        """Save the current state to disk atomically."""
        try:
            adapter = TypeAdapter(list[Message])

            json_bytes = adapter.dump_json(self._messages, indent=2)

            self._file_path.write_bytes(json_bytes)

        except OSError as error:
            logger.error(f"Critical error saving memory to {self._file_path}: {error}")
            raise MemoryError("I/O failure while saving history") from error

    def add_message(self, role: Role, content: str) -> None:
        """
        Add a new message, apply rotation, and persist changes.

        :param role: The role of the sender (user, assistant, system).
        :param content: The content of the message.
        """
        try:
            # DATA MODELING: Pydantic validates role and content here
            new_msg = Message(role=role, content=content)

            self._messages.append(new_msg)
            self._prune_history()
            self._save_memory()

        except ValidationError as error:
            logger.error(f"Attempted to save invalid message: {error}")

    def _prune_history(self) -> None:
        """Keep the in-memory list within the configured limit."""
        if len(self._messages) > self._max_messages:
            self._messages = self._messages[-self._max_messages:]

    def get_history(self) -> list[Message]:
        """
        Return a copy of the current history.

        :return: List of immutable Message objects.
        """
        # CLEAN CODE: Return a copy to avoid accidental external mutation
        return self._messages[-self._max_messages:].copy()

    def clear(self) -> None:
        """Clear memory and delete the persistence file."""
        self._messages = []
        try:
            self._file_path.unlink(missing_ok=True)
            logger.info(f"Memory cleared and file {self._file_path} deleted.")
        except OSError as error:
            logger.error(f"Error deleting memory file: {error}")
