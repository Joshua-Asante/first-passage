# Tradeify Five-Active-Source Phase 1 Normalization Design

**Status:** Approved by the operator on 2026-09-02
**Branch:** `codex/tradeify-stage1-normalization`
**Base:** `11d22e280db71d798f5c4e37edd85a62bc71f392`
**Claim class:** `EXPLORATORY`

## 1. Goal and scope

Build a deterministic, strict reconciliation pipeline for five retained TradingView Pine/CSV pairs. The pipeline folds the skipped Phase 0 inventory duties into Phase 1, converts every active source row into a canonical event representation, reconstructs one accounting record per trade, validates instrument and venue constraints, and emits one aggregate reconciliation report per strategy plus a joint-ledger manifest. Two dropped swap-port records remain provenance-only inventory.

The operator explicitly skipped Phase 0. Therefore all supplied history is consumed development data. Nothing produced by this phase may be described as untouched, out-of-sample, confirmatory, qualified, admitted, or deployable.

The phase reproduces the exports' accounting and event structure. It does not re-run Pine signal logic: the supplied set does not include the TradingView execution engine or a complete, timestamp-compatible bar corpus.

## 2. Source set and frozen identity

The source directory is supplied at runtime and is not encoded as an absolute path in committed artifacts. Basenames and SHA-256 values are frozen below.

| strategy ID | intended instrument | Pine source (SHA-256) | TradingView export (SHA-256) | known intake concern |
|---|---|---|---|---|
| `aegis_6j1` | `6J` | `aegis_6J1_venue_bound.pine` (`db78ecba95ae78aca14501a5eaccfda2a42164d83cac12321cb7f293a9adca7c`) | `Aegis_6J1_VB_CME_6J1!_2026-09-03_cc310.csv` (`71e732fc92d28a56fbc1e4aa358e10b68f317a110f3facc95ed34508fad96eaa`) | venue-bound inventory; Pine declares `$1.30`/side while export charges `$3.10`/side/contract |
| `orb_mnq_recon_v7` | `MNQ` | `orb_mnq_7_reconstruction_venue_bound.pine` (`176c4f70c67d58053c4d3b8170d0a9be3733bc6b76b1e2f928bd7a877be052a3`) | `ORB-MNQ-1_recon_v7_VB_CME_MINI_MNQ1!_2026-09-03_d03ac.csv` (`bff235ea0934dace8a000dbad7eeede8673506718bd020f54f2c04cbae304568`) | venue-bound reconstruction; old Friday-to-Sunday hold inventory is not current |
| `striker_dj30_mym_pyramid_250` | `MYM` | `striker_dj30_v4.5_mym_pyramid_250_cap100k.pine` (`712cf395396568ce22ae43f1f15b085eaba23acf1b85502abb92129f277fffd7`) | `Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-09-03_9d7ea.csv` (`5a5006588fa5c87628df7b1c15c8af8d8ae2250be0abb0371ea4d93665ef998e`) | `UNPINNED_MODIFIED` 100K body; `pyramid 250% vs locked 750%; initial_capital 100000 vs research-variant pin 200000` |
| `striker_nas100_mnq_dow_wed_excluded` | `MNQ` | `striker_nas100_v1_mnq_dow_wed_excluded_cap100k.pine` (`fa6a70cde002131bbd266bee70defb01e32deae2de79fdc327d661f829115c39`) | `Striker_NAS100_MNQ_CME_MINI_MNQ1!_2026-09-03_30a74.csv` (`f6a93bb653d710a77f8ebde8e64639ed913171c814cd13de5f00f76d0c3d1513`) | `UNPINNED_MODIFIED` 100K body; `day-of-week set {Mon,Tue,Thu,Fri} vs locked {Mon,Tue}; initial_capital 100000 vs research-variant pin 200000` |
| `vanguard_mgc_v04` | `MGC` | `Vanguard_Gold_MGC_v0.4_venue_bound.pine` (`af26899ca94bb0e9ee26d09e0176b6b94bba2f5da252399ce4d899fe7e3bad15`) | `Vanguard_Gold_Futures_v0.4_VB_(MGC)_COMEX_MINI_MGC1!_2026-09-03_0e3e3.csv` (`7b9cc65c98945055f35d55cdd43f049efc4b5924e2caa59f36d50b3eb872f9f2`) | venue-bound inventory; fee is `$2.12` round trip |

