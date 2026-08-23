# Q-S5CAP-1 — verdict pre-registration

**Frozen:** 2026-08-23, before Phase 1 result inspection — the gate criteria below are
transcribed verbatim from `Q-S5CAP-1-capped-concurrency-invariant.md` §6, which was itself
written and locked on 2026-08-18, five days before this pre-registration and Phase 1
execution. No criterion here was chosen or adjusted after seeing any
`validate_promotion_packet()` / `refute_promotion_packet()` output.

**Process note (honest disclosure, matching the Q-GATESTACK-1 precedent):** operator GO was
recorded this session ("open and run this Pre-Q brief's Phase 1"), and this pre-registration,
Phase 1 execution, and verdict assertion happened inside the same investigative session
rather than as three cleanly separated turns. As with Q-GATESTACK-1, the *content* of this
pre-registration could not have been shaped by the results — §6's gate table was already
frozen in the brief's own text on 2026-08-18, four days before this session began, and is
transcribed below byte-for-byte from that frozen text, not re-derived. The letter of
"committed, then Phase 1 run, as two separate steps" (brief §7) was not observed as two
distinct turns; recorded here rather than presented as clean two-step sequencing.

---

## Frozen gate (verbatim from §6)

| Verdict | Trigger condition | Disposition (typed) |
|---|---|---|
| `RESOLVED` (Accept H-S5CAP) | Both Limb-V and Limb-R Pass all N≥3 synthetic packets; Section 0 code reads confirm no cross-packet state anywhere in either call path | `INTEGRATE` — record "capped concurrency" as **per-packet self-report only, not a system invariant** in the S5 lifecycle owner/CLAUDE.md pointer row; name (do not open) a successor decision packet for whether/how a real counter is wired, gated on M1 `RESOLVED` per the ADR's own §6. No code changes under this brief. |
| `FALSIFIED` (Reject H-S5CAP) | Limb-V or Limb-R Fails a packet past the 2nd, for a concurrency-attributable reason | `STOP` — the property already binds at the system level for the failing function; close with the mechanism identified (it was missed by direct source read and needs correction to Section 0), and check whether the other limb still needs a separate verdict. |
| `AMBIGUOUS-HOLD` | Sequential run cannot complete cleanly at $0 (unrelated schema/path failure blocks the clone sequence) | `ITERATE` — record the blocking defect, fix the fixture-clone mechanics only (no production code), and re-run Phase 1 before any verdict is asserted. |

## Hypothesis statement (verbatim from §4)

**H-S5CAP:** If Limb-V holds (`validate_promotion_packet()` returns Pass on all of N≥3
synthetic packets, each self-declaring `concurrency_slots=1`, run sequentially with no shared
state between calls) AND Limb-R holds (`refute_promotion_packet()` also returns Pass on the
same N≥3 packets, same sequence) — then the "capped concurrency" property is a per-packet
self-report only, sequential admits silently exceed the declared `max_concurrency=2`, and the
S5 ADR's blast-radius argument is currently missing its third factor as a system invariant.

**Reject H-S5CAP if:** Limb-V or Limb-R Fails any packet beyond the 2nd in the sequence, for a
reason attributable to cumulative concurrency (not an unrelated schema defect in the clone).

## Execution commitment

Phase 1 runs exactly the §7/§10 script: clone `tests/fixtures/promotion/clean_packet.json`
three times (N=3, no larger — §5 forbids inflating N "to make it more convincing"), each
clone individually declaring `concurrency_slots=1` (legal within a single packet; cumulative
across the 3 clones = 3, which exceeds `max_concurrency=2` — the only way a real cross-packet
counter could reject one of them), call `validate_promotion_packet()` then
`refute_promotion_packet()` on each clone independently, in sequence, in a local Python REPL,
no repo mutation, no commit, no data pull. The verdict is read mechanically off the frozen
table above against that output — no re-framing after the fact.
