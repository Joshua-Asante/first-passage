#!/usr/bin/env python3
"""check_order.py — mechanical gates for The Order (docs/framework/the-order.md).

Reads docs/framework/order-state.json. Three entry points:

  * default (gate; listed in scripts/gates.yml, so it runs in pre-commit and in the
    required ``skills (3.12)`` CI job):
      - every registration's file matches its recorded sha256;
      - a registration whose test has started (``started`` set) is frozen: compared
        with the base, its entry and file may not change or disappear;
      - an active quarantine may not be removed, moved or shortened;
      - during a quarantine that is active on the base, the change adds no
        registration, changes no contract, and every commit subject starts with
        ``closure:`` (CI only; pre-commit cannot see the commit message).
  * ``--session-start``: a Claude Code SessionStart hook that puts the current state of
    The Order in front of every agent session.
  * ``--pre-tool-use``: a Claude Code PreToolUse hook that refuses Edit/Write calls on a
    frozen registration. Best effort: CI is the enforcement boundary.

Hashes are of the committed blob (``git show HEAD:<path> | sha256sum``), so line-ending
conversion in a working tree does not change them. Stdlib only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = "docs/framework/order-state.json"
CLOSURE_PREFIX = "closure:"
STEPS = ("aim", "ask", "subtract", "choose", "register", "run", "rule", "stop")
MODES = ("witness", "holder")
EMPTY_STATE: dict = {"version": 1, "mode": "witness", "step": "aim", "contract": None,
                     "quarantine": None, "registrations": []}


# ---------------------------------------------------------------- pure checks

def today() -> dt.date:
    override = os.environ.get("ORDER_TODAY")
    return dt.date.fromisoformat(override) if override else dt.datetime.now(dt.timezone.utc).date()


_ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def _date(value, field: str, errors: list[str]) -> dt.date | None:
    """Only canonical YYYY-MM-DD: fromisoformat also accepts e.g. 20261215."""
    try:
        if not isinstance(value, str) or not _ISO_DATE.fullmatch(value):
            raise ValueError
        return dt.date.fromisoformat(value)
    except (TypeError, ValueError):
        errors.append(f"{field}: expected a YYYY-MM-DD date, got {value!r}")
        return None


def validate_schema(state: dict) -> list[str]:
    errors: list[str] = []
    if state.get("version") != 1:
        errors.append("version: must be 1")
    if state.get("mode") not in MODES:
        errors.append(f"mode: must be one of {', '.join(MODES)}")
    if state.get("step") not in STEPS:
        errors.append(f"step: must be one of {', '.join(STEPS)}")
    contract = state.get("contract")
    if contract is not None:
        if not isinstance(contract, dict) or not {"path", "sha256", "end_date"} <= contract.keys():
            errors.append("contract: must be null or have path, sha256 and end_date")
        else:
            _date(contract["end_date"], "contract.end_date", errors)
    q = state.get("quarantine")
    if q is not None:
        if not isinstance(q, dict) or not {"start", "until"} <= q.keys():
            errors.append("quarantine: must be null or have start and until")
        else:
            start = _date(q["start"], "quarantine.start", errors)
            until = _date(q["until"], "quarantine.until", errors)
            if start and until and (until - start).days < 14:
                errors.append("quarantine: must last at least 14 days")
    regs = state.get("registrations")
    if not isinstance(regs, list):
        errors.append("registrations: must be a list")
        return errors
    seen: set[str] = set()
    for i, reg in enumerate(regs):
        where = f"registrations[{i}]"
        if not isinstance(reg, dict) or not {"id", "path", "sha256", "started"} <= reg.keys():
            errors.append(f"{where}: must have id, path, sha256 and started")
            continue
        if reg["id"] in seen:
            errors.append(f"{where}: duplicate id {reg['id']!r}")
        seen.add(reg["id"])
        if reg["started"] is not None:
            _date(reg["started"], f"{where}.started", errors)
    return errors


def quarantine_active(state: dict, on: dt.date) -> bool:
    q = state.get("quarantine")
    if not q:
        return False
    try:
        return dt.date.fromisoformat(q["start"]) <= on <= dt.date.fromisoformat(q["until"])
    except (KeyError, TypeError, ValueError):
        return False


def check_hashes(state: dict, read, is_regular=lambda path: True, *, started_only: bool = False) -> list[str]:
    """``read(path) -> bytes | None``; ``is_regular(path)`` is False for a symlink or
    submodule, whose committed bytes are not the document. Every registration (and the
    contract) is a regular file matching its hash."""
    errors: list[str] = []
    items = [(f"registration {r['id']}", r) for r in state.get("registrations", [])
             if r.get("started") or not started_only]
    if state.get("contract") and not started_only:
        items.append(("contract", state["contract"]))
    for label, item in items:
        data = read(item["path"])
        if data is None:
            errors.append(f"{label}: {item['path']} does not exist")
        elif not is_regular(item["path"]):
            errors.append(f"{label}: {item['path']} must be a regular file, not a symlink or submodule")
        elif hashlib.sha256(data).hexdigest() != item["sha256"]:
            errors.append(f"{label}: {item['path']} does not match its recorded sha256 "
                          "(a registration that has not started needs its new hash recorded; "
                          "one that has started is frozen)")
    return errors


def check_transition(base: dict, head: dict, on: dt.date) -> list[str]:
    errors: list[str] = []
    head_regs = {r["id"]: r for r in head.get("registrations", [])}
    for reg in base.get("registrations", []):
        if reg.get("started") is None:
            continue
        new = head_regs.get(reg["id"])
        if new is None:
            errors.append(f"registration {reg['id']}: frozen (started {reg['started']}) and may not be removed")
        elif any(new.get(k) != reg.get(k) for k in ("path", "sha256", "started")):
            errors.append(f"registration {reg['id']}: frozen (started {reg['started']}); "
                          "its path, sha256 and start date may not change. Replace it with a new registration")
    if quarantine_active(base, on):
        bq, hq = base["quarantine"], head.get("quarantine")
        head_until = _date(hq.get("until"), "quarantine.until", []) if hq else None
        if not hq or hq.get("start") != bq["start"] or head_until is None \
                or head_until < dt.date.fromisoformat(bq["until"]):
            errors.append(f"quarantine: active until {bq['until']}; it may not be removed, moved or shortened")
        base_regs = {r["id"]: r for r in base.get("registrations", [])}
        changed = sorted(i for i in set(base_regs) | set(head_regs) if base_regs.get(i) != head_regs.get(i))
        if changed:
            errors.append(f"quarantine: no registration may be added, changed or started until {bq['until']} "
                          f"(changed: {', '.join(changed)})")
        if head.get("contract") != base.get("contract"):
            errors.append(f"quarantine: the contract may not change until {bq['until']}")
    return errors


def check_commit_subjects(subjects: list[str], base: dict, on: dt.date) -> list[str]:
    if not quarantine_active(base, on):
        return []
    bad = [s for s in subjects if not s.startswith(CLOSURE_PREFIX)]
    if not bad:
        return []
    until = base["quarantine"]["until"]
    return [f"quarantine: active until {until}; only `{CLOSURE_PREFIX}` commits are allowed. "
            f"Offending: {'; '.join(bad[:5])}"]


def status_text(state: dict, on: dt.date) -> str:
    lines = ["THE ORDER — this repository runs under docs/framework/the-order.md "
             f"(state: {STATE_PATH}).",
             f"Mode: {state.get('mode')}. Step: {state.get('step')}."]
    c = state.get("contract")
    if c:
        overdue = dt.date.fromisoformat(c["end_date"]) < on
        lines.append(f"Contract: {c['path']}, ends {c['end_date']}" + (" — PAST END DATE: work stops." if overdue else "."))
    else:
        lines.append("Contract: none. No programme work (builds, tests, spend) until Joshua writes and hashes one; "
                     "stopping or shrinking needs no contract.")
    if quarantine_active(state, on):
        q = state["quarantine"]
        lines.append(f"QUARANTINE until {q['until']}: closure-only commits (`{CLOSURE_PREFIX}`), no successors, "
                     "no reopening proposals, agents draft no options.")
    for r in state.get("registrations", []):
        lines.append(f"Registration {r['id']}: {r['path']} — "
                     + (f"FROZEN since {r['started']}." if r.get("started") else "not started; editable, re-hash on change."))
    lines.append("Before acting on a request, name its step in The Order and check that step's gate. If a gate "
                 "is unmet (no contract, an unanswered outside question, an unregistered test, a same-day ruling, "
                 "quarantine), say so and do not proceed with that work. Silence means STOP.")
    return "\n".join(lines)


# ---------------------------------------------------------------- git plumbing

def _git(*args: str) -> str | None:
    r = subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True)
    return r.stdout.decode("utf-8", "replace") if r.returncode == 0 else None


def _git_bytes(spec: str) -> bytes | None:
    r = subprocess.run(["git", "show", spec], cwd=REPO_ROOT, capture_output=True)
    return r.stdout if r.returncode == 0 else None


def _is_regular(prefix: str, path: str) -> bool:
    """Mode 100644/100755 in the tree (``REV:``) or index (``:``) the reader uses."""
    if prefix == ":":
        out = _git("ls-files", "-s", "--", path) or ""
    else:
        out = _git("ls-tree", prefix.rstrip(":"), "--", path) or ""
    return out.split(" ", 1)[0] in ("100644", "100755")


def _load(data: bytes | None) -> dict:
    return json.loads(data) if data is not None else dict(EMPTY_STATE)


class StateError(ValueError):
    """The state file is unreadable as committed: not regular, or not JSON."""


def _state_at(prefix: str) -> dict:
    """The state as committed at ``prefix`` (``REV:`` or ``:`` for the index). A symlink's
    blob is its target path, so the state file must be a regular file to be read at all."""
    data = _git_bytes(f"{prefix}{STATE_PATH}")
    if data is not None and not _is_regular(prefix, STATE_PATH):
        raise StateError(f"{STATE_PATH} must be a regular file, not a symlink or submodule")
    try:
        return _load(data)
    except json.JSONDecodeError as exc:
        raise StateError(f"{STATE_PATH} is not valid JSON: {exc}") from exc


def _target_rev() -> str | None:
    """The current tip of the branch a pull_request merges into."""
    if os.environ.get("GITHUB_EVENT_NAME") != "pull_request":
        return None
    ref = os.environ.get("GITHUB_BASE_REF", "main")
    return (_git("rev-parse", "--verify", "-q", f"origin/{ref}") or "").strip() or None


def resolve_context() -> tuple[str | None, str, str | None]:
    """(base rev or None, head prefix for `git show`, tip of the commits under review).

    On ``pull_request`` HEAD is GitHub's synthetic merge, so the commits under review
    end at the PR head named in the event payload; every commit in range is checked,
    authored merges included.
    """
    event = os.environ.get("GITHUB_EVENT_NAME")
    if event not in ("pull_request", "push"):  # local / pre-commit: staged index against HEAD
        base = (_git("rev-parse", "--verify", "-q", "HEAD") or "").strip() or None
        return base, ":", None
    tip = "HEAD"
    if event == "pull_request":
        tip = _pr_head_sha() or tip
    if event == "pull_request":
        base_ref = os.environ.get("GITHUB_BASE_REF", "main")
        base = (_git("merge-base", f"origin/{base_ref}", tip) or "").strip() or None
    else:
        base = (_git("rev-parse", "--verify", "-q", "HEAD^1") or "").strip() or None
    return base, "HEAD:", tip


def _pr_head_sha() -> str | None:
    """The PR's own head commit, from the event payload GitHub writes for every run."""
    try:
        with open(os.environ["GITHUB_EVENT_PATH"], encoding="utf-8") as fh:
            sha = json.load(fh)["pull_request"]["head"]["sha"]
    except (KeyError, OSError, TypeError, json.JSONDecodeError):
        return None
    return sha if isinstance(sha, str) and re.fullmatch(r"[0-9a-f]{40}", sha) else None


