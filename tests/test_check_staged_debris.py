"""staged-debris gate -- banned local-only roots, force-added ignored files and oversize blobs."""
from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "check_staged_debris.py"
_SPEC = importlib.util.spec_from_file_location("check_staged_debris", SCRIPT)
csd = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = csd
_SPEC.loader.exec_module(csd)


def test_path_finding_bans_exactly_the_local_only_roots():
    banned = [
        "recovery/pkt/evidence.md",   # local-only evidence-packet root
        "tmp/session.log",            # main-checkout scratch root
        "tmp",                        # bare root stem; guard is stem-based
        "tmp-pr409-listener/f.py",    # root tmp-* directory (2026-09-24 incident)
        "tmp-phase2-.md",             # root tmp-* file (2026-09-24 incident)
        # Case variants: on a case-insensitive checkout (Windows,
        # core.ignorecase=true) these name the same on-disk root.
        "Recovery/pkt/evidence.md",
        "TMP/session.log",
        "Tmp-phase2-.md",
    ]
    for path in banned:
        assert csd.path_finding(path), path
    allowed = [
        "docs/x.md",                  # normal tree
        "tmp_screenshots/s.png",      # different name (underscore): ignore rule, not this gate
        ".zcodeignore",               # ignored by .gitignore; not in this gate's banned set
        "sub/tmp/x",                  # nested tmp dir: not the root-anchored incident class
        "sub/recovery/x",             # nested recovery dir: same
        "tmpp/x",                     # prefix collision guard
    ]
    for path in allowed:
        assert csd.path_finding(path) is None, path


def test_size_finding_threshold_and_allowlist():
    assert csd.size_finding("docs/big.bin", csd.MAX_STAGED_FILE_BYTES) is None
    assert csd.size_finding("docs/big.bin", csd.MAX_STAGED_FILE_BYTES + 1)
    assert csd.size_finding("docs/big.bin", None) is None
    # Research-results corpus and its archived form: the one legitimate
    # >1 MB shape (largest tracked file: lab/analysis/.../results.json, 988,529 B),
    # capped at ALLOWLISTED_MAX_STAGED_FILE_BYTES since the 2026-09-26 ruling.
    cap = csd.ALLOWLISTED_MAX_STAGED_FILE_BYTES
    assert cap == 2_000_000
    for root in ("lab/analysis/", "lab/archive/"):
        assert csd.size_finding(root + "big.json", cap) is None
        assert csd.size_finding(root + "big.json", cap + 1)
        assert csd.size_finding(root + "big.json", 5_000_000)  # a multi-year bar panel
    assert csd.size_finding("lab/other/big.json", 1_500_000)  # not allowlisted
    assert csd.size_finding("core/big.json", 1_500_000)
    # Case-sensitive prefix: a case variant is not allowlisted and gets the 1 MB cap.
    assert "single-file limit" in csd.size_finding("Lab/Analysis/big.json", 1_500_000)


def test_staged_paths_parses_name_status_z(monkeypatch):
    stream = (
        b"A\0a.py\0M\0m.py\0T\0t.py\0"
        b"R100\0old.py\0renamed.py\0C75\0src.py\0copy.py\0"
    )
    monkeypatch.setattr(csd, "_git", lambda root, *args: stream)
    # Rename/copy are judged on their destination side only.
    assert csd.staged_paths(Path(".")) == [
        "a.py", "m.py", "t.py", "renamed.py", "copy.py",
    ]


def test_staged_paths_returns_none_when_head_unborn(monkeypatch):
    def boom(root, *args):
        raise subprocess.CalledProcessError(128, "git")
    monkeypatch.setattr(csd, "_git", boom)
    assert csd.staged_paths(Path(".")) is None


def test_tree_entries_parses_ls_tree_z(monkeypatch):
    stream = (
        b"100644 blob 1111111111111111111111111111111111111111 1234\tdocs/a.md\0"
        b"160000 commit 2222222222222222222222222222222222222222 -\tvendored\0"
        b"100644 blob 3333333333333333333333333333333333333333\0"  # no size column: skipped
    )
    monkeypatch.setattr(csd, "_git", lambda root, *args: stream)
    assert csd.tree_entries(Path(".")) == [
        ("docs/a.md", 1234),
        ("vendored", None),  # gitlink: no blob size to judge
    ]


