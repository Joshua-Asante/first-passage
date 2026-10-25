#!/usr/bin/env python3
"""merge_train.py — read-only merge-gate check and change watcher for the PR merge train.

Mechanizes what merge-train coordinator sessions kept re-deriving by hand (merge-order
agent 2026-10-04..07, merge-train coordinator 2026-10-25): per PR, read the head, the
Codex review state *at that exact head*, every check in ``statusCheckRollup``,
``mergeStateStatus``, the base branch and unresolved review threads, and say whether the
merge rule holds (surface-allocation ADR, Addendum 2026-10-24b A and its 2026-10-25
amendment). Rules live there; this applies them.

Never merges, comments or pushes. For a READY PR it prints the merge command with the
literal 40-hex head SHA; ``scripts/guard_operator_acts.py`` refuses a SHA passed through
a shell variable or command substitution, so paste that command as printed.

    python scripts/merge_train.py gate 912 913            # table; exit 0 only if all READY
    python scripts/merge_train.py gate 912 --json
    python scripts/merge_train.py watch --min 911         # one line per change; for a Monitor

The review is Codex: the GitHub connector's summary card or receipt, or a Codex CLI
fallback result posted by the repository owner's account whose first line is
``codex-cli-review:v1 <40-hex sha> clean`` (or ``findings``). Every completed Codex review
counts toward the limit, one per reviewed commit.

``watch`` takes a lock in its state directory, clears old state so its first poll reports
every PR, and exits by itself after ``--max-seconds`` (default 1680, under a 30-minute
Monitor limit). A GitHub review still "running" at the head after ``--stall-minutes``
(default 30) is flagged STALLED, the cue for the Codex CLI fallback. Requires ``gh``.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REPO = "Joshua-Asante/first-passage"
CODEX_BOT = "chatgpt-codex-connector[bot]"
GREEN = {"SUCCESS", "NEUTRAL", "SKIPPED"}
_STATE_RE = re.compile(r"codex-review-state:v1 (\{.*?\}) -->")
_RECEIPT_RE = re.compile(r"Reviewed commit:\*\*\s*`([0-9a-f]{7,40})`")
_RUNNING_SINCE_RE = re.compile(r'Running\*\*\s+since\s+<relative-time datetime="([^"]+)"')
_CLI_RE = re.compile(r"\A\s*codex-cli-review:v1 ([0-9a-f]{40}) (clean|findings)\b")
_THREADS_QUERY = (
    "query($o:String!,$n:String!,$p:Int!,$c:String){repository(owner:$o,name:$n)"
    "{pullRequest(number:$p){reviewThreads(first:100,after:$c)"
    "{nodes{isResolved} pageInfo{hasNextPage endCursor}}}}}"
)

Runner = Callable[[list[str]], str]


def gh_runner(args: list[str]) -> str:
    """Run ``gh`` and return stdout; raise RuntimeError with stderr on failure."""
    proc = subprocess.run(
        ["gh", *args], cwd=str(REPO_ROOT), capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False, timeout=120,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args[:3])} failed: {proc.stderr.strip()[:300]}")
    return proc.stdout


@dataclass
class CodexState:
    sha: str = ""          # commit the GitHub review card (or receipt) refers to
    status: str = "none"   # none | running | completed
    findings: bool | None = None
    running_since: str = ""


@dataclass
class PrGate:
    number: int
    title: str = ""
    state: str = "OPEN"    # OPEN | MERGED | CLOSED
    base: str = "main"
    head: str = ""
    draft: bool = False
    merge_state: str = ""
    pending_checks: list[str] = field(default_factory=list)
    failing_checks: list[str] = field(default_factory=list)
    codex: CodexState = field(default_factory=CodexState)
    clean_at_head: bool = False
    findings_at_head: bool = False
    reviews: dict[str, bool] = field(default_factory=dict)   # commit -> review found issues
    unresolved_threads: int = 0
    verdict: str = ""      # READY | WAIT | HOLD | MERGED | CLOSED
    reasons: list[str] = field(default_factory=list)
    merge_command: str = ""


def classify_checks(rollup: list[dict]) -> tuple[list[str], list[str]]:
    """Split a statusCheckRollup into (pending, failing) names. Green otherwise.

    A check run's conclusion is "" while it runs, so gate on status COMPLETED first.
    """
    pending, failing = [], []
    for item in rollup or []:
        name = item.get("name") or item.get("context") or "?"
        if "state" in item and "status" not in item:   # commit StatusContext
            state = (item.get("state") or "").upper()
            if state in ("PENDING", "EXPECTED", ""):
                pending.append(name)
            elif state != "SUCCESS":
                failing.append(name)
            continue
        if (item.get("status") or "").upper() != "COMPLETED":
            pending.append(name)
        elif (item.get("conclusion") or "").upper() not in GREEN:
            failing.append(name)
    return pending, failing


def _same_commit(a: str, b: str) -> bool:
    return bool(a and b) and (a.startswith(b) or b.startswith(a)) and min(len(a), len(b)) >= 7


def codex_state(bot_bodies: list[str]) -> tuple[CodexState, dict[str, bool]]:
    """The connector's current review state, and every commit it reviewed.

    The summary card (``codex-review-state:v1 {json}``) is one comment edited in place, so
    it is the current state whatever its position; receipts ("Reviewed commit: `sha`") are
    appended per clean review and only stand in when no card exists.
    """
    card, receipts = None, []
    for body in bot_bodies:
        m = _STATE_RE.search(body)
        if m:
            try:
                review = json.loads(m.group(1)).get("code_review") or {}
            except json.JSONDecodeError:
                continue
            findings = review.get("has_any_findings")
            if findings is None:
                findings = review.get("has_unresolved_findings")
            card = CodexState(sha=review.get("commit_sha") or "",
                              status=review.get("status") or "none", findings=findings)
            since = _RUNNING_SINCE_RE.search(body)
            card.running_since = since.group(1) if since and card.status == "running" else ""
            continue
        r = _RECEIPT_RE.search(body)
        if r and "find any major issues" in body:
            receipts.append(r.group(1))
    reviewed: dict[str, bool] = {sha: False for sha in receipts}
    if card and card.status == "completed" and card.sha:
        reviewed[card.sha] = bool(card.findings) or reviewed.get(card.sha, False)
    if card:
        return card, reviewed
    if receipts:
        return CodexState(sha=receipts[-1], status="completed", findings=False), reviewed
    return CodexState(), reviewed


def cli_reviews(owner_bodies: list[str]) -> dict[str, bool]:
    """Codex CLI fallback verdicts posted by the repository owner's account."""
    out: dict[str, bool] = {}
    for body in owner_bodies:
        m = _CLI_RE.match(body)
        if m:
            out[m.group(1)] = m.group(2) == "findings"
    return out


