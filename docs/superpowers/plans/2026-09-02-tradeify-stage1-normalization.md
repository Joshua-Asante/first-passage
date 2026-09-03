# Tradeify Seven-Strategy Phase 1 Normalization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and run a strict, deterministic, exploratory normalization and reconciliation pipeline for the seven supplied TradingView Pine/CSV pairs.

**Architecture:** Reusable `research_utils` modules verify source identity, normalize TradingView events, reconstruct trades, calculate accounting/venue checks from a campaign-local primary-source fee table, and build deterministic joint weekly blocks. A campaign-local runner loads a frozen JSON mapping, writes full row-level outputs only to a gitignored directory, and commits aggregate reports and hashes.

**Tech Stack:** Python 3.11+, standard-library `dataclasses`, `decimal`, `hashlib`, `json`, `pathlib`, and `zoneinfo`; pandas; pytest; existing `lab.discovery.cost_model` and `core.firm_rules`.

**Spec:** `docs/superpowers/specs/2026-09-02-tradeify-stage1-normalization-design.md`

## Global Constraints

- Every result is `EXPLORATORY`; the operator skipped Phase 0 and every supplied row is consumed development data.
- Never describe an output as untouched, out-of-sample, confirmatory, qualified, admitted, or deployable.
- Keep the fourteen supplied files and generated row-level ledgers out of Git under campaign-local `local_artifacts/`.
- Preserve source rows and source ordering; never repair, delete, shift, roll, or relabel a source event.
- Keep `timestamp_utc` and `exchange_session_date` null until a source timezone is explicitly configured.
- Use the hashed primary-source Tradeify schedule for 6J/MNQ/MYM/MGC fees and reconcile it to production comments; never use `cost_model.resolve_commission` as the Phase 1 fee resolver.
- Keep `lab/discovery/cost_model.py` byte-unchanged; its closed-world guard is intentional.
- Use `Decimal` for source money and quantity parsing; aggregate currency tolerance is exactly `$0.01`.
- A source hash/schema failure aborts the complete campaign; a strategy reconciliation blocker still produces that strategy's report.
- Do not modify Pine, strategy locks, allocation, `dd_protection`, lifecycle, rail, or deployment code.
- Use TDD for every behavior change and commit after each independently passing task.

---

## File map

- `lab/research_utils/tv_trade_ledger.py`: frozen configuration types, source hashing, strict TradingView CSV parsing, event normalization, and timestamp localization.
- `lab/research_utils/trade_reconciliation.py`: strict trade reconstruction, accounting metrics, position exposure bounds, and stable issue records.
- `lab/research_utils/joint_trade_blocks.py`: deterministic cross-strategy event union and zero-filled ISO-week exit blocks.
- `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/phase1_config.json`: exact fourteen-file mapping and hashes.
- `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/tradeify_commission_schedule.json`: primary-source 6J/MNQ/MYM/MGC round-trip fee capture and provenance.
- `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/run_phase1.py`: command-line orchestration, atomic local outputs, aggregate JSON, and Markdown rendering.
- `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/.gitignore`: exclude `local_artifacts/`.
- `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/README.md`: claim boundary, invocation, output ownership, and issue interpretation.
- `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/reconciliation_manifest.json`: committed aggregate machine-readable result from the frozen sources.
- `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/RESULTS.md`: committed human-readable seven-strategy reconciliation.
- `tests/test_tv_trade_ledger.py`: source/config/schema/numeric/timezone tests.
- `tests/test_trade_reconciliation.py`: pairing, accounting, exposure, fee, and force-flat tests.
- `tests/test_joint_trade_blocks.py`: deterministic joint ordering and weekly zero-fill tests.
- `tests/test_tradeify_phase1_runner.py`: synthetic end-to-end output, exit-code, determinism, and data-leak tests.
- Existing `tests/core/test_mc_intraday_barrier.py`, `tests/core/test_trailing_dd_boundary.py`, `tests/core/test_trailing_locking_boundary.py`, and `tests/core/test_mc_preflight.py`: unchanged production firm-barrier verification evidence.

---

### Task 1: Freeze campaign configuration and source identity

**Files:**
- Create: `lab/research_utils/tv_trade_ledger.py`
- Create: `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/phase1_config.json`
- Create: `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/tradeify_commission_schedule.json`
- Create: `tests/test_tv_trade_ledger.py`

**Interfaces:**
- Consumes: JSON configuration path and a runtime source directory.
- Produces: `Issue`, `SourceSpec`, `VerifiedSource`, `FeeSchedule`, `load_source_specs(path)`, `load_fee_schedule(path)`, `sha256_file(path)`, and `verify_source_pair(source_dir, spec)`.

