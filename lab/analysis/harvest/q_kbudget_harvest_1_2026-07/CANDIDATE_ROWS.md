# Candidate rows — Q-KBUDGET-HARVEST-1 Phase 1 → Phase 2

**Status:** **Phase-2 RATIFIED 2026-07-16** — both rows **ACCEPT** (operator: "accept both").  
**Inventory:** [`docs/briefs/Q-KBUDGET-HARVEST-1-inventory-addendum.md`](../../../docs/briefs/Q-KBUDGET-HARVEST-1-inventory-addendum.md) (H1 / H2).  
**Ratification record:** [`PHASE2_RATIFICATION.md`](PHASE2_RATIFICATION.md).  
**Do not extend `floor_scan.py` until Phase 3** (next).  
**Screen arithmetic:** Phase 3 via `floor_scan` / `axis_screen` — not a blessing here.

---

## H-OD-1 — Overnight drift (inventory-risk / EU-open window) on equity-index futures

| Field | Declaration |
|---|---|
| **Axis short name** | `H-OD-1` overnight-drift inventory-risk (2:00–3:00 ET) |
| **Path 1a/1b** | **1a** — market makers absorb end-of-U.S.-day order imbalance, earn liquidity-premium overnight as Asia/EU participants arrive (Grossman–Miller inventory risk). Named losers: constrained overnight liquidity providers / end-of-day demand shocks (asymmetric: selloffs reverse more than rallies). |
| **Source + tier** | Boyarchenko, Larsen & Whelan, *The Overnight Drift*, FRBNY Staff Report No. 917 (Feb 2020; rev. Aug 2022), SSRN 3546173. **Tier 2** (reputable central-bank staff report / working paper with extractable per-contract futures stats). Liberty Street Economics companion posts 2021-05 and 2026-07. |
| **Instrument family → K_banked** | Primary published cohort: **ES (E-mini S&P 500 futures)**. Cross-contract signature (NQ, YM) affirmed in 2026-07 Liberty Street update — **confirmatory only, no separately published per-contract δ/σ**. Declaration ratified: **family = ES → K_banked=1** (SR917's sole fully-quantified cohort — Table I/IX are ES-specific; ES's micro sibling is MES, per `ops/instruments/ES.md`). **MNQ/NQ (or MYM) expression: `UNSCREENABLE:nq-native-delta-sigma-not-extracted`** — a different underlying index is a separate axis-expression needing its own cohort δ/σ (intake ADR requirement 2 no-transplant; D5 gamma-sign precedent), never an ES venue variant. Recovery = extract an NQ-native δ/σ (SR917 rev. 2022 cross-contract tables are the first place to look) — the H-TSMOM-1 stub→scrape pattern. *[Amended 2026-07-16 at Phase-2, operator-directed: struck the pre-ratification "prefer MYM/MNQ (K_banked=0)" and "MNQ re-expression is a venue variable after PASSes, not a second axis" framing — see PHASE2_RATIFICATION.md §Amendment; now consistent with the addendum §1 family-pin line.]* |
| **Design → K_intrinsic** | Mechanism-first confirm: (H1) long ES 02:00–03:00 ET unconditionally; optional (H2) long only after negative closing RSV ("buy-the-dip" BtD). **K_intrinsic = (1, 2)**. No lookback/holding grid. |
| **OOS era → N** | Declared panel: daily OD events over ~6.5y OOS ⇒ **N ≈ 1,000–1,500**. (Publication sample Jan 1998–Dec 2020 used only for δ/σ derivation.) |
| **δ/σ (cohort-cited)** | Table I: 02:00–03:00 mean **+1.5 bps/day**, **t = 7.1** (HAC). t-scaled δ/σ at N_pub≈5,500 ≈ **0.096**; conservative central plug used here: **δ/σ = 0.093** (t/√5796). Break-even at N=1000 ≈ 0.062. Informational power Φ(√1000·0.093−1.96) ≈ **0.84 ≥ 0.50**. |
| **Net-of-cost / decay caveats (required honesty)** | (1) Unconditional OD Sharpe **1.1 → −0.5** after bid–ask (Table IX) — net tradeability is the *campaign* question (same class of caveat as D5 Baltussen). BtD (RSV\<0) remains the more plausible confirm expression. (2) Liberty Street 2026-07: OD **faded toward zero since 2021** via RSV-dispersion compression — attenuation named; Path 1a still holds (mechanism named); do **not** claim Path 1b immunity. |
| **Dedup** | Distinct from D5 (last-30m ROD momentum / gamma-hedging) and from D3 (month-end). Same inventory-risk family as Q3 but first harvest row. |
| **Proposed screen posture** | Clause K: K_eff = 2–3 (ES bank 1 + intrinsic 1–2) → floor 0.85–0.98 ≤ Cap 1.0 → PASS-able. Clause N: power ≈ 0.84 → PASS-able on paper. **Ratification still required** before any floor_scan append. |

