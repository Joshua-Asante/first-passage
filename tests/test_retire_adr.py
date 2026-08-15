"""Tests for scripts/retire_adr.py - ADR lifecycle retire helper (Task 7).

Design: docs/superpowers/specs/2026-07-17-adr-lifecycle-graph-design.md
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
_RA_PATH = REPO_ROOT / "scripts" / "retire_adr.py"
_spec = importlib.util.spec_from_file_location("retire_adr", _RA_PATH)
ra = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = ra
_spec.loader.exec_module(ra)


OLD_BODY = """# old
**Status:** `Accepted`
**Decision date:** 2026-01-01
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

## A2 - Decision

See [brief](../briefs/x.md).
"""

NEW_BODY = """# new
**Status:** `Accepted`
**Decision date:** 2026-02-01
**Supersedes:** `2026-01-01-old.md` full
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

## A2 - Decision

y
"""


def _setup_repo(tmp_path: Path) -> tuple[Path, Path, Path]:
    adr = tmp_path / "docs" / "adr"
    ltm = tmp_path / "docs" / "ltm" / "adr"
    adr.mkdir(parents=True)
    return tmp_path, adr, ltm


def _run_cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(_RA_PATH), *args],
        check=False, capture_output=True, text=True,
    )


def test_retire_superseded_writes_stub_and_ltm(tmp_path: Path):
    tmp, adr, ltm = _setup_repo(tmp_path)
    (adr / "2026-01-01-old.md").write_text(OLD_BODY, encoding="utf-8")
    (adr / "2026-02-01-new.md").write_text(NEW_BODY, encoding="utf-8")

    rc = _run_cli(
        "2026-01-01-old.md", "--reason", "superseded",
        "--by", "2026-02-01-new.md", "--repo-root", str(tmp),
    )
    assert rc.returncode == 0, rc.stderr

    stub = (adr / "2026-01-01-old.md").read_text(encoding="utf-8")
    assert "**Body:**" in stub
    assert "## " not in stub
    assert stub.count("\n") + 1 <= 40
    assert "`Superseded`" in stub
    assert "2026-02-01-new.md" in stub

    body = (ltm / "2026-01-01-old.md").read_text(encoding="utf-8")
    assert "../../briefs/x.md" in body or "../briefs/" not in body
    assert "relocated from docs/adr" in body
    assert "`Superseded`" in body

    idx = (adr / "INDEX.md").read_text(encoding="utf-8")
    assert "2026-01-01-old.md" in idx
    assert "2026-02-01-new.md" in idx


def test_retire_superseded_requires_by(tmp_path: Path):
    tmp, adr, _ltm = _setup_repo(tmp_path)
    (adr / "2026-01-01-old.md").write_text(OLD_BODY, encoding="utf-8")

    rc = _run_cli("2026-01-01-old.md", "--reason", "superseded", "--repo-root", str(tmp))
    assert rc.returncode != 0
    assert "--by" in rc.stderr


def test_retire_superseded_rejects_non_accepted_successor(tmp_path: Path):
    tmp, adr, _ltm = _setup_repo(tmp_path)
    (adr / "2026-01-01-old.md").write_text(OLD_BODY, encoding="utf-8")
    proposed_new = NEW_BODY.replace("`Accepted`", "`Proposed`", 1)
    (adr / "2026-02-01-new.md").write_text(proposed_new, encoding="utf-8")

    rc = _run_cli(
        "2026-01-01-old.md", "--reason", "superseded",
        "--by", "2026-02-01-new.md", "--repo-root", str(tmp),
    )
    assert rc.returncode != 0
    assert "Accepted" in rc.stderr


def test_retire_superseded_rejects_missing_supersedes_edge(tmp_path: Path):
    tmp, adr, _ltm = _setup_repo(tmp_path)
    (adr / "2026-01-01-old.md").write_text(OLD_BODY, encoding="utf-8")
    no_edge_new = NEW_BODY.replace(
        "**Supersedes:** `2026-01-01-old.md` full", "**Supersedes:** none"
    )
    (adr / "2026-02-01-new.md").write_text(no_edge_new, encoding="utf-8")

    rc = _run_cli(
        "2026-01-01-old.md", "--reason", "superseded",
        "--by", "2026-02-01-new.md", "--repo-root", str(tmp),
    )
    assert rc.returncode != 0
    assert "Supersedes" in rc.stderr


def test_retire_superseded_rejects_in_part_edge(tmp_path: Path):
    tmp, adr, _ltm = _setup_repo(tmp_path)
    (adr / "2026-01-01-old.md").write_text(OLD_BODY, encoding="utf-8")
    in_part_new = NEW_BODY.replace(
        "**Supersedes:** `2026-01-01-old.md` full",
        "**Supersedes:** `2026-01-01-old.md` in part - partial",
    )
    (adr / "2026-02-01-new.md").write_text(in_part_new, encoding="utf-8")

    rc = _run_cli(
        "2026-01-01-old.md", "--reason", "superseded",
        "--by", "2026-02-01-new.md", "--repo-root", str(tmp),
    )
    assert rc.returncode != 0


def test_retire_withdrawn_no_successor_needed(tmp_path: Path):
    tmp, adr, ltm = _setup_repo(tmp_path)
    (adr / "2026-01-01-old.md").write_text(OLD_BODY, encoding="utf-8")

    rc = _run_cli(
        "2026-01-01-old.md", "--reason", "withdrawn", "--repo-root", str(tmp),
        "--today", "2026-07-17",
    )
    assert rc.returncode == 0, rc.stderr
    stub = (adr / "2026-01-01-old.md").read_text(encoding="utf-8")
    assert "`Withdrawn`" in stub
    assert "**Superseded-by:** none" in stub
    body = (ltm / "2026-01-01-old.md").read_text(encoding="utf-8")
    assert "`Withdrawn`" in body
    assert "2026-07-17" in body


def test_retire_retired_no_successor_needed(tmp_path: Path):
    tmp, adr, ltm = _setup_repo(tmp_path)
    (adr / "2026-01-01-old.md").write_text(OLD_BODY, encoding="utf-8")

    rc = _run_cli("2026-01-01-old.md", "--reason", "retired", "--repo-root", str(tmp))
    assert rc.returncode == 0, rc.stderr
    stub = (adr / "2026-01-01-old.md").read_text(encoding="utf-8")
    assert "`Retired`" in stub
    assert (ltm / "2026-01-01-old.md").is_file()


def test_retire_missing_adr_errors(tmp_path: Path):
    tmp, _adr, _ltm = _setup_repo(tmp_path)
    rc = _run_cli("2026-01-01-nope.md", "--reason", "retired", "--repo-root", str(tmp))
    assert rc.returncode != 0
    assert "missing ADR" in rc.stderr


def test_rewrite_relative_links_parent_gets_extra_dotdot():
    text = "See [brief](../briefs/x.md) for context."
    out = ra.rewrite_relative_links(text)
    assert "../../briefs/x.md" in out


def test_rewrite_relative_links_peer_adr_rebased():
    text = "See [peer](2026-01-01-peer.md) and [also](./2026-02-02-other.md)."
    out = ra.rewrite_relative_links(text)
    assert "../../adr/2026-01-01-peer.md" in out
    assert "../../adr/2026-02-02-other.md" in out


def test_rewrite_relative_links_leaves_external_and_anchors():
    text = "See [notion](https://www.notion.so/abc) and [self](#section)."
    out = ra.rewrite_relative_links(text)
    assert "https://www.notion.so/abc" in out
    assert "(#section)" in out


def test_set_header_field_only_touches_first_occurrence():
    text = (
        "**Status:** `Accepted`\n\n## Addendum\n\n**Status:** `Withdrawn`\n"
    )
    out = ra.set_header_field(text, "Status", "`Superseded`")
    lines = out.splitlines()
    assert lines[0] == "**Status:** `Superseded`"
    assert "`Withdrawn`" in out


def test_extract_tier_reads_light_value():
    text = OLD_BODY.replace(
        "**Retain-until:** none\n",
        "**Retain-until:** none\n**Tier:** light\n",
        1,
    )
    assert ra.extract_tier(text) == "light"


def test_extract_tier_absent_returns_none():
    assert ra.extract_tier(OLD_BODY) is None


def test_build_stub_preserves_light_tier():
    stub = ra.build_stub(
        "2026-08-10-example.md",
        "example",
        "Superseded",
        "2026-08-10",
        "`2026-08-13-successor.md`",
        "Fully superseded by `2026-08-13-successor.md` on 2026-08-13.",
        tier="light",
    )
    assert "**Tier:** light" in stub
    # Tier sits with the other header fields, before Body.
    assert stub.index("**Tier:** light") < stub.index("**Body:**")


def test_build_stub_omits_tier_when_absent():
    stub = ra.build_stub(
        "2026-01-01-old.md",
        "old",
        "Retired",
        "2026-01-01",
        "none",
        "Retired on 2026-01-01.",
    )
    assert "**Tier:**" not in stub


def test_retire_light_tier_adr_preserves_tier_in_stub(tmp_path: Path):
    """Light-tier ADRs must keep **Tier:** light on the hot stub for census greps."""
    tmp, adr, _ltm = _setup_repo(tmp_path)
    light_old = OLD_BODY.replace(
        "**Retain-until:** none\n",
        "**Retain-until:** none\n**Tier:** light\n",
        1,
    )
    (adr / "2026-01-01-old.md").write_text(light_old, encoding="utf-8")
    (adr / "2026-02-01-new.md").write_text(NEW_BODY, encoding="utf-8")

    rc = _run_cli(
        "2026-01-01-old.md", "--reason", "superseded",
        "--by", "2026-02-01-new.md", "--repo-root", str(tmp),
    )
    assert rc.returncode == 0, rc.stderr
    stub = (adr / "2026-01-01-old.md").read_text(encoding="utf-8")
    assert "**Tier:** light" in stub


def test_retire_pre_tiering_adr_omits_tier_from_stub(tmp_path: Path):
    """Pre-tiering / full ADRs have no Tier field — stub must not invent one."""
    tmp, adr, _ltm = _setup_repo(tmp_path)
    (adr / "2026-01-01-old.md").write_text(OLD_BODY, encoding="utf-8")

    rc = _run_cli("2026-01-01-old.md", "--reason", "retired", "--repo-root", str(tmp))
    assert rc.returncode == 0, rc.stderr
    stub = (adr / "2026-01-01-old.md").read_text(encoding="utf-8")
    assert "**Tier:**" not in stub


def test_main_bad_reason_rejected_by_argparse(tmp_path: Path):
    rc = _run_cli("2026-01-01-old.md", "--reason", "bogus", "--repo-root", str(tmp_path))
    assert rc.returncode != 0

def test_retire_withdrawn_with_by_does_not_write_superseded_by(tmp_path: Path):
    """FU-6: --by on withdrawn must not fabricate a Superseded-by edge."""
    tmp, adr, ltm = _setup_repo(tmp_path)
    (adr / "2026-01-01-old.md").write_text(OLD_BODY, encoding="utf-8")
    (adr / "2026-02-01-new.md").write_text(NEW_BODY, encoding="utf-8")

    rc = _run_cli(
        "2026-01-01-old.md", "--reason", "withdrawn",
        "--by", "2026-02-01-new.md", "--repo-root", str(tmp),
        "--today", "2026-08-05",
    )
    assert rc.returncode == 0, rc.stderr

    stub = (adr / "2026-01-01-old.md").read_text(encoding="utf-8")
    assert "**Superseded-by:** none" in stub
    assert "2026-02-01-new.md" not in stub.split("**Superseded-by:**")[1].splitlines()[0]

    body = (ltm / "2026-01-01-old.md").read_text(encoding="utf-8")
    assert "**Superseded-by:** none" in body


def test_retire_index_failure_after_stub_ltm_shows_recovery_hint(tmp_path: Path, monkeypatch, capsys):
    tmp, adr, ltm = _setup_repo(tmp_path)
    (adr / "2026-01-01-old.md").write_text(OLD_BODY, encoding="utf-8")
    (adr / "2026-02-01-new.md").write_text(NEW_BODY, encoding="utf-8")

    def boom(_repo_root: Path) -> None:
        raise OSError("simulated index write failure")

    monkeypatch.setattr(ra, "_regenerate_index", boom)

    rc = ra.main([
        "2026-01-01-old.md", "--reason", "superseded",
        "--by", "2026-02-01-new.md", "--repo-root", str(tmp),
        "--today", "2026-07-17",
    ])
    assert rc == 1
    recovery = (
        f"python scripts/check_adr_graph.py --regenerate-index --repo-root {tmp}"
    )
    assert recovery in capsys.readouterr().err
    assert (ltm / "2026-01-01-old.md").is_file()
    assert "**Body:**" in (adr / "2026-01-01-old.md").read_text(encoding="utf-8")

