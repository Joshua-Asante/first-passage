import pandas as pd, numpy as np
F="BAR_EXPORT_v0_1_FX_USOIL_2026-06-14_16557.csv"
df=pd.read_csv(F, encoding="utf-8-sig")
def ps(s):
    if not isinstance(s,str) or '|' not in s: return None
    p=s.split('|')
    try: return (int(p[0]),float(p[1]),float(p[2]),float(p[3]),float(p[4]))
    except: return None
b=[ps(s) for s in df['Signal']]; b=[x for x in b if x]
bd=pd.DataFrame(b,columns=['e','O','H','L','C']).drop_duplicates('e').sort_values('e').reset_index(drop=True)
bd['ts']=pd.to_datetime(bd['e'],unit='ms',utc=True)
# EXCLUDE April-2020 corruption window + any stray sub-$1 bar
pre=len(bd)
bd=bd[~((bd['ts']>="2020-04-01")&(bd['ts']<="2020-05-15"))]
bd=bd[(bd[['O','H','L','C']]>1.0).all(axis=1)].reset_index(drop=True)
print(f"bars: {pre} -> {len(bd)} after Apr-2020/sub-$1 exclusion ({pre-len(bd)} removed)")
print(f"clean range: {bd['ts'].min().date()} .. {bd['ts'].max().date()}")

O,H,L,C=bd['O'].values,bd['H'].values,bd['L'].values,bd['C'].values
sma=pd.Series(C).rolling(50).mean().values
tr=np.maximum(H-L, np.maximum(np.abs(H-np.roll(C,1)), np.abs(L-np.roll(C,1)))); tr[0]=H[0]-L[0]
atr=np.full(len(C),np.nan); atr[14]=np.nanmean(tr[1:15])
for i in range(15,len(C)): atr[i]=(atr[i-1]*13+tr[i])/14
n=len(C)

def find_entries(m):
    edge=sma+m*atr; out=[]; i=1
    while i<n:
        if not np.isnan(edge[i]) and C[i]>edge[i] and (np.isnan(edge[i-1]) or C[i-1]<=edge[i-1]):
            hi=H[i]; j=i
            while j+1<n and C[j+1]>edge[j+1]: j+=1; hi=max(hi,H[j])
            k=j+1
            if k<n: out.append((k, max(hi,H[k])))
            i=k
        i+=1
    return out

def walk(k, spike_high, Tatr, HOR):
    # short from C[k]; R = stop distance = spike_high - entry
    entry=C[k]; ak=atr[k]; Sd=spike_high-entry
    if Sd<=0 or np.isnan(ak) or k+HOR>=n: return None
    Satr=Sd/ak; tgt=entry-Tatr*ak; stop=spike_high
    for j in range(k+1, k+1+HOR):
        ht = L[j]<=tgt; hs = H[j]>=stop
        if ht and hs: return ("amb",Satr,Sd)
        if ht: return ("win",Satr,Sd)
        if hs: return ("loss",Satr,Sd)
    rel=(entry-C[k+HOR])/ak
    return ("open",Satr,Sd,rel)

def evaluate(entries, Tatr, HOR, xprice=0.08):
    best=[];worst=[];cw=cl=amb=opn=0; costs=[]
    for k,sh in entries:
        r=walk(k,sh,Tatr,HOR)
        if r is None: continue
        kind=r[0]; Satr=r[1]; Sd=r[2]; cost=xprice/Sd; costs.append(cost)
        if kind=="win": v=Tatr/Satr; best.append(v-cost); worst.append(v-cost); cw+=1
        elif kind=="loss": best.append(-1-cost); worst.append(-1-cost); cl+=1
        elif kind=="amb": best.append(Tatr/Satr-cost); worst.append(-1-cost); amb+=1
        else: rr=r[3]/Satr; best.append(rr-cost); worst.append(rr-cost); opn+=1
    N=len(best); mb,mw=np.mean(best),np.mean(worst)
    return dict(N=N,cw=cw,cl=cl,amb=amb,opn=opn,best=mb,worst=mw,mid=(mb+mw)/2,cost=np.mean(costs))

print("\nEpisodes: " + "  ".join([f"m={m}:{len(find_entries(m))}" for m in [1.5,2.0,2.5]]))

print("\n=== TARGET CURVE  (m=2.0, H=30 bars ~5d, cost x=0.08, net of cost) ===")
ent=find_entries(2.0)
print(f"{'T(ATR)':>6} {'n':>4} {'cw':>4} {'cl':>4} {'amb':>4} {'opn':>4} {'meanCost':>9} {'E[R]best':>9} {'E[R]mid':>9} {'E[R]worst':>9}")
for T in [1.0,1.5,2.0,2.5]:
    r=evaluate(ent,T,30)
    print(f"{T:>6} {r['N']:>4} {r['cw']:>4} {r['cl']:>4} {r['amb']:>4} {r['opn']:>4} {r['cost']:>9.3f} {r['best']:>9.3f} {r['mid']:>9.3f} {r['worst']:>9.3f}")
