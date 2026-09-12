# Track B — final-validation pre-registration for the Tradeify portfolio (DRAFT — NOT FROZEN)

**Status:** DRAFT · 2026-09-12 · packet TB-P1 of the [Track B umbrella](../handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md) · **nothing here is frozen** — every field marked `OWED-BY: TB-F1` is filled and frozen only by TB-F1 after wave 2 merges, TB-C1 merges and the [TB-P2 admission ADR](../../adr/2026-09-12-tradeify-book-protection-instance-admission.md) is ratified · authorizes nothing ($0 · K=0)
**Parent:** [governing plan](../../superpowers/plans/2026-09-02-seven-strategy-tradeify-select-configuration.md) (accepted boundaries, S1/S2, Task 3/Task 5) · [campaign record](../programs/2026-09-03-seven-strategy-select-campaign-state.md) §25a (D28), §28b (D31), §38 (D32), §41 (D33), §55 (D-B1..D-B15), §56 (O-1, O-5..O-9) · [acceptance record](../../notes/2026-09-10-tradeify-protection-selection.md) · [evaluation order](../../adr/2026-08-30-evaluation-order.md) (standing order; this contract is campaign-specific and cites it)
**Companion drafts:** [ORB R2 supersession skeleton](../../adr/2026-09-12-orb-mnq-r2-supersession-DRAFT.md) · [TB-S2 replay spec](../../spec/2026-09-12-tradeify-synchronized-replay-spec.md) · [TB-S3 rail spec](../../spec/2026-09-12-c1-multi-leg-rail-extension-spec.md) · [snapshot-seal contract](../../spec/2026-09-12-tradeify-account-snapshot-seal-contract.md) · [TB-R2 read](../../notes/2026-09-12-track-b-scaling-faithfulness-read.md)

## 0 — Rule 0 reads (anchors at `origin/main @ c41e2be`, 2026-09-12)

Governing plan `@ 3c439f7` lines 69–137 (boundaries; S1: one-sided 95 % lower bound on P(T ≤ 200 business days) ≥ 0.50 on the full n3 sample, T = ∞ for failed or unresolved attempts; S2: n3 after parity and the fresh snapshot, immediately before the deployment decision), 218–262 (Task 3 freeze fields; "the old equal-q three-limb `q**3` calculation is insufficient"), 294–316 (Task 5) · campaign §25a (the decision bound rests on an independent stage-2 sample; a stage-1 screen contributes nothing to the bound), §28b (n3 on a third disjoint seed stream; `N_conf ≥ 59` waived), §38 (overlap-keyed DD limb), §41 (one attempt; a failed n3 ends the attempt; no runner-up), §7 prerequisite block · `scripts/certification_power.py` `@ 5e5a216` + this packet's additive speed-limb mode (below) · `tests/test_certification_power.py` (`--limbs 3` = full/H1/H2, not n1/n2/n3) · acceptance record lines 55–69 (the selection evidence is unregistered exploratory analysis; native ORB no-add exits and integer sizing were the open validation questions) · ORB ADR `@ 770413b` §2, §4 R2/R3, §5 · campaign D20-c · `phase1_config.json` `@ 9f69e94` (roll policy `ACCEPTED_UNMODELED`, two obligations) · `cme_early_close_calendar.json` (`coverage_start 2022-09-01`, `coverage_end 2026-09-02`, 40 rows).

## 1 — The object under test (fixed; by reference, never restated with values)

- **Catalogue K = 1:** the Tradeify portfolio — `aegis_6j` (sell-only, fixed 8), `dj30_mym_p250` (buy-only, risk ladder), `vanguard_mgc` (buy-only, adapter ladder), `orb_mnq_v7` (buy-only, one micro, ≤ 2 adds) — exactly the acceptance record's book; no fifth leg, no on/off search, no runner-up, no replacement path (D-B4).
- **Fixed policy:** the TB-P2 instance `(trailing, 0.01, 0.40)` with the per-leg response map of campaign §56 (O-5: law B Striker, law A Vanguard; O-6: Striker executed-base adds; ORB base unchanged, adds off while protected); lifecycle ladder `{1, 0.5, 0.25}` retained; Call-4 off-rail (O-1). **The TB-P2 ADR must be ratified before this contract freezes** (D-B11).
- **Reachable legal quantities/modes:** the TB-R2 §2 table under the ruled laws; every state the decision-bearing run can execute is export-intaken and parity-passed before TB-F1 (D-B14 (a)); the decision-bearing paths run the AUTHORIZED tier × {NORMAL, PROTECTED}; WATCH tiers are monitoring controls (§7) with parity-only evidence.
- **Account-protection semantics:** by reference to TB-S1 (candidate policy object, prior-close timing, integer tables, carried positions, capacity, D-B8 takeover); **symbol/capacity rules:** by reference to TB-S2 RC-5 and TB-S3 R-E.

