"""Stage 8 holdout looks: ``python -m builder.holdout <run.yaml>`` (the same run.yaml as builder.run).

Refused, before any look, unless the development attempt that run.yaml describes finished:
``out/verdict.json`` (deleted by builder.run before it ledgers, written last) lists exactly the
cards in run.yaml with each ``out/<card id>.report.json``'s sha256, and every report has this
run_id, a final verdict (survivor | killed | unresolved) and the evaluation inputs run.yaml and
the engine give now (``BOUND``): card hash, split, calendar and data sha256, firm, cost per trade
and engine sha256. The survivors are the cards whose report verdict is ``survivor``. Looks are
taken in card-id order, each ledgered (``ledger.append_holdout_look``) before its holdout bars are
simulated, and each writes ``out/<card id>.holdout.json``.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from builder import data, gates, run

FINAL = {"survivor", "killed", "unresolved"}
BOUND = ("card_sha256", "split", "calendar_sha256", "data_sha256", "firm", "cost_per_trade_usd", "engine_sha256")


class HoldoutError(run.RunError):
    pass


def _read(path: Path):
    try:
        return path.read_bytes(), json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        raise HoldoutError(f"{path}: missing or not JSON; the development run has not finished") from None


def survivors(s: dict, cs: list, cost: dict) -> list:
    """The cards with a survivor report, in card-id order, after checking every report."""
    out = Path(s["out"])
    _, listed = _read(out / "verdict.json")
    if not isinstance(listed, list) or any(not isinstance(v, dict) for v in listed):
        raise HoldoutError(f"{out / 'verdict.json'} is not a list of card verdicts")
    marked = {v.get("card"): v.get("report_sha256") for v in listed}
    if sorted(marked) != sorted(c.id for c in cs) or len(marked) != len(listed):
        raise HoldoutError(f"{out / 'verdict.json'} does not list exactly the cards in run.yaml")
    engine = gates.engine_version()
    keep = []
    for c in sorted(cs, key=lambda c: c.id):
        raw, rep = _read(out / f"{c.id}.report.json")
        if hashlib.sha256(raw).hexdigest() != marked[c.id]:
            raise HoldoutError(f"{c.id}: report is not the one verdict.json recorded (stale or edited)")
        if not isinstance(rep, dict) or rep.get("run_id") != s["run_id"] or rep.get("verdict") not in FINAL:
            raise HoldoutError(f"{c.id}: no final development report for run {s['run_id']}")
        want = {"card_sha256": c.sha256, "split": s["data"][c.instrument]["split"],
                "calendar_sha256": s["calendar"]["sha256"], "data_sha256": s["data"][c.instrument]["sha256"],
                "firm": s["firm"], "cost_per_trade_usd": cost[c.instrument].per_trade(c.instrument),
                "engine_sha256": engine}
        for k in BOUND:
            if rep.get(k) != want[k]:
                raise HoldoutError(f"{c.id}: report {k} {rep.get(k)!r} != the {want[k]!r} run.yaml and the engine give now")
        if rep["verdict"] == "survivor":
            keep.append(c)
    return keep


def main(argv: list[str]) -> int:
    s = run.spec(Path(argv[0]))
    cs = run.load_cards(s)
    cost = run.costs(s, sorted({c.instrument for c in cs}))
    keep = survivors(s, cs, cost)
    cal = data.load_calendar(Path(s["calendar"]["path"]), s["calendar"]["sha256"])
    loaded = {i: run.load_data(s, i, cal) for i in sorted({c.instrument for c in keep})}
    out = Path(s["out"])
    for c in keep:
        bars, _, hold, summary = loaded[c.instrument]
        look = gates.holdout_look(c, bars, hold, Path(s["ledger"]), s["run_id"], cost[c.instrument], closed=cal.closed)
        look.update(card_id=c.id, run_id=s["run_id"], split=s["data"][c.instrument]["split"],
                    data_sha256=summary["sha256"], calendar_sha256=cal.sha256)
        (out / f"{c.id}.holdout.json").write_text(json.dumps(look, indent=1), encoding="utf-8")
        print({k: look[k] for k in ("card_id", "verdict", "pass")})
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
