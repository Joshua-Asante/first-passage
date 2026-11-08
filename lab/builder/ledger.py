"""Append-only, hash-chained trial ledger with a head anchor (spec: Trial ledger).

Each line is one JSON entry whose ``entry_sha256`` covers every other field, including the
previous entry's hash, so an edit, reordering or interior deletion breaks the chain. Cards are
appended before the engine reads any data; K is the number of distinct card hashes ever appended,
for one instrument (``k_scope: instrument``) or across all of them (``k_scope: ledger``). Holdout
looks are their own entries and do not count toward K.

A chain alone accepts any valid prefix, so a truncated tail or an older copy of the file would
read clean, lose a holdout look and shrink K. The head anchor ``<ledger>.head`` (``{"seq",
"entry_sha256"}`` of the last entry) closes that: it is rewritten atomically after every append,
and ``read`` refuses a non-empty ledger without an anchor, a ledger (or a missing ledger) that
does not hold its anchor's seq with that hash, and a ledger longer than its anchor.

Crash order: an append writes and fsyncs the ledger line(s), then replaces the anchor. A crash
between the two leaves the ledger longer than its anchor, which ``read`` refuses like any other
mismatch (it cannot tell an interrupted append from a rolled-back anchor) until an operator checks
the tail and runs ``python -m builder.ledger adopt-head <ledger> --confirm <entry_sha256>``.
``read`` never creates an anchor; ``adopt-head`` without ``--confirm`` only prints the head, and
it refuses to write over an anchor the ledger does not hold.

Limit: the anchor lives beside the ledger, so restoring both together (a whole-folder restore from
an older backup) is not detected here. ``builder.holdout`` also checks that the ledger still holds
the head ``builder.run`` recorded in ``verdict.json``; that catches such a restore only when the
run's ``out`` folder was not restored with it.

Every check-and-append (``append_cards``, ``append_holdout_look``) and every ``read`` holds
``exclusive_file_lock(<ledger>)`` (lock file ``<ledger>.lock``) across the read, the validation,
the seq/prev computation, the append and the anchor update, so two callers cannot both spend one
holdout look and a reader never lands between a ledger write and its anchor update.

``read`` verifies the whole file on every call and raises on anything it cannot vouch for: a
blank, truncated or non-object line, a broken chain, an unknown kind or field set, a card entry
whose YAML does not re-hash to its ``card_sha256``, a holdout look that is repeated or names an
unledgered card (invariants I-L1..I-L3, I-L5), or a disagreement with the head anchor.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from lib.atomic_io import atomic_write_text
from lib.file_lock import exclusive_file_lock

from builder import cards
from builder.cards import Card

GENESIS = "0" * 64
_BASE = {"seq", "prev", "ts", "kind", "run_id", "entry_sha256"}
FIELDS = {"card": _BASE | {"card_sha256", "card_yaml", "family", "instrument"},
          "holdout_look": _BASE | {"card_sha256", "instrument"}}
_HEX64 = re.compile(r"[0-9a-f]{64}")


class LedgerError(RuntimeError):
    pass


def _digest(entry: dict) -> str:
    body = {k: v for k, v in entry.items() if k != "entry_sha256"}
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def head_path(path: Path) -> Path:
    path = Path(path)
    return path.with_name(f"{path.name}.head")


def _head_of(entries: list[dict]) -> dict | None:
    return {"seq": entries[-1]["seq"], "entry_sha256": entries[-1]["entry_sha256"]} if entries else None


def check_head(h, what: str) -> dict:
    """``h`` if it is a well-formed head ``{seq: int >= 1, entry_sha256: 64 hex}``; LedgerError otherwise."""
    if not isinstance(h, dict) or set(h) != {"seq", "entry_sha256"} or type(h["seq"]) is not int \
            or h["seq"] < 1 or not isinstance(h["entry_sha256"], str) or not _HEX64.fullmatch(h["entry_sha256"]):
        raise LedgerError(f"{what} is not a ledger head {{seq, entry_sha256}}")
    return h


def _verify(path: Path) -> list[dict]:
    """The chain and content checks, without the anchor."""
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


def _anchor(path: Path) -> dict | None:
    hp = head_path(path)
    if not hp.exists():
        return None
    try:
        h = json.loads(hp.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise LedgerError(f"{hp}: not JSON") from None
    return check_head(h, str(hp))


def _holds(entries: list[dict], h: dict) -> bool:
    """The ledger has ``h``'s seq with ``h``'s hash: it equals or extends the ledger ``h`` was taken from."""
    return len(entries) >= h["seq"] and entries[h["seq"] - 1]["entry_sha256"] == h["entry_sha256"]


def _read_locked(path: Path) -> list[dict]:
    entries = _verify(path)
    h = _anchor(path)
    if h is None:
        if entries:
            raise LedgerError(f"{path}: {len(entries)} entries but no head anchor {head_path(path).name}; "
                              f"verify the ledger, then `python -m builder.ledger adopt-head {path}`")
        return entries
    if not _holds(entries, h):
        raise LedgerError(f"{path}: rolled back or replaced: {len(entries)} entries, and it does not hold its "
                          f"head anchor (seq {h['seq']}, {h['entry_sha256'][:12]})")
    if len(entries) != h["seq"]:
        raise LedgerError(f"{path}: {len(entries) - h['seq']} entries past its head anchor (seq {h['seq']}): an "
                          f"append was interrupted before its anchor was written, or the anchor was rolled back; "
                          f"verify the tail, then `python -m builder.ledger adopt-head {path}`")
    return entries


def read(path: Path) -> list[dict]:
    """Return every entry after verifying the file and its head anchor; raise LedgerError on anything else."""
    path = Path(path)
    if not path.parent.is_dir():  # nothing can be there; do not create the folder just to lock it
        return []
    with exclusive_file_lock(path):
        return _read_locked(path)


def _append_locked(path: Path, entries: list[dict], kind: str, run_id: str, rows: list[dict]) -> list[dict]:
    """Chain ``rows`` onto the verified ``entries``, write and fsync them, then replace the anchor.
    The caller holds the lock and has validated ``rows`` against ``entries``."""
    prev, new = entries[-1]["entry_sha256"] if entries else GENESIS, []
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for fields in rows:
        e = {"seq": len(entries) + len(new) + 1, "prev": prev, "ts": ts, "kind": kind, "run_id": run_id, **fields}
        e["entry_sha256"] = prev = _digest(e)
        new.append(e)
    with open(path, "a", encoding="utf-8", newline="\n") as fh:
        fh.write("".join(json.dumps(e, sort_keys=True, separators=(",", ":")) + "\n" for e in new))
        fh.flush()
        os.fsync(fh.fileno())
    atomic_write_text(head_path(path), json.dumps(_head_of(new)) + "\n")
    return new


def append_cards(path: Path, run_id: str, cs: list[Card]) -> list[dict]:
    path = Path(path)
    if not cs:
        return []
    with exclusive_file_lock(path):
        return _append_locked(path, _read_locked(path), "card", run_id,
                              [{"card_sha256": c.sha256, "card_yaml": c.source, "family": c.family,
                                "instrument": c.instrument} for c in cs])


def append_holdout_look(path: Path, run_id: str, card: Card) -> dict:
    """Spend ``card``'s one holdout look; the checks and the append are one locked transaction."""
    path = Path(path)
    with exclusive_file_lock(path):
        entries = _read_locked(path)
        if not any(e["kind"] == "card" and e["card_sha256"] == card.sha256 for e in entries):
            raise LedgerError(f"holdout look for unledgered card {card.id}")
        if any(e["kind"] == "holdout_look" and e["card_sha256"] == card.sha256 for e in entries):
            raise LedgerError(f"card {card.id} already had its one holdout look")
        [e] = _append_locked(path, entries, "holdout_look", run_id,
                             [{"card_sha256": card.sha256, "instrument": card.instrument}])
        return e