print("  (4x cost bar at x=0.08, meanCost~ shown: clear with margin = mid >> ~4x meanCost)")

# PLACEBO at primary cell m=2.0 H=30 T=1.5
print("\n=== PLACEBO (m=2.0,H=30,T=1.5): real vs random-day short, matched n & stop sizes ===")
rng=np.random.default_rng(11)
def rand_eval(N, Sd_pool, Tatr, HOR, xprice=0.08):
    idx=rng.integers(0, n-HOR-1, size=N); sdraw=rng.choice(Sd_pool, size=N, replace=True)
    best=[];worst=[]
    for ii,Sd in zip(idx,sdraw):
        ak=atr[ii]
        if np.isnan(ak) or Sd<=0: continue
        entry=C[ii]; Satr=Sd/ak; tgt=entry-Tatr*ak; stop=entry+Sd; cost=xprice/Sd
        out=None
        for j in range(ii+1, ii+1+HOR):
            ht=L[j]<=tgt; hs=H[j]>=stop
            if ht and hs: out=("amb"); break
            if ht: out=("win"); break
            if hs: out=("loss"); break
        if out=="win": v=Tatr/Satr; best.append(v-cost); worst.append(v-cost)
        elif out=="loss": best.append(-1-cost); worst.append(-1-cost)
        elif out=="amb": best.append(Tatr/Satr-cost); worst.append(-1-cost)
        else: rr=(entry-C[ii+HOR])/ak/Satr; best.append(rr-cost); worst.append(rr-cost)
    return (np.mean(best)+np.mean(worst))/2
real=evaluate(ent,1.5,30); real_mid=real['mid']
Sd_pool=np.array([walk(k,sh,1.5,30)[2] for k,sh in ent if walk(k,sh,1.5,30)])
null=np.array([rand_eval(real['N'],Sd_pool,1.5,30) for _ in range(1000)])
p=np.mean(null>=real_mid)
print(f"  real E[R]_mid={real_mid:+.3f} (n={real['N']}) | null mean={null.mean():+.3f} sd={null.std():.3f} p95={np.percentile(null,95):+.3f}")
print(f"  p(null>=real) = {p:.3f}   {'<-- SELECTION ADDS EDGE' if p<0.05 else ('<-- marginal' if p<0.10 else '<-- no edge over random')}")

# HALVES / THIRDS stationarity at primary cell
print("\n=== STATIONARITY (m=2.0,H=30,T=1.5, net mid E[R]) ===")
ts=bd['ts'].values
def seg_eval(lo,hi):
    e=[(k,sh) for k,sh in ent if lo<=k<hi]; r=evaluate(e,1.5,30); return r['N'],r['mid']
half=n//2
for lab,(lo,hi) in [("H1",(0,half)),("H2",(half,n))]:
    N,m=seg_eval(lo,hi); print(f"  {lab} ({pd.Timestamp(ts[lo]).date()}..{pd.Timestamp(ts[min(hi,n-1)]).date()}): n={N} mid={m:+.3f}")
t=n//3
for lab,(lo,hi) in [("T1",(0,t)),("T2",(t,2*t)),("T3",(2*t,n))]:
    N,m=seg_eval(lo,hi); print(f"  {lab} ({pd.Timestamp(ts[lo]).date()}..{pd.Timestamp(ts[min(hi,n-1)]).date()}): n={N} mid={m:+.3f}")

# KILL-SWITCH at primary cell
print("\n=== KILL-SWITCH (suppress after k=2 consecutive new-high fails) m=2.0,H=30,T=1.5 ===")
def killswitch_eval(entries,Tatr,HOR,kk=2):
    consec=0; ev=[]
    for k,sh in entries:
        r=walk(k,sh,Tatr,HOR)
        if r is None: continue
        if consec>=kk:
            consec = 0 if r[0]!="loss" and r[0]!="amb" else consec
            continue
        ev.append((k,sh))
        if r[0]=="win": consec=0
        elif r[0] in ("loss","amb"): consec+=1
        else: consec=0
    return evaluate(ev,Tatr,HOR)
ks=killswitch_eval(ent,1.5,30)
print(f"  naive: n={real['N']} mid={real['mid']:+.3f}  |  killswitch: n={ks['N']} mid={ks['mid']:+.3f}")

print("\n=== HORIZON robustness (m=2.0, T=1.5, net mid E[R]) ===")
for HOR in [12,30,60]:
    r=evaluate(ent,1.5,HOR); print(f"  H={HOR:>2} (~{HOR*4//24}d): n={r['N']} cw={r['cw']} cl={r['cl']} amb={r['amb']} opn={r['opn']} mid={r['mid']:+.3f}")
