# Aegis USDJPY v4.3 — LOCK

**Strategy version:** v4.3
**Lock date:** 2026-04-22
**Instrument:** USDJPY 15m
**Risk per trade:** 1.50% (canonical owner: `firm_rules.py` `_BASE_RISK["aegis"]`; Pine `risk_pct` mirrors it)
**Phase parity:** challenge = funded (unified 2026-04-17)

## Source blob hashes (git-canonical, line-ending-normalized)

These are git's `hash-object` blob SHA1s — the authoritative content hashes
for files tracked under `core.autocrlf=true`. Raw `sha1sum` will diverge by
EOL bytes; trust the values below. Cross-check against `strategies/MANIFEST.sha256`
(SHA256 of the same blobs).

- Strategy:     `081f1da7bc1c5379010c1cc459276944ffc838b3` — strategies/aegis/aegis_usdjpy_v4.3.pine
- Indicator:    `ffb004749e858b4f4cf4344eb3fa63326650fee2` — strategies/aegis/aegis_usdjpy_v4.3_indicator.pine

## Reference backtest

Parameter and backtest-performance detail redacted from the public tree (2026-08-14, per
docs/adr/2026-08-14-repo-public-visibility-transition.md) — see the private operational
archive. Reconciled via `trade-csv-reconcile` (`scripts/reconcile.py --strategy aegis`).

## Lock decision Notion anchor

`<await user supply>`

Source of truth: Pine source (strategy logic) + `docs/adr/` (lock + allocation rationale),
per Rule 0 / `docs/operational_rules.md` Rule 5. `firm_rules.py` owns the live risk %.

## Locked config

Parameter detail redacted from the public tree (2026-08-14) — see the private operational
archive. Source of truth remains the Pine strategy file (gitignored) per Rule 0.

## Notes

- BE logic is load-bearing edge — a large share of winners are BE-manufactured.
- Permanent manual BOJ binary-event pause rule applies (operational, not in Pine).