- [ ] **Step 1: Write failing configuration and hash tests**

```python
from hashlib import sha256
import json

import pytest

from research_utils.tv_trade_ledger import (
    SourceIdentityError,
    load_source_specs,
    verify_source_pair,
)


def test_load_source_specs_rejects_duplicate_strategy_id(tmp_path):
    payload = {
        "claim_class": "EXPLORATORY",
        "strategies": [
            _spec_dict("same", "one.csv", "one.pine"),
            _spec_dict("same", "two.csv", "two.pine"),
        ],
    }
    path = tmp_path / "config.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate strategy_id: same"):
        load_source_specs(path)


def test_verify_source_pair_rejects_changed_export(tmp_path):
    export = tmp_path / "source.csv"
    pine = tmp_path / "source.pine"
    export.write_bytes(b"changed")
    pine.write_bytes(b"pine")
    spec = _source_spec(
        export_sha256=sha256(b"expected").hexdigest(),
        pine_sha256=sha256(b"pine").hexdigest(),
    )
    with pytest.raises(SourceIdentityError, match="source.csv.*SHA-256"):
        verify_source_pair(tmp_path, spec)
```

- [ ] **Step 2: Run the focused tests and confirm failure**

Run: `python -m pytest tests/test_tv_trade_ledger.py -q`

Expected: collection fails because `research_utils.tv_trade_ledger` does not exist.

- [ ] **Step 3: Add immutable configuration and identity types**

```python
@dataclass(frozen=True)
class Issue:
    code: str
    severity: Literal["INFO", "WARNING", "BLOCKER", "FATAL"]
    strategy_id: str
    detail: Mapping[str, object]
    trade_id: int | None = None
    source_rows: tuple[int, ...] = ()


@dataclass(frozen=True)
class SourceSpec:
    strategy_id: str
    intended_instrument: str
    encoded_instrument: str
    export_filename: str
    export_sha256: str
    pine_filename: str
    pine_sha256: str
    source_timezone: str | None
    session_timezone: str
    declared_bar_size_minutes: int
    declared_session: str
    direction_evidence: str
    quantity_convention: str
    continuous_symbol: bool
    synchronized_intraday_path_available: bool
    lineage_notes: tuple[str, ...]
    pine_commission_per_side_usd: Decimal
    pine_slippage_ticks_per_side: Decimal
    contract_cap: int


@dataclass(frozen=True)
class VerifiedSource:
    spec: SourceSpec
    export_path: Path
    pine_path: Path
```

Implement `load_source_specs()` with exact required keys, `claim_class == "EXPLORATORY"`, unique strategy IDs and basenames, 64-character lowercase hexadecimal hashes, valid IANA `session_timezone`, and nullable valid IANA `source_timezone`. Validate positive bar size/cap, non-empty inventory strings, and `continuous_symbol is True` for this frozen source set. Implement `verify_source_pair()` using resolved child paths, basename equality, regular-file checks, and byte-stream SHA-256 comparison.

- [ ] **Step 4: Freeze all fourteen source pins in configuration**

Create `phase1_config.json` with the seven rows and exact hashes from the approved design. Set every `source_timezone` to `null`, every bar size to 15 minutes, and every synchronized-intraday-path flag to false. Set session timezones to `America/New_York` for Aegis, ORB-MNQ, and Vanguard; set them to `UTC` for the four Striker variants. Record Aegis `10:00-13:45 America/New_York, Mon-Wed` with its separate 16:30 force-flat, ORB `09:15-16:55 America/New_York`, each Striker `13:00-17:00 UTC` with 15:45 America/New_York force-flat, and Vanguard `09:00-16:59 America/New_York`. Encode intended/export instruments separately so the two prototype mismatches remain visible. Set contract caps to `8` for 6J and `80` for MNQ, MYM, and MGC. Record quantity as integer contracts, continuous-symbol status as true, and the known tuning/lineage concerns from the approved design.

Create `tradeify_commission_schedule.json` as a compact primary-source capture with source URL `https://help.tradeify.co/en/articles/10468315-trading-commission-fees`, page date `2026-04-28`, observation date `2026-09-02`, the statement that totals include exchange, NFA, clearing, and commission, and exact round-trip rows `6J=6.20`, `MNQ=1.82`, `MYM=1.82`, `MGC=2.12`. `load_fee_schedule()` validates the source metadata, unique symbols, positive two-decimal round-trip amounts, and derives per-side values using `Decimal` division by two. Add behavior tests for the four values and duplicate/malformed rows.

- [ ] **Step 5: Run identity tests and the real read-only hash gate**

Run: `python -m pytest tests/test_tv_trade_ledger.py -q`

