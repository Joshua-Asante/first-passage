# `core/data/bar_data/` — frozen CME micros only

Derived M15 OHLC panels for CME futures micros. CSV bytes are **gitignored**
(vendor TOS); only `SHA256SUMS` (and this README) are tracked.

| Panel | Instrument | Disposition |
|---|---|---|
| `6J_M15.csv` | CME 6J | **KEEP · REFRESHED 2026-09-03 (2nd capture)** — CME BAR EXPORT v0.2 `6J1!` (`…_ed300.csv`), operator-supplied; 94,805 bars, span 2022-09-01T23:00Z→2026-09-03T00:00Z; sha256 `94d237cc…a54bc`. Sidecar `6J_M15.meta.json` pins `mintick 5e-7 · pointvalue 12,500,000 · tz America/Chicago`. **Encoding-precision trap fixed**: the TV harness's OHLC format was widened from a fixed 5dp literal (`"#.#####"`) to `format.mintick` (renders at 6J's own 7dp tick precision). Evidence: tick-multiple test (`ticks = price/mintick`; `ticks % 20 == 0` share) reads **0.0475–0.0499** across open/high/low/close, matching the ~0.05-by-chance expectation for arbitrary-precision encoding (was ~1.0 pre-fix); `flat_frac` is **0.000105** (was 0.5121); `max_close_decimals` is **7** (was 5); an independent cross-check against the raw export's own `Price USD` column vs. the encoded close, across all 94,805 entry rows, shows **max deviation 0.0 ticks**. A first re-capture attempt same day (`…_c2642.csv`, discarded, never landed) had the same fixed encoding but hit TradingView's ~9,000-order regular-mode cap — the window inputs weren't set before that run, truncating it to ~4.5 months (2026-04-20→2026-09-04) (Aegis lane PARKED; historical + ledger) |
| `MCL_M15.csv` | NYMEX MCL | **KEEP · LANDED 2026-08-13** — CME BAR EXPORT v0.2 `MCL1!` (`…_3fd7c.csv`), operator-supplied; 106,261 bars, span 2022-01-02T23:00Z→2026-07-02T00:00Z; sha256 `5aa50456…bbd23`. Sidecar `MCL_M15.meta.json` pins `mintick 0.01 · pointvalue 100 · tz America/New_York`. ⚠ Panel **ends 2026-07-02**, ~6 weeks before its export date — any CONFIRM window must end at the panel, not at "today" |
| `M2K_M15.csv` | CME M2K | **KEEP · LANDED 2026-08-13** — CME BAR EXPORT v0.2 `M2K1!` (`…_14faf.csv`), operator-supplied; 106,131 bars, span 2022-01-02T23:00Z→2026-07-02T00:00Z; sha256 `81922570…12349`. Sidecar `M2K_M15.meta.json` pins `mintick 0.1 · pointvalue 5 · tz America/Chicago`. ⚠ Panel **ends 2026-07-02** — CONFIRM reserved through 2026-08-13 in G0 but unread bytes stop at panel end |
| `MGC_M15.csv` | COMEX MGC | **KEEP · REFRESHED 2026-09-03** — CME BAR EXPORT v0.2 `MGC1!` (`…_08a82.csv`), operator-supplied; 94,617 bars, span 2022-09-01T00:00Z→2026-09-03T00:00Z; sha256 `c5487470…a6aad`. Sidecar `MGC_M15.meta.json` pins `mintick 0.1 · pointvalue 10 · tz America/New_York`. `flat_frac` 0.0000, `max_close_decimals` 1 — clean decode, no encoding trap |
| `MNQ_M15.csv` | CME MNQ | **KEEP · REFRESHED 2026-09-03** — CME BAR EXPORT v0.2 `MNQ1!` (`…_4cea4.csv`), operator-supplied; 94,503 bars, span 2022-09-01T00:00Z→2026-09-03T00:00Z; sha256 `cceaac41…27fc8`. Sidecar `MNQ_M15.meta.json` pins `mintick 0.25 · pointvalue 2 · tz America/Chicago`. `flat_frac` 0.0000, `max_close_decimals` 2 — clean decode, no encoding trap (c1 / Striker NAS venue edition research) |
| `MYM_M15.csv` | CBOT MYM | **KEEP · REFRESHED 2026-09-03** — CME BAR EXPORT v0.2 `MYM1!` (`…_23dd6.csv`), operator-supplied; 94,499 bars, span 2022-09-01T00:00Z→2026-09-03T00:00Z; sha256 `15b34615…6b156`. Sidecar `MYM_M15.meta.json` pins `mintick 1 · pointvalue 0.5 · tz America/Chicago`. `flat_frac` 0.0000, `max_close_decimals` 1 — clean decode, no encoding trap (c1 / Striker DJ30 venue edition research) |

**Pepperstone producer is dead.** `scripts/parse_bar_export.py` defaulted to
Pepperstone `bar_export/` inputs retired 2026-08-02
([Pepperstone feed ADR](../../../docs/adr/2026-08-02-pepperstone-feed-retirement.md)).
`6J` / `MGC` / `MNQ` / `MYM` are now landed via explicit `--in` from fresh CME
BAR EXPORT v0.2 captures (MGC first 2026-08-12, see
[`docs/notes/2026-08-12-guardian-mgc-nsurv-bar-derived-intraday-prep.md`](../../../docs/notes/2026-08-12-guardian-mgc-nsurv-bar-derived-intraday-prep.md);
all four refreshed 2026-09-03, `6J` a second time same day to fix a Signal-field
encoding trap). **Regenerable only for the window a fresh export actually
captures** — currently ~2022-09-01 onward — not from the dead Pepperstone default
path. That is narrower than the multi-year history the pre-refresh `6J`/`MNQ`/`MYM`
panels held: `6J` alone was previously captured at 161,750 bars (see
`6j_orb_ny_v0_2.pine`'s data-provenance comment, Downloads-local), implying a span
of roughly 6-7 years. Those earlier bytes were never committed (gitignored per
vendor TOS) and are not recoverable from this tree — a fresh capture reproduces
only what its own window covers, not the historical depth several prior studies
consumed.

**CFD-era panels deleted 2026-08-03** (`US30*`, `NAS100*`, `USDJPY*`, `XAUUSD*`,
`XAGUSD`) — owning ADR
[`docs/adr/2026-08-03-bar-data-cfd-and-candidates-retirement.md`](../../../docs/adr/2026-08-03-bar-data-cfd-and-candidates-retirement.md);
hashes in
[`docs/ltm/notes/2026-08-03-bar-data-cfd-candidates-tombstone.md`](../../../docs/ltm/notes/2026-08-03-bar-data-cfd-candidates-tombstone.md).

Integrity gate: `python scripts/check_data_manifests.py --check` (regen + commit
`SHA256SUMS` in the same commit as any CSV change).
