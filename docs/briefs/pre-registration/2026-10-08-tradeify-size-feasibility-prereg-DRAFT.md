# Pre-registration — size-feasibility check for the accepted Tradeify book (one-sided, necessary condition)

**Status:** `DRAFT — NOT FROZEN`
**Date:** 2026-10-08. **Loop:** STRATEGIC. **Authored:** Claude Code worker (drafting only) for the Deployment Coordinator, on Joshua's request in chat 2026-10-08. Joshua owns every OWED value, the signature and the freeze.
**Harness of record (adopted, not re-decided):** the four-firm re-MC executor [`run_four_firm_remc.py`](../../../lab/analysis/c1/four_firm_remc_2026-10/run_four_firm_remc.py) under its [frozen prereg](2026-10-02-four-firm-dated-remc-prereg-DRAFT.md) (`FROZEN 2026-10-05`), with the run of record and depth re-run in [RESULTS](../../../lab/analysis/c1/four_firm_remc_2026-10/RESULTS.md). **Gate numbers:** [prereg v2](2026-08-26-prop-survivor-scoring-prereg-v2.md) §3. **Gate shape:** [T00 screen prereg](2026-10-01-tradeify-t00-step2-screen-prereg.md) A2/A6.
**Not:** four-firm §4 evidence; a T00 re-screen; a successor screen; qualification evidence.

## §D — Disclosure: what the drafter saw

