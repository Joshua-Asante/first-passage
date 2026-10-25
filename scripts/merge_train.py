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

The review is Codex. The GitHub connector keeps one summary card per PR and edits it in
place, so its text shows only the latest review; GitHub keeps every earlier version, and
each version that turns ``completed`` is one review, re-requests on the same commit
included. A Codex CLI fallback result posted by the repository owner's account, first
line ``codex-cli-review:v1 <40-hex sha> clean`` (or ``findings``), is one more. Reviews
are put in time order and the limit applies to where the first clean review at the head
falls. The connector's receipts and PR reviews are other records of the same reviews; a
record the card's history does not account for, an old-format card, an unrecognised
connector comment, a deleted or foreign card revision, or an edited CLI comment means the
history is incomplete, and the PR HOLDs for a count by hand: a missed review could make a
later clean one look like the fourth.

``watch`` holds an OS lock on its state directory, clears old state so its first poll reports
every PR, and exits by itself after ``--max-seconds`` (default 1680, under a 30-minute
Monitor limit). A GitHub review still "running" at the head after ``--stall-minutes``
(default 30) is flagged STALLED, the cue for the Codex CLI fallback. Requires ``gh``.
"""
from __future__ import annotations

import argparse
import json
import os
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
CODEX_LOGIN = CODEX_BOT.removesuffix("[bot]")   # GraphQL drops the suffix
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
_EDITS_QUERY = (
    "query($id:ID!,$c:String){node(id:$id){...on IssueComment{userContentEdits(first:100,after:$c)"
    "{nodes{editedAt deletedAt editor{login} diff} pageInfo{hasNextPage endCursor}}}}}"
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
    sha: str = ""          # commit the GitHub review card refers to now
    status: str = "none"   # none | running | completed
    findings: bool | None = None
    running_since: str = ""


@dataclass
class Review:
    sha: str
    findings: bool         # an unknown result counts as findings
    source: str            # connector | cli
    at: str                # ISO time the result was recorded


@dataclass
class PrGate:
    number: int
    repo: str = DEFAULT_REPO
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
    reviews: list[Review] = field(default_factory=list)   # every completed review, oldest first
    history_problems: list[str] = field(default_factory=list)   # why the count can't be trusted
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


def _card(body: str) -> CodexState | None:
    """The code-review state one version of the summary card records."""
    m = _STATE_RE.search(body or "")
    if not m:
        return None
    try:
        review = json.loads(m.group(1)).get("code_review") or {}
    except json.JSONDecodeError:
        return None
    findings = review.get("has_any_findings")
    if findings is None:
        findings = review.get("has_unresolved_findings")
    state = CodexState(sha=review.get("commit_sha") or "", status=review.get("status") or "none",
                       findings=findings)
    since = _RUNNING_SINCE_RE.search(body)
    state.running_since = since.group(1) if since and state.status == "running" else ""
    return state


def connector_reviews(versions: list[tuple[str, str]]) -> list[Review]:
    """One Review per summary-card version that turns ``completed``, from (time, body)
    versions oldest first. A completed version that only restates the previous one (same
    commit, e.g. after threads are resolved) is the same review; findings win."""
    out: list[Review] = []
    prev: CodexState | None = None
    for at, body in versions:
        state = _card(body)
        if state is None:
            continue
        dirty = state.findings is not False
        if state.status == "completed" and state.sha:
            if prev and prev.status == "completed" and _same_commit(prev.sha, state.sha):
                out[-1].findings = out[-1].findings or dirty
            else:
                out.append(Review(state.sha, dirty, "connector", at))
        prev = state
    return out


def cli_reviews(owner_comments: list[dict]) -> list[Review]:
    """Codex CLI fallback verdicts posted by the repository owner's account."""
    out = []
    for c in owner_comments:
        m = _CLI_RE.match(c.get("body") or "")
        if m:
            out.append(Review(m.group(1), m.group(2) == "findings", "cli", c.get("created_at") or ""))
    return out


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
    if g.history_problems:
        hold.append("Codex review history incomplete (" + "; ".join(g.history_problems)
                    + "): count the reviews by hand and ask Joshua")
    n = len(g.reviews)
    dirty = sum(1 for r in g.reviews if r.findings)
    at_head = [(i, r.findings) for i, r in enumerate(g.reviews, 1) if _same_commit(r.sha, g.head)]
    g.findings_at_head = any(f for _, f in at_head)
    g.clean_at_head = bool(at_head) and not g.findings_at_head
    # Clean within three Codex reviews; amended 2026-10-25: a clean fourth counts;
    # beyond the fourth is not ruled on. A later review does not undo a clean fourth.
    if g.clean_at_head:
        pos = at_head[0][0]
        if pos > 4:
            hold.append(f"first clean review at head is review {pos}; beyond the fourth is "
                        "not ruled on: ask Joshua")
    elif n >= 4:
        early = next((i for i, r in enumerate(g.reviews[:4], 1) if not r.findings), None)
        if early:
            hold.append(f"review {early} was clean at an older head; a fresh review would be "
                        f"review {n + 1}, beyond the fourth: ask Joshua")
        else:
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
        nxt = f"; it would be review {n + 1}: ask Joshua first" if n >= 4 else ""
        wait.append(f"mergeStateStatus=BEHIND (gh pr update-branch; then a fresh review{nxt})")
    elif g.merge_state == "DIRTY":
        wait.append("mergeStateStatus=DIRTY (conflict: route to the owner)")
    elif g.merge_state != "CLEAN":
        wait.append(f"mergeStateStatus={g.merge_state or '?'}")
    g.reasons = hold + wait
    g.verdict = "HOLD" if hold else ("WAIT" if wait else "READY")
    g.merge_command = (
        f"gh pr merge {g.number} --repo {g.repo} --merge --match-head-commit {g.head}"
        if g.verdict == "READY" else ""
    )
    return g


