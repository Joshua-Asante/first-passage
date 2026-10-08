# Pre-registration — size-feasibility check for the accepted Tradeify book (one-sided, necessary condition)

**Status:** `FROZEN 2026-10-08` (Joshua in chat to the Deployment Coordinator, verbatim: "freeze and merge 735").
**Date:** 2026-10-08. **Loop:** STRATEGIC. **Authored:** Claude Code worker (drafting only) for the Deployment Coordinator, on Joshua's request in chat 2026-10-08. Joshua owns every OWED value, the signature and the freeze.
**Harness of record (adopted, not re-decided):** the four-firm re-MC executor [`run_four_firm_remc.py`](../../../lab/analysis/c1/four_firm_remc_2026-10/run_four_firm_remc.py) under its [frozen prereg](2026-10-02-four-firm-dated-remc-prereg-DRAFT.md) (`FROZEN 2026-10-05`), with the run of record and depth re-run in [RESULTS](../../../lab/analysis/c1/four_firm_remc_2026-10/RESULTS.md). **Gate numbers:** [prereg v2](2026-08-26-prop-survivor-scoring-prereg-v2.md) §3. **Gate shape:** [T00 screen prereg](2026-10-01-tradeify-t00-step2-screen-prereg.md) A2/A6.
**Not:** four-firm §4 evidence; a T00 re-screen; a successor screen; qualification evidence.
**Review folded:** [#735 review 6066105704](https://github.com/Joshua-Asante/first-passage/pull/735#issuecomment-6066105704) (P1-1, P2-1 to P2-4, P3-1 to P3-5); P2-4 by coordinator ruling 2026-10-08: uniform k only. [#735 re-check 6066185454](https://github.com/Joshua-Asante/first-passage/pull/735#issuecomment-6066185454) (P2-A, P3-A to P3-C).

## §D — Disclosure: what the drafter saw

- Public records only: the files in §0, the published RESULTS figures (Tradeify Run-1/Run-2 rates at k = 1), the T00 step-12 verdict (#724, `NO-GO-evidence-robust`), the Tier-1 finding as summarized in the task ("early erosion of the trailing rope by ordinary sessions"), and the Tier-2 card.
- Drafter memory held size-dependence results for other constructs (an ORB-MYM quantity sweep, an MGC rope screen). None concerns this book; none of their figures appear here.
- No private input, series, Pine, port, effective-input file or `t00-step3` directory was read. Nothing was run.
- **Consequence:** the grid (§3) was fixed after the k = 1 rates and the Tier-1 shape were known. It is not blind to them. It is fixed before any rescaled output exists, which is what this file controls.

## §R — Standing rule

No rescaled arm (k ≠ 1) is scored before this file is FROZEN and merged. The wrapper (§2.3) is built and tested on synthetic inputs only. An unsigned run voids this file.

---

## §0 — Production reads (anchor `origin/main` `f038dee`, 2026-10-08)

| Surface | Fact used here |
|---|---|
| `lab/discovery/prop_survivor_scoring.py:788-987` `score_candidate` | Computes G1 from `candidate_daily_pnl` and `full_res_trades`, G2 from `g1.r_deploy` and the edge, then per tier the non-vacuity guard and G4 Run-1 and Run-2 (`run_tier_remc`). A G2-killed tier gets `clears_part_a = False` and an empty `run2`. `tiers=` restricts the tier set; its docstring says "override only in unit tests … never for a live scoring claim". |
| `prop_survivor_scoring.py:138-150` `TierSeries` | Four channels per tier: `daily_pnl`, `intraday_low`, `protected_pnl`, `protected_low`. Combined across legs; no per-leg channel. |
| `prop_survivor_scoring.py:582-680` guard | Runs three arms at gating depth and consistency (EOD with no low, zeros, real) and returns all three as `{"eod", "zeros", "real"}`; `score_candidate` discards the return. It flags "non-vacuity FAIL" when the real arm's bust **and** pass equal the EOD arm's. |
| `prop_survivor_scoring.py:446-470` G2 | Hurdle = multiple × round-trip cost per contract × `R_deploy`. It does not scale with contracts. |
| `prop_survivor_scoring.py:768-773`, `:977-980` G7 | `clears_funded` reads the **eval** Run-2 headline bust against the 1.0% ceiling. No funded geometry is simulated. `core/firm_rules.py` has no Tradeify funded tier row. |
| `core/mc/simulation.py:693-760` `run_seed` | Returns `days_to_pass` for passing sims. |
| `core/mc/preflight.py:268-312` `summarize_outcomes` | Drops `days_to_pass`. Hence RESULTS disclosure 4: no median days-to-pass. |
| `core/mc/simulation.py:372-417` | Mode-switching: a day is protected when `round((equity − peak)/peak, 6) ≤ −mode_trigger`. Equity-relative, so a smaller k fires protection less often. |
| `lab/discovery/remc_series_builder.py:1-40`, `:596-760` | `pnl = gross − sides × cost_per_side`; `intraday_low = −Σ|adverse excursion| − day cost` (coincident sum, conservative). Striker and ORB as exported; Vanguard normal as exported, protected zero; Aegis rescaled to a fixed count. Any exit after 16:45 ET raises. The manifest records each tier CSV's SHA-256 and `n_days`. Capacity and takeover are not modelled. |
| `ops/c1_rail/book_policy.py:279-310` `entry_quantities` | Striker is risk-sized with a cap (floor of risk over per-contract risk). Vanguard, Aegis and ORB bases are small fixed integers; protected sizes are floors of base × protected scale. |
| `run_four_firm_remc.py:184-203` | Candidate stage: one `score_candidate` call; `candidate_daily_pnl` is the manifest's FULL `normal.gross`; `full_res_trades`, envelope and edge from `prep.json`; `mode_trigger` from `book_policy.CANDIDATE_TRIGGER`. |
| [T00 prereg](2026-10-01-tradeify-t00-step2-screen-prereg.md) A1, A2, A6, §6 | FULL/H1/H2 by chronological ceil partition; bust ≤ 5.0% on all three; pass floor on FULL, halves `REPORTED`; median rule `LOWER_NEAREST_RANK_INF_INCLUDED`; `deadline_only_is_bust: true`; a NO-GO is labelled robust when it also fails the optimistic assignment. |
| [Tier-2 card](../handoffs/2026-10-08-t00-step12-diagnostic-tier2-scoping-card-DRAFT.md) §1, §2.1 row 5, §7 | "Leg off, rescale, adds off or any input change is a candidate replay." Row 5 points to "a uniform or early-phase size cut across legs". |
| [Checklist](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md) item 7.6.1 (:634-638) | No agent runs any candidate-configurable replay against a pre-registered edition before that pre-registration is frozen, including an accepted port with input overrides. |

---

## §1 — Question and one-sided logic

**Question.** Is there any uniform size multiplier k at which the accepted four-leg Tradeify book could clear the T00 gate shape on `Tradeify_Select_100K`?

**Method.** Multiply every channel of the Tradeify tier series by k (`k × pnl`, `k × low`, `k × protected_pnl`, `k × protected_low`). Costs and the low are linear in contract-sides, so this is exactly the book at k × every traded quantity, with fractional contracts allowed. Score it with the frozen harness.

**Intended logic.** A linear rescale is generous to the hypothesis "some size cut works". If no k clears even so, no uniform size cut rescues the book. If some k clears, that is licence to spend on a proper successor, nothing more.

### §1.1 — What the rescale omits, and the bias of each

| Omission | Effect on bust | Effect on pass | One-sided? |
|---|---|---|---|
| **Contract granularity.** Fixed-size legs trade small integer bases; no real size lies between 1 and 0. A uniform k < 1 on a one-lot leg is either kept at 1 (more risk than modelled) or dropped (a different book). | Optimistic against keep-at-1 rounding. Not bounded against dropping. | **Unsigned.** Keep-at-1 scales losses as well as gains; where the barrier binds, more size can lower the pass rate. | Bust only, and only against keep rounding. |
| **Port-internal loss thresholds** in account dollars or equity (e.g. Striker's day soft-stop and halt, a named approximation in four-firm I-17). At smaller size the real threshold fires later or not at all. | Optimistic (the scaled series keeps the full-size truncation). | Neutral to slightly pessimistic. | Yes on bust. Price-denominated thresholds are exact. |
| **Port-internal profit-side thresholds** in dollars or equity. | Neutral. | **Pessimistic** (real upside is larger at small size). | No on pass. |
| **Risk- or equity-sized legs** (Striker, risk-sized per `book_policy`; Vanguard, equity-sized per the coordinator, not verified here, Pine not read). Export quantities follow TradingView's own sizing path and are used as exported. The rescale scales that path; it does not re-size from the prop account's equity or risk inputs. | Undetermined. | Undetermined. | **No.** |
| **Port drawdown kills** (a port that stops trading after its own drawdown). Timing is inherited from the full-size run; a smaller real size would trade on longer. | Undetermined; usually optimistic, since the kill follows losses. | Undetermined. | **No, in general.** |
| **Capacity and takeover** (80-micro cap, Aegis-priority takeover). Not in the series at any k. | Optimistic at k = 1; the omission shrinks as k falls. | Optimistic. | Yes. |
| **Deadline-only failures.** T00 counts an own-flat deadline failure as a bust (`deadline_only_is_bust: true`). The builder raises on any exit after 16:45 ET, so this harness has none. A T00-shape difference. | Optimistic. | Neutral. | Yes on bust. |
| **Coincident-sum intraday low** (builder). Sums each leg's worst excursion as if simultaneous; scales with k. | **Pessimistic** at every k. | Pessimistic. | **No on the intraday clock.** Handled by the EOD read (§4, §6). |
| **MGC at the index-micro cost rate** (four-firm I-19). | Optimistic. | Optimistic. | Yes. |
| **Protection policy at small size.** The trigger is equity-relative and fires less as k falls; that is modelled. Protected sizes are floors, so at small k some round to zero. | Mixed. | Mixed. | No. |
| **One historical window, block bootstrap.** | Neither. | Neither. | Not a bias; a scope limit. |

### §1.2 — Does "optimistic bound" hold? Drafter's view

**Partly. It does not hold as stated.**

1. **The pass side is not optimistic.** Profit-side thresholds bias the rescaled pass rate down; granularity is unsigned. A pass-driven failure is not one-sided, so it never triggers stopping (§6 PASS-LIMITED).
2. **The intraday clock is conservative.** The coincident-sum low overstates intraday drawdown, so an intraday failure alone is not one-sided. The EOD clock is a lower bound on bust (`load_bearing_numbers.md` §1). INFEASIBLE therefore rests on the EOD bust gates (§6).
3. **Two omissions have no sign:** risk- or equity-sized legs and port drawdown kills.
4. **Scope is the uniform ray, k ≥ 0.2.** Real integer configurations lie off the ray, because legs round differently. INFEASIBLE speaks to uniform cuts on the grid's range only. Dropping, reshaping or re-sizing one leg is out of scope; per-leg questions belong to Tier 2 (rows 1–3).
5. **Grid resolution.** A clearing interval narrower than the grid spacing can be missed. §6 GRID-GAP handles the one case that matters.

**What survives.** INFEASIBLE requires every k to fail at least one bust gate on the EOD clock. That is close to one-sided; the remaining unsigned omissions are risk- or equity-sized legs and port kills. It is the only reading this file lets trigger the stopping rule.

### §1.3 — What each outcome means

- **INFEASIBLE** (§6): every k fails at least one EOD bust gate. It supports stopping uniform-size-cut successors of this book on this tier. Joshua adopted the stopping rule on 2026-10-08 (§9 item 6).
- **FEASIBLE** is **not** a successor result. It gives a target k range for Tier 2 and for a successor screen, which needs its own frozen pre-registration and an integer-sized book.
- Every other label is non-stopping (§6).

---

## §2 — Harness and inputs

### §2.1 — Frozen harness, reused unchanged

- Series: the depth re-run's private bundle, chained by digest. `prep.json` `feefa7ab28ff17d8b1a727bae0adf6656369a4ea73eafea2218cdafbd8f4c3b5` (RESULTS) → its `series_manifest_sha256` → the manifest → the `Tradeify_Select_100K.csv` SHA-256 in the manifest `outputs`. Any mismatch is INVALID. The series is not rebuilt.
- Reproduction target: `candidate_report.json` `4076857777e67cedd5755ba637693ce45638357a8a5b1fb17077e63ac28ec2ed` and its depth record `87a66d8e9d2baf3b474feb7e69e1e2cdb4138f27e911f666d9b57d0118e483f2` (RESULTS, depth re-run root).
- Clock: intraday-honest, paired `intraday_low` (four-firm I-12). EOD read per §4.
- Protection: mode-switching as in candidate (A) (four-firm I-17); trigger from `book_policy.CANDIDATE_TRIGGER`, unchanged at every k.
- Depth: 10,000 sims × seeds 42/123/2026, horizon 1500, inactivity OFF, pristine start (four-firm I-6, I-8, I-18).
- **G1/G2 inputs pinned.** Every call passes the k = 1 FULL values, byte-identical: `candidate_daily_pnl` = the manifest's FULL `normal.gross`; `full_res_trades`, `envelope_verdict` and `gross_edge_usd` from `prep.json`, exactly as `run_four_firm_remc.py` passes them. They are never scaled and never sliced by population. G2's hurdle does not scale with contracts, so scaling only the edge would kill tiers by artefact. G1/G2 are not this check's question. Any G1 halt or G2 kill is INVALID (§6).

### §2.2 — Venue

`Tradeify_Select_100K` only, gating on Run-2 (consistency 40%). Run-1 is reported. Other tiers are out of scope and are not scored at k ≠ 1. This uses `score_candidate(tiers=…)`, which departs from its docstring; reproduction (b) (§2.3) validates it, and the build packet is authorized with it (§9 item 7).

### §2.3 — Build needed (its own packet, review and launcher record; synthetic tests only)

1. **Wrapper** `lab/analysis/c1/size_feasibility_2026-10/run_size_feasibility.py`: public code; reads the private bundle at run time by digest; writes to a gitignored private root. It builds `TierSeries` with every channel × k, slices populations (§4.1), and calls `score_candidate` once per (k, population) with the pinned G1/G2 inputs (§2.1). It writes each report plus a depth record bound to its SHA-256, as `write_depth_record` does.
2. **EOD retention.** Opt-in capture of the guard's three arms (`eod`, `zeros`, `real`) **as each is computed, before the guard's assertions**, so the sidecar exists even when the guard raises. The `eod` arm's `headline_bust` and `pass_rate` are what §6 reads. Per tier, in a sidecar file, not in the report. Default path byte-identical.
3. **Median days-to-pass.** Opt-in retention of `run_seed`'s `days_to_pass` through `run_tier_remc`, pooled over 30,000 sims with non-passers at ∞, under T00's `LOWER_NEAREST_RANK_INF_INCLUDED`. Sidecar only; default bytes unchanged.
4. **Guard reasons.** The sidecar records each tier's `gate_grade` reason text verbatim (§6 vacuity reading).

**Acceptance tests (synthetic):**
- k = 1 through the wrapper gives report bytes identical to a direct `score_candidate` call.
- `x × 1.0` leaves every channel bit-equal.
- A Tradeify-only call's tier entry equals that tier's entry in a four-tier call.
- Sidecars off vs on: identical report bytes.
- The retained EOD arm equals the guard's internal EOD arm; the median equals a direct computation.
- Vacuity case: a synthetic series whose real and EOD arms give identical bust and pass makes the guard raise; the EOD sidecar is still present and complete, and the §6 reader labels that k `vacuity-read`. A zeros-check failure on a synthetic series reads INSUFFICIENT.
- Population slicing gives H1 = the first ⌈N/2⌉ rows and H2 = the rest, in order; the G1/G2 inputs are identical bytes in every call.

**Run-time reproduction (first arms, sidecars ON; a mismatch is INVALID and nothing else runs):**
- (a) k = 1, all four tiers, FULL: `candidate_report.json` SHA-256 equals `40768577…2ec2ed`.
- (b) k = 1, Tradeify only, FULL: its tier entry equals (a)'s Tradeify entry, as canonical JSON.

---

## §3 — Grid (fixed now)

### §3.1 — Uniform

k ∈ {**1.0**, 0.75, 0.5, 0.4, 0.33, 0.25, 0.2}. k = 1.0 is the reproduction check and an ordinary grid point. 0.33 means exactly 0.33. The only other k that may run is the GRID-GAP midpoint fixed in §6.

### §3.2 — Per-leg vectors: none

Dropped by coordinator ruling 2026-10-08 (#735 P2-4). Uniform k only. Per-leg questions (one leg's size, dropping or reshaping a leg) belong to Tier 2 and its successors. This also keeps §5's no-rebuild rule whole: per-leg channels would need the builder re-run on private exports.

### §3.3 — Early-phase (cushion-dependent) sizing

Not expressible. The kernel switches modes on drawdown from the running peak, not on cushion to the trailing floor or profit since start. Left out. Tier-2 row 5 names it; a successor would need a kernel change.

---

## §4 — Hypothesis and gates per k

**H-SIZE.** If, for some k on the grid, the rescaled book clears every §4.2 gating cell on the intraday-honest clock, then a uniform size cut is not ruled out (FEASIBLE). **Falsifier:** if every k fails at least one bust gate on the EOD clock, no uniform size cut in the grid's range rescues the book (INFEASIBLE).

### §4.1 — Populations

T00's chronological ceil partition, adapted to the daily window. N is the series row count (`n_days` in the manifest; RESULTS disclosure 1 gives 1,020 weekdays). FULL = all N rows; H1 = the first ⌈N/2⌉ rows; H2 = the remaining ⌊N/2⌋ rows. Only the four `TierSeries` channels are sliced; G1/G2 inputs are not (§2.1). Each population is bootstrapped independently at full depth and horizon, as T00 does (A2). With N = 1,020, H2 starts 102 weeks in, so its 5-day blocks keep FULL's Thursday-to-Wednesday phase (RESULTS disclosure 1). The H2 bootstrap resamples about two years into a 1500-day horizon; disclosed.

### §4.2 — Gates (each k, each clock)

| Gate | FULL | H1 | H2 | Owner |
|---|---|---|---|---|
| Run-2 headline bust ≤ 5.0% (a **bust gate**) | **gates** | reported | **gates** | v2 §3; T00 A2 |
| Run-2 P(pass) ≥ 50% (a **pass gate**) | **gates** | reported | reported (DECIDED, §9 item 1) | v2 §3; T00 A2, §6 `pass_floor_halves` |
| Median days-to-pass finite and ≤ 1500 | reported | reported | reported | v2 §3; T00 A2 |
| G7-style: Run-2 eval bust ≤ 1.0% (`clears_funded`) | reported | — | — | v2 §2 G7, §3 Part B |

- **H1 bust.** T00 A6 also gates H1 bust. Omitting it makes this check more lenient than A6, which a necessary condition allows.
- **H2 pass floor: `REPORTED`** (DECIDED, §9 item 1). T00 ratified halves as `REPORTED`, and a necessary condition must not be stricter than the successor's gate. Pass gates never decide INFEASIBLE (§6).
- **Median.** Under the T00 rule over 30,000 pooled sims, the median is finite exactly when P(pass) ≥ 50%. It adds no gate; it is reported for the successor's time-cost read.
- **G7.** The harness reads eval geometry, not funded geometry, and no Tradeify funded tier row exists. Reported only; never gates.
- **EOD clock.** The retained guard `eod` arm is the Run-2 consistency-on EOD read for that population. It never makes a k FEASIBLE; its bust gates decide INFEASIBLE (§6).

---

## §5 — Forbidden moves

- Scoring any rescaled arm before FROZEN (§R).
- Changing the grid, gates, populations or clocks after any rescaled output exists.
- Running any k other than the grid and the §6 GRID-GAP midpoint; running per-leg vectors.
- Rebuilding or editing the series; reading any private input other than the digest-chained bundle.
- Scaling or slicing the G1/G2 inputs.
- Scoring tiers other than `Tradeify_Select_100K` at k ≠ 1.
- Presenting any outcome as four-firm §4 evidence, a T00 verdict change, or a successor result.
- Replaying ports or editions (`replay_bracket`, `BookReplay`), or overriding any input.
- Publishing per-k bust, pass, median or G7 values, dollar figures, or counts from data.
- Re-using these outputs as the successor's evidence; the successor re-estimates on its own screen.

---

## §6 — Decision rule (fixed now)

**Terms.** For a valid k and a clock: *bust-clear* = every gating bust cell of §4.2 holds; *pass-clear* = every gating pass cell holds. The intraday clock reads the report; the EOD clock reads the retained guard `eod` arm.

**Validity of a k.** A k is **INSUFFICIENT** if any of its (population) calls is incomplete at frozen depth, lacks a depth record, was not run before the §8.1 budget cap was hit, lacks a valid EOD or median sidecar (the EOD sidecar is captured even when the guard raises, §2.3 item 2), or has a `gate_grade = false` reason other than the vacuity case below.

**Vacuity reading.** At k < 1, a call whose **only** `gate_grade` reason contains `real intraday_low channel is vacuous` is read **as is** (the honest arm stands, flagged `vacuity-read`) when k = 1 for the same population passed the guard. That reason text is raised only after the zeros-channel check held. Identical rates then mean that no path's outcome changed between clocks, not that the channel was dropped. A reason containing `zeros-channel must reproduce EOD`, any other reason, or a k = 1 guard failure for that population makes the k INSUFFICIENT. A strictly-negative-entry condition is not used: every trade day carries a cost in `intraday_low`, so it would almost always hold and adds no protection; the zeros check and the k = 1 condition do the work.

Labels, assigned in this order (the first that holds):

| # | Label | Trigger | Meaning | Stops? |
|---|---|---|---|---|
| 1 | **INVALID** | Digest-chain mismatch; reproduction (a) or (b) fails; any `halted_at` set; Tradeify `gated_on` ≠ `run2`; or G1/G2 inputs not byte-identical across calls | No reading. Fix and re-run under this file. | — |
| 2 | **FEASIBLE** | Some valid k is bust-clear and pass-clear on the intraday clock | Report the largest clearing k (the smallest risk cut), every clearing k, and the full curve. A target range for Tier 2 and a successor only. | No |
| 3 | **CLOCK-DEPENDENT** | Else, some valid k is bust-clear and pass-clear on the EOD clock | The coincident-sum low may drive the intraday failure. | No |
| 4 | **GRID-GAP** | Else, the gap pair exists (below) and its larger k is pass-clear on the EOD clock | A clearing interval may lie between grid points. | No |
| 5 | **PASS-LIMITED** | Else, some valid k is bust-clear on the EOD clock | Failures there are pass-driven, the side §1.2 calls not one-sided. | No |
| 6 | **INCONCLUSIVE** | Else, some k is INSUFFICIENT | An unread k could be bust-clear. | No |
| 7 | **INFEASIBLE** | Else: every k is valid and fails at least one EOD bust gate | Stopping (below). | Yes |

**GRID-GAP midpoint (fixed now).**
- **Pair:** the largest adjacent grid pair (k_hi > k_lo), both valid, where k_lo is bust-clear on the EOD clock and k_hi is not. That is the boundary at the smallest risk cut.
- **Value:** (k_hi + k_lo) / 2, rounded to 2 decimals.
- **Runs:** all three populations; both clocks (the intraday report and the EOD sidecar), with the same sidecars and validity rules.
- **Conclusions:** the midpoint is bust-clear and pass-clear on the intraday clock → FEASIBLE. On the EOD clock only → CLOCK-DEPENDENT. Otherwise, or if it is INSUFFICIENT → GRID-GAP stands. The midpoint can never produce INFEASIBLE.
- Authorized (DECIDED, §9 item 2). It runs after the grid and counts against the §8.1 cap; if the cap is hit first, it is INSUFFICIENT and GRID-GAP stands.

**Stopping rule (ADOPTED, §9 item 6).** On INFEASIBLE, stop pursuing uniform-size-cut successors of the accepted book on `Tradeify_Select_100K`. It retires no strategy. Tier 2 becomes an optional explanation. It does not bar per-leg or leg-composition successors. Every other label is non-stopping.

---

## §7 — K and exposure

- **K** = uniform k values (7) + the GRID-GAP midpoint if run (0–1): 7 or 8. Populations and clocks are conjunctive and add no K.
- **Selection.** A FEASIBLE k is the best of K, so its rates are optimistic for that reason too. The successor discloses K and re-estimates.
- **Successor disclosure.** Any successor pre-registration (a size-cut book, the Tier-2 row-5 direction, or a four-firm candidate) names this run, its K, its labels and its readers as prior looks. Readers of the private outputs are logged with the run.
- **Tier 2.** Tier-2 criteria are frozen (rows 1–4 at `34c31c4`, row 5 at admission), so this output cannot change them. It overlaps row 5's pointer: a FEASIBLE here and a row-5 hit there point the same way from different evidence. Neither confirms the other.
- **Checklist 7.6.1.** The rule covers candidate-configurable **replays** against a **pre-registered edition**. This check replays nothing: no port, bar panel, edition or input override. It transforms an already-computed daily series inside the MC, and no size-cut edition is pre-registered. So it is outside 7.6.1 as written.
  - **Borderline, flagged.** Tier-2 card §1 calls a rescale "a candidate replay". That sentence concerns `BookReplay`, but a reader could extend it here. In spirit, this check scores a candidate-like configuration before its successor pre-registration exists, which is the harm item 7.6.1's 2026-10-02 incident records. The mitigation is this file: freeze first, disclose to the successor.
  - **Operator ruling (§9 item 4):** outside 7.6.1. It is an MC rescale, not a replay against a pre-registered edition.
- **Four-firm §4.** Not evidence: Tradeify only, and the four-firm prereg §5 bars substituting sizes after output. The early-fail branch stands: any §4 candidate needs fresh operator authorization.
- **T00.** Cannot change `NO-GO-evidence-robust`. T00 A1 forbids re-sizing within T00; this check sits outside it.

---

## §8 — Cost, outputs, return

### §8.1 — Cost (from RESULTS stage timings)

- RESULTS depth re-run: the candidate stage ran 22:37:11–22:58:07Z, about 21 min for 19 arms (Bulenox 4; three tiers × 5), so **≈ 66 s per arm** (3 seeds × 10k).
- Per (k, population), Tradeify only: 5 arms (3 guard, Run-1, Run-2) ≈ **5.5 min**.
- Grid: 7 k × 3 populations = 21 calls ≈ **116 min**. Reproduction (a): ≈ 21 min. A GRID-GAP midpoint: ≈ 17 min. Total ≈ 2.3 h serial, ≈ 2.6 h with the midpoint.
- **Not a bound.** Smaller k keeps paths alive longer, so arms slow toward the full-horizon figure (four-firm I-15: 1005 s per arm, ×1.5 margin). Worst case ≈ 2.1 CPU-h per (k, population), so the cap below can bind. Arms may run in parallel; seeds are fixed, so scheduling cannot change a result.
- **Budget cap (DECIDED, §9 item 3): 12 CPU-hours total**, including the k = 1 reproduction and any midpoint arm. CPU time is the summed process CPU time of every arm, recorded per arm in `run.json`. An arm counts as run within the cap only if the running sum, including that arm, is ≤ 12 h when the arm completes.
- **Fixed run order:** reproduction (a), then (b); then k = 1 H1 and H2; then k = 0.2, 0.25, 0.33, 0.4, 0.5, 0.75 (smallest first), each k's FULL, H1 and H2 together; then the GRID-GAP midpoint if triggered. Parallel arms start in this order.
- **Cap hit:** every unrun or incomplete arm is INSUFFICIENT, so its k is INSUFFICIENT (§6) and the label cannot be INFEASIBLE.

### §8.2 — Outputs (private)

Private root: `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts/size-feasibility-<date>/` (gitignored). Per (k, population): report, depth record, EOD sidecar, median sidecar. Plus `run.json` (commands, PIDs, exit codes, stdout/stderr SHA-256) and `verdict.json`.

### §8.3 — Return (public)

- The verdict label (§6), any `vacuity-read` k labels, and, for FEASIBLE, the clearing k labels.
- The SHA-256 of every private file, the `main` SHA, the wrapper commit, and the result of reproductions (a) and (b).
- The reader list.
- No rates, medians, dollar figures or counts.

---

## §9 — Operator decisions and signature

**Source of every DECIDED item.** Joshua, 2026-10-08, in chat to the Deployment Coordinator, verbatim: "as recommended". He was answering this recommendation list, sent by the Deployment Coordinator to Joshua in chat on 2026-10-08, quoted verbatim:

> 1. Late-half pass floor: reported only.
> 2. Grid gap: one midpoint run.
> 3. Budget cap: 12 CPU-hours in total, including the reproduction and midpoint runs. Run the smallest k first (k = 1 reproduction, then 0.2, 0.25, 0.33, 0.4, 0.5, 0.75). If the cap is hit, the remaining runs count as insufficient, and the result can't be "infeasible".
> 4. Checklist rule 7.6.1: rule that it falls outside the rule, and record the ruling.
> 5. Who runs it, and when: a fresh Opus session, run by about 10-12.
> 6. Stopping rule: adopt it as written. "Infeasible" stops uniform size-cut successors of this book on Select 100K. It doesn't retire any strategy, and it makes Tier 2 an optional explanation. Every other label is non-stopping.
> 7. Build: approve it, including scoring Tradeify alone against the function's documented use; as a code PR it gets a Claude review and a Codex verdict.

Each item below is DECIDED from the quoted item of the same number.

1. **H2 pass floor: `REPORTED`** (§4.2).
2. **GRID-GAP: one midpoint arm**, as fixed in §6.
3. **Budget: 12 CPU-hours total**, including the k = 1 reproduction and any midpoint arm; fixed run order, smallest k first (§8.1). A cap hit leaves the unrun arms INSUFFICIENT, so the label cannot be INFEASIBLE (§6).
4. **Checklist 7.6.1: outside the rule** (an MC rescale, not a replay against a pre-registered edition). Operator ruling (§7).
5. **Executor:** a fresh Opus session, run by about 2026-10-12, after the build passes review. Not part of the quoted decision, but standing constraints: no GLM, and private series read in place only (AGENTS.md "Public-clone posture"; §5). Run order relative to Tier 2: independent (§7).
6. **Stopping rule: ADOPTED** (§6). The adopted text is the `bcdeac9` wording plus the amendment in quoted item 6, which Joshua accepted.
   - `bcdeac9` wording: "On INFEASIBLE, stop pursuing uniform-size-cut successors of the accepted book on `Tradeify_Select_100K`. It does not retire any strategy, close Tier 2, or bar per-leg or leg-composition successors."
   - Amendment: "it makes Tier 2 an optional explanation" (replacing "close Tier 2"), and "Every other label is non-stopping."
7. **Build packet: AUTHORIZED** (§2.3), including `tiers=("Tradeify_Select_100K",)` against the `score_candidate` docstring. A code PR with a Claude review and a Codex verdict. Synthetic tests only before the run (§R, §2.3).
- *Closed:* per-leg vectors, dropped by coordinator ruling 2026-10-08 (§3.2).
- **Signed:** Joshua, 2026-10-08, "freeze and merge 735" (in chat to the Deployment Coordinator; recorded by the Deployment Coordinator).

---

## §10 — Audit hooks

```bash
f=docs/briefs/pre-registration/2026-10-08-tradeify-size-feasibility-prereg-DRAFT.md
# Gate numbers resolve to v2 (expect 0.05 0.01 0.5).
python -I scripts/fp.py python -c "import sys; sys.path[:0]=['lab','core']; from discovery.prop_survivor_scoring import load_scoring_thresholds as l; t=l(); print(t.eval_bust_ceiling, t.funded_bust_ceiling, t.pass_floor)"
# The chain and reproduction digests are the ones RESULTS publishes.
r=lab/analysis/c1/four_firm_remc_2026-10/RESULTS.md
for d in feefa7ab28ff17d8b1a727bae0adf6656369a4ea73eafea2218cdafbd8f4c3b5 4076857777e67cedd5755ba637693ce45638357a8a5b1fb17077e63ac28ec2ed 87a66d8e9d2baf3b474feb7e69e1e2cdb4138f27e911f666d9b57d0118e483f2; do grep -q "$d" "$r" && grep -q "$d" "$f" || { echo "digest $d"; false; }; done
# Production facts §0 relies on: tiers= exists; run_seed keeps days_to_pass; summarize_outcomes drops it; the guard returns all three arms.
grep -n "tiers: Sequence\[str\] | None = None" lab/discovery/prop_survivor_scoring.py
grep -n '"days_to_pass": days_to_pass' core/mc/simulation.py
! grep -n "days_to_pass" core/mc/preflight.py
grep -n 'return {"eod": eod, "zeros": zero_arm, "real": real_arm}' lab/discovery/prop_survivor_scoring.py
# The grid is stated once; INFEASIBLE is the last label.
grep -c "k ∈ {\*\*1.0\*\*, 0.75, 0.5, 0.4, 0.33, 0.25, 0.2}" "$f"
grep -n "^| 7 | \*\*INFEASIBLE\*\*" "$f"
# No dollar figure in this file (absence exits 0).
! grep -nE '\$[0-9]' "$f"
# No result cites this file before freeze (expect no output until the run).
grep -rl "2026-10-08-tradeify-size-feasibility-prereg" lab/ || true
# At freeze only: no OWED marker (passes now), §9 signed and Status frozen (both fail while DRAFT).
! grep -nE "OWED [(]operat[o]r[)]" "$f"
! grep -nE '^- \*\*Signed:\*\* —$' "$f"
grep -nE '^\*\*Status:\*\* `FROZEN [0-9]{4}-[0-9]{2}-[0-9]{2}`' "$f"
```

## §11 — Addendum 2026-10-08, before any scoring: label semantics and the decision tree

**Authority.** Joshua, 2026-10-08, in chat to the Deployment Coordinator: "I agree with your recommendations". He was answering three recommendations:
1. add this addendum before any scoring;
2. adopt one successor decision tree with the #734 rule binding;
3. scope the R1/R2 resolution now and build it only if this check clears.

This follows an independent review relayed by Codex (on `6e79354` and #734 `c139cd7`): 2 P1 inference objections and 3 P2.

**Timing.** No arm of this file has been scored. The frozen text above is unchanged. This addendum governs where it differs.

**1. INFEASIBLE is renamed GRID-NO-CLEAR.** The §6 conditions are unchanged.
- Meaning: every required sampled k completed, and none clears this retained-series approximation.
- It does **not** exclude unsampled sizes between grid points. There is no monotonicity or interval guarantee, and state-dependent protection can break the inference from linear scaling.
- It does **not** exclude executable successors. Those have integer sizing, admissions and internal state that this harness does not model.
- It is evidence for a judgment, not a mathematical exclusion.

**2. GRID-GAP is descriptive only.** The midpoint arm cannot certify any interval.

**3. Bias directions.** Capacity and takeover, port loss stops, and rounding have no universal sign. Removing losers can help and removing winners can hurt. The §1 table and §1.2 wording claiming "optimistic" or "close to one-sided" are read as unsigned for these three.

**4. Interpretation note (descriptive, not a claim of equivalence).**
- At k = 1 this harness's Tradeify bust read sits closer to T00's favourable (R2) anchor than its pessimistic (R1) one (RESULTS.md; #724).
- So GRID-NO-CLEAR reads as "even a favourable-side approximation clears at no sampled size".
- A clear here says nothing about the pessimistic anchor.
- This check does not resolve R1/R2 and is not #734's successor-screen trigger.

**5. Stopping.** The §6 rule adopted in §9 item 6 is replaced by the successor decision tree recorded on the T00 card §8 (#734, as amended):
- **GRID-NO-CLEAR:** the Deployment Coordinator recommends stopping uniform-cut successors of the accepted book on `Tradeify_Select_100K`. That is Joshua's discretionary investment judgment, with this model uncertainty stated. No strategy is retired.
- **Any clear:** viability turns on R1/R2. Resolve it, or run the successor screen judged on the pessimistic anchor. If the pessimistic anchor is confirmed, stop (#734 rule). Otherwise, Tier 2 picks the legs and one successor screen follows.
- **Every other label** is non-stopping.

**6. Code.** The wrapper (#737) reports `GRID-NO-CLEAR` in place of `INFEASIBLE`, and re-pins the freeze gate to this file's blob after this addendum.
