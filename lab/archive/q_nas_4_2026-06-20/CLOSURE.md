# Q-NAS-4 — Inquire closure: NAS100 pyramid-monster sign-gate (full panel)

**Date:** 2026-06-20 · **Loop:** INQHIORI pre-Q gate (D-S-A) → Q → H → Inquire (I/O/R) → closure.
**Verdict:** **PARTIAL** — strict gate **FALSIFIED**; a weak graded directional tendency survives but clears **no** honest correction at 0.05.
**Routing:** **CLOSED** (characterization-only; nothing to forward, no action — belt forbids every operable reading).
**Belt:** Striker NAS100 v1 LOCKED. Verdict carries **zero** sizing/parameter consequence by construction.

---

## Pre-Q gate (D-S-A, data domain)

```
D: deleted the 2y-subset leg detail, bar microstructure, opportunity-surface funnel, and all
   measurement caveats not bearing on the sign-gate. D-test = "outside the temporal/instrument
   scope of the question class" (permitted) — the 2y subset is a temporal subset of the 4y panel.
S: collapsed to one per-quarter table {quarter, index_return_sign, n_trades, monster_present}
   — lowest-dimension form preserving the 6-vs-2 anomaly.
A: precomputed quarter aggregates once so each Q-variant (sign vs magnitude, alt monster defs,
   trade-frequency confound, real-bar-only) costs seconds.
```

## Q / H

- **Q:** On the full 4y/196-leg panel, does the Max-Hold-pyramid_add "monster" mechanism remain absent in **every** negative-index quarter and present in **every** positive one, or does the clean 6-vs-2 split (from the n=2-down-quarter 2y subset) break?
- **H (falsifiable):** The strict sign-gate generalizes — monsters present in all positive quarters, absent in all negative quarters — on ≥6 down quarters.

## Data

- **Trades:** LOCK-anchor panel `Striker_NAS100_v1_PEPPERSTONE_NAS100_2026-05-24_11605.csv`, n=196, reconciles to LOCK.md **exactly** (net $369,698.41, PF 3.717, WR 55.61%).
- **Index sign:** real Pepperstone bars (assembled 3 pages, 2024-01→2026-06, 10 quarters) + panel-price proxy for 2022Q1–2023Q4 (8 quarters). Proxy **validated 10/10 on sign** vs real bars on the overlap (magnitude error up to ~7pp → magnitudes not used as load-bearing).
- **Monster (primary):** leg with `exit_signal=='Max Hold'` AND `leg_type=='pyramid_add'`.

## Result (18 quarters, 12 positive / 6 negative)

| | monster present | monster absent |
|---|---|---|
| **positive quarter** | 9 | **3** ← 2022Q4 +1.1%, 2023Q1 +11.0%, **2024Q2 +7.2% (real bar)** |
| **negative quarter** | **1** ← 2022Q3 −1.5% (proxy) | 5 |

Concordance 14/18 · Fisher one-sided p=0.0317 · permutation p≈0.031 (re-derived end-to-end, zero mismatch).

## Verdict — PARTIAL

**FALSIFIED (strict gate):**
- "Monster in **every** positive quarter" is **false on real data alone** — 2024Q2 (+7.23%, real bar, 8 trades, the single highest-q_net positive at $68.3k) has **zero** monsters. Independent of the proxy and of 2022Q3.
- No defensible reframe rescues it: flat-bin sweep clean-gate count **0/5** (the strong-trend false-absences 2023Q1 +11%, 2024Q2 +7.2% survive every band); magnitude reframe falsified outright (Spearman |ret| 0.086, p=0.73).
- The motivating clean 6-vs-2 split was an **artifact of the n=2-down-quarter 2y subset**; it does not generalize.

**SURVIVES (graded tendency) — SUGGESTIVE, NOT ROBUST:**
- A noisy **directional** (not magnitude) sign-association: positive quarters tend to carry a monster, negative quarters tend not to (concordance 14/18, raw p≈0.032; Spearman signed-ret 0.625, |ret| 0.086).
- But it clears **no single honest correction** at 0.05:
  - **trade-frequency confound is load-bearing** — monster-present quarters avg 12.1 trades vs 9.4 absent; n_trades-stratified permutation **p≈0.07** (Spearman(n_trades, monster)=0.41).
  - drop-influential-positive jackknife **p up to ~0.06** (drop-1 range 0.009–0.060, never robustly <0.05).
  - Bonferroni over the 3-gate family **p≈0.095**.
  - **half-split:** signal lives in the 2024-2026 half (p≈0.067, the window that *motivated* Q-NAS-4) and is **absent** in the newly-added 2022-2023 half (p=0.50) → the 4y "test" is largely in-sample re-confirmation, not OOS validation.
- Negative side rests on n=6 with effectively **one** neg-present cell (2022Q3, proxy, −1.47% within sign-error).

## Routing — CLOSED

Nothing to forward, no action. The belt is **characterization-only**: every operable reading (base-entry filter / regime overlay / exit-timing rule / relock) is **forbidden** by the pyramid-is-the-strategy belt, and the **causal** "edge gated by trend persistence" reading is already a **closed tautology** (Identify phase). The finding adds nothing operable: a noisy, in-sample-concentrated, n_trades-confounded descriptive sign-tendency on a LOCKED strategy.

**Reopen criteria:** exogenous regime/trend data (not re-derived OHLC or panel-price proxy) **plus** a mechanism that does not collapse to the closed tautology — the same bar the catalog directional families failed (cf. US500 Q-SPX-F09 directional-axis closure). Real 2022-2023 Pepperstone bars would replace the only proxy-dependent cell (2022Q3) but cannot rescue the strict gate (carried by the real-bar 2024Q2) and would not change the CLOSED routing.

## Artifacts
`lab/analysis/q_nas_4_2026-06-20/`: `inquire_qnas4.py`, `probe_rescue.py`, `probe_confounds.py`, `qnas4_quarter_table.csv`, `qnas4_results.json`, this `CLOSURE.md`.
Source Notice: `docs/notes/notice/N-2026-06-20-nas100-identify-corpus-routing.md` §4 (Q-NAS-4 opened).
