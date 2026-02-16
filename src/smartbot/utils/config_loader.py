"""Environment configuration loader utilities."""

from __future__ import annotations

from dotenv import dotenv_values, load_dotenv


def load_env(path: str | None = None) -> dict[str, str]:
    """Load environment variables from a .env file.

    :param path: Optional path to the .env file.
    :type: string or None
    :returns: Dictionary with environment variables.
    :rtype: dict[tr, str]
    """
    load_dotenv(dotenv_path=path)
    values = dotenv_values(dotenv_path=path)

    return {key: value for key, value in values.items() if value is not None}
