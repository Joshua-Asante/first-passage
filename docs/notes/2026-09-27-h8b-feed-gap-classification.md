# Feed gap queue classified against the four-leg consumer (H8 step (b))

**Status:** RETURNED FOR OPERATOR/COORDINATOR REVIEW 2026-09-27. Documentary classification only. It proposes no empty-interval rule, and it edits no owner text. The §4.3 rule stays the operator's to set before freeze.
**Assignment:** [handoff H8 step (b)](../briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md#h8--feed-provider-neutral-preparation), which grew out of the coordinator's acceptance of [H8 step (a)](2026-09-27-feed-provider-neutral-preparation.md#coordinator-acceptance-2026-09-27), decision 4. **Base:** `875ecf2` (main after #520).
**Where it ran:** the operator's machine. The private inputs were read in place in the primary checkout. The classifier and its full per-interval output are in session scratch space, outside every checkout. This note gives only counts, classes and digests. It contains no timestamps, prices or volumes from the panels.

## 1. Answer

**Across four years of canonical data, the consumer would have met exactly one in-session gap.** Every other interval in the queue falls outside a permitted session. Each is either the daily break, a weekend, or an account day that the calendar practice denies as HOLIDAY/SHORTENED.

- **No quiet slots.** None of the four legs has a no-trade 15-minute slot inside a permitted session. That includes the 18:00 ET session-open slot, which no leg ever misses.
- **The 171 residual gaps:** 170 fall on account days with a holiday early close or closure. **One** falls in a regular permitted session. It is 6 consecutive MGC slots in the middle of the day, in 2026, while the other three legs deliver every slot. The bar before the gap is thin and the bar after it carries a volume burst. That pattern fits a trading halt or a source interruption, not a quiet market. Whether the exchange halted or the chart source lost data is **UNRESOLVED**.
- **Consumer effect of that one event:** it would **halt the book**. The three other legs complete the first missing boundary, so the MGC barrier expires 15 min 30 s after that slot opens (`barrier-expired`). The halt comes before the 16:00 ET own-flat cap, so positions may be open. The routing condition in the card therefore holds. This result also goes to **TB-I3** (consumer owner) and to the **halt/resume owner** (§4 below).

## 2. Inputs verified (SHA-256, read in place)

| Input | Digest | Check |
|---|---|---|
| `calendar-gap-queue.json` (the pinned queue) | `509346d6…b35328` | matches the pin at [execution domain](2026-09-15-packet1-execution-domain.md) `:502` |
| `regular-session-gap-screen.json` (the 171 screen) | `54d6e96d…caf24` | bound in the private `step3-evidence-index-v3.json`; reproduces 27 / 46 / 49 / 49 = 171 residual and 3,972 regular-only intervals (`:689–:691`) |
| Panels `6J/MGC/MYM/MNQ_M15.csv` | `94d237cc…` / `c5487470…` / `15b34615…` / `cceaac41…` | equal to the queue's own `panel_sha256` values |
| `6J_M15-with-attested-prefix.csv` (the screen's 6J input) | `8ae083d0…3648fd2` | matches execution domain `:574` |
| `ops/calendars/cme_holiday_calendar_2022_2026.json` | `2698f268…1e9` | identical to `main` |
| Classifier script (private) | `18717cd2…ece67` | — |
| Summary output (private) | `63b1cda3…24267` | — |
| Per-interval detail (private) | `8c49ff90…b069` | — |

## 3. Classification rules (read at `875ecf2`, not inferred)

A gap slot is a 15-minute bar-open with no row in a leg's panel. Each slot gets one class. An interval takes its most severe slot class.

| Class | Rule | Consumer basis |
|---|---|---|
| `OUT_DAILY_BREAK` | bar-open in [17:00, 18:00) ET | The account day runs from 18:00 ET on the prior day to 17:00 ET (`scripts/author_book_session_calendar.py:53–:54`, `:155–:156`; enforced at `ops/c1_rail/book_session_calendar.py:302–:306`). A bar outside the bound session halts (`book_runtime.py:352`), so these slots must stay empty |
| `OUT_WEEKEND` | account date is a Saturday or Sunday | No account-day row exists |
| `DENIED_HOLIDAY_OR_SHORTENED` | account date is a calendar entry with any product group not `NORMAL` (65 dates) | HOLIDAY/SHORTENED rows are DENIED (`book_session_calendar.py:308`). `session_for` then returns no `BookSession` (`:236–:238`), so no barrier runs. Date membership only, under D19; the file's trade-date basis equals the account date used here |
| `HOLIDAY_ADJACENT` | the next weekday after such a date (50 dates) | Denied only if the forward UNCERTAIN_ADJACENT practice is applied (`author_book_session_calendar.py:21`). Counted separately |
| `IN_PERMITTED_SESSION` | anything else | Would halt: a non-contiguous boundary (`book_runtime.py:373`, `:381`), an incomplete four-leg barrier (`:390`, expiring at `:483`, which becomes `barrier-expired` at `book_account_owner.py:924`), or silence beyond 2 × 15 min + 30 s (`book_evaluate_loop.py:33`; `book_account_owner.py:865`) |

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

### 4.3 Book level (common window: 6J panel start to the shared panel end)

- **Permitted sessions:** 954 by the slot-walk method, and 993 non-holiday weekday sessions fully inside the window by the independent check. The difference is the 41 holiday-adjacent sessions, together with how each method treats window edges.
- **Permitted sessions with any absent leg slot:** **1**. It has 6 distinct slots, one leg absent at each, mid-session and not at the open.
- **Holiday-adjacent sessions:** 41, none with an absent slot. Gaps give no reason for the UNCERTAIN_ADJACENT denial; that practice rests on qualification grounds instead.

**Independent cross-check.** A second pass walked every 15-minute slot of every non-holiday weekday account day directly from the four panels, without using the queue. It required all four legs at every slot, including 18:00 ET. It found the same single session, the same 6 slots and the same leg.

## 5. What this means for the §4.3 empty-interval rule (for the operator; no rule is proposed)

1. **Quiet slots vs missing input.** The spec (§4.3) marks the 171 residual gaps as the load-bearing unknown. On canonical data they are **not quiet slots**. 170 are holiday account days, which the consumer never runs. One is an interruption.
2. **"Absent means absent input" is historically cheap.** At 15 minutes, all four legs traded in every permitted-session slot except during that one event. An empty-interval rule that treats any omitted in-session slot as absent input, and so halts under the existing contiguity rule, would have halted about 1 in 990 permitted sessions on this history. The alternative is to have the provider emit, or the adapter synthesize, a zero-volume bar. That would change what the adapters see, which falls under note §3 D. Nothing in this history supports it.
3. **Early closes are the other constraint.** A permitted row's session always closes at 17:00 ET, and the consumer has no per-product halt. On a permitted day, a product that stops trading early breaks the barrier and halts the book. The loader already covers **known** early closes. A row that is not HOLIDAY/SHORTENED must carry every product's regular matching close (`book_session_calendar.py:351–:355`), and a permitted row needs every product qualified from captured sources (`:325–:326`). So a known early close cannot be permitted. The remaining exposure is an early close or ad-hoc closure that **no captured source recorded**. That becomes a mid-session halt rather than a scheduled flat. It moves the D19 residual (ii) risk ([calendars README](../../ops/calendars/README.md)) from an audit-deadline error to a halt.

## 6. Returns and unresolved questions

**To the operator (spec §4.3, before freeze):**
- Q-1: Adopt a rule consistent with this history, where an omitted in-session slot is absent input, the consumer halts, and no synthesized bars are allowed? Or set a different one? Operator decision.
- Q-2: Is the MGC event an exchange halt or a loss of chart-source data? An exchange halt would mean Side B is correct, and a provider must also omit those slots (M1). A source loss would mean the canonical panel is incomplete, and any Side A bar there is not an M1 failure. Settling it needs a primary exchange record or a second source for that date. The date is in the private detail file.

**To TB-I3 (consumer owner) and the halt/resume owner (the routing condition holds):**
- Q-3: The operator's 2026-09-27 ruling classifies a **late** bar as a source incident ([halt/resume §4.1](../spec/2026-09-14-tb-s3-halt-resume-contract.md) `:97`). It explicitly leaves other cases unclassified. Is a `barrier-expired` or `bar-sequence` halt caused by an **omitted** in-session slot also a source incident that ends the session under [incident ADR §A11.2](../adr/2026-09-17-bounded-platform-protection-incident-contract.md) `:378`? This history puts the rate at about 1 in 990 sessions, so the answer decides whether roughly one session in four years ends early.
- Q-4: An early close or ad-hoc closure that no captured source recorded passes the loader as a regular permitted row (§5 item 3). The consumer then halts mid-session. Should that halt be treated the same way as Q-3? No other control would catch it.

**Carried, not answered here:**
- The holiday classification uses the D19 calendar, which is secondary provenance accepted for date membership only. All 170 holiday intervals land on its 65 non-`NORMAL` dates, and none land on its 20 `NORMAL`-listed dates. No primary exchange source was read.
- The panels are the charting platform's continuous series. The history says nothing about how a live provider behaves (Q8 in note §5).
- The 6J panel boundary (a 23-hour-later start) remains the Step 3 boundary obligation. It is not a gap.

## 7. Verification

- `git merge --ff-only origin/main` → `875ecf2`. Consumer and calendar code was read at that head with `sed -n` and `grep -n`, at the line anchors cited above.
- `sha256sum` was run on the queue, the screen, the four panels and the 6J derivative. Every digest matches its pin.
- The classifier (Python 3.14.3) asserts every input digest before it reads. It printed the tables in §4.
- The independent panel-only slot walk found 1 session, 6 slots and 1 leg.
- `git check-ignore` confirms the private inputs are ignored (`lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/.gitignore:3`). No private file was copied into this worktree.
- `make check`: see the PR.

**Not granted and not done:** no provider contact, spend, collection or emission change; no owner-text edit; no rule adopted.
