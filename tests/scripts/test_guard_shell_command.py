"""Regression tests for scripts/guard_shell_command.py.

The guard was ported from `.cursor/hooks/before_shell.py` when the Cursor
harness was retired (`docs/adr/2026-07-14-cc-cursor-surface-allocation.md`,
Revision 2026-09-15). These tests pin the *logic* independently of any harness
wiring, so the discipline stays verifiable whether or not the operator elects to
register the PreToolUse hook. Retiring the Cursor carrier must not quietly
retire the rule it enforced.
"""
from __future__ import annotations

import importlib.util
import io
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
GUARD = REPO / "scripts" / "guard_shell_command.py"
# Destructive words are built by concatenation so no test source line is itself
# a command a shell guard would stop on.
RMRF, HARD, NOV, FORCE = "rm " + "-rf", "git reset " + "--hard", "--no-" + "verify", "--for" + "ce"


def _load():
    spec = importlib.util.spec_from_file_location("guard_shell_command", GUARD)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def mod():
    return _load()


@pytest.mark.parametrize(
    "cmd",
    [
        "git commit --no-verify -m wip",
        "git commit -m x --no-gpg-sign",
        "git commit --no-verify --no-gpg-sign -m both",
    ],
)
def test_hook_bypass_asks(mod, cmd):
    """--no-verify is the one rule no git hook can enforce on itself."""
    permission, agent_msg, user_msg = mod.classify(cmd)
    assert permission == "ask"
    assert "standing path" in agent_msg
    assert user_msg


@pytest.mark.parametrize(
    "cmd",
    [
        "git reset --hard origin/main",
        "git clean -fd",
        "git clean -xdf",
        "git checkout -- .",
        "git push --force origin main",
        "git push origin main -f",
        "git branch -D feature",
        "rm -rf build/",
    ],
)
def test_destructive_asks(mod, cmd):
    permission, agent_msg, user_msg = mod.classify(cmd)
    assert permission == "ask"
    assert "git status" in agent_msg
    assert user_msg


@pytest.mark.parametrize(
    "cmd",
    [
        "git status",
        "git commit -m 'ordinary commit'",
        "git push origin my-branch",
        "git push --force-with-lease origin my-branch",
        "pytest tests/ -x",
        "rm build/artifact.o",
        "",
    ],
)
def test_benign_allows(mod, cmd):
    """Force-with-lease and a plain rm must not be swept up as destructive."""
    permission, agent_msg, user_msg = mod.classify(cmd)
    assert permission == "allow"
    assert agent_msg == ""
    assert user_msg == ""


@pytest.mark.parametrize(
    "payload,expected",
    [
        ({"command": "git status"}, "git status"),
        ({"shell_command": "ls"}, "ls"),
        ({"cmd": "pwd"}, "pwd"),
        ({"tool_input": {"command": "git diff"}}, "git diff"),
        ({"tool_input": {}}, ""),
        ({}, ""),
        ("not-a-dict", ""),
    ],
)
def test_command_extraction_accepts_both_payload_shapes(mod, payload, expected):
    """Cursor's beforeShellExecution shape and Claude's PreToolUse shape."""
    assert mod.command_of(payload) == expected


def test_malformed_stdin_fails_open(mod, monkeypatch, capsys):
    """Fail-open is the contract: a parse error must never block a command.

    2026-09-23: fail-open no longer means emitting `allow` — a hook `allow`
    bypasses the operator's permission rules — so unparsable input now
    produces no output at all and defers to the normal permission flow.
    """
    monkeypatch.setattr(sys, "stdin", io.StringIO("{not json"))
    assert mod.main() == 0
    assert capsys.readouterr().out.strip() == ""


def test_end_to_end_ask_via_stdin(mod, monkeypatch, capsys):
    monkeypatch.setattr(
        sys, "stdin", io.StringIO(json.dumps({"tool_input": {"command": "rm -rf /tmp/x"}}))
    )
    assert mod.main() == 0
    out = json.loads(capsys.readouterr().out)
    block = out["hookSpecificOutput"]
    assert block["permissionDecision"] == "ask"
    assert block["permissionDecisionReason"]
    assert block["additionalContext"]


