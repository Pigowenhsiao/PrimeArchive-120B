from pathlib import Path
import zipfile

from pypdf import PdfWriter

from src.services.loader import load_text


def _write_min_pdf(path: Path) -> None:
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    with path.open("wb") as handle:
        writer.write(handle)


def _write_min_epub(path: Path) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("mimetype", "application/epub+zip")
        archive.writestr(
            "META-INF/container.xml",
            "<?xml version=\"1.0\"?>"
            "<container version=\"1.0\" xmlns=\"urn:oasis:names:tc:opendocument:xmlns:container\">"
            "<rootfiles><rootfile full-path=\"content.xhtml\" media-type=\"application/xhtml+xml\"/>"
            "</rootfiles></container>",
        )
        archive.writestr(
            "content.xhtml",
            "<html><body><h1>Title</h1><p>Hello EPUB</p></body></html>",
        )


def test_loader_supports_txt(tmp_path: Path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("content", encoding="utf-8")
    text = load_text(file_path)
    assert "content" in text


def test_loader_supports_pdf(tmp_path: Path):
    file_path = tmp_path / "sample.pdf"
    _write_min_pdf(file_path)
    text = load_text(file_path)
    assert isinstance(text, str)


def test_loader_supports_epub(tmp_path: Path):
    file_path = tmp_path / "sample.epub"
    _write_min_epub(file_path)
    text = load_text(file_path)
    assert "Hello EPUB" in text
