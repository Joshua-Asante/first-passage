# Belief formation and correction: bounded workflow replay

Date: 2026-09-08. Implementation: `0473a2349d4703b49bf0e0a7a36f4d9fb5e8175b`.
Continuation of the [retrieval replay](2026-09-08-evidence-retrieval-replay.md).

## Method and scope

An isolated exercise repository copied the real
[Q-XMEM-1 owner record](../briefs/Q-XMEM-1-cross-surface-memory-sidecar-pilot.md).
Two exact excerpts in its Limb B addendum supplied evidence: the tool's recorded
discovery benefit and its explicit exclusion as an attestation source. No new
measurement of that tool was performed.

Claims, review artifacts, assessments and the consuming decision were expressly
simulation-only. Synthetic ordered exercise times enabled historical checks;
they are not assertions about actual past reviews or effective times. The real
source owner's hash remained unchanged:
`9de272e287d83c0531870467d486d30066757b54f8dcf521a2b116802e99d36a`.

## Observed lifecycle

1. A deliberately broad exercise claim said keyword retrieval could establish
   that prior work had been checked. Its initial review was insufficient: a
   discovery benefit alone did not establish attestation authority.
2. A replacement assessment included the explicit authority restriction as
   challenging evidence and recorded contested. The challenge remained visible.
3. A new claim revision narrowed the role to source pointers with owner
   verification. It started unassessed, then received its own supported review,
   retaining the authority restriction as scope-limiting evidence.
4. Two citations from the same owner file produced one shared-source group;
   the tool did not treat them as independent evidence votes.
5. An exercise decision declared its dependency on the narrowed belief and
   recorded applied use through a retrieval receipt.
6. Adding a simulation marker to the copied source flagged the belief and
   consuming decision for review. The recorded supported judgment remained
   supported; the prior receipts remained exactly equal to their saved values.
7. Historical selection still returned the original insufficient assessment.
   Deleting and rebuilding SQLite reproduced the graph exactly.

## Queries exercised and Neo4j implication

| Workflow question | Mechanism exercised | Result |
|---|---|---|
| Which declared beliefs and decisions depend on this changed source? | Recursive SQLite impact plus reverse traversal of active exported graph edges | Identical record sets. |
| What assessment was known at an earlier point? | Belief `known_at`/`as_of` read | Original assessment retained. |
| Did several citations share preserved source bytes? | Belief evidence grouping | Shared source exposed explicitly. |
| What assessment and sources accompanied an applied belief? | SQLite join of use and receipt tables, inspection of pinned receipt fields | Found the exercise decision and its exact assessment/source versions. |
| Can the store reproduce these results after losing its index? | Journal replay and SQLite rebuild | Graph and earlier receipts preserved. |

The graph had 24 nodes and 38 edges. The verification segment completed in
approximately 0.34 seconds locally; this is an observation of a tiny fixture,
not a latency target or scale benchmark. No query in this exercise required a
Neo4j service. This supports continuing SQLite-first for these demonstrated
workflows; it does not establish performance for large graphs or many users.

Declared correction dependencies and reported use remain separate. The exercise
explicitly wrote both. The use/receipt join demonstrates that stored information
can support a future use-audit interface without treating all applied evidence as
an automatically declared substantive dependency. No such new interface is
claimed as implemented here.

## Evidence and continuation

Ignored local diagnostics:
`.cache/belief-workflow-c56dfdaf40c2441e92dfe2f544b91ab1/result.json`,
`use-query.json`, and its `store/` directory in the evidence-foundation worktree.
Receipts: `61cf6760-c127-413c-925e-84dbdc27d0e8` and
`c801027b-f66f-4adf-af5a-26a7bac7308f`.

Next integration priority is making these proven queries convenient in a real
decision review: connect source verification, the selected belief assessment,
receipt and explicit use to the review artifact. A use-audit query should expose
which decisions relied on earlier snapshots when a correction arrives. Retain
the Neo4j projection contract; introduce its runtime only against a demonstrated
query or operational need. Numeric confidence still requires an evidence-specific
measurement contract. No live workflow, automatic decision authority, measured
operator benefit or causal learning claim follows from this exercise.
