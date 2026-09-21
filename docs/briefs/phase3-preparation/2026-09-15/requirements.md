# F1 requirements and dependency matrix

**DRAFT preparation; no gate is frozen by this table.** The governing references
were grounded at the original base `c86a0a0`, including addenda; implementation
status below includes subsequent tooling integration. `ACCEPTED` means only the
stated scope; `DRAFT` is a proposed F1 value; `EVIDENCE` identifies an actual fact
still owed; `LATER` is not a new pristine-E1 gate. Implemented checks do not supply
their future inputs or combined acceptance. Current evidence is in
[production-readiness.md](production-readiness.md),
[tooling-review.md](tooling-review.md) and
[representative-workloads.md](representative-workloads.md).

## Governing source key

| Key | Current source / revision |
|---|---|
| P1 | `docs/briefs/pre-registration/2026-09-12-track-b-final-validation-prereg.md`, DRAFT, especially §§1–10a |
| P2 | `docs/adr/2026-09-12-tradeify-book-protection-instance-admission.md`, rev9 plus first-ratification addendum September 14 |
| S1 | `docs/spec/2026-09-12-tradeify-book-protection-capacity-spec.md`, current quantity/settlement amendments |
| S2 | `docs/spec/2026-09-12-tradeify-synchronized-replay-spec.md`, RC-1–9 plus current incident and schedule amendments |
| S3/H | `docs/spec/2026-09-12-c1-multi-leg-rail-extension-spec.md` and `docs/spec/2026-09-14-tb-s3-halt-resume-contract.md`, rev9 attended incident amendment, §5 schedule retained |
| U/C | `docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md`, wave gates/TB-F1/O-items and September amendments; `docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md` §§55–57 |
| EP/U | `docs/briefs/handoffs/2026-09-14-track-b-ratifications.md`, approved content at `8101ba498aad812e79c3d80c45f963cd67b55de6`; first P2 blob `f94be43e25a9f4e4c0b10ccf3bb115f41aded3ec` |
| CAL | `docs/notes/2026-09-15-packet1-step4-session-calendar.md`, `ops/calendars/RATIFIED.json`, U/C September 15 calendar/parity amendment |
| SNAP | `docs/spec/2026-09-12-tradeify-account-snapshot-seal-contract.md`, including C8 settlement clarification and C10/P2 stop boundary |
| SET | `docs/spec/2026-09-15-tradeify-attended-settlement-contract.md`, approved design; runtime implementation and affected acceptance owned by Phase 2/coordinator |
| FP | `docs/spec/tb-i1-fingerprint-interface.md`, `policy_fingerprint.py`, literal vectors; accepted TB-I1 record in EP/U |
| GATE | `docs/methodology/regime_robustness_gate.md`, as specifically amended by P2 A1/B1/B2 |
| PH1 | Local Phase 1 handoff identified in README plus byte-verified [identity ledger](identity-ledger.md) |

The newer EP/U, S3 rev9 and calendar/parity addenda govern over stale proposed
headings and catalogue rows. Older claims that all seven bundles remain unaccepted
are superseded only within PH1's reviewed domain. P1 itself remains unfrozen.

## One requirements matrix

