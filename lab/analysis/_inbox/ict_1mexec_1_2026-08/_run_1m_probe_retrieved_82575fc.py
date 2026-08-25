"""Q-ICT-MNQ-1 / Layer 1M -- fill-mechanics probe (order-free).

Answers exactly ONE pre-registered question (PREREG_1H_1M.md sec 3):

    Given a displacement FVG on MNQ 1-minute bars, what fraction retrace to the
    FVG MID within 6 subsequent bars?

That is the mechanism which placed 247 limit orders and filled 0 on US500
(`limit-on-return`, `fillEdge=mid`, `retraceK=6`). The archived closure calls its
instrument-generality a "strong mechanism prior, not a measured fact." This measures it.

NOT the archived 16-cell strategy ablation (`harness_1m.py`) -- that would be K-bound
candidate generation, forbidden here (PREREG_1H_1M sec 4 item 2). No orders, no P&L,
no cost model, no strategy engine.

FROZEN thresholds (PREREG_1H_1M sec 3, set before any 1m bar was pulled):
    < 5%      -> WALL-CONFIRMED
    5% - 20%  -> WALL-CONFIRMED (marginal)
    > 20%     -> WALL-NOT-CONFIRMED (names, never opens, a follow-up)

Usage:  python lab/analysis/ict_mnq_2026-08/run_1m_probe.py <mnq_1m.parquet>
"""
from __future__ import annotations

import datetime as _dt
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_ARCHIVE = _HERE.parents[1] / "archive" / "ict_cascade_2026-06-18"
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_ARCHIVE))

import _ict_offline as M  # noqa: E402  (shared frozen detectors)
import _build_w_export_retrieved as B  # noqa: E402  (frozen roll-window helper)

# ---- FROZEN (PREREG_1H_1M sec 3) --------------------------------------------
RETRACE_K = 6          # the verdict cell -- the locked 1M retraceK
DISP_MLT = 1.5         # shared with the D layer
ATR_LEN = 14
USE_BODY = False       # wick basis
WALL_CONFIRMED_MAX = 0.05
WALL_MARGINAL_MAX = 0.20
# Disclosure-only sensitivity curve. Selecting from this is a forbidden move.
K_CURVE = (3, 6, 12, 30)


