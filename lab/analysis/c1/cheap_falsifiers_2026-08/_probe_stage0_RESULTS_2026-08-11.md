# Q-MCLTAS-1 — Stage 0a + 0b RESULTS · `STOP-UNREACHABLE` (Wall B fires)

**Date:** 2026-08-11 · **$0.00 · K=0 · no manifest · no data pull · no market data read**
**Authorized by:** operator ("run 0a and 0b") against the frozen
[`Q-MCLTAS-1` scoping brief](../../../docs/briefs/Q-MCLTAS-1-tas-settlement-delta-extraction-probe-scoping.md) §7.
**Gate:** brief §6, pre-registered before either stage ran.

**Headline:** Wall A returns `AMBIGUOUS-HOLD` on one unverified costed route; **Wall B returns
`STOP-UNREACHABLE` on measured, committed σ**. Per §4, *either* limb failing falsifies H-MCLTAS-1.
**Wall B is dispositive because it is independent of how the sign is obtained** — so Wall A's
open item does not need resolving to close this.

---

## Stage 0a — sign-source enumeration ($0, K=0, no data)

**Test (frozen in §7):** does any candidate source satisfy *free-or-entitled* ∧ *signed (net, not
gross)* ∧ *exogenous to the window's own price* ∧ *aligned to the daily 14:28–14:30 ET window*?

| # | Candidate source | Free/entitled | Signed | Price-exogenous | Window-aligned | Verdict |
|---|---|---|---|---|---|---|
| 1 | **CME published TAS volume** (daily bulletin) | ✅ free | ❌ **gross** | ✅ | ✅ | **FAIL (signed)** |
| 2 | **TAS instrument order flow in `GLBX.MDP3`** (aggressor side / quote imbalance on the TAS book) | ⚠️ entitled-**costed** | ✅ | ✅ | ✅ | **HOLD — the only survivor; unverified** |
| 3 | **Daily open-interest change** (CME free) | ✅ free | ❌ | ✅ | ❌ daily | **FAIL (signed + WHEN)** |
| 4 | **CFTC COT / TFF net positioning** | ✅ free | ✅ | ✅ | ❌ weekly, lagged | **FAIL (WHEN)** |
| 5 | **Published settlement-window imbalance print** | — | — | — | — | **FAIL — does not exist** |
| 6 | **Index-roll calendars (GSCI/BCOM)** | ✅ free | ✅ ex ante | ✅ | ❌ ~5 d/mo | **BARRED** (spread-shaped) |
| 7 | **The window's own price action** | ✅ free | ✅ | ❌ | ✅ | **FORBIDDEN** (§5 / BE1) |

**Row-by-row grounds, with confidence labelled honestly:**

- **1 — definitional.** Exchange volume counts *contracts traded*; every trade has a buyer and a
  seller, so a published volume figure carries no net direction. This is the load-bearing check and
  it fails on the construction of the datum, not on its availability. **The closure's recorded route
  — "free CME TAS volumes, non-circular" — is therefore confirmed non-circular for Req 1a(iv)
  decay observables, and confirmed insufficient as a *sign* source.** Both halves of that reading hold.
- **2 — ⚠️ UNVERIFIED, and deliberately not verified.** Whether `GLBX.MDP3` carries TAS instruments
  as separately-symbolized books, and at what cost, is **not established anywhere in this repo** and
  was not checked (checking is free but pointless — see the disposition note below). Also constrained
  by the standing entitlement fact: the databento entitlement is **RECENT-DATA; full-span tick BILLS**
  ([`project_databento_research_stack`](../../../docs/notes/notice/N-2026-08-11-daily-auction-settlement-MCL.md)-adjacent
  standing memory), so a cohort-length TAS pull is a costed operator decision regardless.
- **3 — definitional.** OI change is directionally agnostic: every long is matched by a short, so
  ΔOI reports contracts opened/closed, never a net direction. Independently fails WHEN (daily).
- **4 — structural.** COT is a weekly *positioning level* published with a lag; it cannot supply the
  sign of *today's* two-minute window. Harvest §2.3 rank-4 already flags COT power-marginal at weekly
  frequency, independently.
- **5 — the structural asymmetry, and it is the sharpest row.** Equity closing auctions publish a
  pre-close imbalance indication — that print is precisely the datum `F1`/MOC proposed to trade. **CME
  futures settlement windows publish no analogous pre-print.** So this cell is not gated like F1 was;
  it is *empty*. F1 had a real datum behind a procurement wall; this has no datum.
- **6 — barred, not merely failing.** Roll direction is genuinely signed ex ante, which is exactly why
  it is tempting. ENV-1 closure §6.4.1 rules any spread-framed envelope a **new campaign**, and `SFX-1`
  (settlement + GSCI-roll) is already `DEAD`.
- **7 — forbidden.** Brief §5, first entry: BE1's *"constraint carries neither sign nor level;
  direction laundered from price."*

**Stage 0a verdict: `AMBIGUOUS-HOLD`.** The intersection over *free* sources is **EMPTY**. One
*entitled-but-costed* route (row 2) survives on paper, which under §6 routes to `AMBIGUOUS-HOLD`
rather than `STOP-CIRCULAR` — but it is unverified, and Stage 0b makes it moot.

