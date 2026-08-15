# NOTICE 2026-08-13 — external population data for the eval model (first external referent)

**Type:** Notice-phase observation log. **Records observations; rules on nothing.** $0 · K=0 · no gate moved, no candidate admitted, no threshold changed.
**Trigger:** operator proposed researching what currently-funded Tradeify traders trade (2026-08-13). The strategy-harvest reading of that proposal is barred (see §5); the *model-validation* reading was found genuinely unrun and is recorded here.
**Method:** 4 parallel read-only agents (corpus dedup · Tradeify primary surface · practitioner archetype · population statistics). Two load-bearing claims re-verified parent-side by direct fetch before this note was written.

---

## §1 — The gap this fills

Prior state, established by corpus audit this session: the estate's eval model is a **closed deductive system** — venue rules (primary-sourced, well-verified) → arithmetic boundaries → Monte Carlo over the estate's own panels → gates whose thresholds are set by internal poles. Its rule inputs are rigorously external. **Its outcome model had never touched an external outcome distribution.** No published pass rate, no trader population, no funded-account outcome, anywhere in the corpus.

The survivor gate's own provenance ([`2026-07-13 prereg`](../../briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md) §3): 3.0% = *"the $100K band's own barrier width"* bracketed by two of the estate's own MC outputs (1.0% null-by-construction, 17.70% falsified book); the 50% pass floor is a **no-trade-grinder loophole patch**. Both are conventions. ⚠ Note the barrier-width rationale welds a *drawdown width as a fraction of equity* to a *probability of ruin* — same numeral, different quantities. Recorded, not adjudicated.

## §2 — Firm-published funnel disclosures [INDUSTRY-DISCLOSED]

**Tradeify** — verbatim, tradeify.co footer, verified parent-side 2026-08-13:

> "Trader Performance Statistics (August 2025 – July 2026, calculated as of 9 August 2026): Across Tradeify's Growth, Advanced and Select evaluation products, (a) 17.2% of evaluation accounts initiated were successfully completed and afforded the opportunity to advance to the Funded Level; (b) 40.3% of individual participants who initiated one or more evaluations advanced to the Funded Level in at least one of their evaluations - participants may purchase multiple evaluations and resets, and initiated a median of 3 each over the period; (c) 28.5% of individual participants at the Funded Level received a payout; and (d) 3.0% of individual participants trading in a Funded Account were called up to a Live Funded Account."

**Topstep** — topstep.com/risk-disclosure, updated 2025-09-25, Jan–Dec 2025: **16.8%** of Combines completed · **51.8%** of participants funded in ≥1 · **33.3%** of funded participants received a payout · **0.71%** reached Live Funded.

| Quantity | Tradeify (Aug25–Jul26) | Topstep (2025) |
|---|---:|---:|
| Per-**account/attempt** pass | **17.2%** | **16.8%** |
| Per-**participant** pass (multiple attempts) | 40.3% (median 3 evals) | 51.8% |
| Funded participants → any payout | 28.5% | 33.3% |
| Funded → Live | 3.0% | 0.71% |
| Chained P(payout \| bought an eval) | ≈**11.5%** | ≈**17.2%** |

**The per-attempt rate is ~17% at both firms independently.** Denominators differ per clause and are routinely conflated downstream — per-attempt and per-participant are not interchangeable.

**Scope limits:** Tradeify's figure pools Growth + Advanced + Select (different rules; Growth has a DLL and can pass in 1 day, Select needs ≥3 days via the 40% rule) — it is **not Select-100K-specific**. Both are single-period snapshots with no measured stability. No firm publishes time-to-pass or funded-account survival curves. **Apex, MyFundedFutures and BluSky publish no outcome disclosure at all.**

## §3 — Population base rates for the underlying activity

