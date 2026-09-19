# S1 recovery repair

**Selected outcome:** Resolve the coordinator's two recovery findings with persisted, charged recovery semantics; no process launch or signing.

**Prerequisites:** Reviewed S1 snapshot c95d902e67624a25a1a087d4f20dc50449efc8a3ffa772c04aead365eb5d80b9 restored at merge 1e4928360b95812b04725dc1e8da97709d670ff4. Original checkout was removed; immutable packet is preserved. Doctor: Python 3.13.2, 62 packages.

**Ownership:** Coordinator implements inline and retains S1 review and combined acceptance; independent reviewer checks the corrected interface. No S2 assignment.

**Verification:** First regressions for settled START_INTENT/RUNNING/CAPTURED recovery, new boot/downtime/duplicate/changed counters; linked signing retry, charge retention, interrupted retry, immutable intent, serialization and VOID. Then required five-file S1 pytest selection, check, diff whitespace. Inspect completed source-bound records and preserve outside worktree.

**Checkpoint:** Preserve revised schemas and proof in a new recovery packet. Escalate only a scope conflict outside this assigned persisted interface.

**Return boundary:** Locally verified S1 repair and review. Exclude S2, real OS enforcement, actual signing/publication, remote actions, merges, deployment and accounts.

## Design and steps

1. Recover already-settled work without resettling: validate current attributed observation, preserve immutable charge, observe fresh clock/memory/OOM, mark changed known CPU as uncertain. No capture means IN_DOUBT before cleanup. Repeated unchanged recovery has no event.
2. Extend the closed reservation object with optional signing_retry_of. The linked work must use the parent's phase and fixed payload hash, and parent must have settled SIGNING_INTENT without candidate. One retry at a time, original fixed intent stays locked. Retry work cannot create signing intent/candidate or stochastic work. Known interrupted retry is ABORTED without reviving any authority; unknown usage remains terminal. Fresh linked reservations use original allowance and unique work scopes.
3. Linked retry bookkeeping preserves the prepared authority token; terminal resource facts still invalidate it. Parent candidate/finalization waits for every linked retry to close and settle. Common transaction serializes VOID.
4. Extend canonical snapshot parser to validate links while retaining old unlinked snapshot readability. No database layout change. Document downstream retry sequence, then independently review and preserve completed evidence.

Related cases: settlement remains byte-idempotent; recovery may observe current facts without mutating settlement. Reserved recovery unchanged. Captured recovery never redraws. Linked retries are deterministic signing work only, not a loophole for another N1/N2/PART_A operation. Existing dormant/N1 layouts remain intact.

## Final private recovery interface

Existing method signatures remain unchanged. `recover_work` accepts fresh attributed observations after prior settlement: it preserves the original observation/charge, observes current clock and parent memory/OOM, and treats changed known CPU as uncertainty. A missing new CPU counter does not erase a known final charge; missing current parent memory/OOM is fail-closed. Unchanged repeated recovery adds no event. Original START_INTENT/RUNNING still becomes IN_DOUBT before cleanup; captured bytes remain unchanged.

`reserve_work` accepts either the original closed reservation object or its explicit linked variant with `signing_retry_of`. A linked reservation uses the original parent's phase limits, input_sha256 equal to SHA256 of its fixed signing payload, a new work ID and subsequently a new work scope. The parent must be settled SIGNING_INTENT, with no candidate or open retry. N1/N2/PART_A and nested retry parents are prohibited. Reuse exact reservation bytes for idempotent retry.

First linked reservation atomically advances the logical snapshot to qualification_campaign_budget_snapshot/v2; v1 history stays unchanged and readable. v1 rejects linked fields. SQLite remains exact v6; no table migration or downgrade. Old readers reject v2 safely. Preserve pre-change databases if rollback to old code is required.

Consumers run only the fixed deterministic signer for linked work. Child START_INTENT/RUNNING/COMPLETED are charged but do not change the prepared authority token. Child recovery with known final usage closes it ABORTED so another linked reservation can retry; unavailable usage charges the full reservation and makes the campaign uncertain. Parent SIGNED/COMPLETED is barred until every linked child is closed and settled. Other work remains blocked by the fixed intent. Terminal accounting, deadline and VOID still invalidate authority. All children and the original work retain their own immutable final charges; the campaign cap never resets.

A settled process interval is no longer timed as running during later custody/recovery; settlement already checked its phase wall limit. Each retry has its own phase timer and the original campaign deadline. Save exact candidate only after child settlement/closure, then finalize the original work under the existing transaction and token. Actual signature verification, current keys/approvals, supervision and publication remain downstream responsibilities.
