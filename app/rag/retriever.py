"""Retrieval wrapper around the Chroma knowledge base."""

import chromadb

from app.config import settings


class Retriever:
    def __init__(self):
        self._client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
        self._collection = self._client.get_or_create_collection(settings.chroma_collection)

    def query(self, text: str, n_results: int = 3) -> list[dict]:
        """Return the top-k grounding passages for `text`.

        Each result: {"source": str, "excerpt": str, "distance": float}.
        """
        results = self._collection.query(query_texts=[text], n_results=n_results)
        hits = []
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        dists = results.get("distances", [[]])[0]
        for doc, meta, dist in zip(docs, metas, dists):
            hits.append(
                {
                    "source": meta.get("source", "unknown"),
                    "excerpt": doc,
                    "distance": dist,
                }
            )
        return hits
