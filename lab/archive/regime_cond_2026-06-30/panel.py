"""Q-REGIME-COND-1 (re-scoped Option-B) — composite-input panel + point-in-time states.

PRE-REGISTRATION-PHASE ARTIFACT. This module builds ONLY the regime composite and its
tercile states from four free-fetchable risk axes. It DOES NOT touch SPY or any forward
return — that is deliberately deferred to conditional.py so the preregistration.md commit
provably precedes the first forward-return read (brief §5 #1, §10 audit hook).

Four axes (one representative proxy each, to avoid intra-axis double-count), all oriented so
that HIGHER oriented-z = MORE risk-off:
  volatility   VIX            (CBOE, 1990->)               +z
  credit       HYG/LQD ratio  (Yahoo, 2007-04->) binding   -z   (high HY/IG = risk-ON)
  rates/x-asset MOVE          (Yahoo ^MOVE, 2002-11->)     +z
  FX           DXY            (Yahoo DX-Y.NYB, 2001-07->)  +z   (broad USD strength = risk-off)

Normalization is EXPANDING / point-in-time only (forbidden move §5 #2: no full-sample z).
Composite primary = equal-weight mean of oriented expanding-z. Secondary = expanding PCA-1.
States = expanding (point-in-time) tercile cuts on the composite. K=3 (pre-registered).

Run:
  python panel.py            # fetch live, build panel.csv + coverage.json, print coverage
  python panel.py --selftest # run the point-in-time correctness self-tests (no network)
"""
from __future__ import annotations
import sys, io, json, urllib.request
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
WARMUP = 252          # trading days before an expanding-z / expanding-tercile is emitted
PCA_REFIT_STRIDE = 5  # refit expanding PCA-1 every N days (loadings ffilled between), for speed

# ───────────────────────────── fetchers (reused from regime_signal_research score_newfree.py) ──
def _get(url: str, ua: bool = True) -> bytes:
    h = {"User-Agent": "Mozilla/5.0"} if ua else {}
    return urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=60).read()

def cboe(sym: str, col: str = "CLOSE") -> pd.Series:
    d = pd.read_csv(io.BytesIO(_get(f"https://cdn.cboe.com/api/global/us_indices/daily_prices/{sym}_History.csv")))
    d.columns = [c.strip().upper() for c in d.columns]
    dt = pd.to_datetime(d["DATE"], format="%m/%d/%Y")
    vc = col if col in d.columns else [c for c in d.columns if c != "DATE"][-1]
    return pd.Series(d[vc].astype(float).values, index=dt).sort_index()

