import json
from pathlib import Path

from src.cli.validate import run_validation, DEFAULT_SAMPLE_SIZE


def test_fixed_sampling_size(tmp_path: Path):
    records = [
        {
            "concept": f"c{i}",
            "description": "d",
            "application": "a",
            "tags": ["t"],
            "type": "concept",
            "reference": f"p{i}-{i}",
        }
        for i in range(DEFAULT_SAMPLE_SIZE)
    ]
    path = tmp_path / "data.jsonl"
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record))
            handle.write("\n")
    rate = run_validation(path)
    assert rate == 0.0
