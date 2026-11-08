"""Stage 8 holdout looks: ``python -m builder.holdout <run.yaml>`` (the same run.yaml as builder.run).

Refused, before any look, unless the current run.yaml describes exactly the finished development
attempt: ``out/verdict.json`` (deleted by builder.run before it ledgers, written last by an atomic
rename) must carry the sha256 that ``run.binding`` recomputes from run.yaml and the engine now,
list exactly run.yaml's cards with each report's sha256, and every report must match its sha256,
carry the same binding sha256, this run_id and a final verdict (survivor | killed | unresolved).
The survivors are the cards whose report verdict is ``survivor``; each survivor's report must
carry well-formed book statistics, checked for every survivor before the first look. The ledger
must still hold the head ``builder.run`` recorded in ``verdict.json`` (``ledger_head``: that seq
with that entry_sha256; later appends are fine), and no survivor may already have an
``out/<card id>.holdout.json`` (defence in depth only: the file can be deleted, so the ledger's
one-look rule and head anchor stay the guard; see ``ledger`` for their limit). Looks are
taken in card-id order, each ledgered (``ledger.append_holdout_look``) before its holdout bars
are simulated, and each writes ``out/<card id>.holdout.json``. After a holdout pass, gate 5g
(step 10 portfolio fit) runs on the development-window book statistics in the card's report, so
no new data is read, and sets ``placement: clear | fail`` in the holdout file, or
``not_evaluated`` when run.yaml declares ``book: null``, with ``placement_book_sha256`` (the
pinned book, inside the same ``dev_binding_sha256``); the look's verdict is unchanged
(``gates.holdout_look``). Gate 5h (``venue.py``) would attach at this stage; it is not wired.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from builder import data, gates, ledger, run

FINAL = {"survivor", "killed", "unresolved"}


class HoldoutError(run.RunError):
    pass


def _read(path: Path):
    try:
        raw = path.read_bytes()
        return raw, json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        raise HoldoutError(f"{path}: missing or not JSON; the development run has not finished") from None


def _differences(old, new, at="") -> list[str]:
    """Names the binding fields that changed, for the refusal message."""
    if isinstance(old, dict) and isinstance(new, dict):
        return [d for k in sorted(set(old) | set(new)) for d in _differences(old.get(k), new.get(k), f"{at}{k}.")]
    return [] if old == new else [at.rstrip(".")]


def survivors(s: dict, cs: list, cost: dict) -> list[tuple]:
    """(card, development report) for each survivor, in card-id order, after checking the binding,
    every report and each survivor's book statistics."""
    out = Path(s["out"])
    _, marker = _read(out / "verdict.json")
    bind = run.binding(s, cs, cost)
    want = run.binding_sha256(bind)
    if not isinstance(marker, dict) or set(marker) != {"dev_binding_sha256", "binding", "ledger_head", "cards"}:
        raise HoldoutError(f"{out / 'verdict.json'} is not a finished development marker")
    if marker["dev_binding_sha256"] != want or run.binding_sha256(marker["binding"]) != want:
        changed = _differences(marker["binding"], bind) or ["dev_binding_sha256"]
        raise HoldoutError(f"run.yaml no longer describes the development run; changed: {changed}")
    listed = marker["cards"]
    if not isinstance(listed, list) or any(not isinstance(v, dict) for v in listed):
        raise HoldoutError(f"{out / 'verdict.json'} cards is not a list of card verdicts")
    marked = {v.get("card"): v.get("report_sha256") for v in listed}
    if sorted(marked) != sorted(c.id for c in cs) or len(marked) != len(listed):
        raise HoldoutError(f"{out / 'verdict.json'} does not list exactly the cards in run.yaml")
    keep = []
    for c in sorted(cs, key=lambda c: c.id):
        raw, rep = _read(out / f"{c.id}.report.json")
        if hashlib.sha256(raw).hexdigest() != marked[c.id]:
            raise HoldoutError(f"{c.id}: report is not the one verdict.json recorded (stale or edited)")
        if not isinstance(rep, dict) or rep.get("dev_binding_sha256") != want or rep.get("run_id") != s["run_id"] \
                or rep.get("card_sha256") != c.sha256 or rep.get("verdict") not in FINAL:
            raise HoldoutError(f"{c.id}: no final development report for this binding")
        if rep["verdict"] == "survivor":
            try:
                gates.check_book_stats(rep.get("book"))
                gates.check_book_identity(rep["book"], None if s["book"] is None else s["book"]["sha256"])
            except gates.GateError as e:
                raise HoldoutError(f"{c.id}: {e}") from None
            keep.append((c, rep))
    try:
        ledger.check_holds(Path(s["ledger"]), marker["ledger_head"])
    except ledger.LedgerError as e:
        raise HoldoutError(str(e)) from None
    done = [c.id for c, _ in keep if (out / f"{c.id}.holdout.json").exists()]
    if done:
        raise HoldoutError(f"{done} already have a holdout result in {out}; a look is never retaken")
    return keep


def main(argv: list[str]) -> int:
    s = run.spec(Path(argv[0]))
    cs = run.load_cards(s)
    cost = run.costs(s, sorted({c.instrument for c in cs}))
    keep = survivors(s, cs, cost)
    cal = data.load_calendar(Path(s["calendar"]["path"]), s["calendar"]["sha256"])
    loaded = {i: run.load_data(s, i, cal) for i in sorted({c.instrument for c, _ in keep})}
    out = Path(s["out"])
    for c, rep in keep:
        bars, _, hold, summary = loaded[c.instrument]
        look = gates.holdout_look(c, bars, hold, Path(s["ledger"]), s["run_id"], cost[c.instrument], closed=cal.closed,
                                  book=rep["book"], book_sha256=None if s["book"] is None else s["book"]["sha256"])
        look.update(card_id=c.id, run_id=s["run_id"], split=s["data"][c.instrument]["split"],
                    data_sha256=summary["sha256"], calendar_sha256=cal.sha256,
                    dev_binding_sha256=run.binding_sha256(run.binding(s, cs, cost)))
        (out / f"{c.id}.holdout.json").write_text(json.dumps(look, indent=1), encoding="utf-8")
        print({k: look[k] for k in ("card_id", "verdict", "pass", "placement")})
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
