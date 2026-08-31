# Venue-edition ledger — `Tradeify_Select_100K`

Markdown, hand-maintained (same convention as `ops/instruments/*.md`). T2 (stale-vs-`LEG_MAP`) is the owning ADR's quarterly catch.

**Owner:** [`2026-08-05-strategy-venue-binding-axis.md`](../../docs/adr/2026-08-05-strategy-venue-binding-axis.md) §2.6 / §7 Phase 1.

**Live edition set is empty** — no row is live at this firm-tier. That is the §1.3 fact.

**Book authorization is unchanged.** Striker and Striker NAS100 stay `AUTHORIZED · MECHANISM @ 1.00×` at book level (canonical: [`strategy_lifecycle.md`](../../docs/methodology/strategy_lifecycle.md)). Venue-fit is not decay.

**ORB-MNQ-1** book entry is PARKED / payability FALSIFIED. `SCREEN-DEAD` here is edition-only (owning ADR §2.4 ruling 2) — do not read it as the book death.

| strategy | edition | state | cap_alloc | symbol | screen verdict + date | deployment |
|---|---|---|---|---|---|---|
| Striker | `Striker@Tradeify_Select_100K` | `WITHDRAWN` | 0 (was 69 — released 2026-08-26, [ADR](../../docs/adr/2026-08-26-striker-legmap-cap-release.md)) | MYM1! | venue de-scoped 2026-08-04 ([ADR](../../docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md)) | `leg_id=dj30_mym` RETIRED (rail retained, `dry_run=true`, F2 keep-warm) |
| Striker NAS100 | `Striker NAS100@Tradeify_Select_100K` | `WITHDRAWN` | 0 (was 11 — released 2026-08-26, [ADR](../../docs/adr/2026-08-26-striker-legmap-cap-release.md)) | MNQ1! | venue de-scoped 2026-08-04 ([ADR](../../docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md)) | `leg_id=nas100_mnq` RETIRED (rail retained, `dry_run=true`, F2 keep-warm) |
| ORB-MNQ-1 | `ORB-MNQ-1@Tradeify_Select_100K` | `SCREEN-DEAD` | — | MNQ1! | S7 occupancy SCREEN-DEAD 2026-08-04. Book-level payability remains FALSIFIED ([repark ADR](../../docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md)) — do not read SCREEN-DEAD as the book death | none — never deployed |
