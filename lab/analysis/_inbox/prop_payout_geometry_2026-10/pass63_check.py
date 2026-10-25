"""Independent check of the Select 100K pass-within-63-days requirement curve.

Synthetic Gaussian strategies only: daily P&L ~ N(SR*sd/sqrt(252), sd^2); no strategy
data, no account state. Two engines, each searched over sd = $200..$1,800 in $100 steps
with common random numbers across sd (one draw per horizon, rescaled per cell):

  A  core.mc.simulation.simulate_path with firm_kwargs("Tradeify_Select_100K",
     consistency=0.40), dd protection inert, intraday_low = exact Brownian-bridge
     minimum of each day given its close (generated here).
  B  payout_sim.run_phase on the Select eval Phase from programs.py (26 discrete
     intraday steps), single attempt, no resets, days_left = horizon.

Reproduce (fixed seeds; worker count does not change results):
  python -I scripts/fp.py python lab/analysis/_inbox/prop_payout_geometry_2026-10/pass63_check.py
"""
import math
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "core"))
sys.path.insert(0, str(HERE))
import payout_sim  # noqa: E402
from mc.preflight import firm_kwargs  # noqa: E402
from mc.simulation import simulate_path  # noqa: E402
from programs import tradeify  # noqa: E402

N = 20_000
SDS = list(range(200, 1801, 100))
SRS = {63: [0.0, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0], 126: [0.0, 1.0, 2.0, 3.0]}
SEED_A = {63: 6301, 126: 12601}       # engine A grid draw (shared by every SR and sd)
SEED_A_HOLD = {63: 6302, 126: 12602}  # engine A independent re-estimate at the chosen sd
SEED_B = {63: 6303, 126: 12603}       # engine B grid (rng re-seeded per cell = CRN over sd)
SEED_B_HOLD = {63: 6304, 126: 12604}
CLAIM = {0.0: (0.151, 900), 1.0: (0.248, 700), 1.5: (0.312, 600), 2.0: (0.388, 600),
         2.5: (0.465, 600), 3.0: (0.542, 600), 4.0: (0.699, 500)}
SELECT_EVAL = tradeify(100)["TFY Select Flex 100K"].ev
FINE_SUB = 390  # one-minute steps over a 6.5 h session, engine B granularity check


def draws(seed, h):
    rng = np.random.default_rng(seed)
    z = rng.standard_normal((N, h))
    u = 1.0 - rng.random((N, h))  # (0, 1], so log(u) is finite
    return z, u


def bridge_min(close, sd, u):
    """Minimum of a Brownian bridge from 0 to `close` with variance sd^2 over the day.

    Inverts P(min <= m | close) = exp(-2 m (m - close) / sd^2), m <= min(0, close).
    The bridge minimum does not depend on the drift, only on the close.
    """
    m = 0.5 * (close - np.sqrt(close * close - 2.0 * sd * sd * np.log(u)))
    return np.minimum(m, 0.0)  # exact value is <= 0; simulate_path rejects positives


def engine_a(task):
    h, sr, sd, seed, intraday, cons = task
    z, u = draws(seed, h)
    close = sr * sd / math.sqrt(252) + sd * z
    low = bridge_min(close, sd, u) if intraday else None
    kw = firm_kwargs("Tradeify_Select_100K", consistency=cons)
    counts = {"pass": 0, "bust_trailing": 0, "horizon_cap": 0}
    for i in range(N):
        outcome, _, _, _ = simulate_path(
            close[i][:, None], 1.0, 1.0, h,
            intraday_low=None if low is None else low[i], **kw)
        counts[outcome] += 1  # KeyError on any other bucket: none should occur here
    return counts["pass"] / N, counts["bust_trailing"] / N, counts["horizon_cap"] / N


def engine_b(task):
    h, sr, sd, seed, sub = task
    payout_sim.SUB = sub  # module constant read by _day; set on every call
    rng = np.random.default_rng(seed)
    out, _, _ = payout_sim.run_phase(rng, SELECT_EVAL, N, sr * sd / math.sqrt(252),
                                     sd / math.sqrt(sub), None, None, np.full(N, h), False)
    return (out == 1).mean(), (out == 0).mean(), (out == -1).mean()


def se(p):
    return math.sqrt(p * (1 - p) / N)


def bridge_selfcheck():
    """P(daily low <= -a) against the closed form for drifted Brownian motion."""
    rng = np.random.default_rng(99)
    sd, mu, a = 1.0, 0.1, 1.0
    close = mu + sd * rng.standard_normal(1_000_000)
    hit = (bridge_min(close, sd, 1.0 - rng.random(1_000_000)) <= -a).mean()
    phi = lambda x: 0.5 * math.erfc(-x / math.sqrt(2))  # noqa: E731
    exact = phi((-a - mu) / sd) + math.exp(-2 * mu * a / sd ** 2) * phi((-a + mu) / sd)
    return hit, exact


def best(grid):
    """grid: {sd: (p, bust, run)} -> (sd*, row, sds within 1 pp of the max)."""
    sd_star = max(SDS, key=lambda s: grid[s][0])
    top = grid[sd_star][0]
    near = [s for s in SDS if grid[s][0] >= top - 0.01]
    return sd_star, grid[sd_star], (min(near), max(near))


