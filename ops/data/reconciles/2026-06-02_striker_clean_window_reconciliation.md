# Striker DJ30 + NAS100 Clean-Window Execution Reconciliation — CC Return

**Date:** 2026-06-02 · **HEAD:** `c0ec998` · **Branch:** `fix/copygram-coderabbit-followups`
**Status return:** `BLOCKED: plan-wrong` (escalate to parent) · secondary `NEEDS_CONTEXT` (fresh counterfactual CSVs)
**Binary closure verdict:** `AMBIGUOUS` — premise not yet diagnosable · **Re-test ≈ 2026-06-16**

> Uncommitted. Per §5, commit is Joshua's call.

---

## Phase 0 reads (with anchors)

| # | Read | Result | Anchor |
|---|------|--------|--------|
| 1 | HEAD commit | `c0ec998` (fix/copygram-coderabbit-followups) | `git log -1` |
| 2 | Pipeline pyramid-aware? | **YES** — window extends to `exit_time` for pyramid arch; `multi_fill_ok = is_pyramid or len==1` | `live_journal/scripts/journal_review.py:354-356, 395`; ECR `:695` |
| 3a | DJ30 v4.5 backtest CSV coverage | **2022-01-04 → 2026-04-17** (last trade #218 @ 2026-04-17 13:00). **Does NOT cover clean window.** | `data/tv_exports/pepperstone/Striker_DJ30_v4.5_PEPPERSTONE_US30_2026-05-24_567e1.csv` |
| 3b | NAS100 v1 backtest CSV coverage | **2022-01-11 → 2026-04-14** (last trade #196 @ 2026-04-14 14:00). **Does NOT cover clean window.** | `data/tv_exports/pepperstone/Striker_NAS100_v1_PEPPERSTONE_NAS100_2026-05-24_11605.csv` |
| 4 | Lock dates | NAS100 v1 + DJ30 v4.5 migration **2026-05-05** ✓ (commit `4c65d29`). Allocation-refresh-2 (DJ30 0.70%/pyr750, NAS 0.37%): commit `fd2a967`/`365aff8` dated **2026-05-18**, ADR named **2026-05-23** — minor date discrepancy, non-gating (only DJ30 trade in window is 2026-05-29, post both). | `git log` |

**§0.5 resolutions:**
1. **Live-truth source — SUPPLIED.** DXTrade Single-Currency account statement (`Downloads/Single-Currency_account_statement (2).pdf`), account 1840123, 09 Mar → 02 Jun 2026, $200K start / $199,307 end. Replaces the too-sparse Notion journal. ✓
2. **Window:** default 2026-05-05 → 2026-06-01 used; 2026-05-23 DJ30 sub-boundary noted (moot — sole in-window DJ30 trade is 2026-05-29).
3. **Scope:** Striker DJ30 + NAS100 only. ✓

---

## The two blockers

### Blocker A (structural — binding) — clean window too short / too sparse → AMBIGUOUS
Clean-window live Striker activity (DXTrade statement, intraday — **no Striker overnight holds in window**, so no swap-cf gap):

| Leg | Closed trades (05-05→06-01) | Realized |
|-----|---|---|
| NAS100 | 4 | −$581.94 |
| DJ30 | 1 | +$30.00 |
| **Combined** | **5** | **−$551.94** |

(Extending end to 06-02 adds one NAS trade → 6 trades, −$506.29.)

Combined on-spec signal count **≈5 (< 10 floor)** and window **≈4 weeks (< 6-week floor)**. Per §6 + Trap #7, ECR is a 6-week+ metric; this window cannot support a non-AMBIGUOUS verdict **even with a perfect counterfactual.** This is the §6 `BLOCKED: plan-wrong` case: premise not yet diagnosable.

### Blocker B (data — secondary) — no in-window counterfactual
Freshest backtest CSVs (2026-05-24 vintage) end **2026-04-17 / 2026-04-14** — entirely before the clean window. **Zero backtest signals in 2026-05-05 → 2026-06-02.** ECR denominator is uncomputable from the brief-mandated source. (The `live_journal/data/counterfactuals/` Pine pipeline has NAS-May coverage but **no DJ30 post-March** counterfactuals, and is a different methodology than §2.3 authorizes — not substituted.)

Note: with no in-window backtest, the live 2026-05-29 DJ30 (+$30) and the NAS fills cannot even be classified ON-SPEC vs OFF-SPEC vs SKIPPED. Whether the live DJ30 trade had a matching backtest signal is itself unknown until a covering export exists.

---

## §4 verdict
Hypothesis **not evaluable.** ECR ≥ 80% AND behavioral-leakage ≈ 0 cannot be tested: counterfactual absent, sample below floor. **Neither RESOLVED-OPEN nor RESOLVED-CLOSED** — `AMBIGUOUS`. The new long-only strategy build stays gated (Stage-0 unresolved, not cleared).

## Re-dispatch spec (≈ 2026-06-16, when ~6 weeks post-05-05 accrue)
Needed to re-run:
1. Fresh TV strategy-tester exports, **chart loaded through ≥ 2026-06-16**, static `initial_capital` basis:
   - `StrikerDJ30:` Striker DJ30 v4.5 PEPPERSTONE US30
   - `StrikerNAS100:` Striker NAS100 v1 PEPPERSTONE NAS100
2. Refreshed DXTrade statement through re-test date.
3. Re-run: `python live_journal/scripts/journal_review.py --dxtrade <stmt.csv> --backtest striker_dj30:<dj30.csv> striker_nas:<nas.csv> --start 2026-05-05 --end <retest> --feed pepperstone`
   - DXTrade PDF → CSV first (statement is PDF; pipeline expects CSV with Open/Close Time, Symbol, Net P&L).
   - Unit note: live NAS lots (1.0–1.85) vs backtest qty (33–465) differ in units — confirm normalization before pairing.

Even at re-test, combined Striker signal count must clear ≥10 or the gate stays AMBIGUOUS.