def _pages(query: str, fields: list[str], path: list[str], run: Runner) -> list[dict]:
    """Every node of a paginated GraphQL connection reached by ``path``."""
    nodes, cursor = [], None
    while True:
        args = ["api", "graphql", "-f", f"query={query}", *fields]
        if cursor:
            args += ["-f", f"c={cursor}"]
        page = json.loads(run(args))["data"]
        for key in path:
            page = page[key]
        nodes += page["nodes"]
        info = page.get("pageInfo") or {}
        if not info.get("hasNextPage"):
            return nodes
        cursor = info.get("endCursor")


def _unresolved_threads(number: int, repo: str, run: Runner) -> int:
    owner, name = repo.split("/", 1)
    nodes = _pages(_THREADS_QUERY, ["-F", f"o={owner}", "-F", f"n={name}", "-F", f"p={number}"],
                   ["repository", "pullRequest", "reviewThreads"], run)
    return sum(1 for node in nodes if not node.get("isResolved"))


def _card_versions(comment: dict, run: Runner) -> tuple[list[tuple[str, str]], list[str]]:
    """Every version of a summary card, oldest first, and why its history can't be trusted.
    GitHub's edit list holds every version of an edited comment, the current one included,
    so the REST body (read earlier, so possibly older) stands in only for a card never edited."""
    edits = _pages(_EDITS_QUERY, ["-f", f"id={comment['node_id']}"],
                   ["node", "userContentEdits"], run) if comment.get("node_id") else []
    problems = []
    for e in edits:
        editor = ((e.get("editor") or {}).get("login") or "").lower()
        if e.get("deletedAt") or e.get("diff") is None:
            problems.append(f"a revision of Codex card {comment.get('id')} was deleted")
        elif editor != CODEX_LOGIN:
            problems.append(f"Codex card {comment.get('id')} was edited by {editor or 'a deleted account'}")
    if not edits:
        return [(comment.get("updated_at") or "", comment.get("body") or "")], problems
    return sorted((e.get("editedAt") or "", e.get("diff") or "") for e in edits), problems


def _receipt(body: str, commit: str = "") -> tuple[str, bool] | None:
    """(commit, findings) a connector receipt records, or None."""
    m = _RECEIPT_RE.search(body)
    sha = m.group(1) if m else commit
    return (sha, "find any major issues" not in body) if sha else None