def _merge_reviews(*maps: dict[str, bool]) -> dict[str, bool]:
    """One entry per reviewed commit (short and full SHAs unified); findings win."""
    merged: dict[str, bool] = {}
    for mp in maps:
        for sha, findings in mp.items():
            key = next((k for k in merged if _same_commit(k, sha)), None)
            if key is None:
                merged[sha] = findings
            else:
                merged[key] = merged[key] or findings
                if len(sha) > len(key):
                    merged[sha] = merged.pop(key)
    return merged


def is_stalled(state: CodexState, head: str, now: datetime, minutes: int) -> bool:
    if state.status != "running" or not _same_commit(state.sha, head) or not state.running_since:
        return False
    try:
        since = datetime.fromisoformat(state.running_since.replace("Z", "+00:00"))
    except ValueError:
        return False
    if since.tzinfo is None:
        since = since.replace(tzinfo=timezone.utc)
    return (now - since).total_seconds() >= minutes * 60


def decide(g: PrGate) -> PrGate:
    """Apply the merge rule; fill verdict, reasons and the literal merge command."""
    if g.state != "OPEN":
        g.verdict, g.reasons, g.merge_command = g.state, [], ""
        return g
    hold, wait = [], []
    if g.draft:
        hold.append("draft")
    if g.base != "main":
        hold.append(f"base is {g.base}, not main: retarget it first")
    if g.failing_checks:
        hold.append("failing: " + ", ".join(g.failing_checks))
    n = len(g.reviews)
    dirty = sum(1 for f in g.reviews.values() if f)
    # Clean within three Codex reviews; amended 2026-10-25: a clean fourth counts;
    # beyond the fourth is not ruled on.
    if g.clean_at_head:
        if n > 4:
            hold.append(f"clean review is review {n}; beyond the fourth is not ruled on: ask Joshua")
    elif n >= 4:
        hold.append(f"{n} Codex reviews without a clean one at head: return to the original owner")
    elif g.findings_at_head:
        hold.append("Codex findings at head: back to the owner")
    else:
        running = g.codex.status == "running" and _same_commit(g.codex.sha, g.head)
        note = " (only a clean fourth can clear it)" if dirty == 3 else ""
        wait.append(("Codex review running" if running else "no Codex review at head") + note)
    if g.pending_checks:
        wait.append(f"{len(g.pending_checks)} check(s) running")
    if g.unresolved_threads:
        wait.append(f"{g.unresolved_threads} unresolved thread(s)")
    if g.merge_state == "BEHIND":
        wait.append("mergeStateStatus=BEHIND (gh pr update-branch; then a fresh review)")
    elif g.merge_state == "DIRTY":
        wait.append("mergeStateStatus=DIRTY (conflict: route to the owner)")
    elif g.merge_state != "CLEAN":
        wait.append(f"mergeStateStatus={g.merge_state or '?'}")
    g.reasons = hold + wait
    g.verdict = "HOLD" if hold else ("WAIT" if wait else "READY")
    g.merge_command = (
        f"gh pr merge {g.number} --merge --match-head-commit {g.head}" if g.verdict == "READY" else ""
    )
    return g


