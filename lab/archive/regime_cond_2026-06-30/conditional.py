"""Q-REGIME-COND-1 (re-scoped) — POST-FREEZE conditional forward-distribution characterization.

Runs AFTER the preregistration.md commit. Fetches SPY, computes forward returns at {1,5,20},
the conditional distribution per state (RAW states), then the load-bearing null: residualize the
composite on trailing 20d realized vol (point-in-time expanding OLS), re-derive states from the
residual, and re-run the conditional tables (RESIDUAL states). Emits both side-by-side +
persistence diagnostics. Significance/robustness live in robustness.py.

Run:  python conditional.py        # writes conditional_results.json, prints summary
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import skew as sp_skew

from panel import yahoo, expanding_tercile_state, AXES, expanding_z  # reuse frozen primitives

HERE = Path(__file__).resolve().parent
HORIZONS = [1, 5, 20]
RV_WIN = 20
WARMUP = 252


# ───────────────────────────── SPY forward returns ──
def spy_logret() -> pd.Series:
    import urllib.request, json as _json
    raw = urllib.request.urlopen(urllib.request.Request(
        "https://query1.finance.yahoo.com/v8/finance/chart/SPY?range=30y&interval=1d",
        headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read()
    r = _json.loads(raw)["chart"]["result"][0]
    ts = pd.to_datetime(r["timestamp"], unit="s").normalize()
    adj = pd.Series(r["indicators"]["adjclose"][0]["adjclose"], index=ts, dtype="float64").dropna().sort_index()
    adj = adj[~adj.index.duplicated(keep="last")]
    return np.log(adj).diff().dropna(), adj


def fwd_window_stats(logret: pd.Series, h: int) -> pd.DataFrame:
    """For each date t, forward h-day log return (sum of r[t+1..t+h]) and the worst intra-window
    drawdown of that cumulative path (positive magnitude). Indexed by start date t."""
    lr = logret.to_numpy()
    n = len(lr)
    idx = logret.index
    fwd = np.full(n, np.nan)
    mdd = np.full(n, np.nan)
    for i in range(n - h):
        seg = lr[i + 1: i + 1 + h]
        cum = np.cumsum(seg)
        fwd[i] = cum[-1]
        peak = np.maximum.accumulate(np.concatenate([[0.0], cum]))
        dd = peak - np.concatenate([[0.0], cum])
        mdd[i] = float(dd.max())  # >=0 ; worst peak-to-trough within window
    return pd.DataFrame({"fwd": fwd, "mdd": mdd}, index=idx)


def bucket_metrics(fwd: np.ndarray, mdd: np.ndarray) -> dict:
    fwd = fwd[np.isfinite(fwd)]
    n = len(fwd)
    if n < 10:
        return dict(n=n, insufficient=True)
    s = np.sort(fwd)
    k5 = max(1, int(np.ceil(0.05 * n)))
    k1 = max(1, int(np.ceil(0.01 * n)))
    md = mdd[np.isfinite(mdd)]
    return dict(
        n=int(n),
        mean=float(np.mean(fwd)),
        stdev=float(np.std(fwd, ddof=1)),
        skew=float(sp_skew(fwd)),
        semidev=float(np.sqrt(np.mean(np.minimum(fwd, 0.0) ** 2))),
        cvar5=float(np.mean(s[:k5])),          # left-tail mean (negative)
        cvar1=float(np.mean(s[:k1])),
        hit=float(np.mean(fwd > 0)),
        mdd_mean=float(np.mean(md)) if len(md) else float("nan"),
        mdd_p95=float(np.percentile(md, 95)) if len(md) else float("nan"),
    )


def conditional_table(states: pd.Series, fwdstats: pd.DataFrame, h: int) -> dict:
    """Non-overlapping (stride h, offset 0) primary buckets per state."""
    df = pd.DataFrame({"state": states}).join(fwdstats, how="inner").dropna(subset=["fwd"])
    df = df[df["state"].notna()]
    nonov = df.iloc[::h]  # non-overlapping start dates
    out = {"_n_nonoverlap_total": int(len(nonov))}
    for st in ("off", "neutral", "on"):
        b = nonov[nonov["state"] == st]
        out[st] = bucket_metrics(b["fwd"].to_numpy(), b["mdd"].to_numpy())
    # SEP statistics (off - on), pre-registered expected > 0
    o, n_, on = out["off"], out["neutral"], out["on"]
    if not o.get("insufficient") and not on.get("insufficient"):
        out["SEP_vol"] = o["stdev"] - on["stdev"]
        out["SEP_cvar"] = abs(o["cvar5"]) - abs(on["cvar5"])
        out["SEP_mdd"] = o["mdd_mean"] - on["mdd_mean"]
        out["mono_vol"] = bool(o["stdev"] > n_["stdev"] > on["stdev"]) if not n_.get("insufficient") else None
        out["mono_cvar"] = bool(abs(o["cvar5"]) > abs(n_["cvar5"]) > abs(on["cvar5"])) if not n_.get("insufficient") else None
    return out


# ───────────────────────────── point-in-time residualization (the load-bearing null) ──
def expanding_ols_residual(y: pd.Series, x: pd.Series, warmup: int = WARMUP) -> pd.Series:
    """Residual of expanding OLS y ~ [1, x], coefficients using only obs <= t (point-in-time).
    O(n) via cumulative normal-equation sums over complete cases."""
    df = pd.DataFrame({"y": y, "x": x}).dropna()
    yv, xv = df["y"].to_numpy(), df["x"].to_numpy()
    n = len(df)
    res = np.full(n, np.nan)
    Sn = Sx = Sxx = Sy = Sxy = 0.0
    for i in range(n):
        xi, yi = xv[i], yv[i]
        Sn += 1; Sx += xi; Sxx += xi * xi; Sy += yi; Sxy += xi * yi
        if i + 1 >= warmup:
            det = Sn * Sxx - Sx * Sx
            if abs(det) > 1e-12:
                b0 = (Sxx * Sy - Sx * Sxy) / det
                b1 = (Sn * Sxy - Sx * Sy) / det
                res[i] = yi - (b0 + b1 * xi)
    return pd.Series(res, index=df.index)


def full_sample_residual(y: pd.Series, x: pd.Series) -> pd.Series:
    df = pd.DataFrame({"y": y, "x": x}).dropna()
    X = np.column_stack([np.ones(len(df)), df["x"].to_numpy()])
    beta, *_ = np.linalg.lstsq(X, df["y"].to_numpy(), rcond=None)
    return pd.Series(df["y"].to_numpy() - X @ beta, index=df.index)


# ───────────────────────────── persistence diagnostics ──
def persistence(states: pd.Series) -> dict:
    s = states.dropna()
    # dwell times
    runs = []
    prev, length = None, 0
    for v in s:
        if v == prev:
            length += 1
        else:
            if prev is not None:
                runs.append((prev, length))
            prev, length = v, 1
    runs.append((prev, length))
    dwell = {st: [l for (v, l) in runs if v == st] for st in ("off", "neutral", "on")}
    # transition matrix
    labs = ["off", "neutral", "on"]
    idx = {l: i for i, l in enumerate(labs)}
    T = np.zeros((3, 3))
    arr = s.to_numpy()
    for a, b in zip(arr[:-1], arr[1:]):
        T[idx[a], idx[b]] += 1
    Tn = T / T.sum(axis=1, keepdims=True)
    n_years = (s.index.max() - s.index.min()).days / 365.25
    n_changes = int((arr[:-1] != arr[1:]).sum())
    return dict(
        dwell_median={st: (float(np.median(d)) if d else None) for st, d in dwell.items()},
        dwell_mean={st: (float(np.mean(d)) if d else None) for st, d in dwell.items()},
        transition_matrix={labs[i]: {labs[j]: round(float(Tn[i, j]), 3) for j in range(3)} for i in range(3)},
        changes_per_year=round(n_changes / n_years, 1),
        min_median_dwell=min([np.median(d) for d in dwell.values() if d]),
    )


# ───────────────────────────── main ──
def main():
    panel = pd.read_csv(HERE / "panel.csv", index_col=0, parse_dates=True)
    logret, adj = spy_logret()
    rv = logret.rolling(RV_WIN).std()

    # align RV to panel dates
    comp = panel["composite_eqw"]
    comp_pca = panel["composite_pca1"]
    rv_on_panel = rv.reindex(comp.index)

    # residual composites (point-in-time + full-sample cross-check)
    resid_pit = expanding_ols_residual(comp, rv_on_panel).reindex(comp.index)
    resid_fs = full_sample_residual(comp, rv_on_panel).reindex(comp.index)
    resid_pca = expanding_ols_residual(comp_pca, rv_on_panel).reindex(comp.index)  # SECONDARY composite

    states_raw = panel["state_eqw"]
    states_resid = expanding_tercile_state(resid_pit)
    states_resid_fs = expanding_tercile_state(resid_fs)
    states_pca = panel["state_pca1"]
    states_resid_pca = expanding_tercile_state(resid_pca)  # SECONDARY: residualized PCA-1 states

    fwd = {h: fwd_window_stats(logret, h) for h in HORIZONS}

    def tables(states):
        return {f"{h}d": conditional_table(states, fwd[h], h) for h in HORIZONS}

    results = {
        "meta": dict(
            spy_span=[str(logret.index.min().date()), str(logret.index.max().date())],
            n_states_raw=int(states_raw.notna().sum()),
            n_states_resid=int(states_resid.notna().sum()),
            rv_corr_composite=float(pd.concat([comp, rv_on_panel], axis=1).dropna().corr().iloc[0, 1]),
            resid_rv_corr=float(pd.concat([resid_pit, rv_on_panel], axis=1).dropna().corr().iloc[0, 1]),
            resid_pca_rv_corr=float(pd.concat([resid_pca, rv_on_panel], axis=1).dropna().corr().iloc[0, 1]),
        ),
        "raw_states_eqw": tables(states_raw),
        "residual_states_eqw_PIT": tables(states_resid),
        "residual_states_eqw_fullsample_xcheck": tables(states_resid_fs),
        "raw_states_pca1": tables(states_pca),
        "residual_states_pca1_PIT_secondary": tables(states_resid_pca),
        "persistence_raw": persistence(states_raw),
        "persistence_resid": persistence(states_resid),
    }
    (HERE / "conditional_results.json").write_text(json.dumps(results, indent=2))

    # ── readable summary ──
    print(f"SPY span {results['meta']['spy_span']}  | corr(composite, trailingRV)={results['meta']['rv_corr_composite']:+.3f}"
          f"  corr(residual, trailingRV)={results['meta']['resid_rv_corr']:+.3f} (should be ~0)")
    print(f"persistence raw: changes/yr={results['persistence_raw']['changes_per_year']} "
          f"min-median-dwell={results['persistence_raw']['min_median_dwell']}d  dwell_median={results['persistence_raw']['dwell_median']}")
    for label, key in [("RAW states (eqw)", "raw_states_eqw"),
                       ("RESIDUAL states (eqw, PIT)  <-- load-bearing", "residual_states_eqw_PIT")]:
        print(f"\n=== {label} ===")
        print(f"{'h':>3} {'off.std':>8} {'neu.std':>8} {'on.std':>8} {'SEP_vol':>8} {'mono':>5} "
              f"{'off.cv5':>8} {'on.cv5':>8} {'SEP_cv':>7} {'off.mdd':>8} {'on.mdd':>8} {'noff':>5} {'non':>4}")
        for h in HORIZONS:
            t = results[key][f"{h}d"]
            if "SEP_vol" not in t:
                print(f"{h:>3}d  (insufficient)"); continue
            o, ne, on = t["off"], t["neutral"], t["on"]
            print(f"{h:>3} {o['stdev']:>8.4f} {ne['stdev']:>8.4f} {on['stdev']:>8.4f} {t['SEP_vol']:>+8.4f} "
                  f"{str(t['mono_vol']):>5} {o['cvar5']:>+8.4f} {on['cvar5']:>+8.4f} {t['SEP_cvar']:>+7.4f} "
                  f"{o['mdd_mean']:>8.4f} {on['mdd_mean']:>8.4f} {o['n']:>5} {on['n']:>4}")
    print(f"\nwrote conditional_results.json")


if __name__ == "__main__":
    main()