- **Ferko, Mixon & Onur (2024), "Retail Traders in Futures Markets," CFTC OCE Staff Paper 2023-002** [REGULATOR STAFF PAPER — best futures-specific source found]. 36,538 retail traders, 50 futures markets, Feb 2021–Nov 2022, from CFTC regulatory margin-position data at a large retail FCM. Median trader: **4 trading events of ~4 days** across 2 markets; median loses **$100–200**; **~60th percentile of P&L ≈ zero**; left-skewed; larger first-trade losses predict permanent exit. Explicitly notes retail concentration in **micro equity index contracts** — our instrument class.
- **Barber, Lee, Liu & Odean (Taiwan)** [PEER-REVIEWED]: *"in the typical six month period, more than eight out of ten day traders lose money"* — with a persistently skilled small subgroup (top-500 +61.3 bps/day gross, +37.9 net).
- **Chague, De-Losso & Giovannetti**, Brazilian **equity futures**, ≥300-day persisters: **97% lost money; 0.4% earned more than a bank teller**; *"no evidence of learning by day trading."* ⚠ version discrepancy — secondary sources circulate a different cut; cite the version read.
- **ESMA (2018)** [REGULATORY]: 74–89% of retail CFD accounts lose money.
- **No academic literature on the prop-firm evaluation model exists.** Targeted searches across SSRN/arXiv/NBER/RePEc/ScienceDirect returned zero. Real absence, not search failure.

## §4 — The modeling anchor [PEER-REVIEWED] — the actionable find

**Magdon-Ismail, Atiya, Pratap & Abu-Mostafa (2004), "On the Maximum Drawdown of a Brownian Motion," *J. Applied Probability* 41:147–161.** This is our first-passage problem stated in its own terms: drawdown `D(t) = sup_{s≤t}X(s) − X(t)` as reflected BM with drift −μ and reflecting barrier at 0; absorbing barrier `h`; closed-form `G_D̄(h) = P[D̄ ≥ h]` as an infinite series (eigenvalue condition `tan θₙ = σ²θₙ/(μh)`); **numerical tables in Appendix B**. **Appendix A carries the static barrier** (inverse-Gaussian first-passage density).

Two consequences:
1. **`core/mc/simulation.py` has an available external regression anchor for the first time** — the continuous-time analogue of the trailing-barrier bust computation, with published numerical tables. As far as the published record goes our simulator reproduces no one, which also means it has never been validatable against anyone.
2. **The trailing→static equivalence mapping is unpublished anywhere**, and this machinery answers it directly by solving `G_D̄(h_trail) = G_H(h_static)`. Adjacent literature (Grossman–Zhou 1993, Cvitanić–Karatzas 1995) enforces the HWM barrier *by construction* so breach probability is zero by design — they answer what the constraint costs in growth, not P(survive). Discrete-time: Atiya & Magdon-Ismail (2018) — relevant because our enforcement is per-trade, not diffusion.

## §5 — Sourcing-route findings (why the literal proposal is barred)

Corpus audit, this session, verbatim anchors available in the agent record:
1. **Practitioner sourcing is channel rank 6** in `strategy_harvest.md` §2.3 — the worst tier, *"idea generation only"*, already declared and run (MNQBASE-1 §2.1). Being rank-6 means it is **not** "a new sourcing channel" and does not clear the MNQBASE-1 bar.
2. The free-data 5th-leg **SNAG scope sentence names *"published/retail strategies"* verbatim**; admission needs paid data / new venue class / dated live incident.
3. Harvest **Req 1a** kills a trader-sourced mechanism before Req 2 does — *"Preference/behavioral stories … no longer satisfy 1a."* R-REQSCOPE's carve-out is scoped to **internally-composed** candidates only.
4. **Tradeify FTA §6.6** (verified parent-side): sole-ownership proof required, *"using it across multiple firms is against Tradeify's policy."* Copy-and-deploy of another trader's strategy is independently non-executable.

## §6 — Venue clauses verified parent-side this session

