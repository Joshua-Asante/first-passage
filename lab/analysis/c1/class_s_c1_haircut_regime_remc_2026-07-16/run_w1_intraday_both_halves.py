"""W1 — intraday-honest both-halves re-run (frozen Phase-4 contract / Cursor packet).

Feeds ``intraday_low`` from 15m bars through the paired survivor-scoring channel.
``dd_lock_offset_usd`` stays unreachable. Thresholds frozen (3.0% / 50%).

Scope (Cursor execution packet 2026-08-09): full-panel + H1/H2 on the 0.50× arm
(admissibility question). Bootstrap long-pole is out of this packet's wall-clock.
No rung / lifecycle / allocation motion from the numbers.

Owner: docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md
Contract: docs/spec/2026-08-04-phase4-both-halves-intraday-rerun-spec.md
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[3]
_SCORING = _ROOT / "lab" / "analysis" / "c1" / "class_s_candidate1_scoring_2026-07-15"
_BAR = _ROOT / "core" / "data" / "bar_data"
for _p in (_ROOT / "core", _ROOT / "lab", str(_SCORING), str(_HERE)):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import firm_rules  # noqa: E402
from discovery.prop_survivor_scoring import (  # noqa: E402
    assert_intraday_channel_nonvacuous,
    load_scoring_thresholds,
    paired_blocks_from_daily,
    run_tier_remc,
    score_part_a,
)

sys.argv = [sys.argv[0]]
import run_class_s_c1_scoring as S  # noqa: E402
import run_class_s_c1_regime_gate as R  # noqa: E402

LOCKING_TIERS = ("Tradeify_Select_100K", "MFFU_Rapid_100K")
UNREACHABLE = 1_000_000.0
ARM_MULT = 0.50  # admissibility question first (Phase-4 P3)
POINT_VALUE = {"striker": 0.50, "striker_nas100": 2.00}  # MYM / MNQ USD per point
BAR_FILES = {"striker": "MYM_M15.csv", "striker_nas100": "MNQ_M15.csv"}
# Non-vacuity uses a short horizon so the guard finishes in seconds; production
# arms use the frozen prereg horizon.
NONVAC_HORIZON = 400
NONVAC_SIMS = 200


def _load_bars(leg: str) -> pd.DataFrame:
    path = _BAR / BAR_FILES[leg]
    if not path.is_file():
        raise FileNotFoundError(
            f"missing 15m panel {path} — restore via "
            f"scripts/parse_bar_export.py --symbol {{MYM|MNQ}}"
        )
    df = pd.read_csv(path)
    df["dt"] = pd.to_datetime(df["time"], utc=True).dt.tz_convert("America/New_York")
    return df.sort_values("dt").reset_index(drop=True)


def _paired_trades_scaled(leg: str, scale: float) -> pd.DataFrame:
    """Entry/exit rows at the same static×1R scale as ``build_scaled_panel``."""
    path = S.resolve_panel_path(leg)
    df = S.load_csv(path)
    trades = S.pair_trades(df)
    exits = df[df["Type"].astype(str).str.startswith("Exit")].sort_values("dt")
    initial = S.detect_initial(exits)
    t = S.reconstruct_static(trades, initial)
    # Side from the raw entry Type.
    entries = df[df["Type"].astype(str).str.startswith("Entry")].copy()
    side = []
    qty = []
    entry_px = []
    exit_px = []
    for _, row in t.iterrows():
        e = entries[entries["Trade #"] == row["trade_no"]]
        x = df[
            (df["Trade #"] == row["trade_no"])
            & df["Type"].astype(str).str.startswith("Exit")
        ]
        et = str(e.iloc[0]["Type"]).lower()
        side.append(+1.0 if "long" in et else -1.0)
        qty.append(float(e.iloc[0]["Size (qty)"]))
        entry_px.append(float(e.iloc[0]["Price USD"]))
        exit_px.append(float(x["Price USD"].iloc[-1]))
    t = t.copy()
    t["side"] = side
    t["qty"] = qty
    t["entry_px"] = entry_px
    t["exit_px"] = exit_px
    t["pnl_scaled"] = t["pnl_static"].astype(float) * float(scale)
    t["entry_dt"] = pd.to_datetime(t["entry_dt"])
    t["exit_dt"] = pd.to_datetime(t["exit_dt"])
    return t


def _aware_et(ts) -> pd.Timestamp:
    t = pd.Timestamp(ts)
    if t.tzinfo is None:
        return t.tz_localize("America/New_York")
    return t.tz_convert("America/New_York")


def _leg_daily_excursion(
    trades: pd.DataFrame,
    bars: pd.DataFrame,
    *,
    point_value: float,
    bdays: pd.DatetimeIndex,
) -> pd.Series:
    """Per-bday min MTM excursion (≤0) from that day's opening mark, scaled dollars.

    Days with no bar coverage fall back to ``min(0, exit-day pnl)`` on exit days
    and 0 elsewhere — residual optimistic on the pre-bar span (documented in RESULTS).
    """
    del point_value  # sizing comes from pnl_scaled / realized move (static×1R faithful)
    bars = bars.copy()
    bars["day"] = bars["dt"].dt.date
    by_day = {d: g for d, g in bars.groupby("day", sort=False)}

    exc = pd.Series(0.0, index=bdays, dtype=float)
    fallback_exit = pd.Series(0.0, index=bdays, dtype=float)
    bar_touched = pd.Series(False, index=bdays, dtype=bool)

    for _, tr in trades.iterrows():
        entry = _aware_et(tr["entry_dt"])
        exit_ = _aware_et(tr["exit_dt"])
        side = float(tr["side"])
        entry_px = float(tr["entry_px"])
        exit_px = float(tr["exit_px"])
        pnl_scaled = float(tr["pnl_scaled"])
        move_denom = (exit_px - entry_px) * side

        exit_key = pd.Timestamp(exit_.date())
        if exit_key in fallback_exit.index:
            fallback_exit.loc[exit_key] += min(0.0, pnl_scaled)

        if abs(move_denom) <= 1e-9:
            continue

        def mtm_at(px: float, _e=entry_px, _s=side, _d=move_denom, _p=pnl_scaled) -> float:
            return (px - _e) * _s / _d * _p

        day = entry.normalize()
        end_day = exit_.normalize()
        while day <= end_day:
            d = day.date()
            day_key = pd.Timestamp(d)
            seg_all = by_day.get(d)
            if seg_all is not None and day_key in exc.index:
                seg = seg_all[(seg_all["dt"] >= entry) & (seg_all["dt"] <= exit_)]
                if len(seg):
                    worst_px = (
                        float(seg["low"].min()) if side > 0 else float(seg["high"].max())
                    )
                    open_px = entry_px if d == entry.date() else float(seg.iloc[0]["open"])
                    day_exc = min(0.0, mtm_at(worst_px) - mtm_at(open_px))
                    exc.loc[day_key] += day_exc
                    bar_touched.loc[day_key] = True
            day = day + pd.Timedelta(days=1)

    # Pre-bar / missing-bar residual: exit-day close as a floor (still optimistic).
    for idx in exc.index:
        if not bool(bar_touched.loc[idx]) and fallback_exit.loc[idx] < 0.0:
            exc.loc[idx] = float(fallback_exit.loc[idx])
    return exc.clip(upper=0.0)


def build_book_intraday_low(
    panel_200k: pd.DataFrame, meta: dict
) -> tuple[np.ndarray, dict]:
    """Book-level daily ``intraday_low`` at the $100K band, paired to ``book_daily_at_100k``."""
    bdays = panel_200k.index
    book = pd.Series(0.0, index=bdays, dtype=float)
    coverage = {"legs": {}, "fallback_days": 0, "bar_days": 0}
    for leg in S.C1_STRATS:
        scale = float(meta["legs"][leg]["scale"])
        trades = _paired_trades_scaled(leg, scale)
        bars = _load_bars(leg)
        leg_exc = _leg_daily_excursion(
            trades, bars, point_value=POINT_VALUE[leg], bdays=bdays
        )
        book = book + leg_exc
        coverage["legs"][leg] = {
            "n_trades": int(len(trades)),
            "bar_file": BAR_FILES[leg],
            "bar_span": f"{bars['dt'].min().date()}->{bars['dt'].max().date()}",
            "scale": scale,
            "exc_sum": float(leg_exc.sum()),
            "exc_min": float(leg_exc.min()),
        }
    # $200K panel → $100K band (same factor as book_daily_at_100k).
    book_100k = book.to_numpy(dtype=float) * (100_000.0 / S.ACCOUNT)
    book_100k = np.minimum(0.0, book_100k)
    coverage["book_exc_min_100k"] = float(book_100k.min())
    coverage["n_negative_days"] = int(np.sum(book_100k < 0))
    return book_100k, coverage


def _run_partition(daily, intraday, firm_key, thr, *, n_sims):
    blocks_p, blocks_l = paired_blocks_from_daily(daily, intraday)
    cons = R._consistency_frac(firm_key)
    run = run_tier_remc(
        firm_key,
        blocks_p,
        thr,
        n_sims=n_sims,
        consistency=cons,
        intraday_blocks=blocks_l,
    )
    return {
        "firm_key": firm_key,
        "consistency": cons,
        "n_sims": run["n_sims"],
        "headline_bust": float(run["headline_bust"]),
        "pass_rate": float(run["pass_rate"]),
        "clears_part_a": bool(score_part_a(run, thr)),
        "floor_ok": bool(
            float(run["headline_bust"]) <= thr.eval_bust_ceiling
            and float(run["pass_rate"]) >= thr.pass_floor
        ),
        "gated_on": "run2" if cons is not None else "run1_degenerate",
        "intraday_low": True,
    }


def main() -> int:
    S.phase0_verify()
    for leg in S.C1_STRATS:
        S.resolve_panel_path(leg)
    panel, meta, _ = S.build_scaled_panel(
        S.C1_STRATS, S.C1_ALLOCS, expect_1r=dict(S.EXPECTED_1R)
    )
    daily = S.book_daily_at_100k(panel)
    thr = load_scoring_thresholds(S.GATE_PREREG)
    print(
        f"[w1] panel {meta['panel_span']} n={meta['n_bdays']} "
        f"floor bust<={thr.eval_bust_ceiling:.1%} pass>={thr.pass_floor:.0%} "
        f"arm={ARM_MULT}x",
        flush=True,
    )

    print("[w1] deriving bar-level intraday_low …", flush=True)
    t0 = time.time()
    intraday, cov = build_book_intraday_low(panel, meta)
    print(
        f"[w1] intraday_low ready in {time.time()-t0:.1f}s "
        f"min={float(intraday.min()):.2f} neg_days={int(np.sum(intraday < 0))}",
        flush=True,
    )
    assert len(intraday) == len(daily)

    # Patch lock unreachable (production default; do not restore-to-100).
    for t in LOCKING_TIERS:
        firm_rules.FIRM_RULES[t]["dd_lock_offset_usd"] = UNREACHABLE

    # Non-vacuity on the 1.00× book (short horizon). At 0.50× the deepest
    # bar-derived excursion (~$1.3k) sits inside the $3k trail, so EOD and
    # intraday rates can match for the right reason — that must not be read as
    # a dropped channel. Threading is proven where the limb can fire (1.00×).
    print("[w1] non-vacuity guard (1.00x book, short horizon) …", flush=True)
    from dataclasses import replace

    thr_nv = replace(thr, horizon=NONVAC_HORIZON)
    blocks_p, blocks_l = paired_blocks_from_daily(daily, intraday)
    nv = assert_intraday_channel_nonvacuous(
        blocks_p,
        blocks_l,
        thresholds=thr_nv,
        firm_key="Tradeify_Select_100K",
        n_sims=NONVAC_SIMS,
        horizon=NONVAC_HORIZON,
    )
    print(
        f"[w1] non-vacuity OK — eod bust={nv['eod']['headline_bust']:.4f} "
        f"real bust={nv['real']['headline_bust']:.4f}",
        flush=True,
    )

    # Lifecycle haircut co-moves both channels (book size). Not dd_scale —
    # simulate_path applies dd_scale itself (frozen Phase-4 §5).
    dh = daily * ARM_MULT
    ih = intraday * ARM_MULT

    out: dict = {
        "date": "2026-08-09",
        "packet": "docs/spec/2026-08-09-w1-intraday-rerun-execution-spec.md",
        "contract": "docs/spec/2026-08-04-phase4-both-halves-intraday-rerun-spec.md",
        "adr": "docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md",
        "geometry": "intraday_low from 15m bars; dd_lock_offset_usd unreachable",
        "arm": ARM_MULT,
        "floor": {
            "bust_ceiling": thr.eval_bust_ceiling,
            "pass_floor": thr.pass_floor,
        },
        "panel_meta": meta,
        "intraday_coverage": cov,
        "nonvacuity": {
            "eod_bust": float(nv["eod"]["headline_bust"]),
            "eod_pass": float(nv["eod"]["pass_rate"]),
            "real_bust": float(nv["real"]["headline_bust"]),
            "real_pass": float(nv["real"]["pass_rate"]),
            "ok": True,
        },
        "tiers": {},
    }

    h1, h2, mid = R.half_panel_split(dh)
    i1, i2, _ = R.half_panel_split(ih)
    assert mid == len(i1)

    for firm_key in LOCKING_TIERS:
        print(f"[w1] ===== {firm_key} =====", flush=True)
        t1 = time.time()
        full = _run_partition(dh, ih, firm_key, thr, n_sims=None)
        print(
            f"[w1]   full bust={full['headline_bust']:.2%} pass={full['pass_rate']:.2%} "
            f"{'PASS' if full['floor_ok'] else 'FAIL'} ({time.time()-t1:.0f}s)",
            flush=True,
        )
        t1 = time.time()
        r1 = _run_partition(h1, i1, firm_key, thr, n_sims=None)
        print(
            f"[w1]   H1  bust={r1['headline_bust']:.2%} pass={r1['pass_rate']:.2%} "
            f"{'PASS' if r1['floor_ok'] else 'FAIL'} ({time.time()-t1:.0f}s)",
            flush=True,
        )
        t1 = time.time()
        r2 = _run_partition(h2, i2, firm_key, thr, n_sims=None)
        print(
            f"[w1]   H2  bust={r2['headline_bust']:.2%} pass={r2['pass_rate']:.2%} "
            f"{'PASS' if r2['floor_ok'] else 'FAIL'} ({time.time()-t1:.0f}s)",
            flush=True,
        )
        out["tiers"][firm_key] = {
            "full": full,
            "H1": r1,
            "H2": r2,
            "both_halves_ok": bool(r1["floor_ok"] and r2["floor_ok"]),
            "gate_pass_full_and_halves": bool(
                full["floor_ok"] and r1["floor_ok"] and r2["floor_ok"]
            ),
        }

    dest = _HERE / "w1_intraday_both_halves_report.json"
    dest.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"[w1] written {dest}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
