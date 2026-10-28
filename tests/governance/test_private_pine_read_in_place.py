"""Private Pine is read in place, never copied into a worktree.

docs/operational_rules.md §9 and campaign §60 rule 1: the accepted book's Pine
and runtime ports are read by the primary checkout's absolute path. The retired
worktree-copy tool copied every ``*.pine`` under the primary checkout, book files
included; these tests keep it retired and keep operational_rules §9 on the in-place mechanism.
"""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parents[2]
STEM = "sync_pine_to_worktree"
# A bare or repo-relative citation is a live instruction; one inside a pinned URL is history.
LIVE_CITATION = re.compile(rf"(?<![/\w])(?:scripts/)?{STEM}\b")
# Dated audit bodies and the generated, report-only docs-runtime inventory.
DATED_PREFIXES = ("docs/notes/audits/",)
EFFECTIVE_INPUTS = "ops/c1_signal_daemon/ports/effective_inputs.json"

needs_git = pytest.mark.skipif(shutil.which("git") is None, reason="git required")


def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True)


def _book_sources() -> list[str]:
    lines = (REPO / "core/strategies/BOOK_SOURCES.sha256").read_text(encoding="utf-8").splitlines()
    return [line.split()[-1] for line in lines if line.strip() and not line.startswith("#")]


def test_copy_tool_is_retired():
    assert not (REPO / "scripts" / f"{STEM}.py").exists()
    layers = yaml.safe_load((REPO / "scripts/repo_map_layers.yml").read_text(encoding="utf-8"))
    assert STEM not in layers["scripts_layer"]


@needs_git
def test_no_tracked_file_cites_the_copy_tool_live():
    listed = _git("grep", "-l", "-I", "-F", STEM)
    assert listed.returncode in (0, 1), listed.stderr
    own = Path(__file__).resolve().relative_to(REPO).as_posix()
    live = []
    for relative in listed.stdout.splitlines():
        if relative == own or relative.startswith(DATED_PREFIXES):
            continue
        text = (REPO / relative).read_text(encoding="utf-8")
        live += [f"{relative}:{n}" for n, line in enumerate(text.splitlines(), 1) if LIVE_CITATION.search(line)]
    assert not live, f"retired Pine copy tool cited as live: {live}"


def test_rule_9_reads_pine_in_place():
    rules = (REPO / "docs/operational_rules.md").read_text(encoding="utf-8")
    rule_9 = rules[rules.index("\n## 9. "):rules.index("\n## 10. ")]
    assert "absolute path" in rule_9 and "Never copy" in rule_9
    assert "core/strategies/book/" in rule_9


@needs_git
@pytest.mark.parametrize("relative", [*_book_sources(), EFFECTIVE_INPUTS])
def test_private_source_is_gitignored(relative):
    # Tooling that copies only tracked and unignored files (the P7 code root) then cannot copy it.
    assert _git("check-ignore", "-q", relative).returncode == 0, relative
