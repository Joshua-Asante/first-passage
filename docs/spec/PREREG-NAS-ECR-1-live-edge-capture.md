# PREREG-NAS-ECR-1 — Live edge-capture of the NAS100 pyramid edge

> **Engine retired 2026-07-11.** `ops/live_journal/scripts/ecr_rolling.py` and the CFD
> estate were deleted per
> [`docs/adr/2026-07-11-ops-cfd-estate-retirement.md`](../adr/2026-07-11-ops-cfd-estate-retirement.md).
> This pre-reg remains a **PARKED** historical record (unreachable since 2026-07-01);
> paths citing `ops/live_journal/` below are forensic, not live.

**Type:** Forward-test pre-registration (frozen BEFORE the first live NAS100 fill).
**Epistemic status:** OUT-OF-EVIDENCE-BASE — there is **zero** live NAS100 execution data. This is a forward hypothesis, not a confirmation. Enabling it = a new test, not evidence.
**Status:** PRE-REGISTERED / GATED on first verified Striker NAS100 v1 Copygram→DXTrade fill.
**Authored:** 2026-06-20. **Belt:** Striker NAS100 v1 LOCKED — this test is **characterization + operational**, it touches no Pine parameter.

**Status update (2026-07-01 — reachability only; no frozen criterion changed):** the §6 gate below (first Copygram→DXTrade NAS100 fill) is now **UNREACHABLE** — per [`docs/adr/2026-06-30-no-manual-trading-cfd-retirement.md`](../adr/2026-06-30-no-manual-trading-cfd-retirement.md) manual trading is retired and the DXTrade/CFD venue is idle, and the futures replacement (TV→TradersPost→Tradovate MNQ) does not yet exist. This pre-reg is therefore **PARKED**, not awaiting-first-fill. The frozen §4 hypothesis and §6 thresholds are **untouched**; re-pointing the test to MNQ fills is **not type-preserving** (different fill microstructure + CFD-specific cost anchor) and requires a **fresh Pre-Q**, not an edit here.

---

## §0 — Rule-0 production reads (verified this session)

| Source | What it grounds | Anchor |
|---|---|---|
| `core/firm_rules.py` `_BASE_RISK["striker_nas100"]=0.0037` | live sizing 0.37% | read 2026-06-20 |
| `core/strategies/nas/LOCK.md` | params, **contractValue=10**, Mon/Tue, 13–17 UTC, pyramid 1000% @1.10×ATR / ≥6 bars, maxHold 15b | read 2026-06-20 |
| `ops/live_journal/scripts/ecr_rolling.py` | **ECR = realized/counterfactual**, per-strategy, rolling 6-wk, **feed=Alchemy**, `INSTRUMENT_TO_ENGINE["NAS100"]="striker_nas"`; per-fill rows in the **gitignored** `reports/ecr/<asof>_rolling6w.json` | read 2026-06-20 |
| `docs/notes/notice/N-2026-06-03-nas100-indicator-contractvalue-missing.md` | live lot sizing 10× defect **fixed** (so a live-vs-backtest gap will be execution, not a sizing bug) | read 2026-06-20 |
| `lab/archive/q_nas_4_2026-06-20/cost_proxy.py` + `cost_proxy_results.json` | the friction thresholds this pre-reg pins (add-cohort linear headroom **31.7 pts**; √-impact ~8.6 pts→PF 2.45; linear-in-size ~24 pts→PF 1.30) | authored 2026-06-20, independently re-derived |
| `lab/analysis/identify_nas100_2026-06-20/` + `q_nas_4_2026-06-20/CLOSURE.md` | the edge is ~88–92% pyramid-add legs (32–61-lot orders); Q-NAS-4 closed the regime-gate angle | this session |

**Gap surfaced by §0 (load-bearing for §3):** `ecr_rolling.py` aggregates ECR to **strategy level only**. The per-fill rows needed for a **cohort split (base vs pyramid_add)** and a **per-fill slippage** measure already exist in the gitignored JSON (`entry["fills"]`), but are not surfaced. The test therefore needs a small read-only post-processor over that JSON — **not** a new engine (D4: refactor, never fork).

**Threshold provenance caveat:** the **ECR floor 0.70** is the DJ30 live precedent; it is **not** a constant in `ecr_rolling.py`. It is pre-registered here as the operator's chosen floor, not cited as production truth.

---

## §1 — Context

The Identify→Notice→Inquire loop (2026-06-20) established, on backtest data: the NAS100 edge is **~88–92% concentrated in pyramid-add "monster" legs** that ride intraday continuation to the 15-bar maxHold; the base layer is near-breakeven by design (belt: *pyramid IS the strategy*). Q-NAS-4 closed the "monsters fire in up regimes" angle as a fragile, non-actionable tendency. The **only operable open question** is whether this backtest edge **transfers to live fills** — and the cost-proxy showed the edge's entire friction exposure is **market impact on the large (32–61-lot) pyramid-add orders**: it survives linear and √-impact cost (add-cohort tolerates 31.7 pts of pure linear cost) but degrades to marginal (PF 1.30) under linear-in-size impact. That regime is unobservable in backtest and resolvable only live. Doctrine connection: the operation's documented ~$10K live execution leakage (DJ30/Guardian) is the prior that this bites; ECR is the standing live falsifier.

