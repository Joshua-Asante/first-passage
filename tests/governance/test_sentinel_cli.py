"""Sentinel CLI end-to-end (subprocess) tests.

Exercises `__main__.main()`'s print path, not just the pure scan/report
functions the other test_sentinel_*.py files cover. The 2026-08-17 weekly
run crashed here: `docs/notes/sentinel/queue.md` was written correctly
(`_prepend_run` pins `encoding="utf-8"`), but the console summary print
raised `UnicodeEncodeError` on a stock Windows console (cp1252 can't encode
the U+2192 arrow in the activity-decision label), taking the CLI's exit code
from the documented "always exits 0" (see __main__.py's module docstring) to
a crash.

`PYTHONIOENCODING=cp1252` forces the same console encoding in the child
process regardless of host OS/locale, so this reproduces deterministically
in CI, not just on a Windows box.
"""
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def _run_cli(tmp_path: Path, asof: str = "2026-08-17") -> subprocess.CompletedProcess:
    env = {**os.environ, "PYTHONIOENCODING": "cp1252"}
    return subprocess.run(
        [sys.executable, "-m", "sentinel", "--asof", asof, "--root", str(tmp_path)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        env=env, cwd=REPO_ROOT,
    )


def test_cli_survives_legacy_console_codepage(tmp_path):
    """Regression: must not crash when stdout is bound to cp1252 (2026-08-17
    weekly run). The module docstring promises exit 0 always -- report-only
    tools must not fail the caller (`make sentinel`) over a console encoding
    quirk after the real work (the queue write) already succeeded."""
    result = _run_cli(tmp_path)
    assert result.returncode == 0, (
        f"sentinel CLI must exit 0 under cp1252 stdout; stderr:\n{result.stderr}"
    )
    assert "UnicodeEncodeError" not in result.stderr


def test_cli_prints_activity_line_and_summary(tmp_path):
    """Sanity: the console summary this bug hid (activity line + finding
    count) actually reaches stdout when the process succeeds, and the queue
    file lands where documented."""
    result = _run_cli(tmp_path)
    assert "weekly activity decision" in result.stdout
    assert "sentinel: 0 finding(s)" in result.stdout
    assert (tmp_path / "docs" / "notes" / "sentinel" / "queue.md").exists()
