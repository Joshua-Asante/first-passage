#!/usr/bin/env python3
"""Q-EVALSEQ-1 — frozen K=4 within-eval schedule family on the recovered book-comp harness.

Runs ONLY what OPERATIONALIZATION.md (committed first) freezes:
fidelity gate (m=1.0 must reproduce recorded 37.78% eval pass) -> control (a) ->
policies (b)(c)(d) on full panel -> halves verification of the full-panel winner ->
sham-policy placebo + best-of-3 correction. Emits out/evalseq_results.json.

Path machinery and eval rules are a faithful port of gap_stage2.py build_paths/eval_sim
(tag pre-prune-2026-08-08), with the scalar multiplier generalized to a per-day,
start-of-day-state policy. With a constant policy the loop is algebraically identical.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
HARNESS = HERE.parent / "tradeify_book_composition_2026-07-23"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)

DD, CAP_EVAL, TARGET, START = 3_000.0, 80.0, 106_000.0, 100_000.0
SEEDS, N_PATHS, H_EVAL = (11, 12, 13), 10_000, 520
FIDELITY_HISTORICAL = 37.78   # RESULTS.md recorded anchor (2026-07-28 environment)
FIDELITY_REGEN = 38.2         # recovered ORIGINAL gap_stage2.py, this environment (gate v2)
FIDELITY_TOL = 0.1


def load_panel():
    panel = pd.read_csv(HARNESS / "out" / "daily_panel.csv", index_col=0, parse_dates=True)
    # qty series exactly as gap_stage2.main builds it
    files = [
        HARNESS / "inputs" / "Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-23_626e8.csv",
        HARNESS / "inputs" / "Striker_NAS100_MNQ_CME_MINI_MNQ1!_2026-07-23_0ebc6.csv",
    ]
    events = []
    for f in files:
        df = pd.read_csv(f, encoding="utf-8-sig")
        df.columns = [c.strip().replace(chr(0xFEFF), "") for c in df.columns]
        df["dt"] = pd.to_datetime(df["Date and time"])
        en = df[df["Type"].str.startswith("Entry")][["dt", "Size (qty)"]].assign(q=lambda d: d["Size (qty)"])
        ex = df[df["Type"].str.startswith("Exit")][["dt", "Size (qty)"]].assign(q=lambda d: -d["Size (qty)"])
        events.append(pd.concat([en[["dt", "q"]], ex[["dt", "q"]]]))
    ev = pd.concat(events).sort_values("dt")
    ev["date"] = ev["dt"].dt.normalize()
    day_max = {}
    for date, g in ev.groupby("date"):
        g = g.sort_values("dt")
        day_max[date] = float(g["q"].cumsum().max())
    qty = pd.Series(day_max).reindex(panel.index).fillna(0.0)
    return panel.index, panel["combined"].values, qty.values


def week_blocks(dates, sel=None):
    idx = np.arange(len(dates))
    if sel is not None:
        idx = idx[sel]
        dates = dates[sel]
    s = pd.Series(idx, index=dates)
    wk = s.groupby(dates - pd.to_timedelta(dates.weekday, unit="D")).apply(lambda x: x.values)
    return [b for b in wk.values if len(b) > 0]


def build_paths(pnl, qmax, blocks, n_paths, horizon, rng):
    nb = len(blocks)
    p = np.zeros((n_paths, horizon))
    q = np.zeros((n_paths, horizon))
    max_blocks = horizon // 3 + 3
    picks = rng.integers(0, nb, size=(n_paths, max_blocks))
    for i in range(n_paths):
        seq_p, seq_q, tot = [], [], 0
        for b in picks[i]:
            idxs = blocks[b]
            seq_p.append(pnl[idxs])
            seq_q.append(qmax[idxs])
            tot += len(idxs)
            if tot >= horizon:
                break
        p[i] = np.concatenate(seq_p)[:horizon]
        q[i] = np.concatenate(seq_q)[:horizon]
    return p, q


def eval_sim_policy(p, q, policy, t_b=None):
    """gap_stage2.eval_sim with m generalized to per-day start-of-day-state multiplier.

    policy(t, bal, peak, stepped) -> m_t (vector over paths). 'stepped' is the (d) latch.
    """
    n, h = p.shape
    bal = np.full(n, START)
    peak = bal.copy()
    tdays = np.zeros(n)
    maxpos = np.zeros(n)
    alive = np.ones(n, bool)
    passed = np.zeros(n, bool)
    bust = np.zeros(n, bool)
    stepped = np.zeros(n, bool)
    t_pass = np.full(n, np.nan)
    m_sample = []  # realized multipliers on alive paths (for the sham marginal)
    for t in range(h):
        m = policy(t, bal, peak, stepped, t_b)
        qm = q[:, t] * m
        clip = np.minimum(1.0, np.where(qm > 0, CAP_EVAL / np.maximum(qm, 1e-9), 1.0))
        d = p[:, t] * m * clip
        if t < 260:
            m_sample.append(m[alive][:50].copy())
        bal[alive] += d[alive]
        traded = alive & (np.abs(d) > 1e-9)
        tdays[traded] += 1
        maxpos = np.where(traded, np.maximum(maxpos, d), maxpos)
        floor = peak - DD
        nbust = alive & (bal <= floor)
        bust |= nbust
        alive &= ~nbust
        profit = bal - START
        ok = alive & (bal >= TARGET) & (tdays >= 3) & (maxpos <= 0.4 * profit)
        t_pass[ok & ~passed] = t
        passed |= ok
        alive &= ~ok
        peak = np.where(alive, np.maximum(peak, bal), peak)
        stepped |= peak >= 101_500.0  # (d) latch: EOD peak >= +$1,500
    return passed, bust, t_pass, np.concatenate(m_sample) if m_sample else np.array([])


# --- the frozen family (OPERATIONALIZATION.md) ---
def pol_const(mval):
    def f(t, bal, peak, stepped, t_b):
        return np.full(bal.shape, mval)
    return f


def pol_linear(t, bal, peak, stepped, t_b):
    return np.full(bal.shape, float(np.clip(0.75 - 0.50 * (t / t_b), 0.25, 0.75)))


def pol_cushion(t, bal, peak, stepped, t_b):
    cushion = bal - (peak - DD)
    return 0.75 * np.minimum(1.0, np.maximum(cushion, 0.0) / DD)


def pol_step(t, bal, peak, stepped, t_b):
    return np.where(stepped, 0.375, 0.75)


def pol_sham(mults, rng_seed):
    """i.i.d. per-day draw from a realized multiplier marginal (state-dependence destroyed)."""
    srng = np.random.default_rng(rng_seed)
    def f(t, bal, peak, stepped, t_b):
        return np.full(bal.shape, float(srng.choice(mults)))
    return f


def run_policy(pnl, qmax, blocks, policy, t_b=None, seeds=SEEDS):
    rows, msamps = [], []
    for s in seeds:
        rng = np.random.default_rng(s)
        p, q = build_paths(pnl, qmax, blocks, N_PATHS, H_EVAL, rng)
        passed, bust, t_pass, msamp = eval_sim_policy(p, q, policy, t_b)
        rows.append(dict(pass_pct=passed.mean() * 100, bust_pct=bust.mean() * 100,
                         med_days=float(np.nanmedian(t_pass)) if passed.any() else float("nan")))
        msamps.append(msamp)
    agg = {k: float(np.mean([r[k] for r in rows])) for k in rows[0]}
    agg["per_seed"] = rows
    return agg, np.concatenate([m for m in msamps if m.size])


def main():
    dates, pnl, qmax = load_panel()
    blocks_full = week_blocks(dates)
    res = {}

    # 1) fidelity gate: constant m=1.0 must reproduce the recorded 37.78%
    fid, _ = run_policy(pnl, qmax, blocks_full, pol_const(1.0))
    res["fidelity"] = fid
    print(f"FIDELITY m=1.0: pass {fid['pass_pct']:.2f}% (regen-original {FIDELITY_REGEN}; historical {FIDELITY_HISTORICAL})  bust {fid['bust_pct']:.2f}%")
    if abs(fid["pass_pct"] - FIDELITY_REGEN) > FIDELITY_TOL:
        print("FIDELITY GATE FAIL — stopping before any policy read.")
        (OUT / "evalseq_results.json").write_text(json.dumps(res, indent=2))
        sys.exit(2)
    print("FIDELITY GATE PASS")

    # 2) control (a) flat 0.50x
    ctrl, _ = run_policy(pnl, qmax, blocks_full, pol_const(0.50))
    res["control"] = ctrl
    t_b = ctrl["med_days"]
    res["T_b"] = t_b
    print(f"CONTROL 0.50x: pass {ctrl['pass_pct']:.2f}%  bust {ctrl['bust_pct']:.2f}%  med {t_b:.0f}bd")

    # 3) policies (b)(c)(d) on full panel
    fams = {"b_linear": (pol_linear, t_b), "c_cushion": (pol_cushion, None), "d_step": (pol_step, None)}
    winner, msamp_w = None, None
    for name, (fn, tb) in fams.items():
        r, msamp = run_policy(pnl, qmax, blocks_full, fn, tb)
        r["lift_pt"] = r["pass_pct"] - ctrl["pass_pct"]
        r["bust_delta"] = r["bust_pct"] - ctrl["bust_pct"]
        res[name] = r
        print(f"{name}: pass {r['pass_pct']:.2f}% (lift {r['lift_pt']:+.2f}pt)  bust {r['bust_pct']:.2f}% (delta {r['bust_delta']:+.2f})")
        if winner is None or r["lift_pt"] > res[winner]["lift_pt"]:
            winner, msamp_w = name, msamp
    res["winner"] = winner
    print(f"WINNER (full-panel selection): {winner}")

    # 4) halves verification of the selected policy only
    mid = len(dates) // 2
    for half, sel in (("H1", np.arange(len(dates)) < mid), ("H2", np.arange(len(dates)) >= mid)):
        blocks_h = week_blocks(dates, sel)
        ch, _ = run_policy(pnl[:], qmax[:], blocks_h, pol_const(0.50))
        fn, tb = fams[winner]
        wh, _ = run_policy(pnl[:], qmax[:], blocks_h, fn, tb)
        res[f"{half}"] = dict(control=ch, winner=wh,
                              lift_pt=wh["pass_pct"] - ch["pass_pct"],
                              bust_delta=wh["bust_pct"] - ch["bust_pct"],
                              split_date=str(dates[mid].date()))
        print(f"{half}: ctrl pass {ch['pass_pct']:.2f}/bust {ch['bust_pct']:.2f} | win pass {wh['pass_pct']:.2f}/bust {wh['bust_pct']:.2f} | lift {res[half]['lift_pt']:+.2f}pt")

    # 5) placebo: 60 shams from the winner's realized multiplier marginal + best-of-3 correction
    sham_lifts = []
    for i in range(60):
        r, _ = run_policy(pnl, qmax, blocks_full, pol_sham(msamp_w, 1000 + i), seeds=(11,))
        sham_lifts.append(r["pass_pct"] - ctrl["per_seed"][0]["pass_pct"])
    sham_lifts = np.array(sham_lifts)
    w_lift = res[winner]["lift_pt"]
    p_placebo = float((sham_lifts >= w_lift).mean())
    boot = np.random.default_rng(7)
    max3 = np.max(boot.choice(sham_lifts, size=(10_000, 3)), axis=1)
    p95_max3 = float(np.percentile(max3, 95))
    res["placebo"] = dict(sham_mean=float(sham_lifts.mean()), sham_p95=float(np.percentile(sham_lifts, 95)),
                          p_placebo=p_placebo, p95_max3=p95_max3, winner_lift=w_lift,
                          pass_placebo=bool(p_placebo < 0.05), pass_max3=bool(w_lift > p95_max3))
    print(f"PLACEBO: sham mean {sham_lifts.mean():+.2f}pt  p={p_placebo:.3f}  max3 p95 {p95_max3:+.2f}pt  winner {w_lift:+.2f}pt")

    (OUT / "evalseq_results.json").write_text(json.dumps(res, indent=2))
    print(f"saved -> {OUT / 'evalseq_results.json'}")


if __name__ == "__main__":
    main()
