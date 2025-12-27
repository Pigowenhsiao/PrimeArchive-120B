import logging
from typing import Any, Dict


LOGGER_NAME = "bookrag"


def get_logger() -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def safe_log(event: str, metadata: Dict[str, Any]) -> None:
    if "raw_text" in metadata:
        metadata = {k: v for k, v in metadata.items() if k != "raw_text"}
    logger = get_logger()
    logger.info("%s | %s", event, metadata)
