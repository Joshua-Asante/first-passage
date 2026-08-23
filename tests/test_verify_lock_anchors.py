"""Fixture tests for `scripts/verify_lock_anchors.py` (dd + historical + living)."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import verify_lock_anchors as vla  # noqa: E402


BASELINE_DD_PROTECTION = """\
DD_TRIGGER = 0.015
DD_SCALE = 0.40
"""

BASELINE_FIRM_RULES = """\
_BASE_RISK = {"striker": 0.0070, "striker_nas100": 0.0037}
"""

BASELINE_HISTORICAL = """\
HISTORICAL_CHALLENGE_BASE_RISK = {"guardian": 0.0034, "striker": 0.0070, "aegis": 0.0150, "striker_nas100": 0.0037}
"""


def _write_baseline(tmp_path: Path, **overrides: str) -> vla.Sources:
    dd = tmp_path / "dd_protection.py"
    fr = tmp_path / "firm_rules.py"
    hc = tmp_path / "historical_challenge.py"
    dd.write_text(
        overrides.get("dd_protection", BASELINE_DD_PROTECTION), encoding="utf-8"
    )
    fr.write_text(
        overrides.get("firm_rules", BASELINE_FIRM_RULES), encoding="utf-8"
    )
    hc.write_text(
        overrides.get("historical_challenge", BASELINE_HISTORICAL), encoding="utf-8"
    )
    return vla.Sources(
        dd_protection=dd, firm_rules=fr, historical_challenge=hc
    )


def test_default_sources_use_live_paths():
    sources = vla.Sources()
    assert sources.dd_protection == vla.REPO_ROOT / "core" / "dd_protection.py"
    assert sources.firm_rules == vla.REPO_ROOT / "core" / "firm_rules.py"
    assert sources.historical_challenge == (
        vla.REPO_ROOT / "core" / "historical_challenge.py"
    )
    assert sources.dd_protection.is_file()
    assert sources.firm_rules.is_file()
    assert sources.historical_challenge.is_file()


def test_baseline_routes_closed(tmp_path):
    sources = _write_baseline(tmp_path)
    decision = vla.decide(sources)
    assert decision.routing == "Closed", (
        f"baseline must route Closed; got {decision.routing} with "
        f"drifts={decision.drifts} triggers={decision.triggers} "
        f"errors={decision.errors}"
    )
    assert decision.drifts == []
    assert decision.triggers == []
    assert decision.errors == []
    assert decision.exit_code() == 0


def test_forward_guardian_safe_band(tmp_path):
    drifted = BASELINE_HISTORICAL.replace(
        '"guardian": 0.0034',
        '"guardian": 0.0050',
    )
    sources = _write_baseline(tmp_path, historical_challenge=drifted)
    decision = vla.decide(sources)
    assert decision.routing == "Forward"
    names = {t.name for t in decision.triggers}
    assert "guardian_safe_band" in names, f"expected guardian_safe_band; got {names}"


def test_guardian_band_top_edge_does_not_fire(tmp_path):
    sources = _write_baseline(tmp_path)
    decision = vla.decide(sources)
    assert decision.routing == "Closed", (
        f"Guardian at exact top-edge 0.34% must not fire safe-band; "
        f"got {decision.routing} triggers={decision.triggers}"
    )


def test_error_missing_file(tmp_path):
    sources = _write_baseline(tmp_path)
    sources.dd_protection.unlink()
    decision = vla.decide(sources)
    assert decision.routing == "Error"
    assert decision.exit_code() == 3
    assert decision.errors
    assert any("dd_protection.py" in e for e in decision.errors)


def test_error_missing_dd_constant(tmp_path):
    bad = BASELINE_DD_PROTECTION.replace("DD_TRIGGER = 0.015\n", "")
    sources = _write_baseline(tmp_path, dd_protection=bad)
    decision = vla.decide(sources)
    assert decision.routing == "Error"
    assert any("DD_TRIGGER" in e for e in decision.errors)


def test_error_missing_historical_guardian(tmp_path):
    bad = 'HISTORICAL_CHALLENGE_BASE_RISK = {"striker": 0.0070}\n'
    sources = _write_baseline(tmp_path, historical_challenge=bad)
    decision = vla.decide(sources)
    assert decision.routing == "Error"
    assert any("HISTORICAL_CHALLENGE_BASE_RISK" in e for e in decision.errors)


def test_error_living_still_has_guardian(tmp_path):
    bad = (
        '_BASE_RISK = {"guardian": 0.0034, "striker": 0.0070, '
        '"aegis": 0.0150, "striker_nas100": 0.0037}\n'
    )
    sources = _write_baseline(tmp_path, firm_rules=bad)
    decision = vla.decide(sources)
    assert decision.routing == "Error"
    assert any("guardian" in e for e in decision.errors)
