"""Environment configuration loader utilities."""

from __future__ import annotations

from dotenv import dotenv_values, load_dotenv


def load_env(path: str | None = None) -> dict[str, str]:
    """Load environment variables from a .env file.

    :param path: Optional path to the .env file.
    :returns: Dictionary with environment variables.
    """
    # Load into os.environ for libraries that rely on it
    load_dotenv(dotenv_path=path)

    # Also return explicit mapping
    values = dotenv_values(dotenv_path=path)

    # Filter out unset values (None)
    return {key: value for key, value in values.items() if value is not None}
