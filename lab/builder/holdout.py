"""Stage 8 holdout looks: ``python -m builder.holdout <run.yaml>`` (the same run.yaml as builder.run).

Refused, before any look, unless the development run finished: ``out/verdict.json`` lists every
card in run.yaml and each card has its ``out/<card id>.report.json`` with this run_id, a final
verdict (survivor | killed | unresolved), and the card hash and split that run.yaml gives now.
The survivors are the cards whose report verdict is ``survivor``. Looks are taken in card-id
order, each ledgered (``ledger.append_holdout_look``) before its holdout bars are simulated, and
each writes ``out/<card id>.holdout.json``.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from builder import data, gates, run

FINAL = {"survivor", "killed", "unresolved"}


class HoldoutError(run.RunError):
    pass


def _read(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        raise HoldoutError(f"{path}: missing or not JSON; the development run has not finished") from None


def survivors(s: dict, cs: list) -> list:
    """The cards with a survivor report, in card-id order, after checking every report."""
    out = Path(s["out"])
    listed = _read(out / "verdict.json")
    ids = sorted(c.id for c in cs)
    if not isinstance(listed, list) or sorted(v.get("card") for v in listed if isinstance(v, dict)) != ids:
        raise HoldoutError(f"{out / 'verdict.json'} does not list exactly the cards in run.yaml")
    keep = []
    for c in sorted(cs, key=lambda c: c.id):
        rep = _read(out / f"{c.id}.report.json")
        if not isinstance(rep, dict) or rep.get("run_id") != s["run_id"] or rep.get("verdict") not in FINAL:
            raise HoldoutError(f"{c.id}: no final development report for run {s['run_id']}")
        if rep.get("card_sha256") != c.sha256:
            raise HoldoutError(f"{c.id}: report card hash {rep.get('card_sha256')} != run.yaml card {c.sha256}")
        if rep.get("split") != s["data"][c.instrument]["split"]:
            raise HoldoutError(f"{c.id}: report split {rep.get('split')} != run.yaml split {s['data'][c.instrument]['split']}")
        if rep["verdict"] == "survivor":
            keep.append(c)
    return keep


def main(argv: list[str]) -> int:
    s = run.spec(Path(argv[0]))
    cs = run.load_cards(s)
    keep = survivors(s, cs)
    cost = run.costs(s, sorted({c.instrument for c in keep}))
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
