# `core/data/bar_data/` — frozen CME micros only

Derived M15 OHLC panels for CME futures micros. CSV bytes are **gitignored**
(vendor TOS); only `SHA256SUMS` (and this README) are tracked.

| Panel | Instrument | Disposition |
|---|---|---|
| `6J_M15.csv` | CME 6J | **KEEP · FROZEN** (Aegis lane PARKED; historical + ledger) |
| `MCL_M15.csv` | NYMEX MCL | **KEEP · LANDED 2026-08-13** — CME BAR EXPORT v0.2 `MCL1!` (`…_3fd7c.csv`), operator-supplied; 106,261 bars, span 2022-01-02T23:00Z→2026-07-02T00:00Z; sha256 `5aa50456…bbd23`. Sidecar `MCL_M15.meta.json` pins `mintick 0.01 · pointvalue 100 · tz America/New_York`. ⚠ Panel **ends 2026-07-02**, ~6 weeks before its export date — any CONFIRM window must end at the panel, not at "today" |
| `M2K_M15.csv` | CME M2K | **KEEP · LANDED 2026-08-13** — CME BAR EXPORT v0.2 `M2K1!` (`…_14faf.csv`), operator-supplied; 106,131 bars, span 2022-01-02T23:00Z→2026-07-02T00:00Z; sha256 `81922570…12349`. Sidecar `M2K_M15.meta.json` pins `mintick 0.1 · pointvalue 5 · tz America/Chicago`. ⚠ Panel **ends 2026-07-02** — CONFIRM reserved through 2026-08-13 in G0 but unread bytes stop at panel end |
| `MGC_M15.csv` | COMEX MGC | **KEEP · LANDED 2026-08-12** — CME BAR EXPORT v0.2 `MGC1!` (`…_76a31.csv`); span 2022-08-01→2026-08-12 UTC; sha256 `88da9f15…caf3f3` |
| `MNQ_M15.csv` | CME MNQ | **KEEP · FROZEN** (c1 / Striker NAS venue edition research) |
| `MYM_M15.csv` | CBOT MYM | **KEEP · FROZEN** (c1 / Striker DJ30 venue edition research) |

**Pepperstone producer is dead.** `scripts/parse_bar_export.py` defaulted to
Pepperstone `bar_export/` inputs retired 2026-08-02
([Pepperstone feed ADR](../../../docs/adr/2026-08-02-pepperstone-feed-retirement.md)).
`6J` / `MNQ` / `MYM` are **usable but not regenerable** without an offline
restore. **MGC** was landed via explicit `--in` from a fresh CME BAR EXPORT
(see [`docs/notes/2026-08-12-guardian-mgc-nsurv-bar-derived-intraday-prep.md`](../../../docs/notes/2026-08-12-guardian-mgc-nsurv-bar-derived-intraday-prep.md)).

**CFD-era panels deleted 2026-08-03** (`US30*`, `NAS100*`, `USDJPY*`, `XAUUSD*`,
`XAGUSD`) — owning ADR
[`docs/adr/2026-08-03-bar-data-cfd-and-candidates-retirement.md`](../../../docs/adr/2026-08-03-bar-data-cfd-and-candidates-retirement.md);
hashes in
[`docs/ltm/notes/2026-08-03-bar-data-cfd-candidates-tombstone.md`](../../../docs/ltm/notes/2026-08-03-bar-data-cfd-candidates-tombstone.md).

Integrity gate: `python scripts/check_data_manifests.py --check` (regen + commit
`SHA256SUMS` in the same commit as any CSV change).
