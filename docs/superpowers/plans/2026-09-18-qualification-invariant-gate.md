# Qualification invariant gate implementation plan

> **For agentic workers:** Execute with superpowers:executing-plans. Preserve the behavioral contract and integration owner.

**Goal:** CI cannot accept omitted, renamed, skipped or failed critical qualification cases.
**Architecture:** One versioned manifest owns exact node IDs and their invariant provenance. The existing disposable-host recorder runs its selected files, retains actual collection and JUnit, validates every required case, and fails before acceptance on any mismatch. Recorder completion, source stability, capture and cleanup remain mandatory.
**Tech Stack:** Python, pytest, existing JUnit recorder, GitHub Actions Ubuntu hosts.
**Spec:** `docs/superpowers/specs/2026-09-17-qualification-structural-closure-design.md`, section 12; structural-closure roadmap Task 9.

**Selected outcome:** Canonical manifest wired into mandatory CI; three planned structural mutations fail on behavioral assertions; identified final revision passes the focused suite and two-host gate.
**Prerequisites:** Verified lifecycle code and evidence at `8d48bd9`/`9cd2e99`; existing strict invariant report parser. The current isolated lifecycle checkout is clean. Preserve the older dirty invariant prototype. Doctor selected operations Python 3.13.2 and 62 locked packages.
**Ownership:** Root implements and accepts this gate outcome; independent reviewer examines the combined boundary. Broader production/full-campaign acceptance remains separate.
**Verification:** Red/green gate process tests; exact manifest collection; planned basis/registry/role-content mutations in isolated disposable copies, with failing test calls rather than collection/setup errors; focused qualification suite, repository checks and real two-host TEST_ONLY gate. Retain commands, source identity, reports and cleanup.
**Checkpoint:** Record integration and mutation findings here and in the audit; report evidence after local checks and remote runs.
**Return boundary:** Return when this invariant gate and its negative controls are verified. Do not merge, deploy, enroll production credentials, authorize a full campaign, or assert full-campaign capability.

## Behavioral contract

The manifest supplies exact test identities and producer/consumer obligations for all nine invariant families. Pytest supplies actual collection and completed reports. The existing strict parser checks parent/child reports and adverse outcomes; collection alone never supplies execution. The host recorder supplies source/capture/cleanup validity. CI runs the real gate on both hosts for code changes, and cannot silently substitute host-readiness-only checks.

## Execution

- [x] Add failing process tests for absent/renamed/skipped/failed cases and invalid recorder evidence; implement collection capture and recorder integration.
- [x] Populate exact IDs from collected tests, review their behavioral coverage, and bind the canonical manifest into CI.
- [x] Disable product-basis, registry, and role-content validation separately in disposable copies; require the intended assertion to fail and retain exact diffs/reports.
- [x] Run the planned focused suite and gates; independent review of enforcement and unchanged consumers.
- [x] Run the identified candidate on two fresh Linux hosts, audit records, publish the scoped evidence and return.

Local checkpoint: 621 exact critical IDs; broad run1096passed/1fixture failure/1Windows
skip retained as failed; corrected affected selection97passed/1Windows skip;
repository check passed. All three mutations killed on intended assertions with
valid controls and byte-exact retained patch hashes/restoration. Independent review
findings resolved. See the [evidence audit](../../notes/audits/2026-09-18-qualification-invariant-gate.md)
for commands, records and limitations. Candidate `f3099bb` passed run35358450882:
621/621 per host, zero skips/errors/failures, completed stable records and successful
cleanup. Offline canonical verification and combined lifecycle/permission/identity
audit passed for both hosts. Final documentation and the manifest LF checkout pin
change no tested Linux runtime bytes. Selected outcome complete; production and
full-campaign acceptance remain outside this handoff.