| Clause | Verbatim | Bearing |
|---|---|---|
| **§6.6** | *"using it across multiple firms is against Tradeify's policy. The bot must be solely for the Trader's own use within Tradeify"* | **Collides with the four-firm prop-portfolio architecture** (one validated strategy, four venues). §6.10 grants audit without notice. **Operator ruling owed** — interacts with F1 and the 2026-11-08 §4 falsifier |
| **§6.5** | *"maintaining consistent trading sizes, avoiding dollar-cost averaging and high-frequency trading"* | Help centre states the opposite (*"DCA is allowed"*). Both Striker legs pyramid; `DD_SCALE` 0.40× is by construction a varying size. Not a safe harbour |
| **§6.7(c)** | *"prohibited from holding Opposing Positions in (i) the same futures product, or (ii) two or more futures products assigned to the same Product Group"* … *"regardless of the Trader's intent"* | MYM and MNQ share the Equity Index group; binds evaluation accounts too |

**Consistency rule — structural finding:** at **every** firm checked, a consistency breach is **non-terminal** — it withholds the payout until further trading dilutes the best day. It is a **withdrawal gate, not a survival gate**, so it can never appear in a bust rate and attacks P(payout) invisibly. Tradeify Select carries **40% at evaluation and none once funded** — our incumbent's exposure is confined to the eval. Unformalized ratchet: the numerator (best day) is locked history while the denominator (total profit) is live and mean-reverts down, so a drawdown after a good day *raises* consistency % with no new trade — it tightens exactly when a trend book is drawing down.

## §7 — What this does NOT establish