---

## §2 — Question (symptom, no fix baked in)

What is the cost of the NAS100 edge being concentrated in the few legs most exposed to fill friction (the large pyramid adds), and does that edge survive contact with live execution? Stated as a symptom, not a remedy: *the edge is ~90% in 32–61-lot orders fired mid-continuation and exited on a timeout, and we have no live measurement of how those specific orders fill.*

---

## §3 — Operationalization

**Data sources (live):** DXTrade fills (via Copygram bridge) → `ops/live_journal` reconcile → `reports/ecr/<asof>_rolling6w.json` per-fill rows. Counterfactual = Alchemy backtest (the runner's feed).

**Metrics (computed by a read-only post-processor over the per-fill JSON; cohort = base vs pyramid_add from the matched signal's leg type):**
1. **Per-fill round-trip slippage (points)** = entry_slip + exit_slip, where entry_slip = (live_fill − expected_entry) in the adverse (long: higher) direction, exit_slip = (expected_exit − live_fill) adverse. Expected prices = the matched backtest signal prices. Report per add leg, in points **and** in R (÷ that leg's stop distance).
2. **ECR_add** = Σ realized P&L (pyramid_add legs) / Σ counterfactual P&L (pyramid_add legs). Also ECR_base for contrast.
3. **Live pyramid P&L share** = realized add P&L / realized total P&L.
4. **Add-spawn rate** = live pyramid_add legs / live base legs.

**Why cohort-specific (the load-bearing design choice):** aggregate (strategy-level) ECR — what `ecr_rolling.py` reports today — is **dominated by the many small base legs** and would read "healthy" even if every monster leg were clipped. The edge is in the add cohort; the test must be on the **add cohort**.

---

## §4 — Hypothesis (falsifiable)

**H-NAS-ECR-1 (primary — fast, per-fill):**
> **IF** live pyramid-add fills realize round-trip slippage ≤ **8 index points** (the √-impact band), **THEN** the designed edge transfers (live add-cohort ECR ≥ 0.70 and pyramid P&L share ≥ 70%); **IF** add-fill round-trip slippage is sustained **> 16 points** (the linear-in-size regime), **THEN** the edge is execution-capped and live NAS100 expectancy approaches the backtest a=1 floor (PF ≈ 1.30) — escalate.

**H-NAS-ECR-1 (secondary — slow, cohort ECR):**
> Over the first **N ≥ 10 pyramid-add legs**, the **add-cohort** ECR (`Σ realized_add / Σ counterfactual_add`) holds **≥ 0.70** AND live **pyramid P&L share ≥ 70%**. Reject if ECR_add < 0.70 across two consecutive rolling-6-wk windows, or pyramid share < 70%.

**Null (what refutes "the edge transfers"):** add-fill slippage habitually AMBER/RED (>8, trending >16 pts), ECR_add < 0.70, OR the add mechanism fails to engage (trade-rate clause, §6).

---

## §5 — Forbidden moves

- **No Pine parameter change** regardless of outcome (belt: locked). A poor ECR routes to **execution mechanics or NAS100 allocation sizing** (firm_rules / bridge), never to the strategy.
- **No substituting aggregate ECR for ECR_add** to make the number look healthy (the entire point is the cohort split).
- **No dropping "bad" add fills as outliers** — the monster legs ARE the tail; a clipped monster is the signal, not noise.
- **No re-defining the §6 thresholds after fills arrive** (any post-hoc move voids the checkpoint — §10).
- **No treating a re-backtest on another feed as a live test** (see §8).

---

## §6 — Frozen config, thresholds, and gate (binary)

**Frozen (do not change after data arrives):** locked NAS100 v1 Pine (risk 0.37%, contractValue 10, Mon/Tue, 13–17 UTC, pyramid 1000% @1.10×ATR/≥6 bars, maxHold 15b, SL 1.20×ATR, TP 9×ATR); Copygram 1:1 passthrough; ECR engine = `ecr_rolling.py` / `journal_review.review_window`.

**Slippage bands (round-trip, add-cohort) → backtest-PF consequence (from `cost_proxy_results.json`):**

| Band | add round-trip slippage | implied backtest PF | verdict |
|---|---|---|---|
| GREEN | ≤ 8 pts (√-impact) | ≥ 2.4 | edge transfers |
| AMBER | 8–16 pts | 1.7–2.4 | degraded, viable |
| RED | 16–24 pts | 1.3–1.7 | marginal — escalate |
| KILL | > 24 pts sustained, OR ECR_add < 0.5 | < 1.3 (a=1 collapse) | edge gone |

**Floors:** ECR_add ≥ **0.70** (DJ30 precedent, operator-set); pyramid P&L share ≥ **70%** (LOCK.md tripwire).
**Trade-rate clause:** add-spawn rate ≥ **10%** of base legs (half the backtest ~20%). If adds rarely trigger live, the edge mechanism is not engaging — a **distinct** failure from slippage, equally falsifying "the edge transfers."

**Checkpoints + binary verdicts:**
- **CP-1 (first 3 add fills):** classify each by slippage band. GREEN ×3 → continue. Any RED → escalate to a fill-mechanics review (limit vs market on the add; broker depth at 30–60 lots) before the next add. KILL band on any fill → halt NAS100 adds.
- **CP-2 (first rolling-6-wk window with ≥1 add):** publish ECR_add + slippage distribution. On-track gate: median add slippage ≤ 8 pts AND ECR_add ≥ 0.70.
- **CP-3 (N ≥ 10 add legs OR 4 quarters, whichever first):** **RESOLVED** = ECR_add ≥ 0.70 + share ≥ 70% + slippage GREEN/AMBER. **FALSIFIED** = ECR_add < 0.70 sustained 2 windows, or slippage sustained RED. **AMBIGUOUS** = add-spawn < 10% (mechanism didn't engage — re-scope to the spawn question).

---

## §7 — Power disclosure

The edge legs accrue **glacially**: backtest add-spawn ≈ 8 add legs/year, of which ~3–5/year are Max-Hold monsters. So **ECR_add to N ≥ 10 takes ~15 months**; significance on ECR_add is years away. Per-trade σ on add P&L is large (a few monsters dominate), so cohort-ECR checkpoints are **expectation-based stops, not significance tests** — this doc says so explicitly. **Therefore the PRIMARY instrument is per-fill slippage**, observable on **fill #1**: a single 30-lot fill tells you the impact regime (GREEN vs RED) long before any ECR sample exists. ECR_add is the slow confirmer.

---

## §8 — Path-independence

The validation must be on **live DXTrade broker fills** (market orders via Copygram), NOT a re-backtest on any data feed. A re-backtest — Pepperstone, OANDA, or Alchemy — uses the **same `process_orders_on_close` fill assumption** and would show ECR ≈ 1 **spuriously** (cf. the Pepperstone↔OANDA entry-date Jaccard 0.96 lesson: a different source is the same *path*). The independent variable here is the **fill mechanism** (live market fill at 30–60 lots vs encoded close), which only real fills expose.

---

## §10 — Audit hooks (runnable)

```bash
# ECR engine + NAS100 mapping (expect striker_nas, ECR=realized/counterfactual):
grep -nE "INSTRUMENT_TO_ENGINE|edge_captured_ratio|FEED" ops/live_journal/scripts/ecr_rolling.py

# Run the rolling ECR once a verified NAS100 fills export exists:
python -m live_journal.scripts.ecr_rolling --asof <YYYY-MM-DD> --dxtrade <fills.csv>
# -> reports/ecr/<asof>_rolling6w.{md,json}; per-fill rows in the .json

# Cohort split (the post-processor to add): classify reports/ecr/*.json fills by
# matched-signal leg type (base vs pyramid_add) and compute ECR_add + per-fill slippage.

# Thresholds this pre-reg is pinned to (must reproduce):
python -c "import json;d=json.load(open('lab/archive/q_nas_4_2026-06-20/cost_proxy_results.json'));print('add breakeven pts',d['linear_breakeven_pts']['add']);print(d['size_aware']['impact linear-size (a=1)'])"
# expect add breakeven 31.68; a=1 net ~75,634 / pyr_share ~0.726

# Append-only integrity: was any §6 threshold or gate moved after the first fill?
# If yes -> the checkpoint is VOID (p-hacking at the execution layer). Record in this file's changelog.
```

---

## §11 — Cross-references

- Lineage: `lab/archive/identify_nas100_2026-06-20/IDENTIFY.md` → `docs/notes/notice/N-2026-06-20-nas100-identify-corpus-routing.md` (§4 opened Q-NAS-ECR-1) → `lab/archive/q_nas_4_2026-06-20/CLOSURE.md` + `cost_proxy.py`.
- Engine: `ops/live_journal/scripts/ecr_rolling.py`, `journal_review.py`; skill `live-execution-journal`.
- Bridge state: memory `project_copygram_migration_state` (NAS100 unverified until first fill), `reference_copygram_option_semantics`.
- Belt: `core/strategies/nas/LOCK.md` Known concerns; memory `project_pyramid_is_strategy_for_nas100`.
- Registry: STATE.md → Q-NAS-ECR-1 (Forward, gated).
