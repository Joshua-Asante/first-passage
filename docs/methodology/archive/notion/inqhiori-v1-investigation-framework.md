<!--
Notion export (verbatim content) — Phase-2 migration per docs/adr/2026-06-12-notion-surface-retirement.md
Notion page-ID : 34cdc0b53c11812d96f8f6e9ee500d5e  (legacy canon-referenced page; resolved in docs/governance/notion-redirect-map.md)
Notion URL     : https://app.notion.com/p/34cdc0b53c11812d96f8f6e9ee500d5e
Notion path    : Trading Plan ▸ Dev-phase archive ▸ INQHIORI — the investigation framework (reference)
Source last-edited (per MCP fetch): 2026-04-24T15:05:05Z
Exported       : 2026-06-13 by Claude Code (Notion MCP fetch); container tags normalized to Markdown, text verbatim
Disposition    : framework/lesson/rule page → docs/methodology/archive/notion/
Note           : predecessor (v1) of the canonical INQHIORI mirror at docs/methodology/inqhiori-canon.md.
                 Preserved per canon §12 "for definitional content." Child page Rule 1 exported separately
                 (rule-1-small-cell-variance-prior.md).
-->

# 🧭 INQHIORI — the investigation framework (reference)

> **Purpose.** Canonical definition of the INQHIORI loop. Linked from Claude Code briefs so that phase language has a single, stable meaning. If a brief says "this is a Notice-phase pass," the scope is what this page says it is — nothing more, nothing less.
> **Domain.** General-purpose. Applied heavily in trading-system work (Guardian / Striker / Aegis) but the framework is not trading-specific. The same phases govern systems design, execution workflow refactors, and personal-development loops.

# The loop

**I**dentify → **N**otice → **Q**uestion → **H**ypothesize → **I**nvestigate → **O**bserve → **R**eflect → **I**ntegrate / **I**terate

Order matters. Each phase has entry criteria (what the previous phase hands off) and exit criteria (what must be produced before advancing). Skipping a phase is the most common failure mode — it usually looks like "jumping to Integrate" (proposing a fix before the mechanism is validated) or "jumping to Hypothesize" (inventing mechanisms before the data has been characterized).

This loop is orthogonal to **The Algorithm** (Question → Delete → Simplify → Accelerate → Automate). The Algorithm governs *what to build / keep / remove.* INQHIORI governs *how to learn before deciding.* Use INQHIORI to decide whether something is real; then use The Algorithm to decide what to do about it.

---

# Phase definitions

## 1. Identify

**What it is.** Find the high-leverage data points. Characterize the problem space structurally — where does the phenomenon live? What cells, what subsets, what anomalies?

**Entry.** A candidate worth investigating exists. Usually surfaced as an anomaly, an unexpected result, a flag from a counterfactual test, or a user observation.

**Exit criteria.** A set of *specific* data points that localize the phenomenon. Not "Wednesday is weak" — rather, "Wed-10:00-ET is the cell; 37 trades; 49% WR vs Mon-H10 65% WR on same gate." The exit artifact is usually 2–5 contingency tables or distributions, not a narrative.

**Anti-patterns.**
- Running descriptive stats without a ranked view (a flat mean tells you nothing about where the effect lives).
- Stopping at the day-level when hour-level or (day × year) sub-slicing would reveal structure.
- Carrying numbers forward from a prior doc instead of re-deriving from the source data (Rule 0 violation).

## 2. Notice

**What it is.** Note the phenomenon in detail and acquire surrounding context — exogenous data, adjacent regimes, calendar events, release schedules, correlated series. The goal is to *enrich* the Identify output, not yet to interpret it.

**Entry.** Identify phase produced a localized phenomenon.

**Exit criteria.** Identify's core finding is now annotated with context that could plausibly explain it. This phase typically produces: joined datasets, tagged trade lists, macro calendar overlays, cross-symbol comparisons. *No mechanism is selected yet.*

**Anti-patterns.**
- Proposing fixes or Pine changes (that is Integrate territory, five phases away).
- Selecting a single mechanism before the data has been annotated (that is Hypothesize).
- Collecting context that can't discriminate any hypothesis — noise enrichment.

## 3. Question

**What it is.** Formulate the precise, falsifiable questions whose answers would move belief. Each question should have a clear yes/no / measured-value resolution and should *discriminate* between candidate mechanisms.

**Entry.** Notice phase enriched the data with context.

**Exit criteria.** A short list of questions, each with (a) what the test looks like, (b) what each possible answer implies for which hypothesis. "Is Wed-H10-BOJ-week expectancy materially worse than Wed-H10-non-BOJ-week?" is a valid Question. "Is Wed bad?" is not.

**Anti-patterns.**
- Questions that can only be answered "yes" — confirmation-seeking.
- Questions whose answer doesn't change the decision (waste motion).
- Questions that require data not yet collected — that's a signal to go back to Notice.

## 4. Hypothesize

**What it is.** State candidate mechanisms explicitly. Each hypothesis must make a distinct prediction that one or more Questions from phase 3 can test. Rank by prior plausibility.

**Entry.** Questions are defined.

**Exit criteria.** A ranked list of 2–5 hypotheses. Each has: mechanism (one sentence), prediction under the Questions, rough prior.

