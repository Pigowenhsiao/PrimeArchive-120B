from typing import List


def embed_texts(texts: List[str]) -> List[List[float]]:
    embeddings = []
    for text in texts:
        value = float(sum(ord(ch) for ch in text) % 1000) / 1000.0
        embeddings.append([value] * 8)
    return embeddings
