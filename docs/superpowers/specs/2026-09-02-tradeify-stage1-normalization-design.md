# Tradeify Seven-Strategy Phase 1 Normalization Design

**Status:** Approved by the operator on 2026-09-02
**Branch:** `codex/tradeify-stage1-normalization`
**Base:** `11d22e280db71d798f5c4e37edd85a62bc71f392`
**Claim class:** `EXPLORATORY`

## 1. Goal and scope

Build a deterministic, strict reconciliation pipeline for the seven supplied TradingView Pine/CSV pairs. The pipeline folds the skipped Phase 0 inventory duties into Phase 1, converts every source row into a canonical event representation, reconstructs one accounting record per trade, validates instrument and venue constraints, and emits one aggregate reconciliation report per strategy plus a joint-ledger manifest.

The operator explicitly skipped Phase 0. Therefore all supplied history is consumed development data. Nothing produced by this phase may be described as untouched, out-of-sample, confirmatory, qualified, admitted, or deployable.

The phase reproduces the exports' accounting and event structure. It does not re-run Pine signal logic: the supplied set does not include the TradingView execution engine or a complete, timestamp-compatible bar corpus.

## 2. Source set and frozen identity

The source directory is supplied at runtime and is not encoded as an absolute path in committed artifacts. Basenames and SHA-256 values are frozen below.

| strategy ID | intended instrument | Pine source (SHA-256) | TradingView export (SHA-256) | known intake concern |
|---|---|---|---|---|
| `aegis_6j1` | `6J` | `aegis_6J1.pine` (`8578ee3d760b5112bb1dd77e65a07466aee8629a9424e4115e422fdaab5aede8`) | `Aegis_6J1_CME_6J1!_2026-09-02_a0c7a.csv` (`7affdcb832db31b2d6b18b1e379b59206e7166e2a7f166fb310aaed484c69bb9`) | Pine declares `$1.30`/side while the export charges `$3.10`/side/contract |
| `orb_mnq_recon_v7` | `MNQ` | `orb_mnq_7_reconstruction.pine` (`f05c7aa429846811149e6ff7c8e63a2fd4457075b6c45dedfc77c7e0fa76e9b4`) | `ORB-MNQ-1_recon_v7_CME_MINI_MNQ1!_2026-09-02_c1f14.csv` (`ece1eaf52db118302c6e51b1781dd47decb57f67f44d6990c4ea0ba3500281e6`) | development-tuned reconstruction; three Friday-to-Sunday holds |
| `striker_dj30_qtxg1_swap_body_on_mym` | `MYM` | `striker_dj30_v4.5_mnq_qtxg1_prototype.pine` (`178a2a8e1c78e45a5142749f92284c09d286907a7e096883e1133297cb8a806d`) | `Striker_DJ30_MNQ_Q-TXG-1_PROTOTYPE_CBOT_MINI_MYM1!_2026-09-02_82cba.csv` (`2c2d893ba0daa127f1c857e81ec436b535e4e8eb85f0c728e2ba39dc6485826d`) | `PINNED_SWAP_PROTOTYPE`: DJ30 logic ported to MNQ, exported here on MYM at pyramid 750; literal `EXPLORATORY` chart run only, not locked/native-edition evidence or proof of correct swap-port point-value overrides |
| `striker_dj30_native_pyramid_down_on_mym` | `MYM` | `striker_dj30_v4.5_mym.pine` (`5c4b1026cb6f3a475dba962783b2a053e9fbeb123570dd964d7154ea80b3f9d0`) | `Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-09-02_4e60e.csv` (`7082a16d5ec8b17dafa4bf0b026c0a5dc23190de9d21d4036700f0ce97448c63`) | `UNPINNED_MODIFIED`: local byte diff against `2b895317…` changes only `pyramidSize` default 750→250; sole pyramid-down source, not a pinned locked venue edition |
| `striker_nas100_native_dow_modified_on_mnq` | `MNQ` | `striker_nas100_v1_mnq.pine` (`d18c2699ea3856df884eced84c9384adea953f3a2470bea4f2d671b6cd294057`) | `Striker_NAS100_MNQ_CME_MINI_MNQ1!_2026-09-02_57a64.csv` (`edfe73c60b441c13855d0129dc82e830b032b7159313519d5a212a97cf30f22a`) | `UNPINNED_MODIFIED`: local byte diff against `bb921399…` changes only `allowThu` and `allowFri` defaults false→true; pyramid remains 1000, a DOW-modified body, not pyramid-down |
| `striker_nas100_qtxg1_swap_body_on_mnq` | `MNQ` | `striker_nas100_v1_mym_qtxg1_prototype.pine` (`19264da29a3d9a30200600689e1950931f1abfb648e9071a232ee83fdec2756c`) | `Striker_NAS100_MYM_QTXG1_CME_MINI_MNQ1!_2026-09-02_304f8.csv` (`f1e35c4ee1c9735c3ebbed99648a42034d9b3f57b53960f9e41f6e6c09b25f9c`) | `PINNED_SWAP_PROTOTYPE`: NAS100 logic ported to MYM, exported here on MNQ at pyramid 1000; literal `EXPLORATORY` chart run only, not locked/native-edition evidence or proof of correct swap-port point-value overrides |
| `vanguard_mgc_v04` | `MGC` | `Vanguard_Gold_MGC_v0.4.pine` (`ae5fd66ce51c478187c605574a03f89a64e6f8f245e77477eeaedd1efe2cf772`) | `Vanguard_Gold_Futures_v0.4_(MGC)_COMEX_MINI_MGC1!_2026-09-02_65e4e.csv` (`491d41c7168b1a9645efb74fb4ac9b898c8a6e3a5ce4c8fbbc4ddd5c9e6ced83`) | venue fee is `$2.12` round trip; continuous-symbol roll provenance remains absent |

