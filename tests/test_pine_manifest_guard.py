"""Unit tests for scripts/check_pine_manifest.py (M-9 Pine-manifest gate).

Pins the presence-aware semantics:
  - clean present environment passes,
  - the historical M-9 skew (some files present, a stale entry pointing at a
    deleted file) HARD-fails via MISSING — this is the case the gate exists for,
  - hash drift fails via MISMATCH,
  - an unpinned on-disk .pine WARNS via EXTRA (exit 0) — a coverage gap, not a
    lie, so it must not block unrelated commits on an always-on hook,
  - a bare clone/CI (manifest entries but zero files on disk) warn-skips, exit 0,
  - a malformed manifest line fails regardless of environment.

PORT_MANIFEST.sha256 (port / venue-edition pins) is verified with the SAME
semantics as MANIFEST.sha256, sharing one union presence gate — pinned here as
regressions of the two 2026-07-17 silent failures (MYM drift MISMATCH, MNQ
MISSING) the previously MANIFEST-only gate never fired on. A path pinned in
both manifests under different digests is a CROSS_MANIFEST_CONFLICT hard-fail
in every environment.

All tests run on synthetic tmp trees, so they pass on a public clone / CI where
no real .pine is present.
"""
from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

_CPM_PATH = Path(__file__).resolve().parent.parent / "scripts" / "check_pine_manifest.py"
_spec = importlib.util.spec_from_file_location("check_pine_manifest", _CPM_PATH)
cpm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cpm)


def _write_pine(root: Path, rel: str, body: bytes) -> str:
    """Write a .pine file and return its sha256 (working-tree bytes)."""
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(body)
    return cpm.hash_file(p)


def _write_manifest(root: Path, lines: list[str], name: str = "MANIFEST.sha256") -> Path:
    m = root / "strategies" / name
    m.parent.mkdir(parents=True, exist_ok=True)
    header = "# Pine strategy source manifest\n# Hashes pinned for verification.\n\n"
    m.write_text(header + "\n".join(lines) + "\n", encoding="utf-8")
    return m


def _run(root: Path, is_linked_worktree: bool | None = None):
    # Mirror production wiring (both manifests), but only pass the ones a test
    # actually wrote — a missing manifest file is its own hard-fail, exercised
    # separately in test_missing_port_manifest_hard_fails.
    manifests = [
        root / "strategies" / name
        for name in ("MANIFEST.sha256", "PORT_MANIFEST.sha256")
        if (root / "strategies" / name).is_file()
    ]
    return cpm.check(
        manifest_paths=manifests,
        repo_root=root,
        pine_roots=[root / "strategies"],
        is_linked_worktree=is_linked_worktree,
    )


def test_clean_present_passes(tmp_path: Path) -> None:
    h = _write_pine(tmp_path, "strategies/a/strat.pine", b"//@version=6\nfoo\n")
    _write_manifest(tmp_path, [f"{h}  strategies/a/strat.pine"])
    res = _run(tmp_path)
    assert res.ok, res.failures
    assert not res.warnings


def test_m9_partial_presence_missing_hard_fails(tmp_path: Path) -> None:
    # Live file present + a stale entry pointing at a file that is not on disk.
    h_live = _write_pine(tmp_path, "strategies/a/live.pine", b"live\n")
    _write_manifest(
        tmp_path,
        [
            f"{h_live}  strategies/a/live.pine",
            "0" * 64 + "  archive/strategies/striker/striker_dj30_v4.4.pine",
        ],
    )
    res = _run(tmp_path)
    assert not res.ok
    assert any(f.startswith("MISSING ") and "v4.4" in f for f in res.failures), res.failures


def test_mismatch_hard_fails(tmp_path: Path) -> None:
    _write_pine(tmp_path, "strategies/a/strat.pine", b"real bytes\n")
    _write_manifest(tmp_path, ["a" * 64 + "  strategies/a/strat.pine"])
    res = _run(tmp_path)
    assert not res.ok
    assert any(f.startswith("MISMATCH ") for f in res.failures), res.failures


def test_extra_unpinned_pine_warns_not_fails(tmp_path: Path) -> None:
    # An unpinned on-disk .pine is a coverage gap, not a lie: WARN, exit-0.
    h = _write_pine(tmp_path, "strategies/a/pinned.pine", b"pinned\n")
    _write_pine(tmp_path, "strategies/a/unpinned.pine", b"new strategy\n")
    _write_manifest(tmp_path, [f"{h}  strategies/a/pinned.pine"])
    res = _run(tmp_path)
    assert res.ok, res.failures
    assert any(w.startswith("EXTRA ") and "unpinned" in w for w in res.warnings), res.warnings


