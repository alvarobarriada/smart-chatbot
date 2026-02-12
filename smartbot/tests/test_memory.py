import tempfile
import time
from pathlib import Path

import pytest

from smartbot.memory.in_memory import InMemoryBackend
from smartbot.memory.json_memory import JsonFileMemory

# ------------------------
# InMemoryBackend
# ------------------------

def test_inmemory_add_and_get():
    memory = InMemoryBackend()

    memory.add_message("user", "Hola")

    history = memory.get_history()

    assert len(history) == 1
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "Hola"
    assert isinstance(history[0]["timestamp"], float)


def test_inmemory_clear():
    memory = InMemoryBackend()
    memory.add_message("user", "Hola")
    memory.clear()

    assert memory.get_history() == []


def test_inmemory_returns_copy():
    memory = InMemoryBackend()
    memory.add_message("user", "Hola")

    history = memory.get_history()
    history.append({"role": "user", "content": "hack", "timestamp": time.time()})

    # No debe modificarse la memoria interna
    assert len(memory.get_history()) == 1


# ------------------------
# JsonFileMemory
# ------------------------

def test_json_memory_persistence():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        file_path = tmp.name

    memory = JsonFileMemory(file_path=file_path, max_messages=5)
    memory.add_message("user", "Hola")

    # Nueva instancia debe cargar del disco
    memory2 = JsonFileMemory(file_path=file_path, max_messages=5)
    history = memory2.get_history()

    assert len(history) == 1
    assert history[0]["content"] == "Hola"

    Path(file_path).unlink()


def test_json_memory_window():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        file_path = tmp.name

    memory = JsonFileMemory(file_path=file_path, max_messages=2)

    memory.add_message("user", "1")
    memory.add_message("assistant", "2")
    memory.add_message("user", "3")

    history = memory.get_history()

    assert len(history) == 2
    assert history[0]["content"] == "2"
    assert history[1]["content"] == "3"

    Path(file_path).unlink()


def test_json_memory_invalid_role():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        file_path = tmp.name

    memory = JsonFileMemory(file_path=file_path)

    with pytest.raises(ValueError):
        memory.add_message("invalid", "Hola")

    Path(file_path).unlink()


def test_json_memory_empty_content():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        file_path = tmp.name

    memory = JsonFileMemory(file_path=file_path)

    with pytest.raises(ValueError):
        memory.add_message("user", "   ")

    Path(file_path).unlink()
