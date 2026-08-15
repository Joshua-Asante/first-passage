# RATES-EV-ZF-1 Phase-0 RESULTS — native ZF, CPI+NFP-conditioned event-anchored ORB

**Verdict: CLOSED — FALSIFIED at Phase-0 (P0.2 cost-law + P0.4 power both fail; the instrument-choice and decorrelation theses both VALIDATED, but no usable edge survives realistic cost). Closes the rates-event 2×2 matrix fully dead.**

**Scoping brief:** [`docs/briefs/rnd-pipeline/RATES-EV-ZF-1-conditional-event-breakout-scoping.md`](lab/archive/../../docs/briefs/rnd-pipeline/RATES-EV-ZF-1-conditional-event-breakout-scoping.md)
**Run:** 2026-07-21 · `run_phase0.py` (K=0 δ-extraction, pre-committed PRIMARY+SECONDARY K_intrinsic=2 design, not a registered search) · operator GO recorded (§8).
**Engine:** `orb_universe_2026-06-22/orb_lib.py` `orb_backtest` / `placebo_within_day` reused **verbatim** (calibration-pinned); only the loader (native ZF), the `Instrument` economics, the OR-anchor shift (08:30 ET release, not 09:30 ET cash open), and a day-filter to the pre-committed event calendar are new.
**Data:** native `ZF.v.0` continuous 1m (Databento GLBX.MDP3, pull `$0.00`, `ohlcv-1m_continuous_3af3c763cfcedd61.dbn`, 2,408,647 rows). Event calendar: **179 CPI+NFP events (89 NFP + 90 CPI, 0 same-day collisions)**, primary-sourced from `bls.gov/schedule/{2019..2026}/home.htm` via browser (WebFetch 403s bls.gov — memory `reference_bls_release_date_sourcing`), **not** a first-Friday/mid-month heuristic. Median close **110.28** — valid 5Y-note price.

---

## A real finding on the calendar itself, before any market data

Sourcing the calendar directly from BLS's per-year schedule pages surfaced and confirmed the **2025 government-shutdown gap** the memory had already flagged from a different investigation: the **October-reference-month release was never published** for either NFP or CPI. September-data NFP was delayed to **2025-11-20** (a Thursday, not the shutdown-shift's own Friday convention); the next NFP row is "for November 2025" on **2025-12-16** (Tuesday) — there is no "for October 2025" row anywhere. Same gap, same shape, for CPI (September-data delayed to Oct-24; no October-data row; November-data on Dec-18). The 2026-02-11 (Wednesday, not Friday) date also reproduced exactly as the memory predicted. This corroborates the source is reliable and the memory's warning was correct — a first-Friday heuristic would have fabricated non-existent October 2025 events and mis-timed the delayed September ones.

## P0.1 — event-day range geometry: the instrument-choice thesis is VALIDATED

| | Value |
|---|---|
| n event-day breakouts formed | 143 (of 178/179 event days present in the panel) |
| median event-day OR range | 0.2969 pt (38.0 ticks) |
| median-range/RT-headline ratio | **17.62:1** |
| ZB unconditional benchmark (this morning) | 4.3:1 |

ZF really does offer materially better cost geometry on event days than ZB offers unconditionally — **>4× better**. The tick-geometry rationale for choosing ZF over ZB/ZN held up under measurement, not just the a priori CME-spec arithmetic.

## P0.2/P0.4 — PRIMARY: cost-law and power both FAIL

| Quantity (n=143) | Value |
|---|---|
| mean GROSS edge | **+0.1033 R** (t **+1.45** — not significant) |
| HEADLINE cost_R 0.0895 → 4× hurdle 0.358 | ratio **1.15×** → **KILL** |
| 0-slip (commission-only) cost_R 0.0065 → 4× hurdle 0.0259 | ratio **15.94×** → **PASS** |
| net-of-cost meanR | +0.0138 (t +0.20), WR 0.503, PF 1.049 |
| **P0.4 power** (Req-4) | **0.3047** vs bar 0.50 → **FAIL** |

The edge clears cost trivially at an unrealistic zero-slip commission-only floor, but **fails the realistic headline convention by a wide margin** (1.15× vs the 4.0× bar) — the gross edge (t=1.45) is not distinguishable from noise at this N, and what little there is gets consumed by execution cost the moment slippage is modeled. This is the opposite failure shape from D5/H-OD-1 (which had *significant*, cost-walled edges) — here the edge itself is marginal before cost is even applied.

