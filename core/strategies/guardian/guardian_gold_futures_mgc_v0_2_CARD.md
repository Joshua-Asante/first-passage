# guardian_gold_futures_mgc_v0_2

**Family:** guardian
**Disposition:** PARKED_PROTOTYPE
**Body:** `core/strategies/_archive/guardian/`
**Supersedes:** `guardian_gold_futures_mgc_v0_1` (decision-grade use only — v0_1 retained hot as the sizing-fix-only record)

## Hash pins

- `60484f4f851758d79ea8677999f22f373dca3c52546e4ffbc5bb73406f84f160  guardian_gold_futures_mgc_v0_2_prototype.pine`

## Provenance

Adds F4 — a venue-mandatory EOD force-flat — to the v0.1 sizing/commission fix. All four
FRIENDLY firms auto-liquidate open positions daily at the platform level (Bulenox: no
overnight/weekend carry; Tradeify: 16:45 ET; MFFU: 16:10 ET; BluSky: ~16:45 ET); v0.1 still
inherited the locked file's `maxHoldBars=850` multi-day hold, which cannot execute as
backtested at any of these firms. This is a mandatory venue fact being modeled honestly, not
a signal-logic redesign: no re-entry-on-continuation mechanic was added for positions F4 cuts
short — the next session's re-entry still depends entirely on the untouched locked
`recoveryLong` signal re-firing. Every locked parameter remains byte-identical to v5.5.

**Still open, not resolved by this file:**
- N-SURV (trail-survival bust rate vs `Tradeify_Select_100K`'s $3,000 EOD trail) — not yet
  simulated on any panel; the block-bootstrap MC (mirroring `trail_survival_tradeify.py` from
  the Aegis→6J lane) is still owed.
- Session-filter timezone ambiguity (newly noticed, unverified): the locked v5.5 file's own
  session/hour/day gates use bare `hour`/`dayofweek`, which resolve in the chart's display
  timezone, not a code-guaranteed UTC. Not rewritten here — see the file's own header for why.
- Holiday-short calendar (Tradeify's 12:59 ET early-close days) not modeled.

## ADR

- `docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md` (R7 origin)
- `docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md` (R7 park, unchanged)
- `docs/adr/2026-08-04-strategy-coldstore-phase-a.md` (archive path convention)
