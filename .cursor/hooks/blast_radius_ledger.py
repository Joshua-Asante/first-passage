#!/usr/bin/env python3
"""Shared edit-ledger helpers for blast-radius Cursor hooks.

Ledger lives under ``.cursor/hooks/state/`` (gitignored). Fail-open everywhere:
ledger I/O errors never block edits or stop.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

# Paths we never treat as judgment-surface edits (meta / ephemeral).
_SKIP_PATH_RES = (
    re.compile(r"(^|[/\\])\.cursor[/\\]hooks[/\\]state([/\\]|$)"),
    re.compile(r"(^|[/\\])\.git([/\\]|$)"),
    re.compile(r"(^|[/\\])__pycache__([/\\]|$)"),
    re.compile(r"\.pyc$"),
)

# Hot surfaces where a missed propagation is expensive (Rule 7 + orientation).
_HOT_PATH_RES = (
    re.compile(r"(^|[/\\])CLAUDE\.md$", re.I),
    re.compile(r"(^|[/\\])STATE\.md$", re.I),
    re.compile(r"(^|[/\\])PIPELINES\.md$", re.I),
    re.compile(r"(^|[/\\])REPO_MAP\.md$", re.I),
    re.compile(r"(^|[/\\])README\.md$", re.I),
    re.compile(r"(^|[/\\])docs([/\\]|$)"),
    re.compile(r"(^|[/\\])\.claude[/\\]skills([/\\]|$)"),
    re.compile(r"(^|[/\\])lab[/\\]CATALOG\.md$", re.I),
    re.compile(r"(^|[/\\])ops[/\\]instruments([/\\]|$)"),
    re.compile(r"(^|[/\\])core[/\\]strategies[/\\].*\.md$", re.I),
)


def repo_root() -> Path:
    # .cursor/hooks/<file>.py → parents[2] is repo root
    return Path(__file__).resolve().parents[2]


def state_dir(root: Path | None = None) -> Path:
    d = (root or repo_root()) / ".cursor" / "hooks" / "state"
    d.mkdir(parents=True, exist_ok=True)
    return d


def ledger_path(conversation_id: str, root: Path | None = None) -> Path:
    safe = re.sub(r"[^a-zA-Z0-9._-]+", "_", conversation_id or "default")[:120]
    return state_dir(root) / f"{safe}.json"


def normalize_rel(file_path: str, root: Path | None = None) -> str:
    root = root or repo_root()
    try:
        p = Path(file_path)
        if p.is_absolute():
            return p.resolve().relative_to(root.resolve()).as_posix()
        return p.as_posix()
    except Exception:
        return str(file_path).replace("\\", "/")


def should_skip_path(rel: str) -> bool:
    return any(rx.search(rel) for rx in _SKIP_PATH_RES)


def is_hot_path(rel: str) -> bool:
    return any(rx.search(rel) for rx in _HOT_PATH_RES)


def load_ledger(conversation_id: str, root: Path | None = None) -> dict:
    path = ledger_path(conversation_id, root)
    if not path.exists():
        return {"paths": [], "nudged": False}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"paths": [], "nudged": False}
    if not isinstance(data, dict):
        return {"paths": [], "nudged": False}
    paths = data.get("paths") or []
    if not isinstance(paths, list):
        paths = []
    return {
        "paths": [str(p) for p in paths if p],
        "nudged": bool(data.get("nudged")),
    }


def save_ledger(conversation_id: str, data: dict, root: Path | None = None) -> None:
    path = ledger_path(conversation_id, root)
    payload = {
        "paths": sorted(set(data.get("paths") or [])),
        "nudged": bool(data.get("nudged")),
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def record_edit(conversation_id: str, file_path: str, root: Path | None = None) -> None:
    root = root or repo_root()
    rel = normalize_rel(file_path, root)
    if should_skip_path(rel):
        return
    data = load_ledger(conversation_id, root)
    if rel not in data["paths"]:
        data["paths"].append(rel)
        # New edits after a prior nudge reopen the debt for the next stop.
        data["nudged"] = False
        save_ledger(conversation_id, data, root)


def hot_paths(data: dict) -> list[str]:
    return [p for p in data.get("paths") or [] if is_hot_path(p)]
