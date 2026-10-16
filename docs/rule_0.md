# Rule 0 — Audit-first

Before any decision brief or implementation step touching risk controls
(`dd_protection`, lot sizing, protection tiers, allocation, calibration constants),
read the production code directly first. Not memory. Not prior decision docs.

Order: production file → brief against ground truth → validate → lock → implementation.

## Corollaries

- Suspect single-rule descriptions of multi-rule systems.
- Data-source labels are NOT data-source verification.
- Where prior docs and code disagree, code wins; flag the discrepancy.
- Load-bearing claims without code-resident verification are unverified, regardless of how they're phrased in prose. Identity, contract, and cardinality assertions are the baseline; helpers in `core/lib/mvd.py`. Scope (MVD discipline): artifacts that cross the live capital boundary — artifacts whose silent failure would change allocation, risk parameters, or lock decisions: MC input panels; lock decision inputs (every performance number cited in a lock brief must be reproducible by a script with identity assertions); risk-control production code (any change requires self-validation that guards fire and fallbacks don't, e.g. `dd_protection._validate_protection_rule()` at import); allocation changes; specific numbers or named behavior cited in memory, ADR, or CHANGELOG (must trace to a reproducing script with identity assertions). Out of scope (no mandatory tax): exploratory scripts, methodology drafts, ad-hoc charts, broker-feed comparisons not yet promoted, datasets on disk until used in scope. For any artifact in scope, identity assertions appear within ~5 lines of identifier declaration; cardinality and contract assertions appear at producing site, not consuming site. The doc audit table and consumer-side MVD-attest line were dropped by 2026-08-14 and are not part of this rule. Consolidated 2026-10-15 from 2026-04-24-mvd-discipline (removed; see [TOMBSTONES](adr/TOMBSTONES.md#2026-10-15-adr-decay-audit-removals)).

## Triggering failures

- 2026-04-17: `dd_protection` misstatement against production constants. Brief described a single rule; production carried a second equity tier that was dead under the live `min()` combining semantics. The dead tier was deleted (Algorithm step 2: Delete) only after Rule 0 read of production; brief had been authored from prior-doc memory.
- 2026-04-24: retrospective audit of nine debugging instances — plausibly-shaped output, never a crash; failure at component boundaries; caught only by independent re-derivation; 6/9 an identity sub-pattern (a string identifier treated as verified to refer to its claimed referent). Generalized into corollary 4 ([MVD ADR, pinned](https://github.com/Joshua-Asante/first-passage/blob/dad73e3d2c6b78a2ca10a4ba90df2765a05286e8/docs/adr/2026-04-24-mvd-discipline.md)).
- 2026-04-27: weakened-form Rule 0 (read-prior-doc-not-code) produced wrong audit verdict on Q-meta-a brief. Strengthened: prior decision docs are not a Rule 0 substrate.

## Scope

New rules are written only against observed failures during execution phase, not hypothesized ones.
Resurrection rule + 90-day review gate: `git show pre-prune-2026-06-05:archive/docs/methodology/archive/README.md`.
