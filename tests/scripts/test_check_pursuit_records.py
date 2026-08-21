"""Adversarial tests for scripts/check_pursuit_records.py (GRAND tier §10).

Discipline guards need adversarial tests — a checker that passes on an empty
directory or a vacuous fixture is assurance theater. Every REQUIRED failure
mode below has a fixture that must FAIL, and the compliant fixture must PASS.
Live-corpus assertions pin the regex against on-disk reality so a typo cannot
silently disable a limb (trap M-AHF: hooks tested against the author's mental
form, not the artifact's stored form).
"""
from __future__ import annotations

import importlib.util
import sys
from datetime import date
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
_SPEC = importlib.util.spec_from_file_location(
    "check_pursuit_records", REPO / "scripts" / "check_pursuit_records.py"
)
cpr = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
sys.modules[_SPEC.name] = cpr
_SPEC.loader.exec_module(cpr)


COMPLIANT_PARK = """# Fixture PARK — compliant

**Class:** (b) parked lane · **Standing:** PARK
**re-entry:** successor venue registers a live seat for this lane
**expiry:** 2026-11-08 (converts to SUBTRACT absent explicit operator renewal)
**Aim served (if re-entered):** A1
"""

PARK_MISSING_REENTRY = """# Fixture PARK — missing re-entry

**Class:** (b) parked lane · **Standing:** PARK
**expiry:** 2026-11-08 (converts to SUBTRACT absent explicit operator renewal)
"""

PARK_MISSING_EXPIRY = """# Fixture PARK — missing expiry

**Class:** (b) parked lane · **Standing:** PARK
**re-entry:** successor venue registers a live seat for this lane
"""

PARK_EXPIRED = """# Fixture PARK — past expiry

**Class:** (b) parked lane · **Standing:** PARK
**re-entry:** successor venue registers a live seat for this lane
**expiry:** 2026-11-08 (converts to SUBTRACT absent explicit operator renewal)
"""

COMPLIANT_KEEP = """# Fixture KEEP — compliant

**Class:** (a) active campaign · **Standing:** KEEP
**Aim served:** A1 — fund/deploy automated futures strategies
**Measure:** ≥1 candidate clears the bust ceiling
**Survive bound:** operator gate-walk cadence
**Review date:** 2026-11-08
"""

KEEP_MISSING_MEASURE = """# Fixture KEEP — missing Measure

**Class:** (a) active campaign · **Standing:** KEEP
**Aim served:** A1 — fund/deploy automated futures strategies
**Survive bound:** operator gate-walk cadence
**Review date:** 2026-11-08
"""

KEEP_NO_REENTRY_FIELD = """# Fixture KEEP — correctly lacks park fields

**Class:** (a) active campaign · **Standing:** KEEP
**Aim served:** A1 — fund/deploy
**Measure:** progress metric
**Survive bound:** resource ceiling
**Review date:** 2026-11-08
"""

STANDING_SUBTRACT_EMDASH = """# Fixture — SUBTRACT em-dash qualifier

**Class:** (d) meta-belt · **Standing:** SUBTRACT — **no file operation performed or possible**
**Re-entry armor:** requires out-of-frame evidence plus an attached falsifier.
"""

STANDING_SUBTRACT_PAREN = """# Fixture — SUBTRACT parenthetical

**Class:** (c) standing exploration · **Standing:** SUBTRACT (complete — verdicts already landed,
this is bookkeeping closure, not a new kill)
**Re-entry armor:** requires out-of-frame evidence plus an attached falsifier.
"""

STANDING_SUBTRACT_COMPLETE = """# Fixture — SUBTRACT-complete title form on Standing

**Class:** (c) standing exploration · **Standing:** SUBTRACT-complete
**Re-entry armor:** requires out-of-frame evidence plus an attached falsifier.
"""

STANDING_MERGE_TARGET = """# Fixture — MERGE with target

**Class:** (d) meta-belt · **Standing:** MERGE (target: repo copy `.claude/skills/trade-csv-reconcile/`)
**Residuals transferred:** none
"""

STANDING_NO_ACTION = """# Fixture — terminal register (e2 form)

**Class:** (e) aim-scale branch · **Standing:** no action — already subtracted, already armored
**Why this row exists:** inventory completeness; nothing to act on.
"""

STANDING_INVALID = """# Fixture — unknown standing

**Class:** (x) unknown · **Standing:** WATCH-1
**Aim served:** A1
"""


def _write(tmp_path: Path, name: str, body: str) -> Path:
    p = tmp_path / name
    p.write_text(body, encoding="utf-8")
    return p


ASOF_BEFORE = date(2026, 8, 9)
ASOF_AFTER = date(2026, 11, 9)


def test_compliant_park_passes(tmp_path):
    findings = cpr.scan_file(
        _write(tmp_path, "compliant-park.md", COMPLIANT_PARK), asof=ASOF_BEFORE
    )
    assert findings == []


def test_park_missing_reentry_fails(tmp_path):
    findings = cpr.scan_file(
        _write(tmp_path, "park-no-reentry.md", PARK_MISSING_REENTRY), asof=ASOF_BEFORE
    )
    assert any(f.limb == "park-completeness" and "re-entry" in f.message for f in findings), (
        findings
    )


