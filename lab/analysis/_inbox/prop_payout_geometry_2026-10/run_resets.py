import numpy as np, math
rng=np.random.default_rng(11); SUB=13
def attempt(S,sd,N,T):
    # returns outcome (1 pass,0 bust,-1 unfinished) and day ended, for horizon T
    mu=S*sd/math.sqrt(252); s=sd/math.sqrt(SUB)
    eq=np.zeros(N); hwm=np.zeros(N); best=np.full(N,-1e18); act=np.ones(N,bool); out=np.full(N,-1); tend=np.full(N,T)
    for d in range(1,T+1):
        if not act.any(): break
        floor=hwm-3000; st=eq.copy(); x=eq.copy(); br=np.zeros(N,bool)
        for k in range(SUB):
            x=x+mu/SUB+s*rng.standard_normal(N); br|=x<=floor
        b=act&br; out[b]=0; tend[b]=d; act[b]=False
        ok=act; eq[ok]=x[ok]; best[ok]=np.maximum(best[ok],(x-st)[ok]); hwm[ok]=np.maximum(hwm[ok],eq[ok])
        p=ok&(eq>=6000)&(best<=0.4*eq)&(d>=3); out[p]=1; tend[p]=d; act[p]=False
    return out,tend
def with_resets(S,sd,N=6000,T=200):
    left=np.full(N,T); passed=np.zeros(N,bool); n=np.zeros(N,int); active=np.ones(N,bool)
    while active.any():
        idx=np.where(active)[0]
        # simulate attempts with full T horizon, then truncate by remaining days
        out,tend=attempt(S,sd,len(idx),T)
        n[idx]+=1
        fin=tend<=left[idx]
        ps=fin&(out==1); passed[idx[ps]]=True; active[idx[ps]]=False
        bs=fin&(out==0); left[idx[bs]]-=tend[bs]; 
        unf=~fin|(out==-1); active[idx[unf]]=False
        active[left<3]=False
    return passed.mean(), n.mean(), np.percentile(n,95)
for S,sd in [(0,1000),(1.0,300),(1.0,600),(2.0,300),(2.0,400),(2.7,300),(2.7,400),(2.7,600)]:
    p,m,q=with_resets(S,sd)
    print(f"S={S} sd={sd}: P(pass within 200d, resets)={p:.3f} mean attempts={m:.2f} p95 attempts={q:.0f} mean fees=${265+169*(m-1):.0f}")
