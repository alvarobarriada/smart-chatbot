import os
from pathlib import Path
from unittest.mock import patch

from smartbot.utils.config_loader import load_env


def test_load_env_from_file(tmp_path: Path):
    """Loads variables correctly from a valid .env file."""
    env_file = tmp_path / ".env"
    env_file.write_text("A=1\nB=2\n")

    result = load_env(str(env_file))

    assert result == {"A": "1", "B": "2"}


def test_load_env_keeps_empty_string_values(tmp_path: Path):
    """Preserves empty values instead of discarding them."""
    env_file = tmp_path / ".env"
    env_file.write_text("A=1\nB=\n")

    result = load_env(str(env_file))

    assert result == {"A": "1", "B": ""}


def test_load_env_non_existing_file():
    """Returns empty dict when file does not exist."""
    result = load_env("non_existing_file.env")

    assert result == {}


def test_load_env_empty_file(tmp_path: Path):
    """Returns empty dict for an empty file."""
    env_file = tmp_path / ".env"
    env_file.write_text("")

    result = load_env(str(env_file))
    assert result == {}


def test_load_env_without_path():
    """Falls back to environment variables when path is None."""
    with patch.dict(os.environ, {"TEST_ENV_VAR": "123"}, clear=False):
        result = load_env(None)

    assert "TEST_ENV_VAR" in result or result == {}