def _git(root: Path, *args: str) -> None:
    subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True, text=True
    )


def _write(root: Path, relpath: str, data: str | bytes) -> None:
    target = root / relpath
    target.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, bytes):
        target.write_bytes(data)
    else:
        target.write_text(data, encoding="utf-8")


def _run_gate(root: Path, env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root)],
        capture_output=True,
        text=True,
        env=env,
    )


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "config", "user.email", "gate@example.invalid")
    _git(tmp_path, "config", "user.name", "Gate Test")
    (tmp_path / "README.md").write_text("seed\n", encoding="utf-8")
    _git(tmp_path, "add", "README.md")
    _git(tmp_path, "commit", "-q", "-m", "seed")
    return tmp_path


def test_rejects_banned_roots_when_staged(repo: Path):
    _write(repo, "recovery/pkt.md", "evidence\n")
    _write(repo, "tmp/session.log", "scratch\n")
    _write(repo, "tmp-phase2-.md", "debris\n")
    _git(repo, "add", "-A")
    result = _run_gate(repo)
    assert result.returncode == 1
    for path in ("recovery/pkt.md", "tmp/session.log", "tmp-phase2-.md"):
        assert path in result.stdout, result.stdout


def test_clean_small_stage_passes(repo: Path):
    (repo / "docs.md").write_text("fine\n", encoding="utf-8")
    _git(repo, "add", "docs.md")
    result = _run_gate(repo)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "staged vs HEAD" in result.stdout


def test_rejects_oversize_outside_allowlist(repo: Path):
    (repo / "big.bin").write_bytes(b"x" * (csd.MAX_STAGED_FILE_BYTES + 1))
    _git(repo, "add", "big.bin")
    result = _run_gate(repo)
    assert result.returncode == 1
    assert "big.bin" in result.stdout
    assert "single-file limit" in result.stdout


def test_allows_research_results_up_to_the_allowlisted_ceiling(repo: Path):
    _write(repo, "lab/analysis/results.json", b"x" * 2_000_000)
    _git(repo, "add", "-A")
    result = _run_gate(repo)
    assert result.returncode == 0, result.stdout + result.stderr


def test_rejects_research_results_over_the_allowlisted_ceiling(repo: Path):
    """2026-09-26 ruling: allowlisted roots are capped at 2,000,000 B, not unbounded."""
    _write(repo, "lab/analysis/results.json", b"x" * 2_000_001)
    _git(repo, "add", "-A")
    result = _run_gate(repo)
    assert result.returncode == 1
    assert (
        "lab/analysis/results.json: 2000001 B exceeds the 2000000 B ceiling for "
        "allowlisted roots" in result.stdout
    ), result.stdout
    # A size finding is not told it sits in a local-only root (the footer bug).
    assert "local-only" not in result.stdout, result.stdout
    assert "1 oversize blob(s)" in result.stdout, result.stdout


def test_case_variant_of_allowlisted_root_gets_the_tighter_cap(repo: Path):
    _write(repo, "Lab/Analysis/results.json", b"x" * (csd.MAX_STAGED_FILE_BYTES + 1))
    _git(repo, "add", "-A")
    result = _run_gate(repo)
    assert result.returncode == 1
    assert "single-file limit" in result.stdout, result.stdout


def test_banned_root_footer_still_names_local_only_roots(repo: Path):
    _write(repo, "recovery/pkt.md", "evidence\n")
    _git(repo, "add", "-A")
    result = _run_gate(repo)
    assert result.returncode == 1
    assert "local-only" in result.stdout
    assert "oversize" not in result.stdout


def _ignore(repo: Path, rules: str) -> None:
    _write(repo, ".gitignore", rules)
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-q", "-m", "ignore rules")


