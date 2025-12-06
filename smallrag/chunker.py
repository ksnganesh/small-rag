from __future__ import annotations
from typing import List


class SmallChunker:
    def __init__(self, default_size: int = 512, overlap: int = 64):
        self.default_size = default_size
        self.overlap = overlap

    def chunk(self, text: str, chunk_size: int | None = None) -> List[str]:
        if chunk_size is None:
            chunk_size = self.default_size
        text = text.strip()
        if len(text) <= chunk_size:
            return [text]
        chunks = []
        i = 0
        while i < len(text):
            end = i + chunk_size
            chunk = text[i:end]
            chunks.append(chunk)
            i = end - self.overlap
        return [c.strip() for c in chunks if c.strip()]