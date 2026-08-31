"""Q-RANGECOND-1 Phase 1-3: build ORB-MNQ-1's own per-day trade log, join it against
Q-RANGEXFER-1's already-presence-verified overnight-range conditioner, compute
conditioned-vs-unconditioned win-rate/mean-win with the frozen block-bootstrap CI.

Rule 0: read before writing this script --
  lab/analysis/orb/orb_mnq_2026-07/run_orb_mnq_bulenox_blusky.py::make_inst
    (the exact Instrument construction ORB-MNQ-1's own payability runs use: or_bars=2,
    open_tod=09:30 ET, close_tod=15:45 ET, tick=0.25, spread_pt=0.25 -- confirmed by
    direct read, not memory, per Q-RANGECOND-1 brief's own SS5 forbidden-move)
  lab/analysis/orb/orb_universe_2026-06-22/orb_lib.py (orb_backtest, session_panel,
    _finalize -- reused verbatim, not modified; this file's own docstring bars editing
    the SIBLING us500_discovery files, not this one, but nothing here is edited either
    way -- only imported)
  lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/data_lib.py,
  candidate2_overnight_rth_transfer.py (the exact conditioner definition:
    WINDOW=60, Q_BIAS=0.80, strictly-prior; reused verbatim, not re-derived)
  docs/briefs/pre-registration/Q-RANGECOND-1-verdict-preregistration.md SSA (frozen
    n-floor=30, block-bootstrap block=20/draws=4000/seed=42)

No cached `_mnq_15m.pkl` exists in this worktree (heavy artifact absent, confirmed
2026-08-30) -- the panel is built fresh from the hash-verified core/data/bar_data/MNQ_M15.csv
via a minimal loader matching orb_lib.py's own expected schema (epoch/open/high/low/close/
volume), NOT from run_orb_mnq_bulenox_blusky.py's own _PRIMARY fallback (a different
checkout). orb_lib's own `d` column (plain ET calendar date, RTH-scoped) is equivalent to
data_lib.py's own `trading_day` (CME Globex 18:00-cutover convention) for RTH-session dates
specifically -- the cutover only affects overnight bars, which session_panel() discards
before pivoting -- so the join on trading_day/day needs no date adjustment; disclosed here,
not assumed silently.

$0. No new pull. K_intrinsic=1 per the brief's own SS8 (disclosure only).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[4]
ORB_LIB_DIR = ROOT / "lab" / "analysis" / "orb" / "orb_universe_2026-06-22"
RANGEXFER_DIR = ROOT / "lab" / "analysis" / "_inbox" / "mnq_dailygeom_notice_2026-08-29"
for _p in (ORB_LIB_DIR, RANGEXFER_DIR):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import orb_lib as ol  # noqa: E402
from candidate2_overnight_rth_transfer import (  # noqa: E402
    rolling_pct_strict_prior, WINDOW, Q_BIAS,
)
from data_lib import overnight_ohlc, range_series  # noqa: E402

CSV = ROOT / "core" / "data" / "bar_data" / "MNQ_M15.csv"
SHA256SUMS = ROOT / "core" / "data" / "bar_data" / "SHA256SUMS"
HERE = Path(__file__).resolve().parent

# Frozen (pre-registration SSA)
CI_BLOCK, CI_DRAWS, CI_SEED = 20, 4000, 42
N_FLOOR = 30
WR_FLOOR = 0.55

# Tradeify cost basis (core/firm_rules.py line 350: cost_per_side_usd=0.91, index micros)
TRADEIFY_COST_PER_SIDE_USD = 0.91
SLIP_TICK_USD = 0.50
MNQ_USD_PER_PT = 2.0
RT_COST_PT = 2.0 * (TRADEIFY_COST_PER_SIDE_USD + SLIP_TICK_USD) / MNQ_USD_PER_PT  # 1.41, matches MNQ.md's own cited figure

CLOSE_TOD_CORRECT = 15 * 60 + 45  # 15:45 ET, matching make_inst's own CLOSE_TOD_CORRECT


def hash_verify() -> None:
    h = hashlib.sha256(CSV.read_bytes()).hexdigest()
    lines = SHA256SUMS.read_text().splitlines()
    expected = next((ln.split()[0] for ln in lines if "MNQ_M15.csv" in ln), None)
    assert expected is not None, "MNQ_M15.csv not listed in SHA256SUMS"
    assert h == expected, f"MNQ_M15.csv hash mismatch: got {h}, expected {expected}"
    print(f"[hash] MNQ_M15.csv verified: {h[:16]}...")


def load_orb_lib_frame() -> pd.DataFrame:
    """Minimal loader matching orb_lib.py's own expected schema (epoch ms, o/h/l/c/v),
    built from the same CSV data_lib.py's own load_raw() reads -- NOT a reimplementation
    of orb_lib's own BAR_EXPORT/OANDA parsers (this file's own schema is neither), just a
    format bridge. _finalize() itself (time/et/d/hour/minute/tod/dow) is reused verbatim."""
    raw = pd.read_csv(CSV)
    assert list(raw.columns) == ["time", "open", "high", "low", "close", "volume"], raw.columns
    # Known pandas-2.x trap (already hit once in this repo, Q-ICTEXP-1, MNQ.md): pd.to_datetime
    # can resolve to datetime64[us] rather than [ns] depending on the source strings, silently
    # changing what .astype("int64") means. Force ns explicitly before converting to epoch-ms.
    t = pd.to_datetime(raw["time"], utc=True).astype("datetime64[ns, UTC]")
    epoch_ms = t.astype("int64") // 1_000_000
    df = pd.DataFrame({
        "epoch": epoch_ms,  # ns -> ms, unit forced above
        "open": raw["open"].astype(float), "high": raw["high"].astype(float),
        "low": raw["low"].astype(float), "close": raw["close"].astype(float),
        "volume": raw["volume"].astype("int64"),
    })
    return ol._finalize(df)


def build_conditioner(df: pd.DataFrame) -> pd.DataFrame:
    """Reuses Q-RANGEXFER-1's own frozen bias_overnight definition verbatim, computed
    from the same raw bars via data_lib.py's own overnight_ohlc/range_series (not
    orb_lib's session frame -- overnight bars are outside session_panel's own RTH-only
    scope, so this needs the raw, unfiltered frame with data_lib's own trading_day
    column, joined back onto orb_lib's own `day` afterward)."""
    import importlib
    dl = importlib.import_module("data_lib")
    raw = dl.load_raw()
    on = overnight_ohlc(raw)
    on_range = range_series(on).to_numpy()
    thresh = rolling_pct_strict_prior(on_range, WINDOW, Q_BIAS)
    bias = (on_range >= thresh).astype(float)
    bias[np.isnan(thresh)] = np.nan
    out = pd.DataFrame({"trading_day": on.index.date, "bias_overnight": bias})
    return out


