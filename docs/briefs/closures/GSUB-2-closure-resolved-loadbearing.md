# GSUB-2 — CLOSURE: `RESOLVED-LOADBEARING` (2 ratified dispositions differ from PARK)

**Verdict:** `RESOLVED-LOADBEARING`
**Closed:** 2026-08-19
**Lane:** UNASSIGNED
**Pre-registration:** §4/§6 gate frozen in
[`GSUB-2-park-cohort-early-review.md`](../programs/GSUB-2-park-cohort-early-review.md) §4/§8 — anchor commit
`ea087cc` (the commit that froze the brief, before Phase 2.5 spawned)
**Successor:** none authored — the six unchanged PARKs ride to their pre-registered 2026-11-08
expiry as-is; no new Q or pursuit opened
**Spend / K:** $0.00 · K consumed: 0
**Live effect:** none on any live-risk surface (CRO's own independent review confirmed no row
touches `dry_run`, `armed_until`, M1 status, any locked strategy's authorization multiplier, or
`DD_TRIGGER`/`DD_SCALE`). Effect is governance-layer only: 2 pursuit records flipped PARK→SUBTRACT,
1 Q-roster row closed, 2 superseding notes added to the GSUB-1 inventory (never silently edited).
**Artifacts:** [`GSUB-2 brief`](../programs/GSUB-2-park-cohort-early-review.md) ·
[`b2 pursuit record`](../../pursuits/b2-striker-mym-reconstruction.md) ·
[`c1 pursuit record`](../../pursuits/c1-q-xmem-1.md) ·
[`Q-XMEM-1 closure`](Q-XMEM-1-closure-subtract.md) ·
persona logs (`cio-log.md`, `coo-log.md`, `cro-log.md`, 2026-08-19 entries — docs/personas/ deleted 2026-08-31, see [retirement ADR](../../adr/2026-08-31-persona-hierarchy-full-retirement.md))

---

## 1. Verdict (§6 asserted against actual numbers)

Every pre-registered §6 route walked, not only the one that fired:

| §6 route | Trigger (frozen) | Actual | Fired? |
|---|---|---|---|
| `RESOLVED-LOADBEARING` | ≥1 ratified disposition differs from PARK | **2** ratified differences (b2, c1 → SUBTRACT) | ✓ |
| `RESOLVED-CEREMONIAL` | zero ratified dispositions differ from PARK | 2 ≠ 0 | — |
| `AMBIGUOUS` | panel or inventory not completable within budget | Phase 1–3 completed in-session | — |

**Phase 2.5 (persona panel, first real non-rehearsal use):** CIO + COO + CRO independently
reviewed the frozen brief. Verdict `CLEAR-WITH-CONCERNS` — no CRO hard-block, no confirmed
BLOCKER (two BLOCKER-severity domain-routing-scope claims raised, both unanimously refuted by
independent skeptics), one CONCERN confirmed (c3 missing from the Phase 2.5 coverage table) and
fixed in place before Phase 3. Full synthesis: workflow run `wf_e016a5d9-3f6`.

**Operator ratification (Phase 3):** 2026-08-19, in-session — both nominations ratified
individually (`Ratify SUBTRACT` selected for b2 and for c1, each after being shown the panel's
finding that nothing survived to undermine either nomination). Authority channel: the D user-gate
extended one tier up (GRAND ADR §2.2 / canon L282), same channel GSUB-1 used.

**Against the persona-hierarchy ADR's own §4 falsifier:** this is real data point 1 of the needed
3. H did not fire in the strong sense (no confirmed BLOCKER or CRO hard-block changed a
disposition) — but the panel's confirmed CONCERN (c3 coverage gap) is itself a real,
ratification-relevant correction that would not have existed without the panel, and is logged as
such in the ADR's own tracking, not re-tracked here.

## 2. What the pre-registration predicted vs what happened

§0.5 flagged two judgment calls up front: whether "no live catalyst before expiry" is a
legitimate SUBTRACT ground (new test, not GSUB-1-permitted as written), and whether elapsed
dormancy alone can escalate an already-applied permitted test. Both were surfaced transparently
rather than smuggled in, and both survived panel review unchallenged on their substance — the
panel's actual finding was a **routing-table completeness gap** (c3), not a challenge to either
test's legitimacy. That is a narrower defect than either §0.5 ambiguity anticipated, which is
itself informative: the panel caught a mechanical gap in *this* brief's own execution of the
persona-hierarchy mechanism, not a flaw in the underlying disposition reasoning.

## 3. What this closure does NOT license

- **It does not license any lower-tier change.** No strategy parameter, allocation,
  `dd_protection` constant, MC calibration, locked Pine, campaign pre-registration, or arming
  state was touched (GRAND ADR §2.2 downward interface: scoping authority only — independently
  confirmed by CRO's own clean review).
- **It does not re-verdict Q-XMEM-1's own investigation history.** The 2026-08-15 `ASSISTIVE-ONLY`
  Limb B measurement stands unchanged; c1's SUBTRACT dispositions the *pursuit* (whether standing
  exploration continues), not the measurement (see c1 pursuit record and the Q-XMEM-1 closure).
