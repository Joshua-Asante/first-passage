# GSUB-1 — CLOSURE: `RESOLVED-LOADBEARING` (19 ratified dispositions differ from status quo)

**Verdict:** `RESOLVED-LOADBEARING`
**Closed:** 2026-08-09
**Pre-registration:** §4 gate frozen in [`GSUB-1-first-grand-subtract-pass.md`](../programs/GSUB-1-first-grand-subtract-pass.md) §4/§8 — anchor commit `c90746d` (the ratification commit; no separate pre-reg file, per §8 — the gate has no tunable thresholds)
**Successor:** none authored — the ADR's own §4 reading at 2026-11-08 is the next scheduled act, not a successor Q
**Spend / K:** $0.00 · K consumed: 0
**Live effect:** none on any live-risk surface (no strategy, allocation, `dd_protection`, Pine, rail, or arming state touched). Effect is governance-layer only: 37 pursuit records created; 3 user-level skill directories archived-then-removed; 1 Q-roster row closed; 1 retirements-record row flipped.
**Artifacts:** [`inventory + dispositions`](../programs/GSUB-1-inventory-and-dispositions.md) · [`docs/pursuits/`](../../pursuits/) (37 records) · [`archived skills`](../../ltm/notes/archive/skills/)

---

## 1. Verdict (§6 asserted against actual numbers)

Every pre-registered §6 route walked, not only the one that fired:

| §6 route | Trigger (frozen) | Actual | Fired? |
|---|---|---|---|
| `RESOLVED-LOADBEARING` | ≥1 ratified disposition differs from status-quo standing | **19** ratified differences (8 PARK · 9 SUBTRACT · 2 MERGE) | ✓ |
| `RESOLVED-CEREMONIAL` | zero ratified dispositions differ from status quo | 19 ≠ 0 | — |
| `AMBIGUOUS` | inventory not completable within the §6 budget | inventory completed in-session (37 rows, all five classes a–e) | — |

**Operator ratification (Phase 3):** 2026-08-09, in-session — *"these are good judgements. proceed
as recommended"* — a bulk ratification of the full Phase-2 proposal table, which the spec's Phase 3
explicitly permits ("Bulk options are legitimate"). Authority channel: the D user-gate extended one
tier up (ADR §2.2 / canon L282).

**The paired ADR's §4 reads off this:** ≥1 ratified difference ⇒ the GRAND tier is **load-bearing**;
the ADR holds and its sunset review does **not** arm. Recorded as an addendum on the ADR.

## 2. What the pre-registration predicted vs what happened

The §4 gate anticipated a binary and got a decisive one — 19 differences against a threshold of 1.
Three findings were **not** anticipated at pre-registration:

1. **Two long-pending decisions surfaced as unowned residuals, not as active pursuits.** The Notion
   estate's Phase-3 disposition (c6) had sat undecided through *two* quarterly audits with its own
   §4 hypothesis holding the whole time; Q-USOIL-1's park (b4) named an "08-08 revisit" whose board
   row was deleted at the Great Prune with no re-park. Neither was visible as accretion from any
   existing surface — both required the cross-surface inventory to see. This is the clearest
   evidence for the tier's load-bearingness.
2. **The meta-belt split into two very different classes on execution.** Three user-level skills
   were real, deletable directories (d4–d6, executed). Four `anthropic-skills:` entries (d7–d10)
   turned out to be **platform-bundled, not user-installed** — verified against
   `installed_plugins.json` (only `superpowers` + `hookify`), `known_marketplaces.json`, and the
   `cache/`/`marketplaces/` trees. No deletion path exists, so the pre-registered fallback
   (marker-only, §0.5 ruling 6) applied — not as a judgment call but as the only available action.
3. **The MERGE precondition failed as literally stated and had to be verified, not assumed.** d4's
   disposition said "verify-no-unique-content diff"; the diff came back **non-empty** on three
   files. Reading them showed every hunk was the repo copy being strictly *more* current (futures/c1
   scope, an added `check_futures_identity()`, and the repo copy's own history documenting the
   correction of "a stale claude.ai-side skill-copy anchor" — i.e. the very copy being merged). The
   disposition survived on inspection; it would have been wrong to execute on the label alone.

## 3. What this closure does NOT license

- **It does not license any lower-tier change.** No strategy parameter, allocation, `dd_protection`
  constant, MC calibration, locked Pine, campaign pre-registration, or arming state was touched or
  is authorized by this run (ADR §2.2 downward interface: scoping authority only).
- **It does not close the campaigns inside the KEEP pursuits.** a1–a6 remain governed by their own
  ADRs and gates; a KEEP is a statement that the pursuit should exist, not a verdict on any question
  inside it.
- **It does not make PARK a soft KEEP.** All 8 PARKs carry a named re-entry condition and a
  2026-11-08 expiry that converts to SUBTRACT absent explicit operator renewal (ADR §2.3).
- **It does not retire the questions behind the SUBTRACTs.** Re-entry armor is out-of-frame evidence
  plus an attached falsifier via a governance channel — a higher bar than the original open, not a
  bar on the subject matter. Specifically: b4 is **not** an oil/energy exposure bar (the live route
  is the MCL instrument-lane intake under a3).
