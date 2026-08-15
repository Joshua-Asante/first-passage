# Gen-2 parity gate — band freeze (FROZEN-PRE-RUN)

**Status:** `FROZEN-PRE-RUN` — bands set **before** any family TV-anchor run.
**Date:** 2026-08-07
**Owner brief:** [`Q-FILLTAX-1`](../../../../docs/briefs/Q-FILLTAX-1-fill-realism-and-parity-scoping.md)
**Spec:** [`SPEC S3`](../../../../docs/spec/2026-08-07-loop-s3-arbiter-two-tier-spec.md)
**Methodology shape:** [`prefilter_rank_correlation_gate.md`](../../../../docs/methodology/prefilter_rank_correlation_gate.md)
**Cost:** $0 · K=0 · no arming · no vendor CSV required for the harness unit tests

> ⚠ These constants are **independent FROZEN-PRE-RUN placeholders** for the Gen-2
> engine↔TV-anchor arbiter. They are **not** claimed as inherited Gen-1 sweep-layer
> values. Gen-1 `lab/validation` is retired. Any post-hoc widening after seeing a
> family result is forbidden (S3 boundary + methodology falsifier).

---

## §1 — Admission bands (FROZEN-PRE-RUN)

| Constant | Value | Role | Label |
|---|---:|---|---|
| `RANK_RHO_FLOOR` | **0.75** | Spearman ρ floor on aligned per-trade PnL (engine vs TV anchor). Below → FAIL | `FROZEN-PRE-RUN` |
| `NET_REL_BAND` | **0.02** | \|net_engine − net_tv\| / max(\|net_tv\|, ε) ≤ band | `FROZEN-PRE-RUN` |
| `PF_REL_BAND` | **0.02** | \|pf_engine − pf_tv\| / max(pf_tv, ε) ≤ band | `FROZEN-PRE-RUN` |
| `MIN_TRADES` | **30** | Minimum aligned trade count; below → FAIL (underpowered, not ADMIT) | `FROZEN-PRE-RUN` |
| `EPS_DENOM` | **1e-12** | Denominator floor for relative bands | `FROZEN-PRE-RUN` |

**Verdict mapping (harness exit):**

| Outcome | Condition | Exit |
|---|---|---:|
| `ADMIT` | ρ ≥ `RANK_RHO_FLOOR` **and** net rel ≤ `NET_REL_BAND` **and** PF rel ≤ `PF_REL_BAND` **and** n ≥ `MIN_TRADES` | 0 |
| `FAIL` | any limb misses | 1 |

---

## §2 — What is scored

- **Inputs:** two same-feed trade series on CME TV exports — `engine` (Python) and
  `tv_anchor` (one manual TradingView export per strategy family).
- **Alignment:** join on `trade_id` when present; else positional alignment after
  sorting by `entry_time` (ISO-8601). Mismatched lengths → FAIL.
- **Ranking metric:** per-trade `pnl` (float, account currency of the export).
- **Agreed scalars:** sum(`pnl`) = net; profit factor = gross_wins / max(gross_losses, ε).

No mutation battery is frozen in this scaffold (Q-FILLTAX-1 Phase 1 still owed).
This freeze covers **admission bands only**.

---

## §3 — Forbidden moves

- Tuning any row in §1 after seeing a family anchor result.
- Claiming Gen-1 inheritance for these numbers.
- Granting research authority without a passing family TV anchor.
- Treating offline fill-ports as a substitute for a native TV anchor.
- Arming the rail or capturing live fills under this freeze ($0 scaffold only).
