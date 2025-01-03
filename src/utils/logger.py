import logging
from logging.handlers import RotatingFileHandler
from typing import Optional
import os


class CustomFormatter(logging.Formatter):
    """Własny formatter z różnymi kolorami ANSI dla różnych części logu"""
    # Kolory ANSI
    grey = "\x1b[38;20m"
    cyan = "\x1b[36m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31m"
    bold_red = "\x1b[31;1m"
    green = "\x1b[32m"
    reset = "\x1b[0m"

    def __init__(self, fmt: Optional[str] = None):
        super().__init__()
        self.fmt = fmt or '%(asctime)s - %(levelname)s - %(name)s - [%(filename)s:%(lineno)d] - %(message)s'

    def format(self, record):
        # Zachowaj oryginalny format
        format_orig = self._style._fmt

        # Dodaj kolory do różnych części komunikatu
        timestamp = self.grey + record.asctime + self.reset
        level = self.get_level_color(record.levelno) + record.levelname + self.reset
        name = self.yellow + record.name + self.reset
        location = self.cyan + f"[{record.filename}:{record.lineno}]" + self.reset
        message = self.green + record.message + self.reset

        # Złóż komunikat
        formatted = f"[{timestamp}] - [{level}] - {name} - {location} - {message}"

        return formatted

    def get_level_color(self, levelno):
        if levelno >= logging.CRITICAL:
            return self.bold_red
        elif levelno >= logging.ERROR:
            return self.red
        elif levelno >= logging.WARNING:
            return self.yellow
        elif levelno >= logging.INFO:
            return self.green
        return self.grey


def setup_logger(name: str, log_file: str, level: int = logging.DEBUG) -> logging.Logger:
    """
    Return a logger with the specified name and level.

    Args:
        name (str): Name of the logger.
        log_file (str): Path to the log file.
        level (int): Logging level (default: logging.INFO).

    Returns:
        logging.Logger: Configured logger.
    """

    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Format dla pliku (bez kolorów)
    file_formatter = logging.Formatter(
        '[%(asctime)s] - %(levelname)s - %(name)s - [%(filename)s:%(lineno)d] - %(message)s'
    )

    # Utwórz handler pliku
    # handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=2)
    handler = logging.FileHandler(log_file, mode='w')
    handler.setFormatter(file_formatter)

    # Utwórz handler konsoli z kolorami
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(CustomFormatter())

    # Skonfiguruj logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Usuń istniejące handlery
    logger.handlers = []

    # Dodaj oba handlery
    logger.addHandler(handler)
    logger.addHandler(console_handler)

    return logger


# Ustaw root logger żeby uniknąć duplikowania
root_logger = logging.getLogger()
root_logger.handlers = []
