"""One builder run: ``python -m builder.run <run.yaml>`` (spec stages 0-7, locally).

run.yaml (exactly these keys; commission_per_side is the only optional one):
    run_id: mcl-orb-r1
    ledger: <path to ledger.jsonl>         # outside the repo for real runs
    firm: Tradeify_Select_100K
    data: {MCL: {path: <BAR_EXPORT_v0.2 csv>, sha256: <pinned>}}
    roll: "TV 1! continuous series as exported; no roll reconstructed"
    book: {path: <JSON {date: book P&L per session}>, sha256: <pinned>, min_overlap: 500}
                                           # or null: an empty book, declared
    cards: [<card yaml paths>]
    out: <report directory>
    commission_per_side: {XYZ: 1.00}      # only where FIRM_RULES has no row (refused otherwise); cite it in the prereg

Order: the spec, cards, costs and book are validated, then every card is appended to the ledger
before any bar is read, then the data is loaded and checked, and the book must cover
``min_overlap`` development sessions of every instrument before any card is evaluated. Reports
land in ``out/<card id>.report.json`` with a one-line verdict each in ``out/verdict.json``.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import yaml

from builder import cards, data, gates, ledger

REQUIRED = {"run_id", "ledger", "firm", "data", "roll", "cards", "out", "book"}
OPTIONAL = {"commission_per_side"}


class RunError(ValueError):
    pass


def _positive(v) -> bool:
    return not isinstance(v, bool) and isinstance(v, (int, float)) and math.isfinite(v) and v > 0


def _costs(firm: str, instrument: str, override) -> gates.Costs:
    """FIRM_RULES first; an override is allowed only where the firm has no row, and must be > 0."""
    try:
        firm_costs = gates.Costs.for_firm(firm, instrument)
    except ValueError:
        if not _positive(override):
            raise RunError(f"{instrument}: no {firm} commission row; a positive commission_per_side is required") from None
        return gates.Costs(float(override))
    if override is not None:
        raise RunError(f"{instrument}: {firm} has a commission row; remove the commission_per_side override")
    if not _positive(firm_costs.commission_per_side):
        raise RunError(f"{instrument}: {firm} commission {firm_costs.commission_per_side} is not positive")
    return firm_costs


def _spec(path: Path) -> dict:
    spec = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(spec, dict) or not REQUIRED <= set(spec) or set(spec) - REQUIRED - OPTIONAL:
        got = sorted(spec) if isinstance(spec, dict) else spec
        raise RunError(f"run.yaml needs keys {sorted(REQUIRED)} (optional {sorted(OPTIONAL)}); got {got}")
    if not isinstance(spec["run_id"], str) or not spec["run_id"]:
        raise RunError("run_id must be a non-empty string")
    if not isinstance(spec["data"], dict) or any(not isinstance(v, dict) or set(v) != {"path", "sha256"}
                                                  for v in spec["data"].values()):
        raise RunError("data must map each instrument to {path, sha256}")
    b = spec["book"]
    if b is not None and (not isinstance(b, dict) or set(b) != {"path", "sha256", "min_overlap"}
                          or isinstance(b["min_overlap"], bool) or not isinstance(b["min_overlap"], int)
                          or b["min_overlap"] < 1):
        raise RunError("book must be null or {path, sha256, min_overlap: int >= 1}")
    if not isinstance(spec["cards"], list) or not spec["cards"]:
        raise RunError("cards must be a non-empty list")
    return spec


def main(argv: list[str]) -> int:
    spec = _spec(Path(argv[0]))
    cs = [cards.parse(Path(p).read_text(encoding="utf-8")) for p in spec["cards"]]
    for what, vals in (("ids", [c.id for c in cs]), ("hashes", [c.sha256 for c in cs])):
        if len(set(vals)) != len(vals):
            raise RunError(f"duplicate card {what}: {sorted({v for v in vals if vals.count(v) > 1})}")
    instruments = sorted({c.instrument for c in cs})
    missing = set(instruments) - set(spec["data"])
    if missing:
        raise RunError(f"no data for {sorted(missing)}")
    overrides = spec.get("commission_per_side") or {}
    costs = {i: _costs(spec["firm"], i, overrides.get(i)) for i in instruments}
    book = None if spec["book"] is None else data.load_book(Path(spec["book"]["path"]), spec["book"]["sha256"])
    ledger.append_cards(Path(spec["ledger"]), spec["run_id"], cs)  # before any bar is read
    loaded = {}
    for i in instruments:
        bars, summary = data.load_bars(Path(spec["data"][i]["path"]), i, spec["data"][i]["sha256"])
        dev, _ = data.split(data.session_dates(bars, i))
        if book is not None and len(set(dev) & set(book)) < spec["book"]["min_overlap"]:
            raise data.BookError(f"book covers {len(set(dev) & set(book))} {i} development sessions; "
                                 f"min_overlap is {spec['book']['min_overlap']}")
        loaded[i] = (bars, dev, summary)
    out = Path(spec["out"]); out.mkdir(parents=True, exist_ok=True)
    verdicts = []
    for c in cs:
        bars, dev, summary = loaded[c.instrument]
        rep = gates.evaluate(c, bars, dev, Path(spec["ledger"]), costs[c.instrument], summary["sha256"], book)
        rep.update(run_id=spec["run_id"], roll=spec["roll"], firm=spec["firm"], data=summary)
        (out / f"{c.id}.report.json").write_text(json.dumps(rep, indent=1), encoding="utf-8")
        verdicts.append({"card": c.id, "card_sha256": c.sha256, "verdict": rep["verdict"],
                         "stopped_at": rep["stopped_at"], "book_s": rep["book"].get("book_s"),
                         "book_s_with_card": rep["book"].get("book_s_with_card")})
    (out / "verdict.json").write_text(json.dumps(verdicts, indent=1), encoding="utf-8")
    for v in verdicts:
        print(v)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