def test_park_missing_expiry_fails(tmp_path):
    findings = cpr.scan_file(
        _write(tmp_path, "park-no-expiry.md", PARK_MISSING_EXPIRY), asof=ASOF_BEFORE
    )
    assert any(f.limb == "park-completeness" and "expiry" in f.message for f in findings), (
        findings
    )


def test_keep_without_reentry_is_not_park_flagged(tmp_path):
    """Unscoped re-entry grep is trap M-AHF — KEEP correctly lacks the field."""
    findings = cpr.scan_file(
        _write(tmp_path, "keep-no-reentry.md", KEEP_NO_REENTRY_FIELD), asof=ASOF_BEFORE
    )
    assert not any(f.limb == "park-completeness" for f in findings), findings


def test_expired_park_fails(tmp_path):
    findings = cpr.scan_file(
        _write(tmp_path, "park-expired.md", PARK_EXPIRED), asof=ASOF_AFTER
    )
    assert any(f.limb == "expiry-enforcement" for f in findings), findings


def test_park_not_expired_at_asof_on_expiry_day(tmp_path):
    findings = cpr.scan_file(
        _write(tmp_path, "park-on-expiry.md", PARK_EXPIRED), asof=date(2026, 11, 8)
    )
    assert not any(f.limb == "expiry-enforcement" for f in findings), findings


def test_compliant_keep_passes(tmp_path):
    findings = cpr.scan_file(
        _write(tmp_path, "compliant-keep.md", COMPLIANT_KEEP), asof=ASOF_BEFORE
    )
    assert findings == []


def test_keep_missing_measure_fails(tmp_path):
    findings = cpr.scan_file(
        _write(tmp_path, "keep-no-measure.md", KEEP_MISSING_MEASURE), asof=ASOF_BEFORE
    )
    assert any(f.limb == "entry-record" and "Measure" in f.message for f in findings), (
        findings
    )


@pytest.mark.parametrize(
    "name,body",
    [
        ("subtract-emdash.md", STANDING_SUBTRACT_EMDASH),
        ("subtract-paren.md", STANDING_SUBTRACT_PAREN),
        ("subtract-complete.md", STANDING_SUBTRACT_COMPLETE),
        ("merge-target.md", STANDING_MERGE_TARGET),
        ("no-action.md", STANDING_NO_ACTION),
    ],
)
def test_deviating_standings_are_accepted(tmp_path, name, body):
    findings = cpr.scan_file(_write(tmp_path, name, body), asof=ASOF_BEFORE)
    assert not any(f.limb == "standing-vocabulary" for f in findings), findings


def test_invalid_standing_fails(tmp_path):
    findings = cpr.scan_file(
        _write(tmp_path, "invalid-standing.md", STANDING_INVALID), asof=ASOF_BEFORE
    )
    assert any(f.limb == "standing-vocabulary" for f in findings), findings


def test_violations_are_warn_tier_and_exit_zero(tmp_path, capsys):
    bad = _write(tmp_path, "park-no-reentry.md", PARK_MISSING_REENTRY)
    rc = cpr.main(["--asof", "2026-08-09", str(bad)])
    assert rc == 0
    out = capsys.readouterr().out
    assert "WARN" in out
    assert "HARD" not in out


def test_live_park_count_and_fields():
    parks = [
        p for p in cpr.PURSUITS_DIR.glob("*.md")
        if cpr.parse_standing(p.read_text(encoding="utf-8")) == "PARK"
    ]
    # Live PARK set after GSUB-2 (b2-striker-mym-reconstruction SUBTRACT):
    # b1, b3, b5, b6, c3. Do not invent a sixth PARK to keep this pin.
    assert len(parks) == 5, f"expected 5 live PARK records, got {len(parks)}"
    for p in parks:
        text = p.read_text(encoding="utf-8")
        assert cpr.RE_ENTRY_FIELD.search(text), f"{p.name} missing re-entry:"
        assert cpr.EXPIRY_FIELD.search(text), f"{p.name} missing expiry:"
        exp = cpr.parse_expiry(text)
        assert exp == date(2026, 11, 8), f"{p.name} expiry={exp}"


def test_live_standing_variants_exist_on_disk():
    bodies = {
        p.name: p.read_text(encoding="utf-8")
        for p in cpr.PURSUITS_DIR.glob("*.md")
    }
    joined = "\n".join(bodies.values())
    assert "**Standing:** PARK" in joined
    assert "**Standing:** KEEP" in joined
    assert "**Standing:** MERGE (target:" in joined
    assert "**Standing:** SUBTRACT" in joined
    assert "**Standing:** no action" in joined
    assert any("SUBTRACT —" in b for b in bodies.values())
    assert any("SUBTRACT (complete" in b or "SUBTRACT (ruling" in b for b in bodies.values())


def test_live_corpus_clean_at_gsub1_asof(capsys):
    rc = cpr.main(["--asof", "2026-08-09"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "OK" in out


def test_live_corpus_all_parks_expired_after_asof(capsys):
    rc = cpr.main(["--asof", "2026-11-09"])
    assert rc == 0
    out = capsys.readouterr().out
    expiry_lines = [
        line for line in out.splitlines()
        if "expiry-enforcement" in line
    ]
    assert len(expiry_lines) == 5, out
