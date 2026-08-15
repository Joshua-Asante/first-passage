# Closed-loop programme — spec index (2026-08-07)

Objective: move the programme from operator-stepped research to a budgeted closed loop at
the live `Tradeify_Select_100K` eval — generate → validate → sandbox-deploy → measure,
automated within operator-set ceilings; rule changes stay human.

Status: S1+S2+S5 `RESOLVED` (ADRs Accepted; S5 + validator fixtures); S2b `Accepted`
2026-08-08 (build still needs build ADR + operator GO) · S3–S4+S6–S7 `PROPOSED` · S3
scaffold `CODE_LANDED` 2026-08-07 (Gate RESOLVED still needs first family TV anchor) ·
**S7 Phase 7:** W1 `Proposed` · W3 blocked · W4/W5/W6 `Accepted` (sweeps in progress on
branch) · authorize nothing beyond Accepted lane doctrine ($0 · K=0) · each spec styled
per [TEMPLATE-minimal-spec.md](TEMPLATE-minimal-spec.md) (standing convention, ratified
JA 2026-08-07 — recorded in `STATE.md` decision index + `docs/SESSIONS.md`).

| # | Spec | One line | Depends |
|---|---|---|---|
| S1 | [environment ratification](2026-08-07-loop-s1-environment-ratification-spec.md) | F2+F3 ruled: rail kept warm, incumbent eval = the environment | — |
| S2 | [signal-host fork](2026-08-07-loop-s2-signal-host-fork-spec.md) | Python-native ruled; M1 item-5 origin expressly superseded | S1 |
| S2b | [Python signal daemon](2026-08-07-loop-s2b-python-signal-daemon-spec.md) | bar source · B1 contract · heartbeat · fail-closed · second Fly app; no build alone | S2 |
| S3 | [arbiter, two-tier](2026-08-07-loop-s3-arbiter-two-tier-spec.md) | Python engine = research authority per family; eval fills = deployment truth · **scaffold CODE_LANDED** (`parity_gen2_2026-08/`); Gate RESOLVED → first family TV anchor | S2, S4 |
| S4 | [sensor layer](2026-08-07-loop-s4-sensor-layer-spec.md) | M1 → RESOLVED; execution-quality fields captured from fill one | S1 |
| S5 | [bounded promotion lane](2026-08-07-loop-s5-bounded-promotion-lane-spec.md) | automation promotes into a capped sandbox; ceiling-crossings stay operator-only | S1, S4 |
| S6 | [K-aware generation](2026-08-07-loop-s6-k-aware-generation-spec.md) | corridor + DSR-cap arithmetic executable at campaign-open | — |
| S7 | [repo alignment](2026-08-07-loop-s7-repo-alignment-spec.md) | each ruling lands with its propagation sweep, from a pre-built manifest | consumes all |

Series boundary (the recursion line): automation improves candidates and sandbox-budget
allocations within operator-set ceilings (locked `BASE_RISK`/allocation constants
untouched) and may *propose* rule changes with evidence packets — it never enacts them;
gates, budgets, ceilings, and the reflex layer (`dry_run` interlock · `armed_until` ·
fresh idempotency tags) change only by ADR + operator; attended-only posture and the
per-armed-session operator GO stand until a separate ADR replaces them.