1. **Estimand mismatch is the governing caveat.** Every population figure measures *discretionary retail humans with no validated edge*. Our MC estimates *one fixed pre-validated systematic strategy*. These are different quantities. **The population data does not falsify P(pass) ≥ 50%** — it tells us what percentile of an unselected population that gate implicitly claims (~3× the per-attempt rate).
2. **This is not a license to loosen any gate.** Q-BUSTGATE-1 already established that re-deriving a survival gate under a different objective *"degenerates to 'looser,' not 'more correct.'"* A population base rate is a third input, not a dial. Any threshold change runs its own pre-registration; changing one after a near-miss is the named goalpost move.
3. **Coincidence trap:** Tradeify's 3.0% Live call-up rate and our 3.0% bust ceiling are unrelated quantities sharing a numeral. Do not weld them.
4. **Coverage gap:** Reddit is unfetchable from this environment (hard block at search-filter and fetch layers), so the largest practitioner source class is absent. All forum-side evidence here is second-hand except NexusFi threads read directly.
5. **Archetype evidence is survivorship-selected and bimodal, not clustered** — both low-WR/2–3R trend-following and high-WR/tiny-target/**no-stop** scalping demonstrably pass. The strongest signal is revealed preference: Apex's rulebook explicitly bans *"very small ticks but with huge stop losses or no stop losses"* — firms legislate against what their passers do. Hypothesis worth recording, **not established**: high win rate may be *purchased by stop-removal*, which would place high-WR-with-hard-stop (our design box) in a region with no observed passers.

## §8 — Two fabrication incidents (process, not content)

Both caught independently by two agents in this session:
1. **`track360.io` "Q3 2026 regulation roundup"** — published 2026-05-20, reports as fact a CFTC consultation closing 2026-11-30, SEC enforcement filed 2026-08-15, NFA Notice I-26-12 dated 2026-08-30. **Every date postdates the article's own publication.** Direct checks against sec.gov / cftc.gov / nfa.futures.org / federalregister.gov corroborated none of it. **The web-search summarizer relayed these as fact repeatedly.**
2. **"EOD drawdown has an 83% higher pass rate"** — originates from a firm that *sells* EOD-drawdown accounts; the pages search summaries credited with the figure **do not contain it**. The attributions were manufactured at the summarizer layer.

Also: **CFTC v. Traders Global (My Forex Funds)** — the widely-cited $310M/135,000-customer figures are **allegations that were never adjudicated**; dismissed with prejudice May 2025 with >$3.1M Rule 11 sanctions against the CFTC. Do not cite as findings.

## §9 — Intersection with the frozen MSL-C1 G0 (a stated prior, not a prediction)

[`MSL-C1 PREREG_G0`](../../../lab/archive/msl_c1_mym_2026-08/PREREG_G0.md) froze **rr=1 with a hard stop** on 2026-08-13, the same day this sweep ran. **That G0 is FROZEN and nothing here may edit it** — this section exists so the explore reader meets the prior *before* the number, rather than fitting an explanation after it.

**The arithmetic:** break-even win rate with cost is `WR* = (S+c)/(T+S)`. At the G0's frozen geometry (S = T, RT $2.82, $160 R/contract at the Stage-1 disclose point), `WR* ≈ 50.9%`. The construct must clear ~51% just to break even, before any survival margin.

**The empirical prior (§7.5):** observed passers cluster at **low-WR / 2–3R with a stop** or at **high-WR / tiny-target / no stop**. The high-WR-*with-hard-stop*-at-rr≈1 region — where this G0 sits — has **no observed passers** in the sample gathered. Candidate mechanism, unestablished: high win rate may be *purchased by stop removal*, in which case imposing a hard stop drops WR below break-even by construction.

**Why this is worth stating rather than acting on:** it is absence-of-evidence in a survivorship-selected sample, not proof of an empty region — and the sample is retail-discretionary, a different estimand from a pre-registered systematic construct (§7.1). But it is the opposite of corroboration, and the G0's explore **measures WR directly**, so one IS run falsifies or confirms it cheaply. **Forbidden:** using this section to retune the frozen G0, to soften its gate vocabulary, or as post-hoc explanation of an adverse result. It is a reading aid, recorded before the read.

Sizing note, disclosure only: the Stage-1 disclose point (4 contracts, ≈$651 all-lose day) leaves ~4.6 consecutive losses of headroom against the $3,000 trail; the G0 correctly defers qty to scoring rather than freezing it. The §3.3 pincer applies at the low end — at 1 contract an all-win day is ≈$157, below the $200 floor — so the payable-and-survivable band is narrow but non-empty around 2–3 contracts.

## §10 — Operator rulings on §9's open items (2026-08-13, same day)

1. **§6.6 vs the four-firm architecture — DEFERRED, not decided.** Architecture stands unchanged as of this ruling. No superseding ADR, no §4 F1 reading taken. Re-raise before the 2026-11-08 clock, not after.
2. **Funded-phase mortality — DEFERRED, not decided.** No TNEC limb added. Operator: *"we will construct the funded phase mortality numbers when we cross that bridge"* — i.e. when a candidate is close enough to funded-phase design for the question to bind, not before. Do not pre-empt with a limb no candidate needs yet.
3. **§9's no-stop-archetype tension — RULED, standing design constraint.** Operator: *"a stop is necessary with the strategy, having no stop makes catastrophic loss possible in a way that is not the case with a hard stop. This may inform the shape of the strategy we are looking for."* **A hard stop is mandatory for any MSL candidate, independent of what §9's win-rate evidence shows.** This does not dispute the empirical finding (high-WR may be purchased by stop removal) — it accepts the finding and rules the *bounded-tail* archetype governs anyway, because the tail-risk asymmetry of an unbounded loss is not one the operator will trade against a WR advantage. **Consequence for card design:** the design box's existing "chunky per-trade R with hard stop" line ([first slate](../../briefs/2026-08-12-msl-first-slate.md) header) is confirmed as a hard constraint, not a stylistic default — a future card proposing a no-stop or soft-stop (time-only, discretionary, "let it come back") construct is out of scope for this channel regardless of any WR/pass-rate case it could make. **What remains open, and is where "inform the shape" should be read:** the constraint is on stop *presence*, not on stop *type* — a hard stop can be tight, wide, time-based, or structure-adaptive; C1's rr=1 fixed-distance choice is one expression, not the only admissible one. If C1's explore measures WR below the ~50.9% break-even line, the correct reading per this ruling is "find a bounded-tail shape that clears break-even" (wider stop, better R:R, a different entry that raises WR within the hard-stop constraint), never "remove the stop."

**The Magdon-Ismail regression anchor** (§4) is spawned as a separate task, unaffected by the above. Where these figures live permanently is settled by this note's own landing (`docs/notes/notice/`) — no further placement question outstanding.
