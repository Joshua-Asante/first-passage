"""Regression tests for the #470 review round 2 (independent review of f09399e).

Each case was a reproduced bypass of Revision 1's rules (F30-F32) or of D8/D10/D11/D14.
They reuse the frozen acceptance suite's fake gh/git at the `_run` seam, so they
exercise the same argv contract; the frozen suite itself is not modified.
"""
import pytest

from scripts import guard_s2_runs as guard
from test_guard_s2_runs_acceptance import (  # pylint: disable=unused-import
    DISPATCH, REPO, WORKFLOW_FILE, FakeShell, X, Y, _opt, dispatch_run, live_pr, sh)

OWNER = "Joshua-Asante/first-passage"
BRANCH_SUB = '"$(git branch --show-current)"'


def decide(command, cwd=REPO):
    return guard.refusal_for_command(command, cwd=cwd)


def gh_repos(fake):
    """The -R value of every gh call the guard made (None when absent)."""
    out = []
    for cmd, _ in fake.calls:
        if cmd[0].removesuffix(".exe").endswith("gh") and "api" not in cmd[1:3]:
            out.append(_opt(cmd, "-R", "--repo"))
    return out


def live_full(fake):
    fake.runs["feat"] = [dispatch_run(status="in_progress", conclusion=None)]


def live_diagnostic(fake):
    fake.runs["feat"] = [dispatch_run(status="in_progress", conclusion=None, cases="deadline")]


# --- F30: every pflag spelling of -R, anywhere cobra accepts it ------------------

@pytest.mark.parametrize("prefix", [f"-R{OWNER}", f"-R={OWNER}", f"-R {OWNER}",
                                    f"--repo {OWNER}", f"--repo={OWNER}"])
def test_repo_flag_spellings_before_the_subcommand(sh, prefix):  # pylint: disable=redefined-outer-name
    live_full(sh)
    assert decide(f"gh {prefix} workflow run {WORKFLOW_FILE} --ref feat")
    assert set(gh_repos(sh)) == {OWNER}


@pytest.mark.parametrize("command", [
    f"gh -R{OWNER} run rerun 101",
    f"gh -R={OWNER} run rerun 101",
    f"gh run -R {OWNER} rerun 101",
    f"gh run --repo={OWNER} rerun 101",
    f"gh run rerun 101 -R{OWNER}",
])
def test_rerun_with_repo_flag_anywhere(sh, command):  # pylint: disable=redefined-outer-name
    sh.runs["feat"] = [dispatch_run(conclusion="failure", rid=101)]
    sh.views["101"] = sh.runs["feat"][0]
    assert decide(command), command


def test_update_branch_with_attached_repo_flag(sh):  # pylint: disable=redefined-outer-name
    live_pr(sh, "feat", 462)
    sh.pr_heads["462"] = "feat"
    assert decide(f"gh -R={OWNER} pr update-branch 462")


@pytest.mark.parametrize("command", [
    f"gh --ref feat workflow run {WORKFLOW_FILE}",
    f"gh workflow -r feat run {WORKFLOW_FILE}",
    f"gh workflow --ref=feat run {WORKFLOW_FILE}",
    f"gh -R {OWNER} --ref feat workflow run {WORKFLOW_FILE}",
])
def test_leaf_flags_before_the_subcommand(sh, command):  # pylint: disable=redefined-outer-name
    live_full(sh)
    assert decide(command), command


def test_typed_field_before_the_group_still_wins(sh):  # pylint: disable=redefined-outer-name
    sh.runs["feat"] = [dispatch_run(mode="s3", conclusion="success")]
    assert decide(f"gh -F mode=s3 workflow run {WORKFLOW_FILE} --ref feat -f mode=s2")


@pytest.mark.parametrize("command", [
    f"gh --help workflow run {WORKFLOW_FILE} --ref feat",
    f"gh -R o/r --help workflow run {WORKFLOW_FILE} --ref feat",
    f"gh workflow run {WORKFLOW_FILE} --ref feat -h",
])
def test_help_is_not_a_command(sh, command):  # pylint: disable=redefined-outer-name
    live_full(sh)
    assert decide(command) is None


def test_the_last_repo_flag_wins(sh):  # pylint: disable=redefined-outer-name
    live_full(sh)
    assert decide(f"gh -R a/b workflow run {WORKFLOW_FILE} --ref feat -R {OWNER}")
    assert set(gh_repos(sh)) == {OWNER}


# --- D14: a substitution never ends its command --------------------------------

