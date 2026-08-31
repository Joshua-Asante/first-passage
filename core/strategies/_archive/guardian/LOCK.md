# Guardian Gold v5.5 — LOCK

**Strategy version:** v5.5
**Lock date:** 2026-04-23
**Instrument:** XAUUSD 15m
**Risk per trade:** 0.34% (cold-start base, post-2026-04-23 relock)
**Phase parity:** challenge = funded (unified 2026-04-17)

## Source blob hashes (git-canonical, line-ending-normalized)

These are git's `hash-object` blob SHA1s — the authoritative content hashes
for files tracked under `core.autocrlf=true`. Raw `sha1sum` will diverge by
EOL bytes; trust the values below. Cross-check against `core/strategies/MANIFEST.sha256`
(SHA256 of the same blobs).

- Strategy:     `de54ef3b6d9abcdd83ae45d8bb2ead6a5c281ce0` — core/strategies/_archive/guardian/guardian_gold_v5.5.pine
- Indicator:    `e2db94052e07e49f45d281b11f19f1b50c772bf4` — core/strategies/_archive/guardian/guardian_gold_v5.5_indicator.pine
                  (combined: emits both FIRE-class `longSignal` and anticipation-class
                   `strictApproach`/`approachZone` alertconditions plus matching
                   `alert()` push calls — see indicator file's 2026-05-07 patch header)
- Anticipation: combined into indicator file (see indicator blob above)

## Reference backtest

Parameter and backtest-performance detail redacted from the public tree (2026-08-14, per
docs/adr/2026-08-14-repo-public-visibility-transition.md) — see the private operational
archive. Reconciled via `trade-csv-reconcile` (`scripts/reconcile.py --strategy guardian`).

## Lock decision Notion anchor

`<await user supply>`

Source of truth: Pine source (strategy logic) + docs/adr/ (lock rationale), per Rule 0.
(Prior Notion root 346…d1b8d5 = SUPERSEDED 2026-04-17 brief, archived.)

## Locked config

Parameter detail redacted from the public tree (2026-08-14) — see the private operational
archive. Source of truth remains the Pine strategy file (gitignored) per Rule 0.

## Notes

- Guardian re-locked from 0.30% → 0.34% on 2026-04-23 after Pepperstone-sourced
  panel showed available headroom (per CLAUDE.md).
- Indicator file header documents a 2026-05-07 NON-STRATEGY PATCH that added
  `alert()` push calls for anticipation states; strategy logic untouched.
  See `docs/audits/2026-05-08-guardian-v55-indicator-strategy-diff.md` for
  the indicator-vs-strategy entry-condition audit.
