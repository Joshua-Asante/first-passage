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
DEPLOY = "fly " + "deploy"
ARM = "python ops/c1_rail/c1_rail_arm.py --" + "arm"
SHA = "0123456789abcdef0123456789abcdef01234567"
PIN = f"--match-head-commit {SHA}"


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
    # Fails if a merge pinned to a head SHA runs without an operator prompt.
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
    f"sh -c '{DEPLOY}; {MERGE} 502 --auto'",
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
    # Fails if auto-merge (retired, no automated exception) is merely asked, not refused.
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
    f"{DEPLOY} -a c1-rail",
    "flyctl -a c1-rail " + "deploy --image x",
])
def test_rail_deploy_asks(command):
    # Fails if a c1 rail deploy can run without an operator prompt.
    assert g.classify_command(command) == ("ask", "rail.deploy")


@pytest.mark.parametrize("command", [
    f"{ARM} --hours 4",
    "python3 -m ops.c1_rail.c1_rail_arm --" + "arm",
    "fly ssh console -a c1-rail -C '" + ARM + "'",
])
def test_arm_asks(command):
    # Fails if arming the rail can run without an operator prompt.
    assert g.classify_command(command) == ("ask", "rail.arm")


@pytest.mark.parametrize("command", [
    "python ops/c1_rail/c1_rail_arm.py --disarm",
    "python ops/c1_rail/c1_rail_arm.py --status",
    "fly ssh console -a c1-rail -C 'python ops/c1_rail/c1_rail_arm.py --disarm'",
    "fly status -a c1-rail",
    "gh pr view 501",
    "gh pr create --title 'do not " + MERGE + " yet' --body x",
    f"git commit -m 'document {MERGE} and {DEPLOY}'",
    f"grep -rn '{MERGE}' docs/",
    f"echo '{ARM}'",
])
def test_data_and_risk_reducing_exits_are_silent(command):
    # Fails if disarm/status waits on a prompt, or if text that only mentions an act asks
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
    "git push --repo=origin main",
    "git push --repo origin main",
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
    assert block["permissionDecision"] == "ask"
    assert SHA in block["permissionDecisionReason"]  # the operator sees what they approve
    assert _run(json.dumps({"tool_name": "Bash", "tool_input": {"command": "ls"}})) == ""
    assert _run("not json") == ""


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
    block = _reason(f"git show {OLD} && {MERGE} 501 {PIN}")
    assert block["permissionDecision"] == "ask"
    assert SHA in block["permissionDecisionReason"]
    assert OLD not in block["permissionDecisionReason"]


def test_prompt_names_every_act_and_sha_in_one_call():
    # Fails if one approval covers an operator act the prompt does not name.
    two = _reason(f"{MERGE} 501 {PIN} && {MERGE} 502 --match-head-commit {OLD}")
    assert SHA in two["permissionDecisionReason"] and OLD in two["permissionDecisionReason"]
    mixed = _reason(f"{DEPLOY} -a c1-rail && {MERGE} 501 {PIN}")
    assert "rail.deploy" in mixed["permissionDecisionReason"]
    assert "pr.merge" in mixed["permissionDecisionReason"]
    assert SHA in mixed["permissionDecisionReason"]


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
    "pwsh -File ./fp.ps1 python ops/c1_rail/c1_rail_arm.py --" + "arm",
    "./fp.ps1 python ops/c1_rail/c1_rail_arm.py --" + "arm",
    "powershell -NoProfile -ExecutionPolicy Bypass -File fp.ps1 python -m ops.c1_rail.c1_rail_arm --" + "arm",
    "python ops/c1_rail/c1_rail_arm.py --" + "ar",
    "python -I scripts/fp.py python ops/c1_rail/c1_rail_arm.py --" + "arm",
])
def test_launcher_and_abbreviated_arm_ask(command):
    # Fails if the repository's own launcher (`fp.ps1`, via pwsh or directly) or
    # argparse's `--ar` abbreviation arms the rail without an operator prompt
    # (Codex #503 thread TG-; `--ar` found in the babysit re-check).
    assert g.classify_command(command) == ("ask", "rail.arm")