def test_emits_claude_not_cursor_decision_shape(mod, monkeypatch, capsys):
    """The whole hook is inert if it emits Cursor's contract.

    The first draft of this port carried `.cursor/hooks/before_shell.py`'s
    `{"permission", "agentMessage", "userMessage"}` shape over verbatim. Claude
    Code reads `hookSpecificOutput.permissionDecision`, so that draft would have
    been a silent no-op once wired. Adversarial review caught it before wiring;
    this test is what stops it coming back. It exercises a command that asks
    (`rm -rf`), because a benign command now produces no output at all (D15).
    """
    monkeypatch.setattr(
        sys, "stdin", io.StringIO(json.dumps({"tool_input": {"command": "rm -rf /tmp/x"}}))
    )
    assert mod.main() == 0
    out = json.loads(capsys.readouterr().out)
    assert set(out) == {"hookSpecificOutput"}, "top level must be hookSpecificOutput only"
    block = out["hookSpecificOutput"]
    assert block["hookEventName"] == "PreToolUse"
    assert block["permissionDecision"] in {"allow", "deny", "ask"}
    # Cursor's keys must not reappear at either level.
    for dead in ("permission", "agentMessage", "userMessage"):
        assert dead not in out
        assert dead not in block


def test_guard_is_actually_wired(mod):
    """An unwired gate nobody knows is unwired is a named failure class here.

    The guard was ported unwired, then registered at the operator's instruction.
    This pins that the registration exists and points at this script, so the
    discipline cannot be silently lost a second way.
    """
    settings = json.loads(
        (REPO / ".claude" / "settings.json").read_text(encoding="utf-8")
    )
    pre = settings.get("hooks", {}).get("PreToolUse", [])
    entries = [
        h.get("command", "")
        for group in pre
        if group.get("matcher") == "Bash"
        for h in group.get("hooks", [])
    ]
    assert any("guard_shell_command.py" in c for c in entries), (
        "guard_shell_command.py is not registered as a PreToolUse Bash hook"
    )


# --- 2026-09-23 card 2 (E1-E3): commands, not text -----------------------------
# The acceptance suite (tests/test_harness_guards_acceptance.py) pins the card's
# cases; these pin how the strict tokenizer reads the neighbouring spellings.

@pytest.mark.parametrize(
    "cmd",
    [
        # a flag after a command substitution stays in its command
        f"git commit -m \"$(cat <<'EOF'\nfix: it's (F29)\nEOF\n)\" {NOV}",
        f"git push origin \"$(git branch --show-current)\" {FORCE}",
        # substitutions anywhere in a double-quoted word run
        f"echo \"cleaning $({RMRF} build)\"",
        f"echo \"x `{RMRF} build` y\"",
        # runners whose arguments are a command
        f"find . -name '*.pyc' -exec {RMRF} {{}} +",
        f"ls | xargs -n1 {RMRF}",
        f"eval '{RMRF} d'",
        f"{{ {RMRF} d; }}",
        f"sudo -u root {RMRF} d",
        f"timeout -s KILL 5 {HARD}",
        f"nice -n 5 {RMRF} d",
        f"bash -ec '{HARD}'",
        f"X=1 bash -c 'Y=2 {HARD}'",
        f"cat <<< 'x'\n{RMRF} d",  # a here-string is not a heredoc
        # abbreviations git 2.43 accepts for the guarded long options
        "git clean --f", "git checkout --forc", "git restore --staged --w f",
        "git switch --disc x", "git branch --d --forc x", "rm --r --f d",
        # option values are not flags: -s takes "S", so this restores the work tree
        "git restore -sS f",
        "git checkout -fb x",
    ],
)
def test_strict_reading_still_asks(mod, cmd):
    """Spellings the shell or git would run as a destructive operation still ask."""
    assert mod.classify(cmd)[0] == "ask", cmd


