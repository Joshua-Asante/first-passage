"""Append-only, hash-chained trial ledger (spec: Trial ledger).

Each line is one JSON entry whose ``entry_sha256`` covers every other field, including the
previous entry's hash, so an edit or deletion anywhere breaks the chain. Cards are appended
before the engine reads any data; K for an instrument is the number of distinct card hashes
ever appended for it. Holdout looks are their own entries and do not count toward K.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from builder.cards import Card

GENESIS = "0" * 64


class LedgerError(RuntimeError):
    pass


def _digest(entry: dict) -> str:
    body = {k: v for k, v in entry.items() if k != "entry_sha256"}
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def read(path: Path) -> list[dict]:
    """Return every entry after verifying the chain; raise LedgerError on any break."""
    path = Path(path)
    if not path.exists():
        return []
    entries, prev = [], GENESIS
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        e = json.loads(line)
        if e.get("seq") != n or e.get("prev") != prev or e.get("entry_sha256") != _digest(e):
            raise LedgerError(f"ledger chain broken at line {n} of {path}")
        entries.append(e)
        prev = e["entry_sha256"]
    return entries


def _append(path: Path, kind: str, run_id: str, fields: dict) -> dict:
    entries = read(path)
    e = {"seq": len(entries) + 1, "prev": entries[-1]["entry_sha256"] if entries else GENESIS,
         "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"), "kind": kind, "run_id": run_id, **fields}
    e["entry_sha256"] = _digest(e)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(e, sort_keys=True, separators=(",", ":")) + "\n")
    return e


def append_cards(path: Path, run_id: str, cards: list[Card]) -> list[dict]:
    return [_append(path, "card", run_id, {"card_sha256": c.sha256, "card_yaml": c.source, "family": c.family,
                                           "instrument": c.instrument}) for c in cards]


def append_holdout_look(path: Path, run_id: str, card: Card) -> dict:
    if not contains(path, card.sha256):
        raise LedgerError(f"holdout look for unledgered card {card.id}")
    if any(e["kind"] == "holdout_look" and e["card_sha256"] == card.sha256 for e in read(path)):
        raise LedgerError(f"card {card.id} already had its one holdout look")
    return _append(path, "holdout_look", run_id, {"card_sha256": card.sha256, "instrument": card.instrument})


def contains(path: Path, card_sha256: str) -> bool:
    return any(e["kind"] == "card" and e["card_sha256"] == card_sha256 for e in read(path))


def k(path: Path, instrument: str) -> int:
    return len({e["card_sha256"] for e in read(path) if e["kind"] == "card" and e["instrument"] == instrument})