@pytest.mark.parametrize("command", [
    "./fp.ps1 python ops/c1_rail/c1_rail_arm.py --disarm",
    "python ops/c1_rail/c1_rail_arm.py --dis",
    "./fp.ps1 test",
    "pwsh -File ./fp.ps1 doctor",
    "pwsh -NoProfile -Command 'git status'",
])
def test_launcher_exits_and_checks_are_silent(command):
    # Fails if the launcher's ordinary commands or a disarm through it prompt.
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
    ("Set-Location C:\\repo; .\\fp.ps1 python ops\\c1_rail\\c1_rail_arm.py --" + "arm",
     ("ask", "rail.arm")),
    ("C:\\tools\\gh.exe pr " + "merge 501 --auto", ("deny", "pr.auto_merge")),
    ("Set-Location C:\\repo; .\\fp.ps1 python -m pytest tests\\scripts", None),
])
def test_powershell_backslash_paths_are_read_as_paths(command, expected):
    # Fails if a PowerShell path (`.\fp.ps1`, `C:\tools\gh.exe`) loses its separators to
    # POSIX backslash escaping and hides the program it runs.
    assert g.classify({"tool_name": "PowerShell", "tool_input": {"command": command}}) == expected


@pytest.mark.parametrize("flag", ["--acknowledge-m1-unresolved 'attended test'",
                                  "--ack 'attended test'"])
def test_m1_override_prompt_does_not_claim_resolved(flag):
    # Fails if an arm that bypasses an unresolved M1 is put to the operator under a prompt
    # that says M1 is RESOLVED (Codex #503 thread Dr-; whether to refuse it outright
    # is an operator decision, so it still asks).
    command = f"{ARM} --hours 4 {flag}"
    assert g.classify_command(command) == ("ask", "rail.arm")
    reason = _reason(command)["permissionDecisionReason"]
    assert "UNRESOLVED" in reason and "acknowledge-m1-unresolved" in reason
    assert "M1 RESOLVED and a GO" not in reason


# --- 2026-09-25 verifier round on fd126c3: argv is read the way gh (cobra/pflag) and pwsh
# read it, and a flag whose arity the guard cannot know is read both ways. ---

LAUNCH_ARM = "-File ./fp.ps1 python ops/c1_rail/c1_rail_arm.py --" + "arm"
UNPINNED_Q = "mutation { merge" + GQL_MERGE + '(input: {pullRequestId: "x"}) { x } }'
PINNED_Q = ("mutation { merge" + GQL_MERGE
            + f'(input: {{pullRequestId: "x", expectedHeadOid: "{SHA}"}}) {{ x }} }}')


@pytest.mark.parametrize("command,expected", [
    (f"pwsh -ep Bypass {LAUNCH_ARM}", ("ask", "rail.arm")),
    (f"pwsh -wd . {LAUNCH_ARM}", ("ask", "rail.arm")),
    (f"pwsh -of Text {LAUNCH_ARM}", ("ask", "rail.arm")),
    (f"pwsh -if Text {LAUNCH_ARM}", ("ask", "rail.arm")),
    (f"pwsh -ea x {LAUNCH_ARM}", ("ask", "rail.arm")),
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
    # Fails if the common Windows idiom `-ep Bypass` hides an arm from the PowerShell tool.
    command = "pwsh -ep Bypass -File .\\fp.ps1 python ops\\c1_rail\\c1_rail_arm.py --" + "arm"
    assert g.classify({"tool_name": "PowerShell", "tool_input": {"command": command}}) == (
        "ask", "rail.arm")


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
    (f"gh --admin 501 pr merge {PIN}", ("ask", "pr.merge")),
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
    ("fly -t tok " + "deploy", ("ask", "rail.deploy")),
    ("fly --access-token tok " + "deploy", ("ask", "rail.deploy")),
    ("fly --no-such-flag v " + "deploy", ("ask", "rail.deploy")),
    (f"fly ssh console -a c1-rail -sC '{ARM}'", ("ask", "rail.arm")),
    (f"fly ssh console -a c1-rail -C'{ARM}'", ("ask", "rail.arm")),
    ("fly -t tok status -a c1-rail", None),
    ("fly ssh console -a c1-rail -sC 'python ops/c1_rail/c1_rail_arm.py --disarm'", None),
])
def test_fly_flags_are_read_as_cobra_reads_them(command, expected):
    # Fails if a global flag's value (`-t <token>`) or a shorthand cluster (`-sC '…'`)
    # hides a deploy or an arm (found in the fd126c3 re-check).
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