def test_extra_does_not_mask_missing(tmp_path: Path) -> None:
    # EXTRA (warn) coexisting with MISSING (hard) must still hard-fail overall.
    _write_pine(tmp_path, "strategies/a/unpinned.pine", b"new\n")
    _write_manifest(tmp_path, ["0" * 64 + "  strategies/a/gone.pine"])
    res = _run(tmp_path)
    assert not res.ok
    assert any(f.startswith("MISSING ") for f in res.failures), res.failures
    assert any(w.startswith("EXTRA ") for w in res.warnings), res.warnings


def test_bare_clone_warn_skips(tmp_path: Path) -> None:
    # Manifest has entries but NO .pine on disk → clone/CI → warn, exit-0 semantics.
    _write_manifest(tmp_path, ["b" * 64 + "  strategies/a/strat.pine"])
    res = _run(tmp_path)
    assert res.ok, res.failures
    assert res.warnings


def test_malformed_line_hard_fails(tmp_path: Path) -> None:
    _write_pine(tmp_path, "strategies/a/strat.pine", b"x\n")
    _write_manifest(tmp_path, ["not-a-valid-manifest-line"])
    res = _run(tmp_path)
    assert not res.ok
    assert any(f.startswith("BAD_LINE ") for f in res.failures), res.failures


# --- PORT_MANIFEST.sha256 (port / venue-edition pins) ------------------------


def test_port_drift_mismatch_hard_fails(tmp_path: Path) -> None:
    # 2026-07-17 MYM regression: the venue edition re-authored on disk while
    # PORT_MANIFEST still pins the pre-rewrite hash → MISMATCH hard-fail.
    h_locked = _write_pine(tmp_path, "strategies/s/dj30.pine", b"locked\n")
    _write_pine(tmp_path, "strategies/s/dj30_mym.pine", b"re-authored edition\n")
    _write_manifest(tmp_path, [f"{h_locked}  strategies/s/dj30.pine"])
    _write_manifest(
        tmp_path,
        ["f" * 64 + "  strategies/s/dj30_mym.pine"],
        name="PORT_MANIFEST.sha256",
    )
    res = _run(tmp_path)
    assert not res.ok
    assert any(
        f.startswith("MISMATCH ") and "PORT_MANIFEST" in f and "mym" in f
        for f in res.failures
    ), res.failures


def test_port_missing_hard_fails_while_locked_set_intact(tmp_path: Path) -> None:
    # 2026-07-17 MNQ regression: a pinned venue edition gone from disk must
    # hard-fail even though every locked-manifest file is present and clean.
    h_locked = _write_pine(tmp_path, "strategies/n/nas.pine", b"locked\n")
    _write_manifest(tmp_path, [f"{h_locked}  strategies/n/nas.pine"])
    _write_manifest(
        tmp_path,
        ["e" * 64 + "  strategies/n/nas_mnq.pine"],
        name="PORT_MANIFEST.sha256",
    )
    res = _run(tmp_path)
    assert not res.ok
    assert any(
        f.startswith("MISSING ") and "PORT_MANIFEST" in f and "mnq" in f
        for f in res.failures
    ), res.failures


def test_port_pinned_file_is_not_extra(tmp_path: Path) -> None:
    # EXTRA is computed against the UNION of both manifests: a clean, port-pinned
    # edition must neither warn nor fail.
    h_locked = _write_pine(tmp_path, "strategies/s/dj30.pine", b"locked\n")
    h_port = _write_pine(tmp_path, "strategies/s/dj30_mym.pine", b"edition\n")
    _write_manifest(tmp_path, [f"{h_locked}  strategies/s/dj30.pine"])
    _write_manifest(
        tmp_path,
        [f"{h_port}  strategies/s/dj30_mym.pine"],
        name="PORT_MANIFEST.sha256",
    )
    res = _run(tmp_path)
    assert res.ok, res.failures
    assert not res.warnings, res.warnings


def test_bare_clone_with_port_entries_warn_skips(tmp_path: Path) -> None:
    # Union presence gate: entries in BOTH manifests, zero .pine on disk →
    # clone/CI → warn-only, exit 0.
    _write_manifest(tmp_path, ["b" * 64 + "  strategies/a/strat.pine"])
    _write_manifest(
        tmp_path,
        ["c" * 64 + "  strategies/a/strat_mym.pine"],
        name="PORT_MANIFEST.sha256",
    )
    res = _run(tmp_path)
    assert res.ok, res.failures
    assert res.warnings


