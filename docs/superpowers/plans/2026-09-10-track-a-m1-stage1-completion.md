# Track A — complete M1 / B7-REFIRE Stage 1

**Date:** 2026-09-10
**Scope:** finish the one required strategy-originated dry-run proof and resolve M1.
**Authority:** this plan does not authorize an arm, a live order, or deployment of the accepted
Tradeify book.

## Outcome

Track A is complete only when all of the following are true:

1. A real test strategy runs through the normal Python daemon evaluation hook.
2. The listener records one correlated `dry_run` decision with `qty_out=1`.
3. No sender or broker-order path runs.
4. The operator signs the evidence.
5. The M1 artifact passes strict validation as `RESOLVED`.
6. The running listener contains that resolved artifact and remains `dry_run=true`.

PR #332 supplied the offline-only test identity, one-micro sizing, live-mode rejection, and
one-attempt daemon controls. PR #334 retired Databento without approving a replacement. The
remaining work is operational qualification, not accepted-book implementation.

## Non-negotiable safety rules

- The listener stays `dry_run=true`; never use `--arm`, `dry_run=false`, or
  `--acknowledge-m1-unresolved` in Track A.
- `m1_stage1_test` is entry-only, capped at one micro, and rejected before sender invocation in
  every non-dry-run state.
- The daemon starts and finishes with emission disabled. A timeout or uncertain transport is
  terminal and is never retried automatically.
- No withdrawn identity, manual POST, `NullStrategy` event, fabricated event ID, or zero-size
  decision qualifies.
- Before a listener deploy or restart, the operator must verify broker flatness and confirm access
  to the authenticated private recovery procedure.
- Secrets, account identifiers, account values, and raw private evidence stay out of commits and
  public transcripts.
- Each live phase requires its own explicit release. A completed planning or code PR is not that
  release.

## The four remaining phases

### A1 — approve and implement the signal source

**Purpose:** replace the retired Databento source without weakening the definition of a real
strategy-originated signal.

1. Write a short ADR amendment with the proposed source, what the proof certifies, health and
   staleness rules, credential ownership, and why replay or fixtures do or do not qualify.
2. The operator selects one option or records NO-GO.
3. Record the ruling in the ADR before implementation; a comment or oral ruling is insufficient.
4. Implement only the selected daemon-side source. It must boot disconnected and disabled, use
   the existing `BarSource`/evaluation/B1 path, and preserve the one-attempt ceremony controls.
5. Build and test the final daemon image on Linux. Confirm import/COPY closure, POSIX locking and
   atomic writes, inert boot, no boot-time network connection, and no automatic retry.

**Gate:** the source ruling is merged, the Linux image is green, and the daemon image starts
inert. If no source is approved, Track A stops here without deployment.

### A2 — prove deployment readiness

**Purpose:** establish that both apps can be changed safely before touching Fly.

The readiness record must show:

- The listener is currently healthy, `dry_run=true`, and has no active `armed_until`.
- The daemon is currently healthy and emission-disabled.
- The operator can open the authenticated recovery procedure.
- Broker flatness can be verified at the required deployment checkpoints.
- Listener and daemon candidate images build on Linux and have complete import/COPY closures.
- The listener migration adds only the test identity, initially `RETIRED` with zero allocation.
- The daemon candidate boots with the source disconnected and test emission disabled.
- Current and rollback image identities are recorded for both apps.
- The exact in-container fixture-hash refresh and final M1-artifact bake sequence is written down.

**Gate:** separate GO/NO-GO rows for the listener and daemon. Do not deploy from an incomplete or
ambiguous readiness record.

### A3 — deploy both apps, disabled

**Listener deployment (separate release):**

1. Reconfirm broker flatness, `dry_run=true`, inactive `armed_until`, recovery access, and daemon
   emission disabled.
2. Deploy the reviewed listener image from the reviewed `main` commit.
3. Apply only the approved test-identity migration; keep it `RETIRED` with zero allocation.
4. Refresh image-carried fixture pins from the actual container bytes and complete the reviewed
   artifact re-bake sequence if required.
5. Verify boot output, health, artifact digest, `dry_run=true`, inactive `armed_until`, and the
   live-mode test-identity rejection. Stop with no signal.

**Daemon deployment (later, separate release):**

1. Reconfirm the listener is disarmed and healthy.
2. Deploy the reviewed daemon image with the test strategy, source, and emission disabled.
3. Verify image identity, health, disconnected source, inert one-shot state, and no listener-ledger
   change during boot. Stop before preparing a ceremony.

**Gate:** both deployed apps match the reviewed images and are demonstrably inert. A deploy that
needs an improvised repair fails this phase and returns for review.

### A4 — run one attended proof and close M1

**Ceremony (operator attended):**

1. Reconfirm listener health, `dry_run=true`, inactive `armed_until`, daemon health, and disabled
   emission.
2. Run the read-only sizing preflight against current state; the frozen expectation must be
   exactly one micro.
3. Prepare a fresh, unused ceremony for one approved source event.
4. The operator enables that ceremony.
5. Allow one ordinary evaluate-hook event and at most one ordinary B1 POST attempt.
6. Correlate the input, strategy signal, request, listener decision, and transport record.
7. Require `qty_out=1`, `dry_run=true`, `sender_invoked=false`, no live order, and no duplicate.
8. Disable/close the ceremony and reconfirm listener disarm and daemon disablement.

Any ambiguity, timeout, wrong quantity, duplicate, or missing correlation ends the attempt without
automatic retry. Preserve the evidence and return for adjudication.

**Resolution:**

1. Record the genuine listener event UUID in `dry_run_strategy_signal_event_id`.
2. Obtain explicit operator signoff; no agent infers or writes it on the operator's behalf.
3. Update the M1 artifact honestly and run both ordinary and `--require-resolved` validation.
4. Merge the resolution record.
5. Under a separate listener-deploy release, bake that exact resolved artifact into the listener.
6. Verify the deployed artifact digest and strict gate, with the listener still `dry_run=true`.

**Stop:** M1 is `RESOLVED`, but the rail remains disarmed. Track B, final `n3`, the separate
deployment GO, and operator arming remain outside Track A.

## Dependency line

```text
A1 source ruling + implementation
              ↓
A2 listener and daemon readiness
              ↓
A3 listener deploy (disarmed) → daemon deploy (disabled)
              ↓
A4 one attended dry-run → operator signoff → resolved-artifact re-bake
              ↓
STOP — no arm
```

Track B may proceed in parallel. The tracks join only after Track A has M1 `RESOLVED` and Track B
has winner-specific Phase 8 parity, before the fresh account snapshot and sole final `n3`.

## Session discipline

- Generate one bounded handoff immediately before each phase from this plan and current repository
  and live state. Do not pre-freeze later operational commands that may become stale.
- Every return states `DONE`, `NEEDS_OPERATOR`, or `BLOCKED`, lists exact checks, and confirms no
  unauthorized arm, send, deploy, or mutation occurred.
- Two failures on the same blocker stop the sequence for replanning.

## Canonical checks

```bash
python scripts/validate_c1_monitoring_acceptance.py \
  docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json
python scripts/validate_c1_monitoring_acceptance.py \
  docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json --require-resolved
pytest tests/ops/ tests/rail_crosstrade/ -q
git diff --check
```

The strict validator is expected to fail until A4 records the genuine event and operator signoff.
