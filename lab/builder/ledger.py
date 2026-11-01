"""Append-only, hash-chained trial ledger (spec: Trial ledger).

Each line is one JSON entry whose ``entry_sha256`` covers every other field, including the
previous entry's hash, so an edit or deletion anywhere breaks the chain. Cards are appended
before the engine reads any data; K is the number of distinct card hashes ever appended, for one
instrument (``k_scope: instrument``) or across all of them (``k_scope: ledger``). Holdout looks are their own entries and do not count toward K.

``read`` verifies the whole file on every call and raises on anything it cannot vouch for: a
blank, truncated or non-object line, a broken chain, an unknown kind or field set, a card entry
whose YAML does not re-hash to its ``card_sha256``, or a holdout look that is repeated or names
an unledgered card (invariants I-L1..I-L3, I-L5).
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from builder import cards
from builder.cards import Card

GENESIS = "0" * 64
_BASE = {"seq", "prev", "ts", "kind", "run_id", "entry_sha256"}
FIELDS = {"card": _BASE | {"card_sha256", "card_yaml", "family", "instrument"},
          "holdout_look": _BASE | {"card_sha256", "instrument"}}


class LedgerError(RuntimeError):
    pass


def _digest(entry: dict) -> str:
    body = {k: v for k, v in entry.items() if k != "entry_sha256"}
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def read(path: Path) -> list[dict]:
    """Return every entry after verifying the file; raise LedgerError on anything else."""
    path = Path(path)
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    if text and not text.endswith("\n"):
        raise LedgerError(f"{path}: last line is not newline-terminated (truncated write?)")
    entries, prev, card_inst, looked = [], GENESIS, {}, set()
    for n, line in enumerate(text.split("\n")[:-1], 1):
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            raise LedgerError(f"{path}:{n}: not JSON") from None
        if not isinstance(e, dict) or set(e) != FIELDS.get(str(e.get("kind")), set()):
            raise LedgerError(f"{path}:{n}: unknown kind or field set")
        if e["seq"] != n or e["prev"] != prev or e["entry_sha256"] != _digest(e):
            raise LedgerError(f"ledger chain broken at line {n} of {path}")
        if e["kind"] == "card":
            try:
                c = cards.parse(e["card_yaml"])
            except cards.CardError as err:
                raise LedgerError(f"{path}:{n}: ledgered card no longer parses: {err}") from None
            if (c.sha256, c.instrument, c.family) != (e["card_sha256"], e["instrument"], e["family"]):
                raise LedgerError(f"{path}:{n}: card_sha256/instrument/family do not match card_yaml")
            card_inst[c.sha256] = c.instrument
        else:
            if card_inst.get(e["card_sha256"]) != e["instrument"] or e["card_sha256"] in looked:
                raise LedgerError(f"{path}:{n}: holdout look for an unledgered card or a second look")
            looked.add(e["card_sha256"])
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


def append_cards(path: Path, run_id: str, cs: list[Card]) -> list[dict]:
    return [_append(path, "card", run_id, {"card_sha256": c.sha256, "card_yaml": c.source, "family": c.family,
                                           "instrument": c.instrument}) for c in cs]


def append_holdout_look(path: Path, run_id: str, card: Card) -> dict:
    if not contains(path, card.sha256):
        raise LedgerError(f"holdout look for unledgered card {card.id}")
    if any(e["kind"] == "holdout_look" and e["card_sha256"] == card.sha256 for e in read(path)):
        raise LedgerError(f"card {card.id} already had its one holdout look")
    return _append(path, "holdout_look", run_id, {"card_sha256": card.sha256, "instrument": card.instrument})


def contains(path: Path, card_sha256: str) -> bool:
    return any(e["kind"] == "card" and e["card_sha256"] == card_sha256 for e in read(path))


def k(path: Path, instrument: str | None) -> int:
    """Distinct ledgered card hashes for ``instrument``, or across every instrument when None."""
    return len({e["card_sha256"] for e in read(path)
                if e["kind"] == "card" and instrument in (None, e["instrument"])})
