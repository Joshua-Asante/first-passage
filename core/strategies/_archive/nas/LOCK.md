# Striker NAS100 v1 — LOCK

**Strategy version:** v1 (Pine title string: "Striker NAS100 v1.0")
**Lock date:** 2026-05-05 (operational integration 2026-05-07 after DXTrade contractValue=10 broker-verified); allocation refresh 2026-05-23 (risk 0.45% → 0.37%, pyramid 1000% unchanged)
**Instrument:** NAS100 15m
**Risk per trade:** 0.37% (pyramid 1000%) — canonical owner: `firm_rules.py` `_BASE_RISK["striker_nas100"]`; Pine `riskPerTrade` mirrors it
**Phase parity:** challenge = funded (unified 2026-04-17)

## Source blob hashes (git-canonical, line-ending-normalized)

These are git's `hash-object` blob SHA1s — the authoritative content hashes
for files tracked under `core.autocrlf=true`. Raw `sha1sum` will diverge by
EOL bytes; trust the values below. Cross-check against `core/strategies/MANIFEST.sha256`
(SHA256 of the same blobs).

- Strategy:     `2ad68d10aec0b4df346ae06bc880b747f94ca398` — core/strategies/nas/striker_nas100_v1.pine
- Indicator:    `ab17c31832702831da7a1b5d020cc6761b2edc8c` — core/strategies/nas/striker_nas100_v1_indicator.pine

## Reference backtest

Parameter and backtest-performance detail redacted from the public tree (2026-08-14, per
docs/adr/2026-08-14-repo-public-visibility-transition.md) — see the private operational
archive. Reconciled via `trade-csv-reconcile` (`scripts/reconcile.py --strategy striker_nas`).

## Lock decision Notion anchor

`<await user supply>`

Source of truth: Pine source (strategy logic) + `docs/adr/` (lock + allocation rationale),
per Rule 0 / `docs/operational_rules.md` Rule 5. `firm_rules.py` owns the live risk %;
allocation rationale in `docs/adr/2026-05-23-allocation-refresh-2.md`.

## Locked config

Parameter detail redacted from the public tree (2026-08-14) — see the private operational
archive. Source of truth remains the Pine strategy file (gitignored) per Rule 0.

## Notes

- 2026-05-23 allocation-refresh-2: risk 0.45% → 0.37%, pyramid 1000% unchanged. No version
  bump — v1 designation retained per the no-version-bump doctrine.
- **Provenance-docstring lag (known):** the strategy `.pine` LOCK-PROVENANCE
  docstring and the indicator `riskPerTrade` tooltip still narrate an older locked value.
  The live `input.float` default is correct at the risk% stated above; only the narrative
  text lags. Fix = docstring/tooltip refresh (no-version-bump doctrine,
  `docs/adr/2026-05-23-allocation-refresh-2.md`). Pending cosmetic Pine-source edit,
  tracked in this LOCK.md note.
- Pyramid dependence is load-bearing: a large majority of net P&L comes from a
  small fraction of pyramid legs; bust risk concentrates in any regime
  suppressing the pyramid trigger.