Both research variants have their candidate `PORT_MANIFEST.sha256` pin refs recorded in configuration. The dropped `striker_dj30_qtxg1_swap_body_on_mym` and `striker_nas100_qtxg1_swap_body_on_mnq` records retain their original export/Pine basenames, hashes, and archive pin refs with reason `SWAP_PORT_BODY_POINT_VALUE_NOT_OVERRIDDEN`. Their 4× wrong point-value sizing interacts with cap/pyramid, is not rescalable, and is never repaired. They are provenance only, never normalized or counted.

Hash mismatch, byte-length mismatch, missing file, extra configured source, or filename mismatch is a hard intake error. A configured instrument disagreement is a reportable blocking issue; it is never repaired by substituting an instrument.

## 3. Data ownership

The ten active supplied files and the generated row-level event/trade ledgers remain local and gitignored. Git receives only:

- source basenames and SHA-256 pins;
- a compact primary-source Tradeify fee capture and its SHA-256;
- implementation and deterministic synthetic fixtures/tests;
- aggregate reconciliation JSON and Markdown;
- row counts, date bounds, metrics, issue counts, and output hashes;
- no absolute source path and no complete vendor-derived row stream.

The campaign runner writes local material under `local_artifacts/`. The directory is ignored by a campaign-local `.gitignore`.

## 4. Architecture and interfaces

### 4.1 Frozen campaign configuration

`phase1_config.json` defines each active strategy ID, source basenames/hashes/byte lengths, intended instrument, instrument encoded by the export filename, Pine-declared commission/slippage/pyramiding, `pine_pin_status`, nullable `pin_ref`, declared bar size/session/direction evidence, platform and lineage notes, quantity convention, continuous-symbol status, and `source_timezone`. It also defines strictly validated `dropped_sources` and `continuous_contract_roll_policy` objects. The actual `PORT_MANIFEST.sha256` is parsed once per inventory load: pinned active/dropped refs require safe normalized repo-relative target membership, equal Pine basename and equal SHA-256. Directory placement belongs to the manifest, not hardcoded candidates/archive prefixes; malformed/duplicate/dangling entries fail closed. `PINNED_RESEARCH_VARIANT` requires nonempty divergence; `NOT_IN_PORT_MANIFEST` has null ref/divergence. `UNPINNED_MODIFIED` requires an existing ancestor ref without claiming equal modified-body hash. Private dropped source bytes are never read.

Operator ruling D9 freezes `source_timezone="America/New_York"` for all five active strategies. Direction, bar-size, session, venue, scalar-MAE, and synchronized-intraday-path availability remain inventoried without inferring any other missing evidence. Operator ruling D8 freezes the actual Pine pyramid values: DJ30 is a 250% research cell versus locked 750%; NAS100 remains 1000%.

### 4.2 Strict source normalization

`research_utils.tv_trade_ledger` owns the TradingView schema and normalization:

- accept UTF-8 with an optional BOM;
- require each canonical column exactly once after known alias normalization;
- retain `source_row_number`, `source_row_sha256` (SHA-256 of exact raw CSV record bytes, including its original terminator when present), raw timestamp text, signal text, type text, and all numeric source fields;
- parse money and quantity through `Decimal`, rejecting non-finite or malformed values;
- classify event type and direction from `Type` without guessing unknown labels;
- verify configured byte length and SHA-256 before parsing;
- retain the source row ordering and assign canonical order by `(timestamp_naive, source_row_number)`;
- flag same-timestamp groups rather than inventing causal order;
- localize the frozen `America/New_York` source wall time with `zoneinfo`, convert to UTC, and derive the configured session-timezone date;
- treat ambiguous or nonexistent DST timestamps as hard errors and never guess a fold or repair a wall time.

