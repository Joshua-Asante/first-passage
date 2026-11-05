# INSTRUMENT LEDGER — M6E

**Symbol:** CME Micro EUR/USD futures. **Status:** research only. **Updated:** 2026-11-04.

## PROFILE (machine-readable)

```yaml
symbol: M6E
asset_class: fx-futures
family: []
venue_tradable: true
venue_note: "M6E is listed in Tradeify's published fee schedule. This is product availability, not a strategy deployment or account authorization."
k_bank_source: "../../discovery_manifests/"
cost_hurdle:
  value: 6.60
  units: "USD/round-trip/contract (exploratory assumption)"
  basis: "Tradeify 1.60 fees plus two adverse ticks per side at 1.25 per tick; not an observed spread."
  source: "#e1-fixed-european-morning-exploration"
structure:
  - claim: "One fixed European-morning breakout was evaluated without optimization or a holdout look. No candidate was submitted to validation. Restricted performance evidence stays private; independent review is pending."
    source: "#e1-fixed-european-morning-exploration"
```

## E1: fixed European-morning exploration

Direct operator authorization, 2026-11-04: run one fixed rule with $6.60 round-trip costs, register data, preserve R2's reserved sample, do not optimize.

- [Frozen rules and execution plan](../../docs/superpowers/plans/2026-11-04-m6e-fixed-exploration.md).
- [Input registration](../../lab/analysis/fx/m6e_european_breakout_2026_11/registration.json): 18 M6E1! M15 exports hash-registered; exactly nine 2016–2024 files allowed for scoring. Continuous contract and adjustment/roll mapping remain unverified.
- [Authoritative K manifest](../../discovery_manifests/m6e_european_breakout_fixed_20261104.json). One declared exploratory look. This external expression must be reconciled in any subsequent R2 registration; the builder's separate card ledger alone cannot establish no prior exposure. No fabricated builder card is added.
- Sample: 2016-01-04 through 2024-12-31. All 2025–2026 returns remain outside this experiment, conservatively protecting R2 D9's final approximately 378 sessions. The earlier audit inspected structural coverage, not returns.
- Related prior: [R2 Asia-to-London dossier at dba5b94](https://github.com/Joshua-Asante/first-passage/blob/dba5b9424a74f77c9897192f5cd4ebc6280c8e4a/docs/briefs/dossiers/R2/r2-m6e-asialdn.md). Its Asia range differs from this one-hour range; neither is independent evidence for the other. The dossier reports no established mechanism/effect estimate. Its M6A DL-2 stop-geometry warning motivates the report-only geometry diagnostic here.
- Historical cost prior: [M6B ledger W4](M6B.md#standing-warnings-read-first) records M6E's earlier third-leg E-COST rejection. That is a prior on cost feasibility, not a result for this fixed expression; the original archived study was not re-run here.
- [Result and private-evidence references](../../lab/analysis/fx/m6e_european_breakout_2026_11/RESULTS.md): the lab owner records permitted counts and hashes; full performance evidence stays private. No candidate was submitted to validation. Independent review remains pending; direction/year splits were diagnostic.

Contract units and costs, checked 2026-11-04: [CME FX product guide](https://www.cmegroup.com/markets/fx/fx-product-guide), EUR 12,500 contract and USD 0.0001/EUR tick = $1.25; [Tradeify fees](https://help.tradeify.co/en/articles/10468315-trading-commission-fees), $1.60 round trip.
