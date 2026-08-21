#!/usr/bin/env python3
"""Q-TODVOL-1 D2 pre-G0 cheap falsifier.

Frozen per lab/analysis/c1/todvol_1_2026-08-20/FREEZE.md (2026-08-20). Tests
the tod-baseline-range-trigger construct's mean signed GROSS points per
triggered signal against half the standard 4x round-trip-cost hurdle, on the
IS panel only (this is the whole panel -- no CONFIRM split exists yet for
this candidate; that split is a later, separate step if D2 passes).

$0, K=0, no CONFIRM read, no core/ or lab/discovery/ touch, no simulate_path
call. Pure OHLCV walk-forward on the same cached MNQ 15m panel the ORB/cushion
work this session already used.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(r"C:/Users/joshu/multi_firm_operations/.claude/worktrees/cursor-grok-dispatch-4de91f")
ORB_LIB_DIR = REPO / "lab" / "analysis" / "orb" / "orb_universe_2026-06-22"
OUT_DIR = Path(__file__).resolve().parent

sys.path.insert(0, str(ORB_LIB_DIR))
import orb_lib as ol  # noqa: E402

_PRIMARY = Path(r"C:/Users/joshu/multi_firm_operations")
PANEL_CANDIDATES = (
    REPO / "lab/analysis/orb/orb_mnq_2026-07/_mnq_15m.pkl",
    _PRIMARY / "lab/analysis/orb/orb_mnq_2026-07/_mnq_15m.pkl",
)

# ---- frozen per FREEZE.md; not tunable after seeing a result ----
MNQ_USD_PER_PT = 2.0
SLIP_TICK_USD = 0.50
TRADEIFY_SIDE = 0.91
RT_PT_TRADEIFY = 2.0 * (TRADEIFY_SIDE + SLIP_TICK_USD) / MNQ_USD_PER_PT  # 1.41 pt

EXCLUDE_BARS = 2          # opening-range window (matches ORB-MNQ-1's or_bars=2), excluded
LOOKBACK_SESSIONS = 60    # trailing per-tod baseline window
THETA = 2.0                # trigger threshold multiple
STOP_MULT = 1.0            # x trigger bar's own range
TARGET_MULT = 2.0          # x trigger bar's own range (rr=2)


def resolve_panel() -> Path:
    for p in PANEL_CANDIDATES:
        if p.exists():
            return p
    raise FileNotFoundError("cached MNQ 15m panel not found: " + str(PANEL_CANDIDATES))


def main() -> int:
    panel_pkl = resolve_panel()
    df = pd.read_pickle(panel_pkl)
    print(f"[data] {panel_pkl}  rows={len(df):,}  span={df['et'].min()} -> {df['et'].max()}")

    inst = ol.Instrument(
        name="mnq_todvol", path=Path("(mem)"), loader="none", feed="databento",
        tick=0.25, spread_pt=0.25, rt_cost_pt=RT_PT_TRADEIFY,
        open_tod=ol.OPEN_TOD_US, close_tod=15 * 60 + 45, tz="America/New_York",
        note="Q-TODVOL-1 D2 falsifier, native MNQ 15m",
    )
    piv, meta = ol.session_panel(df, inst)
    o, h, l, c = piv["open"], piv["high"], piv["low"], piv["close"]
    tods = sorted(t for t in c.columns if inst.open_tod <= t <= inst.close_tod)
    trigger_tods = tods[EXCLUDE_BARS:]
    print(f"[grid] {len(tods)} tods/session, {len(trigger_tods)} eligible after excluding first {EXCLUDE_BARS}")

    rng = h - l

    signals = []
    days = list(c.index)
    for i, day in enumerate(days):
        if i < LOOKBACK_SESSIONS:
            continue
        trail_idx = days[i - LOOKBACK_SESSIONS: i]  # causal: strictly prior sessions only
        baseline = rng.loc[trail_idx, trigger_tods].median(axis=0)

        for t in trigger_tods:
            r = rng.loc[day, t]
            b = baseline[t]
            if not np.isfinite(r) or not np.isfinite(b) or b <= 0:
                continue
            if r < THETA * b:
                continue

            entry = float(c.loc[day, t])
            bar_range = float(r)
            direction = 1 if c.loc[day, t] >= o.loc[day, t] else -1
            stop_px = entry - direction * STOP_MULT * bar_range
            target_px = entry + direction * TARGET_MULT * bar_range

            rest_tods = [tt for tt in tods if tt > t]
            exit_px, exit_reason = None, "session_flat"
            for tt in rest_tods:
                bh, bl = h.loc[day, tt], l.loc[day, tt]
                if not np.isfinite(bh):
                    continue
                hit_target = (bh >= target_px) if direction == 1 else (bl <= target_px)
                hit_stop = (bl <= stop_px) if direction == 1 else (bh >= stop_px)
                if hit_stop and hit_target:
                    exit_px, exit_reason = stop_px, "stop_and_target_same_bar_conservative"
                    break
                if hit_stop:
                    exit_px, exit_reason = stop_px, "stop"
                    break
                if hit_target:
                    exit_px, exit_reason = target_px, "target"
                    break
            if exit_px is None:
                # session-flat: use the LAST non-NaN close this day (early-close sessions --
                # half days before Labor Day / Thanksgiving / Christmas -- have no bar at the
                # nominal last tod). A mechanical data-handling fix, not a construct parameter.
                day_closes = c.loc[day, tods].dropna()
                if day_closes.empty:
                    exit_px = entry  # degenerate: no bar after entry at all (should not occur)
                else:
                    exit_px = float(day_closes.iloc[-1])

            gross_pts = direction * (exit_px - entry)  # GROSS, cost NOT subtracted (cost-law convention)
            signals.append(dict(
                day=str(day), tod=int(t), direction=direction,
                entry=entry, exit=float(exit_px), exit_reason=exit_reason,
                bar_range=bar_range, baseline=float(b), gross_pts=float(gross_pts),
            ))
            break  # first valid signal per session only (k=1)

    n = len(signals)
    n_sessions_eligible = len(days) - LOOKBACK_SESSIONS
    coverage = n / n_sessions_eligible if n_sessions_eligible else float("nan")
    gross = np.array([s["gross_pts"] for s in signals]) if signals else np.array([])
    mean_signed_gross = float(gross.mean()) if len(gross) else float("nan")
    wr = float((gross > 0).mean()) if len(gross) else float("nan")
    hurdle_4x = 4 * RT_PT_TRADEIFY
    pass_bar = 0.5 * hurdle_4x
    passed = bool(len(gross) and mean_signed_gross >= pass_bar)

    print(f"\n[D2] n_sessions_eligible={n_sessions_eligible}  n_signals={n}  coverage={coverage:.4%}")
    print(f"[D2] mean_signed_gross={mean_signed_gross:+.4f} pt  WR={wr:.4%}")
    print(f"[D2] RT cost={RT_PT_TRADEIFY:.4f} pt | 4xRT hurdle={hurdle_4x:.4f} pt | pass bar (0.5x)={pass_bar:.4f} pt")
    print(f"[D2] VERDICT: {'PASS' if passed else 'FAIL'}")

    report = dict(
        panel=str(panel_pkl), n_sessions_total=len(days), n_sessions_eligible=n_sessions_eligible,
        n_signals=n, coverage=coverage, mean_signed_gross_pts=mean_signed_gross, wr=wr,
        rt_cost_pt=RT_PT_TRADEIFY, hurdle_4x_pt=hurdle_4x, pass_bar_pt=pass_bar, passed=passed,
        theta=THETA, lookback_sessions=LOOKBACK_SESSIONS, exclude_bars=EXCLUDE_BARS,
        stop_mult=STOP_MULT, target_mult=TARGET_MULT, signals=signals,
    )
    out = OUT_DIR / "d2_falsifier_results.json"
    out.write_text(json.dumps(report, indent=2))
    print(f"[write] {out}")
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
