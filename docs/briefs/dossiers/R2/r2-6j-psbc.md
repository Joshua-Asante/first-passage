# r2-6j-psbc: 6J × prior-session-breakout-continuation × Bulenox

Status: R2 dossier (Part A §A2–§A3, tasks T2–T3) · 2026-11-04 · K = 0 (no data read) · decides nothing; generation never blesses (Rule 25)

## Cell
- Instrument: 6J (full-size; no M6J at any firm) · Mechanism: `prior-session-breakout-continuation` (existing, minted 2026-08-22) · Provisional firm: Bulenox (D10 proposed mapping, not decided) · Session: London morning (European open up to the US morning). The break is measured against the prior full Globex session's high and low, and the position is flat well before the venue flat-by.
- Event frequency: at most one signal per session (k=1, per the MECHANISMS.md definition). The share of sessions with a qualifying break is unknown and would come from the panel (K-charging). This is supply-map cell #5 (generation DRAFT §8.3).

## Mechanism (harvest Req 1, path 1b)
- WHO pays: none named, so path 1b. The closest story is clustered stop-loss orders beyond prior extremes, which "stops get hunted" style accounts call a preference/behavioral driver. That is inadmissible under 1a (harvest §1).
- WHEN: London-session hours, keyed to the prior session's extremes (declared before data).
- WHY it persists: not argued (1b does not require it).
- HOW it dies: sign decay of breakout returns in the FX technical-rule literature. In repo terms: the edge CUSUM and the hit-rate decomposition that killed J16 (payoff ratio held, hit rate collapsed).
- 1b limbs, at the class level (FX channel/trend rules). No cohort exists for the exact construct.
  - (i) ≥3 decades of sample: **met (class)**. Olson (2004), cited in Neely & Weller (2013), covers 1971–2000 across 18 currencies.
  - (ii) ≥3 independent cohorts: **met (class)**. Many currency pairs.
  - (iii) a replication ≥10 years after discovery: **met (class)**. Neely & Weller, St. Louis Fed WP 2011-021D, revised 2013.
  - (iv) no known sign-reversal condition: **NOT met.** Neely & Weller (2013): Olson "finds that returns declined from the 1970s to about zero in the 1990s". And "in research on intraday technical trading strategies Neely and Weller (2003) found that realistic transaction costs eliminated very high gross excess returns in the case of four highly liquid currencies, the German mark, the Japanese yen, the British pound and the Swiss franc."
  - Overall: **1b fails on limb (iv).** Under Req 1 this is not an admissible seed unless the reviewer weighs the no-counterparty channel (capped K ≤ 3, §8.3).

## Effect priors (Req 2)
| Source (date accessed) | Cohort | Figure | Transplant? |
|---|---|---|---|
| Neely & Weller, *Lessons from the Evolution of Foreign Exchange Trading Strategies*, FRB St. Louis WP 2011-021D (rev. 2013); https://files.stlouisfed.org/files/htdocs/wp/2011/2011-021.pdf (2026-11-04) | daily FX technical rules (channel, MA, filter), majors and EM | qualitative only: decay to about zero by the 1990s; intraday JPY gross returns eliminated by costs (citing Neely & Weller 2003, JIMF 22) | class-level, and not this construct |
| M6A DL-2 (repo, lab/archive/dl2_m6a_pdhpdl_2026-08-22, via ops/instruments/M6A.md) | M6A/6A parent, same mechanism id | all 10 frozen variants net-negative on TRAIN; SPA p 0.9755; geometry infeasible | different instrument, so a transplant and inadmissible as δ (disclosed as a prior only) |

- Decay haircut: not applicable (no δ). If a cohort δ appears, use McLean & Pontiff (2016) 58% (see r2-6j-tokyofix).
- Screen figure: **UNSCREENABLE.** No published 6J or USDJPY intraday prior-session-break cohort with a mean and σ was found. A δ-extraction probe on the 6J panel would supply it, charging K (one of the 4 lifetime 6J builder looks, DRAFT §11).

## Prior consult (advisory, Rule 26)
```text
$ python3 -I scripts/fp.py python scripts/instrument_profiles.py cell 6J prior-session-breakout-continuation
=== 6J x prior-session-breakout-continuation ===
ledger: ops/instruments/6J.md
verdict: untested — no prior on this cell.
class finding (mechanism-wide, not specific to 6J): (M6A, 2026-08-22 — same day as minting): DL-2's TRAIN scoring closed AMBIGUOUS/ABANDONMENT the same day this id was minted — nominee V9 fails 3 of 4 nomination gates; a same-day geometric-feasibility diagnostic found the construction structurally infeasible on M6A and retired it for that instrument, with a stop-rule/re-proposal bar binding any successor. [`RESULTS.md`](../../lab/archive/dl2_m6a_pdhpdl_2026-08-22/RESULTS.md).
K bank: read ../../discovery_manifests/ — never trust a snapshot.
prior: Aegis-to-6J venue-transfer retains measured panel evidence (n=129, PF 2.318, ~50% venue haircut vs canonical) - parked as a scale-path decision, not falsified by the evidence. [#J1]
prior: The venue structurally throttles Aegis sizing: the 12-contract cap binds on 76% of trades, realizing effective risk ~0.5-1.0% against the locked 1.5% target. [#J5]
exit=0
```
- Register hits:
  - The M6A DL-2 ABANDONMENT is the only prior use of this id. It failed M-16 slip-stress, the cost law and SPA. Its re-proposal bar binds M6A, not 6J. 6J's tick is larger relative to its range (tick $6.25), so the geometry differs, but this has not been measured.
  - 6J J16 `orb-ny-breakout`: a breakout-continuation sibling on the same instrument, IS-real then OOS-falsified (PF 0.846). "The edge is the tail" (BOJ 2022-09-22 intervention and COVID 2020-03 cluster). Same entry family (stop-entry through a level), different reference level and window.
  - The MYM session-aware continuation class finding (MECHANISMS.md, `opening-range-continuation`) is a sibling continuation class, dead on MYM.
