#!/usr/bin/env python3
"""Q-NAS-4 Inquire: does the pyramid-monster 'sign-gate' (absent in negative-index quarters)
hold on the full 4y/196-leg panel, or break with more down quarters?

Ground truth, computed once. Trades = LOCK-anchor 11605 (n=196). Index sign = real Pepperstone
bars (2024-2026, assembled pages) where available + a panel-price proxy (validated on overlap)
for 2022-2023 (real 2022-23 bars not yet on hand).
Characterization-ONLY (belt forbids converting a confirmed gate into any overlay/relock).
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats

REPO = Path(r"C:/Users/joshu/multi_firm_operations/.claude/worktrees/tender-perlman-7824ea")
sys.path.insert(0, str(REPO / "core"))
from bar_export_loader import parse_bar_export  # noqa

DL = Path(r"C:/Users/joshu/Downloads")
PANEL = DL / "Striker_NAS100_v1_PEPPERSTONE_NAS100_2026-05-24_11605.csv"     # LOCK anchor, n=196
BAR_PAGES = [
    DL / "BAR_EXPORT_v0.1_PEPPERSTONE_NAS100_2026-06-20_68113.csv",          # 2024-01 -> 2024-06
    DL / "BAR_EXPORT_v0.1_PEPPERSTONE_NAS100_2026-06-20_f780b.csv",          # 2024-06 -> ...
    DL / "BAR_EXPORT_v0.1_PEPPERSTONE_NAS100_2026-06-20_c64de.csv",          # 2026 page
]
OUT = REPO / "lab" / "analysis" / "q_nas_4_2026-06-20"; OUT.mkdir(parents=True, exist_ok=True)
ACCOUNT = 200_000.0
rng = np.random.default_rng(20260620)
def jr(x, n=4):
    if x is None: return None
    if isinstance(x, (np.floating, np.integer)): x = x.item()
    if isinstance(x, float) and (np.isnan(x) or np.isinf(x)): return None
    return round(x, n)

out = {}

# ---------- 1. PANEL (11605) : reconcile + per-quarter monster tally ----------
df = pd.read_csv(PANEL, encoding="utf-8-sig"); df.columns = [c.strip() for c in df.columns]
tid, pnl, cum, px = "Trade #", "Net P&L USD", "Cumulative P&L USD", "Price USD"
df[tid] = df[tid].astype(int)
en = df[df["Type"].str.startswith("Entry")].copy()
ex = df[df["Type"].str.startswith("Exit")].copy()
legs = en[[tid, "Date and time", "Signal", px]].rename(columns={"Date and time": "edt", "Signal": "esig", px: "epx"}).merge(
    ex[[tid, "Date and time", "Signal", px, pnl]].rename(columns={"Date and time": "xdt", "Signal": "xsig", px: "xpx", pnl: "pnl"}),
    on=tid, how="inner").sort_values(tid).reset_index(drop=True)
legs["leg_type"] = np.where(legs["esig"].str.contains("Add"), "pyramid_add", "base")
legs["edt"] = pd.to_datetime(legs["edt"]); legs["xdt"] = pd.to_datetime(legs["xdt"])
legs["q"] = legs["xdt"].dt.to_period("Q").astype(str)

# reconcile vs LOCK.md (n=196, net 369698.40, PF 3.717, WR 55.61%)
net = legs["pnl"].sum(); wins = legs[legs["pnl"] > 0]; losses = legs[legs["pnl"] <= 0]
pf = wins["pnl"].sum() / abs(losses["pnl"].sum())
out["panel_reconcile"] = {"n_legs": int(len(legs)), "n_base": int((legs.leg_type == "base").sum()),
    "n_add": int((legs.leg_type == "pyramid_add").sum()), "net": jr(net, 2), "pf": jr(pf, 3),
    "wr_pct": jr((legs["pnl"] > 0).mean() * 100, 2),
    "lockmd_target": "n=196 net=369698.40 pf=3.717 wr=55.61",
    "reconciles": bool(len(legs) == 196 and abs(net - 369698.40) < 1.0)}

# monster definitions
legs["is_mh_add"] = (legs["xsig"] == "Max Hold") & (legs["leg_type"] == "pyramid_add")
legs["is_add"] = legs["leg_type"] == "pyramid_add"
legs["is_mh"] = legs["xsig"] == "Max Hold"

# ---------- 2. REAL BARS (assembled) : quarterly index return where available ----------
bars = parse_bar_export(BAR_PAGES, symbol="NAS100"); bars["time"] = pd.to_datetime(bars["time"], utc=True)
bars = bars.sort_values("time").drop_duplicates("time").reset_index(drop=True)
bars["q"] = bars["time"].dt.tz_convert("UTC").dt.to_period("Q").astype(str)
real_q = {}
for q, g in bars.groupby("q"):
    cc = g["close"].to_numpy()
    real_q[q] = (cc[-1] / cc[0] - 1) * 100
out["real_bar_quarters"] = {q: jr(v, 2) for q, v in real_q.items()}
out["real_bar_span"] = f"{bars['time'].min()} -> {bars['time'].max()} (n={len(bars)})"

# ---------- 3. PROXY index return from panel prices (validate on overlap) ----------
# sparse REAL Pepperstone prices at trade times: entry+exit price points, chronological
pts = pd.concat([
    legs[["edt", "epx"]].rename(columns={"edt": "t", "epx": "p"}),
    legs[["xdt", "xpx"]].rename(columns={"xdt": "t", "xpx": "p"}),
]).dropna().sort_values("t")
pts["q"] = pts["t"].dt.to_period("Q").astype(str)
proxy_q = {}
for q, g in pts.groupby("q"):
    if len(g) >= 2:
        # robust: linear regression slope sign over the quarter + first->last return
        x = (g["t"].astype("int64") / 1e9).to_numpy(); x = x - x.mean()
        y = g["p"].to_numpy()
        slope = np.polyfit(x, y, 1)[0]
        proxy_q[q] = {"firstlast_ret_pct": (y[-1] / y[0] - 1) * 100, "slope_sign": int(np.sign(slope)),
                      "n_pts": len(g), "mean_px": float(y.mean())}
# validate proxy vs real on overlap
val = []
for q in sorted(set(real_q) & set(proxy_q)):
    rs = np.sign(real_q[q]); ps = np.sign(proxy_q[q]["firstlast_ret_pct"])
    val.append({"q": q, "real_ret": jr(real_q[q], 2), "proxy_firstlast": jr(proxy_q[q]["firstlast_ret_pct"], 2),
                "proxy_slope_sign": proxy_q[q]["slope_sign"], "real_sign": int(rs), "sign_match": bool(rs == ps)})
out["proxy_validation_overlap"] = val
out["proxy_sign_match_rate"] = f"{sum(v['sign_match'] for v in val)}/{len(val)}"

# ---------- 4. BUILD SIGN-GATE TABLE (real where available, else proxy) ----------
all_q = sorted(set(legs["q"]) | set(proxy_q) | set(real_q))
rows = []
for q in all_q:
    gl = legs[legs["q"] == q]
    if q in real_q:
        idx_ret, src = real_q[q], "real_bar"
    elif q in proxy_q:
        idx_ret, src = proxy_q[q]["firstlast_ret_pct"], "panel_proxy"
    else:
        idx_ret, src = None, "none"
    rows.append({"q": q, "idx_ret_pct": jr(idx_ret, 2), "idx_src": src,
                 "idx_sign": (int(np.sign(idx_ret)) if idx_ret is not None else None),
                 "n_trades": int(len(gl)), "n_base": int((gl.leg_type == "base").sum()),
                 "n_mh_add": int(gl["is_mh_add"].sum()), "n_add": int(gl["is_add"].sum()),
                 "n_mh": int(gl["is_mh"].sum()),
                 "monster_present": bool(gl["is_mh_add"].sum() >= 1),
                 "any_add": bool(gl["is_add"].sum() >= 1),
                 "any_mh": bool(gl["is_mh"].sum() >= 1),
                 "q_net": jr(gl["pnl"].sum(), 2)})
tbl = pd.DataFrame(rows)
tbl.to_csv(OUT / "qnas4_quarter_table.csv", index=False)
out["quarter_table"] = rows

# ---------- 5. SIGN-GATE TEST (primary monster def = Max-Hold pyramid_add) ----------
t = tbl[tbl["idx_sign"].notna()].copy()
neg = t[t["idx_sign"] < 0]; pos = t[t["idx_sign"] > 0]
def gate_stats(col):
    a = int(((pos[col]) ).sum()); b = int((~pos[col]).sum())     # pos: present / absent
    c = int(((neg[col]) ).sum()); d = int((~neg[col]).sum())     # neg: present / absent
    # 2x2: rows=[pos,neg], cols=[present,absent]
    table = [[a, b], [c, d]]
    odds, p_fisher = stats.fisher_exact(table, alternative="greater")  # present more likely in pos
    # permutation: shuffle sign labels, recompute concordance = pos_present + neg_absent
    obs_conc = a + d
    signs = t["idx_sign"].to_numpy(); present = t[col].to_numpy().astype(bool); N = 20000
    perm = np.empty(N)
    for i in range(N):
        s = rng.permutation(signs)
        perm[i] = ((present & (s > 0)).sum()) + ((~present & (s < 0)).sum())
    p_perm = (perm >= obs_conc).mean()
    return {"pos_present": a, "pos_absent": b, "neg_present": c, "neg_absent": d,
            "n_pos": len(pos), "n_neg": len(neg), "concordance": obs_conc, "n_q": len(t),
            "fisher_p_greater": jr(p_fisher, 4), "perm_p": jr(float(p_perm), 4)}
out["gate_primary_mh_add"] = gate_stats("monster_present")
out["gate_robust_any_add"] = gate_stats("any_add")
out["gate_robust_any_mh"] = gate_stats("any_mh")

# confound: is monster-absence in neg quarters just low trade count?
out["confound_trade_freq"] = {
    "median_ntrades_pos": jr(pos["n_trades"].median(), 1),
    "median_ntrades_neg": jr(neg["n_trades"].median(), 1),
    "neg_quarters_detail": neg[["q", "idx_ret_pct", "idx_src", "n_trades", "n_mh_add", "q_net"]].to_dict("records"),
}
# magnitude (not just sign): does monster presence track |ret| or sign?
t2 = t.copy(); t2["abs_ret"] = t2["idx_ret_pct"].abs()
out["confound_magnitude"] = {
    "spearman_absret_vs_monster": jr(stats.spearmanr(t2["abs_ret"], t2["monster_present"].astype(int)).statistic, 3),
    "spearman_signedret_vs_monster": jr(stats.spearmanr(t2["idx_ret_pct"], t2["monster_present"].astype(int)).statistic, 3),
}

with open(OUT / "qnas4_results.json", "w") as f: json.dump(out, f, indent=2)

# ---- console summary ----
print(f"RECONCILE 11605: {out['panel_reconcile']}")
print(f"REAL BAR SPAN: {out['real_bar_span']}")
print(f"PROXY validation (sign match on overlap): {out['proxy_sign_match_rate']}")
for v in val: print("  ", v)
print(f"\nQUARTER TABLE ({len(rows)} quarters):")
print(f"{'q':8s}{'idx_ret':>9s}{'src':>12s}{'sign':>5s}{'ntr':>5s}{'mh_add':>7s}{'monster':>9s}{'q_net':>12s}")
for r in rows:
    print(f"{r['q']:8s}{str(r['idx_ret_pct']):>9s}{r['idx_src']:>12s}{str(r['idx_sign']):>5s}"
          f"{r['n_trades']:>5d}{r['n_mh_add']:>7d}{str(r['monster_present']):>9s}{str(r['q_net']):>12s}")
print(f"\nGATE (Max-Hold pyramid_add): {out['gate_primary_mh_add']}")
print(f"GATE (any pyramid_add):      {out['gate_robust_any_add']}")
print(f"GATE (any Max-Hold):         {out['gate_robust_any_mh']}")
print(f"\nCONFOUND trade-freq: median ntrades pos={out['confound_trade_freq']['median_ntrades_pos']} neg={out['confound_trade_freq']['median_ntrades_neg']}")
print("NEG quarters:")
for d in out['confound_trade_freq']['neg_quarters_detail']: print("  ", d)
print(f"CONFOUND magnitude: {out['confound_magnitude']}")
print(f"\n=== wrote {OUT}")
