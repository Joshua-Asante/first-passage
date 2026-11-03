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
The earlier local attempt stopped at `fly apps list --json`: exit 1,
`no access token available`; that attempt made no host changes.
The later operator-run [Stage 1 record](https://github.com/Joshua-Asante/first-passage/blob/4af558dc0692834ff4daa8b314fa4a19503b4489/docs/adr/2026-07-17-c1-rail-build-account-registration-go.md#stage-1-record--2026-11-03)
reports disarmed configs, scale-to-zero, empty machine lists and endpoint
timeouts at 14:55 UTC. This reconciliation did not independently query Fly.
The reported rollback window starts November 3, with review around November 17;
Stage 2 requires a separate operator decision. Billing and remaining resources
are unverified: potential charges are not limited to volumes. Costs remain open,
not zero. CrossTrade cancellation remains the separate d14 operator report.
