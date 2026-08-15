# `MNQFLOW-1` — 10-level book imbalance → next-minute mid return: frozen pre-registration

**Status:** `FROZEN` — committed before any MBP-10 outcome number is examined.
**Date:** 2026-08-04 · **Operator authorization:** in-session direction *"run the order-flow
probe on the recent MBP-10 windows"* (route 2 named by [`MNQFVG-1` Open/next](lab/archive/mnq_fvg_draw_probe_2026-08-04/RESULTS.md)
after two same-day ICT OHLCV kills).
**Route:** domain-bar **route 2** (order-flow / microstructure modality) on the Databento
subscription's recent-window entitlements. Harvest §1 does not apply. Discovery K discipline
applies.
**K_intrinsic = 1** — one frozen construct, zero swept axes. `K_banked(MNQ)` after MNQFVG-1 is 4
(disclosure, not a gate).
**Cost:** estimate-first. Recent NQ RTH `mbp-10` windows priced at **$0.0000** under the standing
subscription (billable size ~3.2 GB / RTH day). Pull ceiling `--max-cost 1.00`. No `core/`, lock,
allocation, `dd_protection`, lifecycle, Pine, rail, or `LEG_MAP` change.

---

## §0 — Rule-0 reads (executed before this file)

| Source | What it pins |
|---|---|
| [`docs/briefs/2026-07-24-avenue-a-microstructure-scoping.md`](lab/archive/../../../docs/briefs/2026-07-24-avenue-a-microstructure-scoping.md) §2/§6 | Depth-shape is the only live microstructure fork; flow-category is a4-killed; pull needs the qualifying triple **or** (as here) operator-named route-2 on subscription-covered recent windows |
| [`docs/briefs/2026-07-14-a4-flow-data-fork-scoping.md`](lab/archive/../../../docs/briefs/2026-07-14-a4-flow-data-fork-scoping.md) | L3/tick is net-imbalance only for *participant categories* — does **not** kill book-geometry imbalance |
| MNQFVG-1 / MNQPOOL-1 RESULTS (same day) | Route-1 ICT OHLCV expressions on MNQ are presumptively exhausted; Open/next names route 2 |
| `db_fetch estimate` this session | NQ.v.0 `mbp-10` RTH day **$0.00 / ~3.2 GB**; MNQ.v.0 same window **$0.00 / ~8–11 GB**. Prefer **NQ** parent book for structural discovery (proxy-discipline Rule 4); MNQ economics are not scored here |
| `.claude/skills/databento-data/SKILL.md` | Estimate before pull; coarsest schema that answers the question — MBP-10 is required for 10-level depth shape |

**Dedup:** `rg --no-ignore -il "order.?flow|mbp.?10|depth.?imbalance"` over `discovery_manifests/` and
`rejected_candidates.md` — Avenue-A / M2K procurement rulings exist; **no closed in-house
depth-imbalance → next-bar probe on NQ/MNQ**. Distinct from OPENPRESS-1 (OHLCV volume×efficiency)
and from Q-COSTGEO (fill-depth for c1 sizing).

---

## §1 — Hypothesis

**H-MNQFLOW-1.** On RTH minutes of the recent NQ front-month book, the contemporaneous 10-level
size imbalance

\[
I_t = \frac{\sum_{k=1}^{10} bid\_sz_{t,k} - \sum_{k=1}^{10} ask\_sz_{t,k}}
           {\sum_{k=1}^{10} bid\_sz_{t,k} + \sum_{k=1}^{10} ask\_sz_{t,k}}
\]

computed from the last MBP-10 snapshot in minute \(t\) predicts the sign of the next-minute
mid-price return \(r_{t+1} = \mathrm{mid}_{t+1}/\mathrm{mid}_t - 1\), with Spearman
\(\rho(I_t, r_{t+1})\) strictly above the 95th percentile of a minute-shuffled null (same
\(r\) series, \(I\) permuted across minutes within day).

**Why this construct (not a session strategy):** a few-day recent window cannot power a
session-scale n≥150 probe. The honest instrument of the subscription's recent entitlement is
**intra-window minute resolution**. A null here falsifies short-horizon depth-shape predictability
on these windows; it does **not** license a longer historical MBP-10 campaign by itself.

