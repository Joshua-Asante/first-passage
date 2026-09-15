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
