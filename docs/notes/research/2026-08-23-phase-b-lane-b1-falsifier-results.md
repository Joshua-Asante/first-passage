# Phase B Lane B1 (MOC-imbalance wake, MES) — falsifier task results

**Date:** 2026-08-23
**Plan:** [`Phase B mechanism supply`](../../superpowers/plans/2026-08-23-viable-strategy-phase-b-mechanism-supply.md) — Lane B1, tasks B1.0/B1.1/B1.2/B1.4
**Owner artifacts:** [`F1 ruling`](../../briefs/2026-07-27-f1-moc-imbalance-mym-ruling.md) (the re-proposal bar B1 routes through) · [`ops/instruments/MES.md`](../../../ops/instruments/MES.md) · [`ox-alpha notice`](../notice/N-2026-08-23-ox-alpha-mechanism-supply-candidates.md) (zero authority; framing only)
**Authorization:** operator per-lane GO this session for B1/B2 (task brief). No card opened; no admission bar claimed cleared; B1.3 (operator bar-reading) explicitly **not** ruled here.

Catalog attestation (this session, before writing): `lab/CATALOG.md` / `docs/briefs/INDEX.md` / `docs/rejected_candidates.md` carry no B1/MOC-imbalance-MES harness slug — nothing duplicated.

---

## B1.0 — venue/hours + cost-floor recompute

**CME afternoon-pause fact-check — the plan's premise is stale.** The daily 3:15–3:30pm CT (16:15–16:30 ET) equity-index halt that the **plan doc itself** (L39–40: "the wake window fragments into 16:01–16:15 and 16:30–16:45") and the **ox-alpha notice** (`N-2026-08-23-ox-alpha-mechanism-supply-candidates.md` L43) both assume **was removed by CME Group effective 2021-06-28** ("the halt was initially implemented to account for transactions conducted via open outcry in the trading pits and is therefore no longer necessary" — CME Group announcement, corroborated independently by a CFTC equity-index-products filing describing the halt as **month-end-only** going forward). On every non-month-end session the 16:01–16:45 ET wake window is **continuous**, not fragmented; the halt persists only on the last trading day of each month (16:15–16:30 ET that one day).

