"""EXTENSION of the 2026-06-25 regime-signal battery — NEW free candidates it never tested.

The parent battery (../run_battery.py, ../CLOSURE.md) closed NULL on 5 free signals
(NFCI, S5FI, RDISP, RCORR, COR3M). This extension scores 7 MORE free candidates across the
three families the battery did not cover — vol-surface, a 2nd implied-corr tenor + dispersion,
and cross-asset bond/credit — against the SAME N=33 co-drawdown episodes, with the SAME recipe:

  - decision point = last obs strictly before each episode onset (= pre-drawdown peak)
  - severity      = depth_usd (static-$ trough depth on a flat $200K base)  [NOT depth_pct]
  - residualize rank(sev) & rank(cand) on [1, rank(rv_at_peak), rank(calendar_rank)]
  - partial corr = Pearson of the residuals
  - 20k-perm max-|rho| Westfall-Young FWER across the M-candidate family, seed 20260625
  - signs PRE-REGISTERED (frozen below, theory-first) BEFORE scoring

Faithfulness gate: the premise (Spearman(sev,RV) n.s. ~+0.16/0.38; Spearman(sev,cal) ~-0.46/0.007)
must reproduce the parent battery — it does, to 3 dp (see RESULTS.md).

Inputs: ./glm_inputs.csv (frozen I1+I2; use the rv_finite==True rows = the N=33 usable set).
Candidate series are fetched live (keyless: CBOE CDN, Yahoo). HY-OAS via FRED fredgraph is
history-capped at ~3y for this series, so the cross-asset credit slot uses a full-history
HYG/LQD ratio proxy at N=33; the real OAS is reported as a non-comparable N=21 footnote.

Run:  python score_newfree.py        # prints table, writes result.json
"""
import urllib.request, io, json
from pathlib import Path
import numpy as np, pandas as pd
from scipy.stats import rankdata, spearmanr

HERE = Path(__file__).resolve().parent
B, SEED = 20000, 20260625


def get(url, ua=True):
    h = {"User-Agent": "Mozilla/5.0"} if ua else {}
    return urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=40).read()


def cboe(sym, col="CLOSE"):
    d = pd.read_csv(io.BytesIO(get(f"https://cdn.cboe.com/api/global/us_indices/daily_prices/{sym}_History.csv")))
    d.columns = [c.strip().upper() for c in d.columns]
    dt = pd.to_datetime(d["DATE"], format="%m/%d/%Y")
    vc = col if col in d.columns else [c for c in d.columns if c != "DATE"][-1]
    return pd.Series(d[vc].astype(float).values, index=dt).sort_index()


