import logging

from smartbot.utils.logger import (
    LevelBasedFormatter,
    get_logger,
    setup_logging,
)


def test_formatter_info_level() -> None:
    """Formats INFO records using the simple message format."""
    formatter: LevelBasedFormatter = LevelBasedFormatter()

    record: logging.LogRecord = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="",
        lineno=1,
        msg="hello world",
        args=(),
        exc_info=None,
    )

    result: str = formatter.format(record)

    assert result == "hello world"


def test_formatter_non_info_level() -> None:
    """Formats non-INFO records using the detailed format."""
    formatter: LevelBasedFormatter = LevelBasedFormatter()

    record: logging.LogRecord = logging.LogRecord(
        name="test_logger",
        level=logging.DEBUG,
        pathname="",
        lineno=1,
        msg="debug message",
        args=(),
        exc_info=None,
    )

    result: str = formatter.format(record)

    assert "DEBUG" in result
    assert "test_logger" in result
    assert "debug message" in result


def test_setup_logging_sets_level() -> None:
    """Configures root logger with the provided level."""
    root: logging.Logger = logging.getLogger()
    root.handlers.clear()

    setup_logging(level=logging.DEBUG)

    assert root.level == logging.DEBUG
    assert len(root.handlers) == 1


def test_setup_logging_no_duplicate_handlers() -> None:
    """Does not attach multiple handlers on repeated setup calls."""
    root: logging.Logger = logging.getLogger()
    root.handlers.clear()

    setup_logging()
    setup_logging()

    assert len(root.handlers) == 1


def test_get_logger_returns_named_logger() -> None:
    """Returns a logger instance with the requested name."""
    logger: logging.Logger = get_logger("my_custom_logger")

    assert isinstance(logger, logging.Logger)
    assert logger.name == "my_custom_logger"
