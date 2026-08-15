"""Put the harness dir and core/ on sys.path so tests/scripts can
`import metrics`, `import portfolio_mc as pmc`, `from lib.mvd import ...`
without an editable install. Mirrors lab/analysis/*/conftest.py convention."""
from __future__ import annotations
import sys
from pathlib import Path

_HARNESS = Path(__file__).resolve().parent          # .../timeframe_5m_2026-06-25
_CORE = _HARNESS.parents[2] / "core"                # repo_root/core
for _p in (_HARNESS, _CORE):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