---

## Stage 0b — σ-pin ($0, K=0, no data pull)

**⚠ A brief-grounding defect, found and repaired here.** §7 scoped Stage 0b against *"the committed
2023 MCL cache"*. **That cache is not on disk** — `lab/analysis/c1/tradeify_fade_stage0_2026-07-30/`
holds `RESULTS*` markdown only; the heavy artifacts are gitignored and absent from this checkout
(consistent with the CATALOG's standing heavy-column WARNs). The brief asserted the cache's presence
without verifying it — Known Trap #13 (*brief precision exceeds brief grounding*), my own, one turn
after authoring.

**The substitute is strictly better than the plan.** `RESULTS_sigma_native.md` carries a **measured
σ surface** (`stage2_sigma.windowed_sigma`, wed_thu ex-FOMC cohort) — a committed *result*, so the
σ-pin needs no re-derivation and no data at all.

Required δ (Wall B) = **$11.60/contract/event**. Settlement window = **2 min**. Source = the measured
**15-minute** σ column, √-time scaled.

| σ reading (increasingly generous to the candidate) | σ₂ₘᵢₙ | required δ/σ | vs D5 optimistic (0.194) | vs D5 conservative (0.113) |
|---|---:|---:|---:|---:|
| (a) nearest-in-time — 14:00 cell, adjacent to the window | $8.57 | 1.354 | **7.0×** | 12.0× |
| (b) most generous cell anywhere in the surface — 10:30 | $14.31 | 0.811 | **4.2×** | 7.2× |
| (c) (b) + published-panel inflation (1.30×) | $18.64 | 0.622 | **3.2×** | 5.5× |

Comparator: **D5's δ/σ = 0.113 conservative (the reading actually used) / 0.194 optimistic (explicitly
rejected by `strategy_harvest.md` §4 as too generous)** — the estate's only *committed* causal-public
δ/σ. Reading (c) stacks every available generosity (busiest cell in the day, the larger published
panel, and the δ/σ the estate itself rejected): **the floor is 3.2×, and it never closes.**

**Stage 0b verdict: `STOP-UNREACHABLE`.**

### The correction this stage produced — and it went the wrong way

The scoping brief predicted the cohort-bound gap would **narrow to ~2.4×**. It does not: measured, the
floor is **3.2×** and the defensible reading is **7.0×**. The 2.4× rested on a GC fix-window σ **I
invented rather than measured** — `lesson_metric_cohort_provenance_binding`, **second firing inside
this one probe**, first against the falsifier's bp-space comparison and now against my own repair of it.
The lesson's own instruction ("bind every borrowed metric to its cohort … pre-check the anchor's own
percentile") was followed on the *required* side and skipped on the *comparator* side.

**Direction of the error matters:** the unmeasured guess was optimistic about the candidate. Had 0b been
skipped as "probably confirmatory", the brief's 2.4× would have stood as the record — a number that
makes the probe look ~35% closer to fundable than it is.

### σ caveats, stated

√-time scaling assumes iid increments. Intraday vol is U-shaped, and the settlement window is plausibly
*elevated* relative to the 14:00–14:15 cell — which is why reading (b) takes the busiest cell in the
entire day as the generous bound rather than scaling the adjacent one up by an invented factor. The
underlying surface also carries a known unresolved defect: it **does not reproduce** the published
pinned cell (−33.1%, panel discrepancy, "reported, not adjudicated"). Reading (c) absorbs that
discrepancy in the candidate's favour.

---

## Composite verdict against the frozen §6 gate

| Wall | Result | Fires? |
|---|---|---|
| A — circularity | `AMBIGUOUS-HOLD` (one unverified, costed route survives) | no |
| **B — magnitude** | **`STOP-UNREACHABLE`** — 3.2× at the friendliest constructible reading | **✓** |

§4: *"Reject H if **either** limb fails."* **H-MCLTAS-1 FALSIFIED on Wall B.**

**Why Wall A is not resolved, and does not need to be:** Wall B is independent of *how* a sign is
obtained. Verifying whether `GLBX.MDP3` carries TAS books would cost nothing but could only convert
Wall A from `AMBIGUOUS-HOLD` to `STOP-CIRCULAR` — a strictly *more* negative result on a question
already dead on the other wall. Leaving it open is the honest record; closing it would be work that
cannot change the disposition.

## What this does NOT license

Reading Wall B as a kill on **MCL the instrument** — it is not; per the MCL ledger's 2026-08-10c
precedent, what dies is a design region, not the symbol. Reading it as a kill on settlement-window
mechanisms **generally** — the arithmetic is MCL's tick geometry against MCL's own σ. Treating the
`AMBIGUOUS-HOLD` on Wall A as a live route. Any re-run of this arithmetic as a re-proposal.

## Reproduce

```bash
python lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_mcl_tas_probe_2026-08-11.py   # Wall B, bp space
python lab/analysis/c1/cheap_falsifiers_2026-08/_probe_stage0b_sigma_pin_2026-08-11.py         # Wall B, delta/sigma space
# Expected: 4.63x / 3.01x (bp) and 7.0x / 4.2x / 3.2x (delta/sigma)
```
