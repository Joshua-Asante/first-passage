# ADR 2026-07-25 — Instrument-profile index: mechanism × instrument verdict view + intake consult

**Status:** Accepted
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Decision date:** 2026-07-25
**Authors:** Joshua (ratification) + Claude Code (design + build, Tasks 1-10)
**Supersedes:** none
**Related:** [`docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md`](2026-06-11-instrument-ledger-and-cfg-fingerprint.md) (parent decision — homes the ledgers this project indexes; §5 backfill rule this ADR scopes an override against; template for this ADR's shape) · [`docs/superpowers/specs/2026-07-25-instrument-profiles-design.md`](../superpowers/specs/2026-07-25-instrument-profiles-design.md) (design doc this ADR records) · [`docs/operational_rules.md`](../operational_rules.md) Rule 10 (amended one clause by this ADR) · [`docs/methodology/strategy_harvest.md`](../methodology/strategy_harvest.md) §1 (amended one requirement by this ADR) · [`docs/superpowers/specs/2026-07-16-status-consistency-checker-design.md`](../superpowers/specs/2026-07-16-status-consistency-checker-design.md) (C1 lesson this design inherits as a hard constraint)
**Layer:** governance / infrastructure (R&D session tooling) — does not touch strategy code, allocations, `dd_protection`, Pine, or vendor panels

---

## §0 — Rule 0 reads (production-source verification)

Read before authoring, in this session, at worktree HEAD `171c7d0` (== `origin/main` at authoring time; `git log HEAD..origin/main` and `git log origin/main..HEAD` both empty, 2026-07-25):

- [`docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md`](2026-06-11-instrument-ledger-and-cfg-fingerprint.md) — the direct parent decision. Confirms: §5 forbids pre-emptive ledger backfill; the 2026-07-16 addendum is the ratified scoped-override precedent this ADR's §2c copies the shape of; §6/§10's Consequences/Audit-hooks layout is the template this ADR follows.
- [`docs/superpowers/specs/2026-07-25-instrument-profiles-design.md`](../superpowers/specs/2026-07-25-instrument-profiles-design.md) — the design this ADR ratifies into governance. §3 (schema), §3.2 (the two asymmetries), §6 (intake checker + the C1 lesson), §7 (seeding-pass override scope), and §9 (falsifier, quoted verbatim below) are load-bearing.
- [`docs/operational_rules.md`](../operational_rules.md) Rule 10 (current text at HEAD, pre-amendment) — confirms the section this ADR appends a clause to, and that the append point (after the "Boundaries" bullet list) does not collide with the existing Phase-0 cost-geometry pre-gate clause that follows it.
- [`docs/methodology/strategy_harvest.md`](../methodology/strategy_harvest.md) §1 (current text at HEAD) — confirms the five-requirement admission table this ADR appends a sixth, differently-shaped item after; confirms requirement 3 already cites `discovery_manifests/` (repo-root), not `docs/discovery_manifests/` — a parallel session's fix, already merged, left untouched by this ADR.
- [`docs/superpowers/specs/2026-07-16-status-consistency-checker-design.md`](../superpowers/specs/2026-07-16-status-consistency-checker-design.md) §Addendum (2026-07-16) — confirms the exact C1 finding this design's §5 forbidden-moves clause inherits: the designed slug-join from `rejected_candidates.md` to CATALOG status fell to **100% false positives** on its first real run and was dropped, not softened.
- [`scripts/instrument_profiles.py`](../../scripts/instrument_profiles.py) — the tooling actually landed by Tasks 1-9 (single consolidated script, `build`/`check`/`cell` subcommands), read to confirm §10's audit hooks and §7's implementation description match what is on disk rather than the design doc's three-script sketch.
- [`ops/instruments/MYM.md`](../../ops/instruments/MYM.md), [`ops/instruments/ZN.md`](../../ops/instruments/ZN.md), [`ops/instruments/MECHANISMS.md`](../../ops/instruments/MECHANISMS.md) — worked PROFILE block, the Treasury tail-exhaustion bar (R1) referenced in §Execution-notes below, and the 15-entry seeded vocabulary.
- `tests/test_instrument_profiles.py` — 51 tests, synthetic `tmp_path` fixtures only (no dependence on live ledger content, per the repo's fixture-test discipline).

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

**What this override permits:** adding a derived-index `## PROFILE (machine-readable)` block (or the `no-profile` marker) to `ops/instruments/*.md` ledgers that **already exist**. Every seeded cell traces to an existing ledger row or closure — the pass is a re-indexing of committed findings, not an adjudication; a finding whose class is genuinely ambiguous was seeded at the grain the prose supports, or left out with the omission noted, never resolved by the seeding session's own judgment (design doc §7, "no new research claims").

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

**Downstream artifacts (this commit):**
- [`docs/adr/2026-07-25-instrument-profile-index.md`](2026-07-25-instrument-profile-index.md) — this ADR, placed.
- [`docs/operational_rules.md`](../operational_rules.md) Rule 10 — profile-block clause appended after the "Boundaries" bullet list.
- [`docs/methodology/strategy_harvest.md`](../methodology/strategy_harvest.md) §1 — profile-consult requirement appended after the five-requirement admission table.
- [`docs/adr/INDEX.md`](INDEX.md) — regenerated (`check_adr_graph.py --regenerate-index`) to include this ADR's header row.

**Already landed (Tasks 1-9, this branch, prior commits — recorded, not re-done here):** `ops/instruments/MECHANISMS.md`; PROFILE blocks in all 21 substantive `ops/instruments/*.md` ledgers + the `no-profile` marker on `US500.md`; `ops/instruments/PROFILES.md` + `profiles.json` (generated); `scripts/instrument_profiles.py` (`build`/`check`/`cell`); `tests/test_instrument_profiles.py` (51 tests); the gate 11 wiring in `scripts/githooks/pre-commit`, `Makefile`, and CI.

---

## §7 — Implementation plan

- **Phase 0 (Tasks 1-9, prior commits on this branch)** — schema design, taxonomy seeding, builder + gate + consult tooling, 21-ledger seeding pass, pre-commit/Makefile/CI wiring, test suite. Complete before this task opened.
- **Phase 1 (this task)** — governance record: this ADR; the Rule 10 clause; the `strategy_harvest.md` §1 amendment; `docs/adr/INDEX.md` regeneration; verification (§10 below) and commit.

**Implementation-vs-design divergence, noted for the record:** the design doc's §4/§5/§6 sketch three separate scripts (`build_instrument_profiles.py`, `check_instrument_profiles.py`, `check_candidate_cell.py`); Tasks 1-9 landed one consolidated script, `scripts/instrument_profiles.py`, with `build`/`check`/`cell` subcommands. This ADR governs the landed shape; the design doc's script names are historical intent, not the audit-hook surface (§10 below uses the real path).

**Not implemented (deliberately, per design doc §10 "Out of scope"):** parsing verdicts out of ledger prose (Approach C, §3 above); auto-generating `structure` rows from closure documents; any semantic join to `rejected_candidates.md` or `lab/CATALOG.md` (§5 above); backfilling ledgers for un-ledgered instruments (§2b); machine-verifying the `cost_hurdle` value against its prose row (§2a, named limitation); a profile surface for firms/venues rather than instruments.

---

## Execution notes — what building this taught (2026-07-25)

Three findings surfaced during Tasks 1-9's build and seeding pass that belong in the permanent record, not just the PR history:

1. **Date provenance was the weak point; it is now PARTIALLY gated.** Review caught five separate instances where a cell's `date` was not findable in that row's own cited `source` — one taken from an unrelated tool-deletion event, one from an unrelated venue closure, ones whose cited source carried no self-date at all. **Standing rule:** a `source` should be a record that self-dates its verdict — prefer a closure / scoping / ADR document over a `RESULTS.md` carrying only numbers.

   **Amendment (2026-07-26) — `P4` / `P5` / `P5-WEAK` added.** The rule is now mechanized to the extent it can be without semantics:

   - **`P4` (HARD)** — the source declares exactly one labelled verdict date and the cell disagrees. Fires on the real historical defect: a cell dated `2026-07-10` (the CFD-venue closure) citing `guardian/LOCK.md`, whose only labelled date is `2026-04-23`.
   - **`P5` (HARD)** — the source declares no labelled date *and* the cell's date appears nowhere in it — unverifiable as cited.
   - **`P5-WEAK` (NOTE, advisory, never changes the exit code)** — the source declares no verdict date at all; push toward one that self-dates.

   Measured on all 47 cells: **0 P4, 0 P5, 5 NOTE.** Sources decompose as **26 one-labelled-date (all matching, fully P4-checked)**, 5 unlabelled, 5 multi-label registries, 11 anchor-only.

   **Advisory sweep (2026-07-26).** The nine NOTEs the check first surfaced were worked down to five, two ways. Widening the label pattern to accept a date anywhere on the label's own line — this repo also writes `**Status:** CLOSED — FALSIFIED 2026-07-21`, a genuine self-dated verdict with prose between label and date — converted two cells to fully-checked and fired **zero** new P4s. Two more were repointed at records that actually own and self-date their verdict: MYM `event-window-reversal` from an undated `RESULTS.md` to [`MYM-3FPS-1-closure-falsified.md`](../briefs/closures/MYM-3FPS-1-closure-falsified.md), and MYM `venue-transfer` from the sibling `YM.md` ledger to the prototype `RESULTS.md` that YM's own cell already cites.

   The remaining five are **left as NOTEs deliberately**: MNQ/NQ `opening-range-breakout`, MYM `trend-following`, SPX500 `opening-range-breakout`, USDCAD `band-pierce-continuation`. A repo-wide search for any record self-dating those verdict dates found none that owns the verdict — the 2026-07-23 self-dating artifacts are c1 monitoring and cost-geometry decisions, not the ORB parking ruling; the 2026-06-22 ADR is NAS100 ORB, not SPX500. Forcing a repoint at a record that merely shares a date would be worse than the advisory: it would read as provenance while asserting a connection nobody checked. The NOTE is the correct resting state until one of those verdicts gets a dated closure of its own.

   **What stays discipline-only, deliberately.** A multi-entry registry (`rejected_candidates.md`) gets the `P5` fallback but never `P4`: selecting *which* of its many dated entries a cell refers to needs semantics, which is precisely the join the status-consistency checker's `C1` was dropped for after scoring 100% false positives on real data. Anchor-only sources resolve to the ledger itself, take the `P5` fallback, and are exempt from the NOTE — a ledger row is not a decision artifact, so the note would fire on all 11 as noise. Net: the gate now closes the class where a date is **unverifiable** from its source; it does not close the class where a date is **plausible but wrong**, and that one still needs a reader.

   Note the pattern detail that cost a full measurement round: this repo writes `**Closed:** 2026-07-21` with the colon **inside** the bold. A pattern expecting `**Closed**:` matches almost nothing and silently disarms the check.
2. **A missing `bars` entry silently under-reports.** Seeding initially missed the Treasury-complex tail-exhaustion bar (`treasury-complex-tail-exhaustion`, [`ZN.md`](../../ops/instruments/ZN.md) R1) on ZB/ZF/ZN — without it, a `cell` consult on any Treasury directional mechanism would have returned a clean "untested, proceed" on an instrument complex the ledgers themselves say needs its parent question reformulated, not a fourth directional construct. Fixed in-branch (`9d0b46c`) before this ADR landed, but the class of defect is real: `bars` are as load-bearing as `cells`, and nothing in P1/P2/P3 catches an *omitted* bar the way it catches a malformed one.
3. **Two mechanism classes recur in the corpus but are not yet in the vocabulary.** A calendar/day-of-week selection-gate class and a carry/term-structure class both surface repeatedly across ledgers without a matching `MECHANISMS.md` entry. They were deliberately **not** invented mid-seeding — inventing a class to make a seeding pass complete is exactly the judgment-call risk the growth rule (§2a) is designed to keep out of a routine pass. They are noted here as the first expected users of the `NEW` growth path the next time either recurs in an actual pre-registration.

---

## §10 — Audit hooks (runnable)

```bash
# Core gate + wiring + vocabulary size (this task's brief hooks, verbatim)
python scripts/instrument_profiles.py check
grep -n "instrument_profiles" scripts/githooks/pre-commit Makefile
grep -c "^## " ops/instruments/MECHANISMS.md
```

```bash
# Rule 10 profile-block clause landed, pointing at this ADR
grep -n "Profile-block clause" docs/operational_rules.md

# strategy_harvest.md §1 profile-consult requirement landed, pointing at this ADR
grep -n "Profile consult" docs/methodology/strategy_harvest.md

# discovery_manifests/ citation NOT reverted by this task (parallel-session fix)
grep -n "discovery_manifests/" docs/methodology/strategy_harvest.md
```

```bash
# ADR well-formedness + lifecycle graph + root-doc link liveness
python scripts/check_brief.py docs/adr/2026-07-25-instrument-profile-index.md --type adr
python scripts/check_adr_graph.py
python scripts/check_root_doc_liveness.py
```

```bash
# No semantic join to rejected_candidates.md exists in the tooling (§5 forbidden move)
grep -n "rejected_candidates" scripts/instrument_profiles.py || echo "no reference — as designed"
```

---

## Verification

```bash
# Discipline check (mechanical) — repo-side checker
python scripts/check_brief.py docs/adr/2026-07-25-instrument-profile-index.md --type adr
# Expected: PASS

# Governance-tier gates
python scripts/check_root_doc_liveness.py
python scripts/check_adr_graph.py
# Expected: both OK

# Tooling gate + full test suite
python scripts/instrument_profiles.py check
python -m pytest tests/test_instrument_profiles.py -v
# Expected: exit 0; 51 passed

# Downstream artifact update verification (§6 list)
grep -q "instrument-profile-index" docs/adr/INDEX.md \
  && grep -q "Profile-block clause" docs/operational_rules.md \
  && grep -q "Profile consult" docs/methodology/strategy_harvest.md \
  && echo ALL-PLACED
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

**(b) — parser fragility record; structured-authoring floated as a future phase, not authorized
here.** Since ratification, the prose-extraction path (`MECHANISMS.md` definitions, `Class finding`
bullets) broke on four distinct soft-line-wrap shapes, each fixed same-day (2026-08-29):
definition-paragraph wrap (#196), annotated-bullet capture (#197), multi-bullet body wrap (#198),
bold-annotation-span wrap (#203). Each hardened the regex; none changed the underlying design —
prose is hand-authored, `PROFILES.md`/`profiles.json` are recovered from it by pattern-matching.
The same day, `REPO_MAP.md` §2.1 converted from hand-maintained prose to a live-source generator
(`f32d8cc`), eliminating that defect class structurally rather than patching it. **Considered as a
future phase, not authorized here:** inverting §2a's authoring direction — verdict/status/citation/
finding-text fields authored as structured front-matter, prose rendered from it — sequenced the way
the SSOT remediation program phases its own work, not attempted as one rewrite. Authorizing the
inversion itself needs a fresh admitting ADR (schema-replacement scope: the PROFILE-block contract,
the value-carrying rule, and the vocabulary-growth rule would all need re-authoring, then content
re-authored across 21+ ledgers and MECHANISMS.md), not a further amendment to this one.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-25 | Initial authoring; ratifies Tasks 1-9's shipped design (schema, value-carrying rule, vocabulary growth rule, intake consult, generated-view invariant), records the scoped §5 override for the 21-ledger seeding pass, copies the design doc §9 falsifier verbatim (incl. thin-sample clause), and records three execution findings (date provenance, missing-bar under-report, two unvocabularied mechanism classes). | Joshua + Claude Code |
| 2026-08-29 | Addendum: (a) P6/P7 verdict-label-to-precondition binding, directed not yet implemented; (b) parser-fragility record (4 same-day soft-wrap fixes) + structured-authoring floated as a future phase, not authorized here. | Claude Code |
