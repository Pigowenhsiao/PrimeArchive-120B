import pathlib
import zipfile
from html.parser import HTMLParser
from typing import List

from pypdf import PdfReader


SUPPORTED_EXTENSIONS = {".pdf", ".epub", ".txt"}


class _HTMLStripper(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._chunks: List[str] = []

    def handle_data(self, data: str) -> None:
        if data.strip():
            self._chunks.append(data.strip())

    def text(self) -> str:
        return "\n".join(self._chunks)


def _strip_html(content: str) -> str:
    parser = _HTMLStripper()
    parser.feed(content)
    return parser.text()


def load_text(path: pathlib.Path) -> str:
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported extension: {path.suffix}")
    if suffix == ".txt":
        return path.read_text(encoding="utf-8", errors="ignore")
    if suffix == ".pdf":
        reader = PdfReader(str(path))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages).strip()
    if suffix == ".epub":
        return _read_epub(path)
    raise ValueError(f"Unsupported extension: {path.suffix}")


def _read_epub(path: pathlib.Path) -> str:
    text_parts: List[str] = []
    with zipfile.ZipFile(path, "r") as archive:
        for name in archive.namelist():
            if name.lower().endswith((".xhtml", ".html", ".htm")):
                content = archive.read(name).decode("utf-8", errors="ignore")
                text_parts.append(_strip_html(content))
    return "\n".join(part for part in text_parts if part).strip()


def split_paragraphs(text: str) -> List[str]:
    paragraphs = [p.strip() for p in text.splitlines() if p.strip()]
    return paragraphs