def test_cross_manifest_conflict_hard_fails_without_pine(tmp_path: Path) -> None:
    # Same path pinned under two different digests cannot both be true — fails
    # even in a bare clone (no bytes needed to detect the contradiction).
    _write_manifest(tmp_path, ["a" * 64 + "  strategies/a/strat.pine"])
    _write_manifest(
        tmp_path,
        ["b" * 64 + "  strategies/a/strat.pine"],
        name="PORT_MANIFEST.sha256",
    )
    res = _run(tmp_path)
    assert not res.ok
    assert any(f.startswith("CROSS_MANIFEST_CONFLICT ") for f in res.failures), res.failures


# --- linked-worktree MISSING relaxation (2026-08-11) ------------------------


def test_worktree_missing_warns_not_fails(tmp_path: Path) -> None:
    # Same M-9 partial-presence shape as test_m9_partial_presence_missing_hard_fails,
    # but explicitly told it's a linked worktree: MISSING must warn, not fail —
    # gitignored bytes the main checkout has are an expected absence there.
    h_live = _write_pine(tmp_path, "strategies/a/live.pine", b"live\n")
    _write_manifest(
        tmp_path,
        [
            f"{h_live}  strategies/a/live.pine",
            "0" * 64 + "  archive/strategies/striker/striker_dj30_v4.4.pine",
        ],
    )
    res = _run(tmp_path, is_linked_worktree=True)
    assert res.ok, res.failures
    assert any(
        w.startswith("MISSING ") and "v4.4" in w and "linked worktree" in w
        for w in res.warnings
    ), res.warnings


def test_worktree_mismatch_still_hard_fails(tmp_path: Path) -> None:
    # A file that IS present with the WRONG hash is real drift in any checkout —
    # the linked-worktree relaxation must not touch MISMATCH.
    _write_pine(tmp_path, "strategies/a/strat.pine", b"real bytes\n")
    _write_manifest(tmp_path, ["a" * 64 + "  strategies/a/strat.pine"])
    res = _run(tmp_path, is_linked_worktree=True)
    assert not res.ok
    assert any(f.startswith("MISMATCH ") for f in res.failures), res.failures


def test_main_checkout_missing_still_hard_fails(tmp_path: Path) -> None:
    # Explicit False must reproduce the pre-existing strict behavior exactly —
    # this is the regression guard for the M-9 case the gate exists for.
    h_live = _write_pine(tmp_path, "strategies/a/live.pine", b"live\n")
    _write_manifest(
        tmp_path,
        [
            f"{h_live}  strategies/a/live.pine",
            "0" * 64 + "  archive/strategies/striker/striker_dj30_v4.4.pine",
        ],
    )
    res = _run(tmp_path, is_linked_worktree=False)
    assert not res.ok
    assert any(f.startswith("MISSING ") and "v4.4" in f for f in res.failures), res.failures


def test_is_linked_worktree_detects_real_git_worktree(tmp_path: Path) -> None:
    # End-to-end: an actual `git worktree add` must auto-detect True, and the
    # main checkout it was added from must auto-detect False — not just the
    # injected-boolean path the tests above exercise.
    main = tmp_path / "main"
    main.mkdir()
    run = lambda *args: subprocess.run(  # noqa: E731
        ["git", *args], cwd=main, capture_output=True, text=True, check=True
    )
    subprocess.run(["git", "init", "-q"], cwd=main, check=True)
    run("config", "user.email", "test@example.com")
    run("config", "user.name", "Test")
    (main / "README.md").write_text("x\n", encoding="utf-8")
    run("add", "README.md")
    run("commit", "-q", "-m", "initial")

    assert cpm._is_linked_worktree(main) is False

    linked = tmp_path / "linked"
    run("worktree", "add", "-q", str(linked), "-b", "wt-branch")

    assert cpm._is_linked_worktree(linked) is True


def test_is_linked_worktree_defaults_false_outside_git(tmp_path: Path) -> None:
    # No .git anywhere above tmp_path — must not raise, must default to the
    # strict main-checkout behavior.
    assert cpm._is_linked_worktree(tmp_path) is False


def test_missing_port_manifest_hard_fails(tmp_path: Path) -> None:
    # Both manifests are tracked files; one absent from disk is drift, not an
    # environment artifact — MISSING_MANIFEST regardless of Pine presence.
    _write_manifest(tmp_path, ["b" * 64 + "  strategies/a/strat.pine"])
    res = cpm.check(
        manifest_paths=[
            tmp_path / "strategies" / "MANIFEST.sha256",
            tmp_path / "strategies" / "PORT_MANIFEST.sha256",
        ],
        repo_root=tmp_path,
        pine_roots=[tmp_path / "strategies"],
    )
    assert not res.ok
    assert any(f.startswith("MISSING_MANIFEST ") for f in res.failures), res.failures
