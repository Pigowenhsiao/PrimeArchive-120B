from src.services.embeddings import embed_texts


def test_embeddings_shape():
    embeddings = embed_texts(["alpha", "beta"])
    assert len(embeddings) == 2
    assert all(len(vec) == 8 for vec in embeddings)