**Avenue-A triple (stated, not waived):**
1. Depth-shape (10-level size imbalance) — escapes a4 ✓
2. Not fill-trivial — answers predictability, not ORB fill realism ✓
3. Survivor-tie — **operator-authorized route-2 after ICT exhaustion**, not a blind mine; ORB-MNQ
   payability is FALSIFIED so limb 3 is not claimed via ORB. Recorded as operator route-2, not as
   Avenue-A §6 RESOLVED procurement.

---

## §2 — Frozen construct

| # | Element | Frozen value |
|---|---|---|
| S1 | Instrument / schema | `NQ.v.0` continuous, schema `mbp-10` |
| S2 | Windows | RTH 09:30–16:00 ET on **2026-07-28, 2026-07-29, 2026-07-30** (three finalized sessions; exclusive end 20:00 UTC) |
| S3 | Snapshot | last MBP-10 row per ET minute |
| S4 | Mid | \((\mathrm{bid\_px\_00} + \mathrm{ask\_px\_00}) / 2\) |
| S5 | Feature | \(I_t\) as in §1; skip minute if denom = 0 |
| S6 | Target | next-minute mid return; drop last minute of each day |
| S7 | Null | 1,000 within-day shuffles of \(I\); seed `20260804` |
| S8 | Gate | empirical p = fraction of null \(\rho\) ≥ observed \(\rho\) (one-sided, predicted positive) |

---

## §4 — Pre-registered expectation

**Most likely: V2 (null).** Short-horizon book imbalance is heavily studied and typically tiny after
costs; three RTH days are a modality shakedown, not a discovery campaign. V1 is live only if the
subscription book carries a large, un-arbitraged imbalance→return link — not the prior.

---

## §5 — Forbidden moves

- **FM-1** — any second cell: no MNQ-scored arm, no TBBO-only arm, no threshold sweep on \(I\),
  no horizon sweep (1m only), no session-aggregate strategy claim.
- **FM-2** — extending the window after seeing results.
- **FM-3** — reading a significant ρ as deployable edge (rail disarmed; no Stage-0 opened here).
- **FM-4** — claiming Avenue-A §6 RESOLVED; this is operator route-2 on subscription windows.
- **FM-5** — pulling MBO or multi-week history under this freeze.

---

## §6 — Verdict gates

| # | Condition | Verdict | Disposition |
|---|---|---|---|
| V5 | usable minute pairs < 500 | `AMBIGUOUS-UNDERPOWERED` | Report census; do not extend window without a new freeze |
| V2 | p_emp ≥ 0.05 | `FALSIFIED` | Short-horizon depth-imbalance predictability absent on these windows; route 2 needs a different named feature or a literature δ |
| V1 | p_emp < 0.05 AND ρ > 0 | `RESOLVED (diagnostic)` | Names (does not open) a Stage-0 for a longer subscription-covered panel; no strategy claim |

---

## §7 — Protocol order

1. This file committed (freeze) before examining pull outcomes.
2. `register_search open` binds K=1, run-id `mnqflow_depth_imbalance`.
3. Harness + synthetic unit tests green before reading parquet.
4. Single run → RESULTS.md + manifest close + board write.

---

## §10 — Audit hooks

```bash
PYTHONPATH=lab .venv-research/Scripts/python -m databento_fetch.db_fetch estimate \
  --symbols NQ.v.0 --stype continuous --schema mbp-10 \
  --start 2026-07-28T13:30:00 --end 2026-07-28T20:00:00
# expect cost $0.00 under subscription

PYTHONPATH=lab .venv-research/Scripts/python -m discovery.register_search open \
  --run-id mnqflow_depth_imbalance --tool custom \
  --search-space-size 1 --alpha 0.05 \
  --data-window 2026-07-28:2026-07-31 \
  --hypothesis "NQ 10-level book imbalance predicts next-minute mid return on 3 RTH days"

.venv-research/Scripts/python lab/archive/mnq_orderflow_probe_2026-08-04/test_run_flow_probe.py
.venv-research/Scripts/python lab/archive/mnq_orderflow_probe_2026-08-04/run_flow_probe.py
```