- **It does not perform the two named mechanical follow-ups** (see the Iterate block).

## 4. Defects found in the frozen brief (recorded, not repaired)

1. **§10 park-compliance audit hook was defective as authored** (trap M-AHF: tested against the
   author's mental form, not the artifact's stored form). `grep -rL "re-entry:" docs/pursuits/`
   flags every KEEP/SUBTRACT/MERGE record too — those correctly lack the field. Discovered by
   *running* the hook against real records. **Corrected in place** in both the ADR §10 and the spec
   §10 to scope by standing:
   `grep -l '\*\*Standing:\*\* PARK' docs/pursuits/*.md | xargs grep -L "re-entry:"`.
   Corrected rather than recorded-only because a §10 hook is machinery, not a frozen verdict
   construct — Trap #12 protects gate criteria, not broken greps.
2. **Row-count misstatement in downstream summaries** (not in the frozen brief itself). The run
   record's inventory is **37 rows**; SESSIONS, PR #708, and the memory record each said "30-row".
   Corrected in all three on discovery. The 19-difference figure was correct throughout and is the
   only number the §4 gate consumes.

## 5. Lesson candidates

- **Candidate (below the two-incident bar — watch):** *a disposition label is not a verified
  precondition.* d4's MERGE carried an explicit verification clause that failed on execution while
  the disposition itself survived on inspection. Adjacent to the standing
  [[lesson_verify_source_not_label]] but distinct — there the failure is trusting a label over a
  source; here it is trusting one's own prior proposal's stated precondition without re-running it.
  One incident, $0 cost (caught pre-action). Watch for a second firing before promoting.
- **Datum for the ADR-ceremony-tiering falsifier:** this run is a governance artifact whose omitted
  apparatus would have been directly implicated had the §10 hook not been run — a point in favor of
  running audit hooks at authoring time rather than deferring them to the gate.

## Iterate — loop exit

- **Verdict used:** `RESOLVED-LOADBEARING`
- **Model update:** the pursuit-accretion symptom was real but its *shape* was mis-predicted. The
  expectation was a belt bloated with active-but-unjustified pursuits; what the inventory actually
  found was **decisions left unowned** — two long-pending dispositions (Notion Phase-3, Q-USOIL-1's
  lapsed revisit) that no existing surface flagged because each had fallen out of its own tracking
  board without dying. Accretion here is less "too many things running" than "things with no owner
  and no expiry quietly persisting." That is precisely what PARK-with-expiry and the intake rule
  are built to catch, which is the substantive case for the tier beyond the bare ≥1 count.
- **Next:** INTEGRATE
- **Routing:** INTEGRATE → (a) 37 pursuit records committed at `docs/pursuits/`; (b) GRAND-tier ADR
  gains a §4-satisfied addendum (tier load-bearing; sunset review does not arm); (c) three
  user-skill directories archived + removed; (d) Q-roster row closed and retirements-record row
  flipped; (e) STATE queue row 3 deleted, 2026-11-08 forward-trigger row retained for the ADR's §4
  reading. Re-validation: the §10 hooks below, re-run at the 2026-11-08 gate.
- **Entry packet:** n/a
- **Stop rule / re-proposal bar:** n/a — integrated. (The 8 PARK expiries and the ADR's own
  2026-11-08 §4 reading are the live forward obligations, carried on the STATE board, not
  re-proposal bars on this run.)
- **Board write:** STATE `### 2026-11-08` retains — *"**GRAND-tier ADR §4 first evaluation** —
  load-bearing vs ceremonial read against GSUB-1's ratified outcome; sunset review arms here on a
  zero-difference run."* — now discharged-in-advance by this closure (19 > 0), with the 8 PARK
  expiries co-dated there. STATE operator-queue row 3 (GSUB-1 Phase 3) is **deleted** — done.

## §10 audit-hook discharge

Run this session against the newly-written records:

```bash
$ grep -l '\*\*Standing:\*\* PARK' docs/pursuits/*.md | xargs grep -L "re-entry:"
(empty)
$ grep -l '\*\*Standing:\*\* PARK' docs/pursuits/*.md | xargs grep -L "expiry:"
(empty)
$ grep -l '\*\*Standing:\*\* PARK' docs/pursuits/*.md | wc -l
8
$ ls docs/pursuits/*.md | wc -l
37
```

Park compliance: **PASS** (8/8 PARKs carry both required fields). Hook itself corrected first —
see Defect 1 above; the pre-correction form returned false positives on every non-PARK record.

Resurrection counter and intake-diff hooks are **not discharged this session** — both are
next-gate instruments (they measure drift *since* GSUB-1, which is zero by construction on day
zero).

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-09 | Closure authored at Phase-4 completion | Joshua (ratification) + Claude Code (execution) |
| 2026-08-10 | Notion cold-archival mechanical follow-up recorded (retirement ADR Addendum 2026-08-10 / PR #709); `usoil_regime_capture` lab archival still open | Cursor Cloud Agent (operator GO) |
