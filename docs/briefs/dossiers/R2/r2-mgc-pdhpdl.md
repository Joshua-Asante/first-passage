# r2-mgc-pdhpdl: MGC × pdh-pdl-breakout-rth × BluSky

Status: R2 dossier (Part A §A2–§A3, tasks T2–T3) · 2026-11-04 · K = 0 (no data read) · decides nothing; generation never blesses (Rule 25)

## Cell
- Instrument: MGC (COMEX Micro Gold) · Mechanism: `pdh-pdl-breakout-rth` (existing; MNQ-minted 2026-08-10, untested on MGC) · Provisional firm: BluSky Premium (D10 proposed mapping, not decided) · Session: COMEX day session (US morning into early afternoon), reference = prior COMEX day-session high/low, flat well before the venue flat-by.
- Event frequency: ≤1 per session (mechanism definition: "first valid signal per session"). Fraction of MGC sessions with a qualifying break: **unpublished, not known at K = 0**. Upper bound N = 2,325 dev sessions.

## Mechanism (harvest Req 1, path 1a | 1b)
- WHO pays: none named: path 1b. (Stop-cluster / breakout-follower stories are preference/behavioural; ADR 2026-07-26 §2-A excludes them from 1a.)
- WHEN: a day-session close beyond the prior day-session extreme (state trigger, declarable ex ante).
- WHY it persists: no capacity/awkwardness argument available (would be "nobody noticed", inadmissible).
- HOW it dies: no constraint observable; only an edge CUSUM.
- 1b limbs:
  - (i) ≥3 decades: **not met** for an intraday-flat prior-day-level break on gold. Nearest: Marshall, Cahan & Cahan 2008 (*JBF* 32(9)) daily support/resistance rules on 15 commodity futures incl. gold, 1984–2005 (22 y, daily horizon, not intraday) — and that study is **negative** (data-snooping adjustment "eliminates reliable profits for 14 of 15 commodities"; secondary source CXO, abstract not on IDEAS).
  - (ii) ≥3 independent cohorts: **not met** (no peer-reviewed gold intraday cohort found; only vendor material, e.g. Unger Academy, unaudited).
  - (iii) replication ≥10 y after discovery: **not met** on gold intraday.
  - (iv) no known sign reversal: **not met / unknown**; the one in-repo cohort (MNQ CON-4) straddles zero both arms.
- **Req 1: FAIL on both paths at K = 0.** Admissible only via the no-counterparty statistical channel (declared K ≤ 3), not harvest.

