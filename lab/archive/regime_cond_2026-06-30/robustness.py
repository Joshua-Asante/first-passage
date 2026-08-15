"""Q-REGIME-COND-1 (re-scoped) — POST-FREEZE robustness battery (brief §2.7).

Block-bootstrap CIs + block-shuffle placebo + drop-one-axis jackknife + subperiod stability +
Westfall-Young multiplicity discount over the pre-registered 4-test primary family
(eqw composite x residual states x {5d,20d} x {SEP_vol, SEP_cvar}). iid bootstrap forbidden (§5 #7).

Run:  python robustness.py     # writes robustness_results.json, prints summary
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

from panel import expanding_z, expanding_tercile_state, AXES, fetch_raw, build_panel
from conditional import (spy_logret, fwd_window_stats, expanding_ols_residual, full_sample_residual,
                         RV_WIN, HORIZONS)

HERE = Path(__file__).resolve().parent
BLOCK = 21          # trading-day circular block (matches preregistration §6)
B = 2000
SEED = 20260630
PRIMARY_HZ = [5, 20]


# ───────────────────────────── core separation stat (non-overlapping stride-h) ──
def _cvar5(x: np.ndarray) -> float:
    if len(x) < 5:
        return np.nan
    s = np.sort(x); k = max(1, int(np.ceil(0.05 * len(x))))
    return float(np.mean(s[:k]))


def sep_nonoverlap(state: np.ndarray, fwd: np.ndarray, h: int) -> dict:
    """SEP_vol/SEP_cvar (off-on) on non-overlapping stride-h buckets + monotonicity."""
    idx = np.arange(0, len(state), h)
    st, fw = state[idx], fwd[idx]
    m = np.isfinite(fw) & (st != None)  # noqa: E711
    st, fw = st[m], fw[m]
    def grp(lbl):
        return fw[st == lbl]
    o, ne, on = grp("off"), grp("neutral"), grp("on")
    if len(o) < 10 or len(on) < 10:
        return dict(SEP_vol=np.nan, SEP_cvar=np.nan, mono_vol=False, mono_cvar=False, n_off=len(o), n_on=len(on))
    sv = np.std(o, ddof=1) - np.std(on, ddof=1)
    sc = abs(_cvar5(o)) - abs(_cvar5(on))
    mono_v = bool(np.std(o, ddof=1) > np.std(ne, ddof=1) > np.std(on, ddof=1)) if len(ne) >= 10 else False
    mono_c = bool(abs(_cvar5(o)) > abs(_cvar5(ne)) > abs(_cvar5(on))) if len(ne) >= 10 else False
    return dict(SEP_vol=float(sv), SEP_cvar=float(sc), mono_vol=mono_v, mono_cvar=mono_c,
                n_off=int(len(o)), n_on=int(len(on)))


def aligned(states: pd.Series, fwdstats: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    df = pd.DataFrame({"state": states}).join(fwdstats["fwd"], how="inner")
    df = df.dropna(subset=["fwd"])
    df = df[df["state"].notna()]
    return df["state"].to_numpy(object), df["fwd"].to_numpy(float)


# ───────────────────────────── block shuffle / resample ──
def block_permute(n: int, rng) -> np.ndarray:
    """Indices for a circular block permutation (preserves autocorrelation, ~exact marginal)."""
    start = int(rng.integers(n))
    roll = np.concatenate([np.arange(start, n), np.arange(0, start)])
    nb = int(np.ceil(n / BLOCK))
    blocks = [roll[i * BLOCK:(i + 1) * BLOCK] for i in range(nb)]
    order = rng.permutation(nb)
    out = np.concatenate([blocks[i] for i in order])[:n]
    return out


def block_resample(n: int, rng) -> np.ndarray:
    """Indices for a circular block bootstrap with replacement."""
    out = []
    while len(out) < n:
        s = int(rng.integers(n))
        out.extend(((s + np.arange(BLOCK)) % n).tolist())
    return np.array(out[:n])


# ───────────────────────────── battery ──
def placebo_and_multiplicity(states: pd.Series, fwd: dict, rng) -> dict:
    """Block-shuffle state labels; real SEP must beat 95th pct. WY max-stat across the
    4-test primary family (residual x {5,20} x {vol,cvar})."""
    aln = {h: aligned(states, fwd[h]) for h in PRIMARY_HZ}
    real = {h: sep_nonoverlap(aln[h][0], aln[h][1], h) for h in PRIMARY_HZ}
    tests = [(h, m) for h in PRIMARY_HZ for m in ("SEP_vol", "SEP_cvar")]
    null = {t: np.empty(B) for t in tests}
    for b in range(B):
        for h in PRIMARY_HZ:
            st, fw = aln[h]
            perm = block_permute(len(st), rng)
            d = sep_nonoverlap(st[perm], fw, h)
            for m in ("SEP_vol", "SEP_cvar"):
                null[(h, m)][b] = d[m]
    # scale-fair Westfall-Young: standardize each test by its OWN placebo SD before the max,
    # so the larger-scale metric (cvar ~0.03) doesn't dominate the smaller (vol ~0.01).
    sigma = {t: float(np.nanstd(null[t])) or 1.0 for t in tests}
    maxnull_std = np.full(B, -np.inf)
    for t in tests:
        z = np.where(np.isfinite(null[t]), null[t] / sigma[t], -np.inf)
        maxnull_std = np.maximum(maxnull_std, z)
    out = {}
    for (h, m) in tests:
        r = real[h][m]
        nd = null[(h, m)][np.isfinite(null[(h, m)])]
        pct = float((nd < r).mean() * 100) if len(nd) else np.nan          # 1-sided percentile of real
        zr = r / sigma[(h, m)] if np.isfinite(r) else np.nan
        p_fwer = float((maxnull_std >= zr).mean()) if np.isfinite(zr) else np.nan  # WY scale-fair
        out[f"{h}d_{m}"] = dict(real=round(r, 5), placebo_pct=round(pct, 1),
                                p_fwer=round(p_fwer, 4), mono=real[h]["mono_vol"] if m == "SEP_vol" else real[h]["mono_cvar"],
                                beats_95=bool(pct >= 95), n_off=real[h]["n_off"], n_on=real[h]["n_on"])
    return out


def bootstrap_ci(states: pd.Series, fwd: dict, rng) -> dict:
    out = {}
    for h in PRIMARY_HZ:
        st, fw = aligned(states, fwd[h])
        n = len(st)
        sv = np.empty(B); sc = np.empty(B)
        for b in range(B):
            idx = block_resample(n, rng)
            d = sep_nonoverlap(st[idx], fw[idx], h)
            sv[b] = d["SEP_vol"]; sc[b] = d["SEP_cvar"]
        sv = sv[np.isfinite(sv)]; sc = sc[np.isfinite(sc)]
        out[f"{h}d"] = dict(
            SEP_vol_ci=[round(float(np.percentile(sv, 5)), 5), round(float(np.percentile(sv, 50)), 5), round(float(np.percentile(sv, 95)), 5)],
            SEP_cvar_ci=[round(float(np.percentile(sc, 5)), 5), round(float(np.percentile(sc, 50)), 5), round(float(np.percentile(sc, 95)), 5)],
            vol_ci_excludes_0=bool(np.percentile(sv, 5) > 0 or np.percentile(sv, 95) < 0),
            cvar_ci_excludes_0=bool(np.percentile(sc, 5) > 0 or np.percentile(sc, 95) < 0),
        )
    return out


def jackknife_axes(comp_inputs: pd.DataFrame, rv_on_panel: pd.Series, fwd: dict) -> dict:
    """Drop each axis; rebuild eqw composite -> residual states -> SEP at primary horizons."""
    out = {}
    zo = pd.DataFrame({n: AXES[n]["orient"] * expanding_z(comp_inputs[n]) for n in AXES})
    for drop in list(AXES):
        keep = [c for c in AXES if c != drop]
        comp = zo[keep].mean(axis=1, skipna=False)
        resid = expanding_ols_residual(comp, rv_on_panel).reindex(comp.index)
        rstates = expanding_tercile_state(resid)
        out[f"drop_{drop}"] = {f"{h}d": {k: sep_nonoverlap(*aligned(rstates, fwd[h]), h)[k]
                                          for k in ("SEP_vol", "SEP_cvar", "mono_vol")} for h in PRIMARY_HZ}
    return out


def subperiods(states_resid: pd.Series, fwd: dict) -> dict:
    out = {}
    masks = {
        "2009-2017": lambda d: d < pd.Timestamp("2018-01-01"),
        "2018-2026": lambda d: d >= pd.Timestamp("2018-01-01"),
        "covid_out": lambda d: ~((d >= pd.Timestamp("2020-02-01")) & (d <= pd.Timestamp("2020-06-30"))),
    }
    for name, fn in masks.items():
        sub = states_resid[fn(states_resid.index)]
        out[name] = {f"{h}d": {k: sep_nonoverlap(*aligned(sub, fwd[h]), h)[k]
                                for k in ("SEP_vol", "SEP_cvar", "mono_vol", "n_off", "n_on")} for h in PRIMARY_HZ}
    return out


def main():
    rng = np.random.default_rng(SEED)
    panel = pd.read_csv(HERE / "panel.csv", index_col=0, parse_dates=True)
    raw = fetch_raw()                      # for jackknife axis inputs (common-sample)
    filled = raw.ffill(limit=3).dropna()
    logret, _ = spy_logret()
    rv = logret.rolling(RV_WIN).std()
    comp = panel["composite_eqw"]
    rv_on_panel = rv.reindex(comp.index)

    resid_pit = expanding_ols_residual(comp, rv_on_panel).reindex(comp.index)
    resid_pca = expanding_ols_residual(panel["composite_pca1"], rv_on_panel).reindex(comp.index)
    states_raw = panel["state_eqw"]
    states_resid = expanding_tercile_state(resid_pit)
    states_resid_pca = expanding_tercile_state(resid_pca)  # SECONDARY composite (closes §7 Pass-D gap)
    fwd = {h: fwd_window_stats(logret, h) for h in HORIZONS}

    res = {
        "config": dict(block=BLOCK, B=B, seed=SEED, primary_family="eqw x residual x {5,20}d x {vol,cvar}"),
        "placebo_multiplicity_RESIDUAL": placebo_and_multiplicity(states_resid, fwd, np.random.default_rng(SEED)),
        "placebo_multiplicity_RAW_context": placebo_and_multiplicity(states_raw, fwd, np.random.default_rng(SEED + 1)),
        "bootstrap_ci_RESIDUAL": bootstrap_ci(states_resid, fwd, np.random.default_rng(SEED + 2)),
        "bootstrap_ci_RAW_context": bootstrap_ci(states_raw, fwd, np.random.default_rng(SEED + 3)),
        "jackknife_axes_RESIDUAL": jackknife_axes(filled, rv_on_panel, fwd),
        "subperiods_RESIDUAL": subperiods(states_resid, fwd),
        # SECONDARY composite (PCA-1) residual — NOT in the primary multiplicity family; closes §7 Pass-D gap
        "placebo_multiplicity_RESIDUAL_PCA1_secondary": placebo_and_multiplicity(states_resid_pca, fwd, np.random.default_rng(SEED + 4)),
        "bootstrap_ci_RESIDUAL_PCA1_secondary": bootstrap_ci(states_resid_pca, fwd, np.random.default_rng(SEED + 5)),
        "subperiods_RESIDUAL_PCA1_secondary": subperiods(states_resid_pca, fwd),
    }
    (HERE / "robustness_results.json").write_text(json.dumps(res, indent=2))

    print("=== PLACEBO + MULTIPLICITY (RESIDUAL states; primary family) ===")
    print(f"{'test':14} {'real':>9} {'placebo_pct':>11} {'p_FWER':>7} {'mono':>5} {'beats95':>7}")
    for k, v in res["placebo_multiplicity_RESIDUAL"].items():
        print(f"{k:14} {v['real']:>+9.5f} {v['placebo_pct']:>11} {v['p_fwer']:>7} {str(v['mono']):>5} {str(v['beats_95']):>7}")
    print("\n  (RAW context, for comparison)")
    for k, v in res["placebo_multiplicity_RAW_context"].items():
        print(f"  {k:14} real={v['real']:>+9.5f} placebo_pct={v['placebo_pct']:>5} p_FWER={v['p_fwer']:>6} mono={v['mono']}")
    print("\n=== BLOCK-BOOTSTRAP CIs (RESIDUAL) [5,50,95] ===")
    for h, v in res["bootstrap_ci_RESIDUAL"].items():
        print(f"  {h}: SEP_vol {v['SEP_vol_ci']} excl0={v['vol_ci_excludes_0']} | SEP_cvar {v['SEP_cvar_ci']} excl0={v['cvar_ci_excludes_0']}")
    print("\n=== DROP-ONE-AXIS JACKKNIFE (RESIDUAL SEP_vol) ===")
    for k, v in res["jackknife_axes_RESIDUAL"].items():
        print(f"  {k}: 5d={v['5d']['SEP_vol']:+.5f}(mono {v['5d']['mono_vol']}) 20d={v['20d']['SEP_vol']:+.5f}(mono {v['20d']['mono_vol']})")
    print("\n=== SUBPERIODS (RESIDUAL SEP_vol / mono) ===")
    for k, v in res["subperiods_RESIDUAL"].items():
        print(f"  {k:10}: 5d={v['5d']['SEP_vol']:+.5f}(mono {v['5d']['mono_vol']},n_off {v['5d']['n_off']}) "
              f"20d={v['20d']['SEP_vol']:+.5f}(mono {v['20d']['mono_vol']})")
    print("\n=== SECONDARY: RESIDUAL-PCA1 composite (closes §7 Pass-D gap; NOT in primary family) ===")
    for k, v in res["placebo_multiplicity_RESIDUAL_PCA1_secondary"].items():
        ci = res["bootstrap_ci_RESIDUAL_PCA1_secondary"]
        print(f"  {k:14} real={v['real']:>+9.5f} placebo_pct={v['placebo_pct']:>5} p_FWER={v['p_fwer']:>6} mono={v['mono']} beats95={v['beats_95']}")
    for h in PRIMARY_HZ:
        c = res["bootstrap_ci_RESIDUAL_PCA1_secondary"][f"{h}d"]
        sp = res["subperiods_RESIDUAL_PCA1_secondary"]
        print(f"  {h}d CI SEP_vol {c['SEP_vol_ci']} excl0={c['vol_ci_excludes_0']} | subperiod 2009-2017 {sp['2009-2017'][f'{h}d']['SEP_vol']:+.4f} vs 2018-2026 {sp['2018-2026'][f'{h}d']['SEP_vol']:+.4f} | covid_out {sp['covid_out'][f'{h}d']['SEP_vol']:+.4f}")

    print("\nwrote robustness_results.json")


if __name__ == "__main__":
    main()