### 4.3 Strict trade reconstruction

`research_utils.trade_reconciliation` groups events by strategy and source trade number. A valid simple trade has exactly one entry and one exit, matching direction, positive integral quantities, entry time not after exit time, and duplicated trade-summary values that agree within frozen tolerances.

Orphan legs, duplicate legs, partial exits, pyramiding within one trade ID, direction disagreement, negative/zero quantities, or reversed timestamps are retained as issues. They are not silently skipped and are not reduced to “first entry.” Unsupported structures block the affected strategy's simple-trade reconciliation while the source events remain preserved locally.

The reconstructed trade ledger carries entry/exit timestamps and prices, quantity, net P&L, commission, scalar MAE/MFE, duration, and source-row references. Scalar MAE/MFE remain explicitly `excursion-bounded`; they do not become a timestamped intratrade path.

### 4.4 Reconciliation and venue checks

For each structurally valid strategy, compute from exit-designated trade rows:

- trade count and date bounds;
- net P&L and commission totals;
- gross P&L only when the export identity proves `gross = net + commission`; otherwise `UNKNOWN`;
- wins, losses, flats, win rate, and profit factor;
- chronological running-net maximum drawdown;
- exit-month net totals;
- final cumulative-P&L agreement;
- entry/exit tick-grid alignment using `lab.discovery.cost_model.INSTRUMENT_SPECS`;
- simultaneous open quantity in Tradeify micro-equivalents (`6J=10`, `MNQ/MYM/MGC=1`) and the per-strategy 80-micro account-cap check; the joint book-cap verdict is deferred to Phase 4;
- daily Tradeify force-flat crossings, raw cross-date holds, and Friday-to-Sunday holds as a sub-count;
- same-timestamp ordering ambiguity.

The cost layer leaves `lab/discovery/cost_model.py` unchanged: its closed-world separation between instrument geometry and the production index-micro fee scalar is intentional. Campaign-local geometry includes the repo-verified 6J specification (`multiplier=12_500_000`, `tick_size=0.0000005`, `tick_value=6.25`) and reuses existing MNQ/MYM/MGC geometry.

`tradeify_commission_schedule.json` captures and hashes the four relevant rows from Tradeify's primary commission schedule (`https://help.tradeify.co/en/articles/10468315-trading-commission-fees`, page date 2026-04-28, observed 2026-09-02). Total round-trip costs are 6J `$6.20`, MNQ `$1.82`, MYM `$1.82`, and MGC `$2.12`, inclusive of exchange, NFA, clearing, and commissions. The runner derives per-side values of `$3.10`, `$0.91`, `$0.91`, and `$1.06` and reconciles them to `core/firm_rules.py` comments without using its index-micro scalar as a non-index resolver. Pine-declared, export-implied, and venue fee bases remain separate report fields.

Bid/ask spread is recorded as not separately observable in the TradingView trade list. Pine-declared adverse slippage ticks and fill-price-derived P&L are retained separately; the runner never invents a spread or double-charges slippage already embedded in fills.

Venue checks identify violations but never edit trades. `FORCE_FLAT_VIOLATION` is a blocker whenever a venue deadline instant falls in `(entry, exit]`: `16:45 America/New_York` every regular day and `12:59 America/New_York` on an allowlisted CME early-close date. `overnight_holds` is the deadline-spanning count; raw date boundaries remain separately inventoried as `cross_date_holds`. The historical ORB-MNQ three Friday-to-Sunday-hold inventory is not current for the venue-bound source; N4's fresh ledger is the only current count. The total force-flat violation count is whatever the daily-deadline audit yields.

