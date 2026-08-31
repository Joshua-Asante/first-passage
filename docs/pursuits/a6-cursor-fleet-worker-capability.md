# Cursor-fleet worker capability — KEEP

**Class:** (a) active campaign · **Standing:** KEEP
**Aim served:** A2/A4 — offload spec-freezable implementation packets to Cursor workers, CC stays orchestrator
**Measure:** packet claim-manifest completion rate; defect rate on dispatched packets (per the surface-allocation ADR)
**Survive bound:** Cursor subscription cost (see d16 — same underlying subscription, tracked once there)
**Review date:** per-packet, no fixed date
**Ratified:** 2026-08-09 (GSUB-1 Phase 3)

**Owner artifacts:** `cursor-fleet` skill · three frozen packets pending dispatch (2026-08-09: dense-1m entry lane, instrument lane, W1 re-run)

⚠ Status update 2026-08-31: all three 2026-08-09 packets have since run — dense-1m lane closed
CON-2 through CON-5 (all AMBIGUOUS-HOLD, 2026-08-10/11/12, Cursor + JA); W1 ADR Accepted
2026-08-22 with Class-S 0.50x RESULTS measured (`RESULTS_INTRADAY_W1.md`); instrument lane
closed MCL DEAD 2026-08-13 (MSL-S2A) and AMBIGUOUS-PARKED 2026-08-18 (Q-CONDVAL-1) — see
GSUB-1 inventory / respective closures for detail.

**Source:** [`GSUB-1 inventory`](../briefs/GSUB-1-inventory-and-dispositions.md) row a6
