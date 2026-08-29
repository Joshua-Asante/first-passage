"""Adversarial tests for scripts/check_instrument_rejection_coverage.py.

D4 enforcement instrument for docs/adr/2026-08-09-rejection-register-topology-
and-bar-wiring.md -- the ADR's own §4 falsifier (checked quarterly, next
2026-11-08) needs to know: does every terminal-negative closure naming a
specific instrument have a corresponding DEAD row in that instrument's
ops/instruments/<SYM>.md?

Mutation-testing discipline (feedback_discipline_guards_need_adversarial_tests):
a checker that only has a failing fixture could pass by always returning
non-zero. Every REQUIRED behavior below has a fixture that must produce that
exact outcome -- including fixtures that must come back CLEAN, so a
vacuous "always flag everything" implementation cannot pass this file either.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts" / "check_instrument_rejection_coverage.py"


def _run(tmp_path: Path, extra_args: list[str] | None = None) -> subprocess.CompletedProcess:
    env_override = {"REPO_ROOT_OVERRIDE": str(tmp_path)}
    import os

    env = {**os.environ, **env_override}
    return subprocess.run(
        [sys.executable, str(SCRIPT), *(extra_args or [])],
        capture_output=True,
        text=True,
        cwd=REPO,
        env=env,
    )


def test_flags_a_closure_with_no_dead_row(tmp_path, monkeypatch):
    closures = tmp_path / "docs" / "briefs" / "closures"
    closures.mkdir(parents=True)
    (closures / "Q-FAKE-1-closure-falsified.md").write_text(
        "# Q-FAKE-1\n\n**Instrument:** MNQ\n\n**Closure basis:** FALSIFIED.\n"
    )
    instruments = tmp_path / "ops" / "instruments"
    instruments.mkdir(parents=True)
    (instruments / "MNQ.md").write_text("# MNQ\n\n## DEAD / REJECTED\n\n| date | mechanism |\n|---|---|\n")

    monkeypatch.setenv("REPO_ROOT_OVERRIDE", str(tmp_path))
    result = subprocess.run(
        [sys.executable, "scripts/check_instrument_rejection_coverage.py"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "Q-FAKE-1" in result.stdout
    assert "MNQ" in result.stdout


def test_passes_when_closure_is_linked_from_the_dead_row(tmp_path):
    """Adversarial guard: the mirror-image fixture must come back CLEAN.

    A checker that flags everything regardless of content would pass the
    RED test above but must fail here.
    """
    closures = tmp_path / "docs" / "briefs" / "closures"
    closures.mkdir(parents=True)
    (closures / "Q-REAL-1-closure-falsified.md").write_text(
        "# Q-REAL-1 -- CLOSURE: `FALSIFIED`\n\n**Verdict:** `FALSIFIED`\n\n**Instrument:** MNQ\n"
    )
    instruments = tmp_path / "ops" / "instruments"
    instruments.mkdir(parents=True)
    (instruments / "MNQ.md").write_text(
        "# MNQ\n\n## DEAD / REJECTED (instrument-specific)\n\n"
        "| Rejection | Discriminator | K | Source |\n|---|---|---|---|\n"
        "| some construct | some test | 0 | `FALSIFIED` -- "
        "[`closure`](../../docs/briefs/closures/Q-REAL-1-closure-falsified.md) |\n"
    )

    result = _run(tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr


def test_ignores_domain_level_closure_naming_no_instrument(tmp_path):
    """A closure that names zero known instrument tickers is domain-level /
    cross-instrument under D3 -- it belongs in rejected_candidates.md, not an
    instrument ledger, so this gate must not flag it even with no DEAD row
    anywhere."""
    closures = tmp_path / "docs" / "briefs" / "closures"
    closures.mkdir(parents=True)
    (closures / "Q-DOMAIN-1-closure-falsified.md").write_text(
        "# Q-DOMAIN-1 -- CLOSURE: `FALSIFIED`\n\n**Verdict:** `FALSIFIED`\n\n"
        "A cross-portfolio breadth argument, no single instrument named.\n"
    )
    instruments = tmp_path / "ops" / "instruments"
    instruments.mkdir(parents=True)
    (instruments / "MNQ.md").write_text("# MNQ\n\n## DEAD / REJECTED\n\n| date | mechanism |\n|---|---|\n")

    result = _run(tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr


def test_ignores_positive_verdict_closure(tmp_path):
    """A RESOLVED (pass) closure is not a rejection at all -- must not be
    flagged just because no DEAD row cites it."""
    closures = tmp_path / "docs" / "briefs" / "closures"
    closures.mkdir(parents=True)
    (closures / "Q-PASS-1-closure-resolved.md").write_text(
        "# Q-PASS-1 -- CLOSURE: `RESOLVED`\n\n**Verdict:** `RESOLVED`\n\n**Instrument:** MNQ\n"
    )
    instruments = tmp_path / "ops" / "instruments"
    instruments.mkdir(parents=True)
    (instruments / "MNQ.md").write_text("# MNQ\n\n## DEAD / REJECTED\n\n| date | mechanism |\n|---|---|\n")

    result = _run(tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr


def test_reports_skip_not_silent_pass_when_ledger_has_no_dead_section(tmp_path):
    """An instrument ledger with no DEAD/REJECTED (or 'Dead / parked') heading
    at all (e.g. the real repo's 6J.md / GER40.md today) must be reported as
    SKIPPED / uncheckable, never silently counted as either covered or a gap."""
    closures = tmp_path / "docs" / "briefs" / "closures"
    closures.mkdir(parents=True)
    (closures / "Q-NOHOME-1-closure-falsified.md").write_text(
        "# Q-NOHOME-1 -- CLOSURE: `FALSIFIED`\n\n**Verdict:** `FALSIFIED`\n\n**Instrument:** GER40\n"
    )
    instruments = tmp_path / "ops" / "instruments"
    instruments.mkdir(parents=True)
    (instruments / "GER40.md").write_text(
        "# GER40\n\n## DURABLE FINDINGS\n\nNo dead table on this ledger.\n"
    )

    result = _run(tmp_path)
    assert "GER40" in result.stdout
    assert "skip" in result.stdout.lower() or "no dead" in result.stdout.lower()


def test_passes_when_dead_row_cites_campaign_id_without_a_closure_link(tmp_path):
    """Real-corpus finding (MNQ.md's Q-R2VBUCK-1 row): a genuine DEAD-table row
    often names the campaign ID and links a RESULTS/PREREG file instead of the
    closures/ file itself. That must still count as covered -- requiring a
    literal closures/<filename> link would false-flag real, well-formed rows."""
    closures = tmp_path / "docs" / "briefs" / "closures"
    closures.mkdir(parents=True)
    (closures / "Q-IDONLY-1-closure-falsified.md").write_text(
        "# Q-IDONLY-1 -- CLOSURE: `FALSIFIED`\n\n**Verdict:** `FALSIFIED`\n\n**Instrument:** MNQ\n"
    )
    instruments = tmp_path / "ops" / "instruments"
    instruments.mkdir(parents=True)
    instruments_dir_text = (
        "# MNQ\n\n## DEAD / REJECTED (instrument-specific)\n\n"
        "| Rejection | Discriminator | K | Source |\n|---|---|---|---|\n"
        "| some construct (`Q-IDONLY-1` Route B) | null result | 1 | "
        "`FALSIFIED` 2026-08-08 -- [`RESULTS_g2.md`](../../lab/archive/foo/RESULTS_g2.md) |\n"
    )
    (instruments / "MNQ.md").write_text(instruments_dir_text)

    result = _run(tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr


def test_exit_zero_flag_never_fails_even_on_a_real_gap(tmp_path):
    """gates.yml wiring flag (Step 7, WARN-tier posture): must always exit 0
    while still printing the finding, since gate_manifest.py has no tier that
    runs-but-never-blocks other than a script's own exit code."""
    closures = tmp_path / "docs" / "briefs" / "closures"
    closures.mkdir(parents=True)
    (closures / "Q-FAKE-2-closure-falsified.md").write_text(
        "# Q-FAKE-2\n\n**Instrument:** MNQ\n\n**Verdict:** `FALSIFIED`\n"
    )
    instruments = tmp_path / "ops" / "instruments"
    instruments.mkdir(parents=True)
    (instruments / "MNQ.md").write_text("# MNQ\n\n## DEAD / REJECTED\n\n| date | mechanism |\n|---|---|\n")

    result = _run(tmp_path, ["--exit-zero"])
    assert result.returncode == 0
    assert "Q-FAKE-2" in result.stdout
