# guardian_gold_futures_mgc_v0_3

**Family:** guardian
**Disposition:** PARKED_PROTOTYPE
**Body:** `core/strategies/_archive/guardian/`
**Supersedes:** `guardian_gold_futures_mgc_v0_2` (decision-grade use only — v0_1/v0_2 retained hot as provenance)

## Hash pins

- `0f0aa81712baacd5080092c009b937c0416b029ce181ab53ddd194980871c56d  guardian_gold_futures_mgc_v0_3_prototype.pine`

## Provenance

Fixes F5: v0.2's EOD force-flat (16:45 ET target) filled ~75 minutes late on every one of
199 exits, landing at 18:00 instead. Root cause confirmed by web search — CME Globex halts
electronic trading 17:00-18:00 ET Monday-Thursday for daily maintenance; v0.2's close signal
fired correctly pre-halt, but `process_orders_on_close=false` defers the fill to the next
bar's open, and the next bar after the halt-window gap is the 18:00 reopen. Same defect
class and fix shape as the Aegis→6J port's own F1 (EOD cutoff firing on a post-maintenance
bar). Default `flatMinuteET` moved 45 → 15: the signal now fires at 16:15 ET and the fill
lands ~16:30 ET, a 15-minute/one-bar buffer clear of both the true 16:45 ET deadline and the
17:00 ET halt.

Also adds a dashboard row displaying `syminfo.timezone` directly — the still-open question
of whether this COMEX symbol's bare `hour`/`dayofweek` (used by the locked file's own
session/hour/day gates) resolve in UTC as documented, or in `America/New_York` as the
entry-hour clustering suggests, can now be read off the chart instead of inferred.

**Still open, not resolved by this file:**
- Session-filter timezone — dashboard now shows `syminfo.timezone`; still needs a human to
  read it and decide whether the locked file's gates need attention (not touched, per Rule 0).
- N-SURV (trail-survival bust rate vs `Tradeify_Select_100K`'s $3,000 EOD trail) — use
  `lab/research_utils/nsurv_channel.py` (W1-pin-proven), not a bespoke harness.
- Cell-level pre-registration (Q-TXG-1 §5 shape) still owed — see `docs/pursuits/b8-guardian-mgc-transfer-lane.md`.
- Holiday-short calendar (Tradeify's 12:59 ET early-close days) not modeled.

## ADR

- `docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md` (R7 origin)
- `docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md` (R7 park, unchanged)
- `docs/adr/2026-08-04-strategy-coldstore-phase-a.md` (archive path convention)
- `docs/pursuits/b8-guardian-mgc-transfer-lane.md` (RATIFIED PARK, this cell's governing record)
