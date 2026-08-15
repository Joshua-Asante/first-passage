<!--
Notion export (verbatim content) — Phase-2 migration per docs/adr/2026-06-12-notion-surface-retirement.md
Notion page-ID : 34cdc0b53c11812cbb4ff637ba44736e  (legacy canon-referenced page; resolved in docs/governance/notion-redirect-map.md)
Notion URL     : https://app.notion.com/p/34cdc0b53c11812cbb4ff637ba44736e
Notion path    : Trading Plan ▸ Dev-phase archive ▸ INQHIORI (reference) ▸ Rule 1
Source last-edited (per MCP fetch): 2026-04-24T15:05:05Z
Exported       : 2026-06-13 by Claude Code (Notion MCP fetch); container tags normalized to Markdown, text verbatim
Disposition    : framework/lesson/rule page → docs/methodology/archive/notion/
-->

# 📐 Rule 1 — Small-cell variance prior (codified 2026-04-24)

> 📐 **STATUS: CODIFIED — 2026-04-24.** Standing rule. Applies to all INQHIORI investigations on strategy-cell-level data. Derived from the Mon-H10 2024 inversion closure (page 34cdc0b53c1181428679d7c901873489).
>
> 🔄 **EXTENSION CODIFIED — 2026-04-24.** Partition-hypothesis gate added (see section below). Evidence: Mon-H10 release-day inversion evaluation screened out at p=0.23 under permutation test while passing the core year-slice top-k gate (36.8% < 80%) — demonstrating the core gate alone does not cover partition-type hypotheses. Cross-ref: page 34cdc0b53c11818899ebcd52e6f051f7.

# The rule

**Sub-cell annual deviations at n ≤ 10 are noise-first. Require a tail-contribution gate test before any structural interpretation.**

Before treating an anomaly that lives in a cell of ≤10 trades/year (hour×day, regime-split, session-bucket, etc.) as structural evidence of anything, run this gate:

1. Sort the cell's trades by signed P&L contribution.
2. Compute: `top_k_ratio = |sum of top-k extreme contributions| / |cell total|` for k∈{1,2}.
3. **Gate:** if `top_2_ratio ≥ 0.80`, the anomaly is tail-driven. Log as noise-consistent and do not escalate to Notice or Question phase.
4. Only if `top_2_ratio < 0.80` on all legs of the anomaly → advance to structural testing (distribution shifts, regime overlays, filter hypotheses).

# Why

At n ≤ 10 per cell, single trades move annual expectancy by thousands of dollars. The base rate of "a year that looks inverted by this mechanism" is not negligible — it's what small-sample variance *does*. The naive prior ("if one year looks different, something changed") is wrong at this sample size.

In the Mon-H10 2024 closure:
- Mon-H10 2024 had n=4. Top-2 contribution was 105% of the year's |total| — the two worst losers more than accounted for the full loss; residual was +$67.
- Wed-H10 2024 had n=8. Top-2 contribution was 89%. Residual was +$372, in line with non-2024 years' $0–500 profile.
- Both legs cleared the 80% gate. The bilateral "inversion" was two independent pairs of tail events.
- Had the gate not been run first, H-B would have required building a 15-min OHLC panel from scratch to test hypotheses that never needed testing.

# What this rule replaces

The older habit of framing "X of Y years" consistency stats as peer-equivalent confirmations. That framing treats a 4-trade year and a 40-trade year as equal pieces of evidence. They aren't. Rule 1 formalizes the correction: weigh consistency by sample-size-adjusted variance, not by calendar years.

# Scope

- **Applies to:** any sub-cell (hour×day, year-slice, regime-slice, session-bucket) with n ≤ 10 trades where the analyst is considering escalating an anomaly to structural testing.
- **Does not apply to:** portfolio-level or strategy-level panels with n ≥ 50. At those sample sizes, tail-driver checks are still useful but not gate-critical — proceed through the normal INQHIORI flow.
- **Does not apply to:** operational risk checks where even a single tail event matters (e.g. bust risk, solo-gap-fill exposure, pyramid reversal). Those require the tail event to be characterized, not dismissed.

# Extension — partition-hypothesis gate (added 2026-04-24)

The core Rule 1 (top-k contribution test) addresses anomalies of the form "this year/slice deviated from the panel." It does **not** address anomalies of the form "subset A differs from subset B." Partition-type hypotheses require a different instrument.

## The extension

**When an anomaly takes the form "subset A differs from subset B" at small partition size (n ≤ ~20 per side), run a permutation test before treating the difference as structural.**