def head(path: Path) -> dict | None:
    """``{seq, entry_sha256}`` of the last verified entry, or None for an empty ledger."""
    return _head_of(read(path))


def check_holds(path: Path, h) -> None:
    """Refuse unless the ledger still holds ``h``, a head recorded earlier (equal or extended since)."""
    h = check_head(h, "recorded ledger head")
    if not _holds(read(path), h):
        raise LedgerError(f"{path} no longer holds the recorded head (seq {h['seq']}, {h['entry_sha256'][:12]}): "
                          f"rolled back or replaced since it was recorded")


def contains(path: Path, card_sha256: str) -> bool:
    return any(e["kind"] == "card" and e["card_sha256"] == card_sha256 for e in read(path))


def k(path: Path, instrument: str | None) -> int:
    """Distinct ledgered card hashes for ``instrument``, or across every instrument when None."""
    return len({e["card_sha256"] for e in read(path)
                if e["kind"] == "card" and instrument in (None, e["instrument"])})


def adopt_head(path: Path, confirm: str | None) -> dict:
    """Verify the chain and report its head and current anchor. Only with ``confirm`` equal to the
    head's entry_sha256 is the anchor written, and never over an anchor the ledger does not hold."""
    path = Path(path)
    if not path.is_file():
        raise LedgerError(f"{path}: no ledger file")
    with exclusive_file_lock(path):
        entries = _verify(path)
        h, anchor = _head_of(entries), _anchor(path)
        out = {"ledger": str(path), "entries": len(entries), "head": h, "anchor": anchor, "written": False}
        if confirm is None:
            return out
        if h is None:
            raise LedgerError(f"{path}: empty ledger; there is no head to anchor")
        if confirm != h["entry_sha256"]:
            raise LedgerError(f"--confirm {confirm[:12]} is not the head entry_sha256 {h['entry_sha256'][:12]}")
        if anchor is not None and not _holds(entries, anchor):
            raise LedgerError(f"{path} does not hold its existing anchor (seq {anchor['seq']}): rolled back or "
                              f"replaced; adopt-head will not overwrite that anchor")
        atomic_write_text(head_path(path), json.dumps(h) + "\n")
        return {**out, "anchor": h, "written": True}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="python -m builder.ledger")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("adopt-head", help="print the verified head; with --confirm, write it as the anchor")
    a.add_argument("ledger", type=Path)
    a.add_argument("--confirm", metavar="ENTRY_SHA256", help="the head entry_sha256 you verified; writes the anchor")
    ns = ap.parse_args(argv)
    print(json.dumps(adopt_head(ns.ledger, ns.confirm), indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