## Structural placebo — informative, not a rescue

Within-day OR-window placebo (event days only): obs meanR +0.0138, **placebo p = 0.0010**, placebo mean **−0.3913**. This says something real: on event days, breakouts at *arbitrary* intraday windows are **strongly negative** (matching this morning's unconditional ZB fade-finding), while the actual 08:30 OR window is merely **flat** rather than deeply negative. The OR window is "the least bad" window on event days too — informative about mechanism (some event-day mean-reversion dominates except right at the release), but a flat PRIMARY is still not a tradeable edge.

## P0.3 — SECONDARY (informational, never gating): no rescue, mildly negative

Top-half-by-OR-range subcohort (n=60, the higher-surprise-magnitude days): mean gross **+0.0236 R** (t +0.38), ratio 0.74× (fails), net-of-cost **−0.0081** (PF 0.951). If anything the largest-range days are *slightly worse* net — the "informed high-surprise days carry it" story does not hold up.

## Per-year — alternates, same tell as NG

```
2019 +0.059   2020 -0.165   2021 +0.276   2022 -0.050
2023 +0.104   2024 -0.224   2025 +0.118   2026 -0.199
```

Sign alternates almost every year — the same noise signature that killed NG-EIA-1, reinforcing that neither result is an artifact of one candidate's specific construction.

## P0.5 — decorrelation pre-flight: VALIDATED cleanly

Zero-padded daily-$ series (143 event trades against 2,346 total calendar days — **6.1%** in-market): daily-$std at the 0.37%/$100K reference weight = **$76.31**. **ρ = $76.31 / $273 = 0.280** — comfortably under the 1.0 presumptive-reject line, honestly computed (not the always-in-market convention that would have overstated it). The "sparse by construction" decorrelation thesis from the scoping brief's §1 held up exactly as argued — the problem here is not variance-dominance (unlike ORB-MNQ-1), it's that there's no edge worth adding in the first place.

## Disposition — third of three distinct directional constructs on the Treasury complex, zero survivors

| Instrument | Construct | Verdict | Failure mode |
|---|---|---|---|
| ZN | auction-day drift (H-ZNAUC-1) | dead (prior session) | δ 1.01bp, sub-cost by 6–10× |
| ZB | unconditional intraday breakout (ORB-ZB-1) | dead (this session, AM) | negative gross edge — Treasuries fade the OR |
| **ZF** | **conditional (CPI/NFP) intraday breakout** | **dead (this result)** | **geometry + decorrelation validated; edge itself sub-cost + underpowered** |

Honest scope note: CL-EIA/F-B is an *adjacent* informed-flow precedent on a **different instrument** (crude oil, not the Treasury complex) — not a fourth rates-instrument cell. A fixed-hold conditional-drift construct (release-anchored, no breakout/stop structure) has never itself been run on a Treasury instrument and is not claimed dead here. Mean-reversion/fade is also untested at this resolution (the MICRO10Y/2YY entry in `rejected_candidates.md` was a **daily-proxy chop-native** fade on yield futures, not a native-intraday fade on ZB/ZN/ZF price futures) — though the placebo evidence here and in ORB-ZB-1 (arbitrary-window breakouts strongly negative on both) weakly favors a fade in sign, that is not the same as a measured result.

- **CLOSED — FALSIFIED.** K = 0 consumed (the pre-committed PRIMARY+SECONDARY design never opened `register_search`); Treasury-complex family bank stays **0**. Databento spend **$0.00**.
- Append to [`docs/rejected_candidates.md`](lab/archive/../../docs/rejected_candidates.md) — `conditional event-anchored ORB on ZF`, class edge-failure (marginal gross edge, fails realistic cost, underpowered) — NOT venue/cost-geometry (that limb passed) and NOT a decorrelation failure (that limb passed too). **Tail-methodology-exhaustion per INQHIORI §6** (3 directional Treasury-complex constructs sharing the same parent question and analysis level, all dead) — not a formal domain-SNAG closure (that bar in `rejected_candidates.md` is calibrated to ~17–22 candidates); a 4th directional construct at this level needs the question reformulated, not just a new instrument/window.
- No `core/` / allocation / `dd_protection` / `ACTIVE_FIRM` / Pine touch. Lock HELD.

## Reproduce

```bash
PYTHONIOENCODING=utf-8 .venv-research/Scripts/python.exe lab/archive/rates_ev_zf_recon_2026-07/run_phase0.py
```
