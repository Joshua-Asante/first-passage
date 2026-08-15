**Theme:** regime
**Status:** ACTIVE — Q-REGIME-FIT-1 closure findings
# Q-REGIME-FIT-1 — closure (2026-06-17)

**Question (symptom, not fix):** the locked 4-strategy book returned ~nothing since mid-April (~2 months).
What accounts for it, and does any part indicate the strategies have stopped performing within their
locked MC model? (Pre-Q brief: [`Q-REGIME-FIT-1.md`](Q-REGIME-FIT-1.md), pre-registered 2026-06-17 before any number was seen.)

**Verdict — two-part:**

1. **Structural decay: RULED OUT.** Signal-level (locked-blob, to-spec, canonical Pepperstone, static-$200K)
   over the frozen window 2026-04-13→06-17 = **+$34,247 = +17.12% of $200K** — an above-median, clearly-passing
   path vs the locked envelope (median MC pass 26 d / 99.83% pass). INSIDE (≥ p25). The flat-since-mid-April
   feeling is the **modeled idle-in-chop tail**, not a broken edge.
2. **Execution: the actual problem → FIX-EXECUTION.** The live DXTrade account is **−$1,271.71 settled
   (−$1,436 incl. financing), balance $198,563.72**, over the same period the signal book made +17%.
   Edge-captured ratio = **−10.2%** all-in / **−53.2%** behavioral-only (deployed window). The strategies
   are fine; the execution is destroying the edge. **The operator's rebuild / "build new regime signals"
   instinct is exactly wrong** — it would rebuild healthy strategies while the leak is execution discipline.

No `core/` / locked-config / allocation / dd_protection change. Research + diagnosis only. Locked anchor
(99.83 / 0.17 / 4.37) stands.

---

## §0 Rule-0 reads (verified on disk this session, read-only)

| Artifact | Anchor confirmed |
|---|---|
| `core/firm_rules.py` `_BASE_RISK` | guardian 0.0034 / striker(DJ30) 0.0070 / aegis 0.0150 / striker_nas100 0.0037 ✓ |
| `core/strategies/MANIFEST.sha256` | Guardian v5.5 / Striker DJ30 v4.5 / Aegis v4.3 / NAS100 v1, each + `_indicator.pine` ✓ |
| `docs/adr/2026-06-12-tv-csv-canonical-feed-policy.md` | TV/Pepperstone canonical; non-TV feeds staging-only (Alchemy non-canonical) ✓ — **load-bearing**: the §7.2 read uses Pepperstone, not the Alchemy exports |
| `tests/test_mc_anchors.py` | Pepperstone anchor 99.83 / 0.17 / 4.37 pinned (`abs=1e-4`) ✓ |
| `ops/data/gold_gate_shadow_log.csv` | last & only row 2026-04-19 WAIT, KER126 0.0841 < 0.12 ✓ (gate idle since; NOT re-run — see Open) |
| `ops/live_journal/scripts/{ecr_rolling,journal_review}.py` | ECR pipeline requires `--dxtrade <fills.csv>` ✓ |
| `lab/analysis/regime_stress_2026-06-15/` | FALSIFIED-FAIRWEATHER; resizing dead, drift not detection ✓ (forbids the regime-timing lever) |

## The chain

| # | step | artifact | finding |
|---|---|---|---|
| 1 | Feed parity (Alchemy vs Pepperstone) | [`signal_level.py`](signal_level.py) | Canonical Pepperstone does **not** re-sign the read; reads marginally **stronger** (+17.12% vs +16.22%). Load-bearing in-window trades present on both feeds. Feed-translation caveat resolved. |
| 2 | Signal-level vs MC envelope (§7.2/§7.4) | [`signal_level.py`](signal_level.py) | Portfolio static-$200K **+17.12%** over the window → above-median vs median-pass-26d envelope → **INSIDE (≥p25)**. **Decay RULED OUT.** Convention-robust (exit-conv reads higher). |
| 3 | Execution-capture (§7.5, ECR) | [`ecr_reconcile.py`](ecr_reconcile.py), [`ecr_summary.md`](ecr_summary.md) | ECR **−10.2%** all-in / **−53.2%** behavioral. Live −$1,272 vs +$34K counterfactual. **FIX-EXECUTION.** |
| 4 | Reconcile DXTrade statement | [`build_fills.py`](build_fills.py) | 37 round-trips parsed, total settled PnL **−$1,271.71** = exact statement match; 30 pre-5/21 match the already-logged ledger; **7 new trades** (5/22→6/17) saved. |

## Why the book felt dead but isn't (signal level)

Per-strategy, in-window (Pepperstone, static-$200K, entry-date convention):

| Strategy | trades | W/L | static $ | % of $200K | gain timing |
|---|---|---|---|---|---|
| NAS100 v1 | 10 | 7W/3L | +27,513 | +13.76% | ~90% from 04-13/04-14 pyramid Long-Adds |
| Aegis v4.3 | 3 | 2W/1L | +6,071 | +3.04% | one winner 04-15 |
| DJ30 v4.5 | 4 | 4W/0L | +3,393 | +1.70% | ~83% on 04-17 |
| Guardian v5.5 | 4 | 0W/4L | −2,730 | −1.36% | dead in-window — the leg the gold gate switched **OFF** (WAIT 04-19) |
| **PORTFOLIO** | | | **+34,247** | **+17.12%** | front-loaded; post-04-20 tail (~8wk) = **−1.14%** |

