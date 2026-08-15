**Theme:** harvest
**Status:** ACTIVE — harvest mechanism deep search fan-out (2026-07-23)
# Harvest mechanism deep search — 2026-07-23

**Status:** COMPLETE — **0 SCREENABLE seeds** (accept-idle reaffirmed; no intake-row opened)  
**Scope:** Aimed Tier-A / conditional Tier-B literature search for **new mechanism evidence** that can clear harvest Req 1–5 at sniff, after Q-INVENTORY-1 `FALSIFIED` (band empty) and radar burst-1.  
**Doctrine:** [`docs/methodology/strategy_harvest.md`](../../../docs/methodology/strategy_harvest.md) §1–§2  
**Dedup:** `rejected_candidates.md`, closed discovery manifests, Q-INVENTORY PHASE0 kill list, radar `SOURCES_LOG`, D5/H-OD/H-TSMOM closures.  
**K / pulls:** zero. No `register_search open`, no Databento spend.

---

## Verdict (one paragraph)

A fresh deep search does **not** produce a seed that is ready to admit into the intake screen. The empty band is structural, not a coverage gap: under Default-#1 OOS (`N≈86` monthly), Tier-A monthly mechanisms need predictive `δ/σ ≳ 0.21` (≈ annualized SR ≳ 0.73 on the *confirm rule*) to clear Clause N — above typical published per-instrument TSMOM/carry SRs (0.5–0.6). The high-N alternatives either die on cost (daily microstructure), venue (VIX/SR3), K-bank (GC/MGC), informed-flow (surprise-conditioned EIA), or remain **UNSCREENABLE** until a δ is extracted. Best next moves stay the already-priced probe forks, with updated decay/cost caution on ZN auctions.

---

## Hard constraints used (re-read, not re-derived)

| Gate | Binding number |
|---|---|
| Clause K | `K_eff ≤ 3` (floors 0.65/0.85/0.98) |
| Clause N | `power = Φ(√N·\|δ\|/σ − 1.96) ≥ 0.50` |
| Default #1 OOS | statistical start **2019-05-06** → monthly **N≈86**; weekly **N≈374**; ZN-auction ≈36/yr → **N≈259** |
| Req 5 | `δ (bp/event) ≥ 4 × RT_frac` panel-era |
| Banks (snapshot) | GC/MGC **3177** · ES **2** · MNQ **1** · others **0** |
| Tradeify instrument reality | micros MNQ/MYM/MES/M2K/MGC/MCL/M6E/M6A; **no** VIX complex, **no** SR3/SOFR strip on the fee-table set |

Monthly break-even at N=86: `δ/σ ≥ 1.96/√86 ≈ 0.211`.  
Weekly break-even at N=374: `δ/σ ≥ 0.101`.  
ZN-auction break-even at N=259: `δ/σ ≥ 0.122`.

---

## Dead / do-not-restage (confirmed again)

| Class | Why |
|---|---|
| Month-end / pension flow | D3/D7 FAIL(N); Q-HARV-1 §R DECLINED |
| Monthly 12m/1m TSMOM @ Default #1 | H-TSMOM-1 / H-TSMOM-6J Clause-N FAIL |
| Baltussen intraday mom / dealer-gamma | D5 + D5-RECOST; Tier-C graveyard |
| Overnight drift | H-OD-1 cost-law |
| GC/MGC any design | FAIL-K bank 3177 |
| FX fixing-window drift | Q-INVENTORY R3 Req-5 FAIL (even published *net* SR 0.99) |
| Macro pre-release drift | informed-flow / leakage shutoff |
| NG-EIA / rates-EV-ZF / OPENPRESS / MYM-3FPS / ORB→ZB | Phase-0 FALSIFIED 2026-07-21 |

---

## Candidates examined this pass

### A. ZN post-auction dealer-hedge unwind — **ALREADY CLOSED `SCREEN-FAIL` (H-ZNAUC-1, 2026-07-20)**

- **Correction (this session):** F-A was **not** still open. Operator-authorized own-cohort δ-extraction already ran — Smales PDF never needed. Canonical: [`docs/briefs/closures/H-ZNAUC-1-closure-screen-fail.md`](../../../docs/briefs/closures/H-ZNAUC-1-closure-screen-fail.md) · [`lab/archive/q_znauc_1_2026-07/`](../../q_znauc_1_2026-07/).
- **Measured (primary 10Y-family, 0→15m):** N=134 · **δ = 1.01 bp/event** · σ=7.29 · δ/σ=0.139 · t=1.61. Direction confirms Smales. **Req-5 FAIL** vs 6–10 bp hurdle (**6–10× under**). Power also marginal at realized N. K=0; ZN bank stays 0; Databento **$0.00**.
- **Disposition:** **do not re-scrape / re-run.** Re-proposal bar = new mechanism evidence, not a Smales table re-read. Sibling forks: F-C carry timing also closed `SCREEN-FAIL` ([`H-FCCARRY-1`](../../../docs/briefs/closures/H-FCCARRY-1-closure-screen-fail.md)); F-B CL EIA remains lowest priority.