Procedure:
1. Pool both subsets back into a single cohort of n_total trades.
2. Randomize the A/B labels 10K–100K times, preserving the original subset sizes.
3. For each randomization, compute the group-mean gap (mean_A − mean_B).
4. Report the p-value of the observed gap against this empirical null.
5. **Screen-out threshold:** if p ≥ 0.10 two-sided, the difference is indistinguishable from sampling variance. Close as noise-consistent. Do not advance to Notice phase.

## Why the core gate is insufficient for partitions

The top-k contribution gate asks: "is this cohort's total dominated by a few extreme trades?" It's the right tool when you suspect that a slice's overall expectancy was moved by 1–2 outliers within that slice. It's the **wrong tool** when you're comparing two subsets of a parent cohort — because both subsets inherit the parent's tail structure, and the question becomes "is the observed between-subset gap explainable by how the tails happened to distribute across the random partition," which is a permutation-test question.

Mon-H10 release-day inversion (evaluated 2026-04-24) demonstrated this gap directly:
- Core Rule 1 top-k gate on the full Mon-H10 cohort (n=31) **passed** (top-2 = 36.8% < 80%). Under Rule 1 as originally written, the hypothesis would have greenlit further investigation.
- Permutation test on the claimed 15/16 partition produced z=1.21, p=0.23 two-sided. The observed $1,926/trade gap sat inside the 95% CI ([–$3,097, +$3,095]) of random-label null splits of the same 31 trades.
- Additional diagnostic: at n=15 per side, ~30% of random splits produce a top-2 ratio ≥ 80% on one side from pure sampling variance. Small-cell partitions **routinely** generate apparent tail-drivenness that means nothing.

The core gate passed, but the hypothesis was noise. Without the permutation extension, Rule 1 would have let this through.

## Scope of the extension

- **Applies to:** partition-style hypotheses (A vs B, release vs no-release, day-of-week splits, regime splits, session splits, etc.) where either subset has n ≤ ~20.
- **Sample-size guidance:** most potent at n_per_side ≤ 20. Beyond ~30 per side the permutation test still works but the null tightens quickly; at large n most real differences survive.
- **Does not replace** the core top-k gate. Year-slice anomalies still use the top-k contribution test. The two gates are complementary and target different hypothesis shapes.

## Expanded Protocol Step 0

Replaces the single-step version in the core rule with two sub-steps:

> **Step 0a — Year-slice small-cell gate (Rule 1 core).** If the anomaly is a single year/slice with n ≤ 10, compute top-2 contribution ratio on that slice. If ≥ 80%, close as tail-noise-consistent.
>
> **Step 0b — Partition-hypothesis gate (Rule 1 extension).** If the anomaly is a between-subset comparison with either side at n ≤ ~20, run a permutation test on the observed between-group statistic (10K–100K randomizations). If p ≥ 0.10 two-sided, close as sampling-noise-consistent.
>
> Proceed to downstream hypotheses only if the relevant gate falsifies.

## Reference implementation

The gate test script used in the Mon-H10 release-day evaluation (pandas + numpy) is reproducible from the CSV alone. Key blocks: load + pair + filter → cohort summary → top-k gate → 100K-permutation null distribution → per-trade contribution dump. When the `15-min USDJPY OHLC panel ingestion` item (page 34cdc0b53c1181cdab8bd2c3a91118e8) lands in the repo, commit the gate script alongside as `analysis/rule1_gate.py` — the two infra items are adjacent in purpose.

# Interaction with existing rules

- **Rule 0 (audit-first for risk-control decisions):** Orthogonal. Rule 0 is Identify-phase discipline (read production code before authoring risk briefs). Rule 1 is Investigate-phase discipline (run the gate test before structural hypothesis work on small cells). Both apply together when applicable.
- **The Algorithm:** Rule 1 is a *Delete before Simplify* instance — delete the hypothesis tree before simplifying or automating against it.

# Protocol text for future INQHIORI briefs

When authoring an Investigate-phase brief for any sub-cell anomaly, include this as Protocol Step 0:

> **Step 0 — Small-cell gate (Rule 1).** If the anomaly cell has n ≤ 10, compute top-2 contribution ratio. If ≥ 80% on all relevant legs, close as tail-noise-consistent. Only proceed to downstream hypotheses if the gate falsifies.

# Cross-refs

- Originating investigation (core rule): Mon-H10 2024 Inversion INVESTIGATE brief (page 34cdc0b53c1181428679d7c901873489).
- Canonical worked example (extension): Mon-H10 release-day inversion evaluation 2026-04-24 (page 34cdc0b53c11818899ebcd52e6f051f7).
- Related infra item: LOGGED: 15-min USDJPY OHLC panel ingestion (page 34cdc0b53c1181cdab8bd2c3a91118e8).
- Framework reference: INQHIORI — the investigation framework (page 34cdc0b53c11812d96f8f6e9ee500d5e).
