# ADR 2026-07-25 — Instrument-profile index: mechanism × instrument verdict view + intake consult

**Status:** Accepted
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Revision:** 2026-10-15 — retention trim (ADR decay audit; operator direction 2026-10-15): §0 read list compressed; §2b one-time permission restated in the past tense; §6 landing-artifact lists, §7 build narrative, Execution-note-1 measurement/sweep detail, stale §10 hooks, the Verification block, Addendum (b) narrative and the change-history table removed; dead design-doc links unlinked. Pre-trim text at blob `663a229d073cad2f0c3d21f3ca11295f703c443c` (commit `4121e84c95f4990b71962e3b9570c4c3fad88426`).
**Decision date:** 2026-07-25
**Authors:** Joshua (ratification) + Claude Code (design + build, Tasks 1-10)
**Supersedes:** none
**Related:** [`docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md`](2026-06-11-instrument-ledger-and-cfg-fingerprint.md) (parent decision — homes the ledgers this project indexes; §5 backfill rule this ADR scopes an override against; template for this ADR's shape) · `docs/superpowers/specs/2026-07-25-instrument-profiles-design.md` (design doc this ADR records — not in the public tree; private archive per `docs/ltm/README.md`; this ADR is the public owner of the contract) · [`docs/operational_rules.md`](../operational_rules.md) Rule 10 (amended one clause by this ADR) · [`docs/methodology/strategy_harvest.md`](../methodology/strategy_harvest.md) §1 (amended one requirement by this ADR) · `docs/superpowers/specs/2026-07-16-status-consistency-checker-design.md` (C1 lesson, restated in §5; private archive only)
**Layer:** governance / infrastructure (R&D session tooling) — does not touch strategy code, allocations, `dd_protection`, Pine, or vendor panels

---

## §0 — Rule 0 reads (production-source verification)

Read at worktree HEAD `171c7d0` (2026-07-25) before authoring: the parent decision (Related), `docs/operational_rules.md` Rule 10, `docs/methodology/strategy_harvest.md` §1, `scripts/instrument_profiles.py`, worked `ops/instruments/` ledgers and the two private design specs. Full read list: pre-trim text (Revision line).

---

## §1 — Context

Tasks 1-9 built and landed the tooling this ADR governs: a `## PROFILE (machine-readable)` YAML block seeded into all 21 substantive `ops/instruments/*.md` ledgers (plus a `no-profile` marker on the `US500.md` redirect stub), a curated mechanism vocabulary at [`ops/instruments/MECHANISMS.md`](../../ops/instruments/MECHANISMS.md), a builder that emits a mechanism-first derived view (`ops/instruments/PROFILES.md` + `profiles.json`), a consistency gate wired into `scripts/githooks/pre-commit`, the `Makefile`, and CI, and a `cell` consult subcommand. What was not yet done — and is this task's entire scope — is the governance record: the ADR that ratifies the design, the Rule 10 clause that folds the profile block into the standing session-end obligation, and the `strategy_harvest.md` §1 amendment that binds the consult into intake.

**Why a second surface over the ledgers is admissible** (inherited from the design doc, §Problem): the ledgers are, and remain, the source of record — *"the ledger links out, never restates"* is the parent ADR's own rule, applied one level down. What was missing was not a ledger defect but an addressing defect: instrument-only addressing makes a prior finding reachable only by someone who already knows to open that instrument's file, which is exactly backwards from how a new candidate is scoped (mechanism first, instrument sometimes still open). The distinction that keeps this design from repeating the `STATE.md` hand-sync drift class: **the profile view is generated, never authored** — `PROFILES.md`/`profiles.json` carry a `GENERATED — do not hand-edit` header and a P3 gate (§2 below) makes the committed view unfalsifiable against a fresh build.

**Decision driver (one sentence):** Tasks 1-9 shipped working, gated tooling with no governing decision behind it — an ungoverned gate is exactly the ceremony trap the monorepo-boundaries ADR's H3 warns against (§4 below), so the record has to land before this is treated as a standing obligation rather than a one-off seeding pass.

---

## §2 — Decision

### §2a — Schema, value-carrying rule, vocabulary growth rule, generated-view invariant (ratified)

Each instrument ledger MAY carry a fenced-YAML `## PROFILE (machine-readable)` block (placed between the ledger header and `## STANDING WARNINGS`) with the schema below. A ledger with nothing to index (the `US500.md` redirect stub) carries an explicit `<!-- no-profile: redirect stub -->` marker instead; an unmarked ledger with neither is a gate failure (P1).

```yaml
symbol: MYM
asset_class: equity-index-futures
family: [YM]                    # parent/sibling ledgers whose bars + warnings are inherited
venue_tradable: true             # at the live firm; false ⇒ research-only
venue_note: "..."                # optional, one line, when false/conditional
k_bank_source: "../../discovery_manifests/"   # POINTER ONLY
cost_hurdle:
  value: 6.57
  units: "bp/event"              # as-stated; never normalized across units
  basis: "4x Tradeify hurdle"
  source: "#M6"                  # anchor into this file's own prose row
cells:
  - mechanism: opening-range-continuation
    verdict: DEAD
    date: 2026-07-16
    source: "../../docs/briefs/closures/2026-07-16-striker-mym-reconstruction-candidate-2-falsified.md"
bars:
  - id: index-intraday-ohlcv-directional-timing-2026-07-21
    source: "../../docs/rejected_candidates.md"
structure:
  - claim: "Granularity-tolerant at plausible stops (unlike MNQ)."
    source: "#active-open"
```

**Verdict vocabulary (closed, four values):** `DEAD` · `AMBIGUOUS-PARKED` · `CONTINGENT-FORWARD` · `LIVE`. Untested is the absence of a cell — no row means no prior, which is the exact signal candidate generation needs; the schema never distinguishes "not tested" from "tested, inconclusive" by an easily-forgotten explicit marker. `structure` is a separate top-level list, not a fifth verdict: a `DEAD` verdict and a positive structural finding routinely coexist on the same null (ZB × `opening-range-breakout` is `DEAD` as a trade *and* yields "ZB fades its opening range" as a cross-instrument prior) — both are indexed, only `structure` propagates to the class level via `MECHANISMS.md`.

**The value-carrying rule (general — decides every future "should the block hold X?" question without re-litigation): a PROFILE block may carry a *value* only where this ledger is that value's canonical home.** Values canonical elsewhere are carried as pointers only. Two deliberate asymmetries this rule produces, both load-bearing:

- **K bank — pointer, never a value.** `K_banked(family)` is canonical in `discovery_manifests/` (repo-root, per `lab/discovery/register_search.py`'s `LEDGER` path), it only ever grows, and `strategy_harvest.md` §1 already instructs readers to *re-read the manifests, never trust a snapshot line*. A PROFILE block carrying a number would be a third K surface violating that instruction on day one. `k_bank_source` carries the pointer; the `cell` consult prints it and tells the caller to read it, never a cached figure.
- **Cost hurdle — value carried, with a stated limitation.** The hurdle is a ledger-owned durable finding (e.g. MYM M6), so the value rule permits carrying it, and the `cell` consult needs it machine-readably to feed `strategy_harvest.md` requirement 5's arithmetic. The block carries value + units + a source anchor, and the checker always prints the number **with** its source, never bare. Known limitation, stated rather than hidden: the gate verifies the anchor *resolves* — it does not verify the number matches the cited prose row (that would require parsing the heterogeneous per-ledger prose tables this design's Approach C rejected, §3 below). This is intra-file duplication (one file, one editor, both visible on one screen) — materially lower drift risk than the cross-file class, but not zero and not machine-caught. Units are carried as-stated and never converted (`bp/event` and `R` hurdles do not convert safely; a silent normalization would be a wrong-number-with-confidence failure, worse than the pointer form).

**Vocabulary growth rule.** `MECHANISMS.md` is curated and closed-by-default (seeded from the 15 families observed in the 2026-07-25 scan — see `ops/instruments/MECHANISMS.md`). A candidate declares its nearest existing class **or** explicitly declares `NEW`. `NEW` is permitted — it is not a bar — but it lands as a `MECHANISMS.md` entry **in the same commit** as the pre-registration that introduced it. An id that never reaches `MECHANISMS.md` fails the gate (P2) with a nearest-match suggestion rather than silently creating a synonym. This is not an attempt at an ontology: class boundaries are judgment calls, the taxonomy will be imperfect, and the gate's job is to force the declaration to be explicit and reviewable, not automatically correct — a miscategorized candidate is visible in review, an undeclared one is not.

**The intake consult requirement.** Every candidate pre-registration and every `strategy_harvest.md` §1 admission must run the `cell` consult (`python scripts/instrument_profiles.py cell <SYMBOL> <mechanism-id>`) and record the result before proceeding. Nonzero exit means a prior binds the cell (a re-proposal bar, a parked concept sharing the instrument's anti-SNAG budget, or a running forward test) — the pre-registration must name and address it; it is not a permanent bar. `structure` priors print on every consult regardless of verdict: nulls aim the next candidate, they do not merely block it. This is the design's stated operator framing — *"use the null findings and/or positive findings to our advantage"* — made mechanical.

**The derived-view-is-generated invariant.** `ops/instruments/PROFILES.md` and `ops/instruments/profiles.json` are generated artifacts (`GENERATED — do not hand-edit; source = ledger PROFILE blocks` header on both) and are never hand-edited. `python scripts/instrument_profiles.py build` regenerates them from the authored PROFILE blocks + `MECHANISMS.md`; `python scripts/instrument_profiles.py check` (P3) diffs the committed view against a fresh in-memory build and hard-fails on drift. This is the property that makes a second surface admissible over the ledgers at all (§1) — a derived artifact that a gate regenerates and diffs cannot silently drift from its source, it can only fail the build.

### §2b — Scoped §5 override for the seeding pass (ratified)

The parent ADR's §5 forbids pre-emptively backfilling ledgers, and Tasks 1-9's seeding pass touched all 21 existing substantive ledgers (plus the `US500.md` stub) in one motion. Per the same operator-approval pattern as the parent ADR's ratified **Addendum — 2026-07-16 · Scoped §5 override (XAGUSD + EURUSD ledger creation)**, this is recorded as a **scoped** override, not a general repeal:

**What this override permitted (one-time, executed 2026-07-25):** adding a derived-index PROFILE block (or the `no-profile` marker) to ledgers that already existed — a re-indexing of committed findings, not an adjudication.

**What this override does NOT permit:** creating `ops/instruments/*.md` ledgers for **un-ledgered instruments**. The parent ADR's §5 creation-on-touch default — a ledger is created on the first session touching a new instrument, no pre-emptive backfill — stands untouched. A PROFILE block can only be added to a ledger that a prior session already had cause to create; this ADR does not license inventing new instrument coverage to complete the matrix.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **B — central structured registry (`profiles.yaml`), ledgers link out** | Simpler parsing, but inverts ownership: the ledger stops being the single source of instrument truth and every closure gains a second mandatory write target — precisely the dual-surface drift class that produced the `STATE.md` incidents and the status-consistency gate. Rejected on the repo's own precedent. |
| **C — generate from existing prose tables, add nothing** | Zero authoring burden, but ledger tables are heterogeneous by design (MYM uses `M#`, XAUUSD uses `F#`/`D#`; column sets differ per file), so the parser would be brittle; a mechanism-class column would still have to be added everywhere for the matrix to mean anything — most of the chosen approach's authoring cost with a worse, prose-parsing-dependent gate. |
| **A — PROFILE block in each ledger + generated matrix + intake checker (CHOSEN)** | Ledger stays the source of record; the index is derived, so it cannot drift; the gate reuses the established pre-commit pattern (gates 1-10 → this joins as gate 11). Cost: a 21-ledger seeding pass + taxonomy curation, both one-time. |
| A semantic auto-join between profile cells and `rejected_candidates.md` entries | Deliberately not built — this is exactly the join the status-consistency checker's C1 tried and that fell to 100% false positives on real data (a rejection context legitimately links apparatus/parent studies that are themselves live). §5 below. |
| Do nothing (leave the profile view instrument-addressed only, as it was pre-Task-1) | The three concrete failure modes the design doc names (re-spending K on a known-dead cell; positive structure buried inside nulls; class-level bars not binding where authored) are all *currently occurring* patterns in this ledger corpus, not hypothetical — see the Treasury-complex tail-exhaustion miss under §Execution-notes below, caught in this same build. |

---

## §4 — Falsifier (revert trigger)

**H:** the profile layer changes candidate-generation behavior at sustainable cost.

Copied verbatim from the design doc §9 (the frozen calibration this ADR ratifies):

> It is **falsified** if, at the second `programme-audit` cycle after acceptance, either (a) no pre-registration has recorded a profile consult that altered its scoping — the layer is ceremony, and should be reduced to the generated view with the intake requirement withdrawn; or (b) the P2 vocabulary check fires so often on legitimate new mechanisms that the taxonomy is obstructing rather than indexing — in which case the closed-vocabulary default is wrong and the check drops to advisory. It is **resolved** if at least one candidate has been redirected or re-scoped by a consult, or one `structure` prior has aimed a new candidate.
>
> The honest prior on (a): this programme's research cadence means the sample after two cycles may be small. If exposure is under two scoped candidates, the correct verdict is **AMBIGUOUS — carry unchanged**, not a forced call. Recorded here so a thin sample is not read as a pass.

The thin-sample clause is deliberate and must not be dropped on any future re-read of this ADR: a low-exposure window reads AMBIGUOUS, not a default pass and not a default fail. This is the same H3 "gate that never bites decays to ceremony" calibration standard the design doc cites from [`docs/adr/2026-06-05-monorepo-layer-boundaries.md`](2026-06-05-monorepo-layer-boundaries.md) §4 — a falsifier that a thin sample could satisfy by default would not be measuring anything.

**Trigger check schedule:** rides the existing `programme-audit` cadence; first look at the next scheduled cycle after 2026-07-25, binary evaluation at the second.

---

## §5 — Forbidden moves (under this ADR)

- **No semantic join to `rejected_candidates.md`.** No mechanism auto-joins a profile cell to a `rejected_candidates.md` entry's own status. This is the C1 lesson from the status-consistency checker's first real run — designed as exactly this join, it fell to **100% false positives** (a rejection context legitimately links apparatus/parent studies that are themselves live, e.g. an active harness cited as apparatus for a rejected gate) and was dropped, not softened. Profile cells point at `rejected_candidates.md` with explicit links; link *resolution* is checked (P1), link *meaning* is not.
- **No restating evidence in PROFILE blocks.** The block carries verdict rows and pointers, not evidence — discriminator text, statistics, and re-proposal-bar wording stay in the prose tables that already own them; the block points at them. A block that restates values becomes the next `STATE.md`-class drift incident, one level down from the parent ADR's own §5 rule against ledgers restating strategy parameters or locked constants.
- **No snapshotting K values.** `k_bank_source` is a pointer field only (§2a); a PROFILE block, an audit note, or a consult output that hardcodes a `K_banked(family)` number instead of pointing at `discovery_manifests/` violates the value-carrying rule and reintroduces the exact stale-snapshot risk `strategy_harvest.md` §1 already warns against.
- **No hand-editing the generated view.** `ops/instruments/PROFILES.md` and `ops/instruments/profiles.json` are regenerated by `python scripts/instrument_profiles.py build`, never edited by hand — both carry a `GENERATED — do not hand-edit` header, and P3 catches a hand-edit as drift against a fresh build.
- **No creating ledgers for un-ledgered instruments under this ADR's scoped override.** §2b's override covers seeding PROFILE blocks into ledgers that already exist; it does not extend the parent ADR's creation-on-touch exception. A new instrument still needs a live touching session, not a "complete the matrix" motive.

---

## §6 — Consequences

**Positive:**
- A mechanism-first cross-instrument view exists where before the ledgers were reachable only instrument-first — the three concrete failure modes named in §1 (re-spent K, buried positive structure, non-binding class-level bars) now have a mechanical index and consult surface.
- The derived-view-is-generated property (§2a) means this second surface cannot drift silently from the ledgers the way `STATE.md` drifted from its sources — a stale view is a build failure, not a slow-motion incident.
- The intake consult (§2a) folds directly into the existing `strategy_harvest.md` admission chain and the `register_search` pre-registration lane — no parallel gate invented, per the design doc's binding-points discipline.

**Negative (real cost):**
- A curated, closed-by-default vocabulary (`MECHANISMS.md`) is a maintenance surface that grows only deliberately (§2a growth rule) — a legitimate new mechanism class that a session forgets to land in the same commit as its pre-registration fails P2 until corrected.
- The cost-hurdle intra-file duplication risk named in §2a (value + prose row, same file, not machine-cross-checked) is accepted, not eliminated.
- Every future session touching an instrument now has one more mechanical obligation at session end (Rule 10's amended clause, below) beyond the existing ledger disposition append.

**Risks:**
- Date provenance on seeded cells is not gate-enforced (§Execution-notes below) — a `source` link resolving on disk (P1) says nothing about whether that source self-dates the cited verdict date. Mitigation: the standing rule recorded in §Execution-notes (prefer a self-dating closure/scoping/ADR document over a numbers-only `RESULTS.md`), enforced by review discipline, not machine gate, until/unless a future amendment adds one.
- A missing `bars` entry silently under-reports rather than erroring loudly (§Execution-notes below) — the schema has no mechanical check that every applicable class-level bar was actually inherited.

---

## §7 — Implementation plan

**Out of scope (not built):** prose-verdict parsing (Approach C), auto-generated `structure` rows, any semantic join to `rejected_candidates.md`/`lab/CATALOG.md`, ledger backfill, machine-verifying `cost_hurdle` against prose, a firm/venue profile surface. Tooling: `scripts/instrument_profiles.py` `build`/`check`/`cell`.

---

## Execution notes — what building this taught (2026-07-25)

Three findings surfaced during Tasks 1-9's build and seeding pass that belong in the permanent record, not just the PR history:

1. **Date provenance was the weak point; it is now PARTIALLY gated.** Review caught five separate instances where a cell's `date` was not findable in that row's own cited `source` — one taken from an unrelated tool-deletion event, one from an unrelated venue closure, ones whose cited source carried no self-date at all. **Standing rule:** a `source` should be a record that self-dates its verdict — prefer a closure / scoping / ADR document over a `RESULTS.md` carrying only numbers.

   **Amendment (2026-07-26) — `P4` / `P5` / `P5-WEAK` added.** The rule is now mechanized to the extent it can be without semantics:

   - **`P4` (HARD)** — the source declares exactly one labelled verdict date and the cell disagrees. Fires on the real historical defect: a cell dated `2026-07-10` (the CFD-venue closure) citing `guardian/LOCK.md`, whose only labelled date is `2026-04-23`.
   - **`P5` (HARD)** — the source declares no labelled date *and* the cell's date appears nowhere in it — unverifiable as cited.
   - **`P5-WEAK` (NOTE, advisory, never changes the exit code)** — the source declares no verdict date at all; push toward one that self-dates.

   A NOTE is a correct resting state until the verdict gets a dated closure of its own; never repoint a cell at a record that merely shares the date to silence it.

   **What stays discipline-only, deliberately.** A multi-entry registry (`rejected_candidates.md`) gets the `P5` fallback but never `P4`: selecting *which* of its many dated entries a cell refers to needs semantics, which is precisely the join the status-consistency checker's `C1` was dropped for after scoring 100% false positives on real data. Anchor-only sources resolve to the ledger itself, take the `P5` fallback, and are exempt from the NOTE — a ledger row is not a decision artifact, so the note would fire on all 11 as noise. Net: the gate now closes the class where a date is **unverifiable** from its source; it does not close the class where a date is **plausible but wrong**, and that one still needs a reader.
2. **A missing `bars` entry silently under-reports.** Seeding initially missed the Treasury-complex tail-exhaustion bar (`treasury-complex-tail-exhaustion`, [`ZN.md`](../../ops/instruments/ZN.md) R1) on ZB/ZF/ZN — without it, a `cell` consult on any Treasury directional mechanism would have returned a clean "untested, proceed" on an instrument complex the ledgers themselves say needs its parent question reformulated, not a fourth directional construct. Fixed in-branch (`9d0b46c`) before this ADR landed, but the class of defect is real: `bars` are as load-bearing as `cells`, and nothing in P1/P2/P3 catches an *omitted* bar the way it catches a malformed one.
3. **Two mechanism classes recur in the corpus but are not yet in the vocabulary.** A calendar/day-of-week selection-gate class and a carry/term-structure class both surface repeatedly across ledgers without a matching `MECHANISMS.md` entry. They were deliberately **not** invented mid-seeding — inventing a class to make a seeding pass complete is exactly the judgment-call risk the growth rule (§2a) is designed to keep out of a routine pass. They are noted here as the first expected users of the `NEW` growth path the next time either recurs in an actual pre-registration.

---

## §10 — Audit hooks (runnable)

```bash
python scripts/instrument_profiles.py check
grep -n "rejected_candidates" scripts/instrument_profiles.py || echo "no reference — as designed"
```

---

## Addendum — 2026-08-29

**Does not amend §2a's closed verdict vocabulary, the value-carrying rule, P1–P5, or §5's forbidden moves.**

**(a) — verdict-label-to-precondition binding (P6/P7).** Two same-day incidents showed a cell's
verdict label can be asserted past what its own cited source actually demonstrates: two MYM cells
and both MNQ reconciliation cells sat `CONTINGENT-FORWARD` with no forward test actually running
(fixed `80585fd`/`0240ad9`); a MECHANISMS.md `INCREMENT` class finding stood on an uncomputed
within-stratum null-p until Codex review #207 caught it and forced `UNRESOLVED` (`bb97c9d`). This
extends the same provenance discipline the 2026-07-26 amendment applied to the `date` field
(§Execution notes item 1) to the verdict/class-finding label itself:

- **`P6` (HARD):** a `CONTINGENT-FORWARD` cell's cited `source` must resolve to a live/running
  forward-test registration — not a Pre-Q, a GRADUATE note, or a deferred pre-registration.
- **`P7` (HARD):** an `INCREMENT`-labeled class finding must cite a results artifact carrying a
  computed null-p field — a bootstrap CI alone does not satisfy this.

Both are directed at `scripts/instrument_profiles.py check`; **not implemented by this addendum** —
record + direction now, mechanization later, the same sequencing P4/P5 followed.

**(b) — structured authoring not authorized.** Prose extraction broke on four soft-wrap shapes on 2026-08-29 (#196/#197/#198/#203), each fixed same-day. Inverting §2a's authoring direction (structured front-matter, prose rendered from it) is **not authorized here**: it needs a fresh admitting ADR (schema-replacement scope: PROFILE contract, value-carrying rule, vocabulary-growth rule), not a further amendment to this one.