## 2 — Streams, sizes and power (the four-limb conjunction)

**Limbs on shared paths:** (F-full) full-sample one-sided 95 % Clopper-Pearson upper bound on the failure proportion ≤ 0.05; (F-H1), (F-H2) the same on each chronological half; (S) full-sample one-sided 95 % Clopper-Pearson **lower** bound on the pass-by-200 proportion ≥ 0.50. Unresolved attempts count as failures in the three failure limbs and as T = ∞ in the speed limb. A path is one used-account evaluation started from the frozen initial state (§9) over the frozen horizon (§5).

**Streams:** n1 (stage-1 screen; contributes nothing to any bound; frozen continuation cutoff), n2 (independent confirmation bounds; disjoint seed stream), n3 (the sole final sample after parity and the fresh B7 snapshot; third disjoint stream). Stream identities (`OWED-BY: TB-F1`): three named 64-bit seeds recorded as hex digests of the seed strings, disjoint by construction; the block-bootstrap family and block length are the joint-flat family of TB-S2 (`OWED-BY: TB-F1`).

**Power calculator (additive mode, this packet):** `scripts/certification_power.py` gains `min_certifying_passes`, `speed_limb_power`, `joint_power_four` and `size_for_joint_four`, plus the CLI flags `--true-pass-rate` / `--pass-target`; the legacy output is byte-identical without them (test `test_cli_speed_mode_smoke_and_legacy_line_unchanged`); an exact-rational oracle pins `min_certifying_passes(100, 0.5, 0.05) == 59` and the small-binomial speed power. Speed-limb identity used: a lower bound on the pass proportion ≥ t is the upper bound on the failure proportion ≤ 1 − t.

Design alternatives are **planning assumptions, not measured rates.** Commands and outputs, run 2026-09-12 (alpha 0.05, ceiling 0.05, pass target 0.50, step 10):

```
$ python scripts/certification_power.py --true-rate 0.03 --true-pass-rate 0.65 --power 0.80 --dependence frechet
n=970 fail_limb=0.939 speed_limb=1.000 joint4=0.816 (pass_target=0.5 ceiling=0.05 alpha=0.05 dependence=frechet step=10)
$ python scripts/certification_power.py --true-rate 0.03 --true-pass-rate 0.65 --power 0.80 --dependence independent
n=950 fail_limb=0.932 speed_limb=1.000 joint4=0.809 (pass_target=0.5 ceiling=0.05 alpha=0.05 dependence=independent step=10)
$ python scripts/certification_power.py --true-rate 0.03 --true-pass-rate 0.60 --power 0.80 --dependence frechet
n=970 fail_limb=0.939 speed_limb=1.000 joint4=0.816 (...)
$ python scripts/certification_power.py --true-rate 0.02 --true-pass-rate 0.60 --power 0.80 --dependence frechet
n=390 fail_limb=0.947 speed_limb=0.990 joint4=0.831 (...)
$ python scripts/certification_power.py --true-rate 0.03 --true-pass-rate 0.65 --n 950
n=950 fail_limb=0.932 speed_limb=1.000 min_passes=501 max_busts=36 joint4_independent=0.809 joint4_frechet=0.795 (...)
$ python scripts/certification_power.py --true-rate 0.03 --true-pass-rate 0.65 --n 1200
n=1200 fail_limb=0.970 speed_limb=1.000 min_passes=629 max_busts=47 joint4_independent=0.913 joint4_frechet=0.910 (...)
```

Reading: at a true failure rate of 3 % the failure limbs bind and the speed limb is essentially non-binding once the true pass-by-200 rate is ≥ 0.60 (its minimum certifying count is 501 of 950); the dependence-valid Fréchet bound at 80 % joint power gives **n = 970 per stream**. **Proposed (`OWED-BY: TB-F1`):** n2 = n3 = 970 at the (3 %, 0.65) design alternative under Fréchet; n1 = 200 as a screen with continuation cutoff "stage-1 point-estimate failure proportion ≤ 0.05 on full and both halves" (a failed cutoff ends the attempt; a passed cutoff certifies nothing). n3 is **never** sized from n1/n2 results.

## 3 — Acceptance bounds (verbatim from the plan; not relaxable)

