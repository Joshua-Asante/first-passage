# ADR Tombstone Index

One line per pruned ADR — the decision's *current consequence* survives here; the
full body is retrievable via `git show pre-prune-2026-08-08:docs/adr/<file>`
in the **private archive** — that tag is not on this public clone
(`git log --follow -- docs/adr/<file>` is the fallback here)
(ADR [`2026-08-08-great-prune`](2026-08-08-great-prune.md) §3 class 4; retention
test R1–R5). Revival of any tombstoned decision requires fresh pre-registration
under the standing chain — never a lookup. Rows are grouped by disposition,
newest first. Obligations that died with a carrier are recorded in the
[2026-08-08 audit note](../notes/audits/programme-audit/2026-08-08-quarterly-audit.md) §2.

| Date | ADR | Consequence now | Body |
|---|---|---|---|
| 2026-07-03 | hardcore-p1-automated-execution-gate | **Tombstoned by operator ruling 2026-08-08.** §4 could only ever return AMBIGUOUS-OPERABLE (E1 unattempted — no strategy-signal fill has ever occurred) and its §6 budget clock was pegged to "90 days after R6 issues a GO", which R6's spent NO-GO makes unreachable | `git show pre-prune-2026-08-08:docs/adr/2026-07-03-hardcore-p1-automated-execution-gate.md` |
| 2026-07-03 | hardcore-p2-edge-transfer-gate | **MOOT** — §4 already fired and was operator-ratified terminal 2026-07-06 ("§4 FALSIFIED-on-venue"); the Pepperstone measurement basis retired 2026-08-02, so no re-run is possible | `git show pre-prune-2026-08-08:docs/adr/2026-07-03-hardcore-p2-edge-transfer-gate.md` |
| 2026-07-03 | hardcore-p3-compounding-ceiling-amendment | **Tombstoned by operator ruling 2026-08-08.** ⚠ Kill-D's per-firm `M_f` payout-extraction arithmetic was **never computed** and had been owed since its own 2026-07-06 hard date; the "RESOLVED" record was a triage label, not the work. Re-enters as a fresh dated packet if wanted — not as a revived ADR | `git show pre-prune-2026-08-08:docs/adr/2026-07-03-hardcore-p3-compounding-ceiling-amendment.md` |
| 2026-07-03 | hardcore-p4-tail-survival-gate | **UNFALSIFIABLE** — both limbs dark (limb 1 dormant pending a live venue; limb 2 orphaned when the decompound HOLD's limb-2 was struck 2026-08-03); §5 forbids forking a second process | `git show pre-prune-2026-08-08:docs/adr/2026-07-03-hardcore-p4-tail-survival-gate.md` |
| 2026-07-03 | hardcore-p5-source-truth-rail-gate | **UNFALSIFIABLE** — §6 struck its own calendar backstop and pegged the gate to "before R6 issues a GO", which a spent NO-GO one-shot can never satisfy | `git show pre-prune-2026-08-08:docs/adr/2026-07-03-hardcore-p5-source-truth-rail-gate.md` |
| 2026-08-02 | striker-tradeify-funded-phase-descope | Withdrawn, never ratified; wider whole-venue de-scope elected 2026-08-04 (live ADR) | `git show pre-prune-2026-08-08:docs/adr/2026-08-02-striker-tradeify-funded-phase-descope.md` |
| 2026-06-22 | nas100-orb-5th-leg | Withdrawn same-day: native TV-CSV falsified the offline harness (fills ~5.6× optimistic); no 5th leg | `git show pre-prune-2026-08-08:docs/adr/2026-06-22-nas100-orb-5th-leg.md` |
| 2026-06-12 | rnd-feed-instrument-class-split | Superseded by TV-CSV canonical-feed policy; CME futures TV exports are the live feed | `git show pre-prune-2026-08-08:docs/adr/2026-06-12-rnd-feed-instrument-class-split.md` |
| 2026-05-14 | allocation-refresh | Superseded by 2026-05-23 allocation-refresh-2 (lock lineage lives in CLAUDE.md §Strategy Reference) | `git show pre-prune-2026-08-08:docs/adr/2026-05-14-allocation-refresh.md` |
| 2026-05-11 | objective-map-section-4-tighten-falsifier | Retired with the Objective Map surface (challenge era closed) | `git show pre-prune-2026-08-08:docs/adr/2026-05-11-objective-map-section-4-tighten-falsifier.md` |
