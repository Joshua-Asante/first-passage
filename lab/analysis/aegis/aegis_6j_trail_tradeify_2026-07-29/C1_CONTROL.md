# Control C1 — engine equivalence: **GREEN (exact)**

**Date:** 2026-07-29 · **Control for:** [`Q-6JCOMPOSE-2`](../../../docs/briefs/pre-registration/Q-6JCOMPOSE-2-verdict-preregistration.md) §7 C1 / §3 P5
**Inherited from:** [`Q-6JCOMPOSE-1`](../../../docs/briefs/closures/Q-6JCOMPOSE-1-closure-void-unexecutable.md) (CLOSED `VOID`) — C1 is
independent of the 6J input, so it survives the predecessor's closure.
**Evidence:** [`c1_control_full.log`](c1_control_full.log) · [`c1_control_report.json`](c1_control_report.json)
**Command (engine imported UNMODIFIED — no wrapper, no patch):**

```bash
python lab/archive/q_compose_1_2026-07/run_compose_regime_remc.py --out-dir <scratch>
```

---

## Result — exact reproduction on all four partitions

`Tradeify_Select_100K [trailing_locking]`:

| Partition | Published Q-COMPOSE-1 | This run | Δ |
|---|---:|---:|---|
| full | 38.75% | **38.75%** | 0.00 |
| H1 | 54.73% | **54.73%** | 0.00 |
| H2 | 25.84% | **25.84%** | 0.00 |
| bootstrap-95th | 47.14% | **47.14%** | 0.00 |

§7 C1 required reproduction "to within reporting precision." Achieved **digit-for-digit**, which is
stronger: it establishes that the engine, *this* environment, the local DBN cache, and the seed set
(42/123/2026; bootstrap 20260715) jointly reproduce the published row.

Corroborating rows also reproduced: `pass5 = 52.9%`, breadth `dependence N_eff 1.9948 → 2.9502
(+0.9554)`, `risk N_eff 1.9593 → 1.9628 (+0.0034)`, and the engine's own
`VERDICT FALSIFIED` for the ORB composition.

**⇒ C1 GREEN. Q-6JCOMPOSE-2 §3 P5 is DISCHARGED.**

## Environment notes (no spend, no data pull)

- `databento` installed at the repo's **own pinned** versions (`requirements-research.txt`:
  `databento==0.81.0`, `databento-dbn==0.62.0`). Import-only need.
- The DBN cache was **already local** — `~/.databento_cache/` (481 files), including the required
  `ohlcv-1m_continuous_ce119c1e8f923316.dbn`. **$0.00 spend; no `get_range` call.**
- Hook 2 verified empty before and after: the engine was never edited.

## Measured cost — relevant to the §2 tier decision

**Wall clock 4,562 s ≈ 76 min** on 8 cores (`--n-jobs -1`; 15 worker processes observed).

The engine loops tiers **serially** (`n_jobs=args.n_jobs, tiers=(fk,)` per call), each tier
internally parallel, over 4 tiers × (Part A full + Part B H1 + H2) × 3 seeds × 10,000 sims plus
Part A bootstrap 100 panels × 126 bd per tier.

**Only `Tradeify_Select_100K` is Q-6JCOMPOSE-2's verdict surface**, so ~3/4 of that wall clock is
spent on tiers the verdict does not read ⇒ a single-tier arm run would cost **≈19 min**. Taking that
saving requires **pre-registering** it in §2 while the brief is still unsigned — doing it after the
freeze would be either an engine edit (violates hook 2) or a method deviation. **Operator decision,
not taken here.**

## What this does NOT establish

C1 proves the **engine** is intact and reproducible. It says nothing about the 6J column: that is
**C2**'s job (all-zero 6J must return the 2-leg baseline 0.11 / 0.22 / 0.04, proving the wrapper does
not perturb the incumbents). **No 6J composed number has been computed or read.**
