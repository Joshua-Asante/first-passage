"""Tests for scripts/validate_c1_monitoring_acceptance.py.

Focus: the `fixture_hashes` tree-skew check added 2026-07-31.

`fixture_hashes` records the bytes ACTUALLY RUNNING on the Fly host, read
in-container. So "pin != tree" is a normal state between deploys, and the
load-bearing properties are (a) it is reported, and (b) it is NOT an error by
default — a gate that failed on legitimate drift would be turned off within a
day, and the pin would go back to drifting unwatched, which is the failure this
closes (28ab8a6 moved two of six pinned files and nothing noticed, because the
validator only ever checked the field was present).
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_PATH = _REPO / "scripts" / "validate_c1_monitoring_acceptance.py"
_spec = importlib.util.spec_from_file_location("validate_c1_m1", _PATH)
vm = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = vm
_spec.loader.exec_module(vm)

ADR = "2026-07-22-c1-venue-native-monitoring-maturity.md"


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _tree(root: Path, files: dict[str, str]) -> dict[str, str]:
    """Write files under root; return {relpath: sha256 of what was written}."""
    hashes = {}
    for rel, body in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(body.encode())
        hashes[rel] = _sha(p)
    return hashes


def _artifact(root: Path, fixture_hashes: dict[str, str]) -> Path:
    p = root / "M1.json"
    p.write_text(json.dumps({
        "schema_version": 1,
        "status": "CODE_LANDED",
        "adr": ADR,
        "code_commit_or_branch": "test",
        "offline_tests_note": "test",
        "secrets_present": False,
        "fixture_hashes": fixture_hashes,
    }, indent=2), encoding="utf-8")
    return p


def test_no_skew_when_tree_matches_the_deployed_pin(tmp_path):
    hashes = _tree(tmp_path, {"ops/a.py": "alpha\n", "ops/b.py": "beta\n"})
    assert vm.tree_skew(_artifact(tmp_path, hashes), root=tmp_path) == []


def test_skew_reports_the_file_with_both_hashes(tmp_path):
    """The 28ab8a6 shape: a pinned file moves in the tree while the host keeps
    running the pinned bytes."""
    hashes = _tree(tmp_path, {"ops/a.py": "alpha\n", "ops/b.py": "beta\n"})
    pinned_b = hashes["ops/b.py"]
    (tmp_path / "ops/b.py").write_bytes(b"beta CHANGED\n")   # main moves ahead

    skew = vm.tree_skew(_artifact(tmp_path, hashes), root=tmp_path)
    assert len(skew) == 1
    rel, pinned, actual = skew[0]
    assert rel == "ops/b.py"
    assert pinned == pinned_b, "must still report the DEPLOYED hash"
    assert actual == _sha(tmp_path / "ops/b.py") and actual != pinned


def test_a_pinned_file_missing_from_the_tree_is_reported_not_skipped(tmp_path):
    hashes = _tree(tmp_path, {"ops/a.py": "alpha\n"})
    (tmp_path / "ops/a.py").unlink()
    assert vm.tree_skew(_artifact(tmp_path, hashes), root=tmp_path) == [
        ("ops/a.py", hashes["ops/a.py"], "MISSING")]


def test_skew_is_not_an_error_by_default(tmp_path):
    """A plain run must stay exit 0 with skew present.

    Drift between deploys is legitimate; if the default run failed on it, the
    check would be disabled and the pin would drift unwatched again.
    """
    hashes = _tree(tmp_path, {"ops/a.py": "alpha\n"})
    (tmp_path / "ops/a.py").write_bytes(b"changed\n")
    art = _artifact(tmp_path, hashes)
    assert vm.main([str(art), "--root", str(tmp_path)]) == 0
    assert vm.main(
        [str(art), "--check-tree-skew", "--root", str(tmp_path)]
    ) == 0, "reports, does not fail"


def test_require_tree_current_is_the_opt_in_that_fails(tmp_path, capsys):
    """Pre-deploy / pre-arm use, where "deployed == what I reviewed" matters."""
    hashes = _tree(tmp_path, {"ops/a.py": "alpha\n"})
    art = _artifact(tmp_path, hashes)
    assert vm.main([str(art), "--require-tree-current", "--root", str(tmp_path)]) == 0

    (tmp_path / "ops/a.py").write_bytes(b"changed\n")
    assert vm.main([str(art), "--require-tree-current", "--root", str(tmp_path)]) == 1
    out = capsys.readouterr().out
    assert "ops/a.py" in out
    assert "never from these tree bytes" in out, (
        "must say how to refresh, or the next deploy repeats the miss")


def test_the_check_never_rewrites_the_artifact(tmp_path):
    """It would be self-defeating for a skew reporter to 'fix' the pin: that
    would assert a deploy that never happened."""
    hashes = _tree(tmp_path, {"ops/a.py": "alpha\n"})
    art = _artifact(tmp_path, hashes)
    (tmp_path / "ops/a.py").write_bytes(b"changed\n")
    before = art.read_bytes()
    vm.main([str(art), "--check-tree-skew", "--root", str(tmp_path)])
    assert art.read_bytes() == before


def test_live_artifact_records_the_open_skew_rather_than_hiding_it(tmp_path):
    """Guards the honesty fix itself: while deployed != main, the artifact must
    say so. Structural — it asserts the note tracks the check, not a hash."""
    live = _REPO / "docs" / "notes" / "rail_build" / "M1_MONITORING_ACCEPTANCE.json"
    data = json.loads(live.read_text(encoding="utf-8"))
    skew = vm.tree_skew(live)
    if skew:
        note = data["fixture_hashes_note"]
        assert "SKEW OPENED" in note
        for rel, _pinned, _actual in skew:
            assert rel in note, f"{rel} diverges but is not named in the note"
