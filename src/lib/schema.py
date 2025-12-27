import json
import pathlib
from typing import Any, Dict

from jsonschema import Draft202012Validator


DEFAULT_SCHEMA_PATH = pathlib.Path(
    "specs/001-universal-book-rag/contracts/schema.json"
)


def load_schema(path: pathlib.Path = DEFAULT_SCHEMA_PATH) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Schema not found: {path}")
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_payload(payload: Dict[str, Any], schema: Dict[str, Any]) -> None:
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        messages = "; ".join(error.message for error in errors)
        raise ValueError(f"Schema validation failed: {messages}")
