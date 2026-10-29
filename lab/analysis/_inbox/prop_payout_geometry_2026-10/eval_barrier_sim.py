import numpy as np, math
rng=np.random.default_rng(7)
SUB=13
def eval_sim(S,sd,N=20000,T=200,tgt=6000,dd=3000,cons=0.4,mind=3,attempt_limit=None):
    mu=S*sd/math.sqrt(252); s=sd/math.sqrt(SUB)
    eq=np.zeros(N); hwm=np.zeros(N); best=np.full(N,-1e18); alive=np.ones(N,bool); passed=np.zeros(N,bool); tpass=np.full(N,np.nan)
    for d in range(1,T+1):
        floor=hwm-dd
        start=eq.copy(); x=eq.copy(); breach=np.zeros(N,bool)
        for k in range(SUB):
            x=x+mu/SUB+s*rng.standard_normal(N); breach|=x<=floor
        dayp=x-start
        a=alive&~passed
        newb=a&breach
        alive[newb]=False
        ok=a&~breach
        eq[ok]=x[ok]; best[ok]=np.maximum(best[ok],dayp[ok]); hwm[ok]=np.maximum(hwm[ok],eq[ok])
        p=ok&(eq>=tgt)&(best<=cons*eq)&(d>=mind)
        passed[p]=True; tpass[p]=d
    return passed.mean(), np.nanmedian(tpass) if passed.any() else np.nan, (~alive).mean()
def funded_sim(S,sd,N=20000,T=250,dd=3000,lock=100,cap=4000,frac=0.5,split=0.9):
    mu=S*sd/math.sqrt(252); s=sd/math.sqrt(SUB)
    eq=np.zeros(N); hwm=np.zeros(N); alive=np.ones(N,bool); wins=np.zeros(N,int); paid=np.zeros(N); npay=np.zeros(N,int); locked=np.zeros(N,bool)
    for d in range(T):
        floor=np.where(locked,lock,hwm-dd)
        x=eq.copy(); br=np.zeros(N,bool); st=eq.copy()
        for k in range(SUB):
            x=x+mu/SUB+s*rng.standard_normal(N); br|=x<=floor
        a=alive.copy(); alive[a&br]=False
        ok=a&~br; eq[ok]=x[ok]; hwm[ok]=np.maximum(hwm[ok],eq[ok])
        locked|=(hwm-dd)>=lock
        wins[ok&(x-st>0)]+=1
        req=ok&(wins>=5)&(eq>0)
        amt=np.minimum(frac*np.maximum(eq,0),cap)
        req&=amt>=500
        paid[req]+=split*amt[req]; eq[req]-=amt[req]; npay[req]+=1; wins[req]=0
    return paid.mean(), (npay>=1).mean(), (npay>=5).mean(), alive.mean()
if __name__=="__main__":
    print("zero-edge / Sharpe sweep, eval single attempt, 200d")
    for S in [-0.5,0,0.7,1.0,1.5,2.0,2.7,3.5]:
        best=None
        for sd in [250,400,600,800,1000,1300,1700]:
            p,tm,b=eval_sim(S,sd,N=8000)
            if best is None or p>best[1]: best=(sd,p,tm,b)
        print(f"S={S:4} best sd={best[0]:5} pass={best[1]:.3f} median_days={best[2]} bust={best[3]:.3f}")