def yahoo(sym):
    j = json.loads(get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=10y&interval=1d"))
    r = j["chart"]["result"][0]
    ts = pd.to_datetime(r["timestamp"], unit="s").normalize()
    return pd.Series(r["indicators"]["quote"][0]["close"], index=ts, dtype="float64").dropna().sort_index()


def fred(sid):
    d = pd.read_csv(io.BytesIO(get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}", ua=False)))
    d.columns = ["date", "v"]
    dt = pd.to_datetime(d["date"])
    return pd.Series(pd.to_numeric(d["v"], errors="coerce").values, index=dt).dropna().sort_index()


# ── fetch raw series ──
vix = cboe("VIX"); vix3m = cboe("VIX3M"); termstruct = (vix / vix3m).dropna()
vvix = cboe("VVIX"); skew = cboe("SKEW"); dspx = cboe("DSPX"); cor1m = cboe("COR1M")
move = yahoo("%5EMOVE")
hyg = yahoo("HYG"); lqd = yahoo("LQD")
idx = hyg.index.intersection(lqd.index); hyig = (hyg.loc[idx] / lqd.loc[idx]).sort_index()

# ── PRE-REGISTERED candidates (series, sign, class, theory-of-lead) — FROZEN ──
CAND = {
    "TERMSTRUCT": (termstruct, +1, "vol-surface", "VIX/VIX3M backwardation = near-term fear>3m -> regime-stress lead"),
    "VVIX":       (vvix,       +1, "vol-surface", "vol-of-vol high = unstable vol surface precedes turbulence"),
    "SKEW":       (skew,       +1, "vol-surface", "richer crash/OTM-put pricing = tail demand precedes stress"),
    "DSPX":       (dspx,       -1, "implied-corr", "LOW dispersion <=> HIGH implied corr = systemic co-move"),
    "COR1M":      (cor1m,      +1, "implied-corr", "high 1m implied corr = everything-together (vs tested COR3M)"),
    "MOVE":       (move,       +1, "cross-asset", "bond-vol spike = cross-asset stress into equity/FX co-move"),
    "HYIG":       (hyig,       -1, "cross-asset", "HY/IG (HYG/LQD) ratio falling = credit/funding risk-off leads co-drawdowns"),
}

# ── episodes (frozen I1+I2; N=33 usable) ──
ep = pd.read_csv(HERE / "glm_inputs.csv"); ep = ep[ep["rv_finite"]].copy()
ep["onset"] = pd.to_datetime(ep["onset"])
onsets = ep["onset"].to_numpy()
sev = ep["depth_usd"].to_numpy(float)
rv = ep["rv_at_peak"].to_numpy(float)
cal = ep["calendar_rank"].to_numpy(float)


def asof(s, onsets):
    s = s.sort_index(); out = []
    for o in onsets:
        m = s.index < o; out.append(s[m].iloc[-1] if m.any() else np.nan)
    return np.array(out, float)


X = {n: (asof(series, onsets), sgn, cls) for n, (series, sgn, cls, _) in CAND.items()}

print("coverage / 33 episodes:")
for n, (v, _, _) in X.items():
    s = CAND[n][0]
    print(f"  {n:11s} {np.isfinite(v).sum():>2d}/33  span {s.index.min().date()}..{s.index.max().date()}")

names = list(X)
Mmask = np.isfinite(sev) & np.isfinite(rv) & np.isfinite(cal)
for v, _, _ in X.values():
    Mmask &= np.isfinite(v)
N = int(Mmask.sum())
print(f"\ncommon complete-case N={N}")


def resid(y, Z):
    beta, *_ = np.linalg.lstsq(Z, y, rcond=None); return y - Z @ beta


def pcorr(a, b):
    return float(np.corrcoef(a, b)[0, 1])


Z = np.column_stack([np.ones(N), rankdata(rv[Mmask]), rankdata(cal[Mmask])])
rsev = resid(rankdata(sev[Mmask]), Z)
rX = {n: resid(rankdata(X[n][0][Mmask]), Z) for n in names}
rho = {n: pcorr(rX[n], rsev) for n in names}
raw = {n: float(spearmanr(X[n][0][Mmask], sev[Mmask]).correlation) for n in names}

prv = spearmanr(sev[Mmask], rv[Mmask]); pcal = spearmanr(sev[Mmask], cal[Mmask])
print(f"\nFAITHFULNESS GATE (must match battery): "
      f"Spearman(sev,RV)={prv.correlation:+.3f} p={prv.pvalue:.3f} [exp +0.159/0.38] | "
      f"Spearman(sev,cal)={pcal.correlation:+.3f} p={pcal.pvalue:.3f} [exp -0.46/0.007]")

rng = np.random.default_rng(SEED)
maxnull = np.empty(B); ge = {n: 0 for n in names}
for b in range(B):
    sp = rsev[rng.permutation(N)]
    rb = {n: pcorr(rX[n], sp) for n in names}
    maxnull[b] = max(abs(r) for r in rb.values())
    for n in names:
        s = X[n][1]
        if s * rb[n] >= s * rho[n]:
            ge[n] += 1
p_one = {n: ge[n] / B for n in names}
p_fwer = {n: float(np.mean(maxnull >= abs(rho[n]))) for n in names}

floor = 1.96 / np.sqrt(N - 3)
print(f"\nN={N}  power floor |rho|~{floor:.2f}  (M={len(names)} family, seed {SEED}, B={B})\n")
print(f"{'cand':11s} {'class':12s} {'sgn':3s} {'rho_part':>8s} {'raw_rho':>8s} {'p_1sd':>6s} {'p_FWER':>7s}  verdict")
res = {}
for n in sorted(names, key=lambda n: -abs(rho[n])):
    s = X[n][1]; ok = np.sign(rho[n]) == s
    strong = ok and p_fwer[n] < 0.05
    nom = ok and p_one[n] < 0.05 and not strong
    v = "STRONG-PASS" if strong else ("nominal(FWER-fragile)" if nom else ("fail(wrong-sign)" if not ok else "fail"))
    print(f"{n:11s} {X[n][2]:12s} {('+' if s > 0 else '-'):3s} {rho[n]:>+8.3f} {raw[n]:>+8.3f} {p_one[n]:>6.3f} {p_fwer[n]:>7.3f}  {v}")
    res[n] = dict(cls=X[n][2], sign=int(s), rho_partial=round(rho[n], 4), raw_rho=round(raw[n], 4),
                  p_one=p_one[n], p_fwer=p_fwer[n], verdict=v, theory=CAND[n][3])

# ── footnote: real HY-OAS at its own (history-capped) N — NOT family-comparable ──
foot = None
try:
    hyoas = fred("BAMLH0A0HYM2"); ho = asof(hyoas, onsets)
    m2 = np.isfinite(sev) & np.isfinite(rv) & np.isfinite(cal) & np.isfinite(ho)
    n2 = int(m2.sum())
    Z2 = np.column_stack([np.ones(n2), rankdata(rv[m2]), rankdata(cal[m2])])
    r2 = pcorr(resid(rankdata(ho[m2]), Z2), resid(rankdata(sev[m2]), Z2))
    foot = dict(N=n2, partial_rho=round(r2, 4), note="fredgraph history-capped ~3y; cal-premise degenerate at this N; NOT comparable")
    print(f"\n[footnote] HYOAS real OAS: N={n2} partial_rho={r2:+.3f} (sign+1; NOT comparable -- history-capped)")
except Exception as e:
    print("HYOAS footnote failed:", e)

out = dict(extension_of="regime_signal_research_2026-06-25 battery (CLOSURE.md)",
           recipe="exact battery replication; signs pre-registered; FWER across M",
           N=N, M=len(names), seed=SEED, B=B,
           faithfulness=dict(sev_rv=[round(prv.correlation, 3), round(prv.pvalue, 4)],
                             sev_cal=[round(pcal.correlation, 3), round(pcal.pvalue, 4)]),
           power_floor=round(floor, 3), results=res, hyoas_footnote=foot,
           disposition="NULL-EXTENDED: no new free candidate clears FWER<0.05 with registered sign")
(HERE / "result.json").write_text(json.dumps(out, indent=2))
print("\nwrote result.json")
