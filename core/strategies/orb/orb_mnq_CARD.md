# orb_mnq

**Family:** orb
**Disposition:** FALSIFIED_PARKED
**Body:** `core/strategies/_archive/orb/`

## Hash pins

- `df05512deb959acf12b56bf27189b4cabea305c7e18b0d69c9927d45570c49e0  orb_mnq_v0_1.pine`
- `e3b3785734c68e5ef275846a0c9635b3146ebabe2d8b9710da9c8918b2f08056  orb_mnq_v0_2.pine`

## ADR

- `docs/adr/2026-08-04-strategy-coldstore-phase-a.md`

## Active research pointer (2026-08-31)

`core/strategies/candidates/orb_mnq_recon_v3.pine` (`MANIFEST.sha256` `be800cb4…`) is
the current best-known research iteration in the DD-reduction tuning lineage
(v1→v7) that diverges from this construct's own frozen parameters — the
reference candidate for further ORB-MNQ tuning work. **Not a lifecycle
change**: this construct's `Disposition`/`Body` above are untouched, recon-v3
is a distinct candidate, and it has its own measured result —
[`lab/analysis/orb/orb_mnq_recon_v3_2026-08-31/RESULTS.md`](../../../lab/analysis/orb/orb_mnq_recon_v3_2026-08-31/RESULTS.md)
— FAILS the live Tradeify survivor-scoring gate (bust ≤5.0%) at every
tested contract size (k=1 20.78% intraday-honest bust, 4.2× over). Not
authorized, not promoted, not cleared for capital.
