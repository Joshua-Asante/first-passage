# ADR — Five root roles; current work has one owner

**Status:** `Accepted` — operator-approved consolidation, 2026-09-08.
**Decision date:** 2026-07-16
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Format:** concise
**Revision:** 2026-09-08; [prior full decision](https://github.com/Joshua-Asante/first-passage/blob/4fb2b88f3b7d56d77463c43ba45c87ffadff6a31/docs/adr/2026-07-16-root-doc-charter-dedup.md). Root routing remains effective from 2026-09-06.

## Decision

Keep five root guides: README for human routing, CLAUDE for agent constraints and
essential safeguards, REPO_MAP for architecture/module entry points, PIPELINES
for workflows/handoffs, and STATE for current priorities and obligation pointers.
Do not add a sixth root guide or another state store.

[Rule 7](../operational_rules.md#7-one-canonical-owner-per-fact-every-other-mention-links-or-is-a-labeled-mirror) owns the root/STATE roles, dormant-thread protection and assistive-only memory boundary.
[STATE](../../STATE.md#operator-queue--strictly-ordered-5-live-items) owns the ≤5 concurrency Survive bound and dependency/operator order; campaign plans own executable next steps and campaign records own evidence and decisions.
[SESSIONS](../SESSIONS.md) owns append-only history and judgment-based logging; its living header routes to STATE, without queue-copy stubs.
[Gate operating contract](../../scripts/README.md#gate-composition-and-admission) owns manifest selectors, reachability, blocking versus audit tiers and structural M1 versus report-only tree skew.
[ADR admission](2026-08-08-adr-ceremony-tiering.md) permits a distinct record only for a durable architecture/governance/authority choice whose future-useful rationale cannot live clearly in an existing owner.

A specification, campaign, plan, PR or existing ADR may own a decision. Root guides
carry a useful consequence and owner link; they do not retell the decision. Record
choice does not supply evidence, approval or execution authority. Preserve unique
facts with an appropriate owner before removing their last committed home.

## Grounds

The June 3 STATE drift incident and July 16 duplicated posture narratives showed
that repeated facts become stale while their owners change. The September 6 routing
repair also removed a competing work queue from append-only session history.
Combining the five guides would couple different readers and update cadences;
folding STATE into memory or the journal would lose its consolidated dormant-thread
and forward-obligation view. Keeping pointers costs one owner-hop for detail.

If that demotion causes a documented material decision error, a dormant thread is
lost for lack of a home, or existing owners demonstrably cannot serve a load-bearing
need for a deleted STATE role, [Rule 7](../operational_rules.md#7-one-canonical-owner-per-fact-every-other-mention-links-or-is-a-labeled-mirror)
requires restoration of the affected role/block and matching ownership rule.

The A–D session classes and ~40-word prose targets, exact-two-STATE-headers hook,
and overlapping quarterly document-size/maintenance/stability reviews are
**retired by this revision**, not passed. The September 4 posture-size exception
was already discharged on September 6. Incident protection above remains; the
separate queue-attention review below remains owed.

## Queue-attention review

The portfolio Survive bound rations attention by concurrency, without an hours
budget or a time-metering subsystem. Its failure condition remains: a queue above
five items at two consecutive quarterly reviews, or repeated out-of-order serving.
Review queue history against dependency order and explicit operator direction;
record the finding and any needed correction with the owner. Queue placement,
completion or a failed review does not grant phase GO, open a replacement/channel,
or change the [M1 license and arming boundaries](2026-07-22-c1-venue-native-monitoring-maturity.md#addendum-2026-08-24--test-strategy-licensed-for-item-5-dated-08-24).

**Trigger check schedule:** 2026-11-08 — first queue-cap/attention and out-of-order review; retain the quarterly attention check, with the next dated check recorded here and in STATE when rolled.

## Current owner

The operating routes above replace the retired STATE-role, W5 and queue-cap
carriers; [tombstones](TOMBSTONES.md#2026-09-08-governance-consolidation) retain exact
historical bodies and obligation dispositions. Brief-checker/template unification
remains with the scripts guide; the unresolved 26-letter session-label ceiling
remains with the SESSIONS header and `roll_sessions.py`. H6 CI composition was
discharged on August 23; neither remaining issue was discharged with it.

Grounding: the four source ADRs, five roots, Rule 7, session rules, manifest/runner,
STATE and session readers, Sentinel schedule parser, retrieval consumers and
M1 validator/arm source were inspected at `5699cdaaa6ee325e287630cb7b63447da9dd9e1d`.
CLAUDE's Strategy Reference, Protection, Continuous improvement, historical MC
source read by `ops/recall/guard.py`, and old heading stubs remain unchanged.
This consolidation changes no risk, strategy, Pine or live execution authority.

Verification: `python scripts/check_root_doc_liveness.py`,
`python scripts/check_state_currency.py`, `python scripts/check_sessions_queue_bind.py`
and `python scripts/check_adr_graph.py`. These do not prove semantic equivalence,
queue-cap/order enforcement or Sentinel schedule coverage; inspect those directly.
