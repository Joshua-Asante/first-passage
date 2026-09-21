# Phase 6 Exact Release Acceptance and Launch Implementation Plan

> **For agentic workers:** Execute with superpowers:executing-plans; use superpowers:subagent-driven-development when bounded delegation is useful and authorized. Preserve the behavioral contract and integration owner. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Accept the exact attended candidate and complete the fresh B7 → sole n3 → deployment GO/reseal → verified initial activation chain within its validity and authorization boundaries.

**Architecture:** Use one prepared release packet and the existing seal, qualification journal, fingerprint, config and activation owners. Rehearse the entire timed sequence with synthetic inputs before obtaining expiring real evidence. Advance only on confirmed outputs, with a durable stop at uncertainty rather than a replacement draw or automatic rollback/rearm.

**Tech Stack:** Existing Python sealer and qualification libraries, private evidence roots, canonical fingerprint implementation, exact image/config manifests, host read-back, durable authorization/attempt journals and the Phase 5 attended operations path.

**Spec:** [Phase 3](2026-09-16-phase3-simplified-qualification.md), [Phase 4](2026-09-16-phase4-real-capability-qualification.md), [Phase 5](2026-09-16-phase5-attended-operations.md), accepted TB-P2 admission ADR sections 2a–2b/T10–T11, final-validation preregistration, B7 account-snapshot contract and initial arming procedure. The accepted governing versions supply exact criteria, not this summary.

## Global Constraints

- **PROPOSED — planning only, 2026-09-16.** No deployment, live ceremony, seal capture, qualification run, GO, arm or account action is authorized here.
- Complete Phase 3 qualification/admission/ORB GO and Phase 4–5 acceptance before final release acceptance. Reuse valid evidence; do not rerun completed ceremonies merely to fill this plan.
- Preserve the sole final n3, frozen streams/depth/criteria and prescribed terminal/void dispositions. Part A is not rerun.
- Initial B7 is distinct from ongoing settlement and from recovery E1/E2/E3 guarantees. Keep original evidence roles and consumers explicit.
- B7 consumption is strictly before `valid_until`; the initial arm must be effectively active after restart before expiry, not merely written to config beforehand.
- No fill, order or adjustment may intervene within the governing B7-to-initial-activation no-activity chain. Fresh sealing alone cannot make an old result valid.
- Only the accepted T10 GO-only transition may change EF1 into EF2. All required non-GO layers/shared/config identities retain their prescribed equality.
- Deployment GO, bounded dry-run emit GO and initial-session authorization are separate. The agent prepares subjects; Joshua retains the decisions and initial arm.
- Maintain private evidence and numerical outputs under ignored primary-checkout roots; publish only permitted digests, verdicts and counts.
- An incident ends automated trading for that account session. Planned initial activation restart follows the accepted Phase 5 distinction; it cannot erase an existing incident restriction.

---

## One release packet and ownership

The coordinating agent owns the complete chain and its evidence consistency. Existing validators own qualification/identity checks; authorized result/seal roles authenticate their actual subjects; the config and account owners confirm effective activation. Joshua supplies required account evidence, attends ceremonies and makes distinct GOs.

Create or extend one release record, proposed location `docs/briefs/phase6-preparation/2026-09-16/release-decision.md`, with private attachments. Record each gate's input identities, authority, output digest, timestamp, expiry, consumer receipt and exact blocker. Do not build a second runtime authority or duplicate Phase 4's capability matrix.

| Gate | Input → confirmed output | Authority retained |
|---|---|---|
| Candidate acceptance | Phase 3–5 evidence and exact disarmed image/config → reviewed candidate and attended dry-run evidence | Technical acceptance plus separately scoped dry-run emit GO |
| Timing rehearsal | Synthetic account/result/signing fixtures and actual build/check path → measured critical path and feasible window | No real sample or production seal |
| B7 | Fresh dashboard, flat/order and full-history evidence → private sealed account snapshot and EF1 | Evidence-backed operator submission and TB-T1 checks |
| n3 | B7/EF1, unchanged FBR, retained ORB GO and frozen attempt → one adjudicated final result | Existing qualification authority and one-attempt journal |
| Deployment GO/reseal | Actual qualifying result and release packet → authenticated GO and verified EF2 | Separate deployment decision; only permitted GO-artifact transition |
| Initial activation | EF2/GO, current seal and boot-bound no-activity evidence plus bounded session approval → durable effective-activation acknowledgment | Joshua's initial arm and existing activation owner |

## Work package 1: Accept the exact candidate while disarmed

**Outcome:** The release is engineering-complete and accepted on its actual source/config/image, before the expiring launch window begins.

**Files/consumers:** Existing TB-I3 integration and release manifest, Phase 4 capability record, Phase 5 operations record, TB-I4/TB-V1 bindings, arming procedure and fingerprint consumers. Select final paths and executable host commands from the accepted baseline; do not guess a deployment CLI.