- Public records only: the files in §0, the published RESULTS figures (Tradeify Run-1/Run-2 rates at k = 1), the T00 step-12 verdict (#724, `NO-GO-evidence-robust`), the Tier-1 finding as summarized in the task ("early erosion of the trailing rope by ordinary sessions"), and the Tier-2 card.
- Drafter memory held size-dependence results for other constructs (an ORB-MYM quantity sweep, an MGC rope screen). None concerns this book; none of their figures appear here.
- No private input, series, Pine, port, effective-input file or `t00-step3` directory was read. Nothing was run.
- **Consequence:** the grid (§3) was fixed after the k = 1 rates and the Tier-1 shape were known. It is not blind to them. It is fixed before any rescaled output exists, which is what this file controls.

## §R — Standing rule

No rescaled arm (k ≠ 1, or any vector) is scored before this file is FROZEN and merged. The wrapper (§2.3) is built and tested on synthetic inputs only. An unsigned run voids this file.

---

## §0 — Production reads (anchor `origin/main` `f038dee`, 2026-10-08)

| Surface | Fact used here |
|---|---|
| `lab/discovery/prop_survivor_scoring.py:788-987` `score_candidate` | Per tier: non-vacuity guard, then G4 Run-1 and Run-2 (`run_tier_remc`). `tiers=` restricts the tier set; its docstring says "override only in unit tests … never for a live scoring claim". |
| `prop_survivor_scoring.py:138-150` `TierSeries` | Four channels per tier: `daily_pnl`, `intraday_low`, `protected_pnl`, `protected_low`. Combined across legs; no per-leg channel. |
| `prop_survivor_scoring.py:582-680` guard | Runs three arms at gating depth and consistency: EOD (no low), zeros, real. Returns the EOD arm's `headline_bust` / `pass_rate`; `score_candidate` discards that return. |
| `prop_survivor_scoring.py:446-470` G2 | Hurdle = multiple × round-trip cost per contract × `R_deploy`. It does not scale with contracts. |
| `prop_survivor_scoring.py:768-773`, `:977-980` G7 | `clears_funded` reads the **eval** Run-2 headline bust against the 1.0% ceiling. No funded geometry is simulated. `core/firm_rules.py` has no Tradeify funded tier row. |
| `core/mc/simulation.py:693-760` `run_seed` | Returns `days_to_pass` for passing sims. |
| `core/mc/preflight.py:268-312` `summarize_outcomes` | Drops `days_to_pass`. Hence RESULTS disclosure 4: no median days-to-pass. |
| `core/mc/simulation.py:372-417` | Mode-switching: a day is protected when `round((equity − peak)/peak, 6) ≤ −mode_trigger`. Equity-relative, so a smaller k fires protection less often. |
| `lab/discovery/remc_series_builder.py:1-40`, `:596-760` | `pnl = gross − sides × cost_per_side`; `intraday_low = −Σ|adverse excursion| − day cost` (coincident sum, conservative). Striker and ORB as exported; Vanguard normal as exported, protected zero; Aegis rescaled to a fixed count. The manifest records each tier CSV's SHA-256 and `n_days`. Capacity and takeover are not modelled. |
| `ops/c1_rail/book_policy.py:279-310` `entry_quantities` | Striker is risk-sized with a cap (floor of risk over per-contract risk). Vanguard, Aegis and ORB bases are small fixed integers; protected sizes are floors of base × protected scale. |
| `run_four_firm_remc.py:184-203` | Candidate stage: one `score_candidate` call, `mode_trigger` from `book_policy.CANDIDATE_TRIGGER`, G1/G2 inputs from `prep.json`. |
| [T00 prereg](2026-10-01-tradeify-t00-step2-screen-prereg.md) A1, A2, A6, §6 | FULL/H1/H2 by chronological ceil partition; bust ≤ 5.0% on all three; pass floor on FULL, halves `REPORTED`; median rule `LOWER_NEAREST_RANK_INF_INCLUDED`; a NO-GO is labelled robust when it also fails the optimistic assignment. |
| [Tier-2 card](../handoffs/2026-10-08-t00-step12-diagnostic-tier2-scoping-card-DRAFT.md) §1, §2.1 row 5, §7 | "Leg off, rescale, adds off or any input change is a candidate replay." Row 5 points to "a uniform or early-phase size cut across legs". |
| [Checklist](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md) item 7.6.1 (:634-638) | No agent runs any candidate-configurable replay against a pre-registered edition before that pre-registration is frozen, including an accepted port with input overrides. |

---

## §1 — Question and one-sided logic

**Question.** Is there any size multiplier k at which the accepted four-leg Tradeify book could clear the T00 gate shape on `Tradeify_Select_100K`?

**Method.** Multiply every channel of the Tradeify tier series by k (`k × pnl`, `k × low`, `k × protected_pnl`, `k × protected_low`). Costs and the low are linear in contract-sides, so this is exactly the book at k × every traded quantity, with fractional contracts allowed. Score it with the frozen harness.

**Intended logic.** A linear rescale is generous to the hypothesis "some size cut works". If no k clears even so, no uniform size cut rescues the book. If some k clears, that is licence to spend on a proper successor, nothing more.

### §1.1 — What the rescale omits, and the bias of each

| Omission | Effect on bust | Effect on pass | One-sided? |
|---|---|---|---|
| **Contract granularity.** Fixed-size legs trade small integer bases; no real size lies between 1 and 0. A uniform k < 1 on a one-lot leg is either kept at 1 (more risk than modelled) or dropped (a different book). | Optimistic against keep-at-1 rounding. Not bounded against dropping. | **Pessimistic** against keep-at-1 rounding (real P&L is larger). | Bust only, and only against keep rounding. |
| **Port-internal loss thresholds** in account dollars or equity (e.g. Striker's day soft-stop and halt, a named approximation in four-firm I-17). At smaller size the real threshold fires later or not at all. | Optimistic (the scaled series keeps the full-size truncation). | Neutral to slightly pessimistic. | Yes on bust. Price-denominated thresholds are exact. |
| **Port-internal profit-side thresholds** in dollars or equity. | Neutral. | **Pessimistic** (real upside is larger at small size). | No on pass. |
| **Equity-sized legs** (the coordinator names Vanguard; not verified here, Pine not read). Export quantities follow TradingView's own equity path and are used as exported. The rescale scales that path; it does not re-size from the prop account's equity. | Undetermined. | Undetermined. | **No.** |
| **Port drawdown kills** (a port that stops trading after its own drawdown). Timing is inherited from the full-size run; a smaller real size would trade on longer. | Undetermined; usually optimistic, since the kill follows losses. | Undetermined. | **No, in general.** |
| **Capacity and takeover** (80-micro cap, Aegis-priority takeover). Not in the series at any k. | Optimistic at k = 1; the omission shrinks as k falls. | Optimistic. | Yes. |
| **Coincident-sum intraday low** (builder). Sums each leg's worst excursion as if simultaneous; scales with k. | **Pessimistic** at every k. | Pessimistic. | **No on the intraday clock.** Handled by §4's EOD read. |
| **MGC at the index-micro cost rate** (four-firm I-19). | Optimistic. | Optimistic. | Yes. |
| **Protection policy at small size.** The trigger is equity-relative and fires less as k falls; that is modelled. Protected sizes are floors, so at small k some round to zero. | Mixed. | Mixed. | No. |
| **One historical window, block bootstrap.** | Neither. | Neither. | Not a bias; a scope limit. |

### §1.2 — Does "optimistic bound" hold? Drafter's view

**Partly. It does not hold as stated.**

1. **The pass side is not optimistic.** Granularity and profit-side thresholds bias the rescaled pass rate downward. An INFEASIBLE driven by the pass floor is not one-sided.
2. **The intraday clock is conservative.** The coincident-sum low overstates intraday drawdown, so an INFEASIBLE on the intraday clock alone is not one-sided. The EOD clock is a lower bound on bust (`load_bearing_numbers.md` §1). This file therefore requires INFEASIBLE to hold on both clocks (§6).
3. **Two omissions have no sign:** equity-sized legs and port drawdown kills.
4. **Scope is the uniform ray.** Real integer configurations lie off the ray, because legs round differently. INFEASIBLE speaks to uniform cuts and the named vectors (§3.2) only. Dropping or reshaping a leg is out of scope; that is Tier-2 rows 1–3.
5. **Grid resolution.** A clearing interval narrower than the grid spacing can be missed. §6 labels that case.

**What survives.** A bust-side INFEASIBLE that holds on the EOD clock is close to one-sided; the remaining unsigned omissions are equity sizing and port kills. That is the only reading this file lets trigger the stopping proposal.

### §1.3 — What each outcome means

- **INFEASIBLE** (§6): no k clears, on either clock. It supports stopping uniform-size-cut successors of this book on this tier. Stopping is Joshua's decision (§6).
- **FEASIBLE** is **not** a successor result. It gives a target k range for Tier 2 and for a successor screen, which needs its own frozen pre-registration and an integer-sized book.

---

## §2 — Harness and inputs

### §2.1 — Frozen harness, reused unchanged

- Series: the depth re-run's private bundle, chained by digest. `prep.json` `feefa7ab28ff17d8b1a727bae0adf6656369a4ea73eafea2218cdafbd8f4c3b5` (RESULTS) → its `series_manifest_sha256` → the manifest → the `Tradeify_Select_100K.csv` SHA-256 in the manifest `outputs`. Any mismatch is INVALID. The series is not rebuilt.
- Reproduction target: `candidate_report.json` `4076857777e67cedd5755ba637693ce45638357a8a5b1fb17077e63ac28ec2ed` and its depth record `87a66d8e9d2baf3b474feb7e69e1e2cdb4138f27e911f666d9b57d0118e483f2` (RESULTS, depth re-run root).
- Clock: intraday-honest, paired `intraday_low` (four-firm I-12). EOD read per §4.
- Protection: mode-switching as in candidate (A) (four-firm I-17); trigger from `book_policy.CANDIDATE_TRIGGER`, unchanged at every k.
- Depth: 10,000 sims × seeds 42/123/2026, horizon 1500, inactivity OFF, pristine start (four-firm I-6, I-8, I-18).
- G1/G2: carried from `prep.json` at k = 1, unscaled. G2's hurdle does not scale with contracts, so scaling only the edge would kill tiers by artefact. G1/G2 are not this check's question.

### §2.2 — Venue

`Tradeify_Select_100K` only, gating on Run-2 (consistency 40%). Run-1 is reported. Other tiers are out of scope and are not scored at k ≠ 1. This uses `score_candidate(tiers=…)`, which departs from its docstring; the k = 1 sub-report check (§2.3) validates it, and the build review rules on it.

### §2.3 — Build needed (its own packet, review and launcher record; synthetic tests only)

1. **Wrapper** `lab/analysis/c1/size_feasibility_2026-10/run_size_feasibility.py`: public code; reads the private bundle at run time by digest; writes to a gitignored private root. It builds `TierSeries` with every channel × k, slices populations (§4.1), and calls `score_candidate` once per (k, population). It writes each report plus a depth record bound to its SHA-256, as `write_depth_record` does.
2. **EOD retention.** Opt-in return of the guard's EOD arm (`headline_bust`, `pass_rate`) per tier, in a sidecar file, not in the report. Default path byte-identical.
3. **Median days-to-pass.** Opt-in retention of `run_seed`'s `days_to_pass` through `run_tier_remc`, pooled over 30,000 sims with non-passers at ∞, under T00's `LOWER_NEAREST_RANK_INF_INCLUDED`. Sidecar only; default bytes unchanged.
4. **Per-leg channels** (only if §3.2 vectors are ruled in). Opt-in per-leg `gross` / `sides` / `adverse_excursion` from the builder on the same window; default bundle bytes unchanged. Not built otherwise.

**Acceptance tests (synthetic):**
- k = 1 through the wrapper gives report bytes identical to a direct `score_candidate` call.
- `x × 1.0` leaves every channel bit-equal.
- A Tradeify-only call's tier entry equals that tier's entry in a four-tier call.
- Sidecars off vs on: identical report bytes.
- The retained EOD arm equals the guard's internal EOD arm; the median equals a direct computation.
- Population slicing gives H1 = the first ⌈N/2⌉ rows and H2 = the rest, in order.
- Per-leg columns, if built, sum to the combined columns (same summation order).

**Run-time reproduction (first arm; a mismatch is INVALID and nothing else runs):**
- (a) k = 1, all four tiers, FULL: `candidate_report.json` SHA-256 equals `40768577…2ec2ed`.
- (b) k = 1, Tradeify only, FULL: its tier entry equals (a)'s Tradeify entry, as canonical JSON.

---

## §3 — Grid (fixed now)

### §3.1 — Uniform

k ∈ {**1.0**, 0.75, 0.5, 0.4, 0.33, 0.25, 0.2}. k = 1.0 is the reproduction check and an ordinary grid point. 0.33 means exactly 0.33.

### §3.2 — Per-leg vectors

**OWED (operator):** none, or at most 3 named vectors, each a multiplier per leg (Aegis, Striker, Vanguard, ORB). They are named before freeze, by structure only (e.g. "Striker at k, others 1"), never chosen from output. Each needs build item 4.

### §3.3 — Early-phase (cushion-dependent) sizing

Not expressible. The kernel switches modes on drawdown from the running peak, not on cushion to the trailing floor or profit since start. Left out. Tier-2 row 5 names it; a successor would need a kernel change.

---

## §4 — Hypothesis and gates per k

**H-SIZE.** If, for some k on the grid (or a named vector), the rescaled book clears every §4.2 gating cell on the intraday-honest clock, then a uniform size cut is not ruled out (FEASIBLE). **Falsifier:** if no k clears on the intraday-honest clock **and** none clears on the EOD clock, no uniform size cut rescues the book (INFEASIBLE).

### §4.1 — Populations

T00's chronological ceil partition, adapted to the daily window. N is the series row count (`n_days` in the manifest; RESULTS disclosure 1 gives 1,020 weekdays). FULL = all N rows; H1 = the first ⌈N/2⌉ rows; H2 = the remaining ⌊N/2⌋ rows. Each population is bootstrapped independently at full depth and horizon, as T00 does (A2). With N = 1,020, H2 starts 102 weeks in, so its 5-day blocks keep FULL's Thursday-to-Wednesday phase (RESULTS disclosure 1). The H2 bootstrap resamples about two years into a 1500-day horizon; disclosed.

### §4.2 — Gates (each k, each clock)

| Gate | FULL | H1 | H2 | Owner |
|---|---|---|---|---|
| Run-2 headline bust ≤ 5.0% | **gates** | reported | **gates** | v2 §3; T00 A2 |
| Run-2 P(pass) ≥ 50% | **gates** | reported | **OWED (operator)** | v2 §3; T00 A2, §6 `pass_floor_halves` |
| Median days-to-pass finite and ≤ 1500 | reported | reported | reported | v2 §3; T00 A2 |
| G7-style: Run-2 eval bust ≤ 1.0% (`clears_funded`) | reported | — | — | v2 §2 G7, §3 Part B |

- **H1 bust.** T00 A6 also gates H1 bust. Omitting it makes this check more lenient than A6, which a necessary condition allows.
- **H2 pass floor.** The task draft makes it binding. T00 ratified halves as `REPORTED`. A necessary condition must not be stricter than the successor's gate, so the drafter recommends `REPORTED`. If ruled binding, INFEASIBLE may rest only on the FULL/H2 bust gates and the FULL pass gate.
- **Median.** Under the T00 rule over 30,000 pooled sims, the median is finite exactly when P(pass) ≥ 50%. It adds no gate; it is reported for the successor's time-cost read.
- **G7.** The harness reads eval geometry, not funded geometry, and no Tradeify funded tier row exists. Reported only; never gates.
- **EOD clock.** The guard's EOD arm, retained (§2.3 item 2), is the Run-2 consistency-on EOD read. It never makes a k FEASIBLE; it only decides whether INFEASIBLE is robust (§6).

---

## §5 — Forbidden moves

- Scoring any rescaled arm before FROZEN (§R).
- Changing the grid, gates, populations, clocks or vectors after any rescaled output exists.
- Adding a k or vector after output, except a midpoint pre-authorized under §6 GRID-GAP.
- Rebuilding or editing the series; reading any private input other than the digest-chained bundle.
- Scoring tiers other than `Tradeify_Select_100K` at k ≠ 1.
- Presenting any outcome as four-firm §4 evidence, a T00 verdict change, or a successor result.
- Replaying ports or editions (`replay_bracket`, `BookReplay`), or overriding any input.
- Publishing per-k bust, pass, median or G7 values, dollar figures, or counts from data.
- Re-using these outputs as the successor's evidence; the successor re-estimates on its own screen.

---

## §6 — Decision rule (fixed now)

Evaluated mechanically, in order:

| Label | Trigger | Meaning |
|---|---|---|
| **INVALID** | Digest-chain mismatch, or §2.3 run-time reproduction (a) or (b) fails | No reading. Fix and re-run under this file. |
| **INSUFFICIENT** (per k) | Arm incomplete at frozen depth, missing depth record, or `gate_grade = false` on an intraday arm | That k cannot support INFEASIBLE. FEASIBLE may still be read from valid k. |
| **FEASIBLE** | ≥ 1 k (or vector) clears every gating cell of §4.2 on the intraday-honest clock | Report the largest clearing uniform k (the smallest risk cut), every clearing k, and the full curve. A target range for Tier 2 and a successor only. |
| **GRID-GAP** | No k clears, but adjacent grid points split the gates on either clock (the larger k clears every pass gate, the smaller every bust gate) | Not INFEASIBLE; does not trigger stopping. **OWED (operator):** report only, or one pre-authorized midpoint arm (K + 1). |
| **CLOCK-DEPENDENT** | No k clears on the intraday clock, but some k clears every gating cell on the EOD clock | Not INFEASIBLE (the coincident-sum low may drive it); does not trigger stopping. |
| **INFEASIBLE** | Every k is valid and fails on both clocks, and GRID-GAP does not hold | Supports stopping (below). |

**Proposed stopping rule (Joshua's decision; not adopted here).** On INFEASIBLE, stop pursuing uniform-size-cut successors of the accepted book on `Tradeify_Select_100K`. It does not retire any strategy, close Tier 2, or bar leg-composition successors.

---

## §7 — K and exposure

- **K** = uniform k values (7) + named vectors (0–3) + any GRID-GAP midpoint (0–1): 7 to 11.
- **Selection.** A FEASIBLE k is the best of K, so its rates are optimistic for that reason too. The successor discloses K and re-estimates.
- **Successor disclosure.** Any successor pre-registration (a size-cut book, the Tier-2 row-5 direction, or a four-firm candidate) names this run, its K, its labels and its readers as prior looks. Readers of the private outputs are logged with the run.
- **Tier 2.** Tier-2 criteria are frozen (rows 1–4 at `34c31c4`, row 5 at admission), so this output cannot change them. It overlaps row 5's pointer: a FEASIBLE here and a row-5 hit there point the same way from different evidence. Neither confirms the other.
- **Checklist 7.6.1.** The rule covers candidate-configurable **replays** against a **pre-registered edition**. This check replays nothing: no port, bar panel, edition or input override. It transforms an already-computed daily series inside the MC, and no size-cut edition is pre-registered. So it is outside 7.6.1 as written.
  - **Borderline, flagged.** Tier-2 card §1 calls a rescale "a candidate replay". That sentence concerns `BookReplay`, but a reader could extend it here. In spirit, this check scores a candidate-like configuration before its successor pre-registration exists, which is the harm item 7.6.1's 2026-10-02 incident records. The mitigation is this file: freeze first, disclose to the successor. **OWED (operator):** accept this classification, or treat the check as under 7.6.1 and require the successor pre-registration to freeze first.
- **Four-firm §4.** Not evidence: Tradeify only, and the four-firm prereg §5 bars substituting sizes after output. The early-fail branch stands: any §4 candidate needs fresh operator authorization.
- **T00.** Cannot change `NO-GO-evidence-robust`. T00 A1 forbids re-sizing within T00; this check sits outside it.

---

## §8 — Cost, outputs, return

### §8.1 — Cost (from RESULTS stage timings)

- RESULTS depth re-run: the candidate stage ran 22:37:11–22:58:07Z, about 21 min for 19 arms (Bulenox 4; three tiers × 5), so **≈ 66 s per arm** (3 seeds × 10k).
- Per (k, population), Tradeify only: 5 arms (3 guard, Run-1, Run-2) ≈ **5.5 min**.
- Grid: 7 k × 3 populations = 21 calls ≈ **116 min**. Reproduction (a): ≈ 21 min. Each vector: ≈ 17 min. Total ≈ 2.3 h serial without vectors, ≈ 3.1 h with 3.
- **Not a bound.** Smaller k keeps paths alive longer, so arms slow toward the full-horizon figure (four-firm I-15: 1005 s per arm, ×1.5 margin). Worst case ≈ 2.1 CPU-h per (k, population). Arms may run in parallel; seeds are fixed, so scheduling cannot change a result.
- **OWED (operator):** a wall-clock budget cap. A cap hit before every arm completes reads INSUFFICIENT for the missing k.

### §8.2 — Outputs (private)

Private root: `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts/size-feasibility-<date>/` (gitignored). Per (k, population): report, depth record, EOD sidecar, median sidecar. Plus `run.json` (commands, PIDs, exit codes, stdout/stderr SHA-256) and `verdict.json`.

### §8.3 — Return (public)

- The verdict label (§6) and, for FEASIBLE, the clearing k labels.
- The SHA-256 of every private file, the `main` SHA, the wrapper commit, and the result of reproductions (a) and (b).
- The reader list.
- No rates, medians, dollar figures or counts.

---

## §9 — OWED (operator) and signature

1. H2 pass floor: binding or `REPORTED` (§4.2). Drafter: `REPORTED`.
2. Per-leg vectors: none, or up to 3 named (§3.2). Drafter: none, unless Tier 2 has returned a concentrated-leg pattern before freeze.
3. GRID-GAP: report only, or one midpoint arm (§6).
4. Budget cap (§8.1).
5. 7.6.1 classification (§7).
6. Executor and run-by date. Run order relative to Tier 2: independent (§7); the drafter sees no ordering need.
7. Stopping rule: adopt, amend or decline, before the run (§6).
8. Build packet authorization for §2.3, including the `tiers=` departure.
- **Signed:** —

---

## §10 — Audit hooks

```bash
f=docs/briefs/pre-registration/2026-10-08-tradeify-size-feasibility-prereg-DRAFT.md
# Gate numbers resolve to v2 (expect 0.05 0.01 0.5).
python -I scripts/fp.py python -c "import sys; sys.path[:0]=['lab','core']; from discovery.prop_survivor_scoring import load_scoring_thresholds as l; t=l(); print(t.eval_bust_ceiling, t.funded_bust_ceiling, t.pass_floor)"
# The chain and reproduction digests are the ones RESULTS publishes.
r=lab/analysis/c1/four_firm_remc_2026-10/RESULTS.md
for d in feefa7ab28ff17d8b1a727bae0adf6656369a4ea73eafea2218cdafbd8f4c3b5 4076857777e67cedd5755ba637693ce45638357a8a5b1fb17077e63ac28ec2ed 87a66d8e9d2baf3b474feb7e69e1e2cdb4138f27e911f666d9b57d0118e483f2; do grep -q "$d" "$r" && grep -q "$d" "$f" || { echo "digest $d"; false; }; done
# Production facts §0 relies on: tiers= exists; run_seed keeps days_to_pass; summarize_outcomes drops it.
grep -n "tiers: Sequence\[str\] | None = None" lab/discovery/prop_survivor_scoring.py
grep -n '"days_to_pass": days_to_pass' core/mc/simulation.py
! grep -n "days_to_pass" core/mc/preflight.py
# The grid is stated once.
grep -c "k ∈ {\*\*1.0\*\*, 0.75, 0.5, 0.4, 0.33, 0.25, 0.2}" "$f"
# No dollar figure in this file (absence exits 0).
! grep -nE '\$[0-9]' "$f"
# No result cites this file before freeze (expect no output until the run).
grep -rl "2026-10-08-tradeify-size-feasibility-prereg" lab/ || true
# At freeze only (each fails while DRAFT): no OWED marker, §9 signed, Status frozen.
! grep -n "OWED (operator)" "$f"
! grep -nE '^- \*\*Signed:\*\* —$' "$f"
grep -nE '^\*\*Status:\*\* `FROZEN [0-9]{4}-[0-9]{2}-[0-9]{2}`' "$f"
```