`cme_early_close_calendar.json` is hashed with the other campaign inputs. Its primary-source path remains unchanged, but the separately tagged secondary path may be `COMPLETE` only with the exact D19 accepted-secondary metadata and complete verified venue-date membership; D19 does not upgrade it to primary evidence or product close-time/exchange-session modeling. It binds only the secondary account-level `EARLY_CLOSE` union to 12:59 ET rows and never infers dates, unions trade-date full closures, or fabricates annual CME captures. The report retains the 13 unresolved and 3 sub-deadline source limitations, the conservatively included 2025-11-28 scheduled-half-day/outage classification, and possible non-conservative missing ad-hoc closures from 2026-05-28 through 2026-09-02.

If explicitly selected, the separately tagged `tradeify_secondary_early_close/v1` adapter binds a wrapper to the exact bytes of `ops/calendars/cme_holiday_calendar_2022_2026.json`, whose provenance remains `SECONDARY`. The exact D19 object permits `COMPLETE` for verified venue-date membership only; absent, malformed, or incomplete D19 evidence remains `NEEDS_CONTEXT` or fails closed. It accepts only the verified account-level union of entry dates with any `EARLY_CLOSE` group as 12:59 ET deadline rows, including when another campaign product group such as 6J is `NORMAL`. CME-trade-date full closures remain inventory rather than wall-date deadline rows. Pre-12:59 closes, unresolved details, inert source URLs, source-revision caveat, 2025-11-28 conservative classification, and possible non-conservative missing 2026-05-28..2026-09-02 ad-hoc closures remain published limitations. The primary calendar schema and its yearly-CME-capture checks remain unchanged.

