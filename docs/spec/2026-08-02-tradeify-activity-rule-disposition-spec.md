# SPEC — Tradeify weekly-activity-rule disposition: the option set

**Type:** Options spec for an operator ruling (decision artifact, `docs/spec/`)
**Status:** `CLOSED — MOOT 2026-08-04` — no option is recommended-by-default; §6 is **not** a live ruling gate (F1(b) reversed next day)

> ⚠ **CLOSED — MOOT 2026-08-04 — do not rule, do not build.**
> ADR [`2026-08-04`](../adr/2026-08-04-tradeify-venue-descope-eval-included.md) §3 **reversed** the
> F1(b) "hold the eval through 2026-11-08" ruling this entire options card rests on. §3 arithmetic
> (~14 weeks / ~4 instances / P(≥1) ≈ 98.6% / "the live set is B or C") is **premise-dead**.
> §6 item 1's "✅ DISCHARGED" for F1(b) is **void**. The residual question (keep the account at all)
> is fork **F2**, which subsumes this card; Option D is a branch F2 may elect.
>
> **PRESERVED as live F3 inputs:** the Rule-13 venue-fact table (idle → warning → permanent
> deletion, no reinstatement, no refund, both phases) and §1's measured cadence exposure —
> **including that the WATCH-1 haircut *worsens* it 93.57% → 97.63%**.