def test_rejects_force_added_ignored_file(repo: Path):
    """`git add -f` past an ignore rule is a finding (2026-09-26 ruling B)."""
    _ignore(repo, "lab/analysis/**/inputs/*.csv\n")
    _write(repo, "lab/analysis/study/inputs/bars.csv", "t,o,h,l,c\n")
    _git(repo, "add", "-f", "lab/analysis/study/inputs/bars.csv")
    result = _run_gate(repo)
    assert result.returncode == 1
    assert (
        "lab/analysis/study/inputs/bars.csv: force-added ignored file" in result.stdout
    ), result.stdout
    assert "1 force-added ignored file(s)" in result.stdout, result.stdout
    assert "local-only" not in result.stdout, result.stdout


def test_force_add_check_covers_renames_into_ignored_paths(repo: Path):
    _ignore(repo, "*.csv\n")
    _write(repo, "data.txt", "a,b\n" * 50)
    _git(repo, "add", "data.txt")
    _git(repo, "commit", "-q", "-m", "data")
    _git(repo, "mv", "data.txt", "data.csv")
    result = _run_gate(repo)
    assert result.returncode == 1
    assert "data.csv: force-added ignored file" in result.stdout, result.stdout


GRANDFATHERED = "tests/fixtures/c1_image_validation/lifecycle_state.json"


def test_grandfathered_constant_names_exactly_the_two_known_files():
    """Codex P1 4111056549: the tracked-despite-ignore exemption is a named,
    closed list, not a HEAD-membership test."""
    assert csd.TRACKED_IGNORED_GRANDFATHERED == frozenset(
        {
            "lab/pine/mnq_mym_mechanism_diagnostic_v0_1.pine",
            "tests/fixtures/c1_image_validation/lifecycle_state.json",
        }
    )


def test_grandfathered_tracked_ignored_file_is_not_flagged(repo: Path):
    """A grandfathered file tracked despite an ignore rule is never flagged."""
    _write(repo, GRANDFATHERED, "{}\n")
    _git(repo, "add", GRANDFATHERED)
    _git(repo, "commit", "-q", "-m", "fixture tracked before the rule")
    _ignore(repo, "lifecycle_state.json\n")
    # Nothing staged: HEAD-tree mode.
    result = _run_gate(repo)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "HEAD tree" in result.stdout
    # Modifying and re-staging it: still not flagged.
    _write(repo, GRANDFATHERED, '{"k": 1}\n')
    _git(repo, "add", GRANDFATHERED)
    result = _run_gate(repo)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "staged vs HEAD" in result.stdout


def test_head_tree_mode_flags_committed_ignored_file_anywhere(repo: Path):
    """Codex P1 4111056549: CI checks ALL HEAD paths, not just lab/analysis/ and
    lab/archive/ -- a committed .env or vendor CSV elsewhere fails."""
    _ignore(repo, ".env\n*.csv\n")
    _write(repo, ".env", "TOKEN=x\n")
    _write(repo, "core/data/bars.csv", "t,o,h,l,c\n")
    _git(repo, "add", "-f", ".env", "core/data/bars.csv")
    _git(repo, "commit", "-q", "--no-verify", "-m", "force add")
    result = _run_gate(repo)
    assert result.returncode == 1, result.stdout
    assert "HEAD tree" in result.stdout
    assert ".env: force-added ignored file" in result.stdout, result.stdout
    assert "core/data/bars.csv: force-added ignored file" in result.stdout, result.stdout


def test_head_tree_mode_flags_non_grandfathered_tracked_then_ignored_file(repo: Path):
    """Tracked before the rule is no exemption unless grandfathered by name."""
    _write(repo, "lifecycle_state.json", "{}\n")
    _git(repo, "add", "lifecycle_state.json")
    _git(repo, "commit", "-q", "-m", "tracked before the rule")
    _ignore(repo, "lifecycle_state.json\n")
    result = _run_gate(repo)
    assert result.returncode == 1, result.stdout
    assert "lifecycle_state.json: force-added ignored file" in result.stdout


def test_staged_modify_of_non_grandfathered_tracked_ignored_file_blocks(repo: Path):
    _write(repo, "lifecycle_state.json", "{}\n")
    _git(repo, "add", "lifecycle_state.json")
    _git(repo, "commit", "-q", "-m", "tracked before the rule")
    _ignore(repo, "lifecycle_state.json\n")
    _write(repo, "lifecycle_state.json", '{"k": 1}\n')
    _git(repo, "add", "lifecycle_state.json")
    result = _run_gate(repo)
    assert result.returncode == 1, result.stdout
    assert "staged vs HEAD" in result.stdout
    assert "lifecycle_state.json: force-added ignored file" in result.stdout


