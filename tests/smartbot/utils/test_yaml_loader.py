from pathlib import Path
from unittest.mock import patch

import pytest

from smartbot.utils.yaml_loader import load_yaml_config


def test_yaml_valid_file(tmp_path: Path):
    file_path = tmp_path / "config.yaml"
    file_path.write_text("key: value\n", encoding="utf-8")

    config = load_yaml_config(file_path)

    assert config == {"key": "value"}


def test_yaml_valid_file_string_path(tmp_path: Path):
    file_path = tmp_path / "config.yaml"
    file_path.write_text("key: value\n", encoding="utf-8")

    config = load_yaml_config(str(file_path))

    assert config == {"key": "value"}


def test_yaml_empty_file(tmp_path: Path):
    file_path = tmp_path / "empty.yaml"
    file_path.write_text("", encoding="utf-8")

    config = load_yaml_config(file_path)

    assert config == {}


def test_yaml_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_yaml_config("non_existent.yaml")


def test_yaml_not_a_file(tmp_path: Path):
    with pytest.raises(IsADirectoryError):
        load_yaml_config(tmp_path)


def test_yaml_invalid_syntax(tmp_path: Path):
    file_path = tmp_path / "invalid.yaml"
    file_path.write_text("key: [unclosed_list", encoding="utf-8")

    with pytest.raises(ValueError) as exc_info:
        load_yaml_config(file_path)

    assert "Invalid YAML syntax" in str(exc_info.value)


def test_yaml_root_not_dict(tmp_path: Path):
    file_path = tmp_path / "list.yaml"
    file_path.write_text("- item1\n- item2\n", encoding="utf-8")

    with pytest.raises(ValueError) as exc_info:
        load_yaml_config(file_path)

    assert "YAML root element must be a dictionary" in str(exc_info.value)


def test_yaml_permission_error(tmp_path: Path):
    file_path = tmp_path / "config.yaml"
    file_path.write_text("key: value\n", encoding="utf-8")

    # Simulamos OSError al abrir el archivo
    with patch("pathlib.Path.open", side_effect=OSError), pytest.raises(PermissionError):
        load_yaml_config(file_path)
