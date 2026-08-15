"""Dealer-gamma addendum to the extension: score SqueezeMetrics FREE index-level DIX & GEX
(the one untested family with an academic theory-of-lead: Barbon & Buraschi 'Gamma Fragility',
t-1 dealer-gamma imbalance predicts next-period fragility). Same battery recipe; signs FROZEN."""
import urllib.request, io
from pathlib import Path
import numpy as np, pandas as pd
from scipy.stats import rankdata, spearmanr
HERE=Path(__file__).resolve().parent; B,SEED=20000,20260625
raw=urllib.request.urlopen(urllib.request.Request("https://squeezemetrics.com/monitor/static/DIX.csv",headers={"User-Agent":"Mozilla/5.0"}),timeout=40).read()
sm=pd.read_csv(io.BytesIO(raw)); sm["date"]=pd.to_datetime(sm["date"])
dix=pd.Series(sm["dix"].astype(float).values,index=sm["date"]).sort_index()
gex=pd.Series(sm["gex"].astype(float).values,index=sm["date"]).sort_index()
# PRE-REGISTERED (frozen by theory): lower GEX -> less dealer stabilization -> bigger moves -> worse;
# lower DIX -> bearish/uncertain dark-pool flow -> worse. Both sign -1 (lower => higher severity).
CAND={"GEX":(gex,-1,"dealer-gamma"),"DIX":(dix,-1,"dealer-flow")}
ep=pd.read_csv(HERE/"glm_inputs.csv"); ep=ep[ep["rv_finite"]].copy(); ep["onset"]=pd.to_datetime(ep["onset"])
onsets=ep["onset"].to_numpy(); sev=ep["depth_usd"].to_numpy(float); rv=ep["rv_at_peak"].to_numpy(float); cal=ep["calendar_rank"].to_numpy(float)
def asof(s,onsets):
    s=s.sort_index(); out=[]
    for o in onsets:
        m=s.index<o; out.append(s[m].iloc[-1] if m.any() else np.nan)
    return np.array(out,float)
X={n:(asof(v,onsets),sgn,cls) for n,(v,sgn,cls) in CAND.items()}
for n,(v,_,_) in X.items(): print(f"  {n} {np.isfinite(v).sum()}/33  span {CAND[n][0].index.min().date()}..{CAND[n][0].index.max().date()}")
names=list(X); Mmask=np.isfinite(sev)&np.isfinite(rv)&np.isfinite(cal)
for v,_,_ in X.values(): Mmask&=np.isfinite(v)
N=int(Mmask.sum())
def resid(y,Z): beta,*_=np.linalg.lstsq(Z,y,rcond=None); return y-Z@beta
def pcorr(a,b): return float(np.corrcoef(a,b)[0,1])
Z=np.column_stack([np.ones(N),rankdata(rv[Mmask]),rankdata(cal[Mmask])])
rsev=resid(rankdata(sev[Mmask]),Z); rX={n:resid(rankdata(X[n][0][Mmask]),Z) for n in names}
rho={n:pcorr(rX[n],rsev) for n in names}; raw_={n:float(spearmanr(X[n][0][Mmask],sev[Mmask]).correlation) for n in names}
prv=spearmanr(sev[Mmask],rv[Mmask]); pcal=spearmanr(sev[Mmask],cal[Mmask])
print(f"\nfaithfulness: Spearman(sev,RV)={prv.correlation:+.3f}/{prv.pvalue:.3f}  Spearman(sev,cal)={pcal.correlation:+.3f}/{pcal.pvalue:.3f}")
rng=np.random.default_rng(SEED); maxnull=np.empty(B); ge={n:0 for n in names}
for b in range(B):
    sp=rsev[rng.permutation(N)]; rb={n:pcorr(rX[n],sp) for n in names}; maxnull[b]=max(abs(r) for r in rb.values())
    for n in names:
        s=X[n][1]
        if s*rb[n]>=s*rho[n]: ge[n]+=1
p_one={n:ge[n]/B for n in names}; p_fwer={n:float(np.mean(maxnull>=abs(rho[n]))) for n in names}
print(f"\nN={N}  power floor |rho|~{1.96/np.sqrt(N-3):.2f}  (M={len(names)} dealer-gamma family)\n")
print(f"{'cand':5s} {'class':12s} {'sgn':3s} {'rho_part':>8s} {'raw_rho':>8s} {'p_1sd':>6s} {'p_FWER':>7s}  verdict")
for n in sorted(names,key=lambda n:-abs(rho[n])):
    s=X[n][1]; ok=np.sign(rho[n])==s; strong=ok and p_fwer[n]<0.05; nom=ok and p_one[n]<0.05 and not strong
    v="STRONG-PASS" if strong else ("nominal(FWER-fragile)" if nom else ("fail(wrong-sign)" if not ok else "fail"))
    print(f"{n:5s} {X[n][2]:12s} {('+' if s>0 else '-'):3s} {rho[n]:>+8.3f} {raw_[n]:>+8.3f} {p_one[n]:>6.3f} {p_fwer[n]:>7.3f}  {v}")
