# Disaster-stop Phase 0 — recorded BLOCKED

**Date:** 2026-08-23
**Owner ADR:** [`2026-07-28-c1-disaster-stop-payload-supported.md`](../../adr/2026-07-28-c1-disaster-stop-payload-supported.md)
**Plan:** [`2026-08-23-disaster-stop-phase-0-1-implementation.md`](../../superpowers/plans/2026-08-23-disaster-stop-phase-0-1-implementation.md)
**Procedure owner:** ADR §7 (no second RUNBOOK)

| Limb | Result | Why |
|---|---|---|
| **0a** empirical SIM (real eval, min-qty `stop_loss=` then separate `closeposition`) | `BLOCKED / capability-problem` | Cloud/agent worker has no attended Tradeify/CrossTrade access. Plan Task 3: halt and record. Not PASS / FAIL / AMBIGUOUS. |
| **0b** CrossTrade-support questions (cross-command cancel; fire-while-flat) | `BLOCKED / capability-problem` | No operator identity to file a vendor ticket from this session. 0b is corroborating, not a 0a blocker. |
| **0c** `check_pine_manifest.py` (+ pin-provenance) | Ran | Exit 0 both. WARN: no Pine source on this public clone — manifests not verified against disk. Do not treat PORT_MANIFEST citations as freshly disk-checked. |

**Phase 1 `sl=` wiring:** not started. Plan forbids it until a recorded 0a PASS. Listener still has no `sl=`. Payload builder already accepts `sl: float | None` and emits `stop_loss=` when set.

**Not done (and not claimed):**
- `dry_run=false`
- TP attach
- add-leg stops
- sizing-host edit
- new RUNBOOK as a second owner
- 08-04 de-scope book redeploy (this would have been a payload-mechanics SIM; it did not run)

**Operator resume:** attend 0a on the real eval (ADR §7). Only a PASS unlocks Phase 1 tests + listener `sl=`. FAIL or AMBIGUOUS stays on ADR §6 — no partial wiring.
