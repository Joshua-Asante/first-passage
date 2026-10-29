"""Follow-ups to PASS63_CHECK.md (2026-10-26), synthetic Gaussian strategies only.

  pass90    P(pass <= 90 days) vs Sharpe 3.0..6.0, single attempt (engines A and B of pass63_check)
  resets    P(funded within 63 / 90 days), resets allowed, Select Flex 100K vs 50K (payout_sim)
  renewal   per-attempt p(sd) and length L(sd); argmin_sd (reset + lam*L)/p, time to funded
  payout    time to first payout >= $1,000 net (payout_sim.first_payout), eval and funded sd separate
  payout_t4 / payout_t3   the same with fat-tailed days: Student-t daily P&L (nu = 4 / 3) via a per-day
            volatility scale mixture, same mean and sd, Brownian path within the day

Reproduce (fixed seeds): python -I scripts/fp.py python lab/analysis/_inbox/prop_payout_geometry_2026-10/pass63_followups.py <section>
"""
import math
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[3] / "core"))
sys.path.insert(0, str(HERE))
import pass63_check as pc  # noqa: E402
import payout_sim  # noqa: E402
from payout_sim import first_payout  # noqa: E402
from programs import tradeify  # noqa: E402

N = 20_000
PROG = {100: tradeify(100)["TFY Select Flex 100K"], 50: tradeify(50)["TFY Select Flex 50K"]}


def _best(g):
    s = max(sorted(g), key=lambda k: g[k][0])
    near = [k for k in sorted(g) if g[k][0] >= g[s][0] - 0.01]
    return s, g[s], (near[0], near[-1])


# --- pass90 -------------------------------------------------------------------------------
P90_SRS = [3.0 + 0.25 * i for i in range(13)]
P90_SDS = list(range(200, 1001, 50))


def pass90(ex):
    h = 90
    ta = [(h, sr, sd, 9001, True, 0.40) for sr in P90_SRS for sd in P90_SDS]
    tb = [(h, sr, sd, 9003, 26) for sr in P90_SRS for sd in P90_SDS]
    ra = dict(zip(ta, ex.map(pc.engine_a, ta)))
    rb = dict(zip(tb, ex.map(pc.engine_b, tb)))
    A = {sr: _best({sd: ra[(h, sr, sd, 9001, True, 0.40)] for sd in P90_SDS}) for sr in P90_SRS}
    B = {sr: _best({sd: rb[(h, sr, sd, 9003, 26)] for sd in P90_SDS}) for sr in P90_SRS}
    hold = {sr: ex.submit(pc.engine_a, (h, sr, A[sr][0], 9002, True, 0.40)) for sr in P90_SRS}
    hold = {k: f.result() for k, f in hold.items()}
    print("| SR | A P ± SE (sd) | A pass / bust / running | A sd within 1 pp | A re-est. (new seed) | B P (sd) |")
    print("|---|---|---|---|---|---|")
    for sr in P90_SRS:
        sa, (p, b, r, _), na = A[sr]
        sb, (pb, *_), _ = B[sr]
        print(f"| {sr:g} | {p:.3f} ± {pc.se(p):.3f} ({sa}) | {p:.3f} / {b:.3f} / {r:.3f} | {na[0]}–{na[1]} "
              f"| {hold[sr][0]:.3f} | {pb:.3f} ({sb}) |")
    for name, src in (("A grid", {s: A[s][1][0] for s in P90_SRS}), ("A re-est", {s: hold[s][0] for s in P90_SRS}),
                      ("B grid", {s: B[s][1][0] for s in P90_SRS})):
        for lo, hi in zip(P90_SRS, P90_SRS[1:]):
            if src[lo] < 0.80 <= src[hi]:
                x = lo + (0.80 - src[lo]) / (src[hi] - src[lo]) * (hi - lo)
                print(f"{name}: P = 0.80 at SR ≈ {x:.2f} (between {lo:g}: {src[lo]:.3f} and {hi:g}: {src[hi]:.3f})")


# --- resets -------------------------------------------------------------------------------
RS_SDS = list(range(100, 1801, 50))
RS_SRS = (0.0, 1.0, 2.0, 3.0)


def _resets_cell(task):
    size, h, sr, sd, seed = task
    prog = PROG[size]
    rng = np.random.default_rng(seed)
    mu, s = sr * sd / math.sqrt(252), sd / math.sqrt(payout_sim.SUB)
    left = np.full(N, h); done = np.zeros(N, bool); att = np.zeros(N, int); active = np.ones(N, bool)
    first = None
    while active.any():
        ix = np.where(active)[0]
        o, u, _ = payout_sim.run_phase(rng, prog.ev, len(ix), mu, s, None, None, left[ix].copy(), False)
        att[ix] += 1
        if first is None:
            first = (o == 1).mean()
        done[ix[o == 1]] = True
        active[ix[o != 0]] = False
        left[ix] -= u
        active &= left >= prog.ev.min_days  # a reset starts the next trading day
    fees = prog.price + prog.reset * (att - 1)
    return done.mean(), first, att.mean(), fees.mean(), np.percentile(fees, 95)


