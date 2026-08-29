# SSOT Phase 3 — Cost-model closed-world partition

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax.
>
> **Authorization:** addendum on
> [`docs/adr/2026-08-27-ssot-data-lineage-remediation-program.md`](../../adr/2026-08-27-ssot-data-lineage-remediation-program.md)
> (limb-4: new path-conditional gate). Parent program plan
> [`2026-08-27-ssot-data-lineage-remediation.md`](2026-08-27-ssot-data-lineage-remediation.md)
> named this phase and refused bite-sized steps until recon (a)(b)(c) landed. This file
> is that scoped plan. **$0 / K=0.**
>
> **Queue:** off the live operator table (`#1` strategy · `#2` B7/M1). Implementation
> is `queue-exception: operator GO on the attached Phase 3 plan`. Do not open a
> STATE queue row.

**Goal:** Keep `lab/discovery/cost_model.py`'s three instrument sets a declared
partition so the next `INSTRUMENT_SPECS` add cannot land unclassified. Void a
bars prose-parser. Do not join ledgers. Do not add `firm_rules` commission
dollars. Do not rewrite harvest gate-2 FAIL policy.

**Parent:** SSOT/data-lineage remediation program. This is the **program** Phase 3,
not the parent ADR's §7 verification-block "Phase 3" (operator GO on the 2026-08-27
ratification).

---

## Recon (answered 2026-08-29, this worktree, `origin/main` @ `d276076`)

**(a) Do the two cited gaps still exist as described?**

- **Bars (partially stale).** [`2026-07-25-instrument-profile-index.md`](../../adr/2026-07-25-instrument-profile-index.md)
  §Risks / Execution-notes still names the *class*: P1–P3 catch malformed `bars`,
  not an omitted one. The Treasury instance is already fixed (ZN/ZB/ZF each declare
  `treasury-complex-tail-exhaustion` with `family: []`). Inheritance cannot model
  that complex. A prose-only bar is invisible by construction. The 2026-08-12 MSL
  note that “MGC emits zero bars” is stale — `MGC.md` now carries a bar. Empty
  `bars` on some ledgers remains legal.
- **Commission closed-world (still live, wider than cited).**
  `resolve_commission` still resolves only the index-micro set and raises for
  everything else — intentional. Q-CAPBAND-1 §4.2 is still true for harvest gate 2.
  What changed: `INSTRUMENT_SPECS` grew; several keys raise via the catch-all and
  are not in `NO_COMMISSION_ROW_INSTRUMENTS`. The named set drifted from the table
  it claims to document.

```
$ git log --oneline -1 -- lab/discovery/cost_model.py
027a729 Initial public release
```

**(b) Is there a fourth closed-world hole?** The live hole is intra-`cost_model`:
`INSTRUMENT_SPECS` ⊈ `INDEX_MICRO ∪ NO_COMMISSION`. Q-TNEC-ENV-1 (missing cell /
once-missing M6A ledger) is a different class — do not fold. D4 / M1 stay on
their owners. Ledger-symbol ⋈ SPECS is the **wrong** join (many ledgers are
CFD/retired/research-only and unpriced by design).

**(c) Is a shared schema / harvest rewrite cheaper?** No. Bars prose→YAML repeats
Approach C / C1. Adding commission rows touches `firm_rules.py`. Making gate 2
FAIL on “no row” is harvest-policy. Cheapest honest check: declare the partition
the raise already implements, then gate it.

Amendment-first (sub-rule 10): owner is the parent program ADR. `rg` against
`lab/CATALOG.md`, `docs/briefs/INDEX.md`, `docs/rejected_candidates.md` for
`closed-world|ssot-phase-3|check_cost_model` — CATALOG empty; INDEX owns
Q-CAPBAND-1 as a closed Cap counterfactual; rejected_candidates empty. No new
ADR file.

---

## Design

**Void the bars checker in this packet.** Class stays on the 2026-07-25 ADR Risks
line (review discipline; no semantic join).

**Build a cost-model closed-world invariant** as
`cost_model.closed_world_findings()` + thin
`scripts/check_cost_model_closed_world.py` (classified **lab** so the
`discovery.cost_model` import is a legal lab→lab edge):

1. `INDEX_MICRO_COMMISSION_INSTRUMENTS ⊆ INSTRUMENT_SPECS`
2. `INSTRUMENT_SPECS ⊆ INDEX_MICRO ∪ NO_COMMISSION`
3. `INDEX_MICRO ∩ NO_COMMISSION = ∅`

Classify the undeclared SPECS keys into `NO_COMMISSION_ROW_INSTRUMENTS`.
Behavior is unchanged: they already raise. Do not add MCL / 6J / 6E / M6E to
SPECS. Mutation-test a fake SPECS key in neither set before binding
`gates.yml` (path-conditional on `lab/discovery/cost_model.py`). Do not put
this on `make validate`.

**Out of this packet:** D4 21.4%; M1 report-only; Phase 4; CATALOG /
rejection-register topology; harvest gate-2 FAIL policy; commission dollars;
Pine / `dd_protection.py` / `firm_rules.py` / allocations.

