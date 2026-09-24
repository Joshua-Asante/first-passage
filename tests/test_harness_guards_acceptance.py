"""Acceptance suite for the harness-guard hardening card (F29, A1-A7, B1-B3).

Card: docs/briefs/handoffs/2026-09-23-harness-guards-hardening.md. Coordinator-authored
and frozen by SHA-256 in that card: the worker makes these pass without editing this
file. `classify()` and `decide()` are the pure functions the guards already expose;
the tests call them directly, so they hold whatever the hooks' `main()` emits for an
allow (card 1's D15 makes that silent).
"""
import json
import re
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from scripts import guard_open_verification_record as write_guard
from scripts import guard_shell_command as shell_guard
from scripts.record_verification import RunRecord

ROOT = Path(__file__).resolve().parents[1]


def permission(cmd):
    return shell_guard.classify(cmd)[0]


# --- A1: every way git skips hooks or signing asks ----------------------------

@pytest.mark.parametrize("cmd", [
    "git commit --no-verify -m wip",                   # existing
    "git commit -n -m wip",                            # -n is commit's --no-verify
    "git commit -nm wip",
    "git commit -anm wip",
    "git commit --no-verif -m x",                      # git accepts unique long-option prefixes
    "git commit --no-gpg -m x",
    "git -c core.hooksPath=/nonexistent commit -m z",  # hooks redirected away
    "git -c core.hookspath=x commit -m z",             # config keys are case-insensitive
    "git -C sub commit --no-verify -m x",
    "git merge --no-verify topic",
    "git push --no-verify origin feat",
    "cd sub && git commit -n -m x",
])
def test_a1_hook_and_signing_bypass_asks(cmd):
    perm, agent_msg, user_msg = shell_guard.classify(cmd)
    assert perm == "ask", cmd
    assert "standing path" in agent_msg and user_msg


@pytest.mark.parametrize("cmd", [
    "git push -n origin feat",       # push -n is --dry-run, not a bypass
    "git merge -n topic",            # merge -n is --no-stat
    "git commit -m 'fix -n handling'",
])
def test_a1_short_n_is_a_bypass_only_for_commit(cmd):
    assert permission(cmd) == "allow", cmd


# --- A2-A7: destructive commands in every spelling git and rm accept ----------

@pytest.mark.parametrize("cmd", [
    # existing cases
    "git reset --hard origin/main", "git clean -fd", "git clean -xdf", "git checkout -- .",
    "git push --force origin main", "git push origin main -f", "git branch -D feature", "rm -rf build/",
    # A2: global options before the subcommand
    "git -C sub reset --hard", "git --no-pager reset --hard", "git -C x clean -fdx",
    "git -c color.ui=never reset --hard",
    # A3: flag order and abbreviation
    "git reset -q --hard", "git reset HEAD~1 --hard", "git reset --har",
    "git clean -d -f", "git clean --force", "git clean -d --force",
    # A4: checkout/restore/switch that discard work
    "git checkout HEAD -- .", "git checkout main -- file.py", "git checkout -f",
    "git restore .", "git switch -f other", "git switch --discard-changes other",
    # A5: force-push forms
    "git push origin +main", "git push origin +HEAD:main", "git push -uf origin x", "git push -fu origin x",
    # A6: branch force-delete forms
    "git branch --delete --force x", "git branch -d -f x", "git branch -fD x", "git branch -Df x",
    # A7: recursive force rm forms
    "rm -fr d", "rm -r -f d", "rm -Rf d", "rm --recursive --force d", "/bin/rm -rf d",
    # wrappers and compound commands
    "sudo rm -rf d", "env X=1 git reset --hard", 'bash -c "git reset --hard"',
    "git fetch && git reset --hard origin/main", "(cd a && git clean -fd)", "true; rm -rf d",
])
def test_a2_a7_destructive_commands_ask(cmd):
    perm, agent_msg, user_msg = shell_guard.classify(cmd)
    assert perm == "ask", cmd
    assert "git status" in agent_msg and user_msg


@pytest.mark.parametrize("cmd", [
    "git push --force-with-lease origin my-branch",   # the guard's own recommended path
    "git push --force-with-lease=main origin main",
    "git push origin my-branch",
    "git restore --staged file.py",                  # unstages only; the work tree is untouched
    "git reset --soft HEAD~1",
    "git reset HEAD file.py",
    "rm build/artifact.o",
    "git branch -d merged-branch",
    "git clean -n",                                  # dry run
])
def test_non_destructive_neighbours_are_allowed(cmd):
    assert permission(cmd) == "allow", cmd


# --- F29: destructive text that is only data is allowed --------------------------

RMRF, HARD, NOV = "rm " + "-rf", "git reset " + "--hard", "--no-" + "verify"