**Anti-patterns.**
- A single hypothesis (always have a null / alternative).
- Hypotheses that all predict the same outcome (can't discriminate).
- Hypotheses built on physical ground-truth when the domain is reflexive (e.g., trading: headlines drive price regardless of physical facts; see overlay-rejection lesson).

## 5. Investigate

**What it is.** Execute the test. Run the analysis, query the data, build the counterfactual, run the MC, write the code.

**Entry.** Questions + Hypotheses are defined. This is usually where Claude Code briefs are authored — the scope is bounded by the prior phases.

**Exit criteria.** Raw results produced. Tables, plots, stats, counterfactual P&L. Not yet interpreted.

**Anti-patterns.**
- Running an Investigate before Questions are defined — produces stats without a decision rule, invites motivated reasoning.
- Scope creep mid-investigation (if a new question arises, note it, finish this run, *then* loop back).
- Modifying code or production data instead of producing analysis artifacts (Integrate jumping).

## 6. Observe

**What it is.** Read the results. State what the numbers say. Note surprises. Do *not* yet select a hypothesis winner.

**Entry.** Investigate produced results.

**Exit criteria.** A plain-language summary of what was measured and what the data showed. Confidence / sample-size caveats explicit. Surprises flagged.

**Anti-patterns.**
- Collapsing Observe into Reflect — jumping straight to "this proves H2."
- Ignoring surprises because they don't fit the leading hypothesis.
- Over-interpreting thin samples (flag cohort sizes; if n < 5 in a cell, say so).

## 7. Reflect

**What it is.** Interpret the observations. Select the hypothesis the evidence supports, refutes, or leaves undetermined. Identify what was wrong in the prior framing — especially before the loop started. Decide whether the mechanism is understood well enough to act on.

**Entry.** Observe produced a clean read of results.

**Exit criteria.** A stated interpretation with confidence level, a list of what changed about the prior model, and a Go / No-Go / Loop-Back decision for Integrate.

**Anti-patterns.**
- Reflecting only on the winning hypothesis (what did we learn about the losers? what did we learn about the *problem framing* itself?).
- Declaring understanding with no mechanism ("it's just Wednesday" — no).
- Premature confidence — if the Investigate was a single pass on a short window, say so.

## 8. Integrate / Iterate

**What it is.** Either commit the finding to the locked system (this is Integrate) or go back to an earlier phase with refined understanding (this is Iterate).

**Integrate** = parameter change, version bump, ADR, CHANGELOG entry, skill update, new methodology note. Always accompanied by a re-validation (MC re-run for trading-system changes; test suite for code changes). No silent integrations.

**Iterate** = specify which phase to return to and what new information triggered the loop-back. Common triggers: surprise in Observe that no hypothesis covered (back to Hypothesize); ambiguous Reflect (back to Question / Investigate with a tighter test); mechanism confirmed but sub-structure unresolved (forward to a new Identify loop).

**Exit criteria (Integrate).** The change is committed, validated, documented, and linked back to this loop's Notion page. A future person reading the commit / ADR can trace to the loop that generated it.

**Exit criteria (Iterate).** The next phase has a clear entry packet. No dangling state.

**Anti-patterns.**
- Integrating without re-validating (silent lock = future Rule-0 violation).
- Integrating a filter without an ADR / methodology note (knowledge loss).
- Iterating forever — if three Investigate passes haven't discriminated hypotheses, the question itself may be underspecified; go back to Question.

---

# Phase boundaries matter (worked example)

Current example in flight: **Aegis Wed-H10 investigation** (see "🔬 Wednesday on Aegis — NOTICED 2026-04-24", Notion page `34cdc0b53c1181beb912fdfee9713177`).

| Step | Phase | Artifact |
|---|---|---|
| Surfaced during BE-limit rejection post-mortem | (entry signal) | Logged candidate page |
| 3 contingency derivations on Pepperstone CSV | **Identify** | Wed-H10 localized as the cell |
| Draft brief for BOJ calendar + 10:00-ET US release calendar | **Notice** | Exogenous data to be joined |
| (pending) "Is Wed-H10-release-day materially worse than non-release-day?" | **Question** | — |
| (pending) Release-clustering vs BOJ-proximity vs structural-flow | **Hypothesize** | — |
| (pending) Joined subgroup expectancy tables | **Investigate** | — |
| (pending) Read what the tables say, flag thin cohorts | **Observe** | — |
| (pending) Select / reject mechanisms, state reframe | **Reflect** | — |
| (pending) Either filter proposal + MC re-run + ADR, or loop back | **Integrate / Iterate** | — |

Each phase produces a linkable artifact. A brief that claims to be in "Notice" but proposes Pine changes has jumped six phases and needs to be rejected.

---

# Cross-references

- **Rule 0** (audit-first for risk-control decisions) is Identify-phase discipline: *always* re-derive from production code / source data before authoring a brief. See fxify-challenge skill.
- **The Algorithm** (Question → Delete → Simplify → Accelerate → Automate) runs *after* INQHIORI delivers a validated finding. INQHIORI tells you if X is real; The Algorithm tells you whether to delete / simplify / accelerate / automate X.
- **Headlines-not-physics lesson**: Hypothesize phase must not build on physical ground-truth in reflexive domains (markets). The Hormuz-overlay rejection is the canonical example.
- **Single-rule-suspicion corollary**: when Identify finds a phenomenon described as "one rule," assume there's a second rule and look for it (belt-and-suspenders is the default engineering pattern).

---

# Usage notes for Claude Code

- Every brief should declare its phase in the header ("Notice-phase pass," "Investigate-phase run," etc.).
- A brief must not request work from phases it hasn't entered. If a Notice brief's deliverables include "propose a filter," the brief is malformed — reject and request a scoped-down version.
- Phase exits are user-gated. Claude Code does not advance phases autonomously; it produces the current phase's artifact and returns to the user for the Reflect / next-phase decision.
- When in doubt about phase, ask. The framework is worthless if phase labels drift.

---

*Child page (exported separately):* 📐 Rule 1 — Small-cell variance prior (`34cdc0b53c11812cbb4ff637ba44736e`) → `rule-1-small-cell-variance-prior.md`