def _unresolved_threads(number: int, repo: str, run: Runner) -> int:
    owner, name = repo.split("/", 1)
    count, cursor = 0, None
    while True:
        args = ["api", "graphql", "-f", f"query={_THREADS_QUERY}", "-F", f"o={owner}",
                "-F", f"n={name}", "-F", f"p={number}"]
        if cursor:
            args += ["-f", f"c={cursor}"]
        page = json.loads(run(args))["data"]["repository"]["pullRequest"]["reviewThreads"]
        count += sum(1 for node in page["nodes"] if not node.get("isResolved"))
        info = page.get("pageInfo") or {}
        if not info.get("hasNextPage"):
            return count
        cursor = info.get("endCursor")


def fetch_gate(number: int, repo: str, run: Runner = gh_runner) -> PrGate:
    pr = json.loads(run([
        "pr", "view", str(number), "--repo", repo, "--json",
        "number,title,state,isDraft,baseRefName,headRefOid,mergeStateStatus,statusCheckRollup",
    ]))
    if pr.get("state", "OPEN") != "OPEN":
        return decide(PrGate(number=number, title=pr.get("title", ""), state=pr["state"],
                             head=pr.get("headRefOid", "")))
    head = pr["headRefOid"]
    pending, failing = classify_checks(pr.get("statusCheckRollup") or [])
    comments = [c for page in json.loads(run(
        ["api", "--paginate", "--slurp", f"repos/{repo}/issues/{number}/comments"])) for c in page]
    login = lambda c: (c.get("user") or {}).get("login")  # noqa: E731
    owner = repo.split("/", 1)[0]
    card, connector = codex_state([c.get("body") or "" for c in comments if login(c) == CODEX_BOT])
    cli = cli_reviews([c.get("body") or "" for c in comments if login(c) == owner])
    pr_reviews = [r for page in json.loads(run(
        ["api", "--paginate", "--slurp", f"repos/{repo}/pulls/{number}/reviews"])) for r in page]
    # The connector leaves a PR review only when it has inline findings.
    dirty = {r["commit_id"]: True for r in pr_reviews if login(r) == CODEX_BOT and r.get("commit_id")}
    reviews = _merge_reviews(connector, dirty, cli)
    at_head = [f for sha, f in reviews.items() if _same_commit(sha, head)]
    findings_at_head = any(at_head) or (
        card.status == "completed" and bool(card.findings) and _same_commit(card.sha, head))
    clean_at_head = bool(at_head) and not findings_at_head
    return decide(PrGate(
        number=number, title=pr.get("title", ""), base=pr.get("baseRefName") or "main",
        head=head, draft=bool(pr.get("isDraft")), merge_state=pr.get("mergeStateStatus") or "",
        pending_checks=pending, failing_checks=failing, codex=card,
        clean_at_head=clean_at_head, findings_at_head=findings_at_head, reviews=reviews,
        unresolved_threads=_unresolved_threads(number, repo, run),
    ))


def _codex_label(g: PrGate) -> str:
    if g.clean_at_head:
        return "clean@head"
    if g.findings_at_head:
        return "findings@head"
    c = g.codex
    if c.status == "running":
        return "running@" + ("head" if _same_commit(c.sha, g.head) else c.sha[:7])
    return "none@head"