def check_range(base: str, tip: str, on: dt.date) -> list[str]:
    """Every commit in base..tip, against each of its parents: a registration frozen in
    one commit of a PR cannot be rewritten by a later one, and every commit (merges
    included) during an active quarantine carries the closure prefix."""
    errors: list[str] = []
    out = _git("rev-list", "--reverse", "--topo-order", "--parents", f"{base}..{tip}") or ""
    for line in out.splitlines():
        commit, *parents = line.split()
        short = commit[:8]
        try:
            head = _state_at(f"{commit}:")
            invalid = validate_schema(head)
            if invalid:  # an invalid draft would break the freeze history: reject it
                errors += [f"{short}: {e}" for e in invalid]
                continue
            errors += [f"{short}: {e}" for e in check_hashes(
                head, lambda p, c=commit: _git_bytes(f"{c}:{p}"),
                lambda p, c=commit: _is_regular(f"{c}:", p), started_only=True)]
            for parent in parents:
                parent_state = _state_at(f"{parent}:")
                if validate_schema(parent_state):
                    continue
                errors += [f"{short}: {e}" for e in check_transition(parent_state, head, on)]
                subject = (_git("log", "-1", "--format=%s", commit) or "").strip()
                errors += [f"{short}: {e}" for e in check_commit_subjects([subject], parent_state, on)]
        except StateError as exc:
            errors.append(f"{short}: {exc}")
    return sorted(set(errors), key=errors.index)


def run_gate() -> int:
    on = today()
    base_rev, head_prefix, tip = resolve_context()
    try:
        head = _state_at(head_prefix)
        base = _state_at(f"{base_rev}:") if base_rev else dict(EMPTY_STATE)
    except StateError as exc:
        print(f"order-gates: {exc}", file=sys.stderr)
        return 1
    errors = validate_schema(head)
    if not errors:
        errors += check_hashes(head, lambda p: _git_bytes(f"{head_prefix}{p}"),
                               lambda p: _is_regular(head_prefix, p))
        errors += check_transition(base, head, on)
        target = _target_rev()
        if target and target != base_rev:
            # main may have frozen a registration or started a quarantine after the PR
            # branched: the merged state must also respect the target as it is now.
            try:
                target_state = _state_at(f"{target}:")
            except StateError as exc:  # fail closed: the target's obligations are unknown
                errors.append(f"target {target[:8]}: {exc}")
                target_state = {"version": 0}
            if not validate_schema(target_state):
                errors += check_transition(target_state, head, on)
                if base_rev and tip and quarantine_active(target_state, on):
                    out = _git("log", "--format=%s", f"{base_rev}..{tip}") or ""
                    errors += check_commit_subjects([x for x in out.splitlines() if x.strip()], target_state, on)
        if tip and tip != "HEAD":
            # The PR head's own freezes bind the merge too: main may have rewritten a
            # registration the PR started.
            try:
                tip_state = _state_at(f"{tip}:")
                if not validate_schema(tip_state):
                    errors += check_transition(tip_state, head, on)
            except StateError:
                pass  # check_range reports an unreadable PR head
        if base_rev and tip:
            errors += check_range(base_rev, tip, on)
            if quarantine_active(base, on):
                out = _git("log", "--format=%s", f"{base_rev}..{tip}") or ""
                errors += check_commit_subjects([x for x in out.splitlines() if x.strip()], base, on)
    for e in sorted(set(errors), key=errors.index):
        print(f"order-gates: {e}", file=sys.stderr)
    return 1 if errors else 0


