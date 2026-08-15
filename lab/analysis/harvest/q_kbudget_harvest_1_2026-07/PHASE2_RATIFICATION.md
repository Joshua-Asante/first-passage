# Phase-2 ratification — Q-KBUDGET-HARVEST-1

**Date:** 2026-07-16  
**Operator:** Joshua — directive "accept both" (this session)  
**Parent:** [`docs/briefs/Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md`](../../../docs/briefs/Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md) §7 Phase 2  
**Inventory addendum:** [`docs/briefs/Q-KBUDGET-HARVEST-1-inventory-addendum.md`](../../../docs/briefs/Q-KBUDGET-HARVEST-1-inventory-addendum.md)  
**Does not fire §6 RESOLVED** — Phase 3 (extend `floor_scan.py` + run) remains.

---

## Verdicts

| Candidate | Operator act | N declared | Path 1 | Notes |
|---|---|---|---|---|
| **H-OD-1** | **ACCEPT** | 1000 (daily OD events, ~6.5y OOS) | **1a** (cleared Phase 1) | Net-cost + 2021+ fade caveats ride as campaign honesty, not ratification kills |
| **H-TSMOM-1** | **ACCEPT** | **192** (monthly; ≈2010–2025 post-publication OOS) | **1b** scored below | Family **ES only**; no NQ transplant |

Zero rejects. Zero parks.

---

## H-TSMOM-1 — Path 1b four-bar score (owed at Phase 2)

| Bar | Criterion | Score | Evidence |
|---|---|---|---|
| **(i)** | ≥3 decades covered sample | **PASS** | Moskowitz 2012 futures panel 1985–2009 (~25y) alone is short of 3 decades; the TSMOM / trend-following **class** is documented across ≥3 decades via Hurst/AQR *A Century of Evidence on Trend-Following* (*JPM* 2017) + the multi-decade Moskowitz panel. Decades bar is class-level, not Fig.-2-bar-only. |
| **(ii)** | ≥3 independent non-overlapping cohorts | **PASS** | Moskowitz Fig. 2 alone: ≥3 distinct equity-index futures markets (e.g. S&P 500, DAX, TOPIX) with positive gross TSMOM Sharpe; paper further spans equity / FX / FI / commodity classes. No cross-instrument δ transplant — Clause-N δ remains S&P/ES-only. |
| **(iii)** | ≥1 replication published ≥10yr after original discovery | **PASS** (pin recorded) | **Discovery pin:** momentum / trend class at Jegadeesh–Titman 1993 (cross-sectional) + earlier CTA trend literature; Moskowitz 2012 is a peer-reviewed futures TSMOM formalization ≥10yr after JT1993; Hurst/AQR 2017 is a further published class replication. **Caveat:** if discovery were pinned strictly to Moskowitz’s 2012 coining of “time series momentum,” a peer-reviewed ≥2022 replication was not located this session — operator ACCEPT uses the class-discovery pin above. |
| **(iv)** | No known structural sign-reversal condition | **PASS** (named) | Moskowitz’s own long-horizon **partial reversal** (beyond ~12m) is the paper’s under-/over-reaction prediction — it does **not** reverse the sign of the frozen 12m/1m confirm. Named attenuation risks (gross-of-cost; post-sample fade debates) ride as campaign honesty, same class as D5 / H-OD-1. |

**Path 1b overall:** **PASS** under the class-discovery pin in (iii).

---

## What this unblocks

- Inventory addendum rows H1 / H2 (do **not** rewrite D1–D7).
- **Phase 3** — append ratified rows to `floor_scan.py` (or `axis_screen` + manifest); regenerate RESULTS; fire parent §6.

## What this does **not** do

- No pulls. No K. No `register_search open`.
- Does not bless either axis (screen PASS, when Phase 3 runs, still only licenses campaign scoping).
- Does not block D5 execution.

---

## Amendment — H-OD-1 MNQ expression posture (2026-07-16, same day, operator-directed)

AUTH: operator said "apply this correction — strike the 'venue variable' framing, mark MNQ UNSCREENABLE pending its own δ/σ — as part of Phase-2 ratification"

**What was wrong:** H-OD-1's Phase-1 family field in [`CANDIDATE_ROWS.md`](CANDIDATE_ROWS.md) carried two claims contradicting the intake ADR's requirement 2 (cohort-cited **per-instrument** δ/σ; cross-instrument transplant inadmissible): a "prefer expression family MYM/MNQ (K_banked=0)" preference, and "MNQ re-expression is a venue variable after PASSes, not a second axis." MNQ tracks the Nasdaq-100 — a different underlying index from ES (whose micro sibling is MES, per [`ops/instruments/ES.md`](../../../ops/instruments/ES.md)) — and SR917 fully quantifies **ES only** (Table I: +1.5bp/day, t=7.1; Table IX net-of-cost); the 2026-07 Liberty Street update names the NQ/YM cross-contract signature confirmatorily, with no per-contract δ/σ. Verified against both sources 2026-07-16. The unburned-K attraction of MNQ/MYM (K_banked=0) is exactly the lure requirement 2 exists to resist: the δ must travel with the instrument, not the K-bank.

**Corrected posture** (now consistent with the inventory addendum §1 family-pin line, which was already right): H1's ratified family is **ES → K_banked=1, unchanged**. Any MNQ/NQ (or MYM) expression is `UNSCREENABLE:nq-native-delta-sigma-not-extracted` — a separate axis-expression requiring its own cohort-cited δ/σ before screening (recovery = the H-TSMOM-1 stub→scrape pattern; SR917 rev. 2022 cross-contract tables are the first place to look).

**Scope:** this amendment does not alter either ACCEPT verdict, any frozen pre-reg section (§B–§E untouched), the parent screen, or the addendum. Files touched: `CANDIDATE_ROWS.md` (H-OD-1 family field, amendment marker inline), `candidates.json` (H1 caveat appended), this record.