def block_bootstrap_ci_diff(cond_vals: np.ndarray, uncond_vals: np.ndarray, cond_mask: np.ndarray,
                             all_vals: np.ndarray, block: int, draws: int, seed: int):
    """Circular day-block bootstrap CI on (mean(cond_vals) - mean(uncond_vals)), resampling
    the FULL trade array jointly with its own conditioner mask each draw (preserves pairing).
    Same construction as the presence-battery's own frozen L2 (rangexfer_presence_battery
    _block_bootstrap_ci_single), block/draws/seed reused verbatim."""
    rng = np.random.default_rng(seed)
    n = len(all_vals)
    nblocks = int(np.ceil(n / block))
    diffs = []
    for _ in range(draws):
        st = rng.integers(0, n, size=nblocks)
        idx = (st[:, None] + np.arange(block)[None, :]) % n
        idx = idx.ravel()[:n]
        v, m = all_vals[idx], cond_mask[idx]
        if m.any() and (~m).any():
            diffs.append(float(v[m].mean() - v[~m].mean()))
    diffs = np.asarray(diffs)
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    return float(lo), float(hi), float(diffs.mean()), int(len(diffs))


def main() -> None:
    hash_verify()

    df = load_orb_lib_frame()
    print(f"[data] rows={len(df):,} span={df['et'].min()} -> {df['et'].max()}")

    inst = ol.Instrument(
        name="mnq_tradeify_rangecond1", path=Path("(in-memory)"), loader="none",
        feed="databento", tick=0.25, spread_pt=0.25, rt_cost_pt=RT_COST_PT,
        open_tod=ol.OPEN_TOD_US, close_tod=CLOSE_TOD_CORRECT, tz="America/New_York",
        note="native MNQ.v.0 15m; close_tod=15:45; Tradeify $0.91/side + 1 tick slip",
    )
    piv, meta = ol.session_panel(df, inst)
    bt = ol.orb_backtest(piv, meta, inst, or_bars=2)

    n_trades = len(bt["R"])
    print(f"[orb ] n_trades={n_trades}")
    # Sanity check vs the already-cited headline (RESULTS.md Stage 2: 1,846/1,857, 99.4%)
    # before trusting anything downstream (brief SS7 Phase 1 requirement).
    n_session_days = piv["close"].index.nunique()
    entry_rate = n_trades / n_session_days if n_session_days else float("nan")
    print(f"[sanity] session_days={n_session_days} entry_rate={entry_rate:.4f} "
          f"(expected ~99.4%, n~1846/1857, ADMISSION.md/RESULTS.md Stage 2)")

    summ = ol.summ(bt["R"])
    print(f"[orb ] mean_R={summ['mean_R']:+.4f} t={summ['t']:.2f} wr={summ['wr']:.4f} "
          f"pf={summ['pf']:.3f}")

    cond = build_conditioner(df)
    cond_map = dict(zip(cond["trading_day"], cond["bias_overnight"]))

    trade_days = bt["day"]
    trade_R = bt["R"]
    bias_for_trade = np.array([cond_map.get(d, np.nan) for d in trade_days])

    scored = ~np.isnan(bias_for_trade)
    n_dropped = int((~scored).sum())
    print(f"[join] trades with a conditioner value: {scored.sum()}/{n_trades} "
          f"({n_dropped} dropped -- inside the conditioner's own 60-day warmup or "
          f"a day the RTH panel scores but the raw-bar overnight panel does not)")

    R = trade_R[scored]
    bias = bias_for_trade[scored].astype(bool)
    is_win = (R > 0).astype(float)

    n_cond = int(bias.sum())
    n_uncond = int((~bias).sum())
    print(f"[split] n_conditioned(bias=1)={n_cond}  n_unconditioned(bias=0)={n_uncond}")

    wr_cond = float(is_win[bias].mean()) if n_cond else float("nan")
    wr_uncond = float(is_win[~bias].mean()) if n_uncond else float("nan")
    # "mean win" = mean R among winning trades only (the payoff-shape quantity the
    # Tradeify floor is stated against), not mean R over the whole population.
    mw_cond = float(R[bias & (R > 0)].mean()) if (bias & (R > 0)).any() else float("nan")
    mw_uncond = float(R[(~bias) & (R > 0)].mean()) if ((~bias) & (R > 0)).any() else float("nan")

    print(f"[result] WR: conditioned={wr_cond:.4f} unconditioned={wr_uncond:.4f} "
          f"diff={wr_cond - wr_uncond:+.4f}")
    print(f"[result] mean-win: conditioned={mw_cond:+.4f} unconditioned={mw_uncond:+.4f} "
          f"diff={mw_cond - mw_uncond:+.4f}")

    # Frozen block-bootstrap CI (pre-registration SSA/SSB: block=20, draws=4000, seed=42)
    # on chronologically-ordered trades, resampled jointly with the bias mask.
    order = np.argsort(trade_days[scored])
    R_o, bias_o, isw_o = R[order], bias[order], is_win[order]

    wr_lo, wr_hi, wr_mean, wr_n = block_bootstrap_ci_diff(None, None, bias_o, isw_o, CI_BLOCK, CI_DRAWS, CI_SEED)
    print(f"[L2  ] WR diff CI=[{wr_lo:+.4f},{wr_hi:+.4f}] mean={wr_mean:+.4f} n_valid={wr_n}")

    win_only_mask = R_o > 0
    if win_only_mask.any():
        Rw = R_o[win_only_mask]
        biasw = bias_o[win_only_mask]
        mw_lo, mw_hi, mw_mean, mw_n = block_bootstrap_ci_diff(None, None, biasw, Rw, CI_BLOCK, CI_DRAWS, CI_SEED)
    else:
        mw_lo = mw_hi = mw_mean = float("nan"); mw_n = 0
    print(f"[L3  ] mean-win diff CI=[{mw_lo:+.4f},{mw_hi:+.4f}] mean={mw_mean:+.4f} n_valid={mw_n}")

    l1 = n_cond >= N_FLOOR
    l2 = wr_lo > 0
    l3 = mw_lo > 0
    l4 = wr_cond >= WR_FLOOR

    if not l1:
        verdict = "AMBIGUOUS-HOLD"
    elif l2 and l3 and l4:
        verdict = "RESOLVED"
    else:
        verdict = "FALSIFIED"

    print(f"\n[gate] L1(n>=30)={l1} L2(WR-CI>0)={l2} L3(MW-CI>0)={l3} L4(WR>=0.55)={l4}")
    print(f"[gate] VERDICT: {verdict}")

    out = dict(
        n_trades_total=n_trades, n_session_days=int(n_session_days), entry_rate=entry_rate,
        summ_all=summ,
        n_scored=int(scored.sum()), n_dropped=n_dropped,
        n_conditioned=n_cond, n_unconditioned=n_uncond,
        wr_conditioned=wr_cond, wr_unconditioned=wr_uncond,
        mean_win_conditioned=mw_cond, mean_win_unconditioned=mw_uncond,
        wr_diff_ci=[wr_lo, wr_hi], wr_diff_mean=wr_mean, wr_diff_n_valid=wr_n,
        mw_diff_ci=[mw_lo, mw_hi], mw_diff_mean=mw_mean, mw_diff_n_valid=mw_n,
        L1_n_floor=bool(l1), L2_wr_ci=bool(l2), L3_mw_ci=bool(l3), L4_wr_floor=bool(l4),
        verdict=verdict,
        rt_cost_pt=RT_COST_PT,
    )
    (HERE / "RESULTS.json").write_text(json.dumps(out, indent=2, default=float))
    print(f"\nWrote {HERE / 'RESULTS.json'}")


if __name__ == "__main__":
    main()