Queue succession: do **not** auto-open a STATE row when this ships.

---

## Global constraints (inherited)

No trade placement. Mutation-test the checker before trusting it. No hand-edit
of `docs/adr/INDEX.md` or `lab/CATALOG.md`. Retention test on any new artifact.

---

## Task 1: Author this plan + point the parent plan at it

**Files:**
- Create: this file
- Modify: [`2026-08-27-ssot-data-lineage-remediation.md`](2026-08-27-ssot-data-lineage-remediation.md) Phase 3 section

- [x] **Step 1:** Write this file with recon (a)(b)(c) pasted from live reads.
- [x] **Step 2:** Replace the parent plan's "scoped, not yet detailed" Phase 3
  stub with a pointer at this file. Do not delete the Phase 4 stub.
- [ ] **Step 3:** Commit.

```bash
git add docs/superpowers/plans/2026-08-29-ssot-phase-3-cost-model-closed-world.md \
        docs/superpowers/plans/2026-08-27-ssot-data-lineage-remediation.md
git commit -m "docs(plan): scope SSOT Phase 3 cost-model closed-world check"
```

---

## Task 2: Parent-ADR addendum (no STATE queue row)

**Files:**
- Modify: `docs/adr/2026-08-27-ssot-data-lineage-remediation-program.md`
- Modify: `STATE.md` (decision-index one-liner + keep-15 roll only)

- [ ] **Step 1:** Addendum authorizing the partition check. Record recon
  (a)(b)(c). Void the bars checker. Forbid ledger join, `firm_rules` dollars,
  and harvest gate-2 rewrite. §10 hook:
  `python scripts/check_cost_model_closed_world.py`.
- [ ] **Step 2:** Decision-index line; keep-15 roll if needed. Do **not** add
  an operator-queue row.
- [ ] **Step 3:** `python scripts/check_brief.py docs/adr/2026-08-27-ssot-data-lineage-remediation-program.md --type adr`
  and `python scripts/check_adr_graph.py`. Do not hand-edit INDEX.
- [ ] **Step 4:** Commit.

---

## Task 3: TDD partition + classify

**Files:**
- Modify: `lab/discovery/cost_model.py`
- Modify: `tests/test_cost_model.py`
- Create: `scripts/check_cost_model_closed_world.py`
- Modify: `scripts/check_boundaries.py` + `scripts/repo_map_layers.yml` (lab classification)

- [ ] **Step 1: Failing tests first**
  - live partition after classification → clean
  - mutation: SPECS key in neither set → finding
  - mutation: INDEX_MICRO key missing from SPECS → finding
  - mutation: INDEX_MICRO ∩ NO_COMMISSION nonempty → finding
- [ ] **Step 2:** Classify undeclared SPECS keys; implement
  `closed_world_findings()` + thin CLI. Confirm tests green.
- [ ] **Step 3:** Live run **before** `gates.yml` bind:

```bash
python scripts/check_cost_model_closed_world.py
# Expected: exit 0
```

- [ ] **Step 4:** Commit.

---

## Task 4: gates.yml bind + hygiene

- [ ] **Step 1:** Path-conditional `gates.yml` entry on
  `lab/discovery/cost_model.py`. Update `tests/test_gate_manifest.py`
  (`EXPECTED_PATH_CONDITIONAL` + `REACHABILITY_PROBES`).
- [ ] **Step 2:** `python -m pytest tests/test_cost_model.py tests/test_gate_manifest.py -q`
- [ ] **Step 3:** Blast-radius on “Phase 3 … not yet detailed” / “does not
  authorize Phase 3” tokens. Leave historical SESSIONS / Phase 2 addendum
  “Does not authorize Phase 3” (Trap #12; new addendum is the GO).
- [ ] **Step 4:** `python scripts/roll_sessions.py --next-label 2026-08-29`
  then append a wrap-up citing remaining live queue rows (#1 · #2) plus
  `queue-exception`.
- [ ] **Step 5:** Commit.

---

## Forbidden moves

- Reopen CATALOG hot/disposition or rejection-register topology
- Touch Pine, `dd_protection.py`, `firm_rules.py`, allocations
- Join `ops/instruments/*.md` symbols to SPECS
- Parse ledger prose into `bars`
- Fold D4 21.4% or M1 report-only into this PR
- Auto-open a STATE operator-queue row
- Hand-edit `docs/adr/INDEX.md` or `lab/CATALOG.md`

---

## Verification

```bash
python scripts/check_cost_model_closed_world.py
python -m pytest tests/test_cost_model.py tests/test_gate_manifest.py -q
python scripts/check_brief.py docs/adr/2026-08-27-ssot-data-lineage-remediation-program.md --type adr
python scripts/check_adr_graph.py
python scripts/check_boundaries.py
python scripts/check_repo_map_layers.py
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-29 | Initial scoped plan; recon (a)(b)(c) answered against `origin/main` @ `d276076` | Cursor Cloud Agent |