Expected: PASS.

Run:

```powershell
python -c "from pathlib import Path; from research_utils.tv_trade_ledger import load_source_specs,verify_source_pair; cfg=Path('lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/phase1_config.json'); src=Path(r'C:\Users\joshu\Downloads\strategies'); [verify_source_pair(src,s) for s in load_source_specs(cfg)]; print('14/14 hashes verified')"
```

Expected: `14/14 hashes verified`.

- [ ] **Step 6: Commit the identity boundary**

```bash
git add lab/research_utils/tv_trade_ledger.py lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/phase1_config.json lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/tradeify_commission_schedule.json tests/test_tv_trade_ledger.py
git commit -m "feat: freeze Tradeify phase 1 source identity"
```

---

### Task 2: Normalize TradingView rows without repairs

**Files:**
- Modify: `lab/research_utils/tv_trade_ledger.py`
- Modify: `tests/test_tv_trade_ledger.py`

**Interfaces:**
- Consumes: `VerifiedSource` and `SourceSpec` from Task 1.
- Produces: `NormalizationResult(events: pd.DataFrame, issues: tuple[Issue, ...])` and `normalize_export(source)`.

- [ ] **Step 1: Add failing schema, Decimal, ordering, and timezone tests**

```python
def test_normalize_retains_exit_first_source_order_and_flags_timestamp_tie(tmp_path):
    source = _verified_csv(
        tmp_path,
        rows=[
            _row(1, "Exit long", "2026-01-05 10:00", net="8.18", commission="1.82"),
            _row(1, "Entry long", "2026-01-05 10:00", net="8.18", commission="1.82"),
        ],
        source_timezone=None,
    )
    result = normalize_export(source)
    assert result.events["source_row_number"].tolist() == [1, 2]
    assert result.events["event_type"].tolist() == ["EXIT", "ENTRY"]
    assert result.events["timestamp_utc"].isna().all()
    assert result.events["exchange_session_date"].isna().all()
    assert result.events["concurrent_timestamp"].tolist() == [True, True]


def test_normalize_localizes_only_with_explicit_timezone(tmp_path):
    source = _verified_csv(
        tmp_path,
        rows=[_row(1, "Entry long", "2026-01-05 09:30")],
        source_timezone="America/New_York",
    )
    event = normalize_export(source).events.iloc[0]
    assert event["timestamp_utc"].isoformat() == "2026-01-05T14:30:00+00:00"
    assert str(event["exchange_session_date"]) == "2026-01-05"


def test_normalize_rejects_unknown_type_instead_of_guessing(tmp_path):
    source = _verified_csv(tmp_path, rows=[_row(1, "Buy maybe", "2026-01-05 09:30")])
    with pytest.raises(TradeExportSchemaError, match="unknown Type.*Buy maybe"):
        normalize_export(source)
```

Add cases for BOM input, missing/duplicate aliases, accounting parentheses, blank required numerics, non-integral quantity, non-finite numerics, and ambiguous/nonexistent DST wall times.

- [ ] **Step 2: Run the new tests and confirm the missing behavior**

Run: `python -m pytest tests/test_tv_trade_ledger.py -q`

Expected: FAIL because `normalize_export` and the strict parsing behavior are absent.

- [ ] **Step 3: Implement exact aliases and strict parsing**

Define `REQUIRED_COLUMNS` for the seventeen supplied columns and only these compatibility aliases:

```python
COLUMN_ALIASES = {
    "Trade #": "Trade number",
    "Net P&L USD": "Net PnL USD",
}
```

Normalize a BOM from the first header only. Reject a missing canonical column and reject aliases that create duplicate canonical columns. Parse `Trade number` and `Size (qty)` as positive integral `Decimal` values before conversion to `int`. Parse every monetary/price/percentage field as finite `Decimal`, supporting `($12.34)` as `-12.34` but rejecting thousands separators that are not valid CSV field content.

- [ ] **Step 4: Implement event classification and timestamp policy**

```python
def _classify_type(value: str) -> tuple[str, str]:
    normalized = " ".join(value.strip().lower().split())
    match normalized.split():
        case ["entry", "long"]:
            return "ENTRY", "LONG"
        case ["entry", "short"]:
            return "ENTRY", "SHORT"
        case ["exit", "long"]:
            return "EXIT", "LONG"
        case ["exit", "short"]:
            return "EXIT", "SHORT"
        case _:
            raise TradeExportSchemaError(f"unknown Type value: {value!r}")
```

