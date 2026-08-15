# ORB-MNQ-1 Stage-8 breadth RESULTS — vs the prop-portfolio book

**Campaign:** `orb_mnq_intraday_breakout` · **Pre-reg:** [`docs/briefs/pre-registration/2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md`](../../../docs/briefs/pre-registration/2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md) §3 Stage-8 (comparison target = prop-portfolio book, operator-chosen 2026-07-16)
**Harness:** [`run_stage8.py`](run_stage8.py). **Book of record:** Class-S candidate #1 = 2-leg {Striker-DJ30→MYM, Striker-NAS100→MNQ}, G8-intake CANDIDATE @1.00× **with standing regime-fragile caveat** ([`../class_s_candidate1_scoring_2026-07-15/G8_INTAKE.md`](../class_s_candidate1_scoring_2026-07-15/G8_INTAKE.md)). Precedes [`RESULTS_stage7.md`](RESULTS_stage7.md).

---

> **⚠ CORRECTED by the realized N_eff ([`RESULTS_stage8_neff.md`](RESULTS_stage8_neff.md), legs procured 2026-07-16).**
> The "instrument-concentration" claim below is a **structural pre-data hypothesis that the measured
> data overturned**: realized weekly corr(ORB, MNQ-Striker) = **+0.15** despite the same instrument,
> and dependence N_eff rises **1.99→2.95** (a near-independent bet). ORB is NOT instrument-concentrating.
> The concentration is real only on (a) the **regime** axis (common-mode chop-fragility, below — average
> correlation doesn't capture it) and (b) a **risk-mass** axis (ORB is high-variance). Read this section
> as the structural reasoning of record, superseded on the correlation axis by the realized file.

## Verdict — ORB-MNQ **concentrates** the book's instrument + regime exposure; it is **not a breadth-adding leg** for this book

*(Structural, pre-realized-data. The instrument-concentration limb is CORRECTED above; the regime limb stands.)*
A real, direction-agnostic intraday edge — but on the two axes that matter for *this* book it
adds concentration, not diversification. Not a breadth-based admit.

### (1) Exposure declaration (ADR 2026-07-13 companion)

| Coordinate | Value |
|---|---|
| Side | long 53% / short 47% — **direction-agnostic** (not long-beta; a genuine breadth positive) |
| Entry window | 09:30 ET cash open; OR 09:30–10:00; entries after 10:00 ET (median 10:00, mean 10:13) |
| In-market / trade | ~346 min (~5.8h), exit at RTH close (E1-flat) |
| In-market / yr | ~79,900 min = **81% of the RTH-session clock** / 15.2% of the 24h clock |
| Episodic? | **No** (≫5% of session clock) ⇒ realized correlation *is* relevant (data-gated, see (3)) |
| P&L-bearing | 1,846 entries / ~1,846 sessions (~99%); ~231 trades/yr |

### (2) Regime common-mode test — the load-bearing finding

The book's binding vulnerability (G8_INTAKE): **H1 2020–2023 FAILS both tiers (bust ~4.37%)**;
H2 2023–2026 passes (~1.70%). Does ORB-MNQ offset or share that H1 fragility?

| ORB-MNQ segment | n | meanR |
|---|---|---|
| book-H1 2020–2023 | 1027 | **+0.0590** (net positive over the window) |
| book-H2 2023–2026 | 906 | +0.0932 |
| **2020 alone (book's worst year)** | 258 | **−0.0285** (negative — does NOT offset) |
| 2021–2022 (H1 trend half) | 514 | +0.0826 |

**Reading:** ORB-MNQ is net-positive over the whole 2020–2023 window (so on average it does not
*deepen* the H1 problem, and adds return), **but its strength is entirely trend-regime** — dead in
2020 (−0.029) and the whole pre-2021 period (N2), strong in the 2021–2024 trend years. That is
**exactly the regime profile of the book itself** (trend-loving, chop-fragile): ORB-MNQ helps in
the trend years the book already survives (H2) and is weak in the chop (2020) where the book
busts. So it **shares the book's binding regime dependence rather than hedging it** — no
regime-breadth added. This is the standing "no regime-robust static counterbalance exists" finding
(5th-leg search closed NULL) reconfirmed: ORB-MNQ is another trend-regime leg, not the chop-hedge
this book wants.

### (3) Instrument concentration + realized N_eff (data-gated)

- **Instrument:** ORB-MNQ is **Nasdaq-100** — the *same instrument* as the book's Class-S MNQ leg
  (Striker-NAS100→MNQ) and the *same US-equity-index factor* as MYM (Dow). Admitting it makes the
  book **3 US-equity-index legs, 2 of them on MNQ/Nasdaq.** Heavy concentration.
- **Structural mitigant (unconfirmed):** ORB runs a *different clock* (09:30-ET cash-open intraday
  breakout, exit-at-close) from the Striker-NAS100 leg (Mon/Tue swing/pyramid) and is
  direction-agnostic — so instrument-level correlation should overstate strategy-level correlation
  (the standing NAS100/DJ30 belt finding). But this is a **structural expectation, not a measured
  fact.**
- **Realized cross-leg correlation / N_eff:** **NOT computable in this worktree** — the CFD 4-leg
  Pepperstone panel is absent (`breadth.baseline_panel_available=False`) and no MYM/MNQ Striker
  edition return CSVs exist locally (all gitignored). Computing `research_utils.breadth` N_eff delta
  is a **Stage-8-completion data-procurement item**, not fabricated. The concentration verdict above
  does not depend on it (it stands on the exposure declaration + regime split).

---

## Disposition

- **Stage-8 breadth:** ORB-MNQ **concentrates** the prop-portfolio book on both binding axes —
  instrument (2nd Nasdaq/MNQ leg) and regime (trend-loving/chop-fragile, aligned with the book's
  own H1 vulnerability). Direction-agnosticism is its one genuine breadth positive. **It is not a
  breadth-based admit to *this* book**; it would fit better in a book lacking Nasdaq exposure and
  not already trend-regime-fragile.
- **Realized N_eff** is owed at Stage-8 completion (needs the prop-book legs' aligned return series
  — a data-procurement item, operator-gated).
- **Campaign status:** ORB-MNQ-1 clears the confirm gates (Stage-2 cost-law, Stage-5/6 DSR+temporal
  +placebo, Stage-7 firm/slip realism on 2021+), but Stage-8 flags it as instrument+regime-
  concentrating for the current book. Net: a **real edge, admissible as a lifecycle CANDIDATE with
  a standing breadth/concentration caveat** (symmetric to how the Class-S book itself carries a
  regime-fragile caveat) — **not** a portfolio-diversifying leg. Lifecycle admission + rail/account/
  live-spend remain separately gated; the regime-dependence (2021+ carries it; 2026-partial the
  tripwire) is the dominant standing risk.

Reproduce:

```bash
PYTHONPATH=lab .venv-research/Scripts/python.exe lab/analysis/orb_mnq_2026-07/run_stage8.py
```
