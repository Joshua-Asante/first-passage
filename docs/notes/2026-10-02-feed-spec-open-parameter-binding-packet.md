# Feed equivalence spec: binding packet for the eleven OPEN parameters

**Status:** PROPOSED for operator binding, 2026-10-02. Nothing here is bound, and the frozen spec is not edited. Worker return to the deployment coordinator.
**Serves (Rule 7):** the [frozen spec](../spec/2026-09-27-cme-execution-feed-equivalence-test-DRAFT.md) §16.2 (`:302–:316`) and §16.3 (`:323–:328`), and the [checklist CP-7 row](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md) `:500`. That row records the operator ruling of 2026-10-02 (sitting 1, PR #610): CP-7 may open after T00 GO-evidence, A9-PREP and a bound spec, meaning every OPEN parameter bound under §16.3. The same ruling names this packet as authorized provider-neutral preparation.
**Spec state, verified:** PR #585 merged as `721be61`, UTC committer date 2026-10-02. `git show 721be61:<spec> | sed '3d' | sha256sum` and the same command on the working tree at `10b3929` both give `a9b93a36…cadad5`, which matches the Status line (`:3`). There is exactly one `**Status:**` line. §16.4 records no binding (`:334`).
**Citation keys.** `path:line` refers to `origin/main` at `10b3929` unless marked otherwise.
- "spec" is the frozen spec.
- "H8 note" is [the H8 preparation note](2026-09-27-feed-provider-neutral-preparation.md).
- "h8b" is [the H8(b) gap classification](2026-09-27-h8b-feed-gap-classification.md).
- "#583 note" is `docs/notes/2026-10-01-feed-provider-questions-DRAFT.md` at commit `8387e66` of [PR #583](https://github.com/Joshua-Asante/first-passage/pull/583), which is open and not on main. Since then the PR has added a "Quiet intervals" clause to Q10 (`e14ff77`); the citations below are pinned to `8387e66`.
- "Step 3" is [the Packet 1 Step 3 acceptance](2026-09-15-packet1-step3-acceptance.md); "execution domain" is [the Packet 1 execution domain](2026-09-15-packet1-execution-domain.md).
- "template" is [the locked template](../spec/feed_equivalence_discovery_test_LOCKED.md); "umbrella" is [the Track B umbrella](../briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md); "Track A" is [the Track A plan](../superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md); "halt/resume contract" is [the TB-S3 halt/resume contract](../spec/2026-09-14-tb-s3-halt-resume-contract.md).

**Web sources.** The TradingView support page was opened on 2026-10-02. Every cmegroup.com fetch timed out, so each CME fact below comes from a search excerpt and is marked **[excerpt]**. Treat those as UNVERIFIED until they are read on cmegroup.com, the same standard as #583 note `:16–:21`.

## 1. Deadline and mechanics

- **How a binding is made.** Each OPEN item is bound by a dated operator decision, written into the body together with a §16.4 row. The new digest goes only in the Status line (spec `:323–:324`).
- **When a binding is allowed.** Only before any provider data has been seen and before CP-6 (spec `:325`). The 2026-10-02 ruling makes a bound spec a CP-7 entry condition. In practice, then, all eleven items bind before any provider account or data exists.
- **Recommended timing.** Bind before any reply to the Q1–Q12 questions arrives (#583 note `:85–:119`). Then no value can be read as fitted to a provider's answer. A reply can only select a branch already declared here (OPEN-1), or fail eligibility (#583 note `:58–:64`).
- **Order.** Dependencies run OPEN-11 → OPEN-3 → OPEN-4 → then OPEN-10 and OPEN-8. The other items have no dependency.
- **Commits.** One commit per item keeps the §16.3 step 2 digest chain literal, because each row records the digest it supersedes. The first binding commit also rewrites the Status line to the §9 form `FROZEN 2026-10-02 <digest>` (spec `:292`).

## 2. Summary

**No item has to wait for a provider answer.** Provider facts enter in two ways only:
- as later-binding items B.4 (provider-native codes) and B.5 (timestamp translation), under H8 note `:85–:92`;
- as eligibility screens (#583 note §2).

Four items need a non-provider input before they bind, shown in the right-hand column.

| # | Controls | Recommended value | Basis | Input needed before binding (operator binds all) |
|---|---|---|---|---|
| OPEN-1 | §4.2 detail: which time places a constituent in a bucket; close-stamped bars | Exchange time where delivered, else the provider's stamp, never receipt time. A bar's start is its interval start. A constituent that straddles a boundary is inadmissible | spec `:95`, `:303`; `book_runtime.py:369` | None for (i), (ii), the placement part of (iii), (v) and (vi). The bust/cancel exclusion in (iii) and clause (iv) (trade prices only) each need an operator ruling that they are within `:95`. §7 completeness is not an OPEN-1 binding (§4, question 6) |
| OPEN-2 | 6J canonical adjustment and trading hours | Electronic trading hours and back-adjustment off, like the other three legs | Hours derived from h8b `:63`, `:103`; adjustment unresolved | The operator's 6J attestation, or a private roll-gap read |
| OPEN-3 | Live dated-contract selection per leg | The contract that the canonical rule (OPEN-11) selects, defined once and shared by the feed and TB-V1 | spec `:118`; AGENTS.md `:233` | TB-V1 confirms the venue can trade each selected contract up to the switch |
| OPEN-4 | Roll-exclusion band | The switch session ± 3 sessions, per leg | RESULTS.md `:145–:147` | OPEN-11 |
| OPEN-5 | Volume (M4): role and threshold | A verdict role on every leg whose body reads volume. At most 1 compared bar per such leg with a different volume. Descriptive on the other legs | spec `:132`; Step 3 `:31–:35` | A yes/no read of which bodies read volume |
| OPEN-6 | Threshold for revisions seen only in the raw stream | No threshold: counted and reported | The adopted forwarded-revision limit of 0 (spec `:313`) plus M1–M4 already score the delivered bars | None |
| OPEN-7 | M9 role | Descriptive | Constraint at spec `:314`; TB-W1 boundary is the panel origin | None |
| OPEN-8 | Window start and end | Opens at the first Sunday 18:00 ET session after collection starts. Closes once it holds ≥ 10 covered sessions, 2 Sunday opens, 2 Friday closes and 1 month-end-adjacent session | spec `:139`, `:181`; template `:42` | OPEN-4 |
| OPEN-9 | Re-application after a FAIL that changed B items only | One per provider | spec `:194–:199` | None |
| OPEN-10 | Minimum overlap for arm C | From the band around each leg's most recent canonical switch to the canonical end, and at least 10 sessions | spec `:85`, `:302` | OPEN-11, OPEN-4 |
| OPEN-11 | Canonical `1!` roll behavior | The platform's per-symbol rule: switch N_s business days before the last trading day, with N_s attested | TradingView support 43000691027; RESULTS.md `:145–:147` | The operator attests the four N_s values |

## 3. Per parameter

### OPEN-1: per-granularity constituent rule (§4.2)

**What it controls.** How delivered constituents become the Side-A 15-minute bar, both the one compared in the test and the one forwarded to the consumer.

**Spec text.**
- Adopted already: the bucket `[open, open + 15 min)`, O = first open, H = max high, L = min low, C = last close, V = summed volume (spec `:95`, `:303`).
- OPEN: "which timestamp assigns a constituent to a bucket (exchange time or provider stamp), and how a 1-minute bar stamped at its close maps to its bucket" (`:303`).
- §7: "A bucket whose completeness cannot be established by the deadline is not emitted" (`:147`).

**Candidates.**

| Choice | Option | Consequence |
|---|---|---|
| Placing clock | **Exchange transaction time, falling back to the provider's stamp (rec.)** | Places trades by the exchange events the canonical bars are built from. That the platform builds from exchange time is UNVERIFIED, though it is the norm. The stamp actually used is recorded for each stream |
| | Provider stamp only | Always available, but an aggregation-time stamp can push constituents across a boundary, which M2 or M3a would count as failures |
| | Receipt time | Network delay moves trades across boundaries. Rejected |
| Close-stamped bar | **Place the bar by its interval start, `stamp − d` (rec.)** | A 1-minute bar stamped 10:15 belongs to the 10:00 bucket |
| | Place it by its stamp | Every bucket would be shifted by one constituent |
| Straddling constituent | **Make that stream inadmissible (rec.)** | Splitting it would invent data, which §7 forbids ("never interpolate", `:147`) |
| Completeness | *Not an OPEN-1 choice* | §7 (`:147`) requires completeness to be *established* but does not define how. Defining it is a body change, not a binding; see §4, question 6 |

**Recommended binding text.**
> **§4.2 per-granularity rule.**
> (i) *Clock.* A constituent is placed by the exchange transaction time when the provider delivers it, and otherwise by the provider's stamp. Receipt time never places a constituent. The clock used for each stream is recorded in the adapter configuration (later-binding item B.5).
> (ii) *Bars of any duration d up to 15 minutes.* A constituent covers `[t0, t0 + d)`. Here `t0` is its stamp if the provider stamps bars at their open, or its stamp minus `d` if it stamps them at their close. The constituent belongs to the bucket that contains `t0`, and is admissible only if its whole interval lies inside that bucket. A stream whose constituents straddle bucket boundaries is inadmissible; constituents are never split.
> (iii) *Trades.* A trade belongs to the bucket that contains its time. A trade at exactly `open + 15 min` belongs to the next bucket. V is the sum of exchange-reported quantities. A busted or cancelled trade that is known before emission is excluded. **[Operator ruling needed: this exclusion is within `:95`, as for (iv).]** How a bust learned after emission is scored is not part of this binding; it goes with OPEN-6 and §4 question 7, because spec M7 (`:135`) covers revised delivered bars only.
> (iv) *Prices.* O, H, L and C come from executed trade prices only. A stream whose bars are built from bid/ask, midpoint, settlement or indicative prices is inadmissible. **[Operator ruling needed: this clause is within `:95`'s "exact constituent rule". If not, drop it from the binding and route it with question 6.]**
> (v) *Ordering.* "First" and "last" follow the clock in (i). Ties are broken by the provider's sequence identifier, where one is given.
> (vi) *Native 15-minute bars* are compared as delivered, after the B.5 stamp translation.

**Not part of the OPEN-1 binding: §7 completeness.** A candidate definition, for the body change in §4 question 6, is: a bucket is complete when the stream delivers, timed at or after `open + 15 min`, any of a constituent, a provider no-trade marker or a sequenced status message; for a bar stream, also when the constituent ending at `open + 15 min` arrives. A no-trade marker proves completeness only and is not trade evidence (§4.3(c), `:103`). Like the "capture incomplete" definition, this goes beyond §16.3 because §7 leaves "established" undefined.

**Sources.**
- The consumer's bar-open `Bar.ts` (`ops/c1_signal_daemon/book_runtime.py:369`) and the delivery deadline `bar.ts + BAR_PERIOD + BAR_SLACK` (`:351–:353`; `book_protocol.py:39–:40`).
- spec `:94–:95`, `:147`, `:150`.

**Provider dependence.** This item binds now. The provider's own conventions are asked in #583 Q4 (`:95–:103`), Q8 (`:111`) and Q10 (`:115`): open or close stamps, time zone, exchange time, trade or quote prices, and no-trade markers. A provider's answer selects a branch of this rule and the B.5 translation (H8 note `:90`). A stream that fits no branch is inadmissible; that is not a reason to re-bind the rule.

**Consequence.** In thin intervals, such as 6J or MGC overnight, a stream may send no marker, heartbeat or sequenced message after a boundary. It then cannot prove completeness within 30 s, the bucket is not emitted, and the book halts (M5, M8). If the body change in §4 question 6 adopts in-stream proof, completeness signalling becomes an eligibility fact. PR #583 now asks about it directly (Q10 "Quiet intervals", `e14ff77`).

**Binds:** operator.

### OPEN-2: 6J adjustment basis (§4.5)

**What it controls.** Whether the 6J canonical side is built the same way as the other three legs. That decides whether §4.5's rule, "no back-adjustment on either side" (`:107`), can apply to 6J. Spec `:305`, `:258`.

**Evidence.**
- **Trading hours: derived, electronic hours.**
  - The 6J panel has no absent slot inside any permitted 18:00–17:00 ET session (h8b `:63`, `:74`).
  - Across all four legs, the 952 fully observed permitted sessions had every slot filled, except six MGC slots (h8b `:64`, `:68`; one leg, `:103`, `:106`).
  - A panel exported for regular trading hours only would leave most of each 23-hour session empty.
  - This is an inference from the data, not an attestation.
- **Back-adjustment: unresolved.**
  - The 6J ledger says "back-adjusted continuous" (`ops/instruments/6J.md:3`).
  - The Step 3 "back-adjustment off" attestation names only MGC, MYM and MNQ (Step 3 `:17–:20`).
  - The 6J attestation covers the chart, the harness and the date window only (execution domain `:534–:536`).
  - Precedent: the platform's `1!` exports of NQ and MNQ were measured as not back-adjusted (`lab/analysis/_inbox/ict_mnq_2026-08/RESULTS.md:145–:147`).

**How to settle it.** Either of:
- **(a)** the operator reads the retained 6J chart settings;
- **(b)** a private read on the operator's machine of the 6J derivative (digest `8ae083d0…`) at each quarterly switch. An unadjusted series jumps at each switch session by roughly the quarterly USD–JPY carry; a back-adjusted series does not. This is the RESULTS.md method, and only digests and the yes/no answer are recorded.

**Candidates.**

| Value | Consequence |
|---|---|
| **Off, electronic hours (rec., if (a) or (b) confirms it)** | §4.5 applies to 6J unchanged |
| On | The book was qualified on adjusted 6J prices, but live trading would see unadjusted ones. That is a behavior question for its owner before CP-6 (checklist `:506–:511`), not a binding. For the test: Side B is exported with adjustment off (§4.5). Arm C for 6J is then limited to bars after the canonical input's last switch, which replaces OPEN-10 for 6J. That limit works only if the platform adjusts history before each switch, which is UNVERIFIED |

**Recommended binding text.**
> **6J canonical settings:** electronic trading hours and back-adjustment off. §4.5 applies to 6J unchanged.

**Provider dependence:** none.

**Binds:** operator, after (a) or (b).

### OPEN-3: live contract-selection rule (R-MAP-1)

**What it controls.** Which dated contract the feed subscribes to in each session, and which one the venue trades. Spec `:114–:118`, `:306`; R-MAP-2 `:119`; H8 note A.4 `:82` and B.4 `:89`.

**Candidates.**

| Value | Consequence |
|---|---|
| **The canonical rule (OPEN-11), by construction (rec.)** | The adapters see the contract the strategies were qualified on. The two can diverge only if the platform changes N_s, and OPEN-4 covers that |
| A fixed calendar rule independent of the platform (for example, k business days before the last trade or before first notice) | Deterministic. Between the two rules' switch dates, though, the live contract differs from the canonical one. That is a behavior question before CP-6 (spec `:118`), and the band must span both dates |
| A live volume-lead rule | Needs data on the next contract and is decided during the session, so it is not fixed before data. It can disagree with the platform's fixed-offset rule on any roll |
| The bridge's own continuous mapping | A third party sets the rule, and the repo has no primary source for it. TB-V1 owns broker symbols (`ops/c1_rail/c1_sizing_host_reference.py:127–:128`) |

**Recommended binding text.**
> **R-MAP-1 live rule.** For each leg, the live dated contract in a session is the contract that the bound OPEN-11 rule assigns to that session. One per-leg contract-selection object (N_s, the listed cycle, and the last-trading-day rule) is defined once. Both the feed adapter's subscription (R-MAP-2) and the TB-V1 order binding consume it. Provider-native codes are later-binding item B.4.

This follows AGENTS.md's configuration-as-code rule (`:233`).

**Before binding.** TB-V1 confirms that the venue can hold and trade each leg's selected contract right up to its switch. For example, physically delivered 6J and MGC must not face an earlier forced liquidation. 6J is physically settled **[excerpt]**, and MGC contracts still open after the last trade settle by delivery **[excerpt]**. If the venue cannot, the live rule must differ from the canonical one: use the second row above, and send the difference to its owner before CP-6.

**Provider dependence.** This item binds now. #583 Q9 (`:113`) asks whether a provider can name dated contracts and refuses silent substitution. That answer decides eligibility under R-MAP-2; it does not change the rule.

**Binds:** operator.

### OPEN-4: roll-exclusion band

**What it controls.** Which sessions around each switch are excluded from the verdict and reported as a separate stratum (spec `:116`, `:308`; compared slot `:124`). Through OPEN-8, the band also decides which sessions count toward the window.

**Candidates.**

| Width | Consequence |
|---|---|
| ±1 session (3 sessions) | Excludes the least. If the platform moves N_s by 2 sessions or more, sessions with mismatched contracts enter the verdict. The result is an M3a FAIL, which is final for that configuration |
| **±3 sessions (7 sessions) (rec.)** | Covers the measured spread of the platform's switch for NQ/MNQ: 17 quarterly gaps cluster within ±4 days of the third-Friday expiry (RESULTS.md `:145–:147`). Reading that as about ±3 business days, and extending it to 6J and MGC, whose last-trading-day rules differ, is this note's inference. The four legs' bands exclude more sessions, so the window (OPEN-8) runs longer |
| ±5 sessions (11 sessions) | More margin. MGC rolls six times a year (listed in even months only **[excerpt]**), so windows grow materially longer |

**Recommended binding text.**
> **Roll-exclusion band.** For each leg, the band is the leg's switch session under the bound OPEN-11 rule, plus the three permitted sessions before it and the three after it. If the OPEN-3 rule differs from OPEN-11, the band runs from three sessions before the earlier switch to three sessions after the later one. A band session is excluded for that leg only, and it does not count toward the four-leg window (OPEN-8).

**Sources.**
- Mismatched roll rules produce known noise (`docs/briefs/Q-DATAFIDELITY-1-tv-price-fidelity-and-integrity-gate-scope.md:18`).
- RESULTS.md `:145–:147`.
- The platform derives N_s from statistics (OPEN-11), so it may be revised.

**Provider dependence:** none.

**Binds:** operator, after OPEN-11 and OPEN-3.

### OPEN-5: M4 volume role and threshold

**What it controls.** Whether volume differences enter the verdict, and how much difference is tolerated.
- Spec `:132`, `:311`: M4 is "not descriptive-only by default", because the ORB entry reads volume.
- §10 lets M4 enter the verdict only if a role is frozen (`:186`).
- The body requires the tolerance to allow for the canonical side's re-capture differences (`:132`).

**Facts.**
- The ORB (MNQ) entry reads volume (`8c15f18:docs/notes/2026-09-26-orb-lifecycle-evidence.md:22`).
- Whether the other three legs read volume is UNVERIFIED (spec `:259`).
- Canonical instability: the 2026-09-15 re-captures differed in volume on 8 rows, across 6J, MGC and MNQ (Step 3 `:31–:35`). The four panels hold 378,424 rows (execution domain `:265–:268`), so the rate is about 2×10⁻⁵ per bar.
- A ten-session window has about 920 bars per leg (92 slots × 10). At that rate, canonical-only differences would number about 0.02, and the chance of 2 or more is below 0.1%.
- Caveat: the re-captures were 12 days apart, and drift over months is not measured.

**Candidates.**

| Value | Consequence |
|---|---|
| Descriptive on every leg | A provider whose volume definition differs could PASS while ORB's volume filter behaves differently live. That contradicts the body (`:132`) |
| Verdict, exact (0 differing bars) | About a 2–3% chance per volume-reading leg that a FAIL comes from the canonical side alone. A FAIL is final for that configuration |
| **Verdict, at most 1 differing bar per volume-reading leg; maximum difference reported (rec.)** | Allows for the canonical instability, as the body requires. Any systematic difference in volume definition (for example, block or other off-book trades counted differently) still FAILs |
| Verdict, ≤ 0.5% incidence | Mirrors the relaxed M3a option the freeze rejected (`:310`). It has no basis in the canonical data |
| Applied to all four legs instead of the legs that read volume | A volume difference on a leg that never reads volume would FAIL the book without any change in behavior |

**Recommended binding text.**
> **M4.** M4 has a verdict role on each leg whose accepted strategy body reads bar volume: MNQ (ORB) is established, and the other legs follow the yes/no read. Per such leg, at most one compared bar in the window may have `V_A ≠ V_B`, counted in integer contracts. The maximum difference is reported. On the other legs M4 is descriptive. Side B volume is taken from the fresh capture (arm L).

**Before binding.** A yes/no read, for each of the other three accepted bodies, of whether it reads bar volume. That read uses the private read surface (AGENTS.md; campaign §60) and records no body text or values. If the read is not authorized, the fallback is all four legs, with the cost shown in the last row of the table.

**Provider dependence.** This item binds now. #583 Q4 (`:101`) asks whether the provider's volume is exchange-reported trade volume. That answer is an eligibility fact; it does not set the threshold.

**Binds:** operator.

### OPEN-6: threshold for revisions seen only in the raw stream (M7)

**What it controls.** Whether revisions that the adapter holds back from the consumer can fail the test. Spec `:135`, `:313`. Already adopted: **0** revisions forwarded.

**Candidates.**

| Value | Consequence |
|---|---|
| **No threshold: counted per symbol, labelled and reported (rec.)** | A revision that is held back never reaches the consumer. If the delivered bar was wrong, M1, M2, M3a and M4 catch it against the canonical capture exported after the window. If the delivered bar was right, the revision has no effect on behavior |
| 0 | Normal exchange trade busts and corrections would FAIL providers whose delivered bars matched exactly |
| A capped rate | No basis without data. Choosing one later would be the per-provider tolerance forbidden at `:245` |

**Recommended binding text.**
> **M7 raw-stream revisions.** No verdict threshold. Post-delivery revisions seen only in the raw stream are counted per symbol, labelled, and reported in the private record. They reach the verdict only through M1–M4 and the adopted forwarded-revision limit of 0.

**Provider dependence.** This item binds now. Whether a provider flags revisions (#583 Q7, `:109`) is an eligibility fact: an unflagged revision can be neither held back nor labelled (#583 note `:62`).

**Binds:** operator.

### OPEN-7: M9 role

**What it controls.** Whether a difference in decisions between the adapters run on Side A and on Side B can fail the test. Spec `:137`, `:314`.

**Constraint already frozen.** M9 can take a verdict role only together with three things: a matched pre-window capture on both Side A and Side B that reaches each leg's TB-W1 warm-up boundary; warm-up completed before scoring; and recorded adapter parity (`:314`).

**Facts.**
- The TB-W1 boundary is the panel origin, 2022-09-01 (`docs/notes/2026-09-12-track-b-scaling-faithfulness-read.md:133–:138`). It is "a Step 3 replay claim, not warm-restart" (`:130–:131`).
- A live feed collected after CP-7 cannot supply Side-A bars back to 2022.
- With M1, M2 and M3a exact (all adopted) and M4 bound, the only channels left through which decisions could differ are volume and pre-window history.

**Candidates.**

| Value | Consequence |
|---|---|
| **Descriptive (rec.)** | Satisfies the frozen constraint. Run the replay with canonical history shared up to the window start, and Side A versus Side B bars inside the window. Any boundary where the intents differ can then be attributed to the window bars, and is reported |
| Verdict | Needs Side-A bars back to the origin, which means provider history in arm H, an item that needs funding (spec `:86`). Without them the constraint fails |

**Recommended binding text.**
> **M9.** Descriptive; no verdict role.

**Provider dependence:** none.

**Binds:** operator.

### OPEN-8: window start and end rule

**What it controls.** Which sessions are scored, fixed before collection starts (spec `:139`, `:181`, `:315`). The minimum content is already adopted, matching template `:42`.

**Candidates.**

| Value | Consequence |
|---|---|
| Fixed calendar dates chosen now | Simple, but the dates may fall before CP-7 or before collection starts. Rebinding them is then inadmissible after CP-6 |
| **The first qualifying span after collection starts (rec.)** | Mechanical. Its length depends only on the calendar and the bands |
| Start declared by the operator during collection | A choice made while provider data is visible, for example during adapter shakedown |

**Recommended binding text.**
> **Window rule.**
> *Covered session:* a session that has a ratified, permitted calendar row (not DENIED), lies entirely inside the collection, and is outside every leg's roll-exclusion band.
> *Start:* the first Sunday 18:00 ET session open strictly after the collection start. The collection start is the instant recorded in the private record before the collector connects.
> *End:* the 17:00 ET close of the first session at which the window holds at least 10 covered sessions, at least 2 covered sessions opening Sunday 18:00 ET, at least 2 covered sessions closing Friday 17:00 ET, and at least 1 covered session whose account date is the last business day of a month or the first business day of the next.
> *Other sessions:* every non-covered session inside the window is listed with its reason and is never scored. If calendar rows run out first, the run is BLOCKED (calendar coverage missing, `:200`).

**Provider dependence:** none.

**Binds:** operator, after OPEN-4.

### OPEN-9: re-application after a B-items-only change

**What it controls.** How many times a provider may try again after a FAIL by changing only later-binding B items (H8 note `:85–:92`). Spec `:194–:199`, `:316`.

**Candidates.**

| Value | Consequence |
|---|---|
| None | Strictest. With M5, M6 and M8 at 0, one transient fault anywhere in the window ends that provider |
| **Once per provider (rec.)** | Allows one configuration fix. The advantage from drawing another window is limited to two windows, and every attempt is reported |
| Unlimited | Every retry is another chance to pass the zero-tolerance timing metrics, so a PASS becomes more likely with each attempt (`:199`) |

**Recommended binding text.**
> **Re-application.** After a FAIL, a provider may apply once more, changing only later-binding B items. Before the new window starts, the change, the FAIL record it answers and the new configuration digest are frozen. The new window is the next one the OPEN-8 rule produces after that freeze. If the re-application FAILs, applications by that provider end. A change outside the B items is a requalification (H8 note D, `:100–:105`), not a re-application. Every attempt, including BLOCKED runs, is reported (`:195`).

**Provider dependence:** none.

**Binds:** operator.

### OPEN-10: minimum overlap for arm C

**What it controls.** How much of the canonical input the fresh capture must reproduce exactly, field for field, before arm L is scored. A shorter overlap is BLOCKED (spec `:85`, `:302`).

**Candidates.**

| Value | Consequence |
|---|---|
| 10 sessions ending at the canonical end | Little exposure to the platform revising its history. But no contract switch is exercised, so a change in the platform's roll rule would pass unseen |
| **From the start of the band around each leg's most recent canonical switch before 2026-09-03, through the canonical end, and at least 10 sessions (rec.)** | Exercises one switch per leg against the bound OPEN-11 rule, with no provider involved. For the quarterly legs this is about three months |
| The full canonical span, 2022-09-01 to 2026-09-03 | The strongest check. The 2026-09-15 re-captures agreed on timestamps and prices (Step 3 `:35`), but they were taken 12 days after the original export. A platform revision anywhere in four years of history BLOCKs the test, and nothing short of a §13 re-opening can cure that |

**Recommended binding text.**
> **Arm C minimum overlap, per symbol.** The common span is contiguous up to the canonical input's last bar (2026-09-03T00:00Z). It starts no later than the first session of the roll-exclusion band around that symbol's most recent canonical switch before 2026-09-03, and it contains at least 10 complete permitted sessions. If OPEN-2 finds 6J back-adjusted, 6J's span starts after that switch instead.

**Provider dependence:** none.

**Binds:** operator, after OPEN-11 and OPEN-4.

### OPEN-11: canonical `1!` roll behavior

**What it controls.** On which session the canonical series switches contracts. OPEN-3, OPEN-4 and OPEN-10 all depend on it. Spec `:307`, `:257`; owed before CP-6 "from a primary source or the operator's attestation".

**Primary source.** The platform's [support page](https://www.tradingview.com/support/solutions/43000691027) (read 2026-10-02):
- the switch condition is the next contract's daily volume exceeding the current contract's;
- for each symbol, that condition is turned into a fixed rule from statistics, for example to "switch contracts 6 business days before the expiration".

This agrees with the repo's own measurement: NQ and MNQ gaps fall within ±4 days of expiry (RESULTS.md `:145–:147`). MNQ ledger `:96` ("volume-lead … the TV-`1!` analogue") is a claim made without a primary source, and the support page refines it.

**Last trading day and listed cycle, per leg.**
- **6J:** Mar/Jun/Sep/Dec; the second business day before the third Wednesday **[excerpt]**.
- **MNQ:** Mar/Jun/Sep/Dec; 9:30 ET on the third Friday **[excerpt]**.
- **MYM:** Mar/Jun/Sep/Dec; third-Friday expiry (`ops/instruments/YM.md:31`, inherited at `MYM.md:90`).
- **MGC:** Feb/Apr/Jun/Aug/Oct/Dec; the third-last business day of the contract month **[excerpt]**.

**Candidates.**

| Value | Consequence |
|---|---|
| **The platform rule, with each N_s attested (rec.)** | The form of the rule comes from a primary source. The values are attested by the operator and checked against the panels |
| Daily volume crossover, reconstructed | The page says the rule is a fixed offset set from averages, so a day-by-day crossover would disagree on some rolls |
| Switch on the expiry day | Contradicted by the page. RESULTS.md `:145–:147` (±4 days around expiry, NQ/MNQ) neither supports nor rules it out |

**Recommended binding text.**
> **Canonical roll.** For each leg, the canonical `1!` series switches to the next listed contract at the 18:00 ET open of the session whose account date is the N_s-th CME business day before the current contract's last trading day. The values N_6J, N_MNQ, N_MYM and N_MGC are integers, recorded here.

**Before binding.** The operator attests the four N_s values:
- (a) from the platform's display of the dated contract behind the `1!` chart across its most recent switch;
- cross-checked against (b) the switch sessions, which show as unadjusted discontinuities in the canonical panels. That check is a private read on the operator's machine that records digests and session dates only.

Whether the switch takes effect at the session open or at another boundary is not stated on the page; the band covers that.

**Provider dependence:** none.

**Binds:** operator.

## 4. Open questions

1. **Completeness signalling.** Resolved: PR #583 added the question to Q10 ("Quiet intervals", `e14ff77`).
2. **OPEN-2.** Is there a retained record of the 6J chart's adjustment setting, or is the roll-gap read needed?
3. **OPEN-11.** Can the operator read the dated contract behind the `1!` chart on the platform? The page does not say whether or when the platform revises N_s. Under the frozen text, a revision made between binding and the window would surface as an M3a FAIL outside the band, not as BLOCKED. Making it BLOCKED would change §10 (`:200`), which is a body change, not a binding.
4. **TB-V1.** Can each leg be traded in its selected contract up to the switch, particularly physically delivered 6J and MGC? The answer decides between the first and second rows of the OPEN-3 table.
5. **OPEN-5.** Authorize the yes/no volume read (private read surface), or accept the all-four-legs fallback?
6. **BLOCKED versus FAIL.** "Capture incomplete" (§10, `:200`) is not objectively defined. Under the OPEN-9 recommendation a BLOCKED run uses up no re-application, so a definition is needed: for example, a gap in the collector's own liveness record, independent of provider messages. That is a body change beyond a binding. §7's "established" completeness (`:147`) is the same class; a candidate definition is in OPEN-1. Both need an operator decision on whether to amend the body before CP-6, under §13.
7. **Meaning of "raise health."** If the §7 correction row's "raise health" (`:150`) means the source reports itself unhealthy, then every raw revision halts the book and is already scored by M6 or M8. OPEN-6 is unaffected, but the adapter contract (A9-PREP, Track A `:236`) has to say which reading applies. *Ruled 2026-10-02 (operator, sheet 2 item 3, "all recommended", direct to coordinator (3)); recorded here 2026-10-03:* a revision of a bar already forwarded **latches the source unhealthy** (whole-book halt, operator recovery; fail-closed). Coordinator (3) Track B disposition: an identical redelivery inside the one-day delivered memory is dropped; a late bar at or before the last forwarded `ts` but outside that memory latches as `late_bar_unverifiable`. Implemented in #619. OPEN-6 is unaffected. The frozen spec carries only a Status-line pointer to this record (its body digest is unchanged).
8. **Calendar coverage (R-MAP-3).** Calendar rows must cover the whole window before collection starts. `ops/calendars/book_session_calendar_2026-10.json` exists, but its ratification was not read here. This is a prerequisite, not an OPEN item.

## 5. Verification

- `git fetch`; branch `claude/feed-open-binding-packet` from `origin/main` `10b3929`.
- Spec digest and freeze checks: `sed '3d' <spec> | sha256sum` and `git show 721be61:<spec> | sed '3d' | sha256sum` both gave `a9b93a36…cadad5`. `grep -c '^\*\*Status:\*\*'` gave 1. `TZ=UTC git log -1 --date=format-local:%Y-%m-%d --format=%cd 721be61` gave 2026-10-02.
- Reads by line:
  - spec (all);
  - H8 note (all);
  - h8b `:45–:110`, `:140–:160`;
  - Step 3 `:1–:50`;
  - execution domain `:255–:276`, `:340–:365`, `:525–:580`, `:684–:694`;
  - the locked template `:35–:83`;
  - checklist `:440–:512`, `:536`;
  - umbrella `:108`, `:225`, `:514`, `:556`, `:563`, `:647`;
  - TB-W1 read `:128–:140`;
  - Track A `:204`, `:236`;
  - the halt/resume contract `:36`;
  - `book_runtime.py`, `book_protocol.py`, `book_policy.py` and `c1_sizing_host_reference.py` at the cited lines;
  - the 6J, MNQ, YM and MYM ledgers, and RESULTS.md, at the cited lines;
  - #583 note (all) at `8387e66`.
- Web: WebFetch of the TradingView support page 43000691027. WebSearch excerpts for CME 6J, MNQ, MGC and MYM. Three WebFetch calls to cmegroup.com timed out.
- No private data, Pine source or port was read. No provider was contacted.

## Addendum 2026-10-04 — hyper's requirements-simplification proposals: operator dispositions

**Decision:** Joshua, 2026-10-04T00:17:19Z, to coordinator (4): "go on the proposal dispositions and open-3/4 as recommended". The proposals came from hyper's scrutiny worker at main `822c3ea`, relayed by Codex Coordinator 2 on 2026-10-03. They were recommendations only; this records which are adopted.

1. **Live month-end-adjacent session: rejected.** The adopted window minimum stays as frozen (spec §16.2). Removing it would need a §13 re-opening, and the saving may be zero.
2. **Window start: adopted for the OPEN-8 binding.** The window may open at the first complete permitted session after collection starts, not only at a Sunday 18:00 ET open. Every adopted minimum is kept, including two Sunday opens inside the window. The text is written when OPEN-8 is bound. **OPEN-4 per-leg evidence:** supplied by the coordinator's panel read and cited in the OPEN-4 binding.
3. **Provider late/missing data versus collector evidence loss: adopted as a separate pre-data §13 body amendment,** drafted together with the "capture incomplete" definition and §7 completeness (§4 question 6). It must use independent liveness and transport-completion evidence; a generic heartbeat is not completion proof. It is not part of any OPEN binding. The coordinator owes the draft before CP-6.
4. **Funded, emission-disabled collection overlap: deferred.** T00 is not shown to be the final CP-7 blocker. Revisit only if it is.
5. **FEED-16 shadow reuse for live-only warm-up: accepted as already permitted;** no change.