def resets(ex):
    tasks = [(z, h, sr, sd, 1000 * z + h) for z in PROG for h in (63, 90) for sr in RS_SRS for sd in RS_SDS]
    r = dict(zip(tasks, ex.map(_resets_cell, tasks)))
    print("| Tier | Days | SR | best sd | P(funded) ± SE | P(1st attempt) | mean attempts | mean fees | p95 fees "
          "| cheapest sd within 1 pp: sd, P, mean fees |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for z in PROG:
        for h in (63, 90):
            for sr in RS_SRS:
                g = {sd: r[(z, h, sr, sd, 1000 * z + h)] for sd in RS_SDS}
                b = max(RS_SDS, key=lambda k: g[k][0]); p = g[b][0]
                c = min((k for k in RS_SDS if g[k][0] >= p - 0.01), key=lambda k: g[k][3])
                print(f"| {z}K | {h} | {sr:g} | {b} | {p:.3f} ± {pc.se(p):.3f} | {g[b][1]:.3f} | {g[b][2]:.2f} "
                      f"| ${g[b][3]:.0f} | ${g[b][4]:.0f} | {c}, {g[c][0]:.3f}, ${g[c][3]:.0f} |")


# --- renewal ------------------------------------------------------------------------------
RN_HMAX = 750
RN_LAMS = (5, 10, 25, 50, 100, 250)


def _renewal_cell(t):
    size, sr, sd = t
    rng = np.random.default_rng(7000 + size)
    o, u, _ = payout_sim.run_phase(rng, PROG[size].ev, N, sr * sd / math.sqrt(252), sd / math.sqrt(payout_sim.SUB),
                                   None, None, np.full(N, RN_HMAX), False)
    return (o == 1).mean(), u.mean(), (o == -1).mean()


def renewal(ex):
    tasks = [(z, sr, sd) for z in PROG for sr in RS_SRS for sd in RS_SDS]
    r = dict(zip(tasks, ex.map(_renewal_cell, tasks)))
    print("max unfinished share at", RN_HMAX, "days (any sd):", max(v[2] for v in r.values()))
    print("| Tier | SR | λ $/day | best sd | p per attempt | L days/attempt | unfinished | E[attempts] | E[fees] "
          "| E[days to funded] |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for z in PROG:
        pr = PROG[z]
        for sr in RS_SRS:
            for lam in RN_LAMS:
                def obj(sd):
                    p, L, _ = r[(z, sr, sd)]
                    return (pr.reset + lam * L) / p
                sd = min((s for s in RS_SDS if r[(z, sr, s)][0] > 0), key=obj)
                p, L, un = r[(z, sr, sd)]
                print(f"| {z}K | {sr:g} | {lam} | {sd} | {p:.3f} | {L:.1f} | {un:.3f} | {1 / p:.1f} "
                      f"| ${pr.price + pr.reset * (1 / p - 1):.0f} | {L / p:.0f} |")


# --- payout -------------------------------------------------------------------------------
PO_H, PO_N, PO_MIN_NET = 500, 8000, 1000
PO_SDE = {100: [400, 600, 800, 1000, 1250, 1500], 50: [250, 400, 550, 700, 850, 1000]}
PO_SDF = {100: [250, 500, 700, 1000, 1400, 2000], 50: [165, 330, 465, 700, 1000, 1400]}
PO_LAMS = (10, 25, 100)


_GAUSS_DAY = payout_sim._day


def _t_day(nu):
    """payout_sim._day with each path-day's sd scaled by sqrt((nu-2)/chi2_nu): unit-variance Student-t days."""
    def day(rng, n, mu, s, stop, take):
        v = np.sqrt((nu - 2) / rng.chisquare(nu, n))[:, None]
        inc = mu / payout_sim.SUB + s * v * rng.standard_normal((n, payout_sim.SUB))
        cum = np.concatenate([np.zeros((n, 1)), np.cumsum(inc, axis=1)], axis=1)
        assert stop is None and take is None  # first_payout is called without stops or takes here
        return cum
    return day


def _payout_cell(t):
    size, sr, se, sf, nu = t
    payout_sim._day = _GAUSS_DAY if nu is None else _t_day(nu)  # module function read by run_phase
    try:
        r = first_payout(PROG[size], sr, se, sd_f=sf, H=PO_H, N=PO_N, seed=size * 100 + int(sr * 10),
                         min_net=PO_MIN_NET)
    finally:
        payout_sim._day = _GAUSS_DAY  # workers persist across sections: never leave Student-t days installed
    return r["p_pay"], r["cost"], r["first_pay"], r["days_med"]


def payout(ex, nu=None):
    tasks = [(z, sr, se, sf, nu) for z in PROG for sr in RS_SRS for se in PO_SDE[z] for sf in PO_SDF[z]]
    r = dict(zip(tasks, ex.map(_payout_cell, tasks)))
    print(f"H={PO_H} days, N={PO_N}, first payout >= ${PO_MIN_NET} net; min P(paid by H) over grid:",
          round(min(v[0] for v in r.values()), 3))
    print("| Tier | SR | λ $/day | eval sd | funded sd | P(paid ≤ H) | E[fees] | E[1st payout | paid] | median days "
          "| cash net | net − λ·days |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for z in PROG:
        for sr in RS_SRS:
            keys = [k for k in tasks if k[0] == z and k[1] == sr]
            for lam in PO_LAMS:
                def score(k):
                    return r[k][0] * r[k][2] - r[k][1] - lam * r[k][3]
                k = max(keys, key=score)
                p, c, fp, md = r[k]
                print(f"| {z}K | {sr:g} | {lam} | {k[2]} | {k[3]} | {p:.3f} | ${c:.0f} | ${fp:.0f} | {md:.0f} "
                      f"| ${p * fp - c:.0f} | ${score(k):.0f} |")


if __name__ == "__main__":
    sections = {"pass90": pass90, "resets": resets, "renewal": renewal, "payout": payout,
                "payout_t4": lambda ex: payout(ex, 4), "payout_t3": lambda ex: payout(ex, 3)}
    chosen = sys.argv[1:] or list(sections)
    with ProcessPoolExecutor(4) as ex:
        for name in chosen:
            print(f"\n## {name}\n")
            sections[name](ex)