| Required field/gate | Governing source/revision | Producer/owner | Existing evidence | Remaining action | Consumer/hold point |
|---|---|---|---|---|---|
| F01 Fixed K=1 book and no replacement | P1 §1; U/C D-B4 | F1/coordinator | ACCEPTED four IDs/sides in current `BOOK_LEGS` | Pin complete book configuration, no optional leg | F1; every stage |
| F02 Fixed trailing policy/response | P2 §2; S1 §2 | I1/F1 | ACCEPTED candidate code; registry empty; no legacy constant substitution | Freeze planned canonical row + response map; never admit here | F1/E1; D0 later |
| F03 First P2 decision | P2 addendum; EP/U P | Operator record/coordinator | ACCEPTED revision-bound September 14 first decision | Reuse, authenticate record/blob at final head | F1, not a new approval request |
| F04 Execution/incident/schedule authority | EP/U E/U; S3/H rev9 | Coordinator/Phase 2 | ACCEPTED E/U and attended incident amendment | Verify integrated revision implements current amendments | F1 acceptance, no re-ratification |
| F05 Wave 2 accepted and merged | P1 §10a; U/C F1 | Phase 2/coordinator | Runtime and TB-I2 tooling integrated at bounded reviewed checkpoints; see tooling review | Final adopted head, affected independent review and combined G1–G5 composition acceptance | F1 hard hold |
| F06 Calendar completion | P1 §10a; CAL | TB-C1/coordinator | ACCEPTED bounded September domain only | Resolve historical/path/forward coverage, horizon and artifact inventory | F1 hard hold for consumed claims |
| F07 Seven admissions/source identity | U/C D-B14/O-9; PH1 | Phase 1 | ACCEPTED formal contract/review/run, hashes verified | Preserve unchanged; carry exact supplementary binding | F1 input |
| F08 Every reachable decision-bearing state | P1 §1; S1; D-B14 | Phase 1 + I2/I3 | EVIDENCE: historical seven results; no universal-state proof | Coverage map AUTHORIZED×NORMAL/PROTECTED; explicit risk/stop/allocation/confirmed-base witnesses; schedule-affected evidence | F1 hard hold |
| F09 WATCH parity/control inventory | P1 §§1,7; O-1/O-5 | Phase 1/I1/F1 | Historical WATCH bundles; shared law and zero Vanguard WATCH | Bind parity-only coverage; no WATCH optimization/decision candidate | F1 controls |
| F10 Source/port/runtime distinction | S2 RC-1; FP; PH1 | Phase 1 + Phase 2 | Owner corrected stale original c81aa5… to admitted efd479… at d107ebd; source verified | Verify adopted registry, stale-byte refusal and affected accepted parity; preserve original artifacts | F1 hard hold |
| F11 Panels, source fidelity and warmup | P1 §6; S2 RC-1/7; TB-W1; O-8/O-9 | Phase 1/I2 | Panel/export digests; provider-reset and Step3 pins in ledger | Validate all four coverage reports and warmup from each panel origin on accepted engine; exact exclusions | F1 |
| F12 Quantity and lifecycle laws | S1; P2 §2.2 | I1/Phase 2 | ACCEPTED shared risk-before-floor/cap; executed-base adds; Call-4 off-rail | Pin actual consumer path, configuration and unchanged law tests | F1 and replay/rail equality |
| F13 Capacity/priority/allocation | S1; S2 RC-5; U/C D-B8 | Phase 2/F1; V1 later | Pure capacity reducer exists; gross+reservations cap; atomic takeover spec | Freeze per-leg `cap_alloc` inputs; proof of reserve-before-send/whole-leg quiescence and identical replay law | F1 policy inputs; V1 actual deployment |
| F14 Protection timing/carried positions | S1; S2 RC-3 | Phase 2/I2 | `BookProtectionClock`, transition cancellation and sizing binding present | Continuous own-path close/peak, no intraday switch, no resize, cancellation race traces | F1 implementation |
| F15 Calendar/overlay digests | P1 §§6,9; CAL | TB-C1/F1 | Exact September/overlay/D19/ratification hashes in ledger | Keep immutable D19; add accepted mapping/coverage artifacts without extrapolation | F1; later extension separate |
| F16 Schedule and instant fills | S2 RC-8; H §5 | Phase 2/I2 | APPROVED D=min(16:00,V−15), cutoff D−15, flatten D−5 | Regenerated regular/early/DST/scheduler parity and fill-at-instant evidence; old 16:30 rule not reused | F1 |
| F17 Dates, session pool and halves | P1 §5; P2 B2; S2 RC-7 | I2/F1 | DRAFT full 2022-09-01..2026-09-02 | Exact usable source-session index N, H1 first ceil(N/2), H2 rest; disjoint union, per-leg late origin and exclusion reasons | F1, Part B |
| F18 Horizon | P1 §5; S2 RC-3/7; CAL | F1/coordinator | DRAFT 500 business/covered-session days; speed 200 | Resolve clock semantics/coverage, freeze exact horizon and no compression of unavailable sessions | F1 hard hold |
| F19 E1 initial state class | P1 §9; S2 ProtectionClock | F1 | DRAFT pristine equity=peak=basis, days=best=0 is permitted | Freeze explicit `EvaluationState`; optional sealed alternative only with authorization before F1 | F1/E1; no fresh B7 imposed |
| F20 Actual ongoing close | SET; S1 settlement; SNAP C8 | Phase 1 evidence + Phase 2 owner | EVIDENCE missing timezone/query, Sep14 boundary value/flatness, correction status | Source-qualified close and atomic listener chain tests; coordinator maps combined-acceptance dependency explicitly | Actual settlement/live use; F1 only through its required combined acceptance, not pristine initialization |
| F21 E2 initial state | P1 §9; SNAP/P2 C10 | T1/B7/operator | LATER fresh used-account snapshot absent | Fresh sealed B7, validity/no-activity and FBR/EF identity | Phase 6 sole n3; not pristine E1 |
| F22 Fill and cost model | P1 §9; S2 RC-4/9 | I2/F1 | TV emulator and venue commission schedule exist | Pin slippage/commission bytes and native full-fill composition; partial/conservative cells separate | F1 |
| F23 Continuous joint-flat bootstrap | P1 §§2,3a; S2 RC-3 | I2/F1 | Implemented continuous replay, joint-flat proof/sampling, source/path clocks and population pools; bounded synthetic review accepted | Bind actual source, startup and coverage artifacts; final composed runtime acceptance | F1 hard hold |
| F24 Calculator implementation/review | P1 §§2,10a | Calculator owner/F1 | PRESENT merged code 4e7a25d; fresh calculator+FP 150 tests passed | Preserve current byte hash; rerun on changes; use four-limb method | F1 sizing |
| F25 Design assumptions/joint power | P1 §2 | F1 | DRAFT p_fail=.03, p_200=.65, power=.80, Fréchet | Freeze assumptions independent of portfolio outcomes; retain sensitivity inputs only as design | F1 |
| F26 Exact n1/cutoff | P1 §§2,4 | F1 | DRAFT 200 per full/H1/H2; each failure fraction≤.05 | 600 evals; 10 failures max per population; screen adds no confidence | F1/E1 |
| F27 Exact n2/n3 depths | P1 §§2–3; P2 B1/B2 | F1 | DRAFT 970 each full/H1/H2; speed reuses full | Freeze 2,910 each stage; n3 not sized from n1/n2; exact CP method | F1/E1/E2 |
| F28 RNG roots/algorithm | P1 §2; P2 §2.4 | I2/F1 | Implemented domain-separated seed inputs and retained path/panel inventory; candidate labels remain unfrozen | Freeze actual root, recipe/runtime and child identities; reconcile old seed-label proposal with implemented recipe; no qualification n3 consumption | F1 |
| F29 Part A outer construction | P2 §2.4; P1 §3a | I2/F1 | ACCEPTED six-month replacement, original length, 100/200 rule | Concrete boundary/index/truncation definitions and accepted block ledger | F1 |
| F30 Part A inner construction | P2 §2.4; P1 §3a | I2/F1 | Accepted five-session rebuild rule implemented with continuous alternate-panel proof and deterministic splice fixtures | Bind actual qualified joins, panel indices and startup model; complete composed acceptance | F1 |
| F31 Part A statistic/expansion | GATE/P2; P1 §3a | F1/I2 | Floor .95; p5≤full pass sanity; within 1pp expand200 | Freeze percentile method, inclusive expansion boundary, reserve 200 panels and cumulative rule | F1/E1 |
| F32 Part A exact depth/budget | P2 A1; S2 RC-3 | F1/I2 | DRAFT d=200; repeated 500-session path/Part A proof measurements available, provisional | Complete controller/proof/actual-workload overhead and approved numerical budget; no linear illustration treated as resource bound | F1 hard hold |
| F33 Second exact-depth decision | P2 §7/T2 | Operator/coordinator | LATER; never granted by first decision/calculator | After F1, dated addendum with actual depth, contract and tool/runtime/vector digests | E1 hard hold; not requested here |
| F34 Part B workload | P2 B1/B2; P1 §3a | I2/F1 | DRAFT n2 H1/H2 970 each, not half-depth | Map to exact session pools; no extra Part B draws; bounds imply point floor | F1/E1; n3 halves later |
| F35 Legality and all other workloads | P1 §§3–4; S2 | I2/F1 | G1–G5 interfaces and once-only N1/CUTOFF/joint-N2/Part-A controller implemented; signed full composition pending | Actual legality/source coverage; accepted composed sequence, deterministic diagnostics and complete budgets | F1/E1 |
| F36 Complete shared inventory | P1 §6; P2 serialization; FP | F1/Phase 2 | Retained-byte/module-origin collector and signed trust-domain validator implemented; provenance is not execution binding | Complete actual code/data/port closure and captured execution binding under final reviewed runtime; bind approved source/config artifacts | F1 hard hold |
| F37 Canonical recipe/exclusions | P2 serialization; FP | I1/F1 | ACCEPTED single `tb-i1-canonical-v1`, tests/vectors | Pin runtime/tool/deps; full `book_policy`; only permitted policy provenance/registry-node exclusions | F1 and every downstream consumer |
| F38 Independent governance checks | P2 T4/T11; FP | D0/I3/F1 | Registry validation helper exists | Authenticate expected rows/provenance, approval chain separately; helper identity is not approval | F1 recipe; D0/activation later |
| F39 Config/initial-arm vectors | P1 §6; P2 T11; FP | F1/I3 | Canonical config and two-field delta tests present | Exact real baseline config and before/after vectors pinned; no hidden state exclusion | F1 recipe; activation later |
| F40 FBR/EF/result binding | P1 §6; P2 §2a/b | E1/B7/D2 | LATER; none issued | E1 contract+n2+PartA; B7 shared equality; GO-only EF reseal | E1 seal and later chain |
| F41 Year partitions/removal variants | P1 §7 | F1/I2 | DRAFT monitoring table in candidate | Materialize partial-year session indices and each removal map before results | F1; monitoring only |
| F42 Dependence/cost/fill/outage variants | P1 §7 | F1/I2 | DRAFT exact perturbations/cutoffs | Accepted stress implementation, child streams, count and missing handling | F1; not n3 acceptance additions |
| F43 Best-trade/month/year/downside | P1 §7 | F1/I2 | DRAFT deterministic tie/statistic definitions | Freeze transformation semantics and outputs; no candidate replacement | F1; descriptive only |
| F44 Seam risk and windows | P1 §§7–8; phase1_config | Phase 1/F1/I2 | ACCEPTED_UNMODELED; no exact seam index claimed | Evidence-backed contract-month seam indices ±2 sessions, count M, budgets; if unavailable unresolved before F1 | F1 monitoring contract |
| F45 Replica/RNG/budget/severity/action | P1 §7 battery contract | F1 | DRAFT per-cell fields in candidate | Freeze exact variant list incl M, budget, unresolved disposition, operator/down-only action | F1 before results |
| F46 Predictive interval/clock | P1 §7 | F1; E2; O1 | DRAFT q10/q50/q90 unconditional T incl infinity | Freeze inverse-ECDF method, effective-activation session anchor and trigger/action rules | F1 rule; n3 quantities later |
| F47 One attempt/failure/void | P1 §4; P2 §4/R1 | Coordinator/I2 | Durable journal/checkpoint dispatch and terminal-prefix/no-redraw tests implemented | Combined authenticated controller/result acceptance; preserve terminal failure, ambiguous closure and C10 stop | Every stage |
| F48 Privacy/output roots | P1 §10; U/C D-B12 | All owners | Public docs; private inputs remain primary ignored roots | Private numerical results; public only approved digest/verdict/exclusion/idle counts; no ports/account data | Every stage |
| F49 Executable command contract | S2 Interfaces; P1 §10a | I2/F1 | Calculator/benchmark commands and gated production source/executor/controller APIs implemented | Final composition, real authority/input bindings and reviewed invocation; no ungated actual-run command | F1/E1 |
| F50 Pre-reopen readiness | P1 §10a; S3/H; O1 | Coordinator/Phase 2 | Approved rev9 incident/preflight design; runtime acceptance pending | Named contract plus accepted implementation trace; distinguish source/route live evidence | F1 dependent implementation; activation separately |
| F51 Independent review | Assignment E; repo workflow | Phase 3 reviewer | Review recorded separately | Resolve blocking preparation findings; recheck integrated refresh later | Preparation acceptance only |
| F52 D0/D1/V1/live releases | P2 T4 onward; P1 §10a | Coordinator/operator | LATER gated sequence | E1 PASS→D0 admission + separate D1 GO→V1→qualified image/B7→sole n3→D2 | Not performed; no GO inferred |

