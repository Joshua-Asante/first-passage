# Cursor handoff: opt-in strict BAR EXPORT v0.2 validation

**Type:** cc_handoff  
**Date:** 2026-09-05  
**Status:** Frozen implementation contract; parent review required before merge  
**Owner:** Cursor implementation; Codex integration/review; operator merge

## 0. Current sources and Phase 0

Baseline: `846a437d6f1ccbd30435c81730725cdb553b6beb`. Read `CLAUDE.md`, `docs/adr/2026-07-14-cc-cursor-surface-allocation.md`, `docs/adr/2026-06-05-monorepo-layer-boundaries.md`, `core/bar_export_loader.py`, `tests/core/test_bar_export_loader.py`, `scripts/parse_bar_export.py`, `REPO_MAP.md` and `pyproject.toml`.

Current loader skips undecodable Entry signals, converts numeric values to float, tolerates price differences and merges cross-page duplicate timestamps with keep-last. Those are existing permissive producer behaviors. The new validator is a separate manual evidence check; it changes none of them. The existing SIGNAL_PIPE_V2_RE is the public wire grammar and must be imported read-only for matching raw fields.

## 0.5. Clarification defaults

**Recommended default A:** validate only supplied raw v0.2 pages, never infer missing expectations or use the legacy float decoder for strict comparisons. **Recommended default B:** preserve permissive callers and their tests unchanged. **Recommended default C:** keep output deterministic and synthetic; report a material contradiction before changing scope. Routine factoring and formatting are yours. Post the Phase 0 read/dependency report, then proceed without waiting for another permission round when these defaults and the contract are consistent.

## 0.75. Cloud availability

All required source and test dependencies are public tracked files. Tests create invented CSVs under tmp_path. No vendor data, private captures, account information, Pine source, secrets, ignored artifacts or external services are needed or authorized.

## 1. Purpose

A replacement bar evidence set must not silently lose a malformed entry, change precise values during float conversion, or select one of two disagreeing overlapping rows. This read-only validator makes those failures explicit before a caller accepts the bytes. It does not certify market history, produce canonical bars, change a manifest or run a strategy.

## 2. Allowed deliverables and API

Only new `scripts/validate_bar_export_v2.py`, new `tests/scripts/test_validate_bar_export_v2.py`, one REPO_MAP.md script-table row, and a factual completion note in this handoff if useful. Do not add global gates or dependencies. Existing parser and core files are read-only.

Expose frozen value types and a read-only filesystem validation function:

```python
@dataclass(frozen=True)
class ExpectedBarExportV2:
    price_column: str
    ticker: str
    instrument_type: str
    quote_currency: str
    base_currency: str
    mintick: Decimal
    pointvalue: Decimal
    timezone: str
    timeframe_minutes: int
    expected_unique_bars: int
    expected_first_open_utc: datetime
    expected_last_open_utc: datetime

@dataclass(frozen=True)
class BarExportValidationReceipt:
    schema: str
    status: str
    page_count: int
    input_sha256: tuple[str, ...]
    entry_row_count: int
    unique_bar_count: int
    identical_cross_page_overlap_count: int
    first_open_utc: datetime
    last_open_utc: datetime
    metadata: Mapping[str, str]

def validate_bar_export_v2(
    paths: Sequence[Path], *, expected: ExpectedBarExportV2,
) -> BarExportValidationReceipt: ...
```

Use schema `bar_export_v2_validation_v1`, status `PASS`. Validation errors raise ValueError with a concise page/row/field reason; filesystem failures may retain their precise OSError. Receipt metadata must be immutable, not a mutable dictionary inside a frozen dataclass. Keys: ticker, type, quote_currency, base_currency, mintick, pointvalue, timezone, timeframe. Decimal strings retain the first valid raw representation; comparison uses exact Decimal numeric equality, so trailing zeros alone are not disagreement.

CLI:

```text
python scripts/validate_bar_export_v2.py --in PAGE [PAGE ...]
  --price-column NAME --expected-ticker TEXT --expected-type TEXT
  --expected-quote-currency TEXT --expected-base-currency TEXT
  --expected-mintick DECIMAL --expected-pointvalue DECIMAL
  --expected-timeframe-minutes INT --expected-timezone TEXT
  --expected-unique-bars INT
  --expected-first-open-utc ISO_UTC --expected-last-open-utc ISO_UTC
  [--receipt PATH]
```

On success print deterministic JSON, and optionally atomically write identical bytes to receipt (including one terminal newline). On validation/usage/input or output-write failure, exit 2 and report concisely to stderr. Validate fully before touching an output; failure leaves a preexisting receipt unchanged. Refuse a receipt path that aliases any input, including a symlink/hardlink, before writing. No other file writes. Successful status is emitted only after any requested receipt write succeeds.

## 3. Strict rules

1. Read/hash each page from the same exact byte buffer, UTF-8 with optional BOM; no float conversion by CSV loading. Require at least one page and one Entry per page. Headers include Type, Date and time, the named price column, Signal or Comment, and Trade # or Trade number. Reject duplicate headers and malformed row widths. Prefer Signal when present, matching the current loader; blank/malformed Signal does not silently fall back to Comment. Ignore non-Entry rows. Date and time is transport text; epoch is authoritative and its timezone must not be inferred from this column.
2. Every Type starting with Entry must full-match the existing v0.2 grammar after surrounding whitespace removal. Reject malformed, blank, v0.1 or mixed-version Entry rows; skip none. Numeric Entry trade IDs are positive integers, unique within each page. Sort by numeric ID, then require strictly increasing epoch opens; reverse physical CSV ordering is permitted. Preserve caller page order for hashes and first metadata representation.
3. Parse epoch/time_close/volume/trade IDs as exact integers and all prices/tick/point value as Decimal, never float. Require finite positive prices, mintick and pointvalue, nonnegative integer volume, valid OHLC geometry and exact encoded-close versus Entry-price equality. No tick quantization, tolerance or market-specific minimum decimal-place rule.
4. Validate expected argument types and signs too: finite positive Decimal tick/pointvalue; positive non-boolean integer timeframe/count; nonempty strings for required fields (base currency may be empty); aware zero-offset UTC endpoint datetimes in order. Raw metadata must be nonempty except explicitly empty base currency, identical across all entries and equal the expected values. String identity is exact; no symbol alias or timezone normalization. Timeframe metadata must be the canonical decimal minute string for expected timeframe_minutes.
5. Epoch milliseconds are UTC opens. Require `epoch_ms < time_close_ms <= epoch_ms + timeframe_minutes * 60000`. This is a structural duration bound, not a claim that every session bar has full duration or that a fixture's minus-one-millisecond endpoint defines Pine semantics. Retain/compare the exact reported close timestamp. Day-of-week and session flags are shape-validated by the existing grammar; do not infer them from a guessed chart timezone.
6. Within-page duplicate timestamps fail. Across pages, overlap is accepted only when every decoded v0.2 field and Entry price agrees exactly (numeric Decimal equality for numeric fields, exact other identities). Metadata/per-bar-field/OHLCV disagreements fail. Count every accepted repeated row across pages; never select a winner. Same timestamp with differing trade ID across distinct pages is allowed because those are transport IDs, not payload identity.
7. Sort reconciled unique opens, require exact supplied count/first/last, and report hashes in input page order. Use exact integer/datetime conversion, no epoch float round-trip. Do not infer continuity across exchange closures, session completeness, contract roll, feed equivalence or chart timezone. This receipt does not compare a separate canonical history; that integration remains caller-owned.
8. Reject a repeated underlying input file, including repeated paths and symlink/hardlink aliases. Distinct files may contain legitimate identical overlap. After successful reconciliation, identical_cross_page_overlap_count equals entry_row_count minus unique_bar_count; count repeated rows, not all pairwise matches.

