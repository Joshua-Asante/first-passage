**Theme:** c1
# F3 cadence measurement — Bulenox / MFFU / BluSky vs Striker's book

> ⚠ **The BluSky rows below are SUPERSEDED — read [Addendum 2026-08-05b](#addendum-2026-08-05b--bluskys-rule-was-sourced-the-limit-is-real-and-the-unit-was-wrong) before quoting any BluSky number.**
> §1 concluded BluSky's cadence exposure was **UNKNOWN** because no activity rule existed in the repo.
> That was true of the repo and **wrong about the venue**: BluSky publishes one, in its **Terms of Use**
> (art. 11490284 §3.3), which the 2026-07-12 collection-scoped sweep never opened. The rule is real,
> trade-based, binds evaluation accounts — and counts **calendar** days, so the faithful engine limit is
> **22 idle bdays, not 30**. Corrected BluSky exposure is **4.87–13.14%**, not the 0.52–1.40% tabled below.
> **Bulenox, MFFU and the Tradeify control are unaffected and reproduce exactly.** Body left unedited
> (Trap #12); this banner is the reader-intercept (`operational_rules.md` Rule 14).

**Status:** ACTIVE — the cadence axis F3 required is measured, and **F3 is not decidable on it.** Bulenox and MFFU sit in the same inactivity-death class as Tradeify (90.85–97.54% path death at idle=5) and are eliminated on measured grounds. BluSky's idle=30 is nearly non-binding (0.52–1.40%) — but that 30 is recorded as a **subscription renewal window, not a published activity rule**, so BluSky's cadence exposure is **UNKNOWN, not low**.

**Date:** 2026-08-05. **Trigger:** operator queue item F3 ([`ADR 2026-08-04`](../../../docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md) §7) — *"Requires scoring Bulenox / MFFU / BluSky against Striker's cadence axis — the measurement none of them has."* Sibling of [`c1_cadence_inactivity_2026-08-02`](../c1_cadence_inactivity_2026-08-02/RESULTS.md) (Tradeify only). Read-only compute on committed inputs; **$0 · K=0 · no manifest · no `core/` / Pine / allocation / `dd_protection` / lifecycle / rail change.** Does **not** elect a successor venue — that remains the operator fork dated 2026-08-08.

**Harness:** [`run_f3_cadence.py`](run_f3_cadence.py) · **Raw:** [`out/f3_cadence.json`](out/f3_cadence.json) · [`out/f3_cadence.log`](out/f3_cadence.log)
**Repo anchor:** HEAD `21e09c8` at run start · panel = committed 2026-07-23 book-composition daily panel.

---

## §0 — Control pin (Tradeify) before any new cell

Same panel, seeds, and C2-off · 1.00× cell as the 2026-08-02 Tradeify study:

| Cell | Published pin | This run | Δ |
|---|---|---|---|
| pass · inactivity OFF | 68.07% | **68.07%** | 0.003 pp |
| bust_inactivity · ON | 92.60% | **92.60%** | 0.003 pp |

**MATCH.** Shared engine/panel/seeds; new cells below inherit that pin. The driver **exits 2 on drift** before measuring any F3 tier.

**Cohort caveat (binding, same as sibling):** panel-geometry (backtest sizing), **not** rail-geometry. Absolute pass/bust levels are not comparable to the published 4.74% / 1.20% pins. The deliverable is the inactivity OFF→ON **delta** per tier.

**Geometry notes (attested in log):**
- `MFFU_Rapid_100K` — native `dd_lock_offset_usd = 1_000_000` (unreachable-lock idiom; ADR 2026-08-04 firm-rules fix).
- `Bulenox_100K` / `BluSky_Premium_100K` — `firm_kwargs` expresses **%-of-peak** trailing (optimistic vs venue fixed-$ ropes). Absolute DD-bust is **not** gate-grade; inactivity delta is.
- **Consistency rules are unmodeled in every arm** (`consistency_frac: None` — Bulenox 40% payout-checkpoint, MFFU 50% eval-soft, BluSky 34% eval-soft). None fails an eval account, so the omission is conservative-neutral here — but it is an omission.

---

## §1 — Provenance of the discriminating field (frozen before the grid was interpreted)

F3's entire result turns on one integer per tier: `inactivity_max_idle_days`. That single field name carries **four different kinds of source**, established by reading `core/firm_rules.py` and searching the full tree (incl. LTM, `rg --no-ignore`) **before** §2 was read:

| Tier | Value | Recorded source | Kind |
|---|---|---|---|
| `Tradeify_Select_100K` (control) | 5 | art. 10468318 + 12268494 — idle week → marked inactive → email warning → **permanent deletion**, *"cannot be reactivated"*. ADR 2026-08-04 §0 attests it as **"a VENUE FACT"** | genuine, **absorbing** activity rule |
| `Bulenox_100K` | 5 | *"≥1 trade per 5 trading days"* (2026-07-03 sweep; corrected 2026-07-06 off an FXIFY placeholder). Comment states the venue counts **calendar trading days idle** while the engine counts **consecutive zero-P&L bdays** — *"the intended encoding pending a scheduled token-micro-trade mitigation"* | genuine activity rule, **documented proxy** encoding |
| `MFFU_Rapid_100K` | 5 | *"≥1 trade/week; **not modeled as absorbing barrier**"* — the field's own annotation disclaims absorbing treatment | activity rule, **annotation contradicts the modeling** |
| `BluSky_Premium_100K` | **30** | *"30-day eval **subscription renewal window**"* | **a billing cycle — not a trading-activity rule** |

**No BluSky activity rule exists anywhere in the repo.** The 2026-07-12 BluSky block cites `help.blusky.pro` article 12434059 + the automation FAQ for drawdown, consistency, cost and auto-liquidation, and is **silent on inactivity**. The `30` is the subscription window, sitting in the field the engine reads as an idle-trading barrier.

This section is placed **before** §2 deliberately. The ranking §2 produces is exactly the one this table predicts; reporting them together would let the provenance read as post-hoc rationalisation of an inconvenient result.

---

## §2 — Headline table (C2-off · 1.00×)

| Tier | `inactivity_max_idle_days` | pass OFF | pass ON | **bust_inactivity ON** | med days OFF→ON |
|---|---|---|---|---|---|
| Tradeify_Select_100K (control) | 5 | 68.07% | 6.34% | **92.60%** | 52 → 11 |
| **Bulenox_100K** | 5 | 69.13% | 8.13% | **90.85%** | 52 → 7 |
| **MFFU_Rapid_100K** | 5 | 68.15% | 7.18% | **91.77%** | 52 → 7 |
| **BluSky_Premium_100K** | **30** | 69.13% | 68.77% | **0.52%** | 52 → 52 |

---

## §3 — Full factorial

### Bulenox_100K (`trailing`, idle=5)

| Arm | pass OFF | pass ON | bust_inactivity ON | med OFF→ON |
|---|---|---|---|---|
| C2-off · 1.00× | 69.13% | 8.13% | **90.85%** | 52 → 7 |
| C2-off · 0.50× | 88.34% | 2.48% | **97.50%** | 131 → 11 |
| C2-on · 1.00× | 78.05% | 7.89% | **91.81%** | 67 → 7 |
| C2-on · 0.50× | 97.04% | 2.46% | **97.54%** | 152 → 11 |

### MFFU_Rapid_100K (`trailing_locking`, idle=5)

| Arm | pass OFF | pass ON | bust_inactivity ON | med OFF→ON |
|---|---|---|---|---|
| C2-off · 1.00× | 68.15% | 7.18% | **91.77%** | 52 → 7 |
| C2-off · 0.50× | 87.61% | 2.48% | **97.50%** | 131 → 11 |
| C2-on · 1.00× | 76.71% | 6.92% | **92.75%** | 66 → 7 |
| C2-on · 0.50× | 96.46% | 2.46% | **97.54%** | 151 → 11 |

### BluSky_Premium_100K (`trailing`, idle=30)

| Arm | pass OFF | pass ON | bust_inactivity ON | med OFF→ON |
|---|---|---|---|---|
| C2-off · 1.00× | 69.13% | 68.77% | **0.52%** | 52 → 52 |
| C2-off · 0.50× | 88.34% | 87.41% | **1.09%** | 131 → 131 |
| C2-on · 1.00× | 78.05% | 77.49% | **0.76%** | 67 → 67 |
| C2-on · 0.50× | 97.04% | 95.70% | **1.40%** | 152 → 151 |

---

## §4 — Findings

1. **The 5-day barrier is venue-invariant, and it is fatal.** Bulenox **90.85–97.54%** and MFFU **91.77–97.54%** — a 1.90pp spread between them at 1.00×, within 2.72pp of the Tradeify control, across two different `dd_type` branches, two different `min_trading_days`, and one different lock idiom. The book's cadence, not any venue's drawdown geometry, is what kills these paths. **Switching from Tradeify to Bulenox or MFFU buys nothing on the axis that de-scoped Tradeify.** The ~90%+ figure now rests on four measurements across three venues: Bulenox C5 ~96% ([`RESULTS_C5`](../../archive/bulenox_futures_remc_2026-07-01/RESULTS_C5_integer_2026-07-03.md), 2026-07-03, different panel vintage and sizing), Tradeify 92.60% (2026-08-02), and Bulenox + MFFU here.

2. **BluSky's advantage is one integer, and the counterfactual needs no run.** `firm_kwargs` for `Bulenox_100K` and `BluSky_Premium_100K` are **identical apart from `inactivity_limit`** — same `trailing`, same −0.03 rope, same $106,000 target, same `min_trading_days: 0` — verified directly and confirmed by their OFF arms measuring identically (69.13% / 30.87% / med 52). Therefore **if BluSky's true activity rule is 5 days, BluSky's INACT *is* Bulenox's: 90.85 / 97.50 / 91.81 / 97.54%.** The entire 0.52%-vs-91% gap is carried by `30` versus `5`, and §1 shows the `30` is a billing window. The book's max realized idle-gap is 27 bdays and its longest dead-week run is 4 weeks ([sibling §1](../c1_cadence_inactivity_2026-08-02/RESULTS.md)) — a 30-bday barrier never fires on the realized panel and only absorbs under bootstrap resampling, which is why the measured value is ~1% rather than 0.

3. **The 0.50× / longer-horizon interaction survives across venues — and is a property of the barrier width, not the book.** At every idle=5 tier the WATCH-1 haircut that repairs DD geometry **raises** inactivity exposure (Bulenox C2-on 91.81 → 97.54% as DD-bust falls 21.95 → 2.96%; MFFU 92.75 → 97.54%) — the mechanism the Tradeify sibling named. At BluSky's 30 days the same lever costs only **+0.64pp** (0.76 → 1.40%). De-risking is nearly free on the cadence axis once the barrier is wide enough, so the lever conflict is generated by the barrier, not by the strategies.

4. **F3 is not decidable on this measurement.** It eliminates two of three candidates on measured grounds and reduces the third to a single unverified venue fact. That is the honest yield: F3 becomes "two are eliminated; the survivor needs BluSky's actual published activity rule sourced before it can be picked." Electing a successor off §2 today would be the **"successor-venue drift"** the de-scope ADR §Risks named in advance — *"'three firms untouched' can decay into 'three firms assumed viable'."* Successor election additionally needs payout mechanics, automation posture, rail fit, and operator GO; none is opened here.

---

## §5 — What this does NOT license

- **No successor venue is registered, recommended, or ranked for selection.** F3 remains open and operator-owned. §4.2 is a *sensitivity result*, not a BluSky endorsement.
- **No BluSky claim rests on the 30.** Until an activity rule is sourced from BluSky's own published material, BluSky's cadence exposure is **UNKNOWN**, not "low". The measured 0.52–1.40% holds only *conditional on the encoded field being an activity rule*, which §1 shows is not established.
- **No pin is impeached and no gate moves.** The Tradeify control reproduces exactly; the inactivity-off modeling choice in every published run remains the documented choice it always was. This prices it at three more tiers; it does not refute it.
- **No token trade or mitigation is authorized**, at any venue. The book-composition brief §5 forbidden move stands, and the rail-level-vs-accept-warnings choice remains unmade.
- **Bulenox / BluSky absolute DD-bust levels are not gate-grade** (%-of-peak vs fixed-$). Quoting 30.87% or 11.66% against a Part A threshold would be an error.
- **Engine barrier ≠ venue rule.** Engine = rolling N-consecutive-idle-bday **absorbing**; venue encodings differ per §1. These numbers price the *unmitigated barrier assumption* every published `INACT_OFF` figure makes — not a forecast of any venue's soft-enforcement path.

---

## §6 — What would decide F3

1. **Source BluSky's activity rule** from `help.blusky.pro` (the 2026-07-12 sweep captured drawdown / consistency / cost / auto-liquidation from articles 12434059 + 12434069 and recorded no inactivity rule). Three outcomes: a 5-day-class rule ⇒ **all three candidates are eliminated** and F3's answer is "no successor survives the unmitigated barrier"; a 30-day-class rule ⇒ §3's BluSky rows stand as measured; no published rule ⇒ re-encode the field and declare the exposure unknown.
2. **Correct the field's semantics regardless of the F3 outcome.** `BluSky_Premium_100K`'s `30` is a subscription window sitting in a field the engine reads as an absorbing trading barrier — a live mis-encoding that will silently shape any future run reading that tier, the `lesson_driver_layer_fix_leaves_kernel_default_stale` shape. Flagged here, **not fixed in this read-only pass.**
3. **Note that mitigation, not venue choice, is the live lever.** All four tiers' 5-day results are unmitigated-barrier figures. The R8 scheduled-maintenance-trade remedy remains owed and remains the cheapest cadence instrument at every venue measured.

---

## §7 — Reproduction

```bash
python lab/analysis/c1/f3_cadence_successor_venues_2026-08-05/run_f3_cadence.py
# writes out/f3_cadence.json + out/f3_cadence.log
# control pin must MATCH before F3 cells are emitted (exit 2 on drift)
```

Reads only committed inputs (`daily_panel.csv`, `core/firm_rules.py`); 10,000 sims × 3 seeds (`portfolio_mc.SEEDS`), horizon 1500d, identical seeds across all 26 arms; results checkpoint to `out/f3_cadence.json` after each tier. Panel gap distribution is not re-derived — inherited from the 2026-08-02 sibling (sizing-invariant at the zero/non-zero level). Windows note: run under `PYTHONUTF8=1` / `-X utf8`; the console default (cp1252) cannot encode the log's `×` / `—`.

---

## Addendum 2026-08-05b — BluSky's rule WAS sourced: the limit is real, and the unit was wrong

**Body above is unedited** (house discipline: the impeachment lives in the addendum). **Bulenox, MFFU
and the Tradeify control are untouched — every one of their numbers stands and reproduces exactly.**
What changes is the BluSky column and, with it, §4.4's characterisation of F3 as undecidable.

**§1's factual claim was true; its conclusion was not.** *"No BluSky activity rule exists anywhere in
the repo"* was correct — and it is not the same statement as "BluSky publishes no activity rule". It
does. Sourced in-browser 2026-08-05 on operator directive:

- **Terms of Use art. 11490284 §3.3 "Abandoned Accounts"** (under §3 *Refunds and Billing Policy*) —
  *"Evaluation, BluLive, SimFunded, or brokerage accounts inactive for 30 consecutive days may be
  closed at our discretion."* **Evaluation accounts named explicitly**; enforcement **discretionary**.
- **Brokerage Funded Rules art. 12434442** defines what BluSky means by *active* — *"place at least one
  trade every 30 days to keep the account active"* — so "inactive" is **trade-based**, not login- or
  billing-based. This is what disambiguates §3.3.
- **Billing art. 12434108** — *"The billing period of 30 calendar days will auto renew each period"* —
  the subscription window the 2026-07-12 sweep had actually encoded. Both objects are real, both are
  "30 days", and the sweep encoded the wrong one.

**Why the sweep missed it:** it was **collection-scoped, not document-scoped** — it read the Evaluations
articles (which carry no activity rule at all) and never opened the Terms of Use. Right collection,
wrong document class. Note the exact parallel with the Tradeify sibling, whose binding inactivity rule
also lived outside the main rules article (art. 12268494, not 10468318).

**The unit, not the number, was the defect.** The clause counts **calendar** days; the engine counts
consecutive idle **business** days. A literal `30` models ~42 calendar days — **~40% more lenient than
the published rule**, in the optimistic direction, on the axis F3 turns on. The faithful threshold is
**22 idle bdays** (4 weeks + 2 days = the point at which 30 calendar days has certainly elapsed).

**Corrected BluSky exposure** (`run_blusky_unit_sensitivity.py` → `out/blusky_unit_sensitivity.{log,json}`;
same panel, seeds, geometry):

| Arm | limit 30 (§3, superseded) | **limit 22 (corrected)** | limit 21 (bracket) |
|---|---|---|---|
| C2-off · 1.00× | 0.52% | **4.87%** | 5.59% |
| C2-off · 0.50× | 1.09% | **10.48%** | 11.88% |
| C2-on · 1.00× | 0.76% | **7.04%** | 7.98% |
| C2-on · 0.50× | 1.40% | **13.14%** | 14.80% |

**What survives, and what changes:**

- **§4.1 stands unchanged.** The 5-day barrier is venue-invariant and fatal; Bulenox and MFFU remain
  eliminated at 90.85–97.54%.
- **§4.2 stands, with a smaller multiplier.** BluSky's advantage is still carried by one integer, and
  the `firm_kwargs` identity with `Bulenox_100K` still holds exactly. The gap is now **6–20×**, not ~100×.
- **§4.3 strengthens.** The lever conflict is much sharper once the unit is right: the 0.50× haircut
  moves BluSky 7.04% → 13.14% (C2-on), a **+6.10pp** cadence cost for the DD repair, versus the +0.64pp
  the superseded encoding implied. De-risking is no longer close to free on the cadence axis.
- **§4.4 is the limb that changes.** F3 is **no longer undecidable for want of a venue fact** — the fact
  exists and is encoded. BluSky is the one candidate that survives the cadence axis, at **4.87–13.14%**
  unmitigated path death, worst at the **C2-on 0.50× rung the book would actually deploy at**.
  What remains open is not evidence but *decision*: payout mechanics, automation posture, rail fit, and
  operator GO — none opened here.
- **§5's non-licenses all stand.** No successor venue is registered, recommended, or ranked; no gate
  moves; no token trade is authorized.

**Residual, explicitly not corrected:** §3.3 is **discretionary** (*"may be closed at our discretion"*)
and art. 12434442 is warning-first, while the engine barrier is absorbing and certain — so real hazard
is **≤** modelled. Direction is conservative, magnitude unmeasured. This is *not* a licence to loosen
the limit: the Tradeify sibling's Addendum 2026-08-02b is the cautionary case, where a *"soft-enforced,
warning first"* reading turned out to be permanent, irreversible deletion.

Decision record: [`ADR 2026-08-05b`](../../../docs/adr/2026-08-05b-blusky-inactivity-rule-sourced.md),
superseding [`ADR 2026-08-05`](../../../docs/adr/2026-08-05-blusky-inactivity-unsourced-encoding.md)
by discharging its §4 T1.
