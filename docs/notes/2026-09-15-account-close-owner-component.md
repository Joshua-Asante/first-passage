# Account-close durable owner component

Fourth component of the approved #395 split, following calendar #396, evidence
#398 and pure calculation #399. This component serializes acceptance and retains
its evidence; the calculator alone only proposes a close.

## Current review repair plan

Coordinator owns combined acceptance across the component stack. Starting owner
revision: `524fac1`. The source-to-calculation repair in #399 must reach this
owner's signed submission path; component tests alone do not establish acceptance.

- [x] Reproduce deletion/edit of authority rotation events and naive restore
  clocks through real SQLite restart/read paths. Bind all audit events in the
  history digest, updating the anchor atomically with every event; refuse old
  store formats unchanged rather than blessing unauthenticated prior events.
- [x] Reproduce an accepted empty source followed by correction, and preserve
  its exact bytes during invalidation, reviewed resolution and restart.
- [x] Reproduce malformed canonical package/envelope values and out-of-range
  B7 numbers. Refuse caller data before storage mutation or policy conversion;
  durable corruption must continue to raise `SettlementError`.
- [x] Restore the historical enrollment provenance without changing enrollment;
  align version guidance and test the affected owner/component suites.
- [ ] Integrate repaired upstream components, verify source-backed calculations
  and halt-required refusals through signed submission, and independently review
  the combined change before publishing. Actual venue qualification stays open.

## Signing without a dependency cycle

1. Assemble the evidence package (`account_close_package/v3`). It contains capture
   times and attestations, but no predicted operator signing time.
2. The owner issues `settlement_challenge/v2`, bound to the package digest and the
   current account, boot, generation, scope, sessions and policy/calendar digests.
3. On the operator device, review the package and challenge. Immediately before
   signing, call `settlement_signing.signing_envelope(challenge, signed_at=...)`
   with the current timezone-aware time. It adds `operator_signed_utc` without
   changing the issued challenge. Sign the canonical bytes of the entire result
   with the enrolled Ed25519 private key.
4. Submit that signed envelope unchanged with signature, key id, package and
   original source bytes. The owner checks the signature over every field, then
   matches the issued challenge after removing only `operator_signed_utc`.
5. The owner checks `issue <= signing <= receipt < expiry`; the pure verifier
   checks `capture <= issue` and the other evidence chronology. Acceptance retains
   the full signed envelope, signature and key id in the history-bound event.

Example on the operator device (the private key is already provisioned and stays
outside the repository/runtime):

```python
import json
from datetime import datetime, timezone
from settlement_signing import signing_envelope

reply = signing_envelope(challenge, signed_at=datetime.now(timezone.utc))
message = json.dumps(reply, sort_keys=True, separators=(",", ":"),
                     ensure_ascii=False, allow_nan=False).encode("utf-8")
signature = private_key.sign(message)
# Pass reply as submit(envelope=reply, signature=signature, ...).
```

Signing time remains operator-attested, not a trusted external clock. Clock
uncertainty refuses. No changes to the 300-second challenge or 30-minute source
freshness limits, signature authority, protection policy or activation gates.

## Corrections keep their source bytes

`record_revision(session_id=..., revised_package=..., sources=..., now=...)`
requires the correction record's `account_id` and `session_id`, a nonempty source
manifest, and exactly those original bytes. Every source binds `file`, `sha256`
and `account_id`; normal complete revised packages retain their richer source
metadata. Missing, mismatched, duplicated or undeclared sources refuse before
state changes. Timestamps supplied to the owner must be aware.

A correction is evidence that an accepted record is wrong, not an accepted
replacement close. It may contain contradictory economics or partial diagnostic
evidence; it cannot advance the close chain. The owner atomically retains it and
its sources, invalidates dependent closes, voids unused challenges and requests
a halt. This also supports a B7 correction record, whose resolution still needs
a separate reseal workflow.

Revision observations use a `settlement_revision/v1` wrapper containing the
exact revised package and source manifest. This gives the observation its own
digest without colliding with later acceptance of that same corrected package.
Previously superseded identical packages are reused only after verifying retained
content; each new acceptance still needs a fresh signature and current checks.

Every chain read verifies original and revised source bytes, including after
resolution moves the affected closes to the superseded archive and after restart.
The shared history digest covers revisions and all audit events, including
reconciliation, signed acceptance, authority rotation and restore. Each event
updates the anchor in its existing transaction. Reconciliation does not erase
either version or grant resumption. Corrections retain exact bytes, including
empty files that were previously accepted; they cannot silently discard them.

## B7 boundary

The effective close must be exactly 17:00 ET on the named weekday. `valid_until`
must equal 18:00 ET that day, or Sunday 18:00 ET after Friday. Derive this in the
ET timezone before converting to UTC: DST weekends can span 48 or 50 elapsed
hours. The existing ordering requires every capture and seal at or after the
close, at or before receipt, with receipt strictly before reopen.

## Versioning and acceptance limits

Store schema is v4; older stores refuse unchanged pending a reviewed migration.
Packages v1/v2 and challenge v1 are not silently upgraded. Reassemble fresh
packages and issue fresh challenges. Retained history is never rewritten to
manufacture compliance with the stronger protocol.

Synthetic tests cover actual Ed25519 signing, delayed construction/issue/signing,
tampering, replay, concurrent submissions, source retention, invalidation,
resolution, restart, and B7 weekday/DST boundaries. This is code-level evidence.
Actual report filter semantics, historical close equity, and live admission
qualification remain owed. No deployment or activation is authorized here.

Validation on the owner component: **1,990 operations tests passed, 15 skipped**,
with two upstream seaborn deprecation warnings. An independent reviewer accepted
the scope after reproducing the revision/readmission collision and rechecking
its repair; their focused owner run passed **162 tests**. Hosted CI is recorded
on the component PR separately.

That count describes the prior `524fac1` revision. The current owner repair
reproduced 23 failures, then passed 185 owner tests; a further older-store
compatibility regression also passes (53 focused repair tests). Combined
source-derived calculation and B7 inventory verification remain in progress.
