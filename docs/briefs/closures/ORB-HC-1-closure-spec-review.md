# ORB-HC-1 — closure at specification review (untested)

**Status:** `CLOSED — spec review, untested`. This is not a rejected or falsified candidate. K += 0. No edition, export, data read or run occurred.
**Date:** 2026-10-21.
**Authority:** the H-C closure rule in the PM's v3 handoff, which Joshua approved: "one final review; NEEDS FIXES-important → no v4". Closure relayed by the coordinator 2026-10-21.

## What was specified

ORB H-C: the corrected v7 baseline (O-N, CSV `8e4902c3…e861`), with v7's adds replaced by a single conditional add. The add is a resting buy-stop at base fill + T·R0, at most one per session. It ran as an EM3 research-only exception.

Joshua's rulings bound in the spec:
- the add reuses entry ID `ORB Long` under v7's single `from_entry` exit;
- a position-flat cancel of a pending add;
- the stall counter counts the add at fill;
- an orphan keeps the native bracket.

Captured O-N breakeven is OFF, so the add never moves the stop. Specs and label notes are held privately in the session notes and the relay; they are not published.

## Review record

| Round | Candidate | Verdict |
|---|---|---|
| 1 | v1 `d4444c97…4748` | NEEDS FIXES (F1–F5) |
| 2 | v2 `ba76b130…9d7b` | NEEDS FIXES (R1–R4) |
| 3, final | v3.1 `a0f772b8…f728` | **NEEDS FIXES (N1, important)**; R1–R4 addressed |

The final report is `CODEX-REVIEW-3.md`, sha256 `e44376e43647c11efa085d497105fc76cc0ed8206de1dc77473ad064c89ada4f`, from the same reviewer. It is held in private relay custody.

## Finding N1 (accepted by the author)

With on-fill recalculation off, a stall `close_all` created at the cut-time bar-close evaluation fills at that close. No later evaluation in that bar sees the flat position.

An actual-flat cancel therefore cannot fire in that evaluation. The resting add can fill on the next bar: a later-bar orphan, which the spec said could not occur. The same gap applies to v7's other bar-close exits.

The contract left open whether the cancel is coupled to the action that creates the close, or whether the chronology admits the pending interval. That choice changes add eligibility, orphan frequency and the orphan guardrail.

## For any successor

A future continuation-add specification needs fresh authorization. Before review it must bind:
- the cancel-coupling choice (cancel issued together with any closing action, or the pending interval modelled explicitly);
- the order of the close and the add.

The R1–R4 repairs (power method, restored add-count and worst-trade/episode guardrails, Bonferroni M = 1, F0 disposition) were accepted and can be reused as text.

## Iterate — loop exit

- **Verdict used:** CLOSED at spec review, untested.
- **Model update:** under bar-close execution, a cancel triggered by the actual flat position lags any close created in the same evaluation. Conditional-add specs must bind how the cancel is coupled to the close.
- **Next:** STOP
- **Routing:** STOP. The closure rule allows no v4. Deployment is on hold (Joshua, 2026-10-21), and ORB lineage work waits on Q-RESTART-1.
- **Entry packet:** n/a
- **Stop rule / re-proposal bar:** reopening needs a fresh spec under new operator authorization that binds cancel coupling and close/add ordering up front. No outcome evidence exists for or against the mechanism.
- **Board write:** none — STOP, nothing owed
- **Registry:** n/a — closed at spec review before any test; not a rejected candidate