For each of full, H1, H2: one-sided 95 % exact upper failure bound ≤ 0.05 on n3. On the full n3 sample: one-sided 95 % exact lower bound on P(T ≤ 200 business days) ≥ 0.50. Unresolved attempts are failures and T = ∞. The unconditional pass-by-day curve is reported from the same n3 paths with every attempt in the denominator, labelled descriptive; it adds no acceptance test.

### 3a — Regime-robustness gate (concept ADR §4 step 3, as TB-P2 §2.4 ratifies it; frozen here, not relaxable)

The gate is mandatory for a new `POLICY_REGISTRY` instance and its three Part C criteria are the admission test; every deviation from [`docs/methodology/regime_robustness_gate.md`](../../methodology/regime_robustness_gate.md) is named. **Part A (criterion 1):** 100 alternate-history panels built from 6-month contiguous blocks of the replay's venue-session series, each replayed continuously at the fixed instance on the **n2 stream inside TB-E1**; the 5th percentile of the per-panel pass-rate distribution must be ≥ 0.95 (the full-panel floor, one minus the 5 % ceiling; no separate regime floor); close-call rule n = 200 when p5 is within 1 pp of the floor; sanity checks retained (p5 ≤ the full-panel pass-rate; H1 + H2 path counts ≈ full). **Deviation A1 (ratified by TB-P2):** per-panel path depth `OWED-BY: TB-F1`, sized to the compute budget — a reduction in depth, not a removal. **Part B (criteria 2–3):** the F-H1 / F-H2 limbs of §2 on each chronological half (§5), replayed independently as the gate requires. **Deviation B1 (stricter, recorded so the substitution is visible):** each half's limb is the one-sided 95 % upper failure bound ≤ 0.05, which implies the gate's point criterion (pass-rate ≥ 0.95) and never passes a half the gate would fail. **Part A is not rerun on n3:** TB-E2 evaluates only §3's four conditions; TB-E1's Part A result is retained admission evidence whose digest enters the fixed-book replay fingerprint (§6). A Part A failure ends the attempt exactly as a failed n2 bound does (§4).

## 4 — K = 1, one attempt, no runner-up, tie rule

D-B4 / D33: any failed screen, n1 cutoff, n2 bound, regime-gate Part A (§3a) or n3 bound ends the attempt with no qualifying configuration; no runner-up, extra sample or repeated n3. **Tie rule (written for a future K > 1 freeze to inherit; inert at K = 1):** rank by the frozen speed statistic (lower-bound P(T ≤ 200), higher is better), then by the full-sample failure upper bound (lower is better), then by the H1/H2 maximum failure upper bound, then by fewer executable legs, then by the lexical `leg_id` set.

## 5 — Dates, halves and horizon (proposals)

Full = the documented coverage **2022-09-01 → 2026-09-02** (D19 `coverage_end`; the panels end 2026-09-03 00:00Z). H1/H2 by the **chronological-midpoint rule on venue sessions**: H1 = the first ⌈N/2⌉ covered sessions, H2 = the rest (`OWED-BY: TB-F1` with the session count). **Horizon (proposed, `OWED-BY: TB-F1`): 500 business days** per attempt — 2.5× the 200-day speed reservation; an attempt unresolved at day 500 is a failure and T = ∞ (conservative in every limb). The overall horizon was never frozen by the campaign; this is the first proposal.

## 6 — Fingerprints (three layers, kept distinct)

| Layer | Contents | Sealed by |
|---|---|---|
| **K = 1 confirmation contract** | adapter port hashes (`PORT_MANIFEST.sha256` via TB-A0), replay-engine commit, bar-panel digests (`SHA256SUMS`), warm-up boundaries (TB-W1: panel origin), D19 calendar digest, TB-C1 forward-calendar and closure-overlay digests, commission-schedule digest, capacity rules (TB-S1), fill model (§10), E1 initial state (§9), the fixed book and fixed policy, streams and sizes (§2), dates/halves/horizon (§5) | **TB-F1** (`OWED-BY: TB-F1` for every digest) |
| **Fixed-book replay fingerprint** | the contract + the exact four-leg book + the exact 1 % / 40 % policy | **TB-E1** seal; unchanged through Phase 8, B7 and n3 |
| **Execution fingerprint** | rail/daemon commit, image hashes, deployed config digests, the dd-state seed (TB-S3 R-L), TB-I5 source identity, the B7 snapshot digest + `valid_until` | **TB-B7**; must prove equality of every shared component with the replay fingerprint |

