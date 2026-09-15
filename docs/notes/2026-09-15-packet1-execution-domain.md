# Packet 1 execution and evidence domain

Status: implementation scope for independent review; no admitted bundles or live
qualification. Base: `821ee9044712a766f03cb798fed32f29153d064c`.

Joshua authorized completing Packet 1 after merging #392. He delegated the forward
calendar end date to the coordinator; the initial bound is **2026-09-30**, starting
2026-09-03. Missing or expired accepted rows refuse risk. This choice does not
authorize a weekday fallback, extend D19 or imply deployment by that date.

## Source binding

Joshua has attested that the pinned Striker and ORB bodies ran unchanged between
the seven-export collection and corrected O-N export. The separate private
attestation binds both preserved manifests and both registry Pine digests. Its
scope is source history, not effective settings, cashflow reconciliation or parity.
Both current chart timezones were visibly checked as New York and captured privately.
The private source-history attestation SHA-256 is
`7c58510aeb8fe924798e54c464f9daea92b042ea6f65508af092252a6d0a568f`.

## Shared sizing comparison domain

The seven cases remain the five collected Striker mode/lifecycle combinations and
ORB normal/adds-off. Preserve the original collected cap and Account Size overrides
as source evidence. The shared sizing path consumes the original unscaled account
risk, actual intent stop distance and point value, explicit mode and lifecycle,
and the independently specified comparison allocation. Do not recover risk by
dividing a rounded source quantity. Call production `entry_quantities` and
`add_quantity`; do not supply a quantity-only callback to the private port.

The comparison allocation matches the approved chart cap for these evidence cases.
This is a bounded chart-evidence domain, not production allocation acceptance.
The account capacity remains 80; actual production allocations remain under TB-V1.
The full allocation domain retains the production-law boundary tests and later
combined replay requirements. A seven-case PASS cannot waive those gates.

Actual emulator fills, terminal cancellations, rejections and commissions pass
unchanged to the private adapter. Adds derive from cumulative confirmed base fills
for the current position, never the source's intended base. Partial closes retain
remaining fills; an empty position resets its base identity. No live sender is
introduced by this offline comparison path.

## Finite-margin acceptance criterion (before execution)

Preserve the captured ORB finite-margin affordability check. For the fixed complete
historical MNQ panel, captured initial cash/costs, one-contract base and no more
than two same-sized adds, verify a conservative margin bound at every processed
bar execution phase (`process_bar`, then `submit`). Long-only scope is explicit.
Before each phase, pessimistically value every existing lot at low minus exit
slippage, charging its unpaid entry and possible exit commission. Separately
allow up to three NEW contracts in that phase, each bought at high plus entry
slippage, sold at low minus exit slippage, and charged both commissions. This
allows old lots to close and replacements to enter; the new-contract bound is
not reduced by existing exposure. Verify the actual phase's queued/new entry
quantities do not exceed that bound. Require the equity lower bound to exceed
margin at high plus slippage for existing PLUS all possible new contracts. Check
the post-close state as well. The bound deliberately permits more simultaneous
exposure than the chart ceiling so replacement turnover cannot escape it.

There are no intrabar strategy recalculations in this domain. Each phase executes
only its already enumerated finite action set; future stops remain for the next
phase/bar check. Enforce long-side, quantity and supported-order assumptions at
the actual execution boundary. These inequalities then dominate all prices along
the emulator's piecewise path, gaps and slipped fills, rather than sampling only
closing equity. Independent review must accept the implementation and assumptions.

Any short exposure, excess quantity, nonfinite/invalid price, failed bound or
unsupported event refuses the proof. Report the tested domain and code/input
digests; never use absence of a margin-call CSV row as proof. A PASS applies only
to these exact initial states, settings and complete panels. It does not cover
new prices, production balances, altered allocations or the later combined book.

## Remaining producer boundaries

The TB-T1 tool implements the existing offline snapshot contract using the real
kernel and tier geometry. It records an evidence attestation, not broker API
verification or an authenticated daily-close producer. Live producer selection,
session identity and freshness consumption still require their own acceptance.
Calendar provenance and the immutable D19/closure-overlay separation remain owed.

## Implemented and verified continuation

These changes are offline components. The source-admission code requires an
independently reviewed contract digest and exact evidence artifacts. Execution
requires that trusted digest again, verifies the configured port path, and
compiles the verified port byte snapshot. Panel and export snapshots cannot fall
back to historical filename lookup or environment-selected replacement files.
Complete export pairs, integer quantities, explicit panel endpoints, ordering,
finite prices, zero excluded trades and resolved final state are required.
Comparison uses quantity scale 1 and the established price/PnL tolerances.

No real admission contract has been issued. A semantic `PASS` field is a reviewed
fact whose bytes are bound by the loader, not a fact discovered by the loader.
Any decision-bearing execution must bind the runtime revision/component digests
as well as the returned admission and evidence identities.

Private results retained under the existing `op1/2026-09-14-seven` evidence root:

| Artifact | Result | SHA-256 |
|---|---|---|
| `packet1-shared-law-margin.json` | Seven shared-law comparisons MATCH, zero excluded; both finite-margin ORB phase envelopes pass | `aabac77cd874e1ca2cddac0599394d55b15583346ef5112b885044ee68b53674` |
| `packet1-normalization-diagnostic.json` | Seven normalization/reconstruction diagnostics PASS, no issues | `10680786b54622106956354b9f3e03020b7c18f7b1cfe9c1773f5f908e7c2246` |

The margin diagnostic records tool/components, exports and ports; it does not
contain the panel-byte identity required for formal admission. Preserve that
diagnostic and produce fully bound evidence through the reviewed runner once
coverage and admission facts are available. Do not retrofit an unrecorded input
identity onto the older result.

Independent review of the five new Striker summary captures accepted scalar
cashflow/count/win-rate/PF reconciliation and independent exit-month reconstruction.
All five have closed-interval overlaps or ties: under D32 the panel drawdown is
`RECORDED`, not equated to the reconstructed walk. Monthly totals are
`RECONSTRUCTED`; independent commissions are `AMENDED_OUT` under D17. These are
bounded reconciliation verdicts, not synchronized account-drawdown evidence.

Reviewed text capture identities:

| Case | SHA-256 |
|---|---|
| S-P | `07928c14fa31a81a9c8590abf02a243a91aa47d4d00c1920d4eeda9e8e5bc023` |
| S-W1 | `e2db7768886b385622df266fd7b630cd92acb0e9a735a2e66bfab11654e77118` |
| S-W1P | `c1bb72ef706c17ca695f8bb7c19fe17d8f66c48596a6f2c8afbeca76d0c14204` |
| S-W2 | `6501756f05227f86c1682169e2c693f1699285259336e4409a120ea5b576ac4a` |
| S-W2P | `c65f8926ec137af751d44a1ca2fbff432b63508bbcf82ee72f8622d41036f2b4` |

Validation on Python 3.11.9:

- `tests/ops` plus the offline sealer suite: **1696 passed, 12 skipped**; two
  existing dependency deprecation warnings. No credit for missing private inputs.
- Explicit historical private adapter suite, with the original config, Downloads
  exports and primary panel/port roots: **13 passed, no skips**. Original export
  hashes remain enforced. The initial default-path attempts skipped the export
  cases; this explicit run replaces those attempts as regression evidence.
- Independent integration reviewer ran the admission/execution suites:
  **31 passed**, no blocking findings. Sealer and finite-margin corrections were
  independently reviewed before integration.
- `scripts/gate_manifest.py --tier check`: **PASS, exit 0**. Existing private-tree
  absence and catalog/session advisories remain disclosed.

## Exact remaining acceptance work

1. **Completed:** retain and reconcile O-N/O-P summary panels, including the
   inactive-input equivalence evidence below. Earlier trade-list captures remain
   preserved; fresh summary captures supply the independent scalar anchors.
2. Bind the seven settings/source/summary artifacts and establish exact deep-start
   semantics and full panel coverage. The panel starts at 2022-09-01 00:00 UTC;
   displaying a September 1 date range in New York does not alone prove that origin.
   Then issue independently reviewed admission manifests and run exact-byte parity
   with complete panel/runtime identities.
