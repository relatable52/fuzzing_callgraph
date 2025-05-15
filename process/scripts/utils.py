import json
import logging
import subprocess


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


def list_classes(jar_path):
    """List all class files in the JAR."""
    result = subprocess.run(["jar", "tf", jar_path], capture_output=True, text=True)
    class_files = [
        line for line in result.stdout.splitlines() if line.endswith(".class")
    ]
    return class_files
