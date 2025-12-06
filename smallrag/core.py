from __future__ import annotations
import math
import time
from typing import Callable, Iterable, List, Optional, Dict, Any
from .store import SmallStore
from .chunker import SmallChunker
from .preprocessor import SmallPreprocessor
from .embedder import SmallEmbedder
from .utils import simple_logger


class SmallRAG:
    """Primary class. Manage store, embedder, chunker, preprocessing.

    Example:
        rag = SmallRAG("./data/rag.db")
        rag.set_embedder(my_fn)
        rag.add_document(text)
    """

    def __init__(self, db_path: str = "smallrag.db", *, verbose: bool = False):
        self.store = SmallStore(db_path)
        self.chunker = SmallChunker()
        self.preproc = SmallPreprocessor()
        self.embedder = SmallEmbedder()  # default: raises until set
        self.logger = simple_logger("SmallRAG", enabled=verbose)

    # ---------------- Embedder ----------------
    def set_embedder(self, fn: Callable[[str], List[float]]):
        self.embedder.set(fn)
        self.logger(f"Embedder set: {fn}")

    def use_openai(self, model_name: str):
        raise NotImplementedError("OpenAI helper not included; please pass a custom embedder")

    # ---------------- Documents ----------------
    def add_document(self, text: str, *, metadata: Optional[Dict[str, Any]] = None,
                     chunk: bool = True, chunk_size: int = 512):
        """Add a document; optionally chunk and cache embeddings.

        Args:
            text: full text of document
            metadata: optional metadata dict
            chunk: whether to chunk
            chunk_size: chars per chunk
        """
        start = time.time()
        text = self.preproc.clean(text)
        chunks = [text]
        if chunk:
            chunks = self.chunker.chunk(text, chunk_size=chunk_size)
        inserted = 0
        for c in chunks:
            # check cache
            exists = self.store.find_text(c)
            if exists:
                self.logger("skip embed — cached")
                continue
            emb = self.embedder.embed(c)
            self.store.insert(text=c, embedding=emb, metadata=metadata)
            inserted += 1
        self.logger(f"Inserted {inserted} chunks in {time.time() - start:.3f}s")

    # ---------------- Query ----------------
    def query(self, query_text: str, top_k: int = 5, *, min_score: float = 0.0,
              filter: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Query the DB and return top_k documents with scores.

        Returns list of dicts: {id, text, metadata, score}
        """
        start = time.time()
        q = self.preproc.clean(query_text)
        qemb = self.embedder.embed(q)
        candidates = self.store.fetch_all(filter=filter)
        scored = []
        for doc in candidates:
            score = self._cosine(qemb, doc["embedding"]) if doc.get("embedding") else 0.0
            if score >= min_score:
                scored.append({"id": doc["id"], "text": doc["text"], "metadata": doc.get("metadata", {}), "score": score})
        scored.sort(key=lambda x: x["score"], reverse=True)
        res = scored[:top_k]
        self.logger(f"Query executed in {time.time() - start:.3f}s — returned {len(res)} items")
        return res

    # ---------------- Import / Export ----------------
    def export_db(self, path: str):
        self.store.export(path)
        self.logger(f"Exported DB to {path}")

    def import_db(self, path: str):
        self.store.import_(path)
        self.logger(f"Imported DB from {path}")

    # ---------------- Utilities ----------------
    @staticmethod
    def _cosine(a: List[float], b: List[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(y * y for y in b))
        return dot / (na * nb + 1e-12)

    def get(self, doc_id: int) -> Optional[Dict[str, Any]]:
        return self.store.get(doc_id)