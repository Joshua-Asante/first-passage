# Feed: provider-neutral preparation for the four-leg book (H8)

**Status:** RETURNED FOR COORDINATOR REVIEW 2026-09-27. This is preparation only. It contains PROPOSED text for the F1 packet and owner decisions, and nothing in it is in force. The companion is the [draft TB-I5 successor specification](../spec/2026-09-27-cme-execution-feed-equivalence-test-DRAFT.md) (status DRAFT — NOT FROZEN).
**Assignment:** [handoff H8](../briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md#h8--feed-provider-neutral-preparation). **Sequencing owner:** [checklist addendum 2026-09-27](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-09-27--staged-acceptance-evidence-proportional-to-the-next-step) (Feed row; CP-6, CP-7; §1.4; §5). **Base:** `521d8f2`.
**Owners this note serves, not replaces (Rule 7):**
- the O-4 feed decision stays with the operator: [umbrella](../briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md) `:106` and the [S2b build ADR §2](../adr/2026-08-08-s2b-signal-daemon-build.md) Live CME bar source row `:48`;
- the D-feed gate is ruled in the [2026-09-22 addendum](../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#d-feed--tick-as-a-gate-not-a-provider);
- the F1 packet belongs to [T10](../briefs/handoffs/2026-09-21-tradeify-t10-source-and-freeze-packet.md), phase 2;
- A9-PREP belongs to the [Track A plan](../superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md#32-a9--production-feed-verification-record-and-funding-checkpoint-added-2026-09-11) (`:236`, unchecked). Its scope includes freezing "four-symbol mapping requirements". Note §2 and spec §5 are **inputs offered to A9-PREP**. A9-PREP (Track A) remains the owner that freezes the mapping requirements, and this preparation discharges no A9-PREP checkbox.

**Not granted:** provider selection, naming, pricing, contact, signup, subscription, credential staging or spend; any shadow collection; any change to `emit_enabled`, `dry_run`, the listener, arming or deployment; any order; any edit to an owner document. Accepting the later-binding rule is an operator act at CP-6. Funding is CP-7.

---

## 1. Gating state: why provider-specific work waits

**D-feed**, ruled 2026-09-22 ([addendum](../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#d-feed--tick-as-a-gate-not-a-provider) `:140`, adopted `:142`): "provider-specific work opens when **(a)** T00 returns a verdict other than INSUFFICIENT or NO-GO-evidence **and (b)** T10 phase 2 has assembled the F1 packet … no signup, subscription or credential staging before both conditions hold."

| Condition | State at `521d8f2` | Source |
|---|---|---|
| (a) T00 verdict ∉ {INSUFFICIENT, NO-GO-evidence} | **Not met.** The step-1 return was accepted as INSUFFICIENT on 2026-09-23. Step 1b (P7 closure) was authorized on 2026-09-24; no step-1b return is recorded at `521d8f2` (UNVERIFIED beyond that). The checklist still records "T00 INSUFFICIENT on P7(b)" | [STATE](../../STATE.md) `:58`; [checklist current state](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#current-state--september-26-2026-refreshed-from-the-acceptance-ledger) `:32`; [T00 P7 closure](../briefs/handoffs/2026-09-24-tradeify-t00-p7-closure.md) status `:5` *2026-10-01: still not met. Step 1 is now RESOLVED (P7 MET at `2baa516`), but (a) needs the step-3 screen's verdict, in practice GO-evidence, which needs step 2 ratified first.* |
| (b) T10 phase 2 has assembled the F1 packet | **Not met.** "Phase 2: pending" | [T10 packet](../briefs/handoffs/2026-09-21-tradeify-t10-source-and-freeze-packet.md) `:26–:28`, `:56` |

**Why the wait is correct, from the owners:**
- STATE's source disposition (`:32`) and the S2b §2 row (`:48`) allow provider-neutral preparation. Provider-specific implementation and spend wait until the fixed book clears every source-independent gate and the operator returns for the funding decision.
- The umbrella's O-4 row (`:106`) adds three conditions for funding: one provider clears the licensing, authentication and coverage facts; its adapter is ready for immediate validation; and a live-test window is booked. None of these can be true while the book's own feasibility is INSUFFICIENT.
- The addendum's circularity is **stated, not circular** (§1.4, `:447–:449`). D-feed (b) needs the F1 packet, and the F1 packet must bind the feed. It therefore carries the provider-neutral contract and a later-binding rule (§3 below) rather than a provider.
- A feed finding that would change intended behavior must reach its owner decision before CP-6 (addendum §5, `:499–:506`). That is why the roll and empty-interval questions below are raised now, provider-independently.

The next feed action after this note is **CP-7** (funding), reviewed against the D-feed conditions and this H8 packet (addendum §4, `:495`).

## 2. Four-leg symbol, roll and session mapping

Legs and symbols are verified from `ops/c1_rail/book_policy.py:172–:197` (`BOOK_LEGS`, D-B8 priority order) and match the rail spec's `LEG_MAP` table (`docs/spec/2026-09-12-c1-multi-leg-rail-extension-spec.md`, `521d8f2:…:160–:163`). The task's candidate "6J/M6J" resolves to **6J**: `MICRO_EQUIVALENT` counts 6J as 10 (`book_policy.py:132`), and the ledger records the micro-yen scale path as parked (`ops/instruments/6J.md:5`).

| Field | `aegis_6j` | `dj30_mym_p250` | `vanguard_mgc` | `orb_mnq_v7` |
|---|---|---|---|---|
| Root / book symbol | `6J` (`book_policy.py:180`) | `MYM` (`:184`) | `MGC` (`:189`) | `MNQ` (`:193`) |
| Rail `order_symbol` | `6J1!`: "provisional continuous-contract notation" (`book_policy.py:144`) | `MYM1!` | `MGC1!` | `MNQ1!` |
| Venue dated-contract binding | Absent by design; "TB-V1 supplies verified deployed bindings later" (`c1_sizing_host_reference.py:124–:133`) | same | same | same |
| Exchange / entitlement | CME (Track A plan `:175`) | **CBOT** (`:177`; `ops/instruments/MYM.md:3`) | COMEX (`:176`) | CME (`:178`) |
| Canonical panel | Step-3-accepted input: the attested 88-bar-prefix derivative `6J_M15-with-attested-prefix.csv` (private; 94,893 rows; digest `8ae083d0…`), which preserves every row of `core/data/bar_data/6J_M15.csv` (94,805 rows, from CME BAR EXPORT v0.2 `6J1!`, bar_data README `:8`) and adds 88 attested bars (Step 3 acceptance `:11–:12`; execution domain `:562–:566`, `:574`) | `MYM_M15.csv` from `MYM1!` (`:13`) | `MGC_M15.csv` from `MGC1!` (`:11`) | `MNQ_M15.csv` from `MNQ1!` (`:12`) |
| TV export symbol (manifest filenames) | `CME_6J1!` (`core/data/tv_exports/cme/SHA256SUMS`) | `CBOT_MINI_MYM1!` | `COMEX_MINI_MGC1!` | `CME_MINI_MNQ1!` |
| Tick (`mintick`) / point value, panel sidecar | 5e-7 / 12,500,000 (README `:8`); quoted USD per JPY (`6J.md:3`) | 1 / 0.5 (`:13`) | 0.1 / 10 (`:11`) | 0.25 / 2 (`:12`) |
| Sidecar `tz` (role UNVERIFIED; spec §4.1) | America/Chicago (`:8`) | America/Chicago (`:13`) | America/New_York (`:11`) | America/Chicago (`:12`) |
| Panel bar period | 15 min (M15; README `:3`) | 15 min | 15 min | 15 min |
| Panel back-adjustment | **UNVERIFIED / CONFLICTING.** `6J.md:3` says "`CME:6J1!` (back-adjusted continuous)". The Step 3 attestation of "back-adjustment off" names MGC/MYM/MNQ only and says "Earlier … 6J attestations remain in force" (`2026-09-15-packet1-step3-acceptance.md:17–:20`). The 6J attestation read in the execution-domain note covers the chart, harness and date window only ("only the date window changed", `2026-09-15-packet1-execution-domain.md:534–:538`), not back-adjustment | **Off** (Step 3 `:17–:20`) | **Off** (same) | **Off** (same) |
| Panel trading hours | **UNVERIFIED** (not in the Step 3 attestation, nor in the 6J attestation at execution domain `:534–:538`) | Electronic trading hours (Step 3 `:17–:20`) | same | same |
| Contract-month cycle | **UNVERIFIED** in repo sources read | Quarterly Mar/Jun/Sep/Dec, 3rd-Friday expiry (`ops/instruments/YM.md:31`, inherited by `MYM.md:90`); S2b option D requires `^MYM[HMUZ]\d$` (S2b ADR `:246`) | **UNVERIFIED** in repo sources read | **UNVERIFIED** as a contract spec. Measured: TV `1!` NQ/MNQ series show quarterly unadjusted gaps within ±4 days of 3rd-Friday expiry (`lab/analysis/_inbox/ict_mnq_2026-08/RESULTS.md:145–:147`) |
| Canonical `1!` roll rule | **UNVERIFIED.** No primary source for the charting platform's roll rule is in the repo; `MNQ.md:96` asserts that a volume-lead roll is "the TV-`1!` analogue" (a claim, not a primary read). D13(b) accepts the continuous basis with a stated seam limitation (campaign record `:191`) | same | same | same |
| Live contract-selection rule | **OWED** (spec R-MAP-1); must agree with the TB-V1 venue binding | same | same | same |
| Product session | Sunday–Friday 18:00–17:00 ET, daily break from 17:00 ET (Step 4 `:35–:36`) | same | same | same |
| Holiday / early close | `ops/calendars/` ratified forward rows (Step 4 `:9–:14`), coverage to 2026-09-30 21:00Z (`:64–:67`); D19 is date membership only (`ops/calendars/README.md`). Observed 2026-09-07 halt 17:00 ET (Step 4 `:37–:38`) | halt 13:00 ET observed 2026-09-07 (Step 4 `:37–:38`) | 14:30 ET (same) | 13:00 ET (same) |
| DST | Consumer carries UTC instants; DST gap/fold wall times refused (Step 4 `:53–:54`); schedule in America/New_York (halt/resume §5) | same | same | same |
| Holiday-sensitive strategy behavior | The Aegis prototype has an `early_close_dates` input (2022–2027 defaults) that "does not update itself" (`6J.md:81`). Whether the accepted Aegis body uses it is **UNVERIFIED** (private ports and Pine not read, per AGENTS.md) | — | Post-holiday no-trade latch on the platform's daily key, kept as captured; "parity depends on it" (umbrella `:111`, O-8) | The accepted ORB Pine body: "Early-close dates end the session earlier through the same rule" (`8c15f18:docs/notes/2026-09-26-orb-lifecycle-evidence.md:22`). Whether the runtime port does the same is not stated there (`:23`) |
| Volume read by the strategy | **UNVERIFIED** | **UNVERIFIED** | **UNVERIFIED** | **Yes:** the ORB entry is placed "if the day and volume filters pass" (`8c15f18:docs/notes/2026-09-26-orb-lifecycle-evidence.md:22`); the port "if its filters pass" (`:23`) |
| Provider-native code | Provider-specific: funding-decision question (§5) | same | same | same |

**Consequences for the spec** (carried as OWED items, not rules):
- The canonical roll rule and the live contract-selection rule are both unestablished. Comparing across mismatched roll rules is known noise (Q-DATAFIDELITY-1 `:18`), so the spec proposes a roll-exclusion band and requires a frozen live rule (R-MAP-1).
- ORB reads volume, so volume equivalence has a verdict role to set (spec M4), against a canonical side whose re-captures are not volume-stable (Step 3 `:31–:35`).
- The 6J back-adjustment conflict must be resolved from the operator's attestation before freeze. A back-adjusted Side B against an unadjusted live feed would fail M3 away from every seam.

## 3. Later-binding rule — PROPOSED text for the F1 packet

The addendum §1.4 (`:447–:449`) requires this rule to be accepted with the F1 packet. T15 permits final provider-funded binding "only under explicit accepted later-binding rules" (checklist `:288`). T10 phase 2 enumerates permitted later bindings (T10 packet `:27`). The text below is proposed for T10 phase 2 to carry into the packet. Acceptance is the operator's, at CP-6.

> **Feed later-binding rule (PROPOSED).**
>
> **A. Frozen at F1** (part of the freeze inventory; a change after CP-6 voids the freeze inventory for the feed component, per addendum §5):
> 1. the feed-equivalence specification at its frozen digest: metrics, thresholds, window rule, roll-exclusion band, empty-interval rule and verdict rule;
> 2. the consumer contract at the frozen head:
>    - `Bar` fields and validation (`feed.py`, `book_validation.py`);
>    - `BAR_PERIOD` 15 min and `BAR_SLACK` 30 s (`book_protocol.py`);
>    - the bar-open UTC timestamp convention, session-bounded contiguity, the four-leg barrier, the silence and barrier timeouts, and conflict and stale-bar halts (`book_runtime.py`, `book_evaluate_loop.py`, `book_account_owner.py`);
>    - fail-closed emission (S2b §2);
>    - no resume on source recovery (halt/resume §2; rail §5);
> 3. the 15-minute construction rule, for each delivery granularity the contract admits;
> 4. per leg: root, exchange, the live dated-contract selection rule, and the calendar source and ratification procedure;
> 5. the source-identity field set that PASS writes into the B7 execution fingerprint (umbrella `:637–:638`, `:644`).
>
> **B. May be bound after F1 for the funded provider, without requalifying the book**, only if every item in C holds:
> 1. provider identity, endpoints, protocol and client library (pinned by hash);
> 2. authentication mechanism and **credential references** (never values; secrets outside versioned configuration);
> 3. entitlement records;
> 4. provider-native symbol codes mapped under A.4;
> 5. the translation of the provider's timestamp convention into A.2;
> 6. transport reconnect and backoff parameters inside the A.2 timing bounds;
> 7. the adapter module implementing the frozen `BarSource` contract.
>
> **C. Conditions on every B binding:**
> 1. the unchanged frozen consumer tests pass on the adapter;
> 2. the frozen equivalence test PASSES for all four symbols on that exact source-identity configuration;
> 3. the configuration digest enters the B7 execution fingerprint before any live test;
> 4. emission stays disabled until its own gates (M1, D-B15 emit GO and the arming rules) are met.
>
> **D. Triggers requalification, or a void freeze for the feed component; never absorbed as a binding:**
> - any change to what the adapters see: bar period, timestamp meaning, aggregation or empty-interval rule, session or calendar semantics, roll or contract-selection rule, price adjustment;
> - any change to consumer timing or fail-closed behavior;
> - any tolerance, window or verdict change;
> - a provider that can meet the contract only with a carve-out;
> - a feed finding that changes intended strategy behavior. Before CP-6 it goes to its owner decision (a pre-registered change with requalification, an explicit accepted binding, or a hold); after CP-6 it voids the freeze inventory for the component (addendum §5).
>
> **E. Re-binding (PROPOSED; the umbrella supplies no finality clause, `:644`):**
> - a FAIL is final for that source identity and configuration digest;
> - a different provider or a changed B item is a new binding that must meet C in full. It inherits no earlier PASS;
> - every attempt is counted and reported per provider, and a re-application follows the spec §10 re-application rule. Whether a change to B items only may re-apply after a FAIL is an operator rule, OWED.

## 4. Shadow-collection design (emission disabled)

**When:** only after CP-7 authorizes a provider and its adapter (addendum §4, `:495`), and after the equivalence spec is frozen (spec §9). This section is a design, not an authorization.

**Topology (proposed).**
- **Stage S-1: record-only collector.** A process that holds the provider connection and appends every delivered message's original bytes, with receipt wall-clock and monotonic time, to a private append-only store. It parses into `Bar` through the candidate adapter and writes the built 15-minute bars, the per-leg delivery times and the health transitions beside the raw bytes. It constructs no `ListenerClient`, holds no listener URL or path token, and imports no B1 payload builder.
- **Stage S-2: offline consumer replay.** After the window closes, the recorded bars are driven through `FourLegEvaluateLoop` with a synthetic broker in a test harness. That loop "deliberately has no config constructor, HTTP endpoint, sender, or daemon CLI registration" (`book_evaluate_loop.py:1–:5`). The replay observes which recorded deliveries would have halted the book (M5–M8), and produces M9 decision identity against the fresh canonical capture.

**How emission stays disabled (layered; each layer exists today and is cited):**
1. **No sender in the path.** S-1 has no listener client. S-2 uses the book loop, which has no sender.
2. **Daemon config.** If the collector is ever co-hosted with the signal daemon, `emit_enabled=false` stays in its config. The operative gate is the M1 coordinator, not a constructor literal:
   - `build_loop` always passes an `M1Coordinator` (`ops/c1_signal_daemon/daemon.py:88`, `:94–:95`), and the evaluate loop then reads `coordinator.effective_emit`, ignoring its own `emit_enabled` argument (`evaluate_loop.py:100`). It suppresses with `emit_disabled` before any payload is built (`:100–:105`);
   - `effective_emit` starts False (`m1_stage1.py:21`), is reset to False before every poll (`:31`), and becomes True (`:49`) only when `active_ceremony` finds an active ceremony. That requires the config's `emit_enabled` to be True (`m1_stage1_control.py:118`), and `load_config` refuses `emit_enabled=true` without a complete M1 ceremony configuration (`daemon.py:61–:76`);
   - the `emit_enabled=False` literal at `daemon.py:94` and the boot log line at `:129` are fixed text. They are not evidence of the effective state and are not counted as layers.
3. **Listener.** It stays `dry_run=true` with no arm (AGENTS.md live-execution posture). Arming needs M1 plus a separate operator GO, which this design does not touch.
4. **Account separation.**
   - The feed account is never linked to the broker bridge.
   - No order endpoint is implemented.
   - Credentials are operator-staged, volume-only and excluded from logs and images (Track A plan readiness checkpoint 5, `:212`).
   - If a provider's credential is order-capable, that is a funding-decision fact (§5 Q3), not something application code can fix (Track A plan `:193`).
5. **No agent order.** No agent places, amends or cancels an order (AGENTS.md).

**Emission-disabled evidence to retain** (following the A6 precedent in the Track A plan `:234`):
- health reads showing `emit_enabled=false` and `effective_emit=false` at start, at intervals and at end;
- the listener ledger sequence unchanged across the window;
- the collector's import closure, showing no listener client or B1 builder;
- the absence of any broker-bridge linkage for the feed account.

**What the collection must record:** spec §12, items 1–10.

**Prerequisites before collection starts:**
- ratified calendar rows covering the window (spec R-MAP-3);
- the frozen spec;
- the live contract-selection rule;
- a booked window with an owner (Track A plan readiness checkpoint 6, `:213`).

## 5. Provider-specific facts that become funding-decision questions

These cannot be answered provider-neutrally. Per the H8 stop condition, each is recorded as a question for CP-7 rather than guessed. Q1–Q6 restate the Track A plan's six written questions (`:195–:202`) in provider-neutral form; Q7 onward are added by this preparation.

| # | Question | Why the equivalence test or consumer needs it |
|---|---|---|
| Q1 | Licensing: may a non-professional subscriber consume real-time data for all four symbols from a headless service for internal automated decisions (non-display use)? | Without it, no admissible Side A exists |
| Q2a | Coverage and entitlement: CME (6J, MNQ), CBOT (MYM) and COMEX (MGC) real-time | Book PASS needs all four symbols |
| Q2b | Cost and capital terms: all-in monthly cost, minimum balance, deposits, inactivity and withdrawal terms. Whether a refundable deposit counts against the $700 ceiling is an operator reading taken when D-feed (a) and (b) hold (D-feed wording `:140`) | The funding decision (CP-7); not an equivalence input |
| Q3 | Credential scope: is there a technically enforced data-only credential, or can order permission be disabled at the account level? | Emission and account separation (§4, layer 4) |
| Q4 | Delivery granularity: completed bars, or trades only? Exchange timestamps? Is the bar stamp at open or close, and in which zone? | Spec §4.1–§4.2 construction and translation |
| Q5 | Unattended authentication and renewal for weeks with no UI, MFA or desktop gateway; session and connection caps across four symbols | M6 silence; reconnect handling |
| Q6 | Cloud or VPS use, and local persistence of original bytes and derived bars for private audit retention | Spec §11: raw bytes retained privately |
| Q7 | Correction, backfill and replay semantics after reconnect: are revisions flagged, and are sequence identifiers provided? | M7; the correction rule |
| Q8 | Empty-interval behavior: does the provider emit bars for no-trade intervals? | Spec §4.3 |
| Q9 | Symbology: dated-contract codes, continuous-symbol availability and roll conventions | R-MAP-1, R-MAP-2 |
| Q10 | Delivery latency after bar close, and maintenance windows during the 18:00–17:00 ET session | M5 hard bound of 30 s after close |
| Q11 | Historical depth and cost, for the optional arm H | Spec §3 |
| Q12 | DST and early-close handling in the provider's session model | Spec §7 |

Answers are operator-verified at the provider's own terms or UI, per the Track A plan's "primary signup verification" (`:210`). The existing rule (`:204`) rejects "any answer that leaves licensing, all-four-symbol coverage, unattended authentication, or the ability to disable order actions ambiguous". That covers Q1, Q2a, Q3 and Q5. An ambiguous Q2b is not a disqualification under that rule; it is an input to the funding decision.

## 6. Operator decisions this preparation returns (none is taken here)

1. **Freeze the equivalence spec** before any provider data. The OWED values are the spec §9.1 list:
   - the §3 arm C rule (compared fields, units, tolerance, and 6J prefix treatment);
   - the §4.2 constituent rules;
   - the §4.3 empty-interval rule;
   - the §4.5 6J adjustment basis;
   - R-MAP-1: the live contract-selection rule and the roll-exclusion band;
   - the M1–M9 thresholds and roles, including M3a's default-or-relaxed choice, M4's role and threshold, and M7's raw-revision threshold;
   - the window rule;
   - the §10 re-application rule;
   - the §13 re-opening vehicle.
2. **Live contract-selection (roll) rule** per leg, and whether it must match the canonical `1!` roll. If the two differ in what the adapters see, the finding goes to its owner decision before CP-6 (addendum §5).
3. **6J panel settings:** resolve the back-adjustment conflict and confirm trading hours from the retained 6J attestation.
4. **Empty-interval rule:** classify the existing private gap queue (`calendar-gap-queue.json`, digest `509346d6…`, execution domain `:502`) against the consumer's contiguity rule, including the 171 residual regular-session gaps (`:689–:691`), then decide the rule. The canonical representation is already established: absent slots are omitted and there are no zero-volume rows (`:262–:274`). If the rule conflicts with the consumer's contiguity and barrier rules, the consumer owner (TB-I3) decides.
5. **Volume tolerance (M4):** set M4's verdict role and threshold. ORB reads volume, and the canonical re-captures of 2026-09-15 differed in volume from the retained original generation on eight rows (6J, MGC, MNQ) while prices agreed (Step 3 `:31–:35`). The tolerance must be set without provider data.
6. **Later-binding rule (§3):** carry it into the T10 phase-2 F1 packet for acceptance at CP-6.
7. **At CP-7:** answers to Q1–Q12 (Q2 split into Q2a and Q2b) for any candidate; the funding decision; the window booking.

## 7. Verification of this note

Commands actually run in this session (read-only, on a working tree shared with concurrent agents; no suite or gate run):
- `git log --oneline -1` → `521d8f2d`.
- `sed -n` / `grep -n` reads of:
  - the H8 card and handoff header;
  - the checklist addendum §0–§5 and T10/T14/T15;
  - STATE `:1–:66`;
  - S2b ADR §2 and the 2026-09-10/11 addenda;
  - umbrella O-4, O-8, TB-I5, TB-S3 (A), TB-B7/TB-E2;
  - the D-feed disposition;
  - the T10 packet and the T00 P7 closure;
  - Track A plan §3.2;
  - the locked template;
  - the bar_data and tv_exports READMEs and both manifests (names only);
  - the four instrument ledgers and YM.md;
  - Packet 1 Step 3/Step 4 and execution-domain notes;
  - `ops/calendars/README.md`;
  - `book_policy.py`, `c1_sizing_host_reference.py`, `feed.py`, `book_protocol.py`, `book_validation.py`, `book_runtime.py`, `book_evaluate_loop.py`, `book_account_owner.py`, `daemon.py`, `evaluate_loop.py`, `book_session_calendar.py`.
- `git show 521d8f2:<path> | grep -n` for the three concurrently edited specs (rail, replay, halt/resume).
- `git show 8c15f18:<path> | grep -n -i "feed\|provider\|roll\|DST\|market data"` over the #519 notes and cards (first pass). This reported no market-data finding, which was wrong: see the review round and spec §0. Campaign §59 Ruling 7 read at `:3985–:4010`.
- `grep -rn -i "back-adjust"` across `docs ops core lab` (the 6J conflict above).
- `python3 scripts/check_md_relative_links.py --strict --glob <file>` on both H8 files → 23 and 13 targets, 0 unresolved. A local heading-slug check of every `#anchor` in both files → 0 unresolved.
- `python3 scripts/check_handoff_authority.py --all` → 2 cards with an authority block, 0 violations.
- `grep -n -i` for provider names and prices over both files → none. The only dollar figure is the standing $700 spend ceiling (AGENTS.md).

- Review round: re-reads of every cited line (listed in spec §15). The seven-path grep `git show 8c15f18:<path> | grep -n -i -E "feed|provider|market.data|volume|roll|DST|bar source|BarSource"` is tabulated in spec §0. After the fixes, `check_md_relative_links.py --strict` → 25 and 13 targets, 0 unresolved, and `check_handoff_authority.py --all` → 2 cards, 0 violations.

Not run: the full gate suite (excluded by the task), any data comparison (the data is absent from this checkout), any provider or network contact.

## Review and fix round (2026-09-27)

The review list reused ids R1–R10, so its two batches are labelled **A** (the first thirteen findings) and **B** (the second ten). Every finding was checked against its cited lines before it was applied.

| Id | Outcome | What changed / why |
|---|---|---|
| A-R1 | Applied | Spec §4.3 and §14.1 now cite execution domain `:262–:274`, `:485–:489`, `:502`, `:689–:691` and amendment `:48–:52`: panels omit absent slots and have no zero-volume rows. Only the residual 171 gaps remain UNVERIFIED. Decision 4 (§6) now classifies the existing gap queue. The executor's return ("concern 2") is not a file this fixer owns; this section supersedes it |
| A-R2 | Applied | Arm C is defined over existence and `(bar_open_utc, O, H, L, C)` in integer ticks; volume is descriptive unless a volume role is frozen. The "same-day captures" wording is corrected to the 2026-09-15 re-captures versus the retained original generation (Step 3 `:31–:35`) |
| A-R3 | Applied | M3a now defaults to 0, with ≤ 0.5% as a relaxed option. The basis states that template `:66–:67` require exact or consistently rounded matches and that `:69` is a rejection trigger. The §0 template row is corrected to match |
| A-R4 | Applied | Q-DATAFIDELITY-1 `:17` → `:18` in spec §0, R-MAP-1 and note §2 (`sed -n 17p` is blank; `:18` holds the Q-TVCOV-1 quote) |
| A-R5 | Applied | Spec §0 and §13 quote template `:81` verbatim ("a separate ADR justifying why prior thresholds were misspecified …"). The draft proposes the same vehicle, and a lighter one would be an operator-adopted departure (§9.1) |
| A-R6 | Applied | The window proposal now requires two Sunday opens, two Friday closes and one month-end-adjacent session, matching template `:42` |
| A-R7 | Applied | Spec §8 now states that an overtaking leg halts the book (`bar-sequence`, `book_runtime.py:377–:381`), and M8 counts it (PROPOSED) |
| A-R8 | Applied | Note §4 layer 2 now names the operative chain: `M1Coordinator.effective_emit` (`m1_stage1.py:21`, `:31`, `:49`), `active_ceremony` requiring config `emit_enabled` True (`m1_stage1_control.py:118`), `load_config` (`daemon.py:61–:76`) and `evaluate_loop.py:100`. The `:94` literal and the `:129` log line are demoted as fixed text |
| A-R9 | Applied | Spec §11 is split into a public note (digests and verdict labels, umbrella `:234`) and a private evidence record (counts, host identity, clock evidence and the rest). Whether any field moves public is OWED |
| A-R10 | Applied | 6J's canonical input is the Step-3-accepted derivative (digest `8ae083d0…`; Step 3 `:11–:12`; execution domain `:562–:566`, `:574`). Arm C states its prefix treatment (PROPOSED). The 6J attestation (`:534–:538`) is cited as covering chart, harness and window only, so adjustment and hours stay UNVERIFIED |
| A-R11 | Applied | The row is renamed "Sidecar `tz`" and its role marked UNVERIFIED. Spec §4.1 cites `bar_export_loader.py:47`, `:56`, `:107` for what the decoder does with `tz`, without claiming the panel consumer's use |
| A-R12 | Applied | `6J.md:81` moves to the holiday-sensitive-behavior row for `aegis_6j`; whether the accepted Aegis body uses `early_close_dates` is UNVERIFIED |
| A-R13 | Applied | Spec §0 lists the seven `8c15f18` paths, the grep pattern and a per-file result |
| B-R1 | Applied | M4's verdict role and threshold are OWED, citing `8c15f18:docs/notes/2026-09-26-orb-lifecycle-evidence.md:22` (ORB "day and volume filters"). §14.4 is narrowed to legs other than ORB. The "no feed finding" statements in spec §0 and §15 and note §7 are corrected. Decision 5 (volume tolerance) is added. The same `:22` line also shows the ORB Pine uses early-close dates; that is added to the holiday-behavior row |
| B-R2 | Applied | Arm C fields, units and a PROPOSED 0 tolerance are stated. Arm C is in the §9.1 freeze list and decision 1, the re-capture differences are cited, and achievability is §14 item 8 |
| B-R3 | Applied | Spec §10 separates the umbrella quote (`:644`, no finality clause) from a PROPOSED re-application rule: attempt counting, a pre-declared and frozen change and window, and an OWED operator rule on re-applying after a B-item-only change. Note §3 E is relabelled PROPOSED to match |
| B-R4 | Applied | Same changes as A-R5 and A-R6 |
| B-R5 | Applied | The M1 basis is restated: a missing bar on either side halts; an extra Side-A bar is an equivalence difference whose effect depends on §4.3. The §8 wording is fixed as in A-R7 |
| B-R6 | Applied | Q2 is split into Q2a (coverage/entitlement) and Q2b (cost and capital terms). The `:204` disqualification is quoted verbatim and applied to Q1, Q2a, Q3 and Q5 only |
| B-R7 | Applied | MYM CBOT is cited as `:177` and MGC COMEX as `:176` (verified against Track A plan `:175–:178`) |
| B-R8 | Applied | The header states that note §2 and spec §5 are inputs to A9-PREP, which stays the owner (`:236`, unchecked); no A9-PREP checkbox is discharged |
| B-R9 | Applied | Spec §9.1 and note §6 decision 1 now carry the same enumerated OWED list, including the §4.2 constituent rules and the M7 raw-revision threshold |
| B-R10 | Applied | Condition (a) now reads: authorized 2026-09-24 (closure `:5`); no step-1b return recorded at `521d8f2` (UNVERIFIED beyond that) |

No finding was rejected. No owner document was edited.

---

## Coordinator acceptance (2026-09-27)

**ACCEPTED**, together with the [draft TB-I5 successor spec](../spec/2026-09-27-cme-execution-feed-equivalence-test-DRAFT.md). The spec stays **DRAFT — NOT FROZEN**, and every OWED value remains the operator's to freeze before any data is seen. Reviewer: the coordinating session. The artifact was the executor draft plus the fix round, which applied all 23 findings of two refute-first reviews. The coordinator read §1–§3 and §6 of this note, and spec §4.3, §6 (M1, M8), §7 and §14.

- **Missing owner (cross-handoff critic X-05): assigned as [H8 step (b)](../briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md#h8--feed-provider-neutral-preparation).** Decision 4 needs a classification of the private gap queue (`calendar-gap-queue.json`, digest `509346d6…`), including the 171 residual regular-session gaps, against the consumer's contiguity and four-leg barrier rules. The queue is private, so the step runs on the operator's machine, as a documentary read with no data committed. It returns before CP-6. If an omitted in-session slot would halt the book, the result goes to TB-I3 (consumer owner) and to the halt/resume owner. That second route matters because such a halt interacts with the §A11.2 incident rule applied by H5: whether a feed-gap halt is an incident that ends the session.
- **One spend-scope question (critic X-13).** Q2b (whether feed deposits or fees count against the $700 ceiling) is folded into the commissioning packet's single CP-2 question F-4.
- **Later-binding rule (§3):** carried into T10 phase 2 as proposed text. It is accepted only at CP-6.

**Not granted:** unchanged from the Status line. No provider, contact, spend, collection or emission change.