Hash mismatch, missing file, extra configured source, or filename mismatch is a hard intake error. A configured instrument disagreement is a reportable blocking issue; it is never repaired by substituting an instrument.

## 3. Data ownership

The fourteen supplied files and the generated row-level event/trade ledgers remain local and gitignored. Git receives only:

- source basenames and SHA-256 pins;
- a compact primary-source Tradeify fee capture and its SHA-256;
- implementation and deterministic synthetic fixtures/tests;
- aggregate reconciliation JSON and Markdown;
- row counts, date bounds, metrics, issue counts, and output hashes;
- no absolute source path and no complete vendor-derived row stream.

The campaign runner writes local material under `local_artifacts/`. The directory is ignored by a campaign-local `.gitignore`.

## 4. Architecture and interfaces

### 4.1 Frozen campaign configuration

`phase1_config.json` defines each strategy ID, source basenames/hashes, intended instrument, instrument encoded by the export filename, Pine-declared commission/slippage/pyramiding, `pine_pin_status`, declared bar size/session/direction evidence, platform and lineage notes, quantity convention, continuous-symbol status, and `source_timezone`. `PORT_MANIFEST.sha256` is authoritative for `pine_pin_status`; its closed values distinguish pinned swap prototypes, unpinned modified bodies, and sources absent from that manifest.

Operator ruling D9 freezes `source_timezone="America/New_York"` for all seven strategies. Direction, bar-size, session, venue, scalar-MAE, and synchronized-intraday-path availability remain inventoried without inferring any other missing evidence. Operator ruling D8 freezes the actual Pine pyramid values: exactly one reduced cell (DJ30 250% versus its 750% sibling); both NAS100 Pines remain 1000%. The seven exports represent five entry/exit templates.

### 4.2 Strict source normalization

`research_utils.tv_trade_ledger` owns the TradingView schema and normalization:

- accept UTF-8 with an optional BOM;
- require each canonical column exactly once after known alias normalization;
- retain `source_row_number`, raw timestamp text, signal text, type text, and all numeric source fields;
- parse money and quantity through `Decimal`, rejecting non-finite or malformed values;
- classify event type and direction from `Type` without guessing unknown labels;
- verify the configured SHA-256 before parsing;
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

Venue checks identify violations but never edit trades. `FORCE_FLAT_VIOLATION` is a blocker whenever a venue deadline instant falls in `(entry, exit]`: `16:45 America/New_York` every regular day and `12:59 America/New_York` on an allowlisted CME early-close date. `overnight_holds` is the deadline-spanning count; raw date boundaries remain separately inventoried as `cross_date_holds`. ORB-MNQ's exactly three Friday-to-Sunday holds remain in every total as a sub-count; the total force-flat violation count is whatever the daily-deadline audit yields.

`cme_early_close_calendar.json` freezes the primary-source CME holiday-calendar capture over the seven exports' combined date span and is hashed with the other campaign inputs. When complete primary-source rows cannot be captured, the file and every report say `NEEDS_CONTEXT`; the runner must not infer holiday dates or silently claim complete 12:59 coverage.

All seven exports identify continuous `1!` chart symbols rather than specific tradable contract months. Each report emits `CONTINUOUS_CONTRACT_ROLL_UNRESOLVED`; without a roll ledger or individual-contract export, Phase 1 cannot prove which contract generated a fill or whether a fill crosses a back-adjustment seam.

### 4.5 Joint ledger and weekly adapter

`research_utils.joint_trade_blocks` concatenates normalized events using deterministic ordering `(timestamp_utc when available else timestamp_naive, strategy_id, source_row_number)`. Cross-strategy timestamp ties are marked concurrent.

The calendar-week adapter groups trade exits by ISO Monday-start week while preserving empty weeks between the minimum and maximum exit date. It returns both per-strategy columns and a joint total. This is plumbing only: Phase 1 performs no portfolio ranking, dependence estimation, bootstrap, or qualification simulation.

### 4.6 Campaign runner and reports

`run_phase1.py` accepts `--source-dir`, `--output-dir`, and `--config`. It first verifies all fourteen files, then processes strategies independently so one blocked strategy does not erase the other reports. It writes local canonical event/trade ledgers atomically, hashes them, and writes aggregate JSON/Markdown deterministically.