The +17% is a lumpy, pyramid/breakout-front-loaded book catching one mid-April cluster; the ~8-week tail is
−1.14% (modeled chop). Guardian's in-window deadness is *anticipated by the operator's own gate*.

## Why the account lost money anyway (execution)

The +17% signal edge was **not captured**. Attribution (static-$200K counterfactual = +$34,247):

- **Deployment gap — $27,658 (81% of the edge), un-capturable.** The 04-13/04-14 NAS100 pyramid *was* the
  window's edge, but **NAS100 v1 wasn't operationally deployed until ~2026-05-07** (first live USTEC fill 05-11).
  Not behavioral — the book wasn't fully live during its best opportunity.
- **Behavioral leakage on the deployed window (cf +$6,589 → realized −$3,507 = −53% ECR):**
  - **Aegis 04-15 decomposition −$5.7K** — backtest one 12:30 entry held to +$6,086; live split into three
    fills (one stopped, others continued) → +$362. This **is** documented lesson E2 (the 2026-04-15 Aegis incident).
  - **Aegis 05-19 −$2.3K** — flat +$47 signal taken at 25 lots and exited 7 min later for −$2,300.
  - **DJ30 04-17 behavioral skip −$2.8K** — the +$3,144 backtest winner; DJ30 *was* deployed, signal skipped.
  - **Guardian 05-14 skip** (a loser, so +$686 avoided by luck), **DJ30 06-16 skip**, plus **OFF-SPEC
    discretionary** XAUUSD/USDJPY/DJ30 trades (4/14, 4/16, 5/20) netting +$1,800 but high-variance, off-system.

## Honest bottom line

The brief did its job: the operator held a strong "strategies are dead, rebuild" prior; measurement shows the
**strategies are healthy (+17% signal-level, INSIDE the envelope) and the live execution is the entire problem.**
Two of the three behavioral failures are *already-documented* lessons (E2 Aegis decomposition fired again).
The single largest miss (NAS pyramid) is a deployment-timing gap, not a skip. The disposition is **FIX-EXECUTION,
not rebuild** — and the regime-stress prior independently forbids the regime-signal-build lever anyway.

§6 verdict cell: **signal-level ≥ p25 AND ECR < 0.70 → FIX-EXECUTION.**

## §7.1 convention pin (closure amendment — does not change the verdict)

The pre-registered brief left window-membership entry-vs-exit dating unpinned (a known split-convention trap).
Pinned at closure to **entry-date** membership (measures edge the window *originated*). The portfolio verdict
is **convention-robust**: exit-date reads *higher* (Guardian flips to +$1,606), so INSIDE/decay-ruled-out holds
either way. Only Guardian's per-leg sign is convention-sensitive. Pinning is recorded here, not back-edited into
the frozen brief (avoids p-hacking the pre-registration).

## Forward action

The disposition is FIX-EXECUTION → see [`ACTION_NOTE.md`](ACTION_NOTE.md): the four measured leaks (Aegis
04-15 decomposition −$5.7K = lesson E2, Aegis 05-19 oversizing −$2.3K, DJ30 04-17 skip −$2.8K, off-spec
discretionary) distilled into pre-trade rules + the deployment-completeness lesson, with the weekly ECR
cadence (now runnable — the pipeline schema-drift fix landed this session).

## Gold gate — re-run 2026-06-17 (sets E1/E2)

Re-ran `ops/regime_gate/gold_gate_shadow.py` (fetched fresh OANDA bars through 06-17). Current reading
**WAIT**, gold **KER_126 = 0.055** < 0.12, TSMOM_126 **−10.7%**, TSMOM_252 +25.8% — **deeper chop than
the 04-19 reading** (KER 0.084), short-trend now negative. → **E2 (regime-honest) is primary.** This
corroborates the diagnosis (Guardian's in-window deadness is the gate-flagged, persisting chop) and does
**not** flip the INSIDE call (the +17% / above-median signal-level result holds under either envelope).
Log row appended to `ops/data/gold_gate_shadow_log.csv`.

Two `scripts/fetch_oanda_bars.py` maintenance drifts surfaced (flagged, not silently committed): (1) `END`
is hard-frozen at `2026-04-20` so it cannot produce a current reading; (2) it writes to the pre-monorepo
`data/bar_data/` instead of `core/data/bar_data/`. The current reading above used a one-off fetch through
`lib.oanda`; the committed script and the bar manifest are untouched.

## Open (not outcome information about the decay test)
- **MC envelope** — the INSIDE call rests on the verified median-pass-26d anchor (a +17% / 45-day path is
  above-median). A bespoke D-day cumulative-R envelope would sharpen the percentile, not the call.
- **journal_review schema drift** — `load_backtest` expects `Trade #` / `Net P&L USD`; current TV exports use
  `Trade number` / `Net PnL USD`, so the canonical pipeline could not parse them. ECR here was computed by
  `ecr_reconcile.py` (static-$200K normalized, deployment-aware). The pipeline shim is a separate maintenance task.

## Reproduce

```
python signal_level.py     # canonical Pepperstone + Alchemy feed-parity, static-$200K
python build_fills.py      # parse DXTrade statement -> fills ledger, reconcile vs already-logged
python ecr_reconcile.py    # static-$200K edge-captured ratio, deployment vs behavioral attribution
```
Scripts read the gitignored vendor exports + the DXTrade statement from `~/Downloads` (same convention as the
2026-06-15 regime-stress chain). The complete fills ledger (PII) is saved at
`~/Downloads/dxtrade_account_statement_2026-06-17.csv` (37 trades, 3/10→6/17); it is NOT committed.
