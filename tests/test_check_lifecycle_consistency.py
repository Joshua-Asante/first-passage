"""Unit tests for scripts/check_lifecycle_consistency.py — lifecycle-tier
restatement gate.

core/lifecycle.py's TIER_MULTIPLIER ladder is the ground truth; tests write
synthetic markdown under tmp_path and check against the REAL core/lifecycle.py
(the script always imports the real module — only the scanned directory is a
fixture, matching how the gate actually runs in production).
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_LC_PATH = REPO_ROOT / "scripts" / "check_lifecycle_consistency.py"
_spec = importlib.util.spec_from_file_location("check_lifecycle_consistency", _LC_PATH)
lc = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = lc
_spec.loader.exec_module(lc)


def _write(tmp_path: Path, rel: str, text: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def test_clean_correct_restatement_produces_no_findings(tmp_path):
    _write(tmp_path, "CLAUDE.md", "state: `AUTHORIZED · MECHANISM @ 1.00×`\n")
    assert lc.collect_findings(tmp_path) == []


def test_l1_flags_internally_inconsistent_tier_multiplier_pair(tmp_path):
    _write(tmp_path, "doc.md", "stays `AUTHORIZED · MECHANISM @ 0.50×`\n")
    findings = lc.collect_findings(tmp_path)
    assert len(findings) == 1
    assert findings[0].code == "L1"
    assert "AUTHORIZED" in findings[0].message and "0.50" in findings[0].message


def test_l2_flags_non_default_tier_when_state_is_uniform(tmp_path):
    # No lifecycle_state.json in this real repo -> uniform_state is True, so
    # WATCH-1 (a real, ladder-valid pairing) is still stale relative to the
    # actual current default.
    _write(tmp_path, "doc.md", "leg is `WATCH-1 · MECHANISM @ 0.50×`\n")
    findings = lc.collect_findings(tmp_path)
    assert len(findings) == 1
    assert findings[0].code == "L2"


def test_unknown_tier_word_flagged_as_l1(tmp_path):
    _write(tmp_path, "doc.md", "leg is `PENDING · MECHANISM @ 1.00×`\n")
    # "PENDING" isn't in TIER_MULTIPLIER's alternation, so the regex itself
    # won't match it -- confirms the gate doesn't false-positive on prose
    # that merely LOOKS tier-shaped but uses a word outside the real ladder.
    assert lc.collect_findings(tmp_path) == []


def test_historical_paths_are_exempt(tmp_path):
    for prefix in (
        "docs/adr/2026-01-01-x.md",
        "docs/briefs/closures/Q-X-closure-dead.md",
        "docs/notes/audits/2026-01-01-x.md",
        "docs/ltm/notes/x.md",
        "docs/superpowers/specs/x.md",
    ):
        _write(tmp_path, prefix, "stays `AUTHORIZED · MECHANISM @ 0.50×`\n")
    assert lc.collect_findings(tmp_path) == []


def test_live_path_outside_exempt_prefixes_is_checked(tmp_path):
    _write(tmp_path, "ops/instruments/FOO.md", "stays `AUTHORIZED · MECHANISM @ 0.50×`\n")
    findings = lc.collect_findings(tmp_path)
    assert len(findings) == 1 and findings[0].code == "L1"


def test_multiple_pairs_on_one_line_all_checked(tmp_path):
    _write(
        tmp_path, "doc.md",
        "A `AUTHORIZED @ 1.00×` and B `AUTHORIZED @ 0.50×` differ.\n",
    )
    findings = lc.collect_findings(tmp_path)
    assert len(findings) == 1  # only the second pairing is inconsistent
    assert findings[0].code == "L1"


def test_current_repo_tree_is_clean():
    """Guards against a real regression: today's ~9 live citations of the
    lifecycle tier must actually pass this gate, not just the synthetic
    fixtures above."""
    assert lc.collect_findings(REPO_ROOT) == []


def test_main_cli_exit_code_nonzero_on_finding(tmp_path, capsys):
    _write(tmp_path, "doc.md", "stays `AUTHORIZED · MECHANISM @ 0.50×`\n")
    rc = lc.main(["--repo-root", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "L1" in out


def test_main_cli_exit_code_zero_when_clean(tmp_path, capsys):
    _write(tmp_path, "doc.md", "stays `AUTHORIZED · MECHANISM @ 1.00×`\n")
    rc = lc.main(["--repo-root", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "OK" in out
