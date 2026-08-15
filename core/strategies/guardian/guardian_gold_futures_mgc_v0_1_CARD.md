# guardian_gold_futures_mgc_v0_1

**Family:** guardian
**Disposition:** PARKED_PROTOTYPE
**Body:** `core/strategies/_archive/guardian/`

## Hash pins

- `7a296676e0615c9852feac026fd985899f3db8739167d9162e3bc6f7f69fc120  guardian_gold_futures_mgc_v0_1_prototype.pine`

## Provenance

Venue-transfer prototype for the R7 self-funded Guardian→MGC lane, authored 2026-08-11
after running the LOCKED `guardian_gold_v5.5.pine` (XAUUSD) unmodified on the MGC1! chart
surfaced a ~10-13× position-sizing defect (`calcSize()` had no `syminfo.pointvalue`
reference — correct for XAUUSD/DXTrade, wrong for a native futures `qty`). This file
fixes the execution-mechanical layer only (sizing point-value division, commission,
contract-count cap, `initial_capital` aligned to `Tradeify_Select_100K`); every locked
signal/risk parameter is byte-identical to v5.5 (values redacted from the public tree
2026-08-14 — see the private archive). NON-CANONICAL — do not lock/deploy.

**Still open, not resolved by this file:** force-flat/no-overnight-carry at all four
FRIENDLY firms vs. this strategy's `maxHoldBars=850` multi-day-hold design — an
unresolved design question, not a defect fix. See the file's own header comment and
`docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md` §2 (R7).

## ADR

- `docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md` (R7 origin)
- `docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md` (R7 park, unchanged)
- `docs/adr/2026-08-04-strategy-coldstore-phase-a.md` (archive path convention)
