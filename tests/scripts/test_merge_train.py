"""Tests for scripts/merge_train.py — the read-only merge gate and change watcher.

A fake ``gh`` runner returns canned JSON, so the suite needs no network or credentials.
Each case pins one clause of the merge rule (surface-allocation ADR Addendum 2026-10-24b A
and its 2026-10-25 amendment) or one failure the merge-train sessions hit by hand.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

_PATH = Path(__file__).resolve().parents[2] / "scripts" / "merge_train.py"
_spec = importlib.util.spec_from_file_location("merge_train", _PATH)
mt = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = mt
_spec.loader.exec_module(mt)

HEAD = "a1943a3ed9708e00716374cd56313bbf978ced7c"
OLD = "4499cb7e8ec534883b900be145955d36c4d0a084"
A, B, C, D = (c * 40 for c in "abcd")
BOT = mt.CODEX_BOT
OWNER = mt.DEFAULT_REPO.split("/")[0]
NOW = datetime(2026, 10, 25, 4, 0, tzinfo=timezone.utc)


def t(i: int, s: int = 0) -> str:
    return f"2026-10-25T05:{i:02d}:{s:02d}Z"


def card(sha: str, status: str, findings, since: str = "2026-10-25T03:25:05Z", any_=None) -> str:
    review = {"commit_sha": sha, "status": status, "has_unresolved_findings": findings}
    if any_ is not None:
        review["has_any_findings"] = any_
    running = (f'| **Running** since <relative-time datetime="{since}">x</relative-time> |'
               if status == "running" else "")
    return (f"<!-- codex-review-state:v1 {json.dumps({'code_review': review})} -->\n"
            f"## Codex Review Summary\n{running}")


def receipt(sha: str) -> str:
    return f"Codex Review: Didn't find any major issues.\n\n**Reviewed commit:** `{sha[:10]}`"


def cli(sha: str, verdict: str) -> str:
    return f"codex-cli-review:v1 {sha} {verdict}\n\nCodex CLI review (fallback) ..."


def timeline(*events) -> dict:
    """PR fields from events in time order. ("codex", sha, findings) is one connector review:
    a running then a completed version of the one summary card. ("running", sha, None) is a
    review still running. ("cli", sha, findings) is an owner CLI-fallback comment."""
    versions, human = [], []
    for i, (kind, sha, findings) in enumerate(events):
        if kind == "cli":
            human.append((OWNER, cli(sha, "findings" if findings else "clean"), t(i, 30)))
            continue
        versions.append((t(i), card(sha, "running", None)))
        if kind == "codex":
            versions.append((t(i, 30), card(sha, "completed", findings, any_=findings)))
    return {"bot": [{"history": versions}] if versions else [], "human": human}


def green(*names: str) -> list[dict]:
    return [{"name": n, "status": "COMPLETED", "conclusion": "SUCCESS"} for n in names]


class FakeGh:
    """Answers the calls fetch_gate makes, per PR number. A bot entry is a card body that
    was never edited, a plain comment body, or {"history": [(time, body), ...]}, whose last
    version is the current text; GitHub returns edit versions newest first."""

    def __init__(self, prs: dict[int, dict], thread_pages: int = 1, edit_page: int = 100):
        self.prs, self.thread_pages, self.edit_page, self.edits = prs, thread_pages, edit_page, {}

    def _comments(self, n: int) -> list[dict]:
        out = []
        for j, entry in enumerate(self.prs[n].get("bot", [])):
            versions = entry["history"] if isinstance(entry, dict) else [("2026-10-25T03:00:00Z", entry)]
            node = f"IC_{n}_{j}"
            self.edits[node] = versions if len(versions) > 1 else []
            rest = versions[entry.get("rest", -1)] if isinstance(entry, dict) else versions[-1]
            out.append({"id": 100 + j, "user": {"login": BOT}, "node_id": node, "body": rest[1],
                        "created_at": versions[0][0], "updated_at": rest[0]})
        for j, entry in enumerate(self.prs[n].get("human", [])):
            who, body, at, edited = (*entry, *("2026-10-25T03:00:00Z", None)[len(entry) - 2:])
            out.append({"id": 200 + j, "user": {"login": who}, "body": body, "created_at": at,
                        "updated_at": edited or at})
        return out

    def __call__(self, args: list[str]) -> str:
        if args[:2] == ["pr", "list"]:
            return json.dumps([{"number": n} for n in self.prs])
        if args[:2] == ["pr", "view"]:
            p = self.prs[int(args[2])]
            if p.get("raise"):
                raise RuntimeError("gh pr view failed: boom")
            return json.dumps({
                "number": int(args[2]), "title": p.get("title", "t"),
                "state": p.get("state", "OPEN"), "isDraft": p.get("draft", False),
                "baseRefName": p.get("base", "main"),
                "headRefOid": p.get("head", HEAD), "mergeStateStatus": p.get("merge", "CLEAN"),
                "statusCheckRollup": p.get("checks", green("skills (3.12)", "build (3.11)")),
            })
        if args[0] == "api" and args[-1].endswith("/comments"):
            return json.dumps([self._comments(int(args[-1].split("/")[-2]))])
        if args[0] == "api" and args[-1].endswith("/reviews"):
            return json.dumps([self.prs[int(args[-1].split("/")[-2])].get("reviews", [])])
        if args[:2] == ["api", "graphql"]:
            cursor = next((a.split("=", 1)[1] for a in args if a.startswith("c=")), None)
            page = int(cursor or 0)
            node = next((a.split("=", 1)[1] for a in args if a.startswith("id=")), None)
            if node:
                newest_first = [{"editedAt": v[0], "diff": v[1], "deletedAt": None,
                                 "editor": {"login": mt.CODEX_LOGIN}, **(v[2] if len(v) > 2 else {})}
                                for v in reversed(self.edits[node])]
                chunk = newest_first[page * self.edit_page:(page + 1) * self.edit_page]
                more = (page + 1) * self.edit_page < len(newest_first)
                return json.dumps({"data": {"node": {"userContentEdits": {
                    "nodes": chunk, "pageInfo": {"hasNextPage": more, "endCursor": str(page + 1)}}}}})
            n = int(next(a for a in args if a.startswith("p=")).split("=")[1])
            unresolved = self.prs[n].get("threads", 0) if page == self.thread_pages - 1 else 0
            nodes = [{"isResolved": False}] * unresolved + [{"isResolved": True}]
            more = page < self.thread_pages - 1
            return json.dumps({"data": {"repository": {"pullRequest": {"reviewThreads": {
                "nodes": nodes, "pageInfo": {"hasNextPage": more, "endCursor": str(page + 1)}}}}}})
        raise AssertionError(f"unexpected gh call {args}")


def gate(**pr) -> "mt.PrGate":
    return mt.fetch_gate(1, mt.DEFAULT_REPO, FakeGh({1: pr}))


def test_ready_prints_literal_full_sha_merge_command():
    g = gate(bot=[card(HEAD, "completed", False)])
    assert g.verdict == "READY", g.reasons
    # guard_operator_acts refuses a SHA in a variable or $(...): the command must carry it literally
    assert g.merge_command == f"gh pr merge 1 --repo {mt.DEFAULT_REPO} --merge --match-head-commit {HEAD}"


def test_merge_command_targets_the_checked_repository():
    # Codex P2 on #915: without --repo, the pasted command acts on the caller's checkout.
    g = mt.fetch_gate(7, "someone/fork", FakeGh({7: {"bot": [card(HEAD, "completed", False)]}}))
    assert g.verdict == "READY" and "--repo someone/fork " in g.merge_command


def test_printed_merge_command_is_a_pinned_merge_to_the_guard():
    spec = importlib.util.spec_from_file_location("guard_operator_acts",
                                                  _PATH.with_name("guard_operator_acts.py"))
    guard = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(guard)
    command = gate(bot=[card(HEAD, "completed", False)]).merge_command
    assert guard.classify_command(command) == ("pass", "pr.merge")


def test_clean_review_of_an_older_head_does_not_count():
    g = gate(bot=[card(OLD, "completed", False)])
    assert g.verdict == "WAIT" and "no Codex review at head" in g.reasons
    assert g.merge_command == ""


def test_running_review_waits_and_findings_hold():
    assert gate(bot=[card(HEAD, "running", None)]).verdict == "WAIT"
    assert gate(bot=[card(HEAD, "completed", True)]).verdict == "HOLD"


def test_resolved_threads_do_not_turn_findings_clean():
    # has_any_findings is the review's result; has_unresolved_findings tracks threads
    g = gate(bot=[card(HEAD, "completed", False, any_=True)])
    assert g.verdict == "HOLD" and g.findings_at_head
    # the connector edits the card again as threads resolve: still one review, still dirty
    resolved = {"history": [(t(0), card(HEAD, "running", None)), (t(1), card(HEAD, "completed", True)),
                            (t(2), card(HEAD, "completed", False))]}
    g = gate(bot=[resolved])
    assert len(g.reviews) == 1 and g.findings_at_head and g.verdict == "HOLD"


def test_completed_card_without_a_result_is_not_clean():
    g = gate(bot=[card(HEAD, "completed", None)])
    assert g.verdict == "HOLD" and g.findings_at_head


def test_receipts_and_pr_reviews_are_not_counted_again():
    # #906 as recorded: the card's history holds all four reviews; the receipt and the three
    # connector PR reviews are other records of the same reviews.
    pr = timeline(("codex", A, True), ("codex", B, True), ("codex", C, True), ("codex", HEAD, False))
    pr["bot"].append(receipt(HEAD))
    pr["reviews"] = [{"user": {"login": BOT}, "state": "COMMENTED", "commit_id": c, "body": "x"}
                     for c in (A, B, C)]
    g = gate(**pr)
    assert len(g.reviews) == 4 and g.verdict == "READY"


def test_cli_fallback_marker_from_owner_clears_a_stalled_review():
    stalled = card(HEAD, "running", None)
    g = gate(bot=[stalled], human=[(OWNER, cli(HEAD, "clean"))])
    assert g.verdict == "READY" and g.clean_at_head
    assert gate(bot=[stalled], human=[(OWNER, cli(HEAD, "findings"))]).verdict == "HOLD"


def test_cli_marker_from_anyone_else_or_for_another_commit_is_ignored():
    stalled = card(HEAD, "running", None)
    assert gate(bot=[stalled], human=[("drive-by", cli(HEAD, "clean"))]).verdict == "WAIT"
    assert gate(bot=[stalled], human=[(OWNER, cli(OLD, "clean"))]).verdict == "WAIT"
    assert gate(bot=[stalled], human=[(OWNER, "see below\n" + cli(HEAD, "clean"))]).verdict == "WAIT"


def test_owner_match_ignores_the_case_of_repo():
    # gh and the API accept any case in --repo; GitHub returns the login's own case.
    fake = FakeGh({1: {"bot": [card(HEAD, "running", None)], "human": [(OWNER, cli(HEAD, "clean"))]}})
    assert mt.fetch_gate(1, mt.DEFAULT_REPO.lower(), fake).verdict == "READY"


def test_no_approval_substitutes_for_codex():
    # Addendum 2026-10-25: Claude does not review its own work; Codex is the reviewer.
    approvals = [{"user": {"login": "claude[bot]"}, "state": "APPROVED", "commit_id": HEAD}]
    assert gate(reviews=approvals).verdict == "WAIT"
    assert gate(bot=[card(HEAD, "completed", True)], reviews=approvals).verdict == "HOLD"


# The review limit, from the order reviews completed in. Joshua 2026-10-25: "a clean fourth
# review counts, it can still merge then"; beyond the fourth is not ruled on.
LIMIT_CASES = {
    "906: three dirty, clean fourth": (
        [("codex", A, True), ("codex", B, True), ("codex", C, True), ("codex", HEAD, False)],
        "READY", 4, ""),
    "codex P1: a re-requested review of the same commit counts again": (
        [("codex", A, True), ("codex", A, True), ("codex", B, True), ("codex", C, True),
         ("codex", HEAD, False)], "HOLD", 5, "ask Joshua"),
    "a review only the card recorded still counts after the card moves on": (
        [("codex", A, True), ("codex", B, True), ("codex", C, True), ("codex", D, False),
         ("codex", HEAD, False)], "HOLD", 5, "ask Joshua"),
    "a clean fourth stands when the stalled review completes after the CLI fallback": (
        [("codex", A, True), ("codex", B, True), ("codex", C, True), ("cli", HEAD, False),
         ("codex", HEAD, False)], "READY", 5, ""),
    "connector and CLI reviews of one commit are two reviews": (
        [("codex", A, True), ("cli", B, True), ("codex", B, True), ("cli", C, True),
         ("cli", HEAD, False)], "HOLD", 5, "ask Joshua"),
    "fourth review with findings returns to the owner": (
        [("codex", A, True), ("codex", B, True), ("codex", C, True), ("codex", HEAD, True)],
        "HOLD", 4, "original owner"),
    "three dirty and the fourth running waits for a clean fourth": (
        [("codex", A, True), ("codex", B, True), ("codex", C, True), ("running", HEAD, None)],
        "WAIT", 3, "clean fourth"),
    "findings at head win over a later clean review of the same head": (
        [("codex", HEAD, True), ("codex", HEAD, False)], "HOLD", 2, "findings at head"),
    "a clean review of an older head leaves the head unreviewed": (
        [("codex", OLD, False)], "WAIT", 1, "no Codex review at head"),
    "a connector clean review after CLI fallbacks keeps its time position": (
        [("codex", A, True), ("cli", B, True), ("cli", C, True), ("cli", D, True),
         ("codex", HEAD, False)], "HOLD", 5, "ask Joshua"),
    "a clean fourth at an older head is spent once the head moves": (
        [("codex", A, True), ("codex", B, True), ("codex", C, True), ("codex", D, False)],
        "HOLD", 4, "review 4 was clean at an older head; a fresh review would be review 5"),
}


@pytest.mark.parametrize("events,verdict,n,reason", LIMIT_CASES.values(), ids=LIMIT_CASES.keys())
def test_review_limit(events, verdict, n, reason):
    g = gate(**timeline(*events))
    assert (g.verdict, len(g.reviews)) == (verdict, n), g.reasons
    assert reason in " ".join(g.reasons)


def test_behind_after_a_clean_fourth_warns_before_update_branch():
    g = gate(**timeline(("codex", A, True), ("codex", B, True), ("codex", C, True),
                        ("codex", HEAD, False)), merge="BEHIND")
    assert g.verdict == "WAIT" and "it would be review 5: ask Joshua first" in " ".join(g.reasons)


def test_completed_on_one_commit_then_another_is_two_reviews():
    history = [(t(0), card(A, "running", None)), (t(1), card(A, "completed", True, any_=True)),
               (t(2), card(B, "completed", True, any_=True))]
    assert [r.sha for r in gate(bot=[{"history": history}]).reviews] == [A, B]


def test_rest_body_older_than_the_edit_history_is_not_counted_again():
    # The connector edited the card between the REST read and the GraphQL read.
    pr = timeline(("codex", A, True), ("codex", B, True), ("codex", C, True), ("running", HEAD, None))
    pr["bot"][0]["rest"] = -2   # REST still shows C's completed version
    g = gate(**pr)
    assert len(g.reviews) == 3 and g.codex.status == "running"


HISTORY_GAPS = {
    "old-format card (before about 2026-10-14)": (
        {"bot": ["<!-- codex-pull-request-review-summary -->\n| Code Review | **Completed** | `abc1234` |",
                 card(HEAD, "completed", False)]}, "old-format Codex card"),
    "a Codex reply that is neither a card nor a receipt (#896)": (
        {"bot": [card(HEAD, "running", None), "## Review Result\n\n**No blocking findings.**"]},
        "unrecognised Codex comment"),
    "a deleted card revision": (
        {"bot": [{"history": [(t(0), card(A, "running", None)), (t(1), "", {"diff": None}),
                              (t(2), card(HEAD, "completed", False))]}]}, "was deleted"),
    "a card revision by someone else": (
        {"bot": [{"history": [(t(0), card(A, "running", None)),
                              (t(1), card(HEAD, "completed", False), {"editor": {"login": "someone"}})]}]},
        "edited by someone"),
    "an edited CLI review comment": (
        {"bot": [card(HEAD, "running", None)], "human": [(OWNER, cli(HEAD, "clean"), t(0), t(9))]},
        "CLI review comment 200 was edited"),
    "a connector PR review the card's history lacks": (
        {"bot": [card(HEAD, "completed", False)],
         "reviews": [{"user": {"login": BOT}, "state": "COMMENTED", "commit_id": A,
                      "body": f"<!-- codex-review-receipt:v1 -->\n**Reviewed commit:** `{A[:10]}`"}]},
        "findings record at aaaaaaa is missing"),
    "a clean receipt the card's history lacks": (
        {"bot": [card(HEAD, "completed", True, any_=True), receipt(HEAD)]},
        "clean record at a1943a3 is missing"),
}


@pytest.mark.parametrize("pr,reason", HISTORY_GAPS.values(), ids=HISTORY_GAPS.keys())
def test_incomplete_review_history_holds_for_a_count_by_hand(pr, reason):
    g = gate(**pr)
    assert g.verdict == "HOLD" and reason in " ".join(g.reasons), g.reasons
    assert "count the reviews by hand" in " ".join(g.reasons)


def test_card_edit_history_is_paginated():
    pr = timeline(("codex", A, True), ("codex", B, True), ("codex", HEAD, False))
    g = mt.fetch_gate(1, mt.DEFAULT_REPO, FakeGh({1: pr}, edit_page=1))
    assert len(g.reviews) == 3 and g.verdict == "READY"


def test_check_running_is_wait_even_with_empty_conclusion():
    checks = green("skills (3.12)") + [{"name": "pytest (3.11)", "status": "IN_PROGRESS",
                                        "conclusion": ""}]
    g = gate(bot=[card(HEAD, "completed", False)], checks=checks)
    assert g.verdict == "WAIT" and g.pending_checks == ["pytest (3.11)"]


def test_failing_or_cancelled_check_holds_and_status_context_is_read():
    checks = green("skills (3.12)") + [
        {"name": "build (3.11)", "status": "COMPLETED", "conclusion": "CANCELLED"},
        {"context": "CodeRabbit", "state": "SUCCESS"},
    ]
    g = gate(bot=[card(HEAD, "completed", False)], checks=checks)
    assert g.verdict == "HOLD" and g.failing_checks == ["build (3.11)"]
    pending, failing = mt.classify_checks([{"context": "ci/x", "state": "PENDING"}])
    assert pending == ["ci/x"] and failing == []


def test_merge_state_threads_draft_and_stacked_base():
    base = {"bot": [card(HEAD, "completed", False)]}
    assert gate(**base, merge="UNKNOWN").verdict == "WAIT"
    assert "update-branch" in " ".join(gate(**base, merge="BEHIND").reasons)
    assert gate(**base, threads=2).verdict == "WAIT"
    assert gate(**base, draft=True).verdict == "HOLD"
    stacked = gate(**base, base="claude/other-pr")
    assert stacked.verdict == "HOLD" and "retarget" in " ".join(stacked.reasons)


def test_review_threads_are_paginated():
    g = mt.fetch_gate(1, mt.DEFAULT_REPO, FakeGh({1: {"bot": [card(HEAD, "completed", False)],
                                                      "threads": 1}}, thread_pages=3))
    assert g.unresolved_threads == 1 and g.verdict == "WAIT"


def test_merged_pr_reports_terminal_state():
    g = gate(state="MERGED", merge="UNKNOWN")
    assert g.verdict == "MERGED" and g.merge_command == ""


def test_stall_flag_after_thirty_minutes_at_current_head_only():
    running = mt._card(card(HEAD, "running", None, since="2026-10-25T03:25:05Z"))
    assert mt.is_stalled(running, HEAD, NOW, 30)
    assert not mt.is_stalled(running, HEAD, NOW, 40)
    assert not mt.is_stalled(running, OLD, NOW, 30)
    done = mt._card(card(HEAD, "completed", False))
    assert not mt.is_stalled(done, HEAD, NOW, 30)


def test_watch_emits_new_changed_closed(tmp_path):
    prs = {901: {"bot": [card(HEAD, "running", None)]},
           902: {"bot": [card(HEAD, "completed", False)], "title": "x\ty → z"}}
    fake = FakeGh(prs)
    first = mt.watch_once(mt.DEFAULT_REPO, 900, tmp_path, 30, NOW, fake)
    assert [e.split()[0] for e in first] == ["NEW", "NEW"]
    assert mt.watch_once(mt.DEFAULT_REPO, 900, tmp_path, 30, NOW, fake) == []
    prs[901]["bot"] = [card(HEAD, "completed", False)]
    del prs[902]
    events = mt.watch_once(mt.DEFAULT_REPO, 900, tmp_path, 30, NOW, fake)
    assert events[0].startswith("CHANGED #901") and "verdict=READY" in events[0]
    assert events[1] == "CLOSED #902"


def test_watch_error_mid_poll_loses_no_event(tmp_path):
    prs = {901: {"bot": [card(HEAD, "completed", False)]}, 902: {"raise": True}}
    with pytest.raises(RuntimeError):
        mt.watch_once(mt.DEFAULT_REPO, 900, tmp_path, 30, NOW, FakeGh(prs))
    assert not list(tmp_path.glob("pr_*.txt"))   # nothing recorded as seen
    del prs[902]["raise"]
    events = mt.watch_once(mt.DEFAULT_REPO, 900, tmp_path, 30, NOW, FakeGh(prs))
    assert any(e.startswith("NEW #901") for e in events)


def test_watch_ignores_and_keeps_state_at_or_below_min(tmp_path):
    (tmp_path / "pr_880.txt").write_text("from a run with a lower --min", encoding="utf-8")
    fake = FakeGh({889: {}, 890: {"bot": [card(HEAD, "completed", False)]}})
    events = mt.watch_once(mt.DEFAULT_REPO, 889, tmp_path, 30, NOW, fake)
    assert events == [e for e in events if e.startswith("NEW #890")] and len(events) == 1
    assert (tmp_path / "pr_880.txt").exists()


def test_watch_flags_stall(tmp_path):
    fake = FakeGh({905: {"bot": [card(HEAD, "running", None, since="2026-10-25T03:00:00Z")]}})
    (event,) = mt.watch_once(mt.DEFAULT_REPO, 900, tmp_path, 30, NOW, fake)
    assert "STALLED" in event


def test_watch_command_holds_the_lock_while_polling_clears_state_and_exits(monkeypatch, tmp_path):
    (tmp_path / "pr_901.txt").write_text("stale", encoding="utf-8")
    seen = []

    def poll(*a, **k):
        seen.append(sorted(p.name for p in tmp_path.glob("pr_*")))
        with pytest.raises(SystemExit):   # a second watcher is refused mid-poll
            mt._acquire_lock(tmp_path)
        return []

    monkeypatch.setattr(mt, "watch_once", poll)
    monkeypatch.setattr(mt.time, "sleep", lambda s: None)
    clock = iter([0.0, 0.0, 5.0, 999.0, 999.0, 999.0])
    monkeypatch.setattr(mt.time, "monotonic", lambda: next(clock))
    args = mt.argparse.Namespace(repo=mt.DEFAULT_REPO, min=0, state_dir=str(tmp_path),
                                 stall_minutes=30, interval=1, max_seconds=20)
    assert mt.cmd_watch(args) == 0
    assert seen and seen[0] == []                       # old state cleared before first poll
    mt._release_lock(mt._acquire_lock(tmp_path))       # lock released on exit
    assert (tmp_path / "watch.lock").exists()           # never deleted: a new file is a free lock


def test_second_watcher_is_refused_while_the_first_holds_the_lock(tmp_path):
    first = mt._acquire_lock(tmp_path)
    with pytest.raises(SystemExit):
        mt._acquire_lock(tmp_path)
    mt._release_lock(first)
    mt._release_lock(mt._acquire_lock(tmp_path))


def test_lock_lasts_any_poll_length_and_dies_with_the_process(tmp_path):
    # Codex P2 on #915: a TTL lock expired during a slow poll. The OS lock has no TTL: a
    # live holder keeps it however long it waits, and its exit frees it.
    holder = subprocess.Popen(
        [sys.executable, "-I", "-c",
         "import importlib.util, sys; s = importlib.util.spec_from_file_location('m', sys.argv[1]);"
         " m = sys.modules['m'] = importlib.util.module_from_spec(s); s.loader.exec_module(m);"
         " h = m._acquire_lock(__import__('pathlib').Path(sys.argv[2])); print('held', flush=True);"
         " sys.stdin.read()", str(_PATH), str(tmp_path)],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    try:
        assert holder.stdout.readline().strip() == "held"
        with pytest.raises(SystemExit):
            mt._acquire_lock(tmp_path)
    finally:
        holder.stdin.close()
        holder.wait(timeout=30)
    mt._release_lock(mt._acquire_lock(tmp_path))


def test_gate_exit_code_json_and_unicode_title(capsys):
    fake = FakeGh({1: {"bot": [card(HEAD, "completed", False)], "title": "cloud → return"},
                   2: {"bot": [card(HEAD, "running", None)]}})
    ns = mt.argparse.Namespace(repo=mt.DEFAULT_REPO, prs=[1], json=True)
    assert mt.cmd_gate(ns, fake) == 0
    assert json.loads(capsys.readouterr().out)[0]["verdict"] == "READY"
    ns.prs, ns.json = [1, 2], False
    assert mt.cmd_gate(ns, fake) == 1
    assert "→" in capsys.readouterr().out


@pytest.mark.parametrize("a,b,same", [(HEAD, HEAD[:7], True), (HEAD, HEAD[:6], False),
                                      (HEAD, OLD, False), ("", HEAD, False)])
def test_same_commit_needs_seven_hex(a, b, same):
    assert mt._same_commit(a, b) is same
