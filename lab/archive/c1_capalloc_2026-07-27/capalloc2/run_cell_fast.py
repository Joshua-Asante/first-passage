#!/usr/bin/env python3
"""Q-CAPALLOC-2 cell runner — same harness, skip CAPALLOC-1's embedded sensitivity.

Does not edit run_capalloc.py. Clears SENSITIVITY before main() so the D1–D5
main sweep is identical; only the parent's unused 5-arm sensitivity loop is
skipped. --out redirects measured.json so parallel cells do not collide.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_CAPALLOC2 = Path(__file__).resolve().parent
_HARNESS = _CAPALLOC2.parent
if str(_HARNESS) not in sys.path:
    sys.path.insert(0, str(_HARNESS))

import run_capalloc as R  # noqa: E402

# CAPALLOC-2 scores its own 6-cell pin grid externally; do not re-run the
# parent's frozen SENSITIVITY brackets (WIN_MIN 100/300, PAYOUT 500/2000, …).
R.SENSITIVITY = []


def main() -> int:
    ap = argparse.ArgumentParser(
        description="run_capalloc.py with SENSITIVITY=[] and redirected --out")
    ap.add_argument("--out", type=Path, required=True,
                    help="where to write this cell's measured JSON")
    args, rest = ap.parse_known_args()
    out = args.out.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    measured = (R._HERE / "measured.json").resolve()
    _orig_write_text = Path.write_text

    def _write_text(self, data, encoding="utf-8", errors=None, newline=None):
        target = self
        try:
            if self.resolve() == measured:
                target = out
        except OSError:
            pass
        return _orig_write_text(target, data, encoding=encoding,
                                errors=errors, newline=newline)

    Path.write_text = _write_text  # type: ignore[method-assign]
    try:
        sys.argv = [sys.argv[0], *rest]
        return int(R.main())
    finally:
        Path.write_text = _orig_write_text  # type: ignore[method-assign]


if __name__ == "__main__":
    raise SystemExit(main())
