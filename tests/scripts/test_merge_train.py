"""Tests for scripts/merge_train.py — the read-only merge gate and change watcher.

A fake ``gh`` runner returns canned JSON, so the suite needs no network or credentials.
Each case pins one clause of the merge rule (surface-allocation ADR Addendum 2026-10-24b A
and its 2026-10-25 amendment) or one failure the merge-train sessions hit by hand.
"""
from __future__ import annotations

import importlib.util
import json
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
BOT = mt.CODEX_BOT
OWNER = mt.DEFAULT_REPO.split("/")[0]
NOW = datetime(2026, 10, 25, 4, 0, tzinfo=timezone.utc)


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


def dirty(*commits: str) -> list[dict]:
    return [{"user": {"login": BOT}, "state": "COMMENTED", "commit_id": c} for c in commits]


def green(*names: str) -> list[dict]:
    return [{"name": n, "status": "COMPLETED", "conclusion": "SUCCESS"} for n in names]


class FakeGh:
    """Answers the calls fetch_gate makes, per PR number."""

    def __init__(self, prs: dict[int, dict], thread_pages: int = 1):
        self.prs, self.thread_pages = prs, thread_pages

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
            p = self.prs[int(args[-1].split("/")[-2])]
            comments = [{"user": {"login": BOT}, "body": b} for b in p.get("bot", [])]
            comments += [{"user": {"login": who}, "body": b} for who, b in p.get("human", [])]
            return json.dumps([comments])
        if args[0] == "api" and args[-1].endswith("/reviews"):
            return json.dumps([self.prs[int(args[-1].split("/")[-2])].get("reviews", [])])
        if args[:2] == ["api", "graphql"]:
            n = int(next(a for a in args if a.startswith("p=")).split("=")[1])
            cursor = next((a.split("=", 1)[1] for a in args if a.startswith("c=")), None)
            page = int(cursor or 0)
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
    assert g.merge_command == f"gh pr merge 1 --merge --match-head-commit {HEAD}"


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


def test_card_is_edited_in_place_so_later_receipts_do_not_override_it():
    # Observed order: the summary card is the first bot comment; receipts follow.
    g = gate(bot=[card(HEAD, "running", None), receipt(OLD)])
    assert g.verdict == "WAIT" and "Codex review running" in g.reasons
    assert mt.is_stalled(g.codex, HEAD, NOW, 30)


def test_receipt_alone_counts_when_no_card_exists():
    assert gate(bot=[receipt(HEAD)]).verdict == "READY"


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


def test_no_approval_substitutes_for_codex():
    # Addendum 2026-10-25: Claude does not review its own work; Codex is the reviewer.
    approvals = [{"user": {"login": "claude[bot]"}, "state": "APPROVED", "commit_id": HEAD}]
    assert gate(reviews=approvals).verdict == "WAIT"
    assert gate(bot=[card(HEAD, "completed", True)], reviews=approvals).verdict == "HOLD"


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


def test_clean_fourth_review_still_clears_after_three_dirty():
    # Joshua 2026-10-25: "a clean fourth review counts, it can still merge then" (#906)
    three = dirty("6fc7e35", "89ccb09", "8a245a6")
    g = gate(bot=[card(HEAD, "completed", False)], reviews=three)
    assert len(g.reviews) == 4 and g.verdict == "READY"
    pending = gate(bot=[card(HEAD, "running", None)], reviews=three)
    assert pending.verdict == "WAIT" and "clean fourth" in " ".join(pending.reasons)


def test_fourth_review_with_findings_returns_to_owner():
    g = gate(bot=[card(HEAD, "completed", True)], reviews=dirty("a1b2c3d", "b2c3d4e", "c3d4e5f"))
    assert g.verdict == "HOLD" and "original owner" in " ".join(g.reasons)


def test_clean_review_beyond_the_fourth_asks_joshua():
    # four earlier reviews (one clean at an older head) then a clean fifth at head
    g = gate(bot=[receipt(OLD), card(HEAD, "completed", False)],
             reviews=dirty("a1b2c3d", "b2c3d4e", "c3d4e5f"))
    assert len(g.reviews) == 5 and g.verdict == "HOLD"
    assert "ask Joshua" in " ".join(g.reasons)


def test_reviews_unify_short_and_full_shas():
    merged = mt._merge_reviews({HEAD[:10]: False}, {HEAD: False}, {"6fc7e35": True})
    assert len(merged) == 2 and merged[HEAD] is False


def test_merged_pr_reports_terminal_state():
    g = gate(state="MERGED", merge="UNKNOWN")
    assert g.verdict == "MERGED" and g.merge_command == ""


def test_stall_flag_after_thirty_minutes_at_current_head_only():
    running, _ = mt.codex_state([card(HEAD, "running", None, since="2026-10-25T03:25:05Z")])
    assert mt.is_stalled(running, HEAD, NOW, 30)
    assert not mt.is_stalled(running, HEAD, NOW, 40)
    assert not mt.is_stalled(running, OLD, NOW, 30)
    done, _ = mt.codex_state([card(HEAD, "completed", False)])
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


def test_watch_command_locks_clears_state_and_exits(monkeypatch, tmp_path):
    (tmp_path / "pr_901.txt").write_text("stale", encoding="utf-8")
    seen = []
    monkeypatch.setattr(mt, "watch_once",
                        lambda *a, **k: seen.append(sorted(p.name for p in tmp_path.glob("pr_*"))) or [])
    monkeypatch.setattr(mt.time, "sleep", lambda s: None)
    clock = iter([0.0, 0.0, 5.0, 999.0, 999.0, 999.0])
    monkeypatch.setattr(mt.time, "monotonic", lambda: next(clock))
    args = mt.argparse.Namespace(repo=mt.DEFAULT_REPO, min=0, state_dir=str(tmp_path),
                                 stall_minutes=30, interval=1, max_seconds=20)
    assert mt.cmd_watch(args) == 0
    assert seen and seen[0] == []                       # old state cleared before first poll
    assert not (tmp_path / "watch.lock").exists()       # lock released on exit


def test_second_watcher_is_refused_while_lock_is_fresh(tmp_path):
    mt._acquire_lock(tmp_path, ttl=300)
    with pytest.raises(SystemExit):
        mt._acquire_lock(tmp_path, ttl=300)


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
