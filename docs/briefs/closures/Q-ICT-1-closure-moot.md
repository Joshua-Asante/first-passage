# Q-ICT-1 — closure: MOOT (premise refuted by production)

**Type:** Inquire-phase brief (Pre-Q) — **never executed**
**Opened:** 2026-07-24 (DRAFT) · **Closed:** 2026-07-24 · **Verdict:** `MOOT`
**Corpus resolved to:** `lab/archive/ict_cascade_2026-06-18/` (the brief's §0 row 1 "path TBD")

## Why MOOT (not FALSIFIED, not AMBIGUOUS)

Q-ICT-1's single question was: *"What is the probability that the observed W/D-over-LTF advantage arises from a zero-edge panel under best-of-4 selection?"* — predicated (§1 evidentiary problem) on the W/D residual **never having been gated** and having **no multiplicity accounting**.

Both predicates are false against the corpus, so the question dissolves before its gate can run:

- **W was gated to RESOLVED under its own pre-registration** — structure-only 0.5571, moving-block-CI [0.5242, 0.5901] lb>0.50, stationary halves/thirds, eff_N 910, and its **own best-of-K** (4-vote max-stat label-permutation, B=10000) — `PREREG-W.md`, `TEST_PLAN.md` cont.7, `CLOSURE-1M-INSUFFICIENT-N.md` §4.
- **Multiplicity was booked** — joint family **M=65** (`DSR_PBO_LEDGER.md`), not "best-of-4."
- **The cascade is a sequential filter (W→D→1H→1M), not four parallel bets** — so "best-of-4 timeframe family" is the wrong denominator either way.

Running the brief's §4 best-of-K/permutation on the four timeframe expectancy vectors would therefore be a **fresh, coarser K=4 gate applied post-hoc to survivors that already cleared a stronger, pre-registered M=65 gate** — the garden-of-forking-paths re-entry the cascade's ledger was built to prevent, and a DUPLICATE of a closed verdict. It must not run. `MOOT` (the question's premise is void), not `FALSIFIED` (which would wrongly imply the residual was tested here and failed).

## What survives (named, not opened — parent-Q convention)

- **The only real forward thread** is the one the cascade itself flagged: **W-RESOLVED and D-SSL-RESOLVED are single-instrument (US500), mostly-single-regime** and route to *path-independent confirmation on an independent instrument/period* (`CLOSURE-1M-INSUFFICIENT-N.md` §4/§5). This is **"confirm a RESOLVED belt finding on independent data,"** a different question with a different method than "gate an ungated residual." It is **low priority**: the cascade found no deployable edge, and the 1M execution layer is un-runnable on the canonical 1m feed (0/247 fills; F8 multi-regime-1m wall). Do not open without a data-procurement justification.
- **Q-ARCH-1 (instrument-first architecture) stays closed.** Per the brief's own §4 otherwise-clause, a non-`RESOLVED-REAL` Q-ICT-1 means Q-ARCH-1 "must find independent motivation or stay closed." The W/D residual cannot motivate a research re-architecture — it is already-gated, non-deployable, single-panel. Q-ARCH-2 stays closed downstream.

## What the brief got right (retained, independent of the verdict)

- **F2 is correctly grounded.** ORB-MNQ-1 pre-reg §5 (`docs/briefs/pre-registration/2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md`) does forbid reopening the Friday / GEX / T10Y3M conditioning slices; routing them into an MNQ ledger edge tier would be that forbidden amendment relabeled. If an MNQ descriptive ledger is ever built, that guard stands.
- **The MNQ descriptive-tier ledger (§9.2)** is an independent, ORB-MNQ-scoped task — unaffected by this disposition and neither blocked nor advanced by it.

## Corrected citations (for any successor artifact)

- Real test implementations: `lab/research_utils/step0_battery.py`, `lab/research_utils/selection_tests.py`, `lab/research_utils/permutation.py` — **not** `scripts/…` (the brief's §0/§10 paths are wrong).
- Gate-audit governance: INQHIORI §6.2 (trigger + write-target), §4/§5 — **not** §12 (Cross-references).
- Companion: `docs/notes/audits/2026-07-24_gate_composite-closure-deletion.md` (corrected — worked example retracted).
