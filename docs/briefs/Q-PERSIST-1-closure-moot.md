# Q-PERSIST-1 — closure: does the one-week block bootstrap understate multi-week regime persistence?

**Loop:** OUTER (INQHIORI), fast-follow to Q-DECAY-1. **Domain:** data.
**Status:** CLOSED at §2.1 — **MOOT / ALREADY-ANSWERED** (premise-verification gate fired, as the brief anticipated). **Return:** `DONE_WITH_CONCERNS`.
**Reversibility:** analysis only. No MC re-pin, no block-length change, no resampler adoption. No new computation run (would re-derive a settled result — §5; and the locked panel is absent in-worktree, Rule 9).
**Consumer:** the 2026-08-08 quarterly regime check `accept-beta` fork (bust-*probability* input, paired with Q-DECAY-1's bust-*cost* input).

---

## H (falsifiable)

> The one-week block bootstrap materially understates multi-week regime persistence in the real panel, so the MC's common-mode bust probability is optimistic.

**Verdict: the question was already answered by Q-REGIME-TIME-1 (2026-06-09).** H is directionally **CONFIRMED** — the production one-week (iid-weekly) bootstrap *does* understate bust relative to a persistence-preserving block — with the magnitude already in the record: **+0.46pp bust** on the tail-relevant 2020–26 decompounded panel. The locked-anchor transfer is feasibility-limited and bounded small (below).

---

## §0 — Rule-0 production reads (anchors)

| # | Artifact | Anchor | What it establishes |
|---|---|---|---|
| 1 | `lab/analysis/regime/regime_time_cost_2026-06-09/RESULTS.md` (was `ops/reports/regime_time_cost/RESULTS.md` until 2026-08-03; moved under `regime/` with the analysis tree) | `7196893` (analysis `6d843ac` 2026-06-09) | **THE gating read.** Step 2.2 ran the exact one-week-vs-persistence comparison Q-PERSIST-1 specifies (below). |
| 1 | `lab/analysis/regime/regime_time_cost_2026-06-09/regime_time_cost.py` | `6d843ac` | `_build_paths_seed(..., L)`: `L=1` == production iid-weekly; `L=8` == contiguous persistence-preserving block. Both run. |
| 1 | `docs/ltm/briefs/Q-REGIME-TIME-1-cc-handoff.md` | `66d25ce` | Its own §0 read #2: *"Resampling = Mon-anchored 5-bday week blocks sampled **iid** — multi-week serial dependence destroyed."* Q-PERSIST-1's premise was Q-REGIME-TIME-1's **starting point**. |
| 2 | `core/portfolio_mc.py` | `83e589f` | `build_week_blocks`:341 = Mon-anchored 5-day (one-week) tiles; `run_seed`:476 draws `blocks_per_sim` **independent** block indices (`rng.integers(0, n_blocks, ...)`) → **iid weekly**. Block length is **hardcoded** (not a parameter); `blocks_per_sim=(horizon+4)//5` assumes 5-day tiles. |
| 3 | `core/data/tv_exports/pepperstone/*.csv` | — | **ABSENT in worktree** (Rule 9), same as Q-DECAY-1. Real-panel ACF cannot be computed here → §2.2 falls to Q-REGIME-TIME-1's already-published persistence object. |
| 4 | Prior persistence analysis | `6d843ac` | Q-REGIME-TIME-1 Step 2.1 **is** the prior persistence measurement: dead-run distribution median **1w**, p90 **2w**, longest **5w** (2020–26). No separate formal ACF exists in-repo; `regime_stress_2026-06-15` is the regime-signal battery (CLOSED NULL), not a persistence measure. |

---

## §2.1 — Coverage classification (closes the loop)

Production MC = **iid one-week blocks** (`run_seed` draws each week independently). This is precisely Q-REGIME-TIME-1's `L=1` "iid weekly (reconcile)" baseline — which it verified reproduces the pinned S_2020 anchor "to the decimal." Q-REGIME-TIME-1 then ran a **persistence-preserving contiguous block** at `L = max(8, p90 dead-run) = 8 weeks` (≥ longest observed dead-run, so every historical dead-run reproduces intact inside one block — full persistence capture, not partial). Its Step 2.2 result **is** Q-PERSIST-1's §2.2 (real persistence object = run-length distribution) + §2.3 (iid-reproduced) + §2.4 (persistence-preserving variant + bust delta):

| config | pass | bust | median d | p90 d | p99 DD |
|---|---|---|---|---|---|
| iid weekly (= production one-week) | 97.04% | 2.96% | 31 | 125 | 5.93% |
| block L=8 (persistence-preserving) | 96.57% | **3.43%** | 31 | 133 | 5.78% |

**Serial-dependence premium: the production one-week sampler understates bust by +0.46pp** (and p90 by 8 days), median unchanged; p99 DD is slightly *lower* under the block (5.78% vs 5.93% — the tail-compression-not-median-speed finding). This directly confirms H's direction and gives its magnitude — on the 2020–26 decompounded panel.

**§0.5-A classification:** Q-REGIME-TIME-1 did *not* sweep block length across many values (two points: L=1 and L=8) and did *not* justify the production one-week length as persistence-preserving — the opposite: it showed one-week understates. Per §0.5-A this is "iid-vs-single-[longer]-length → proceed." But proceeding reveals that the identical comparison was already run, so the loop closes at §2.1 as **already-answered** (a MOOT-by-prior-work disposition), not a fresh §2.2–§2.4.

## §2.5 — Verdict + concerns

- **H CONFIRMED (already, in the record): UNDERSTATED-by-~0.46pp bust** on the 2020–26 decompounded panel. Median pass-time unchanged; the understatement is a pure tail/survivability quantity — consistent with Q-DECAY-1 (common-mode risk is a bust-tail phenomenon, not a median-speed one).
- **Feasibility-limited on the locked anchor (the load-bearing concern).** The +0.46pp is on the **2020–26 decompounded** panel (334 blocks, HOLD-ADR basis), **not** the locked **2022–26 compounded** anchor (227 blocks, 99.83/0.17/4.37). Re-measuring on the locked panel needs that panel, which is **absent in-worktree** (Rule 9) — do not manufacture it. **Bound:** the understatement on the locked anchor is **> 0 but well below +0.46pp**. The decompounded panel's persistence is dominated by the 2020–21 dead-week-heavy chop (dead-share 2020 29% / 2021 38%); the locked 2022–26 window excludes both, leaving a benign regime with weak multi-week dead-run clustering. At the locked 0.17% bust, the persistence premium is a small fraction of a percentage point. So: the MC's common-mode bust probability is *optimistic in the same direction*, but by a **bounded-small, feasibility-unmeasured** amount on the anchor of record.

## §5 forbidden moves — honored
No MC re-pin, no production block-length change, no resampler adoption. **Did not skip 2.1** — read Q-REGIME-TIME-1 first and let it gate (it closed the loop). **Did not assert dilution without measuring** — cited Q-REGIME-TIME-1's measured +0.46pp rather than the §1 motivation. **Did not re-derive a settled result** (the ACF overlay would re-characterize the same persistence object Q-REGIME-TIME-1 already published, and the real panel is absent). **Did not import Q-DECAY-1's ~11.7%** as a probability (that is conditional-on-kill drawdown; this loop is likelihood).

## Re-check hook
**2026-08-08 quarterly regime check:** pair with Q-DECAY-1. Q-DECAY-1 = "the common-mode tail costs a bust"; Q-PERSIST-1 = "and the MC understates how *likely* that tail is — directionally yes, by +0.46pp on the tail-relevant decompounded panel, bounded-small and feasibility-unmeasured on the locked 2022–26 anchor." If a locked-panel re-measurement is ever wanted, it needs the panel restored locally (Rule 9) and is a scratch persistence-preserving-block re-run vs `99.83/0.17/4.37` — bounded above by +0.46pp; **not a re-pin**.

## Anchors
`portfolio_mc.py`@`83e589f` · Q-REGIME-TIME-1 `RESULTS.md`@`7196893` / analysis `6d843ac` / handoff@`66d25ce` · decompound panel basis `lab/analysis/regime/decompound_remc_2026-06-07/`@`0d6465c`.