@pytest.mark.parametrize(
    "cmd",
    [
        f"git commit -m \"$(cat <<'EOF'\ndon't {RMRF} (ever\nEOF\n)\"",
        f"gh pr create --body \"$(cat <<'EOF'\nNever `{RMRF}`; don't {NOV}.\nEOF\n)\"",
        f"echo 'x `{RMRF} build` y'",
        f"cat <<< '{RMRF} d'\necho ok",
        f"# {RMRF}\necho ok",
        f"git log --oneline | grep '{FORCE}'",
        "command -v rm",
        "git commit -mn",                 # -m with the message "n"
        "git commit -uno -m x",           # -u with the mode "no"
        "git commit -m x -- -n",          # after --, -n is a path
        "git -c core.editor=vim commit -m x",
        "git checkout -bfix",
        "git switch -c fix",
        "git restore --staged --no-worktree f",
        "git push -o +x origin main",     # a push option, not a refspec
        "git push --force-with-lease --force-if-includes origin x",
        "rm -r -- -f",                    # after --, -f is a path
    ],
)
def test_strict_reading_allows(mod, cmd):
    """Data, lookups and option values never read as a guarded command (F29)."""
    assert mod.classify(cmd)[0] == "allow", cmd


@pytest.mark.parametrize(
    "cmd",
    [
        "git commit -qn -m x",
        "git --config-env=core.hooksPath=HP commit -m x",
        "git -c core.hooksPath commit -m x",
        "git commit --no-g -m x",
        f"git rebase {NOV} main",
    ],
)
def test_strict_reading_finds_bypasses(mod, cmd):
    """Clusters, config options and abbreviations that skip hooks ask (E2)."""
    permission, agent_msg, _ = mod.classify(cmd)
    assert permission == "ask" and "standing path" in agent_msg, cmd


@pytest.mark.parametrize(
    "command,expected",
    [
        (f"cat > p.py <<'EOF'\nx = '{RMRF} /'\nEOF", None),
        ("git commit -n -m x", "ask"),
    ],
)
def test_hook_runs_as_a_script(command, expected):
    """The §4 live smoke, run the way Claude Code runs the hook (script path, stdin)."""
    result = subprocess.run(
        [sys.executable, str(GUARD)], input=json.dumps({"tool_input": {"command": command}}),
        capture_output=True, text=True, encoding="utf-8", cwd=REPO, check=False, timeout=30,
    )
    assert result.returncode == 0, result.stderr
    if expected is None:
        assert result.stdout == ""
    else:
        assert json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"] == expected


# --- 2026-09-23 card 2, judge round 1: spellings the first strict read missed --
BYPASS, NCOMMIT = f"git commit {NOV} -m x", "git commit -" + "n -m x"
WIN_GIT = '"C:\\Program Files\\Git\\cmd\\git.exe"'
WIN_RM = '"C:\\Program Files\\Git\\usr\\bin\\rm.exe"'


@pytest.mark.parametrize("shell", [
    "bash -euo pipefail -c", "sh -eo pipefail -c", "bash -euxo pipefail -c",
    "bash -eO extglob -c", "bash --noprofile --norc -eo pipefail -c",
    "bash -oe pipefail -c", "bash -oO pipefail extglob -c", "bash -co pipefail",
    "bash +euo pipefail -c", "bash +c", "sh +c", "bash -c -", "bash -c --",
])
@pytest.mark.parametrize("inner,message", [
    (BYPASS, "standing path"), (NCOMMIT, "standing path"),
    (HARD, "git status"), (f"{RMRF} d", "git status"),
])
def test_shell_option_groups_do_not_hide_the_script(mod, shell, inner, message):
    """Round 1 P1: bash reads every letter of a `-`/`+` group — `c` makes the
    first operand the script, each `o`/`O` takes one word (`-euo pipefail`) —
    so the script is re-parsed and its bypass or destructive command asks."""
    permission, agent_msg, _ = mod.classify(f"{shell} '{inner}'")
    assert permission == "ask" and message in agent_msg, shell


@pytest.mark.parametrize("cmd", [
    "bash -euo pipefail -c 'echo ok'", "bash -o pipefail script.sh", "bash -eo pipefail",
])
def test_shell_option_values_are_not_scripts(mod, cmd):
    """Round 1 P1 neighbours: an option's value is not the script."""
    assert mod.classify(cmd)[0] == "allow", cmd