## Concrete contradictions to resolve

1. **Port generation:** Phase 2 confirmed c81aa5… was the preserved original port,
   not a wrapper; its committed registry now pins admitted efd479…. Verify the
   correction/refusal on the adopted integration and preserve affected verification.
2. **S2 stage coverage:** continuous MC/Part A replay and G1–G5 orchestration now
   have dedicated implementations. Runtime crash/restart replay remains a different
   consumer. Final signed composition and affected review are still required;
   implementation existence must not be reported as source or F1 acceptance.
3. **Coverage and clock:** historical source pool ends September 2, forward file
   begins September 3 and expires September 30, proposed path horizon is 500.
   Resolve which exact calendar evidence drives each clock; no date extrapolation.
4. **Budget:** repeated representative path/proof measurements supersede the
   generic-component proxy for provisional planning. Full controller/proof and
   actual-runtime costs remain incomplete; no numerical budget is approved.
5. **Actual evidence versus prerequisites:** pristine E1 needs no used-account
   reconstruction; missing actual closes remain unresolved for their real consumers.
   Any claim that combined acceptance blocks F1 must identify the exact required
   implementation/evidence gate, not invent a fresh-B7-before-E1 condition.

## Addendum 2026-09-21 — T10 phase 1 evidence status

Per-F phase-1 status from the T10 source/freeze executor (steps 1–3 only; step 4 and phase 2 not performed). Full table, bundle reconciliation, contradiction dispositions and missing producer facts: `docs/notes/2026-09-21-t10-phase1-source-reconciliation.md`. No row above is edited; ACCEPTED means the phase-1-verifiable evidence is in hand, BLOCKED names the missing fact, NOT-PHASE-1 defers to this packet's phase 2 / step 4 or a later stage.