## 4. Hypothesis and independent tests

H: opt-in validation detects raw-entry corruption and conflicting evidence without changing the permissive producer. Falsifier: an Entry is silently omitted, distinct precise values collapse, conflicting overlap passes, expectations are ignored, input bytes change, or an existing producer behavior changes.

Write independent synthetic expected-value tests before implementation:

- Two valid pages, one identical logical overlap: exact page/entry/unique/overlap counts, endpoints, metadata and independently computed byte hashes; deterministic immutable receipt.
- Bad single Entry; blank/v0.1/mixed Signal; missing/duplicate headers; malformed widths; empty input/page; bad/duplicate trade IDs; descending opens in numeric-ID order; reverse physical order allowed.
- Every expected binding mismatch; invalid expected type/sign; empty required metadata and within/across-page drift.
- More significant decimal digits than float preserves: exact close/Entry equality passes, one final-digit difference fails; nonfinite/invalid numerics, bad OHLC geometry and volume fail. Different trailing zeros alone agree.
- Close at open or beyond duration fails; exact full duration, one millisecond shorter and a shorter positive session bar pass this structural bound. Close timestamp/dow/session disagreement in overlap fails. Duplicate within-page fails; exact cross-page duplicate passes; divergent overlap fails.
- Wrong unique count/first/last and non-UTC/naive expected endpoints fail. Identical repeat calls and changed Decimal context cannot alter comparisons.
- CLI success JSON and receipt bytes identical; validation failure exit2 leaves existing receipt intact; input-alias output refused; no source or canonical writes. Duplicate underlying input paths/aliases fail. A timestamp repeated in three distinct pages contributes two overlaps, not three.
- One focused regression calls unchanged parse_bar_export_with_meta on synthetic malformed/overlapping data to demonstrate its retained permissive behavior. If a symbol mapping is needed, monkeypatch a synthetic key within the test; use no real captured row.

## 5. Forbidden moves

- Do not edit core/bar_export_loader.py, scripts/parse_bar_export.py, their tests, price maps, Pine, data, manifests, campaign policy or scripts/gates.yml.
- Do not publish real exports, account values, private paths/digests or sample spans/counts taken from a live campaign.
- Do not fetch vendor data, run source backtests, scoring, search, Monte Carlo or create an ingestion framework.
- Do not merge, auto-merge, deploy or change another agent's branch.

## 6. Gate and return taxonomy

RESOLVED requires exact contract coverage, focused tests, required CI and parent review of the actual diff. Otherwise FALSIFIED names the failing case, or AMBIGUOUS identifies an unresolved contract dependency.

Return DONE or DONE_WITH_CONCERNS with commit, files, test commands/counts, synthetic CLI example and limits. NEEDS_CONTEXT identifies missing factual input. BLOCKED distinguishes tool/environment failure, contradictory spec or outside-scope dependency. Operator retains merge control.

## 7. Execution and review

Use one consolidated Phase 0 read. Then test-first implementation, focused verification and two-pass self-review (specification then code quality), including a final consolidated read of all changes. Keep implementation on this PR's existing branch. Codex owns independent review and integration. Do not repeatedly run a full repository suite during local development; existing CI retains its required checks.

## 10. Audit hooks

```bash
python scripts/check_brief.py docs/briefs/handoffs/2026-09-05-cursor-strict-bar-export.md --type cc_handoff
python -m pytest tests/scripts/test_validate_bar_export_v2.py -q
git diff --check
git diff --stat origin/main...HEAD
```

## Completion note (Cursor)

Implemented on `codex/strict-bar-export-validation`: `scripts/validate_bar_export_v2.py`, `tests/scripts/test_validate_bar_export_v2.py` (9 synthetic tests), and one `REPO_MAP.md` scripts-table row. Permissive producer unchanged. Parent/Codex review still required before merge.
