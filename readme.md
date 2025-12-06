# smallrag

A minimal RAG engine with zero external runtime dependencies. Stores documents and embeddings in SQLite, supports chunking, metadata filtering, caching, import/export, and a simple embedder interface.

## Install

```bash
pip install small-rag
```

## Quick example

```python
from Smallrag import SmallRAG

# Provide a simple embedder (random stub or a real model)
def dummy_embed(text: str) -> list[float]:
    # Real users should plug SentenceTransformers, OpenAI embeddings, Ollama, etc.
    import hashlib
    bs = hashlib.sha256(text.encode()).digest()
    return [b/255 for b in bs]

rag = SmallRAG("./data/rag.db", verbose=True)
rag.set_embedder(dummy_embed)
rag.add_document("Kafka is a distributed streaming platform.")
rag.add_document("Spark is used for large-scale data processing.")
print(rag.query("stream processing"))
```

## Features
- Chunking
- Metadata filtering
- Caching of embeddings
- Import / Export
- Simple CLI