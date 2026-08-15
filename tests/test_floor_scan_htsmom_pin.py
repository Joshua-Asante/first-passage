"""H-TSMOM-1 living harness prints the operator-pinned reading (c) (audit R4)."""
from __future__ import annotations

import importlib.util
from pathlib import Path

_FLOOR = Path("lab/archive/q_kbudget_1_2026-07/floor_scan.py")


def _load():
    spec = importlib.util.spec_from_file_location("floor_scan_r4", _FLOOR)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_htsmom1_is_clause_n_fail_not_stale_pass():
    rows = {r["axis"]: r for r in _load().screen()}
    h2 = next(r for key, r in rows.items() if "H-TSMOM-1" in key)
    assert h2["clause_n"].startswith("FAIL (N,")
    assert h2["verdict"] == "FAIL (Clause N)"
    assert "power=0.34" in h2["clause_n"]
    assert not h2["clause_n"].startswith("PASS:")
    passing = [r for r in rows.values() if r["verdict"] == "PASS"]
    failing = [r for r in rows.values() if r["verdict"].startswith("FAIL")]
    assert len(passing) == 2  # D5 + H-OD-1
    assert len(failing) == 7
