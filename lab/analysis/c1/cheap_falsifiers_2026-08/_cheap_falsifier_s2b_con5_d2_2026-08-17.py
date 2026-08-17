"""D2 cheap falsifier for MSL-S2B successor -- CON-5 pause route-reliance gate.

Spec frozen in docs/adr/2026-08-16-con5-timeframe-scope-cheap-falsifier-gate.md SS2
(D2). Tests whether "sweep-failure-filtered-continuation" x MYM 15m clears a
generous half-of-CON-5's-own-bar on the IS panel only (CONFIRM never touched).

Entry signal (operator-elected 2026-08-17, since S2B never coded one beyond a
qualitative story -- see the falsifier's own LOG for the gap this closes):
reuse MSL-C1's own PDH/PDL sweep + failed-extension-reclaim signal
(lab/archive/msl_c1_mym_2026-08/construct_lib.py), taken on the "flip" (join
the original sweep direction) side -- the only already-coded candidate matching
"sweep-failure gates a continuation entry." Imported verbatim, not re-derived.

Stop/target box: S2B's OWN frozen placeholder geometry from
lab/analysis/c1/msl_s2b_mym_2026-08/card.yaml (stop 40 pts, rr=3 -> target
120 pts) -- NOT C1's dynamic sweep-extreme-based stop. Per the ADR: "using the
construct's own already-frozen stop/target box -- not re-tuned for this test."
This is the one piece of numeric geometry S2B's own record actually carries,
even though STAGE1/card.yaml flag it "not adjudicated" (route died before
Step 3) -- reused as-is, not invented here.

Kill: PASS if mean signed gross points/signal >= 0.5 x (4 x RT_pts); else FAIL.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_REPO = _HERE.parents[3]
_C1_DIR = _REPO / "lab" / "archive" / "msl_c1_mym_2026-08"
sys.path.insert(0, str(_C1_DIR))

import construct_lib as C1  # noqa: E402

PANEL = _REPO / "core" / "data" / "bar_data" / "MYM_M15.csv"
SHA256SUMS = _REPO / "core" / "data" / "bar_data" / "SHA256SUMS"
EXPECTED_SHA = "24e169528f7ea6693b75c71c3195edf6a04f3a26c6b6dff0f2e9c623fd597a58"

# S2B's own frozen (placeholder) box -- lab/analysis/c1/msl_s2b_mym_2026-08/card.yaml
STOP_PTS = 40.0
TARGET_PTS = 120.0  # rr = 3, upper end of the elected [2,3] slate-2 box
RT_USD = 2.82  # STAGE1.md Cost basis -- Tradeify Select 100K index-micro RT
POINT_VALUE_USD = 0.5
RT_PTS = RT_USD / POINT_VALUE_USD  # 5.64
FOUR_X_RT_PTS = 4.0 * RT_PTS  # 22.56
PASS_BAR_PTS = 0.5 * FOUR_X_RT_PTS  # 11.28, half of CON-5's own clearance bar

IS_END = pd.Timestamp("2025-08-31").date()  # IS < 2025-09-01, matches S2B/C1 split


def _file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def assert_panel_ok(panel: Path) -> None:
    if not panel.is_file():
        raise SystemExit(f"REFUSE: panel missing {panel}")
    got = _file_sha256(panel)
    if got != EXPECTED_SHA:
        raise SystemExit(f"REFUSE: MYM_M15 sha mismatch\n  got  {got}\n  want {EXPECTED_SHA}")


def load_is_bars(panel: Path) -> pd.DataFrame:
    df = pd.read_csv(panel)
    ts = pd.to_datetime(df["time"], utc=True)
    et = ts.dt.tz_convert("America/New_York")
    out = pd.DataFrame(
        {
            "session": pd.DatetimeIndex(et).normalize().date,
            "minute": et.dt.hour * 60 + et.dt.minute,
            "open": df["open"].to_numpy(dtype=float),
            "high": df["high"].to_numpy(dtype=float),
            "low": df["low"].to_numpy(dtype=float),
            "close": df["close"].to_numpy(dtype=float),
        }
    )
    return out[out["session"] <= IS_END].copy()  # CONFIRM never touched


def _path_pts_asymmetric_box(
    entry: float,
    side: int,
    stop_level: float,
    target_level: float,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    start: int,
) -> tuple[float, str]:
    """Stop-first same-bar; then target; else flat at last bar (session end).

    NOTE: C1's own construct_lib.path_pts_stop_target_flat hardcodes the
    target-hit payout as +stop_dist, which is only correct for C1's own
    symmetric 1R:1R box. S2B's box is asymmetric (40 stop / 120 target,
    rr=3), so this local variant pays out the actual signed distance to
    whichever level was hit -- same stop-first-same-bar / target / flat
    priority order as the original, corrected for asymmetry only.
    """
    n = len(high)
    for j in range(start, n):
        if side > 0:
            hit_stop = float(low[j]) <= stop_level
            hit_tgt = float(high[j]) >= target_level
        else:
            hit_stop = float(high[j]) >= stop_level
            hit_tgt = float(low[j]) <= target_level
        if hit_stop:
            return side * (stop_level - entry), "stop"
        if hit_tgt:
            return side * (target_level - entry), "target"
    pts = side * (float(close[n - 1]) - entry)
    return pts, "flat"


def flip_trade_with_s2b_box(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    signal: dict,
) -> dict | None:
    """C1's sweep/failed-reclaim signal, flip (continuation) side, S2B's own 40/120 box."""
    entry_i = int(signal["entry_i"])
    entry = float(open_[entry_i])
    side = -int(signal["fade_side"])  # flip = join the original sweep direction
    if side > 0:
        stop_level = entry - STOP_PTS
        target_level = entry + TARGET_PTS
    else:
        stop_level = entry + STOP_PTS
        target_level = entry - TARGET_PTS
    pts, kind = _path_pts_asymmetric_box(
        entry, side, stop_level, target_level, high, low, close, entry_i
    )
    if not np.isfinite(pts):
        return None
    return {"side": side, "pts": pts, "kind": kind, "stop_dist": STOP_PTS}


def main() -> int:
    t0 = time.perf_counter()
    assert_panel_ok(PANEL)
    df = load_is_bars(PANEL)
    sessions = sorted(df["session"].unique())
    by_sess = {s: g for s, g in df.groupby("session", sort=False)}

    prior_hl: dict = {}
    prev_hi, prev_lo = float("nan"), float("nan")
    for s in sessions:
        prior_hl[s] = (prev_hi, prev_lo)
        grp = by_sess[s]
        hi, lo = C1.rth_hl(
            grp["high"].to_numpy(dtype=float),
            grp["low"].to_numpy(dtype=float),
            grp["minute"].to_numpy(dtype=int),
        )
        if np.isfinite(hi) and np.isfinite(lo):
            prev_hi, prev_lo = hi, lo

    n_eligible = 0
    trades: list[dict] = []
    for s in sessions:
        phi, plo = prior_hl[s]
        if not (np.isfinite(phi) and np.isfinite(plo)):
            continue
        n_eligible += 1
        grp = by_sess[s]
        o = grp["open"].to_numpy(dtype=float)
        h = grp["high"].to_numpy(dtype=float)
        lo_ = grp["low"].to_numpy(dtype=float)
        c = grp["close"].to_numpy(dtype=float)
        m = grp["minute"].to_numpy(dtype=int)
        sig = C1.find_failed_extension_signal(o, h, lo_, c, m, phi, plo)
        if sig is None:
            continue
        tr = flip_trade_with_s2b_box(o, h, lo_, c, sig)
        if tr is not None:
            trades.append(tr)

    gross = np.asarray([t["pts"] for t in trades], dtype=float)
    n = len(gross)
    mean_signed_pts = float(gross.mean()) if n else float("nan")
    wr = float((gross > 0).mean()) if n else float("nan")
    coverage = (n / n_eligible) if n_eligible else 0.0
    ratio = (mean_signed_pts / FOUR_X_RT_PTS) if np.isfinite(mean_signed_pts) else None
    kind_counts: dict[str, int] = {}
    for t in trades:
        kind_counts[t["kind"]] = kind_counts.get(t["kind"], 0) + 1

    passed = np.isfinite(mean_signed_pts) and mean_signed_pts >= PASS_BAR_PTS
    verdict = "D2_PASS" if passed else "D2_FAIL"
    elapsed = time.perf_counter() - t0

    out = {
        "verdict": verdict,
        "adr": "docs/adr/2026-08-16-con5-timeframe-scope-cheap-falsifier-gate.md",
        "card": "sweep-failure-filtered-continuation x MYM 15m (S2B successor)",
        "entry_signal": "MSL-C1 flip_join (sweep+failed-reclaim, continuation side) -- operator-elected 2026-08-17",
        "stop_target_box": {"stop_pts": STOP_PTS, "target_pts": TARGET_PTS, "rr": TARGET_PTS / STOP_PTS,
                             "source": "lab/analysis/c1/msl_s2b_mym_2026-08/card.yaml (placeholder, not adjudicated -- reused as-is)"},
        "cost_basis": {"rt_usd": RT_USD, "point_value_usd": POINT_VALUE_USD, "rt_pts": RT_PTS,
                       "four_x_rt_pts": FOUR_X_RT_PTS, "pass_bar_pts": PASS_BAR_PTS},
        "n_eligible_sessions": n_eligible,
        "n_trades": n,
        "coverage_pct": coverage * 100.0,
        "mean_signed_gross_pts": mean_signed_pts,
        "wr": wr,
        "kind_counts": kind_counts,
        "gross_vs_4x_rt": ratio,
        "is_window": f"panel start .. {IS_END.isoformat()}",
        "confirm_touched": False,
        "cost_usd": 0.0,
        "k_spent": 0,
        "panel": str(PANEL),
        "panel_sha256": EXPECTED_SHA,
        "elapsed_s": elapsed,
    }
    stamp = "2026-08-17"
    results_path = _HERE / f"_cheap_falsifier_s2b_con5_d2_{stamp}_RESULTS.json"
    results_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    print(f"WROTE {results_path}")
    print(f"VERDICT {verdict}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