Parse `%Y-%m-%d %H:%M` exactly. Preserve `timestamp_raw`. With no source timezone, store a naive pandas timestamp and nullable UTC/session fields. With a timezone, reject both DST folds and gaps, convert to UTC, and derive the session date through `ZoneInfo(spec.session_timezone)`. Mark every row belonging to a duplicate naive timestamp as concurrent. Stable-sort on `(timestamp_naive, source_row_number)`.

- [ ] **Step 5: Verify normalization**

Run: `python -m pytest tests/test_tv_trade_ledger.py -q`

Expected: PASS.

- [ ] **Step 6: Commit strict normalization**

```bash
git add lab/research_utils/tv_trade_ledger.py tests/test_tv_trade_ledger.py
git commit -m "feat: normalize TradingView events strictly"
```

---

### Task 3: Reconstruct trades and reconcile accounting

**Files:**
- Create: `lab/research_utils/trade_reconciliation.py`
- Create: `tests/test_trade_reconciliation.py`

**Interfaces:**
- Consumes: normalized event DataFrames, `Issue`, and `SourceSpec` from Tasks 1–2.
- Produces: `InstrumentGeometry`, `instrument_geometry(symbol)`, `ReconstructionResult(trades, issues)`, `reconstruct_trades(events, spec)`, `AccountingMetrics`, and `calculate_accounting(trades)`.

- [ ] **Step 1: Write failing strict-pairing tests**

```python
def test_reconstruct_requires_exactly_one_entry_and_exit():
    events = _events(
        _event(7, "ENTRY", row=1),
        _event(7, "ENTRY", row=2),
        _event(7, "EXIT", row=3),
    )
    result = reconstruct_trades(events, _spec())
    assert result.trades.empty
    assert [(i.code, i.trade_id, i.source_rows) for i in result.issues] == [
        ("UNSUPPORTED_TRADE_LEG_CARDINALITY", 7, (1, 2, 3))
    ]


def test_reconstruct_does_not_silently_skip_orphan_exit():
    result = reconstruct_trades(_events(_event(9, "EXIT", row=4)), _spec())
    assert result.trades.empty
    assert result.issues[0].code == "ORPHAN_EXIT"
    assert result.issues[0].severity == "BLOCKER"


def test_reconstruct_validates_price_pnl_identity():
    events = _round_trip(
        instrument="MNQ", entry="100.00", exit="101.00", qty=2,
        net="2.18", commission="1.82",
    )
    result = reconstruct_trades(events, _spec(instrument="MNQ"))
    trade = result.trades.iloc[0]
    assert trade["gross_pnl_usd"] == Decimal("4.00")
    assert not result.issues


def test_6j_campaign_geometry_supports_price_identity_without_changing_cost_model():
    geometry = instrument_geometry("6J")
    assert geometry.multiplier == Decimal("12500000")
    assert geometry.tick_size == Decimal("0.0000005")
    assert geometry.tick_value == Decimal("6.25")
```

Add cases for direction disagreement, exit before entry, unequal quantities, duplicated trade-summary fields that differ by more than `$0.01`, and scalar MAE/MFE retaining the `excursion-bounded` label.

- [ ] **Step 2: Run the pairing tests and confirm failure**

Run: `python -m pytest tests/test_trade_reconciliation.py -q`

Expected: collection fails because `research_utils.trade_reconciliation` does not exist.

- [ ] **Step 3: Implement strict trade reconstruction**

For each `source_trade_id`, count entry and exit rows before accessing either. Emit stable blocker codes for zero/duplicate legs and retain all source row numbers in each issue. Require matching direction and quantity and `entry_timestamp <= exit_timestamp`.

Define campaign-local 6J geometry as `multiplier=12500000`, `tick_size=0.0000005`, `tick_value=6.25`. For MNQ/MYM/MGC, convert the existing `cost_model.INSTRUMENT_SPECS` values to `Decimal(str(value))` at the boundary. Do not modify `cost_model.py`.

Build one row per valid trade with:

```python
TRADE_COLUMNS = [
    "strategy_id", "source_trade_id", "direction",
    "entry_timestamp_naive", "exit_timestamp_naive",
    "entry_timestamp_utc", "exit_timestamp_utc",
    "entry_price", "exit_price", "quantity",
    "net_pnl_usd", "commission_usd", "gross_pnl_usd",
    "mae_usd", "mfe_usd", "excursion_bound",
    "entry_source_row", "exit_source_row",
]
```

Compute price-implied gross as `(exit-entry) * multiplier * quantity * direction_sign`. Set `gross_pnl_usd` only when it agrees with `net_pnl_usd + commission_usd` to `$0.01`; otherwise leave it null and emit `GROSS_IDENTITY_MISMATCH`.

- [ ] **Step 4: Write and implement accounting tests**

