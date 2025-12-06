"""SQLite-backed vector store; embeddings saved as JSON arrays."""
from __future__ import annotations
import sqlite3
import json
from typing import List, Dict, Any, Optional


class SmallStore:
    def __init__(self, path: str = "smallrag.db"):
        self.path = path
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create()

    def _create(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                embedding TEXT,
                metadata TEXT,
                created_at REAL DEFAULT (strftime('%s','now'))
            )
            """
        )
        self.conn.commit()

    def insert(self, text: str, embedding: List[float], metadata: Optional[Dict[str, Any]] = None):
        emb = json.dumps(embedding)
        meta = json.dumps(metadata or {})
        cur = self.conn.execute(
            "INSERT INTO documents (text, embedding, metadata) VALUES (?, ?, ?)",
            (text, emb, meta),
        )
        self.conn.commit()
        return cur.lastrowid

    def fetch_all(self, filter: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        cur = self.conn.execute("SELECT * FROM documents")
        rows = cur.fetchall()
        docs = []
        for r in rows:
            doc = {"id": r["id"], "text": r["text"], "embedding": None, "metadata": {}}
            if r["embedding"]:
                doc["embedding"] = json.loads(r["embedding"])
            if r["metadata"]:
                doc["metadata"] = json.loads(r["metadata"])
            # apply simple filter: all items in filter must match metadata's key
            if filter:
                ok = True
                for k, v in filter.items():
                    if str(doc["metadata"].get(k, None)) != str(v):
                        ok = False
                        break
                if not ok:
                    continue
            docs.append(doc)
        return docs

    def find_text(self, text: str) -> Optional[int]:
        cur = self.conn.execute("SELECT id FROM documents WHERE text = ? LIMIT 1", (text,))
        r = cur.fetchone()
        return r["id"] if r else None

    def get(self, doc_id: int) -> Optional[Dict[str, Any]]:
        cur = self.conn.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
        r = cur.fetchone()
        if not r:
            return None
        return {"id": r["id"], "text": r["text"], "embedding": json.loads(r["embedding"]) if r["embedding"] else None, "metadata": json.loads(r["metadata"]) if r["metadata"] else {}}

    def export(self, path: str):
        rows = self.fetch_all()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)

    def import_(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            rows = json.load(f)
        for r in rows:
            self.insert(r.get("text", ""), r.get("embedding", []), r.get("metadata", {}))
