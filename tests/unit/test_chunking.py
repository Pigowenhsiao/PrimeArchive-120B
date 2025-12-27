from src.services.chunker import smart_chunk
from src.models.document_chunk import MAX_CHUNK_LEN


def test_chunking_respects_max_length():
    text = "# Title\n" + ("a" * (MAX_CHUNK_LEN + 50))
    chunks = smart_chunk(text)
    assert all(len(chunk) <= MAX_CHUNK_LEN for chunk in chunks)
