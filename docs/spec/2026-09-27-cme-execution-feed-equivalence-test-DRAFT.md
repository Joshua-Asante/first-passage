# SPEC: CME execution-feed equivalence test for the four-leg book (TB-I5 successor)

**Status:** FROZEN 2026-10-02 9391d9d51f0afe8d4727349edb044624f79c63bb8388bf8f85df2ca2aab08834 (§16.1 form; frozen on the operator's merge of PR #585, merge commit `721be61`). **Frozen body:** this file with this one Status line removed (recompute: `sed '3d' docs/spec/2026-09-27-cme-execution-feed-equivalence-test-DRAFT.md | sha256sum`; valid only if line 3 is this line and is the file's only line starting `**Status:**`, §16.3 step 6). **Three parameters stay OPEN** as operator decisions (§16.2; bindings logged in §16.4). Each is bound before any provider data by the §16.3 procedure, and collection may not start while any is OPEN. Provider-neutral: no provider is named, selected, priced or contacted here. The path keeps its `-DRAFT` suffix so that existing links resolve (§16.5). *Reading recorded 2026-10-03 (status-line pointer only; body unchanged):* the §7 correction row's "raise health" (`:150`) is read as **the source latches unhealthy** on a revision of a delivered bar (operator ruling 2026-10-02, sheet 2 item 3); the owner record is [binding packet §4 item 7](../notes/2026-10-02-feed-spec-open-parameter-binding-packet.md).
**Date:** 2026-09-27. **Base:** `claude/clever-wozniak-bx0u95` at `521d8f2`.
**Assignment:** [handoff H8](../briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md#h8--feed-provider-neutral-preparation) (provider-neutral preparation only). **Sequencing owner:** [deployment-checklist addendum 2026-09-27](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-09-27--staged-acceptance-evidence-proportional-to-the-next-step), workstream row "Feed" and checkpoints CP-6/CP-7.
**Successor to:** the TB-I5 specification named in the [Track B umbrella](../briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md) (row TB-I5 at `:234`, packet text at `:644`). The umbrella's placeholder path `docs/spec/2026-09-1x-cme-execution-feed-equivalence-test.md` does not exist; this file is that specification in draft. It does not edit the [locked XAUUSD feed-equivalence spec](feed_equivalence_discovery_test_LOCKED.md), which it uses as a structural template only.
**Companion:** the per-leg mapping table, the later-binding rule text for the F1 packet, the shadow-collection design and the funding-decision questions are in [the H8 preparation note](../notes/2026-09-27-feed-provider-neutral-preparation.md).

**Not granted:** provider selection, contact, signup, subscription, credential staging, spend or funding (D-feed and CP-7 remain closed); application of this test; shadow collection; any change to `emit_enabled`, `dry_run`, arming, deployment or orders; any edit to an owner document; any tolerance chosen after seeing data. Freezing this draft is an operator act.

---

## §0 — Reads (Rule 0; line anchors at `521d8f2` unless marked working tree)

| Source | Passage that binds this spec |
|---|---|
| [AGENTS.md](../../AGENTS.md) `:132` | "a new execution feed also requires the feed-equivalence pre-flight" |
| [STATE.md](../../STATE.md) `:32` | Source disposition: "no live feed approved … Provider-neutral preparation may proceed, but provider-specific implementation and spend wait until the fixed book clears every source-independent gate and the operator returns for the funding decision" |
| [S2b build ADR §2](../adr/2026-08-08-s2b-signal-daemon-build.md) `:48–:56` | Live CME bar source row (no live source selected; O-4 deferral; "Provider-neutral adapter-contract and feed-equivalence preparation may proceed"); Reconnect `:49`; Staleness `2 × bar_period + 30s` `:50`; Fail-closed "emit no signals of any type" `:52`; Strategy surface "`emit_enabled=false`" `:55` |
| Umbrella `:106` (O-4) | Funding "returns only after the fixed book survives every source-independent gate, one provider clears the mandatory licensing/auth/coverage facts, its adapter is ready for immediate validation and a live-test window is booked"; the broker bridge "is not a source" |
| Umbrella `:234`, `:644` (TB-I5) | Successor must keep the locked spec's shape ("binary 15-minute OHLC equivalence over a frozen overlap window"), re-scoped to the four order symbols and an abstract delivered source, "with OHLC aggregation, session boundary, timezone, continuous-roll handling, bar-close timing, a frozen overlap window, tolerances and a binary verdict rule fixed before provider data is observed"; "FAIL blocks the live test (the source, not the adapters, is the defect); PASS records the source identity and configuration digest as a shared component of the B7 execution fingerprint" |
| Umbrella `:553` (TB-S3 (A)) | One `BarSource` per order symbol (6J, MGC, MYM, MNQ; all 15-minute); "satisfying the protocol is not equivalence" |
| Umbrella `:111` (O-8) | Vanguard's post-holiday no-trade latch depends on TradingView's daily key; "parity depends on it" |
| [Checklist T14](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#t14--production-feed-selected-and-qualified-500k1m) `:273–:283` | "qualify original delivered bytes against canonical panels"; "Verify reconnect, corrections/backfill, duplicate/out-of-order, stale/missing symbol, DST/early-close and synchronization behavior"; "no post-result tolerance changes"; "no signal emission or account orders" |
| [Checklist addendum §1.4, §3 Feed row, §4 CP-6/CP-7, §5](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#1-circular-prerequisites-corrected) `:447–:449`, `:479`, `:494–:495`, `:499–:506` | Provider-neutral feed contract plus an explicit later-binding rule accepted with the F1 packet; behavior-changing findings settle before CP-6 |
| [Locked template](feed_equivalence_discovery_test_LOCKED.md) `:35–:83` | Shape: H_0 of identical 15m OHLC; UTC alignment on `(timestamp, symbol)`; window of "two completed weeks … two Sunday opens, two Friday closes, one EOM-adjacent period" (`:42`); single precision convention (F1, `:59`). Decision branches: H_0 is not rejected only if all bars match exactly at displayed precision, or within consistent sub-precision rounding (`:66–:67`); divergence localized to specific dates is "not yet decisive" (`:68`); systematic small differences, **or** differences on more than 0.5% of bars, reject H_0 (`:69`), so 0.5% is a rejection trigger, not a tolerance. F2: bar-diff incidence is not downstream-impact evidence (`:71`). Thresholds are immutable; "Re-opening requires a separate ADR justifying why prior thresholds were misspecified, written without reference to observed data" (`:81`) |
| [Q-DATAFIDELITY-1](../briefs/Q-DATAFIDELITY-1-tv-price-fidelity-and-integrity-gate-scope.md) `:18`, `:23` | Price comparison across differently rolled/adjusted continuous series was forbidden in Q-TVCOV-1 ("roll-rule/adjustment mismatch noise"); the locked spec tests "no CME-futures instrument" |
| `core/data/bar_data/README.md` `:3`, `:8`, `:11–:13` | Canonical M15 panels for 6J, MGC, MNQ, MYM, each "CME BAR EXPORT v0.2 … operator-supplied", span to 2026-09-03T00:00Z, sidecar `mintick · pointvalue · tz` |
| `core/data/tv_exports/README.md` `:3` | TV exports under `cme/` are the canonical research feed; CSV bytes gitignored |
| [Packet 1 Step 3 acceptance](../notes/2026-09-15-packet1-step3-acceptance.md) `:11–:12`, `:17–:20`, `:31–:35`, `:39–:40` | The accepted 6J input is "the separately attested 88-bar-prefix derivative" (`:11–:12`); MGC/MYM/MNQ exports: "15-minute continuous-contract charts … electronic trading hours and back-adjustment off" (`:17–:20`); the 2026-09-15 re-captures differed in **volume** from the retained original generation on eight rows (6J, MGC, MNQ), while "Fresh timestamps/prices and MYM OHLCV agree completely" and no tolerance was applied (`:31–:35`); shared absent intervals are absent input, not closures (`:39–:40`) |
| [Packet 1 execution domain](../notes/2026-09-15-packet1-execution-domain.md) `:262–:274`, `:356–:361`, `:485–:489`, `:502`, `:534–:538`, `:562–:566`, `:574`, `:689–:691` | Panel rows and "Adjacent intervals longer than 15 minutes" per panel (6J 1,035; MGC 1,035; MYM 1,036; MNQ 1,036); "No zero-volume rows occurred"; every longer interval retained and classified `UNCLASSIFIED` (`:262–:274`). The pinned 6J panel's raw source reproduces all its bars exactly; an earlier 6J capture "differs on every overlapping OHLCV row"; two duplicate September 5 exports "differ from the panel on one row" (`:356–:361`). Gap queue of 4,142 product-specific intervals (`:485–:489`), private `calendar-gap-queue.json` digest `509346d6…` (`:502`). 6J prefix attestation: same chart and harness, "only the date window changed" (`:534–:538`); the 94,893-row derivative (`:562–:566`), digest `8ae083d0…` (`:574`). Regular-session screen: 3,972 ordinary-closure candidates and 171 residual gaps, diagnostic only (`:689–:691`) |
| [Calendar/parity amendment](../notes/2026-09-15-calendar-parity-separation-amendment.md) `:48–:52` | An absent timestamp "is **absent from the qualified provider input**. It is not thereby an exchange closure, a zero-volume bar …" |
| [Packet 1 Step 4 session calendar](../notes/2026-09-15-packet1-step4-session-calendar.md) `:35–:39`, `:53–:54`, `:64–:67` | Product hours Sunday–Friday 18:00–17:00 ET with a 17:00 ET daily break; holiday halts per product; UTC instants, DST gap/fold refused; coverage 2026-09-02 22:00Z to 2026-09-30 21:00Z |
| [Replay spec TB-S2](2026-09-12-tradeify-synchronized-replay-spec.md) RC-2 (`521d8f2:…:21`), `BarPanel` (`:30`) | "One clock: the 15-minute bar grid keyed by UTC open time"; panels loaded digest-checked against `core/data/bar_data/SHA256SUMS` (file concurrently edited in the working tree; cited at `521d8f2`) |
| [Halt/resume contract](2026-09-14-tb-s3-halt-resume-contract.md#2-trigger-decisions) §2 (`521d8f2:…:27–:30`, `:37`), [§5](2026-09-14-tb-s3-halt-resume-contract.md#5-exact-schedule-rule) (`:67–:73`) | Unhealthy source halts the whole book; missing-bar timeout `2 × bar_period + 30 s` (30 min 30 s), "Do not count periods outside the source's required session coverage as missing bars"; barrier timeout `bar_period + 30 s`; "A recovered report updates health only; it grants no trading permission"; schedule in `America/New_York` from source-backed per-symbol rows |
| [Rail spec TB-S3 §5](2026-09-12-c1-multi-leg-rail-extension-spec.md#5--replacement-s2b-addendum-for-ratification) (`521d8f2:…:169`) | "Unhealthy sources emit no ordinary strategy signal until valid bars return … Source recovery never resumes trading. Preserve separate apps/volumes, source selection, build GO, M1 and emission gates" |
| `ops/c1_signal_daemon/feed.py` `:11–:58` | `Bar(ts, open, high, low, close, volume)`; `BarSource.poll()` + `connected`; `staleness_limit_s = 2 × bar_period + 30` |
| `ops/c1_signal_daemon/book_protocol.py` `:39–:40` | `BAR_PERIOD = 15 min`, `BAR_SLACK = 30 s` |
| `ops/c1_signal_daemon/book_validation.py` `:34–:46` | Bar validation: timezone-aware `ts`; finite OHLCV; `volume ≥ 0`; `low ≤ open, close ≤ high` |
| `ops/c1_signal_daemon/book_runtime.py` `:347–:391`, `:483` | UTC normalization; halt if `ts` outside the bound session, in the future, or delivered after `ts + BAR_PERIOD + BAR_SLACK`; `Bar.ts` "is the bar-open timestamp used by the Pine adapters"; first bar must equal the session open; non-contiguous or backward `ts` halts; a conflicting second bar for the same `ts` halts; a boundary waits for all four legs; partial barriers expire |
| `ops/c1_signal_daemon/book_evaluate_loop.py` `:1–:5`, `:21`, `:33` | Exact four-leg source registry in priority order; no config constructor, HTTP endpoint or sender; source-silence check at `2 × BAR_PERIOD + BAR_SLACK` |
| `ops/c1_rail/book_account_owner.py` `:847–:866` | Feed silence inside session coverage halts (`feed-silence`); startup cannot erase earlier missing history |
| `ops/c1_rail/book_policy.py` `:132`, `:172–:197` | Book legs and symbols `6J`, `MYM`, `MGC`, `MNQ`; `order_symbol` is "provisional continuous-contract notation" (`6J1!`, `MYM1!`, `MGC1!`, `MNQ1!`) |
| `ops/c1_rail/c1_sizing_host_reference.py` `:124–:133` | "absent broker symbols are intentional. TB-V1 supplies verified deployed bindings later" |
| [Campaign record §59 Ruling 7](../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#ruling-7--orb-lifecycle-l1-reaffirmed-and-the-account-fence-classification-contract-2026-09-27) (`:3997`) | ORB L1: "The halt/resume §5 cutoff overlay applies unchanged" |
| Campaign record `:191` (D13) | Continuous `1!` basis accepted with a stated seam limitation; `CONTINUOUS_CONTRACT_ROLL_UNRESOLVED` remains a recorded limitation |
| [Track A plan §3.2 (A9)](../superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md#32-a9--production-feed-verification-record-and-funding-checkpoint-added-2026-09-11) `:171–:217`, `:236` | Entitlements CME (6J, MNQ), CBOT (MYM), COMEX (MGC); six vendor questions; readiness checkpoint; A9-PREP: "freeze the provider-neutral `BarSource` contract, four-symbol mapping requirements and mocked … test contract" |

**#519 returns (read at `8c15f18`).** Each of the seven paths was grepped with `git show 8c15f18:<path> | grep -n -i -E "feed|provider|market.data|volume|roll|DST|bar source|BarSource"`:

| `8c15f18:` path | Result |
|---|---|
| `docs/notes/2026-09-26-s5-part-a-measurement-proposal.md` | Hits at `:83`, `:155`, `:210`, `:286` are code identifiers (`provider.py`, `proof_provider`) or incidental substrings; no market-data finding |
| `docs/briefs/handoffs/2026-09-26-s5-part-a-measurement-proposal.md` | No hit |
| `docs/notes/2026-09-26-orb-lifecycle-evidence.md` | **`:22`** (the accepted ORB Pine body, described in public prose): "The entry is placed once, on the bar where the opening range completes, if the day and volume filters pass"; "Early-close dates end the session earlier through the same rule". `:23` (runtime port `orb_mnq_v7`): emits the entry "if its filters pass", without naming the filters. Carried into M4 (§6) and the note's holiday-sensitive-behavior row |
| `docs/notes/2026-09-26-account-fence-four-state-trace.md` | Hits at `:63–:65`, `:145`, `:243` concern order fences, adapter feedback and test file names; no market-data finding |
| `docs/briefs/handoffs/2026-09-26-orb-lifecycle-and-fence-trace.md` | `:42`: a test file name only |
| `docs/notes/2026-09-26-close-semantics-c-a.md` | Hits concern cancellation rollback on liquidation (`:23`, `:126`, `:139`, `:161`, `:217`); no market-data finding |
| `docs/briefs/handoffs/2026-09-26-close-semantics-c-a.md` | No hit |

Two consequences are carried. The ORB entry reads volume (`orb-lifecycle-evidence.md:22`), so the volume metric M4 cannot default to descriptive (§6). And through Ruling 7 (campaign record `:3997`), the ORB L1 lifecycle leaves the §5 cutoff overlay unchanged, so this spec keeps the session and schedule inputs as they are.

## §1 — Purpose and what the test decides

**Question.** For each of the four order symbols, do the original bytes delivered by a future funded provider produce, after a frozen construction rule, the same 15-minute bars as the canonical CME TradingView-export panels the accepted book was qualified on? And do they arrive in time, and in step across the four legs, for the consumer that will read them?

**It decides:** a binary PASS/FAIL per symbol and for the book (§10). The umbrella makes PASS a prerequisite of the TB-I3 live-feed test, and it records the source identity and configuration digest in the B7 execution fingerprint (umbrella `:637–:638`, `:644`).

**It does not decide:**
- whether a divergence changes strategy outcomes or Monte Carlo results. Per template F2 (`:71`), bar-diff incidence is not impact evidence, so any impact claim needs its own analysis;
- provider selection, funding or licensing (CP-7);
- broker-route behavior;
- the book's qualification;
- any GO.

## §2 — Hypothesis

**H_0 (per symbol s):** over the frozen window, the provider's delivered data, constructed under §4, yields a 15-minute bar set for `s` equal to the canonical capture for `s` in existence, UTC bar-open timestamp and OHLC at the symbol's tick precision, within the frozen tolerances of §6. It is also delivered within the consumer's timing and revision bounds (§6 M5–M8).

## §3 — What is compared

| Arm | Side A (provider) | Side B (canonical) | Role |
|---|---|---|---|
| **L — live arm (verdict)** | Original delivered bytes captured during shadow collection (§12), unmodified, with receipt timestamps | A **fresh** CME BAR EXPORT v0.2 capture per symbol covering the same window. It is exported with the settings attested for the pinned panels: 15-minute continuous chart, electronic trading hours, back-adjustment off, the unchanged precision-corrected harness (Step 3 acceptance `:17–:20`). For 6J, the attested 6J chart and harness (execution domain `:534–:538`); its adjustment and trading-hours settings are UNVERIFIED (§4.5) | Decides PASS/FAIL |
| **C — canonical continuity (precondition)** | — | The fresh capture compared with the Step-3-accepted canonical input over their common span: for MGC, MYM and MNQ the pinned panel `core/data/bar_data/<SYMBOL>_M15.csv` (digest in `core/data/bar_data/SHA256SUMS`); for 6J the attested 88-bar-prefix derivative `6J_M15-with-attested-prefix.csv` (private, digest `8ae083d0…`; Step 3 `:11–:12`; execution domain `:562–:566`, `:574`), which preserves every row of the pinned 6J panel and adds 88 attested bars before it. The prefix bars enter arm C only if the fresh capture's range reaches them, and they are then compared like any other row (PROPOSED) | **Compared fields (PROPOSED, OWED):** existence and `(bar_open_utc, O, H, L, C)` in integer ticks (§4.4), with **0** differences on the common span. Volume is reported descriptively and is not part of arm C unless the operator freezes a volume role (M4). The fresh capture is admissible as Side B only if it meets this rule. A mismatch stops the test as `BLOCKED — canonical capture not reproducible`, not as a provider FAIL. The common span must be non-empty and at least the frozen minimum overlap (§16.2, OPEN-10). The rule must be set explicitly before freeze because re-captures are not byte-stable: the 2026-09-15 re-captures differed from the retained original generation in volume on eight rows (6J, MGC, MNQ), with timestamps and prices agreeing (Step 3 `:31–:35`); an earlier 6J capture differed on every overlapping OHLCV row, and two September 5 duplicate exports differed from the panel on one row in an unstated field (execution domain `:356–:361`) |
| **H — historical arm (optional, descriptive)** | Provider historical bars for a span inside the pinned panels | Pinned panel | Reported only; it cannot turn an L-arm FAIL into a PASS. Whether it is available is a funding-decision question (note §5) |

**Why a fresh capture is needed.** The pinned panels end at 2026-09-03T00:00Z (bar_data README `:8`, `:11–:13`). Shadow collection can only begin after CP-7 (addendum §4), so no delivered live bytes can overlap the pinned span. Arm C ties the fresh capture back to the Step-3-accepted inputs.

**Provenance observation (UNVERIFIED).** The bar_data README names the 2026-09-03 raw source exports of the panels (`…_ed300`, `…_08a82`, `…_4cea4`, `…_23dd6`). None of those names appears in `core/data/tv_exports/cme/SHA256SUMS`, which lists earlier captures only. The pinned *panels* are what the replay consumes (TB-S2 `BarPanel`), so Side B is defined by the panel manifest. Where the refresh raw files are pinned is not established here.

## §4 — Bar construction (frozen with the spec)

1. **Normalization.** Convert both sides to UTC. The key is `(symbol, bar_open_utc)` on the 15-minute grid, matching TB-S2 RC-2 and `Bar.ts` as the bar-open time (`book_runtime.py:369`). Panel sidecar `tz` values differ by symbol (`America/Chicago` for 6J, MNQ and MYM; `America/New_York` for MGC; bar_data README `:8`, `:11–:13`). Their role is **UNVERIFIED**: the README says only that the sidecar pins `tz`. The raw v0.2 export row carries an epoch field and a separate `tz` field (`core/bar_export_loader.py:47`, `:56`), and the decoder stores `tz` as a `timezone` metadata value (`:107`); how the derived panel consumer uses it was not read here. The key below does not depend on `tz`. A provider that stamps bars at close, or in a local zone, is translated to this key by a rule recorded in the adapter configuration. The translation is a later binding (note §3); the key is not.
2. **Aggregation.** If the provider delivers finer bars or trades, build a 15-minute bar from the constituents whose timestamps fall in `[open, open + 15 min)`. O is the first open, H the maximum high, L the minimum low, C the last close and V the summed volume. The exact constituent rule for each delivery granularity (1-minute bars, trades) is fixed before freeze; which granularity a provider offers is a funding-decision question.
3. **Empty intervals — rule OWED (operator); the canonical representation is established.** The pinned panels represent an absent 15-minute slot **by omission**: each panel has more than a thousand adjacent intervals longer than 15 minutes (6J 1,035; MGC 1,035; MYM 1,036; MNQ 1,036), and "No zero-volume rows occurred" (execution domain `:262–:274`). An absent timestamp is absent input, "not thereby an exchange closure, a zero-volume bar …" (amendment `:48–:52`; Step 3 `:39–:40`). The private gap queue keeps all 4,142 product-specific intervals, every group `UNCLASSIFIED` (execution domain `:485–:489`; `calendar-gap-queue.json`, digest `509346d6…`, `:502`), and a regular-session screen left 171 residual gaps, diagnostic only (`:689–:691`). **UNVERIFIED:** whether those residual in-session gaps are no-trade quiet slots or missing input. It is load-bearing. The consumer waits for all four legs at every boundary (`book_runtime.py:387–:391`) and halts on a non-contiguous boundary (`:376–:381`), so an omitted in-session slot on any leg halts the book. The operator sets the rule before freeze, from a classification of the existing gap queue against the contiguity rule (note §6). The rule is then applied identically to Side A, and the same finding goes to the consumer owner if it conflicts with the contiguity rule (addendum §5).

   *[2026-09-27: the classification was returned by [H8 step (b)](../notes/2026-09-27-h8b-feed-gap-classification.md). It found one observed affected permitted session; the other residual gaps fall on holiday account days. The operator gave guidance (Q-1) that missing required input halts and no bars are invented. The text below is **PROPOSED** for adoption at freeze and is not in force.]*

   **Empty-interval rule (PROPOSED).**
   - **(a) Absent is absent.** An in-coverage 15-minute slot with no trade-evidenced bar is missing required input, on either side. The adapter emits nothing for it. The consumer's contiguity, barrier and silence rules then halt the book. Under the halt/resume contract §4.1 (operator ruling 2026-09-27), that halt is an incident in commissioning and the first attended release.
   - **(b) No invented bars.** Neither the adapter nor the test harness synthesizes a bar for an absent slot: no carry-forward, no interpolation, and no zero-volume placeholder.
   - **(c) Provider-originated empty bars.** A delivered bar is **not trade evidence** if it has zero volume, or if the provider marks it as synthetic, filled-forward or no-trade. The adapter does not forward such a bar. It retains the bar in the raw capture, labelled, and the slot is scored as absent under M1. A provider that cannot distinguish trade bars from empty ones fails R-MAP-2's "never a silent fallback" test for this purpose, and that becomes a funding-decision fact (note §5 Q8).
   - **(d) Halted intervals.** An exchange trading halt inside a session is scored like any absent slot. How a provider encodes a halted interval (omission, a flagged bar, or a status message) is a Q8 fact for the funding decision. This rule does not presume that encoding.
   - **(e) Scope.** The daily break, weekends and DENIED account days are outside coverage (§4.6) and are never scored as absent.
4. **Precision.** Compare in integer ticks, using each symbol's `mintick` from its panel sidecar. That is one convention across all four OHLC fields, per template F1 (`:59`).
5. **Adjustment.** No back-adjustment on either side. This is attested for MGC, MYM and MNQ (Step 3 `:17–:20`). For 6J it is UNVERIFIED: the 6J attestation read here covers the chart, harness and date window only (execution domain `:534–:538`), and the 6J ledger says "back-adjusted continuous" (note §2).
6. **Session coverage.** Only slots inside the product's session per the ratified calendar rows are compared (`ops/calendars/`; Step 4 `:35–:39`), mirroring the halt/resume §2 rule not to count periods outside required coverage.

## §5 — Per-symbol mapping requirements

Each leg needs, **fixed before freeze** (each item's freeze status is classified in §16.2, row "§5 per-leg mapping") and cited to a source: the root and exchange; the provider-native symbol code; the **dated-contract selection (roll) rule** used live; the canonical panel's `1!` roll behavior; the session and holiday calendar rows; and the DST mapping. The table of what is established, and what is UNVERIFIED, is [note §2](../notes/2026-09-27-feed-provider-neutral-preparation.md#2-four-leg-symbol-roll-and-session-mapping). The binding requirements:

- **R-MAP-1 (roll rule, OWED).** The canonical `1!` series switch contracts on dates set by the charting platform's continuous-contract rule. The repo does not establish that rule from a primary source (MNQ ledger W1 calls a volume-lead roll "the TV-`1!` analogue", `ops/instruments/MNQ.md:96`; measured unadjusted quarterly gaps cluster near 3rd-Friday expiry, `lab/analysis/_inbox/ict_mnq_2026-08/RESULTS.md:145–:147`). Two things are owed before freeze:
  - a **live contract-selection rule** per symbol, which must agree with the venue binding TB-V1 supplies (`c1_sizing_host_reference.py:124–:133`);
  - a **roll-exclusion band** around each canonical roll date. Sessions in the band are reported as a separate descriptive stratum and are excluded from the verdict, because comparing across different roll rules is known noise (Q-DATAFIDELITY-1 `:18`).

  If the live rule and the canonical roll differ on which contract the strategies see, that is a behavior question. It settles before CP-6 (addendum §5) and is not absorbed as a binding.
- **R-MAP-2.** A provider-native code maps to exactly one dated contract per session. An unmapped, ambiguous or expired code is a stale/missing-symbol condition (§7), never a silent fallback to another contract.
- **R-MAP-3.** Calendar rows covering the whole window must exist and be ratified before collection starts. The ratified forward calendar currently ends 2026-09-30 (Step 4 `:64–:67`), and coverage expiry refuses new risk without inventing sessions.

## §6 — Metrics and PROPOSED thresholds (all OWED — operator freezes before data)

"Compared slot": an in-coverage 15-minute slot outside the roll-exclusion band, where Side B has a bar under the §4.3 rule. Counts are per symbol. **M1 is counted over a wider universe** (§16.2): every in-coverage slot outside the roll-exclusion band where **either** side has a bar, plus any Side-A bar after a product's early-close halt (§7). A Side-A-only bar therefore counts against M1. **Every Side-A bar after an early-close halt counts as an M1 failure, whether or not Side B also has a bar there**: §7 requires such slots to be absent on both sides (Codex review on #585). **A Side-B bar after an early-close halt anywhere in the verdict-window capture makes the run `BLOCKED — canonical capture inconsistent with the ratified calendar`** (§10). This check covers the full verdict-window capture against the calendar rows, not only arm C's historical common span, so a canonical post-halt bar can never pass silently (Codex review on #585). **Scope of the post-halt rules:** they apply only to **in-coverage** sessions, the permitted sessions in the ratified calendar rows. On DENIED account days and other out-of-coverage periods nothing is scored or blocked (§4.3(e), §4.6).

| # | Metric | Definition | PROPOSED threshold (OWED) | Basis of the proposal |
|---|---|---|---|---|
| M1 | Existence | Slots where exactly one side has a bar | 0 | Either side's missing in-session bar halts the book in the consumer: a later bar fails contiguity (`book_runtime.py:376–:381`), or the four-leg barrier expires (`:387–:391`; halt/resume §2 `:30`). A Side-A bar at a slot Side B omits is an equivalence difference; its consumer effect depends on the §4.3 empty-interval rule |
| M2 | Timestamp | Bars whose derived `bar_open_utc` differs from Side B's | 0 | One clock (TB-S2 RC-2) |
| M3a | OHLC incidence | Share of compared bars with any nonzero tick difference in O, H, L or C | **Default: 0** (exact match in integer ticks). Relaxed option: ≤ 0.5% | New proposal. The template's H_0-not-rejected branches require an exact match at displayed precision, or a match within consistent sub-precision rounding (`:66–:67`), and its 0.5% (`:69`) is a **rejection trigger**, not a tolerance; systematic small differences reject even below it. A nonzero incidence tolerance is a relaxation that needs explicit operator adoption |
| M3b | OHLC magnitude | Maximum absolute difference in ticks, any field | ≤ 1 tick (binding only if the relaxed M3a option is adopted) | New proposal: a severity cap so that incidence cannot hide large errors. It needs explicit operator adoption |
| M4 | Volume | Share of bars with a volume difference, and the maximum difference | **Verdict role and threshold OWED.** Not descriptive-only by default: the accepted ORB entry is gated by "the day and volume filters" (`8c15f18:docs/notes/2026-09-26-orb-lifecycle-evidence.md:22`), so at least the MNQ leg reads volume. Which other legs read volume is UNVERIFIED (private ports and Pine not read) | The canonical side is not volume-stable: the 2026-09-15 re-captures differed in volume from the retained original generation on eight rows (6J, MGC, MNQ), while timestamps and prices agreed (Step 3 `:31–:35`). A volume tolerance must allow for that, and the operator sets it (note §6) |
| M5 | Delivery deadline (L arm) | Bars delivered to the consumer after `bar_open + 15 min + 30 s` | 0 | Hard consumer bound (`book_runtime.py:350–:353`; `BAR_SLACK`). Each late bar would halt the book, so a nonzero tolerance means explicitly accepting that halt rate |
| M6 | Silence | In-coverage intervals with no bar for more than `2 × 15 min + 30 s` | 0 | Halts via `feed-silence` (`book_account_owner.py:847–:866`) |
| M7 | Post-delivery revision | Delivered bars whose OHLCV the provider later revised (a correction, or a backfill differing from the live delivery) | 0 revisions forwarded to the consumer; revisions seen only in the raw stream are counted, **threshold OWED** | A conflicting redelivery halts (`book_runtime.py:361–:363`, `:382–:385`) |
| M8 | Four-leg completion | Boundaries where not all four legs arrived within the M5 bound, **plus** (PROPOSED) boundaries at which a leg delivered its next bar while the previous boundary was still pending | 0 | Barrier timeout `bar_period + 30 s` halts (halt/resume §2); an overtaking leg halts the book with `bar-sequence` (`book_runtime.py:377–:381`) |
| M9 | Decision identity (descriptive) | Boundaries where the four adapters, replayed offline on Side A bars and on Side B bars, emit different intents | Reported; its verdict role is OWED | Template F2: bar equality and decision equality are different claims |

**Window (OWED).** Proposed minimum: ten complete covered sessions for all four symbols at once, including two Sunday opens, two Friday closes and one month-end-adjacent session. This matches the template's window content (`:42`: "two completed weeks. Captures two Sunday opens, two Friday closes, one EOM-adjacent period"). DST transitions and early closes are included if they fall in the window. If they do not, the verdict records them as **not observed**, and those cases rest on consumer tests (halt/resume §7 names "early-close/DST/missing coverage") rather than on this test.

## §7 — Handling rules

Each rule states the consumer's existing behavior (the owner), how this test counts the event, and what the adapter must do. The adapter must never repair data into equivalence.

| Condition | Consumer behavior (owner) | Test treatment | Adapter requirement |
|---|---|---|---|
| **Gap**: a missing constituent inside a 15-minute bucket | None directly; it sees only the built bar | Built bar compared under M1–M3. Constituent gaps are logged from the raw capture | Build only from delivered constituents; never interpolate. A bucket whose completeness cannot be established by the deadline is not emitted, and M5/M8 count it |
| **Gap**: a missing 15-minute slot | Non-contiguous `ts` halts (`book_runtime.py:376–:381`); silence halts (`book_account_owner.py:864–:866`) | M1 and M6 | Emit nothing; report unhealthy |
| **Reconnect** | Unhealthy while disconnected (S2b §2 Reconnect `:49`); an unhealthy source halts the book; recovery grants no permission (halt/resume §2 `:37`; rail §5) | Each disconnect, its duration and the reconnect are recorded; affected slots are scored under M1/M5/M6 | Reconnect with backoff; after reconnect deliver only bars still within the M5 bound |
| **Correction / backfill** | A second, different bar for a known `ts` halts (`book_runtime.py:361–:363`, `:382–:385`); a stale `ts` halts (`:350–:353`) | M7. Backfill is recorded in the raw capture and labelled; it never substitutes for the live delivery in the L arm | Never forward a revised bar for a delivered `ts`. Record it and raise health |
| **Duplicate** | An identical bar for the same `ts` is ignored (`book_runtime.py:358–:364`, `:382–:386`) | Counted, not a failure | Forward at most once per `ts` |
| **Out-of-order** | Backward `ts` halts (`book_runtime.py:376`) | Counted; M1/M5 score the effect | Deliver in `ts` order per symbol |
| **Stale or missing symbol** (one leg silent, unmapped, expired contract) | Barrier incomplete, then halt (halt/resume §2 `:30`); silence halt | M6, M8; R-MAP-2 | Report the leg unhealthy; never substitute another contract or symbol |
| **Early close** | Calendar rows set `V` and the §5 schedule (halt/resume §5 `:67–:73`); product halts differ (Step 4 `:37–:38`) | Slots after the product's halt must be absent on both sides; a provider bar there is an M1 failure | Emit nothing after the product's halt |
| **DST** | UTC instants; DST gap/fold wall times refused at calendar load (Step 4 `:53–:54`) | UTC keys only. The window's DST exposure is reported | Timestamps in UTC or an unambiguous offset; never naive local time |
| **Daily break (17:00–18:00 ET)** | Outside session coverage; not counted as missing (halt/resume §2 `:28`) | Excluded from compared slots | Emit nothing in the break |

## §8 — Synchronization across the four legs

The consumer registry is exactly four sources in priority order (`book_evaluate_loop.py:21`). A boundary releases only when all four legs have reported (`book_runtime.py:387–:391`); otherwise the barrier expires and halts (`:483`; halt/resume §2 `:30`). Two further constraints come from the same code:
- A leg that delivers its next boundary while the previous boundary is still pending **halts the book** (`bar-sequence`, `book_runtime.py:377–:381`). A fast leg overtaking a slow one is therefore a book halt, not a rejected input; M8 counts it (PROPOSED).
- Without retained history, the first accepted bar must be the session's opening boundary (`:371–:373`).

The test therefore scores the book, not only each symbol. M8 counts the boundaries that fail to complete, and the record keeps each leg's arrival time for every boundary, so that inter-leg skew is visible. Whether the four legs come from one source identity or several is a provider-specific choice; the record names each leg's source identity.

## §9 — Freeze procedure (before any data is seen)

*Step 1 is amended at freeze by §16.3: the document is frozen with its OPEN parameters listed, and each is bound before any provider data.*

1. The operator sets every OWED value, then freezes this document by digest. Status becomes `FROZEN <date> <digest>`. The OWED values are:
   - the §3 arm C rule (compared fields, units, tolerance, and 6J prefix treatment);
   - the §4.2 constituent rule for each delivery granularity;
   - the §4.3 empty-interval rule;
   - the §4.5 6J adjustment basis;
   - R-MAP-1: the live contract-selection rule per leg and the roll-exclusion band;
   - the M1–M9 thresholds and roles, including M3a's default-or-relaxed choice, M4's role and threshold, and M7's raw-revision threshold;
   - the window rule;
   - the §10 re-application rule;
   - the §13 re-opening vehicle.
2. Only after that may shadow collection start (it is itself post-CP-7). Any provider data seen before the freeze, including trial or sample data, is quarantined and may not be part of the verdict window.
3. The window's start and end are fixed by rule before collection (for example, "the first N complete covered sessions after the collection start"), not chosen afterwards.
4. The fresh canonical capture (arm L, Side B) is exported after the window closes, with the attested settings. Arm C must pass before arm L is scored.

## §10 — Verdict and what a FAIL blocks

- **Per symbol:** PASS if arm C passes and M1, M2, M3a, M5, M6, M7 and M8 meet their frozen thresholds, plus M3b **only if** the relaxed M3a option was frozen. Under the frozen exact-match M3a (§16.2), M3b is not checked. Otherwise FAIL. M4 and M9 enter only if the operator froze a role for them.
- **Book:** PASS only if all four symbols PASS within the same source-identity configuration.
- **FAIL blocks:**
  - the TB-I3 live-feed test, TB-E2 timing, TB-D2 and TB-B10 (umbrella `:106`, `:644`);
  - trading use of that provider configuration (checklist T14).

  The umbrella says only that a FAIL "blocks the live test (the source, not the adapters, is the defect)" (`:644`); it contains no finality or re-application clause.

  **Re-application rule (PROPOSED, OWED operator).** A FAIL is final for that source identity and configuration digest. A later application must:
  - count and report every attempt per provider, including the failed ones;
  - declare the configuration change and freeze it, with the window rule, before the new window starts;
  - follow an operator rule, OWED, on whether a change to later-binding B items only (note §3) may re-apply after a FAIL, and if so how many times.

  Without such a rule, a trivial setting change would reopen the test, and the zero-tolerance M5, M6 and M8 thresholds make outcomes sensitive to which window is drawn.
- **BLOCKED** (not FAIL): arm C fails; calendar coverage is missing; the capture is incomplete; or the fresh canonical capture has a bar after an early-close halt in an in-coverage session anywhere in the verdict window (§6). The test did not run.
- **PASS grants nothing** beyond recording the source identity and configuration digest in the B7 execution fingerprint. Emission, arming and deployment keep their own gates.

## §11 — Evidence record format

The umbrella requires "a RESULTS note with digests only" (`:234`) and that PASS records "the source identity and configuration digest" (`:644`). Raw provider bytes, the fresh capture and any derived bars stay in the private root; vendor-licensed data is never committed (AGENTS.md public-clone posture).

**Public RESULTS note (digests and verdict labels):**
- the spec digest and freeze date;
- the source-identity label and configuration digest (no credential values);
- the adapter commit;
- the mapping-table digest and the calendar ratification digest;
- the per-symbol verdict labels (PASS, FAIL or BLOCKED) and the book verdict;
- the digest of the private evidence record below;
- private-manifest digests for the raw capture, the fresh canonical capture and the canonical inputs.

**Private evidence record (private root):**
- the realized window, with the sessions excluded and why;
- per-symbol M1–M9 counts or rates;
- arm C results;
- the DST and early-close exposure observed or not observed;
- the collector host identity and its clock-synchronization evidence;
- per-boundary, per-leg arrival times;
- the emission-disabled evidence (§12);
- the attempt count for this provider (§10).

No owner read here permits public counts. Moving any field to the public note is an operator decision, OWED.

## §12 — What shadow collection with emission disabled must record

The design is [note §4](../notes/2026-09-27-feed-provider-neutral-preparation.md#4-shadow-collection-design-emission-disabled). For this test the collection must record:
1. every delivered message's original bytes with receive wall-clock and monotonic timestamps;
2. connection, authentication-renewal and subscription lifecycle events per symbol;
3. provider sequence identifiers, if any;
4. correction and backfill messages, labelled as such;
5. the dated contract subscribed per symbol per session;
6. the built 15-minute bars, with references to their constituent messages;
7. per-boundary, per-leg delivery times;
8. health state transitions;
9. the calendar rows in force;
10. emission-disabled evidence, as specified in the note.

## §13 — Forbidden moves

- Changing any threshold, window rule, aggregation rule, empty-interval rule, roll-exclusion band or verdict rule after any provider data has been seen. The template's rule is: "Re-opening requires a separate ADR justifying why prior thresholds were misspecified, written without reference to observed data" (`:81`). This draft proposes the same vehicle, a separate ADR. Any lighter vehicle would be a departure the operator must adopt explicitly (OWED, §9).
- Provider-specific carve-outs after data: excluding a symbol, session or failure class for one provider, or adding a tolerance for one provider.
- Re-running with a new window to obtain a PASS for the same source identity and configuration, or re-applying outside the §10 re-application rule.
- Substituting backfill or historical bars for live-delivered bytes in arm L.
- Repairing, interpolating or smoothing Side A.
- Editing the pinned panels, or using a fresh capture that fails arm C.
- Treating an interface or `BarSource` implementation as equivalence (umbrella `:553`).
- Any signal emission, listener POST or order during collection.
- Naming, selecting or funding a provider through this document.

## §14 — Open items and UNVERIFIED register

1. Whether the 171 residual regular-session gaps in the pinned panels are no-trade quiet slots or missing input (§4.3; execution domain `:689–:691`). The representation, by omission with no zero-volume rows, is established (`:262–:274`).
2. The canonical `1!` roll rule per symbol; the live contract-selection rule; the roll-exclusion band (R-MAP-1). *Roll rule resolved 2026-10-03/04 by the OPEN-11 binding (§16.2, §16.4); the live contract-selection rule (OPEN-3) and the band (OPEN-4) are bound or open per §16.4.*
3. 6J back-adjustment and trading-hours settings. 6J ledger `:3` says "back-adjusted continuous", while the Step 3 attestation of "back-adjustment off" names MGC, MYM and MNQ only (note §2). *Resolved 2026-10-03 by the OPEN-2 binding (§16.4): electronic hours, back-adjustment off; the 6J ledger line is corrected.*
4. Which legs besides ORB read volume (M4). ORB's entry reads volume (`8c15f18:docs/notes/2026-09-26-orb-lifecycle-evidence.md:22`). *Resolved 2026-10-03 by the OPEN-5 binding (§16.4): none besides ORB MNQ.*
5. Where the 2026-09-03 raw source exports are pinned (§3).
6. The role of M9 in the verdict. *Resolved 2026-10-03 by the OPEN-7 binding (§16.4): descriptive.*
7. Calendar rows for the eventual window (R-MAP-3).
8. Whether a fresh capture can reproduce the canonical inputs exactly in `(bar_open_utc, O, H, L, C)` (arm C). The 2026-09-15 re-captures agreed on timestamps and prices (Step 3 `:31–:35`). The field of the one-row difference in the September 5 duplicates is not stated (execution domain `:359–:361`).
9. The role of the panel sidecar `tz` value (§4.1).

## §15 — Verification of this spec

Commands run in this session (read-only; the working tree was shared with concurrent agents):
- `git log --oneline -1` → `521d8f2`.
- Owner reads by `sed -n`/`grep -n` on every §0 source. `git show 521d8f2:<path> | grep -n` was used for the three specs being edited concurrently in the working tree, so their line anchors refer to `521d8f2`.
- `git show 8c15f18:<path> | grep -n -i "feed\|provider\|roll\|DST"` over the #519 notes and cards (first pass). This reported no feed finding, which was wrong: see the review round.
- `awk '{print $2}' core/data/tv_exports/cme/SHA256SUMS` and `core/data/bar_data/SHA256SUMS`: names only; data absent in this checkout.
- `python3 scripts/check_md_relative_links.py --strict --glob <this file>` → 23 targets, 0 unresolved. A local heading-slug check of every `#anchor` in this file → 0 unresolved.
- `python3 scripts/check_handoff_authority.py --all` → 2 cards with an authority block, 0 violations.
- `grep -n -i` for provider names and prices over this file → none.

Review and fix round (2026-09-27), commands run: `sed -n`/`grep -n` re-reads of every cited line in the review findings (execution domain `:262–:274`, `:356–:361`, `:485–:502`, `:534–:574`, `:689–:691`; amendment `:48–:52`; Step 3 `:1–:45`; template `:40–:82`; Q-DATAFIDELITY-1 `:16–:23`; umbrella `:234`, `:644`; `book_runtime.py:370–:392`; `daemon.py:55–:100`, `:129`; `evaluate_loop.py:95–:106`; `m1_stage1.py:15–:52`; `m1_stage1_control.py:112–:119`; `bar_export_loader.py:44–:58`, `:100–:110`; `6J.md:3`, `:81`; Track A plan `:170–:237`; T00 P7 closure `:5`; STATE `:58`). The seven-path `8c15f18` grep is in §0. The outcomes are in [the note's review section](../notes/2026-09-27-feed-provider-neutral-preparation.md#review-and-fix-round-2026-09-27).

No test suite, no gate suite and no data comparison was run. No provider was contacted.

## §16 — Freeze record (2026-10-01)

### 16.1 Authority, and what the operator's merge does

**Authority.** Joshua's ruling of 2026-10-01, item 2: "The feed-equivalence spec may be **frozen now**, before any provider data". It is recorded in the deployment-checklist addendum "first-session simplification rulings" ([PR #580](https://github.com/Joshua-Asante/first-passage/pull/580), branch `claude/first-session-cuts`). The same ruling keeps signup and spend behind D-feed (a)+(b) and CP-7. **Who wrote this, and under what grant.** This section was drafted by a **worker** session, dispatched by the coordinating session to prepare the freeze under that ruling. The worker holds no `governance.author` on this owner record. The H8 card's grants (`governance.author` among them) are labelled "(coordinator)", so they belong to the coordinator seat, not to a worker (Codex review on #585). The section is therefore the worker's **task return, routed through the coordinator**. It takes effect only if two things happen, in order: the coordinator accepts it on the PR, and then the operator merges it. The same applies to the one-line pointer this PR adds to the H8 note.

**The merge is the freeze act.** Freezing is the operator's act (Not granted line, §9). The operator's merge of the PR that adds this section:
1. freezes the body at the digest in the Status line, **provided the merge commit's own copy of this file reproduces that digest**: `git show <merge-commit>:docs/spec/2026-09-27-cme-execution-feed-equivalence-test-DRAFT.md | sed '3d' | sha256sum` must equal the Status-line digest, with the §16.3 step 6 single-Status-line check passing on the same blob. If main changed this file after the branch's last sync and the merged copy does not reproduce the digest, the merge is **not** a freeze. The file stays the draft until a later commit records the merged copy's digest and the coordinator re-accepts it (Codex review on #585);
2. adopts every value marked **ADOPTED** in §16.2. Each one is a value this draft already PROPOSED before any provider data existed, and none is new in this section;
3. leaves every item marked **OPEN** as an operator decision, bound under §16.3.

**Freeze date.** The freeze date is the UTC committer date of the merge commit that brings this section into `main` (`TZ=UTC git log -1 --date=format-local:%Y-%m-%d --format=%cd <merge-commit>`). The date is normalized to UTC first: `%cI` keeps the committer's own offset, so a merge at 23:27 at UTC−4 would otherwise give the previous calendar day (Codex review on #585). It is not the 2026-10-01 drafting date in this section's heading. The first later commit that touches this file updates the Status line, which the digest excludes, to the §9 form `FROZEN <date> <digest>`. Until then the merge commit is the authoritative record of the date, and RESULTS notes (§11) cite it from there (Codex review on #585).

Before that merge, nothing here is in force and the document remains the draft. No provider data of any kind has been seen in preparing this freeze (§15; the H8 note §7; the 2026-10-01 provider-questions draft sent nothing and received nothing).

### 16.2 Status of each §9.1 item at freeze

Where the body says PROPOSED or OWED, this table governs.

| §9.1 item | Status | What is frozen, or what is owed |
|---|---|---|
| §3 arm C rule | **ADOPTED** | Compared fields: existence and `(bar_open_utc, O, H, L, C)` in integer ticks, **0** differences on the common span. **The common span must be non-empty.** The fresh capture must extend back into the canonical input's span, and an empty common span is `BLOCKED — canonical capture not reproducible`, never a vacuous pass (Codex review on #585). **OPEN-10:** the minimum overlap (covered sessions per symbol); an overlap below it is also `BLOCKED`. Volume is descriptive unless M4 gets a role. 6J: the 88 attested prefix bars enter only if the fresh capture reaches them, and are then compared like any row. A mismatch is `BLOCKED — canonical capture not reproducible` |
| §4.2 constituent rule | **ADOPTED; OPEN-1 BOUND 2026-10-03 (§16.4)** | Adopted: the bucket `[open, open + 15 min)`; O first open, H max high, L min low, C last close, V summed volume. **OPEN-1, bound:** (i) *Clock.* A constituent is placed by the exchange transaction time when the provider delivers it, and otherwise by the provider's stamp. Receipt time never places a constituent. The clock used for each stream is recorded in the adapter configuration (later-binding item B.5). (ii) *Bars of any duration d up to 15 minutes.* A constituent covers `[t0, t0 + d)`, where `t0` is its stamp if the provider stamps bars at their open, or its stamp minus `d` if it stamps them at their close. It belongs to the bucket that contains `t0` and is admissible only if its whole interval lies inside that bucket; a stream whose constituents straddle bucket boundaries is inadmissible, and constituents are never split. (iii) *Trades.* A trade belongs to the bucket that contains its time; a trade at exactly `open + 15 min` belongs to the next bucket. V is the sum of exchange-reported quantities. A busted or cancelled trade known before emission is excluded (operator ruling with this binding: within the exact constituent rule above). A bust learned after emission is not covered here; it goes with §4 question 7 of the binding packet. (iv) *Prices.* O, H, L and C come from executed trade prices only; a stream whose bars are built from bid/ask, midpoint, settlement or indicative prices is inadmissible (operator ruling with this binding: within the exact constituent rule above). (v) *Ordering.* "First" and "last" follow the clock in (i); ties are broken by the provider's sequence identifier, where one is given. (vi) *Native 15-minute bars* are compared as delivered, after the B.5 stamp translation. §7 completeness is not part of this binding |
| §4.3 empty-interval rule | **ADOPTED** | Rule (a)–(e) as written: absent is absent; no invented bars; zero-volume, synthetic, filled-forward or no-trade bars are not trade evidence; a halted interval is scored as absent; the daily break, weekends and DENIED days are outside coverage. Adoption at freeze is the path named in the [H8(b) acceptance](../briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md#h8--feed-provider-neutral-preparation) (Q-1) |
| §4.5 6J adjustment basis | **OPEN-2 BOUND 2026-10-03 (§16.4)** | **OPEN-2, bound:** 6J canonical settings are electronic trading hours and back-adjustment off; §4.5 applies to 6J unchanged. Evidence, method (b): the coordinator's private read on the operator's machine of the 6J derivative (digest `8ae083d0…`), recording dates and gap ratios only, found a discontinuity at each of the 15 quarterly switch sessions in the panel span (45–106× the median session gap), as an unadjusted series shows; hours follow from the H8(b) coverage (every permitted 18:00–17:00 ET session filled). The 6J ledger's "back-adjusted continuous" label is corrected with this binding |
| R-MAP-1 live contract-selection rule | **OPEN-3 BOUND 2026-10-04 (§16.4)** | **OPEN-3, bound:** for each leg, the live dated contract in a session is the contract that the bound OPEN-11 rule assigns to that session. One per-leg contract-selection object (N_s or the first-notice rule, the listed cycle including MGC's skipped October, and the last-trading-day rule) is defined once; both the feed adapter's subscription (R-MAP-2) and the TB-V1 order binding consume it. Provider-native codes are later-binding item B.4. **Venue check (coordinator, 2026-10-04, public sources):** Tradovate prohibits trading physically deliverable contracts "beginning on the business day preceding the earlier of the Last Trade Date or the 1st Notice Date" ([liquidation policy](https://www.tradovate.com/liquidation-policy)). For 6J and MGC, the old contract's last canonical session is the trade date before that prohibited day, so the live rule equals the canonical rule with **zero margin**; Tradeify's 16:45 ET daily flatten (`core/firm_rules.py:248`) means no position carries into it. MNQ and MYM are cash-settled. If the venue's rule or the flatten changes, the difference is a behavior question that settles before CP-6 (§5). TB-V1 still records the order-side binding |
| §5 per-leg mapping | **Classified per item** (Codex review on #585) | **Root and exchange:** ADOPTED as tabulated in [note §2](../notes/2026-09-27-feed-provider-neutral-preparation.md#2-four-leg-symbol-roll-and-session-mapping): 6J and MNQ on CME, MYM on CBOT, MGC on COMEX. **Provider-native symbol code:** not a freeze value. It is a provider-specific binding, mapped under the frozen per-leg rule, under later-binding rule items A.4 and B.4 ([note §3](../notes/2026-09-27-feed-provider-neutral-preparation.md#3-later-binding-rule--proposed-text-for-the-f1-packet), PROPOSED for acceptance at CP-6). If that rule is not accepted at CP-6, the codes become a pre-CP-6 hold. **Canonical `1!` roll behavior:** **OPEN-11 BOUND 2026-10-03 (§16.4).** For MNQ, MYM and 6J, the canonical `1!` series switches to the next listed contract at the 18:00 ET open of the session whose account date is the N_s-th CME business day (exchange holidays excluded) before the current contract's last trading day, with **N_MNQ = 3, N_MYM = 3, N_6J = 1**. Form: the platform's support page 43000691027 (fixed per-symbol offset). Values: the coordinator's private read of the canonical panels, 2026-10-03, recording session dates only; every switch from 2022-12 to 2026-06 matches. **MGC (bound 2026-10-04 by operator ruling; second OPEN-11 row in §16.4):** the canonical `MGC1!` series cycles Feb, Apr, Jun, Aug and Dec (the Oct contract is skipped), and switches to the next contract in that cycle at the 18:00 ET open of the session whose CME trade date is **1 CME business day before the expiring contract's first notice day** (the last CME business day of the month before the contract month). Evidence: the coordinator's private panel read, recording dates only, matches every switch from 2022-12 to 2026-08 once holiday sessions are dated by CME trade date and weekend price gaps are set aside; the August switches show the larger four-month spread; and the platform's public symbol page (read 2026-10-03, not signed in) showed `MGCZ2026` as `MGC1!`'s front month on 2026-10-02 while `MGCV2026` was still listed. The roll-exclusion band (OPEN-4) is applied around these dates. **Calendar rows:** a prerequisite before collection (R-MAP-3), not a freeze value. **DST mapping:** ADOPTED: UTC keys only; DST gap and fold wall times are refused (§4.1, §7) |
| R-MAP-1 roll-exclusion band | **OPEN-4** | No width proposed. Owed: the band around each canonical roll date |
| M1, M2 | **ADOPTED** | 0 and 0. M1 is counted over its §6 universe: every in-coverage slot outside the roll-exclusion band where either side has a bar, plus any Side-A bar after an early-close halt (§7). Side-A-only bars count, and every Side-A bar after an early-close halt is an M1 failure even if Side B also has one. A Side-B bar after an early-close halt anywhere in the verdict window makes the run BLOCKED (§6, §10). Both post-halt rules apply only to in-coverage sessions; DENIED account days are never scored (§4.3(e)). This reads M1's own definition ("exactly one side has a bar") and §7 over the narrower "compared slot" (Codex review on #585) |
| M3a, M3b | **ADOPTED** | M3a **0** (the default; the relaxed ≤ 0.5% option is **not** adopted). M3b is therefore not binding |
| M4 role and threshold | **OPEN-5 BOUND 2026-10-03 (§16.4)** | **OPEN-5, bound:** M4 has a verdict role on each leg whose accepted strategy body reads bar volume, which is **MNQ (ORB) only**: the coordinator's in-place yes/no read of 2026-10-03 (campaign §60; no body text or values recorded) found the accepted Pine and runtime port agree that ORB MNQ reads volume and Aegis 6J, Striker MYM and Vanguard MGC do not. On MNQ, at most one compared bar in the window may have `V_A ≠ V_B`, counted in integer contracts; the maximum difference is reported. On the other legs M4 is descriptive. Side B volume is taken from the fresh capture (arm L) |
| M5, M6, M8 | **ADOPTED** | 0, 0 and 0. M8 includes overtaking-leg boundaries |
| M7 | **ADOPTED; OPEN-6 BOUND 2026-10-03 (§16.4)** | Adopted: **0** revisions forwarded to the consumer. **OPEN-6, bound:** no verdict threshold. Post-delivery revisions seen only in the raw stream are counted per symbol, labelled, and reported in the private record. They reach the verdict only through M1–M4 and the adopted forwarded-revision limit of 0. The unhealthy latch on a revision of a delivered bar (Status-line reading) is unchanged |
| M9 role | **OPEN-7 BOUND 2026-10-03 (§16.4)** | **OPEN-7, bound:** M9 is descriptive; no verdict role. **Constraint on any binding:** M9 may get a verdict role only together with three things: matched pre-window Side-A and Side-B capture that covers each leg's frozen warm-up boundary (TB-W1); warm-up before scoring; and recorded adapter parity. The umbrella says "a leg without its warm-up bars cannot enter parity or a decision-bearing run" ([umbrella](../briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md) `:512`). Without these, M9 stays descriptive (Codex review on #585) |
| Window rule | **ADOPTED in part; OPEN-8** | Adopted minimum content: ten complete covered sessions for all four symbols at once, including two Sunday opens, two Friday closes and one month-end-adjacent session. DST and early closes are recorded as **not observed** if absent. **OPEN-8:** the exact start/end rule required by §9.3, fixed before collection |
| §10 re-application rule | **ADOPTED; OPEN-9 BOUND 2026-10-03 (§16.4)** | Adopted: a FAIL is final for that source identity and configuration digest. Every attempt per provider is counted and reported. A new application declares and freezes its configuration change and window rule before its window starts. **OPEN-9, bound:** after a FAIL, a provider may apply once more, changing only later-binding B items. Before the new window starts, the change, the FAIL record it answers and the new configuration digest are frozen. The new window is the next one the OPEN-8 rule produces after that freeze. If the re-application FAILs, applications by that provider end. A change outside the B items is a requalification (H8 note D), not a re-application. Every attempt, including BLOCKED runs, is reported |
| §13 re-opening vehicle | **ADOPTED** | A separate ADR "justifying why prior thresholds were misspecified, written without reference to observed data" (template `:81`) |

Unchanged by this freeze: §11's default that no count moves to the public note (moving a field stays an operator decision), and the §14 UNVERIFIED register.

### 16.3 Binding an OPEN item (amends §9 step 1)

1. Each OPEN item is bound by a dated operator decision, recorded as a row in §16.4 in the same commit that writes the value into the body.
2. Each binding produces a new frozen-body digest. It is written **only** in the Status line, which the digest excludes, replacing the previous one. The §16.4 row records the **superseded** digest (the one in force before the binding), so the log never contains the digest of the body it sits in. The current digest is always the Status line's; the chain of earlier ones is §16.4.
3. A binding is admissible only **before the earlier of** two events: any provider data being seen, including trial or sample data (§9.2); or **CP-6**, the F1 freeze. After provider data, any change is a re-opening under §13. After CP-6, any change to this spec, a binding included, **voids the freeze inventory for the feed component** and needs requalification. It is never absorbed as a binding ([checklist addendum §5](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#5-behavior-changing-findings-settle-before-the-final-freeze); the F1 freeze of this spec's digest is item A.1 of the later-binding rule, [note §3](../notes/2026-09-27-feed-provider-neutral-preparation.md#3-later-binding-rule--proposed-text-for-the-f1-packet), PROPOSED for acceptance at CP-6) (Codex review on #585).
4. **Every OPEN item must be bound before CP-6.** An item still OPEN at CP-6 is a hold that blocks the freeze (addendum §5).
5. Shadow collection may not start while any item is OPEN. This is in addition to §9.2–§9.4 and CP-7.
6. **Hashing.** The digest is computed over LF bytes. The file is pinned `text eol=lf` in `.gitattributes` so that a Windows checkout with `core.autocrlf=true` reproduces it. The digest is taken over the file with **line 3 only** removed: `sed '3d' <path> | sha256sum`. A checkout-independent equivalent is `git show <commit>:<path> | sed '3d' | sha256sum`, which reads the blob. **The digest is valid only if line 3 is the Status line and is the only line in the file starting `**Status:**`** (check: `grep -c '^\*\*Status:\*\*' <path>` returns 1, and `sed -n 3p <path>` starts with `**Status:**`). A body line starting `**Status:**` is therefore never silently excluded from the hash (Codex review on #585).

### 16.4 Binding log

| Date | Item | Value bound | Decision record | Frozen-body digest superseded by this binding |
|---|---|---|---|---|
| 2026-10-03 | OPEN-1 | §4.2 per-granularity rule (i)–(vi): exchange time else provider stamp, never receipt; close-stamped bars placed at interval start; straddling streams inadmissible; pre-emission busts/cancels excluded; executed trade prices only; ties by provider sequence; native 15-min bars as delivered after B.5. Rulings: (iii) exclusion and (iv) are within the exact constituent rule | Joshua, 2026-10-03T22:28:50Z, to coordinator (4): "bind Group 1 as recommended" (binding packet `docs/notes/2026-10-02-feed-spec-open-parameter-binding-packet.md`, blob `f6edd73`) | `a9b93a3679087cd9bda632c51e06a75e081d30ec4e4099aafa2dfe18e7cadad5` |
| 2026-10-03 | OPEN-5 | M4: verdict role on MNQ (ORB) only; ≤ 1 compared bar with V_A ≠ V_B (integer contracts), max difference reported; descriptive on 6J, MYM, MGC. Volume-use read: coordinator in-place yes/no read 2026-10-03 (§60) | Joshua, 2026-10-03T22:28:50Z, to coordinator (4): "bind Group 1 as recommended" (binding packet `docs/notes/2026-10-02-feed-spec-open-parameter-binding-packet.md`, blob `f6edd73`) | `b633a9ff939a6b2aef89e9ec3851864ef546858069d62c925570ee520cfff9ad` |
| 2026-10-03 | OPEN-6 | M7 raw-stream revisions: no verdict threshold; counted per symbol, labelled, reported privately; verdict only via M1–M4 and the forwarded limit 0 | Joshua, 2026-10-03T22:28:50Z, to coordinator (4): "bind Group 1 as recommended" (binding packet `docs/notes/2026-10-02-feed-spec-open-parameter-binding-packet.md`, blob `f6edd73`) | `693e752fca56196fc9e2c81743cde375da406d6ef0ffe7985eef12de07efbb33` |
| 2026-10-03 | OPEN-7 | M9: descriptive; no verdict role | Joshua, 2026-10-03T22:28:50Z, to coordinator (4): "bind Group 1 as recommended" (binding packet `docs/notes/2026-10-02-feed-spec-open-parameter-binding-packet.md`, blob `f6edd73`) | `04da52097205626e8c159c4a04a3e68e8812d02efd5bd5fc8134966b0eed9f6d` |
| 2026-10-03 | OPEN-9 | Re-application: once per provider after a FAIL, B items only, frozen before the next OPEN-8 window; a second FAIL ends that provider; all attempts reported | Joshua, 2026-10-03T22:28:50Z, to coordinator (4): "bind Group 1 as recommended" (binding packet `docs/notes/2026-10-02-feed-spec-open-parameter-binding-packet.md`, blob `f6edd73`) | `0b50554ac0301437d95d2640321c241b474378977739a231059fc71e92769b33` |
| 2026-10-03 | OPEN-2 | 6J canonical: electronic trading hours, back-adjustment off; §4.5 applies unchanged. Evidence: private read of `8ae083d0…`, a switch discontinuity at all 15 rolls (unadjusted) | Joshua, 2026-10-03T22:52:15Z, to coordinator (4): "go on open 2 and open 11" (coordinator (4) recommendation from its private panel read the same day) | `cc8f840990e116dc6db67c8004e51b286ff9edd657980480ff90f3135ee13635` |
| 2026-10-03 | OPEN-11 (MNQ, MYM, 6J) | MNQ N=3, MYM N=3, 6J N=1 CME business days before last trading day (holidays excluded), switch at the 18:00 ET open. MGC still OPEN | Joshua, 2026-10-03T22:52:15Z, to coordinator (4): "go on open 2 and open 11" (coordinator (4) recommendation from its private panel read the same day) | `ae94cd6bee9d6b2192182329d332d543c7f57ca0d79a778bbd56ebd0474d0d63` |
| 2026-10-04 | OPEN-11 (MGC) | MGC: cycle Feb/Apr/Jun/Aug/Dec (Oct skipped); switch at the 18:00 ET open of the session whose CME trade date is 1 CME business day before the expiring contract's first notice day | Joshua, 2026-10-04T00:17:19Z, to coordinator (4): "yes, bind MGC as stated" (the rule as stated in this row and in §16.2, put to him after the 2026-10-03 panel read and public-page check; supersedes reliance on the pre-check 22:52:15Z "go on open 11", per Codex review on #661) | `12b6c434a2a5146c16c0a568d9c242ae7facc1c388dfe2a8fee383224a7ecc05` |
| 2026-10-04 | OPEN-3 | Live contract = the OPEN-11 canonical contract for each session; one per-leg selection object shared by feed (R-MAP-2) and TB-V1. Venue check: Tradovate physical-delivery prohibition begins exactly at the 6J/MGC canonical switch day (zero margin); 16:45 ET daily flatten prevents carry | Joshua, 2026-10-04T00:17:19Z, to coordinator (4): "go on the proposal dispositions and open-3/4 as recommended" (binding packet `f6edd73` recommended text, with the coordinator's venue check) | `b24000200481b3b750280294ccd6f7eb3f9ca3066e2ab678bf0ffd9bd8f75b5b` |

### 16.5 Path

The path keeps the `-DRAFT` suffix. Renaming it would break the inbound links from the [H8 note](../notes/2026-09-27-feed-provider-neutral-preparation.md), the H8 card and the H5(b) card for no change in content. The Status line, not the filename, states the document's state.
