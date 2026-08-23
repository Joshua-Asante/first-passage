# Disaster-stop — Phase 0 empirical SIM, then Phase 1 `sl=` wiring

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**AUTHORIZATION:** Accepted ADR [`2026-07-28-c1-disaster-stop-payload-supported.md`](../../adr/2026-07-28-c1-disaster-stop-payload-supported.md) — Phase 0 is **operator-attended** on the real Tradeify eval. Phase 1 code is **gated on a recorded 0a PASS**. This plan does **not** set `dry_run=false`.

**Goal:** Execute (or record BLOCKED) Phase 0a/0b/0c from the ADR's own §7. Only after 0a PASS, land listener `sl=` + `protective_stop_placed` + tests.

**Architecture:** Phase 0 is procedure, not a code PR. Phase 1 is a one-field attach on the existing `build_crosstrade_payload` path. Primary exit stays `closeposition`. Base-entry only. No TP.

**Tech Stack:** Existing `ops/c1_rail/crosstrade_payload.py`, `c1_rail_listener.py`, `c1_rail_telemetry.py`, `tests/ops/`, `tests/rail_crosstrade/`.

## Global Constraints

- `docs/notes/rail_build/RUNBOOK.md` is **absent** from this public tree (claim-alignment M15 residue). **ADR §7 is the procedure owner.** Do not invent a new RUNBOOK as authority.
- Phase 0a uses the real eval account (CrossTrade has no separate paper dest). Minimum qty. Attended. In-eval P&L, not $700 ceiling — still real money.
- No Phase 1 `sl=` in the listener until a Phase 0 result is recorded in `docs/notes/rail_build/` **or** the ADR Change History.
- No `add` coverage. No `tp=`. No sizing-host change.
- Striker legs stay barred from *strategy-signal* deploy; this SIM is a payload-mechanics test, not a book redeploy. If operator judges §2 clause 3 of the 08-04 de-scope applies, **stop and escalate** — do not freelance.

## Rule 0 (verified 2026-08-23)

| Source | Anchor | What it pins |
|---|---|---|
| Disaster-stop ADR §7 | `56663b2` | 0a/0b/0c then 1a/1b/1c |
| `ops/c1_rail/crosstrade_payload.py` | `027a729` | `sl`/`tp` already payload-correct |
| `ops/c1_rail/c1_rail_listener.py` | `027a729` | no `sl=` yet |
| 08-04 de-scope Addendum | `2c3b3c5` | Bar is Striker-book redeploy, not all Tradeify-shaped work — still escalate if this SIM is judged redeploy |

---

### Task 1: Phase 0c (cheap, first)

- [ ] **Step 1:** `python scripts/check_pine_manifest.py` (and pin-provenance). Record result. Do not trust stale PORT_MANIFEST citations.

### Task 2: Phase 0b (parallel, non-blocking)

- [ ] **Step 1:** File the two CrossTrade-support questions (cross-command cancel; fire-while-flat). Record ticket id. 0a can proceed without the reply.

### Task 3: Phase 0a (operator only)

- [ ] **Step 1:** Halt if you are not the operator with attended access. Cloud/agent workers record `BLOCKED / capability-problem` and stop.
- [ ] **Step 2:** Place min-qty entry with `stop_loss=`, then separate `closeposition`. Observe whether the resting stop auto-cancels.
- [ ] **Step 3:** Write `docs/notes/rail_build/2026-XX-XX-disaster-stop-phase-0.md` with PASS / FAIL / AMBIGUOUS and raw observations. No `sl=` code in that commit.

If FAIL or AMBIGUOUS: **do not start Task 4.** Status path is ADR §6 (Withdrawn or stay pending). No "partial wiring."

### Task 4: Phase 1 (only after 0a PASS)

- [ ] **Step 1:** Failing tests: entry + submit + not halt → payload contains `stop_loss=` at `close - stop_dist_pts`; add/exit/flat do not; halt/submit-false do not.
- [ ] **Step 2:** `handle_signal` wires `sl=` for base entry only.
- [ ] **Step 3:** `protective_stop_placed` on `EventLedger` next to `decision`.
- [ ] **Step 4:** Tests green. `grep sl= ops/c1_rail/c1_rail_listener.py` now matches.

### Task 5: Phase 2–3 stay out of this PR

Dry-fire (`dry_run=true`) and first live-armed observation are operator sessions. Do not schedule them in a code PR.

## Verification

```bash
grep -n "sl: float | None" ops/c1_rail/crosstrade_payload.py
grep -n "stop_loss={sl}" ops/c1_rail/crosstrade_payload.py
# After Task 3 only:
test -f docs/notes/rail_build/*disaster-stop-phase-0.md
# After Task 4 only:
grep -n "sl=" ops/c1_rail/c1_rail_listener.py
pytest tests/ops/ tests/rail_crosstrade/ -q
```

## Forbidden moves

- Landing `sl=` before a recorded 0a result.
- `dry_run=false`.
- Attaching TP.
- Wiring add-leg stops.
- Editing the sizing host.
- Recreating RUNBOOK as a second owner.
