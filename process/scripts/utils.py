import json
import logging


def read_json(file_path: str):
    with open(file_path) as f:
        data = json.load(f)
    return data


def get_logger(name: str = "app_logger") -> logging.Logger:
    logger = logging.getLogger(name)

    # Avoid adding handlers multiple times
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.DEBUG)

    # Handlers
    file_handler = logging.FileHandler("process.log")
    console_handler = logging.StreamHandler()

    file_handler.setLevel(logging.INFO)
    console_handler.setLevel(logging.DEBUG)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
