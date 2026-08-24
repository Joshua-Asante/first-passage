import sys, json, time, os, pathlib
SP = str(pathlib.Path(__file__).resolve().parent)
sys.path[:0] = [SP]
import multiprocessing as mp

# firm -> risk scale (keeps rope/risk matched to the 100K grid, isolating TARGET/ROPE)
FIRMS = {
    'Tradeify_Select_100K':  1.0,      # rope $3,000  ratio 2.000  (the map's own)
    'Tradeify_Growth_100K':  3500/3000,# rope $3,500  ratio 1.714  (matched rope/risk)
    'Tradeify_Select_50K':   2000/3000,# rope $2,000  ratio 1.500
    'Tradeify_Select_25K':   1000/3000,# rope $1,000  ratio 1.500
}
NW = 5200

def work(args):
    import panel_noise_probe as P, shape_generator as sg
    wr, sh, cd, rk = args
    seed = sg.DGP_MASTER_SEED + sg.tuple_index(wr, sh, cd, rk)
    out=[]
    for firm, scale in FIRMS.items():
        r = P.score(wr, sh, cd, rk*scale, firm, n_weeks=NW, seed=seed, n_sims=500)
        r.update(win_rate=wr, shape=sh, cadence=cd, risk_usd_base=rk,
                 risk_usd_used=rk*scale, firm=firm, n_weeks=NW,
                 cell_id=f"wr{wr:.2f}_{sh}_cd{cd}_rk{int(rk)}_{firm}")
        out.append(r)
    return out

if __name__=='__main__':
    sys.path[:0]=['core','lab','.','lab/analysis/c1/shape_feasibility_map_2026-08']
    import shape_generator as sg
    tuples = sg.all_tuples()
    t0=time.time()
    with mp.Pool(3) as pool, open(f'{SP}/longpanel_tiers.jsonl','w') as fh:
        for i, res in enumerate(pool.imap_unordered(work, tuples, chunksize=4)):
            for r in res: fh.write(json.dumps(r)+'\n')
            fh.flush()
            if i%25==0: print(f"{i}/{len(tuples)} {time.time()-t0:.0f}s", flush=True)
    print("DONE", time.time()-t0)
