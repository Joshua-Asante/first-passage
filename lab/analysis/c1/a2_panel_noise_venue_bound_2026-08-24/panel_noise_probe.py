"""Panel-draw noise probe for the A2 shape-feasibility map.

Read-only w.r.t. the repo: imports the committed harness + production engine,
never edits them. Adds ONE degree of freedom the committed harness does not
expose -- the DGP panel's length and seed -- to measure how much of each cell's
verdict is a property of the shape and how much is a property of the single
520-week panel draw that cell happens to sit on.
"""
import sys, math, json, statistics
from collections import Counter
from pathlib import Path as _P
_ROOT = _P(__file__).resolve().parents[4]
sys.path[:0] = [str(_ROOT/'core'), str(_ROOT/'lab'), str(_ROOT),
                str(_ROOT/'lab/analysis/c1/shape_feasibility_map_2026-08')]
import numpy as np
import shape_generator as sg
from run_region_sweep import (_run_with_days, firm_consistency, se_of_proportion,
                              gate_status, combine_verdict, DD_GATE, PASS_GATE)
from discovery.prop_survivor_scoring import paired_blocks_from_daily, load_scoring_thresholds

THR = load_scoring_thresholds()


def build_panel(win_rate, shape, cadence, risk, *, n_weeks, seed):
    """Byte-identical to sg.build_panel when n_weeks=520 and seed=its own DGP seed."""
    rng = np.random.default_rng(seed)
    counts = Counter(sg.WEEKDAY_PATTERN[cadence])
    n_days = n_weeks * 5
    daily = np.zeros(n_days); intraday = np.zeros(n_days)
    for w in range(n_weeks):
        for wd, n_tr in counts.items():
            cum = 0.0; day_low = 0.0
            for _ in range(n_tr):
                is_win = bool(rng.random() < win_rate)
                r = sg._draw_trade_r(rng, shape, is_win)
                mae_r = sg._draw_trade_mae_r(rng, shape, is_win, r)
                trade_low = cum + mae_r * risk
                if trade_low < day_low: day_low = trade_low
                cum += r * risk
            idx = w * 5 + wd
            daily[idx] = cum; intraday[idx] = min(0.0, day_low)
    return daily, intraday


def score(win_rate, shape, cadence, risk, firm, *, n_weeks, seed, n_sims=500):
    daily, intraday = build_panel(win_rate, shape, cadence, risk, n_weeks=n_weeks, seed=seed)
    bp, bl = paired_blocks_from_daily(daily, intraday)
    summary, days = _run_with_days(firm, bp, THR, n_sims=n_sims,
                                   consistency=firm_consistency(firm), intraday_blocks=bl)
    bust = float(summary['headline_bust']); passr = float(summary['pass_rate'])
    n_total = n_sims * len(THR.seeds)
    sb = se_of_proportion(bust, n_total); sp = se_of_proportion(passr, n_total)
    return dict(bust=bust, pass_rate=passr,
                verdict=combine_verdict(gate_status(bust, sb, DD_GATE, direction='le'),
                                        gate_status(passr, sp, PASS_GATE, direction='ge')),
                median_days=float(np.median(days)) if days else None,
                panel_mean_per_day=float(daily.mean()))


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', required=True, choices=['reproduce', 'longpanel', 'redraw'])
    ap.add_argument('--redraws', type=int, default=12)
    a = ap.parse_args()

    CELLS = [
        (0.50, 'mild_right_skew', 2, 250.0, 'Tradeify_Growth_100K', 'GROWTH HEADLINE (RESULTS s13.2)'),
        (0.50, 'mild_right_skew', 2, 250.0, 'Tradeify_Select_100K', 'same cell, Select'),
        (0.55, 'symmetric',       1, 275.0, 'Tradeify_Select_100K', 'largest map/theory divergence'),
        (0.60, 'bounded_clustered', 3, 275.0, 'Tradeify_Select_100K', 'MARGINAL-band control'),
        (0.70, 'mild_right_skew', 8, 325.0, 'Tradeify_Select_100K', 'clean-FEASIBLE control'),
        (0.40, 'symmetric',       8, 325.0, 'Tradeify_Select_100K', 'clean-INFEASIBLE control'),
    ]

    if a.mode == 'reproduce':
        print('Harness fidelity check: my build_panel at n_weeks=520 + the cell DGP seed')
        print('must reproduce the committed region_data values exactly.\n')
        comm = {json.loads(l)['cell_id']: json.loads(l) for l in
                open(_ROOT/'lab/analysis/c1/shape_feasibility_map_2026-08/region_data_with_growth.jsonl')}
        for wr, sh, cd, rk, firm, lab in CELLS:
            seed = sg.DGP_MASTER_SEED + sg.tuple_index(wr, sh, cd, rk)
            r = score(wr, sh, cd, rk, firm, n_weeks=520, seed=seed)
            cid = f"wr{wr:.2f}_{sh}_cd{cd}_rk{int(rk)}_{firm}"
            c = comm[cid]
            ok = (abs(r['bust'] - c['bust']) < 1e-12 and abs(r['pass_rate'] - c['pass_rate']) < 1e-12)
            print(f"{'MATCH' if ok else 'DIFFER':7s} {cid[:52]:52s} mine {r['bust']:.4f}/{r['pass_rate']:.4f}  committed {c['bust']:.4f}/{c['pass_rate']:.4f}")

    elif a.mode == 'longpanel':
        print('Same DGP, same seed, panel 520 weeks -> 5,200 weeks (10x). Nothing else changes.')
        print('Engine, frozen seeds, horizon, sims_per_seed, intraday limb all identical.\n')
        print(f"{'cell':50s} {'520wk verdict':>16} {'5200wk verdict':>16}   bust 520 -> 5200")
        for wr, sh, cd, rk, firm, lab in CELLS:
            seed = sg.DGP_MASTER_SEED + sg.tuple_index(wr, sh, cd, rk)
            s = score(wr, sh, cd, rk, firm, n_weeks=520, seed=seed)
            L = score(wr, sh, cd, rk, firm, n_weeks=5200, seed=seed)
            cid = f"wr{wr:.2f} {sh[:16]} cd{cd} ${int(rk)} {firm.split('_')[1]}"
            flag = '   <-- VERDICT FLIPS' if s['verdict'] != L['verdict'] else ''
            print(f"{cid:50s} {s['verdict']:>16} {L['verdict']:>16}   {s['bust']:.4f} -> {L['bust']:.4f}{flag}")

    else:  # redraw
        print(f'Same cell, same length (520wk), {a.redraws} INDEPENDENT panel seeds.')
        print('This is the uncertainty the map\'s se_bust bars do not contain.\n')
        for wr, sh, cd, rk, firm, lab in CELLS[:4]:
            base = sg.DGP_MASTER_SEED + sg.tuple_index(wr, sh, cd, rk)
            out = [score(wr, sh, cd, rk, firm, n_weeks=520, seed=base + 100000 * (i + 1))
                   for i in range(a.redraws)]
            b = sorted(o['bust'] for o in out)
            v = Counter(o['verdict'] for o in out)
            cid = f"wr{wr:.2f} {sh} cd{cd} ${int(rk)} {firm}"
            print(f"{cid}   [{lab}]")
            print(f"   committed panel bust: (see reproduce)   redraws: min {b[0]:.4f}  median {statistics.median(b):.4f}  max {b[-1]:.4f}")
            print(f"   verdicts across {a.redraws} redraws: {dict(v)}\n")
