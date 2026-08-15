#!/usr/bin/env python3
"""Gen-2 engine↔TV-anchor parity gate (SPEC S3 / Q-FILLTAX-1 V2).

Loads two trade series, scores Spearman ρ + net/PF relative bands against
FROZEN-PRE-RUN constants in PREREG.md, exits ADMIT (0) or FAIL (1).

$0 scaffold — no live fills, no vendor CSV required for unit tests.
Bands are independent FROZEN-PRE-RUN placeholders; not Gen-1 inheritance.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Mapping, Sequence

# ── FROZEN-PRE-RUN bands (mirror PREREG.md §1; do not tune post-hoc) ──

RANK_RHO_FLOOR: float = 0.75
NET_REL_BAND: float = 0.02
PF_REL_BAND: float = 0.02
MIN_TRADES: int = 30
EPS_DENOM: float = 1e-12

EXIT_ADMIT = 0
EXIT_FAIL = 1


@dataclass(frozen=True)
class TradeSeries:
    pnl: tuple[float, ...]
    trade_ids: tuple[str, ...] | None = None
    entry_times: tuple[str, ...] | None = None


@dataclass(frozen=True)
class GateResult:
    verdict: str  # "ADMIT" | "FAIL"
    n_trades: int
    spearman_rho: float
    net_engine: float
    net_tv: float
    net_rel: float
    pf_engine: float
    pf_tv: float
    pf_rel: float
    reasons: tuple[str, ...]


def load_trade_series(path: Path) -> TradeSeries:
    """Load a minimal trade CSV with a required ``pnl`` column."""
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise ValueError(f"{path}: empty or missing header")
        fields = {f.strip() for f in reader.fieldnames}
        if "pnl" not in fields:
            raise ValueError(f"{path}: required column 'pnl' missing; got {sorted(fields)}")

        pnls: list[float] = []
        ids: list[str] = []
        times: list[str] = []
        has_id = "trade_id" in fields
        has_time = "entry_time" in fields

        for row in reader:
            raw = (row.get("pnl") or "").strip()
            if raw == "":
                continue
            pnls.append(float(raw))
            if has_id:
                ids.append((row.get("trade_id") or "").strip())
            if has_time:
                times.append((row.get("entry_time") or "").strip())

    if not pnls:
        raise ValueError(f"{path}: no pnl rows")

    return TradeSeries(
        pnl=tuple(pnls),
        trade_ids=tuple(ids) if has_id else None,
        entry_times=tuple(times) if has_time else None,
    )


def align_series(engine: TradeSeries, tv: TradeSeries) -> tuple[tuple[float, ...], tuple[float, ...]]:
    """Align engine and TV PnL vectors.

    Prefer ``trade_id`` join; else sort by ``entry_time`` and align positionally;
    else positional as loaded. Length mismatch → ValueError (caller → FAIL).
    """
    if engine.trade_ids is not None and tv.trade_ids is not None:
        tv_map: dict[str, float] = {}
        for tid, pnl in zip(tv.trade_ids, tv.pnl, strict=True):
            if tid == "":
                raise ValueError("tv_anchor: empty trade_id")
            if tid in tv_map:
                raise ValueError(f"tv_anchor: duplicate trade_id {tid!r}")
            tv_map[tid] = pnl
        eng_pnl: list[float] = []
        tv_pnl: list[float] = []
        for tid, pnl in zip(engine.trade_ids, engine.pnl, strict=True):
            if tid == "":
                raise ValueError("engine: empty trade_id")
            if tid not in tv_map:
                raise ValueError(f"trade_id {tid!r} present in engine but not tv_anchor")
            eng_pnl.append(pnl)
            tv_pnl.append(tv_map.pop(tid))
        if tv_map:
            leftover = sorted(tv_map)[:5]
            raise ValueError(
                f"tv_anchor has {len(tv_map)} trade_id(s) absent from engine; e.g. {leftover}"
            )
        return tuple(eng_pnl), tuple(tv_pnl)

    if engine.entry_times is not None and tv.entry_times is not None:
        eng_order = sorted(range(len(engine.pnl)), key=lambda i: engine.entry_times[i])  # type: ignore[index]
        tv_order = sorted(range(len(tv.pnl)), key=lambda i: tv.entry_times[i])  # type: ignore[index]
        eng_pnl = tuple(engine.pnl[i] for i in eng_order)
        tv_pnl = tuple(tv.pnl[i] for i in tv_order)
    else:
        eng_pnl = engine.pnl
        tv_pnl = tv.pnl

    if len(eng_pnl) != len(tv_pnl):
        raise ValueError(
            f"length mismatch: engine={len(eng_pnl)} tv_anchor={len(tv_pnl)}"
        )
    return eng_pnl, tv_pnl


def _rankdata(values: Sequence[float]) -> list[float]:
    """Average ranks for ties (1-based), matching common Spearman practice."""
    n = len(values)
    order = sorted(range(n), key=lambda i: values[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and values[order[j + 1]] == values[order[i]]:
            j += 1
        # average of 1-based ranks (i+1) .. (j+1)
        avg = (i + 1 + j + 1) / 2.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def spearman_rho(x: Sequence[float], y: Sequence[float]) -> float:
    if len(x) != len(y):
        raise ValueError("spearman_rho: length mismatch")
    n = len(x)
    if n < 2:
        return float("nan")
    rx = _rankdata(x)
    ry = _rankdata(y)
    mean_x = sum(rx) / n
    mean_y = sum(ry) / n
    num = 0.0
    dx2 = 0.0
    dy2 = 0.0
    for a, b in zip(rx, ry, strict=True):
        da = a - mean_x
        db = b - mean_y
        num += da * db
        dx2 += da * da
        dy2 += db * db
    denom = math.sqrt(dx2 * dy2)
    if denom == 0.0:
        return 0.0
    return num / denom


def net_pnl(pnls: Sequence[float]) -> float:
    return float(sum(pnls))


def profit_factor(pnls: Sequence[float], eps: float = EPS_DENOM) -> float:
    wins = sum(p for p in pnls if p > 0.0)
    losses = sum(-p for p in pnls if p < 0.0)
    return wins / max(losses, eps)


def relative_error(a: float, b: float, eps: float = EPS_DENOM) -> float:
    return abs(a - b) / max(abs(b), eps)


def evaluate(engine_pnl: Sequence[float], tv_pnl: Sequence[float]) -> GateResult:
    """Compare aligned PnL vectors to FROZEN-PRE-RUN bands."""
    n = len(engine_pnl)
    reasons: list[str] = []

    if n < MIN_TRADES:
        reasons.append(f"n_trades={n} < MIN_TRADES={MIN_TRADES}")

    rho = spearman_rho(engine_pnl, tv_pnl) if n >= 2 else float("nan")
    if math.isnan(rho) or rho < RANK_RHO_FLOOR:
        reasons.append(f"spearman_rho={rho!r} < RANK_RHO_FLOOR={RANK_RHO_FLOOR}")

    net_e = net_pnl(engine_pnl)
    net_t = net_pnl(tv_pnl)
    net_rel = relative_error(net_e, net_t)
    if net_rel > NET_REL_BAND:
        reasons.append(f"net_rel={net_rel:.6g} > NET_REL_BAND={NET_REL_BAND}")

    pf_e = profit_factor(engine_pnl)
    pf_t = profit_factor(tv_pnl)
    pf_rel = relative_error(pf_e, pf_t)
    if pf_rel > PF_REL_BAND:
        reasons.append(f"pf_rel={pf_rel:.6g} > PF_REL_BAND={PF_REL_BAND}")

    verdict = "ADMIT" if not reasons else "FAIL"
    return GateResult(
        verdict=verdict,
        n_trades=n,
        spearman_rho=rho,
        net_engine=net_e,
        net_tv=net_t,
        net_rel=net_rel,
        pf_engine=pf_e,
        pf_tv=pf_t,
        pf_rel=pf_rel,
        reasons=tuple(reasons),
    )


def run_gate(engine_path: Path, tv_path: Path) -> GateResult:
    engine = load_trade_series(engine_path)
    tv = load_trade_series(tv_path)
    try:
        eng_pnl, tv_pnl = align_series(engine, tv)
    except ValueError as exc:
        return GateResult(
            verdict="FAIL",
            n_trades=0,
            spearman_rho=float("nan"),
            net_engine=0.0,
            net_tv=0.0,
            net_rel=float("nan"),
            pf_engine=float("nan"),
            pf_tv=float("nan"),
            pf_rel=float("nan"),
            reasons=(f"align: {exc}",),
        )
    return evaluate(eng_pnl, tv_pnl)


def _result_json(result: GateResult) -> Mapping[str, object]:
    payload = asdict(result)
    # JSON-friendly NaNs
    for key, val in list(payload.items()):
        if isinstance(val, float) and math.isnan(val):
            payload[key] = None
    payload["bands"] = {
        "RANK_RHO_FLOOR": RANK_RHO_FLOOR,
        "NET_REL_BAND": NET_REL_BAND,
        "PF_REL_BAND": PF_REL_BAND,
        "MIN_TRADES": MIN_TRADES,
        "label": "FROZEN-PRE-RUN",
    }
    return payload


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Gen-2 engine↔TV-anchor parity gate (FROZEN-PRE-RUN bands)."
    )
    parser.add_argument("--engine", type=Path, required=True, help="Engine trade CSV")
    parser.add_argument("--tv-anchor", type=Path, required=True, help="TV anchor trade CSV")
    args = parser.parse_args(list(argv) if argv is not None else None)

    result = run_gate(args.engine, args.tv_anchor)
    print(json.dumps(_result_json(result), indent=2, sort_keys=True))
    return EXIT_ADMIT if result.verdict == "ADMIT" else EXIT_FAIL


if __name__ == "__main__":
    sys.exit(main())
