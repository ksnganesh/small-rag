from __future__ import annotations
from typing import Callable, List

class SmallEmbedder:
    def __init__(self):
        self._fn: Callable[[str], List[float]] | None = None
    def set(self, fn: Callable[[str], List[float]]):
        self._fn = fn
    def embed(self, text: str) -> List[float]:
        if not self._fn:
            raise RuntimeError("No embedder set. Call set_embedder() on SmallRAG instance.")
        v = self._fn(text)
        # ensure native python list of floats
        return [float(x) for x in v]