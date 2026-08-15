"""FROZEN-SPEC RUN — PREREG-REGIME-CHOP-ORTHOGONALITY v3.1.
Episode-level peak-measured partial-Spearman of 7 candidates vs static-$ co-drawdown
severity, residualized on [at-peak realized vol + episode calendar-rank], 20k-permutation,
max-|rho| Westfall-Young FWER. Signs are pre-registered (frozen). Seed pinned."""
import sys, json, hashlib
from pathlib import Path
import numpy as np, pandas as pd
from scipy.stats import rankdata, spearmanr

REPO = Path(r"C:/Users/joshu/multi_firm_operations")
EXT, BD = REPO/"core/data/external", REPO/"core/data/bar_data"
BE = REPO/"core/data/tv_exports/pepperstone/bar_export"
TMP = Path(r"C:/Temp/claude")
HERE = REPO/"lab/analysis/regime_signal_research_2026-06-25"
B, SEED = 20000, 20260625

# ── episodes (frozen) ──
ep = pd.read_csv(HERE/"episodes_raw.csv"); ep["onset"] = pd.to_datetime(ep["onset"])
onsets = ep["onset"]; sev = ep["depth_usd"].to_numpy(float); cal = ep["calendar_rank"].to_numpy(float)
N0 = len(ep)

def asof(df, onsets):           # last obs strictly before onset (= the pre-drawdown peak day)
    s = df.sort_index()
    return np.array([(s.loc[s.index < o]["v"].iloc[-1] if (s.index < o).any() else np.nan) for o in onsets], float)

def daily_close(path):
    d = pd.read_csv(path); d["t"] = pd.to_datetime(d["time"], utc=True).dt.tz_localize(None); d["date"] = d["t"].dt.normalize()
    return d.groupby("date")["close"].last()

def barexport_close(path):      # S5FI: close = 5th pipe token of Signal; date-only
    d = pd.read_csv(path, encoding="utf-8-sig")
    close = d["Signal"].astype(str).str.split("|").str[4].astype(float)
    date = pd.to_datetime(d["Date and time"]).dt.normalize()
    return pd.DataFrame({"v": close.values}, index=date).groupby(level=0).last()

# ── simple daily candidates + RV control ──
nfci = pd.read_csv(TMP/"_fred2_NFCI.csv"); nfci.columns = ["date","v"]; nfci["date"]=pd.to_datetime(nfci["date"]); nfci=nfci.set_index("date")[["v"]]
cor = pd.read_csv(EXT/"COR3M_D1_cboe.csv"); cor["date"]=pd.to_datetime(cor["DATE"]); cor=cor.set_index("date")[["CLOSE"]].rename(columns={"CLOSE":"v"})
s5fi = barexport_close(EXT/"S5FI_D1_index.csv")
sec = pd.read_csv(EXT/"SECTOR_SPDR_D1_yahoo.csv"); sec["date"]=pd.to_datetime(sec["date"]); sec=sec.set_index("date")
secret = sec.pct_change()
rdisp = secret.std(axis=1).rolling(21).mean().to_frame("v")          # cross-sectional dispersion, 21d
us500d = daily_close(BD/"US500_M15.csv")
rv = (np.log(us500d).diff().rolling(21).std()).to_frame("v")

