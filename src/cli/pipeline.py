import argparse
import pathlib
from typing import List

from src.lib.schema import load_schema, validate_payload
from src.services.cleaner import clean_text
from src.services.chunker import smart_chunk
from src.services.exporter import write_jsonl
from src.services.generator import generate_units
from src.services.loader import load_text
from src.services.embeddings import embed_texts
from src.services.vector_store import build_vector_store


def build_references(chunks: List[str]) -> List[str]:
    references = []
    for idx, _ in enumerate(chunks, start=1):
        references.append(f"Chapter#Paragraph{idx}")
    return references


def run_pipeline(input_path: pathlib.Path, output_path: pathlib.Path) -> None:
    raw_text = load_text(input_path)
    cleaned = clean_text(raw_text)
    chunks = smart_chunk(cleaned)
    references = build_references(chunks)
    units = generate_units(chunks, references)

    schema = load_schema()
    for unit in units:
        validate_payload(unit, schema)

    write_jsonl(output_path, units)

    embeddings = embed_texts([u["description"] for u in units])
    store = build_vector_store(collection_name=input_path.stem)
    store.add([f"unit-{idx}" for idx in range(len(units))], embeddings)


def main() -> None:
    parser = argparse.ArgumentParser(description="Book-to-RAG pipeline")
    parser.add_argument("--input", required=True)
    parser.add_argument("--format", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    input_path = pathlib.Path(args.input)
    output_path = pathlib.Path(args.output)

    run_pipeline(input_path, output_path)


if __name__ == "__main__":
    main()
