# Seven-bundle intake and runtime interface plan

Status: INTERFACE PROPOSAL — no intake admission, parity verdict or qualification run. Runtime coordinator owns implementation/amendments; parallel prerequisites owns collection and independent evidence verification. E/P/U remain approved.

Public derivative of the preserved local proposal: exact private override values remain in the #382 manifest, not this publication. No new interface approval is recorded.

## Grounding

Read current `book_parity.run_leg` and `parity_for`, emulator `_affordable` and exclusions, production `book_policy.leg_quantities`, and the frozen D19 metadata. `parity_for` still selects the historical export and `qty_scale`; `run_leg` accepts explicit bars/adapter/emulator overrides but is not a complete law-B admission/feedback owner. The emulator implements entry affordability, not margin calls. Production Striker cap currently consumes the explicit `cap_alloc` input; chart micro-cap and account capacity must not be conflated.

Parallel task reports seven CSVs and 50 evidence hashes verified plus diagnostic checks passing; audit digest `ffcf0ad93d72d8bdada1572b52881105368a4ac9d8a5bfea82b1dbb88d2c8f1c`, collection manifest v2 digest `da7157517032b76179bd3c07850c5779f968298261db6b75bd0c3c1dca383adb`. These are attributed diagnostic results, not independently repeated admission evidence. Actual Pine-body/export-state binding, coverage/warm-up and independent report reconciliation remain missing.

## Amendment ownership and order

1. Runtime owner drafts one scoped S1/R-P/R-Q and export-menu amendment after reading the pinned private Striker body. Privately bind the manifest-recorded chart cap, each actual Account Size and all other effective inputs independently from runtime leg allocation and the fixed account cap. Derive the Pine cap equation and reachable base/add set from that body; never replace the account cap or every capacity input with the chart cap. If the chart override changes the qualified quantity contract, identify that change and its acceptance evidence explicitly before admission/freeze. Approval that an export is the intended backtest does not prove equivalence to the adapter default.
2. Runtime owner drafts one scoped ORB evidence/replay amendment: the actual manifest-bound quantity, finite margin and normal/protected adds settings. Do not relabel finite margin as zero margin. Identify affordability and margin-call semantics separately. Retain the actual finite-margin affordability branch in the oracle. Any unsupported margin-call path must be modeled and independently verified, or proved unreachable over the entire specified acceptance domain under criteria fixed before results. Absence in these CSVs alone is insufficient. If neither is established, admission remains blocked; do not silently switch back to zero margin.
3. Preserve historical `effective_inputs.json`, phase1 manifests and historical `parity_for` behavior. New bundles receive distinct explicit identities and outputs. The runtime owner implements a reusable intake/runner; parallel task verifies the outputs and coverage. Do not build a second sizing implementation in the intake runner.

## Proposed intake and runner boundary

Proposed module: `ops/c1_signal_daemon/book_bundle_intake.py`.

`admit_bundle(candidate_manifest_path, *, trusted_contract_path, evidence_root) -> AdmittedBundle` validates before returning a usable identity. The trusted contract is separately reviewed and digest-bound, not supplied solely by the candidate manifest. Inputs bind bundle ID; source/Pine body hash; adapter version/hash; actual adapter and emulator overrides; CSV and capture hashes; source-state attestation; normalization version; chart/timezone/cost settings; window and warm-up bounds; bar-panel identity/coverage; independent reconciliation report and approved deviations. Invalid/missing fields return a refusal with no admitted artifact. Raw figures/captures stay private; tracked outputs are permitted digests/verdicts only.

`run_bundle_parity(bundle: AdmittedBundle, *, admission, feedback, bars) -> BundleParityResult` resolves the explicitly admitted CSV and overrides, never `locate_export(leg_id)` or a historical default. It validates bars against the admitted panel identity, uses shared law-B sizing with complete risk/stop/point-value/chart-cap/allocation/lifecycle/mode inputs, and routes each actual fill/fee/PnL outcome back to the adapter's halt and executed-base state. The `admission` and `feedback` arguments are proposed integration ports; their actual producer implementations must precede acceptance, not be replaced by a quantity-only callback. Compare actual integer quantities and cashflows with `qty_scale=1` for the new bundles. No scaling of a captured normal ledger to manufacture protected parity.

Tests must plant wrong body/state/override hashes, wrong CSV selection, historical default fallback, missing warm-up, chart/default cap-binding divergence, rounded-normal-vs-law-B divergence, margin affordability rejection, unsupported margin-call exposure, stale executed-base state and size-dependent halt divergence. Preserve historical comparator regression tests. Review amendments before any decision-bearing parity/qualification use.

## Calendar boundary returned to the parallel task

Verified frozen D19 coverage: **2022-09-01 through 2026-09-02 inclusive**, accepted for date membership only. Historical replay requests cover that window plus the actual required pre-window warm-up sessions derived from each pinned adapter; no warm-up start is asserted before that derivation. Forward rows begin **2026-09-03** and must extend through the explicit deployment/qualification horizon. No approved final horizon date is present in this task; retain it as a required input rather than assuming the rest of 2026 is covered.

Proposed `SessionCalendarRow`: source trade date, order symbol/product, timezone, session-open/close UTC, mandatory-flat-deadline UTC, full-closure flag, next-session identity/open, source URL/artifact digest, observed timestamp, attestation identity and coverage bounds. Product settlement time is a separate optional fact, never the trading deadline. Typed overlay dates remain separate from immutable D19. Validate coherent ordering, DST mapping, product agreement and coverage; the earliest applicable deadline supplies V to the approved rev8 formula. No synthesized weekday fallback outside verified coverage.

## Settled-account boundary returned to the parallel task

Proposed `SettledAccountClose`: account identity, prior venue-session identity, balance/equity, historical EOD peak, complete fees/cash adjustments, effective close time, acquisition time, immutable source evidence digests and reconciliation/completeness verdict. Live producer is a venue-backed account statement/history acquisition plus the approved attestation/reconciliation path; the specific API/export provider remains unqualified. Net-position or working-order evidence alone is not this producer.

Replay producer derives terminal session cash/peak from continuous simulated fills and costs and labels it simulated. It cannot serve as live settled-account evidence. Both consumers refuse a missing/wrong-session/incomplete close; do not carry forward a stale mode or substitute a product settlement quote. TB-T1 binds private evidence; TB-I3 consumes validated live state and TB-I2 consumes validated simulated state through the same typed semantics.

These proposed interfaces name the required producers and refusal boundaries. They do not certify any provider, broaden an approved dataset or waive formal intake, parity or live gates. Durable recovery implementation can continue independently while the evidence-contract amendments are prepared.


## September 15 amendment — separate provider coverage and session legality

The operator authorized the [calendar/parity separation amendment](../../notes/2026-09-15-calendar-parity-separation-amendment.md).
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