def cmd_gate(args: argparse.Namespace, run: Runner = gh_runner) -> int:
    gates = [fetch_gate(n, args.repo, run) for n in args.prs]
    if args.json:
        print(json.dumps([asdict(g) for g in gates], indent=2))
    else:
        for g in gates:
            print(f"#{g.number} {g.verdict:5} head={g.head[:7]} codex={_codex_label(g)} "
                  f"reviews={len(g.reviews)} merge={g.merge_state} threads={g.unresolved_threads}"
                  f" | {g.title}")
            for r in g.reasons:
                print(f"    - {r}")
            if g.merge_command:
                print(f"    {g.merge_command}")
    return 0 if gates and all(g.verdict == "READY" for g in gates) else 1


def watch_line(g: PrGate, stalled: bool) -> str:
    ci = ("FAILED:" + ";".join(g.failing_checks)) if g.failing_checks else (
        f"running({len(g.pending_checks)})" if g.pending_checks else "green")
    return (f"#{g.number} head={g.head[:7]} merge={g.merge_state} ci={ci} "
            f"codex={_codex_label(g)}{' STALLED' if stalled else ''} reviews={len(g.reviews)} "
            f"verdict={g.verdict} | {g.title}")


def watch_once(repo: str, min_pr: int, state_dir: Path, stall_minutes: int,
               now: datetime, run: Runner = gh_runner) -> list[str]:
    """One poll: return NEW/CHANGED/CLOSED lines. State is written only after the
    whole poll succeeds, so an error mid-poll loses no event."""
    state_dir.mkdir(parents=True, exist_ok=True)
    listed = json.loads(run(["pr", "list", "--repo", repo, "--state", "open",
                             "--limit", "200", "--json", "number"]))
    numbers = sorted(p["number"] for p in listed if p["number"] > min_pr)
    lines = {}
    for n in numbers:
        g = fetch_gate(n, repo, run)
        lines[n] = watch_line(g, is_stalled(g.codex, g.head, now, stall_minutes))
    events = []
    for n, line in lines.items():
        key = state_dir / f"pr_{n}.txt"
        old = key.read_text(encoding="utf-8") if key.exists() else None
        if old != line:
            events.append(f"{'NEW' if old is None else 'CHANGED'} {line}")
            key.write_text(line, encoding="utf-8")
    for key in sorted(state_dir.glob("pr_*.txt")):
        n = int(key.stem[3:])
        if n > min_pr and n not in lines:
            events.append(f"CLOSED #{n}")
            key.unlink()
    return events


def _acquire_lock(state_dir: Path, ttl: float) -> Path:
    """Refuse a second watcher on the same state while the first is alive."""
    state_dir.mkdir(parents=True, exist_ok=True)
    lock = state_dir / "watch.lock"
    if lock.exists() and time.time() - lock.stat().st_mtime < ttl:
        raise SystemExit(f"another watcher is running ({lock}); stop it first, or wait {int(ttl)} s")
    lock.write_text(str(time.time()), encoding="utf-8")
    return lock


def cmd_watch(args: argparse.Namespace) -> int:
    state_dir = Path(args.state_dir)
    lock = _acquire_lock(state_dir, args.interval + 120)
    for old in state_dir.glob("pr_*.txt"):   # first poll reports every PR as NEW
        old.unlink()
    start = time.monotonic()
    try:
        while time.monotonic() - start < args.max_seconds:
            lock.touch()
            try:
                for line in watch_once(args.repo, args.min, state_dir,
                                       args.stall_minutes, datetime.now(timezone.utc)):
                    print(line, flush=True)
            except (RuntimeError, subprocess.TimeoutExpired, json.JSONDecodeError, KeyError) as exc:
                print(f"ERROR {exc}", flush=True)
            remaining = args.max_seconds - (time.monotonic() - start)
            if remaining <= 0:
                break
            time.sleep(min(args.interval, remaining))
    finally:
        lock.unlink(missing_ok=True)
    return 0


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):   # PR titles carry non-cp1252 characters
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", default=DEFAULT_REPO)
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("gate", help="check the merge rule for one or more PRs")
    g.add_argument("prs", nargs="+", type=int)
    g.add_argument("--json", action="store_true")
    w = sub.add_parser("watch", help="print one line per PR change until --max-seconds")
    w.add_argument("--min", type=int, default=0, help="watch only PRs numbered above this")
    w.add_argument("--interval", type=int, default=150)
    w.add_argument("--max-seconds", type=int, default=1680)
    w.add_argument("--stall-minutes", type=int, default=30)
    w.add_argument("--state-dir", default=str(REPO_ROOT / ".cache" / "merge-train"))
    args = ap.parse_args(argv)
    return cmd_gate(args) if args.cmd == "gate" else cmd_watch(args)


if __name__ == "__main__":
    sys.exit(main())
