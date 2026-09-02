**Theme:** c1
# c1 cadence / inactivity — gap distribution + first inactivity-ON re-MC

> ⚠ **§2's enforcement premise is SUPERSEDED — read [Addendum 2026-08-02b](#addendum-2026-08-02b--the-enforcement-premise-in-2-is-superseded-the-venue-deletes-the-account) before relying on the semantics caveat.**
> The caveat's *"soft-enforced, warning first"* half is wrong: the venue **DELETES the account,
> irreversibly** (art. 12268494 — *"deleted after an email warning"*, *"cannot be reactivated"*).
> Every measured number stands; what changes is the reading of finding 3. Body unedited (Trap #12);
> this banner is the reader-intercept (operational_rules.md Rule 14).

**Status:** ACTIVE — token trade owed 82/312 Mon–Fri weeks (max 4 consecutive); 0.50× haircut raises inactivity exposure

**Date:** 2026-08-02. **Trigger:** operator question ("Striker trade frequency doesn't help
with the weekly inactivity rule") + a two-agent record sweep that established both target
statistics were **absent**: no gap distribution for the c1 book exists anywhere in the repo,
and no Tradeify-tier simulation has ever read `inactivity_max_idle_days` (every published
run uses the `INACT_OFF` idiom — `core/mc/preflight.py:70-79` default, futures3 / selectflex
/ eval-lock-correction drivers). Read-only compute on committed inputs; **no K spend, no
manifest, no gate moved, no locked surface touched.**

## §0 — Anchors (reproduced before anything new was read off)

Panel: [`lab/analysis/c1/tradeify_book_composition_2026-07-23/out/daily_panel.csv`](../tradeify_book_composition_2026-07-23/out/daily_panel.csv)
(committed 2026-07-23 vintage; MYM n=263 / MNQ n=262 exports; backtest sizing; 2020-08-04 →
2026-07-21, 1,556 bdays). This run reproduces its published anchors before reporting
anything novel:

| Anchor | Published | This run |
|---|---|---|
| Zero-trade Mon–Fri weeks | 27% ([book-composition brief §2](../../../docs/briefs/programs/2026-07-23-tradeify-book-composition.md)) | **26.3%** (82/312) |
| Winning days ≥$200 / month | 1.02 panel (`repro_capbound_before_snip.txt`) | **1.01** |
| MYM / MNQ trading days | 191 / 190 ([third-leg spec](../../../docs/spec/2026-07-27-third-leg-target-spec.md) entry rates 191/623, 190/623) | **191 / 190** |

**Cohort caveat (binding):** this is the panel-geometry (backtest-sizing) daily panel, **not**
the rail-geometry panel behind the published bust pins (2.65% / 4.74% / 1.20%). Absolute
pass/bust levels in §2 are **not comparable to those pins** and must not be quoted against
them. The deliverables are (§1) the cadence distribution, which is sizing-invariant at the
zero/non-zero level, and (§2) the inactivity OFF→ON **delta** at fixed everything else.

## §1 — Gap distribution (`gap_cadence.py` → `out/gap_cadence.log`, `out/gap_stats.json`)

First write-down of the statistics the record sweep found absent:

- **Active days:** 329/1,556 (21.1%, z=0.789). Days both legs trade: 52; corr(daily P&L on
  those days) = **−0.13**.
- **Idle bdays between consecutive trading days:** median **3**, p90 **9**, p99 **18**,
  **max 27**. Gaps ≥5 idle bdays: **83 of 328 (25.3%)**. Per leg: MYM median 4 / max **52**;
  MNQ median 4 / max **55**.
- **Mon–Fri weeks (the venue rule's unit,** art. 10468318**):** **82 of 312 (26.3%) have
  zero trades**; 45.2% have exactly one; mean trading days/week 1.05.
- **Consecutive dead-week runs:** 41×1wk, 9×2wk, 5×3wk, **2×4wk** (longest **4 weeks**). A
  token trade is owed in 82 of 312 weeks; the worst historical stretch owes 4 in a row.
- Winning-day rate 41.3% (≥$200: 22.2%); single-day tails +$18,470 / −$1,991. (Note the
  −$1,991 is panel-geometry; Q-GEOFIT-1's −$744 worst day is the $100K-scaled book — different
  sizing, not a contradiction.)

## §2 — Inactivity-ON re-MC (`inactivity_on_remc.py` → `out/inactivity_remc.log`, `.json`)

`Tradeify_Select_100K`, 10,000 × 3 seeds, seeds identical across arms.
**Geometry: corrected eval trail** — `dd_lock_offset_usd` overridden to `1_000_000.0`
(unreachable lock = pure fixed-$3,000 EOD trail, the
`tests/core/test_trailing_locking_boundary.py` idiom), attested in the log. The disk default
`100` (the `firm_rules.py` OPEN-DEFECT lock the eval does not have) was **not** used — using
it silently is the exact `lesson_driver_layer_fix_leaves_kernel_default_stale` trap. In-parent
execution, no process pool, so the worker re-import trap does not apply.

| Arm | pass | bust (DD-class) | **bust_inactivity** | med days-to-pass |
|---|---|---|---|---|
| C2-off · 1.00× · inact OFF | 68.07% | 31.93% | 0.00% | 52 |
| C2-off · 1.00× · inact ON | 6.34% | 1.06% | **92.60%** | 11 |
| C2-off · 0.50× · inact OFF | 87.61% | 12.39% | 0.00% | 131 |
| C2-off · 0.50× · inact ON | 2.39% | 0.02% | **97.59%** | 11 |
| C2-on · 1.00× · inact OFF | 76.65% | 23.35% | 0.00% | 67 |
| C2-on · 1.00× · inact ON | 6.10% | 0.33% | **93.57%** | 11 |
| C2-on · 0.50× · inact OFF | 96.46% | 3.54% | 0.00% | 151 |
| C2-on · 0.50× · inact ON | 2.37% | 0.00% | **97.63%** | 11 |

**Semantics caveat (prominent, load-bearing):** the engine's barrier is a **rolling
5-consecutive-idle-bday absorbing** rule (`core/mc/simulation.py:171-178`); the venue rule is
a **Mon–Fri bucket, soft-enforced, warning first**, satisfiable by a ~$2 token trade. And
`build_week_blocks` samples Mon-anchored 5-day blocks, so any fully-dead week block *is* a
5-idle-day run — with 26.3% dead weeks, absorption is near-certain by construction. **These
numbers are not a Tradeify forecast.** They price the assumption every published figure
makes: without the token-trade mitigation, the book does not survive a strict activity
barrier. The ON-arm "passes" (~2–6%, median 11 days) are the sprint tail that reaches +6%
before ever hitting a dead week — a selection effect, not a strategy property.

## §3 — Findings

1. **The token-trade assumption is load-bearing, now measured on-venue-tier.** 92.6–97.6%
   path death across all arms — independently reproducing Bulenox C5's ~96%
   ([`RESULTS_C5_integer_2026-07-03.md`](../../archive/bulenox_futures_remc_2026-07-01/RESULTS_C5_integer_2026-07-03.md)
   finding #2) on a different venue tier, panel vintage, and sizing. The mitigation the MC
   assumes is the only reason the published pass/bust figures exist.
2. **NEW — the two survival levers pull against each other.** The WATCH-1 0.50× haircut is
   what makes the DD geometry pass (C2-on: bust 23.35% → 3.54%), but it **raises** inactivity
   exposure (93.57% → 97.63%) because it lengthens median days-to-pass (67 → 151), roughly
   doubling the number of Mon–Fri weeks the eval must survive with a 26.3% dead-week rate.
   De-risking the drawdown problem worsens the cadence problem. No prior artifact had
   noticed this interaction. Panel-geometry measurement; a rail-geometry (integer-sized)
   re-run is the bounded follow-up if this is ever consumed at gate grade.
3. **The idle-rule exposure statistic for operations is §1's, not §2's:** a token trade owed
   in **26.3% of weeks, max 4 consecutive**, at ~$1.82 RT + a tick of risk per instance
   (≈$150 cumulative over the 6-year panel). The cost is negligible; the open problem is
   *disposition*, not economics — the
   [book-composition brief §5 item 5](../../../docs/briefs/programs/2026-07-23-tradeify-book-composition.md)
   forbids manual token trades ("Rail-level answer or accept warnings") and neither branch
   has been chosen, specified, or built. The compliance surface remains one unchecked
   checkbox ([`TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md` §4a](../../../docs/notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md)).

## §4 — What this does NOT license

- **No token trade is authorized by this analysis** — the §5 forbidden move in the
  book-composition brief stands; the rail-level-vs-accept-warnings choice is an operator
  decision (routed to the 08-08 packet via STATE.md).
- **No published pin is impeached.** Inactivity-off was an explicit, documented modeling
  choice (`firm_rules.py:188-194` says so in as many words); this analysis prices it, it
  does not refute it.
- **No gate moves.** Finding 2 bears on how the c1 GO ADR §6 WATCH-1 figures are *read*
  (they are DD-survival figures, silent on cadence exposure), not on their values.

## Reproduction

```bash
python lab/analysis/c1_cadence_inactivity_2026-08-02/gap_cadence.py
python lab/analysis/c1_cadence_inactivity_2026-08-02/inactivity_on_remc.py
```

Both read only committed inputs (`daily_panel.csv`); deterministic seeds from
`core/portfolio_mc.py` (`SEEDS`, `SIMS_PER_SEED`); outputs under `out/` are committed.

---

## Addendum 2026-08-02b — the enforcement premise in §2 is superseded: the venue DELETES the account

**Body above is unedited** (house discipline: the impeachment lives in the addendum). **No number in
this analysis moves, and no finding is withdrawn** — what changes is one clause of the semantics
caveat and, with it, the reading of finding 3.

**§2's semantics caveat describes the venue rule as** *"a Mon–Fri bucket, **soft-enforced, warning
first**, satisfiable by a ~$2 token trade."* The *soft-enforced* half is **wrong**, and it was
inherited in good faith — article 10468318 states only the status change (*"marked as inactive"*)
and the procedure (*"we will message you before we take any action"*) and **never states the
action**. A **second governing help-centre article does**: [12268494 *Common FAQs*](https://help.tradeify.co/en/articles/12268494-common-faqs),
read in-browser 2026-08-02 —

> *"If inactive, your account will be **deleted** after an email warning."*
> *"Accounts removed due to inactivity **cannot be reactivated**."*
> *"Accounts **cannot be paused or put on hold for any reason**."*

Scope is explicit in the source (*"Funded **and evaluation** accounts"*), so it binds this eval.
Composite rule: **idle week → marked inactive → email warning → permanent deletion.** Authoritative
record: [`TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md` §2a](../../../docs/notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md).

**What survives untouched:**

- Every measured quantity in §1 and §2, and the §0 anchor reproductions.
- The caveat's **purpose** — these MC numbers are *not* a venue forecast. That was right and is
  reinforced: the engine's rolling-5-idle-bday absorbing barrier is still not the venue's Mon–Fri
  bucket, and *warning first* is still accurate as procedure.
- §4's non-licenses. No pin is impeached; no gate moves; **no token trade is authorized.**

**What is re-read — finding 3.** Its conclusion, *"The cost is negligible; the open problem is
disposition, not economics,"* is now only half true, and the half that changes is the load-bearing
one:

- **Mitigation economics: still negligible** — ~$1.82 RT, ≈$149 over the 6-year panel. Unchanged.
- **Failure economics: the whole seat** — non-refundable eval, promo already spent, the +$127.40
  realized progress, account-bound rail-build state, no reactivation.

So the framing "disposition, not economics" holds only if *economics* means the mitigation's price.
The **asymmetry** between the two — ~$1.82 against the account — is what makes the disposition
urgent rather than administrative, and it strengthens rather than weakens the finding.

Disposition remains the operator's at 08-08. Options and preconditions (design-only, nothing
executed): [`2026-08-02-idle-rule-disposition-options.md`](../../../docs/superpowers/specs/2026-08-02-idle-rule-disposition-options.md);
tracking surface: [`2026-08-02-idle-clock-tracking-spec.md`](../../../docs/superpowers/specs/2026-08-02-idle-clock-tracking-spec.md).