@pytest.mark.parametrize("cmd", [
    f"cat > probe.py <<'EOF'\ncases = ['{RMRF} /tmp/x', '{HARD}']\nEOF",
    f"cat <<EOF > notes.md\nnever run {NOV}\nEOF",
    f"grep -rn '{HARD}' scripts/",
    f"rg -n '{NOV}|{RMRF}' .claude",
    f"grep -- '{NOV}' AGENTS.md",
    f"git log --grep='{HARD}'",
    f'git commit -m "docs: never use {NOV}"',
    f"git commit -m \"$(cat <<'EOF'\ndocs: {RMRF} is forbidden\nEOF\n)\"",
    f"echo '{RMRF} is dangerous'",
    f"python3 -c \"print('{HARD}')\"",
    f"printf '%s\\n' '{NOV}'",
])
def test_f29_destructive_text_that_is_only_data_is_allowed(cmd):
    assert permission(cmd) == "allow", cmd


def test_f29_unparsable_commands_fall_back_to_asking():
    assert permission(f'echo "unterminated; {RMRF} d') == "ask"
    assert permission("echo 'unterminated") == "allow"


# --- B1-B3: the open-record write guard --------------------------------------------

def _checkout(tmp_path):
    root = tmp_path / "repo"
    (root / ".git").mkdir(parents=True)
    (root / "docs").mkdir()
    return root


def _record(root, folder, **fields):
    path = root / folder
    path.mkdir(parents=True)
    data = {"status": "running", "started_at": datetime.now(timezone.utc).isoformat(),
            "finished_at": None, "before": None}
    data.update(fields)
    (path / "record.json").write_text(json.dumps(data), encoding="utf-8")


def test_b1_docker_verification_records_lock_the_tree(tmp_path):
    root = _checkout(tmp_path)
    _record(root, ".cache/fp-docker-verification/d1")
    assert write_guard.decide(str(root / "docs" / "x.md"))[0] == "deny"


def test_b1_records_under_cache_are_still_exempt_targets(tmp_path):
    root = _checkout(tmp_path)
    _record(root, ".cache/fp-docker-verification/d1")
    assert write_guard.decide(str(root / ".cache" / "notes.md"))[0] == "allow"


@pytest.mark.parametrize("folder", [".cache/fp-verification/r1", ".cache/fp-docker-verification/d1"])
def test_b2_a_measured_record_that_has_not_started_its_command_locks_the_tree(tmp_path, folder):
    root = _checkout(tmp_path)
    _record(root, folder, status="not_started", before={"fingerprint": "abc"})
    assert write_guard.decide(str(root / "docs" / "x.md"))[0] == "deny"


def test_b2_a_record_that_never_measured_or_has_finished_does_not_lock(tmp_path):
    root = _checkout(tmp_path)
    _record(root, ".cache/fp-verification/r1", status="not_started", before=None)
    _record(root, ".cache/fp-verification/r2", status="not_started", before={"fingerprint": "abc"},
            finished_at=datetime.now(timezone.utc).isoformat())
    _record(root, ".cache/fp-verification/r3", status="completed", before={"fingerprint": "abc"},
            finished_at=datetime.now(timezone.utc).isoformat())
    assert write_guard.decide(str(root / "docs" / "x.md"))[0] == "allow"


def test_b2_stale_measured_records_do_not_lock_forever(tmp_path):
    root = _checkout(tmp_path)
    old = datetime.now(timezone.utc) - timedelta(seconds=write_guard.STALE_AFTER_SECONDS + 60)
    _record(root, ".cache/fp-verification/r1", status="not_started", before={"fingerprint": "abc"},
            started_at=old.isoformat())
    assert write_guard.decide(str(root / "docs" / "x.md"))[0] == "allow"


def test_b2_the_real_recorder_locks_the_tree_from_begin(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    git = ["git", "-C", str(root), "-c", "user.name=t", "-c", "user.email=t@t"]
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    (root / ".gitignore").write_text(".cache/\n", encoding="utf-8")
    (root / "a.txt").write_text("a\n", encoding="utf-8")
    subprocess.run([*git, "add", "-A"], check=True)
    subprocess.run([*git, "commit", "-q", "-m", "init"], check=True)
    record = RunRecord(root, root / ".cache" / "fp-verification" / "r1", ["probe"], allow_ignored=True)
    assert write_guard.decide(str(root / "a.txt"))[0] == "allow"      # nothing measured yet
    record.begin()
    assert write_guard.decide(str(root / "a.txt"))[0] == "deny"       # the before snapshot is taken


def test_b3_notebook_edits_are_guarded(tmp_path, monkeypatch, capsys):
    root = _checkout(tmp_path)
    _record(root, ".cache/fp-verification/r1")
    payload = {"tool_name": "NotebookEdit", "tool_input": {"notebook_path": str(root / "docs" / "n.ipynb")}}
    monkeypatch.setattr("sys.stdin", __import__("io").StringIO(json.dumps(payload)))
    assert write_guard.main() == 0
    assert json.loads(capsys.readouterr().out)["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_b3_settings_route_notebook_edits_to_the_write_guard():
    settings = json.loads((ROOT / ".claude/settings.json").read_text(encoding="utf-8"))
    matchers = [entry.get("matcher", "") for entry in settings["hooks"]["PreToolUse"]
                if any("guard_open_verification_record.py" in h.get("command", "")
                       for h in entry.get("hooks", []))]
    for name in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
        assert any(re.fullmatch(m, name) for m in matchers), name
    assert not any(re.fullmatch(m, "Bash") for m in matchers)
