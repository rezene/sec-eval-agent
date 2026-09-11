"""Build the knowledge base: OWASP Top 10 + CWE slice + MITRE ATT&CK content.

Reads source documents from app/rag/knowledge/, chunks them, embeds them,
and persists them into the Chroma collection defined in settings.

Usage:
    python -m app.rag.ingest
"""

from pathlib import Path

import chromadb

from app.config import settings

KNOWLEDGE_DIR = Path(__file__).parent / "knowledge"


def load_documents() -> list[dict]:
    """Load raw knowledge documents as {id, text, metadata} dicts.

    TODO: replace with real OWASP/CWE/MITRE source files under
    app/rag/knowledge/ (one doc per file, or a structured JSON/YAML index).
    """
    docs = []
    for path in sorted(KNOWLEDGE_DIR.glob("**/*.md")):
        docs.append(
            {
                "id": path.stem,
                "text": path.read_text(encoding="utf-8"),
                "metadata": {"source": path.stem},
            }
        )
    return docs


def build_index() -> None:
    client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
    collection = client.get_or_create_collection(settings.chroma_collection)

    documents = load_documents()
    if not documents:
        print(f"No knowledge documents found under {KNOWLEDGE_DIR}. Add some first.")
        return

    collection.upsert(
        ids=[d["id"] for d in documents],
        documents=[d["text"] for d in documents],
        metadatas=[d["metadata"] for d in documents],
    )
    print(f"Indexed {len(documents)} documents into '{settings.chroma_collection}'.")


if __name__ == "__main__":
    build_index()
