# Cursor-fleet worker capability — KEEP

**Class:** (a) active campaign · **Standing:** KEEP
**Aim served:** A2/A4 — offload spec-freezable implementation packets to Cursor workers, CC stays orchestrator
**Measure:** packet claim-manifest completion rate; defect rate on dispatched packets (per the surface-allocation ADR)
**Survive bound:** Cursor subscription cost (see d16 — same underlying subscription, tracked once there)
**Review date:** per-packet, no fixed date
**Ratified:** 2026-08-09 (GSUB-1 Phase 3)

**Owner artifacts:** `cursor-fleet` skill · three frozen packets pending dispatch (2026-08-09: dense-1m entry lane, instrument lane, W1 re-run)

⚠ Status update 2026-08-31: all three 2026-08-09 packets have since seen dispatch and partial
progress — none is fully closed. Dense-1m lane: CON-2 through CON-5 closed (all AMBIGUOUS-HOLD,
2026-08-10/11/12, Cursor + JA). W1 re-run: ADR Accepted 2026-08-22 with Class-S 0.50x RESULTS
measured (`RESULTS_INTRADAY_W1.md`) — but 3 of its 4 decisions of record, plus the `firm_rules`
caveat update, remain owed per the ADR's own §6 gate. Instrument lane: two individual mechanism
tests closed (MCL DEAD 2026-08-13 per MSL-S2A; a separate AMBIGUOUS-PARKED 2026-08-18 per
Q-CONDVAL-1) — but the lane's own instrument-election decision is still pending operator election
(GSUB-1 inventory Addendum: "election left to operator"), and the ledgers themselves remain open
(`MCL.md`: OPEN — geometry-cleared, mechanism-owed; `MES.md`/`MGC.md`: RE-ENTERED — not elected).
See GSUB-1 inventory / respective closures for detail.

**Source:** [`GSUB-1 inventory`](../briefs/GSUB-1-inventory-and-dispositions.md) row a6
