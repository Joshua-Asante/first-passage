# H9 R2 / D3 recovery slice — keep-or-defer comparison

**PROPOSED comparison for campaign-owner review, then Joshua and the statistical owner.** Prepared 2026-10-03 by Codex Coordinator 3 from `d8e641f20e394b28897c79892ab80d402ab07c75`; current-source pin `ebe5c0ba846d2d7b75227d7b8302a818945974f5`. No recovery build or decision is authorized by this note.

## Settled boundary

ENG-4 has already disabled zero-record recovery for the first production E1. With no retained complete records, IN_DOUBT stays terminal; no production R7 standard was set. Only the keep-or-defer decision on **H9 checkpoint R2 / D3 recovery slice** remains open. Until Joshua rules, R2 remains required and the 2026-09-26 recovery direction stands. H9 R2 is distinct from the terminate-and-fence rule also called R2 and from lane D step 3's measured-closure decision called D3.

Owners at the source pin: [execution-slices ENG-4](https://github.com/Joshua-Asante/first-passage/blob/ebe5c0ba846d2d7b75227d7b8302a818945974f5/docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--c3-accepted-s5-accepted-for-test_only-on-landing-2026-10-01), [Full-E1 spec §2.6](https://github.com/Joshua-Asante/first-passage/blob/ebe5c0ba846d2d7b75227d7b8302a818945974f5/docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md#26-exact-dispatch-restart-and-retry-semantics), and [H9](https://github.com/Joshua-Asante/first-passage/blob/ebe5c0ba846d2d7b75227d7b8302a818945974f5/docs/briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md#h9--resultseal-integration-and-bounded-same-sample-recovery-two-checkpoints).

## What recovery can currently salvage

`execution/worker.py::run_part_a_body` writes the initial Part A prefix through `write_part_a_artifact` (exclusive create, flush, fsync), before expansion, then writes the final artifact after computation. `execution/compute.py::run_part_a_compute` passes the same prefix bytes through custody and its return. This is an existing retained-record producer.

N1/N2 produce the complete result frame at the end. They do not provide an equivalent progressive complete-record artifact. With zero-record recovery disabled, the demonstrated retained-record opportunity is Part A after its initial prefix, before finalized capture. Do not broaden that opportunity to arbitrary partial spool bytes or presume a new N1/N2 producer.

`campaign_store.py` currently refuses another compute reservation for a phase and makes interrupted uncaptured work terminal. The spec expressly says every IN_DOUBT remains terminal until the separate recovery slice is accepted. A prefix alone grants no restart authority. The retry would rerun the entire checkpoint from its first panel, not resume after the prefix.

## Comparison of remaining work

| Dimension | A — Keep bounded retained-record recovery | B — Defer compute re-execution for first production E1 |
|---|---|---|
| Benefit | Can salvage an eligible same-boot Part A interruption after a complete retained prefix, if enough original allowance and time remain | Keeps terminal-only compute behavior and avoids adding a new compute retry state machine to this release |
| Loss / residual | No recovery for zero records, reboot, overrun, committed assessment, completed capture or VOID; a full rerun may not fit after the interrupted charge | Even an otherwise recoverable Part A prefix cannot continue; later work needs separately authorized new-attempt treatment, which may use a new salt/sample |
| Store and service work still owed | Linked retry identity; atomic eligibility and retry-count reservation; immutable history; exact sample/source/runtime/configuration equality; same original deadline and cumulative charge; terminal mismatch incident | Prove current terminal behavior across real service entrypoints; exclude relaunch even when a prefix exists; retain exact history and cleanup evidence |
| Custody and comparison still owed | Freeze a versioned statistical-field comparison schema before admission; authenticate original prefix provenance after fencing; compare the new prefix before allowing later progress; retain both attempts | Preserve prefix bytes as evidence without treating them as execution authority; no new comparison-based continuation mechanism |
| Lifecycle work still owed | Absence proof before retry, no late original capture, concurrent recovery serialization, retry limits, crash/reopen behavior, and Q9 closure/reveal integration | Explicitly amend the release-specific R2 gate; prove no automatic replacement and no accidental weakening of signing recovery or Q9 custody |
| Verification cost | New positive retry route plus all negative/partial/concurrent/restart cases; accepted R1 prerequisite; release identity and affected measurement review | Terminal behavior regression and documentary gate amendment; R1, B4, signing recovery and release acceptance remain owed |
| Authority cost | Current direction still requires this work, but a frozen owner-approved implementation card is needed | Joshua/statistical-owner decision must amend H9, spec and checklist together; absent that decision A remains the obligation |

No duration, interruption rate, monetary saving or probability of recovery success has been measured. This comparison is a source-based inventory of work and capability, not an estimated schedule or production reproducibility claim.

## Recommendation and decision wording

**Recommend B for the first production release**, subject to Joshua and the statistical owner. With zero-record recovery off, the evidenced benefit is a narrower Part A window, while A still needs the full identity, fencing, accounting, comparison and lifecycle mechanism. This recommendation changes the original note's unsupported default to A; it does not decide the tradeoff. Choose A if preserving that continuation opportunity justifies the additional acceptance work. Both branches leave H9 R1 independent.

If **A** is selected: retain H9 R2 as a pre-T06/S8 gate for the enabled retained-record subset. Freeze its schema and service-owned eligibility, enforce all R1–R10 safeguards, and leave zero-record execution prohibited. Do not create a new N1/N2 prefix producer under this decision.

If **B** is selected, proposed owner amendment:

> For the first production E1, defer H9 checkpoint R2's compute re-execution capability, including cases with retained prefixes. Replace its pre-T06/S8 acceptance condition with verified terminal interruption, durable retained evidence and terminate-and-fence cleanup. Prohibit compute relaunch and automatic replacement attempts. Preserve R1 integrated result/seal acceptance, exact historical receipt inspection and durable signing recovery. Future compute recovery requires a separately admitted slice and evidence approval.

The campaign owner applies the selected wording to H9, Full-E1 spec §2.6 and the execution/deployment ledgers as one reconciled change. Q1 remains decided. Q9 option A is already adopted: service-committed closure governs reveal, never a status-read inference; this comparison grants no early disclosure or replacement attempt. Term 8 remains a separate dispatch.

## Acceptance evidence and return boundary

For both branches require: zero records terminal; interrupted original fenced against late capture; failed cleanup never restores authority; reboot/uncertainty, overrun, assessment/FAIL, finalized capture and VOID never compute-retry; exact receipts and signing recovery preserved. Under A add matching-prefix continuation, mismatching-prefix incident, altered identities refused, original cumulative charge/deadline, simultaneous recovery requests, crash around reservation/comparison and retry-count exhaustion. Under B add retained-prefix terminal through reopen and every service recovery entrypoint, with no compute reservation or new sample.

Return this comparison to Claude coordinator (3) for acceptance and integration before presenting the choice to Joshua/statistical owner. No worker dispatch, integration, operational action or research follows from this document. Source review completed; runtime tests were not run because no runtime change was made.
