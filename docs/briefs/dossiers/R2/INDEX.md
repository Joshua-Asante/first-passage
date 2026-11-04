# R2 cell dossiers: index and per-instrument ranking

**Status:** zero-K inputs to R2 (template Part A §A2–§A3, tasks T2–T3; [template](https://github.com/Joshua-Asante/first-passage/blob/0a4c5a92c33b1615cde2e39af85933e01e3992db/docs/briefs/pre-registration/TEMPLATE-builder-round.md), PR #1051 head `0a4c5a9`, unmerged). **K = 0:** no market data was read. It decides nothing: cells, firms and the round are Joshua's (Rule 3), and generation never blesses (Rule 25).
**Authority:** Joshua, 2026-11-04: "yes to all four, spawn the sessions" (a proposal to run parallel dossier sessions on top-ranked cells, ready for R2).
**Date / base:** 2026-11-04, `main` at `8745b40`. **Budget (Rule 2):** ≤12 dossiers plus this index; ≤3 Codex review rounds; K = 0; six parallel research workers, every cited figure re-verified by the coordinator (below).
**Public-file limits:** coarse session words only. Clock settings and parameter values belong to the private card design (T4, not done here). Template Part A is otherwise private. This public form is the operator task's choice, so it carries no card values.
**Dedup (Rule 8):** [DEDUP.md](DEDUP.md). Source logs (URLs, verbatim quotes, consult outputs): [`sources/`](sources/).

## Shared inputs

- **Reach (D7, T3).** Each dossier's reach block is `gates.reachability(k, n)`, run through the fp launcher, with n from the admitted calendar `ops/calendars/cme_holiday_calendar_2016_2026.json`, minus D9's 378-session holdout. Banked builder K is 0 on these six instruments on the public record, which the private `ledger.k()` must confirm at registration.

  | Window | Dev n (est.) | 5f floor at K = 1 | P(pass) at Sharpe 0.85 / 0.89 | Floor at K = 2 |
  |---|---|---|---|---|
  | MNQ, MYM, M2K: 2019-05 → 2026-11 | 1,492 | 0.676 | 0.664 / 0.698 | 0.890 (at the D7 boundary) |
  | MGC, 6J, M6E: 2016-01 → 2026-11 (the calendar binds) | 2,325 | 0.542 | 0.825 / 0.855 | 0.713 |

- **Power (Req 4):** `Φ(√N·|δ/σ| − 1.96)`. Break-even δ/σ for power 0.50 is 0.051 at N = 1,492 and 0.041 at N = 2,325.
- **Haircut:** McLean & Pontiff (2016) "58% lower post-publication" is the central reading; 32% is the sensitivity.
- **Barrier feasibility:** pending the atlas (sibling session) for every cell.

## Ranking and recommendation

Columns:
- **Req 1:** the economic-grounding path.
- **Screen δ/σ:** after the haircut. U = UNSCREENABLE.
- **Power:** at the development N.

| Instrument | # | Dossier | Mechanism × firm (provisional) | Req 1 | Screen δ/σ | Power | R2 recommendation |
|---|---|---|---|---|---|---|---|
| MNQ | 1 | [r2-mnq-ovndrift](r2-mnq-ovndrift.md) | overnight drift (NEW) × Bulenox | 1a, partly met | U (ES only) | — | **Hold: no MNQ card in R2.** Both looks stay in reserve |
| | 2 | [r2-mnq-expin](r2-mnq-expin.md) | expiry pinning (NEW) × Bulenox | 1a; sign not entailed | U (no signed δ) | — | reserve |
| MYM | 1 | [r2-mym-overnight-drift](r2-mym-overnight-drift.md) | overnight drift (NEW) × Bulenox | 1a, partly met | U (ES only; YM named, no number) | — | **Hold.** If Joshua wants one index card, this is the least-bad one (see reasoning) |
| | 2 | [r2-mym-intraday-momentum](r2-mym-intraday-momentum.md) | `intraday-momentum` × Bulenox | 1a | 0.023 | 0.14 (fails) | reserve |
| M2K | 1 | [r2-m2k-ondrift](r2-m2k-ondrift.md) | overnight drift (NEW) × Bulenox | 1a, partly met | U (no Russell cohort) | — | **Hold** |
| | 2 | [r2-m2k-imom](r2-m2k-imom.md) | `intraday-momentum` × Tradeify | 1a | 0.024 | 0.15 (fails) | reserve |
| MGC | 1 | [r2-mgc-cgb](r2-mgc-cgb.md) | `compression-gated-breakout` × BluSky | fails 1a and 1b | U | — | **Skipped in R2** (Joshua, 2026-11-04: no no-counterparty-channel admission) |
| | 2 | [r2-mgc-pdhpdl](r2-mgc-pdhpdl.md) | `pdh-pdl-breakout-rth` × BluSky | fails 1a and 1b | U | — | reserve |
| 6J | 1 | [r2-6j-tokyofix](r2-6j-tokyofix.md) | Tokyo-fix USD demand (NEW) × **MFFU** (was Bulenox) | **1a met** | H2 0.048 · H1 0.034 · H3 U (spot USD/JPY cohort, admitted under harvest §4a) | H2 **0.63** · H1 0.37 | **R2's card** (Joshua, 2026-11-04): H2, the post-fix leg, only; K = 1 |
| | 2 | [r2-6j-psbc](r2-6j-psbc.md) | `prior-session-breakout-continuation` × Bulenox | 1b fails limb (iv) | U | — | reserve |
| M6E | 1 | [r2-m6e-prefix](r2-m6e-prefix.md) | pre-ECB-fix dealer pre-hedge drift (NEW) × **Bulenox** (was MFFU) | **1a met** | 0.042 (spot EUR/USD cohort, admitted under harvest §4a) | **0.52** (marginal) | **R2, conditional:** on the M6E repo landing, and on the pre-registration answering the EURUSD fix-reversal bar |
| | 2 | [r2-m6e-asialdn](r2-m6e-asialdn.md) | Asia-range London break (NEW) × MFFU | fails 1a and 1b | U | — | reserve |

## Decision (Joshua, 2026-11-04)

Joshua, 2026-11-04, verbatim: "go with your recommendations on both". He was answering the coordinator, who relayed the two recommendations below to this session; they are recorded as relayed.

1. **R2 composition.**
   - **r2-6j-tokyofix (post-fix leg) is R2's card.**
   - **r2-m6e-prefix** enters only after the M6E repo landing, and only if its pre-registration answers the EURUSD fix-reversal re-proposal bar.
   - **MGC is skipped:** no no-counterparty-channel admission.
   - **No index card in R2.** MNQ, MYM and M2K hold.
2. **D10 FX mapping (proposed; deployment order still waits on the venue-terms check):** Bulenox ← M6E (cheapest at $0.50/side; a micro suits Bulenox's intraday-high trail better), and **MFFU ← 6J**.

**Applied in this PR:**
- r2-6j-tokyofix's venue limb is re-checked for MFFU, and r2-m6e-prefix's for Bulenox; both dossiers' target firms are updated.
- The re-check changed:
  - the 6J round-trip commission, from 0.76 to 0.82 ticks;
  - the M6E round-trip commission, from 1.15 to 0.80 ticks;
  - M6E's news and DST collision, which drops out at Bulenox;
  - two new Bulenox items: the 30-day access window, and the ToS approval clause for "third-party" algorithms.
- It also corrected the 6J cost reading: the post-fix leg is net negative at 1 tick/side slip at both illustrative levels.

**Spot-cohort ruling.** Joshua, 2026-11-04, verbatim: "go with your recommendation, option a". Same-pair spot cohorts are admissible for CME FX futures under five conditions. The owner is [strategy_harvest §4a](https://github.com/Joshua-Asante/first-passage/pull/1064), on PR #1064, unmerged. Applied here:
- The 6J and M6E cohort limbs read "admitted under §4a", and each dossier shows the five conditions. The 6J sign conversion is explicit: Table I's signs carry over to 6J, so H2 is long 6J.
- Owed before either card freezes (§4a condition 4): an M-16 fill-slip read on the future in the cell's hours.
- These rows were removed from the UNSCREENABLE table.

**Still open:**
- MFFU's count of a full-size 6J against its "8 minis" cap.
- MFFU's 6J rate, $2.56/side from the 07-13 reading, needs a re-read.
- Bulenox's current M6E rate needs a re-read: the PDF the repo cites is from Sept 2024.

## Reasoning

**Index micros (MNQ, MYM, M2K): hold all three looks.**
- All three first picks are one mechanism from one source (Boyarchenko–Larsen–Whelan overnight drift, SR917 / RFS 2023). D9 allows each R2 card a different mechanism, so at most one of the three could run.
- The authors' post-publication follow-up reads against it: "the 2:00–3:00 window that previously generated roughly 3.7 percent per annum has averaged close to zero since 2021. … The same pattern holds in the E-mini Nasdaq-100 (NQ) and E-mini Dow Jones (YM) contracts" ([Liberty Street Economics, 2026-07-01](https://libertystreeteconomics.newyorkfed.org/2026/07/the-disappearing-overnight-drift/), read raw 2026-11-04). The hour in that quote is the paper's, not a card setting.
  - Its own death observable has already moved: end-of-day RSV dispersion fell "from 6.5 percent to 2.9 percent".
  - Most of the 2019–2026 development window is post-2021.
- Both second picks fail Req 4: intraday momentum at δ/σ 0.023–0.024, power 0.14–0.15. They also sit in the mechanism D5 killed on MNQ, under the binding index-intraday raised bar.
- Each instrument has two lifetime looks, so a look spent on a mechanism its authors call faded is waste.
- If Joshua still wants one index card, MYM overnight drift is the least-bad:
  - the authors name YM;
  - MYM is not the ORB instrument, so it passes the working test's instrument limb, which every MNQ cell fails;
  - it is long-only and outside the ORB window, so it cannot oppose ORB-MNQ under Tradeify ESA §6.7.
  - Its likely result is a null that the card's discriminator would attribute to the mechanism.

**MGC: cgb ranks first; skipped in R2 by Joshua's decision.**
- Neither MGC cell has a payer or a 1b-grade record, and no gold intraday cohort exists for either construct.
- cgb ranks first on the drawdown-allowance wall (`MGC.md` W5): a stop at the opposite edge of a compression range is narrow by construction, while a PDH/PDL stop is about one prior-day range.
- MGC has four looks, so a card here is cheapest in reach terms. But a cell that fails Req 1 is "not a seed" under harvest §1, so admitting it through the builder is Joshua's channel call.

**6J: Tokyo fix, post-fix leg only.**
- It is the only dossier with a named payer and a daily event whose cited cohort passes Req 4 after the haircut. That cohort is **spot USD/JPY**: KMW report futures only as a portfolio. It is admitted as a same-pair spot cohort under [harvest §4a](https://github.com/Joshua-Asante/first-passage/pull/1064) (Joshua, 2026-11-04). The dossier shows the five §4a conditions; the M-16 slip read on the 6J future in the cell's hours is owed. Krohn–Mueller–Whelan Table I, JPY: post-Tokyo +7.94%/yr, t 8.22, over 5,264 days, gives δ/σ 0.113 before the haircut and 0.048 after it, so power is 0.63.
- Carding only H2 keeps K = 1 under D9's one-card rule. H1 fails power and H3 is unscreenable.
- **Cost is the risk.** At the repo's 1 tick/side slip, the leg is net negative at both illustrative USDJPY levels (100 and 150). It survives only with less than about 1.8 ticks of total round-trip slip at MFFU, for example with limit fills (dossier Reach; a worker-draft claim that it survived at 100 was corrected on 2026-11-04).
- Disclosed advisory priors:
  - Q-INVENTORY-1 killed this source family on the now-deleted 4× cost law;
  - the EURUSD fix-reversal add-back bar names "a different fix (Tokyo/Frankfurt)".

**M6E: pre-ECB-fix drift, conditional.**
- It has a named payer and a same-pair spot cohort, admitted under harvest §4a as 6J's is: KMW Table I, EUR pre-ECB −8.87%/yr, t −7.24, giving δ/σ 0.042 after the haircut and power 0.52.
- In-sample, the post-2014 dollar-portfolio leg shows no decay, which is the strongest decay evidence among the FX cells.
- Weaknesses:
  - power is marginal;
  - 0.3–0.6 tick of round-trip slip consumes the effect at the 58% haircut, so it is cost-bound;
  - it trips the letter of the EURUSD fix-reversal bar (advisory, Rule 26).
- It cannot freeze before the M6E repo landing (ledger, specs, `SHA256SUMS`).

## Constraints across the dossiers (for D10, Joshua's)

- **Firm slots under the 10-30 "one strategy per firm" reading:**
  - Superseded by the decision below: 6J goes to MFFU and M6E to Bulenox. MGC is skipped in R2.
  - An index card would want Bulenox (every index first pick moved off D10's Tradeify default, because Tradeify hosts ORB-MNQ and bars reuse at another firm), so it would now collide with M6E. No index card runs in R2.
- **D10 premise correction:** D10 says MFFU has "cheapest M6E costs". The repo-held commissions say otherwise:
  - Bulenox $0.50/side;
  - MFFU $0.72/side ($1.44 round trip);
  - Tradeify $0.80/side ($1.60 round trip).

  Sources: `core/firm_rules.py` comments at :102, :241, :371.
- **Same source family:** r2-6j-tokyofix and r2-m6e-prefix both rest on Krohn–Mueller–Whelan dealer fix intermediation.
  - They differ in instrument, fix and session window, so they are distinct under the working three-limb test; the shared counterparty class is disclosed.
  - Both sit in Tradeify's Currencies group. If a Currencies book (for example Aegis 6J) runs at Tradeify, ESA §6.7(c),(i) and BluSky's cross-firm hedging page make opposite simultaneous positions a breach.
  - Aegis's windows were not read (private surface), so overlap is an open check for a seat that may read it.
- **Same mechanism twice:**
  - overnight drift on MNQ, MYM and M2K;
  - intraday momentum on MYM and M2K.

  Each pair or triple can supply at most one card per round.

## UNSCREENABLE limbs (Req 2 unless stated)

| Dossier | Limb | What would supply it |
|---|---|---|
| r2-mnq-ovndrift | δ: ES only (SR917); NQ named with no number | K-charging δ probe on MNQ, split pre/post 2021 |
| r2-mnq-expin | δ: no signed figure (Golez–Jackwerth give an unsigned lower bound on ES monthly expiries) | probe; the sign is not entailed ex ante |
| r2-mym-overnight-drift | δ: ES only; YM named with no number | δ probe on MYM, split pre/post 2021 |
| r2-mym-intraday-momentum | event fraction of the long-only variant that ESA §6.7 forces | probe |
| r2-mym-overnight-drift, r2-mym-intraday-momentum | HOW-it-dies observable (signed flow, gamma) not on the admitted feed | an admitted order-flow source (Rule 18) |
| r2-m2k-ondrift | δ: no Russell cohort | δ probe on M2K |
| r2-mgc-cgb, r2-mgc-pdhpdl | δ: no gold intraday cohort; Req 1 also fails (no payer, 1b limbs unmet) | in-house δ extraction spending an MGC look, with a discriminator (IAAFT null for cgb) |
| r2-6j-tokyofix | H3 (gotobi-only pre-fix leg): no mean or σ (Bessho et al. give profit factor only) | probe with a gotobi dummy, or opening Akiyama et al. 2021 |
| r2-6j-psbc | δ: no 6J/USDJPY cohort; 1b limb (iv) fails | probe |
| r2-m6e-asialdn | δ: no EUR/USD cohort; 1a and all 1b limbs fail | probe, with the DL-2 geometric-feasibility diagnostic |

## Coordinator verification (Rule 0)

Every figure used for a screen, power or ranking call was re-read by the coordinator from the primary text on 2026-11-04 (PDF text extraction or raw HTML).

| Source | Checked |
|---|---|
| Krohn, Mueller & Whelan, BoC SWP 2021-48 (PDF sha256 `807fdb20dac0010b…`) | Table I: EUR pre-E −8.87 (−7.24); JPY pre-T −4.06 (−5.87), post-T 7.94 (8.22). Table II 2014–19 dollar portfolio: pre-T −1.59 (−2.64), post-T 2.08 (2.25), pre-E −3.14 (−2.28). Table VII: JPY 12.00 (10.12). Table IX: JPY −6.54 at full bid-ask. "5,264 daily observations". The post-2013 decline passages |
| Baltussen, Da, Lammers & Martens, *JFE* 142 (2021) | Table B1: ER β_ONFH t 4.62; YM β_ROD t 4.12. Table B3: GC β_ROD 1.09 (t 2.95). Appendix sample tables: ER 6,746, YM 5,639 and GC 9,044 obs |
| McLean & Pontiff, *JF* 71 (2016) | "26% lower out-of-sample and 58% lower post-publication"; "32% (58%–26%)" |
| Boyarchenko, Larsen & Whelan, SR917 | European-open hour "1.5" bp per hour per day, t 7.1; 1.48 bp per day |
| Liberty Street Economics, 2026-07-01 (raw HTML) | the "close to zero since 2021", NQ/YM and RSV 6.5% → 2.9% quotes above |
| Golez & Jackwerth, *JFE* 106 (2012) | "a shift of at least 11.00 bps" |
| Ito & Yamada, CJEB WP 352 | "the average return becomes 1.8bp"; "particularly high at 5th and 10th days" |
| Neely & Weller, FRB St. Louis WP 2011-021D | the "about zero in the 1990s" finding is Olson (2004) as cited by them, which the dossier attributes correctly |
| CME release (Mondovisione reprint) | NQ Tuesday/Thursday weekly options launch "on October 3" (2022) |

**Not verified by the coordinator**, labelled in each dossier:
- figures read only through summarising fetches (`[W-x]`): Bessho et al., MFFU help pages and the Gao et al. DIA row;
- Marshall, Cahan & Cahan (2008), read only as a secondary summary;
- Bulenox's treatment of a position opened after the Globex reopen;
- Striker's and Aegis's private windows.

Venue quotes are taken from the [venue-fact register](../../../notes/2026-11-01-prop-firm-venue-fact-register-DRAFT.md), the [envelope](../../../../ops/prop_envelope_default.md) and PR #1040's cross-firm draft, with each one's date. None is accepted into an owner record (Rule 17).

**Codex round 1 (head `4939ed6`):** spot cohorts relabelled as spot→futures transplants, so the 6J and M6E screens were made conditional on Joshua's ruling, which he gave on 2026-11-04 (harvest §4a, PR #1064); Aegis figures elided from pasted consult output (Rule 13).

**Corrections the coordinator made to worker drafts:**
- removed cell-revealing clock times;
- replaced a derived day count with KMW's stated 5,264;
- completed the reach and distinctness sections.

**Reading limits:**
- n is a calendar estimate; the pinned exports set the real n.
- Every power figure is gross: mid-quote or spot, before costs.
- A PASS on any limb licenses scoping only (Rule 25).
