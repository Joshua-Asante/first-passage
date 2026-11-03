# Fly.io — KEEP

**Class:** (d) meta-belt (subscription) · **Standing:** KEEP
**Aim served:** A1/A3 — hosts the rail listener + `c1-signal-daemon`
**Measure:** rail stays warm/deployed as required by pursuit a2
**Survive bound:** $ unverified — tracked as open in
[`SUBSCRIPTION_LEDGER.md`](SUBSCRIPTION_LEDGER.md) (C-1 still open for this row: asked
2026-08-21, not supplied); rides a2's $700 spend ceiling where applicable
**Review date:** none fixed — tied to a2
**Ratified:** 2026-08-09 (GSUB-1 Phase 3)

**Source:** [`GSUB-1 inventory`](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/docs/briefs/programs/GSUB-1-inventory-and-dispositions.md) row d13

## Retirement status - 2026-11-03

The KEEP/warm-host posture above is historical, superseded by the
[c1 staged retirement](../adr/2026-07-17-c1-rail-build-account-registration-go.md#addendum-2026-10-29--c1-retired-as-an-execution-route-staged-decommission).
The operator authorized verification, disarm and scale-to-zero on 2026-11-03.
The local attempt stopped at `fly apps list --json`: exit 1, `no access token
available`. Neither host state nor billing was obtained; no host was changed.
Stage 1 and its rollback interval have not been verified to start. Costs remain
open, not zero; stopped compute alone would not establish zero storage/IP costs.
CrossTrade cancellation remains the separate d14 operator report.
