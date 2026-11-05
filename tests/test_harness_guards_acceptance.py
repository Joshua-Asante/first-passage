"""Acceptance suite for the shell-command guard (F29, A1-A7).

`classify()` is the pure function the guard exposes; the tests call it directly.
The B1-B3 open-record write-guard cases went with that guard in the 2026-11
governance cut.
"""
import pytest

from scripts import guard_shell_command as shell_guard


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
