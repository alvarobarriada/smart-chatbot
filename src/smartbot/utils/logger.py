import logging


class LevelBasedFormatter(logging.Formatter):
    """
    Custom formatter that changes format depending on log level.
    """

    SIMPLE_FORMAT = "%(message)s"
    DETAILED_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

    def format(self, record: logging.LogRecord) -> str:
        if record.levelno == logging.INFO:
            self._style._fmt = self.SIMPLE_FORMAT
        else:
            self._style._fmt = self.DETAILED_FORMAT
        return super().format(record)


def setup_logging(level: int = logging.INFO) -> None:
    """
    Configure root logging for the application.
    """

    handler = logging.StreamHandler()
    handler.setFormatter(LevelBasedFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    if not root_logger.handlers:
        root_logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
