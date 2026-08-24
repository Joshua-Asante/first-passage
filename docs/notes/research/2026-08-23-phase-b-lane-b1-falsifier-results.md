# Phase B Lane B1 (MOC-imbalance wake, MES) — falsifier task results

**Date:** 2026-08-23
**Plan:** [`Phase B mechanism supply`](../../superpowers/plans/2026-08-23-viable-strategy-phase-b-mechanism-supply.md) — Lane B1, tasks B1.0/B1.1/B1.2/B1.4
**Owner artifacts:** [`F1 ruling`](../../briefs/2026-07-27-f1-moc-imbalance-mym-ruling.md) (the re-proposal bar B1 routes through) · [`ops/instruments/MES.md`](../../../ops/instruments/MES.md) · [`ox-alpha notice`](../notice/N-2026-08-23-ox-alpha-mechanism-supply-candidates.md) (zero authority; framing only)
**Authorization:** operator per-lane GO this session for B1/B2 (task brief). No card opened; no admission bar claimed cleared; B1.3 (operator bar-reading) explicitly **not** ruled here.

Catalog attestation (this session, before writing): `lab/CATALOG.md` / `docs/briefs/INDEX.md` / `docs/rejected_candidates.md` carry no B1/MOC-imbalance-MES harness slug — nothing duplicated.

---

## B1.0 — venue/hours + cost-floor recompute