3. Implement and qualify the shared calendar using immutable D19 solely for its
   accepted historical date membership, separately typed book no-trade overlays,
   and official forward product schedules through September 30. The earlier
   universal primary historical-archive prerequisite is corrected by the
   [Step 1 closure](2026-09-15-calendar-account-contract-resolution.md#step-1-closure--approved-design-and-bounded-calendar-route).
   Historical matching-hour or missing-bar claims still need supporting evidence;
   D19 cannot prove those facts. Actual CME product lookups demonstrate forward
   source access, not complete executable calendar qualification. Keep account
   session IDs, CME business dates, matching pauses and final closes distinct.
4. Complete the named authenticated daily-settlement producer and consumer boundary,
   including prior-session identity, duplicate/out-of-order delivery and stale-seal
   rejection. The implemented C1–C10 offline snapshot seal is an evidence attestation,
   not this producer. Existing later-session activation and E1–E3 gates remain intact.

**Packet 1 remains open; seven bundles remain formally unadmitted.** No live sender,
calendar fallback, policy admission, n3 run, deployment or arming occurred.

## Packet 1 Step 2 — ORB summary reconciliation

2026-09-15 UTC, base/head `821ee9044712a766f03cb798fed32f29153d064c` plus existing
Packet 1 working changes. Fresh fixed-window TradingView summaries were captured
for corrected O-N and original O-P on the existing saved ORB chart. A temporary
desktop viewport exposed report controls missing in the narrow layout; it was
reset after collection. No source body or original export was edited.

Both captures explicitly show September 1, 2022–September 2, 2026, DEEP. Fresh
Inputs match their retained original case controls; Properties retain the captured
capital, quantity, commission, slippage, leverage and execution settings. O-P's
report was explicitly regenerated after each settings change; stale reports were
not used. The pinned normal-mode settings and refreshed report were restored.

### Inactive O-P inputs

The original O-P export retains adds disabled with spacing 0.25 and size 80%.
The pinned source defaults are 0.08 and 100%. These are inert when adds are off:
the verified Pine body computes `scaleInQty` at line 179, but its only order uses
are lines 266/269 inside `if useScaleIn` at line 264. All uses of the spacing
parameter are in that same guarded block. The stall-close condition at line 291
also requires `useScaleIn`; neither parameter leaks into a different exit path.
The Pine digest remains
`176c4f70c67d58053c4d3b8170d0a9be3733bc6b76b1e2f928bd7a877be052a3`.

A second fixed O-P report with only those two inactive inputs changed to the
pinned defaults reproduced all five summary anchors exactly. This corroborates
the source-control-flow proof; aggregate equality alone is not a trade-path proof.
The original export is retained and bound, with this explicit inactive deviation.
No parameter search, book amendment or replacement export was needed.

### Reconciliation evidence

The private `step2-orb/reconcile.py` uses the existing canonical normalization,
trade reconstruction, accounting, D17 monthly and D32 summary routines. It binds
the original export digests and Pine bodies, compares captured input controls,
and reads anchors from independent summary text, never from calculated cashflows.
It also consolidates the five previously reviewed Striker captures into seven
case records. Output values and screenshots remain under the ignored evidence root.

| Case | Count/net/win-rate/profit-factor | D32 panel drawdown | D17 monthly |
|---|---|---|---|
| O-N | MATCH | RECORDED: overlap/ties present | RECONSTRUCTED |
| O-P | MATCH | COINCIDENT: no overlap/ties | RECONSTRUCTED |
| Five Striker cases | MATCH | RECORDED: overlap/ties present | RECONSTRUCTED |

Independent commissions remain `AMENDED_OUT` under D17. D32 informational findings
are retained in the report; a recorded panel value is not synchronized account
drawdown evidence. O-P coincidence does not establish the complete equity path.

Private artifact identities (relative to `op1/2026-09-14-seven/step2-orb`):

| Artifact | SHA-256 |
|---|---|
| `O-N-summary.txt` | `400ec898639b5d89151cd77b75256e3109d9cbada3120af6f68128d706546c81` |
| `O-P-original-summary.txt` | `409de79c274125e8b9dac5e8b9d98ed60cd15e9a7955eb2b3bd99ce7f81b4472` |
| `O-P-pinned-summary.txt` | `74e90696113d56be7926ed4cd78681417bda585d6cf30d01aed823add79d8211` |
| `seven-summary-anchors.json` | `88f48d32f242cc2396c973aead836f1f701b7be998cd341f4e36e954ab33ca4d` |
| `seven-summary-reconciliation.json` | `e3883d1fcf57a442da748f4ba5da569d644699d82e8b1b1b4fd7568b1ff2cff9` |
| `reconcile.py` | `117f22b2bf15e32b8b7f88052cfa38ba58520cc497b22e235cf656a062d53efd` |

The report pins calculation components, capture PNG/text and export identities.
Bundled Python 3.12.14 executed the private runner: seven PASS, exit 0. The first
attempts exposed a missing import path, duplicated accessibility focus text in
the control comparison, and D32 INFO records being treated as errors; those
runner defects were corrected without changing anchors, accounting or tolerances.
No runtime code changed in Step 2. Startup/panel coverage, calendar implementation,
settlement qualification and formal admission remain open. No bundle is admitted
by this bounded reconciliation.

Verification: `tests/test_tv_summary_reconciliation.py` on the repository Python
environment: **68 passed**. The bundled analysis runtime lacks pytest, so its
unsuccessful test invocation supplies no test credit. The seven-case analysis
itself ran on the bundled runtime as recorded above. Rechecked every pinned
capture, calculation component and anchor hash; confirmed the private result is
gitignored; `git diff --check` passed.

Independent reviewer `packet0_review` accepted bounded Step 2 closure with no
material findings. A read-only rerun reproduced all seven reconciliation records;
the reviewer verified original/fresh controls and properties, artifact identities,
O-P's pinned-source inertness proof and unchanged D17/D32/downstream gates.
**Step 2 is complete; Step 3 startup and panel coverage is next.**

## Step 3 — initial panel and startup audit (2026-09-15)

Status: **IN PROGRESS; inventory only, no coverage PASS or admission.** Work
starts from merged PR #393 (`757deb1`) on
`codex/tradeify-packet1-startup-coverage`.

### Exact retained panel boundaries

Read every row of the four retained panels and verified each complete file against
`core/data/bar_data/SHA256SUMS`. Times below are UTC bar-open timestamps; the final
bar-open is not automatically the approved comparison cutoff.

| Panel | Rows | First bar | Last bar | Adjacent intervals longer than 15 minutes |
|---|---:|---|---|---:|
| 6J | 94,805 | 2022-09-01 23:00 | 2026-09-03 00:00 | 1,035 |
| MGC | 94,617 | 2022-09-01 00:00 | 2026-09-03 00:00 | 1,035 |
| MYM | 94,499 | 2022-09-01 00:00 | 2026-09-03 00:00 | 1,036 |
| MNQ | 94,503 | 2022-09-01 00:00 | 2026-09-03 00:00 | 1,036 |

All timestamps are strictly increasing and on the 15-minute grid. OHLCV values
are finite, volumes nonnegative, and opens/closes within the high/low range.
No zero-volume rows occurred. These are structural checks, not independent price
verification. Every longer interval is retained with both endpoints, duration and
absent grid-slot count, classified `UNCLASSIFIED`. A grid slot is not an expected
market bar until product/session evidence establishes that trading was available.

The 6J start is 23 hours later than the other panel starts, consistent with its
existing capture README. The audit does not establish why, whether those hours
belong to the Aegis calculation interval, or whether a recapture is required.
Do not truncate the other legs to 6J's start to conceal this difference.

Private evidence under the existing ignored
`op1/2026-09-14-seven/step3-coverage` directory:

| Artifact | SHA-256 |
|---|---|
| `audit.py` | `8a3b2a8b1865a54b789868c4f9b3ac341e23147683522af7dbdd39c8afd98bdb` |
| `panel-inventory.json` | `607d861714aaaa1eeb7843e58ff9ece1d17df4da833c081c7b3161e332dbddd1` |

The JSON binds full panel hashes, row counts, endpoints, all observed gaps and the
runner hash. The runner uses the bundled Python 3.12.14 and does not change inputs.
An independent pandas read reproduced all four hashes, row counts, endpoints,
strict ordering and gap counts. Both private artifacts are gitignored;
`git diff --check` passed. This is local verification, not independent acceptance
review of Step 3.

### Calculation origin and startup remain distinct questions

TradingView documents that Deep Backtesting starts calculations at the beginning
of the selected date range, and that EMA/RMA results depend on calculation origin.
Its [calculation-origin explanation](https://www.tradingview.com/support/solutions/43000666266-why-do-the-data-of-the-regular-mode-and-deep-backtesting-not-match/)
does not establish the exact UTC first calculation bar for our retained captures.
The visible September 1 date alone does not resolve that instant. The private
TB-W1 inventory's assertion that panel origin equals Deep origin is therefore not
accepted as proof; exact parity alone also does not establish all startup state.

Code inspection of the retained adapters and `pine_ta.py` establishes:

- EMA seeds at its first valid value; RMA seeds from its initial length-sized SMA
  and then remains recursive. A proposed multiple-of-length live hold does not
  prove exact independence from earlier state.
- Aegis carries synthetic-price Bollinger/ATR and previous-close state; Striker
  carries ATR, its moving average, breakout history and session/account state;
  Vanguard carries recursive EMA/ATR and previous-value/session/account state.
- ORB evaluates available prior opening-range volumes. Its empty-history branch
  permits the volume condition, and a partial history is averaged as available.
  Fifteen sessions is a bounded history capacity, not a mandatory cold-replay
  exclusion. Imposing the suggested live hold on the reference replay would
  change behavior.

These observations do not yet bind every effective override or certify live
restart readiness. Broker/account state cannot be recovered solely by warming
indicators. The existing `cold_at_panel_origin` intake assertion requires accepted
coverage evidence; the inventory does not supply that acceptance.

### Remaining Step 3 exit work

1. Bind each reference capture's exact calculation origin and end semantics to
   retained source/settings evidence, including the older 6J/MGC reference cases.
   Resolve the 6J prefix before declaring any common comparison interval complete.
2. Bind actual per-case adapter settings and initialization to those boundaries;
   reconcile first/final trade events and terminal state without exclusions.
3. Join every observed gap to accepted product/session evidence in Step 4. Keep
   unresolved trading-time gaps blocked; obtain source bars when required.
4. Independently review the combined coverage report before issuing coverage PASS.

No strategy, runtime, source settings, calendar verdict or admission changed in
this initial slice.

### Continued investigation — retained 6J prefix candidate

Initial inventory committed as `a2799f8`; repository commit checks passed. A
read-only scan of six September 3/5 raw 6J exports in Downloads found a previously
retained prefix candidate, `BAR_EXPORT_v0.2_CME_6J1!_2026-09-05_a759e.csv`, SHA-256
`4dc86e96ae5ace2fed2e8d9e097a7076bf93301387a89e3f198c342476802018`.

It contains 185 unique entry-encoded bars from 2022-08-31 00:00Z through
2022-09-02 00:00Z, including **88 bars on September 1 before 23:00Z**. All five
overlapping bars match the pinned 6J panel in every OHLCV field. The canonical
`bar_export_loader` decoder accepts all 185 signals and their v0.2 metadata;
instrument metadata is constant and matches the panel sidecar. OHLCV shape,
finite values, nonnegative volume and 6J tick alignment pass. These checks make
it a candidate for qualification, not an accepted splice or proof of the original
strategy's calculation origin.

The raw source of the pinned panel (`ed300`) reproduces every one of its 94,805
bars exactly. The earlier `1e1e0` capture contains the 88-bar prefix but differs
on every overlapping OHLCV row and is not a substitute for the precision-corrected
panel. The two duplicate September 5 full exports (`72d33` and `f79cb`) begin at
the same late boundary and differ from the panel on one row; do not silently
replace the pinned panel with either. The short `c2642` capture supplies no prefix.

Private diagnostic artifacts in `step3-coverage`:

| Artifact | SHA-256 |
|---|---|
| `audit_raw_6j.py` | `6117551f27dc5330fac5a9208547e017491376fa175bbd2577ed2c27b1a6c9d5` |
| `raw-6j-candidates.json` | `9b45c8c3738d2e5c2b6c3733a854d54c71266da54072687e6d5c4528105dec8a` |

The report binds all six raw file hashes, the pinned panel hash, duplicates,
boundaries and overlap comparisons. Its prefix decoder is diagnostic; the
separate canonical-decoder check above validates the candidate's full metadata
shape. Neither checker establishes capture settings or acceptance by itself.

Next: establish the prefix capture's provenance and original strategy calculation
boundary, then compare cold replay with the appropriate retained history. Retain
the current panel unchanged until that evidence is reviewed. A fresh bar export
may be unnecessary; no recapture decision is made by this inventory alone.

### Prefix sensitivity replay (after commit `416169d`)

Executed two fixed diagnostic scenarios without tuning settings: the unchanged
6J panel and an in-memory sequence prepending the candidate's 88 September 1 bars.
Both use the existing private reconstructed effective settings, pinned Aegis
export and current replay components. The private report binds those input and
component hashes; reconstructed settings remain diagnostic, not newly attested
capture evidence. The pinned panel file was not changed.

Both scenarios match all **121** exported closed trades at quantity scale 1,
with zero excluded exports and no quantity, price or P&L mismatches under the
existing comparator tolerances. Their full closed-trade sequences are exactly
equal. Both end with zero position and no pending orders. This establishes
closed-trade insensitivity for these two tested origins only, not equality of
every internal indicator state or live restart readiness.

Crucially, the two different origins both pass: a matching trade sequence cannot
identify the original TradingView calculation boundary. Prefix provenance was
requested from the operator and remains pending. No coverage PASS is issued.

| Private artifact in `step3-coverage` | SHA-256 |
|---|---|
| `replay_prefix.py` | `c08c949f0ec5cedc4c363847029fea500344c94af124c13eeae1367a75062dd2` |
| `prefix-replay.json` | `86ede9ca996e2510b666af0b5a78b7a7eb7e288f9dc6b6a8aa7675bc3f8c0ef9` |

Final runner invocation on bundled Python 3.12.14 exited 0. A preceding attempt
to add terminal-state reporting called the position accessor incorrectly and
failed JSON serialization; corrected to `position()` and reran both scenarios.
The hashes above identify the successful final generation.

### Nine-reference event and held-position coverage

Prefix replay findings committed as `c8ef13b`; commit checks passed. Continued
with all seven September 14 cases (using corrected O-N) and the retained Aegis
and Vanguard references. The private runner verifies each export digest, binds
panel bytes and inspects raw rows without silently dropping incomplete trades.

Across **3,632 trade pairs / 7,264 event rows**:

- Every trade ID has exactly one entry and one exit.
- Every event's New York display-clock timestamp maps to exactly one retained
  panel bar; no event has a missing or ambiguous panel label.
- No adjacent-bar gap intersects a captured entry-to-exit hold. This includes
  gap intervals at hold boundaries, using the actual UTC panel timestamps.

A separate implementation enumerated every 15-minute timestamp inclusively from
entry through exit for each pair and found all timestamps in the corresponding
panel. It also checked entry precedes or equals exit. Both checks ran on bundled
Python 3.12.14 and exited 0. This is local cross-verification, not independent
acceptance review. No source values or runtime behavior changed.

| Private artifact in `step3-coverage` | SHA-256 |
|---|---|
| `event_coverage.py` | `28d1e69b282aa17744bd55c2971c8c6aa6473fe871b8e37a8702a15e54743c99` |
| `event-coverage.json` | `ee1ae712c9f010e8c03f6afbcee7a465b70180bed895a267cfca07673dc3701d` |

This resolves the bounded question of retained bars during captured trade holds.
It does **not** classify gaps while flat: indicators update outside positions,
so those gaps remain in the Step 4 calendar queue. Nor does it establish the exact
Deep calculation origin, end-date inclusion semantics, independently attest all
effective settings, or admit a bundle. The pending 6J provenance question and
Step 3's combined coverage review remain open.

### Seven fresh XLSX range bindings and startup observations

The event-coverage findings were committed as `f511060`; commit checks passed.
Continued beyond the date-only picker by downloading TradingView's complete XLSX
reports for corrected O-N, O-P and all five Striker cases. No Pine source body was
edited. Striker used MYM1!, the recorded per-case account-size overrides and the
fixed September 1, 2022–September 2, 2026 Deep range. ORB used MNQ1! and the pinned
add parameters, with adds disabled only for O-P. O-P's inactive-input difference
remains governed by Step 2. Original ORB adds and Striker account-size controls
were restored after collection; no layout save or live action was performed.

All seven `Properties!B3` cells report **Backtesting range = August 31, 2022,
20:00 through September 2, 2026, 20:00**. In the retained New York display-clock
context these correspond to **September 1, 2022, 00:00Z through September 3, 2026,
00:00Z**, matching MYM/MNQ panel endpoints. The separate `Trading range` field
must not be substituted for this field. TradingView documents that XLSX exports
include the [Properties data and overall available backtesting range](https://www.tradingview.com/pine-script-docs/concepts/strategies/#properties-tab).

The private comparator checks all **6,346 event rows and all 17 columns** against
the original seven CSVs: zero differing cells. Numeric cells compare as decimals;
Excel date serials must be within a tiny representational rounding distance of an
exact minute before comparing the timestamp. Text compares exactly. These are
fresh declared-range bindings plus complete trade-export equivalence. They do not
independently prove historical hidden state or whether the displayed endpoint is
an included calculation bar. No coverage PASS follows solely from those cells.

Independent reviewer `packet0_review` decoded the workbook XML separately and
verified all rows/columns, symbols, intervals, case account-size settings, ranges,
and final runner/workbook pins. **Accepted for this bounded comparison, no
findings.** The earlier stale O-N runner pin was regenerated after generalizing
the comparator; only the final generations indexed below apply.

The startup-state runner observes the first 2,000 retained bars for each of nine
reference cases, retaining full adapter parameters, explicit emulator overrides,
port/runtime hashes and the first observed indicator seeds/windows and entry
intents. It confirms ORB can emit its first entry before its prior-session history
reaches capacity; the five Striker cases share indicator startup observations;
Aegis/Vanguard retain their recursive seeds. This is executable replay evidence,
not a live hold policy or a complete source-to-initial-state acceptance. The older
Aegis/Vanguard effective inputs remain reconstructed evidence. No seed or window
was changed to improve comparison results.

The gap queue preserves all **4,142 product-specific intervals**, grouped into
21 observed patterns for 6J, 22 for MGC, 26 for MYM and 25 for MNQ. Every group is
still `UNCLASSIFIED`, with no source attached. Patterns are descriptive, including
elapsed-time differences around DST; they do not infer market closure. Every
interval and each panel boundary remain available for Step 4's targeted evidence
review. No universal historical archive prerequisite is reintroduced.

Private evidence index: `step3-coverage/step3-evidence-index.json`, SHA-256
`1d764dbf8f21f7690bf45c02f8d9ab3323772a3bcafca54831d8b7982c989fc5`.
It binds seven XLSX files, seven comparisons, captures, startup observations and
the calendar queue to exact bytes. Key final identities:

| Artifact | SHA-256 |
|---|---|
| `inspect_xlsx.py` | `f7efe64379fb5da0e6de6315bf6d9aa3b2b44f6e88c46f36dd362ad1db756049` |
| `startup_state.py` | `d390ed7a7798a77dab1d87185b8f3e645b62f2c7e1d9dc2398261ed8d6e60a1e` |
| `startup-state.json` | `ae14a8dac50751ca6583b2ff85c55d071d16422670898cca19b19bd636ee5eeb` |
| `calendar-gap-queue.json` | `509346d604999baf270a26091727883e1ca583bf03e504028a6654eb86b35328` |

Final analysis invocations on bundled Python 3.12.14 exited 0. The startup runner
was corrected to serialize its frozen date sets explicitly before its successful
final generation. The independent review also reconfirmed the previous panel and
event-coverage claims; it did not rerun the two-origin Aegis replay.

### Step 3 acceptance disposition

**OPEN — not finished, not admitted.** The minimum remaining evidence is:

1. Complete historical source/settings binding for Aegis/Vanguard. Fresh declared
   ranges and the operator's retained-prefix provenance attestation are now bound
   below; they do not independently establish every historical hidden state.
2. Exact end-inclusion interpretation and complete source/settings/initial-state
   binding. The seven fresh workbook ranges remove the date-only ambiguity for
   the declared ranges, not every initialization obligation.
3. Accepted product/session evidence covering the flat-time gaps and boundary
   intervals, joined through Step 4. D19 membership and the four forward event
   observations cannot supply these facts.
4. Combined review of the completed coverage record before issuing PASS.

Existing event/held-position evidence and the seven matching workbook exports
need not be recollected merely because these other prerequisites remain open.

Independent reviewer `packet0_review` accepted this final progress handoff with
no material findings and independently verified all 25 indexed artifact hashes
and sizes. This accepts the evidence record's accuracy, not Step 3 completion.
Local `git diff --check` passed; private XLSX and analysis artifacts remain ignored.

### Attested 6J prefix and older-reference report ranges

The operator confirmed that `BAR_EXPORT_v0.2_CME_6J1!_2026-09-05_a759e.csv`
used the same 6J1! 15-minute chart and precision-corrected harness as the main
September 3 export: **only the date window changed**. This resolves the collection
provenance question. It does not attest exchange-calendar completeness or admit
the panel. The private attestation binds both raw-export hashes.

Fresh full Aegis and Vanguard reports were downloaded from their saved TradingView
layouts without editing inputs, broker-emulator properties or Pine bodies. The
Deep range was set to September 1, 2022–September 2, 2026. Both XLSX Properties
declare August 31, 2022, 20:00 through September 2, 2026, 20:00 in the retained
New York display context: September 1, 2022, 00:00Z through September 3, 2026,
00:00Z. Symbols and 15-minute intervals match their references.

- Vanguard: all **676 event rows × 17 columns match exactly**.
- Aegis: all **242 event rows** compared; exactly **30 cells differ**, exclusively
  `Size (value)`. All other cells match. For each differing cell, exact decimal
  entry price × entry quantity × point value equals the original CSV value;
  ordinary binary floating-point multiplication produces the XLSX value. Parsed
  binary64 values differ by one representable step; the largest decimal difference
  is `1e-10`. These specific derived-value serialization differences are explained,
  retained in the report, and **do not change the comparator's exact-equality
  rule**. Its `all_columns_match=false` remains accurate.

Independent reviewer `packet0_review` reproduced both comparisons, the Aegis
arithmetic explanation and raw-export pins, accepting these bounded claims with
no material findings. Fresh reproduction is distinct from independent proof of
historical installed source bodies or hidden initialization state.

A separate private derivative now joins the attested **88 retained bars** to the
original 6J panel: **94,893 rows**, from September 1, 2022, 00:00Z through
September 3, 2026, 00:00Z. The assembler verifies five raw overlap rows across
OHLCV, strict timestamp ordering and exact preservation of all original panel
rows. No bar was invented and the original panel was not replaced. Its start
matches the fresh declared range. The earlier fixed two-origin replay already
establishes unchanged closed trades for these same decoded prefix bars; that
result alone does not qualify all indicator state or missing intervals.

| Private artifact | SHA-256 |
|---|---|
| `6J-prefix-provenance-attestation.json` | `b85e6b70be5c729b29dc086daee913de8da1c7ad77e3d4a39d6e4eac8e118177` |
| `6J_M15-with-attested-prefix.csv` | `8ae083d07b6870aa427dc69009434da0f3cab2d6818ca356e441ad40f3648fd2` |
| `Aegis-boundary-report.xlsx` | `7e92c06fda51c3e9327810ffdaa9a6836ca09856440de6c08203fc785171886f` |
| `Vanguard-boundary-report.xlsx` | `1e76ccf67f007038723d80807bb1eb3ba72526367e21ef4b5a0fab580a75cec2` |

`step3-evidence-index-v2.json` binds these files, captures, comparison runners,
results and assembler to exact bytes, retaining the prior index unchanged.
SHA-256: `7bfbf0358b75fa860ff2a257aad4967d803417d2586b547eb52be51332fa4d26`.
Final comparator, notional check and assembler invocations on bundled Python
3.12.14 exited 0. The notional check's first attempts exposed a CSV BOM and an
incorrect comparison of decimal string error with a binary ULP; the final check
compares parsed binary64 values and retains the separate decimal difference.

**Step 3 remains OPEN.** No further prefix attestation is needed. Exact endpoint
inclusion, complete source/settings/initial-state binding, and Step 4's accepted
session evidence still require completion. The existing 4,142-gap queue describes
the original panels; the derivative's added prefix intervals must also enter the
calendar join before coverage acceptance. A declared range and a recovered prefix
cannot substitute for that join. No admission, production dispatch or resumption
was enabled.

The independent reviewer also verified all 16 v2-index artifact hashes/sizes,
all 88 derivative prefix bars against the raw export, preservation of the 94,805
original rows, and the five overlap rows. The final bounded evidence handoff was
accepted with no material findings. `git diff --check` passed.


## September 15 amendment — separate provider coverage and session legality

The operator authorized the [calendar/parity separation amendment](2026-09-15-calendar-parity-separation-amendment.md).
It controls the current Packet 1 acceptance method over earlier requirements in
this record to classify every historical gap through exchange calendars.
Provider-data coverage requires complete, source-bound provider bar evidence,
exact ordered timestamp/OHLCV agreement and accepted initialization; matching
trades or shared omissions alone do not establish it. Unexplained shared provider
gaps do not assert exchange closure and remain blocking for any dependent
legality, fill or completeness claim. Existing evidence and verdicts are preserved;
a newly reviewed admission contract is required before using the amended method.

The first forward release uses a versioned September 3–30, 2026 file of qualified
ordinary sessions, denying holiday, shortened and uncertain adjacent sessions.
Missing/expired coverage halts new risk; safe flattening, protective/recovery
ownership, prior-account-session chronology across denied days, settlement,
separate resumption and activation gates remain required. D19 stays immutable
historical date membership only. Step 3 and Packet 1 are not closed by this change.

## Step 3 continued — provider identity, endpoints and cold initialization

Evidence gathered on base `d109cf1`, September 15, 2026, under the approved
calendar/parity amendment. Private raw files remain outside tracked source.
No strategy settings, reference panel, runtime behavior or admission verdict was
changed. The diagnostic browser capture returned to its original 6J symbol,
with the export harness hidden and Aegis selected.

### Provider evidence

The four retained raw BAR EXPORT files reproduce their frozen Python panels
exactly: ordered timestamps and decimal OHLCV, 15-minute durations, stable symbol
metadata and sequential entry identities. The attested 6J prefix remains a
separate derivative. Independent review reproduced all four conversion checks.
This establishes conversion identity, not capture completeness by itself.

Fresh full-window BAR EXPORT workbooks cover the same declared Deep range. All
**378,512 entry-bar timestamps** match the corresponding Python inputs, including
the attested 6J derivative, from September 1, 2022, 00:00Z through September 3,
2026, 00:00Z. Both endpoints are represented. The terminal encoded entry must be
retained even though the report's closed-trade count is one lower.

| Input | Fresh entry bars | Timestamp differences | Price differences | Volume differences |
|---|---:|---:|---:|---:|
| 6J with attested prefix | 94,893 | 0 | 0 | 1 |
| MGC | 94,617 | 0 | 0 | 4 |
| MYM | 94,499 | 0 | 0 | 0 |
| MNQ | 94,503 | 0 | 0 | 3 |

Comparisons use exact decimal values, without interpolation or tolerance. Raw
workbooks and the eight differing values are retained privately. Their cause is
not independently certified. Fresh workbooks corroborate timestamps and prices;
the three differing symbols cannot silently replace the retained generation.
Even MYM's complete agreement does not alone establish historical source state
or export completeness. A separately reviewed evidence disposition is required.

Current installed Aegis source is byte-identical to its pinned file. Vanguard
matches its pinned text after CRLF/LF normalization only. The installed harness
uses corrected tick precision, encodes each in-window bar into alternating
entries, and has window controls covering the selected interval. These current
observations do not retroactively establish original chart provenance. The
original MGC/MYM/MNQ capture attestation is pending; no repeat 6J attestation is
needed. Seven-bundle source-body attestations already recorded remain valid.

### Initialization evidence and remaining state dependency

`full-initialization-and-interval.json` records the actual complete Python cold
adapter and emulator objects for all nine reference cases, preserving indicator
buffers and class defaults. All **851,011 bar calls** occurred once in panel order,
including both endpoints. Each run ended flat with no pending orders. The runner
also compares an empty-run constructor with the actual full-run initial object.
Independent review reproduced the nine cold snapshots and inspected the full-run
instrumentation; it did not independently rerun all nine complete replays.

Source review maps active indicator seeds, session history, position levels and
initial account state to the captured settings. It distinguishes behaviorally
inert initial differences from literal state equality and keeps disabled source
branches conditional on the captured controls. This is a cold-replay claim,
not live restart/recovery acceptance.

**A material source-state obligation remains:** Vanguard's active daily resets
use Pine's provider daily-time series, while Python substitutes a holiday-adjusted
key whose supporting explanation relies on trade outcomes. Striker uses a plain
shifted daily key. Capture actual provider daily timestamps/reset markers for the
complete MGC/MYM interval and compare their transitions with the actual adapters,
including the origin, holiday-adjacent bars and DST. Matching trades cannot
establish this mapping. This is provider-series evidence under Step 3, not a return
to universal exchange-calendar gap classification. Subsequent account/fill event
ordering also remains distinct from empty initial account state.

The earlier regular-session gap screen is retained as diagnostic evidence only:
3,972 ordinary-closure candidates and 171 residual gaps over the derivative-aware
inventory. It neither admits session facts nor supplies trading permission.

### Evidence seal and next acceptance checks

Private `step3-evidence-index-v3.json` binds 30 new artifacts and preserves v2:
`9c8d36cbace103e99cda62e6401d5dc45d32927aa04343feecb2f570b05c6569`.
The seal builder verifies all prior v2 artifact hashes/sizes and the unchanged
runtime/private-port identities used by the full initialization evidence.

| Report | SHA-256 |
|---|---|
| Retained raw/panel identity | `cf107bec15063bae2307359eba5d35afc19b15bfd0eabaf94c52a3872b2f4536` |
| Full initialization and interval | `c1aa67c0fd93d62b423918493b16996cc507aab9de993b47e9c6fcb484eb7da8` |
| Fresh exact 6J/MGC comparison | `231c66f0f118e1df800f4064f9c019db9a9ddf69de80528158a94b5aba67eb8e` |
| Fresh exact MYM comparison | `f311dfb6ed4f746b857e184771efcd765558ff9e7bfe4582b35a00259d42c3d2` |
| Fresh exact MNQ comparison | `5a9c5c9bb86c01ca6ee3166348ea31caa079f051b051154677e3a48d97b39660` |

Final comparison and seal-builder invocations on bundled Python 3.12.14 exited
zero. An exit-zero diagnostic is not a coverage PASS: all eight differences remain
in the reports. The earlier float-based endpoint probes are retained; the exact
decimal reports above control the value-comparison claims.

**Step 3 remains OPEN.** Finish original capture provenance and completeness,
resolve the recorded generation differences through review, establish the active
provider daily series and complete state/event binding, then review the combined
source/settings/panel/runtime evidence and new admission contract. Calendar and
settlement acceptance remain separate Packet 1 gates. No live capability or
automatic resumption is asserted.

Independent reviewer `packet0_review` accepted this bounded continuation with no
material findings. It independently verified all 30 v3 hashes/sizes, fresh MYM
and MNQ exact-decimal results, the reported aggregate bar-call count and the
source-state review record. It did not rerun nine full replays, certify browser
restoration or establish the cause of volume differences. `git diff --check`
passed and all 12 local Markdown targets in the two changed documents resolved.