def main():
    workers = min(4, os.cpu_count() or 1)
    with ProcessPoolExecutor(workers) as ex:
        res = {}
        for h, srs in SRS.items():
            tasks_a = [(h, sr, sd, SEED_A[h], True, 0.40) for sr in srs for sd in SDS]
            tasks_b = [(h, sr, sd, SEED_B[h], payout_sim.SUB) for sr in srs for sd in SDS]
            ra = dict(zip(tasks_a, ex.map(engine_a, tasks_a)))
            rb = dict(zip(tasks_b, ex.map(engine_b, tasks_b)))
            res[h] = {}
            for sr in srs:
                ga = {sd: ra[(h, sr, sd, SEED_A[h], True, 0.40)] for sd in SDS}
                gb = {sd: rb[(h, sr, sd, SEED_B[h], payout_sim.SUB)] for sd in SDS}
                res[h][sr] = {"A": best(ga), "B": best(gb)}
        # Diagnostics, all at the sd chosen above.
        diag = {}
        for h, srs in SRS.items():
            for sr in srs:
                sa = res[h][sr]["A"][0]
                sb = res[h][sr]["B"][0]
                diag[(h, sr, "A_hold")] = ex.submit(engine_a, (h, sr, sa, SEED_A_HOLD[h], True, 0.40))
                diag[(h, sr, "B_hold")] = ex.submit(engine_b, (h, sr, sb, SEED_B_HOLD[h], payout_sim.SUB))
                if h == 63:
                    diag[(h, sr, "A_cons_off")] = ex.submit(engine_a, (h, sr, sa, SEED_A[h], True, None))
                    diag[(h, sr, "A_eod_same_sd")] = ex.submit(engine_a, (h, sr, sa, SEED_A[h], False, 0.40))
                    diag[(h, sr, "B_fine")] = ex.submit(engine_b, (h, sr, sa, SEED_B_HOLD[h], FINE_SUB))
        diag = {k: f.result() for k, f in diag.items()}
        # EOD-only breach, own sd search (engine A, 63 days).
        tasks_e = [(63, sr, sd, SEED_A[63], False, 0.40) for sr in SRS[63] for sd in SDS]
        re_ = dict(zip(tasks_e, ex.map(engine_a, tasks_e)))
        eod = {sr: best({sd: re_[(63, sr, sd, SEED_A[63], False, 0.40)] for sd in SDS})
               for sr in SRS[63]}

    hit, exact = bridge_selfcheck()
    print(f"bridge self-check P(low<=-1sd | mu=0.1sd): sim {hit:.4f} vs closed form {exact:.4f}"
          f" (SE {math.sqrt(exact * (1 - exact) / 1e6):.4f})")
    print(f"N={N} paths per cell; sd grid ${SDS[0]}..${SDS[-1]} step $100; payout_sim.SUB="
          f"{payout_sim.SUB}\n")

    for h in SRS:
        print(f"### Horizon {h} trading days: P(pass) at the best sd\n")
        hdr = "| SR | claim P (sd) " if h == 63 else "| SR "
        print(hdr + "| A simulate_path P ± SE (sd) | B payout_sim P ± SE (sd) | B − A "
              + ("| A − claim | B − claim |" if h == 63 else "|"))
        print("|---" * (6 if h == 63 else 4) + "|")
        for sr in SRS[h]:
            sa, (pa, _, _), _ = res[h][sr]["A"]
            sb, (pb, _, _), _ = res[h][sr]["B"]
            row = f"| {sr:g} "
            if h == 63:
                row += f"| {CLAIM[sr][0]:.3f} ({CLAIM[sr][1]}) "
            row += (f"| {pa:.3f} ± {se(pa):.3f} ({sa}) | {pb:.3f} ± {se(pb):.3f} ({sb}) "
                    f"| {pb - pa:+.3f} ")
            if h == 63:
                row += f"| {pa - CLAIM[sr][0]:+.3f} | {pb - CLAIM[sr][0]:+.3f} "
            print(row + "|")
        print(f"\n### Horizon {h}: outcome split at the best sd, plateau, independent re-estimate\n")
        print("| SR | A pass / bust / running | A sd within 1 pp | A re-est. (new seed) "
              "| B pass / bust / running | B sd within 1 pp | B re-est. (new seed) |")
        print("|---|---|---|---|---|---|---|")
        for sr in SRS[h]:
            _, (pa, ba, ra_), na = res[h][sr]["A"]
            _, (pb, bb, rb_), nb = res[h][sr]["B"]
            ha = diag[(h, sr, "A_hold")][0]
            hb = diag[(h, sr, "B_hold")][0]
            print(f"| {sr:g} | {pa:.3f} / {ba:.3f} / {ra_:.3f} | {na[0]}–{na[1]} | {ha:.3f} "
                  f"| {pb:.3f} / {bb:.3f} / {rb_:.3f} | {nb[0]}–{nb[1]} | {hb:.3f} |")
        print()

    print("### Horizon 63: mechanism checks (engine A unless named)\n")
    print("| SR | A at sd* | consistency off, same sd | EOD-only breach, same sd "
          "| EOD-only, own best sd | B at sd*, 390 steps/day (new seed) |")
    print("|---|---|---|---|---|---|")
    for sr in SRS[63]:
        sa, (pa, _, _), _ = res[63][sr]["A"]
        co = diag[(63, sr, "A_cons_off")][0]
        es = diag[(63, sr, "A_eod_same_sd")][0]
        se_sd, (pe, _, _), _ = eod[sr]
        bf = diag[(63, sr, "B_fine")][0]
        print(f"| {sr:g} | {pa:.3f} ({sa}) | {co:.3f} ({co - pa:+.3f}) | {es:.3f} ({es - pa:+.3f}) "
              f"| {pe:.3f} ({se_sd}; {pe - pa:+.3f}) | {bf:.3f} ({bf - pa:+.3f}) |")


if __name__ == "__main__":
    main()
