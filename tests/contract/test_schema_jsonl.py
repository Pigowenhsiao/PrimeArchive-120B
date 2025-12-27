from src.lib.schema import load_schema, validate_payload


def test_schema_validation_passes():
    schema = load_schema()
    payload = {
        "concept": "Test",
        "description": "Desc",
        "application": "Use",
        "tags": ["tag"],
        "type": "concept",
        "reference": "p1-2",
        "confidence": 0.5,
    }
    validate_payload(payload, schema)
