# P5 (L4) — mutual-fund overweight-dispersion transplant — access probe

**Date:** 2026-08-20
**Authority:** operator un-HOLD ("1 and 2" — this session) on
[`docs/briefs/2026-08-17-six-lead-pursuit-plan.md`](../../../../docs/briefs/2026-08-17-six-lead-pursuit-plan.md)
§2 P5. Licenses the plan's own Phase-1 item only: **access probe on the
holdings-data real-time lag** — the plan pre-registered "expected cheap kill."
**Cost / K:** $0.00 · K=0 — web verification only, no data pull, no `register_search open`.
**Campaign tag:** `P5-L4-MFOVERWEIGHT`

## Verdict: `UNSCREENABLE` — confirmed. Regulatory disclosure lag (45–60 days) structurally exceeds the mechanism's own next-day signal horizon; no systematic real-time substitute exists.

---

## §0 — Rule 0 / access check (this session)

- [`lab/analysis/harvest/koijen_axis2_openalex_2026-08-17/SOURCES_LOG.md:65`](../koijen_axis2_openalex_2026-08-17/SOURCES_LOG.md) — L4 row: Chen, Chen & Cohen (2021), *"Tomorrow Is Another Day: Stocks Overweighted by Active Mutual Funds Predict the Next-Day Market."* Mechanism: active mutual-fund managers' aggregate private information, inferred from cross-fund holdings-overweight dispersion, predicts the **next-day** market (tested on S&P 500 futures; reported >15% annualized, Sharpe >0.9). The log's own note names the load-bearing, unresolved question: real-time availability of the holdings-overweight input, "likely 13F/N-Q, quarterly with ~45-day disclosure lag."
- Web verification, this session (query: "Form 13F N-PORT disclosure lag days real-time mutual fund holdings alternative data 2026"): **Form 13F filings carry a 45-day reporting lag; Form N-PORT quarter-end filings become public after a 60-day delay.** A February 2026 SEC proposal to amend Form N-PORT retains the quarterly-disclosure framework and the 60-day lag — if anything narrowing scope (disclosure only for the third month of each fiscal quarter), not accelerating it. Sources: [SEC.gov Form 13F Data Sets](https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets) · [Alston & Bird, SEC Proposes Relaxation of Form N-PORT Disclosure Requirements](https://www.alston.com/en/insights/publications/2026/02/sec-proposal-relaxes-form-n-port-disclosure) · [Independent Directors Council, SEC Adopts Amendments to Forms N-PORT and N-CEN](https://www.idc.org/node/51957).
- One partial alternative surfaced and rejected as insufficient: "many funds voluntarily disclose monthly holdings on their own websites or through third-party aggregators" (e.g. WhaleWisdom processes filings within minutes of *release*, not within days of the *portfolio date*). This does not resolve the lag — voluntary disclosures are non-systematic, fund-by-fund, and cannot reconstruct the paper's actual signal, which is an **aggregate cross-fund overweight-dispersion measure** requiring broad, consistent coverage, not a handful of early-disclosing funds.

## 1. Why this is a hard wall, not a temporary gap

The mechanism's signal horizon is **next-day** — today's aggregate overweight status predicting tomorrow's return. Even the fastest possible processing of regulatory filings (13F at 45 days, N-PORT at 60) cannot supply "today's" holdings; it can only supply holdings as of a quarter-end 45–60 days stale. Trading on stale holdings information is not what the paper measured, and staleness of this magnitude (weeks, not days) is not a data-engineering problem a faster pipeline solves — it is set by SEC reporting rules, which the 2026 proposal moves toward *less* frequent disclosure, not more. No commercial or alternative dataset identified in this search offers a systematic, near-real-time proxy for aggregate active-mutual-fund overweight dispersion.

## 2. Disposition

**`UNSCREENABLE`**, matching the plan's own pre-registered expectation ("expected cheap kill"). No panel work, no cost dry-run, no construct design is licensed — the access question is the whole blocker, and it is now answered. Closing at $0, consistent with the plan's own Phase-1 scoping for P5.

## 3. Registry / harvest limb-2

Not admitted through intake (no `register_search open`, no manifest, no data ever touched) — per the standing precedent from P1–P4 this same plan, harvest §4 limb-2's counter does **not** increment. No `docs/rejected_candidates.md` row is warranted — this is a data-access finding, not a mechanism kill (the mechanism itself, if real-time holdings existed, is untested here either way).

---

## Verification

```bash
grep -n "13F\|N-Q\|disclosure lag" ../koijen_axis2_openalex_2026-08-17/SOURCES_LOG.md
# Expected: L4 row's own "~45-day disclosure lag" note, unedited
```

## Sources

- [SEC.gov | Form 13F Data Sets](https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets)
- [Alston & Bird — SEC Proposes Relaxation of Form N-PORT Disclosure Requirements](https://www.alston.com/en/insights/publications/2026/02/sec-proposal-relaxes-form-n-port-disclosure)
- [Independent Directors Council — SEC Adopts Amendments to Forms N-PORT and N-CEN](https://www.idc.org/node/51957)