def test_staged_gitignore_rule_that_ignores_a_tracked_file_blocks(repo: Path):
    """Staging a rule that newly ignores an already-tracked file is judged at
    commit time, not first in CI."""
    _write(repo, "data/bars.csv", "t,o,h,l,c\n")
    _git(repo, "add", "data/bars.csv")
    _git(repo, "commit", "-q", "-m", "data")
    _write(repo, ".gitignore", "*.csv\n")
    _git(repo, "add", ".gitignore")
    result = _run_gate(repo)
    assert result.returncode == 1, result.stdout
    assert "data/bars.csv: force-added ignored file" in result.stdout


def test_unstaged_gitignore_edit_cannot_hide_a_staged_force_add(repo: Path):
    """Codex P2 4111056555: rules come from the index, not the working tree."""
    _ignore(repo, "*.csv\n")
    _write(repo, "bars.csv", "t,o,h,l,c\n")
    _git(repo, "add", "-f", "bars.csv")
    _write(repo, ".gitignore", "# rule removed in the working tree only\n")
    result = _run_gate(repo)
    assert result.returncode == 1, result.stdout
    assert "bars.csv: force-added ignored file" in result.stdout


def test_unstaged_nested_gitignore_deletion_cannot_hide_a_force_add(repo: Path):
    _write(repo, "lab/x/.gitignore", "*.csv\n")
    _git(repo, "add", "lab/x/.gitignore")
    _git(repo, "commit", "-q", "-m", "nested rule")
    _write(repo, "lab/x/bars.csv", "t,o,h,l,c\n")
    _git(repo, "add", "-f", "lab/x/bars.csv")
    (repo / "lab/x/.gitignore").unlink()
    result = _run_gate(repo)
    assert result.returncode == 1, result.stdout
    assert "lab/x/bars.csv: force-added ignored file" in result.stdout


def test_unstaged_gitignore_rule_does_not_flag_a_normal_add(repo: Path):
    """The converse: a working-tree-only rule is not a committed rule."""
    _write(repo, "notes.txt", "fine\n")
    _git(repo, "add", "notes.txt")
    _write(repo, ".gitignore", "*.txt\n")  # unstaged
    result = _run_gate(repo)
    assert result.returncode == 0, result.stdout + result.stderr


def test_head_tree_mode_uses_committed_rules_not_working_tree(repo: Path):
    _ignore(repo, "*.csv\n")
    _write(repo, "bars.csv", "t,o,h,l,c\n")
    _git(repo, "add", "-f", "bars.csv")
    _git(repo, "commit", "-q", "--no-verify", "-m", "force add")
    _write(repo, ".gitignore", "# rule removed in the working tree only\n")
    # .gitignore is modified but unstaged: nothing staged -> HEAD-tree mode.
    result = _run_gate(repo)
    assert result.returncode == 1, result.stdout
    assert "HEAD tree" in result.stdout
    assert "bars.csv: force-added ignored file" in result.stdout


@pytest.mark.parametrize("scope", ["info-exclude", "local-config", "global-config"])
def test_personal_ignore_rules_are_not_repository_rules(
    repo: Path, tmp_path_factory, scope: str
):
    """Codex P2 4111056558: .git/info/exclude and a local or global
    core.excludesFile never make a file a finding -- only repository-owned
    .gitignore rules count, so the verdict does not depend on the clone."""
    home = tmp_path_factory.mktemp("home")
    excludes = home / "excludes"
    excludes.write_text("personal.txt\n", encoding="utf-8")
    global_config = home / "gitconfig"
    global_config.write_text("", encoding="utf-8")
    if scope == "info-exclude":
        info = repo / ".git" / "info"
        info.mkdir(exist_ok=True)
        (info / "exclude").write_text("personal.txt\n", encoding="utf-8")
    elif scope == "local-config":
        _git(repo, "config", "core.excludesFile", excludes.as_posix())
    else:
        global_config.write_text(
            f"[core]\n\texcludesFile = {excludes.as_posix()}\n", encoding="utf-8"
        )
    env = {**os.environ, "GIT_CONFIG_GLOBAL": str(global_config)}
    _write(repo, "personal.txt", "x\n")
    # Sanity: git itself treats the file as ignored under this personal rule.
    probe = subprocess.run(
        ["git", "check-ignore", "-q", "personal.txt"], cwd=repo, env=env, check=False
    )
    assert probe.returncode == 0, scope
    _git(repo, "add", "-f", "personal.txt")
    # Staged mode.
    result = _run_gate(repo, env=env)
    assert result.returncode == 0, result.stdout + result.stderr
    # HEAD-tree mode.
    _git(repo, "commit", "-q", "--no-verify", "-m", "personally ignored file")
    result = _run_gate(repo, env=env)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "HEAD tree" in result.stdout


