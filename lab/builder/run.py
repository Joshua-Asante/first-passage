"""One builder run: ``python -m builder.run <run.yaml>`` (spec stages 0-7, locally).

run.yaml:
    run_id: mcl-orb-r1
    ledger: <path to ledger.jsonl>         # outside the repo for real runs
    firm: Tradeify_Select_100K
    data: {MCL: <path to BAR_EXPORT_v0.2 csv or bar_data panel>}
    roll: "TV 1! continuous series as exported; no roll reconstructed"
    book: <optional path to JSON {date: book P&L per session}>
    cards: [<card yaml paths>]
    out: <report directory>
    commission_per_side: {XYZ: 1.00}      # only where FIRM_RULES has no row (refused otherwise); cite it in the prereg

Every card is hashed and appended to the ledger before any bar is read. Reports land in
``out/<card id>.report.json`` with a one-line verdict each in ``out/verdict.json``.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

from builder import cards, data, gates, ledger


def _costs(firm: str, instrument: str, override) -> gates.Costs:
    """FIRM_RULES first; an override is allowed only where the firm has no row, and must be > 0."""
    try:
        firm_costs = gates.Costs.for_firm(firm, instrument)
    except ValueError:
        if override is None or isinstance(override, bool) or not isinstance(override, (int, float)) or override <= 0:
            raise SystemExit(f"{instrument}: no {firm} commission row; a positive commission_per_side is required")
        return gates.Costs(float(override))
    if override is not None:
        raise SystemExit(f"{instrument}: {firm} has a commission row; remove the commission_per_side override")
    return firm_costs


def main(argv: list[str]) -> int:
    spec = yaml.safe_load(Path(argv[0]).read_text(encoding="utf-8"))
    for key in ("run_id", "ledger", "firm", "data", "roll", "cards", "out"):
        if key not in spec:
            raise SystemExit(f"run.yaml missing {key}")
    cs = [cards.parse(Path(p).read_text(encoding="utf-8")) for p in spec["cards"]]
    ids = [c.id for c in cs]
    if len(set(ids)) != len(ids):
        raise SystemExit(f"duplicate card ids: {sorted({i for i in ids if ids.count(i) > 1})}")
    overrides = spec.get("commission_per_side") or {}
    costs = {i: _costs(spec["firm"], i, overrides.get(i)) for i in {c.instrument for c in cs}}
    missing = {c.instrument for c in cs} - set(spec["data"])
    if missing:
        raise SystemExit(f"no data for {sorted(missing)}")
    ledger.append_cards(Path(spec["ledger"]), spec["run_id"], cs)  # before any data read
    book = json.loads(Path(spec["book"]).read_text()) if spec.get("book") else None
    out = Path(spec["out"]); out.mkdir(parents=True, exist_ok=True)
    loaded, verdicts = {}, []
    for c in cs:
        if c.instrument not in loaded:
            path = Path(spec["data"][c.instrument])
            bars = data.load_bars(path, c.instrument)
            dev, _ = data.split(data.session_dates(bars, c.instrument))
            loaded[c.instrument] = (bars, dev, data.file_sha256(path))
        bars, dev, sha = loaded[c.instrument]
        rep = gates.evaluate(c, bars, dev, Path(spec["ledger"]), costs[c.instrument], sha, book)
        rep.update(run_id=spec["run_id"], roll=spec["roll"], firm=spec["firm"])
        (out / f"{c.id}.report.json").write_text(json.dumps(rep, indent=1), encoding="utf-8")
        verdicts.append({"card": c.id, "verdict": rep["verdict"], "stopped_at": rep["stopped_at"],
                         "book_s": rep["book"].get("book_s"), "book_s_with_card": rep["book"].get("book_s_with_card")})
    (out / "verdict.json").write_text(json.dumps(verdicts, indent=1), encoding="utf-8")
    for v in verdicts:
        print(v)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
