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
            "<html><body><h1>Title</h1><p>Body</p></body></html>",
        )


def test_multiformat_ingestion(tmp_path: Path):
    txt_path = tmp_path / "book.txt"
    txt_path.write_text("# Title\nBody", encoding="utf-8")
    assert "Title" in load_text(txt_path)

    pdf_path = tmp_path / "book.pdf"
    _write_min_pdf(pdf_path)
    assert isinstance(load_text(pdf_path), str)

    epub_path = tmp_path / "book.epub"
    _write_min_epub(epub_path)
    assert "Body" in load_text(epub_path)
