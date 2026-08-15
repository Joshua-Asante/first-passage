"""Q-MNQSEL-2 Phase 0 -- selection ceiling on dense RTH 1m bar opens (K=0, $0).

Frozen by PREREG.md. Gate cell G=10 (1R target); diagnostics G=5 and G=20.

Usage:  python lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/run_selection_allbars.py <mnq_1m.parquet>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_SEL1 = _HERE.parent / "mnq_selection_ceiling_2026-08"
_ICT = _HERE.parents[1] / "ict_mnq_2026-08"
sys.path.insert(0, str(_SEL1))
sys.path.insert(0, str(_ICT))

import build_w_export as B  # noqa: E402
import run_1m_probe as P  # noqa: E402
import run_selection as S1  # noqa: E402

# ---- FROZEN (PREREG) ---------------------------------------------------------
GATE_G = 10.0
DIAG_GS = (5.0, 20.0)
RT_PT = 1.41
EDGE_R = 0.40
N_FLOOR_SESSIONS = 250
RANDOM_SEED = 20260808
RTH_OPEN_MIN = 9 * 60 + 30   # 09:30
RTH_CLOSE_MIN = 16 * 60      # exclusive end → last start 15:59


def sessionize_rth(epoch_ms, open_, high, low, close) -> pd.DataFrame:
    """Keep RTH 09:30–15:59 ET bars; session = ET calendar date of the block."""
    ts = pd.to_datetime(np.asarray(epoch_ms, dtype=np.int64), unit="ms", utc=True)
    et = ts.tz_convert("America/New_York")
    minute = et.hour * 60 + et.minute
    keep = (minute >= RTH_OPEN_MIN) & (minute < RTH_CLOSE_MIN)
    et_k = et[keep]
    return pd.DataFrame(
        {
            "session": pd.DatetimeIndex(et_k).normalize().date,
            "open": np.asarray(open_, dtype=float)[keep],
            "high": np.asarray(high, dtype=float)[keep],
            "low": np.asarray(low, dtype=float)[keep],
            "close": np.asarray(close, dtype=float)[keep],
        }
    )


def dense_clock_indices(n: int) -> np.ndarray:
    """Every bar open in the RTH session is a causal clock."""
    if n <= 0:
        return np.array([], dtype=np.int64)
    return np.arange(n, dtype=np.int64)


def candidate_rs_for_session(grp: pd.DataFrame, stop_pt: float, g_pt: float) -> dict:
    o = grp["open"].to_numpy()
    h = grp["high"].to_numpy()
    l = grp["low"].to_numpy()
    c = grp["close"].to_numpy()
    clocks = dense_clock_indices(len(grp))
    long_r = np.empty(len(clocks), dtype=float)
    short_r = np.empty(len(clocks), dtype=float)
    long_hit = np.empty(len(clocks), dtype=bool)
    short_hit = np.empty(len(clocks), dtype=bool)
    for k, idx in enumerate(clocks):
        pts_l, kind_l = S1.path_pts(o[idx], +1, h, l, c, int(idx), stop_pt, g_pt)
        pts_s, kind_s = S1.path_pts(o[idx], -1, h, l, c, int(idx), stop_pt, g_pt)
        long_r[k] = S1.r_from_pts(pts_l, stop_pt, RT_PT)
        short_r[k] = S1.r_from_pts(pts_s, stop_pt, RT_PT)
        long_hit[k] = kind_l == "target"
        short_hit[k] = kind_s == "target"
    return {
        "long_r": long_r,
        "short_r": short_r,
        "long_hit": long_hit,
        "short_hit": short_hit,
        "n_clocks": len(clocks),
    }


def evaluate_at_g(df: pd.DataFrame, g: float) -> dict:
    long_rs, short_rs, long_hits, short_hits = [], [], [], []
    n_clocks = []
    for sess, grp in df.groupby("session", sort=True):
        if len(grp) < 60:
            continue
        if B.in_roll_window(sess):
            continue
        pack = candidate_rs_for_session(grp, stop_pt=g, g_pt=g)
        long_rs.append(pack["long_r"])
        short_rs.append(pack["short_r"])
        long_hits.append(pack["long_hit"])
        short_hits.append(pack["short_hit"])
        n_clocks.append(pack["n_clocks"])

    rng_l = np.random.default_rng(RANDOM_SEED)
    rng_s = np.random.default_rng(RANDOM_SEED + 1)
    long_stats = S1.arm_stats(long_rs, long_hits, rng_l)
    short_stats = S1.arm_stats(short_rs, short_hits, rng_s)
    verdict, detail = S1.verdict_for(long_stats, short_stats)
    return {
        "g_pt": g,
        "stop_pt": g,
        "rt_pt": RT_PT,
        "edge_r": EDGE_R,
        "random_seed": RANDOM_SEED,
        "median_clocks_per_session": float(np.median(n_clocks)) if n_clocks else float("nan"),
        "long": long_stats,
        "short": short_stats,
        "verdict": verdict,
        "verdict_detail": detail,
    }


def evaluate(df: pd.DataFrame) -> dict:
    gate = evaluate_at_g(df, GATE_G)
    diagnostics = {f"g_{int(g)}": evaluate_at_g(df, g) for g in DIAG_GS}
    return {
        "gate_g": GATE_G,
        "gate": gate,
        "diagnostics": diagnostics,
        "verdict": gate["verdict"],
        "verdict_detail": gate["verdict_detail"],
    }


def _print_arm(label: str, result: dict) -> None:
    for arm in ("long", "short"):
        s = result[arm]
        print("=" * 72)
        print(f" {label} ARM={arm}  n_sessions={s['n_sessions']:,}  "
              f"n_candidates={s['n_candidates']:,}")
        print(f"  S1 all-take mean R          {s['S1_all_take_mean_R']:+.4f}")
        print(f"  S2 random-1/day mean R      {s['S2_random_1day_mean_R']:+.4f}")
        print(f"  S3 oracle top-1/day mean R  {s['S3_oracle_top1_mean_R']:+.4f}")
        print(f"  S4 oracle top-2/day mean R  {s['S4_oracle_top2_mean_R']:+.4f}")
        print(f"  S4 oracle top-3/day mean R  {s['S4_oracle_top3_mean_R']:+.4f}")
        print(f"  S5 median target-hits/day   {s['S5_median_target_hits']:.1f}")
        print(f"  S6 frac sessions >=1 hit    {s['S6_frac_sessions_ge1_hit']:.1%}")


def main(argv) -> int:
    if len(argv) < 2:
        print("usage: run_selection_allbars.py <mnq_1m.parquet>")
        return 2
    path = Path(argv[1])
    if not path.exists():
        print(f"MISSING 1m parquet: {path}")
        return 1

    print("Q-MNQSEL-2 Phase 0 -- dense RTH 1m selection ceiling")
    print("PREREG: lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/PREREG.md")
    print(f"FROZEN gate G={GATE_G} (1R); diagnostics {DIAG_GS}; RT={RT_PT}; "
          f"seed={RANDOM_SEED}\n")

    bars = P.load_parquet_bars(path)
    df = sessionize_rth(
        bars["epoch_ms"].to_numpy(),
        bars["open"].to_numpy(),
        bars["high"].to_numpy(),
        bars["low"].to_numpy(),
        bars["close"].to_numpy(),
    )
    print(f"  1m bars {len(bars):,}  ->  RTH {len(df):,}  "
          f"sessions {df['session'].nunique():,}\n")

    result = evaluate(df)
    _print_arm(f"GATE G={GATE_G}", result["gate"])
    for key, diag in result["diagnostics"].items():
        print("\n" + "-" * 72)
        print(f"DIAGNOSTIC (not a gate limb): {key}")
        _print_arm(key, diag)
        print(f"  diagnostic verdict (informational): {diag['verdict']} "
              f"({diag['verdict_detail']})")

    print("\n" + "=" * 72)
    print(f"GATE VERDICT: {result['verdict']}  ({result['verdict_detail']})")
    print(f"  median clocks/session = {result['gate']['median_clocks_per_session']:.1f}")
    print("  UPPER BOUND on selection value -- licenses no candidate alone.")
    print("=" * 72)

    out_json = _HERE / "RESULTS.json"
    out_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"\nwrote {out_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
