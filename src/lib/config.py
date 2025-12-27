import pathlib
from typing import Any, Dict

import yaml


DEFAULT_CONFIG_PATH = pathlib.Path("configs/config.yaml")


def load_config(path: pathlib.Path = DEFAULT_CONFIG_PATH) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError("Config must be a mapping")
    return data
