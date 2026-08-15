#!/usr/bin/env python3
"""plateau_tracker.py — incremental ±1-step neighbor grid tracker with pre-registered gate.

Usage:
  init:   python plateau_tracker.py init grid.json --center-exp 0.248 --center-pf 1.83 \
              --center-n 92 --center-net 68346 --r 3000 --gate-pos 8 --gate-total 10 --gate-median 0.12 \
              --order strong_close_15 strong_close_25 pierce_020 ...
  add:    python plateau_tracker.py add grid.json <csv> --label pierce_020
  show:   python plateau_tracker.py show grid.json

Rules enforced: dedup by label; same-feed discipline is on YOU (center and neighbors
must come from the same feed — 2026-06-11 flaw); gate evaluated only over --order labels
marked core (placebos excluded by suffix '_placebo' or listing after a '|' separator in order).
"""
import argparse, json, os, sys
import numpy as np
import pandas as pd

def parse_csv(path, r):
    df = pd.read_csv(path, encoding='utf-8-sig')
    df.columns = [c.strip() for c in df.columns]
    netcol = [c for c in df.columns if c.startswith('Net PnL') or c.startswith('Net P&L')][0]
    ex = df[df['Type'].str.startswith('Exit')]
    pnl = ex[netcol]
    w, l = pnl[pnl > 0], pnl[pnl <= 0]
    gl = abs(l.sum())
    return {'n': len(ex), 'wr': round(100*len(w)/len(ex), 1),
            'pf': round(float(w.sum()/gl), 3) if gl > 0 else float('inf'),
            'net': round(float(pnl.sum())),
            'exp_r': round(float(pnl.sum()/len(ex)/r), 3)}

def show(g):
    c = g['center']
    print(f"{'Label':<24}{'N':>5}{'WR%':>7}{'PF':>7}{'Net':>11}{'Exp(R)':>9}")
    print(f"{'CENTER (frozen)':<24}{c['n']:>5}{'—':>7}{c['pf']:>7}{c['net']:>11,}{c['exp']:>+9.3f}")
    print('-'*63)
    stored = {x['label']: x for x in g['results']}
    core = [l for l in g['order'] if l != '|' and '|' not in ''.join(g['order'][:g['order'].index(l)+1]).split(l)[0]] if '|' in g['order'] else g['order']
    core = g['order'][:g['order'].index('|')] if '|' in g['order'] else g['order']
    for lbl in [l for l in g['order'] if l != '|']:
        x = stored.get(lbl)
        if x:
            flag = ' <<NEG' if x['exp_r'] < 0 else (' <<LOW' if x['exp_r'] < g['gate']['median'] else '')
            print(f"{lbl:<24}{x['n']:>5}{x['wr']:>7}{x['pf']:>7}{x['net']:>11,}{x['exp_r']:>+9.3f}{flag}")
        else:
            print(f"{lbl:<24}    —")
    done = [stored[l] for l in core if l in stored]
    if done:
        exps = [x['exp_r'] for x in done]
        pos, med = sum(e > 0 for e in exps), float(np.median(exps))
        gt = g['gate']
        verdict = 'PASS' if (len(done) >= gt['total'] and pos >= gt['pos'] and med >= gt['median']) else \
                  ('FAIL' if (len(done) >= gt['total']) else 'pending')
        print(f"\nCore {len(done)}/{gt['total']}: {pos} positive | median {med:+.3f}R | "
              f"gate >= {gt['pos']}/{gt['total']} pos & median >= +{gt['median']}R -> {verdict}")

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    p0 = sub.add_parser('init'); p0.add_argument('store')
    for k in ['center-exp','center-pf','center-net','center-n','r','gate-median']:
        p0.add_argument(f'--{k}', type=float, required=True)
    p0.add_argument('--gate-pos', type=int, required=True)
    p0.add_argument('--gate-total', type=int, required=True)
    p0.add_argument('--order', nargs='+', required=True,
                    help="core labels, then optional '|' then placebo labels")
    p1 = sub.add_parser('add'); p1.add_argument('store'); p1.add_argument('csv')
    p1.add_argument('--label', required=True)
    p2 = sub.add_parser('show'); p2.add_argument('store')
    a = ap.parse_args()

    if a.cmd == 'init':
        g = {'center': {'exp': a.center_exp, 'pf': a.center_pf, 'net': int(a.center_net), 'n': int(a.center_n)},
             'r': a.r, 'order': a.order,
             'gate': {'pos': a.gate_pos, 'total': a.gate_total, 'median': a.gate_median},
             'results': []}
        json.dump(g, open(a.store, 'w'), indent=2); print('initialized'); return
    g = json.load(open(a.store))
    if a.cmd == 'add':
        r = parse_csv(a.csv, g['r']); r['label'] = a.label
        g['results'] = [x for x in g['results'] if x['label'] != a.label] + [r]
        json.dump(g, open(a.store, 'w'), indent=2)
    show(g)

if __name__ == '__main__':
    main()
