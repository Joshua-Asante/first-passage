"""Atomic text-file writes: same-directory temp file + os.replace.

For single-file JSON state stores (e.g. core/dd_protection_state.json) a
direct open(path, "w") truncates before writing — a crash/interrupt mid-write
silently destroys the only copy of the state. This helper guarantees the
target is always either the old complete bytes or the new complete bytes,
never a prefix.

The temp file is created in the target's own directory (not the system temp
dir) so os.replace never crosses a volume boundary — a cross-volume replace
raises on Windows.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path


def atomic_write_text(path: Path | str, text: str, encoding: str = "utf-8") -> None:
    """Write ``text`` to ``path`` atomically.

    On any failure the original file is left untouched, the temp file is
    removed, and the exception propagates (fail-loud, no silent fallback).
    """
    path = Path(path)
    fd, tmp_name = tempfile.mkstemp(
        dir=path.parent, prefix=path.name + ".", suffix=".tmp"
    )
    try:
        # Text mode with default newline translation — byte-parity with the
        # plain open(path, "w") / Path.write_text writers this replaces.
        with os.fdopen(fd, "w", encoding=encoding) as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_name, path)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise
