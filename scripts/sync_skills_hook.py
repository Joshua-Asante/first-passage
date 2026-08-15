#!/usr/bin/env python3
"""PostToolUse hook — deploy in-repo skills to the bundles when a skill file changes.

Mirrors lock_event_hook.py. Reads PostToolUse JSON from stdin. If the edited
file is under .claude/skills/, gates via check_skill_refs.py --all and then
runs sync_skills.py (one-way repo -> deployed bundles) so the deployed copies
never drift from the version-controlled source
(ADR docs/adr/2026-06-04-methodology-skills-under-vc.md §2.2). The recurring
failure this closes: editing a skill in-repo and forgetting `make sync-skills`,
so the running bundle silently lags the source of truth.

Default destinations (see sync_skills.resolve_targets): the AppData
skills-plugin path *and* ~/.claude/skills/ (the user-level bundle Claude Code
sessions load). Explicit --target is not used here — the hook always deploys
to the full default set.

Gate-then-deploy contract (sync_skills.py docstring; ADR §2.2): edits pass the
gate, THEN deploy. If the ref linter fails, the bundles are NOT deployed and the
hook exits 2 — PostToolUse exit 2 surfaces stderr to the agent without blocking
the already-completed edit; the next skill edit re-attempts the deploy. Sync
failures (e.g. the cloud-synced target is offline) likewise exit 2 with the
sync stderr surfaced, never swallowed. Malformed stdin still exits 0 — the
hook must never crash an unrelated edit.

Worktree sessions (repo root under .claude/worktrees/) skip the deploy
entirely: uncommitted branch state must not clobber the shared live bundle.
The main checkout deploys after merge.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def is_under_worktrees(path: Path) -> bool:
    """True if *path* sits inside a `.claude/worktrees/` tree (worktree session)."""
    parts = [s.lower() for s in Path(path).parts]
    return any(
        parts[i] == ".claude" and parts[i + 1] == "worktrees"
        for i in range(len(parts) - 1)
    )


def _iter_paths(tool_input: dict):
    yield str(tool_input.get("file_path", ""))
    for edit in tool_input.get("edits", []) or []:
        yield str(edit.get("file_path", ""))


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    tool_input = data.get("tool_input", {}) or {}
    paths = [p.replace("\\", "/") for p in _iter_paths(tool_input) if p]
    if not any("/.claude/skills/" in p or p.startswith(".claude/skills/") for p in paths):
        return 0

    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    if is_under_worktrees(repo_root):
        return 0

    sync = script_dir / "sync_skills.py"
    if not sync.exists():
        return 0

    # Gate BEFORE deploy (ADR §2.2). Missing gate script also blocks — an
    # ungated deploy is the exact failure mode the contract forbids.
    checker = script_dir / "check_skill_refs.py"
    if not checker.exists():
        print(
            "SKILL SYNC BLOCKED: scripts/check_skill_refs.py missing — cannot "
            "gate, bundle NOT deployed.",
            file=sys.stderr,
        )
        return 2
    gate = subprocess.run(
        [sys.executable, str(checker), "--all"],
        cwd=str(repo_root),
        check=False,
        capture_output=True,
        text=True,
    )
    if gate.returncode != 0:
        print(
            "SKILL SYNC BLOCKED: check_skill_refs.py --all failed — repo edit "
            "kept, bundle NOT deployed; fix the refs and the next skill edit "
            "re-attempts the deploy.",
            file=sys.stderr,
        )
        sys.stderr.write(gate.stdout)
        sys.stderr.write(gate.stderr)
        return 2

    result = subprocess.run(
        [sys.executable, str(sync)],
        cwd=str(repo_root),
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(
            "SKILL SYNC FAILED: sync_skills.py exited "
            f"{result.returncode} — deployed bundle may lag the repo; the next "
            "skill edit re-attempts the deploy.",
            file=sys.stderr,
        )
        sys.stderr.write(result.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