```python
def test_calculate_accounting_uses_exit_chronology_and_decimal_money():
    trades = _trades(
        _trade(1, "2026-01-05 10:00", "10.00", "1.82"),
        _trade(2, "2026-01-05 10:00", "-4.00", "1.82"),
        _trade(3, "2026-02-02 10:00", "2.00", "1.82"),
    )
    metrics = calculate_accounting(trades)
    assert metrics.trade_count == 3
    assert metrics.net_pnl_usd == Decimal("8.00")
    assert metrics.profit_factor == Decimal("3.0000000000")
    assert metrics.max_drawdown_usd == Decimal("4.00")
    assert metrics.monthly_net_pnl == {
        "2026-01": Decimal("6.00"),
        "2026-02": Decimal("2.00"),
    }
```

Use exit timestamp, then exit source row, as deterministic chronology. Classify exact-zero P&L as flat. Return profit factor as null with an issue when there are no gross losses. Compare the last source cumulative value with total exit net P&L at `$0.01`; do not require every intermediate cumulative value to equal a simple running sum because simultaneous TradingView orders can interleave commissions.

- [ ] **Step 5: Verify reconstruction and accounting**

Run: `python -m pytest tests/test_trade_reconciliation.py -q`

Expected: PASS.

- [ ] **Step 6: Commit reconstruction**

```bash
git add lab/research_utils/trade_reconciliation.py tests/test_trade_reconciliation.py
git commit -m "feat: reconstruct and reconcile export trades"
```

---

### Task 4: Add fee, exposure, roll, and force-flat checks

**Files:**
- Modify: `lab/research_utils/trade_reconciliation.py`
- Modify: `tests/test_trade_reconciliation.py`

**Interfaces:**
- Consumes: reconstructed trades, `SourceSpec`, `FeeSchedule`, and `instrument_geometry(symbol)` from Task 3.
- Produces: `VenueMetrics`, `analyze_venue(trades, spec, fee_schedule)`, and stable fee/instrument issue codes.

- [ ] **Step 1: Write failing primary-fee reconciliation tests**

```python
@pytest.mark.parametrize(
    ("symbol", "commission", "per_side"),
    [("6J", "6.20", "3.10"), ("MNQ", "1.82", "0.91"),
     ("MYM", "1.82", "0.91"), ("MGC", "2.12", "1.06")],
)
def test_primary_schedule_drives_phase1_fee_reconciliation(
    fee_schedule, symbol, commission, per_side
):
    trades = _trades(_trade(1, commission=commission, qty=1))
    venue = analyze_venue(trades, _spec(instrument=symbol), fee_schedule)
    assert venue.venue_commission_per_side_usd == Decimal(per_side)
    assert "EXPORT_VENUE_COMMISSION_MISMATCH" not in _issue_codes(venue)
```

- [ ] **Step 2: Run the focused tests and confirm failure**

Run: `python -m pytest tests/test_trade_reconciliation.py -q`

Expected: FAIL because `analyze_venue` and its fee reconciliation are absent.

- [ ] **Step 3: Write failing venue, roll, and spread tests**

```python
def test_exposure_reports_tie_order_bounds(fee_schedule):
    trades = _overlapping_trades_same_boundary(qty=50)
    venue = analyze_venue(trades, _spec(instrument="MNQ", contract_cap=80), fee_schedule)
    assert venue.peak_open_quantity_min == 50
    assert venue.peak_open_quantity_max == 100
    assert "CAP_STATUS_AMBIGUOUS_AT_TIMESTAMP_TIE" in _issue_codes(venue)


def test_friday_to_sunday_hold_is_a_blocker_and_trade_is_retained(fee_schedule):
    trades = _trades(
        _trade_between(41, "2026-01-09 10:00", "2026-01-11 18:00", "25.00")
    )
    venue = analyze_venue(trades, _spec(), fee_schedule)
    assert venue.trade_count == 1
    assert venue.friday_to_sunday_holds == 1
    issue = next(i for i in venue.issues if i.code == "FORCE_FLAT_VIOLATION")
    assert issue.trade_id == 41
    assert issue.severity == "BLOCKER"


def test_aegis_pine_export_and_venue_commissions_stay_separate(fee_schedule):
    trades = _trades(_trade(1, "2026-01-05 10:00", "50.20", "24.80", qty=4))
    venue = analyze_venue(
        trades, _spec(instrument="6J", pine_commission="1.30"), fee_schedule
    )
    assert venue.export_implied_commission_per_side_usd == Decimal("3.10")
    assert venue.venue_commission_per_side_usd == Decimal("3.10")
    assert "PINE_EXPORT_COMMISSION_MISMATCH" in _issue_codes(venue)
    assert "EXPORT_VENUE_COMMISSION_MISMATCH" not in _issue_codes(venue)


def test_continuous_contract_and_unobservable_spread_are_explicit(fee_schedule):
    venue = analyze_venue(_trades(_trade(1)), _spec(continuous_symbol=True), fee_schedule)
    assert "CONTINUOUS_CONTRACT_ROLL_UNRESOLVED" in _issue_codes(venue)
    assert venue.bid_ask_spread_status == "NOT_SEPARATELY_OBSERVABLE"
    assert venue.slippage_basis == "PINE_DECLARED_TICKS_AND_FILL_PRICES"
```