- [ ] Pin the accepted candidate and all prerequisites, including E1 seal, both ratifications, D0, affirmative D1 ORB GO, M1, TB-I4/TB-I5, symbols, route/settlement guarantees and operations acceptance.
- [ ] Complete independent combined review and required repository/image checks. Resolve substantive engineering, unqualified producers, credentials/configuration and operational blockers before B7.
- [ ] Prepare the bounded TB-I3 attended live-feed integration procedure and its emit GO. Verify listener `dry_run=true` and `armed_until` unset through prescribed host reads before the window; real adapters may emit only within that authority.
- [ ] Exercise actual feed → adapters → synchronization → listener admission/refusal and accepted observation/operations boundaries on the exact candidate. Reuse Phase 4 actual route evidence; dry-run transport does not itself prove real order semantics.
- [ ] Record outcomes, revoke the window's emit GO and verify disarmed state afterward. Retain scope distinctions between actual, synthetic and documentary evidence.
- [ ] Seal the candidate acceptance inventory for the next steps. Any later build/config change must pass the governing identity/change rule before this evidence can be reused.

**Acceptance:** Source loss, missing bar participant, identity mismatch, refusal and operation/observation uncertainty are represented by accepted end-to-end evidence. Dry-run sends no broker mutation. Missing pre/post host read-back or a changed image blocks acceptance. This combined ceremony consumes earlier tests instead of repeating every capability characterization.

## Work package 2: Rehearse the complete launch window

**Outcome:** Measured timing shows that capture, n3, adjudication, real decision latency, permitted GO build/reseal and post-restart verification can fit within the actual legal boundary.

- [ ] Prepare packet templates, tested invocation recipes, signing subjects/templates, private paths, source/manifest checks, deployment artifacts and stop procedures. No result or approval is pre-signed.
- [ ] Rehearse with isolated synthetic snapshot/result/authorization domains through the actual n3 compute shape, adjudication, GO-artifact build, reseal, restart and activation-verification path, without touching production authority or consuming the real attempt.
- [ ] Measure the complete critical path, including source checks, I/O, reviewer/operator availability, image build/deploy and host startup/read-back. Record uncertainty and a justified operating margin; no guessed completion deadline.
- [ ] Select a permissible evidence boundary and attended launch window that fits the measured envelope. If it does not fit, resolve scheduling or permitted engineering changes before real B7; never extend seal expiry or reduce frozen n3 depth.
- [ ] Demonstrate synthetic expiry, failed build, missing signer, lost activation acknowledgment and stop/recovery paths. Prepare a read-only status view so operator attention is requested only when an actual subject is ready or a blocker occurs.

**Acceptance:** All real launch commands and consumers are known and exercised in isolation; synthetic authority is rejected by production consumers. No pending code work is hidden inside the launch budget. This rehearsal establishes timing/behavior, not the real n3 verdict or current account eligibility.

## Work package 3: Capture B7 and execute the sole final n3

**Outcome:** One real frozen final attempt is bound to the fresh valid snapshot and exact execution fingerprint, with its prescribed result retained.

**Existing tooling:** `scripts/seal_account_snapshot.py` with `tests/test_seal_account_snapshot.py`; the accepted qualification controller/attempt store and final-stage interfaces; `ops/c1_rail/policy_fingerprint.py`. The snapshot sealer validates supplied evidence rather than independently fetching or certifying broker facts. The Phase 3 `run_production_e1` entry point is not an n3 command: use only the final-stage interface accepted and rehearsed in work package 2.

- [ ] Recheck candidate/evidence identities, retained D1 ORB GO, readiness of signers/operator, current boundary and disarmed/no-activity posture. Stop before capture if the measured window is no longer feasible.
- [ ] Joshua supplies the B7 dashboard, zero positions/working-orders evidence and full inception-to-capture account history, with required provenance/timestamps. Verify actual source facts using the qualified procedures; do not fill missing facts with attestation.
- [ ] Apply TB-T1 checks C1–C10 and write the snapshot only under an ignored private root. Retain distinct original evidence files, tool digest, timestamp and actual `valid_until`; preserve all refusal semantics.
- [ ] Bind B7 and the exact candidate to EF1 and prove prescribed shared-component equality with FBR using the accepted canonical implementation. Retain full manifests and independently verified admission/provenance.
- [ ] Validate the final-stage authority, frozen depth/RNG allocation, unused attempt status and snapshot validity/no activity at dispatch. Execute the sole n3 once through its durable controller. Do not run Part A or use a second namespace as a retry.
- [ ] Adjudicate all prescribed final conditions on actual retained output and obtain required result authentication. Report the true verdict; failure follows terminal retirement/disposition under the governing process.

