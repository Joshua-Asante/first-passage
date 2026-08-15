"""Controls for scripts/check_skills_no_constants.py (extracted from validate_params)."""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_skills_no_constants as snc  # noqa: E402


def _mk_skill(root: Path, name: str, body: str) -> None:
    d = root / ".claude" / "skills" / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(body, encoding="utf-8")


def _hard(repo_root: Path):
    return [v for v in snc.check_skills_no_constants(repo_root) if v.severity == "HARD"]


def test_skills_guard_clean_guarded_skill_no_violation(tmp_path):
    _mk_skill(
        tmp_path, "inqhiori",
        "Constants live in `core/dd_protection.py`; this skill points, never restates.\n",
    )
    assert _hard(tmp_path) == []


def test_skills_guard_restated_version_is_hard(tmp_path):
    _mk_skill(tmp_path, "inqhiori", "Striker version = v4.4 locked.\n")
    hard = _hard(tmp_path)
    assert any("inqhiori" in v.location for v in hard), hard


def test_skills_guard_restated_riskpct_is_hard(tmp_path):
    _mk_skill(tmp_path, "ooda-loop", "Allocation: risk_pct dict is G 0.34%.\n")
    assert _hard(tmp_path), "expected HARD on risk_pct restatement"


def test_skills_guard_restated_ddprotection_scale_is_hard(tmp_path):
    _mk_skill(tmp_path, "programme-audit", "dd_protection single-tier 1.0% / 0.40x.\n")
    assert _hard(tmp_path), "expected HARD on dd_protection constant"


def test_skills_guard_restated_allocation_pct_is_hard(tmp_path):
    _mk_skill(tmp_path, "brief-authoring", "Allocations: G 0.34% / S 1.00% / A 1.50%.\n")
    assert _hard(tmp_path), "expected HARD on allocation percentages"


def test_skills_guard_exempt_skill_not_scanned(tmp_path):
    _mk_skill(
        tmp_path, "prop-firm-challenge",
        "DD_TRIGGER = 0.010, risk_pct 0.34%, dd_protection 1.0% / 0.40x.\n",
    )
    assert _hard(tmp_path) == [], "exempt skill must not be flagged"


def test_skills_guard_noop_when_skills_absent(tmp_path):
    assert snc.check_skills_no_constants(tmp_path) == []
