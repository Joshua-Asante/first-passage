# RESULTS — four-firm dated re-MC (§4 falsifier), candidate (A) Class-S #3

**Status:** ACTIVE (verdict assigned; recording at the owner is pending).
**Pre-registration (frozen):** [`docs/briefs/pre-registration/2026-10-02-four-firm-dated-remc-prereg-DRAFT.md`](../../../../docs/briefs/pre-registration/2026-10-02-four-firm-dated-remc-prereg-DRAFT.md) (`FROZEN 2026-10-05`, merged `bfb13f9`).
**Gate of record:** [`docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md`](../../../../docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md).
**Executor card:** [`docs/briefs/handoffs/2026-10-06-four-firm-remc-executor-card.md`](../../../../docs/briefs/handoffs/2026-10-06-four-firm-remc-executor-card.md) (merged `196ae62`). **Script:** [`run_four_firm_remc.py`](run_four_firm_remc.py) at `81e7dcb`.
**Run date:** 2026-10-06. Prep 16:28Z; scoring started 16:29Z; the reference finished 16:44Z and the candidate 16:52Z. Operator go: "go on the run".
**Start gate (I-17):** `main` read `5d25f9cfc1e8ff00bacda45478322f9858176e8b`. #708 merge `debc13363ff3b85ed5ee41bca97a0ae9d76c5767` is an ancestor, so the branch is **ON** (mode-switching).

## Verdict (prereg §4, assigned mechanically)

**FALSIFIED — early-fail.** No tier clears Part A. AMBIGUOUS does not fire, and no INSUFFICIENT trigger holds.

- **Per-run disposition** (prereg §4): the candidate closes and the early-fail branch arms, so any subsequent candidate needs fresh operator authorization.
- **Not a discharge:** prereg §4 stays undischarged.
- **Program demotion** is the separate check at 2026-11-08 (prereg §4 "Program level"); this run does not decide it.

## Candidate (A): per tier, intraday-honest clock, mode-switching ON

Each tier ran on its own cost-netted series (I-19) at 10,000 sims × seeds 42/123/2026, horizon 1500. Part A requires bust ≤ 5.0% and P(pass) ≥ 50% on the gating run.

| Tier | Run-1 bust | Run-1 P(pass) | Run-2 bust | Run-2 P(pass) | Gating run | Clears Part A | Notes |
|---|---|---|---|---|---|---|---|
| Bulenox_100K | 25.28% | 74.72% | — | — | Run-1 (no consistency) | no | F2 optimistic label |
| Tradeify_Select_100K | 29.54% | 70.46% | 36.08% | 63.92% | Run-2 | no | |
| MFFU_Rapid_100K | 29.82% | 70.18% | 32.66% | 67.34% | Run-2 | no | **I-24 inadmissible** (positions open past 16:10 ET on 403 days); could not clear in any case |
| BluSky_Premium_100K | 27.35% | 72.65% | 34.68% | 65.32% | Run-2 | no | F2 optimistic label |

- **G1:** `DEPLOYABLE-DEFAULT-ENVELOPE: YES`. `R_deploy` is 2,209 round trips (Aegis 120, Striker 199, Vanguard 326, ORB 1,564).
- **G2 per leg (candidate #1 §8 via I-22):** every leg passes on every tier, so no tier is G2-killed.
- **Report:** `breach_clock = intraday_honest`, `gate_grade = true`; every tier's non-vacuity guard ran.
- **Funded-ruin diagnostic (G7):** 0 tiers at ≤ 1.0%.

## Calibration reference (I-20), same harness and clock, protection OFF

| Tier | Run-1 bust | Run-2 bust | Gating bust | ≤ 5.0%? |
|---|---|---|---|---|
| Bulenox_100K | 53.10% | — | 53.10% | no |
| Tradeify_Select_100K | 54.60% | 75.77% | 75.77% | no |
| MFFU_Rapid_100K | 54.42% | 67.57% | 67.57% | no |
| BluSky_Premium_100K | 53.10% | 78.33% | 78.33% | no |

AMBIGUOUS needs ≥ 2 tiers at ≤ 5.0%; there are 0, as predicted in I-20. Reference `gate_grade = true`.

## Disclosures

1. **Window:** 2022-09-08 → 2026-08-05 (1,020 weekdays) starts on a **Thursday**. `paired_blocks_from_daily` blocks positionally, so the weekly blocks are 5 consecutive business days, Thursday to Wednesday. Recorded, not trimmed (card §0.5 item 3).
2. **Launch:** both scoring stages were first started as session background tasks, which this tool caps at 2 h. They were stopped and relaunched as detached processes about a minute later, before any report existed. Nothing was read or re-run in place.
3. **Run evidence:** the launcher writes `record.json` only for pytest runs. Completion evidence for these stages is the two report files, each with its "report written" log line, plus the digests below. The pre-run synthetic smoke covered every stage.
4. **Median days-to-pass** is not emitted by `score_candidate`'s report schema. It is not needed for this verdict, because the bust gate fails on every tier.
5. **Reference:** it bypassed G1/G2 so that it would reach a bust read on every tier (card §0.5 item 5). Its trades are net of costs as exported.
6. **I-21 regime rider:** not run; it applies only on RESOLVED.
7. **Named approximations** (prereg I-17, O-4): continuous daily-series construction, the coincident-sum intraday low (conservative), and no capacity or takeover modelling.

## Provenance: run of record and verdict re-derivation

- **Run of record:** executor `81e7dcb`; RESULTS `b2d6c93`; the reports and digests below, including the original `verdict.json`. These stay the run of record.
- **Correction (#715 Codex review 5433545406):**
  - The executor was repaired at `a8f21c6`. Its verdict derivation now selects each tier's gating run by tier semantics and requires both mandatory runs, `gated_on` and the v2 depth (r4199556582). Its re-hash verifies the manifest bytes before parsing them (r4199556590).
  - The repaired `derive_verdict` was run over the **existing** reports only; the Monte Carlo was not re-run. Its output went to a separate file, `verdict_rederived.json`.
  - **Result: identical.** The verdict, clears, INSUFFICIENT reasons, reference busts and AMBIGUOUS flag all match the original. The digests of `prep.json`, both reports and `verdict.json` are unchanged by the re-derivation.
  - The re-hash fix affects the pre-run gate only. This run's start re-hash had already matched 20/20.

## Private artifacts (gitignored; cited by SHA-256)

Root: `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts/four-firm-remc-run-2026-10-06/`

| File | SHA-256 |
|---|---|
| `prep.json` | `feefa7ab28ff17d8b1a727bae0adf6656369a4ea73eafea2218cdafbd8f4c3b5` |
| `candidate_report.json` | `4076857777e67cedd5755ba637693ce45638357a8a5b1fb17077e63ac28ec2ed` |
| `reference_report.json` | `a8e9fd665a6f21d0620b1903d4175c1276907331bb126ff3045a9bbf5fbd333f` |
| `verdict.json` | `5a9b9eaf437100fb7e8a54bf5af0fefbbe12eeb3aa6af0c98720a271787adc28` |
| `verdict_rederived.json` (repaired executor, re-derivation only) | `a21a2ec7e42b97148e4ce857430c38cd230eecc7c31ce7dcb6f83341626b7216` |

The re-hash at start was 20/20 against the prereg §1a / I-20 pins.