Add tests for off-tick prices, intended/encoded instrument mismatch, confirmed cap breach, non-overlap, MGC matching `$1.06` per side, MNQ/MYM matching `$0.91`, variable export commissions, and a source marked non-continuous producing no roll issue.

- [ ] **Step 4: Implement geometry, tick, fee, roll, exposure, and hold analysis**

Use Task 3's campaign geometry. For tick validation, divide source price by tick size and require distance to the nearest integral tick to be no more than `1e-9` tick.

Infer export commission per side as `commission / (2 * quantity)` only for one-entry/one-exit trades. If values vary, report sorted unique values and emit `VARIABLE_EXPORT_COMMISSION` rather than averaging. Read all venue fees from `FeeSchedule`; compare venue, Pine, and export-implied bases separately at `$0.01`. Do not call `resolve_commission` and do not add 6J to `cost_model.py`.

Emit `CONTINUOUS_CONTRACT_ROLL_UNRESOLVED` for a `continuous_symbol` source and record that contract-month and roll-seam attribution are unavailable. Record bid/ask spread as `NOT_SEPARATELY_OBSERVABLE`; record Pine-declared slippage ticks and fill-based accounting without adding either cost again.

Compute exposure twice at equal timestamps: exits-before-entries for the minimum and entries-before-exits for the maximum. A minimum over cap is `CONTRACT_CAP_BREACH`; only the maximum over cap is `CAP_STATUS_AMBIGUOUS_AT_TIMESTAMP_TIE`. Emit `CROSS_DATE_HOLD` for every raw-date boundary and `FORCE_FLAT_VIOLATION` for each Friday-to-Sunday hold.

- [ ] **Step 5: Verify fee, venue, and unchanged closed-world behavior**

Run: `python -m pytest tests/test_trade_reconciliation.py tests/test_cost_model.py -q`

Expected: PASS; `git diff --exit-code 11d22e280db71d798f5c4e37edd85a62bc71f392 -- lab/discovery/cost_model.py` also exits `0`.

- [ ] **Step 6: Verify the existing production firm-barrier contract**

Run:

```bash
python -m pytest tests/core/test_mc_intraday_barrier.py tests/core/test_trailing_dd_boundary.py tests/core/test_trailing_locking_boundary.py tests/core/test_mc_preflight.py -q
```

Expected: PASS. Record this unchanged-code run in the Task 4 report and final Phase 1 verification evidence rather than duplicating production barrier tests in a campaign test.

- [ ] **Step 7: Commit venue checks**

```bash
git add lab/research_utils/trade_reconciliation.py tests/test_trade_reconciliation.py
git commit -m "feat: audit Phase 1 instrument and venue constraints"
```

---

### Task 5: Build the deterministic joint ledger and calendar-week adapter

**Files:**
- Create: `lab/research_utils/joint_trade_blocks.py`
- Create: `tests/test_joint_trade_blocks.py`

**Interfaces:**
- Consumes: mappings of strategy ID to normalized event/trade DataFrames.
- Produces: `build_joint_events(events_by_strategy)` and `build_weekly_exit_blocks(trades_by_strategy)`.

- [ ] **Step 1: Write failing deterministic-order tests**

```python
def test_joint_events_have_stable_cross_strategy_ties():
    left = _event_frame("zeta", [(2, "2026-01-05 10:00")])
    right = _event_frame("alpha", [(7, "2026-01-05 10:00")])
    joint = build_joint_events({"zeta": left, "alpha": right})
    assert joint[["strategy_id", "source_row_number"]].values.tolist() == [
        ["alpha", 7], ["zeta", 2]
    ]
    assert joint["concurrent_cross_strategy"].tolist() == [True, True]


def test_weekly_blocks_include_empty_calendar_weeks():
    blocks = build_weekly_exit_blocks({
        "alpha": _trade_frame([
            ("2026-01-05 10:00", Decimal("10.00")),
            ("2026-01-19 10:00", Decimal("-2.00")),
        ])
    })
    assert blocks["week_start"].astype(str).tolist() == [
        "2026-01-05", "2026-01-12", "2026-01-19"
    ]
    assert blocks["alpha_net_pnl_usd"].tolist() == [
        Decimal("10.00"), Decimal("0.00"), Decimal("-2.00")
    ]
    assert blocks["joint_trade_count"].tolist() == [1, 0, 1]
```

