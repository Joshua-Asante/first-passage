"""Unit tests for scripts/sync_liveness_indexes.py — report-only liveness."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
_SPEC = importlib.util.spec_from_file_location(
    "sync_liveness_indexes", REPO / "scripts" / "sync_liveness_indexes.py"
)
sli = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = sli
_SPEC.loader.exec_module(sli)


INDEX_STALE = """# Roster

## Open

| Q | Status | Home (canonical) | Next action |
|---|---|---|---|
| **Q-LIVE-1** — still open | **`OPEN`** | [`x`](x.md) | keep going |
| **Q-TNEC-CON-4** — paused parent | **`AMBIGUOUS-HOLD` → ITERATE** | [`c`](c.md) | CON-5 G0 frozen; Cap unclaimed. |

## Recently closed (cross-reference; not open)

- **Q-TNEC-CON-5** — Branch A STOP 2026-08-12
"""

INDEX_ITERATE_LIVE = """# Roster

## Open

| Q | Status | Home (canonical) | Next action |
|---|---|---|---|
| **Q-TNEC-CON-4** — still iterating | **`AMBIGUOUS-HOLD` → ITERATE** | [`c`](c.md) | CON-5 G0 frozen; Cap unclaimed. |

## Recently closed (cross-reference; not open)

- **Q-OTHER-1** — unrelated
"""

CATALOG = """# Catalog

| slug | theme | status | one-liner | path | card |
|---|---|---|---|---|---|
| live_ok | c1 | ACTIVE | still running | lab/analysis/x/ | — |
| archive_owed_active | c1 | ACTIVE | archive owed (FALSIFIED) | lab/analysis/y/ | — |
| hold_owed | c1 | HOLD | archive owed (FALSIFIED) | lab/analysis/z/ | — |
"""


def test_stale_index_open_flags_terminal_with_dead_successor():
    stale = sli.stale_index_open(INDEX_STALE)
    assert any("Q-TNEC-CON-4" in row for row in stale)
    assert not any("Q-LIVE-1" in row for row in stale)


def test_stale_index_open_keeps_iterate_with_live_successor():
    stale = sli.stale_index_open(INDEX_ITERATE_LIVE)
    assert stale == []


def test_stale_index_open_ignores_reserved_dead_close():
    text = """# Roster

## Open

| Q | Status | Home (canonical) | Next action |
|---|---|---|---|
| **Q-TOM-SPX-1** — reserved | Layer A **RESOLVED-ABSENT**; formal DEAD close reserved | [`x`](x.md) | reserved close only |

## Recently closed (cross-reference; not open)

- **Q-OTHER-1** — unrelated
"""
    assert sli.stale_index_open(text) == []


INDEX_OPEN_WITH_CLOSURE = """# Roster

## Open

| Q | Status | Home (canonical) | Next action |
|---|---|---|---|
| **Q-M1WIRE-1** — arming interlock | **`OPEN — DRAFT (pre-lock)`** | [`q`](q.md) | Named, not opened. |
| **Q-LIVE-1** — still open | **`OPEN`** | [`x`](x.md) | keep going |

## Recently closed (cross-reference; not open)

- **Q-OTHER-1** — unrelated
"""


def test_open_with_hot_closure_flags_even_when_status_says_open():
    hits = sli.open_with_hot_closure(
        INDEX_OPEN_WITH_CLOSURE, closure_ids={"Q-M1WIRE-1"}
    )
    assert any("Q-M1WIRE-1" in row for row in hits)
    assert not any("Q-LIVE-1" in row for row in hits)


def test_open_with_hot_closure_empty_when_no_file():
    assert sli.open_with_hot_closure(INDEX_OPEN_WITH_CLOSURE, closure_ids=set()) == []


def test_hot_closure_ids_parses_stem(tmp_path):
    (tmp_path / "Q-M1WIRE-1-closure-falsified.md").write_text("x", encoding="utf-8")
    (tmp_path / "not-a-closure.md").write_text("x", encoding="utf-8")
    assert sli.hot_closure_ids(tmp_path) == {"Q-M1WIRE-1"}


def test_archive_owed_active_only_flags_active():
    hits = sli.archive_owed_active(CATALOG)
    assert any("archive_owed_active" in h for h in hits)
    assert not any("hold_owed" in h for h in hits)
    assert not any("live_ok" in h for h in hits)


def test_check_exits_zero_even_when_stale(tmp_path, monkeypatch):
    idx = tmp_path / "INDEX.md"
    idx.write_text(INDEX_STALE, encoding="utf-8")
    cat = tmp_path / "CATALOG.md"
    cat.write_text(CATALOG, encoding="utf-8")
    monkeypatch.setattr(sli, "INDEX", idx)
    monkeypatch.setattr(sli, "CATALOG", cat)
    assert sli.main([]) == 0