def test_substituted_ref_keeps_the_later_fields(sh):  # pylint: disable=redefined-outer-name
    live_diagnostic(sh)
    assert "whitespace" in decide(f"{DISPATCH.split(' --ref')[0]} --ref {BRANCH_SUB} -f mode=s3 -f cases=' '")
    assert decide(f"gh workflow run {WORKFLOW_FILE} --ref {BRANCH_SUB} -f mode=s3 -f cases=deadline")
    live_full(sh)
    assert decide(f"gh workflow run {WORKFLOW_FILE} --ref {BRANCH_SUB} -f mode=s3 -f cases=deadline") is None
    sh.runs["feat"] = [dispatch_run(mode="s3", conclusion="success")]
    assert decide(f"gh workflow run {WORKFLOW_FILE} -f mode=s2 --ref {BRANCH_SUB} -F mode=s3")


def test_substituted_repo_and_ref_before_the_selector(sh):  # pylint: disable=redefined-outer-name
    live_full(sh)
    assert decide(f'gh -R "$(echo {OWNER})" workflow run {WORKFLOW_FILE} --ref feat')
    assert decide(f"gh workflow run --ref {BRANCH_SUB} {WORKFLOW_FILE}")


def test_backquote_ref_keeps_the_later_fields(sh):  # pylint: disable=redefined-outer-name
    live_diagnostic(sh)
    assert decide(f"gh workflow run {WORKFLOW_FILE} --ref `git branch --show-current` -f cases=' '")


def test_substitution_runs_before_its_command():
    assert guard._segments("out=$(git push origin feat)") == [  # pylint: disable=protected-access
        ["git", "push", "origin", "feat"], ["out=$(git push origin feat)"]]


# --- ANSI-C and locale quoting --------------------------------------------------

def test_ansi_c_whitespace_cases_is_refused(sh):  # pylint: disable=redefined-outer-name,unused-argument
    assert "whitespace" in decide(f"{DISPATCH} -f mode=s3 -f cases=$'\\t'")


@pytest.mark.parametrize("empty", ["$''", '$""'])
def test_ansi_c_empty_cases_is_a_full_dispatch(sh, empty):  # pylint: disable=redefined-outer-name
    live_full(sh)
    assert "cancel" in decide(f"{DISPATCH} -f cases={empty}")


def test_ansi_c_decoding():
    command = "echo $'a\\tb\\x41\\u00e9\\101' $'it''s' $\"x\" $\\\"y\\\""
    tokens = guard._segments(command)  # pylint: disable=protected-access
    assert tokens == [["echo", "a\tbAéA", "its", "x", '$"y"']]  # an escaped $" stays literal


# --- D10/F31: typed @file inputs are read, stdin stays unknown -------------------

def test_typed_file_input_is_read_relative_to_the_segment(sh, tmp_path):  # pylint: disable=redefined-outer-name
    (tmp_path / "empty.txt").write_text("", encoding="utf-8")
    (tmp_path / "diag.txt").write_text("deadline", encoding="utf-8")
    (tmp_path / "mode.txt").write_text("s3", encoding="utf-8")
    sh.current[str(tmp_path).replace("\\", "/")] = "feat"
    live_full(sh)
    assert "cancel" in decide(f"{DISPATCH} -F cases=@empty.txt", cwd=str(tmp_path))
    assert decide(f"{DISPATCH} -F cases=@diag.txt", cwd=str(tmp_path)) is None
    assert decide(f"{DISPATCH} -F cases=@-", cwd=str(tmp_path)) is None
    assert decide(f"{DISPATCH} -F cases=@missing.txt", cwd=str(tmp_path)) is None
    sh.runs["feat"] = [dispatch_run(mode="s3", conclusion="success")]
    assert "passed" in decide(f"{DISPATCH} -F mode=@mode.txt", cwd=str(tmp_path))


def test_unknown_mode_still_gets_the_cancel_check(sh):  # pylint: disable=redefined-outer-name
    live_full(sh)
    assert "cancel" in decide(f"{DISPATCH} -F mode=@-")


def test_raw_at_sign_is_literal(sh):  # pylint: disable=redefined-outer-name
    live_full(sh)
    assert decide(f"{DISPATCH} -f cases=@diag.txt") is None  # non-empty literal: diagnostic group


# --- D8: GH_REPO, and [HOST/]OWNER/REPO -----------------------------------------

@pytest.mark.parametrize("command", [
    f"GH_REPO={OWNER} gh workflow run {WORKFLOW_FILE} --ref feat",
    f"export GH_REPO={OWNER}; gh workflow run {WORKFLOW_FILE} --ref feat",
])
def test_gh_repo_is_carried_into_every_gh_query(sh, command):  # pylint: disable=redefined-outer-name
    live_full(sh)
    assert decide(command)
    assert set(gh_repos(sh)) == {OWNER}


