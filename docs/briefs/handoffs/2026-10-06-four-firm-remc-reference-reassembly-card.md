# CC handoff — four-firm re-MC §8 step 2(e): calibration-reference panel reassembly

**Date:** 2026-10-06.
**Status:** DRAFT, awaiting the operator's go. It was opened at coordinator (4)'s request, from the #616 pre-freeze review on 2026-10-06. It is due 2026-10-16. A failure by then goes to the operator before freeze (#616 blocker 4a).
**Brief type:** CC handoff, bounded build (worker card).
**Authority (on go):** a coordinator (4) worker. The requirement owner is the four-firm dated re-MC prereg ([PR #616](https://github.com/Joshua-Asante/first-passage/pull/616) at `a9ee4a6`): I-20 ("Accept, intraday", operator 2026-10-05), §7 blocker 4a and §8 step 2(e).
**Rule:** the reference is a non-candidate, but it still must not be **run** through any tier, MC or screen before #616 freezes (§R). This card only rebuilds the panel and its intraday channel, tested on synthetic inputs, and pins the panel digest.
**Return boundary:** a pinned private panel with an `intraday_low` channel, the panel digest written into the return, and public code merged. Otherwise a precise blocker. No MC, no scoring, no prereg edit (coordinator (4) folds the digest into I-20).

## §0 — Production reads (`main@bf46e8f`, 2026-10-06)

Read at `main` `bf46e8f` and `first-passage-archive` `f2a89560` on 2026-10-06.

| Surface | Finding |
|---|---|
| Archive `lab/analysis/c1/tradeify_futures3_remc_2026-07-11/RESULTS.md` :28-39 | Book: Aegis→6J (BEPAD-TEST) + DJ30→MYM + NAS→MNQ, at risk 1.50% / 0.70% / 0.37%. Panel: "decompounded static $200K via roe, scaled to locked risk via pin_r_basis(full_stop_mean)", 2020-01-06→2026-07-01 (1,693 business days). Per-leg 1R and scale: Striker 0.5521, NAS100 0.1254, Aegis 1.0299. Files: the `15d8b`, `beabf` and `ae744` exports. |
| Archive driver `run_tradeify_futures3_remc.py` (deleted in `283d1def`; retrievable at `283d1def^`) | Construction: `roe = net_pnl / equity_before`, `pnl_static = roe × ACCOUNT`, then `pin_r_basis` from `reconcile`. |
| `core/data/tv_exports/cme/SHA256SUMS` | ae744 `e82a2c25…8ca38`; 15d8b `9acfa297…01b9e`; beabf `8884e6dd…c6419`. These now confirm the "provisional" inputs in #616 I-20. |
| `.claude/skills/trade-csv-reconcile/scripts/reconcile.py`, `core/portfolio_mc.py`, `core/mc/ingest.py` `load_trades` | The current homes of `pin_r_basis` / `load_csv` and the loader. |
| [Series builder card](2026-10-05-four-firm-remc-series-builder-card.md) §0.5 item 5 | The `intraday_low` construction to reuse: a conservative coincident sum of per-trade `\|Adverse excursion USD\|`, applied with the same per-leg scale as the P&L. |

## §0.5 — Clarifications resolved at freeze

1. **Panel:** the archived construction is reproduced exactly, with the same three exports, risk percentages and 1R basis. A per-leg scale that differs from the archived 0.5521 / 0.1254 / 1.0299 by more than 1e-4 returns NEEDS_CONTEXT.
2. **Intraday channel:** each trade's adverse excursion is decompounded and scaled exactly like its P&L. The daily low is the coincident sum over the three legs, per the series-builder §0.5 item 5, with no per-tier cost subtraction: the reference panel is cost-netted as archived.
3. **Timezone:** `America/New_York`, DST-aware (#616 I-25).
4. **Output:** a gitignored private root, with a manifest of input digests, scales, window and output SHA-256. Public code lives in `lab/`; tests use synthetic exports.

## §1 — Goal

Rebuild the I-20 reference panel with a paired `intraday_low` channel, and report its digest for #616 I-20.

## §4 — Hypothesis and falsifier

**H:** the rebuilt panel's scales reproduce the archived values within 1e-4, and its business-day window is 2020-01-06→2026-07-01, 1,693 days.

**Falsified by** either failing. That returns NEEDS_CONTEXT to coordinator (4) and the operator before freeze.

## §5 — Constraints and forbidden moves

- No MC, `run_tier_remc`, `score_candidate` or tier read on the reference before #616 is FROZEN.
- No input copied into a worktree or committed. No edit to `core/`, `ops/`, the prereg or any existing test.

## §6 — Acceptance and return taxonomy

Synthetic tests for the decompound/scale/intraday construction, plus `check_boundaries`, cited by launcher records. The return gives the panel SHA-256, the window and the three per-leg scales.

Return labels: **DONE**, **DONE_WITH_CONCERNS**, **NEEDS_CONTEXT** (a scale or window mismatch, or an archive drift), or **BLOCKED**.

```yaml authority
seat: worker
parent: docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push, pr.open]
constraints:
  - no_main_write
  - no_merge
  - synthetic_tests_only
  - no_private_copy_or_commit
  - no_mc_or_scoring_run
  - no_core_or_ops_edit
  - no_prereg_or_owner_record_edit
acceptance:
  - panel_digest_window_and_scales_reported
```

## §7 — Return

*(Filled by the executor after the operator's go.)*

## §10 — Audit hooks

```bash
c=docs/briefs/handoffs/2026-10-06-four-firm-remc-reference-reassembly-card.md
# The return reports the panel digest (expect ≥ 1 after execution).
grep -cE 'panel SHA-256 `[0-9a-f]{64}`' "$c" || true
```
