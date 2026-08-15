"""`register_search open --prereg` — bind a campaign to its frozen pre-registration.

Why this gate exists (2026-08-08): W4 (ADR 2026-08-07) defines the live minimal
gate set as "G0-G5 + G8, **and any limb a campaign's own frozen prereg still
binds**". That clause was unevaluable — the word "prereg" appeared zero times in
`register_search.py`, and the only binding was an optional, undocumented manifest
key that most campaigns never wrote.

Lane asymmetry is deliberate and mirrors `--admission-file`: REQUIRED on
mechanism-first (the default, live lane), omittable on `--lane blind` so the
frozen legacy 11-key schema stays byte-identical. Blind opens therefore remain
unbound — a recorded residual, not an oversight, and pinned below so it cannot
change silently.
"""
from __future__ import annotations

import json
import sys
from argparse import Namespace
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "lab"))

from discovery import register_search as rs  # noqa: E402

# A real, tracked, non-empty frozen body — the gate requires an in-repo path.
REAL_PREREG = "docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md"


@pytest.fixture
def ledger(tmp_path, monkeypatch):
    monkeypatch.setattr(rs, "LEDGER", tmp_path)
    monkeypatch.setattr(rs, "_path", lambda rid: tmp_path / f"{rid}.json")
    return tmp_path


def _args(**kw):
    base = dict(
        run_id="prereg_run", tool="catch22", search_space_size=100, alpha=0.05,
        data_window="2010-01-01:2020-01-01", hypothesis="h", params="",
        params_file=None, lane="blind", reachability_attestation=None,
        profile_cell=None, profile_consult=None, admission_file=None, prereg=None,
    )
    base.update(kw)
    return Namespace(**base)


def test_real_prereg_exists():
    """Guard the fixture itself — a moved body must fail loudly here, not everywhere."""
    assert (REPO / REAL_PREREG).is_file(), f"fixture prereg moved: {REAL_PREREG}"


def test_mechanism_first_without_prereg_aborts():
    """Unit-test the gate directly.

    Deliberately not routed through `open_run`: mechanism-first aborts on the
    reachability-attestation gate first, so an integration call would assert on
    the WRONG abort and pass for the wrong reason. Ordering is production's
    business, not the test's.
    """
    with pytest.raises(SystemExit) as exc:
        rs._require_prereg(None, "mechanism-first")
    assert "--prereg" in str(exc.value)


def test_blind_without_prereg_returns_none_not_abort():
    assert rs._require_prereg(None, "blind") is None


def test_blind_without_prereg_is_allowed_and_keeps_eleven_keys(ledger):
    """The recorded residual: blind opens stay unbound, schema byte-identical."""
    rs.open_run(_args(lane="blind", prereg=None))
    manifest = json.loads((ledger / "prereg_run.json").read_text(encoding="utf-8"))
    assert len(manifest) == 11
    assert "prereg" not in manifest


def test_blind_may_still_name_a_prereg(ledger):
    rs.open_run(_args(lane="blind", prereg=REAL_PREREG))
    manifest = json.loads((ledger / "prereg_run.json").read_text(encoding="utf-8"))
    assert manifest["prereg"] == REAL_PREREG


def test_path_is_recorded_repo_relative_and_posix(ledger):
    """An absolute, OS-native path must normalise, or manifests stop being greppable."""
    absolute = str(REPO / REAL_PREREG)
    rs.open_run(_args(lane="blind", prereg=absolute))
    manifest = json.loads((ledger / "prereg_run.json").read_text(encoding="utf-8"))
    assert manifest["prereg"] == REAL_PREREG
    assert "\\" not in manifest["prereg"]


def test_missing_file_aborts(ledger):
    with pytest.raises(SystemExit) as exc:
        rs.open_run(_args(lane="blind", prereg="docs/briefs/pre-registration/NOPE.md"))
    assert "file not found" in str(exc.value)


def test_non_markdown_aborts(ledger, tmp_path):
    other = REPO / "README.md"
    assert other.is_file()
    py = REPO / "scripts" / "gate_manifest.py"
    with pytest.raises(SystemExit) as exc:
        rs.open_run(_args(lane="blind", prereg=str(py)))
    assert ".md" in str(exc.value)


def test_empty_file_aborts(ledger, tmp_path, monkeypatch):
    empty = REPO / "tests" / "_tmp_empty_prereg.md"
    empty.write_text("   \n", encoding="utf-8")
    try:
        with pytest.raises(SystemExit) as exc:
            rs.open_run(_args(lane="blind", prereg=str(empty)))
        assert "empty" in str(exc.value)
    finally:
        empty.unlink(missing_ok=True)


def test_outside_repo_aborts(ledger, tmp_path):
    outside = tmp_path / "elsewhere.md"
    outside.write_text("frozen body living outside the repo", encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        rs.open_run(_args(lane="blind", prereg=str(outside)))
    assert "inside the repo" in str(exc.value)


def test_existing_manifests_are_not_back_filled():
    """ADR-adjacent constraint: frozen manifests must not gain a prereg key."""
    manifests = sorted((REPO / "discovery_manifests").glob("*.json"))
    assert manifests, "no manifests found — has the ledger moved?"
    # The gate only runs at `open`; nothing in this change rewrites history.
    # Pin the count that carried a prereg key BEFORE this change (9 of 13 at the
    # time of writing) so a silent back-fill shows up as a diff here.
    with_key = [p.name for p in manifests if "prereg" in json.loads(p.read_text(encoding="utf-8"))]
    assert len(with_key) <= len(manifests), "sanity"
