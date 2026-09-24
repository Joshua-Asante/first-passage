"""The two modes of scripts/_shell_tokens.py after card 1's #470 rounds 2-3 were ported in.

Default mode is card 1's reading for guard_s2_runs.py (lenient, substitution bodies
before their command); strict mode is card 2's shell-guard reading (raises, bodies
after). Card 1's and card 2's suites pin each mode's details; these pin the split.
"""
from __future__ import annotations

import pytest

from scripts import _shell_tokens as tokens

PUSH = ["git", "push", "origin", "feat"]


def test_substitution_bodies_come_before_the_command_in_default_mode_only():
    """Default mode runs the substitution first (card 1 D14); strict defers it (card 2 E1)."""
    command = 'git commit -m "$(git push origin feat)" --amend'
    enclosing = ["git", "commit", "-m", "$(git push origin feat)", "--amend"]
    assert tokens.segments(command) == [PUSH, enclosing]
    assert tokens.segments(command, strict=True) == [enclosing, PUSH]


@pytest.mark.parametrize("command", [
    "echo $'abc", "x=$(git push origin feat", 'echo "abc', "echo `pwd",
    "cat <<EOF\nno end", "echo x >", "cat <<",
])
def test_default_mode_is_lenient_where_strict_mode_raises(command):
    """guard_s2_runs fails open on unreadable input; the shell guard falls back to its regexes."""
    tokens.segments(command)  # never raises
    with pytest.raises(tokens.ShellSyntaxError):
        tokens.segments(command, strict=True)


@pytest.mark.parametrize("wrapped", [
    "sudo -u me", "sudo -uroot", "sudo -Eu root", "sudo --user=me", "sudo --user me",
    "sudo --", "time -p", "nice -n 5", "nice", "exec -a name", "nohup", "command",
])
@pytest.mark.parametrize("strict", [False, True])
def test_wrapper_options_are_skipped_getopt_style_in_both_modes(wrapped, strict):
    """One option table per wrapper serves both modes (`-uroot` takes no next word)."""
    assert tokens.expand([*wrapped.split(), *PUSH], strict=strict) == [PUSH]


def test_matching_paren_skips_a_heredoc_body_with_parentheses_and_quotes():
    """The `$(cat <<'EOF' … EOF)` commit idiom stays balanced for _whole_substitution."""
    text = "$(cat <<'EOF'\nfix(guard): it's )(\nEOF\n)"
    assert tokens.matching_paren(text, 2) == len(text) - 1
    assert tokens.matching_paren("$(echo ')'", 2) == len("$(echo ')'")  # unclosed: len(text)


def test_default_mode_decodes_ansi_c_and_keeps_empty_quoted_words():
    """`$'…'` is decoded (an unterminated one runs to the end) and `''` stays a word."""
    assert tokens.segments("git push origin $'fe\\x61t' '' \"\"") == [[*PUSH, "", ""]]
    assert tokens.segments("echo $'unterminated\\tvalue") == [["echo", "unterminated\tvalue"]]


@pytest.mark.parametrize("command,first", [
    ("echo $'\\c'; git push origin feat", ["echo", "\\c"]),
    ("printf %s $'a\\c\\'b'; git push origin feat", ["printf", "%s", "a\x1c'b"]),
    ("echo $''#x; git push origin feat", ["echo", "#x"]),
])
def test_default_mode_ansi_c_ends_where_bash_ends_it(command, first):
    """`\\c` never swallows the closing quote and `$''#` is a word, so the push stays visible."""
    assert tokens.segments(command) == [first, PUSH]


@pytest.mark.parametrize("wrapped", [
    "sudo -R /jail", "sudo --role r", "/usr/bin/time --output t.txt", "nice --adjustment 5",
])
def test_default_mode_reads_value_options_from_the_shared_tables(wrapped):
    """Round 3 read these values as the command; the shared tables skip them."""
    assert tokens.expand([*wrapped.split(), *PUSH]) == [PUSH]


# --- card 4 (2026-09-23): default mode reads env/timeout options; comments after '' --

@pytest.mark.parametrize("wrapped", [
    "timeout -k 5 60", "timeout -s KILL 60", "timeout --kill-after 5 10",
    "env -C /repo", "env --chdir /repo", "env -u NAME", "env --unset NAME",
])
def test_default_mode_skips_env_and_timeout_option_values(wrapped):
    """Card 4 item 1: `timeout -k 5 60 cmd` used to leave the duration as the
    command and `env -C dir cmd` the directory; the shared _ENV_OPTS/_TIMEOUT_OPTS
    tables now skip each option's value, and timeout's one duration word."""
    assert tokens.expand([*wrapped.split(), *PUSH]) == [PUSH]


@pytest.mark.parametrize("wrapped", ["timeout 120", "env FOO=1", "env -i"])
def test_default_mode_duration_and_assignments_are_unchanged(wrapped):
    """Card 4 item 1's unchanged neighbours: a bare duration and assignments."""
    assert tokens.expand([*wrapped.split(), *PUSH]) == [PUSH]


def test_default_mode_does_not_split_env_s_and_skips_its_value():
    """Default mode must never raise, so `env -S '…'` is not split (strict mode
    splits it): the option and its value are skipped whole."""
    assert tokens.expand(["env", "-S", "git push origin feat"]) == []


@pytest.mark.parametrize("quote", ["''", '""', '$""'])
def test_default_mode_a_quoted_empty_word_starts_a_word(quote):
    """Card 4 item 2: `#` starts a comment only before a word has begun, and a
    quoted empty word has — `echo ''#x` is `echo #x`, so the push after the `;`
    stays visible (it used to be swallowed as part of the comment)."""
    assert tokens.segments(f"echo {quote}#x; git push origin feat") == [["echo", "#x"], PUSH]


@pytest.mark.parametrize("command", ["echo x #c", "echo x;#c"])
def test_default_mode_comments_still_start_where_bash_starts_them(command):
    """Card 4 item 2's unchanged neighbours: after a word, or after `;`, `#` is
    still a comment."""
    assert tokens.segments(command) == [["echo", "x"]]
