# Rule 2 — Forward trip-log

**Purpose.** The falsifier of record for Rule 2 (budget before acting). Canon: `docs/methodology/inqhiori-canon.md` §15. ADR: `docs/adr/2026-06-16-rule-2-budget-before-acting.md` (§4 falsifier).

This is **one table, not a telemetry subsystem** (ADR §5). Append one row each time a budget *trips* (the wire fires). A budgeted investigation that completes *under* budget is recorded as a non-trip baseline row so the log is never empty-theater and the audit can see the threshold was not even approached.

**The thresholds under test (set 2026-06-16, validated forward only — never re-derived from the cfg00–12 history that set them):**

| Loop class | Budget | Extension authority |
|---|---|---|
| INNER (recoverable/tempo) | **3 iterations** | self-extend once, stated reason |
| OUTER (structural/low-reversibility/statistical) | **8 iterations** | owner / re-audit only |
| STRATEGIC (funding/kill-continue/programme-tier) | **3 constituent OUTER investigations** | owner / re-audit only |

**At each programme audit:** confirm ≥1 entry per active loop class; check whether the wire fired at moments that were, in hindsight, the right place to stop (H holds → 3/8/3 graduates) vs. at productive moments (falsifies the threshold). An empty table across ≥2 audit cycles falsifies the rule as load-bearing (inert → amend-or-delete). Standing bias while learning: **run tight, loosen only on evidence.**

---

## Trip log

| Date | Loop class | Spent / budget | Extend-or-stop (reversibility) | Hindsight-correct? |
|---|---|---|---|---|
| 2026-06-16 | OUTER | 3 / 8 | No trip — landed under budget (canon-edit commit, irreversible class) | n/a (wire did not fire) — recorded as the first budgeted investigation; OUTER=8 was not approached on this 3-iteration task, a calibration baseline, not a trip |
| 2026-08-20 | STRATEGIC | 3 / 3 | **Trip fired — STOP.** Retroactively recognized: the external-mechanism/framework-mapping move-class (3 instances, 2026-08-18→08-20, none formally declared as budgeted OUTER work going in) reads as 3 constituent OUTER investigations of one implicit STRATEGIC question. Reversibility class: recoverable-cost (no locked surface, no capital) but real multi-agent research spend across all 3. Per ADR §4, extension is owner adjudication or a re-audit — never self-granted; this row's own audit ([`2026-08-20-external-mapping-move-class-audit.md`](programme-audit/2026-08-20-external-mapping-move-class-audit.md)) is that re-audit and recommends STOP pending fresh owner GO, not a self-granted 4th instance. | **Yes, hindsight-correct, on a corrected basis.** ⚠ Original text here cited "the pipeline's own cheaper, already-scoped alternative (Q-TRAINKILL-2), unopened" as supporting evidence — **that was wrong**, `Q-TRAINKILL-2`/`-3` had already run to `STOP` same-day 2026-08-18, before instances 2/3 ran (see the audit's own "Correction" section). Corrected basis: the 3rd instance ran under the most favorable conditions of the three (explicit guardrail carve-out, highest structural-fit score measured) and still produced 0 survivors, and the move-class's own belt only ever grew (0 prunes across 3 instances). Stopping here still does not read as a threshold-falsifying case, independent of the retracted TK2 claim. |
| 2026-08-23 | STRATEGIC | 4 / 3 | **Owner adjudication — constrained 4th instance.** Operator GO this session: download NeMo Guardrails and reconcile; freeze = pin + map existing rails, no imported mechanism, no new pipeline stage. Not a self-extension. Record: [`N-2026-08-23-nemo-guardrails-reconciliation.md`](../notice/N-2026-08-23-nemo-guardrails-reconciliation.md). Belt work was a consolidation ([`external_mapping_guardrails.md`](../../methodology/external_mapping_guardrails.md)), not a sixth add. | n/a (wire already fired 2026-08-20; this row records the GO, not a new trip) |

<!-- Append genuine trip rows below as the wire fires. One row per trip. Do not fabricate trips to fill the table (ADR §4 — forward validation, no theater). -->

---

## 2026-08-08 slate — trip-log-starvation disposition (2026-07-01 programme audit)

The Sentinel `precondition_scan` (Action-routed) flags this log as **starved** for the
2026-08-08 programme-audit Rule-2 graduation check (<2 data rows). **Disposition: expected;
run the check as-is.** The log is sparse *by design* — ADR §4 forbids fabricating trips, and
only one budgeted investigation (2026-06-16, non-trip baseline) has occurred since Rule 2 was
codified 2026-06-16. Per canon §15, an empty/starved log is not itself a failure until it
persists **across ≥2 audit cycles**; only 0.16 cycles have elapsed. The 2026-08-08 check
therefore reads the real (sparse) log and returns **AMBIGUOUS-on-schedule** (as the
2026-07-01 scoped meta-audit already did for the #7 falsifier-liveness diagnostic) — *not*
FALSIFIED (barred until the 2nd post-codification cycle, ≈2026-12) and *not* a blocker on
the slate. No policy change; no fabricated rows. This note dispositions the Sentinel finding
so it is not re-raised as novel each scan.

> ⚠ **CORRECTION 2026-08-09 — the 2026-08-08 check did not run.** The paragraph above was written
> *before* that slate and states what the check "therefore reads… and returns". It reads as a
> record; it is a **prediction**. The
> [2026-08-08 quarterly audit note](programme-audit/2026-08-08-quarterly-audit.md) contains **zero**
> occurrences of "Rule 2" or "trip log" (grep count 0) — the check was never executed or recorded at
> that slate, despite
> [`Rule 2 ADR`](../../adr/2026-06-16-rule-2-budget-before-acting.md) §7 making it a standing
> audit checklist item. The 2026-07-01 meta-audit *did* run it properly, so this is a
> single-cycle miss, not a pattern.
>
> **This is the same phantom-discharge class** as the "Reviewed at the 2026-08-08 slate" line
> corrected the same day in `docs/rejected_candidates.md` — a forward instruction that ages into an
> apparent completed record. Both were found by the same sweep; see
> [`ADR 2026-08-09 register topology`](../../adr/2026-08-09-rejection-register-topology-and-bar-wiring.md) D5.
>
> **Consequence for the falsifier clock — genuinely unresolved, do not guess.** The ≥2-cycle
> empty-log falsifier now has an ambiguous denominator: the 2026-07-01 audit's §10 names "the 2nd
> (~2026-12) meta-layer audit" and expects the 1st post-codification audit "~2026-09", but the real
> gates are **2026-08-08** (consumed without recording a disposition) and **2026-11-08**. Whether
> the falsifier is one tick or two from firing is not determinable from the record. **Rule at the
> 2026-11-08 gate**, and state the counting convention there rather than inferring one now.
