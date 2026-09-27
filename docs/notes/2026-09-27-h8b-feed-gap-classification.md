# Feed gap queue classified against the four-leg consumer (H8 step (b))

**Status:** RETURNED FOR OPERATOR/COORDINATOR REVIEW 2026-09-27, revised the same day after operator review (§8). Documentary classification only. It adopts no empty-interval rule, and it edits no owner text. The §4.3 rule stays the operator's to set before freeze.
**Assignment:** [handoff H8 step (b)](../briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md#h8--feed-provider-neutral-preparation), which grew out of the coordinator's acceptance of [H8 step (a)](2026-09-27-feed-provider-neutral-preparation.md#coordinator-acceptance-2026-09-27), decision 4. **Base:** `875ecf2` (main after #520).
**Where it ran:** the operator's machine. The private inputs were read in place in the primary checkout. The scripts, their complete outputs and a hash manifest are private and uncommitted (§2). This note gives only counts, classes and digests. It contains no timestamps, prices or volumes from the panels.

## 1. Answer

**One affected permitted session was observed.** In the examined permitted sessions of the common window (§4.3), one six-slot omission was found on one leg, and no other omission. Every other queue interval falls outside a permitted session: the daily break, a weekend, or an account day the calendar practice denies as HOLIDAY/SHORTENED.

- **The 171 residual gaps:** 170 fall on account days that the holiday calendar lists with an early close or closure. **One** falls in a regular permitted session: 6 consecutive MGC slots in the middle of the day, in 2026, while the other three legs have every slot.
- **Cause of the omission: not established.** The bar before the gap is thin and the bar after it carries a volume burst. That is compatible with several causes and settles none of them (Q-2).
- **What was not established:** these panels do not show that no-trade intervals never occur. They show only that none was observed in the examined sessions of one charting platform's series. One historical gap is not a forecast of live-feed reliability.
- **Consumer effect:** an omitted in-session slot on one leg halts the book. The conditions and the halt reason are stated in §5, from the code and a synthetic trace; the historical panels carry no live arrival timing. This result is routed to **TB-I3** (consumer owner) and the **halt/resume owner** (§6).

## 2. Inputs and private artifacts (SHA-256)

Inputs, read in place:

| Input | SHA-256 | Check |
|---|---|---|
| `calendar-gap-queue.json` (the pinned queue) | `509346d604999baf270a26091727883e1ca583bf03e504028a6654eb86b35328` | matches the pin at [execution domain](2026-09-15-packet1-execution-domain.md) `:502` |
| `regular-session-gap-screen.json` (the 171 screen) | `54d6e96d3664ca3af972c43cae2651d9f29503099e30e52161262d11ddacaf24` | bound in the private `step3-evidence-index-v3.json`; reproduces 27 / 46 / 49 / 49 = 171 residual and 3,972 regular-only intervals (`:689–:691`) |
| `6J_M15.csv` | `94d237cca3290cd9066d04d921ddeec1a3af941fff11dba8c7efd6c2c32a54bc` | equals the queue's `panel_sha256` |
| `MGC_M15.csv` | `c5487470a5a9c8c69303587e5a598f9c66eb28d614695d7d78a4aee918fa6aad` | same |
| `MYM_M15.csv` | `15b34615ef7793ad73d08691713e2f386e2eb05debea5169a58ede1ff4a6b156` | same |
| `MNQ_M15.csv` | `cceaac41a9b5029676cbc36f4d2be7e975723a7aa00610e86f63d7980eb27fc8` | same |
| `6J_M15-with-attested-prefix.csv` (the screen's 6J input) | `8ae083d07b6870aa427dc69009434da0f3cab2d6818ca356e441ad40f3648fd2` | matches execution domain `:574` |
| `ops/calendars/cme_holiday_calendar_2022_2026.json` | `2698f2688cce582b08df58516fd770fa4a71a18de04870d9c14511731ea181e9` | identical to `main` |

Private artifacts (uncommitted; each script asserts every input digest before it reads):

| Artifact | SHA-256 |
|---|---|
| `classify_gaps.py` (classifier) | `18717cd2b634da576b821f951fd3c4bc476d035b4bb4c15ce0c3d5ff6a7ece67` |
| `h8b-classification-summary.json` | `63b1cda3f2e92ae47b09e72c0010cf89a843fab943800d02ef5ebb47d7424267` |
| `h8b-interval-detail.json` | `8c49ff904b6297edd1fc6a40cde43add98ab8879ad2ed52fa67a59ad3932b069` |
| `reconcile_sessions.py` (denominator and panel-only cross-check) | `8b986929b9df00592ea595ffee9acab40609d279ed47a0c2945b2ee70ca60d46` |
| `h8b-denominator-reconciliation.json` | `edc0ff33ec75aca7c1e6ff8ef6211e092b54b44c6d76abc0ea306fd2c93b66c2` |
| `trace_omitted_slot.py` (synthetic trace, §5) | `5ac0fdee9a6951750d0b5d5b21f18ac0c9d5a99248e6ac8dce60e763f2862669` |
| `MANIFEST.json` (hashes, sizes, invocations, interpreters) | `8d27f698f53e656b52d7d8a891d28c9a8db788448d4101a83d5281610e7b51d2` |

**Retention: DONE 2026-09-27.** The operator copied the artifacts to the ignored private directory `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/inputs/private_overrides/op1/2026-09-14-seven/h8b-gap-classification/`, a sibling of `step3-coverage/`. Every file was then checked against `MANIFEST.json` for hash and size. The session's worktree-isolation hook refuses writes to the primary checkout, so the copy was the operator's act.

## 3. Classification rules (read at `875ecf2`, not inferred)

A gap slot is a 15-minute bar-open with no row in a leg's panel. Each slot gets one class. An interval takes its most severe slot class.

| Class | Rule | Consumer basis |
|---|---|---|
| `OUT_DAILY_BREAK` | bar-open in [17:00, 18:00) ET | The account day runs from 18:00 ET on the prior day to 17:00 ET (`scripts/author_book_session_calendar.py:53–:54`, `:155–:156`; enforced at `ops/c1_rail/book_session_calendar.py:302–:306`). A bar outside the bound session halts (`book_runtime.py:352`), so these slots must stay empty |
| `OUT_WEEKEND` | account date is a Saturday or Sunday | No account-day row exists |
| `DENIED_HOLIDAY_OR_SHORTENED` | account date is a calendar entry with any product group not `NORMAL` (65 dates) | HOLIDAY/SHORTENED rows are DENIED (`book_session_calendar.py:308`). `session_for` then returns no `BookSession` (`:236–:238`), so no barrier runs. Date membership only, under D19; the file's trade-date basis equals the account date used here |
| `HOLIDAY_ADJACENT` | the next weekday after such a date (50 dates) | Denied only if the forward UNCERTAIN_ADJACENT practice is applied (`author_book_session_calendar.py:21`). Counted separately |
| `IN_PERMITTED_SESSION` | anything else | Every slot is a required boundary for all four legs (§5) |

## 4. Results

### 4.1 Queue intervals (4,142) by class

| Leg | Intervals | Out of session only | Denied holiday/shortened | Holiday-adjacent | In permitted session |
|---|---:|---:|---:|---:|---:|
| 6J | 1,035 | 1,008 | 27 | 0 | 0 |
| MGC | 1,035 | 989 | 45 | 0 | **1** |
| MYM | 1,036 | 987 | 49 | 0 | 0 |
| MNQ | 1,036 | 987 | 49 | 0 | 0 |

Absent slots: 6J has 5,848 in the daily break, 38,456 on weekends and 1,248 on denied days. The other three legs have 5,852 in the break and 38,456 on weekends. On denied days MGC has 1,518, MYM 1,642 and MNQ 1,638. MGC also has 6 in a permitted session. 6J shows four fewer break slots because its panel starts 23 hours later. No panel has a bar in the break or on a weekend.

### 4.2 The 171 residual gaps (screen `:689–:691`)

| Leg | Residual | Denied holiday/shortened | In permitted session |
|---|---:|---:|---:|
| 6J (attested derivative) | 27 | 27 | 0 |
| MGC | 46 | 45 | **1** |
| MYM | 49 | 49 | 0 |
| MNQ | 49 | 49 | 0 |

All 3,972 of the screen's regular-only intervals reclassify as out of session only.

### 4.3 Book level and the denominator

**Common observation window:** bar-opens from `2022-09-01T23:00Z` to `2026-09-03T00:00Z`, both inclusive. The window starts at the latest first bar across the four queue panels (the 6J start) and ends at the earliest last bar (shared by all four).

**Reconciliation of the two session counts.** The two methods count different sets:
- **Set A (classifier):** 954 account dates. These are permitted account dates with at least one slot in the window; holiday and holiday-adjacent dates are excluded.
- **Set B (cross-check):** 993 account dates. These are non-holiday weekday account dates whose whole session lies in the window, so holiday-adjacent dates are included.

The two sets reconcile exactly:

| Step | Account dates |
|---|---:|
| A | 954 |
| minus the 2 partially observed edge sessions in A but not in B | −2 |
| plus the 41 holiday-adjacent sessions in B but not in A | +41 |
| **B** | **993** |

- The first edge session opens at 18:00 ET, before the window starts. The last closes after the window ends.
- All 41 dates in B but not in A are holiday-adjacent.
- The weekday account dates touched by the window also close: 954 permitted + 50 holiday + 41 holiday-adjacent = 1,045.

**Observed:**
- Examined permitted sessions: 952 fully observed, plus 2 partially observed. One of them had an omitted leg slot: 6 distinct slots, one leg, mid-session, not at the 18:00 ET open.
- Holiday-adjacent sessions: 41 fully observed, none with an omitted slot.

**Independent cross-check.** A second pass walked every slot of every session in set B directly from the four panels, without using the queue. It required all four legs at every slot, including 18:00 ET. It found the same single session, the same 6 slots and the same leg.

This note gives a count, not a rate. One observed event does not support a per-session probability for a live feed.

## 5. Consumer effect of an omitted in-session slot (conditions, with a synthetic trace)

Only the evaluate loop and the runtime decide which halt fires, and when. The historical panels do not.

**The rules, from code at `875ecf2`:**
- **Barrier expiry.** A partial barrier is expired only when `expire_barrier` is called and `now > bar_open + 15 min + 30 s`, strictly (`book_runtime.py:483`). The halt it records is `barrier-expired` (`book_account_owner.py:924`). `FourLegEvaluateLoop.step` calls the expiry before and after polling (`book_evaluate_loop.py:35–:36`, `:56–:57`).
- **Silence.** Each step first runs `check_source_silence` with `max_silence = 2 × 15 min + 30 s` (`book_evaluate_loop.py:33`). It is anchored on the latest **completed** barrier's bar-open (`book_account_owner.py:859–:865`). When one leg omits boundary b(k), this threshold, b(k−1) + 30 m 30 s, equals b(k)'s expiry threshold, b(k) + 15 m 30 s.
- **Overtaking.** A later boundary that reaches `on_completed_bar` while the previous one is still pending halts with `bar-sequence` (`book_runtime.py:377–:381`).
- **Late bars.** A bar handled after `bar_open + 15 min + 30 s` halts with `invalid-bar-time` (`book_runtime.py:350–:353`).

**Synthetic trace.** The script `trace_omitted_slot.py` (private, §2) used the real `FourLegEvaluateLoop`, `FourLegRuntime` and `BookAccountOwner`, with the fixtures of `tests/ops/test_four_leg_runtime.py`. MGC omitted 1 or 6 boundaries from b2, while the other three legs delivered 2 s or 25 s after each bar closed. The run gave 17 passed, launcher record `.cache/fp-verification/20260927T160215Z-961e06721108/record.json`, with `status: completed`, exit 0 and a stable source.

| Driver | First incident | Then | Time |
|---|---|---|---|
| Loop stepped every 5, 15 or 29 s | `feed-silence` (reason `feed`), anchored on b1 | `barrier-expired` for b2 (reason `barrier`), same step | the first step strictly after b2 + 15 m 30 s: +5 s, +15 s, +25 s |
| Runtime called directly, with no expiry call between deliveries | `bar-sequence` for b3 (reason `barrier`) | — | when b3 arrives |
| Loop stepped every 60 s | `invalid-bar-time` for b0 | — | at the first step. The cadence alone makes every bar late, whether or not a slot is omitted |

**What the trace shows:**
- **Under the loop,** a single-leg omission is **first recorded as a `feed` incident, not a `barrier` incident.** The number of omitted slots does not change this.
- **`bar-sequence` appears only if a later boundary reaches the runtime before any expiry call.** Under the loop with prompt polling, the next boundary cannot arrive before b2's expiry: it closes at b3 + 15 m = b2 + 30 m.
- **The loop must poll within the 30 s slack.** Otherwise it halts on late bars. That is a property of the consumer, not of this history.

This is synthetic evidence about consumer behavior. It says nothing about live arrival timing.

## 6. What this means for the §4.3 empty-interval rule

1. **The 171 residual.** On this series they are not in-session gaps of permitted sessions, with one exception. 170 fall on holiday account days that the consumer never runs. The exception is one omission whose cause is not established.
2. **Invented bars.** The only other representation is a zero-volume bar, emitted by the provider or synthesized by the adapter. That would change what the adapters see (note §3 D), and nothing observed here supports it.
3. **Early closes.** A permitted row's session always closes at 17:00 ET, and the consumer has no per-product halt.
   - **Known early closes** cannot be permitted. A row that is not HOLIDAY/SHORTENED must carry every product's regular matching close (`book_session_calendar.py:351–:355`). A permitted row also needs every product qualified from captured sources (`:325–:326`).
   - **The remaining exposure** is an early close or ad-hoc closure that no captured source recorded. That becomes a halt on missing input mid-session, not a scheduled flat. It moves the D19 residual (ii) risk ([calendars README](../../ops/calendars/README.md)) from an audit-deadline error to a halt.

## 7. Returns and unresolved questions

**To the operator (spec §4.3, before freeze):**
- **Q-1: the empty-interval rule.**
  - *Operator guidance (2026-09-27, recommendation, not yet adopted):* a missing required input halts the book, and no bars are invented. §5 is consistent with this: the consumer already halts.

**Evidentiary, not an operator choice:**
- **Q-2: cause of the MGC omission.** It could be an exchange halt, a loss of data at the charting source, or something else. Settling it needs corroboration: a primary exchange record or a second independent source for that date. The date is in the private detail file.
  - Even an exchange halt would not by itself require a provider to encode halted intervals as omitted bars. That representation needs its own contract term in the equivalence spec (§4.3 / M1).
  - *Operator guidance:* leave Q-2 unresolved pending corroboration. It need not block the conservative missing-input rule.

**To TB-I3 (consumer owner) and the halt/resume owner (the routing condition holds):**
- **Q-3: does a missing-slot halt end the session?**
  - The operator's 2026-09-27 ruling classifies a **late** bar as a source incident ([halt/resume §4.1](../spec/2026-09-14-tb-s3-halt-resume-contract.md) `:97`) and leaves other cases unclassified.
  - The question is whether a halt from an **omitted** in-session slot is also an incident that ends the session under [incident ADR §A11.2](../adr/2026-09-17-bounded-platform-protection-incident-contract.md) `:378`. Under the loop, that halt is first recorded as `feed-silence`, followed by `barrier-expired` (§5). Either reason, or `bar-sequence`, should resolve to the same classification.
- **Q-4: unrecorded early closes.** An early close or ad-hoc closure that no captured source recorded passes the loader as a regular permitted row (§6 item 3). The consumer then halts mid-session on missing input.
- *Operator guidance on Q-3 and Q-4 (2026-09-27, recommendation):* loss of required input ends automation for that commissioning or first-release session. The owners record the interpretation and verify the behavior. For example, a pinned test would show that `feed-silence`, `barrier-expired` and `bar-sequence` caused by an omitted slot each end the session under §A11.2.

**Carried, not answered here:**
- **Holiday classification.** It uses the D19 calendar, which is secondary provenance accepted for date membership only. All 170 holiday residual intervals land on its 65 non-`NORMAL` dates, and none land on its 20 `NORMAL`-listed dates. No primary exchange source was read.
- **Live-provider behavior.** The panels are one charting platform's continuous series. They say nothing about how a live provider behaves (Q8 in note §5).
- **The 6J boundary.** The 6J panel starts 23 hours later than the others. That remains the Step 3 boundary obligation; it is not a gap.

## 8. Verification and revision

- `git merge --ff-only origin/main` → `875ecf2`. Consumer and calendar code was read at that head with `sed -n` and `grep -n`, at the line anchors cited above.
- `sha256sum` was run on every input. Each digest matches its pin (§2).
- `classify_gaps.py` and `reconcile_sessions.py` ran on system Python 3.14.3 (stdlib only) and produced §4.
- `trace_omitted_slot.py` ran through `.\fp.ps1 python -m pytest … --rootdir . -c pyproject.toml` on the ops environment, Python 3.13.2, and produced §5.
- `git check-ignore` confirms the private inputs are ignored (`lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/.gitignore:3`). No private file was copied into this worktree.
- `.\fp.ps1 check`: see the PR.

**Revision, 2026-09-27 (operator review):**
- Full hashes and a manifest were added. Retention was completed by the operator's copy, verified against the manifest (§2).
- The denominator is reconciled exactly, and "about 1 in 990" is replaced by one observed affected session.
- "No quiet slots" is narrowed to what was observed. The cause of the omission is stated as unknown.
- The halt claim is restated with its conditions, backed by a synthetic trace. `feed-silence` fires first under the loop, which corrects the earlier `barrier-expired` claim.
- Q-2 is recast as evidentiary, with a separate representation contract.
- The operator's guidance on Q-1 to Q-4 is recorded as recommendations.

**Not granted and not done:** no provider contact, spend, collection or emission change; no owner-text edit; no rule adopted.