@pytest.mark.parametrize("cmd,message", [
    (f"{WIN_GIT} commit {NOV} -m x", "standing path"),
    (f"{WIN_GIT} reset --" + "hard", "git status"),
    (f"{WIN_RM} -" + "rf d", "git status"),
    ("GIT.EXE reset --" + "hard", "git status"),
    (f"Git.Exe commit {NOV} -m x", "standing path"),
])
def test_windows_program_paths_are_recognised(mod, cmd, message):
    """Round 1 P2: inside double quotes a backslash escapes only $ ` " \\ and
    newline, so a quoted Windows path keeps its backslashes; `.EXE` casefolds."""
    permission, agent_msg, _ = mod.classify(cmd)
    assert permission == "ask" and message in agent_msg, cmd


def test_double_quote_escapes_still_escape(mod):
    """Round 1 P2 neighbour: `\\"` inside double quotes is still a quote, not an end."""
    assert mod.classify(f'echo "a \\" {HARD} \\" b"')[0] == "allow"
    assert mod.classify(f'{WIN_GIT} status')[0] == "allow"


@pytest.mark.parametrize("wrapper", [
    "sudo -Eu root", "sudo -Hu root", "sudo -iu root", "sudo -Ec cls", "sudo --user root",
    "env -iu HOME", "env -uHOME", "timeout -vk 5 10", "timeout --kill-after 5 10",
    "time -pf %e", "exec -la name", "nice -n 5", "xargs -0n 1", "command -p", "nohup",
])
@pytest.mark.parametrize("inner", [HARD, BYPASS])
def test_wrapper_option_groups_keep_their_command(mod, wrapper, inner):
    """Round 1 P3: E1's wrappers read option groups getopt-style — the first
    value letter takes the rest of the group or, ending it, the next word."""
    assert mod.classify(f"{wrapper} {inner}")[0] == "ask", wrapper


@pytest.mark.parametrize("cmd,expected", [
    (f"env -S '{HARD}'", "ask"),
    (f"env -iS'{BYPASS}'", "ask"),
    (f"env --split-string='{RMRF} d'", "ask"),
    (f"env --split-string '{RMRF} d'", "ask"),
    ("env -S 'echo ok'", "allow"),
    ("sudo -uE ls", "allow"),          # -u takes "E"; ls is the command
])
def test_env_split_string_runs_its_value(mod, cmd, expected):
    """Round 1 P3: `env -S '…'` splits its value into the command it runs."""
    assert mod.classify(cmd)[0] == expected, cmd


@pytest.mark.parametrize("cmd,expected", [
    (f"function f {{ {RMRF} d; }}; f", "ask"),
    (f"function f {{ {BYPASS}; }}; f", "ask"),
    (f"function f\n{{ {HARD}; }}", "ask"),
    ("function f { echo ok; }; f", "allow"),
])
def test_function_keyword_body_is_in_command_position(mod, cmd, expected):
    """Round 1 P3: `function name { body; }` — the body's first word is a command."""
    assert mod.classify(cmd)[0] == expected, cmd


@pytest.mark.parametrize("cmd,expected", [
    (f"(( x = 1 << 2 ))\n{HARD}", "ask"),
    (f"(( x <<= 1 ))\n{BYPASS}", "ask"),
    (f"for (( i = 1; i << 2; i++ )); do echo; done\n{HARD}", "ask"),
    (f"x=$(( 1 << 2 ))\n{HARD}", "ask"),
    (f"echo $[ 1 << 2 ]\n{HARD}", "ask"),              # unreadable: raw-string fallback
    (f"cat <<EOF\nno delimiter line\n{HARD}", "ask"),   # unreadable: raw-string fallback
    ("(( x = 1 << 2 ))\necho ok", "allow"),
    (f"cat <<EOF\n{HARD}\nEOF", "allow"),
    (f"cat <<EOF\n{HARD}\nEOF\necho ok", "allow"),
    (f"cat <<-EOF\n\t{HARD}\n\tEOF", "allow"),
])
def test_arithmetic_shift_is_not_a_heredoc(mod, cmd, expected):
    """Round 1 P3: `<<` inside (( … )) is a shift, so the next line is a command;
    a heredoc whose delimiter never comes falls back to the raw-string reading."""
    assert mod.classify(cmd)[0] == expected, cmd


