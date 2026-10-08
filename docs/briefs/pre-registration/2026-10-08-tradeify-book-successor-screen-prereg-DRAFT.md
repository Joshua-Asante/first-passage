# Pre-registration (DRAFT skeleton) — one screen of one successor configuration of the Tradeify book

**Status:** `DRAFT — NOT FROZEN.` SKELETON. Every field marked owed to the operator is set before freeze. Nothing here binds a replay, screen, Monte Carlo or verdict until this line reads `FROZEN <YYYY-MM-DD>` and the freeze commit SHA is recorded in §9.
**Authority:** Joshua (operator), 2026-10-08, via the First Passage Deployment Coordinator: "go with your suggestions 1-3" (item 3, parallel work). Drafting only.
**Owner:** the T00 line ([amendment §T00](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#t00--feasibility-evidence-for-the-selected-book-new-investment-decision-not-a-gate-250k500k-may-return-early) step 3: after NO-GO-evidence, "adjust the book" is an operator investment decision). The successor direction comes from the [Tier-2 card](../handoffs/2026-10-08-t00-step12-diagnostic-tier2-scoping-card-DRAFT.md) §2.1 pattern table.
**Loop of record:** STRATEGIC (investment decision on an adjusted book; K accounting in §2).
**Authored:** 2026-10-08, Claude Code (drafting only). The operator owns every OWED field, the stopping rule and the freeze.

**This draft authorizes nothing:** no replay, screen, Monte Carlo, source build, signing, dispatch or spend. It contains no Pine, port, account identifier, private value, rate, dollar figure or count.

## §R — Standing rule: no candidate-configurable replay before freeze

[Deployment checklist](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md) item 7.6.1 (operator ruling 2026-10-02): no agent runs a candidate-configurable replay before its pre-registration is frozen. Every configuration this file could pre-register is candidate-configurable ([Tier-2 card](../handoffs/2026-10-08-t00-step12-diagnostic-tier2-scoping-card-DRAFT.md) §1: "Leg off, rescale, adds off or any input change is a candidate replay").

## §0 — Production reads (anchors: `origin/main@bd07b45`, 2026-10-08)

| Source | What it fixes here |
|---|---|
| [`2026-10-01-tradeify-t00-step2-screen-prereg.md`](2026-10-01-tradeify-t00-step2-screen-prereg.md) (#581, `RATIFIED 2026-10-07`) §2 A2, A5, A6, §3 | The gate this file mirrors: per-population bust ≤ 5.0% under the pessimistic A5 assignment, FULL pass floor with a finite median inside the horizon, robust vs `UNDETERMINED`-dependent labels, the `t00-step2-values/v1` values-block form |
| [`2026-10-02-tradeify-route-native-editions-successor-prereg.md`](2026-10-02-tradeify-route-native-editions-successor-prereg.md) §D, §R, §7, §8, §10 | Successor discipline: disclosure, standing rule, answerer-exposure marker, freeze procedure, OWED grep, frozen-Status hook |
| [`2026-08-26-prop-survivor-scoring-prereg-v2.md`](2026-08-26-prop-survivor-scoring-prereg-v2.md) §2 G7, §3 | G7: funded-phase ruin diagnostic, funded geometry, funded bust ceiling; does not gate §4 |
| [`2026-10-02-four-firm-dated-remc-prereg-DRAFT.md`](2026-10-02-four-firm-dated-remc-prereg-DRAFT.md) row I-10 | Part B funded ceiling carried as a G7 diagnostic, "never gates §4" |
| [Tier-1 card](../handoffs/2026-10-08-t00-step12-diagnostic-tier1-card.md) §8 and its 2026-10-08 addendum | Reader log entries 1–5; keys `60c128a7…329e`; "Any successor pre-registration names these readers" |
| [Tier-2 card](../handoffs/2026-10-08-t00-step12-diagnostic-tier2-scoping-card-DRAFT.md) §1, §2.1, §4, §7 | Pattern rows 1–6 and the directions they point to; shares are accounting, not cause; pattern pick counts as K + 1; Tier-2 readers join the reader log |
| `ops/c1_rail/qualification/screen_authority.py:44-56` | `SCREEN_PURPOSE = 'T00_STEP3_SELECTED_BOOK_SCREEN'`; grant `T00_STEP3_SCREEN_ONCE`; refusals include `PARAMETER_CHANGE` and `FALSIFIER_EVIDENCE`; `PREREG_CHAIN` holds #581 only; "A re-attempt appends a successor here" |
| `ops/c1_rail/qualification/screen_authority.py:197-202`, `:410` | The authority checks that the pre-registration path is a compiled constant and the last `PREREG_CHAIN` entry, and binds `a5_text_sha256` / `a6_text_sha256` |
| `ops/c1_rail/qualification/production_source.py:400-412` | R1 places the schedule instant at the **adverse** vertex, R2 at the favourable one |
| `AGENTS.md` "Strategy Authorization Lifecycle", "Protection", "Firm Expansion" | Decay permits pre-registered de-risking, never re-optimization; `DD_TRIGGER` / `DD_SCALE` change-control path; a funded geometry needs the `core/mc/preflight.py` engine-support pre-flight |

Not read: Pine, ports, effective inputs, the Tier-1 report, series or key list, the #724 private results, any Tier-2 output (none exists).

## §1 — Purpose

One pre-registered screen of **one** successor configuration of the Tradeify book, chosen from the Tier-2 §2.1 pattern before any successor output exists. The configuration is a de-risking of the declared book (size cut, adds off, leg dropped or reshaped, uniform or early-phase per-session risk reduction), never a re-optimization. If the Tier-2 report names row 6 ("no evidence-supported successor"), this file is not frozen and returns to the operator.

| # | Field | Status |
|---|---|---|
| C-1 | **Tier-2 pattern row(s) relied on** (rows 1–5 by number; with the Tier-2 report SHA-256) | **OWED (operator)** |
| C-2 | **Base expressions:** the declared book (r3c identities) or the route-native editions (successor preregs, once frozen) | **OWED (operator)** |
| C-3 | **Leg set** | **OWED (operator)** |
| C-4 | **Size vector** (per leg, base and add; the risk-sized leg's cap) | **OWED (operator)** |
| C-5 | **Adds rule** (unchanged, off when protected, off always) | **OWED (operator)** |
| C-6 | **Per-session risk-reduction rule and its thresholds** (only if row 5 is relied on) | **OWED (operator)** |
| C-7 | **Answerer exposure** for C-1..C-6, in the last cell, in the form `Answerer exposure: seen|not seen — <name>` naming whether the answerer saw the Tier-1 report, the Tier-2 report, both or neither | **OWED (operator)** |

The book protection policy (1% combined-peak trigger, 0.40 scale, prior-close timing, 80-micro capacity, takeover order) is inherited unchanged. Changing it is outside this file (§5).

## §2 — K accounting

- Choosing a configuration from the Tier-2 pattern is one selection: **K + 1** for this successor ([Tier-2 card](../handoffs/2026-10-08-t00-step12-diagnostic-tier2-scoping-card-DRAFT.md) §7, "Selection count").
- **Each further configuration screened is another trial** (K + 2, K + 3 …), whether under this file or a sibling. A sibling needs its own frozen pre-registration (§R).
- K₀, the trial count carried by the declared book's lineage before this pick, is **OWED (operator)**, read from the K ledger (`futures-anomaly-discovery` skill) and recorded here before freeze.
- The step-12 result on the declared book is the observation that prompted the search; it is a trial already counted, not a free look.

## §3 — Exposure statement

Readers of per-session or per-leg step-12 detail, before this file was written:

| # | Reader | Date / time | Saw | Source |
|---|---|---|---|---|
| T1-1 | Executor session (smoke run) | 2026-10-08 | Selected keys, per-stratum counts; no series, no report | Tier-1 card §8 |
| T1-2 | Executor session (read-only attestation check) | 2026-10-08 ~04:57Z | Binding held; in-memory key-list hash | Tier-1 card §8 |
| T1-3 | Executor session | 2026-10-08 ~07:10Z | Per-path sealed series and the report | Tier-1 §8 addendum, reader 3 |
| T1-4 | Joshua | 2026-10-08 ~07:12Z | Findings summary in chat; no series, no keys | Tier-1 §8 addendum, reader 4 |
| T1-5 | Deployment Coordinator | 2026-10-08 ~07:40Z; ~08:10Z | The summary; then the report (no series) | Tier-1 §8 addendum, reader 5 |
| T2-* | Tier-2 readers | **TBD** | **OWED (operator, from the Tier-2 reader log)** | Tier-2 card §7 |

Also exposed to everyone: the public step-12 verdict `NO-GO-evidence-robust` on the declared book (#724), and the Tier-2 card's admission-time row 5 (Tier-2 card §2.1, row 5 provenance).

**Drafter.** This session read the Tier-1 §8 addendum (hashes, labels and the reader log only) and the Tier-2 card. It read no report, series, key list, results file or private source, and ran nothing.

**§3 completeness.** The operator adds any reader the table does not list before freeze — **OWED (operator)**.

## §4 — Hypothesis and falsifier

**H.** If the configuration fixed in §1 is screened under §6 on keys fixed under §7, then it meets every binding §6 gate (GO-evidence); otherwise it is NO-GO-evidence and the configuration is not adopted.

**Falsifier.** Any binding §6 gate fails under the pessimistic A5 assignment, or any binding gate fails on H2 under R1 alone (§6 G2).

The verdict is descriptive of this configuration on these keys. It is not a rate estimate for any other configuration and does not re-open the step-12 verdict.

## §5 — Forbidden moves

- Running any replay, screen, Monte Carlo or source build on a successor configuration before this file is FROZEN (§R).
- Screening more than one configuration under this file, or choosing the configuration after any successor output exists.
- Sweeping sizes, legs or thresholds and keeping the best (re-optimization; AGENTS.md "Strategy Authorization Lifecycle").
- Changing `DD_TRIGGER` / `DD_SCALE`, the book protection cell, capacity or takeover order here. That path is pre-registration → re-MC → both-halves regime gate → admitting ADR (AGENTS.md "Protection").
- Editing locked Pine, ports or `core/strategies` artifacts in place.
- Amending any §1, §6 or §7 value after successor output exists. Close this file and open a fresh one instead.
- Reusing the step-12 grant or run directory, or re-running step 12 (Tier-2 card §3.3).
- Reading or citing a §6 result as four-firm §4 falsifier evidence (§8).
- Publishing any private value (rate, dollar figure, count, key, P&L, port body, effective-input value) in a public surface.

## §6 — Gates and verdict

Each gate's structure mirrors #581 A6; its numbers are the cited owners' unless the operator sets otherwise at freeze. Paths are classified by #581 A5 (1)–(3).

| # | Gate | Population / ordering | Threshold (owner) | Binding? |
|---|---|---|---|---|
| G1 | Bust proportion, pessimistic A5 | FULL, H1, H2 (each) | ≤ 5.0% (prereg v2 §3, as #581 A2) | Binding |
| G2 | Bust proportion, **R1 runs alone** (adverse vertex) | **H2** | ≤ 5.0% (prereg v2 §3) | Binding |
| G3 | P(pass within horizon), pessimistic A5, finite median inside horizon | FULL | prereg v2 §3 pass floor, as #581 A2 | Binding |
| G4 | P(pass within horizon), **R1 runs alone**, finite median inside horizon | **H2** | prereg v2 §3 pass floor, or another value | **OWED (operator)**: value, and binding or reported |
| G5 | **Funded survival (G7-style)**: funded-phase bust proportion on the funded geometry | FULL and H2-R1 | prereg v2 §3 funded ceiling (G7 candidate) | **OWED (operator)**: tier, ceiling, binding or diagnostic |
| G6 | **Economics check** | — | **OWED (operator)**: metric and threshold (placeholder; no figures here) | **OWED (operator)** |

- **Why G2/G4.** FULL alone can hide a late-sample failure; H2 is the more recent half, and R1 is the adverse intrabar vertex (`production_source.py:400-412`). R1-alone is a run-level reading, not the A5 path verdict; it is reported beside A5, never folded into it.
- **G5 producer.** The qualification runner evaluates the eval geometry (`Tradeify_Select_100K`). A funded geometry needs the `core/mc/preflight.py` engine-support pre-flight and a producer that supports it before G5 can bind — **OWED (operator / build owner)**.
- **Assignment dependence.** Each gate is evaluated under the pessimistic (P) and optimistic (O) assignments of #581 A5 (3). G1 and G3 depend on the assignment. G2 and G4 do not: they read each path's R1 run alone, classified by A5 (1), so P = O. G5's FULL component depends on it and its H2-R1 component does not. G6 declares at freeze whether its metric reads A5 path outcomes; if not, P = O — **OWED (operator)**.
- **Decision rule, in precedence order** (*added 2026-10-08, operator review of `6ed1e37`*):
  1. **INSUFFICIENT** if any #581 A6 INSUFFICIENT condition holds, any binding gate has no admissible producer, or any binding gate's value is unset. This is decided before any tally is read, as `verdict.py:evaluate` does for #581 (row V1). No GO or NO-GO subtype is reported with it.
  2. **GO-evidence** if every binding gate passes under P.
  3. **NO-GO-evidence, `UNDETERMINED`-dependent** if not (2) and every binding gate passes under O.
  4. **NO-GO-evidence, robust** otherwise. A failed assignment-independent binding gate therefore always yields a robust NO-GO.
  5. A reported (non-binding) gate never enters the label.
- **Classifier.** `ops/c1_rail/qualification/t00_screen/verdict.py:evaluate` implements this rule for G1 and G3 only. Extending it to G2, G4, G5 and G6 under the rule above is a reviewed code change before freeze — **OWED (build owner)**.
- **Verdict mapping.** On H (§4): GO-evidence is RESOLVED, NO-GO-evidence is FALSIFIED, INSUFFICIENT is AMBIGUOUS. A GO-evidence verdict is an input to an operator investment decision; it admits nothing, authorizes no capital and deploys nothing.

## §7 — Data

- **Panels and populations:** the admitted panels and FULL / H1 / H2 partition bound by the candidate contract (§8). Every panel is already fully exposed through step 12, Tier 1 and Tier 2; disjoint keys give fresh paths over the same history, not new history. The report says so.
- **Key set:** drawn under an RNG tag and roots distinct from step 12's `t00-screen-rng/v1` roots, and **disjoint from the Tier-1 keys (`60c128a7…329e`) and the Tier-2 keys (SHA-256 TBD)**. If disjointness is not achievable or not checked, the overlap is disclosed in the report beside every gate result — **OWED (operator)**: tag, roots, depth, budget, disjointness check or disclosure.
- **Values block:** one `successor-screen-values/v1` line, set at freeze, in the #581 §6 form — **OWED (operator; block name subject to the build owner)**.

## §8 — Governance

1. **Candidate contract.** A configuration that changes sizes, legs, adds or inputs is not r3c (r3c binds the declared book's `effective_settings` and policy code). It needs a new candidate source contract, a fresh operator-signed source approval, and an accepted P7 record for its identities at the executing head — **OWED (operator / build owner)**.
2. **Screen authority.** The existing authority's purpose is the selected book, its grant is `T00_STEP3_SCREEN_ONCE`, and its refusals include `PARAMETER_CHANGE`. A successor screen needs a separately signed authority under a purpose and refusal set that admit this configuration, which is a reviewed code change — **OWED (operator / build owner)**.
3. **Pre-registration chain.** This file is appended to `PREREG_CHAIN` in `screen_authority.py` (design §4.5) by a reviewed change, after freeze. Whether `_check_prereg` accepts this file's shape (section hashes, values block) is for the build owner to confirm before freeze — **OWED (build owner)**.
4. **Not four-firm §4 evidence.** As #581 §1b: no verdict here, GO-evidence included, discharges or fires the four-firm §4 falsifier dated 2026-11-08 or counts toward its clearer count.
5. **D-feed.** What a successor verdict means for D-feed condition (a) is not decided here; it is recorded at the D-feed owner before the screen returns — **OWED (operator)**.

## §9 — OWED list, stopping rule and freeze

Owed (operator) at freeze: C-1..C-7; K₀ (§2); T2-* readers and §3 completeness; G4 value and binding; G5 tier, ceiling and binding; G6 metric and threshold; §7 RNG tag, roots, depth, budget and disjointness; §8 items 1, 2, 3 and 5; G6 assignment dependence and the classifier extension (§6); the stopping rule below.

**Stopping rule (placeholder): OWED (operator), decided at freeze.** Options, none adopted: (a) one configuration only; any NO-GO ends the successor line on this book; (b) a stated maximum number of configurations, each its own frozen file and its own K increment; (c) stop on a named condition (for example a robust NO-GO with G2 failing).

**Freeze procedure.**
1. The Tier-2 report is delivered and accepted; its SHA-256 and the T2-* readers are recorded.
2. The operator sets every OWED field in words or in the values block (no private values in public text).
3. The build owner confirms §8 items 1–3.
4. Claude runs §10 except the Status hook; the operator reviews the full text.
5. The operator says "freeze". Status becomes `` **Status:** `FROZEN YYYY-MM-DD` `` and the freeze commit SHA is recorded here.
6. In the freeze commit, §10 runs in full. Any failure voids the freeze and the Status reverts to `DRAFT — NOT FROZEN.`

- **Freeze commit SHA:** at freeze.

## §10 — Audit hooks

```bash
f=docs/briefs/pre-registration/2026-10-08-tradeify-book-successor-screen-prereg-DRAFT.md
# Form (expect RESULT: well-formed).
python -I scripts/fp.py python scripts/check_brief.py --type brief "$f"
# No unresolved status at freeze (expect no output).
grep -nE '\*\*OW[E]D \(' "$f"
# C-7 answerer exposure present with a nonempty name (expect one line at freeze).
grep -nE '^\| C-7 .*Answerer exposure: (seen|not seen) — [A-Za-z][^|]* \|$' "$f"
# Status is frozen (expect one line at freeze; no output while DRAFT).
grep -nE '^\*\*Status:\*\* `FROZEN [0-9]{4}-[0-9]{2}-[0-9]{2}`' "$f"
# Screen authority anchors still hold (purpose, once-only grant, PARAMETER_CHANGE refusal, chain).
rg -n "SCREEN_PURPOSE|SCREEN_GRANTS|PARAMETER_CHANGE|^PREREG_CHAIN" ops/c1_rail/qualification/screen_authority.py
# R1 is the adverse vertex.
sed -n '400,412p' ops/c1_rail/qualification/production_source.py
# No private value (expect no output).
rg -n '\$[0-9]|[0-9]+(\.[0-9]+)? ?% of|account [0-9]' "$f"
```
