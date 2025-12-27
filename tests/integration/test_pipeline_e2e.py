from pathlib import Path

from src.cli.pipeline import run_pipeline


def test_pipeline_end_to_end(tmp_path: Path):
    input_file = tmp_path / "book.txt"
    output_file = tmp_path / "output.jsonl"
    input_file.write_text("# Title\nSome content here.")

    run_pipeline(input_file, output_file)

    assert output_file.exists()
    lines = output_file.read_text(encoding="utf-8").splitlines()
    assert lines