- F01 ACCEPTED — `BOOK_LEGS` four IDs/sides pinned `book_policy.py:179-197` (`ffcd3aab…`, unchanged since d107ebd), no optional leg.
- F02 ACCEPTED — trailing instance pinned `book_policy.py:65-114`; registry EMPTY; canonical-row freeze remains F1's act.
- F03 ACCEPTED — revision-bound September 14 first decision reused by reference (EP/U `8101ba49…`/`f94be43e…`).
- F04 NOT-PHASE-1 — integrated-revision verification is packet phase 2.
- F05 NOT-PHASE-1 — final adopted head + combined composition acceptance is packet phase 2.
- F06 BLOCKED — missing fact: proven per-symbol regular-session enumeration 2022-09-01..2026-09-02 (coverage inventory `e2841b62…` is INCOMPLETE_NOT_RUNTIME_INPUT).
- F07 ACCEPTED-with-STALE-marker — seven bundles retained-accepted by ledger/Step 6/Step 3 references; registry file moved @`87db6b8` with port pins byte-identical; ruling R1 pending.
- F08 BLOCKED — universal-state coverage map + witnesses owed; historical seven results are not that proof.
- F09 ACCEPTED — historical WATCH bundles retained; parity-only binding at F1 controls.
- F10 ACCEPTED — stale-byte refusal verified at HEAD `book_adapters.py:46-47,121-123`; four pins unchanged since d107ebd; movement characterized.
- F11 ACCEPTED — panel/export digests + warmup pins retained (cold_at_panel_origin, 2022-09-01 origin, four PASS coverage reports); on-changed-engine revalidation owed with that engine's acceptance.
- F12 ACCEPTED — laws pinned (`book_policy.py:282-331`; `core/lifecycle.py` `0a70785d…`); tests pinned not run; consumer path moved @`7ba7844` and pinned at `724667a2…`.
- F13 ACCEPTED-law / inputs-unfrozen — capacity law `book_capacity.py` `95381097…` @`a9175a1`; per-leg `cap_alloc` inputs remain DRAFT (80/shared-80); F1 freezes; production 0 until V1.
- F14 ACCEPTED-clock / traces-owed — `BookProtectionClock` `book_policy.py:414+` unchanged; own-path/cancellation traces owed at F1 (I2).
- F15 ACCEPTED — all six calendar digests re-verified byte-identical at HEAD, unmoved since 2026-09-15; D19 immutable.
- F16 NOT-PHASE-1 — cutoff design approved; regenerated parity/fill-at-instant evidence is Phase 2/I2.
- F17 BLOCKED — exact N/H1/H2 not computable from accepted evidence; ruling R2 (panel-derived vs calendar-derived session index).
- F18 BLOCKED — horizon 500 covered-session / speed 200 proposed with no extrapolation past 2026-09-30; freeze gated on F17.
- F19 ACCEPTED — explicit `EvaluationState` `contract.py:77-83` @`1339604`; pristine `tradeify-e1-pristine/v1`; no fresh-B7-before-E1 prerequisite; instance freeze at F1.
- F20 BLOCKED — three facts still missing: CSV/query timezone+endpoints; Sept-14 boundary equity/flatness; close correction status.
- F21 NOT-PHASE-1 — fresh used-account snapshot is the Phase 6 / E2 chain.
- F22 ACCEPTED — emulator pinned at HEAD `2be77bab…` @`7ba7844` (moved: stale-close guard, noted); cost/slippage bytes frozen at F1.
- F23 NOT-PHASE-1 — final composed runtime acceptance is packet phase 2.
- F24 BLOCKED — calculator moved since its 150-test record (`4cb7851e…`→`896a5a1f…` @`05029ba`); rerun record owed.
- F25 ACCEPTED — design assumptions recorded independently of outcomes; frozen at F1.
- F26 ACCEPTED — design cutoffs (200; ≤10 failures per population) recorded; frozen at F1.
- F27 ACCEPTED — 970 per population design recorded; n3 not sized from n1/n2; frozen at F1.
- F28 ACCEPTED — domain-separated seed inputs implemented; root/recipe freeze + seed-label reconciliation at F1; no n3 consumption.
- F29 ACCEPTED — Part A outer rule accepted; concrete block ledger at F1.
- F30 BLOCKED — actual qualified joins/panel indices/startup model binding owed (private panels + composed acceptance).
- F31 ACCEPTED — expansion rule accepted; percentile method freeze at F1.
- F32 NOT-PHASE-1 — budget is step 4 + the operator's; none approved.
- F33 NOT-PHASE-1 — second exact-depth decision is a dated post-F1 addendum.
- F34 BLOCKED — exact session-pool mapping depends on F17's N.
- F35 BLOCKED — signed full composition + actual legality/source coverage owed.
- F36 BLOCKED — complete closure under the final reviewed runtime; 6 of 19 supplementary files moved since the ledger.
- F37 ACCEPTED — `tb-i1-canonical-v1` + vectors; runtime/tool/deps pinned at F1.
- F38 ACCEPTED — validation helper present; expected-rows authentication is the F1/D0 act (helper identity ≠ approval).
- F39 ACCEPTED — canonical config + delta tests present; real baseline vectors pinned at F1.
- F40 NOT-PHASE-1 — E1 seal chain and later; nothing issued.
- F41 NOT-PHASE-1 — partial-year indices materialized at F1/I2 before results.
- F42 NOT-PHASE-1 — stress variants accepted at F1/I2.
- F43 NOT-PHASE-1 — transformation semantics frozen at F1.
- F44 BLOCKED — exact contract-month seam indices ±2, count M, budgets not yet bound (ACCEPTED_UNMODELED stands).
- F45 NOT-PHASE-1 — exact variant list frozen at F1 before results.
- F46 NOT-PHASE-1 — interval method/anchor frozen at F1; n3 quantities later.
- F47 ACCEPTED — durable journal/checkpoint + terminal-prefix tests implemented; combined authenticated acceptance at F1/E1.
- F48 ACCEPTED — public/private root separation observed in this reconciliation.
- F49 NOT-PHASE-1 — final composition/invocation review at F1/E1.
- F50 NOT-PHASE-1 — pre-reopen readiness binding is packet phase 2 (consumes T07/T08).
- F51 NOT-PHASE-1 — independent review of the assembled F1 packet is phase 2.
- F52 NOT-PHASE-1 — D0/D1/V1/live sequence later; no GO inferred.
