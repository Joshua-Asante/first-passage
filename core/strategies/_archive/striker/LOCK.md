# Striker DJ30 v4.5 — LOCK

**Strategy version:** v4.5
**Lock date:** 2026-05-05 (v4.4 → v4.5); allocation refresh 2026-05-23 (risk 0.75% → 0.70%, pyramid 500% → 750%)
**Instrument:** DJ30 15m
**Risk per trade:** 0.70% (pyramid 750%) — canonical owner: `firm_rules.py` `_BASE_RISK["striker"]`; Pine `riskPerTrade`/`pyramidSize` mirror it
**Phase parity:** challenge = funded (unified 2026-04-17)

## Source blob hashes (git-canonical, line-ending-normalized)

These are git's `hash-object` blob SHA1s — the authoritative content hashes
for files tracked under `core.autocrlf=true`. Raw `sha1sum` will diverge by
EOL bytes; trust the values below. Cross-check against `core/strategies/MANIFEST.sha256`
(SHA256 of the same blobs).

- Strategy:     `1ed736cf82e848cdce8854757aa321f47c1c0007` — core/strategies/_archive/striker/striker_dj30_v4.5.pine
- Indicator:    `3704f026092db5b043dd4f03b9805a13fa23b551` — core/strategies/_archive/striker/striker_dj30_v4.5_indicator.pine

## Reference backtest

Parameter and backtest-performance detail redacted from the public tree (2026-08-14, per
docs/adr/2026-08-14-repo-public-visibility-transition.md) — see the private operational
archive. Reconciled via `trade-csv-reconcile` (`scripts/reconcile.py --strategy striker_dj30`).

## Lock decision Notion anchor

`<await user supply>`

Source of truth: Pine source (strategy logic) + `docs/adr/` (lock + allocation rationale),
per Rule 0 / `docs/operational_rules.md` Rule 5. `firm_rules.py` owns the live risk %;
allocation rationale in `docs/adr/2026-05-23-allocation-refresh-2.md`.

## Locked config

Parameter detail redacted from the public tree (2026-08-14) — see the private operational
archive. Source of truth remains the Pine strategy file (gitignored) per Rule 0.

## Notes

- 2026-05-23 allocation-refresh-2: risk 0.75% → 0.70%, pyramid 500% → 750%. No version
  bump — v4.5 designation retained per the no-version-bump doctrine (2026-05-14 ADR §Open
  items 1+2, ratified 2026-05-23).
- v4.4 archived to `archive/strategies/striker/`.
- Primary bust risk: solo gap-fill on non-pyramid breakouts.
