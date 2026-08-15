# PROVENANCE — HARV-2026-001 literature pins (non-tuning)

**Purpose:** Phase-1 provenance only. Pins sample periods / headline stats from
public sources for the harvest-source record in
[`docs/ltm/briefs/Q-HARV-0-month-end-rebalance-ES.md`](lab/archive/../../docs/ltm/briefs/Q-HARV-0-month-end-rebalance-ES.md) §1.

**Hard constraint:** These pins MUST NOT revise brief §4 windows, thresholds,
or gates. Operationalization (T-3→T-1, T-4 cutoff, 100bp, C/G, verdict partition)
is frozen at registration.

**Status:** Drafted 2026-07-11 from public secondary sources / abstracts. Exact
table-level t-stats that are not confidently verified are marked
`pin pending verification` — do not invent.

---

## Parker, Schoar & Sun (JF 2023) — primary mechanism

| Field | Pin |
|---|---|
| Citation | Parker, J.A., Schoar, A., Sun, Y. (2023). "Retail Financial Innovation and Stock Market Dynamics: The Case of Target Date Funds." *Journal of Finance* 78(5), 2673–2723. DOI: [10.1111/jofi.13258](https://doi.org/10.1111/jofi.13258). NBER WP 28028. |
| Sample period | **2008Q3–2018Q4** (main TDF holdings sample; NBER WP text) |
| Mechanism (qualitative) | TDFs rebalance stock↔bond toward glide-path targets after relative returns — **macrocontrarian** flows (sell equity after equity outperforms) |
| Headline timing (rebalancing lag) | Roughly **~45%** of predicted rebalancing in the same month as the return differential, **~25%** next month, **~10%** at two-month lag (secondary summaries of JF/NBER text — **pin pending verification** against published Table) |
| Price / flow implication | Stocks disproportionately held by TDFs see reduced returns when stock-market returns are relatively high (abstract-level; magnitude **pin pending verification**) |
| Relevance to HARV-0 | Supplies the *conditional fade-the-intra-month-winner* mechanism registered at t=0. Does **not** authorize changing §4's 100bp / T-4 / T-3→T-1 operationalization. |

## Etula, Rinne, Suominen & Vaittinen (RFS 2020) — month-end liquidity / payment cycle

| Field | Pin |
|---|---|
| Citation | Etula, E., Rinne, K., Suominen, M., Vaittinen, L. (2020). "Dash for Cash: Monthly Market Impact of Institutional Liquidity Needs." *Review of Financial Studies* 33(1), 75–111. DOI: [10.1093/rfs/hhz054](https://doi.org/10.1093/rfs/hhz054). |
| Sample period (ANcerno / institutional) | Commonly cited as **1999–2013** (**pin pending verification** against published paper's exact sample-start footnote) |
| Headline pattern | Institutional net selling pressure **T-8→T-4** (esp. T-5→T-4) predicts higher market returns **T-3→T-1**; then reversal dynamics around the turn (abstract / DOI page summaries) |
| Economic magnitude (illustrative) | ~**0.32–0.42** percentage-point increase in T-3→T-1 market return per 1-SD increase in net selling (DOI-page summary — **pin pending verification** against Table 5) |
| Cost illustration | ANcerno institutions' month-end liquidity-related trading cost illustration on the order of tens of billions USD over sample (secondary — **pin pending verification**) |
| Relevance to HARV-0 | Motivates the **T-3→T-1** window as the pressure / reversal window in the month-end family. Context + timing convention only — not a license to widen/narrow §4. |

## Lakonishok & Smidt (RFS 1988) — unconditional TOM (context only)

| Field | Pin |
|---|---|
| Citation | Lakonishok, J., Smidt, S. (1988). "Are Seasonal Anomalies Real? A Ninety-Year Perspective." *Review of Financial Studies* 1(4), 403–425. DOI: [10.1093/rfs/1.4.403](https://doi.org/10.1093/rfs/1.4.403). |
| Sample | **DJIA, 1897–1986** (~90 years) |
| TOM window (their definition) | Last trading day of month through first **three** trading days of next month (**[−1, +3]**) |
| Headline stats | Cumulative TOM return ≈ **0.473%** vs average monthly rise ≈ **0.349%** ⇒ remainder-of-month average return negative (widely cited; **pin pending verification** against published Table) |
| Relevance to HARV-0 | **Context only** — unconditional calendar drift. Explicitly **not** the gated H1. Per §5: promoting unconditional TOM to rescue a failed H1 is forbidden (forks as its own K). |

## Ariel (1987) — related context (not a §3 primary pin)

| Field | Pin |
|---|---|
| Note | Brief §1 harvest-source lists Ariel (1987) alongside Lakonishok–Smidt for unconditional TOM. Exact sample/window **pin pending verification** if cited in RESULTS; not required for H1. |

---

## Mapping discipline (do not invert)

| Literature idea | HARV-0 frozen ops (§4) | Allowed use |
|---|---|---|
| TDF contrarian rebalancing (Parker et al.) | Condition on ES−ZN `R_spread`; fade winner over T-3→T-1 | Mechanism narrative + monitor design inspiration |
| Month-end T-3→T-1 pressure (Etula et al.) | Window = close(T-3)→close(T-1) | Timing convention already frozen |
| Unconditional TOM (Lakonishok–Smidt) | Reported as context metric only | Never gates verdict |

**Executor checklist:** before Phase-5 closure, optionally replace `pin pending verification` rows with page/table citations from the PDFs. Still do not edit §4.