def test_unset_gh_repo_and_explicit_flag_precedence(sh, monkeypatch):  # pylint: disable=redefined-outer-name
    monkeypatch.setenv("GH_REPO", "env/repo")
    live_full(sh)
    assert decide(f"gh workflow run {WORKFLOW_FILE} --ref feat -R {OWNER}")
    assert set(gh_repos(sh)) == {OWNER}
    sh.calls.clear()
    assert decide(f"unset GH_REPO; gh workflow run {WORKFLOW_FILE} --ref feat")
    assert set(gh_repos(sh)) == {None}


@pytest.mark.parametrize("repo,host", [
    (f"github.com/{OWNER}", None),
    (f"https://github.com/{OWNER}.git", None),
    (f"ghe.example.com/{OWNER}", "ghe.example.com"),
])
def test_host_prefixed_repo_builds_a_valid_api_path(sh, repo, host):  # pylint: disable=redefined-outer-name
    sh.runs["feat"] = [dispatch_run(conclusion="success")]
    assert decide(f"gh -R {repo} workflow run {WORKFLOW_FILE} --ref feat")
    api = [cmd for cmd, _ in sh.calls if "api" in cmd[1:4]]
    assert api and all(f"repos/{OWNER}/commits/feat" in cmd for cmd in api)
    assert all(_opt(cmd, "--hostname") == host for cmd in api)


# --- D11: gh run rerun --job resolves its run --------------------------------------

class JobShell(FakeShell):
    """FakeShell that also answers the jobs endpoint."""

    def __init__(self, jobs):
        super().__init__()
        self.jobs = jobs

    def gh(self, cmd):
        path = next((c for c in cmd[2:] if c.startswith("repos/")), "")
        if "api" in cmd[1:3] and "/actions/jobs/" in path:
            run_id = self.jobs.get(path.rsplit("/", 1)[-1])
            return None if run_id is None else f"{run_id}\n"
        return super().gh(cmd)


@pytest.mark.parametrize("flag", ["--job 5555", "-j 5555", "--job=5555", "-j5555"])
def test_rerun_of_a_job_resolves_its_run(monkeypatch, flag):
    fake = JobShell({"5555": 101})
    fake.tips = {"feat": X, "main": Y}
    monkeypatch.setattr(guard, "_run", fake)
    fake.runs["feat"] = [dispatch_run(conclusion="failure", rid=101)]
    fake.views["101"] = fake.runs["feat"][0]
    assert decide(f"gh run rerun {flag}")
    assert decide("gh run rerun --job 9999") is None  # unknown job: fail open


# --- review round 3 (f3fbc77): heredocs in substitutions, directories, inputs ----

APOSTROPHE_COMMIT = "git commit -m \"$(cat <<'EOF'\nDon't push yet (really)\nEOF\n)\""


def test_heredoc_commit_idiom_does_not_swallow_the_push(sh):  # pylint: disable=redefined-outer-name
    live_pr(sh)
    assert decide(f"{APOSTROPHE_COMMIT} && git push origin feat")


def test_heredoc_commit_idiom_does_not_swallow_the_dispatch(sh):  # pylint: disable=redefined-outer-name
    live_full(sh)
    assert decide(f"{APOSTROPHE_COMMIT} && gh workflow run {WORKFLOW_FILE} --ref feat")


@pytest.mark.parametrize("prefix", ['x=$(echo "a\\")b"); ', "grep x <<< \"$v\"\n", "cat <<\\EOF\nbody\nEOF\n"])
def test_quoting_edge_cases_keep_the_following_command(sh, prefix):  # pylint: disable=redefined-outer-name
    live_pr(sh)
    assert decide(f"{prefix}git push origin feat"), prefix


@pytest.mark.parametrize("target", ['"$(git rev-parse --show-toplevel)"', '"$REPO"', "`pwd`"])
def test_unknowable_cd_and_dash_c_targets_keep_the_current_directory(sh, target):  # pylint: disable=redefined-outer-name
    live_pr(sh)
    assert decide(f"cd {target} && git push origin feat")
    assert decide(f"git -C {target} push origin feat")


def test_tilde_directory_is_expanded(monkeypatch):
    monkeypatch.setenv("HOME", "/home/me")
    # Windows expanduser reads USERPROFILE (never the monkeypatched HOME), so
    # both name the same directory and the test holds on either system.
    monkeypatch.setenv("USERPROFILE", "/home/me")
    assert guard._join_dir("/repo", "~/wt") == "/home/me/wt"  # pylint: disable=protected-access


def test_out_of_range_ansi_c_escape_does_not_crash(sh):  # pylint: disable=redefined-outer-name
    live_pr(sh)
    assert decide("echo $'\\U00110000'; git push origin feat")


