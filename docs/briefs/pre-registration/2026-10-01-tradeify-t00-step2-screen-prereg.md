# Pre-registration — T00 step 2: the selected-book feasibility screen (reuses prereg v2 scoring clauses; not falsifier evidence)

**Status:** `DRAFT — NOT RATIFIED.` A draft for the operator's ratification only. Nothing here binds T00 step 3 until this Status line reads `RATIFIED <date>`, every **OPERATOR TO SET** row in §3 holds a value, and the ratifying commit's SHA is recorded beside it. Once ratified, it does not change after any step-3 output is visible ([prereg v2 §5](2026-08-26-prop-survivor-scoring-prereg-v2.md#5--forbidden-moves--same-as-v1-plus-one-new-item-this-reopening-itself-creates), last v1 item; [amendment §T00](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#t00--feasibility-evidence-for-the-selected-book-new-investment-decision-not-a-gate-250k500k-may-return-early) step 2: "verbatim before execution, unchanged after").

**Authority:** operator ruling 2026-10-01, item 6, ["first-session simplification rulings"](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-10-01--first-session-simplification-rulings-six-cuts), as corrected at #580 `e627247` (Codex P1 on #580; branch `claude/first-session-cuts`, not yet on `main`): "The step-2 pre-registration reuses `2026-08-26-prop-survivor-scoring-prereg-v2.md` by citing **its reusable scoring clauses only**. It does **not** import that preregistration's falsifier disposition (G8). **A T00 screen is not four-firm §4 falsifier evidence** (operator ruling 2026-09-23, condition 4). The step-2 contract states that non-falsifier disposition itself. It adds only the expressions, pass floor, scenarios, intraday clock, NO-GO condition and the counting of R1/R2 `UNDETERMINED` days." The ruling also says it "may be drafted now … Ratification stays the operator's act."
**Owner of T00:** [amendment §T00](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#t00--feasibility-evidence-for-the-selected-book-new-investment-decision-not-a-gate-250k500k-may-return-early) and its [D-T00 row](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#d-t00--tick-step-1-now-the-one-decision-on-the-1108-clock). This file is the step-2 artifact those owners name; it does not restate them.
**Loop of record:** STRATEGIC (investment decision; T00 gates nothing).
**Authored:** 2026-10-01, Claude Code worker (drafting only) for the coordinating session "Coordinating parallel Claude sessions". Joshua owns every **OPERATOR TO SET** value, every open decision in §4 and the ratification.

**This draft authorizes nothing:** no screen, Monte Carlo, replay, T00 step-3 run, dispatch, provider contact, spend, deployment or arm. It contains no Pine source, port, account identifier, account figure or private value; private inputs are named by their already-public digests only.

---

## §0 — Owners read (anchors: `origin/main@2b98d22` unless a branch is named)

| Owner | What it fixes here |
|---|---|
| [prereg v2](2026-08-26-prop-survivor-scoring-prereg-v2.md) §2–§7 | Every number this file adopts: Part A bust ceiling **5.0%**, pass floor **P(pass) ≥ 50%** with a finite median inside horizon **1500**, Run-2 (consistency-on) gating, seeds **42/123/2026**, depth **10k**, inactivity disabled, overlay OFF |
| [`docs/load_bearing_numbers.md`](../../load_bearing_numbers.md) §1–§3 | EOD-clock bust figures are lower bounds; published figures assume inactivity OFF; 5.0% / 50% are live, owned by prereg v2 |
| [Amendment §T00 and D-T00 row](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#t00--feasibility-evidence-for-the-selected-book-new-investment-decision-not-a-gate-250k500k-may-return-early) | Step-2 contents; GO-evidence / NO-GO-evidence / INSUFFICIENT; "adopts it or states why the selected book falls outside it"; condition 4 ruled **NO** 2026-09-23, verbatim: "A T00 screen does not count as falsifier evidence" |
| [D-feed row](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#d-feed--tick-as-a-gate-not-a-provider) | Condition (a): provider-specific work opens only on a T00 verdict other than INSUFFICIENT or NO-GO-evidence |
| [T00 step-1 packet](../handoffs/2026-09-22-tradeify-t00-step1-producer-inventory.md) §7.4, §7.9 item 5 (line 312) | Candidate 3′ (`ops/c1_rail/qualification/`) is the producer; "Step 2 should say, before any run, how R1/R2 disagreement days (`UNDETERMINED`) count" |
| [P7-closure packet](../handoffs/2026-09-24-tradeify-t00-p7-closure.md), at `origin/claude/t00-p7-tasks-3-4@6ba5e17` | Step 1 **RESOLVED (P7 MET) at code `2baa516`**; source-only contract r3c `a526b50f…8d97` (FULL 997 / H1 499 / H2 498, PRISTINE `initial_state`); approval valid until 2026-10-08T08:21:08Z; fresh P7 at the post-S5 rebased head still owed |
| [Bracket convention](../phase3-preparation/2026-09-15/schedule-execution-evidence.md#addendum-2026-09-23--path-position-bracket-convention-ratified-2026-09-23) (ratified 2026-09-23) | R1/R2 are evaluated independently; a path's outcome is taken only where they agree, else `UNDETERMINED`, "reported as its own count and never folded into PASS or BUST"; "How UNDETERMINED paths enter the frozen pass-rate gates is an F1 definition" |
| `ops/c1_rail/qualification/runner.py:20–45` (`evaluate_replay`) | The kernel call: `Tradeify_Select_100K`, `inactivity_off=True`, `consistency=.40`, the replay's own `intraday_low`, `dd_scale=1.0`; outcome PASS / FAILURE / UNRESOLVED; `own_flat_deadline` is a FAILURE |
| `ops/c1_rail/qualification/bracket.py:145–183` (`BracketVerdict`, `run_bracket`) | UNDETERMINED is a **path** verdict, from two fresh engines |
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
| §2 G5 and §7 item 2: the headline bust is daily + static + trailing, read through the bucket-sum-checked definition | The bust numerator | `evaluate_replay` reports one more FAILURE reason (`own_flat_deadline`), **OPERATOR TO SET** item 3 |
| §7 item 1: ceiling numbers 5.0% / P(pass) ≥ 50% / finite median inside horizon 1500 | The same thresholds, as frozen | — |
| §7 item 5: Tradeify `consistency_frac` 40%, Run-2 gating | Consistency | Run-2 is what `evaluate_replay` runs (`consistency=.40`, `runner.py:27`). Whether a Run-1 diagnostic is owed is **OPERATOR TO SET** item 5, because the runner has no consistency-off mode |
| §7 item 6: overlay OFF for scoring | No second protection overlay | The kernel receives `dd_scale=1.0` (`runner.py:31`). The book's own 1% / 0.40 protection runs inside the replay (`test_runner.py::test_kernel_uses_intraday_and_no_second_scaling`) |
| §5 last v1 forbidden move: no number amended after a result is visible | The freeze discipline of this file | Applies to this file's own values once ratified |

### §1b — Disposition: this screen is **not** four-firm §4 falsifier evidence

Stated here as this contract's own disposition, not imported from prereg v2:

- **A T00 screen does not count as falsifier evidence** (operator, 2026-09-23, condition 4, verbatim; [D-T00 row](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#d-t00--tick-step-1-now-the-one-decision-on-the-1108-clock) "Condition 4 ruling"). Whatever step 3 returns, it neither discharges nor fires the four-firm §4 falsifier dated 2026-11-08. It does not change that falsifier's 0-of-4 clearer count, and it is not a "dated lab re-MC of a pre-registered candidate" for that clock. The falsifier needs its own dated re-MC regardless of T00.
- **Not imported from prereg v2:** the G8 admission and falsifier disposition; §4 H-SCORE; the §6 verdict table (RESOLVED / FALSIFIED / AMBIGUOUS); the §3 discharge rule (≥ 2 firms, ≥ 1 `trailing_locking`) and F2 labels; the §4 ceiling-mis-set reject and its §7 item 9 calibration reference; §7 item 8 (all-null close); G0–G2 intake, E1 reduction and cost-law gate; G6 routing; Part B and G7 funded diagnostics. These are the falsifier and survivor-admission machinery, or funded-phase scaling, and none of them is a scoring clause the screen needs.
- **What a T00 verdict is instead:** GO-evidence, NO-GO-evidence or INSUFFICIENT, an operator investment decision that gates nothing and admits nothing ([amendment §T00](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#t00--feasibility-evidence-for-the-selected-book-new-investment-decision-not-a-gate-250k500k-may-return-early)). No lifecycle CANDIDATE status, capital authorization or deployment follows from it. Its only named downstream reader is D-feed condition (a), whose NO-GO handling stays open (§4 OD-1).
- **Regime caveat.** prereg v2 §7 item 7 is not imported as a gate. The independent FULL / H1 / H2 populations (§2 A2) give the half-sample view, and no regime gate is added.

---

## §2 — The six additions (and nothing else)

### A1 — The expressions (by identity; no values restated)

Exactly the four legs of the Tradeify portfolio, at the identities **T00 step 1 resolved P7 for**, bound by source-only contract r3c `a526b50fa75e68451bdd2b5b57fa7a04e6ee08e61f96865c915ae8116a848d97` ([P7-closure Task 4 return](../handoffs/2026-09-24-tradeify-t00-p7-closure.md), branch `origin/claude/t00-p7-tasks-3-4`):

| Leg | Identifier | Binding |
|---|---|---|
| Aegis 6J | `aegis_6j` | runtime pin in `ops/c1_signal_daemon/book_adapters.py` |
| Striker MYM | `dj30_mym_p250` | the **corrected** port `efd479b6…`; the preserved original `c81aa59c…` is refused |
| Vanguard MGC | `vanguard_mgc` | runtime pin in `book_adapters.py` |
| ORB MNQ | `orb_mnq_v7` | runtime pin in `book_adapters.py` |

- **Captured sizes and allocations:** the [protection selection note](../../notes/2026-09-10-tradeify-protection-selection.md) "Selected book" table, as reproduced per expression by candidate 3′ ([step-1 §7.4](../handoffs/2026-09-22-tradeify-t00-step1-producer-inventory.md#74-p1p7-per-candidate-the-selected-four-aegis-6j-vanguard-mgc-striker-mym-orb-mnq) "What 3′ reproduces"). Effective inputs: `RUNTIME_EFFECTIVE_INPUTS_SHA256` (`book_adapters.py:72`).
- **Policy:** the candidate book protection policy (`ops/c1_rail/book_policy.py::candidate_book_protection_policy`): combined-peak 1% trigger, 0.40 scale, prior-close timing, ORB base unreduced, ORB adds off when protected, 80-micro capacity refusing rather than clipping, Aegis-priority whole-leg takeover.
- **Panels:** the four M15 panels pinned in `core/data/bar_data/SHA256SUMS` plus the Aegis attested-prefix panel `8ae083d0…` ([identity ledger](../phase3-preparation/2026-09-15/identity-ledger.md)), as bound by contract r3c.
- **Populations:** FULL 997 / H1 499 / H2 498 sessions, chronological ceil partition, as bound by contract r3c.
- **No re-optimization, re-sizing or substitution** ([amendment §T00](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#t00--feasibility-evidence-for-the-selected-book-new-investment-decision-not-a-gate-250k500k-may-return-early) "Forbidden"). Route-native editions are **not** these expressions; see open decision §4 OD-2.

Step 3 runs only at a head where P7 is re-accepted for these identities (the P7-closure "Still owed" item: a fresh P7 record at the post-S5 rebased head, accepted through `accept_p7_record`).

### A2 — Pass floor (and the ceiling it is paired with), per partition

Thresholds are prereg v2's, unchanged. Per-partition application:

| Quantity | FULL | H1 | H2 | Owner of the value · owner of the per-partition application |
|---|---|---|---|---|
| Bust ceiling (§A5 pessimistic count) | **≤ 5.0%** | **≤ 5.0%** | **≤ 5.0%** | prereg v2 §3 · [Track B prereg](2026-09-12-track-b-final-validation-prereg.md) §2 failure limbs F-full/F-H1/F-H2 and the 09-10 formal objective ("full/H1/H2 … failure bounds at most 5%") |
| Pass floor P(pass within 1500) (§A5 pessimistic count) | **≥ 50%** | **OPERATOR TO SET** item 2 | **OPERATOR TO SET** item 2 | prereg v2 §3 · FULL only by default, because the 09-10 closure found "an incorrect all-halves speed requirement" and no owner applies the floor to the halves |
| Median sessions-to-pass (non-passing paths at T = ∞) | finite, ≤ 1500 | reported | reported | prereg v2 §3, §7 item 1 |

Each population is evaluated **independently**, at its own depth (`runner.py:55–59`; `adjudication.py` requires FULL/H1/H2). Values are **point estimates** over the paths, as prereg v2 scores its headline; no confidence bound is added.

### A3 — Scenarios

**S0, the gating scenario.** A1's book and policy; `initial_state` **PRISTINE** (contract r3c, matching prereg v2's $100K common band); the source pack's reviewed `cost_model` (one cost model, no stress multiplier); inactivity OFF; consistency 40%; both bracket runs R1 and R2 on every path; the paths and seeds of §3 items 1 and 4.

**Candidate further scenarios.** Each has an owner. Whether it is run, and whether it gates, is **OPERATOR TO SET** item 7. This draft adds none of them by itself.

| Candidate | Owner | Note |
|---|---|---|
| S1: used-account initial state (the live incumbent eval) | Campaign §6 D23(a), §17 | The scored account is pristine while any deployment would use the used eval. The snapshot values are private. A stale snapshot is a new input, not a scenario parameter |
| S2: the 09-10 cash-flow probes (gains × 0.90; losses × 1.10) | [09-10 screen plan](../../superpowers/plans/2026-09-10-tradeify-feasibility-screen.md) Task 1 (CLOSED) | These scale daily P&L uniformly. T00's own P1 finding is that uniform scaling cannot reproduce the book's integer sizing, ORB base/add, capacity or takeover. On a bar-level replay they would be a post-hoc transformation of the producer's output, not a replay |

### A4 — The intraday clock (mandatory)

- The **only** admissible clock is intraday-honest. Each bracket run's own `SessionRecord.intraday_low` series (unscaled excursions from the day's opening equity, every entry `<= 0`, exact horizon) is passed with **that run's own** daily P&L to `simulate_path` through `runner.evaluate_replay` ([D-T00 wording](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#d-t00--tick-step-1-now-the-one-decision-on-the-1108-clock); `core/mc/simulation.py:325–345`).
- An **EOD-clock** result, or a path without a synchronized `intraday_low`, is **inadmissible** to the verdict. Under [`load_bearing_numbers.md` §1](../../load_bearing_numbers.md#1-standing-rule--eval-bust-figures-are-eod-clock-lower-bounds) any EOD-clock bust figure is a lower bound only, and the amendment forbids "EOD-clock 'zero bust' as survival". Its absence makes the verdict **INSUFFICIENT**, never GO.
- The convention's labelled **hybrid** (R2's P&L with R1's lows) may be reported but never enters the verdict ([bracket convention](../phase3-preparation/2026-09-15/schedule-execution-evidence.md#addendum-2026-09-23--path-position-bracket-convention-ratified-2026-09-23) "Verdict").
- The inactivity barrier is **OFF** with the operator-placed weekly token trade as the mitigation ([`load_bearing_numbers.md` §2](../../load_bearing_numbers.md#2-standing-rule--every-published-figure-assumes-the-inactivity-barrier-is-off)); `evaluate_replay` raises `inactivity_limit` past the horizon (`runner.py:28–30`).

### A5 — How R1/R2 `UNDETERMINED` counts

**Unit.** The ratified convention defines `UNDETERMINED` per **path**: a path whose R1 and R2 evaluations disagree on PASS / FAILURE / UNRESOLVED (`bracket.py:145–183`). Per-session R1/R2 differences in P&L or `intraday_low` are expected by construction wherever an intrabar split is consumed, so they carry no verdict role. The step-1 packet's "disagreement days" wording is read as this path-level verdict. Step 3 reports, per population, the count of paths with a consumed split and the count of `UNDETERMINED` paths, descriptively.

**Counting rule (drafted; the operator ratifies or replaces it).** The `UNDETERMINED` count stays separate, as the convention requires. Each threshold in A2 is evaluated under two assignments of the `UNDETERMINED` paths:

| Assignment | Bust numerator | Pass numerator | Use |
|---|---|---|---|
| Pessimistic | agreed bust + **all** `UNDETERMINED` | agreed PASS only | **Decides GO-evidence** |
| Optimistic | agreed bust only | agreed PASS + **all** `UNDETERMINED` | **Labels** a NO-GO as robust or as `UNDETERMINED`-dependent |

The denominator is always every path in the population. `UNDETERMINED` paths are never dropped, and agreement is never conditioned on.

**Consequence.** A high disagreement share cannot turn the screen back into INSUFFICIENT, which is the [T00→T10→CP-7 note §3](../../notes/2026-09-29-t00-t10-cp7-sequence.md) step-4 concern. It can only prevent GO-evidence.

*Alternatives the operator may prefer, stated so the choice is explicit:* (i) exclude `UNDETERMINED` from the denominator, which is optimistic and conditions on agreement; (ii) a cap on the `UNDETERMINED` share above which the result is INSUFFICIENT. There is no owner for such a cap, so it would be **OPERATOR TO SET**; it also reintroduces the INSUFFICIENT route the CP-7 note warns about.

### A6 — The NO-GO condition (verbatim; not to be edited after any step-3 output exists)

> **INSUFFICIENT** if any of: the producer cannot complete a path for either bracket run; any path lacks its run's own synchronized `intraday_low`; P7 is not accepted for A1's identities at the executing head; the runner raises `NeedsContext` (budget, missing prerequisite) before every population reaches its frozen depth; or any §3 item is unset. No reduced depth, substitute clock or extra draw is run in its place.
>
> Otherwise, in scenario **S0** (and any scenario §3 item 7 makes gating), with `UNDETERMINED` paths counted under the **pessimistic** assignment of A5:
>
> **GO-evidence** if, for FULL, H1 and H2 each, the headline bust proportion is **≤ 5.0%**, **and** FULL's P(pass within 1500 sessions) is **≥ 50%** with a finite median sessions-to-pass inside 1500 (and H1/H2 likewise if §3 item 2 so sets).
>
> **NO-GO-evidence** otherwise. It is labelled **robust** if it also fails under the optimistic assignment, else **`UNDETERMINED`-dependent**. Both labels are NO-GO-evidence.
>
> A NO-GO-evidence verdict is presented to the operator as an investment decision (adjust the book, or accept the risk into T15's F1), never routed automatically to a portfolio-adjustment packet ([amendment §T00](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#t00--feasibility-evidence-for-the-selected-book-new-investment-decision-not-a-gate-250k500k-may-return-early) step 3). Its effect on D-feed (a) is open decision §4 OD-1.
>
> No verdict under this condition, GO-evidence included, is four-firm §4 falsifier evidence (§1b).

---

## §3 — OPERATOR TO SET (no owner supplies these values; all are set before ratification)

| # | Item | Candidates with owners, if any | Why it is not decided here |
|---|---|---|---|
| 1 | **Path depth per population**, and **compute budget** (`budget_seconds`, required by `runner.SyntheticStageRequest` / the production executor) | prereg v2 G4: 10,000 per seed × 3 seeds | v2 has no FULL/H1/H2 axis. Whether 10k × 3 applies to each population is not stated. Bar-level replay cost is unmeasured at this depth × 2 runs × horizon 1500. The runner refuses a batch whose probe exceeds the budget (`runner.py:110–111`) |
| 2 | **Pass floor on H1 and H2**: binding, or reported only | prereg v2 §3 50% (value) | The 09-10 closure found an all-halves speed requirement incorrect. No owner applies the floor to halves |
| 3 | **`own_flat_deadline` FAILURE in the bust numerator** | `evaluate_replay` classifies it FAILURE (`runner.py:36–37`). The deadline is Tradeify's blanket account-level 16:45 ET rule, or 12:59 ET on D19 dates (P7-closure, operator ruling 2 of 2026-09-30) | prereg v2's headline bust is daily + static + trailing only. *Drafter's note:* counting it is the conservative reading, because it is an account rule breach |
| 4 | **Path construction**: block family and length, RNG root namespaces derived from seeds 42/123/2026, path start | `JointFlatBlocks` exists (`blocks.py`); Track B prereg §2 leaves block family/length `OWED-BY: TB-F1`; contract r3c's `path_start_date` 2022-09-01 is PROPOSED, a label origin | No owner has frozen the block family or length |
| 5 | **Run-1 (consistency-off) diagnostic**: owed or waived | prereg v2 §2 G4 runs twice, gating on Run-2 | `evaluate_replay` fixes `consistency=.40`. Run-1 would need a runner change; it never gates |
| 6 | *Withdrawn 2026-10-01:* prereg v2 §7 item 9 calibration reference | — | Not imported. It serves §4's ceiling-mis-set reject, which is part of the falsifier disposition the #580 `e627247` correction excludes (§1b). The row is kept so the numbering stays stable |
| 7 | **Scenarios beyond S0** (S1 used-account, S2 cash-flow probes, or none) and whether any gates | §2 A3 table | Choosing scenarios is the operator's step-2 act. S1 needs a fresh private snapshot; S2 conflicts with T00's P1 finding |
| 8 | **The `UNDETERMINED` counting rule**: ratify A5 as drafted, or replace it | Bracket convention (path-level verdict); CP-7 note §3 step 4 | The convention leaves gate entry to "an F1 definition"; no owner has written it |

---

## §4 — Open operator decisions (stated, not decided)

**OD-1. How D-feed condition (a) treats a NO-GO T00 result whose risk the operator accepts into F1.** D-feed (a) reads: provider-specific work opens when "T00 returns a verdict other than INSUFFICIENT or NO-GO-evidence" ([D-feed row](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#d-feed--tick-as-a-gate-not-a-provider)). Amendment §T00 step 3 separately lets the operator "accept the risk into T15's F1". The first-session rulings' item 6 records this as **still open**. Readings, none adopted here:
- **(a) Literal.** NO-GO-evidence leaves (a) unmet whatever the operator accepts. Provider-specific work opens only through a dated amendment of the D-feed wording.
- **(b) Acceptance satisfies (a).** An operator acceptance recorded in the F1 packet converts the NO-GO into an accepted risk, and (a) is treated as met from that record's date. (b) still holds independently.
- **(c) Label-sensitive.** Acceptance satisfies (a) only for an `UNDETERMINED`-dependent NO-GO (§2 A6); a robust NO-GO needs (a)'s amendment.

Whatever is chosen should be recorded at the D-feed owner, not here, before step 3 returns. The step-3 verdict must not be the input that chooses it.

**OD-2. Declared expressions versus route-native editions.** A1 pins the identities P7 was resolved for. Campaign §59 rulings 3–5 adopt route-native editions of ORB, Striker and (option A) Vanguard for this route ([ORB/Striker prereg](2026-09-25-tradeify-route-native-editions-prereg.md), [Vanguard prereg](2026-09-26-tradeify-vanguard-fixed-stop-edition-prereg.md)). Both are DRAFT, not frozen, and no P7 exists for them. If the operator wants T00 to screen the editions, A1 changes, and P7 for those identities becomes a step-3 prerequisite. If T00 screens the declared book, a GO-evidence result speaks to the declared expressions only.

---

## §5 — Dependencies before step 3 (recorded; none is granted by this file)

1. Ratification of this file, with §3 complete.
2. A fresh P7 record at the post-S5 rebased head, accepted through `accept_p7_record`. The source approval expires 2026-10-08T08:21:08Z, so a later run needs a fresh one (P7-closure "Still owed").
3. A step-3 executor packet, plus whatever contract class the screen path requires. P7's source-only contract refuses the screen modules at load (`part_a`, `bracket`, `result_adjudication` …; P7-closure revision 4.3). Blocker 1 of that packet records that the full production contract needs F1 freeze fields.
4. Results stay under the private root with `results.json` / `REPORT.md` bound to ledger digests ([amendment §T00](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#t00--feasibility-evidence-for-the-selected-book-new-investment-decision-not-a-gate-250k500k-may-return-early) step 3). A public bust or pass figure cites that intraday-honest RESULTS path (`load_bearing_numbers.md` §1).

---

## §6 — Ratification (operator; blank until ruled)

- **Ruling:** —
- **§3 values:** —
- **OD-1 / OD-2:** —
- **Ratifying commit SHA:** —

---

## Audit hooks

```bash
# The reused numbers are prereg v2's, and the loader still resolves v2 (expect 0.05 / 0.01 / 0.50).
python -I scripts/fp.py python -c "import sys; sys.path[:0]=['lab','core']; from discovery.prop_survivor_scoring import load_scoring_thresholds as l; t=l(); print(t.eval_bust_ceiling, t.funded_bust_ceiling, t.pass_floor)"

# The kernel call this file binds to: Tradeify Select, inactivity OFF, consistency 40%, own intraday_low.
rg -n "firm_kwargs\('Tradeify_Select_100K', inactivity_off=True, consistency=.40" ops/c1_rail/qualification/runner.py

# UNDETERMINED is a path verdict from two runs.
rg -n "UNDETERMINED" ops/c1_rail/qualification/bracket.py

# Step 1 verdict and contract identity (branch until the post-S5 merge).
git show origin/claude/t00-p7-tasks-3-4:docs/briefs/handoffs/2026-09-24-tradeify-t00-p7-closure.md | rg -n "RESOLVED|a526b50fa75e6845"

# Every OPERATOR TO SET row is filled before the Status line changes (expect no "| —" rows in §6 at ratification).
rg -n "OPERATOR TO SET" docs/briefs/pre-registration/2026-10-01-tradeify-t00-step2-screen-prereg.md
```
