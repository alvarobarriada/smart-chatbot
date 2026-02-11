"""YAML configuration loader utilities."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_yaml_config(path: str | Path) -> dict[str, Any]:
    """Load and validate a YAML configuration file.

    The YAML document must have a dictionary at its root level.

    :param path: Path to YAML configuration file.
    :returns: Parsed configuration dictionary.
    :raises FileNotFoundError: If the file does not exist.
    :raises IsADirectoryError: If the path points to a directory.
    :raises PermissionError: If the file cannot be read.
    :raises ValueError: If the YAML is invalid or has an unexpected structure.
    """
    config_path = Path(path).expanduser().resolve()

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    if not config_path.is_file():
        raise IsADirectoryError(f"Configuration path is not a file: {config_path}")

    try:
        with config_path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML syntax in configuration file: {config_path}"
                         ) from e
    except OSError as e:
        raise PermissionError(f"Unable to read configuration file: {config_path}"
                              ) from e

    if data is None:
        return {}

    if not isinstance(data, dict):
        raise ValueError("YAML root element must be a dictionary "
                         f"(got {type(data).__name__})")

    return data