### Phase-2 decision

- **ACCEPT** (2026-07-16) → inventory addendum **H1**; Phase 3 extends screen.

---

## H-TSMOM-1 — Time-series momentum confirm on S&P 500 / ES futures

| Field | Declaration |
|---|---|
| **Axis short name** | `H-TSMOM-1` Moskowitz–Ooi–Pedersen 12m/1m TSMOM confirm (S&P 500 futures) |
| **Path 1a/1b** | **1b PASS** (scored at Phase 2 — see [`PHASE2_RATIFICATION.md`](PHASE2_RATIFICATION.md)). |
| **Source + tier** | Moskowitz, Ooi & Pedersen, *Time series momentum*, *JFE* 2012. **Tier 1.** Digitization note: [`H_TSMOM_1_fig2_scrape.md`](H_TSMOM_1_fig2_scrape.md). |
| **Instrument family → K_banked** | **ES (S&P 500 futures)** → K_banked=**1**. Paper equity universe has **no NQ**; S&P→NQ transplant forbidden. |
| **Design → K_intrinsic** | Mechanism-first confirm of the paper’s frozen 12-month lookback / 1-month hold sign rule (vol-scaled). **K_intrinsic = (1, 1)**. No lookback/holding grid. |
| **OOS era → N** | Monthly events. **Ratified: N = 192** (≈2010–2025 post-publication OOS). Alternate 6.5y N≈78 remains sensitivity-only (fails Clause N). |
| **δ/σ (cohort-cited)** | Fig. 2 S&P 500 bar digitized gross annualized Sharpe **0.58** → δ/σ_monthly = 0.58/√12 = **0.167**. Tolerance ±0.03 SR. Informational power at N=192 ≈ **0.64**; haircut SR=0.50 → power 0.52; SR=0.45 → 0.44 FAIL. |
| **Net-of-cost / other caveats** | Gross Sharpe only. Monthly event rate makes Clause N fragile vs daily axes. AQR published factors are class-pooled only — not used as δ. |
| **Prior stub status** | Was `UNSCREENABLE:per-instrument-delta-sigma-not-extracted`; cheap recovery (Fig. 2 scrape) **cleared** 2026-07-16. |
| **Proposed screen posture** | Clause K: K_eff = 2 (ES bank 1 + intrinsic 1) → floor 0.85 ≤ Cap → PASS-able. Clause N: PASS-able at N=192 central; FAIL at N=78. **Ratification picks N + Path-1b bars.** |

### Phase-2 decision

- **ACCEPT** (2026-07-16; N=192 + Path-1b scored PASS) → inventory addendum **H2**; Phase 3 screen.

---

## Coverage discharge (pre-reg §E)

All six query families have dated coverage logs in this directory **and** E.1 seeds are logged. Union of logged sources yields **two** four-field-complete *new* candidates (`H-OD-1`, `H-TSMOM-1`) after the Fig. 2 scrape. §B FALSIFIED (empty harvest) does **not** fire. §B RESOLVED awaits **Phase-3** extended scan (Phase-2 ratification done).