**Acceptance cases:** stale snapshot at dispatch; wrong FBR/EF/account; intervening activity; changed code/config; lost receipt after a possible dispatch; partial/corrupt output; failed statistical condition. Preserve the original attempt and evidence. Unknown dispatch is not “not run.” A valid start alone does not establish later activation eligibility.

## Work package 4: Obtain GO and perform only the permitted reseal

**Outcome:** An actual passing final result supports a separate deployment GO, and the complete deployed artifact satisfies EF2 without non-GO drift.

- [ ] Prepare the decision packet from the actual authenticated result, B7/EF1, remaining validity, complete acceptance evidence and proposed attended session. Include explicit unresolved items; do not present a failed/void result for GO.
- [ ] Obtain the separate deployment GO from Joshua and bind its exact artifact/digest through TB-P2 T10. Reuse unchanged approvals only within their accepted scope.
- [ ] Perform only the permitted GO-artifact/commit/image reseal transition. Compare every shared component and non-GO layer/config identity, not just selected source files or a top-level label.
- [ ] Verify complete EF2 and the actual image/config on the host through the accepted read-back procedure. Keep the runtime disarmed until the separately authorized initial-activation transition.
- [ ] Recheck expiry and no activity before proceeding. A GO signature cannot waive a stale snapshot, drift or incomplete result.

**Acceptance:** Any unexpected non-GO build/config change blocks launch and follows the governing invalidation rule. Reverting to an old image is not automatic recovery authority. A newly sealed snapshot does not retroactively validate the previous n3 result. No operator approval is requested on a hypothetical result.

## Work package 5: Authorize and verify effective initial activation

**Outcome:** The exact authorized release becomes effectively active for the approved attended session, with durable acknowledgment before risk admission.

- [ ] Verify Joshua's platform access/attendance and qualified alert paths, session/calendar eligibility, required settlement/source state, no unresolved obligations and no applicable incident-session restriction.
- [ ] Prepare and obtain the separate bounded initial-session authorization under the accepted boot/request protocol. Its expiry cannot override the entry cutoff, and it cannot replace B7/n3/deployment GO.
- [ ] Joshua performs the initial arm via the accepted procedure. Permit only the defined initial-arm config transition; preserve other config equality.
- [ ] At effective activation after restart, repeat actual image/config/GO and current snapshot validity checks, with fresh no-activity evidence bound to the current boot/request. Use Phase 5's accepted planned-boot distinction; do not reuse a pre-restart attestation.
- [ ] Serialize activation against any new halt, persist authority and effective-activation acknowledgment, and only then permit risk admission from the next complete eligible bar. A config write, healthy process or operator click is not completion.
- [ ] Return a compact activation receipt: permitted session/window, candidate/EF2/GO identities, effective time and acknowledgment digest, plus operating/stop procedure. Hand over to the accepted attended session procedure; do not create an unsolicited monitoring automation.

**Acceptance cases:** seal expires during build/restart; stale or wrong-boot no-activity evidence; concurrent incident; config write succeeds but acknowledgment fails; token replay; unexpected startup identity; missed activation window. Each leaves or returns the runtime to its contractually fenced state. Preserve any possibly effective actions and use attended intervention if required; never issue a second blind arm.

## Stop and disposition table

| Event | Required next step |
|---|---|
| Prerequisite or timing failure before B7/n3 | Remain disarmed; resolve the exact blocker without consuming an outcome-bearing attempt |
| n3 criterion fails | Terminal disposition under TB-P2, including owning admission-retirement process; no extra sample or alternative book |
| Snapshot expires or intervening fill/order/adjustment voids the chain | Stop for the operator under C10/P2; any continuation requires explicit permitted authority, fresh evidence and re-established dependent gates; no automatic replacement draw |
| Shared/non-GO drift | Apply T10/change-rule failure disposition; no silent rehash or presumed continuation exception |
| Lost result/dispatch/activation receipt | Inspect durable state and adjudicate uncertainty; absence of a receipt does not prove absence of effect |
| Incident during launch or session | Apply Phase 5 intervention, retain obligations and session restriction; no same-session restart into trading |
| Reconciliation or disarm incomplete | Attendance/intervention continues; report the exact outstanding obligation |

## Completion and operator overhead

Phase 6 succeeds only on confirmed effective activation of the exact release in the authorized window, with the durable acknowledgment and evidence chain intact. A merged PR, completed n3, deployment GO or arm config write alone is insufficient. If blocked, the final record names the actual disposition rather than declaring launch complete.

Operator involvement is concentrated into the attended dry-run, fresh evidence capture, actual-result deployment decision and separate initial-session authorization. The agent prepares the artifacts and runs authorized checks; those decisions remain sequential because later subjects depend on earlier outcomes. Session attendance and the accepted operating procedure continue after this launch handoff.

This phase-level plan introduces no new command or numerical criterion. The accepted baseline and rehearsed execution inventory must supply concrete invocation/signing/host procedures before real launch. No seal, qualification sample, deployment or activation was performed while drafting it.