Exit codes:

- `0`: run completed and all configured reports were written, even when reports contain expected reconciliation blockers;
- `2`: invocation or configuration error;
- `3`: source identity/schema failure prevented a complete seven-strategy run;
- `4`: output write failure.

Each strategy status is one of:

- `RECONCILED_EXPLORATORY`: structural/accounting tolerances pass and no strategy blocker remains;
- `BLOCKED_EXPLORATORY`: at least one structural, identity, timezone, cost, or venue blocker remains;
- `FAILED_INTAKE`: source identity/schema prevented normalization.

The campaign-wide status is the most severe constituent status. Unresolved continuous-contract rolls remain an explicit blocker dimension, and incomplete primary-source CME early-close coverage caps the holiday-short verdict at `NEEDS_CONTEXT`; neither prevents the remaining accounting report from being produced.

## 5. Frozen tolerances and ordering

- Source hashes, row counts, trade IDs, event labels, timestamp text, quantities, and pairing cardinality: exact.
- Currency fields and aggregates: `Decimal` quantized to `$0.01`; absolute tolerance `$0.01` only at source-vs-derived aggregate boundaries.
- Prices: retained at source precision; tick-grid remainder tolerance `1e-9` tick.
- Win/loss classification: net P&L compared to exact zero before display quantization.
- Timestamp order: parsed naive timestamp, then original one-based source row number. No entry/exit priority is introduced for equal timestamps.
- Joint ties: strategy ID, then source row number, while retaining `concurrent_timestamp=true`.
- Monthly groups: exit calendar month in the source timestamp domain until timezone is known.
- Weekly groups: ISO week beginning Monday in the same explicitly labeled timestamp domain; missing weeks appear with zero P&L and zero trades.

## 6. Failure and evidence policy

All issues use stable codes, severity (`INFO`, `WARNING`, `BLOCKER`, `FATAL`), strategy ID, source rows when applicable, and deterministic detail fields. Reports sort issues by severity, code, trade ID, and source row.

Expected source defects are data, not exceptions. Programming errors and invalid configuration fail loudly. The runner uses temporary sibling files plus atomic replacement so a failed run cannot leave a new file that looks complete.

No result may tune, delete, relabel, roll, or shift a source trade to improve reconciliation. Any later operator-supplied timezone or fee value changes the configuration fingerprint and generates a new report fingerprint.

## 7. Verification and acceptance

The implementation is accepted when:

1. Synthetic tests prove strict schema/hash behavior, Decimal parsing, duplicate/orphan handling, timezone/DST handling, stable ties, tick conversion, fee-table reconciliation, overlap/cap measurement, force-flat reporting, weekly zero-fill, and deterministic output.
2. `lab/discovery/cost_model.py` remains byte-unchanged, and the existing cost-model tests still pass.
3. Existing production firm-barrier tests for Tradeify trailing drawdown, intraday lows, lock behavior, consistency, and horizon-cap outcomes pass and are recorded in the verification evidence.
4. A local smoke run verifies all fourteen frozen hashes and produces seven reports plus joint-ledger hashes without committing source or row-level data.
5. The run reports the observed row/trade counts in configuration order: Aegis `244/122`, ORB-MNQ `1362/681`, DJ30-MYM locked-pyramid `406/203`, DJ30-MYM pyramid-down `406/203`, NAS100-MNQ locked lineage `756/378`, NAS100-MNQ native variant `368/184`, Vanguard-MGC `686/343`.
6. Aggregate net P&L reproduces to the cent: `$28,702.75`, `$47,533.16`, `$10,208.62`, `$31,770.36`, `$112,253.42`, `$170,250.58`, and `$20,388.04`, respectively.
7. The ORB-MNQ report contains exactly three Friday-to-Sunday holds as a sub-count; its total `FORCE_FLAT_VIOLATION` count is frozen from the daily-deadline audit.
8. Aegis reports the `$1.30` Pine setting versus `$3.10` export-implied fee as provenance warnings (`PINE_EXPORT_COMMISSION_MISMATCH` and `PINE_VENUE_COMMISSION_MISMATCH`) because the export-implied `$3.10` equals the venue fee. `EXPORT_VENUE_COMMISSION_MISMATCH` remains a blocker whenever export-implied and venue fees differ. MGC matches the primary-source `$1.06` per-side row. Both source streams remain unaltered.
9. Every strategy reports missing contract-month/roll provenance for its continuous `1!` export.
10. Committed artifacts contain no `C:\Users\...` source path and no raw row-level ledger.

## 8. Explicit exclusions

- No Phase 0 split, holdout, or pre-registration.
- No strategy selection, comparison, ranking, or parameter tuning.
- No portfolio-dependence conclusions or Monte Carlo qualification.
- No Pine modification, production strategy lock, allocation, lifecycle, rail, or deployment change.
- No silent correction of weekend dates, timestamps, instruments, fees, quantities, or trade structure.
