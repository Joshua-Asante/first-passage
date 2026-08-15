#!/usr/bin/env python3
"""CONCEPT-USDCAD-RDM-001 ("Sovereign") — F1 channel-isolating mechanism falsifier.

Brief: docs/briefs/rnd-pipeline/CC-HANDOFF-USDCAD-RDM-001-stage1-f1.md (§2.3, §3).
Concept: rate-differential momentum — widening US–CA 2yr rate-expectation spread
loads long-USDCAD returns positively, beyond plain price trend and the
petro-currency (WTI) confound, and anti-correlates with the Constellation book
on spread-widening days.

Three tests, thresholds pre-registered in §3 BEFORE running (trap #12 — no
mid-run amendment). Primary horizon 5d; 1d and 10d reported as secondary, NOT
gating. FAIL = any of:

  1. F1(b) spread beta perm p >= 0.05 on the primary horizon, or sign negative;
  2. F1(a) conditional correlation >= 0 (no diversification in the target regime);
  3. F1(c) incremental loading insignificant after trend + oil controls
     (perm p >= 0.05 on the spread coefficient, or sign negative — reduction
     to disguised trend / petro channel).

PASS requires all three to clear. A criterion that cannot be evaluated (n below
the pre-registered floor) is UNEVALUABLE -> overall AMBIGUOUS, reported verbatim.

Pre-registered conventions (set before any result was seen):

* Leak-free as-of join (§2.2): rate/WTI state for USDCAD day t is the latest
  observation dated <= t-1 calendar day ("state[t-1]"); staleness > 5 calendar
  days drops the row WITH a count (the NOCT Monday-drop bug class — weekend
  rows must not silently shift the join). US 2yr prints ~20:30 UTC on its own
  date, strictly before the next UTC bar day opens, so date <= t-1 is leak-free.
* Windows: consecutive NON-overlapping h-trading-day windows (overlapping
  windows inflate n and break iid permutation). y_w = USDCAD close-to-close
  return over the window; x_w = change in the as-of spread state across the
  window (both endpoints read with the same t-1 lag, so no x information
  postdates the window's last bar); wti_w = WTI as-of return over the matched
  window (contemporaneous confound channel); trend_w = USDCAD return over the
  20 trading days strictly BEFORE the window (lagged price trend).
* Permutation: house convention from lab/research_utils/permutation.py
  (n_perm=2000, seeded default_rng, two-sided). Group-mean tests REUSE
  label_permutation_test; regression betas use beta_permutation_test below —
  the same convention applied to OLS (permute the spread column only, refit,
  null = |beta| distribution).
* F1(a) composite: the book's true daily P&L — static-$200K allocation-weighted
  P&L summed by exit date, 0.0 on days with no closing trade (zero-fill is the
  honest series; active-days-only Pearson reported as robustness, not gating).
  Widening day t: 5-trading-day as-of spread change ending at t is > 0.
* Evaluability floors (pre-registered): >= 100 5d windows for F1(b)/(c);
  >= 100 widening days AND >= 100 composite-window days for F1(a).
* Episodes (descriptive only, never gating): 2018 cycle 2018-01-01..2019-01-31;
  2022 cycle 2021-10-01..2023-07-31; 2026 episode 2026-01-01..2026-06-10.

Counts reported, never silent.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parents[2]
sys.path.insert(0, str(_REPO_ROOT / "lab"))

from research_utils.permutation import label_permutation_test  # noqa: E402

INPUTS = _HERE / "inputs"

P_THRESH = 0.05          # §3 verbatim — do not drift
N_PERM = 2000            # oil_carry F1 convention
PRIMARY_H = 5
SECONDARY_H = (1, 10)
MAX_STALE_DAYS = 5
MIN_WINDOWS = 100
MIN_COND_DAYS = 100
TREND_LOOKBACK = 20

EPISODES = {
    "2018_cycle": ("2018-01-01", "2019-01-31"),
    "2022_cycle": ("2021-10-01", "2023-07-31"),
    "2026_episode": ("2026-01-01", "2026-06-10"),
}


# ── loading ─────────────────────────────────────────────────────────────────

def _load_bars(path: Path, label: str) -> pd.Series:
    """Daily closes from a TradingView chart export (schema-tolerant: time
    column may be epoch seconds or ISO; column names may be capitalized)."""
    df = pd.read_csv(path)
    cols = {c.strip().lower(): c for c in df.columns}
    tcol = next(cols[k] for k in ("time", "date", "datetime") if k in cols)
    ccol = cols["close"]
    raw = df[tcol]
    if pd.api.types.is_numeric_dtype(raw):
        dt = pd.to_datetime(raw, unit="s", utc=True)
    else:
        dt = pd.to_datetime(raw, utc=True)
    dt = dt.dt.tz_localize(None).dt.normalize()
    s = pd.Series(pd.to_numeric(df[ccol], errors="coerce").to_numpy(float),
                  index=dt, name=label).dropna()
    s = s[~s.index.duplicated(keep="last")].sort_index()
    print(f"  {label}: {len(s)} daily bars {s.index.min():%Y-%m-%d} -> {s.index.max():%Y-%m-%d}")
    return s


def _load_rate(path: Path, col: str) -> pd.Series:
    df = pd.read_csv(path)
    s = pd.Series(df[col].to_numpy(float),
                  index=pd.to_datetime(df["date"]), name=col).sort_index()
    print(f"  {col}: {len(s)} rows {s.index.min():%Y-%m-%d} -> {s.index.max():%Y-%m-%d}")
    return s


def _asof_state(series: pd.Series, days: pd.DatetimeIndex, label: str
                ) -> tuple[pd.Series, int]:
    """state[t-1]: latest observation dated <= t-1 calendar day; staleness
    > MAX_STALE_DAYS drops the day (counted)."""
    obs_dates = series.index.to_numpy()
    idx = np.searchsorted(obs_dates, (days - pd.Timedelta(days=1)).to_numpy(),
                          side="right") - 1
    ok = idx >= 0
    stale = np.zeros(len(days), dtype=bool)
    lag_days = np.full(len(days), np.nan)
    vals = np.full(len(days), np.nan)
    vals[ok] = series.to_numpy()[idx[ok]]
    lag_days[ok] = ((days.to_numpy()[ok] - obs_dates[idx[ok]])
                    / np.timedelta64(1, "D"))
    stale[ok] = lag_days[ok] > MAX_STALE_DAYS
    vals[stale] = np.nan
    n_drop = int((~ok).sum() + stale.sum())
    out = pd.Series(vals, index=days, name=label)
    print(f"  as-of join {label}: {len(days)} days, dropped {n_drop} "
          f"(no-prior {int((~ok).sum())}, stale>{MAX_STALE_DAYS}d {int(stale.sum())}), "
          f"max lag used {np.nanmax(lag_days[~stale & ok]):.0f}d")
    return out, n_drop


# ── permutation (regression analogue of the house convention) ───────────────

def beta_permutation_test(y: np.ndarray, X: np.ndarray, perm_col: int,
                          *, n_perm: int = N_PERM, seed: int = 42
                          ) -> tuple[float, float]:
    """OLS beta for X[:, perm_col] and a two-sided permutation p obtained by
    permuting ONLY that column (controls keep their alignment with y).
    Returns (beta_observed, p_two_sided)."""
    Xd = np.column_stack([np.ones(len(y)), X])
    col = perm_col + 1
    beta_obs = np.linalg.lstsq(Xd, y, rcond=None)[0][col]
    rng = np.random.default_rng(seed)
    null = np.empty(n_perm)
    Xp = Xd.copy()
    for i in range(n_perm):
        Xp[:, col] = rng.permutation(Xd[:, col])
        null[i] = np.linalg.lstsq(Xp, y, rcond=None)[0][col]
    p = float((np.abs(null) >= abs(beta_obs)).mean())
    return float(beta_obs), p


# ── panel ───────────────────────────────────────────────────────────────────

def build_panel() -> pd.DataFrame:
    print("== loading inputs ==")
    px = _load_bars(INPUTS / "USDCAD_D1_TV.csv", "usdcad")
    wti = _load_bars(INPUTS / "WTI_D1_TV.csv", "wti")
    us = _load_rate(INPUTS / "UST_2Y.csv", "us2y")
    ca = _load_rate(INPUTS / "CA_2Y.csv", "ca2y")

    both = us.index.intersection(ca.index)
    spread = (us.loc[both] - ca.loc[both]).rename("spread")
    print(f"  spread: us {len(us)} & ca {len(ca)} -> {len(spread)} joint rate days")

    days = px.index
    spread_asof, _ = _asof_state(spread, days, "spread")
    wti_asof, _ = _asof_state(wti, days, "wti")

    panel = pd.DataFrame({"usdcad": px, "spread_asof": spread_asof,
                          "wti_asof": wti_asof})
    n0 = len(panel)
    panel = panel.dropna()
    print(f"  panel: {n0} USDCAD days -> {len(panel)} complete rows "
          f"({n0 - len(panel)} dropped, counted above)")
    return panel


def build_windows(panel: pd.DataFrame, h: int) -> pd.DataFrame:
    """Consecutive non-overlapping h-day windows with matched-lag x/controls."""
    px = panel["usdcad"].to_numpy()
    sp = panel["spread_asof"].to_numpy()
    wt = panel["wti_asof"].to_numpy()
    idx = panel.index
    rows = []
    start = TREND_LOOKBACK + 1                      # room for the lagged trend
    a = start
    while a + h <= len(panel):
        b = a + h - 1                               # window covers bars a..b
        rows.append({
            "t_start": idx[a], "t_end": idx[b],
            "y": px[b] / px[a - 1] - 1.0,
            "x_dspread": sp[b] - sp[a - 1],
            "wti_ret": wt[b] / wt[a - 1] - 1.0,
            "trend": px[a - 1] / px[a - 1 - TREND_LOOKBACK] - 1.0,
        })
        a += h
    w = pd.DataFrame(rows)
    print(f"  windows h={h}: {len(w)} non-overlapping "
          f"({w['t_start'].min():%Y-%m-%d} -> {w['t_end'].max():%Y-%m-%d})")
    return w


# ── F1 tests ────────────────────────────────────────────────────────────────

def f1b_loading(windows: pd.DataFrame, h: int, *, primary: bool) -> dict:
    y = windows["y"].to_numpy()
    x = windows["x_dspread"].to_numpy()
    beta, p = beta_permutation_test(y, x[:, None], 0, seed=42)
    r = float(np.corrcoef(x, y)[0, 1])
    res = {"h": h, "primary": primary, "n_windows": len(y),
           "beta": beta, "pearson_r": r, "perm_p": p,
           "evaluable": len(y) >= MIN_WINDOWS,
           "fires": bool(p >= P_THRESH or beta < 0)}
    tag = " (PRIMARY)" if primary else ""
    print(f"--- F1(b) h={h}{tag}: n={len(y)} beta={beta:+.5f} "
          f"r={r:+.4f} perm_p={p:.4f} -> {'FIRES' if res['fires'] else 'clear'}")
    return res


def f1a_anticorr(panel: pd.DataFrame) -> dict:
    comp = pd.read_csv(INPUTS / "constellation_daily.csv",
                       index_col="date", parse_dates=True)["composite"]
    lo, hi = comp.index.min(), comp.index.max()
    sub = panel.loc[(panel.index >= lo) & (panel.index <= hi)].copy()
    sub["r1"] = sub["usdcad"].pct_change()
    sub["comp"] = comp.reindex(sub.index).fillna(0.0)   # zero-fill = true book P&L
    d5 = sub["spread_asof"].diff(PRIMARY_H)
    sub = sub.dropna(subset=["r1"])
    widening = d5.reindex(sub.index) > 0

    r_full = float(np.corrcoef(sub["r1"], sub["comp"])[0, 1])
    cond = sub[widening.fillna(False)]
    r_cond = float(np.corrcoef(cond["r1"], cond["comp"])[0, 1]) if len(cond) > 2 else np.nan

    active = sub[sub["comp"] != 0.0]
    r_active = float(np.corrcoef(active["r1"], active["comp"])[0, 1]) if len(active) > 2 else np.nan

    evaluable = (len(cond) >= MIN_COND_DAYS) and (len(sub) >= MIN_COND_DAYS)
    res = {"window": f"{lo:%Y-%m-%d}..{hi:%Y-%m-%d}",
           "n_days": len(sub), "n_widening": int(len(cond)),
           "n_active_days": int(len(active)),
           "corr_full": r_full, "corr_conditional": r_cond,
           "corr_active_only_robustness": r_active,
           "evaluable": evaluable,
           "fires": bool(not np.isnan(r_cond) and r_cond >= 0)}
    print(f"--- F1(a): {len(sub)} days ({res['window']}), widening {len(cond)} | "
          f"corr full {r_full:+.4f}, conditional {r_cond:+.4f}, "
          f"active-only {r_active:+.4f} -> {'FIRES' if res['fires'] else 'clear'}")
    return res


def f1c_isolation(windows: pd.DataFrame) -> dict:
    y = windows["y"].to_numpy()
    X = windows[["x_dspread", "wti_ret", "trend"]].to_numpy()
    beta, p = beta_permutation_test(y, X, 0, seed=43)

    # Descriptive separation (REUSES label_permutation_test, blocked-first).
    widen = windows["x_dspread"].to_numpy() > 0
    yw, yn = y[widen], y[~widen]
    pop = np.concatenate([yw, yn])
    _, _, sep_p = label_permutation_test(pop, len(yw), n_perm=N_PERM, seed=42)

    res = {"n_windows": len(y), "beta_incremental": beta, "perm_p": p,
           "n_widening_windows": int(widen.sum()),
           "mean_y_widening": float(yw.mean()), "mean_y_narrowing": float(yn.mean()),
           "separation_perm_p_descriptive": float(sep_p),
           "evaluable": len(y) >= MIN_WINDOWS,
           "fires": bool(p >= P_THRESH or beta < 0)}
    print(f"--- F1(c): n={len(y)} beta_incr={beta:+.5f} perm_p={p:.4f} | "
          f"widen {widen.sum()} mean {yw.mean()*100:+.3f}% vs narrow {yn.mean()*100:+.3f}% "
          f"(sep p={sep_p:.4f}) -> {'FIRES' if res['fires'] else 'clear'}")
    return res


def episode_betas(panel: pd.DataFrame) -> dict:
    out = {}
    for name, (a, b) in EPISODES.items():
        sub = panel.loc[a:b]
        if len(sub) < TREND_LOOKBACK + 2 * PRIMARY_H:
            out[name] = {"n_windows": 0, "note": "insufficient data"}
            continue
        w = build_windows(sub, PRIMARY_H)
        if len(w) < 10:
            out[name] = {"n_windows": len(w), "note": "n<10, beta not estimated"}
            continue
        yb, xb = w["y"].to_numpy(), w["x_dspread"].to_numpy()
        beta_ep = np.linalg.lstsq(np.column_stack([np.ones(len(yb)), xb]), yb,
                                  rcond=None)[0][1]
        out[name] = {"n_windows": len(w), "beta": float(beta_ep),
                     "pearson_r": float(np.corrcoef(xb, yb)[0, 1])}
    return out


# ── verdict ─────────────────────────────────────────────────────────────────

def verdict_of(c1: dict, c2: dict, c3: dict) -> str:
    crits = [c1, c2, c3]
    if any(not c["evaluable"] for c in crits):
        return "AMBIGUOUS"
    if any(c["fires"] for c in crits):
        return "FAIL"
    return "PASS"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Sovereign F1 mechanism gate")
    ap.add_argument("--out", default=str(_HERE / "gate_result.json"))
    a = ap.parse_args(argv)

    panel = build_panel()

    print("== F1(b) mechanism loading ==")
    w5 = build_windows(panel, PRIMARY_H)
    b_primary = f1b_loading(w5, PRIMARY_H, primary=True)
    b_secondary = []
    for h in SECONDARY_H:
        wh = build_windows(panel, h)
        b_secondary.append(f1b_loading(wh, h, primary=False))

    print("== F1(a) anti-correlation vs Constellation composite ==")
    a_res = f1a_anticorr(panel)

    print("== F1(c) channel isolation (trend + WTI controls) ==")
    c_res = f1c_isolation(w5)

    print("== per-episode loading (descriptive, not gating) ==")
    eps = episode_betas(panel)
    for k, v in eps.items():
        print(f"  {k}: {v}")

    verdict = verdict_of(b_primary, a_res, c_res)
    print(f"\n=== F1 VERDICT: {verdict} ===")
    print("  §3.1 F1(b) primary:", "FIRES" if b_primary["fires"] else "clear")
    print("  §3.2 F1(a) conditional:", "FIRES" if a_res["fires"] else "clear")
    print("  §3.3 F1(c) incremental:", "FIRES" if c_res["fires"] else "clear")

    result = {
        "concept_id": "CONCEPT-USDCAD-RDM-001",
        "verdict": verdict,
        "thresholds": {"p": P_THRESH, "primary_h": PRIMARY_H,
                       "n_perm": N_PERM, "min_windows": MIN_WINDOWS,
                       "min_cond_days": MIN_COND_DAYS},
        "f1b_primary": b_primary,
        "f1b_secondary": b_secondary,
        "f1a": a_res,
        "f1c": c_res,
        "episodes_descriptive": eps,
    }
    Path(a.out).write_text(json.dumps(result, indent=2, default=str),
                           encoding="utf-8")
    print(f"-> {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