**Correction: `ops/instruments/MES.md` is NOT the file carrying this stale premise.** Read in full this session — its `venue_note` (L16) is about Tradeify Equity Index Product Group occupancy/withdrawal, and says nothing about CME hours, halts, or a fragmented window. The stale fragmented-window claim lives only in the plan doc (L39–40) and the ox-alpha notice (L43); those are the two artifacts a correction is owed to, not `MES.md`. (An earlier draft of this note wrongly named `MES.md` as the correction target — flagged and fixed here; still out of this task's scope to actually edit the plan/notice text.)

**This fact was already in the repo's own corpus — should have been grepped before treating it as an external finding.** `lab/analysis/c1/tradeify_fade_stage0_2026-07-30/RESULTS.md` L22 ("The HALT was in force through ~2021-Q2 and was removed afterwards...") and `lab/analysis/c1/tvcov_2026-07/RESULTS.md` L70 ("the CME equity-index daily maintenance halt (16:15–16:30 ET), eliminated in 2021") both already state the same removal, independently, from prior sessions' own work. Per the standing lesson ("unpriced branch? search the corpus" — `feedback_unpriced_branch_search_the_corpus`), this should have been found by `grep -rn "16:15" lab/` first; the CME-announcement/CFTC-filing web sources below are corroboration of an already-known repo fact, not a fresh discovery.
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

**A candidate free source exists in principle — but the evidence for it is weaker than this note first claimed, and one load-bearing claim below was wrong.** Financial Juice (financialjuice.com; also republished on public X/Twitter and a public Telegram channel, ~7K subscribers, no login required) republishes a **signed dollar imbalance figure per major index** (S&P 500, Nasdaq 100, Dow 30, "Magnificent 7") in the ~15:45–15:51 ET window, in the format `financialjuice.com/News/<id>/MOC-Imbalance.aspx`.

**Correction (re-fetched this session to verify): the specific page fetched is NOT a live, current-session confirmation.** The prior draft of this note described `financialjuice.com/News/8389646/MOC-Imbalance.aspx` as "a live fetch this session" showing `S&P 500: +1.2 bln / Nasdaq 100: +1.2 bln / Dow 30: +400 mln / Mag 7: +200 mln` timestamped `19:51 (UTC ≈ 15:51 ET)`, and presented that as same-day evidence. Re-fetched again this session (2026-08-24) to check: **the page itself is dated `06 Sep 2024 19:51`** — a static, ~2-year-old article, not today's imbalance figure. The fetch action was live; the *content returned* is historical. The prior phrasing quoted only the time-of-day and never the date, which reads as a same-day confirmation it is not. This is corrected here because it is the single most consequential claim in the note: it is the fact that keeps B1.2 from being a clean absence, which is what keeps the plan's frozen PARK conjunction from self-clearing.

**What the corrected evidence actually supports, and what it does not:**
- It confirms Financial Juice **has published**, at least once (2024-09-06), a free, no-login, signed-imbalance article in this exact format/URL pattern. That the format and URL pattern exist at all is real.
- It does **not** confirm the page (or a same-day equivalent) is being republished **today**, or on any regular cadence through 2026. No current-dated instance of this article type was found this session — attempts to find one (site search, a Bing site-search, an X/Twitter search for `from:FinancialJuice "MOC IMBALANCE"`) either 404'd, returned no on-topic results, or hit an auth wall, and are **not** independently confirmed here either way.
- The prior draft's other supporting claim — "historical X posts going back to at least 2021 ('MOC IMBALANCE 288 MLN SELL-SIDE.') confirm this is a standing, recurring practice" — is carried forward from the prior session's search **unverified by this fix pass** (X search requires login and could not be re-checked). It should be read as an uncorroborated claim, not a confirmed fact, until someone re-verifies it directly.

**Caveats, stated plainly (these are why this is not a clean "yes" either — and the first one is now the load-bearing one, not an afterthought):**
0. **No current/live instance of this republication has actually been observed.** The one concrete artifact in hand is a single dated (2024-09-06) article. Whether Financial Juice still runs this feature in 2026, and at what cadence, is unverified.
1. This is an **unofficial republication** of a licensed feed (NYSE Order Imbalance Information / Nasdaq NOII) by a third-party news aggregator, not NYSE's own free product. No SLA, no guarantee of coverage on every session, no guarantee it survives as a free offering.
2. The web page showed some login/signup prompts alongside the free headline figures ("VOICE NEWS... DELAYED"); it is not confirmed whether the core imbalance number itself is ever paywalled on higher-volume days.
3. Timing precision across many sessions (does it reliably land by ~15:50–15:52 ET every day, or does it drift) was **not** measured — no monitored run exists.
4. It is a single source with no free cross-check; if Financial Juice's own number is wrong, delayed, or discontinued, nothing here catches it.
5. This is the aggregate **index-level** imbalance (S&P 500 total), which is the right object for a market-wide MES fade — not the per-stock imbalance list (Market Chameleon's free page, ~15-min-delayed, >50K-share stocks only — checked and ruled out as the live signal source: wrong granularity, wrong latency).

NYSE's own free tool (`cmegroup`/`nyse.com` closing-imbalance-analysis-tool) was also checked and ruled out for the live-signal use case: it is **historical only** (trailing 3 months), **per-stock**, not a same-day aggregate feed.

**Conclusion (revised after the date correction above):** what was found is evidence that a free republication **of this exact format has existed** (one dated 2024-09-06 artifact, plus an unverified claim of recurrence back to 2021) — not a verified-live, currently-operating free source. That is a materially weaker finding than "a candidate free source was found this session," which is how the prior draft characterized it. It is still not a **clean absence** the way B1.1 was (B1.1 was a real search that returned nothing on-topic at all; B1.2 has a concrete, dated, on-topic artifact in hand) — but whether "a format that existed once, unverified as current" is enough to keep the plan's PARK conjunction from closing is itself a judgment call, not a mechanical read of the plan text. Not decided here.

**A sharper point, load-bearing for B1.3 and not to be missed:** F1's own ruling (§6, re-open condition 3) explicitly anticipated a free-source finding and named its effect **precisely** — *"the data becoming freely available... would reverse the sign of the argument, dropping F1 straight into the D2 free-data kill rather than rescuing it."* Financial Juice is an **unofficial third-party republication**, not NYSE's own feed going free — whether that distinction matters for F1's "the data becoming freely available" clause is exactly the kind of reading only the operator can make, and it is now compounded by the weaker evidentiary footing above (is a once-observed, unverified-as-current republication even "the data becoming freely available" in the sense F1 meant?). If it counts, B1.2's finding does not open a re-proposal door at all; it triggers F1's own named reversal into the already-SNAG-closed free-data domain (2026-07-01, `docs/rejected_candidates.md`). If it doesn't count (an unofficial, unreliable, unconfirmed-as-current redistribution is not "the data," only a lossy and unverified proxy for it), the Phase-B plan's own frozen PARK criteria is the operative standard, and the question becomes whether this weak a finding even clears that text's bar. **Both readings are named here; neither is decided.**

---

## Frozen kill criteria — does NOT self-clear

> "no free sign source AND no citable δ → PARK" (plan L60)

B1.1 = no citable δ (confirmed). B1.2 = a dated (2024-09-06), unverified-as-current artifact of a free republication format was found — weaker than "a candidate free source," but also not the clean absence B1.1 was. Whether that clears the plan text's "free sign source" bar is a judgment call this note does not make. Because it is not a mechanical resolution either way, the conjunction is **not** mechanically satisfied and this is **not** treated as a self-clearing PARK — no registry row is added, and B1.3 is **not** ruled here.

---

## B1.4 — shape pre-check against the A2 region

Already directly answered by the A2 RESULTS' own first-consumer check — [`shape_feasibility_map_2026-08/RESULTS.md`](../../../lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md) §8(ii), re-read this session:

> "B1... its own row already commits to a predicted shape: 'bounded window, clustered wins, ~2–4 events/week.' That maps directly onto this map's axes: `shape=bounded_clustered`, `cadence∈{2,3}`... at risk=$275 those two columns already show the floor B1's own eventual win-rate measurement will be read against: cadence=2 needs `win_rate≥65%` to clear `FEASIBLE`; cadence=3 needs `≥65%` clean or `60%` `MARGINAL`."

Confirmed against §6.2's `bounded_clustered` (risk=$275) table directly: cadence=2 → 60% INFEASIBLE (bust 5.9%), 65% FEASIBLE (bust 1.6%, pass 98.4%); cadence=3 → 60% MARGINAL (bust 3.6%), 65% FEASIBLE (bust 1.0%, pass 99.0%).

**Reading for the operator:** B1 needs a mechanism whose real, measured win rate is **≥65%** (clean) or **60%** at cadence-3 only (MARGINAL, not a pass) to survive this venue's $3,000 trailing-DD gate at the EM2 mid-tier ($275/trade) risk level. B1 has **zero measured win-rate evidence** for its own mechanism — F1 was rejected at the procurement gate before any measurement was possible, and B1.1 found no transplantable δ either. This is a target the eventual paper-log/backtest will be read against, not a verdict on B1 itself — no shape/win-rate claim is made about the real mechanism here.

---

## Disposition

**RESOLVED — B1.3 ruled `ADMIT`, operator, 2026-08-24, real-time GO.** The corrected (weaker) B1.2 evidence still counts as "a free sign source" for the plan's PARK-conjunction purposes, and F1's §6 condition-3 reversal clause does **not** trip — the operator's reading is that an unofficial third-party republication is not the same as "the data becoming freely available" in the sense F1 meant (F1 anticipated the licensed feed itself going free, not a lossy, unverified, unofficial proxy for it). The lane does not self-clear to PARK and is not ruled dead by the reversal clause either — it stays open, per the task's own "on admit" branch (Task B1.5).

**Next step (not executed by this note or session — spans real calendar time):** Task B1.5's "historical test if B1.1 found data" branch does not apply (B1.1 found no citable δ). The licensed path is the **20-session forward paper-log** — a genuinely real-time observation task (record Financial Juice's daily signed imbalance figure each session at ~15:50 ET, then check MES's post-close/next-session price action against the B1.4 target: win_rate ≥65% clean at cadence 2, or ≥65% clean / 60% MARGINAL at cadence 3, risk=$275) — that cannot be fabricated or compressed into a single working session. See the follow-up scaffolding note for how this is being tracked.

<details><summary>Original (pre-ruling) disposition text, superseded above — kept for the audit trail, not deleted</summary>

LIVE-AWAITING-BAR-READING. Lane does not mechanically self-clear to PARK — B1.2's finding, even after the date correction above knocks it down from "a candidate free source found" to "a dated, unverified-as-current artifact of a free republication format," is still not the clean absence the plan's frozen text requires alongside B1.1's clean absence. Whether that weaker finding is enough to keep the door open, or whether it should now be read as effectively no free source, is a judgment call this note does not make. B1.3 needs an explicit operator ruling on both the strength of the (now corrected) B1.2 evidence and the F1 §6 reversal-clause question. See structured output for the exact bar-reading question.

</details>

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

# Confirm MES.md's venue_note carries no CME-hours/halt/fragmented-window claim
# (the correction in B1.0 is owed to the plan doc + ox-alpha notice, NOT this file)
grep -n "venue_note" ops/instruments/MES.md
# Expected: L16, mentions Tradeify Equity Index Product Group / occupancy release only —
# no "16:15", "16:30", "halt", "pause", or "fragment" text anywhere in the file.
grep -ni "16:15\|16:30\|halt\|pause\|fragment" ops/instruments/MES.md
# Expected: no output (confirms the file does not carry the stale premise)

# Confirm the CME-halt-removal fact was already in the repo corpus before this session
# (per MEMORY.md "unpriced branch? search the corpus" — should have been grepped first)
grep -n "removed afterwards\|eliminated in 2021" lab/analysis/c1/tradeify_fade_stage0_2026-07-30/RESULTS.md lab/analysis/c1/tvcov_2026-07/RESULTS.md
# Expected: 2 hits, one per file

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

External (non-repo) claims in this note — CME halt-removal date, MES broker-spec cross-checks, the literature search results, and the Financial Juice free-page fetch — are **not** repo-greppable; their sources are cited inline as URLs and the fetch actions themselves were run live this session (2026-08-23 and, for the correction, re-checked 2026-08-24), not recalled from training data. **This does not mean the fetched content is current**: the Financial Juice page returned by the fetch is itself dated `06 Sep 2024` (see the corrected B1.2 section above) — a live fetch of a stale/static page is not evidence of a same-day event, and this note originally conflated the two. The historical-X-posts claim in B1.2 is carried over from the prior session's search and was **not** independently re-verified in this fix pass (X/Twitter search requires login and could not be re-checked via the tools available here).
