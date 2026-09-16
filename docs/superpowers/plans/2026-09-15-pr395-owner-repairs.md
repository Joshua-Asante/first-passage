# PR395 settlement-owner repairs

> **For agentic workers:** Execute with superpowers:executing-plans. Coordinator owns integration; preserve the component split.

**Goal:** Close revision retention, signing chronology and B7 reopen defects in the durable owner.

**Architecture:** Keep evidence and arithmetic in the extracted components. The owner serializes challenges, authenticates an operator-added signing timestamp, persists revisions and rechecks retained bytes on every chain read. B7 derives its reopen in America/New_York.

**Spec:** docs/spec/2026-09-15-tradeify-attended-settlement-contract.md; B7 snapshot contract C5/C10.

**Baseline:** clean integration checkpoint 97728a8, 1,977 ops tests passed. Calendar #396 has a separate reviewer; do not edit its branch. Evidence/calculation are #398/#399. No policy constants, activation, deployment or live-source qualification changes.

## 1. B7 boundary

- [x] Reproduce Thursday close with Friday captures accepted under generic 49-hour bound.
- [x] Replace that bound with the next 18:00 ET (same weekday, Sunday after Friday), converted to UTC; require valid_until to equal that boundary. Existing capture <= seal <= receipt < expiry then covers all observations.
- [x] Test ordinary weekday, Friday, DST transition weekend and expiry refusal.

## 2. Revision retention

- [x] Reproduce missing revised bytes and corruption after resolution/restart.
- [x] Require account/session-bound revision evidence and declared source bytes; preserve them atomically with invalidation. A revision is evidence of a problem, not a newly accepted close, so do not require corrected arithmetic to pass.
- [x] Reuse retained-evidence verification for REVISION rows on every chain read. Missing or corrupted revision bytes block reads and restart after reconciliation too.
- [x] Update existing correction callers/fixtures and check refusal leaves state unchanged.

## 3. Signing chronology

- [x] Reproduce construction < challenge < signature < receipt with real Ed25519 signing.
- [x] Remove signing time from package (new v3 schema). Introduce a small operator-side signing-envelope builder: exact challenge plus operator_signed_utc. Verify signature over all fields, compare challenge digest excluding only this added field, and enforce issue <= signed <= receipt < expiry. Retain the signed reply and signature in the acceptance event.
- [x] Keep source capture <= issue in the pure verifier. Update assembler, synthetic producers, protocol docs and tests; refuse old wire formats without silent migration.
- [x] Exercise altered timestamp, malformed/naive time, replay, challenge tampering, concurrency and restart.

## Acceptance

- [x] Focused tests fail before repairs and pass after them.
- [x] Full ops suite, diff checks, independent review of owner and changed component interfaces.
- [ ] Publish owner component on #399 and update #395 integration status; monitor CI. No merge.

Actual account query semantics, historical equity capability and deployment qualification remain owed. The owner changes must not claim those capabilities.
