# Head of Execution — Decision Log

Append-only. One entry per review. See
[design spec §6.4](../superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md) for the format
contract and [`INDEX.md`](INDEX.md) for this persona's definition.

**First-ever entry** — no prior log existed; stated explicitly rather than fabricating history.

## 2026-08-19 — c1-rail deployed-vs-main skew, execution record (not a panel review)

**Type:** Execution record, not a reviewed-artifact verdict — this entry departs from this log's
usual shape because the underlying work was direct CC execution within this seat's Domain
(`ops/c1_rail/`, primary owner per `docs/personas/ownership-map.md`), not an independent persona
spawned to review someone else's proposal. Logged here anyway because it is exactly the kind of
domain-owned finding this log exists to carry forward.

**What happened:** the weekly c1-rail safety check (agenda item 2 from the C-suite's proposed
weekly agenda) surfaced that `ops/c1_rail/c1_rail_arm.py` was unreachable in-container — the
deployed image was still the 2026-08-02 04:26 UTC build, 17+ days stale, flat pre-08-03 layout.
Walked all six `c1-rail` skill deploy preconditions in order, host-verified throughout (`dry_run`
confirmed true before and after, import closure re-traced 16/16 covered, deployed from `main` @
`31fd642`, boot line + health verified, crash-loop recovery path reviewed though inapplicable since
`armed_until` was `None` going in). Redeployed cleanly; `fixture_hashes` re-pathed and refreshed
from fresh in-container hashes — `--check-tree-skew` now reports `tree skew: none`.

**Confirmed findings:** 1 — deployed-vs-`main` skew, open since at least 2026-08-09 (RUNBOOK had
already flagged it; nothing redeployed in the 17 days since). Closed same session.
**Ratified as recommended:** n/a — this was execution of an already-standing operator grant (the
`c1-rail` skill's 2026-08-02 agent-authority table), not a proposal requiring ratification. Operator
(Joshua) drove the SSH/deploy commands throughout; I lack Fly credentials in this session by design.
**Rehearsal:** no — real, live-infrastructure action with real effect (image redeployed).
**CRO hard block fired:** no — see `cro-log.md` same date; independently confirmed no safety
invariant was touched.
