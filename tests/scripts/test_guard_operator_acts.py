"""Acceptance tests for scripts/guard_operator_acts.py.

Rule owner: docs/adr/2026-07-14-cc-cursor-surface-allocation.md §Decision, "Action
classes and the authority block" (2026-09-25 revision). Operator acts ask; forbidden
acts deny; data that merely mentions them, and risk-reducing exits, stay silent.
Command words are built by concatenation so no test source line is itself a command
a shell guard would stop on.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
GUARD = REPO / "scripts" / "guard_operator_acts.py"
sys.path.insert(0, str(REPO))
from scripts import guard_operator_acts as g  # noqa: E402

MERGE = "gh pr " + "merge"
SHA = "0123456789abcdef0123456789abcdef01234567"
PIN = f"--match-head-commit {SHA}"
ADMIN = f"{MERGE} 501 --admin {PIN}"


@pytest.mark.parametrize("command", [
    f"{MERGE} 501 --squash {PIN}",
    f"{MERGE} --repo Joshua-Asante/first-passage 501 --match-head-commit={SHA}",
    f"gh -R Joshua-Asante/first-passage pr merge 501 {PIN}",
    f"cd /repo && {MERGE} 501 {PIN}",
    f"bash -c '{MERGE} 501 {PIN}'",
    "gh api -X PUT repos/o/r/pulls/501/" + f"merge -f sha={SHA}",
    "gh api graphql -f query='mutation { merge" + f"PullRequest(input: {{expectedHeadOid: \"{SHA}\"}}) {{ x }} }}'",
])
def test_pinned_merge_asks(command):
    # Fails if a pinned merge goes through without Joshua's prompt: merges are his
    # (AGENTS.md Roles, 2026-11-07), and the agents' merge GO has ended.
    assert g.classify_command(command) == ("ask", "pr.merge")


@pytest.mark.parametrize("command", [
    f"{MERGE} 501 --squash",
    f"{MERGE} 501 --match-head-commit abc123",
    f"bash -c '{MERGE} 501'",
    "gh api -X PUT repos/o/r/pulls/501/" + "merge",
    "gh api graphql -f query='mutation { merge" + "PullRequest(input: {}) { x } }'",
])
def test_unpinned_merge_denied(command):
    # Fails if an approval could merge bytes other than the head the operator saw
    # (Astra finding 2, PR #503 at 72c435c).
    assert g.classify_command(command) == ("deny", "pr.merge_unpinned")


@pytest.mark.parametrize("command", [
    f"bash -c '{MERGE} 501 {PIN}; {MERGE} 502 --auto'",
    f"{MERGE} 501 {PIN} && {MERGE} 502 --auto",
    f"sh -c '{ADMIN}; {MERGE} 502 --auto'",
])
def test_deny_wins_over_ask_in_one_command(command):
    # Fails if a promptable act earlier in a command launders a forbidden one after it
    # (Astra finding 1, PR #503 at 72c435c).
    assert g.classify_command(command) == ("deny", "pr.auto_merge")


@pytest.mark.parametrize("command", [
    f"{MERGE} 501 --auto --squash",
    "gh api graphql -f query='mutation { enablePullRequest" + "AutoMerge(input: {}) { x } }'",
])
def test_auto_merge_denied(command):
    # Fails if auto-merge (retired; agents merge only pinned) is merely asked, not refused.
    assert g.classify_command(command) == ("deny", "pr.auto_merge")


def test_mcp_tools():
    # Fails if the GitHub MCP merge path bypasses the operator, or auto-merge is askable.
    merge = "mcp__github__merge_pull_request"
    assert g.classify({"tool_name": merge, "tool_input": {"expectedHeadSha": SHA}}) == (
        "ask", "pr.merge")
    assert g.classify({"tool_name": merge, "tool_input": {}}) == ("deny", "pr.merge_unpinned")
    assert g.classify({"tool_name": merge, "tool_input": {"expectedHeadSha": "abc"}}) == (
        "deny", "pr.merge_unpinned")
    assert g.classify({"tool_name": "mcp__github__enable_pr_auto_merge"}) == (
        "deny", "pr.auto_merge")
    assert g.classify({"tool_name": "mcp__github__pull_request_read"}) is None


@pytest.mark.parametrize("command", [
    "gh pr view 501",
    "gh pr create --title 'do not " + MERGE + " yet' --body x",
    f"git commit -m 'document {MERGE} and git push origin main'",
    f"grep -rn '{MERGE}' docs/",
    f"echo '{ADMIN}'",
])
def test_data_is_silent(command):
    # Fails if text that only mentions an act asks
    # (a background agent has nobody to answer a prompt — guard_shell_command F29).
    assert g.classify_command(command) is None


@pytest.mark.parametrize("command", [
    "git push origin main",
    "git push origin HEAD:main",
    "git push -u origin +feature:refs/heads/main",
    "git push origin --delete main",
    "git -C /repo push origin main",
    "git push origin claude/x main",
    "git push --force-with-lease origin main",
    "git push --force-if-includes --force-with-lease origin main",
    "git push --signed origin main",
    "git push --repo=origin origin main",
    "git push --repo origin origin main",
])
def test_push_to_main_denied(command):
    # Fails if a direct push to main, a merge-equivalent that bypasses the PR and the
    # required status, gets through (Fable review of #503, finding A).
    assert g.classify_command(command) == ("deny", "main.direct_push")


@pytest.mark.parametrize("command", [
    "git push -u origin claude/bold-shannon-cc2xmr",
    "git push origin HEAD:refs/heads/claude/x",
    "git push origin main:claude/backup",
    "git push --force-with-lease origin claude/x",
    "git push --repo=origin claude/x",
    "git fetch origin main",
    "git push",
])
def test_other_pushes_are_silent(command):
    # Fails if a branch push, or a push whose destination is not main, prompts.
    assert g.classify_command(command) is None


def test_unreadable_command_fails_closed():
    # Fails if an unterminated quote hides a merge from the guard (unreadable text cannot
    # prove a pin, so it is refused as unpinned).
    assert g.classify_command(f"{MERGE} 501 'unterminated")[0] == "deny"


def _run(payload) -> str:
    return subprocess.run([sys.executable, str(GUARD)], input=payload,
                          capture_output=True, text=True, check=True).stdout


def test_hook_contract():
    # Fails if the hook emits a non-PreToolUse shape, or emits anything (an allow) on
    # benign input, or blocks on malformed input.
    out = json.loads(_run(json.dumps({"tool_name": "mcp__github__merge_pull_request",
                                      "tool_input": {"expectedHeadSha": SHA}})))
    block = out["hookSpecificOutput"]
    assert block["hookEventName"] == "PreToolUse"
    assert block["permissionDecision"] == "ask"  # merges are Joshua's
    assert SHA in block["permissionDecisionReason"]
    assert "independent review" in block["additionalContext"]  # when to report it ready
    assert _run(json.dumps({"tool_name": "Bash", "tool_input": {"command": "ls"}})) == ""
    assert _run("not json") == ""


def test_merge_context_matches_agents_md_review_and_merge():
    # Fails if the merge context drifts from AGENTS.md "Review and merge": every PR,
    # doc-only included, needs green CI and the other agent's clean review at the head.
    # AGENTS.md sets no review-round limit, so the context must not add one.
    context = g.MESSAGES["pr.merge"][1]
    assert "AGENTS.md" in context
    assert "Every PR, doc-only included" in context
    assert "merges on that" not in context
    assert "finished successfully" in context
    assert "COMPLETED and green" not in context  # path-based skips are allowed if explained
    agents = (REPO / "AGENTS.md").read_text(encoding="utf-8")
    review = agents.split("## Review and merge", 1)[1].split("\n## ", 1)[0]
    for phrase in ("doc-only included", "pending, failed or cancelled", "path-based skip"):
        assert phrase in review, phrase  # AGENTS.md still says it
        assert phrase in context, phrase  # and the hook says the same
    assert "Codex reviews Claude's work, Claude reviews Codex's" in context
    for retired in ("fourth", "three reviews", "rewrite", "Addendum 2026-10-24b"):
        assert retired not in context


def test_agents_md_security_review_trigger_is_bare_and_joshuas():
    # Fails if AGENTS.md drops the security-review trigger rule. Codex runs a security
    # review only for a comment holding just "@codex security review"; any other text,
    # including the footer the server adds to every agent comment, gets a code review
    # instead (#1153, #1154, #1156, #1160, #1162 on 2026-11-08). So Joshua posts it.
    agents = (REPO / "AGENTS.md").read_text(encoding="utf-8")
    review = " ".join(agents.split("## Review and merge", 1)[1].split("\n## ", 1)[0].split())
    for phrase in ("`@codex security review`. Joshua posts it",
                   "holding only that text", "gets a code review instead"):
        assert phrase in review, phrase


def test_settings_wire_the_hook():
    # Fails if the hook is not registered for the Bash and PowerShell tools and the MCP
    # merge tools (a Windows session reaches `gh` through either shell tool).
    settings = json.loads((REPO / ".claude" / "settings.json").read_text())
    wired = [(e["matcher"], h["command"]) for e in settings["hooks"]["PreToolUse"]
             for h in e["hooks"]]
    ours = [m for m, c in wired if "guard_operator_acts.py" in c]
    assert "Bash" in ours
    assert "PowerShell" in ours
    assert any("merge_pull_request" in m and "enable_pr_auto_merge" in m for m in ours)


# --- 2026-09-25 babysit repairs (Codex reviews of #503 at e75b653 and 7cfd367) ---

OLD = "fedcba9876543210fedcba9876543210fedcba98"


def _reason(command: str, tool: str = "Bash") -> dict:
    out = _run(json.dumps({"tool_name": tool, "tool_input": {"command": command}}))
    return json.loads(out)["hookSpecificOutput"] if out else {}


@pytest.mark.parametrize("command", [
    "git push origin --all",
    "git push --all origin",
    "git push origin --branches",
    "git push --mirror origin",
    "git push --mirr origin",
    "git push origin --al",
    "git push origin :",
    "git push origin +:",
    "git push origin 'refs/heads/*:refs/heads/*'",
    "git push origin 'refs/heads/*'",
    "git push origin '+refs/heads/m*:refs/heads/m*'",
])
def test_bulk_push_that_covers_main_denied(command):
    # Fails if a bulk push (`--all`/`--branches`/`--mirror`, git's abbreviations of them,
    # the matching refspec `:` or a glob destination covering main) reaches main
    # unjudged (Codex #503 threads Drv / TGb).
    assert g.classify_command(command) == ("deny", "main.direct_push")


@pytest.mark.parametrize("command", [
    "git push origin --tags",
    "git push --atomic origin claude/x",
    "git push origin 'refs/heads/claude/*:refs/heads/claude/*'",
])
def test_bulk_forms_that_miss_main_are_silent(command):
    # Fails if the bulk-push rule over-reaches to pushes that cannot touch main.
    assert g.classify_command(command) is None


def test_unreadable_push_to_main_fails_closed():
    # Fails if a command the strict scanner cannot read hides a push to main
    # (Codex #503 thread TGc; `bash -n` accepts this command).
    command = 'echo "$(case x in x) echo ok;; esac)" && git push origin main'
    assert g.classify_command(command) == ("deny", "main.direct_push")
    assert g.classify_command(command.replace("origin main", "origin claude/x")) is None


def test_prompt_names_the_sha_the_merge_pins():
    # Fails if the operator is shown a SHA other than the one GitHub will enforce
    # (Codex #503 threads Dr1 / TGt).
    # A pinned merge prompts, beside an admin merge too, and must name its SHA.
    block = _reason(f"git show {OLD} && {MERGE} 501 {PIN} && {ADMIN}")
    assert block["permissionDecision"] == "ask"
    assert SHA in block["permissionDecisionReason"]
    assert OLD not in block["permissionDecisionReason"]


def test_prompt_names_every_act_and_sha_in_one_call():
    # Fails if one approval covers an operator act the prompt does not name.
    two = _reason(f"{ADMIN} && {MERGE} 502 --match-head-commit {OLD}")
    assert SHA in two["permissionDecisionReason"] and OLD in two["permissionDecisionReason"]
    assert "pr.merge" in two["permissionDecisionReason"]


@pytest.mark.parametrize("command,expected", [
    (f"{MERGE} 501 {PIN} --match-head-commit ''", ("deny", "pr.merge_unpinned")),
    (f"{MERGE} 501 --match-head-commit abc {PIN}", ("ask", "pr.merge")),
])
def test_repeated_pin_uses_the_last_value(command, expected):
    # Fails if the guard reads a different `--match-head-commit` than gh does (pflag:
    # last wins), so an empty final pin would merge unpinned behind an approved SHA.
    assert g.classify_command(command) == expected


@pytest.mark.parametrize("command,expected", [
    (f"{MERGE} 501 --disable-auto", None),
    (f"{MERGE} 501 --disable-auto=true", None),
    (f"{MERGE} 501 --disable-auto=false --squash", ("deny", "pr.merge_unpinned")),
    (f"{MERGE} 501 --disable-auto --auto", ("deny", "pr.auto_merge")),
])
def test_disabling_auto_merge_is_silent(command, expected):
    # Fails if the risk-reducing `--disable-auto` (gh returns before merging) is refused
    # as a merge, or a false-valued one hides a real merge (Codex #503 thread DsI).
    assert g.classify_command(command) == expected


@pytest.mark.parametrize("command", [
    "gh api graphql --input payload.json",
    "gh api graphql -F query=@payload.graphql",
    "gh api graphql --field=query=@payload.graphql",
    "gh api -X PUT repos/o/r/pulls/501/" + f"merge --input body.json -f sha={SHA}",
])
def test_opaque_request_bodies_are_refused(command):
    # Fails if a body the guard cannot read (a file) can carry a merge or auto-merge
    # past it (Codex #503 thread TGi).
    assert g.classify_command(command) == ("deny", "pr.merge_unpinned")


@pytest.mark.parametrize("command", [
    "gh api graphql -f query='query { viewer { login } }'",
    "gh api graphql -F owner=o -f query='query($owner: String!) { user(login: $owner) { id } }'",
    "gh api repos/o/r/pulls/501",
])
def test_readable_non_merge_api_calls_are_silent(command):
    # Fails if ordinary API reads are refused along with opaque bodies.
    assert g.classify_command(command) is None


GQL_MERGE = "PullRequest"  # concatenated below so no source line is itself a mutation


@pytest.mark.parametrize("query,fields", [
    (f'# expectedHeadOid: "{SHA}"\nmutation {{ merge{GQL_MERGE}(input: {{pullRequestId: "x"}}) {{ x }} }}', ""),
    (f'mutation {{ merge{GQL_MERGE}(input: {{pullRequestId: "x", commitHeadline: "expectedHeadOid: {SHA}"}}) {{ x }} }}', ""),
    (f'mutation {{ merge{GQL_MERGE}(input: {{pullRequestId: "x"}}) {{ x }} }}', f" -F expectedHeadOid={SHA}"),
    (f'mutation {{ a: merge{GQL_MERGE}(input: {{pullRequestId: "x", expectedHeadOid: "{SHA}"}}) {{ x }} '
     f'b: merge{GQL_MERGE}(input: {{pullRequestId: "y"}}) {{ x }} }}', ""),
])
def test_graphql_pin_must_be_structurally_active(query, fields):
    # Fails if a pin in a comment, inside a string, in an unused variable, or on only one
    # of two merges is accepted (Codex #503 thread TGo).
    command = f"gh api graphql -f query='{query}'{fields}"
    assert g.classify_command(command) == ("deny", "pr.merge_unpinned")


@pytest.mark.parametrize("query,fields", [
    (f'mutation($oid: GitObjectID!) {{ merge{GQL_MERGE}(input: {{pullRequestId: "x", '
     f'expectedHeadOid: $oid}}) {{ x }} }}', f" -f oid={SHA}"),
    (f'mutation($in: Merge{GQL_MERGE}Input!) {{ merge{GQL_MERGE}(input: $in) {{ x }} }}',
     f" -F 'in[pullRequestId]=x' -F 'in[expectedHeadOid]={SHA}'"),
])
def test_graphql_pin_through_variables_asks(query, fields):
    # Fails if a merge pinned through a GraphQL variable is refused as unpinned.
    command = f"gh api graphql -f query='{query}'{fields}"
    assert g.classify_command(command) == ("ask", "pr.merge")


@pytest.mark.parametrize("command,expected", [
    ("gh api -X PUT repos/o/r/pulls/501/" + f"merge -H sha={SHA}", ("deny", "pr.merge_unpinned")),
    ("gh api -X PUT repos/o/r/pulls/501/" + f"merge --raw-field=sha={SHA}", ("ask", "pr.merge")),
    ("gh api -X PUT repos/o/r/pulls/501/" + f"merge -F sha={SHA}", ("ask", "pr.merge")),
    ("gh api -X PUT repos/o/r/pulls/501/" + f"merge -f=sha={SHA}", ("ask", "pr.merge")),
])
def test_rest_pin_must_be_a_request_field(command, expected):
    # Fails if a `sha=` that is not a request field (a header) is taken as the pin.
    assert g.classify_command(command) == expected


@pytest.mark.parametrize("command", [
    f"pwsh -File ./fp.ps1 {ADMIN}",
    f"./fp.ps1 {ADMIN}",
    f"powershell -NoProfile -ExecutionPolicy Bypass -File fp.ps1 {ADMIN}",
])
def test_launcher_asks(command):
    # Fails if the repository's own launcher (`fp.ps1`, via pwsh or directly) hides an
    # operator act from the prompt (Codex #503 thread TG-).
    assert g.classify_command(command) == ("ask", "pr.merge_admin")


@pytest.mark.parametrize("command", [
    "./fp.ps1 test",
    "pwsh -File ./fp.ps1 doctor",
    "pwsh -NoProfile -Command 'git status'",
])
def test_launcher_exits_and_checks_are_silent(command):
    # Fails if the launcher's ordinary commands prompt.
    assert g.classify_command(command) is None


def _encoded(command: str) -> str:
    import base64
    return base64.b64encode(command.encode("utf-16-le")).decode()


@pytest.mark.parametrize("command,expected", [
    (f"pwsh -NoProfile -Command '{MERGE} 501 --auto'", ("deny", "pr.auto_merge")),
    ("powershell -c git push origin main", ("deny", "main.direct_push")),
    (f"pwsh -EncodedCommand {_encoded(MERGE + ' 501 --auto')}", ("deny", "pr.auto_merge")),
])
def test_powershell_wrappers_are_read(command, expected):
    # Fails if wrapping a forbidden act in a PowerShell command line hides it.
    assert g.classify_command(command) == expected


def test_powershell_tool_calls_are_judged():
    # Fails if the Claude Code PowerShell tool reaches `gh`/`git` without the guard.
    call = {"tool_name": "PowerShell", "tool_input": {"command": f"{MERGE} 501 --auto"}}
    assert g.classify(call) == ("deny", "pr.auto_merge")
    pinned = {"tool_name": "PowerShell", "tool_input": {"command": f"{MERGE} 501 {PIN}"}}
    assert g.classify(pinned) == ("ask", "pr.merge")


@pytest.mark.parametrize("command,expected", [
    (f"Set-Location C:\\repo; .\\fp.ps1 {ADMIN}", ("ask", "pr.merge_admin")),
    ("C:\\tools\\gh.exe pr " + "merge 501 --auto", ("deny", "pr.auto_merge")),
    ("Set-Location C:\\repo; .\\fp.ps1 python -m pytest tests\\scripts", None),
])
def test_powershell_backslash_paths_are_read_as_paths(command, expected):
    # Fails if a PowerShell path (`.\fp.ps1`, `C:\tools\gh.exe`) loses its separators to
    # POSIX backslash escaping and hides the program it runs.
    assert g.classify({"tool_name": "PowerShell", "tool_input": {"command": command}}) == expected


# --- 2026-09-25 verifier round on fd126c3: argv is read the way gh (cobra/pflag) and pwsh
# read it, and a flag whose arity the guard cannot know is read both ways. ---

LAUNCH_ADMIN = f"-File ./fp.ps1 {ADMIN}"
UNPINNED_Q = "mutation { merge" + GQL_MERGE + '(input: {pullRequestId: "x"}) { x } }'
PINNED_Q = ("mutation { merge" + GQL_MERGE
            + f'(input: {{pullRequestId: "x", expectedHeadOid: "{SHA}"}}) {{ x }} }}')


@pytest.mark.parametrize("command,expected", [
    (f"pwsh -ep Bypass {LAUNCH_ADMIN}", ("ask", "pr.merge_admin")),
    (f"pwsh -wd . {LAUNCH_ADMIN}", ("ask", "pr.merge_admin")),
    (f"pwsh -of Text {LAUNCH_ADMIN}", ("ask", "pr.merge_admin")),
    (f"pwsh -if Text {LAUNCH_ADMIN}", ("ask", "pr.merge_admin")),
    (f"pwsh -ea x {LAUNCH_ADMIN}", ("ask", "pr.merge_admin")),
    (f"pwsh -ep Bypass -c '{MERGE} 1'", ("deny", "pr.merge_unpinned")),
    (f"pwsh -i -ec {_encoded(MERGE + ' 1 --auto')}", ("deny", "pr.auto_merge")),
    (f"pwsh -NewParam x -c '{MERGE} 1'", ("deny", "pr.merge_unpinned")),
    (f"powershell -Version 5.1 -c '{MERGE} 1'", ("deny", "pr.merge_unpinned")),
    (f"pwsh -cwa '{MERGE} 1 --auto'", ("deny", "pr.auto_merge")),
])
def test_powershell_parameters_are_read_as_pwsh_reads_them(command, expected):
    # Fails if a pwsh alias that is not a prefix of its name (`-ep`, `-wd`, `-of`, `-if`,
    # `-ea`), a switch, an unknown parameter or `-CommandWithArgs` makes the guard read a
    # parameter value as the script and skip the act (verifier round on fd126c3).
    assert g.classify_command(command) == expected


def test_powershell_tool_launcher_with_execution_policy_asks():
    # Fails if the common Windows idiom `-ep Bypass` hides an act from the PowerShell tool.
    command = f"pwsh -ep Bypass -File .\\fp.ps1 {ADMIN}"
    assert g.classify({"tool_name": "PowerShell", "tool_input": {"command": command}}) == (
        "ask", "pr.merge_admin")


@pytest.mark.parametrize("command", [
    "pwsh -ep Bypass -File ./fp.ps1 test",
    "pwsh -NoProfile -ep Bypass -c 'git status'",
    "pwsh -i -wd . -c 'gh pr view 501'",
])
def test_powershell_parameter_reading_stays_silent_on_checks(command):
    # Fails if reading pwsh parameters both ways makes an ordinary check prompt.
    assert g.classify_command(command) is None


@pytest.mark.parametrize("command", [
    "gh api -iX POST graphql --input p.json",
    "gh api -iq . graphql --input p.json",
    "gh api -iX POST graphql -F query=@q.graphql",
    "gh api -XPOST graphql --input p.json",
    "gh -X POST api graphql --input p.json",
])
def test_clustered_short_options_are_read_as_pflag_reads_them(command):
    # Fails if a value shorthand inside a cluster (`-iX POST`) is taken as the endpoint and
    # an unreadable GraphQL body goes through silently (verifier round on fd126c3).
    assert g.classify_command(command) == ("deny", "pr.merge_unpinned")


@pytest.mark.parametrize("spoof", ["-iq", "-ip", "--preview", "-t", "--jq", "-H"])
def test_a_pin_inside_another_options_value_is_not_a_pin(spoof):
    # Fails if a pinned query that gh reads as the value of another option (jq, preview,
    # template, header) makes the guard ask and show a SHA while gh sends the unpinned one.
    command = f"gh api graphql -f query='{UNPINNED_Q}' {spoof} '-fquery={PINNED_Q}'"
    assert g.classify_command(command) == ("deny", "pr.merge_unpinned")


@pytest.mark.parametrize("command,expected", [
    (f"{MERGE} 501 -b --disable-auto --squash", ("deny", "pr.merge_unpinned")),
    (f"{MERGE} 501 -sb --disable-auto", ("deny", "pr.merge_unpinned")),
    (f"{MERGE} 501 --subject --disable-auto", ("deny", "pr.merge_unpinned")),
    (f"{MERGE} 501 -t --match-head-commit={SHA}", ("deny", "pr.merge_unpinned")),
    (f"{MERGE} 501 -b --auto", ("deny", "pr.merge_unpinned")),
    (f"{MERGE} 501 --no-such-flag {PIN}", ("deny", "pr.merge_unpinned")),
    (f"{MERGE} 501 -sd {PIN}", ("ask", "pr.merge")),
    (f"{MERGE} 501 -s -t 'Title' -b 'Body' {PIN}", ("ask", "pr.merge")),
    (f"{MERGE} 501 --help", None),
])
def test_merge_options_are_read_as_pflag_reads_them(command, expected):
    # Fails if a word gh reads as another option's value (`-b --disable-auto`, `-t
    # --match-head-commit=…`) is taken as the flag it spells, so a merge runs silently or
    # under a pin gh never sends; or if an unknown flag lets the guard trust its reading.
    assert g.classify_command(command) == expected


@pytest.mark.parametrize("command,expected", [
    ("gh -b x pr " + "merge 501", ("deny", "pr.merge_unpinned")),
    ("gh -A a@b pr " + "merge 501 --auto", ("deny", "pr.auto_merge")),
    ("gh --subject s pr " + "merge 501 --auto", ("deny", "pr.auto_merge")),
    (f"gh --match-head-commit {SHA} pr " + "merge 501", ("ask", "pr.merge")),
    ("gh --no-such-flag v pr " + "merge 501", ("deny", "pr.merge_unpinned")),
    ("gh -R o/r pr view 501", None),
    # While cobra looks for the subcommand only -h/--help/--version are booleans at the
    # root (-h/--help under `pr`); every other flag takes the next word, even one the
    # merge or api command reads as a boolean (verifier blocker on d24f84b).
    ("gh --admin 501 pr " + "merge", ("deny", "pr.merge_unpinned")),
    ("gh -d 501 pr " + "merge", ("deny", "pr.merge_unpinned")),
    ("gh --auto 501 pr " + "merge", ("deny", "pr.auto_merge")),
    ("gh pr --auto 501 " + "merge", ("deny", "pr.auto_merge")),
    (f"gh --admin 501 pr merge {PIN}", ("ask", "pr.merge_admin")),
    ("gh -i repos/o/r/pulls/1/" + "merge api -X PUT", ("deny", "pr.merge_unpinned")),
    ("gh --silent repos/o/r/pulls/1/" + "merge api -X PUT", ("deny", "pr.merge_unpinned")),
    ("gh -i graphql api -f query='mutation { merge" + "PullRequest(input: {}) { x } }'",
     ("deny", "pr.merge_unpinned")),
    # The looser reading this hook used at 7cfd367 is kept alongside cobra's.
    ("gh -q pr " + "merge 1", ("deny", "pr.merge_unpinned")),
])
def test_flags_before_the_command_path_are_read_as_cobra_reads_them(command, expected):
    # Fails if a merge flag written before `pr merge` (cobra accepts it there) hides the
    # merge, including a forbidden auto-merge (found in the fd126c3 re-check), or if a
    # boolean of the merge command is taken as one before the subcommand is found.
    assert g.classify_command(command) == expected


@pytest.mark.parametrize("command,expected", [
    ("git --attr-source HEAD push origin main", ("deny", "main.direct_push")),
    ("git --no-such-option v push origin main", ("deny", "main.direct_push")),
    ("git --attr-source HEAD push origin claude/x", None),
])
def test_git_global_options_are_read_both_ways(command, expected):
    # Fails if a git global option the guard does not list (`--attr-source <tree>`, which
    # git 2.50 accepts) hides the `push` subcommand (found in the fd126c3 re-check).
    assert g.classify_command(command) == expected


def test_unreadable_push_to_heads_main_fails_closed():
    # Fails if the fallback misses a `heads/main` destination that the strict reading
    # denies (verifier round on fd126c3).
    command = 'echo "$(case x in x) echo ok;; esac)" && git push origin HEAD:heads/main'
    assert g.classify_command(command) == ("deny", "main.direct_push")


@pytest.mark.parametrize("command,expected", [
    ("gh pr `" + "merge 1", ("deny", "pr.merge_unpinned")),
    ("git push origin `main", ("deny", "main.direct_push")),
    ("g`h pr " + "merge 501 `-`-auto", ("deny", "pr.auto_merge")),
    ("gh pr m`u{65}rge 501", ("deny", "pr.merge_unpinned")),
    ('pwsh -c "echo x`ngh pr ' + 'merge 1"', ("deny", "pr.merge_unpinned")),
    ("gh pr " + f"merge 501 `\n  {PIN}", ("ask", "pr.merge")),
    ('git commit -m "say `"gh pr ' + 'merge`" later"', None),
    ("Write-Output a`tb", None),
])
def test_powershell_backtick_escapes_are_resolved(command, expected):
    # Fails if a PowerShell backtick escape (`` `m `` is `m`, `` `n `` a newline,
    # `` `u{65} `` an `e`, a backtick at a line end continues the line) hides an act, or if
    # an escaped quote inside a message turns data into a command (verifier round on fd126c3).
    assert g.classify({"tool_name": "PowerShell", "tool_input": {"command": command}}) == expected


@pytest.mark.parametrize("command,expected", [
    ("gh api -X PUT repos/o/r/pulls//1/" + "merge", ("deny", "pr.merge_unpinned")),
    ("gh api -X PUT repos/o/r/pulls/1//" + f"merge -f sha={SHA}", ("ask", "pr.merge")),
])
def test_merge_path_with_repeated_slashes_is_a_merge(command, expected):
    # Fails if a doubled slash takes a REST merge path out of the guard's reading.
    assert g.classify_command(command) == expected


@pytest.mark.parametrize("command,expected", [
    ("pwsh -c " * 40 + f"'{MERGE} 1'", ("deny", "pr.merge_unpinned")),
    ("gh " + "-x w " * 120 + "pr " + "merge 1", ("deny", "pr.merge_unpinned")),
])
def test_reading_every_way_stays_bounded(command, expected):
    # Fails if following every reading of ambiguous parameters grows exponentially, so a
    # constructed command stalls the hook instead of being judged.
    import time
    start = time.perf_counter()
    assert g.classify_command(command) == expected
    assert time.perf_counter() - start < 5


# --- 2026-09-25 babysit repairs (Codex review of #503 at a230f8b) ---

@pytest.mark.parametrize("command", [
    "git push --dry-run origin main",
    "git push -n origin main",
    "git push origin main --dry-run",
    "git push --dry origin main",
    "git push --dr origin HEAD:main",
    "git push -nu origin main",
    "git push -vn --force origin main",
    "git push --no-dry-run --dry-run origin main",
    "git push -n --mirror origin",
    "git push -n origin --delete main",
    "git -C /repo push -n origin main",
])
def test_dry_run_push_to_main_is_silent(command):
    # Fails if a push git only simulates (`--dry-run` / `-n` effective last, git's
    # abbreviations and short clusters included) is refused as main.direct_push
    # (Codex #503, 4109427044).
    assert g.classify_command(command) is None


@pytest.mark.parametrize("command", [
    "git push --dry-run --no-dry-run origin main",
    "git push -n --no-dry origin main",
    "git push --no-dry-run origin main",
    "git push -o -n origin main",
    "git push --push-option -n origin main",
    "git push -on origin main",
    "git push --dry-run=yes origin main",
    "git push --d origin main",
    "git push origin main -- -n",
])
def test_push_that_is_not_a_dry_run_is_still_judged(command):
    # Fails if a dry-run reading silences a real push: a later `--no-dry-run`, a `-n`
    # that is another option's value, an ambiguous abbreviation, or a word after `--`.
    assert g.classify_command(command) == ("deny", "main.direct_push")


@pytest.mark.parametrize("command,expected", [
    (f"{MERGE} 501 --auto=false {PIN}", ("ask", "pr.merge")),
    (f"{MERGE} 501 --auto=0 {PIN}", ("ask", "pr.merge")),
    (f"{MERGE} 501 --auto=f {PIN}", ("ask", "pr.merge")),
    (f"{MERGE} 501 --auto=F {PIN}", ("ask", "pr.merge")),
    (f"{MERGE} 501 --auto=FALSE {PIN}", ("ask", "pr.merge")),
    (f"{MERGE} 501 --auto=False {PIN}", ("ask", "pr.merge")),
    (f"{MERGE} 501 --auto --auto=false {PIN}", ("ask", "pr.merge")),
    (f"{MERGE} 501 --auto=false --squash", ("deny", "pr.merge_unpinned")),
    ("gh --auto=false pr " + f"merge 501 {PIN}", ("ask", "pr.merge")),
    (f"{MERGE} 501 --auto {PIN}", ("deny", "pr.auto_merge")),
    (f"{MERGE} 501 --auto=true {PIN}", ("deny", "pr.auto_merge")),
    (f"{MERGE} 501 --auto=1 {PIN}", ("deny", "pr.auto_merge")),
    (f"{MERGE} 501 --auto=false --auto {PIN}", ("deny", "pr.auto_merge")),
    (f"{MERGE} 501 --auto=yes {PIN}", ("deny", "pr.auto_merge")),
])
def test_explicit_false_auto_is_judged_as_a_merge(command, expected):
    # Fails if `--auto=false` (pflag's false spellings, last value wins) is refused as
    # auto-merge instead of being judged as the pinned or unpinned merge it is, or if
    # any value that is not a false spelling stops being refused (Codex #503, 4109427036).
    assert g.classify_command(command) == expected


# --- 2026-09-25 babysit repairs (Codex review of #503 at a80f819, 4109578933 / 4109578936) ---

@pytest.mark.parametrize("command", [
    "git push --all --no-all origin feature",
    "git push --branches --no-branches origin claude/x",
    "git push --all --no-branches origin claude/x",
    "git push --branches --no-al origin claude/x",
    "git push --al --no-all origin claude/x",
    "git push --mirror --no-mirror origin claude/x",
    "git push --mirr --no-m origin claude/x",
    "git push --all --mirror --no-mirror --no-all origin claude/x",
])
def test_negated_bulk_push_is_silent(command):
    # Fails if a bulk option that a later `--no-…` form clears (git's last-wins; `--branches`
    # is git's alias of `--all`, so either negation clears either) is still refused as
    # main.direct_push (Codex #503, 4109578933; checked against git 2.50 on a local remote).
    assert g.classify_command(command) is None


@pytest.mark.parametrize("command", [
    "git push --no-all --all origin",
    "git push --no-mirror --mirror origin",
    "git push --all --no-mirror origin claude/x",
    "git push --mirror --no-all origin claude/x",
    "git push --all --no-all origin main",
    "git push --all --no-a origin claude/x",
    "git push --all --no-all=x origin claude/x",
    "git push --all -o --no-all origin claude/x",
    "git push --all --push-option --no-all origin claude/x",
    "git push --all origin claude/x -- --no-all",
])
def test_bulk_push_not_cleared_is_still_denied(command):
    # Fails if a negation that git does not apply to the bulk option — an earlier one, one
    # for the other bulk bit, an ambiguous abbreviation, one carrying a value, another
    # option's value, or a word after `--` — silences a push that reaches main.
    assert g.classify_command(command) == ("deny", "main.direct_push")


# --- 2026-09-25 babysit repairs (Codex review of #503 at 8bb2e32, 4109815693 / 4109815694) ---

@pytest.mark.parametrize("command", [
    "git push --all -ox --no-all origin feature",
    "git push --all -vox --no-all origin claude/x",
    "git push --mirror -o=x --no-mirror origin claude/x",
    "git push --all --push-option=x --no-all origin claude/x",
])
def test_negation_after_an_attached_push_option_value_is_read(command):
    # Fails if `-ox` (the value `x` attached to `-o`) is read as taking the next word, so
    # the `--no-all` after it is skipped and the push refused (Codex #503, 4109815693;
    # git 2.50 on a local remote pushes only `feature`). Only a final `o` in a short
    # cluster takes the next word.
    assert g.classify_command(command) is None


@pytest.mark.parametrize("command", [
    "git push --all -vo --no-all origin claude/x",
    "git push --all -o --no-all origin claude/x",
    "git push -ox origin main",
    "git push -vo x origin main",
    "git push --push-opt x origin main",
    "git push --rec check origin HEAD:main",
])
def test_push_option_values_do_not_hide_main(command):
    # Fails if a push-option value (a final `o` taking the next word, or a long value
    # option in an abbreviation git accepts) silences a push that reaches main.
    assert g.classify_command(command) == ("deny", "main.direct_push")


@pytest.mark.parametrize("command", [
    "git push -vo x main",
    "git push --push-opt x main",
    "git push --rec check main",
    "git push --repo=origin main",
    "git push --repo origin main",
])
def test_push_repository_word_is_not_a_refspec(command):
    # Fails if a value option's value is taken for the repository, so the repository
    # word (a remote named `main`) is refused as a refspec; or if `--repo` is read as
    # turning the repository word into a refspec: git reads the first positional as the
    # repository whatever `--repo` says (git 2.50: `git push -n --repo=origin main` looks
    # for a repository called `main`). Same class as 4109815693.
    assert g.classify_command(command) is None


# --- 2026-09-25 verifier follow-up on the 4109815694 repair (`--` taken as a value) ---


# --- 2026-09-26 babysit repair (verifier on eb565d1: bulk word in value position) ---

@pytest.mark.parametrize("command", [
    "git push -o --all origin feature",
    "git push --push-option --all origin feature",
    "git push -vo --mirror origin feature",
    "git push --repo --all origin feature",
    "git push origin feature -o --all",
    "git push --push-opt --branches origin feature",
    "git push origin feature -- --all",
])
def test_bulk_word_as_an_option_value_is_not_a_bulk_push(command):
    # Fails if a bulk-looking word that git reads as a value option's value (`-o --all`
    # sends the push option `--all`; `--repo --all` names a repository) or as a word after
    # `--` is still read as a bulk push, so a push of `feature` is refused as
    # main.direct_push.
    assert g.classify_command(command) is None


@pytest.mark.parametrize("command", [
    "git push --all origin",
    "git push --all -o x origin",
    "git push -o x --all origin",
    "git push -ox --all origin",
    "git push --push-option=x --mirror origin",
    "git push -o --all origin main",
    "git push --repo --all origin main",
    "git push origin main -- --all",
    "git push --all origin main",
])
def test_bulk_push_in_option_position_is_still_denied(command):
    # Fails if a bulk option in option position — before or after a value option whose
    # value is already given — stops being refused, or if a push that names main as a
    # refspec is silenced because a bulk-looking word beside it is a value.
    assert g.classify_command(command) == ("deny", "main.direct_push")


@pytest.mark.parametrize("command,expected", [
    ('echo `date`; git push origin ma""in', ("deny", "main.direct_push")),
    ("echo `date`; g''it push origin main", ("deny", "main.direct_push")),
    ("echo `date`; gh pr me''rge 5", ("deny", "pr.merge_unpinned")),
    ("echo `date`; " + ADMIN.replace("--admin", "--adm''in"), ("ask", "pr.merge_admin")),
    ("echo `date`; git commit -m 'mention git push origin main'", None),
    ("grep -n `echo gh` merge.md", None),
    ("echo `" + ADMIN + "`", ("ask", "pr.merge_admin")),
])
def test_backquotes_are_read_not_dropped_to_raw_patterns(command, expected):
    # Fails if a backquote substitution (whose re-parsed words carry no source span)
    # drops the whole command to the raw-pattern fallback: quote-split acts would be
    # missed and mentions in data would decide.
    assert g.classify_command(command) == expected


@pytest.mark.parametrize("command", [
    f"{MERGE} 501 {PIN} && {ADMIN}",
    f"bash -c '{MERGE} 501 {PIN}; {ADMIN}'",
])
def test_allowed_merge_cannot_launder_an_operator_act(command):
    # Fails if a merge earlier in a call lets another operator act run without a prompt.
    assert g.classify_command(command)[0] == "ask"


def test_bundled_merge_still_asks():
    # Fails if a pinned merge bundled with an unrecognised command goes through without
    # Joshua's prompt, or emits an allow that would skip normal permission evaluation for
    # the whole call (Codex #902).
    block = _reason(f"{MERGE} 501 {PIN} && python scripts/anything.py")
    assert block["permissionDecision"] == "ask"
    assert "independent review" in block["additionalContext"]


# --- 2026-10-25: pinned --admin merges ask (operator ruling 2026-09-26) ---

@pytest.mark.parametrize("command,expected", [
    (f"{MERGE} 501 --admin --merge {PIN}", ("ask", "pr.merge_admin")),
    (f"{MERGE} 501 --admin=true {PIN}", ("ask", "pr.merge_admin")),
    (f"{MERGE} 501 --admin=false --admin {PIN}", ("ask", "pr.merge_admin")),
    (f"bash -c '{MERGE} 501 --admin {PIN}'", ("ask", "pr.merge_admin")),
    (f"{MERGE} 501 --admin --admin=false {PIN}", ("ask", "pr.merge")),
    (f"{MERGE} 501 --admin", ("deny", "pr.merge_unpinned")),
    (f"{MERGE} 501 --admin {PIN} && {MERGE} 502 --auto", ("deny", "pr.auto_merge")),
])
def test_pinned_admin_merge_asks(command, expected):
    # Fails if a pinned `--admin` merge is not put to Joshua as an admin merge: it merges
    # past unmet requirements ("askable admin merges", 2026-09-26;
    # merge-train hard rule 5), or if the ask outranks an unpinned or auto-merge deny.
    assert g.classify_command(command) == expected


def test_admin_merge_prompt_names_the_sha():
    # Fails if the operator approves an admin merge without seeing the head it pins.
    block = _reason(f"{MERGE} 501 --admin {PIN}")
    assert block["permissionDecision"] == "ask"
    assert "pr.merge_admin" in block["permissionDecisionReason"]
    assert SHA in block["permissionDecisionReason"]


@pytest.mark.parametrize("command,expected", [
    (f"fly ssh console -a host -C '{MERGE} 1'", ("deny", "pr.merge_unpinned")),
    (f"fly ssh console -a host -sC '{MERGE} 1'", ("deny", "pr.merge_unpinned")),
    (f"fly ssh console -a host -C'{MERGE} 1'", ("deny", "pr.merge_unpinned")),
    (f"fly ssh console -a host --command='{ADMIN}'", ("ask", "pr.merge_admin")),
    ("fly ssh console -a host -C 'ls'", None),
    ("fly status -a host", None),
])
def test_fly_ssh_command_is_judged(command, expected):
    # Fails if an act run on a remote machine through `fly ssh console -C` goes unread.
    assert g.classify_command(command) == expected
