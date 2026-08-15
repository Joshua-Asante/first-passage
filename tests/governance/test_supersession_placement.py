"""Adversarial tests for check_supersession_placement (operational_rules.md Rule 14).

Per lesson_discipline_guards_need_adversarial_tests: a guard earns trust only by
FAILING on a planted defect. The planted-violation cases here are the load-bearing
ones — if they ever pass, the gate has gone vacuous.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

_spec = importlib.util.spec_from_file_location(
    "check_supersession_placement",
    REPO / "scripts" / "check_supersession_placement.py",
)
csp = importlib.util.module_from_spec(_spec)
sys.modules["check_supersession_placement"] = csp
_spec.loader.exec_module(csp)


def _scan(tmp_path, text: str):
    f = tmp_path / "RESULTS.md"
    f.write_text(text, encoding="utf-8")
    return csp.scan_file(f)


# ---------------------------------------------------------------- planted defects

def test_planted_violation_fails(tmp_path):
    """THE defect shape: supersession confined to a bottom addendum, silent head."""
    msg = _scan(tmp_path, (
        "# Title\n\n## §2 — Results\n\nThe answer is 4 in 5.\n\n"
        "## Addendum 2026-08-02c — resolved against this analysis\n\n"
        "The 4-in-5 figure is WITHDRAWN.\n"
    ))
    assert msg is not None, "gate went VACUOUS: planted violation passed"
    assert "withdraws content" in msg


def test_lowercase_superseded_in_addendum_heading_fails(tmp_path):
    """The real merged instance (cadence RESULTS): token in the heading itself."""
    msg = _scan(tmp_path, (
        "# Title\n\n## §2\n\nSoft-enforced, warning first.\n\n"
        "## Addendum — the premise in §2 is superseded\n\nDetail.\n"
    ))
    assert msg is not None


# ---------------------------------------------------------------- valid patterns

def test_head_banner_passes(tmp_path):
    """The Rule-14 repair: a banner upstream satisfies the intercept."""
    assert _scan(tmp_path, (
        "# Title\n\n> ⚠ SUPERSEDED — see Addendum c before citing §2.\n\n"
        "## §2 — Results\n\nThe answer is 4 in 5.\n\n"
        "## Addendum c\n\nWITHDRAWN.\n"
    )) is None


def test_upstream_pointer_passes(tmp_path):
    """A plain pointer ('read the Addendum first') also satisfies it."""
    assert _scan(tmp_path, (
        "# Title\n\nRead the Addendum before §2.\n\n## §2\n\nStuff.\n\n"
        "## Addendum\n\n§2 is RETRACTED.\n"
    )) is None


def test_additive_addendum_passes(tmp_path):
    """An addendum that extends rather than withdraws needs no banner."""
    assert _scan(tmp_path, (
        "# Title\n\n## §2\n\nMeasured X.\n\n"
        "## Addendum — MYM measured the same way\n\nAlso measured Y.\n"
    )) is None


def test_no_addendum_passes(tmp_path):
    """In-place corrections (no addendum heading) are Rule-14 prose territory,
    deliberately outside the mechanical gate's scope."""
    assert _scan(tmp_path, (
        "# Title\n\n## §1\n\n~~Old claim~~ WITHDRAWN — corrected in place.\n"
    )) is None


def test_empty_file_passes(tmp_path):
    assert _scan(tmp_path, "") is None


# ---------------------------------------------------------------- live repo state

def test_repo_is_currently_clean():
    """The gate holds on the real tree; a regression anywhere in scope fails here
    too, so CI catches what a skipped hook install would miss."""
    violations = [m for f in csp.in_scope(REPO) if (m := csp.scan_file(f))]
    assert violations == [], "\n".join(violations)

# ---------------------------------------------------------------- selector pins (C16 / FU-5)

def test_in_scope_covers_theme_nest_results():
    """Flat glob missed nested RESULTS; selector must reach the theme nest."""
    paths = csp.in_scope(REPO)
    assert len(paths) >= 60, f"selector too narrow: {len(paths)} files"
    assert any("/analysis/orb/" in f.as_posix().replace("\\", "/") for f in paths)
    assert any("DESK_CARD" in f.name for f in paths)
    assert not any("/lab/archive/" in f.as_posix().replace("\\", "/") for f in paths)

