# Evidence retrieval: bounded Q-XMEM-1 replay

Date: 2026-09-08. Implementation: `1d441b372a73c1aa7891b9ab2b5b835d2e705189`.
Purpose: exercise continuity, contextual relevance and correction on actual
First Passage documents before choosing the next belief-assessment interface.
This is a replay with simulated use and source drift, not a live decision,
reopened pilot, new measurement or change to an owner ruling.

## Source scope

- [Pursuit disposition](../pursuits/c1-q-xmem-1.md): pursuit-layer SUBTRACT.
- [Pilot record](../briefs/Q-XMEM-1-cross-surface-memory-sidecar-pilot.md):
  Limb B's separate ASSISTIVE-ONLY ruling, cited at the dated addendum heading.
- [Approved integration design](../superpowers/specs/2026-09-08-evidence-retrieval-design.md):
  the existing decision used as the replay's target for reported evidence use.

All three were copied into a separate local exercise repository. SHA-256 checks
before and after confirmed the real source files did not change. The exercise
used observation time as the effective time of its annotations; it did not
reconstruct unknown historical intraday effective times.

## Observations

| Case | Result |
|---|---|
| Retrieve with pursuit Q-XMEM-1 and limb B | Both records matched; ASSISTIVE-ONLY and SUBTRACT remained separate dispositions. |
| Retrieve the limb record with only pursuit context | Applicability remained unknown because limb was unspecified. |
| Report use against the integration decision | Pursuit closure was marked applied; tool result was marked not applied as sufficient prior-work attestation, each with a replay-only reason. |
| Append a simulation marker to the copied pilot document | The integration record acquired `dependencies_need_review` through its declared tool-record dependency. |
| Read the original receipt after the simulated change | Original receipt was exactly equal to its saved value. |
| Delete SQLite and rebuild | Graph export was exactly equal, including receipt/use relationships. |
| Hash original source owners again | All three hashes were unchanged. |

Local observation time: `2026-09-08T19:16:10.458858+00:00`.
Receipt: `77cfeba3-ee38-4a70-8c58-48ad00fb7d93`.
Use event: `00559902-71b9-4943-a644-2ccf0b737c13`.
Detailed results and durable exercise store are under the ignored directory
`.cache/evidence-replay-d653c5b02bbc482bbe36cfd0a6517ac2/` in the evidence-foundation
worktree. They are local diagnostics, not published evidence inputs.

Source hashes, in the order listed above:

```text
aa1334485179e2f30e9db0e5d6dab8d79fe344afc742c1f2c09abd729752e015
9de272e287d83c0531870467d486d30066757b54f8dcf521a2b116802e99d36a
926cfc5d8151253000e937e9694c3ff41999c04fd1f6ced51b37f83b732b49a3
```

## What this establishes for the next slice

The mechanics preserve distinct scopes, explicit unknowns, past observations and
current correction warnings for this case. The source-drift finding is
conservative: adding a marker changed bytes without changing a ruling. It
therefore correctly requests review rather than declaring an old result false.

Reported use is not an evidence judgment. In this case `not_applied` means the
tool is insufficient for one proposed role; it does not mean its measured result
is false or that the tool has no utility. A belief interface needs separate
supporting, challenging and scope-limiting evidence relationships, tied to exact
revisions and accompanied by reviewed rationale. Counting uses or matching
conditions would not establish belief confidence or independent evidence.

This single replay does not measure corpus recall, demonstrate reduced operator
time, establish general learning performance, or test a Neo4j service. No further
implementation has been added in this continuation; belief-assessment semantics
are the next design decision.