> ### ⚠ Amendment 2026-09-03 — D19: a SECONDARY-sourced calendar is accepted
>
> **Operator ruling D19** ([campaign state](../../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md) §6):
> *"I accept the secondary source."* The paragraph above is amended for this campaign only.
>
> **Why the amendment was needed rather than a workaround** (Codex on
> [#293](https://github.com/Joshua-Asante/first-passage/pull/293), P1, accepted): without it, a worker
> following this frozen design *cannot implement D19*, and a worker following D19 *silently violates
> this design*. Two contradictory rules governing one runner is the defect; this records the single
> executable one.
>
> **Amended rule.** `coverage_status: COMPLETE` may be claimed on a calendar whose rows derive from
> [`ops/calendars/cme_holiday_calendar_2022_2026.json`](../../../ops/calendars/README.md) — a
> **SECONDARY** reconstruction from independent third-party encodings, cross-checked against in-repo
> bar panels, with **no CME primary source** (403 at the egress proxy on cmegroup.com and every broker
> mirror). The row set must equal `derived.venue_flat_dates` intersected with the declared coverage
> span, exactly — never a subset, and never the union with `full_closure_dates`.
>
> **Unchanged by the amendment.** The runner still must not *infer* holiday dates: every row traces to
> that file. `FORCE_FLAT_VIOLATION` semantics are untouched. The other blocker dimensions, including
> `CONTINUOUS_CONTRACT_ROLL_UNRESOLVED`, still cap their own verdicts — D19 lifts the calendar-derived
> cap and nothing else.
>
> **Scope.** The acceptance covers **date membership**, which is all this campaign asks of the file
> (Tradeify's holiday-short deadline is a blanket 12:59 ET account-level rule). It does **not** extend
> to the per-group close-time fields, where the calendar's `unresolved` register carries live disputes
> of up to ~3h15m on MGC and ~4h on 6J.

All five active exports identify continuous `1!` chart symbols rather than specific tradable contract months. Each report emits `CONTINUOUS_CONTRACT_ROLL_UNRESOLVED`; without a roll ledger or individual-contract export, Phase 1 cannot prove which contract generated a fill or whether a fill crosses a back-adjustment seam. Operator ruling 2026-09-03, campaign-state §6 D13(b), accepts the continuous basis for Phases 2–4 as `ACCEPTED_UNMODELED`, not resolved. Exact config policy keys are `{disposition, ruling_date, ruling_ref, obligations}`; accepted metadata requires a valid ISO date, nonempty reference and exactly the two frozen distinct obligations below. The immutable policy flows explicitly to `analyze_venue`; only the roll issue becomes WARNING, while attribution remains UNAVAILABLE and other blockers remain unchanged. Absent policy on other callers defaults to the unresolved BLOCKER.

- Phase 3 pre-registration states back-adjustment seam risk as a limitation of every campaign claim: fills cannot be attributed to a contract month, and a seam crossing is indistinguishable from a price move.
- A Phase 6 seam-sensitivity check is pre-registered with its severity frozen alongside the other Phase 6 cutoffs.

Policy/reference/obligations are echoed in aggregate, per-strategy and detail reports. This acceptance does not discharge those future obligations.

### 4.5 Joint ledger and weekly adapter

`research_utils.joint_trade_blocks` concatenates normalized events using deterministic ordering `(timestamp_utc when available else timestamp_naive, strategy_id, source_row_number)`. Cross-strategy timestamp ties are marked concurrent.

The calendar-week adapter groups trade exits by ISO Monday-start week while preserving empty weeks between the minimum and maximum exit date. It returns both per-strategy columns and a joint total. This is plumbing only: Phase 1 performs no portfolio ranking, dependence estimation, bootstrap, or qualification simulation.

Phase 1 delivers deterministic joint event union and ISO-week exit aggregation only; neither is a joint-flat block builder. The joint-flat block builder is deferred to Phase 3, before Phase 4 composition, because it requires a synchronized all-leg chronology and must prove every included leg is flat at each block edge. The final replacement ledger has zero Friday-to-Sunday holds; no Phase 1 ranking, dependence, composition, Monte Carlo, or Pine rerun occurs.

### 4.6 Campaign runner and reports

`run_phase1.py` accepts `--source-dir`, `--output-dir`, and `--config`. It first verifies the ten active files, then processes strategies independently so one blocked strategy does not erase the other reports. It writes local canonical event/trade ledgers atomically, hashes them, and writes aggregate JSON/Markdown deterministically. Aggregate outputs render five active sources plus two dropped provenance records; dropped sources never enter ledgers or weekly results.

Exit codes:

- `0`: run completed and all configured reports were written, even when reports contain expected reconciliation blockers;
- `2`: invocation or configuration error;
- `3`: source identity/schema failure prevented a complete five-active-source run;
- `4`: output write failure.

Each strategy status is one of:

- `RECONCILED_EXPLORATORY`: structural/accounting tolerances pass and no strategy blocker remains;
- `BLOCKED_EXPLORATORY`: at least one structural, identity, timezone, cost, or venue blocker remains;
- `FAILED_INTAKE`: source identity/schema prevented normalization.

The campaign-wide status is the most severe constituent status. D13(b)'s accepted-unmodeled continuous-roll limitation alone no longer blocks this campaign, but other callers without explicit acceptance retain the roll blocker. D19 accepts the tagged `SECONDARY` calendar's venue-date membership as `COMPLETE` only when its rows are set-equal to `derived.venue_flat_dates` over the declared coverage span; it neither models close times or exchange sessions nor suppresses its preserved residuals. Missing independent scalar summaries retain the `NEEDS_CONTEXT` cap; D17 governs their scope (monthly totals reconstructed from the row-level ledger and commissions amended out). Generation `tradeify-phase1-normalization-v3` is echoed in manifest/RESULTS; fee/config/calendar/summary digests come from exact parsed byte snapshots, never a post-load reread. Every other cap is unchanged.

## 5. Frozen tolerances and ordering

- Source hashes, row counts, trade IDs, event labels, timestamp text, quantities, and pairing cardinality: exact.
- Currency fields and aggregates: `Decimal` quantized to `$0.01`; absolute tolerance `$0.01` only at source-vs-derived aggregate boundaries.
- Independent TradingView summary comparisons: trade count exact; net P&L, commissions, max drawdown, and each monthly amount use inclusive absolute `$0.01`; win rate uses inclusive `0.01` percentage point after converting the accounting ratio to percent; profit factor uses inclusive absolute `0.01`. These display-precision tolerances are frozen before the rerun, not fitted to its outputs. Monthly key sets must agree; missing months are not zero-filled. Undefined nulls match only each other, never missing anchors.
- Prices: retained at source precision; tick-grid remainder tolerance `1e-9` tick.
- Win/loss classification: net P&L compared to exact zero before display quantization.
- Timestamp order: parsed naive timestamp, then original one-based source row number. No entry/exit priority is introduced for equal timestamps.
- Joint ties: strategy ID, then source row number, while retaining `concurrent_timestamp=true`.
- Monthly groups: exit calendar month in the source timestamp domain until timezone is known.
- Weekly groups: ISO week beginning Monday in the same explicitly labeled timestamp domain; missing weeks appear with zero P&L and zero trades.

## 6. Failure and evidence policy

The CME calendar has exact top-level keys `source_url`, `page_date`, `observed_date`, `coverage_start`, `coverage_end`, `coverage_status`, `coverage_note`, `sources`, `rows`. Each source has exactly `{year, source_url, page_date, capture_basename, sha256}`: unique integer year (not bool), primary CME HTTPS URL, nonnull ISO page date, safe local basename, lowercase SHA-256. Each row has exactly `{date, deadline_local, source_year}`; its year must resolve to the declared source. The capture file is loaded from `local_artifacts/calendar_captures` (explicit test directory override allowed); traversal and symlink escapes are rejected, and its exact bytes must match the source hash.

Supported primary captures remain reviewed yearly JSON extracts with exact `{year, source_url, page_date, rows}` keys and `{date, deadline_local}` rows; raw PDF/HTML needs a separately reviewed extraction step. The D19 accepted-secondary wrapper is the checked-in path for this generation: it covers 2022-01-01 through 2026-12-31 with 49 verified venue-date rows and preserves `SECONDARY` provenance. Calendar `COMPLETE` here means only accepted venue-date membership; it neither establishes primary historical truth nor changes the unresolved product-close and exchange-session limitations.

Independent anchors live in `tv_summary_anchors.json` with `EXPLORATORY` claim class. The loader accepts either the legacy four-key top-level schema `{claim_class, coverage_status, coverage_note, strategies}` or the current optional-D17 schema `{claim_class, coverage_status, coverage_note, d17_policy, strategies}`. Every strategy record has exact `{strategy_id, export_sha256, source_note, metrics, missing_metrics}` keys; active IDs are unique, export hashes must match, and dropped IDs are forbidden. In the legacy branch, `metrics` has seven keys: `trade_count`, `net_pnl_usd`, `win_rate_pct`, `profit_factor`, `max_drawdown_usd`, `total_commissions_usd`, and `monthly_net_pnl_usd`. With `d17_policy`, `metrics` has exactly the five scalar keys `trade_count`, `net_pnl_usd`, `win_rate_pct`, `profit_factor`, and `max_drawdown_usd`; commissions and monthly totals are not independent anchor metrics. `d17_policy` itself has exactly `{ruling_date, ruling_ref, monthly_totals, commissions, reason}`, with `monthly_totals` fixed to `RECONSTRUCTED` and `commissions` fixed to `AMENDED_OUT`. Trade count is a nonnegative integer (not bool); scalar decimal values and canonical `YYYY-MM` legacy monthly amounts are finite decimal strings, never JSON floats. Rates are within [0,100]; drawdown, commissions and factor are nonnegative. Missing metric names must be unique and known, with null values; semantic undefined profit factor or zero-trade win rate nulls are NOT listed as missing.

The prior Key-stats panels are historical and never rebound to replacement hashes. The current D17 inventory has `strategies: []` and leaves five independent scalar requirements (count, net, win rate, profit factor, max drawdown); absent fresh panels emit `MISSING_ANCHOR`. Monthly totals are exact exit-month reconstructions from canonical row-level trades and appear only in gitignored local artifacts; manifest/RESULTS/detail outputs retain hashes, basis, bucket count, status and residuals but no monthly map. Independent commission evidence is `AMENDED_OUT` because no independent total exists; derived commission is inventory and fee-audit behavior is unchanged. Present scalar mismatches emit `TV_SUMMARY_MISMATCH` blockers while retaining accounting. `summary_reconciliation_status` can be `COMPLETE` only with every active scalar anchor; the Phase 1 context cap remains `NEEDS_CONTEXT` until fresh panels arrive. Calendar and anchor hashes are frozen from the exact bytes parsed, not a later reread.

All issues use stable codes, severity (`INFO`, `WARNING`, `BLOCKER`, `FATAL`), strategy ID, source rows when applicable, and deterministic detail fields. Reports sort issues by severity, code, trade ID, and source row.

Expected source defects are data, not exceptions. Programming errors and invalid configuration fail loudly. The runner uses temporary sibling files plus atomic replacement so a failed run cannot leave a new file that looks complete.

No result may tune, delete, relabel, roll, or shift a source trade to improve reconciliation. Any later operator-supplied timezone or fee value changes the configuration fingerprint and generates a new report fingerprint.

## 7. Verification and acceptance

The implementation is accepted when:

1. Synthetic tests prove strict schema/hash behavior, Decimal parsing, duplicate/orphan handling, timezone/DST handling, stable ties, tick conversion, fee-table reconciliation, overlap/cap measurement, force-flat reporting, weekly zero-fill, and deterministic output.
2. `lab/discovery/cost_model.py` remains byte-unchanged, and the existing cost-model tests still pass.
3. Existing production firm-barrier tests for Tradeify trailing drawdown, intraday lows, lock behavior, consistency, and horizon-cap outcomes pass and are recorded in the verification evidence.
4. A local smoke run verifies all ten active frozen file hashes and byte lengths, produces five reports plus joint-ledger hashes, and inventories the two dropped records without committing source or row-level data.
5. The final replacement-source run reports row/trade counts in configuration order: Aegis `242/121`, ORB-MNQ `1362/681`, DJ30-MYM pyramid-250 `406/203`, NAS100-MNQ DOW cell `756/378`, Vanguard-MGC `676/338`.
6. Aggregate net P&L reproduces to the cent: `$27,996.05`, `$48,118.16`, `$32,057.36`, `$112,253.42`, and `$18,709.48`, respectively. The exact replacement pairs remain the 2026-09-03 basename/byte/SHA pins in §2; no source body is copied or edited.
7. All five final ledgers report zero `FORCE_FLAT_VIOLATION` and zero Friday-to-Sunday holds. D19 accepts only the 49-date secondary venue-date membership as calendar `COMPLETE`; full-closure dates and product close-time/exchange-session claims remain excluded.
8. The final D17 records five local monthly-reconciliation hashes with bucket counts `45/49/48/49/48`, `RECONSTRUCTED` status, zero aggregate residuals, and no tracked per-month figures. Independent scalar panels remain `MISSING_ANCHOR`; DJ30's unexplained +$287 replacement-versus-prior-200K net delta remains a caveat, not a repaired comparison.
9. Every strategy reports missing contract-month/roll provenance for its continuous `1!` export.
10. Committed artifacts contain no `C:\Users\...` source path and no raw row-level ledger.

## 8. Explicit exclusions

- No Phase 0 split, holdout, or pre-registration.
- No strategy selection, comparison, ranking, or parameter tuning.
- No portfolio-dependence conclusions or Monte Carlo qualification.
- No Pine modification, production strategy lock, allocation, lifecycle, rail, or deployment change.
- No silent correction of weekend dates, timestamps, instruments, fees, quantities, or trade structure.
