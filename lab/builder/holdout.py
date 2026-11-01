"""Stage 8 holdout looks: ``python -m builder.holdout <run.yaml>`` (the same run.yaml as builder.run).

Refused, before any look, unless the current run.yaml describes exactly the finished development
attempt: ``out/verdict.json`` (deleted by builder.run before it ledgers, written last by an atomic
rename) must carry the sha256 that ``run.binding`` recomputes from run.yaml and the engine now,
list exactly run.yaml's cards with each report's sha256, and every report must match its sha256,
carry the same binding sha256, this run_id and a final verdict (survivor | killed | unresolved).
The survivors are the cards whose report verdict is ``survivor``. Looks are taken in card-id
order, each ledgered (``ledger.append_holdout_look``) before its holdout bars are simulated, and
each writes ``out/<card id>.holdout.json``.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from builder import data, gates, run

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


def survivors(s: dict, cs: list, cost: dict) -> list:
    """The cards with a survivor report, in card-id order, after checking the binding and every report."""
    out = Path(s["out"])
    _, marker = _read(out / "verdict.json")
    bind = run.binding(s, cs, cost)
    want = run.binding_sha256(bind)
    if not isinstance(marker, dict) or set(marker) != {"dev_binding_sha256", "binding", "cards"}:
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
                    data_sha256=summary["sha256"], calendar_sha256=cal.sha256,
                    dev_binding_sha256=run.binding_sha256(run.binding(s, cs, cost)))
        (out / f"{c.id}.holdout.json").write_text(json.dumps(look, indent=1), encoding="utf-8")
        print({k: look[k] for k in ("card_id", "verdict", "pass")})
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