## 7 — Monitoring thresholds and down-only controls (D20 battery, restated; severities `OWED-BY: TB-F1` with the proposals shown)

| Control | Proposal | Action (down-only) |
|---|---|---|
| Leave-one-year-out (each of the four panel years dropped in turn) | report each variant's full-sample failure upper bound; severity WARN if any variant > 0.075 | operator review; no re-selection |
| Dependence-length alternatives (block length ×0.5, ×2) | report the failure upper bound and the speed lower bound per variant | WARN if any bound crosses its acceptance value; monitoring input |
| Commission / adverse-fill stress (venue schedule ×1.5; slippage ticks ×2; conservative same-bar ordering; partial-fill fraction 0.5 on adds) | report; WARN if the full-sample failure upper bound > 0.075 | monitoring input |
| Delays / missed trades / outages (drop 5 % of entries at random; one missed session per month) | report | monitoring input |
| Strategy removal, best-trade / best-month / best-year removal | report per removal | monitoring input; a book without a leg is never a substitute |
| Downside correlation / loss clustering (longest joint-loss run; conditional co-loss) | report | monitoring input |
| Rule-faithful tie ordering | fixed by §4 | — |
| Lifecycle ladder | WATCH-1 (0.50×) and WATCH-2 (0.25×) are the only tiers automation may move to; Call-1 decay breach k = 1.0 with two consecutive windows (`core/lifecycle.py`); RETIRED is operator-only; **Call-4 off-rail (O-1)**: three de-authorized legs → operator kill switch / GO-NO-GO | down only |
| Live time-to-pass predictive interval | quantiles q10 / q50 / q90 of T from the n3 paths; clock origin = the first venue session after the arm | a live bust, or T outside [q10, q90], falsifies the model-fitted proposal → all four legs to WATCH-1 pending operator review |
| Seam-sensitivity check (roll obligation 2) | re-run the decision-bearing replay with each contract-month seam window (±2 sessions) excluded; severity WARN if any bound crosses its acceptance value | monitoring input; frozen severity `OWED-BY: TB-F1` |
| Weekly operator token trade | not modelled (D22); a missed venue week is an operational alarm | operator |
| Calendar and closure overlay upkeep | the rail scheduler fails closed past `coverage_end` | operator obligation through the horizon |

## 8 — Continuous-roll obligations (verbatim from `phase1_config.json`)

"Phase 3 pre-registration states back-adjustment seam risk as a limitation of every campaign claim: fills cannot be attributed to a contract month, and a seam crossing is indistinguishable from a price move." "A Phase 6 seam-sensitivity check is pre-registered with its severity frozen alongside the other Phase 6 cutoffs." Both enter the freeze verbatim; the check is §7's seam row.

## 9 — Initial states, calendar overlay and fill model (frozen fields)

- **E1 initial state (screen, n1, n2):** the **pristine** state (equity = peak = basis; zero prior days; zero best day) — screening-only, because no accepted fresh snapshot exists before B7 and a reconstructed one is the derived-input class the campaign forbids; the operator may instead authorize a sealed E1 snapshot via the TB-T1 tool before TB-F1.
- **E2 initial state (n3):** the fresh B7 snapshot sealed by the [snapshot-seal contract](../../spec/2026-09-12-tradeify-account-snapshot-seal-contract.md) (`historical_eod_peak`, `balance`, prior days, best day; consumed before `valid_until`).
- **Typed closure overlay:** 2023-04-07, 2025-01-09, 2026-04-03 are full-closure / no-trade dates (TB-C1 artifact, digest-pinned, separate from the frozen D19 file).
- **Fill model:** TV-faithful emulator semantics with full fills (TB-S2 RC-4/RC-9); the conservative ordering, slippage and partial-fill cells are §7 stress cells.
- **Coverage:** TB-S2 RC-7; excluded-session counts reported; a window past `coverage_end` fails closed.

## 10 — Publication scope (D-B12)

Public: this contract, the digests, the verdict labels (RESOLVED / FALSIFIED / AMBIGUOUS / BLOCKED), the excluded-session and idle-week counts. Private root only: every bound, the pass-by-day curve, replay statistics, snapshot values, stress-cell results. A later publication of any figure needs the explicit authorization D-B12 names.

## 11 — What TB-P1 does not do

It freezes nothing, sizes nothing from results, fills no ORB Decision slot, cites no feasibility-screen or weighting-study figure as evidence, and relaxes no bound. TB-F1 fills every `OWED-BY` field and freezes the contract; any later change is a replacement freeze and a new operator decision.
