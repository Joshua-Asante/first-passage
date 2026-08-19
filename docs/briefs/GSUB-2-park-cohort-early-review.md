# GSUB-2 — Early-review pass over the GSUB-1 PARK cohort, first real persona-panel use

**Status:** `CLOSED` `RESOLVED-LOADBEARING` 2026-08-19 — all phases executed same day → both
nominations (b2, c1) ratified by Joshua →
[`closure`](closures/GSUB-2-closure-resolved-loadbearing.md) · records at
[`b2`](../pursuits/b2-striker-mym-reconstruction.md) / [`c1`](../pursuits/c1-q-xmem-1.md)
**Authored:** 2026-08-19
**Closed:** N/A
**Authors:** Claude Code (proposing office)
**Parent question:** N/A — second GRAND-tier pursuit-disposition pass, same lineage as GSUB-1
**Loop:** Inquire-style brief, GRAND-tier — closure gated on §4 (disposition-difference count),
same shape as GSUB-1
**Loop-of-Record:** GRAND — pursuit-domain dispositions, per
[GRAND-tier ADR](../adr/2026-08-09-grand-tier-quintessentials-binding.md) §2.4.
**D-S-A domain:** pursuit (dispositions only; no corpus-, system-, or meta-process-level D).
**Artifact path:** `docs/briefs/GSUB-2-park-cohort-early-review.md`

---

## §0 — Rule 0 reads (this worktree, 2026-08-19)