- [ ] **Step 2: Run the joint-ledger tests and confirm failure**

Run: `python -m pytest tests/test_joint_trade_blocks.py -q`

Expected: collection fails because `research_utils.joint_trade_blocks` does not exist.

- [ ] **Step 3: Implement deterministic union and concurrency marking**

Concatenate frames in sorted strategy-ID order, verify each frame's own strategy ID, select UTC order only when every row has UTC, otherwise use naive order for the whole joint ledger, and stable-sort by timestamp, strategy ID, then source row. Mark duplicated ordering timestamps as cross-strategy concurrent only when more than one strategy participates.

- [ ] **Step 4: Implement Monday-start weekly zero-fill**

Map each exit timestamp to `date - timedelta(days=date.weekday())`. Build the complete seven-day-spaced range from minimum to maximum week. For sorted strategy IDs, add `<strategy_id>_net_pnl_usd` and `<strategy_id>_trade_count`; add joint sums last. Attach `timestamp_domain` as `UTC` only when all exit UTC timestamps exist, otherwise `SOURCE_NAIVE_UNKNOWN_TIMEZONE`.

- [ ] **Step 5: Verify adapters**

Run: `python -m pytest tests/test_joint_trade_blocks.py -q`

Expected: PASS.

- [ ] **Step 6: Commit the joint plumbing**

```bash
git add lab/research_utils/joint_trade_blocks.py tests/test_joint_trade_blocks.py
git commit -m "feat: build deterministic joint trade blocks"
```

---

### Task 6: Orchestrate Phase 1, render reports, and run the frozen inputs

**Files:**
- Create: `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/run_phase1.py`
- Create: `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/.gitignore`
- Create: `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/README.md`
- Create: `tests/test_tradeify_phase1_runner.py`
- Generate: `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/reconciliation_manifest.json`
- Generate: `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/RESULTS.md`

**Interfaces:**
- Consumes: all Task 1–5 APIs, config path, source directory, and output directory.
- Produces: `run_campaign(config_path, source_dir, output_dir) -> CampaignResult`, CLI exit codes `0/2/3/4`, local CSV ledgers, committed aggregate JSON, and Markdown.

- [ ] **Step 1: Write failing synthetic end-to-end tests**

```python
def test_campaign_writes_local_rows_but_aggregate_contains_no_absolute_path(tmp_path):
    source_dir, config = _seven_source_fixture(tmp_path)
    output_dir = tmp_path / "local_artifacts"
    result = run_campaign(config, source_dir, output_dir)
    manifest_text = result.manifest_path.read_text(encoding="utf-8")
    assert result.status in {"RECONCILED_EXPLORATORY", "BLOCKED_EXPLORATORY"}
    assert (output_dir / "canonical_events.csv").exists()
    assert (output_dir / "canonical_trades.csv").exists()
    assert str(source_dir.resolve()) not in manifest_text
    assert "EXPLORATORY" in manifest_text


def test_campaign_output_is_byte_deterministic(tmp_path):
    source_dir, config = _seven_source_fixture(tmp_path)
    first = run_campaign(config, source_dir, tmp_path / "one")
    second = run_campaign(config, source_dir, tmp_path / "two")
    assert first.manifest_bytes == second.manifest_bytes
    assert first.report_bytes == second.report_bytes


def test_hash_failure_returns_intake_exit_code(tmp_path):
    source_dir, config = _seven_source_fixture(tmp_path)
    (source_dir / "one.csv").write_text("changed", encoding="utf-8")
    assert main(["--config", str(config), "--source-dir", str(source_dir)]) == 3
```

Add a write-failure test returning `4`, invalid invocation returning `2`, blocker reports returning `0`, and a report-order test fixed by configuration strategy order.

- [ ] **Step 2: Run runner tests and confirm failure**

Run: `python -m pytest tests/test_tradeify_phase1_runner.py -q`

Expected: collection fails because the campaign runner is absent.

- [ ] **Step 3: Implement orchestration and atomic local writes**

The runner must verify every Pine/export pair before parsing any CSV. Process all verified strategies independently and retain blocker reports. Write each CSV/JSON/Markdown payload to a temporary sibling path, flush/close it, then replace the destination with `Path.replace()`.

Serialize `Decimal` as fixed-point strings and timestamps as ISO-8601 strings. Set `sort_keys=True`, `indent=2`, and a final newline for JSON. Exclude run time, machine name, current directory, and absolute paths from deterministic artifacts. Include Git base commit, config SHA-256, source hashes, ledger hashes, code version, claim class, timestamp-domain label, and tolerance values.