@pytest.mark.parametrize("cmd,expected", [
    ("git commit --message '-n is dry run'", "allow"),
    (f"git commit --message '{NOV} is banned'", "allow"),
    ("git commit --file -n", "allow"),
    ("git commit --author '-n <a@b>' -m x", "allow"),
    (f"git merge --message '{NOV}' topic", "allow"),
    ("git commit --message x -" + "n", "ask"),
    ("git commit --message=-x -" + "n", "ask"),
    (f"git merge --strategy ours {NOV} topic", "ask"),
])
def test_long_option_values_are_data(mod, cmd, expected):
    """Round 1 P3: the word after `--message`/`--file`/… is the option's value."""
    assert mod.classify(cmd)[0] == expected, cmd


# --- 2026-09-23 card 2, judge round 2: shapes bash 5.2 runs that the strict read missed
HARD_FLAG = "--" + "hard"
NV, DE = "standing path", "git status"  # NO_VERIFY_AGENT_MSG / DESTRUCTIVE_AGENT_MSG


def _asks_with(mod, cmd, message):
    permission, agent_msg, user_msg = mod.classify(cmd)
    return permission == "ask" and message in agent_msg and bool(user_msg)


@pytest.mark.parametrize("cmd,message", [
    (f'echo x > "$({HARD})"', DE),
    (f"echo x >$({RMRF} d)", DE),
    (f"cat < $({HARD})", DE),
    (f'cat <<< "$({RMRF} d)"', DE),
    (f"cat <<< $({HARD})", DE),
    (f"echo x 2>`{RMRF} d`", DE),
    (f"echo x >> `{HARD}`", DE),
    (f'echo x &> "$(git commit {NOV} -m x)"', NV),
    (f"echo x >| $({RMRF} d)", DE),
    (f"cat < <({RMRF} d)", DE),
    (f"echo x > >({RMRF} d)", DE),
    (f"echo x >\n{RMRF} d", DE),  # a redirection with no target is unreadable: fallback
])
def test_substitutions_in_redirection_targets_run(mod, cmd, message):
    """Round 2 P2 (E1): bash runs the `$(…)`, backquote and `<(…)`/`>(…)` inside a
    redirection target or a `<<<` word, so their bodies are read as commands."""
    assert _asks_with(mod, cmd, message), cmd


@pytest.mark.parametrize("cmd", [
    f"echo x > '$({RMRF} d)'",            # single quotes: only a file name
    f"cat <<< '{RMRF} d'",                 # a here-string word is data
    "echo x > out.txt 2>&1",
    "cat < <(git log --oneline)",
    "diff <(git show a:f) <(git show b:f)",
    f"cat <<'EOF' > \"$(mktemp)\"\n{RMRF} d\nEOF",
])
def test_redirection_targets_are_still_data(mod, cmd):
    """Round 2 P2 neighbours: the target word itself is never a command."""
    assert mod.classify(cmd)[0] == "allow", cmd


@pytest.mark.parametrize("cmd", [
    f"git pull {NOV}", f"git -C sub pull --rebase {NOV}", "git pull --no-ver",
    "git -C x pull --no-verif", "git pull --no-gpg", "git -c core.hooksPath=/x pull",
    f"git pull -s ours {NOV} origin main", f"git pull --depth 1 {NOV}",
])
def test_pull_hook_bypass_asks(mod, cmd):
    """Round 2 P2 (E2): `git pull` merges, so `--no-verify` skips the repo's
    pre-merge-commit hook (git 2.43 `git pull -h`)."""
    assert _asks_with(mod, cmd, NV), cmd