def _working_state() -> dict:
    p = REPO_ROOT / STATE_PATH
    if p.is_symlink():
        raise StateError(f"{STATE_PATH} must be a regular file, not a symlink")
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else dict(EMPTY_STATE)


def run_session_start() -> int:
    try:
        text = status_text(_working_state(), today())
    except (json.JSONDecodeError, KeyError, ValueError) as exc:
        text = f"THE ORDER: {STATE_PATH} could not be read ({exc}); treat every gate as unmet."
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": text}}))
    return 0


def frozen_paths(state: dict) -> set[str]:
    return {r["path"] for r in state.get("registrations", []) if r.get("started")}


def run_pre_tool_use(stdin_text: str) -> int:
    try:
        payload = json.loads(stdin_text or "{}")
        tool_input = payload.get("tool_input") or {}
        target = tool_input.get("file_path") or tool_input.get("notebook_path")
        if not target:
            return 0
        root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or REPO_ROOT).resolve()
        resolved = Path(target) if Path(target).is_absolute() else root / target
        rel = resolved.resolve().relative_to(root).as_posix()
        frozen = frozen_paths(_working_state())
    except (json.JSONDecodeError, ValueError, KeyError, OSError):
        return 0  # not ours to judge; CI remains the gate
    if rel in frozen:
        reason = (f"The Order: {rel} is a registration whose test has started, so it is frozen. "
                  "Write a new registration instead (it counts against the round limit).")
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                                 "permissionDecision": "deny",
                                                 "permissionDecisionReason": reason}}))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--session-start", action="store_true")
    mode.add_argument("--pre-tool-use", action="store_true")
    args = ap.parse_args(argv)
    if args.session_start:
        return run_session_start()
    if args.pre_tool_use:
        return run_pre_tool_use(sys.stdin.read())
    return run_gate()


if __name__ == "__main__":
    sys.exit(main())
