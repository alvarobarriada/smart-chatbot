from pathlib import Path
from unittest.mock import patch

import pytest

from smartbot.core.interfaces import MemoryError, Role
from smartbot.memory.json_memory import JsonFileMemory


# ==============================================================================
# SESIÓN 04: FIXTURES (Reusable Setup)
# ==============================================================================
@pytest.fixture
def memory_limit_3(tmp_path: Path) -> JsonFileMemory:
    """Fixture that returns a memory instance with a short limit in a temp folder."""
    temp_file = tmp_path / "history_test.json"
    return JsonFileMemory(file_path=str(temp_file), max_messages=3)

# ==============================================================================
# SESIÓN 02: UNIT TESTS & PARAMETRIZE
# ==============================================================================

@pytest.mark.parametrize("role, content", [
    ("user", "Hello world"),
    ("assistant", "Response"),
    ("system", "Instruction"),
])
def test_add_valid_message(memory_limit_3: JsonFileMemory, role: Role, content: str) -> None:
    """Verify that all valid roles can be stored correctly."""
    memory_limit_3.add_message(role, content)
    history = memory_limit_3.get_history()

    assert len(history) == 1
    assert history[0].role == role
    assert history[0].content == content

def test_add_invalid_message_ignored(memory_limit_3: JsonFileMemory) -> None:
    """Defensive Programming: Empty messages should not be saved."""
    memory_limit_3.add_message("user", "   ")
    assert len(memory_limit_3.get_history()) == 0

def test_add_and_retrieve_message(memory_limit_3: JsonFileMemory) -> None:
    """Verifica que si guardo algo, lo recupero (Happy Path)."""
    # Act
    memory_limit_3.add_message("user", "Hola test")
    history = memory_limit_3.get_history()

    # Assert
    assert len(history) == 1
    assert history[0].content == "Hola test"
    assert history[0].role == "user"

def test_clear_memory(memory_limit_3: JsonFileMemory) -> None:
    """Verifica que clear() borra la lista y el archivo."""
    memory_limit_3.add_message("user", "To be deleted")

    memory_limit_3.clear()

    assert len(memory_limit_3.get_history()) == 0
    assert not memory_limit_3._file_path.exists()

# ==============================================================================
# SESIÓN 06: FUNCTIONAL TESTING (Business Logic + I/O)
# ==============================================================================

def test_rolling_window_logic(memory_limit_3: JsonFileMemory) -> None:
    """Verify that the sliding window removes the oldest messages."""
    # Add 4 messages (limit is 3)
    messages = ["msg1", "msg2", "msg3", "msg4"]
    for m in messages:
        memory_limit_3.add_message("user", m)

    history = memory_limit_3.get_history()

    # Assert
    assert len(history) == 3
    assert history[0].content == "msg2" # Message "1" should be gone
    assert history[-1].content == "msg4"

def test_persistence_between_instances(tmp_path: Path) -> None:
    """Verify that data persists across bot restarts."""
    file = tmp_path / "persist.json"

    # Session 1
    mem1 = JsonFileMemory(file_path=str(file))
    mem1.add_message("user", "I will survive")

    # Session 2 (Simulate restart)
    mem2 = JsonFileMemory(file_path=str(file))
    history = mem2.get_history()

    assert len(history) == 1
    assert history[0].content == "I will survive"

def test_clear_deletes_file(memory_limit_3: JsonFileMemory) -> None:
    """Verify that clear() cleans both RAM and Disk."""
    memory_limit_3.add_message("user", "Delete me")
    assert memory_limit_3._file_path.exists()

    memory_limit_3.clear()

    assert len(memory_limit_3.get_history()) == 0
    assert not memory_limit_3._file_path.exists()

# ==============================================================================
# SESIÓN 05: ERROR HANDLING & MOCKS
# ==============================================================================

def test_io_error_handling(memory_limit_3: JsonFileMemory) -> None:
    """Simulate a disk failure (permissions/space) when saving."""
    with (
        patch("pathlib.Path.write_bytes", side_effect=OSError("Disk full")),
        pytest.raises(MemoryError)
    ):
        memory_limit_3.add_message("user", "Boom")

def test_corrupt_json_recovery(tmp_path: Path) -> None:
    """Verify that if JSON is corrupt, it doesn't crash but starts empty (Fail Safe)."""
    file = tmp_path / "corrupt.json"
    file.write_text("{ this is not json }")

    mem = JsonFileMemory(file_path=str(file))
    assert len(mem.get_history()) == 0 # Should start empty