def load_parquet_bars(path: Path) -> pd.DataFrame:
    df = pd.read_parquet(path)
    df.columns = [str(c).strip().lower() for c in df.columns]
    if "ts_event" in df.columns:
        ts = pd.to_datetime(df["ts_event"], utc=True)
    elif isinstance(df.index, pd.DatetimeIndex):
        ts = pd.to_datetime(df.index, utc=True)
    else:
        raise KeyError(f"no ts_event/DatetimeIndex; columns={list(df.columns)}")
    out = pd.DataFrame(
        {
            "epoch_ms": (ts.astype("int64") // 1_000_000).to_numpy(),
            "open": df["open"].to_numpy(dtype=float),
            "high": df["high"].to_numpy(dtype=float),
            "low": df["low"].to_numpy(dtype=float),
            "close": df["close"].to_numpy(dtype=float),
        }
    )
    return out.drop_duplicates("epoch_ms").sort_values("epoch_ms").reset_index(drop=True)


def build_fvgs(o, h, l, c, atr, roll_mask):
    """Displacement-filtered FVG registry, wick basis -- identical construction to
    the D layer's `_build_fvgs` (same shared detectors, same dispMlt/atrLen), with
    roll-window origins excluded per PREREG_D_W sec 2."""
    fvgs = []
    for i in range(2, len(c)):
        if roll_mask[i]:
            continue
        if not M.displacement(o, h, l, c, i, atr[i], DISP_MLT, use_body=USE_BODY):
            continue
        if M.bull_fvg(o, h, l, c, i, use_body=USE_BODY):
            top, bot = M.bull_bounds(o, h, l, c, i, use_body=USE_BODY)
            fvgs.append({"bar": i, "top": top, "bot": bot, "bull": True})
        elif M.bear_fvg(o, h, l, c, i, use_body=USE_BODY):
            top, bot = M.bear_bounds(o, h, l, c, i, use_body=USE_BODY)
            fvgs.append({"bar": i, "top": top, "bot": bot, "bull": False})
    return fvgs


def retrace_stats(fvgs, high, low, k: int):
    """Fraction of FVGs whose MID is touched within k bars of registration.

    Mid = (top + bot) / 2. A bull FVG sits below price and is reached when a
    subsequent low <= mid; a bear FVG sits above and is reached when a high >= mid.
    Scan starts at bar+1 (the D-1 guard convention: the registration bar cannot
    count as its own touch). Look-ahead-free -- forward scan only.
    """
    n = len(high)
    hits = 0
    eligible = 0
    bars_to_hit = []
    for f in fvgs:
        t0 = f["bar"]
        if t0 + k >= n:          # incomplete window -> censored, like the D layer
            continue
        eligible += 1
        mid = (f["top"] + f["bot"]) / 2.0
        for j in range(t0 + 1, min(n, t0 + k + 1)):
            touched = (low[j] <= mid) if f["bull"] else (high[j] >= mid)
            if touched:
                hits += 1
                bars_to_hit.append(j - t0)
                break
    rate = (hits / eligible) if eligible else float("nan")
    med = float(np.median(bars_to_hit)) if bars_to_hit else float("nan")
    return {"k": k, "n": eligible, "hits": hits, "rate": rate, "median_bars": med}


def main(argv) -> int:
    if len(argv) < 2:
        print("usage: run_1m_probe.py <mnq_1m.parquet>")
        return 2
    path = Path(argv[1])
    if not path.exists():
        print(f"MISSING 1m parquet: {path}")
        return 1

    print("Q-ICT-MNQ-1 / Layer 1M -- fill-mechanics probe (order-free)")
    print("PREREG: lab/analysis/ict_mnq_2026-08/PREREG_1H_1M.md sec 3 (frozen pre-pull)")
    print(f"FROZEN: retraceK={RETRACE_K} fillEdge=mid dispMlt={DISP_MLT} "
          f"atrLen={ATR_LEN} useBody={USE_BODY}")
    print("US500 reference: 247 limit orders placed, 0 filled (0%).\n")

    bars = load_parquet_bars(path)
    o = bars["open"].to_numpy()
    h = bars["high"].to_numpy()
    l = bars["low"].to_numpy()
    c = bars["close"].to_numpy()
    print(f"  1m bars loaded : {len(c):,}")

    atr = M.wilder_atr(h, l, c, ATR_LEN)
    roll_mask = np.array(
        [
            B.in_roll_window(
                _dt.datetime.fromtimestamp(int(e) / 1000, _dt.timezone.utc).date()
            )
            for e in bars["epoch_ms"].to_numpy()
        ],
        dtype=bool,
    )
    print(f"  roll-window bars: {int(roll_mask.sum()):,} (excluded as FVG origins)")

    fvgs = build_fvgs(o, h, l, c, atr, roll_mask)
    n_bull = sum(1 for f in fvgs if f["bull"])
    print(f"  displacement FVGs detected: {len(fvgs):,}  "
          f"(bull {n_bull:,} / bear {len(fvgs) - n_bull:,})\n")

    # ---- THE VERDICT CELL ----------------------------------------------------
    v = retrace_stats(fvgs, h, l, RETRACE_K)
    print("=" * 78)
    print(f"VERDICT CELL  retraceK={RETRACE_K}")
    print("=" * 78)
    print(f"  eligible FVGs        : {v['n']:,}")
    print(f"  retraced to mid      : {v['hits']:,}")
    print(f"  RETRACE RATE         : {v['rate']:.4%}")
    print(f"  median bars to touch : {v['median_bars']}")

    if v["rate"] < WALL_CONFIRMED_MAX:
        disp = "WALL-CONFIRMED"
        note = ("the 0/247 US500 result is instrument-general, as the archived "
                "closure's mechanism prior predicted")
    elif v["rate"] <= WALL_MARGINAL_MAX:
        disp = "WALL-CONFIRMED (marginal)"
        note = ("fills exist but are too rare to reach the archived n>=100 floor "
                "at any plausible signal rate")
    else:
        disp = "WALL-NOT-CONFIRMED"
        note = ("the US500 fill wall does NOT generalize to MNQ; this NAMES a "
                "follow-up decision and does not open one (PREREG sec 3)")
    print(f"\n  DISPOSITION          : {disp}")
    print(f"  reading              : {note}")

    # ---- DISCLOSURE ONLY -- selecting from this curve is forbidden ------------
    print("\n" + "=" * 78)
    print("SENSITIVITY CURVE (disclosure only -- NOT a grid to select from;")
    print("the verdict reads retraceK=6 and only retraceK=6)")
    print("=" * 78)
    for k in K_CURVE:
        s = retrace_stats(fvgs, h, l, k)
        mark = "  <-- VERDICT CELL" if k == RETRACE_K else ""
        print(f"  retraceK={k:>3}  n={s['n']:>7,}  hits={s['hits']:>7,}  "
              f"rate={s['rate']:.4%}  median_bars={s['median_bars']}{mark}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