## Effect priors (Req 2)
| Source (date accessed) | Cohort | Figure | Transplant? |
|---|---|---|---|
| Marshall, Cahan & Cahan 2008, *JBF* 32(9):1810–1819, via cxoadvisory.com summary (2026-11-04) | 15 commodity futures incl. gold, daily, 1984–2005; S/R + channel breakout among 7,846 rules | no reliable profit after data-snooping adjustment in 14/15 commodities; gold not named as the exception | Daily horizon (construct transplant); secondary source |
| MNQ CON-4 (in-repo, `ops/instruments/MECHANISMS.md`) | MNQ dense-1m, explore IS | long −0.007R / short +0.005R, CIs straddle | Cross-instrument: inadmissible as δ (prior only) |
| Search for gold-futures intraday PDH/PDL or ORB cohort (2026-11-04) | — | none found (vendor/blog only) | — |
- Decay haircut: n/a (no admissible δ). Would apply McLean & Pontiff 2016 (*JF* 71(1)) 58% post-publication decline if a published δ appeared.
- Screen figure: **UNSCREENABLE.** Supply route: an in-house δ-extraction on the MGC dev window (spends one of MGC's four builder looks, K ≥ 1; corrected 2026-11-05: the builder ledger's MGC bank is 8 ([note §11](../../../notes/2026-11-01-generation-phase-strengthening-DRAFT.md#11-updates-2026-11-04))) measuring post-break continuation as the card's discriminator; or a published COMEX gold intraday level-break cohort if one exists behind a paywall not reached here.

## Prior consult (advisory, Rule 26)
```text
=== MGC x pdh-pdl-breakout-rth ===
ledger: ops/instruments/MGC.md
verdict: untested — no prior on this cell.
class finding (mechanism-wide, not specific to MGC): MNQ PDH/PDL with-break (`Q-TNEC-CON-4`) explore → `AMBIGUOUS-HOLD` — long −0.007R / short +0.005R; CIs straddle; stop ≈257 pt; gross/(4×RT) ≈0.27×; not FALSIFIED; not live-pass; CONFIRM unread. [MNQ.md](MNQ.md) · [`RESULTS`](../../lab/analysis/c1/mnq_tnec_con4_pdh_pdl_break_2026-08/RESULTS.md)
BINDING BAR: free-data-5th-leg-snag-closed-2026-07-01 -> ../../docs/rejected_candidates.md
K bank: read ../../discovery_manifests/ — never trust a snapshot.
prior: Third-leg E-K elimination is void as a gate after K-bank ADR; large disclosed bank remains a Req-3 fact, not an inherited kill. DISC-CAMP-0 history is disclosure, not re-litigation. [#G1]
exit=1
```
Nearest-id consult also run: `prior-session-breakout-continuation` (full-session sibling) → untested on MGC; class finding M6A DL-2 AMBIGUOUS/ABANDONMENT, "structurally infeasible on M6A"; same binding bar; exit=1.
- Register hits: (1) `free-data-5th-leg` SNAG-CLOSED 2026-07-01 (binding bar; its text: "another free-data mechanism … a different instrument … do not clear"). Prior MGC cards answered it "CLEAR via R-FRAMING §2.1" (non-index MSL framing; MGC.md 2026-08-12b, MSL-S4 STAGE1) — that framing is MSL-charter-owned and MSL closed 2026-10-25; whether it carries to a builder card is the coordinator's call. Advisory under Rule 26 (2026-10-31). (2) MSL-C2 London fade × MGC FALSIFIED; bar "new mechanism evidence (different reference class / direction / TF)" — this cell differs in reference class (prior day vs London) and direction (continuation vs fade). C2's DELETE limb noted a sham prior-RTH reference was "less negative" than London — a fade result, not evidence for continuation. (3) Gold fix `event-window-reversal` DEAD — unrelated window; bar quoted in MGC.md. (4) `daily-range-state-persistence` DEAD, `expiry-oi-strike-convergence` AMBIGUOUS-PARKED — not this mechanism. (5) MGC.md 2026-08-25: informal survey "6 families / ~46 disclosed cells, all NULL" on MGC 15m, families unrecorded in repo — **may overlap this cell; cannot verify** (local-only evidence).
- Domain bars: index-intraday OHLCV raised bar does not apply (non-index; scope excludes "non-index complexes").
- Family K bank (Req 3 disclosure): GC/MGC **3,177** (`discovery_manifests/disccamp0_gc_2010_18.json`, `K: 3177`, catch22/STUMPY/ruptures on GC 1h 2010-06..2018-12, closed). Disclosure only (ADR 2026-08-04). Builder looks: MGC 4 lifetime (generation note §11); builder ledger not read.

## Venue legality at BluSky
- Native route: "Semi-automated and full automated" welcomed (envelope §4 BluSky row; not re-read 2026-10-02); NinjaScript via Tradovate/NT rail or Rithmic-class platforms (envelope §4, `help.blusky.pro/.../17115915`, re-verified 2026-10-02). Conduct policy 12069208 bans "Account Mirroring" (envelope, flagged). · Product offered: MGC on 17115915 commission table (MGC $0.99/$1.19/$1.29 by NT plan; envelope §4, 2026-10-02). · Flat-by: "We recommend closing all trades before 4:45PM EST"; auto-liq ~15 min pre-close, best-effort (12434059 dated 2026-08-12; envelope, re-verified 2026-10-02). · News: "Trading news events at your own risk" — does not fail the account [eval] (12434059, 2026-10-02). · Hold: no weekend/overnight (`core/firm_rules.py` `weekend_holds: False`). · Cross-firm hedging / product group: 12434059 lists "Hedging is not allowed in Futures Trading" among failing acts — scope (cross-account, cross-firm) unclear, page self-contradicts (venue register A1.4, 2026-11-01). BluSky cross-firm/ToS bot clauses **not read** (register §E row 1). Tradeify ESA §6.7(c),(i) binds only if a Tradeify account holds an opposing Metals position (none today: MGC × Select 100K CLOSED, W5).
- Rope: BluSky_Premium_100K $3,000 EOD trail, breach "at any point" (firm_rules; envelope). **Same $3,000 rope as Select 100K → W5's 34% (2026 vol, 0.75×ADR20 stop) transfers unchanged; 50K ($2,000) ≈ 51% [INF arithmetic: 34% × 3,000/2,000].** A stop at the opposite prior-day extreme is ≈ one prior-day range, wider than W5's reference stop, so worse [INF]. MFFU alternative: funded metals micros capped 3/5/10/15 (25K–150K), SI/HG/PL restricted "temporary" (envelope §4, 9735811, 2026-10-02) — cap not binding at 1 micro.

## Distinctness
- vs index ORB book: different product group (Metals vs Equity Index), instrument, reference (prior-day level vs current-day opening range), clock (level-triggered, not open-anchored). Builder has no level-break block today (ORB only, note §8.3).
- vs other R2 dossiers: The only Metals-group dossier besides r2-mgc-cgb, from which it differs in mechanism (prior-day level break vs compression break). Its trigger is a price level, not a clock-anchored range, which separates it from ORB. No other dossier uses `pdh-pdl-breakout-rth`.

## Reach (T3)
- 5f reach (D7, `gates.reachability(k, n)` run 2026-11-04 through the fp launcher; arithmetic only, no data read). Banked builder K on this instrument: **0** on the public record (R1 is MCL-only and unrun; the builder ledger is private, so `ledger.k()` must confirm it at registration). Development sessions n ≈ **2,325**: window 2016-01-04..2026-11-02 (the calendar's 2016 start binds, not the export) ≈ 2,703 sessions by `ops/calendars/cme_holiday_calendar_2016_2026.json` (sha256 `407d93bb815ee6b2…`; weekdays less non-`NORMAL` dates), less D9's 378-session holdout. The pinned export sets the real n.
  | K (banked + this card) | 5f floor (annual SR) | P(pass \| SR 0.85) | P(pass \| SR 0.89) | Reachable (D7) |
  |---|---|---|---|---|
  | 1 (this card) | 0.542 | 0.825 | 0.855 | yes |
  | 2 | 0.713 | 0.662 | 0.705 | yes |
  | 3 | 0.822 | 0.533 | 0.581 | yes |
  | 4 | 0.888 | 0.454 | 0.502 | yes, at the boundary |
  Normal approximation; 5f only, so every other gate lowers P(pass). The instrument's lifetime budget is 4 looks (generation note §11).
- Power at expected event count: **not computable (UNSCREENABLE).** Break-even for power 0.50 is δ/σ ≥ 1.96/√N: 0.041 at N = 2,325 (break every session); 0.057 at half; 0.081 at a quarter (frequency grid illustrative, not estimates).
- Cost and entry-slip sensitivity (M-16, printed only): MGC tick $1.00 (`core/instrument_specs.py`). BluSky commission: repo proxy $1.20/side (`firm_rules.py`, "NOT venue-published") → 2.4 ticks RT; venue range $0.50/side Rithmic-class eval (1.0 tick RT) to $1.29/side NT free plan (2.58 ticks RT). Plus builder slippage 1 tick/side → **RT ≈ 4.4 ticks (proxy), 3.0–4.6 range.** Entry-slip ticks to consume δ: not computable (no δ). M-16 applies squarely (stop/break entry): slip sweep {0, 0.5, 1, 1.5} ticks before any exit/sizing/MC.
- Barrier feasibility: pending atlas (sibling session).