# ── RCORR: trailing-21d avg pairwise sector corr ending strictly before each onset ──
def avg_pair_corr_at(retdf, onset, win=21):
    sub = retdf.loc[retdf.index < onset].tail(win).dropna()
    if len(sub) < max(8, win//2): return np.nan
    c = np.corrcoef(sub.values.T); iu = np.triu_indices_from(c,1)
    return float(np.nanmean(c[iu]))
rcorr = np.array([avg_pair_corr_at(secret, o) for o in onsets])

# ── UNTESTABLE (logged data-availability deviation, pre-result): ICORR (4-instrument corr) and
# HURST (4-leg 15m Hurst) require full-history DJ30 + USDJPY 15m bars, which are NOT on disk
# (US30/USDJPY bar-export panels are 2026-only; only NAS100/gold are full-history; the leg
# STRATEGY CSVs give P&L not continuous instrument bars). Both are the pre-reg's flagged
# ENDOGENOUS/REDUNDANT candidates ("never a clean exogenous win") -> dropped; family M=5 of the
# exogenous + within-equity set, which fully answers the exogenous-signal question.
RV = asof(rv, onsets)
CAND = {  # name: (values, registered_sign, class)
    "NFCI": (asof(nfci,onsets), +1, "cross-asset"),
    "S5FI": (asof(s5fi,onsets), -1, "within-equity"),
    "RDISP":(asof(rdisp,onsets), -1, "within-equity"),
    "RCORR":(rcorr, +1, "within-equity"),
    "COR3M":(asof(cor,onsets), +1, "within-equity"),
}

# ── common complete-case set ──
M = np.isfinite(RV) & np.isfinite(sev) & np.isfinite(cal)
for v,_,_ in CAND.values(): M &= np.isfinite(v)
N = int(M.sum())
print(f"N episodes: frozen={N0}  complete-case used={N}  (dropped {N0-N} for <window coverage at early onsets)")

def resid(y, Z):
    beta,*_ = np.linalg.lstsq(Z, y, rcond=None); return y - Z@beta
Z = np.column_stack([np.ones(N), rankdata(RV[M]), rankdata(cal[M])])
rsev = resid(rankdata(sev[M]), Z)
rX = {n_: resid(rankdata(v[M]), Z) for n_,(v,_,_) in CAND.items()}
def pcorr(a,b): return float(np.corrcoef(a,b)[0,1])
rho = {n_: pcorr(rX[n_], rsev) for n_ in CAND}

# ── premise: do vol / calendar alone rank severity? ──
prem_rv = spearmanr(sev[M], RV[M]); prem_cal = spearmanr(sev[M], cal[M])

# ── permutation: max-|rho| FWER + per-candidate one-sided ──
rng = np.random.default_rng(SEED)
names = list(CAND)
maxnull = np.empty(B); ge = {n_:0 for n_ in names}
for b in range(B):
    sp = rsev[rng.permutation(N)]
    rb = {n_: pcorr(rX[n_], sp) for n_ in names}
    maxnull[b] = max(abs(r) for r in rb.values())
    for n_ in names:
        s = CAND[n_][1]
        if s*rb[n_] >= s*rho[n_]: ge[n_] += 1
p_one = {n_: ge[n_]/B for n_ in names}
p_fwer = {n_: float(np.mean(maxnull >= abs(rho[n_]))) for n_ in names}

# ── raw (non-residualized) Spearman for context ──
raw = {n_: spearmanr(CAND[n_][0][M], sev[M]).correlation for n_ in names}

print(f"\nPREMISE (vol/cal must NOT already rank severity): "
      f"Spearman(sev,RV)={prem_rv.correlation:+.3f} p={prem_rv.pvalue:.3f} | "
      f"Spearman(sev,cal)={prem_cal.correlation:+.3f} p={prem_cal.pvalue:.3f}")
print(f"\n{'cand':6s} {'class':13s} {'sign':4s} {'rho_partial':>11s} {'raw_rho':>8s} {'p_1sided':>9s} {'p_FWER':>7s}  verdict")
order = sorted(names, key=lambda n_: -abs(rho[n_]))
res = {}
for n_ in order:
    s = CAND[n_][1]; ok_sign = np.sign(rho[n_])==s
    strong = ok_sign and p_fwer[n_] < 0.05
    nominal = ok_sign and p_one[n_] < 0.05 and not strong
    verdict = "STRONG-PASS" if strong else ("nominal(FWER-fragile)" if nominal else "fail")
    cls = CAND[n_][2]
    if strong and cls!="cross-asset": verdict += " ["+cls+"]"
    print(f"{n_:6s} {cls:13s} {('+' if s>0 else '-'):4s} {rho[n_]:>+11.3f} {raw[n_]:>+8.3f} {p_one[n_]:>9.4f} {p_fwer[n_]:>7.3f}  {verdict}")
    res[n_] = dict(cls=cls, sign=int(s), rho_partial=round(rho[n_],4), raw_rho=round(float(raw[n_]),4),
                   p_one=p_one[n_], p_fwer=p_fwer[n_], verdict=verdict)

promote = [n_ for n_ in names if res[n_]["verdict"].startswith("STRONG") and CAND[n_][2]=="cross-asset"]
within = [n_ for n_ in names if res[n_]["verdict"].startswith("STRONG") and CAND[n_][2]=="within-equity"]
print("\n=== DISPOSITION ===")
if promote: print(f"PROMOTE (cross-asset STRONG): {promote} -> Part-D sizing re-MC (after ALFRED-vintage NFCI gate)")
elif within: print(f"PARTIAL (within-equity STRONG only): {within} -> within-equity mechanism; HOLD for cross-asset confirmation")
else: print(f"NULL: no candidate clears FWER<0.05 with correct sign at N={N} (underpowered to |rho|~{1.96/np.sqrt(N-3):.2f}; NOT 'no signal exists')")

out = dict(prereg="v3.1", N_frozen=N0, N_used=N, seed=SEED, B=B,
           premise=dict(sev_rv=[round(prem_rv.correlation,3),round(prem_rv.pvalue,4)],
                        sev_cal=[round(prem_cal.correlation,3),round(prem_cal.pvalue,4)]),
           results=res, promote=promote, within=within)
(HERE/"battery_result.json").write_text(json.dumps(out, indent=2))
print(f"\nwrote battery_result.json")
