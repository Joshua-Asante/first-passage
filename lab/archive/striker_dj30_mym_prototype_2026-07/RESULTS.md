# Striker DJ30 → MYM v0.1 prototype — Stage-1 edge-preservation RESULTS

**Date:** 2026-07-09
**Pre-registration:** [`docs/ltm/briefs/pre-registration/2026-07-08-striker-dj30-mym-prototype-prereg.md`](../../docs/ltm/briefs/pre-registration/2026-07-08-striker-dj30-mym-prototype-prereg.md) (frozen before this run)
**Scorer:** `score_stage1.py` — reuses the frozen `p2_replay` `e1_ratios`/`score_e1` verbatim, bypassing only the CLI's commission-incompatible `first_trade_sanity` guard (documented in the script header). Gate thresholds and math UNCHANGED.
**Inputs (gitignored, local):** CFD baseline `Striker_DJ30_v4.5_PEPPERSTONE_US30_2026-07-08_f5f5b.csv` (2020–2026, commission-free); MYM v0.1 edition `Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-08_edaa3.csv` (2020–2026, integer/RESERVE sizing + force-flat + $0.61/side + 1-tick slippage). v0.1 = frozen entry + 5 venue deltas, NO exit tuning.

## Verdict: Stage-1 NOT CLEARED (OOS holdout MISS)

| Window | CFD PF | MYM PF | **PF ratio** | net ratio | E1 |
|---|---|---|---|---|---|
| **OOS holdout (2023–2026)** | 3.644 (n=174) | 2.038 (n=172) | **0.559** | 0.246 | **MISS** |
| In-sample cross-check (2020–2022) | 1.772 (n=98) | 2.058 (n=94) | **1.161** | 0.900 | **PASS** |

Gate = both windows PASS (PF ≥ 0.8× AND net ≥ 0.7×). OOS PF ratio 0.559 < 0.8 → **NOT CLEARED.**

**PF ratio is the load-bearing signal; net ratio is confounded** (MYM $0.50/pt + commission + $150K integer basis vs CFD $1/pt + commission-free + %-equity $200K) — per P2 RESULTS Obs #2. The verdict holds on PF alone.

## The informative part — the miss is regime-located, opposite the usual fragility

- **MYM v0.1's PF is regime-STABLE at ~2.0** (2.038 trend / 2.058 chop). The edition itself is a solid, consistent PF-2.0 book that does not lose money.
- The **CFD baseline is regime-VARIABLE** (1.772 chop → 3.644 trend). The trend-regime amplification — a few huge pyramid trend-days — is what makes the CFD exceptional.
- So the miss is **not** MYM breaking down; it is MYM **failing to reproduce the CFD's trend-regime peak** while comfortably beating its chop trough. The 80%-preservation bar is cleared in chop, missed in the strong-trend half.

## Mechanistic attribution (what compresses MYM's PF to ~2.0)

Structural venue costs, largely OUTSIDE the tunable exit layer:
1. **Commission + slippage** ($0.61/side + 1 tick on up to 114-contract pyramid stacks) — a fixed drag; flips marginal base-leg winners to losers (whole-panel WR 72%→45%). Structural.
2. **Force-flat** (14 EOD exits) — truncates the longest afternoon trend-day holds, exactly where the CFD's biggest winners live. Structural (Bulenox requires it).
3. **Integer/RESERVE sizing** — quantizes the pyramid (cap-bound base ≤17 at 150K). Structural.
4. **Trail/BE fit for MYM microstructure** — the ONE lever in the free exit/cost grid.

Only (4) is tunable. Recoverable headroom from 0.559 toward 0.8 is therefore limited — a wider trail could recapture some trend-day amplification, but it cannot undo commission or the force-flat hold cap.

## Disposition — FALSIFIED (operator-accepted 2026-07-09)

**The plan §10 falsifier is ACCEPTED. DJ30's edge does not transfer to MYM within the exit/cost-only constraint.** The v0.1 OOS PF ratio (0.559) misses the 0.8× edge-preservation bar, and the miss is attributed to *structural* venue costs (commission + slippage on 100+ contract stacks, EOD force-flat truncating trend-day holds, integer/RESERVE pyramid quantization) that the pre-registered free grid (BE pad, trail wide) cannot touch. The operator declined to run the Task-4 exit/cost grid (its only lever — trail width — targets ~10% of the gap and cannot undo commission or the force-flat hold cap), accepting the falsifier directly on the structural attribution.

**Consequences:**
- **Task 4 (exit/cost grid) and Task 5 (v0.2 re-score) are NOT pursued.** No v0.2 is authored.
- **Recovering DJ30 on MYM would require entry-signal changes** — i.e. a different strategy, out of this prototype's scope. Re-opening requires a fresh pre-registered question with a NEW mechanism, not a re-tune (the entry was frozen precisely so it could not be overfit to the CME feed).
- **Stage 2 (Bulenox prop-survivability re-MC) is moot** — there is no edge-preserving prototype to carry into it.
- **Separate, still-open (NOT part of this falsified gate):** v0.1 is a regime-stable PF-2.0 futures book in absolute terms. Whether a below-80%-preservation-but-profitable book is worth deploying to Bulenox is a *different* question that would need its own pre-registered gate (this one was edge-preservation, and it answered no).

**Program note:** DJ30 was the strongest prop-rebuild candidate (conditionally-alive per P2; base transferred at 0.85×). Its falsification on structural venue costs is a strong prior that the exit-only rebuild path faces the same cost wall for the other legs — relevant to whether NAS100→MNQ / Aegis→6J are worth attempting under the same constraint. Not a unilateral closure of those; a signal to weigh before spending on them.
