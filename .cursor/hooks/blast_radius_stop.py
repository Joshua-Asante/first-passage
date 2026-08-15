#!/usr/bin/env python3
"""Cursor stop hook — nudge blast-radius skill after hot-surface edits.

When the agent completes a turn that edited judgment-linked surfaces and has
not yet emitted a ``BLAST-RADIUS:`` report, return a one-shot
``followup_message`` pointing at ``.claude/skills/blast-radius/SKILL.md``.

Guards:
  * status must be ``completed``
  * ``loop_count == 0`` (hooks.json ``loop_limit: 1`` is the hard cap)
  * ledger has at least one hot path for this conversation
  * ledger not already ``nudged`` for the current path set
  * transcript (when present) does not already contain ``BLAST-RADIUS:``

Fail-open: any error → ``{}``.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from blast_radius_ledger import hot_paths, load_ledger, repo_root, save_ledger  # noqa: E402

FOLLOWUP = (
    "Before ending: run the `blast-radius` skill "
    "`.claude/skills/blast-radius/SKILL.md` on this turn's edits. "
    "Deliver a `BLAST-RADIUS: CLEAN|OWED|REPAIRED` report — surface linked "
    "owners/mirrors that may still restate the prior finding (Rule 7). "
    "Report-first; fix only clear silent restatements and stale one-line "
    "pointers owed by this change. Do not restate canonical values."
)


def _transcript_has_report(transcript_path: str | None) -> bool:
    if not transcript_path:
        return False
    path = Path(transcript_path)
    if not path.is_file():
        return False
    try:
        # Tail-read: report should appear near the end of this turn.
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return False
    return "BLAST-RADIUS:" in text


def _emit(payload: dict) -> None:
    sys.stdout.write(json.dumps(payload))
    sys.stdout.flush()


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        _emit({})
        return 0

    if not isinstance(data, dict):
        _emit({})
        return 0

    status = str(data.get("status") or "")
    try:
        loop_count = int(data.get("loop_count") or 0)
    except (TypeError, ValueError):
        loop_count = 0

    if status != "completed" or loop_count != 0:
        _emit({})
        return 0

    if _transcript_has_report(data.get("transcript_path")):
        _emit({})
        return 0

    conversation_id = str(data.get("conversation_id") or "default")
    root = repo_root()
    try:
        ledger = load_ledger(conversation_id, root)
    except Exception as exc:
        sys.stderr.write(f"[blast-radius stop] ledger load: {exc}\n")
        _emit({})
        return 0

    hot = hot_paths(ledger)
    if not hot:
        _emit({})
        return 0

    if ledger.get("nudged"):
        _emit({})
        return 0

    try:
        ledger["nudged"] = True
        save_ledger(conversation_id, ledger, root)
    except Exception as exc:
        sys.stderr.write(f"[blast-radius stop] ledger save: {exc}\n")

    preview = ", ".join(hot[:8])
    if len(hot) > 8:
        preview += f", +{len(hot) - 8} more"
    sys.stderr.write(f"[blast-radius stop] nudge for: {preview}\n")

    _emit({"followup_message": FOLLOWUP})
    return 0


if __name__ == "__main__":
    sys.exit(main())