- **It does not bar Striker legs, Striker research, or the locked Striker book's current
  authorization.** b2's SUBTRACT is specific to the MYM reconstruction candidate's own research
  lane (see b2 pursuit record).
- **It does not disposition the six unchanged rows differently than GSUB-1 already did.** b1, b3,
  b6, b7, c3 remain PARK exactly as GSUB-1 ratified; b5 remains out of scope (already renewed).
  Their 2026-11-08 expiry is untouched.
- **It does not perform the named lab-archival follow-up** for b2's residual CATALOG body — see
  the Iterate block.

## 4. Defects found in the frozen brief (recorded, not repaired in the frozen text)

1. **§7 Phase 2.5 coverage table omitted c3** despite c3 carrying an active Phase 2 proposal on
   the same office/primary-owner basis used to route b1/b3/b6/b7 to CIO. Found by the COO lens,
   confirmed unanimously by both independent skeptics. **Corrected in place** in the GSUB-2 brief
   (post-panel addendum, same commit as the persona-log entries) rather than left as a recorded
   gap only — a coverage-table completeness fix is mechanical, not a re-litigation of any
   disposition, so the ordinary "record defects, don't repair the frozen text" convention does not
   apply here the way it does to a substantive finding.
2. **`check_brief.py`, run without an explicit `--type` flag (as the panel's Form Check stage
   does), auto-detected this brief as `type=handoff` and returned `MALFORMED`** — a false positive;
   the same file passes clean under its own documented `--type inquire`. Recorded as a tooling
   defect, not repaired here (out of this closure's scope); flagged as a standalone follow-up task.

## 5. Lesson candidates

- **Candidate (below the two-incident bar — watch):** *a panel's own routing table is itself a
  testable claim, not just scaffolding.* The persona-hierarchy mechanism's first real use caught a
  defect in the review's own coverage, not in the underlying content — a useful early signal that
  the independence mechanic works as designed (COO's own domain-adjacent lens caught what CIO's
  and CRO's reviews did not), but also a reminder that Phase 2.5 routing tables need the same
  Rule-0 rigor as any other claim in a brief. One incident, $0 cost (caught pre-ratification).
  Watch for a second firing before promoting to a standing brief-authoring check.

## Iterate — loop exit

- **Verdict used:** `RESOLVED-LOADBEARING`
- **Model update:** an early, off-cycle GRAND review (rather than waiting for the 2026-11-08
  quarterly gate) can find real dispositions *and* give the persona-hierarchy panel a genuine
  pre-ratification data point at the same time — the two purposes named in GSUB-2 §1 were not in
  tension. The panel's value showed up as mechanism-quality-control (the c3 gap) rather than as a
  challenge to either SUBTRACT's substance, which is itself informative for how future panel runs
  should be read: a CLEAR-WITH-CONCERNS-with-fixed-CONCERN outcome is a legitimate, useful result,
  not a null one.
- **Next:** INTEGRATE
- **Routing:** INTEGRATE → (a) 2 pursuit records flipped PARK→SUBTRACT with re-entry armor
  (`b2`, `c1`); (b) GSUB-1 inventory gains 2 superseding notes (never silently edited); (c)
  Q-XMEM-1 Q-roster row closed with its own closure stub; (d) 3 persona logs gain their first
  real (non-rehearsal) entries; (e) STATE decision index gains a 2026-08-19 line.
- **Entry packet:** n/a — INTEGRATE
- **Stop rule / re-proposal bar:** n/a for the SUBTRACTs themselves (integrated; re-entry armor is
  on each pursuit record, not a re-proposal bar on this run). For the unrepaired `check_brief.py`
  type-detection defect: re-proposal is simply fixing the auto-detect heuristic, tracked as a
  standalone spawned task (not this closure's obligation).
- **Board write:** STATE decision index gains one 2026-08-19 line (see below); no forward-trigger
  row needed (the persona-hierarchy ADR's own §4 tracking absorbs this run as data point 1/3,
  tracked on that ADR, not duplicated here).
- **Registry:** n/a — a GRAND-tier pursuit-disposition run, not a rejected trading-strategy or
  signal-mechanism candidate; `docs/rejected_candidates.md` tracks strategy/mechanism rejections
  only (Rule 8 sub-rule 9 scope).

## §10 audit-hook discharge

```bash
$ grep -A2 "out-of-frame evidence" docs/pursuits/b2-striker-mym-reconstruction.md docs/pursuits/c1-q-xmem-1.md
(both present)
$ grep -A3 "docs/briefs/programs/GSUB-2" docs/personas/cio-log.md docs/personas/coo-log.md docs/personas/cro-log.md
(all three present, 2026-08-19 entries)
$ grep -c "superseded 2026-08-19" docs/briefs/programs/GSUB-1-inventory-and-dispositions.md
2
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-19 | Closure authored at Phase-4 completion, following Phase 3 operator ratification of both nominations | Joshua (ratification) + Claude Code (execution) |
