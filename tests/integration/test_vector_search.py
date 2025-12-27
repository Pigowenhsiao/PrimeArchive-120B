from src.services.vector_store import build_vector_store


def test_vector_query_returns_ids():
    store = build_vector_store("test")
    store.add(["a", "b"], [[1.0, 0.0], [0.0, 1.0]])
    results = store.query([1.0, 0.0], top_k=1)
    assert results == ["a"]