@pytest.mark.parametrize("cmd", [
    "git pull -n",                          # pull -n is --no-stat
    "git pull -rn origin main",             # -r takes the rest of the cluster
    "git pull --rebase origin main",
    f"git pull -X '{NOV}' origin main",     # option values, not flags
    f"git pull --upload-pack '{NOV}' origin",
    f"git pull --strategy-option '{NOV}' origin",
    "git pull --no-verify-signatures",
])
def test_pull_neighbours_are_allowed(mod, cmd):
    """Round 2 P2 neighbours: pull's -n and option values are not a bypass."""
    assert mod.classify(cmd)[0] == "allow", cmd


@pytest.mark.parametrize("cmd,expected", [
    ("git reset --h", "ask"),
    ("git reset -q --h HEAD~1", "ask"),
    ("git reset --ha", "ask"),
    ("git -C x reset --h", "ask"),
    ("git reset --", "allow"),              # `--` alone ends options
    ("git reset --soft HEAD~1", "allow"),
])
def test_reset_hard_three_character_prefix(mod, cmd, expected):
    """Round 2 P3 (E3): git 2.43 resets hard on `--h`; no other reset option
    starts with h."""
    assert mod.classify(cmd)[0] == expected, cmd


@pytest.mark.parametrize("cmd,expected", [
    (f"nohup -- {RMRF} d", "ask"),
    (f"nohup -- {HARD}", "ask"),
    (f"nohup -- git commit {NOV} -m x", "ask"),
    ("nohup -- sleep 1", "allow"),
])
def test_nohup_double_dash_is_unwrapped(mod, cmd, expected):
    """Round 2 P3 (E1): GNU nohup accepts `--` before the command it runs."""
    assert mod.classify(cmd)[0] == expected, cmd


@pytest.mark.parametrize("cmd,expected", [
    (f"echo ''#; {RMRF} d", "ask"),
    (f'echo ""#; {HARD}', "ask"),
    (f"echo $''#; {RMRF} d", "ask"),
    (f"echo x #; {RMRF} d", "allow"),
    (f"echo x;#{RMRF} d", "allow"),
    (f"git commit -m '' -{'n'}", "ask"),    # an empty quoted word is still a word
])
def test_a_quote_starts_a_word(mod, cmd, expected):
    """Round 2 P3a: `''#` is the word `#`, not a comment, and an empty quoted
    word stays a token (so `-m ''` does not swallow the next flag)."""
    assert mod.classify(cmd)[0] == expected, cmd


@pytest.mark.parametrize("cmd,expected", [
    # a quoted heredoc body is literal: a trailing backslash does not join lines
    (f"cat > a.sh <<'EOF'\nfoo \\\nEOF\n{RMRF} d\ncat > b.sh <<'EOF'\nbar\nEOF", "ask"),
    # a comment ends at its newline even after a backslash
    (f"# note \\\n{RMRF} d", "ask"),
    # an unquoted body joins backslash-newline, so that EOF line is still body
    (f"cat > a.sh <<EOF\nfoo \\\nEOF\n{RMRF} d\nEOF", "allow"),
    # an escaped backslash at the end of a line is no continuation
    (f"cat > a.sh <<EOF\nfoo \\\\\nEOF\n{RMRF} d", "ask"),
    # continuations still join words, in double quotes and in a -c script
    (f"git reset \\\n{HARD_FLAG}", "ask"),
    (f'bash -c "git reset \\\n{HARD_FLAG}"', "ask"),
    (f"bash -c 'git reset \\\n{HARD_FLAG}'", "ask"),
    # a backslash before a CR escapes the CR; the newline still ends the command
    (f"echo \\\r\n{RMRF} d", "ask"),
])
def test_line_continuations_join_only_where_bash_joins(mod, cmd, expected):
    """Round 2 P3b: backslash-newline is removed in words and double quotes only,
    never in single quotes, quoted heredoc bodies or comments."""
    assert mod.classify(cmd)[0] == expected, cmd


