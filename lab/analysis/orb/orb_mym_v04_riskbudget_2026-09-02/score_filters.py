"""Stage B — day-level lift + enumerated circular-shift null for every look in
PREREG_filters.md (primary P1 + exploratory). Sizing rules (P2/P3) are summarized
descriptively here; their decision test is the engine (bust_engine.py)."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
from feat_lib import day_frame

OUT = Path(__file__).resolve().parent
m = day_frame()
s = m[m.scorable].sort_index().copy()
n = len(s)
y = s["pnl_pc"].to_numpy(float)          # per-contract day P&L
print(f"scorable days n={n}  ({s.index.min().date()}..{s.index.max().date()})  hot={int(s.hot.sum())}")


def shift_null(keep: np.ndarray, y: np.ndarray, one_sided: str | None):
    """lift = mean(y|keep) - mean(y|drop); enumerated circular rotations of `keep`.
    one_sided: 'pos' (kept>dropped), 'neg', or None (two-sided)."""
    keep = keep.astype(int); n = len(keep)
    if keep.sum() in (0, n):
        return np.nan, np.nan, int(keep.sum())
    obs = y[keep == 1].mean() - y[keep == 0].mean()
    lifts = np.empty(n)
    for k in range(n):
        r = np.roll(keep, k)
        lifts[k] = y[r == 1].mean() - y[r == 0].mean()
    if one_sided == "pos":
        p = float((lifts >= obs).mean())
    elif one_sided == "neg":
        p = float((lifts <= obs).mean())
    else:
        p = float((np.abs(lifts) >= abs(obs)).mean())
    return float(obs), p, int(keep.sum())


def summary(mask_keep: np.ndarray, scale: np.ndarray | None = None):
    v = y * (scale if scale is not None else mask_keep.astype(float))
    kept = v[mask_keep.astype(bool)] if scale is None else v
    eq = np.cumsum(v); dd = float((np.maximum.accumulate(eq) - eq).max())
    net = float(v.sum()); gw = float(v[v > 0].sum()); gl = float(-v[v < 0].sum())
    pf = gw / gl if gl > 0 else np.inf
    sharpe = float(v.mean() / v.std()) if v.std() > 0 else np.nan
    return dict(net=round(net), pf=round(pf, 3), maxdd=round(dd), rf=round(net / dd, 2) if dd else np.inf,
                worst=round(float(v.min())), sharpe_d=round(sharpe, 4), n_days=int((v != 0).sum()))


rows = []
base = summary(np.ones(n, dtype=int))
rows.append(dict(look="BASE (qty-normalized, common window)", kind="base", **base))


def add(look, kind, keep, one_sided):
    obs, p, nk = shift_null(keep, y, one_sided)
    d = summary(keep.astype(int))
    rows.append(dict(look=look, kind=kind, lift=round(obs, 1) if obs == obs else np.nan, p_shift=p,
                     side=one_sided or "two", kept=nk, **d))


bt = s["base_time_min"].to_numpy(float)
# ---- PRIMARY P1
add("P1 skip base entry after 11:00", "PRIMARY", (bt <= 660).astype(int), "pos")
# ---- exploratory
for cut, lab in ((630, "10:30"), (690, "11:30"), (720, "12:00"), (780, "13:00")):
    add(f"  P1-sens skip after {lab}", "explor", (bt <= cut).astype(int), "pos")
bp = s["bprime"].to_numpy(float)
add("bprime keep (yday RTH range elevated)", "explor", (bp == 1).astype(int), None)
add("bprime drop (keep calm-history days)", "explor", (bp == 0).astype(int), None)
hot = s["hot"].to_numpy(int); gap = s["gap_elev80"].to_numpy(float)
add("NotHot & gap>=P80 keep (else drop) [ledger calm-stratum]", "explor", ((hot == 0) & (gap == 1)).astype(int), "pos")
owa = s["or_width_atr"].to_numpy(float); med = np.nanmedian(owa)
add("keep narrow OR (ORR/ATR <= median)", "explor", (owa <= med).astype(int), None)
add("keep wide OR (ORR/ATR > median)", "explor", (owa > med).astype(int), None)
vt = s["or0930_vol_tod"].to_numpy(float)
add("09:30-bar volume ToD-ratio > 1 keep (~existing knob @1.0x)", "explor", (vt > 1).astype(int), "pos")
add("Hot-only", "explor", hot, None)
add("NotHot-only", "explor", 1 - hot, None)
dow = s["dow"].to_numpy(int)
for d, lab in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri"]):
    add(f"drop {lab}", "explor(DoW)", (dow != d).astype(int), None)
onr = s["on_ret"].to_numpy(float); pr = s["prev_rth_ret"].to_numpy(float)
add("RAISED-BAR: keep overnight-return >= 0", "explor(dir)", (onr >= 0).astype(int), None)
add("RAISED-BAR: keep overnight-return < 0", "explor(dir)", (onr < 0).astype(int), None)
add("RAISED-BAR: keep prev-day RTH up", "explor(dir)", (pr >= 0).astype(int), None)
add("RAISED-BAR: keep prev-day RTH down", "explor(dir)", (pr < 0).astype(int), None)
clv = s["prev_clv"].to_numpy(float); cm = np.nanmedian(clv)
add("keep prev-day CLV >= median (closed high)", "explor", (clv >= cm).astype(int), None)
add("keep prev-day CLV < median (closed low)", "explor", (clv < cm).astype(int), None)

# ---- sizing rules, descriptive only (decision = engine)
wide = s["orr_wide"].to_numpy(int)
for look, sc in (("P2 Hot days x0.5 (descriptive)", np.where(hot == 1, 0.5, 1.0)),
                 ("P3 wide-OR days x0.5 (descriptive)", np.where(wide == 1, 0.5, 1.0))):
    d = summary(np.ones(n, dtype=int), scale=sc)
    rows.append(dict(look=look, kind="PRIMARY-sizing", kept=int((sc == 1).sum()), **d))

res = pd.DataFrame(rows)
cols = ["look", "kind", "kept", "n_days", "lift", "p_shift", "side", "net", "pf", "maxdd", "rf", "worst", "sharpe_d"]
res = res.reindex(columns=cols)
pd.set_option("display.width", 200)
print(res.to_string(index=False))
res.to_csv(OUT / "score_filters_results.csv", index=False)
print("\nBonferroni (K_primary=3): alpha=0.0167 | exploratory looks:", int((res.kind.str.startswith("explor")).sum()))
print(f"\nHot vs NotHot per-contract day P&L: mean {y[hot==1].mean():.1f} vs {y[hot==0].mean():.1f}; "
      f"sd {y[hot==1].std():.1f} vs {y[hot==0].std():.1f}; wide-OR share {wide.mean():.3f}; "
      f"P(wide|hot)={wide[hot==1].mean():.3f} P(wide|nothot)={wide[hot==0].mean():.3f}")
