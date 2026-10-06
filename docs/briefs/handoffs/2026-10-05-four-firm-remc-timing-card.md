# CC handoff — four-firm re-MC §8 step 2(d): synthetic timing for I-15

**Date:** 2026-10-05.
**Status:** FROZEN for execution, 2026-10-05. Joshua directly: "go on the timing card".
**Brief type:** CC handoff, bounded measurement (worker card).
**Authority:** operator go, 2026-10-05, to a coordinator (4) worker. Requirement owner: the four-firm dated re-MC prereg ([PR #616](https://github.com/Joshua-Asante/first-passage/pull/616) at `678b5d7`), I-15 (budget cap of one executor session, figure from a synthetic same-shape timing) and §8 step 2(d).
**Rule:** synthetic inputs only, as prereg §R allows for harness work. No candidate, export, reference or venue datum enters the timing.
**Return boundary:** a wall-clock figure for I-15 with its method, or a precise blocker. No real run, no code merge, no prereg freeze.

## §0 — Production reads (`main@bf46e8f`, 2026-10-05)

| Surface | Finding |
|---|---|
| `lab/discovery/prop_survivor_scoring.py` `run_tier_remc` (:577), `score_candidate` (:652), `assert_intraday_channel_nonvacuous` (:497) | Each tier reaching G4 runs: the guard's three arms (EOD, zeros, real); then Run-1 (consistency off); then Run-2 when the tier has eval consistency. Bulenox has no consistency rule, so Run-2 = Run-1 (`run1_degenerate`). Each arm is 3 seeds × `n_sims`, at horizon 1500. |
| v2 G4; prereg I-6 | 10,000 sims × seeds 42/123/2026, horizon 1500. |
| Prereg I-20 | The calibration reference runs once, through the same harness, in the same session. |
| [identity ledger](../phase3-preparation/2026-09-15/identity-ledger.md) :180 | The accepted references cover 2022-09-01..2026-09-03, about 1,045 weekdays. This is the series shape. |

## §0.5 — Clarifications resolved at freeze

1. **Arm count per run:**
   - Candidate: 4 tiers × (3 guard arms + Run-1) + 3 Run-2s = **19 arms**.
   - Reference: the same, **19 arms**.
   - Total: **38 arms**.
   - The O-8 mode-switching code adds one channel choice per day. Budgeted at ×1.5 until measured; measured at ×1.18 ([PR #708](https://github.com/Joshua-Asante/first-passage/pull/708)) and carried as ×1.2.
2. **Shapes:**
   - *worst*: zero P&L and zero low, so no path busts or passes and every path runs the full 1,500 days. This is an upper bound.
   - *typical*: synthetic N(0, 300) daily P&L, low = min(0, P&L) − 150.
   - The real book's paths end at pass or bust, so its runtime falls between the two.
3. **Timing harness:** a standalone script, reproduced in §10. It calls `paired_blocks_from_daily` and `run_tier_remc` with the Run-2 consistency setting and the intraday channel on. It is not committed as code.

## §1 — Goal

A per-arm wall-clock figure at 10k sims for both shapes, and from it the I-15 cap for one executor session.

## §4 — Hypothesis and falsifier

**H:** arm time is linear in `n_sims`. The 500-sim to 10k-sim ratio is within ±25% of 20.

**Falsified by** a ratio outside that band. The cap is then taken from direct 10k measurements only.

## §5 — Constraints and forbidden moves

- No real input, no `score_candidate` on real data.
- No edit to `lab/`, `core/` or `ops/`; no prereg edit by the executor.

## §6 — Acceptance and return taxonomy

**DONE** requires:
- the per-tier arm times at 500 and 10k (typical), and at 500 (worst) plus one 10k worst tier;
- the derived session figure;
- the machine (CPU count) and the launcher Python.

**DONE_WITH_CONCERNS** if the figure stands with a disclosed limitation. Otherwise **NEEDS_CONTEXT** or **BLOCKED**, with the obstruction.

```yaml authority
seat: worker
parent: docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push, pr.open]
constraints:
  - no_main_write
  - no_merge
  - synthetic_inputs_only
  - no_private_source_read
  - no_code_edit
  - no_prereg_or_owner_record_edit
acceptance:
  - per_arm_times_and_session_figure_recorded
```

## §7 — Return

**DONE (2026-10-06).** Machine: 8 logical CPUs, Windows 11, launcher Python (`fp.py`). One process per run.

| Shape | n_sims | Bulenox | Tradeify | MFFU | BluSky |
|---|---|---|---|---|---|
| typical | 500 | 4.31 s | 4.48 s | 4.21 s | 4.64 s |
| typical | 10,000 | 93.07 s | 79.77 s | 87.45 s | 94.49 s |
| worst | 500 | 48.38 s | 49.39 s | 53.50 s | 46.75 s |
| worst | 10,000 | — | — | 1005.43 s | — |

- **H holds.** The 500 → 10k ratio is 18.8–21.6 (worst MFFU 18.8; typical 17.8–21.6, inside ±25% of 20).
- **Mode-switching overhead:** worst MFFU at 500 sims ran 41.16 s → 48.61 s with protected channels (PR #708), ×1.18, carried as ×1.2.
- **I-15 figure.** 38 arms (§0.5 item 1) at ×1.2:
  - Worst-case bound: 38 × 1005 s × 1.2 ≈ **12.7 h serial**. With 8 arm processes in parallel (arms are seed-deterministic and independent), 5 waves × 1206 s ≈ **1.7 h**.
  - Typical shape: about **1.2 h serial**.
- The real book's paths end at pass or bust, so the expected time is well under the bound.

## §10 — Audit hooks

```bash
c=docs/briefs/handoffs/2026-10-05-four-firm-remc-timing-card.md
# The return records a session figure (expect ≥ 1 line).
grep -c "I-15 figure" "$c"
```

Timing script (synthetic only; run as `python -I scripts/fp.py python remc_timing.py N_SIMS worst|typical [TIER...]`):

```python
import json, sys, time
import numpy as np
sys.path[:0] = ["lab", "core"]
from discovery.prop_survivor_scoring import (
    _consistency_frac, load_scoring_thresholds, paired_blocks_from_daily, run_tier_remc)
n_sims, shape = int(sys.argv[1]), sys.argv[2]
n_days = 1045
rng = np.random.default_rng(20261005)
if shape == "worst":
    pnl = np.zeros(n_days); low = np.zeros(n_days)
else:
    pnl = rng.normal(0.0, 300.0, n_days); low = np.minimum(0.0, pnl) - 150.0
blocks, lows = paired_blocks_from_daily(pnl, low)
thr = load_scoring_thresholds()
out = {"n_sims": n_sims, "shape": shape, "tiers": {}}
for tier in (sys.argv[3:] or thr.tier_keys):
    t0 = time.perf_counter()
    run_tier_remc(tier, blocks, thr, n_sims=n_sims,
                  consistency=_consistency_frac(tier), intraday_blocks=lows)
    out["tiers"][tier] = round(time.perf_counter() - t0, 2)
print(json.dumps(out))
```