def yahoo(sym: str, rng: str = "30y") -> pd.Series:
    j = json.loads(_get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range={rng}&interval=1d"))
    r = j["chart"]["result"][0]
    ts = pd.to_datetime(r["timestamp"], unit="s").normalize()
    return pd.Series(r["indicators"]["quote"][0]["close"], index=ts, dtype="float64").dropna().sort_index()

# ───────────────────────────── point-in-time primitives (correctness-critical) ──
def expanding_z(x: pd.Series, warmup: int = WARMUP) -> pd.Series:
    """Expanding (point-in-time) z-score. Uses ONLY obs <= t. ddof=1. NaN before warmup."""
    mu = x.expanding(min_periods=warmup).mean()
    sd = x.expanding(min_periods=warmup).std(ddof=1)
    return (x - mu) / sd

def expanding_tercile_state(comp: pd.Series, warmup: int = WARMUP) -> pd.Series:
    """Point-in-time tercile state on the composite. Thresholds at t use only comp values <= t.
    Returns labels in {'on','neutral','off'}; 'off' = risk-off (top tercile)."""
    q33 = comp.expanding(min_periods=warmup).quantile(1 / 3)
    q67 = comp.expanding(min_periods=warmup).quantile(2 / 3)
    out = pd.Series(index=comp.index, dtype=object)
    valid = comp.notna() & q33.notna() & q67.notna()
    out[valid & (comp >= q67)] = "off"
    out[valid & (comp <= q33)] = "on"
    out[valid & (comp > q33) & (comp < q67)] = "neutral"
    return out

def expanding_pca1(zmat: pd.DataFrame, warmup: int = WARMUP, stride: int = PCA_REFIT_STRIDE,
                   align_to: pd.Series | None = None) -> tuple[pd.Series, pd.DataFrame]:
    """Expanding PCA-1 projection, loadings refit point-in-time every `stride` days and
    forward-held between refits. Sign aligned so PC1 correlates >=0 with `align_to` (the
    equal-weight composite) using only data <= t. Returns (pc1_series, loadings_trace)."""
    cols = list(zmat.columns)
    idx = zmat.index
    pc1 = pd.Series(index=idx, dtype="float64")
    load_rows = {}
    last_load = None
    Zfull = zmat.to_numpy()
    for i, t in enumerate(idx):
        n = i + 1
        if n < warmup:
            continue
        if last_load is None or (i % stride == 0):
            W = Zfull[:n]
            mask = np.all(np.isfinite(W), axis=1)
            Wc = W[mask]
            if Wc.shape[0] < warmup // 2 or Wc.shape[0] < len(cols) + 2:
                continue
            mu = Wc.mean(axis=0)
            cov = np.cov((Wc - mu).T)
            evals, evecs = np.linalg.eigh(cov)
            load = evecs[:, -1]  # top eigenvector
            # sign-align to equal-weight composite (data <= t only)
            if align_to is not None:
                proj_hist = (W[mask] - mu) @ load
                a = align_to.to_numpy()[:n][mask]
                m2 = np.isfinite(a) & np.isfinite(proj_hist)
                if m2.sum() > 5 and np.corrcoef(a[m2], proj_hist[m2])[0, 1] < 0:
                    load = -load
            else:
                if load.sum() < 0:
                    load = -load
            last_load = (mu, load)
            load_rows[t] = dict(zip(cols, load))
        mu, load = last_load
        xt = Zfull[i]
        if np.all(np.isfinite(xt)):
            pc1[t] = float((xt - mu) @ load)
    return pc1, pd.DataFrame(load_rows).T

# ───────────────────────────── panel build ──
AXES = {
    "VIX":  dict(orient=+1, axis="volatility"),
    "CRED": dict(orient=-1, axis="credit"),      # HYG/LQD ratio; high = risk-ON -> orient -1
    "MOVE": dict(orient=+1, axis="rates_xasset"),
    "DXY":  dict(orient=+1, axis="fx"),
}

def fetch_raw() -> pd.DataFrame:
    vix = cboe("VIX")
    hyg = yahoo("HYG"); lqd = yahoo("LQD")
    idx = hyg.index.intersection(lqd.index)
    cred = (hyg.loc[idx] / lqd.loc[idx]).sort_index()
    move = yahoo("%5EMOVE")
    dxy = yahoo("DX-Y.NYB")
    raw = pd.DataFrame({"VIX": vix, "CRED": cred, "MOVE": move, "DXY": dxy})
    # business-day grid, ffill within each series across small gaps, then common-sample inner join
    raw = raw.sort_index()
    raw = raw[~raw.index.duplicated(keep="last")]
    return raw

def build_panel(raw: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    # ffill small gaps (holidays differ across feeds) up to 3 days, then drop rows lacking any axis
    filled = raw.ffill(limit=3)
    common = filled.dropna()
    start, end = common.index.min(), common.index.max()
    # oriented expanding-z on the COMMON sample (point-in-time within the common window)
    zo = pd.DataFrame(index=common.index)
    for name, meta in AXES.items():
        zo[name] = AXES[name]["orient"] * expanding_z(common[name])
    comp_eqw = zo.mean(axis=1, skipna=False)  # require all 4 present (post-warmup)
    pc1, load_trace = expanding_pca1(zo, align_to=comp_eqw)
    state_eqw = expanding_tercile_state(comp_eqw)
    state_pca = expanding_tercile_state(pc1)
    panel = pd.DataFrame({
        "zVIX": zo["VIX"], "zCRED": zo["CRED"], "zMOVE": zo["MOVE"], "zDXY": zo["DXY"],
        "composite_eqw": comp_eqw, "composite_pca1": pc1,
        "state_eqw": state_eqw, "state_pca1": state_pca,
    })
    cov = {
        "common_start": str(start.date()), "common_end": str(end.date()),
        "n_common_rows": int(len(common)),
        "warmup": WARMUP,
        "n_states_emitted_eqw": int(state_eqw.notna().sum()),
        "first_state_date": str(state_eqw.dropna().index.min().date()) if state_eqw.notna().any() else None,
        "per_axis_raw_span": {c: [str(raw[c].dropna().index.min().date()),
                                  str(raw[c].dropna().index.max().date()),
                                  int(raw[c].notna().sum())] for c in raw.columns},
        "binding_axis": min(raw.columns, key=lambda c: raw[c].dropna().index.min()) if len(raw) else None,
        "state_counts_eqw": {k: int(v) for k, v in state_eqw.value_counts().items()},
        "loading_trace_rows": int(len(load_trace)),
    }
    return panel, cov

# ───────────────────────────── self-tests (no network) ──
def _selftest():
    rng = np.random.default_rng(0)
    n = 1000
    idx = pd.bdate_range("2010-01-01", periods=n)

    # 1) expanding_z is point-in-time: z at t must equal a recomputation using ONLY x[:t+1]
    x = pd.Series(rng.standard_normal(n).cumsum() + 50, index=idx)
    z = expanding_z(x, warmup=50)
    for t in (60, 300, 999):
        sub = x.iloc[: t + 1]
        manual = (x.iloc[t] - sub.mean()) / sub.std(ddof=1)
        assert abs(z.iloc[t] - manual) < 1e-9, f"expanding_z leak at t={t}"
    assert z.iloc[:49].isna().all(), "warmup not respected"

    # 2) future data must NOT change a past z (no look-ahead)
    x2 = x.copy(); x2.iloc[500:] += 999.0
    z2 = expanding_z(x2, warmup=50)
    assert np.allclose(z.iloc[:500].values, z2.iloc[:500].values, equal_nan=True), "future leaked into past z"

    # 3) expanding tercile state is point-in-time and uses only past+current
    comp = pd.Series(rng.standard_normal(n), index=idx)
    st = expanding_tercile_state(comp, warmup=50)
    for t in (200, 700):
        sub = comp.iloc[: t + 1]
        q33, q67 = sub.quantile(1 / 3), sub.quantile(2 / 3)
        exp = "off" if comp.iloc[t] >= q67 else ("on" if comp.iloc[t] <= q33 else "neutral")
        assert st.iloc[t] == exp, f"state mismatch t={t}: {st.iloc[t]} vs {exp}"
    comp2 = comp.copy(); comp2.iloc[600:] += 50
    st2 = expanding_tercile_state(comp2, warmup=50)
    assert (st.iloc[:600].fillna("_") == st2.iloc[:600].fillna("_")).all(), "future leaked into past state"

    # 4) tercile partition is ~1/3 each over the emitted region
    vc = st.dropna().value_counts(normalize=True)
    assert all(abs(vc.get(k, 0) - 1 / 3) < 0.06 for k in ("on", "neutral", "off")), f"terciles off-balance {dict(vc)}"

    # 5) expanding PCA-1 sign-alignment + point-in-time (no future leak in projection)
    zmat = pd.DataFrame({c: expanding_z(pd.Series(rng.standard_normal(n).cumsum(), index=idx), 50)
                         for c in ["a", "b", "c", "d"]}).dropna()
    ew = zmat.mean(axis=1)
    pc1, lt = expanding_pca1(zmat, warmup=50, stride=5, align_to=ew)
    ok = pc1.dropna()
    assert len(ok) > 100 and np.corrcoef(ok.values, ew.loc[ok.index].values)[0, 1] > 0, "PCA sign-align failed"
    print("panel.py self-tests PASS (point-in-time expanding-z, tercile state, no-look-ahead, PCA-1 align)")

# ───────────────────────────── main ──
if __name__ == "__main__":
    if "--selftest" in sys.argv:
        _selftest(); sys.exit(0)
    raw = fetch_raw()
    panel, cov = build_panel(raw)
    panel.to_csv(HERE / "panel.csv")
    (HERE / "coverage.json").write_text(json.dumps(cov, indent=2))
    print(json.dumps(cov, indent=2))
    print(f"\nwrote {HERE/'panel.csv'} ({len(panel)} rows) and coverage.json")
    print("\nstate head/tail (eqw):")
    s = panel["state_eqw"].dropna()
    print("  first:", s.index.min().date(), "last:", s.index.max().date(), "n:", len(s))
