# lab/archive/approach_scoreboard_2026-08/inventory_closed.py
"""Q-SCORE-1 Block-1 Closed: inventory. Grammar = PREREG F3. GRANDFATHERED imported, not copied."""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

_DIR = Path(__file__).resolve().parent
_REPO = _DIR.parents[2]
sys.path.insert(0, str(_REPO))

from scripts.check_closure_disposition import GRANDFATHERED  # noqa: E402  (owner)

CLOSURES = _REPO / "docs" / "briefs" / "closures"
# PREREG F3 acceptor. Python 3.14 rejects inline (?m) mid-alternation; re.M is equivalent.
CLOSED_RE = re.compile(
    r"^(?:\*\*Closed:\*\*|Closed:)\s*\d{4}-\d{2}-\d{2}",
    re.M,
)


def has_machine_closed(text: str) -> bool:
    return CLOSED_RE.search(text) is not None


def summarize() -> dict:
    files = sorted(CLOSURES.glob("*.md"))
    without: list[str] = []
    with_closed = 0
    for p in files:
        text = p.read_text(encoding="utf-8")
        if has_machine_closed(text):
            with_closed += 1
        else:
            without.append(p.name)
    n = len(files)
    gf = [n for n in without if n in GRANDFATHERED]
    recent = [n for n in without if n not in GRANDFATHERED]
    if not without:
        conc = "grandfathered-majority"
    elif len(gf) / len(without) >= 0.80:
        conc = "grandfathered-majority"
    elif len(recent) / len(without) >= 0.40:
        conc = "recent-spread"
    else:
        conc = "mixed"
    return {
        "n_closures": n,
        "n_with_closed": with_closed,
        "n_without_closed": len(without),
        "date_coverage": (with_closed / n) if n else 0.0,
        "without_closed": without,
        "without_closed_grandfathered": gf,
        "without_closed_recent": recent,
        "grandfather_concentration": conc,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(summarize(), indent=2))