### B. WTI / CL own-curve carry (Bouchouev) — **new literature find; Clause-N blocked**

- **Source:** Bouchouev *Oil Risk Premia…* / *Virtual Barrels* — single-contract WTI carry (sign of m3−m12 curve), IR **≈0.50**, ~17% ann since 1993. This is **instrument-native** and is the confirm rule itself (own-carry sign), unlike Koijen Table-1 *unconditional* moments or class timing SR transplants refused in radar burst-1.
- **Sniff:** Path 1a OK (convenience yield / storage) · CL/MCL bank 0 · Req-2 **would clear** on published IR if the axis is pinned as own-curve sign · **Clause N FAIL** at Default #1: `δ/σ = 0.50/√12 ≈ 0.144` → power@N86 ≈ **0.26** (same death as H-TSMOM-6J).
- **Disposition:** **not SCREENABLE** under standing Default #1. Distinct from forbidden class-SR transplant; still dies on N. Re-open only with N-extending evidence or an operator-stated §8 override (not recommended — same fork that closed H-TSMOM-1).

### C. Koijen carry-timing (6J/6E/CL) — **ALREADY CLOSED `SCREEN-FAIL` (H-FCCARRY-1, 2026-07-20)**

- F-C was funded and run: combined carry-timing Sharpe **≈0.09**, δ/σ **0.027** → Req-4 FAIL (effect absent). Canonical: [`H-FCCARRY-1-closure-screen-fail.md`](../../../docs/briefs/closures/H-FCCARRY-1-closure-screen-fail.md). Do not re-run.

### D. Basis-momentum (Boons & Prado *JF* 2019) — **EXCLUDE this pass**

- Strong abstract claim; evidence is primarily **cross-sectional / portfolio** and individual-commodity pricing tests, not a frozen K≤3 single-leg δ on CL/MCL. Monthly → same N wall even if a WTI cell exists. Would need a dedicated table scrape + single-leg pin before staging.

### E. Hedging-pressure / COT extremes — **EXCLUDE this pass**

- Basu–Miffre already EXCLUDE (cross-sectional L/S). Recent individual-commodity OOS predictability literature is weak/mixed. Weekly N helps *if* a CL-native δ existed; none staged without inventing numbers.

### F. VIX futures roll / variance premium — **VENUE-WALL**

- Large published contango/roll effects; **not** on automation-friendly prop instrument lists (Q-INVENTORY already).

### G. SOFR / STIR term-premium roll (SSRN SR≈0.94) — **VENUE-WALL (likely)**

- Attractive Tier-A shape (rates term premium); Tradeify fee table does not list SR3. Drop unless firm coverage verified.

### H. CL EIA unconditional event expression — **still F-B probe**

- Literature remains **surprise-conditioned**; unconditional form is the honest fork, not a published ready δ. Adjacent NG-EIA already FALSIFIED.

---

## Ranked next actions (operator GO)

| Rank | Action | Cost | Note |
|---|---|---|---|
| **Done** | F-A / H-ZNAUC-1 | $0 (2026-07-20) | **CLOSED cost-wall** — δ 1.01 bp vs 6–10 bp; do not re-run |
| **Done** | F-C / H-FCCARRY-1 | already | **CLOSED effect-absence** — Sharpe ≈0.09; do not re-run |
| **1 (default)** | Stay **accept-idle** through 11-08 | $0 | Doctrine-consistent |
| **2 (optional)** | Bouchouev-style CL own-curve carry — only with an N plan that survives Default #1 | probe + possible 1×K | Else dies Clause-N like H-TSMOM |
| **3 (low)** | F-B CL EIA unconditional | ~$0 | Informed-flow trap; lowest prior |

**Not recommended:** Smales PDF scrape (moot); unbounded Tier-A lit sweep; restaging monthly TSMOM/carry @ N≈86; Tier-C event-drift.

---

## Own falsifiers untouched

- Harvest-intake doctrine Stage-6 falsifier: still **0-of-2** (no new Stage-2).  
- Radar Stage-2 cost-law falsifier: still **untriggered** (no Tier-A seed reached Stage-2).

---

## Artifacts

| File | Role |
|---|---|
| This `RESULTS.md` | Verdict + scorecards |
| [`SOURCES.md`](SOURCES.md) | Papers / channels touched this pass |