def test_file_inputs_are_regular_files_only_and_bounded(sh, tmp_path):  # pylint: disable=redefined-outer-name
    big = tmp_path / "big.txt"
    big.write_text(" " * 70000 + "deadline", encoding="utf-8")
    sh.current[str(tmp_path).replace("\\", "/")] = "feat"
    live_full(sh)
    assert decide(f"{DISPATCH} -F cases=@big.txt", cwd=str(tmp_path)) is None  # too big: unknown
    assert decide(f"{DISPATCH} -F cases=@/dev/stdin", cwd=str(tmp_path)) is None  # not ours to read
    assert decide(f"{DISPATCH} -F cases=@.", cwd=str(tmp_path)) is None  # a directory


def test_rerun_job_ignores_the_positional_run_id(monkeypatch):
    fake = JobShell({"5555": 101})
    fake.tips = {"feat": X, "main": Y}
    monkeypatch.setattr(guard, "_run", fake)
    fake.runs["feat"] = [dispatch_run(conclusion="failure", rid=101)]
    fake.views["101"] = fake.runs["feat"][0]
    assert decide("gh run rerun 999 --job 5555")


@pytest.mark.parametrize("repo", ["git@github.com:Joshua-Asante/first-passage.git",
                                  "ssh://git@github.com/Joshua-Asante/first-passage",
                                  "ssh://git@github.com:22/Joshua-Asante/first-passage.git"])
def test_ssh_and_scp_repo_forms_build_a_valid_api_path(sh, repo):  # pylint: disable=redefined-outer-name
    sh.runs["feat"] = [dispatch_run(conclusion="success")]
    assert decide(f"gh -R {repo} workflow run {WORKFLOW_FILE} --ref feat")
    api = [cmd for cmd, _ in sh.calls if "api" in cmd[1:4]]
    assert api and all(f"repos/{OWNER}/commits/feat" in cmd and "--hostname" not in cmd for cmd in api)


def test_env_wrapper_gh_repo_is_carried(sh):  # pylint: disable=redefined-outer-name
    live_full(sh)
    assert decide(f"env GH_REPO={OWNER} gh workflow run {WORKFLOW_FILE} --ref feat")
    assert set(gh_repos(sh)) == {OWNER}


@pytest.mark.parametrize("flag,refused", [("--json=false", True), ("--json=true", False), ("--json", False)])
def test_json_flag_is_a_pflag_bool(sh, flag, refused):  # pylint: disable=redefined-outer-name
    live_full(sh)
    assert (decide(f"{DISPATCH} {flag}") is not None) is refused


def test_double_dash_ends_the_flags(sh):  # pylint: disable=redefined-outer-name
    sh.runs["feat"] = [dispatch_run(conclusion="success")]
    assert decide(f"{DISPATCH} -- -f mode=s2")  # gh ignores words after --: s4 dispatched
    sh.runs["feat"] = []
    sh.runs["main"] = [dispatch_run("main", sha=Y, conclusion="success")]
    assert decide(f"gh workflow run -- {WORKFLOW_FILE} --ref feat")  # default branch, not feat


@pytest.mark.parametrize("command", ["sudo -u me git push origin feat", "time -p git push origin feat",
                                     "sudo -- git push origin feat", "nice -n 5 git push origin feat"])
def test_wrapper_options_are_skipped(sh, command):  # pylint: disable=redefined-outer-name
    live_pr(sh)
    assert decide(command), command


def test_empty_quoted_words_are_kept(sh):  # pylint: disable=redefined-outer-name
    live_full(sh)
    assert decide(f"gh -R '' workflow run {WORKFLOW_FILE} --ref feat")


def test_partial_substitutions_are_unknowable_not_the_current_branch(sh):  # pylint: disable=redefined-outer-name
    live_pr(sh)
    assert decide('git push origin "HEAD:refs/heads/$(git branch --show-current)"')
    assert decide('git push origin "$(git branch --show-current)-backup"') is None


def test_update_branch_records_its_push_for_a_later_dispatch(sh):  # pylint: disable=redefined-outer-name
    sh.pr_heads["462"] = "feat"
    sh.runs["feat"] = [dispatch_run(mode="s3", conclusion="success")]
    assert decide(f"gh pr update-branch 462 && gh workflow run {WORKFLOW_FILE} --ref feat") is None


def test_no_cwd_uses_the_process_directory(sh, monkeypatch):  # pylint: disable=redefined-outer-name
    monkeypatch.chdir("/")
    sh.current["/"] = "feat"
    live_pr(sh)
    assert guard.refusal_for_command("git push origin HEAD") is not None