- [ ] **Step 4: Render issue-led reports and local-only ledgers**

Write local:

```text
local_artifacts/canonical_events.csv
local_artifacts/canonical_trades.csv
local_artifacts/weekly_exit_blocks.csv
```

Write committed aggregates:

```text
reconciliation_manifest.json
RESULTS.md
```

The report starts with the Phase 0 skip/`EXPLORATORY` warning, then a seven-row status table, frozen tolerances, per-strategy accounting and issue sections, joint-ledger hashes, and reproduction command. Sort issues by severity rank, code, trade ID, and source rows.

- [ ] **Step 5: Add ownership documentation and ignore rule**

Set the campaign `.gitignore` to:

```gitignore
local_artifacts/
```

Document that the source directory is runtime-only, that the ledger is vendor-derived and deliberately local, that timezone completion needs an explicit TradingView display timezone, and that re-running Pine requires a separate bar/engine project.

- [ ] **Step 6: Verify the synthetic runner**

Run: `python -m pytest tests/test_tradeify_phase1_runner.py -q`

Expected: PASS.

- [ ] **Step 7: Run all focused tests before consuming the real sources**

Run:

```bash
python -m pytest tests/test_tv_trade_ledger.py tests/test_trade_reconciliation.py tests/test_joint_trade_blocks.py tests/test_cost_model.py tests/test_tradeify_phase1_runner.py -q
```

Expected: PASS with no skipped focused tests.

- [ ] **Step 8: Execute the frozen seven-strategy campaign**

Run:

```powershell
python lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/run_phase1.py --config lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/phase1_config.json --source-dir 'C:\Users\joshu\Downloads\strategies' --output-dir lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts
```

Expected: exit `0`; seven aggregate strategy reports; local event/trade/weekly files; campaign status `BLOCKED_EXPLORATORY` because timezone and known strategy blockers remain.

- [ ] **Step 9: Assert the frozen acceptance numbers from generated JSON**

Run:

```powershell
python -c "import json,pathlib; p=pathlib.Path('lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/reconciliation_manifest.json'); d=json.loads(p.read_text()); exp={'aegis_6j1':(244,122,'28702.75'),'orb_mnq_recon_v7':(1362,681,'47533.16'),'striker_dj30_mnq_prototype':(406,203,'10208.62'),'striker_dj30_mym_v45':(406,203,'31770.36'),'striker_nas100_mnq_v1':(756,378,'112253.42'),'striker_nas100_mym_prototype':(368,184,'170250.58'),'vanguard_mgc_v04':(686,343,'20388.04')}; got={s['strategy_id']:(s['source_row_count'],s['trade_count'],s['net_pnl_usd']) for s in d['strategies']}; assert got==exp,(got,exp); orb=next(s for s in d['strategies'] if s['strategy_id']=='orb_mnq_recon_v7'); assert orb['issue_counts']['FORCE_FLAT_VIOLATION']==3; print('frozen acceptance values verified')"
```

Expected: `frozen acceptance values verified`.

- [ ] **Step 10: Check that Git cannot see vendor or local-ledger rows**

Run: `git status --short --ignored`

Expected: `local_artifacts/` appears ignored; no source Pine/CSV appears as staged or untracked.

Run: `rg -n "C:\\\\Users\\\\joshu|Date and time,Signal,Price USD" lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09 -g '!local_artifacts/**'`

Expected: no matches.

- [ ] **Step 11: Run the full test suite**

Run: `python -m pytest -q`

Expected: PASS. If an unrelated pre-existing failure occurs, record the exact failing test and demonstrate that every focused Phase 1 test still passes; do not alter unrelated code.

- [ ] **Step 12: Commit reports and runner**

```bash
git add lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09 tests/test_tradeify_phase1_runner.py
git commit -m "feat: run Tradeify seven-strategy Phase 1 reconciliation"
```

---

## Final review checkpoint

- [ ] Read the approved specification and map every requirement to Tasks 1–6.
- [ ] Search the implementation and reports for `OOS`, `confirmatory`, `qualified`, `admitted`, and `deployable`; each occurrence must either deny the claim or be removed.
- [ ] Review `git diff 11d22e280db71d798f5c4e37edd85a62bc71f392...HEAD` for source rows, absolute paths, silent repairs, fee substitution, and timezone inference.
- [ ] Run the focused suite and full suite again from a clean worktree.
- [ ] Request code review, resolve verified findings with the receiving-code-review workflow, and repeat verification before claiming Phase 1 complete.
