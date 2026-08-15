#!/usr/bin/env python3
"""NOCT-SPX-001 Stage 1+2 channel-isolating falsifier.

Tests the proposal's claim that the SPX500 European-open window (02:00-05:30 ET)
return is carried *specifically* by days following a US-session sell-off (dealer
inventory-reversal / Grossman-Miller immediacy premium), NOT by an unconditional
time-of-day drift. This is a mechanism falsifier ONLY — no strategy is built
(brief CC-HANDOFF-NOCT-SPX-001-stage1-2 §5 forbidden moves).

Pre-registered gate (brief §2-§4), all NET OF COST:
  (a) bottom-tercile (largest prior US sell-off) mean R_EU > 0, t>=2, n>=200.
  (b) separation = bottom-tercile mean R_EU - all-days mean R_EU, t>=2, with the
      CORRECT overlapping-sample SE (the all-days sample contains the bottom
      tercile). Cross-checks: bottom-minus-top and bottom-minus-complement Welch t.
  (c) monotonicity: bottom-tercile R_EU > top-tercile R_EU.
Stage 1 PASS iff (a) AND (b) AND (c). Stage 2: re-run on 2021-2026 alone, PASS iff
conditional net Sharpe >= 0.5 AND sign of (a)/(b)/(c) preserved. Overall = both.

Causal-lag (load-bearing): the EU window on date t is conditioned on the PRIOR
trading day's US session R_US(t-1). The 02:00-05:30 ET window precedes that day's
09:30 ET US open, so same-day conditioning would be look-ahead. The mechanism
("days following a US-session sell-off") fixes the one-session lag. This mirrors
the classic overnight-reversal pairing: intraday return day d -> overnight/EU
window into day d+1.

Bar mapping (m15 bars stamped at bar-OPEN, :00/:15/:30/:45):
  R_US        = (close[15:45 ET bar] - open[09:30 ET bar]) / open[09:30 ET bar]
                (RTH open-to-close; '15:55' -> close of the final RTH bar = 16:00 print)
  R_US_last90 = (close[15:45] - open[14:30]) / open[14:30]   (robustness only)
  R_EU        = (close[05:15 ET bar] - open[02:00 ET bar]) / open[02:00 ET bar]
                (02:00 -> 05:30 hold; exit = close of the 05:15-05:30 bar)

Cost: round-trip spread applied to R_EU (entry+exit). No recorded FXIFY/Alchemy
SPX500 spread (Phase 0), so sweep {0,1,2,3,5} bps + report BREAKEVEN. Swap=0: the
02:00-05:30 ET window is intraday, well after the 17:00 ET prior rollover and
before the next, so no overnight financing event is incurred.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from scipy import stats as _sps
    def _t_sf(t_abs, df):  # two-sided p
        return float(2 * _sps.t.sf(t_abs, df))
except Exception:  # pragma: no cover - normal approx fallback
    def _t_sf(t_abs, df):
        return float(math.erfc(t_abs / math.sqrt(2)))

SPREAD_SWEEP_BPS = [0, 1, 2, 3, 5]
STAGE2_START = pd.Timestamp("2021-01-01")
TRIGGER_FLOOR = 200          # (a) min trigger days, full sample
STAGE2_TRIGGER_FLOOR = 100   # low-power note threshold, post-2020
T_GATE = 2.0
SHARPE_GATE = 0.5


# ---------------------------------------------------------------------------
# Load + session returns
# ---------------------------------------------------------------------------
def load_bars(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    ts_utc = pd.to_datetime(df["time"], utc=True, format="ISO8601")
    et = ts_utc.dt.tz_convert("America/New_York")
    out = pd.DataFrame({
        "utc": ts_utc.dt.tz_localize(None).values,
        "et": et.dt.tz_localize(None).values,
        "open": df["open"].astype(float).values,
        "high": df["high"].astype(float).values,
        "low": df["low"].astype(float).values,
        "close": df["close"].astype(float).values,
    })
    out["et_date"] = out["et"].dt.normalize()
    out["et_hm"] = out["et"].dt.strftime("%H:%M")
    return out


def session_returns(bars: pd.DataFrame) -> pd.DataFrame:
    """Per ET trading-date R_US / R_US_last90 / R_EU from the bar wall-clock map."""
    # (et_date, HH:MM) -> open/close lookup
    op = bars.set_index(["et_date", "et_hm"])["open"].to_dict()
    cl = bars.set_index(["et_date", "et_hm"])["close"].to_dict()
    dates = sorted(bars["et_date"].unique())

    rows = []
    for d in dates:
        o_eu = op.get((d, "02:00"))
        c_eu = cl.get((d, "05:15"))
        o_us = op.get((d, "09:30"))
        c_us = cl.get((d, "15:45"))
        o_l90 = op.get((d, "14:30"))
        r_eu = (c_eu - o_eu) / o_eu if (o_eu and c_eu) else np.nan
        r_us = (c_us - o_us) / o_us if (o_us and c_us) else np.nan
        r_l90 = (c_us - o_l90) / o_l90 if (o_l90 and c_us) else np.nan
        rows.append((d, r_eu, r_us, r_l90))
    df = pd.DataFrame(rows, columns=["et_date", "R_EU", "R_US", "R_US_last90"]).set_index("et_date")
    df = df.sort_index()
    # Causal lag: condition each EU window (date t) on the most recent PRIOR
    # trading day's US session (strictly < t). NOT shift(1): the frame contains
    # weekend/partial dates with NaN R_US, so a row-shift would map Monday's EU
    # window to the (empty) Sunday row and silently drop every Monday (whose true
    # prior session is Friday). asof-on-valid-US-days fixes that bias.
    df["R_US_prev"] = _prior_session(df.index, df["R_US"])
    df["R_US_last90_prev"] = _prior_session(df.index, df["R_US_last90"])
    return df


def _prior_session(all_dates: pd.Index, us_series: pd.Series) -> np.ndarray:
    """For each date in all_dates, the value of us_series at the most recent date
    STRICTLY BEFORE it that has a non-NaN value (the prior US session)."""
    valid = us_series.dropna()
    vd = valid.index.to_numpy()
    vv = valid.to_numpy()
    if len(vd) == 0:
        return np.full(len(all_dates), np.nan)
    # side='left': for date t, insertion point is t's position among valid US dates;
    # -1 selects the most recent valid US date strictly before t (same-day US is the
    # afternoon session, AFTER the morning EU window, so it must be excluded).
    pos = np.searchsorted(vd, all_dates.to_numpy(), side="left") - 1
    out = np.where(pos >= 0, vv[np.clip(pos, 0, len(vv) - 1)], np.nan)
    return out


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------
def _one_sample_t(x: np.ndarray):
    n = len(x)
    m = float(np.mean(x))
    s = float(np.std(x, ddof=1))
    se = s / math.sqrt(n)
    t = m / se if se > 0 else float("nan")
    return m, se, t, _t_sf(abs(t), n - 1), n


def _welch_t(a: np.ndarray, b: np.ndarray):
    """Two-sample Welch t for mean(a) - mean(b)."""
    na, nb = len(a), len(b)
    ma, mb = float(np.mean(a)), float(np.mean(b))
    va, vb = float(np.var(a, ddof=1)), float(np.var(b, ddof=1))
    se = math.sqrt(va / na + vb / nb)
    diff = ma - mb
    t = diff / se if se > 0 else float("nan")
    # Welch-Satterthwaite df
    df = (va / na + vb / nb) ** 2 / ((va / na) ** 2 / (na - 1) + (vb / nb) ** 2 / (nb - 1))
    return diff, se, t, _t_sf(abs(t), df), df


def terciles(x: np.ndarray):
    q33, q67 = np.quantile(x, [1 / 3, 2 / 3])
    return q33, q67


def evaluate(df: pd.DataFrame, spread_bps: float, x_col: str = "R_US_prev",
             y_col: str = "R_EU") -> dict:
    """Run (a)/(b)/(c) at a given round-trip cost (bps) on the conditioning x_col."""
    sub = df[[x_col, y_col]].dropna()
    x = sub[x_col].to_numpy()
    y_net = sub[y_col].to_numpy() - spread_bps / 1e4  # round-trip cost on R_EU
    q33, q67 = terciles(x)
    bottom_m = x <= q33
    top_m = x >= q67
    comp_m = ~bottom_m            # complement = middle + top

    yb = y_net[bottom_m]
    yt = y_net[top_m]
    yc = y_net[comp_m]
    y_all = y_net

    # (a) bottom-tercile mean > 0
    a_m, a_se, a_t, a_p, a_n = _one_sample_t(yb)

    # (b) separation bottom - all, with overlap-correct SE.
    #     D = mean_B - mean_All = ((n-nB)/n)*(mean_B - mean_C);  B,C disjoint =>
    #     SE(D) = ((n-nB)/n)*sqrt(sB^2/nB + sC^2/nC). The resulting t EQUALS the
    #     bottom-vs-complement Welch t (the (n-nB)/n factor cancels).
    n = len(y_all)
    nB = len(yb)
    scale = (n - nB) / n
    diff_BC, se_BC, t_BC, p_BC, df_BC = _welch_t(yb, yc)
    D = float(np.mean(yb) - np.mean(y_all))
    se_D = scale * se_BC
    t_D = D / se_D if se_D > 0 else float("nan")
    p_D = _t_sf(abs(t_D), df_BC)

    # cross-check: bottom - top
    diff_BT, se_BT, t_BT, p_BT, df_BT = _welch_t(yb, yt)

    # (c) monotonicity bottom > top
    c_ok = bool(np.mean(yb) > np.mean(yt))

    return {
        "spread_bps": spread_bps, "n_all": n,
        "tercile_q33": float(q33), "tercile_q67": float(q67),
        "a": {"mean": a_m, "se": a_se, "t": a_t, "p": a_p, "n_trigger": a_n,
              "pass": bool(a_m > 0 and a_t >= T_GATE and a_n >= TRIGGER_FLOOR)},
        "b": {"separation_D": D, "se_D": se_D, "t": t_D, "p": p_D,
              "pass": bool(D > 0 and t_D >= T_GATE),
              "x_bottom_vs_complement_t": t_BC, "x_bottom_vs_top_t": t_BT,
              "bottom_vs_top_diff": diff_BT},
        "c": {"bottom_mean": float(np.mean(yb)), "top_mean": float(np.mean(yt)),
              "pass": c_ok},
        "means": {"bottom": float(np.mean(yb)), "top": float(np.mean(yt)),
                  "complement": float(np.mean(yc)), "all": float(np.mean(y_all))},
    }


def breakeven_bps(df: pd.DataFrame, x_col="R_US_prev", y_col="R_EU") -> float:
    """Round-trip bps at which gross bottom-tercile mean R_EU -> 0."""
    sub = df[[x_col, y_col]].dropna()
    x = sub[x_col].to_numpy()
    q33, _ = terciles(x)
    yb = sub[y_col].to_numpy()[x <= q33]
    return float(np.mean(yb) * 1e4)  # gross mean in bps


def conditional_sharpe(df: pd.DataFrame, spread_bps: float, x_col="R_US_prev",
                       y_col="R_EU") -> dict:
    """Annualized Sharpe of the net trigger-day R_EU series.

    Annualization convention (pre-registered here, brief left it unspecified):
    annualized = (mean/std) * sqrt(trades_per_year), trades_per_year = n_trigger /
    (calendar span of trigger days in years). Mirrors a per-trade-Sharpe scaled by
    trade frequency (the SR 917 'post-cost Sharpe ~1.1' is an annualized figure).
    """
    sub = df[[x_col, y_col]].dropna()
    x = sub[x_col].to_numpy()
    q33, _ = terciles(x)
    mask = x <= q33
    y = sub[y_col].to_numpy()[mask] - spread_bps / 1e4
    dates = sub.index.to_numpy()[mask]
    n = len(y)
    if n < 2:
        return {"sharpe_ann": float("nan"), "n": n, "per_trade": float("nan")}
    mean, std = float(np.mean(y)), float(np.std(y, ddof=1))
    per_trade = mean / std if std > 0 else float("nan")
    span_days = (pd.Timestamp(dates.max()) - pd.Timestamp(dates.min())).days or 1
    years = span_days / 365.25
    trades_per_year = n / years
    sharpe_ann = per_trade * math.sqrt(trades_per_year)
    return {"sharpe_ann": sharpe_ann, "per_trade": per_trade, "n": n,
            "trades_per_year": trades_per_year, "mean": mean, "std": std}


# ---------------------------------------------------------------------------
# DST verification (brief §2.2 mandatory spot-check)
# ---------------------------------------------------------------------------
def dst_spotcheck(bars: pd.DataFrame) -> list[dict]:
    """For known DST-boundary dates, show the 02:00 ET bar's UTC + London time.

    Confirms the UTC->ET map is DST-aware: 02:00 ET = 06:00 UTC in summer (EDT,
    UTC-4) vs 07:00 UTC in winter (EST, UTC-5); London = 07:00 normally but
    06:00/08:00 during the US-EU mismatch weeks (the load-bearing effect).
    """
    op_utc = bars.set_index(["et_date", "et_hm"])["utc"].to_dict()
    checks = []
    probe_dates = [
        ("2022-07-15", "summer (EDT, both on DST)"),
        ("2022-01-14", "winter (EST, both off DST)"),
        ("2022-03-16", "US-EU mismatch (US on EDT, EU still GMT)"),
        ("2023-03-15", "US-EU mismatch (US on EDT, EU still GMT)"),
        ("2022-11-02", "US-EU mismatch (US still EDT? Nov: EU back first)"),
    ]
    for ds, label in probe_dates:
        d = pd.Timestamp(ds).normalize()
        utc = op_utc.get((d, "02:00"))
        if utc is None:
            checks.append({"date": ds, "label": label, "note": "no 02:00 ET bar (holiday/weekend)"})
            continue
        utc_ts = pd.Timestamp(utc).tz_localize("UTC")
        london = utc_ts.tz_convert("Europe/London")
        et = utc_ts.tz_convert("America/New_York")
        checks.append({
            "date": ds, "label": label,
            "et_0200_in_utc": utc_ts.strftime("%H:%M UTC"),
            "et_offset": et.strftime("%z"),
            "london_time": london.strftime("%H:%M %Z"),
        })
    return checks


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
def run(bars_path: Path, out_dir: Path) -> dict:
    bars = load_bars(bars_path)
    rets = session_returns(bars)

    analysis = rets[["R_US_prev", "R_EU"]].dropna()
    full_n = len(analysis)
    date_min, date_max = analysis.index.min(), analysis.index.max()

    # ---- Stage 1 (full sample) ----
    be = breakeven_bps(rets)
    s1 = {s: evaluate(rets, s) for s in SPREAD_SWEEP_BPS}
    # robustness: last-90-min proxy (reported, NOT a pass route)
    rob = {s: evaluate(rets, s, x_col="R_US_last90_prev") for s in SPREAD_SWEEP_BPS}

    # Stage 1 verdict at each spread; clean KILL if it fails even gross.
    def stage1_pass(ev):
        return ev["a"]["pass"] and ev["b"]["pass"] and ev["c"]["pass"]
    s1_pass_by_spread = {s: stage1_pass(s1[s]) for s in SPREAD_SWEEP_BPS}

    # ---- Stage 2 (2021-2026) ----
    sub = rets[rets.index >= STAGE2_START]
    sub_an = sub[["R_US_prev", "R_EU"]].dropna()
    s2_be = breakeven_bps(sub)
    s2 = {s: evaluate(sub, s) for s in SPREAD_SWEEP_BPS}
    s2_sharpe = {s: conditional_sharpe(sub, s) for s in SPREAD_SWEEP_BPS}

    def stage2_pass(ev, sh):
        sign_ok = (ev["a"]["mean"] > 0 and ev["b"]["separation_D"] > 0 and ev["c"]["pass"])
        return bool(sign_ok and sh["sharpe_ann"] >= SHARPE_GATE)
    s2_pass_by_spread = {s: stage2_pass(s2[s], s2_sharpe[s]) for s in SPREAD_SWEEP_BPS}

    dst = dst_spotcheck(bars)

    result = {
        "data": {
            "instrument": "USA500IDXUSD (Dukascopy)", "tz": "UTC->ET DST-aware",
            "bar_rows": int(len(bars)),
            "bar_first": str(bars["utc"].min()), "bar_last": str(bars["utc"].max()),
            "analysis_days_full": int(full_n),
            "analysis_date_min": str(date_min.date()), "analysis_date_max": str(date_max.date()),
            "analysis_days_stage2": int(len(sub_an)),
        },
        "stage1": {"breakeven_bps": be, "by_spread": s1, "pass_by_spread": s1_pass_by_spread},
        "robustness_last90": rob,
        "stage2": {"start": str(STAGE2_START.date()), "breakeven_bps": s2_be,
                   "by_spread": s2, "sharpe_by_spread": s2_sharpe,
                   "pass_by_spread": s2_pass_by_spread},
        "dst_spotcheck": dst,
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "gate_result.json").write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    return result


def _fmt_pct(x):  # return as bps-ish percentage
    return f"{x*100:.4f}%"


def print_summary(r: dict):
    d = r["data"]
    print("=" * 78)
    print("NOCT-SPX-001 Stage 1+2 channel-isolating falsifier")
    print("=" * 78)
    print(f"data: {d['instrument']}  rows={d['bar_rows']}  {d['bar_first']} -> {d['bar_last']}")
    print(f"analysis days (full): {d['analysis_days_full']}  "
          f"[{d['analysis_date_min']} -> {d['analysis_date_max']}]")
    print(f"analysis days (2021+): {d['analysis_days_stage2']}")
    print()
    print("--- DST spot-check (02:00 ET bar) ---")
    for c in r["dst_spotcheck"]:
        if "et_0200_in_utc" in c:
            print(f"  {c['date']} {c['label']:<42} 02:00 ET = {c['et_0200_in_utc']} "
                  f"(off {c['et_offset']}) = {c['london_time']}")
        else:
            print(f"  {c['date']} {c['label']:<42} {c['note']}")
    print()
    print("--- STAGE 1 (full sample), conditioning = PRIOR US session R_US ---")
    print(f"  breakeven round-trip spread (gross bottom-tercile mean -> 0): {r['stage1']['breakeven_bps']:.3f} bps")
    print(f"  {'spread':>6} {'(a) mean':>11} {'(a) t':>7} {'n_trig':>6} "
          f"{'(b) D':>11} {'(b) t':>7} {'b-top t':>8} {'(c) bot>top':>11} {'PASS':>5}")
    for s in SPREAD_SWEEP_BPS:
        e = r["stage1"]["by_spread"][str(s)] if str(s) in r["stage1"]["by_spread"] else r["stage1"]["by_spread"][s]
        a, b, c = e["a"], e["b"], e["c"]
        print(f"  {s:>6} {_fmt_pct(a['mean']):>11} {a['t']:>7.2f} {a['n_trigger']:>6} "
              f"{_fmt_pct(b['separation_D']):>11} {b['t']:>7.2f} {b['x_bottom_vs_top_t']:>8.2f} "
              f"{str(c['pass']):>11} {str(e['a']['pass'] and e['b']['pass'] and e['c']['pass']):>5}")
    print()
    print("--- STAGE 2 (2021-2026) ---")
    print(f"  breakeven round-trip spread: {r['stage2']['breakeven_bps']:.3f} bps")
    print(f"  {'spread':>6} {'(a) mean':>11} {'(a) t':>7} {'(b) t':>7} {'bot>top':>8} "
          f"{'Sharpe_ann':>11} {'n_trig':>6} {'PASS':>5}")
    for s in SPREAD_SWEEP_BPS:
        e = r["stage2"]["by_spread"][str(s)] if str(s) in r["stage2"]["by_spread"] else r["stage2"]["by_spread"][s]
        sh = r["stage2"]["sharpe_by_spread"][str(s)] if str(s) in r["stage2"]["sharpe_by_spread"] else r["stage2"]["sharpe_by_spread"][s]
        a, b, c = e["a"], e["b"], e["c"]
        print(f"  {s:>6} {_fmt_pct(a['mean']):>11} {a['t']:>7.2f} {b['t']:>7.2f} "
              f"{str(c['pass']):>8} {sh['sharpe_ann']:>11.3f} {sh['n']:>6} "
              f"{str((a['mean']>0 and b['separation_D']>0 and c['pass']) and sh['sharpe_ann']>=SHARPE_GATE):>5}")
    print()
    # Robustness (last-90-min), spread=2 only
    e = r["robustness_last90"]
    e2 = e[str(2)] if str(2) in e else e[2]
    print(f"--- robustness: R_US_last90 proxy @ 2bps (NOT a pass route) ---")
    print(f"  (a) mean {_fmt_pct(e2['a']['mean'])} t={e2['a']['t']:.2f} | "
          f"(b) t={e2['b']['t']:.2f} | (c) bot>top={e2['c']['pass']}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="NOCT-SPX-001 Stage 1+2 falsifier")
    ap.add_argument("--bars", default="core/data/bar_data/USA500IDXUSD_M15.csv")
    ap.add_argument("--out", default="lab/analysis/noct_spx")
    a = ap.parse_args(argv)
    r = run(Path(a.bars), Path(a.out))
    print_summary(r)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