**CME afternoon-pause fact-check — the plan's premise is stale.** The daily 3:15–3:30pm CT (16:15–16:30 ET) equity-index halt that `ops/instruments/MES.md` and the ox-alpha notice both assume ("the wake window fragments into 16:01–16:15 and 16:30–16:45") **was removed by CME Group effective 2021-06-28** ("the halt was initially implemented to account for transactions conducted via open outcry in the trading pits and is therefore no longer necessary" — CME Group announcement, corroborated independently by a CFTC equity-index-products filing describing the halt as **month-end-only** going forward). On every non-month-end session the 16:01–16:45 ET wake window is **continuous**, not fragmented; the halt persists only on the last trading day of each month (16:15–16:30 ET that one day). This is a correction owed to `MES.md`'s `venue_note` and the ox-alpha notice's Candidate-2 row — not made in this note (out of this task's scope; flagged for the operator / a follow-up touch).
Sources: [Optimus Futures community post quoting the CME announcement](https://community.optimusfutures.com/t/cme-group-equity-index-products-trading-session-update/4355); [CFTC filing describing the month-end-only halt](https://www.cftc.gov/sites/default/files/filings/orgrules/18/01/rule012618cbotdcm002.pdf).

**MES contract facts — confirmed, matches `ops/instruments/ES.md` L4.** $5/point multiplier, $1.25/tick (0.25-point tick), quarterly expiry. Cross-checked against three independent broker/CME-derived sources (Ironbeam contract-spec page, QuantVPS, Schwab); all agree.

**Cost-floor recompute — corrects the plan's "~2.3 ES-points/trade" figure.** Current `Tradeify_Select_100K.cost_per_side_usd` = **$0.91** (`core/firm_rules.py` L378, re-read this session — verification command below), unchanged from the F1 ruling's own citation. Applying the repo's standing crossing-slippage convention for Tradeify index micros (1 tick/side × 2 sides — the same formula `docs/briefs/rnd-pipeline/SLR-MYM-1-liquidity-sweep-reclaim-scoping.md` L149 uses for MYM: `slippage = ticks_per_side × tick_value × 2`):

```
commission_RT = 2 × $0.91                    = $1.82
slippage_RT   = 1.0 tick/side × $1.25 × 2     = $2.50
RT_cost       = $1.82 + $2.50                 = $4.32
4x cost-law hurdle = 4 × $4.32                = $17.28
points required     = $17.28 / $5 per point   ≈ 3.46 MES/ES points/trade
```

**≈3.46 points, not ≈2.3.** For context, `ops/instruments/MES.md`'s own already-published `cost_hurdle` (6.84bp ≈ 2.99–3.0 points at the ~4373 study reference price) uses a *different* frozen model — `lab/discovery/cost_es.py`'s ES-parent H-OD-1 passive model ($3.00/side conservative commission assumption, 0.5-tick-RT slippage, explicitly **not** the real Tradeify cost basis; its own docstring says "MES micro cliff is a separate Stage-7 read"). Both real recomputations (≈3.0 pts via the ES-parent passive model, ≈3.46 pts via the Tradeify-crossing model this task was asked to use) land well above the plan's ≈2.3-point estimate — a correction, not a confirmation.

---

## B1.1 — literature route (Requirement 1b)

**Outcome B: no citable δ found.** Real search run (not a guess) for a published cohort effect-size for **post-close, imbalance-sign-conditioned, index-futures** reversal — the exact object the F1 ruling named as missing. Nearest hits, and why none qualifies:

- *Predicting US stock returns using closing auction imbalance data* (Imperial College) — predicts the **closing print itself** for **individual NYSE stocks** using auction-window imbalance data (Apr–Aug 2020); not a post-close reversal, not index futures.
- BMLL / Alpha Architect summaries of closing-price-deviation reversal — reports that stock closing-price deviations "reverse almost fully overnight," "one-third to one-half... within the first half-hour" — but this is **individual-stock** deviation-from-fair-value reversal, not conditioned on the **signed** MOC imbalance number, and not index futures.
- Chordia et al. 2002 (order imbalance → next-day cash-equity returns, 1988–98) — cash equities, general order-flow imbalance (not specifically the closing/MOC print), not futures.
- No hit for "MES/ES futures react to NYSE's 3:50pm imbalance publication" specifically; a Substack piece (Siram Capital Research, "MOC imbalance is there an edge, Part 1") proposes exactly F1/B1's mechanism on ES but explicitly reports **zero backtest data** — "I have not yet conducted the analysis... collect data and send it to me." Not a citable δ.

**Conclusion:** B1.1 = Outcome B, as F1's own ruling predicted was likely. B1.2 is the load-bearing door.

---

## B1.2 — free-access check for the paper-log

**A candidate free source exists — not a clean "no" the way B1.1 was.** Financial Juice (financialjuice.com; also republished on public X/Twitter and a public Telegram channel, ~7K subscribers, no login required) republishes a **signed dollar imbalance figure per major index** (S&P 500, Nasdaq 100, Dow 30, "Magnificent 7") in the ~15:45–15:51 ET window — a live fetch of `financialjuice.com/News/8389646/MOC-Imbalance.aspx` this session showed `S&P 500: +1.2 bln / Nasdaq 100: +1.2 bln / Dow 30: +400 mln / Mag 7: +200 mln`, timestamped `19:51` (UTC ≈ 15:51 ET), with sign visible on the free page. Historical X posts going back to at least 2021 ("MOC IMBALANCE 288 MLN SELL-SIDE.") confirm this is a **standing, recurring** practice, not a one-off.

**Caveats, stated plainly (these are why this is not a clean "yes" either):**
1. This is an **unofficial republication** of a licensed feed (NYSE Order Imbalance Information / Nasdaq NOII) by a third-party news aggregator, not NYSE's own free product. No SLA, no guarantee of coverage on every session, no guarantee it survives as a free offering.
2. The web page showed some login/signup prompts alongside the free headline figures ("VOICE NEWS... DELAYED"); it is not confirmed whether the core imbalance number itself is ever paywalled on higher-volume days.
3. Timing precision across many sessions (does it reliably land by ~15:50–15:52 ET every day, or does it drift) was **not** measured — one live sample plus historical search hits, not a monitored run.
4. It is a single source with no free cross-check; if Financial Juice's own number is wrong or delayed on a given day, nothing here catches it.
5. This is the aggregate **index-level** imbalance (S&P 500 total), which is the right object for a market-wide MES fade — not the per-stock imbalance list (Market Chameleon's free page, ~15-min-delayed, >50K-share stocks only — checked and ruled out as the live signal source: wrong granularity, wrong latency).

NYSE's own free tool (`cmegroup`/`nyse.com` closing-imbalance-analysis-tool) was also checked and ruled out for the live-signal use case: it is **historical only** (trailing 3 months), **per-stock**, not a same-day aggregate feed.

**Conclusion:** a free source that plausibly clears "republished free at ~15:50 ET on a broker/public platform" exists, with real reliability/completeness caveats attached, not verified as robust enough to make it a clean pass — an operator-adjacent read, not a mechanical one.

**A sharper point, load-bearing for B1.3 and not to be missed:** F1's own ruling (§6, re-open condition 3) explicitly anticipated a free-source finding and named its effect **precisely** — *"the data becoming freely available... would reverse the sign of the argument, dropping F1 straight into the D2 free-data kill rather than rescuing it."* Financial Juice is an **unofficial third-party republication**, not NYSE's own feed going free — whether that distinction matters for F1's "the data becoming freely available" clause is exactly the kind of reading only the operator can make. If it counts, B1.2's finding does not open a re-proposal door at all; it triggers F1's own named reversal into the already-SNAG-closed free-data domain (2026-07-01, `docs/rejected_candidates.md`). If it doesn't count (an unofficial, unreliable redistribution is not "the data," only a lossy proxy for it), the Phase-B plan's own frozen PARK criteria is the operative standard, and B1.2's finding keeps the lane open under *that* text. **Both readings are named here; neither is decided.**

---

## Frozen kill criteria — does NOT self-clear

> "no free sign source AND no citable δ → PARK" (plan L60)

B1.1 = no citable δ (confirmed). B1.2 = **a candidate free source was found**, not a clean absence. The conjunction required for PARK does not hold. Per the task's own branching instruction, this is **not** a mechanical self-clearing outcome — no registry row is added, and B1.3 is **not** ruled here.

---

## B1.4 — shape pre-check against the A2 region

Already directly answered by the A2 RESULTS' own first-consumer check — [`shape_feasibility_map_2026-08/RESULTS.md`](../../../lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md) §8(ii), re-read this session:

> "B1... its own row already commits to a predicted shape: 'bounded window, clustered wins, ~2–4 events/week.' That maps directly onto this map's axes: `shape=bounded_clustered`, `cadence∈{2,3}`... at risk=$275 those two columns already show the floor B1's own eventual win-rate measurement will be read against: cadence=2 needs `win_rate≥65%` to clear `FEASIBLE`; cadence=3 needs `≥65%` clean or `60%` `MARGINAL`."

Confirmed against §6.2's `bounded_clustered` (risk=$275) table directly: cadence=2 → 60% INFEASIBLE (bust 5.9%), 65% FEASIBLE (bust 1.6%, pass 98.4%); cadence=3 → 60% MARGINAL (bust 3.6%), 65% FEASIBLE (bust 1.0%, pass 99.0%).

**Reading for the operator:** B1 needs a mechanism whose real, measured win rate is **≥65%** (clean) or **60%** at cadence-3 only (MARGINAL, not a pass) to survive this venue's $3,000 trailing-DD gate at the EM2 mid-tier ($275/trade) risk level. B1 has **zero measured win-rate evidence** for its own mechanism — F1 was rejected at the procurement gate before any measurement was possible, and B1.1 found no transplantable δ either. This is a target the eventual paper-log/backtest will be read against, not a verdict on B1 itself — no shape/win-rate claim is made about the real mechanism here.

---

## Disposition

**LIVE-AWAITING-BAR-READING.** Lane does not self-clear to PARK (B1.2 found a candidate free source); B1.3 needs an explicit operator ruling. See structured output for the exact bar-reading question.

---

## Verification

```bash
# Current Tradeify_Select_100K cost_per_side_usd (repo fact used in the B1.0 recompute)
grep -A12 '"Tradeify_Select_100K": {' core/firm_rules.py | grep "cost_per_side_usd"
# Expected: 0.91
# Or directly:
python -c "import sys; sys.path.insert(0,'core'); sys.path.insert(0,'.'); from core.firm_rules import FIRM_RULES as F; print(F['Tradeify_Select_100K']['cost_per_side_usd'])"
# Expected: 0.91

# MES contract basis already on file (cross-check against this note's independent web confirmation)
grep -n "MES.*\$5/pt\|1.25 tick" ops/instruments/ES.md
# Expected: 2 hits, L4 (headline) + L52 (E4 row, same figures restated)

# F1 ruling's own re-proposal bar text (what B1.1/B1.2 route through)
grep -n "published cohort δ for imbalance" docs/briefs/2026-07-27-f1-moc-imbalance-mym-ruling.md

# F1's own "free data reverses, doesn't rescue" clause (load-bearing for the B1.3 question)
grep -n "reverse" docs/briefs/2026-07-27-f1-moc-imbalance-mym-ruling.md

# A2's own B1 shape-pre-check citation (B1.4 source, not re-derived)
# (phrase wraps across a line break in the source file, so match the two halves separately)
grep -n "bounded window" docs/superpowers/plans/2026-08-23-viable-strategy-phase-b-mechanism-supply.md
grep -n "clustered wins" docs/superpowers/plans/2026-08-23-viable-strategy-phase-b-mechanism-supply.md
grep -n "cadence=2" lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md

# No registry row added by this note (kill criteria did not self-clear)
grep -c "moc-imbalance" docs/rejected_candidates.md
# Expected: unchanged from pre-session count (this note adds none)
```

External (non-repo) claims in this note — CME halt-removal date, MES broker-spec cross-checks, the literature search results, and the Financial Juice free-page fetch — are **not** repo-greppable; their sources are cited inline as URLs and were fetched live this session (2026-08-23), not recalled from training data.