def codex_history(comments: list[dict], pr_reviews: list[dict], owner: str,
                  run: Runner) -> tuple[CodexState, list[Review], list[str]]:
    """The card's current state, every completed Codex review oldest first, and reasons the
    history is incomplete (each one HOLDs the PR)."""
    login = lambda c: ((c.get("user") or {}).get("login") or "").lower()  # noqa: E731
    state, reviews, problems, records = CodexState(), [], [], []
    for c in comments:
        body = c.get("body") or ""
        if login(c) == CODEX_BOT:
            if _card(body):
                versions, bad = _card_versions(c, run)
                problems += bad
                reviews += connector_reviews(versions)
                state = _card(versions[-1][1]) or state
            elif "codex-pull-request-review-summary" in body:
                problems.append(f"old-format Codex card {c.get('id')}")
            elif rec := _receipt(body):
                records.append(rec)
            else:
                first = body.strip().splitlines()[0][:40] if body.strip() else ""
                problems.append(f"unrecognised Codex comment {c.get('id')} ({first!r})")
        elif login(c) == owner and _CLI_RE.match(body):
            if (c.get("updated_at") or "") != (c.get("created_at") or ""):
                problems.append(f"CLI review comment {c.get('id')} was edited")
            reviews += cli_reviews([c])
    # A connector PR review with a body is the receipt of one review; an empty one is a
    # thread reply.
    records += [rec for r in pr_reviews if login(r) == CODEX_BOT and (r.get("body") or "").strip()
                and (rec := _receipt(r["body"], r.get("commit_id") or ""))]
    connector = [r for r in reviews if r.source == "connector"]
    for sha, findings in records:
        def same(s: str, f: bool) -> bool:
            return _same_commit(s, sha) and f == findings
        if sum(same(*rec) for rec in records) > sum(same(r.sha, r.findings) for r in connector):
            problems.append(f"a Codex {'findings' if findings else 'clean'} record at {sha[:7]} "
                            "is missing from the card's history")
    reviews.sort(key=lambda r: r.at)
    return state, reviews, list(dict.fromkeys(problems))


def fetch_gate(number: int, repo: str, run: Runner = gh_runner) -> PrGate:
    pr = json.loads(run([
        "pr", "view", str(number), "--repo", repo, "--json",
        "number,title,state,isDraft,baseRefName,headRefOid,mergeStateStatus,statusCheckRollup",
    ]))
    if pr.get("state", "OPEN") != "OPEN":
        return decide(PrGate(number=number, repo=repo, title=pr.get("title", ""),
                             state=pr["state"], head=pr.get("headRefOid", "")))
    head = pr["headRefOid"]
    pending, failing = classify_checks(pr.get("statusCheckRollup") or [])
    comments, pr_reviews = ([c for page in json.loads(run(
        ["api", "--paginate", "--slurp", f"repos/{repo}/{kind}/{number}/{what}"])) for c in page]
        for kind, what in (("issues", "comments"), ("pulls", "reviews")))
    state, reviews, problems = codex_history(comments, pr_reviews, repo.split("/", 1)[0].lower(), run)
    return decide(PrGate(
        number=number, repo=repo, title=pr.get("title", ""), base=pr.get("baseRefName") or "main",
        head=head, draft=bool(pr.get("isDraft")), merge_state=pr.get("mergeStateStatus") or "",
        pending_checks=pending, failing_checks=failing, codex=state, reviews=reviews,
        history_problems=problems, unresolved_threads=_unresolved_threads(number, repo, run),
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


def _acquire_lock(state_dir: Path):
    """Refuse a second watcher on the same state. The lock is an exclusive OS lock held for
    the process's life, so it never expires mid-poll and the OS drops it however the
    watcher exits. The file is never deleted: a new file would be a second, free lock."""
    state_dir.mkdir(parents=True, exist_ok=True)
    path = state_dir / "watch.lock"
    fh = open(path, "a+b")  # noqa: SIM115 - held until _release_lock
    try:
        if os.name == "nt":
            import msvcrt
            fh.seek(0)
            msvcrt.locking(fh.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        fh.close()
        raise SystemExit(f"another watcher is running ({path}); stop it first") from None
    return fh


def _release_lock(fh) -> None:
    if os.name == "nt":
        import msvcrt
        fh.seek(0)
        msvcrt.locking(fh.fileno(), msvcrt.LK_UNLCK, 1)
    fh.close()


def cmd_watch(args: argparse.Namespace) -> int:
    state_dir = Path(args.state_dir)
    lock = _acquire_lock(state_dir)
    for old in state_dir.glob("pr_*.txt"):   # first poll reports every PR as NEW
        old.unlink()
    start = time.monotonic()
    try:
        while time.monotonic() - start < args.max_seconds:
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
        _release_lock(lock)
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
