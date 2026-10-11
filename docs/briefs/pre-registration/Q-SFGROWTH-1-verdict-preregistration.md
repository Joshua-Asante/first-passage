# Q-SFGROWTH-1 — Verdict pre-registration

**Status:** FROZEN 2026-10-09 (operator: "freeze the plan"), before any export is read or any scorer exists. The freeze commit is recorded in the [parent brief §8](../Q-SFGROWTH-1-self-funded-growth-portfolio-selection.md#8--verdict-pre-registration). A verdict computed after any constant below moves is void; a changed constant is a new pre-registration. Corrections from the freeze review land before Phase 0 reads data, as a dated amendment and re-freeze (see §E). The original freeze text is immutable at `121e2acf`.

**Re-scoped 2026-10-11 (Q-SFCLEAR-1 FROZEN 2026-10-11):** under [ADR addendum 2026-10-11b](https://github.com/Joshua-Asante/first-passage/blob/d7ad4d8d672790dfbe647b22fd9d75a95576f109/docs/adr/2026-10-09-self-funded-tradovate-lane-reopen.md#addendum-2026-10-11b--tradeify-book-reused-on-the-personal-lane-supersedes-the-option-c-split) (PR #784) the personal lane's study is [Q-SFCLEAR-1](Q-SFCLEAR-1-verdict-preregistration.md), a single-tuple clearance of the Tradeify book at R1. See [section G](#g---re-scope-to-q-sfclear-1-2026-10-11). Nothing below runs.

**Lane-split HOLD (superseded by 2026-10-11b):** The operator ruling relayed as dated 2026-10-11 excludes legs 1–4 from the personal pool immediately. Section F8 controls pool reconciliation; the five-leg counts below are historical and cannot authorize exports or scoring.

**Amendment reader notice:** Section A below preserves the October 9 baseline wording. The approved native-guard interpretation in [F7](#f7---captured-native-guards-retained-operator-ruling-pending-re-freeze) supersedes its protection parenthetical on amended re-freeze; exports and scoring remain held.

## A — Pool

Legs with an accepted CME trade list, at their locked parameters, **normal mode** (no Tradeify protection; the only protection modeled is the 15% halt in §C):

| # | Leg | Instrument | Accepted size baseline `Q_i` |
|---|---|---|---|
| 1 | Aegis 6J | 6J (full size) | 8 contracts (`remc_series_builder.DEFAULT_QUANTITY_SPEC["aegis_6j"]["normal"]`) |
| 2 | Striker DJ30 MYM p250 | MYM | as exported |
| 3 | Vanguard Gold MGC v0.4 | MGC | as exported |
| 4 | ORB MNQ v7 reconstruction | MNQ | as exported |
| 5 | Striker NAS100 MNQ, DOW-excluded | MNQ | as exported — included by operator ruling 2026-10-09 ("include it"), scoped to this selection; the Tradeify withdrawal stands |

The pinned Tradeify exports are the reference for each leg's locked inputs, not scoring inputs: legs 1–4 in `lab/analysis/c1/four_firm_remc_2026-10/run_four_firm_remc.py` (normal-mode pins only), leg 5 at `strategies[3].export_sha256` in `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/phase1_config.json`. Leg 1 trades full-size 6J because no micro-yen edition has an accepted trade list; this is a pool limit, not a claim that Tradovate lists no micro yen.

## B — Grid, exports and K

- Each leg gets a multiplier `k_i ∈ {0, 1/8, 1/4, 1/2, 1, 2}`.
- **Size-specific exports, no linear rescaling.** For each leg and each non-zero `k` (k = 1 included), the leg's series comes from its own TradingView export of the locked Pine with every sizing input multiplied by `k` and all other inputs equal to the reference export's:
  - a **contract-count** input is set to `floor(k × its reference value)` (leg 1: `floor(k × 8)`);
  - an **account-size** input used only to compute position size (the Striker legs' static `accountSize` read by `calcSize`, [campaign §D15](../programs/2026-09-03-seven-strategy-select-campaign-state.md)) is set to `k × its reference value`, unrounded; the Pine rounds the resulting quantity itself;
  - the Properties-panel **initial capital** is set to `k × the reference export's initial capital`, so capital-anchored controls (the Striker day soft-stop) keep their locked ratio to position size.

  If a leg ends up with no trades at some `k`, it contributes none at that `k`. Each export's per-trade `Size (qty)` is used as exported. The `E_0` account exists only in the simulator (`E_0`, §C), not in TradingView. Reason: the Striker legs carry size- and capital-dependent state, so a rescaled list from another size can contain trades the smaller strategy would never take.
- Before any export is produced, Phase 0 reads each leg's Pine in the operator checkout (not quoted, not copied) and records in the manifest which inputs are contract-count, account-size and neither. That classification is reviewed before exports are made.
- Before any export is read for scoring, Phase 0 commits a manifest listing every (leg, k) export with its SHA-256, the inputs changed and their values. A missing or hash-mismatched export ⇒ VOID.
- **Excluded combinations:** legs 4 and 5 both non-zero (the rail flattens by account and instrument, so two MNQ legs cannot hold independent positions).
- **Margin exclusion:** a configuration is excluded if `Σ_i max_n_i × IM_i > E_0`, where `max_n_i` is the largest per-trade quantity in leg i's size-k export over the full calendar and `IM_i` is Tradovate's published initial margin per contract for that instrument in a dated snapshot recorded in the Phase-0 manifest. This assumes every leg's largest position is open at once, which is conservative.
- Multiplier vectors are not deduplicated: each is a distinct prospective sizing rule.
- **K = 2,375** = 6^5 − 1 vectors minus the 5,400 with legs 4 and 5 both non-zero, written to the `register_search` manifest before any Explore read. K does not depend on data; margin-excluded vectors count in K.

## C — Statistic

**Costs.** One all-in rate per side per instrument = commission (the account's Tradovate plan at Phase 0) + exchange + clearing + NFA, from a dated Tradovate rate snapshot recorded in the Phase-0 manifest before any export is read. Cost multiple `c ∈ {1, 1.5}` multiplies the whole all-in rate. A missing component ⇒ VOID.

**Series.** Per configuration and `c`, trades parsed by `remc_series_builder.parse_trade_list_csv` (session-contained, flat each session) and assigned to their session date:
- `d_t` = Σ gross P&L − c · cost_t, where cost_t = Σ sides × all-in rate
- `l_t` = 0 − Σ |adverse excursion| − c · cost_t (coincident-sum low, ≤ 0)
- `h_t` = Σ |favorable excursion| (coincident-sum high, ≥ 0, no cost deduction; overstating the peak is conservative). An export without a favorable-excursion column ⇒ VOID.

**Calendar and windows.** One calendar for every configuration: every Monday–Friday (no-trade days zero) from the latest first session date to the earliest last session date across the **k = 1 size-specific exports of all five legs** (a k = 1 export with no trades ⇒ VOID). With W its length, Explore = weekdays 1 … ⌊2W/3⌋, Confirm = weekdays ⌊2W/3⌋ + 1 … W. Trades outside the calendar are ignored.

**Paths.** For each seed `s ∈ {42, 123, 2026}` and each window of length `W_w` (VOID if `W_w < 20`):
- `rng = numpy.random.default_rng(s)` (PCG64)
- `starts = rng.integers(0, W_w − 20 + 1, size=(10_000, 13))` in one call; rows are paths 0 … 9,999 in order; non-circular blocks, starts may overlap
- path p's days = concatenate `range(starts[p, j], starts[p, j] + 20)` for j = 0 … 12, truncated to the first H = 252
- the same `starts` array serves every configuration and both cost multiples

**Per path, E_0 = P_0 = the planned starting capital (value private); for t = 1 … 252 (i = the path's t-th day):**
- intraday peak `P*_t = max(P_{t-1}, E_{t-1} + h_i)` (the high is assumed to come before the low, which is conservative)
- intraday trough `T_t = E_{t-1} + l_i`
- **hit** if `(P*_t − T_t) / P*_t ≥ 0.15`; the path stops with terminal equity `T_t`
- otherwise `E_t = E_{t-1} + d_i` and `P_t = max(P*_t, E_t)`
- terminal equity = `E_252` if never hit

**Clears** (per configuration, window, `c`): hits ≤ 100 of 10,000 on **every** seed.
**Growth** = `numpy.median` of the 30,000 pooled terminal equities (the average of the two middle values).
**Rank** (Explore, c = 1, non-excluded configurations only): among those that clear with growth > E_0, highest growth first; ties go to (i) fewer pooled hits, (ii) the smaller sum of per-trade quantities over Explore-window trades, (iii) the lexicographically smallest multiplier vector in §A leg order.

**Roll-seam limitation and sensitivity.** Every export is from a continuous `1!` chart. Trades are session-contained, so a back-adjustment seam cannot enter a trade's own P&L, but signals computed across sessions can still differ near a seam. Phase 0 records, per instrument and before any export is read, the session dates on which the continuous series changed contract. The sensitivity re-scores the top configuration on Confirm at c = 1 with every trade whose session date lies within 10 weekdays (either side, inclusive) of such a date removed.

### Worked example (synthetic, two days, one path)

Amounts in normalized units (E_0 = 100; not the account's capital). E_0 = P_0 = 100. Day 1: d = +2, l = −3, h = +4. Day 2: d = −14, l = −16, h = 0.

- Day 1: P*_1 = max(100, 100 + 4) = 104; T_1 = 97; drawdown 7 / 104 = 6.73% → no hit; E_1 = 102; P_1 = max(104, 102) = 104.
- Day 2: P*_2 = max(104, 102 + 0) = 104; T_2 = 102 − 16 = 86; drawdown 18 / 104 = 17.31% ≥ 15% → **hit**; terminal equity 86.

## D — Verdict table

Evaluate VOID first; the other rows apply only when no VOID condition holds.

| Verdict | Trigger | Disposition |
|---|---|---|
| VOID | an export is missing or mismatches its manifest hash; run K ≠ manifest K (2,375); the cost snapshot, margin snapshot or roll-date list is missing a component; an export lacks a favorable-excursion column or a k = 1 export has no trades; or a window is shorter than 20 weekdays | ITERATE (fix input, rerun unchanged) |
| RESOLVED | (1) ≥ 1 non-excluded configuration clears on Explore at c = 1 with growth > E_0; (2) the top-ranked one clears on Confirm at c = 1; (3) it clears on Confirm at c = 1.5; (4) its Confirm growth > E_0 at c = 1 and at c = 1.5; (5) it clears the roll-seam sensitivity | INTEGRATE |
| FALSIFIED | condition (1) fails | STOP |
| AMBIGUOUS-HOLD | (1) holds and any of (2)–(5) fails | ITERATE (operator; no second pick) |

Only the top-ranked Explore configuration is scored on Confirm.

## E — Amendment log

- **2026-10-09, Codex freeze review (PR #743, review on `d90eae8`), before any export was read or any scorer existed.** Changes from `121e2acf`:
  1. One calendar for all configurations, from the full five-leg pool; the builder's weekday calendar; the Explore/Confirm cut stated as a function of W.
  2. The 1.5× cost limb also requires Confirm growth > E_0, matching H-SFGROWTH-1.
  3. An intraday-high channel `h_t` feeds the running peak, so the statistic is genuinely intraday peak-to-trough; missing favorable-excursion data ⇒ VOID.
  4. Multiplier vectors are not deduplicated (final K in item 8); a final lexicographic tie-break makes the selected vector unique.
  5. The bootstrap is pinned: generator, start-index range, array shape and order, concatenation and truncation, window boundaries, and shared draws across configurations.
  6. Normal mode only; leg 1's baseline is the accepted 8 contracts; "no micro on Tradovate" removed (pool limit, not broker fact).
  7. Size-specific exports per (leg, k) replace linear rescaling (the Striker day soft-stop depends on size and capital); the quantity baseline is the export itself.
  8. Legs 4 and 5 may not both be non-zero (one MNQ position per account on the rail); K = 2,375, data-independent, so the K manifest no longer requires reading exports.
  9. Conservative initial-margin exclusion against `E_0` from a dated Tradovate snapshot.
  10. Cost = commission + exchange + clearing + NFA from a dated snapshot of the account's plan; 1.5× multiplies the whole rate.
  11. `numpy.median` fixed; VOID evaluated before every payoff row.
  12. Roll-seam limitation carried, with a frozen ±10-weekday sensitivity as RESOLVED condition (5).
- **2026-10-09, independent re-review on `fec6ad2` (PR #743), before any export was read or produced.** Change from `c208bde9`:
  13. The k-mapping now covers risk-sized legs: account-size inputs scale by `k` (unrounded), initial capital scales by `k` (replacing the fixed `E_0` of item 7, which would have tightened the Striker soft-stop many times over against unchanged positions), contract-count inputs stay `floor(k × reference)`; Phase 0 classifies every sizing input from the Pine before producing exports.
- **2026-10-09, public-exposure redaction (not an amendment; accepted by Joshua 2026-10-09, in chat to the merge agent).** The dollar value of the starting capital was replaced by the symbol `E_0` throughout, and the §C worked example was restated in normalized units (same arithmetic, same percentages). No constant changed: `E_0` keeps the value fixed at the freeze, which is held in the private archive (`first-passage-archive`, branch `archive/preserve-exposure-2026-10-09`, commit `950ee0f`).
- **2026-10-10, Phase-0 operator rulings approved; technical contract awaiting review and re-freeze.** Aegis cap interpretation, the five typed disabled-leg slots and the two-control Vanguard cosmetic exemption are recorded in section F. Approval reference: `Sentinel_7915fcd79e948191a0248d3bc3fe0b3d`. Amended re-freeze date: **NOT YET RECORDED**; its commit will be recorded in the parent brief §8.

- **2026-10-10, additional operator ruling:** preserve captured native guards; normal mode excludes external Tradeify protection. Section F7 owns the interpretation and acceptance requirements; independent review and amended re-freeze remain pending.

## F - Phase-0 amendment: approved scope, pending contract review and re-freeze

**Authority:** Joshua approved all three scoped rulings on 2026-10-10, approximately
20:20 UTC, message `Sentinel_7915fcd79e948191a0248d3bc3fe0b3d` ("approve all three").
The unchanged approval transcript is retained in the private local handoff.
**Effectivity:** the rulings are approved; this precise artifact/scorer contract
is prepared for the existing selection owner's review. It takes effect only after
that review and an explicitly recorded amended freeze. Until then Phase 0 remains
HOLD before exports, and scorer implementation awaits reconciled ownership and
the frozen amended contract. Approval is not a run, merge, capital or live GO.
On re-freeze, this section supersedes only the conflicting §A-§D requirements
identified below. The prior freeze remains retrievable at `ff9f6792`.

### F1 - Aegis cap interpretation

The existing §A baseline is the `max_contracts` cap used by §B, not a fixed quantity
on every entry. Actual quantities remain those produced by the pinned equity-risk
sizing; initial capital scales under §B. Keep the baseline, risk ratios, other
strategy settings and Pine/port bytes unchanged. Do not force a fixed count or
post-scale the exported trades. This is the approved semantic clarification.

### F2 - Typed disabled-leg artifacts

For exactly these positive-multiplier slots, replace §B's mandatory TradingView
export with a `ZERO_BY_INTEGER_SIZING` artifact:

| Leg | Multiplier strings | Input |
|---|---|---|
| 3 (Vanguard) | `1/8`, `1/4` | `maxContracts` |
| 4 (ORB) | `1/8`, `1/4`, `1/2` | `qty` |

These are disabled-leg cases chosen by the operator, not an assertion that the
unmodified Pine accepts the inadmissible input or produces an empty export.
Every other positive slot still requires its own TradingView export; `k = 0`
requires no artifact. The Phase-0 manifest must cover all 25 positive slots exactly
once: five structural-zero artifacts and twenty exports. Each entry records its
kind, slot and exact-file SHA-256. A missing, duplicated or incorrectly typed slot
is VOID. Empty/malformed files never stand in for structural-zero artifacts.

**Exact structural-zero schema (version 1):** one UTF-8 JSON object without a BOM;
all keys below are required, with no additional keys or duplicate keys. Hash the
exact file bytes, without normalizing them. Integers below exclude JSON booleans.

| Key | Required type and value |
|---|---|
| `schema_version` | Integer `1` |
| `artifact_type` | String `ZERO_BY_INTEGER_SIZING` |
| `leg` | Integer `3` or `4`, paired with the permitted multiplier/input above |
| `multiplier` | One exact reduced-fraction string from that leg's row above |
| `input_id` | That leg's input identifier above |
| `reason` | String `FLOORED_COUNT_BELOW_INPUT_MIN` |
| `pine_sha256` | 64 lowercase hexadecimal characters identifying that leg's pinned Pine |
| `reference_evidence_sha256` | 64 lowercase hexadecimal characters identifying the reviewed, exact effective-reference evidence used for that input |
| `classification_sha256` | 64 lowercase hexadecimal characters identifying the reviewed classification file frozen for this study |
| `preregistration_sha256` | 64 lowercase hexadecimal characters identifying the complete amended preregistration file at its recorded freeze |

The reference-evidence digest identifies the approved original, recapture or
admission-manifest bytes actually used. Record its provenance separately in the
private Phase-0 manifest; a recapture digest must not replace or claim equality to
an unrecovered historical snapshot pin. The manifest binds each zero slot to its
expected Pine/reference/classification/preregistration digests, independently of
the artifact's self-declarations, and records the frozen revision.

At Phase-0 admission, hash-check those sources and recompute the floor from the
reviewed effective reference and the exact rational multiplier; verify that it is
zero and below the pinned input's declared minimum. A mismatch is VOID, not an
invitation to extend the five-slot exception. Validate this before publishing the
data manifest. All later consumers recheck artifact bytes, schema, eligible slot
and agreement with those admitted manifest bindings before scoring. The artifact
contains no trade rows, dates, cash values, input values or configurable zero
outputs; its type fixes its contribution. Freeze the classification and complete
preregistration first, then generate artifacts, then hash them into the data
manifest; none of those documents contains its own hash or a future artifact hash.

### F3 - Scorer and verdict handling

A validated structural-zero artifact supplies zero daily gross P&L, costs,
favorable/adverse excursions, quantity, `d_t`, `l_t` and `h_t` on the existing
common calendar. Its `max_n_i` and margin contribution are zero. The same holds
at both cost multiples and under the roll-seam sensitivity. It bypasses the CSV
trade parser and does not consume randomness or determine calendar endpoints.

Only this validated artifact type is exempt from the TradingView-export and
favorable-excursion-column requirements. Real exports retain all existing checks,
including favorable-excursion coverage and nonempty `k = 1` exports for all five
legs. A valid non-baseline export with no trades retains §B's existing treatment.
Missing or hash-mismatched artifacts, invalid JSON/schema/bindings, or attempted
use outside the five slots are VOID, evaluated before any payoff verdict.
Cost/margin snapshots, roll dates and all other input requirements remain mandatory.

Preserve the complete nominal vector grid, K = 2,375, the all-zero-vector exclusion,
the exclusion of vectors with both MNQ multipliers nonzero, margin exclusion,
non-deduplication and the existing ranking/tie-break rules. Exclusions use nominal
multipliers even when a slot is structurally zero; never rewrite a vector to `k=0`.
Calendar, windows, seeds/draws, median-growth objective, clearance standard,
Confirm-only-top-selection and all other statistic/verdict rules are unchanged.

### F4 - Vanguard cosmetic provenance exemption

For leg 3 only, record `showEmas` and `showDashboard` historical values as JSON
`null`, with status `UNKNOWN_COSMETIC_EXEMPT` in the private reference record.
Exempt only those two controls from exact historical reference reproduction and
capture-completeness requirements. Source inspection at the pinned book hash
shows plot/dashboard use only. Do not infer or relabel their historical values
from source defaults. Record the display settings actually used for any future
export separately from historical values. Preserve every trading-setting,
Properties, source-identity, original-pin and provenance requirement. All other
unknown required reference values remain blockers. This waives cosmetic equality,
not hash verification or the distinction between attestation and reproduction.

### F5 - Validation design and integration gate

Before re-freeze, the existing owner reconciles this amendment and classification
with the current author branch, reviews the contract, and records the re-freeze
date in §E. Record the commit containing that frozen preregistration in the parent
brief §8 in a subsequent metadata change; do not embed the preregistration commit's
own SHA in its bytes. The date and approval message above
do not themselves identify an amended freeze. Implementation must then demonstrate
these synthetic cases before any real scoring:

| Case | Required outcome |
|---|---|
| Each of the five admitted slots, correctly bound | Accepted as a typed disabled leg; all contributions zero at both costs and through sensitivity; calendar/draws unchanged |
| Every other positive slot, `k=0`, wrong leg/input/fraction spelling or added slot | Structural-zero artifact rejected as VOID; no clamping, grid change or fallback |
| Missing/duplicate slot; byte-hash mismatch; wrong source/freeze binding; nonzero floor or admitted bound inconsistency | VOID before scoring |
| Missing/extra/duplicate JSON key; wrong version/type/reason; non-object/BOM/invalid JSON; extra trade/date/value fields | VOID before scoring |
| Empty or malformed CSV pretending to be a zero; missing favorable column in a real export; empty baseline export | VOID under the applicable real-export rule; no promotion to structural zero |
| Full manifest and nominal-grid enumeration | Exactly 25 positive slots and unchanged K/exclusions; no deduplication or conversion of nominal positive multipliers to zero |
| Zero-slot quantity/margin tie-break contribution | Zero contribution, with nominal vector retained for the existing final tie-break |
| Only the two exempt historical display values unknown | Provenance completeness accepted with explicit unknown status; any additional required unknown or unauthorized trading-setting change rejected |

These are implementation acceptance cases, not tests already run. Contract review
and re-freeze precede exports; ownership reconciliation and the amended freeze
precede scorer implementation; synthetic verification/review and the complete
Phase-0 manifest precede real scoring. The portfolio remains unselected.

### F6 - Committed private manifest identity

The values-bearing Phase-0 manifest stays private. Its durable destination is
`Joshua-Asante/first-passage-archive`, the repository's designated private evidence
store ([archive protocol](../../../scripts/README.md#private-evidence-archive)).
Use its content-addressed path `evidence/sha256/<first-two-hex>/<sha256>`;
`private/` in this study is only a local working copy, not the committed identity.

Before scoring, commit a public `PHASE0_MANIFEST_REF.json` in this study directory
(`lab/analysis/c1/sfgrowth_2026-10/`). It contains only `schema_version` (integer 1),
`archive_repository` (exactly `Joshua-Asante/first-passage-archive`),
`archive_commit` (full 40-character lowercase hexadecimal Git commit),
`archive_path` (the content-addressed path above), and `manifest_sha256`
(64 lowercase hexadecimal characters). Require exactly these keys, no duplicates
or extras; JSON booleans are not integers. Register the manifest digest and its
local private path in `docs/evidence/PRIVATE_EVIDENCE.sha256` in the same public
commit. No private values, credentials or evidence bodies enter either public file.

Sequence: review/re-freeze classification and preregistration; produce/admit the
authorized artifacts; finalize the private manifest with all 25 slots, exact-byte
artifact hashes, changed input values, effective reference/provenance identities,
cost/margin snapshots, roll dates and frozen source bindings; preserve its exact
bytes in the private archive and commit/push them; verify retrieval of that blob
at the recorded commit; then commit the public reference before any scoring read.
The private manifest must not contain its own digest, archive commit, or the
public reference's commit. Preserve archived bytes without newline conversion.

Admission and every scoring consumer resolve the committed public reference,
retrieve the blob from the named repository at that immutable commit/path, and
verify its SHA-256 against both the path and `manifest_sha256`. Verify the frozen
source bindings and every required artifact/evidence hash in the private manifest.
A local working copy is usable only when byte-identical to that committed blob;
branch tips, local paths alone and self-declared artifact hashes are insufficient.
Record the public reference commit and private tuple in the run's input identity.
Missing/unavailable reference, commit, blob or required evidence; malformed
reference; hash mismatch; source/freeze mismatch; or incomplete/duplicate slot
coverage is VOID before scoring, without a fallback to uncommitted local bytes.

The destination above does not itself authorize an upload of new private evidence.
This amendment uploads nothing. Before private publication, the executor must
establish scoped operator authorization for the exact files and verify the remote
is this repository and remains private. If that authorization is absent, stop that
step and request: "Approve committing and pushing the reviewed Q-SFGROWTH-1
values-bearing Phase-0 manifest and its specifically inventoried supporting
private evidence to Joshua-Asante/first-passage-archive, under evidence/sha256/;
publish only repository/commit/path/digest bindings in first-passage."
Inventory paths and digests locally for that approval; do not upload to obtain it.

Add synthetic acceptance cases to F5: valid committed-reference retrieval passes;
wrong repository/commit/path/digest, mutable-ref substitution, malformed reference,
missing archive evidence, local-only or altered manifest, and changed source/freeze
bindings all produce VOID before scoring. Test exact-byte preservation (including
line endings), complete 20-export/five-zero coverage, and the absence of private
values from the public reference. These remain future scorer requirements.

New reference-evidence pins are subject to the same preservation prerequisite:
until scoped authorization and verified private-archive publication exist, retain
their exact inventory locally and defer both public digest citations and registry
rows. Provisional local references cannot satisfy Phase-0 admission. When published,
each registry name must be the actual repo-relative file path without annotations;
stage external captures in an ignored primary-checkout evidence directory first.

### F7 - Captured native guards retained: operator ruling, pending re-freeze

**Operator ruling, 2026-10-10:** "Preserve captured native guards; clarify that
normal mode excludes external Tradeify protection (recommended to preserve
locked trading settings)." This separately resolves the native-guard choice;
the three earlier approvals remain unchanged. Review and amended freeze are owed.

The hash-verified Striker MYM reference activates the pinned Pine's native daily/
total drawdown guard. Source reads on October 10 confirm `ddHit` (line 205) feeds
entry eligibility (241) and position closure (368); `backtestMode` gates it.
This agrees with the [prior source read](../../notes/2026-09-12-track-b-scaling-faithfulness-read.md#1--classification-per-leg-pine-line-refs-are-to-the-pinned-body).

On amended re-freeze, this ruling supersedes section A's parenthetical claim that
only the simulator's 15% halt is modeled: **normal mode excludes external Tradeify
portfolio/venue protection overlays; captured strategy-native guards and soft-stops
remain part of each pinned strategy's behavior.** The simulator additionally applies
the unchanged portfolio-level 15% intraday peak-to-trough halt. A native guard may
alter the genuine size-specific export's entry/exit sample before simulation;
that sample must not be described as free of strategy-native protection.

Section B continues to preserve all non-sizing trading settings at their verified
reference values, including `backtestMode`. Do not toggle a native guard, force an
inactive guard on, remove a leg, post-rescale trades, or add a Tradeify overlay.
Section B's existing capital/account-size/cap scaling remains unchanged. This
interpretation applies across the pool, including the native Striker soft-stop;
it does not assume every leg has the same guard or that every guard is active.

Before admission, the reviewed private reference record identifies each leg's
native guard/soft-stop state and its source/reference provenance. Scorer/input
acceptance must reject unauthorized non-sizing setting changes, retain native
entry/exit effects in genuine exports, and still enforce the separate simulator
15% halt. Check both active and inactive native-guard reference cases and the
size-dependent Striker soft-stop; do not manufacture missing trades to undo them.
K=2,375, nominal vectors, exclusions, tie-breaks, maximum-growth ranking and the
99-in-100 clearance standard are unchanged. Exports and scoring remain HOLD
pending independent review and explicitly recorded amended freeze; this ruling
does not itself record that freeze.


### F8 - Lane split: excluded legs and pool reconciliation HOLD

**Authority:** Joshua's option (c), relayed by the Deployment Coordinator as dated
2026-10-11: the four Tradeify-book strategies stay Tradeify-only. The personal
Tradovate pool excludes Aegis 6J (original leg 1), Striker DJ30 MYM (2), Vanguard
MGC (3) and ORB MNQ v7 (4). These exclusions apply now, before any amended freeze.
The [exclusive-use record](../../notes/2026-10-10-tradeify-exclusive-use-replies.md)
records the venue reply; the coordinator owns the dated addendum to the
[self-funded ADR](../../adr/2026-10-09-self-funded-tradovate-lane-reopen.md).
The [dated addendum](https://github.com/Joshua-Asante/first-passage/blob/d92920946bb7766876ce226a4cea0f67565a2e5f/docs/adr/2026-10-09-self-funded-tradovate-lane-reopen.md#addendum-2026-10-11--strategy-split-between-lanes-option-c) was merged with coordinator PR #778 (`ba000b2`).

The only remaining member of the already admitted section-A pool is Striker
NAS100 MNQ, DOW-excluded (original leg 5). No replacement is admitted by this
amendment. Other locked strategies require explicit eligibility, source/reference
and pool review before inclusion; rejected/withdrawn editions do not gain admission.
Original leg identifiers remain provenance identifiers, not available dimensions.

**Recomputed consequences, conditional on retaining only original leg 5:**

- The existing six multipliers give 6 - 1 = **5 nominal configurations** after
  excluding all-zero. Equivalently, historical vectors are (0,0,0,0,k5), k5 > 0.
  The original both-MNQ exclusion is vacuous; margin-excluded vectors still count
  in K, and nominal vectors are never deduplicated.
- Five positive slots require **5 genuine size-specific exports; 0 structural-zero
  artifacts**. The five F2 exception slots belong entirely to excluded legs.
  A structural-zero artifact cannot substitute for any retained leg-5 export.
- The shared weekday calendar would use the retained leg's genuine nonempty k=1
  export. Missing favorable excursions or an empty baseline still yield VOID.
- K=2,375 and the 20-export/five-zero coverage in A–F7 describe the prior pool,
  not the lane-split pool. They must not be registered or consumed for a new run.

**Operator ruling, 2026-10-10 (America/New_York):** "Hold while additional
locked candidates are admitted." The study remains HOLD for additional eligible
locked candidates; the one-leg alternative is not adopted. The five-configuration
arithmetic above is a counterfactual, not an executable grid. No replacement is
admitted by this ruling. Complete each candidate's eligibility and source/reference
review, record the resulting pool, and recompute its data-independent K and artifact
coverage before re-freeze. Reconcile A/B/C/D, F2/F3/F5/F6 coverage, classification
and brief with that pool without reading outcomes. There is no final amended K yet.

**Disposition of prior rulings:** F1 (Aegis cap), F2/F3's five exceptional slots
and F4 (Vanguard cosmetics) remain historical approvals but are inapplicable to
the personal pool after the exclusions. They grant no exception for a replacement.
F7 remains binding for admitted legs: preserve captured native guards and soft-stops,
exclude external Tradeify overlays, and apply the additional simulator 15% halt.
Its MYM example remains evidence of the prior clarification, not pool admission.
The F7 prohibition on removing a leg was scoped to that guard ruling; this later
lane-split ruling expressly requires removing legs 1–4. Corrected NAS weekday
lineage and original-versus-recaptured evidence distinctions remain required.

The maximum-growth objective, 15% intraday peak-to-trough halt, 99-in-100 clearance,
bootstrap, cost stress, margin rule, ranking/tie-break framework and Confirm-only-top
selection remain unchanged. F6 private committed identity and VOID-on-missing-or-
mismatched evidence remain mandatory; re-inventory only the selected pool's evidence
before requesting scoped upload authorization. The earlier five-file packet is not
an upload authorization or a final pool-specific inventory.

Before scoring, synthetic checks must reject excluded-leg artifacts/vectors and
unadmitted replacements; enumerate the final nominal grid and exact slot coverage;
verify genuine-baseline calendar construction; reject zero artifacts outside any
explicitly frozen eligible slots; and enforce F6 bindings plus retained native
settings. These are acceptance requirements, not an implemented or tested scorer.
Exports/scoring remain HOLD pending additional eligible candidate admission, consistent
contract, exact-head independent review and explicitly recorded amended freeze.
Merge remains with the Claude sequencer after Codex is clean and Joshua gives his word.


### F9 - Exact-head review findings: exposure, Properties and friction

Codex review of `5134cee0578cdc8aad30f770d97fdf7ba58731a3` identified these
additional admission defects. They remain relevant after removing legs 1–4.
The parser source (`lab/discovery/remc_series_builder.py`, inspected at that head)
provides paired `entry_ny`, `exit_ny`, `qty`; `Trade.gross_usd` adds commission to
net P&L but does not remove embedded slippage. No export was read for this review.

**Margin correction, proposed for review/re-freeze:** replace section B's largest
individual trade quantity with each leg/size's maximum concurrent open quantity
over the full calendar. Sum absolute open contracts across overlapping base/add
tranches; partial exits reduce only their matched quantity, without double-counting
paired entry/exit rows. At equal timestamps without a verified finer event ordering,
process all entries before exits to conservatively bound peak exposure (including
zero-duration trades). Reject missing/invalid timestamps, nonpositive/noninteger
quantity, exit-before-entry, inconsistent pairing or unresolvable tranche accounting
as VOID; do not fall back to largest trade size. Margin exclusion remains the sum
of each leg's peak exposure times its dated per-contract initial margin versus E_0.
This correction does not change K, rank tie-break quantity or the clearance standard.
Synthetic acceptance: overlapping base/add exceeds the larger tranche; separated
trades do not sum; tied events use the conservative ordering; partial exits and
multiple closed tranches reconstruct without double counting; malformed exposure
is VOID; a vector exceeding E_0 is excluded and still counted in nominal K.

**Properties provenance correction:** before any export, bind the captured TradingView
Properties `Pyramiding` value for every admitted leg in its reviewed private reference
record and future size-specific artifact manifest. Preserve it as a non-sizing
setting, distinct from the Pine add-size percentage. Source defaults or a saved chart
cannot substitute for captured reference evidence. A missing/unknown value or an
unauthorized difference blocks exports and produces VOID at admission. Test a
matching capture, missing capture, changed value and percentage/value confusion.

**Operator friction ruling, 2026-10-10 (America/New_York):** "Preserve reference
friction; explicitly use fee-only stress." Captured TradingView commission and
slippage remain unchanged for strategy behavior, including native equity/guard
and soft-stop effects. Commission add-back changes the accounting, not that sample.
The technical interpretation below is approved in scope, pending exact-head review
and amended freeze; it does not lift the F8 candidate-admission HOLD.

On amended freeze, interpret section C's "gross P&L" as **P&L before the separately
deducted Tradovate fees, net of retained reference slippage**. Per trade, use
`g = Net PnL USD + Commission USD` exactly once, matching `Trade.gross_usd`.
Do not add back estimated slippage or call g friction-free. With
`fees_t = sum(sides * dated Tradovate all-in per-side fee)`, the day law remains
`d_t = sum(g) - c * fees_t`, `l_t = -sum(abs(adverse excursion)) - c * fees_t`,
and `h_t = sum(abs(favorable excursion))`. Retain the genuine export's excursions;
do not regenerate entries, exits or excursions to undo captured friction effects.
The Tradovate fee contains commission, exchange, clearing and NFA components.
`c in {1, 1.5}` stresses **only those separately deducted fees**. Reference slippage
and the reference-friction-dependent trade sample remain identical in both limbs.
This is a fee-only sensitivity, not slippage stress or a strategy rerun at the
target account's fee schedule. Any reference-versus-target fee difference is
reconciled in cash accounting only; its effects on strategy behavior are not replayed.

The reviewed private manifest records captured commission/slippage Properties and
source/effective-reference evidence, separately from target dated Tradovate fees;
retain the original/recapture distinction. Missing required reference-friction or
fee evidence, unauthorized Properties changes, repeated commission add-back, or
slippage removal are VOID. F6's private publication authorization remains separate.

Synthetic scorer acceptance, before real scoring: commission is added back once;
reference slippage is left embedded; changing c affects d and l by exactly
`-0.5 * fees_t` between the two limbs, with h and the trade sample unchanged;
no reference commission is deducted a second time; missing fee components or
reference bindings yield VOID. Normalized example: exported net=96, commission=4,
target fees=6 gives g=100, d(1)=94 and d(1.5)=91, regardless of any separately
estimated slippage amount. These are required tests, not a scorer implementation.
The maximum-growth, 15% halt, 99-in-100 and ranking rules remain unchanged.

## G - Re-scope to Q-SFCLEAR-1 (2026-10-11)

**Authority:** [ADR addendum 2026-10-11b](https://github.com/Joshua-Asante/first-passage/blob/d7ad4d8d672790dfbe647b22fd9d75a95576f109/docs/adr/2026-10-09-self-funded-tradovate-lane-reopen.md#addendum-2026-10-11b--tradeify-book-reused-on-the-personal-lane-supersedes-the-option-c-split) (PR #784) and Joshua's 2026-10-11 rulings recorded in [Q-SFCLEAR-1 §1](Q-SFCLEAR-1-verdict-preregistration.md#1--context-and-operator-rulings). F8's exclusions are superseded: the pool is the four Tradeify-book legs. F8's HOLD lifted when Joshua ratified Q-SFCLEAR-1 on 2026-10-11.

Nothing ran under this pre-registration; no data or K was consumed. Q-SFCLEAR-1 carries forward §C (statistic mechanics), F6 (private identity), F7 (native guards) and F9 (reference friction, fee-only stress, concurrent-exposure margin). Dropped: the five-leg grid and K = 2,375, NAS leg 5, F1-F4 structural-zero and Aegis-cap rules, Explore/Confirm, F8. Sections A-F stay as history.
