from __future__ import annotations
import re
from typing import Optional

class SmallPreprocessor:
    def __init__(self, lower: bool = True, collapse_spaces: bool = True):
        self.lower = lower
        self.collapse_spaces = collapse_spaces
    def clean(self, text: str) -> str:
        if not isinstance(text, str):
            text = str(text)
        t = text.strip()
        if self.lower:
            t = t.lower()
        if self.collapse_spaces:
            t = re.sub(r"\s+", " ", t)
        return t