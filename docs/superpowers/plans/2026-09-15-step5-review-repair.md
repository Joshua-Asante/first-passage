# Step 5 review repair implementation plan

> **For agentic workers:** Execute with superpowers:executing-plans; preserve the behavioral contract and integration owner.

**Goal:** Close the six rebuild findings on PR #395, with simpler shared enforcement.

**Architecture:** Keep the existing package and owner APIs. Store the earliest unresolved revision boundary directly in integrity-checked state; share package/source verification between active and superseded records. One checked digest binds active, superseded, revision, and reconciliation history. Separate audit timestamps from clock-defined boundaries; signed envelopes own challenge times.

**Tech Stack:** Python, SQLite, pytest, existing Ed25519 signing/verification.

**Spec:** `docs/spec/2026-09-15-tradeify-attended-settlement-contract.md` and B7 snapshot contract.

## Global constraints

- Integration owner: Codex coordinator. Base: `f29ee061fd410fa8ab5e4c9f03245cf107210fa7`.
- Preserve operator-attested evidence, exact predecessor order, independent activation/resumption, and all policy constants.
- No private evidence, enrollment changes, or live settlement actions.
- Storage changes must refuse incompatible stores explicitly; never silently bless previously unverified history or discard data.

## Acceptance and execution

- [x] Reproduce all six findings through the actual store/loader. Include two revisions in both orders, multiple correction cycles, archive row/package/source corruption, and honest timestamp boundary cases.
- [x] Current-close transaction provenance: reject later sessions even without a predecessor account package; permit pre-existing history. Preserve historical catch-up's explicit close-equity requirements.
- [x] Chronology: require captures <= challenge issue <= signing <= receipt, and B7 close <= captures <= seal <= receipt. Keep timezone-aware source timestamps.
- [x] Correction lifecycle: persist the minimum outstanding revision sequence; resolve the entire suffix, reset only on successful resolution, remain restore-pending; protect active/superseded records, correction payloads and linkage against edits/deletion with one digest anchored in checked state.
- [x] Calendar: accept second-precision audit events while refusing sub-minute trading boundaries.
- [x] Run focused regression suites and broader ops checks; review changed behavior independently; update invariant and implementation records with evidence and limits.

Tests exercise signed `submit`, durable `status`/`settled_close`/restart, `resolve_invalidation`, and `load_ratified_calendar`; no mock supplies acceptance. Regressions must fail on the base before implementation. Existing tests establish consumer sizing agreement, concurrency, and restart fencing.