@pytest.mark.parametrize("cmd,expected", [
    (f'cat <<"E\\"F"\nx\nE"F\n{RMRF} d\nEF', "ask"),     # delimiter is E"F
    (f'cat <<"E\\F"\nx\nE\\F\n{RMRF} d\nEF', "ask"),      # "E\F" keeps the backslash
    (f"cat <<E\\F\nx\nEF\n{RMRF} d\nE\\F", "ask"),        # E\F is EF
    (f"cat <<'E\\F'\n{RMRF} d\nE\\F", "allow"),
    (f"cat <<E''OF\n{RMRF} d\nEOF", "allow"),
    # the delimiter line must match exactly, as bash compares it
    (f"cat <<EOF\nx\n EOF\n{RMRF} d\nEOF", "allow"),     # ' EOF' is body
    (f"cat <<EOF\nx\n EOF\ndon't\nEOF\n{RMRF} d", "ask"),
    (f"cat <<EOF\nb\nEOF\r\n{RMRF} d\nEOF", "allow"),    # 'EOF\r' is body
    (f"cat <<-EOF\n\tx\n\tEOF\n{RMRF} d", "ask"),        # <<- strips tabs
    (f"cat <<-EOF\n x\n EOF\n{RMRF} d\nEOF", "allow"),    # ... but not spaces
])
def test_heredoc_delimiter_quote_removal_and_exact_match(mod, cmd, expected):
    """Round 2 P3c: the delimiter gets bash's quote removal, and the body ends
    only on a line equal to it (tabs stripped for `<<-`)."""
    assert mod.classify(cmd)[0] == expected, cmd


@pytest.mark.parametrize("cmd,expected", [
    (f"git commit -m \"$(cat <<'EOF'\nfix: never {RMRF} docs\nEOF)\"", "allow"),
    (f"git commit -m \"$(cat <<'EOF'\nfix: x\nEOF)\" {NOV}", "ask"),
    (f"y=\"$(cat <<'EOF'\nb\nEOF)$({RMRF} d)\"", "ask"),
    # bash cuts at `EOF x)` and `EOFz)` too, runs `x`/`z` as commands, then
    # runs the next line; read without the cut, the `EOF` in z's substitution
    # would end the heredoc and hide it
    (f"y=\"$(cat <<EOF\nb\nEOF x)\"\n{RMRF} d\nz=\"$(echo\nEOF\n)\"", "ask"),
    (f"y=\"$(cat <<EOF\nb\nEOFz)\"\n{RMRF} d\nz=\"$(echo\nEOF\n)\"", "ask"),
    (f"cat <(cat <<EOF\nx\nEOF)\n{RMRF} d", "ask"),           # <( … ) cuts as well
    (f"y=\"$(cat <<EOF\nb\nEOF x)\"\nz=\"$(echo\nEOF\n)\"", "allow"),
    (f"cat <<'EOF'\nx\nEOF)\n{RMRF} d", "ask"),   # top level: no cut, unreadable
])
def test_heredoc_cut_by_the_closing_paren(mod, cmd, expected):
    """Round 2 P3 (F29): inside `$( … )` bash 5.2 ends a heredoc on a line that
    starts with the delimiter and has a `)` later (`EOF)"`, with a warning)."""
    assert mod.classify(cmd)[0] == expected, cmd


@pytest.mark.parametrize("cmd,expected", [
    (f"bash -c $'{HARD}\\n'", "ask"),
    ("bash -c $'git reset \\x2d-hard'", "ask"),
    (f"$'rm' -{'rf'} d", "ask"),
    (f"printf $'%s\\n' '{RMRF}'", "allow"),
    (f"echo $'it\\'s {RMRF}'", "allow"),
    (f'echo $"{RMRF}"', "allow"),
])
def test_ansi_c_quoting_is_decoded(mod, cmd, expected):
    """Round 2 P3 (E1): `$'…'` is read with bash's escapes, so the script of
    `bash -c $'…'` is re-parsed as bash runs it."""
    assert mod.classify(cmd)[0] == expected, cmd


@pytest.mark.parametrize("command", [
    f'echo x > "$({HARD})"',
    f"git pull {NOV}",
])
def test_round_two_shapes_ask_through_the_hook(command):
    """Round 2: the live hook (script path, JSON on stdin) asks on these too."""
    result = subprocess.run(
        [sys.executable, str(GUARD)], input=json.dumps({"tool_input": {"command": command}}),
        capture_output=True, text=True, encoding="utf-8", cwd=REPO, check=False, timeout=30,
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"] == "ask"
