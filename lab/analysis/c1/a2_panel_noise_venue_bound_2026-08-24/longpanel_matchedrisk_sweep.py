import sys, json, time, pathlib, multiprocessing as mp
SP = str(pathlib.Path(__file__).resolve().parent)
sys.path[:0]=[SP]
NW=5200
def work(args):
    import panel_noise_probe as P, shape_generator as sg
    wr,sh,cd,rk=args
    seed=sg.DGP_MASTER_SEED+sg.tuple_index(wr,sh,cd,rk)
    r=P.score(wr,sh,cd,rk,'Tradeify_Select_50K',n_weeks=NW,seed=seed,n_sims=500)
    r.update(win_rate=wr,shape=sh,cadence=cd,risk_usd=rk,firm='Tradeify_Select_50K',
             cell_id=f"wr{wr:.2f}_{sh}_cd{cd}_rk{int(rk)}_Tradeify_Select_50K")
    return r
if __name__=='__main__':
    sys.path[:0]=['core','lab','.','lab/analysis/c1/shape_feasibility_map_2026-08']
    import shape_generator as sg
    t0=time.time()
    with mp.Pool(3) as pool, open(f'{SP}/longpanel_50k_matched.jsonl','w') as fh:
        for i,r in enumerate(pool.imap_unordered(work, sg.all_tuples(), chunksize=4)):
            fh.write(json.dumps(r)+'\n'); fh.flush()
            if i%50==0: print(f"{i}/315 {time.time()-t0:.0f}s", flush=True)
    print("DONE", time.time()-t0)
