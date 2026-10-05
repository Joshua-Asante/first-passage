# Pre-registration — T00 step 2: the selected-book feasibility screen (reuses prereg v2 scoring clauses; not falsifier evidence)

**Status:** `DRAFT — NOT RATIFIED.` A draft for the operator's ratification only. Nothing here binds T00 step 3 until this Status line reads `RATIFIED <date>`, every active §3 row's *Ratified value* cell and every §6 field holds a value, and the ratifying commit's SHA is recorded beside it (checked by the last audit hook). Once ratified, it does not change after any step-3 output is visible ([prereg v2 §5](2026-08-26-prop-survivor-scoring-prereg-v2.md#5--forbidden-moves--same-as-v1-plus-one-new-item-this-reopening-itself-creates), last v1 item; [amendment §T00](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#t00--feasibility-evidence-for-the-selected-book-new-investment-decision-not-a-gate-250k500k-may-return-early) step 2: "verbatim before execution, unchanged after").

*2026-10-02: A5/A6 frozen before the T00 screen build (design #629 §12 item 5, operator-approved; design §8 step 3). Frozen bytes: identical from `f0208f37b8722d177b46a8751440a920c987377a` through this file's merge into `main`; the frozen revision of record is that merge commit, which build card #634 §8 PR-2 records. Section hashes (SHA-256, each from its `###` heading line up to, not including, the next heading line; build card #634 §2.6): A5 `a8f6f25e025a2e136e477580b7e569531d770a1e35e712b72f5a6b9b50eb391b`; A6 `b3bdc77baf3e6383f1df08afd2f0fbb8a7c930d95a0f56b0c5669a5e18b217d9`. #581 merges as DRAFT; ratification and the remaining §3 values follow under the A1 order; ratification must leave these bytes unchanged.*

**Authority:** operator ruling 2026-10-01, item 6, ["first-session simplification rulings"](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-10-01--first-session-simplification-rulings-six-cuts), as corrected at #580 `e627247` (Codex P1 on #580; on `main` since #580 merged as `dd94b41`): "The step-2 pre-registration reuses `2026-08-26-prop-survivor-scoring-prereg-v2.md` by citing **its reusable scoring clauses only**. It does **not** import that preregistration's falsifier disposition (G8). **A T00 screen is not four-firm §4 falsifier evidence** (operator ruling 2026-09-23, condition 4). The step-2 contract states that non-falsifier disposition itself. It adds only the expressions, pass floor, scenarios, intraday clock, NO-GO condition and the counting of R1/R2 `UNDETERMINED` days." The ruling also says it "may be drafted now … Ratification stays the operator's act."
**Owner of T00:** [amendment §T00](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#t00--feasibility-evidence-for-the-selected-book-new-investment-decision-not-a-gate-250k500k-may-return-early) and its [D-T00 row](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#d-t00--tick-step-1-now-the-one-decision-on-the-1108-clock). This file is the step-2 artifact those owners name; it does not restate them.
**Loop of record:** STRATEGIC (investment decision; it gates neither T02, admission nor the four-firm falsifier, and it is D-feed condition (a), §1b).
**Authored:** 2026-10-01, Claude Code worker (drafting only) for the coordinating session "Coordinating parallel Claude sessions". Joshua owns every **OPERATOR TO SET** value, every open decision in §4 and the ratification.

**This draft authorizes nothing:** no screen, Monte Carlo, replay, T00 step-3 run, dispatch, provider contact, spend, deployment or arm. It contains no Pine source, port, account identifier, account figure or private value; private inputs are named by their already-public digests only.

---

## §0 — Owners read (anchors: `origin/main@bd30646`)

| Owner | What it fixes here |
|---|---|
| [prereg v2](2026-08-26-prop-survivor-scoring-prereg-v2.md) §2–§7 | Every number this file adopts: Part A bust ceiling **5.0%**, pass floor **P(pass) ≥ 50%** with a finite median inside horizon **1500**, Run-2 (consistency-on) gating, seeds **42/123/2026**, depth **10k**, inactivity disabled, overlay OFF |
| [`docs/load_bearing_numbers.md`](../../load_bearing_numbers.md) §1–§3 | EOD-clock bust figures are lower bounds; published figures assume inactivity OFF; 5.0% / 50% are live, owned by prereg v2 |
| [Amendment §T00 and D-T00 row](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#t00--feasibility-evidence-for-the-selected-book-new-investment-decision-not-a-gate-250k500k-may-return-early) | Step-2 contents; GO-evidence / NO-GO-evidence / INSUFFICIENT; "adopts it or states why the selected book falls outside it"; condition 4 ruled **NO** 2026-09-23, verbatim: "A T00 screen does not count as falsifier evidence" |
| [D-feed row](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#d-feed--tick-as-a-gate-not-a-provider) | Condition (a): provider-specific work opens only on a T00 verdict other than INSUFFICIENT or NO-GO-evidence |
| [T00 step-1 packet](../handoffs/2026-09-22-tradeify-t00-step1-producer-inventory.md) §7.4, §7.9 item 5 (line 312) | Candidate 3′ (`ops/c1_rail/qualification/`) is the producer; "Step 2 should say, before any run, how R1/R2 disagreement days (`UNDETERMINED`) count" |
| [P7-closure packet](../handoffs/2026-09-24-tradeify-t00-p7-closure.md) §7, landed with #594 at `c3ab0cc` | Step 1 **RESOLVED (P7 MET)** at code `2baa516`, then the post-S5 obligation **discharged**: the [step-1b re-run](../handoffs/2026-09-24-tradeify-t00-p7-closure.md#step-1b-re-run-return--2026-10-02-executor-local-claude-opus) was accepted by the coordinator at merge head `b2c9f9c` (`code_closure_sha256` `48bdc104…9139`), and `c3ab0cc^{tree}` equals `b2c9f9c^{tree}`. Contract **r3c unchanged** (`a526b50f…8d97`: 25 roles, FULL 997 / H1 499 / H2 498, PRISTINE `initial_state`); fresh approval `r3c-a2` valid until 2026-10-09T01:52:19Z. Carried to T05: P3-1 (no real-run coverage of the deadline-failure branch) and P3-2 |
| [Source-only contract design](../../superpowers/specs/2026-09-30-t00-source-only-contract-design.md) §2.2, §2.4 | What r3c binds: `port_runtime_pins` equal to `book_adapters.ADAPTERS`, `effective_settings` equal to `RUNTIME_EFFECTIVE_INPUTS_SHA256`, four admitted-panel roles at the Step 3 admission digests, eight source roles including `cost_model`; its `refusals` include `SCREEN` and `MONTE_CARLO` |
| [Bracket convention](../phase3-preparation/2026-09-15/schedule-execution-evidence.md#addendum-2026-09-23--path-position-bracket-convention-ratified-2026-09-23) (ratified 2026-09-23) | R1/R2 are evaluated independently; a path's outcome is taken only where they agree, else `UNDETERMINED`, "reported as its own count and never folded into PASS or BUST"; "How UNDETERMINED paths enter the frozen pass-rate gates is an F1 definition" |
| `ops/c1_rail/qualification/runner.py:20–44` (`evaluate_replay`) | The kernel call: `Tradeify_Select_100K`, `inactivity_off=True`, `consistency=.40`, the replay's own `intraday_low`, `dd_scale=1.0`; outcome PASS / FAILURE / UNRESOLVED; `own_flat_deadline` is a FAILURE unless the kernel passed earlier, and the kernel's own status is kept as the `kernel_outcome` diagnostic |
| `ops/c1_rail/qualification/bracket.py:96–134` (`BracketVerdict`, `run_bracket`); `production_source.py::replay_bracket` | UNDETERMINED is a **path** verdict, from two fresh engines, comparing status only; each run keeps its own `sessions_to_pass` and failure reason |
| `ops/c1_rail/qualification/replay.py:38–47, 470–480` | `ReplayNeedsContext` is missing evidence ("no successful result exists"); `ReplayDeadlineFailure` is a confirmed own-flat breach carrying the run's series through the breach session ("never a coverage exclusion") |
| `ops/c1_rail/qualification/blocks.py` (`JointFlatBlocks`, `partition_populations`) | Paths are drawn from independent FULL / H1 / H2 populations |
| [Protection selection note](../../notes/2026-09-10-tradeify-protection-selection.md) "Selected book", "Protection behavior selected" | The four legs, captured settings, 1% / 0.40 combined-peak protection, ORB base unreduced, ORB adds off when protected, 80-micro capacity, Aegis-priority takeover |
| [Feasibility-screen plan](../../superpowers/plans/2026-09-10-tradeify-feasibility-screen.md) Task 1 (CLOSED) and its [closure](../../notes/2026-09-10-tradeify-protection-selection.md#feasibility-screen-closure) | The only previously frozen scenario formulas; the closure's finding of "an incorrect all-halves speed requirement" |
| Campaign record [§6 D23](../programs/2026-09-03-seven-strategy-select-campaign-state.md) | Pristine-versus-used initial state is a real fork for a Tradeify score |

---

## §1 — What is reused from prereg v2, and the disposition this file states itself

### §1a — Reused scoring clauses, by section

T00 step 2 cites [prereg v2](2026-08-26-prop-survivor-scoring-prereg-v2.md), frozen 2026-08-26, for the clauses below **only**, and changes none of their numbers. Nothing else in prereg v2 is imported.

| prereg v2 clause (section) | Reused for | Mapping onto T00 |
|---|---|---|
| §3 Part A thresholds: headline bust **≤ 5.0%** (daily + static + trailing), **Run-2**, at the $100K band, paired with **P(pass) ≥ 50%** and a finite median inside the horizon | The screen's thresholds (§2 A2, A6) | `load_bearing_numbers.md` §3 names v2 the owner of 5.0% / 50%. Per-partition application is §2 A2 |
| §3 frozen tier cross-section, the `Tradeify_Select_100K` row only | The scored tier | T00 asks about the selected book on Tradeify Select alone |
| §2 G4 run parameters: 10k sims × seeds 42/123/2026, horizon 1500, inactivity disabled, run twice and score Run-2 | Depth, seeds, horizon, consistency gating | Depth per FULL/H1/H2 population is **OPERATOR TO SET** item 1, because the qualification runner draws per population (`runner.py:55–59`) and v2 has no population axis |
| §2 G5 and §7 item 2: the headline bust is daily + static + trailing, read through the bucket-sum-checked definition | The bust numerator | `evaluate_replay` reports one more FAILURE reason (`own_flat_deadline`). §2 A5 (1) classifies every reason; **OPERATOR TO SET** item 3 decides only the deadline-only case |
| §7 item 1: ceiling numbers 5.0% / P(pass) ≥ 50% / finite median inside horizon 1500 | The same thresholds, as frozen | — |
| §7 item 5: Tradeify `consistency_frac` 40%, Run-2 gating | Consistency | Run-2 is what `evaluate_replay` runs (`consistency=.40`, `runner.py:27`). Whether a Run-1 diagnostic is owed is **OPERATOR TO SET** item 5, because the runner has no consistency-off mode |
| §7 item 6: overlay OFF for scoring | No second protection overlay | The kernel receives `dd_scale=1.0` (`runner.py:31`). The book's own 1% / 0.40 protection runs inside the replay (`test_runner.py::test_kernel_uses_intraday_and_no_second_scaling`) |
| §5 last v1 forbidden move: no number amended after a result is visible | The freeze discipline of this file | Applies to this file's own values once ratified |

### §1b — Disposition: this screen is **not** four-firm §4 falsifier evidence

Stated here as this contract's own disposition, not imported from prereg v2:

- **A T00 screen does not count as falsifier evidence** (operator, 2026-09-23, condition 4, verbatim; [D-T00 row](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#d-t00--tick-step-1-now-the-one-decision-on-the-1108-clock) "Condition 4 ruling"). Whatever step 3 returns, it neither discharges nor fires the four-firm §4 falsifier dated 2026-11-08. It does not change that falsifier's 0-of-4 clearer count, and it is not a "dated lab re-MC of a pre-registered candidate" for that clock. The falsifier needs its own dated re-MC regardless of T00.
- **Not imported from prereg v2:** the G8 admission and falsifier disposition; §4 H-SCORE; the §6 verdict table (RESOLVED / FALSIFIED / AMBIGUOUS); the §3 discharge rule (≥ 2 firms, ≥ 1 `trailing_locking`) and F2 labels; the §4 ceiling-mis-set reject and its §7 item 9 calibration reference; §7 item 8 (all-null close); G0–G2 intake, E1 reduction and cost-law gate; G6 routing; Part B and G7 funded diagnostics. These are the falsifier and survivor-admission machinery, or funded-phase scaling, and none of them is a scoring clause the screen needs.
- **What a T00 verdict is instead:** GO-evidence, NO-GO-evidence or INSUFFICIENT, an operator investment decision ([amendment §T00](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#t00--feasibility-evidence-for-the-selected-book-new-investment-decision-not-a-gate-250k500k-may-return-early)). It does not gate T02 (amendment §T00: "it does not gate T02"), it admits nothing, and no lifecycle CANDIDATE status, capital authorization or deployment follows from it.
- **Where it does gate: D-feed condition (a)** (consumed at CP-7, the feed-funding checkpoint). Under the standing [D-feed wording](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#d-feed--tick-as-a-gate-not-a-provider) (ratified 2026-09-22), provider-specific work opens only when "T00 returns a verdict other than INSUFFICIENT or NO-GO-evidence", together with condition (b). This file does not amend that wording. As written, an INSUFFICIENT or NO-GO-evidence verdict does not meet (a). Whether an operator's acceptance of a NO-GO's risk into F1 changes that is open decision §4 OD-1, decided at the D-feed owner.
- **Regime caveat.** prereg v2 §7 item 7 is not imported as a gate. The independent FULL / H1 / H2 populations (§2 A2) give the half-sample view, and no regime gate is added.

---

## §2 — The six additions (and nothing else)

### A1 — The expressions (by identity; no values restated)

Exactly the four legs of the Tradeify portfolio, at the identities **T00 step 1 resolved P7 for**, bound by source-only contract r3c `a526b50fa75e68451bdd2b5b57fa7a04e6ee08e61f96865c915ae8116a848d97` ([P7-closure §7](../handoffs/2026-09-24-tradeify-t00-p7-closure.md#step-1b-re-run-return--2026-10-02-executor-local-claude-opus): r3c unchanged through the step-1b re-run; its field and role sets are the [contract design](../../superpowers/specs/2026-09-30-t00-source-only-contract-design.md) §2.2 and §2.4):

| Leg | Identifier | Binding in r3c |
|---|---|---|
| Aegis 6J | `aegis_6j` | `port_runtime_pins`, equal to the `book_adapters.ADAPTERS` pin (`ops/c1_signal_daemon/book_adapters.py`); role `aegis_runtime_port` |
| Striker MYM | `dj30_mym_p250` | the same, at the **corrected** port `efd479b6…`; the preserved original `c81aa59c…` is a named refusal; role `striker_runtime_port` |
| Vanguard MGC | `vanguard_mgc` | the same; role `vanguard_runtime_port` |
| ORB MNQ | `orb_mnq_v7` | the same; role `orb_runtime_port` |

- **Captured sizes and allocations:** the [protection selection note](../../notes/2026-09-10-tradeify-protection-selection.md) "Selected book" table, as reproduced per expression by candidate 3′ ([step-1 §7.4](../handoffs/2026-09-22-tradeify-t00-step1-producer-inventory.md#74-p1p7-per-candidate-the-selected-four-aegis-6j-vanguard-mgc-striker-mym-orb-mnq) "What 3′ reproduces"). Effective inputs: r3c's `effective_settings`, equal to `RUNTIME_EFFECTIVE_INPUTS_SHA256` (`book_adapters.py:72`) with `orb_normal_base == 1`, never `66406dee…`.
- **Policy:** the candidate book protection policy (`ops/c1_rail/book_policy.py::candidate_book_protection_policy`): combined-peak 1% trigger, 0.40 scale, prior-close timing, ORB base unreduced, ORB adds off when protected, 80-micro capacity refusing rather than clipping, Aegis-priority whole-leg takeover. This is code, not an r3c field; it is bound by the accepted P7 record's `code_closure_sha256` (§0).
- **Panels:** r3c's four admitted-panel roles, each at the Step 3 admission's digest for its leg ([identity ledger](../phase3-preparation/2026-09-15/identity-ledger.md)): the MYM, MGC and MNQ M15 panels pinned in `core/data/bar_data/SHA256SUMS`, and for Aegis the attested-prefix derivative `8ae083d0…`, **not** the unprefixed `6J_M15.csv` in that manifest.
- **Populations:** FULL 997 / H1 499 / H2 498 sessions, chronological ceil partition, as bound by contract r3c.
- **No re-optimization, re-sizing or substitution** ([amendment §T00](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#t00--feasibility-evidence-for-the-selected-book-new-investment-decision-not-a-gate-250k500k-may-return-early) "Forbidden"). Route-native editions are **not** these expressions; see open decision §4 OD-2.

r3c fixes identities only. Its `purpose` is `T00_P7_SOURCE_VERIFICATION` and its `refusals` include `SCREEN` and `MONTE_CARLO`, so it cannot drive step 3 (§5 item 3). Step 3 runs only at a head where a P7 record for these identities is accepted through `accept_p7_record`. The record accepted on 2026-10-02 authenticates the `c3ab0cc` tree; a step 3 at any other head needs a P7 record accepted at that head.

### A2 — Pass floor (and the ceiling it is paired with), per partition

Thresholds are prereg v2's, unchanged. Per-partition application:

| Quantity | FULL | H1 | H2 | Owner of the value · owner of the per-partition application |
|---|---|---|---|---|
| Bust ceiling (§A5 pessimistic count) | **≤ 5.0%** | **≤ 5.0%** | **≤ 5.0%** | prereg v2 §3 · [Track B prereg](2026-09-12-track-b-final-validation-prereg.md) §2 failure limbs F-full/F-H1/F-H2 and the 09-10 formal objective ("full/H1/H2 … failure bounds at most 5%") |
| Pass floor P(pass within 1500) (§A5 pessimistic count) | **≥ 50%** | **OPERATOR TO SET** item 2 | **OPERATOR TO SET** item 2 | prereg v2 §3 · FULL only by default, because the 09-10 closure found "an incorrect all-halves speed requirement" and no owner applies the floor to the halves |
| Median sessions-to-pass (non-passing paths at T = ∞; each path's day per A5) | finite, ≤ 1500 | reported | reported | prereg v2 §3, §7 item 1 |

Each population is evaluated **independently**, at its own depth (`runner.py:55–59`; `adjudication.py` requires FULL/H1/H2). Values are **point estimates** over the paths, as prereg v2 scores its headline; no confidence bound is added.

### A3 — Scenarios

**S0, the gating scenario.** A1's book and policy; `initial_state` **PRISTINE** (contract r3c, matching prereg v2's $100K common band); the source pack's reviewed `cost_model` (one cost model, no stress multiplier); inactivity OFF; consistency 40%; both bracket runs R1 and R2 on every path; the paths and seeds of §3 items 1 and 4.

**Candidate further scenarios.** Each has an owner. Whether it is run, and whether it gates, is **OPERATOR TO SET** item 7. This draft adds none of them by itself.

| Candidate | Owner | Note |
|---|---|---|
| S1: used-account initial state (the live incumbent eval) | Campaign §6 D23(a), §17 | The scored account is pristine while any deployment would use the used eval. The snapshot values are private. A stale snapshot is a new input, not a scenario parameter |
| S2: the 09-10 cash-flow probes (gains × 0.90; losses × 1.10) | [09-10 screen plan](../../superpowers/plans/2026-09-10-tradeify-feasibility-screen.md) Task 1 (CLOSED) | These scale daily P&L uniformly. T00's own P1 finding is that uniform scaling cannot reproduce the book's integer sizing, ORB base/add, capacity or takeover. On a bar-level replay they would be a post-hoc transformation of the producer's output, not a replay |

### A4 — The intraday clock (mandatory)

- The **only** admissible clock is intraday-honest. Each bracket run's own `SessionRecord.intraday_low` series (unscaled excursions from the day's opening equity, every entry `<= 0`, exact horizon, or through the breach session for a run that ends in a confirmed own-flat deadline failure, A6) is passed with **that run's own** daily P&L to `simulate_path` through `runner.evaluate_replay` ([D-T00 wording](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#d-t00--tick-step-1-now-the-one-decision-on-the-1108-clock); `core/mc/simulation.py:325–345`).
- An **EOD-clock** result, or a path without a synchronized `intraday_low`, is **inadmissible** to the verdict. Under [`load_bearing_numbers.md` §1](../../load_bearing_numbers.md#1-standing-rule--eval-bust-figures-are-eod-clock-lower-bounds) any EOD-clock bust figure is a lower bound only, and the amendment forbids "EOD-clock 'zero bust' as survival". Its absence makes the verdict **INSUFFICIENT**, never GO.
- The convention's labelled **hybrid** (R2's P&L with R1's lows) may be reported but never enters the verdict ([bracket convention](../phase3-preparation/2026-09-15/schedule-execution-evidence.md#addendum-2026-09-23--path-position-bracket-convention-ratified-2026-09-23) "Verdict").
- The inactivity barrier is **OFF** with the operator-placed weekly token trade as the mitigation ([`load_bearing_numbers.md` §2](../../load_bearing_numbers.md#2-standing-rule--every-published-figure-assumes-the-inactivity-barrier-is-off)); `evaluate_replay` raises `inactivity_limit` past the horizon (`runner.py:28–30`).

### A5 — How R1/R2 `UNDETERMINED` counts

**Unit.** The ratified convention defines `UNDETERMINED` per **path**: a path whose R1 and R2 evaluations disagree on PASS / FAILURE / UNRESOLVED (`bracket.py:96–134`). Per-session R1/R2 differences in P&L or `intraday_low` are expected by construction wherever an intrabar split is consumed, so they carry no verdict role. The step-1 packet's "disagreement days" wording is read as this path-level verdict. Step 3 reports, per population, the count of paths with a consumed split and the count of `UNDETERMINED` paths, descriptively.

**Counting rule (drafted; the operator ratifies or replaces it under §3 item 8).** The rule has three frozen parts: how each run is classified, how an agreed path's two runs are combined, and how `UNDETERMINED` paths are assigned. `BracketVerdict` compares status only and keeps each run's own `sessions_to_pass` and failure reason (`bracket.py:96–112`), so the first two parts are needed for every path, not only for `UNDETERMINED` ones. No part is chosen after any step-3 output exists.

*(1) Run classification.* Each run's `PathOutcome` (`model.py:238–253`) falls into exactly one class. The headline reasons are prereg v2's daily + static + trailing: `bust_daily`, `bust_static`, `bust_trailing`.

| Run outcome | Class |
|---|---|
| PASS | **pass**, at that run's `sessions_to_pass` |
| FAILURE with a headline reason | **bust** |
| FAILURE `own_flat_deadline` whose `kernel_outcome` diagnostic is any `bust_*` status | **bust**. The kernel found a bust within the sessions this run replayed, which end at the breach session (`runner.py:31–37`) |
| FAILURE `own_flat_deadline` with any other `kernel_outcome` | **deadline-only**: a bust if §3 item 3 counts it, otherwise neither bust nor pass |
| FAILURE `bust_inactivity` | **bust**. It is unreachable at the runner's barrier setting (`runner.py:28–30`); the row exists so that every reason has a class |
| UNRESOLVED (`horizon_cap`) | **open**: neither bust nor pass |

*(2) Agreed paths (both runs share a status).* The same rule applies under both assignments, so the two assignments differ only in `UNDETERMINED` paths.
- **Agreed PASS:** the path passes at the **later** of its two runs' `sessions_to_pass`. That day is the path's value for P(pass within 1500) and for the median.
- **Agreed FAILURE:** the path is in the bust numerator if **either** run is a bust under (1). Otherwise, with both runs deadline-only and §3 item 3 not counting them, it is in neither numerator. It is never a pass, so its T is ∞.
- **Agreed UNRESOLVED:** neither numerator; T = ∞.

*(3) `UNDETERMINED` paths.* The `UNDETERMINED` count stays separate, as the convention requires. Each threshold in A2 is evaluated under two assignments:

| Assignment | Bust numerator | Pass numerator (and median day) | Use |
|---|---|---|---|
| Pessimistic | agreed paths that are busts under (2) + **all** `UNDETERMINED` | agreed PASS only; every `UNDETERMINED` path at T = ∞ | **Decides GO-evidence** |
| Optimistic | agreed paths that are busts under (2) only | agreed PASS + each `UNDETERMINED` path **one of whose runs passed**, at that run's `sessions_to_pass`. A FAILURE-versus-UNRESOLVED path has no passing run, so it is in neither numerator and its T is ∞ | **Labels** a NO-GO as robust or as `UNDETERMINED`-dependent |

The optimistic assignment takes each `UNDETERMINED` path at the better outcome one of its runs actually produced. It assigns no pass day that neither run produced.

The denominator is always every path in the population. `UNDETERMINED` paths are never dropped, and agreement is never conditioned on.

**Consequence.** A high disagreement share cannot turn the screen back into INSUFFICIENT, which is the [T00→T10→CP-7 note §3](../../notes/2026-09-29-t00-t10-cp7-sequence.md) step-4 concern. It can only prevent GO-evidence.

*Alternatives the operator may prefer, stated so the choice is explicit:* (i) exclude `UNDETERMINED` from the denominator, which is optimistic and conditions on agreement; (ii) a cap on the `UNDETERMINED` share above which the result is INSUFFICIENT. There is no owner for such a cap, so it would be **OPERATOR TO SET**; it also reintroduces the INSUFFICIENT route the CP-7 note warns about.

### A6 — The NO-GO condition (verbatim; not to be edited after any step-3 output exists)

> **INSUFFICIENT** if any of: either bracket run of a path stops for want of producer or model context (`ReplayNeedsContext`, a source refusal, or a series that ends short of the horizon without a confirmed deadline failure); any run lacks its own synchronized `intraday_low` for a session it replayed; P7 is not accepted for A1's identities at the executing head; the runner raises `NeedsContext` (budget, missing prerequisite, or a budget probe that cannot complete a full path, including one that ends in a deadline failure, `runner.py:100–102`; the probe is a timing measurement in its own RNG domain, not a scored path) before every population reaches its frozen depth; or any §3 item is unset. No reduced depth, substitute clock or extra draw is run in its place.
>
> **A confirmed own-flat deadline failure on a scored path is a scored outcome, never INSUFFICIENT.** Such a run ends at its breach session. The replay raises `ReplayDeadlineFailure` with the run's own series through that session (`replay.py:42–47, 470–480`). `run_bracket`, `ProductionSource.replay_bracket` and the runner take that series as the run's result (`bracket.py:128–132`; `runner.py:100–103`), and `evaluate_replay` scores it FAILURE `own_flat_deadline` unless the kernel passed before the breach (`runner.py:33–37`). The run is classified under A5 (1), and §3 item 3 decides whether a deadline-only run is a bust.
>
> Otherwise, in scenario **S0** (and any scenario §3 item 7 makes gating), with `UNDETERMINED` paths counted under the **pessimistic** assignment of A5:
>
> **GO-evidence** if, for FULL, H1 and H2 each, the A5 bust proportion is **≤ 5.0%**, **and** FULL's P(pass within 1500 sessions) is **≥ 50%** with a finite median sessions-to-pass inside 1500 (and H1/H2 likewise if §3 item 2 so sets).
>
> **NO-GO-evidence** otherwise. It is labelled **robust** if it also fails under the optimistic assignment, else **`UNDETERMINED`-dependent**. Both labels are NO-GO-evidence.
>
> A NO-GO-evidence verdict is presented to the operator as an investment decision (adjust the book, or accept the risk into T15's F1), never routed automatically to a portfolio-adjustment packet ([amendment §T00](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#t00--feasibility-evidence-for-the-selected-book-new-investment-decision-not-a-gate-250k500k-may-return-early) step 3). As the standing D-feed wording is written, an INSUFFICIENT or NO-GO-evidence verdict does not meet D-feed condition (a) (§1b); whether an operator-accepted NO-GO does is open decision §4 OD-1.
>
> No verdict under this condition, GO-evidence included, is four-firm §4 falsifier evidence (§1b).

---

## §3 — OPERATOR TO SET (no owner supplies these values; all are set before ratification)

| # | Item | Candidates with owners, if any | Why it is not decided here | Ratified value |
|---|---|---|---|---|
| 1 | **Path depth per population**, and **compute budget** (`budget_seconds`, required by `runner.SyntheticStageRequest` / the production executor) | prereg v2 G4: 10,000 per seed × 3 seeds | v2 has no FULL/H1/H2 axis. Whether 10k × 3 applies to each population is not stated. Bar-level replay cost is unmeasured at this depth × 2 runs × horizon 1500. The runner refuses a batch whose probe exceeds the budget (`runner.py:110–111`) | values block: `depth_per_root`, `budget` |
| 2 | **Pass floor on H1 and H2**: binding, or reported only | prereg v2 §3 50% (value) | The 09-10 closure found an all-halves speed requirement incorrect. No owner applies the floor to halves | values block: `pass_floor_halves` |
| 3 | **A deadline-only run in the bust numerator** (A5 (1): FAILURE `own_flat_deadline` whose `kernel_outcome` is not a `bust_*` status; a `bust_*` `kernel_outcome` is a bust either way) | `evaluate_replay` classifies it FAILURE (`runner.py:36–37`); a confirmed breach is scored, not INSUFFICIENT (A6). The deadline is Tradeify's blanket account-level 16:45 ET rule, or 12:59 ET on D19 dates (P7-closure, operator ruling 2 of 2026-09-30) | prereg v2's headline bust is daily + static + trailing only. *Drafter's note:* counting it is the conservative reading, because it is an account rule breach | values block: `deadline_only_is_bust` |
| 4 | **Path construction**: block family and length, RNG root namespaces derived from seeds 42/123/2026, path start | `JointFlatBlocks` exists (`blocks.py`); Track B prereg §2 leaves block family/length `OWED-BY: TB-F1`; contract r3c's `path_start_date` 2022-09-01 is PROPOSED, a label origin | No owner has frozen the block family or length | values block: `rng`, `block`, `path_start_date` |
| 5 | **Run-1 (consistency-off) diagnostic**: owed or waived | prereg v2 §2 G4 runs twice, gating on Run-2 | `evaluate_replay` fixes `consistency=.40`. Run-1 would need a runner change; it never gates | values block: `run1_diagnostic` |
| 6 | *Withdrawn 2026-10-01:* prereg v2 §7 item 9 calibration reference | — | Not imported. It serves §4's ceiling-mis-set reject, which is part of the falsifier disposition the #580 `e627247` correction excludes (§1b). The row is kept so the numbering stays stable | withdrawn |
| 7 | **Scenarios beyond S0** (S1 used-account, S2 cash-flow probes, or none) and whether any gates | §2 A3 table | Choosing scenarios is the operator's step-2 act. S1 needs a fresh private snapshot; S2 conflicts with T00's P1 finding | values block: `scenarios` |
| 8 | **The A5 counting rule**: ratify all three parts as drafted (run classification, agreed-path aggregation, `UNDETERMINED` assignment), or replace them | Bracket convention (path-level verdict); CP-7 note §3 step 4 | The convention leaves gate entry to "an F1 definition"; no owner has written it | values block: `a5_rule` |

---

## §4 — Open operator decisions (stated, not decided)

**OD-1. How D-feed condition (a) treats a NO-GO T00 result whose risk the operator accepts into F1.** D-feed (a) reads: provider-specific work opens when "T00 returns a verdict other than INSUFFICIENT or NO-GO-evidence" ([D-feed row](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#d-feed--tick-as-a-gate-not-a-provider)). Amendment §T00 step 3 separately lets the operator "accept the risk into T15's F1". The first-session rulings' item 6 records this as **still open**. Readings, none adopted here:
- **(a) Literal.** NO-GO-evidence leaves (a) unmet whatever the operator accepts. Provider-specific work opens only through a dated amendment of the D-feed wording.
- **(b) Acceptance satisfies (a).** An operator acceptance recorded in the F1 packet converts the NO-GO into an accepted risk, and (a) is treated as met from that record's date. D-feed condition (b) is still required independently.
- **(c) Label-sensitive.** Acceptance satisfies (a) only for an `UNDETERMINED`-dependent NO-GO (§2 A6); a robust NO-GO needs (a)'s amendment.

Whatever is chosen should be recorded at the D-feed owner, not here, before step 3 returns. The step-3 verdict must not be the input that chooses it.

**OD-2. Declared expressions versus route-native editions.** A1 pins the identities P7 was resolved for. Campaign §59 rulings 3–5 adopt route-native editions of ORB, Striker and (option A) Vanguard for this route. Their pre-registrations are the 2026-10-02 successors ([ORB/Striker successor](2026-10-02-tradeify-route-native-editions-successor-prereg.md), [Vanguard successor](2026-10-02-tradeify-vanguard-fixed-stop-edition-successor-prereg.md)); the 2026-09-25 and 2026-09-26 originals are CLOSED for replay-output exposure and kept only as records. Both successors are DRAFT, not frozen, and no P7 exists for the editions. Their §R standing rule (operator ruling 2026-10-02) forbids any candidate-configurable replay of an edition before its pre-registration is frozen. If the operator wants T00 to screen the editions, A1 changes, and the successors' freeze and P7 for those identities become step-3 prerequisites. If T00 screens the declared book, a GO-evidence result speaks to the declared expressions only.

---

## §5 — Dependencies before step 3 (recorded; none is granted by this file)

1. Ratification of this file, with §3 complete.
2. A P7 record for A1's identities accepted through `accept_p7_record` at the executing head. The post-S5 re-run is done: the record accepted 2026-10-02 authenticates the `c3ab0cc` tree (§0). Every source use also needs an unexpired source approval; `r3c-a2` expires 2026-10-09T01:52:19Z, so a later run needs a fresh one.
3. A step-3 executor packet and a separately signed `t00_screen_authority/v1` authority under `APPROVE_T00_SCREEN_AUTHORITY`, bound to r3c, the accepted P7 record at the executing head and this ratified pre-registration ([screen-authority design](../../superpowers/specs/2026-10-02-t00-screen-authority-design.md), operator ruling A2, 2026-10-02). The ledgered screen run builds its own source and uses `screen_authority.screen_epoch(source, *, authority)` and `screen_authority.screen_bracket(source, path, *, authority, epoch)` inside its screen-bootstrap workers (PB2-1 [#686](https://github.com/Joshua-Asante/first-passage/pull/686)). The source-only receipt's refusals remain unchanged; the screen authority authorizes step 3. P7 output remains excluded from screen inputs; only its acceptance bindings are consumed as a precondition.
4. Results stay under the private root with `results.json` / `REPORT.md` bound to ledger digests ([amendment §T00](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#t00--feasibility-evidence-for-the-selected-book-new-investment-decision-not-a-gate-250k500k-may-return-early) step 3). A public bust or pass figure cites that intraday-honest RESULTS path (`load_bearing_numbers.md` §1).
5. **ORB-3 and VAN-3 are answered first.** The answers to ORB-3 ([ORB/Striker successor](2026-10-02-tradeify-route-native-editions-successor-prereg.md)) and VAN-3 ([Vanguard successor](2026-10-02-tradeify-vanguard-fixed-stop-edition-successor-prereg.md)), the rows that name what replaces the trail as an exit, are recorded in those rows, with each answerer's exposure statement, before any step-3 output exists. This is a standing rule: operator ruling 2026-10-02 (sheet A3), confirmed "yes to A3" to coordinator (3).

---

## §6 — Ratification (operator; blank until ruled)

The §3 values are recorded in §3's *Ratified value* column.

- **Ruling:** —
- **OD-1 / OD-2:** Operator ruling 2026-10-02 (sitting 2) (Joshua, "all recommended", 2026-10-03T01:42Z). **OD-1:** reading (c), label-sensitive, recorded at its owners, the [D-feed row](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#d-feed--tick-as-a-gate-not-a-provider) and [checklist §4 CP-7](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#4-operator-checkpoints--where-approval-is-taken). **OD-2: the declared book.** A1 stands as drafted, and T00 screens the four declared expressions. A GO-evidence result speaks to them only. Evidence on the route-native editions comes from their own pre-registration §6 requalification, not from T00.
- **Ratifying commit SHA:** —

---

## Audit hooks

```bash
# The reused numbers are prereg v2's, and the loader still resolves v2 (expect 0.05 / 0.01 / 0.50).
python -I scripts/fp.py python -c "import sys; sys.path[:0]=['lab','core']; from discovery.prop_survivor_scoring import load_scoring_thresholds as l; t=l(); print(t.eval_bust_ceiling, t.funded_bust_ceiling, t.pass_floor)"

# The kernel call this file binds to: Tradeify Select, inactivity OFF, consistency 40%, own intraday_low.
rg -n "firm_kwargs\('Tradeify_Select_100K', inactivity_off=True, consistency=.40" ops/c1_rail/qualification/runner.py

# UNDETERMINED is a path verdict from two runs; each run keeps its own outcome.
rg -n "UNDETERMINED" ops/c1_rail/qualification/bracket.py

# A confirmed deadline failure is a scored run result (A6), and the kernel's own status is kept for A5 (1).
rg -n "except ReplayDeadlineFailure" ops/c1_rail/qualification/bracket.py ops/c1_rail/qualification/runner.py
rg -n "'kernel_outcome'|own_flat_deadline" ops/c1_rail/qualification/runner.py

# Step 1 verdict, the step-1b acceptance and the unchanged contract identity, on main.
rg -n "RESOLVED|a526b50fa75e6845|48bdc10460441a57" docs/briefs/handoffs/2026-09-24-tradeify-t00-p7-closure.md

# Ratification completeness: run after the Status line is changed. Success is the single line "OK".
# Any other output names an unfilled or missing §6 field, an unfilled §3 "Ratified value" cell (items 1-5, 7, 8), or a Status line that is not RATIFIED <date>.
f=docs/briefs/pre-registration/2026-10-01-tradeify-t00-step2-screen-prereg.md
{ for k in 'Ruling' 'OD-1 / OD-2' 'Ratifying commit SHA'; do grep -qE "^- [*][*]$k:[*][*] +[^ —]" "$f" || echo "§6 $k: unfilled"; done
  for n in 1 2 3 4 5 7 8; do grep -qE "^[|] $n [|].*[|] +[^ |—][^|]*[|][[:space:]]*\$" "$f" || echo "§3 item $n: Ratified value unfilled"; done
  grep -qE '^[*][*]Status:[*][*] `RATIFIED [0-9]{4}-[0-9]{2}-[0-9]{2}' "$f" || echo 'Status line is not RATIFIED <date>'; } | grep . || echo OK
```