- `docs/pursuits/b1-aegis-6j-transfer-lane.md` — anchor `73a77f7` 2026-08-16.
- `docs/pursuits/b2-striker-mym-reconstruction.md` — anchor `027a729` 2026-08-14.
- `docs/pursuits/b3-orb-mnq-payability-line.md` — anchor `027a729` 2026-08-14.
- `docs/pursuits/b5-q-fundpol-1.md` — anchor `3c7ca2f` 2026-08-16 (renewed to 2027-02-08; read for
  completeness, out of this pass's scope — see §7 Phase 1 row).
- `docs/pursuits/b6-q-nas-ecr-1.md` — anchor `73a77f7` 2026-08-16.
- `docs/pursuits/b7-ict-line.md` — anchor `027a729` 2026-08-14.
- `docs/pursuits/c1-q-xmem-1.md` — anchor `027a729` 2026-08-14.
- `docs/pursuits/c3-q-tom-spx-1.md` — anchor `027a729` 2026-08-14.
- `docs/personas/ownership-map.md` (Layer 2 pursuit classification) — anchor `90fbc52` 2026-08-19.
- `docs/adr/2026-08-09-grand-tier-quintessentials-binding.md` (§2.3 lifecycle states, §2.3 permitted
  test discipline via GSUB-1 §7 Phase 2) — anchor `57d355e` 2026-08-19.
- `docs/briefs/GSUB-1-inventory-and-dispositions.md` (original PARK dispositions + tests applied) —
  anchor `bd283dd` 2026-08-16.
- `docs/adr/2026-08-19-loop-persona-hierarchy-review-panel.md` (just ratified this session — the
  review mechanism this brief's Phase 2.5 invokes) — anchor `66410ed` 2026-08-19.
- `CLAUDE.md` §Live-execution posture ("both Striker legs were withdrawn 2026-08-04 and stay
  barred") — anchor `66410ed` 2026-08-19.

Dispositions proposed before the inventory is complete are Rule-0 violations — suspect even if
right. All eight rows in §7 Phase 1 were read in full before any Phase 2 test was applied.

## §0.5 — Ambiguity halt (mandatory before Phase 2.5)

- **Whether "no live catalyst before the scheduled expiry" is itself a legitimate SUBTRACT ground**
  is not resolved by GSUB-1's own permitted-test list (§7 Phase 2 below) and is not this brief's
  call to settle unilaterally — it is surfaced as a **named new test candidate**, not applied as if
  already permitted, and the persona panel + operator are the ones who rule on its admissibility.
- **Whether elapsed additional dormancy (c1: 34 days since freeze, vs. the ~24 days GSUB-1 itself
  measured) is sufficient new evidence to escalate an already-applied permitted test** (outside
  Survive/resource bounds) from PARK to SUBTRACT is a judgment call surfaced for the panel, not
  assumed.

---

## §1 — Context & motivation

GSUB-1 (2026-08-09) parked eight pursuits, each with a 2026-11-08 expiry that converts to SUBTRACT
absent explicit operator renewal (ADR §2.3) — a self-executing mechanism already in place. This
pass does **not** exist because that mechanism is broken; it exists for two independent reasons:

1. **The persona-hierarchy panel needs its first real (non-rehearsal) GRAND-tier data point.** The
   design spec's own §13 rehearsal record explicitly could not count toward the panel's §4
   falsifier because it ran against an already-closed, already-ratified inventory (GSUB-1). A
   genuine pre-ratification GRAND review is the only thing that can produce that first data point,
   per the [persona-hierarchy ADR](../adr/2026-08-19-loop-persona-hierarchy-review-panel.md) §4 and
   the design spec's own §10.
2. **Some PARKs in the cohort show zero new evidence and a widening idle window**, which is exactly
   the accretion symptom the GRAND tier exists to catch (GRAND ADR §1.4) — waiting mechanically
   for 2026-11-08 is safe but not obviously better than an early, evidence-based look, provided that
   look stays inside GSUB-1's own permitted-test discipline (or transparently flags where it would
   need to go outside it).

---

## §2 — Prior art / lineage

- [GSUB-1 inventory + dispositions](GSUB-1-inventory-and-dispositions.md) — the eight PARK rows this
  pass re-examines, and the permitted/forbidden subtract-test list (§7 Phase 2) this pass inherits
  verbatim.
- [GRAND-tier ADR](../adr/2026-08-09-grand-tier-quintessentials-binding.md) — pursuit lifecycle
  states (§2.3), cadence (§2.6: binds to the quarterly gate, but does not bar an off-cycle review).
- [Persona-hierarchy ADR](../adr/2026-08-19-loop-persona-hierarchy-review-panel.md), ratified this
  session — the panel mechanism this brief's Phase 2.5 invokes for the first real time.
- No prior early-PARK-review pass exists (verified: `GSUB-2|early.*review|park.*cohort` grep over
  `docs/briefs/` and `STATE.md` returns only this brief).

---

## §3 — Question (GSUB-2, symptom-phrased)

**GSUB-2:** Of the eight pursuits GSUB-1 parked, which currently show a live path back to KEEP
before their named expiry, and which show no such path and no new evidence since 2026-08-09 —
and does independent persona-panel review change what the proposing session would have nominated
alone?

**Pre-Q gate:**
```
D: re-deriving each PARK's re-entry condition from memory — test: already captured verbatim in the
   ratified pursuit record; read fresh instead (§0)
S: eight rows collapsed to two buckets — "no change" (with the specific reason each survives) and
   "nominated for early disposition" (with the specific test, permitted or new-and-flagged)
A: a single table (§7 Phase 1/2) so any future re-read costs O(seconds), same convention as GSUB-1
```

---

## §4 — Falsifiable hypothesis

**H:** the persona panel's independent review (Phase 2.5) surfaces at least one confirmed finding —
a BLOCKER, a CRO hard-block, or a preserved dissent — that changes what this brief would have
recommended to Joshua without it (design spec §4/§10; persona-hierarchy ADR §4).

**If** H holds, this is the first real data point toward the persona-hierarchy ADR's own falsifier
(1 of the needed 3, tracked there — not re-tracked here). **If** the panel's synthesis confirms
this brief's nominations and rationale with zero material change, that is **also** a real (negative)
data point for the same falsifier, not a failed run of this brief. **If** the inventory or panel
cannot complete within budget, close `AMBIGUOUS` — capture why, respec; do not amend this gate
mid-run.

This brief's own disposition question (§6) is separate and unconditional on H: it closes
`RESOLVED-LOADBEARING` if ≥1 pursuit's disposition changes from PARK, `RESOLVED-CEREMONIAL`
otherwise — same shape as GSUB-1 §4, one tier down (pursuit-count, not ADR-tier).

---

## §5 — Forbidden moves (genuinely tempting)

- Treating "no live catalyst before 2026-11-08" as an already-permitted GSUB-1 test rather than
  surfacing it as new (§0.5) — smuggling a new test through as if it were old is exactly the
  laundering GSUB-1 §7 Phase 2 already forbids for other tests.
- Nominating a PARK for SUBTRACT because it is *convenient* to shrink the cohort before the
  quarterly gate, rather than because a specific test fires on specific evidence.
- Skipping the panel review (Phase 2.5) and taking this brief straight to Joshua — the whole point
  of running this pass now, rather than waiting for 2026-11-08, is to give the persona-hierarchy
  ADR's own falsifier a real (not rehearsal) data point; skipping the panel defeats that purpose.
- Reaching into any nominated pursuit's own content (e.g., re-litigating b2's Striker terminal-gate
  criteria, or c1's Q-XMEM-1 architecture) — this pass dispositions pursuits, it does not re-derive
  their internals.
- Converting a PARK to SUBTRACT to "tidy the cohort" without the re-entry armor clause (out-of-frame
  evidence + attached falsifier) GRAND ADR §2.3 requires for every SUBTRACT.
- Letting the panel's synthesis substitute for Joshua's own ratification — panels are advisory
  without exception (persona-hierarchy ADR §5, D5).

---

## §6 — Gate criteria (closure verdict) and return taxonomy

| Verdict | Trigger condition | Disposition (typed) |
|---|---|---|
| `RESOLVED-LOADBEARING` | ≥1 ratified disposition differs from PARK (i.e., an early SUBTRACT is ratified) | `INTEGRATE — docs/pursuits/ record updated; GSUB-1 row superseded, not silently edited` |
| `RESOLVED-CEREMONIAL` | zero ratified dispositions differ from PARK (all eight ride to 2026-11-08 as-is) | `INTEGRATE — no record changes; this brief itself is the audit trail that the early look was taken and found nothing to act on` |
| `AMBIGUOUS` | panel or inventory not completable within budget | `ITERATE — capture why, respec fresh; never amend this gate mid-run` |

Spawn/agent returns inside Phase 2.5 use the panel workflow's own taxonomy (BLOCKER / CONCERN / NIT
findings; CRO hard-block is binary).

**Budget:** one attended session for Phases 1–2.5; Phase 3 (Joshua's ratification) is a separate,
subsequent act — this brief does not presume its outcome.

---

## §7 — Execution plan

### Phase 1 — Inventory (the GSUB-1 PARK cohort, re-read fresh)

| Pursuit | Re-entry condition | Days idle (since last activity) | Structural blocker on re-entry? |
|---|---|---|---|
| b1 Aegis→6J | 6J seat opens in book composition (F3 unreachable, corrected 2026-08-16) | 21 (since 2026-07-29) | No — unallocated capacity, not a standing bar |
| b2 Striker MYM recon | candidate clears own lane's terminal gates AND a venue seat exists | ~40+ (idle since 2026-07) | **Yes** — both Striker legs withdrawn 2026-08-04, stay barred (CLAUDE.md), no scheduled review of that bar |
| b3 ORB-MNQ | new payability/cost-geometry evidence at an admissible venue | 16 (since 2026-08-03 re-park) | No — a3's live discovery pipeline can organically surface this |
| b5 Q-FUNDPOL-1 | out of scope — renewed 2026-08-16, new expiry 2027-02-08 | n/a | n/a |
| b6 Q-NAS-ECR-1 | live fills on a NAS100/MNQ-shaped leg | 7 (since 2026-08-12 occupancy release) | No — actively *closer* to re-entry, not further |
| b7 ICT line | operator affirmation → $0 bounded falsifier | n/a (bounded step, not a wait) | No — cheap reserved step, GSUB-1 already reasoned this out |
| c1 Q-XMEM-1 | a dated cross-surface-memory-invisibility incident | 34 (since 2026-07-16 freeze; T0 never begun) | No structural bar, but zero incidents and zero new evidence since GSUB-1's own PARK |
| c3 Q-TOM-SPX-1 | brief-reserved native-Pine confirmation run (already scoped) | n/a (bounded step; expiry converts to reserved formal DEAD, not generic SUBTRACT) | No — already has its own closure path |

### Phase 2 — Disposition proposals (test applied, per row)

| Pursuit | Proposal | Test applied |
|---|---|---|
| b1 | **No change — PARK stands** | No permitted test fires; re-entry is genuine unbounded-but-real optionality (6J capacity), not a dead precondition. |
| **b2** | **Nominate: SUBTRACT** | **New test, flagged per §0.5 (not GSUB-1-permitted as written):** re-entry is gated on a precondition (a Striker venue seat) that is itself barred by separate, undated standing doctrine (CLAUDE.md Live-execution posture) with no scheduled review before this pursuit's own 2026-11-08 expiry — waiting produces no new information between now and expiry. Re-entry armor if ratified: out-of-frame evidence = the Striker bar itself lifting (a CLAUDE.md posture change), attached falsifier = none exists yet at re-entry time — one is authored fresh, per GRAND ADR §2.3. |
| b3 | **No change — PARK stands** | No permitted test fires; a live sibling pipeline (a3) can organically produce the named re-entry evidence before expiry — not dead optionality. |
| b5 | **Out of scope** | Recently renewed (2026-08-16); no new evidence since. |
| b6 | **No change — PARK stands; flagged WATCH, not a candidate** | Steelmanned explicitly: this is the PARK *closest* to firing its own re-entry condition (occupancy released 2026-08-12), the opposite of a SUBTRACT candidate. |
| b7 | **No change — PARK stands** | GSUB-1's own reasoning already applies unchanged: a bounded, dated, $0 re-entry step exists — PARK, not SUBTRACT, is correct. |
| **c1** | **Nominate: SUBTRACT** | **Existing GSUB-1-permitted test, re-applied on updated evidence:** "outside current Survive/resource bounds" — the same test GSUB-1 itself used to justify this PARK (idle then: ~24 days incl. the 2026-07-16 freeze to 2026-08-09 ratification; idle now: 34 days, T0 still never begun, zero incidents against the named re-entry condition). No new evidence has accrued in either direction; only elapsed time has. Re-entry armor if ratified: out-of-frame evidence = a genuine dated cross-surface-memory-invisibility incident, attached falsifier = the same one already on record in the frozen 2026-07-16 design (`docs/briefs/Q-XMEM-1-cross-surface-memory-sidecar-pilot.md`). |
| c3 | **No change — PARK stands** | Already has its own reserved, bounded closure path (formal DEAD on expiry) — not a generic SUBTRACT question. |

**Two nominations, six no-changes, one out-of-scope.** Neither nomination is applied — both are
proposals for the panel (Phase 2.5) and Joshua (Phase 3) to accept, reject, or amend.

### Phase 2.5 — Persona-hierarchy panel review (first real, non-rehearsal use)

Convened via `Workflow({ name: "pre-ratification-adversarial-panel", args: { targetPath:
"docs/briefs/GSUB-2-park-cohort-early-review.md", tier: "GRAND", personas: ["cio", "coo"] } })`
(`cro` auto-added per the mandatory-GRAND-CRO rule). CIO covers b1/b2/b3/b6/b7/c3 (Front office, Head
of Research/Execution domains — per `docs/personas/ownership-map.md` Layer 2, all six rows are
Office=Front); COO covers c1 (Back office, Head of Engineering domain); CRO reviews every row
against the CLAUDE.md safety invariants regardless of domain, per design spec §4.
Precondition: this brief must be a committed, frozen artifact before the panel spawns (design spec
§6.1) — committed in the same commit as this brief's authoring, before Phase 2.5 runs.

> **Post-panel correction (2026-08-19):** the first real panel run confirmed a CONCERN (COO lens,
> unanimous) that c3 carried an active Phase 2 proposal but was absent from this coverage list —
> the omission above is fixed (c3 added to CIO's list). This is a coverage-table completeness fix
> only; it changes no disposition proposal, no test applied, and no nomination in §7 Phase 1/2.
> Not re-run through the panel — see the closure/synthesis record for why a re-run wasn't warranted
> for a routing-table correction that touches no substantive finding.

### Phase 3 — Operator ratification

User-gated per the D user-gate, extended one tier up (GRAND ADR §2.2, persona-hierarchy ADR D5):
Claude proposes (Phases 1–2.5), Joshua authorizes. The panel's synthesis is read alongside this
brief, never as a substitute for it.

### Phase 4 — Record (only on a disposition actually changing)

If either nomination is ratified: the corresponding `docs/pursuits/` record is updated in place
(Standing: PARK → SUBTRACT, re-entry armor clause added per GRAND ADR §2.3), and
`docs/briefs/GSUB-1-inventory-and-dispositions.md` gains a superseding note at the affected row
(never silently edited). If neither is ratified: no record changes; this brief is itself the audit
trail.

---

## §8 — Verdict pre-registration

§4/§6 have no tunable thresholds — the trigger is a disposition-difference count against PARK,
same shape as GSUB-1 §8. The commit that freezes this brief (before Phase 2.5 spawns) is the
pre-registration anchor.

---

## §9 — Closure record format

On verdict, the closure note lands at `docs/briefs/closures/GSUB-2-closure-<verdict>.md` (verdict ∈
`resolved-loadbearing | resolved-ceremonial | ambiguous`), carrying: the verdict vs the §6 table,
the panel synthesis (or a pointer to it), the disposition log, and the mandatory typed `## Iterate`
block. The persona-hierarchy ADR's own falsifier tracker is updated separately, there, not here.

---

## §10 — Audit hooks (runnable)

```bash
# Confirm this brief was frozen before the panel ran (design spec §6.1 precondition)
git log -1 --oneline -- docs/briefs/GSUB-2-park-cohort-early-review.md

# Confirm no other GSUB-2-shaped pass exists (dedup)
grep -rln "GSUB-2" docs/briefs/ docs/pursuits/ STATE.md 2>/dev/null

# Persona logs actually got the panel's verdict appended (design spec §12), once Phase 2.5 runs
grep -A3 "docs/briefs/GSUB-2" docs/personas/cio-log.md docs/personas/coo-log.md docs/personas/cro-log.md 2>/dev/null

# If b2 or c1 SUBTRACT is ratified: re-entry armor clause present on the updated pursuit record
grep -A2 "out-of-frame evidence" docs/pursuits/b2-striker-mym-reconstruction.md docs/pursuits/c1-q-xmem-1.md 2>/dev/null
```

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/GSUB-2-park-cohort-early-review.md --type inquire
# Expected: RESULT: well-formed

# Rule-0 anchor spot-check (matches §0 above)
git log -1 -- docs/pursuits/b2-striker-mym-reconstruction.md   # expect 027a729 or later
git log -1 -- docs/pursuits/c1-q-xmem-1.md                     # expect 027a729 or later
git log -1 -- docs/adr/2026-08-19-loop-persona-hierarchy-review-panel.md  # expect 66410ed or later
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-19 | Initial authoring — Phase 1 inventory + Phase 2 disposition proposals for the eight GSUB-1 PARK pursuits; two nominations (b2, c1) surfaced for Phase 2.5 persona-panel review. | Claude Code |
| 2026-08-19 | Phase 2.5 executed — first real (non-rehearsal) persona-hierarchy panel review (CIO + COO + CRO, per `docs/adr/2026-08-19-loop-persona-hierarchy-review-panel.md`). Verdict `CLEAR-WITH-CONCERNS`: no CRO hard-block; two BLOCKER claims (CIO/COO domain-routing scope) raised and both unanimously refuted by independent skeptics; one CONCERN (c3 missing from the Phase 2.5 coverage table) confirmed unanimously and fixed in place. Neither SUBTRACT nomination's substance (b2, c1) was challenged by any surviving finding. Persona logs appended per design spec §12. Phase 3 (operator ratification) still owed — this brief does not execute either nomination. | Claude Code |