- Domain bars: the index-intraday OHLCV raised bar does not apply (non-index instrument). No FX domain bar exists.
- Family K bank (Req 3 disclosure): `fc_carry_6e6j6cl` K=1, closed. `t00_tradeify_book_lineage_2026_10_10` K=13, open. Informal 43-cell 6J 15m IS battery on 2026-08-25 with no manifest (6J.md session log): its cells are not in the repo, so overlap with this construct is **unknown**. DL-2 on M6A (K_intrinsic ≈ 10), a different family.

## Venue legality at Bulenox
- Native route: Rithmic third-party API, "$100 monthly fee" (envelope §4, 2026-10-02). NinjaScript runs through NT8.
- Product offered: full 6J at $2.36/side; no M6J (firm_rules.py; Rates PDF "Updated Aug/11/2026"). 100K cap is 12 full-size contracts.
- Flat-by: "All positions must be closed by 3:59 PM (CT)" = 16:59 ET (envelope §4, 2026-10-02). A London-morning window closes well before it.
- News: "News trading allowed" (envelope §4, 2026-10-02). London-morning windows collide with European and early US data. Record collision frequency only (E7 overlay).
- Hold: intra-session only; `weekend_holds: False`.
- Inactivity: ≥1 trade per 5 trading days. A k=1 conditional break may leave gaps, and this is unknown until measured.
- Drawdown: Option 1 intraday trail on open profit (envelope §4). Breakout payoffs are tail-shaped (J16), which is the profile the intraday trail punishes most.
- Cross-firm hedging / product group: Tradeify Currencies group (6J, M6E, …; 10495868, envelope §4a) together with ESA §6.7(c),(i) External Accounts (deep-dive item 5). The cell is two-sided. Opposite exposure to any Tradeify Currencies book (Aegis 6J, or M6E if MFFU's book is mirrored at Tradeify) must be prevented.

## Distinctness
- vs index ORB book: different instrument, product group and window (London morning, not the US cash open). The level comes from the prior session, not the current opening range. The entry type (stop through a level) is the **same family** as ORB, which weakens distinctness under DRAFT §10.2 open question 2.
- vs Aegis 6J: continuation versus Aegis's mean reversion, so the sign is often opposite on the same instrument. If both run at once, this raises the cross-account hedging risk, not just a correlation question.
- vs r2-6j-tokyofix: different window (London morning vs Tokyo morning) and mechanism (price-level break vs scheduled flow).
- vs other R2 dossiers: Shares the session-break family with r2-m6e-asialdn (London morning, stop entry) in the same Currencies group; distinct only by instrument and reference range. Differs from every non-FX dossier in instrument, product group and mechanism.

## Reach (T3)
- 5f reach (D7, `gates.reachability(k, n)` run 2026-11-04 through the fp launcher; arithmetic only, no data read). Banked builder K on this instrument: **0** on the public record (R1 is MCL-only and unrun; the builder ledger is private, so `ledger.k()` must confirm it at registration). Development sessions n ≈ **2,325**: window 2016-01-04..2026-11-02 (the calendar's 2016 start binds, not the export) ≈ 2,703 sessions by `ops/calendars/cme_holiday_calendar_2016_2026.json` (sha256 `407d93bb815ee6b2…`; weekdays less non-`NORMAL` dates), less D9's 378-session holdout. The pinned export sets the real n; FX holidays differ from the equity columns, so the calendar estimate is coarser for FX.
  | K (banked + this card) | 5f floor (annual SR) | P(pass \| SR 0.85) | P(pass \| SR 0.89) | Reachable (D7) |
  |---|---|---|---|---|
  | 1 (this card) | 0.542 | 0.825 | 0.855 | yes |
  | 2 | 0.713 | 0.662 | 0.705 | yes |
  | 3 | 0.822 | 0.533 | 0.581 | yes |
  | 4 | 0.888 | 0.454 | 0.502 | yes, at the boundary |
  Normal approximation; 5f only, so every other gate lowers P(pass). The instrument's lifetime budget is 4 looks (generation note §11).
- Power at expected event count: not computable (UNSCREENABLE). Upper bound on N is 2,325 (one per dev session); break-even δ/σ there is 0.0406. If only half the sessions break, N ≈ 1,163 and the break-even is 0.057.
- Cost and entry-slip sensitivity (M-16, printed only): Bulenox round-trip commission 2 × $2.36 = $4.72 = **0.76 ticks** (tick $6.25). M-16 binds fully because this is a stop entry. There is no per-event δ in price terms, so the slip that would consume it is **not computable**. The sibling DL-2 nominee failed M-16 slip-stress on M6A.
- Barrier feasibility: pending atlas (sibling session).
