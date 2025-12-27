import hashlib
from typing import Dict, Any


def hash_file(path: str) -> str:
    hasher = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def build_metadata(model_version: str, dataset_path: str, seed: int, sample_size: int) -> Dict[str, Any]:
    return {
        "model_version": model_version,
        "dataset_hash": hash_file(dataset_path),
        "seed": seed,
        "sample_size": sample_size,
    }
