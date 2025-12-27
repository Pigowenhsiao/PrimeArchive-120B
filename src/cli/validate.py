import argparse
import json
import pathlib
import random
from typing import List, Dict, Any


DEFAULT_SAMPLE_SIZE = 200


def load_jsonl(path: pathlib.Path) -> List[Dict[str, Any]]:
    records = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                records.append(json.loads(line))
    return records


def compute_hallucination_rate(records: List[Dict[str, Any]]) -> float:
    failures = 0
    for record in records:
        if not record.get("reference"):
            failures += 1
    return failures / len(records) if records else 0.0


def run_validation(path: pathlib.Path, sample_size: int = DEFAULT_SAMPLE_SIZE) -> float:
    records = load_jsonl(path)
    if len(records) < sample_size:
        raise ValueError("Insufficient records for fixed sample size")
    sample = random.sample(records, sample_size)
    return compute_hallucination_rate(sample)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate hallucination rate")
    parser.add_argument("--input", required=True)
    args = parser.parse_args()

    input_path = pathlib.Path(args.input)
    rate = run_validation(input_path)
    print(f"hallucination_rate={rate}")


if __name__ == "__main__":
    main()
