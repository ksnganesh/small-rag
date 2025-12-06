from __future__ import annotations
from typing import Callable
import time

def simple_logger(name: str, enabled: bool = False) -> Callable[[str], None]:
    def _log(msg: str):
        if not enabled:
            return
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{ts}] [{name}] {msg}")
    return _log