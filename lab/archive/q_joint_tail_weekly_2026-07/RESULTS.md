# Q-JOINT-TAIL-WEEKLY — RESULTS

**Verdict: RETIRED — §9 panel-shape sanity gate FAILED at authoring time, before any CC handoff. Canonical closure: [docs/briefs/closures/Q-JOINT-TAIL-WEEKLY-closure-retired.md](lab/archive/../../docs/briefs/closures/Q-JOINT-TAIL-WEEKLY-closure-retired.md).**

This card exists so the study carries a machine-readable disposition; the
closure brief above is canonical for the reasoning.

## What this directory holds

`sanity_check.py` — the pre-registered §9 authoring-time gate itself. It read
the Pepperstone anchor panels to check weekly panel shape, failed, and the
parent Pre-Q's own §7/§9 branch ("§9 fails → RETURN TO PRE-Q / RETIRE, mirror
Q-JOINT-TAIL-1") retired the question. No further harness was built and no
verdict was drawn from the data.

## Archive rationale (2026-07-22)

Retired at closure, and an anchor consumer: `sanity_check.py` reads the four
2026-05-24 Pepperstone panels that
[ADR 2026-07-22 challenge-era substrate retirement](lab/archive/../../docs/adr/2026-07-22-challenge-era-substrate-retirement.md)
disposition C retires. Archived rather than migrated — the question is closed,
so there is nothing to re-point at synthetic fixtures.

**Predecessor:** Q-JOINT-TAIL-1 (closed BLOCKED-RETIRED 2026-05-27 at daily resolution).
**Parent Pre-Q:** [docs/briefs/2026-05-27-q-joint-tail-weekly-pre-q.md](lab/archive/../../docs/briefs/2026-05-27-q-joint-tail-weekly-pre-q.md)
