import argparse
import pathlib
from typing import Callable, List, Optional, Tuple

from src.lib.config import load_config
from src.lib.logging import safe_log
from src.lib.schema import load_schema, validate_payload
from src.services.cleaner import clean_text
from src.services.chunker import smart_chunk
from src.services.exporter import write_jsonl
from src.services.generator import generate_units
from src.services.llm_client import LLMClient
from src.services.loader import load_text
from src.services.embeddings import embed_texts
from src.services.vector_store import build_vector_store


def build_references(chunks: List[str]) -> List[str]:
    references = []
    for idx, _ in enumerate(chunks, start=1):
        references.append(f"Chapter#Paragraph{idx}")
    return references


def _emit(
    message: str,
    progress: int,
    log_callback: Optional[Callable[[str], None]],
    progress_callback: Optional[Callable[[int, str], None]],
) -> None:
    print(message)
    if log_callback:
        log_callback(message)
    if progress_callback:
        progress_callback(progress, message)


def run_pipeline(
    input_path: pathlib.Path,
    output_path: pathlib.Path,
    log_callback: Optional[Callable[[str], None]] = None,
    progress_callback: Optional[Callable[[int, str], None]] = None,
    dump_chunks: bool = False,
    dump_path: Optional[pathlib.Path] = None,
    max_chunks: int = 0,
) -> None:
    config = load_config()
    llm_settings = config.get("llm_settings", {})
    llm_client = LLMClient(
        base_url=llm_settings.get("base_url", "http://localhost:11434/v1"),
        model_name=llm_settings.get("model_name", "gpt-oss:120B-cloud"),
        temperature=llm_settings.get("temperature", 0.1),
        top_p=llm_settings.get("top_p", 0.9),
        repeat_penalty=llm_settings.get("repeat_penalty", 1.1),
        max_tokens=llm_settings.get("max_tokens", 2048),
        num_ctx=llm_settings.get("num_ctx", 8192),
        timeout_seconds=llm_settings.get("timeout", 180),
        max_retries=config.get("reliability", {}).get("retry_limit", 3),
    )
    safe_log("pipeline.start", {"input": str(input_path), "output": str(output_path)})
    _emit(
        f"Start pipeline: {input_path} -> {output_path}",
        5,
        log_callback,
        progress_callback,
    )
    raw_text = load_text(input_path)
    safe_log("pipeline.loaded", {"chars": len(raw_text)})
    _emit("Loaded input text", 15, log_callback, progress_callback)
    cleaned = clean_text(raw_text)
    safe_log("pipeline.cleaned", {"chars": len(cleaned)})
    _emit("Cleaned text", 30, log_callback, progress_callback)
    chunks = smart_chunk(cleaned)
    if max_chunks and max_chunks > 0:
        chunks = chunks[:max_chunks]
    safe_log("pipeline.chunked", {"chunks": len(chunks)})
    _emit(f"Chunked text into {len(chunks)} parts", 45, log_callback, progress_callback)
    if dump_chunks:
        for idx, chunk in enumerate(chunks, start=1):
            print(f"## Chunk {idx}\n{chunk}\n")
        if dump_path:
            dump_path.parent.mkdir(parents=True, exist_ok=True)
            with dump_path.open("w", encoding="utf-8") as handle:
                for idx, chunk in enumerate(chunks, start=1):
                    handle.write(f"## Chunk {idx}\n")
                    handle.write(chunk)
                    handle.write("\n\n")
            _emit(
                f"Chunk dump saved to {dump_path}",
                48,
                log_callback,
                progress_callback,
            )
    references = build_references(chunks)
    debug_cfg = config.get("debug", {})
    units = generate_units(
        chunks,
        references,
        llm_client=llm_client,
        print_llm_output=debug_cfg.get("print_llm_output", False),
    )
    safe_log("pipeline.generated", {"units": len(units)})
    _emit(f"Generated {len(units)} units", 70, log_callback, progress_callback)

    schema = load_schema()
    for unit in units:
        validate_payload(unit, schema)

    write_jsonl(output_path, units)
    safe_log("pipeline.exported", {"path": str(output_path)})
    _emit("Exported JSONL output", 85, log_callback, progress_callback)

    embeddings = embed_texts([u["description"] for u in units])
    store = build_vector_store(collection_name=input_path.stem)
    store.add([f"unit-{idx}" for idx in range(len(units))], embeddings)
    safe_log("pipeline.embedded", {"vectors": len(embeddings)})
    _emit("Embedded units", 95, log_callback, progress_callback)
    _emit("Pipeline completed", 100, log_callback, progress_callback)


def main() -> None:
    parser = argparse.ArgumentParser(description="Book-to-RAG pipeline")
    parser.add_argument("--input", required=True)
    parser.add_argument("--format", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--dump-chunks", action="store_true")
    parser.add_argument("--dump-path", default="")
    parser.add_argument("--max-chunks", type=int, default=0)
    args = parser.parse_args()

    input_path = pathlib.Path(args.input)
    output_path = pathlib.Path(args.output)

    config = load_config()
    debug_cfg = config.get("debug", {})
    dump_chunks = args.dump_chunks or debug_cfg.get("dump_chunks", False)
    dump_path = args.dump_path or debug_cfg.get("dump_path", "")
    dump_path_value = pathlib.Path(dump_path) if dump_path else None
    max_chunks = args.max_chunks or debug_cfg.get("max_chunks", 0)

    run_pipeline(
        input_path,
        output_path,
        dump_chunks=dump_chunks,
        dump_path=dump_path_value,
        max_chunks=max_chunks,
    )


if __name__ == "__main__":
    main()