> # ⚠ CORRECTED 2026-08-03 — THE CENTRAL UNKNOWN IS NOW ANSWERED, AND IT INVERTS THE RANKING
>
> This spec was authored on the reading that the idle rule is **soft-edged** (*"may result in your
> account being marked as inactive… we will message you before we take any action"*), and it ranked
> **Option C (accept the warnings)** as the cheap branch whose only defect was that its downside was
> **unpriced**. **That downside is now priced, and it is the most adverse venue fact on this account:
> the account is DELETED, irreversibly, with no reinstatement and no refund.**
>
> Recorded upstream 2026-08-02 as
> [`TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md` §2a](../notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md)
> from a **second** help-centre article this spec never consulted. **§4 H3 is therefore FALSIFIED
> exactly as it predicted**, and the **P0 support question §3 recommended is answered without asking.**
>
> Corrections are applied **at each assertion site below** (Rule 14: living docs are corrected where
> the error is read, not by an appended addendum; this spec is `OPEN` and same-session work is never
> frozen). Superseded text is struck rather than deleted.
**Authored:** 2026-08-02
**Owner of the obligation:** [`TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md` §2 + §4a](../notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md)
**Companion:** [`2026-08-04-tradeify-venue-descope-eval-included.md`](../adr/2026-08-04-tradeify-venue-descope-eval-included.md) (the 08-02 companion is a `Withdrawn` stub) — F2/F3 own the residual account question
**Layer:** ops disposition. **This spec authorizes nothing.** No code, no rail change, no trade, no arming, $0.

---

## §0 — Rule 0 reads (production source, verified 2026-08-02)

| Source | Anchor | What it grounds |
|---|---|---|
| `ops/c1_rail/c1_sizing_host_reference.py` | `c134060` 2026-07-24 | **`_SIGNAL_TYPES = frozenset({"entry", "add", "exit", "flat"})`** (line 100) — there is no token/keepalive signal type. `_REQUIRED_PAYLOAD_FIELDS` (101–102) includes `stop_dist_pts`. |
| `ops/c1_rail/c1_rail_http_server.py` | read this session | `_RISK_ADD_SIGNALS = {"entry","add"}` / `_FLAT_SIGNALS = {"exit","flat"}` (70–72) — an `entry` is **risk-sized** (`BASE_RISK × DD_SCALE × lifecycle`, integer-floored), not fixed-qty. |
| `core/mc/simulation.py` | `fc14682` 2026-07-30 | Lines 171–178: the modeled barrier is `consecutive_idle >= inactivity_limit` where activity ≡ `np.any(strategy_pnls != 0.0)` — a **rolling 5-consecutive-idle-business-day absorbing** rule. |
| `core/mc/preflight.py` | `fc14682` 2026-07-30 | Line 124 — `inactivity_limit` reads `f["inactivity_max_idle_days"]` unless the `INACTIVITY_OFF` idiom is passed. |
| `core/firm_rules.py` | `fc14682` 2026-07-30 | `Tradeify_Select_100K` printed in full this session: `inactivity_max_idle_days: 5`, `cost_per_side_usd: 0.91`, `micro_contract_cap: 80`, `max_dd_pct: 3.0`. |
| `docs/notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md` | recorded 07-30, scope-corrected 07-31 | §2 (idle rule verbatim + soft-enforcement language), §3 (microscalping limbs), §1/§1a (automation identity; FTA §6.7(b)), §4a checklist. |
| `docs/briefs/programs/2026-07-23-tradeify-book-composition.md` | §5 item 5 | The standing prohibition this spec must route around: *"Manual token trades to satisfy the activity rule — off-spec discretion… Rail-level answer or accept warnings."* |
| `lab/analysis/c1/c1_cadence_inactivity_2026-08-02/RESULTS.md` | committed 2026-08-02 | Gap distribution + first inactivity-ON re-MC. |
| `STATE.md` operator queue | curated 2026-08-01 | *"operator-hours are the binding resource and were the only unrationed one"* — the cost axis Option B is scored on. |

**Venue facts, in [Rule 13](../operational_rules.md) form:**

| Quote (verbatim) | Source | Date read | Scope |
|---|---|---|---|
| *"**Maximum Account Idle Time (Funded and Evaluation Accounts)** — To keep your funded or evaluation account active, you must place at least one trade per week (Monday through Friday). This is per account, not per user."* | help.tradeify.co art. **10468318** | 2026-07-30 (in-browser; `WebFetch` 403s this host) | **BOTH PHASES** — the heading scopes itself explicitly. Binds the eval today. |
| *"may result in your account being marked as inactive… we will message you before we take any action"* | same article | 2026-07-30 | **STANDING** — gives the *status change* and the *procedure*. ~~The consequence of "marked as inactive" is nowhere defined.~~ **CORRECTED 2026-08-03 — it is defined, in a second article (next three rows).** |
| *"Funded and evaluation accounts require at least one trade per week (Monday-Friday) to remain active. **If inactive, your account will be deleted after an email warning.**"* | help.tradeify.co art. **12268494** (*Common FAQs*) | **2026-08-02** (in-browser; `WebFetch` 403s this host) | **BOTH PHASES — explicit, not inferred.** The answer names *"Funded **and evaluation** accounts"* in its own text, so it binds the c1 Select 100K eval **today**. No scope silence to resolve. |
| *"**Accounts removed due to inactivity cannot be reactivated.** Expired accounts cannot be reinstated - you would need to purchase a new account."* | same article | 2026-08-02 | **STANDING** — the loss is **permanent**. Combined with *"Tradeify does not offer refunds… all sales are final"*, an idle-week deletion forfeits the account **and** the purchase price. |
| *"**Can I pause or put my account on hold?** No. Accounts cannot be paused or put on hold for any reason."* | same article | 2026-08-02 | **STANDING** — forecloses "park the eval during a research pause" outright. Strictly stronger than C8 below, which only said parking is not *free*. |

| *"Microscalping applies ONLY to sim funded accounts. … you must meet BOTH: Over 50% of your trades are longer than 10 seconds; Over 50% your profit must come from trades held longer than 10 seconds."* | same article | 2026-07-30 | **SIM-FUNDED ONLY** — the source scopes it itself. Does **not** bind the eval. |

> **Composite rule (both articles govern; §Precedence, FTA §11): idle week → marked inactive →
> email warning → deletion, permanent.** Where the two differ in force (*"may"* vs *"will"*), the
> **conservative reading governs per Rule 13 — plan against deletion, not against a warning.**

---

## §1 — The symptom (stated without a fix baked in)

The `Tradeify_Select_100K` account carries a standing weekly obligation the book cannot meet on its own, and **no branch has been chosen, specified, or built** since the question was raised on 2026-07-23. The compliance surface is one unchecked box ([§4a](../notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md), *"Idle clock current"*). The idle clock is tracked nowhere in `ops/`.

**Measured exposure** (cadence RESULTS §1, on the committed 07-23 daily panel, 2020-08-04 → 2026-07-21, 1,556 bdays):

| Statistic | Value |
|---|---|
| Mon–Fri weeks with **zero** trades | **82 of 312 — 26.3%** |
| Longest consecutive dead-week run | **4 weeks** |
| Weeks with exactly one trading day | 45.2% |
| Mean trading days/week | 1.05 |
| Idle-bday gaps between trading days | median **3**, p90 **9**, p99 18, max **27** |
| Gaps ≥ 5 idle bdays | 83 of 328 (25.3%) |

So a keep-alive action is owed in roughly **1 week in 4**, and in the worst historical stretch **4 weeks running**.

**Why this is load-bearing rather than housekeeping.** The first inactivity-ON Tradeify re-MC (same RESULTS, §2) prices the assumption every published pass/bust pin in the repo silently makes: with the rolling-5-idle-bday barrier **on**, **92.6–97.6%** of paths die across all four arms. Those figures are **not a venue forecast** — the engine barrier is a hard rolling-5 absorbing rule while the venue rule is a soft Mon–Fri bucket satisfiable by a ~$2 trade — but they establish that *the mitigation is what the published numbers rest on.* It has never been built.

**Second-order finding from the same run, previously unnoticed:** the two survival levers pull against each other. The WATCH-1 0.50× haircut that makes the DD geometry pass (C2-on bust 23.35% → 3.54%) **raises** inactivity exposure (93.57% → 97.63%) by roughly doubling median days-to-pass (67 → 151). De-risking the drawdown problem worsens the cadence problem.

**Cost is not the issue.** ~$1.82 per instance (2 × `cost_per_side_usd` 0.91) plus a tick of adverse selection; ~14 instances/year; **≈$150 across the entire 6-year panel**. The open problem is **disposition**, not economics.

---

## §2 — Constraint set (binds every option below)

| # | Constraint | Source | Consequence for design |
|---|---|---|---|
| C1 | **Manual token trades are forbidden** — *"Rail-level answer or accept warnings"* | book-composition §5 item 5 (anchored on the CFD-retirement no-discretion doctrine) | Option B exists only if the operator rules that a **zero-discretion, pre-registered, fixed-size** desk action is not "off-spec discretion." **Not self-converted here** (Trap #12). |
| C2 | **No third party may place it** | FTA **§6.7(b)**, applies *"at all times and to every account type, including… evaluation accounts"*; §6.7(h) attaches account-death consequences | Delegation is closed. Not an option at any price. |
| C3 | **The rail has no token signal type** | `_SIGNAL_TYPES` = `{entry, add, exit, flat}`; `entry`/`add` are `_RISK_ADD_SIGNALS` and route through risk sizing | A token trade wants **fixed qty=1**, not `BASE_RISK × DD_SCALE × lifecycle` floored to an integer. Option A needs a new signal type or a qty override — **live-rail code**. |
| C4 | **`dry_run=true` blocks everything, including exits** | 07-28 code read, recorded in STATE.md queue item 3 | ⚠ **The paradox, and it is the hard part.** A token trade is owed precisely in weeks the strategies are quiet — i.e. weeks the rail would be **disarmed**. A rail-native sender must therefore either keep the rail armed all week (rejected: the 07-31 `armed_until` lapse self-bricked the host into an unbootable crash-loop) or be a **separate narrow path not gated by `dry_run`** — which is a new privileged send path on the only live execution surface. |
| C5 | **Attended-only** | GO ADR §1 operator election — **self-imposed, ADR-revisable**; explicitly **not** a Tradeify requirement ([compliance note §1](../notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md)) | An unattended scheduled token trade breaches **posture**, not a venue rule. Distinguishing these is what makes Option A adjudicable rather than automatically barred. |
| C6 | **HFT bots prohibited**; automation identity duties standing | art. 10468318 §Ownership; compliance note §1 | A weekly 1-lot is not HFT. But an automated token sender is *code enabled on this account* → the live-video / sole-ownership readiness duties attach to it too. |
| C7 | **Microscalping limb 1** — >50% of trades held >10s | art. 10468318; **SIM-FUNDED ONLY** | A token trade closed instantly is a sub-10-second trade and counts against limb 1. **Cheap fix: hold ≥ 11 seconds** — but it must be *designed in*, and no artifact has priced it. **Does not bind the eval**, and the companion ADR de-scopes the funded phase, so this constraint is dormant unless F1 reaches sim-funded. Limb 2 is unaffected (a ~$0 token trade contributes ~no profit either way). ⚠ If strategies are ever parked while the account is held, token trades become **~100%** of trade count and limb 1 fails outright on a funded account. |
| C8 | **Parking is not free — and pausing is not permitted at all** | compliance note §2: *"leaving the eval idle for a research pause is **not** zero-maintenance"*; ⚠ **strengthened 2026-08-03** by art. 12268494: *"**Can I pause or put my account on hold? No.** Accounts cannot be paused or put on hold for any reason."* | "Just pause the research" does not avoid the obligation — and there is no pause facility to invoke even if one wanted it. |

---

## §3 — The options

**Instances owed scale with the holding horizon**, so companion-ADR fork **F1** ("what is the eval now for?") is a hard input, not context.

**✅ F1 RULED 2026-08-02 (operator, chat): (b) — hold the eval through 2026-11-08.**

| F1 answer | Horizon | Instances owed | Which options are live |
|---|---|---|---|
| (a) rail proving-out only, then close | weeks | ~1–4 | *not chosen* |
| **(b) hold through 2026-11-08** ← **RULED** | **~14 weeks** | **~4** (14 × 0.263); P(≥1) ≈ **98.6%** | **B and C are the contest.** A is over-built; D defers to 11-08 by construction |
| (c) hold indefinitely | unbounded | ~14/yr | *not chosen* |

**What the ruling settles, and what it does not.**

- **Option A is off the table on cost, not on merit** — recorded, not deleted. Building a privileged `dry_run`-bypassing send path (C4) plus a new signal type (C3) plus an idle-clock tracker, landing *before* M1 is `RESOLVED`, to fire **~4 times**, is not a proportionate build. It returns if F1 is ever re-ruled to (c).
- **Option D is not rejected — it is scheduled.** F1(b) sets the account's purpose to expire at 2026-11-08. D is the natural disposition *at* that date and should be revisited there rather than re-derived.
- **⚠ The ~4 instances are not evenly spread.** The measured distribution has 5 runs of 3 consecutive dead weeks and 2 runs of 4 (§1). A 14-week window can contain a 4-week run, so any option must survive **four consecutive owed instances**, not four scattered ones. This is the constraint that separates B from C: four scattered desk actions are an annoyance, four consecutive ones inside one month are a pattern the venue's soft enforcement may notice.
- **The rationale under which (b) was drafted was corrected in the same ruling** — see the companion ADR §7. The eval is held for B7 Stage-1 / M1 / first live fill / execution-quality data, **not** as §4 evidence (§4 discharges on simulation). This matters here because it means the hold's value is **front-loaded**: queue items 1–3 are targeted at the 08-04 → 08-14 session window, so most of what F1(b) buys is purchasable in the first three weeks, while the activity obligation runs the full fourteen. If items 1–3 discharge early, re-ruling F1 to (a) becomes available and the residual instance count drops toward zero.

---

### Option A — Rail-native scheduled token sender

A narrow, separately-scoped send path: a fixed **qty=1 MYM** round trip, fired on a schedule (e.g. Thursday 10:00 ET if no fill recorded that Mon–Fri week), held ≥11 seconds, then flattened.

**Build surface** (all on the live rail — this is the cost):
1. New signal type or a `qty_override` field bypassing risk sizing (C3) — plus its own tests, since `entry` currently implies `stop_dist_pts` and reserve-cap logic that a token trade must not touch.
2. A send path **not gated by `dry_run`** (C4), with its own arm/disarm semantics narrower than the strategy path.
3. An idle-clock tracker (nothing in `ops/` tracks it today) with a Mon–Fri bucket, not a rolling counter — the engine's rolling-5 rule is **not** the venue's rule.
4. Telemetry/EventLedger events so a token fill is distinguishable from a strategy fill in every downstream reconcile.

- **Satisfies:** C1 (rail-level, the brief's own named branch), C2, C7 (hold floor designed in).
- **Breaches:** C5 posture, unless fired only inside attended windows — which reintroduces the operator-hours cost Option B carries.
- **Real risk:** a privileged send path that ignores `dry_run` on the operation's only live execution surface is exactly the class of thing the M1 monitoring ADR exists to gate. It would want its own acceptance item, and it lands **before** M1 is `RESOLVED`.
- **Honest verdict:** correct at F1(c), over-built at F1(a)/(b).

### Option B — Attended token trade inside a scheduled desk session

A pre-registered, zero-discretion desk action: fixed instrument, fixed qty=1, fixed time, no judgment. Placed by the operator during a deliberately scheduled short session in weeks the book was quiet.

- **Satisfies:** C2, C3 (no code at all), C6, C7.
- **Blocked on:** **C1 adjudication.** The brief bars "manual token trades" as off-spec discretion. Whether a fixed-size, fixed-time, pre-registered action *is* discretion is an interpretation the operator owns — I have not converted it. Note the precedent shape: the CFD-retirement anchor targets *in-the-moment judgment on strategy signals*, which this is not.
- **Real cost:** it spends the binding resource. STATE.md's own framing — *"operator-hours are the binding resource and were the only unrationed one"* — and this converts 26.3% of weeks into a scheduled desk obligation, including the 4-week runs. At F1(c) that is ~14 sessions/year for zero informational return.
- **Honest verdict:** cheapest to build, most expensive to run.

### Option C — ~~Accept the warnings~~ **ACCEPT NEAR-CERTAIN ACCOUNT DELETION** ⚠ CORRECTED 2026-08-03

Do nothing. Let the account be flagged; respond if Tradeify messages.

- **Satisfies:** everything trivially. $0, no code, no operator hours. It is the brief's own second named branch.
- ~~**The problem:** the cost is **unpriced**. *"Marked as inactive"* is undefined in every source read — it may be a flag, a reset, a suspension, or account closure. The compliance note records the rule as **real** while its enforcement is soft-edged. Nobody has asked.~~
- **THE COST IS NOW PRICED, AND IT IS THE ACCOUNT.** Art. 12268494: *"If inactive, your account will be **deleted** after an email warning"* · *"Accounts removed due to inactivity **cannot be reactivated**"* · no refunds, *"all sales are final… regardless of whether they have been traded on."* Option C is therefore not "absorb some warnings" — it is **wagering the registered eval and its $159 purchase on never missing a Mon–Fri week.**
- **Against the measured cadence that wager is near-certain to lose.** 26.3% of weeks are zero-trade; over F1(b)'s ~14-week hold **P(≥1 idle week) ≈ 98.6%**, and the worst historical stretch is **4 consecutive** dead weeks — an email warning followed by continued silence, which is the documented path to deletion.
- ~~**Bounded by horizon:** at F1(a) the exposure is 1–4 warnings over a few weeks against an account whose purpose is nearly discharged. At F1(c) it is an unbounded unknown compounding indefinitely.~~ **Horizon no longer bounds the downside**, because the downside is discrete and terminal rather than accumulating: **one** unanswered warning ends the account at any horizon. A shorter hold reduces the number of chances to trip it; it does not reduce the severity of tripping it once.
- **Residual argument for C, stated fairly:** the warning is a real interlock — deletion follows *"after an email warning"* — so an attended operator reading mail promptly could place a trade inside the warning window. **But that mitigation is Option B under another name** (a manual token trade) and inherits C1's prohibition, plus an unknown warning-window length. It is not a distinct option.

### Option D — Discharge the obligation by closing the account

Not a way to *satisfy* the rule — a way to stop owing it. Once the eval's stated purpose (F1) is discharged, close the account; the weekly duty ends with it.

- **Satisfies:** everything, permanently.
- **Cost:** forfeits the registered eval and the spend already committed against it; any later Tradeify work starts from a fresh purchase. Requires F1 to be answered *first* — closing an account whose purpose is unstated is the same error in the opposite direction.
- **Honest verdict:** this is the option F1(a) implies, and it should be named as such rather than arrived at by attrition.

---

### P0 — The pre-flight that dominates the ranking (recommended regardless of option)

⚠ **CORRECTED 2026-08-03 — P0 IS ANSWERED, AND NOT BY ASKING.** ~~One support question prices Option C and costs nothing else. Option C is currently unrankable because its downside is an undefined term.~~ A **second help-centre article (12268494) answered it directly** — deletion, permanent, no refund. **Do not send the idle-rule question; it is closed.** The §1b Approved-Platforms question remains genuinely open and is still worth bundling into any future support contact. **Method lesson, recorded because it recurred twice this session: the answer was already published — the gap was that only ONE article had been read.** Silence in one source is not absence of a rule (Rule 13); search the sibling articles before pricing an unknown.

> *"If an evaluation account goes a Mon–Fri week without a trade, what does 'marked as inactive' mean in practice — is the account flagged, paused, reset, or closed, and is there a warning count before any action?"*

Bundle it with the §1b Approved-Platforms question already drafted in the compliance note, since both are cheap and neither is urgent alone. **If the answer is "flagged, with warnings and no reset," Option C likely dominates at every F1 horizon and this spec closes at $0 and zero build.**

---

## §4 — Falsifiable hypotheses

**H (the claim this spec rests on, binary):** *the weekly-activity obligation is a real, recurring, unmitigated exposure on the registered account, and it requires a disposition rather than being self-resolving.*

**If** the obligation is real (H1), recurring at the measured rate (H1), cheap in money but not in disposition (H2), and carrying an unpriced downside (H3), **then** a §6 ruling is required; **otherwise** — if any trigger below fires — this spec closes `FALSIFIED` and the §4a checklist item is struck without any option being built.

| # | Hypothesis | Falsified if | Consequence |
|---|---|---|---|
| H1 | **The exposure is real and recurring.** P(≥1 dead Mon–Fri week before 2026-11-08) ≈ **98%**, from 82/312 measured zero-trade weeks over 14 remaining weeks | 14 consecutive Mon–Fri weeks pass with ≥1 fill each and no flag | The 07-23 panel does not describe the live account's cadence; re-derive §1 before ruling |
| H2 | **Cost is disposition, not money.** Full compliance ≤ **$50/yr** (14 × $1.82 = $25.48 + slippage) | Any option's measured direct cost exceeds **$50/yr** | Economics re-enters the ranking; re-score §3 on a cost axis |
| H3 | ~~**Option C is unranked, not cheap.** No source defines the consequence of an inactivity flag~~ | ~~P0 returns a definition~~ | **✅ FALSIFIED 2026-08-03, exactly as this row predicted** — art. 12268494 defines it: **deletion, permanent, no refund**. §3 re-ranked with C priced. The hypothesis worked: it named its own falsifier and the falsifier fired. |
| H4 | **The microscalping interaction is neutralizable.** A ≥11s hold clears limb 1 at any instance count | The venue measures hold time other than fill-to-fill, **or** limb 1 is measured over a window token trades can dominate | C7 becomes a hard constraint on A and B at any funded horizon |
| H5 | **The rule binds this account at all.** Art. 10468318 scopes itself *"(Funded and Evaluation Accounts)"*; **art. 12268494 independently names *"Funded and evaluation accounts"* in the deletion answer** | the article is withdrawn/rescoped on re-verify | **Spec closes `FALSIFIED`** — no option is built, §4a item struck, compliance note updated. ⚠ **2026-08-03: this limb is now much harder to falsify** — two independent help-centre articles scope it to evaluations explicitly, so the earlier "P0 returns that evaluations are not enforced" route is closed. |

**Note the asymmetry:** H5 is the only limb whose falsification closes the spec outright. H1–H4 falsifying changes the *ranking*, not the need for a ruling.

---

## §5 — Forbidden moves (under this spec)

- **Self-converting the C1 prohibition.** Genuinely tempting: Option B is the cheapest path and the argument that "a fixed pre-registered action is not discretion" is a good one. It is still an **interpretation change to a §5 forbidden move in a ratified brief**, and reading a rule in the direction the convenient option needs is Trap #12. The operator converts it or it stays barred.
- **Building Option A before F1 is answered.** It is the most *satisfying* option and the only one that scales — and at F1(a) it is weeks of live-rail work for ~2 token trades. Build order follows the horizon, not the elegance.
- **Adding a `dry_run`-bypassing send path without its own acceptance gate.** The whole point of M1 is that privileged paths on the live rail get attested. A keep-alive that ignores the master safety flag is not a small feature.
- **Quoting the 92.6–97.6% inactivity figures as a Tradeify forecast.** They price the token-trade *assumption* under a hard rolling-5 absorbing barrier; the venue rule is a soft Mon–Fri bucket. The cadence RESULTS §2 says so prominently and this spec inherits that caveat.
- **Treating "park the research" as avoiding the problem.** C8 — parking is the obligation, not an escape from it.
- **Letting the idle clock stay untracked while declaring an option chosen.** Any option except D requires knowing which week is at risk; no surface tracks it today. A ruling without a tracker is a ruling that silently becomes Option C.

---

## §5a — ✅ RULED 2026-08-03: **Option A** — and what it actually requires before code

**Operator ruling, verbatim: *"rule option A, the rail-level token sender"*.** Recorded. §6's
limb 2 is discharged; the spec's remaining life is the implementation path below.

**A is buildable, but three things gate it, and two of them are governance, not engineering.** None
is a reason to re-open the ruling; all three change *what gets built and in what order*.

### Blocker 1 — M1 is `CODE_LANDED`, not `RESOLVED`

`M1_MONITORING_ACCEPTANCE.json` reads `status: CODE_LANDED` today. The monitoring ADR's
**Addendum 2026-07-31b (operator-ratified)** is unambiguous: **"`dry_run=false` may not be set while
M1 is not `RESOLVED`."** A sender that routes real orders is doing that, under whatever flag name it
carries. **So A cannot ship into a live-sending state before M1 resolves** — the remaining M1 field
is `operator_signoff`, itself gated on B7-REFIRE Stage 1 (~~operator-queue item 1~~ **STRUCK 2026-08-06 (M35)** — queue row deleted by ADR §6; desk-carded for
2026-08-04).

### Blocker 2 — `armed_until` is hours-scoped by design, so "unattended weekly" has no safe expression

`ops/c1_rail/c1_rail_arm.py` takes `--arm --hours N` and computes `deadline = now + timedelta(hours=hours)`;
the boot gate **refuses to start** if `dry_run=false` without a valid *future* deadline (the 2026-07-31
self-brick was an expired one, recovered only by entrypoint override). **There is no standing-armed
state, deliberately.** An unattended weekly sender therefore needs either:

- an `armed_until` measured in **months** — i.e. the rail continuously live-armed, which is precisely
  the failure mode the design exists to prevent; or
- **weekly re-arming** — which is Option B's operator-hours cost plus a build.

> ⚠ **Consequence, stated plainly: A's headline benefit — removing operator hours — is partly
> illusory as specced in §3.** If A is realized by re-using the strategy path's arm flag, it does not
> deliver the thing it was chosen for. That is an argument about *design*, not about the ruling.

### Blocker 3 — arming is operator-only, and the bypass is the same act

The 2026-08-02 agent-authority grant is explicit: deploy **yes**, disarm **yes** (flat-verified
first), status **yes**, **`--arm` no** — *"a standing boundary, not an unlifted restriction… do not
re-litigate it as stale policy or route around it (e.g. by hand-editing `/data/c1_rail_config.json`,
which is the same act with the audit trail removed)."* **A send path that ignores `dry_run` is that
act under a different name**, so §3's build item 2 ("a send path not gated by `dry_run`") is **not
buildable as written** and must be replaced.

### The design that survives all three

Not a `dry_run` bypass — an **independently-gated keepalive path with a hard blast-radius cap**:

| Property | Value | Why it is the load-bearing constraint |
|---|---|---|
| Instrument | **MYM only** | granularity-tolerant; MNQ zero-floors at qty 1 anyway |
| Quantity | **fixed 1**, never risk-sized | bypasses `BASE_RISK × DD_SCALE × lifecycle` entirely — no pyramid, no `reserve_cap` interaction |
| Frequency | **≤1 order per Mon–Fri week**, enforced in code | the obligation is exactly one trade/week |
| Hold | **≥11 s**, then auto-flat | clears microscalping limb 1 (C7) if the account ever reaches sim-funded |
| Gate | its **own** enable flag + expiry, **operator-set**, never the strategy `dry_run` | keeps the strategy path disarmed and auditable; the keepalive cannot arm the book |
| Blast radius | **~$5–10** per instance (1 MYM round trip, ~$1.82 commission + a tick) | vs the $3,000 trail — this is the argument that justifies a separate, longer-lived gate at all |

**That last row is the whole case.** A qty-1 MYM keepalive is a categorically different risk object
from arming the pyramided book, and it is the only basis on which a longer-lived enable flag could be
defensible. **It still needs an ADR** — one that (a) carves the keepalive out of the M1 arm gate on
blast-radius grounds, (b) revises the attended-only posture for this path only (GO ADR §1 is
self-imposed and ADR-revisable — it is *not* a venue rule), and (c) records the operator as the sole
enabler.

### Recommended order

1. **ADR first, code second.** Two of three blockers are governance; writing code against an
   unresolved M1 gate would produce a sender that cannot legally be switched on.
2. **B7 Stage-1 (08-04) is upstream of this anyway** — it feeds `operator_signoff`, the last M1 field.
   The keepalive ADR and M1 resolution are naturally sequenced, not competing.
3. **Interim exposure is real and must be named:** until the sender exists, the account is on
   Option C by default, now priced at **deletion** (§3). Over the F1(b) hold that is
   **P(≥1 idle week) ≈ 98.6%**. If the ADR route takes more than a few weeks, an explicit interim
   decision is owed — not silence, which *is* Option C.

**Not authored here.** The ADR is the next artifact; this section is its input, and writing both in
one pass is how a design gets fitted to whatever the author already wants to build.

---

## §6 — Gate criteria (binary — this is the ruling)

**The spec closes `RESOLVED` when both of the following hold:**

1. ~~**F1 is answered** in the companion ADR §7 — (a), (b), or (c).~~ **✅ DISCHARGED 2026-08-02 — ruled (b), ~14 weeks, ~4 instances.**
2. **Exactly one** of A / B / C / D is ratified for that horizon, in writing, with its named cost accepted. **← the only limb still open.** Under F1(b) the live set is **B or C**; A is over-built at 4 instances and D is the scheduled 2026-11-08 disposition rather than a present choice.

**Sequencing under F1(b), given the first owed instance can arrive within days:** the 08-04 desk session is a *scheduled* attended window, so the week of 08-04 is covered whether or not a strategy signal arrives — item 1's own rule is that a session counts *"whether or not a signal arrives"*, but note that only counts the **session**, not a **trade**. A session with no fill leaves the idle clock unsatisfied. **This is the first live decision point and it is inside the week**, which is why P0 should be sent now rather than after a ruling.

**`FALSIFIED`** if §4 H5 fires — a primary-source read or P0 establishes that the weekly rule does not bind an evaluation account, or the rule is withdrawn. Then **no option is built**: the §4a checklist item is struck, the compliance note records the re-scope with its quote/source/date in Rule-13 form, and §1's exposure statistics become historical. This is a real and reachable branch — the venue has already rescinded one rule this repo carried (the mini/micro mixing clause, 2026-07-29), and the idle rule's own enforcement language is the softest of any Tradeify rule tracked here.

~~**`RESOLVED-DEFERRED`** if P0 is run first and the operator elects to rule after the answer returns.~~ ⚠ **CORRECTED 2026-08-03 — this verdict is no longer available on the idle-rule limb:** P0 is answered, so there is nothing to defer *for*. And the decay clause is now severe rather than tidy: **absent a ruling this decays into Option C, which is now near-certain account deletion** (§3). A deferral here is not a neutral holding position.

**`AMBIGUOUS`** if F1 is answered but no option is ratified. Record it as such rather than letting silence stand — **silence *is* Option C, which is now priced at the loss of the account and the purchase**, not merely "chosen without pricing it" (⚠ corrected 2026-08-03).

**Discharge conditions per option:**

| Option | Discharged when |
|---|---|
| A | ⬅ **RULED 2026-08-03 (§5a).** Discharged when: keepalive **ADR accepted** (M1 carve-out + attended-only revision + operator-as-sole-enabler) · **M1 `RESOLVED`** · sender deployed with its own acceptance item green · idle-clock tracker live · first token fill observed and distinguishable from a strategy fill in telemetry. **Not discharged by code alone** — blockers 1–3 in §5a are prerequisites, not caveats. |
| B | C1 adjudicated in writing, desk-card template exists, first attended instance executed |
| C | Ruled in writing with P0's answer (or an explicit acceptance of the unpriced risk) recorded in the compliance note §4a |
| D | Account closed; §4a checklist item struck; compliance note updated |

---

## §10 — Audit hooks (runnable)

```bash
# 1. The obligation is still untracked (the premise of §1)
rg -n "idle|inactivity|token.trade|keepalive" ops/ --glob '!*.md'
# Expected today: only core/mc/* modeling references — nothing in the ops rail tracks a Mon-Fri idle clock

# 2. The rail still has no token signal type (C3)
rg -n "_SIGNAL_TYPES|_RISK_ADD_SIGNALS|_FLAT_SIGNALS" ops/c1_rail/c1_sizing_host_reference.py ops/c1_rail/c1_rail_http_server.py
# Expected: {entry, add, exit, flat} only

# 3. The compliance checkbox is still open (the surface of record)
rg -n "Idle clock current" docs/notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md
# Expected: "- [ ]" while this spec is OPEN; "- [x]" only after a §6 discharge

# 4. The C1 prohibition is unedited unless the operator converted it
rg -n "Manual token trades" docs/briefs/programs/2026-07-23-tradeify-book-composition.md
# Expected: byte-unchanged §5 item 5 unless a dated operator ruling says otherwise

# 5. Reproduce the exposure statistics
python lab/analysis/c1/c1_cadence_inactivity_2026-08-02/gap_cadence.py
# Expected: 82/312 zero-trade weeks (26.3%), max run 4, median gap 3, p90 9

# 6. Venue facts still current (90-day re-verify; browser read — WebFetch 403s this host)
# help.tradeify.co art. 10468318 — "Maximum Account Idle Time (Funded and Evaluation Accounts)"
rg -n "at least one trade per week" docs/notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md
```

---

## Verification

```bash
python "$HOME/.claude/skills/brief-authoring/scripts/check_brief.py" docs/spec/2026-08-02-tradeify-activity-rule-disposition-spec.md --type inquire

# Rule 0 anchors (§0) still current
for f in ops/c1_rail/c1_sizing_host_reference.py core/mc/simulation.py core/mc/preflight.py core/firm_rules.py; do git log -1 --format="%h %ci $f" -- "$f"; done
# Expected: c134060 / fc14682 / fc14682 / fc14682

# The engine barrier is the rolling-5 rule this spec describes (§0, §1)
sed -n '171,178p' core/mc/simulation.py

# Tier constants quoted in §0/§1 reproduce
python -c "import sys;sys.path.insert(0,'.');from core.firm_rules import FIRM_RULES as F;t=F['Tradeify_Select_100K'];print(t['inactivity_max_idle_days'], t['cost_per_side_usd'])"
# Expected: 5 0.91
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-02 | Initial authoring. Four options + a dominating P0 pre-flight. Two findings not previously recorded: the **`dry_run` paradox** (C4 — a keep-alive is owed exactly when the rail is disarmed, and `dry_run=true` blocks exits too) and the **microscalping interaction** (C7 — an instantly-closed token trade counts against limb 1; neutralized by an ≥11s hold, dormant while the funded phase is de-scoped). No option recommended by default; C1 adjudication deliberately not self-converted | Claude Code |