def test_head_tree_mode_flags_committed_force_add_under_allowlisted_root(repo: Path):
    """CI's clean checkout catches a force-added vendor file in lab/analysis/."""
    _ignore(repo, "lab/analysis/**/inputs/*.csv\n")
    _write(repo, "lab/analysis/study/inputs/bars.csv", "t,o,h,l,c\n")
    _git(repo, "add", "-f", "lab/analysis/study/inputs/bars.csv")
    _git(repo, "commit", "-q", "--no-verify", "-m", "force add")
    result = _run_gate(repo)
    assert result.returncode == 1
    assert "HEAD tree" in result.stdout
    assert "lab/analysis/study/inputs/bars.csv: force-added ignored file" in result.stdout


def test_head_tree_mode_catches_committed_debris(repo: Path):
    _write(repo, "recovery/pkt.md", "evidence\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "blanket add")
    # Nothing staged now: the gate falls back to the HEAD tree, which is what
    # CI's `--tier check` sees on a branch that already committed debris.
    result = _run_gate(repo)
    assert result.returncode == 1
    assert "recovery/pkt.md" in result.stdout
    assert "HEAD tree" in result.stdout


def test_deletion_only_cleanup_of_committed_debris_passes(repo: Path):
    """Un-indexing committed debris is a cleanup, never a finding."""
    # Codex P1 on PR #493: a stage holding only deletions must be judged as a
    # staged change, not mistaken for "nothing staged" and routed to the HEAD
    # tree -- which still holds the very files being removed.
    _write(repo, "recovery/pkt.md", "evidence\n")
    _write(repo, "tmp-phase2-.md", "debris\n")
    _write(repo, "big.bin", b"x" * (csd.MAX_STAGED_FILE_BYTES + 1))
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "blanket add")
    _git(repo, "rm", "-q", "-r", "--cached", "recovery", "tmp-phase2-.md", "big.bin")
    result = _run_gate(repo)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "staged vs HEAD" in result.stdout


def test_git_mv_out_of_banned_root_passes(repo: Path):
    """A rename away from a banned root is judged on its clean destination."""
    _write(repo, "recovery/a.md", "evidence worth keeping\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "blanket add")
    _git(repo, "mv", "recovery/a.md", "a.md")
    result = _run_gate(repo)
    assert result.returncode == 0, result.stdout + result.stderr


def test_git_mv_into_banned_root_blocks(repo: Path):
    """A rename into a banned root is judged on its banned destination."""
    _write(repo, "docs/a.md", "doc\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "doc")
    (repo / "recovery").mkdir()
    _git(repo, "mv", "docs/a.md", "recovery/a.md")
    result = _run_gate(repo)
    assert result.returncode == 1
    assert "recovery/a.md" in result.stdout


def test_modifying_tracked_oversize_file_blocks(repo: Path):
    """Re-staging an already-tracked oversize blob is still a finding."""
    _write(repo, "big.bin", b"x" * (csd.MAX_STAGED_FILE_BYTES + 1))
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "pre-existing large file")
    _write(repo, "big.bin", b"y" * (csd.MAX_STAGED_FILE_BYTES + 1))
    _git(repo, "add", "big.bin")
    result = _run_gate(repo)
    assert result.returncode == 1
    assert "big.bin" in result.stdout
    assert "single-file limit" in result.stdout
