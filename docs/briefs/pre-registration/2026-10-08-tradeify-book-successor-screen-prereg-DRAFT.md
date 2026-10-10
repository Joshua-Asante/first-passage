# Pre-registration — one screen of one successor configuration of the Tradeify book (#581's structure; not falsifier evidence)

**Status:** `DRAFT — NOT RATIFIED.` A draft for the operator's ratification only. Nothing here binds a replay, screen, Monte Carlo or verdict until this line reads `RATIFIED <date>`, every §6 field and the §6 values block hold their values, and the ratifying commit's SHA is recorded in §6 (C, then C′, as #581). Under Q5 the status word is RATIFIED, not FROZEN; "freeze" in the cited owners means this ratification.

*2026-10-10, P-S5 rewrite ([build card #758](../handoffs/2026-10-10-t00-successor-screen-build-card-DRAFT.md) §2.7, approved by Joshua 2026-10-10). Rewritten to #581's structure so that `screen_authority._check_prereg` and `_check_sections` accept it once ratified (Q5). §2 A5 and A6 are byte copies of [#581](2026-10-01-tradeify-t00-step2-screen-prereg.md)'s; their SHA-256 (each from its `###` heading line up to, not including, the next heading line) must stay A5 `a8f6f25e025a2e136e477580b7e569531d770a1e35e712b72f5a6b9b50eb391b` and A6 `b3bdc77baf3e6383f1df08afd2f0fbb8a7c930d95a0f56b0c5669a5e18b217d9` (`verdict.A5_TEXT_SHA256`, `A6_TEXT_SHA256`). Ratification must leave those bytes unchanged.*

**Authority:** Joshua (operator), 2026-10-08, via the First Passage Deployment Coordinator: "go with your suggestions 1-3" (item 3, drafting). Rulings Q2, Q3, Q5 (2026-10-10, "agreed on Q2, Q3, Q5"), card approval ("approve #758, S-1 to S-7, P-S4 option A") and the successor configuration ("C-1 row 5 uniform, option A, K₀ = 8") are recorded on [card #758](../handoffs/2026-10-10-t00-successor-screen-build-card-DRAFT.md) §8 and the [T00 card](../handoffs/2026-10-03-t00-screen-authority-build-card-DRAFT.md) §8.
**Owner:** the T00 line ([amendment §T00](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#t00--feasibility-evidence-for-the-selected-book-new-investment-decision-not-a-gate-250k500k-may-return-early) step 3: after NO-GO-evidence, "adjust the book" is an operator investment decision). Step 3 of the [T00 card §8 successor decision tree](../handoffs/2026-10-03-t00-screen-authority-build-card-DRAFT.md#8--approval-prerequisites-and-h-record).
**Loop of record:** STRATEGIC (investment decision on an adjusted book; K accounting in §1c).
**Authored:** 2026-10-08, Claude Code (drafting only); rewritten 2026-10-10 by the P-S5 worker for the Deployment Coordinator. The operator owns every **OWED** field and the ratification.

**This draft authorizes nothing:** no replay, screen, Monte Carlo, source build, signing, dispatch or spend. It contains no Pine, port, account identifier, private value, size-vector value, rate, dollar figure or count.

## §R — Standing rule: no candidate-configurable replay before ratification

[Deployment checklist](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md) item 7.6.1 (operator ruling 2026-10-02): no agent runs a candidate-configurable replay before its pre-registration is frozen (here: ratified). The configuration of §1a is candidate-configurable ([Tier-2 card](../handoffs/2026-10-08-t00-step12-diagnostic-tier2-scoping-card-DRAFT.md) §1). P7 replays a real path over r3d's contract (`p7_driver.py:1-6`), so ratification precedes P7 over r3d ([card #758](../handoffs/2026-10-10-t00-successor-screen-build-card-DRAFT.md) §7 step 4).

---

## §0 — Owners read (anchors: `origin/main@843e743`, 2026-10-10)

| Owner | What it fixes here |
|---|---|
| [#581](2026-10-01-tradeify-t00-step2-screen-prereg.md) (`RATIFIED 2026-10-07`) §1b, §2 A1–A6, §3, §6 | The structure copied here; A5/A6 copied byte for byte; the values block form and its ratified values (the carried candidates in §3) |
| [Card #758](../handoffs/2026-10-10-t00-successor-screen-build-card-DRAFT.md) §0.5 S-1…S-7, §1.1, §1.2, §2.7, §7, §8 | The successor build: size vector in a signed startup-policy v2, r3d by derivation from r3c, per-purpose chain entry, roots disjoint from step 12, the gate mapping under Q5, the ratification step |
| [T00 card](../handoffs/2026-10-03-t00-screen-authority-build-card-DRAFT.md) §8 | Step-12 result (`NO-GO-evidence-robust`), the successor stopping rule and decision tree, Tier-2 result and reader additions, R1/R2 hold, the 2026-10-10 configuration ruling |
| `ops/c1_rail/qualification/screen_authority.py:56`, `:95-100`, `:362-453` | `PREREG_CHAIN`; `VALUES_SCHEMA = 't00-step2-values/v1'`; `SECTION3_KEYS`; the Status regex `_RATIFIED`; `_ratified` (title, blank line, Status as line 3, one Status field); `_values_and_cells` (§6 `- **Ruling:**`, `- **OD-1 / OD-2:**`, one values fence, §3 cells); `_check_prereg` (C→C′ changes only the `- **Ratifying commit SHA:**` line); `_check_sections` |
| `ops/c1_rail/qualification/t00_screen/verdict.py:26-27`, `:44-57`, `:168-178` | A5/A6 hashes and spans (A6 ends at the `## §3` heading); the optimistic assignment's treatment of an `UNDETERMINED` path |
| `ops/c1_rail/qualification/replay.py:612-614` | A leg at quantity 0 has every entry rejected "zero policy quantity" |
| [Tier-1 card](../handoffs/2026-10-08-t00-step12-diagnostic-tier1-card.md) §8 and addendum; [Tier-2 card](../handoffs/2026-10-08-t00-step12-diagnostic-tier2-scoping-card-DRAFT.md) §2.1, §7 | Reader log entries; pattern row 5; "Any successor pre-registration names them" |
| [Readiness map](../../notes/2026-10-10-successor-screen-readiness-map.md) (#757) §5, §6 | Q1–Q8; K₀ prefill; reader row RM-1 |
| [Size-feasibility RESULTS](../../../lab/analysis/c1/size_feasibility_2026-10/RESULTS.md) (#745) | FEASIBLE, largest clearing uniform k 0.5; grid K = 7; its readers |
| [Screen-authority design](../../superpowers/specs/2026-10-02-t00-screen-authority-design.md) §4.5 | A re-attempt's pre-registration names every reader of the earlier run directory |
| `AGENTS.md` "Strategy Authorization Lifecycle", "Protection" | De-risking, never re-optimization; the protection cell's change-control path |

Not read by the P-S5 worker: Pine, ports, effective inputs, the Tier-1 or Tier-2 report, series, key lists, the Q1 options sheet, any private result.

---

## §1 — Purpose, configuration and what is inherited

One pre-registered screen of **one** successor configuration of the Tradeify book, chosen before any successor output exists. It is a de-risking of the declared book (a uniform size cut), never a re-optimization. The book protection policy (1% combined-peak trigger, 0.40 scale, prior-close timing, 80-micro capacity, Aegis-priority takeover, ORB base unreduced, ORB adds off when protected) is inherited unchanged.

### §1a — The configuration (C-1…C-7)

| # | Field | Value |
|---|---|---|
| C-1 | Tier-2 pattern row relied on | Row 5 alone, read as a **uniform** cut (Joshua, 2026-10-10). Row 3 is not relied on. Tier-2 `REPORT.md` SHA-256 `efcf85dbbe5532f5130674ed7bf0c9bcc77fc6e9a0a65ffc27c6fc85ec2bdb7c` |
| C-2 | Base expressions | The declared book (r3c identities); r3d is r3c with only `contract_id` and the `source_startup_policy` row changed (card #758 S-3). Same as §4 OD-2 |
| C-3 | Leg set | All four legs stay in the contract and their signals are generated. A leg whose frozen size is 0 is OFF: every entry is rejected "zero policy quantity" (card #758 §1.2) |
| C-4 | Size vector | The frozen size vector in the signed startup-policy v2 (Q1 option A, FLOOR-HALF: every leg at k = 0.5 under the code's own round-down rule). Values private; bound by `size_vector_sha256` (§2 A1) |
| C-5 | Adds rule | The `adds` field of each leg in the frozen size vector in the signed startup-policy v2; no field may turn on an add today's rule refuses |
| C-6 | Per-session risk-reduction rule | None: row 5 is read as uniform (C-1) |
| C-7 | Answerer exposure for C-1…C-6 (the §10 marker form) | Answerer exposure: not seen — Joshua (he saw neither the Tier-1 nor the Tier-2 report, only hash-and-label returns and the public-safe Q1 summary relayed by the Deployment Coordinator; relayed 2026-10-10) |

**FLOOR-HALF is not the fractional k that cleared.** The size-feasibility FEASIBLE label (k 0.5) is a target range for a uniform fractional cut; it does not transfer to the integer vector this screen tests.

### §1b — Disposition: this screen is **not** four-firm §4 falsifier evidence

As #581 §1b, stated here as this file's own disposition: **a T00 screen does not count as falsifier evidence** (operator, 2026-09-23, condition 4). No verdict here, GO-evidence included, discharges or fires the four-firm §4 falsifier dated 2026-11-08 or counts toward its clearer count. A verdict is GO-evidence, NO-GO-evidence or INSUFFICIENT, an input to an operator investment decision; it admits nothing, authorizes no capital and deploys nothing. Where it touches D-feed condition (a) is §4 OD-1.

### §1c — K accounting

- **K₀ = 8** (Joshua, 2026-10-10): the step-12 screen of the declared book (1) plus the size-feasibility grid (7), counted once. This successor is **K = 9**.
- The coordinator registers this book's lineage in `discovery_manifests/` before ratification (card #758 §7 step 3).
- Each further configuration screened, under this file or a sibling, is another trial and needs its own ratified pre-registration.

### §1d — #733's earlier gates under Q5

The binding verdict is §2 A6, byte for byte. The earlier draft's gates map as follows (card #758 §1.1):

| Gate | Under Q5 |
|---|---|
| G1 bust, pessimistic, FULL/H1/H2 | A6, binding |
| G3 pass floor, pessimistic, FULL | A6, binding |
| G2 bust, R1 alone, H2 | Implied by G1 for GO versus NO-GO: an R1 bust is an agreed FAILURE with a bust run or an `UNDETERMINED` path, and the pessimistic assignment counts both. Not separately bound |
| G4 pass floor, R1 alone, H2 | Implied by the H2 pass floor when `pass_floor_halves` is `BINDING`; not enforced when it is `REPORTED` (§3 item 2) |
| G5 funded survival | Reported, non-binding; no producer exists, so it is reported as "not produced". Confirmation **OWED (operator; Q6)** |
| G6 economics | Outside A6; reported only. No producer exists in the screen, so it is reported as "not produced" |

**Label subtype.** The implications hold for GO versus NO-GO only. The earlier draft made a failed R1-alone gate a robust NO-GO; under A6 the same paths may be labelled `UNDETERMINED`-dependent, because the optimistic assignment does not count an undetermined R1 bust and does count an undetermined R1 pass (`verdict.py:173-175`). A6's labels govern.

---

## §2 — The additions

### A1 — The expressions (by identity; no values restated)

The four legs of the declared book at the identities r3c binds (`a526b50fa75e68451bdd2b5b57fa7a04e6ee08e61f96865c915ae8116a848d97`; #581 A1), driven by **r3d**: r3c with only `contract_id` and the `source_startup_policy` artifact row changed, checked by derivation (card #758 S-3). r3d's startup policy is `qualification-source-startup/v2`: v1's fields plus `sizing`, the frozen size vector in the signed startup-policy v2 (§1a C-4, C-5). Every other startup field equals r3c's v1 policy.

- **Bound three ways:** this file's §6 values block carries `expressions = {"base": "DECLARED_BOOK", "size_vector_sha256": <hex>}` with `size_vector_sha256 = sha256(canonical_json_bytes(sizing))`; the screen authority carries the same; the signed r3d carries the bytes.
- **Refused under the successor purpose:** a v1 startup policy, or a v2 vector that gives today's quantities (card #758 S-5).
- **Policy, panels, populations:** as #581 A1 (candidate book protection policy, bound by the accepted P7 record's `code_closure_sha256`; r3c's four admitted-panel roles; FULL 997 / H1 499 / H2 498).
- **Locked inputs untouched:** no Pine, port, effective input, `dd_protection` constant or `BASE_RISK` changes (Q2).
- **P7:** step 3 runs only at a head where a P7 record over r3d is accepted through `accept_p7_record`.

### A2 — Pass floor (and the ceiling it is paired with), per partition

As #581 A2, unchanged:

| Quantity | FULL | H1 | H2 | Owner |
|---|---|---|---|---|
| Bust ceiling (§A5 pessimistic count) | **≤ 5.0%** | **≤ 5.0%** | **≤ 5.0%** | prereg v2 §3 · #581 A2 |
| Pass floor P(pass within 1500) (§A5 pessimistic count) | **≥ 50%** | §3 item 2 | §3 item 2 | prereg v2 §3 · #581 A2 |
| Median sessions-to-pass (non-passing paths at T = ∞; each path's day per A5) | finite, ≤ 1500 | reported | reported | prereg v2 §3, §7 item 1 |

Each population is evaluated independently at its own depth; values are point estimates.

### A3 — Scenarios

**S0, the gating scenario:** A1's book and policy, `initial_state` PRISTINE, the reviewed `cost_model`, inactivity OFF, consistency 40%, R1 and R2 on every path, the paths and seeds of §3 items 1 and 4. No further scenario (§3 item 7).

### A4 — The intraday clock (mandatory)

As #581 A4: only each bracket run's own synchronized `intraday_low` with that run's own daily P&L, through `runner.evaluate_replay`, is admissible. An EOD-clock result is inadmissible and makes the verdict INSUFFICIENT, never GO. The labelled hybrid may be reported and never enters the verdict. Inactivity barrier OFF.

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

## §3 — OPERATOR TO SET (recorded in the §6 values block at ratification)

| # | Item | Candidate (owner) | Why it is open | Ratified value |
|---|---|---|---|---|
| 1 | **Path depth per population** and **compute budget** | N = 1,002 per population, 334 per root (#581 as ratified; card #758 §7 "Budget": 961,920 path CPU-s, 11,300 overhead CPU-s by #581's formula) | **OWED (operator; Q7)**: depth stays N = 1,002 unless re-ruled | values block: `depth_per_root`, `budget` |
| 2 | **Pass floor on H1 and H2**: binding or reported | #581's ratified `REPORTED`; `BINDING` makes §1d G4 enforced | **OWED (operator)** | values block: `pass_floor_halves` |
| 3 | **A deadline-only run in the bust numerator** | #581's ratified `true` (A5 (1)) | Carried from #581 | values block: `deadline_only_is_bust` |
| 4 | **Path construction**: RNG tag and roots, block, path start | The compiled tag `t00-screen-rng/v1` with `roots` and `probe_root` disjoint from step 12's (`42`, `123`, `2026`, `probe`), so successor keys are disjoint from step 12, Tier 1 and Tier 2 (card #758 S-5); block and path start as #581 | Roots are set in the values block at ratification | values block: `rng`, `block`, `path_start_date` |
| 5 | **Run-1 (consistency-off) diagnostic** | #581's ratified `WAIVED` | Carried from #581 | values block: `run1_diagnostic` |
| 6 | *Withdrawn (as #581):* prereg v2 §7 item 9 calibration reference | — | Not imported; numbering kept | withdrawn |
| 7 | **Scenarios beyond S0** | `["S0"]` only (A3) | Carried from #581 | values block: `scenarios` |
| 8 | **The A5 counting rule** | `T00_A5/v1`, A5 as copied | Carried from #581 | values block: `a5_rule` |

---

## §4 — Hypothesis, falsifier and open operator decisions

**H.** If the configuration of §1a is screened under §2 A6 on keys drawn under §3 item 4, then it is GO-evidence; otherwise it is NO-GO-evidence (robust or `UNDETERMINED`-dependent, per A6) or INSUFFICIENT, and the configuration is not adopted.

**Falsifier.** For FULL, H1 or H2, the A5 pessimistic bust proportion exceeds 5.0%, or FULL's pessimistic P(pass within 1500) is below 50% or its median is not finite inside 1500 (and H1/H2 likewise if §3 item 2 is `BINDING`).

**OD-1. D-feed condition (a) for a successor verdict.** The standing D-feed reading (c) (#581 OD-1, ruled 2026-10-02) is worded on #581 A6's labels, which this file's A6 copies. Whether that reading applies to a successor verdict as written is recorded at the D-feed owner before the screen returns, never chosen by its result — **OWED (operator)**.

**OD-2. Base expressions.** The declared book (§1a C-2; card #758 S-3). Route-native editions are not these expressions.

---

## §5 — Dependencies and forbidden moves

### §5a — Dependencies before the screen (recorded; none is granted here)

1. Accepted H′ with P-S1…P-S3 merged (card #758 §4).
2. r3d assembled and its derivation check run; `size_vector_sha256` computed (card #758 §7 step 2).
3. The K₀ ledger entry merged (§1c).
4. Ratification of this file, C then C′ (§9).
5. A fresh source approval over r3d (`APPROVE_T00_SOURCE_CONTRACT`), then one P7 run at H′ over r3d, accepted through `t00_screen accept-p7`.
6. A screen authority under the successor purpose (`T00_SUCCESSOR_SCREEN`, grant `T00_SUCCESSOR_SCREEN_ONCE`), bound to r3d, the P7 record and this file as chain entry 1 (card #758 S-4); `validate_screen_authority` ISSUED. `PARAMETER_CHANGE` there means any change beyond the frozen size vector (Q3).

### §5b — Forbidden moves

- Any replay, screen, Monte Carlo or source build on this configuration before ratification (§R).
- Screening more than one configuration under this file; choosing or changing the vector after any successor output exists.
- Sweeping sizes, legs or thresholds and keeping the best (re-optimization).
- Changing `DD_TRIGGER` / `DD_SCALE`, the protection cell, capacity or takeover order; editing locked Pine, ports or effective inputs.
- Editing A5/A6, or any §1, §3 or §6 value, after ratification or after successor output exists. Close this file and open a fresh one instead.
- Reusing step 12's grant, roots or run directory.
- Reading or citing a verdict here as four-firm §4 falsifier evidence (§1b).
- Publishing a private value (vector values, rate, dollar figure, count, key, P&L) in a public surface.

---

## §6 — Ratification (operator; blank until ruled)

The §3 values are recorded once, in the `t00-step2-values/v1` block below: one line equal to `canonical_json_bytes(parameters)` (screen-authority design §3, row A8). Each active §3 *Ratified value* cell names only its keys. The successor's `parameters` differ from #581's only in `expressions` (§2 A1), `rng.roots` and `rng.probe_root` (§3 item 4), and any re-ruled `depth_per_root`, `budget` or `pass_floor_halves`. The verdict is GO-evidence, NO-GO-evidence or INSUFFICIENT, per A6; on H (§4) they read RESOLVED, FALSIFIED and AMBIGUOUS.

```t00-step2-values/v1
OWED (operator): replaced at ratification by the single line canonical_json_bytes(parameters)
```

- **Ruling:** **OWED (operator)**
- **OD-1 / OD-2:** **OWED (operator)** for OD-1; OD-2 is the declared book (§4)
- **Ratifying commit SHA:** recorded in C′

---

## §7 — Exposure statement

Readers of per-session or per-leg step-12 detail, of the step-12 run directory (design §4.5), of per-k size-feasibility results, of Tier-2 output or of the Q1 options, before ratification:

| # | Reader | Date / time | Saw | Source |
|---|---|---|---|---|
| S12-1 | Step-12 executor session (step-12 owner) | 2026-10-08 | The finalized step-12 run directory, after `finalize` (row X2) | T00 card §8, step-12 result |
| S12-2 | Coordinator (4), T00 card owner | 2026-10-08 | Hashes and labels from the step-12 return | T00 card §8, step-12 result |
| T1-1 | Executor session (smoke run) | 2026-10-08 | Selected keys, per-stratum counts; no series, no report | Tier-1 card §8 |
| T1-2 | Executor session (read-only attestation check) | 2026-10-08 ~04:57Z | Binding held; in-memory key-list hash | Tier-1 card §8 |
| T1-3 | Executor session | 2026-10-08 ~07:10Z | Per-path sealed series and the report | Tier-1 §8 addendum, reader 3 |
| T1-4 | Joshua | 2026-10-08 ~07:12Z | Findings summary in chat; no series, no keys, no report | Tier-1 §8 addendum, reader 4 |
| T1-5 | Deployment Coordinator | 2026-10-08 ~07:40Z; ~08:10Z | The summary; then the report (no series) | Tier-1 §8 addendum, reader 5 |
| SF-1 | Executor session (size feasibility) | 2026-10-08/09 | Progress lines, then full results | RESULTS "Readers" 1 |
| SF-2 | Deployment Coordinator | 2026-10-09 ~02:55Z | Per-k results from the executor's return | RESULTS "Readers" 2 |
| SF-3 | Joshua | 2026-10-09 ~03:00Z | Per-k results in chat | RESULTS "Readers" 3 |
| RM-1 | Readiness-map session | 2026-10-10 | Public code and docs only; no report, series, keys or private result | Readiness map §6 |
| T2-1 | Tier-2 executor session | 2026-10-10 01:47Z–03:44Z | All sampled series and the Tier-2 report | T00 card §8, Tier-2 result |
| T2-2 | Q1 options worker | 2026-10-10 | The Tier-2 report | T00 card §8, Tier-2 result |
| T2-3 | Deployment Coordinator | 2026-10-10 | The Tier-2 hash-and-label return only | T00 card §8, Tier-2 result |
| T2-4 | Joshua | 2026-10-10 | Neither report; hash-and-label returns and the public-safe Q1 summary | §1a C-7 |
| PS5-1 | P-S5 worker (this rewrite) | 2026-10-10 | Public code and docs only; no report, series, keys, Q1 sheet or private result | this file |

Also exposed to everyone: the public step-12 verdict `NO-GO-evidence-robust` (#724), the Tier-2 card's admission-time row 5, and the public Tier-2 result (rows 4 and 5 hold).

**Data exposure.** Every admitted panel is fully exposed through step 12, Tier 1 and Tier 2. Keys from roots disjoint from step 12's give fresh paths over the same history, not new history; the Tier-1 keys (`60c128a7…329e`) and the 60 Tier-2 paths (`e51bcca1…68c5`) come from step 12's run, so they are excluded by construction. The report says so.

Ratification attests that this table is complete.

---

## §8 — Governance notes

- **Stopping rule.** The successor stopping rule and decision tree on [T00 card §8](../handoffs/2026-10-03-t00-screen-authority-build-card-DRAFT.md#8--approval-prerequisites-and-h-record) govern; this file is tree step 3. **R1/R2 is on hold** (Joshua, 2026-10-10), so no accepted R1/R2 resolution exists and definition **(a)** applies as written: this screen's H2 result under the pessimistic A5 assignment fails the A6 bust ceiling. That comparison is one of A6's own, read from `results.json`; no new code is needed. (a) firing stops successor work on this book. The card's text governs where this summary differs.
- **Chain.** This path is entry 1 of `PREREG_CHAIN`, bound by the successor purpose only; #581 stays entry 0 under the original purpose (card #758 S-4).

## §9 — Ratification procedure

1. P-S5 merged; card #758 §7 steps 2 and 3 done.
2. The operator sets every **OWED** field: G5 confirmation (§1d, Q6), depth (§3 item 1, Q7), `pass_floor_halves` (§3 item 2), OD-1 (§4), the §6 values block, Ruling and OD-1 / OD-2 fields. No private value in public text.
3. Claude runs §10 except the ratification-completeness hook; the operator reviews the full text.
4. **C:** one commit changes the Status line to `RATIFIED <date>` and fills §6 (and nothing in A5/A6). It is the oldest RATIFIED commit of this path reachable from `origin/main`.
5. **C′:** one commit changes only the `- **Ratifying commit SHA:**` line, to C's 40-hex SHA in backticks.
6. §10 runs in full at C′. Any failure voids the ratification.

## §10 — Audit hooks

```bash
f=docs/briefs/pre-registration/2026-10-08-tradeify-book-successor-screen-prereg-DRAFT.md
# Form (expect RESULT: well-formed).
python -I scripts/fp.py python scripts/check_brief.py --type brief "$f"

# A5/A6 equal #581's (expect a8f6f25e...391b then b3bdc77b...17d9), through the authority's own span code.
python -I scripts/fp.py python -c "import hashlib,sys;sys.path.insert(0,'ops');from c1_rail.qualification.t00_screen import verdict as v;b=open(sys.argv[1],'rb').read();print(*(hashlib.sha256(v.section_text(b,s)).hexdigest() for s in ('A5','A6')))" "$f"

# The answerer-exposure marker appears once, in C-7, with a name (expect one line).
grep -nE 'Answerer exposure: (seen|not seen) — [^[:space:]<`|]' "$f"

# Still owed (expect no output at ratification).
grep -nE '\*\*OW[E]D \(|^OW[E]D \(' "$f"

# Ratification completeness: run after C. Success is the single line "OK".
{ for k in 'Ruling' 'OD-1 / OD-2' 'Ratifying commit SHA'; do grep -qE "^- [*][*]$k:[*][*] +[^ —]" "$f" || echo "§6 $k: unfilled"; done
  for n in 1 2 3 4 5 7 8; do grep -qE "^[|] $n [|].*[|] +values block: [^|]*[|][[:space:]]*\$" "$f" || echo "§3 item $n: Ratified value cell"; done
  [ "$(awk '/^## §6/{s=1;next} /^## /{s=0} s' "$f" | grep -c '^```t00-step2-values/v1$')" = 1 ] || echo '§6 values block: missing or repeated'
  awk '/^## §6/{s=1;next} /^## /{s=0} s' "$f" | grep -A1 '^```t00-step2-values/v1$' | tail -1 | grep -q '^{' || echo '§6 values block: not set'
  sed -n 3p "$f" | grep -qE '^[*][*]Status:[*][*] `RATIFIED [0-9]{4}-[0-9]{2}-[0-9]{2}\.?`' || echo 'Status line is not RATIFIED <date>'; } | grep . || echo OK

# Authority anchors (purpose, grants, chain, values schema, Status regex).
rg -n "^SCREEN_PURPOSE|^SCREEN_GRANTS|^PREREG_CHAIN|^VALUES_SCHEMA|^_RATIFIED" ops/c1_rail/qualification/screen_authority.py

# No private value (expect no output).
rg -n '\$[0-9]|[0-9]+(\.[0-9]+)? ?% of|account [0-9]' "$f"
```
