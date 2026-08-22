# MSL-S4 — Stage G0 PREREG — expiry-OI-strike convergence (MGC)

**Status:** `FROZEN` 2026-08-21 — operator **B4 GO** paid; Explore-confirm **DEFERRED BY OPERATOR
OVERRIDE** at freeze (no market-data access in the sourcing session's environment — see §0a); Pine
**authored CC-solo same session** ([runbook](RUNBOOK.md)); TV backtest is the operator's next step
· **Explore-confirm subsequently RUN 2026-08-21 under `EXPLORE_GO.md`** —
[`AMBIGUOUS-HOLD`](_explore_confirm_2026-08-21_LOG.md) (§4 below, disclosed execution record, not
a re-freeze)
**Date:** 2026-08-21 (freeze)
**Card / campaign:** MSL-S4 · [`STAGE1.md`](STAGE1.md) (`STAGE-1 PASS`)
**Parent charter:** [`docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md`](../../../../docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md) step 5
**Discharges:** [E1 HOLD](../../../../docs/briefs/closures/MSL-S7-closure-resolved-e1-hold.md) —
first WHO named outside the 2026-08-10 INTAKE-DRY set and outside a transfer of C1/C2/C3/S2A/S2B
**Mechanism id:** `expiry-oi-strike-convergence` ([`MECHANISMS.md`](../../../../ops/instruments/MECHANISMS.md))
**Intake gate:** [`TNEC-1`](../../../../docs/spec/2026-08-08-tradeify-necessary-conditions-target-spec.md) (downstream of survivor MC; not this freeze)
**`K_intrinsic = 1`** (one construct class). Cap disclosure-not-gate → DSR floor **0.650** at K=1
([ADR 2026-08-04](../../../../docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md)). Family bank
disclosure: GC/MGC bank **K=3,177** (`disccamp0_gc_2010_18`) — disclosure only, does not floor this seed.
**Cost so far:** **$0.0000** · **K spent: 0** (nothing scored on real data — Explore deferred).
**FROZEN ON THIS FILE'S INTRODUCING COMMIT.**

---

## §0 — Rule-0 / Stage-1 discharge / door-check (parent-side)

| Check | Result |
|---|---|
| Stage-1 record | [`STAGE1.md`](STAGE1.md) — three $0 limbs PASS at RT **$4.12**; cheap falsifier recorded NOT AVAILABLE at freeze, **filled 2026-08-21 via a local run once data access existed** — [`NOT DECISIVE`](_cheap_falsifier_expiry_oi_strike_convergence_2026-08-21_LOG.md); Explore-confirm (below §4) **also since run 2026-08-21** — [`AMBIGUOUS-HOLD`](_explore_confirm_2026-08-21_LOG.md) |
| Cost basis | `firm_rules.py` Tradeify Metals `cost_per_side_usd: 1.06` + tick_value $1.00 × 2 sides → RT **$4.12**; 4× = **$16.48** |
| Cell door-check | `instrument_profiles.py cell MGC expiry-oi-strike-convergence` → BINDING BAR `free-data-5th-leg-snag-closed-2026-07-01` answered **CLEAR via R-FRAMING §2.1** (inherits MSL-C2's own resolution of the identical bar on the identical ledger) |
| Occupancy | **CLEAR** — MGC is not an MYM/MNQ occupancy-release instrument (B8 does not apply); MGC's own K-void was cleared 2026-08-09 (`ops/instruments/MGC.md` G1) |
| Dense-1m / CON-5 pause | Does not bind — this construct runs on the parent options chain's own published expiry calendar, not dense-1m OHLCV |
| Adjacencies | `london-range-failed-extension-fade` FALSIFIED on this exact instrument (MGC) — adjacency, not auto-kill; distinguished by data-generating process in `STAGE1.md` and §Req-1a below, not waved past |
| Implied-SR | Not computed — no `p` was invented (disclosure only, not a freeze-time FAIL, per [ADR 2026-08-13](../../../../docs/adr/2026-08-13-implied-sr-report-only-fade-reopen.md)) |
| Delete/flip (Req 1a) | **Reasoned through at freeze** (§Req-1a below) — a coherent delete/flip design exists for this construct-shape, unlike its dead directional sibling. **Not yet executed on real data** — deferred with Explore (§0a) |
| Panel | **Absent** this clone. No `MGC*`/`GC*` under `core/data/bar_data/`. No Databento credential configured. **Unreadable** at freeze even if attempted. |

**Cheap falsifier:** NOT AVAILABLE this session — no data access (see `STAGE1.md` §Step 4). Did
not invent a substitute. Did not read any real IS/CONFIRM panel (none exists in this environment).

**Verdict:** STAGE-1 + B4 license this G0 freeze. **Not** SHAPE-CLEAR. **Not** explore-scored.

---

## §0a — Deferred-step disclosure (operator override, recorded so it is never read as a silent skip)

The MSL charter's default step order gates Pine authoring (step 6) on Explore-confirm (step 5a)
returning `SHAPE-CLEAR` — every prior MSL card that reached a G0 freeze (C2, C3, C3-K2, S2A, S2B)
was correctly blocked from Pine by an Explore kill, and none has ever reached Pine before this
card. **This card is the first to deviate from that order, and it does so by explicit operator
election, not by omission:**

- The sourcing session had **no Databento API key configured and no cached MGC/GC market-data
  panel on disk** — the same environmental block that stopped the databento data-mining sourcing
  lane outright (see `STAGE1.md`).
- Presented with the choice — hold the candidate until a future session can run the real cost
  estimate + OI-by-strike data check (charter's own named next step), or proceed straight to Pine
  and let the operator's own TV backtest (step 7) serve as the first empirical evidence — the
  **operator chose the latter, explicitly, 2026-08-21.**
- This is recorded here as a **disclosed deviation**, not a claim that Explore-confirm ran or that
  its gate was met. `expiry-oi-strike-convergence`'s `MECHANISMS.md` entry states the same thing.
  No `SHAPE-CLEAR` verdict exists for this card. No data was read. No IS/CONFIRM partition was
  reserved (there is nothing to reserve against).
- **Consequence for the operator's TV seat (charter step 7):** the runbook does not, and cannot,
  link an Explore RESULTS artifact — because none was authorized to run. This is flagged
  explicitly in [`RUNBOOK.md`](RUNBOOK.md) rather than left as a silently missing link, so the
  operator is exercising the TV seat with full knowledge of what has and hasn't been checked.

---

## §1 — Universe and trade geometry (frozen)

| Element | Frozen value |
|---|---|
| Instrument | CME **MGC** (Micro Gold futures); reference level sourced from the **GC/OG** parent options chain (see §6 proxy note) |
| Signal TF | Daily session granularity for the arm window; entries evaluated intraday, chart TZ **America/New_York** |
| Reference level | Highest-open-interest strike on the nearest listed Gold options expiry, read from CME's published Options Settlement Tool / OI Heatmap / Daily Bulletin — **manual per-cycle input, not computable inside Pine** (no TV OI-by-strike feed exists) |
| Arm window | Final **N** sessions before the listed expiry (design parameter, default N=3) — **before**, not after, expiry |
| Direction | Converge: long if `close < strike − threshold`; short if `close > strike + threshold` |
| Independence | **First valid signal per expiry event** (k=1) — not per session |
| Cost | Tradeify Metals RT **$4.12**/contract (2×$1.06 + 2×$1.00); R = (pnl_usd − RT×qty) / stop_usd |
| Point / tick | MGC: **$10.00/pt** ($1.00/tick, 0.10pt/tick) |
| Contracts (design disclose) | Stage-1 screen used **1** and stop **15.0 pts** ($150 R/ct); live/explore qty and realized stop distance are scoring parameters, not selection axes |
| Partitions | **Not reserved this freeze** — no real panel exists to partition (§0a). A future Explore pass must name IS/CONFIRM before any read, per charter discipline, exactly as every other MSL card has done. |

**Not licensed:** a second instrument (MCL) as a scored candidate (a new K spend, per charter step
1); the directional dealer-gamma-sign sibling construct; any equity-index expression (Board-lite
bars the family); a same-Product-Group opposing-sign second leg.

---

## §2 — Req 1a clause-by-clause (frozen reasoning, from the sourcing session's own verification pass)

**Clause 1 — WHO pays (constraint, not preference).** Options market-makers who wrote the
concentrated open interest at the magnet strike, mechanically obligated to keep a delta-neutral
book as time-to-expiry shrinks and near-the-money gamma rises (Γ ∝ 1/√T). The trade's direction is
read directly off **observable** data — spot price vs. the published strike — never off an
assumption about unobservable dealer inventory. This is the clause that distinguishes this
construct from its correctly-dead directional sibling (see `MECHANISMS.md` entry).

**Clause 2 — WHEN (schedule declared before data).** CME's Options Calendar publishes over a
year's worth of listing/expiration dates for both monthly and weekly Gold options in advance.
Clean.

**Clause 3 — WHY it survives (capacity/awkwardness/mandate-inelastic demand).** Raw
open-interest-by-strike for Gold options is freely published (CME Options Settlement Tool, OI
Heatmap, Daily Bulletin) — so the route claimed is **mandate-inelastic demand**, not
assembly-awkward data: taking the other side of concentrated gamma near expiry is a
capital-intensive, risky position, not a free arbitrage against a mispricing (the same survival
story the equity pinning literature gives for its own ~20-year persistence despite public OI
data). Separately, and independently: no gold/metals-futures-specific application of this
regularity was found in the published literature this session — the ingredient data is not
secret, but this application is genuinely un-mined.

**Clause 4 — HOW it dies (constraint observable).** OI-by-strike concentration decaying (the
magnet strike losing dominance), or the options/futures volume ratio compressing.

**Delete/flip.** DELETE: remove the near-expiry condition — convergence-toward-strike should
disappear on non-expiry control sessions (mechanically predicted by Γ ∝ 1/√T, not a post-hoc
rationalization; directly testable, and is literally the equity pinning literature's own control).
FLIP: bet on divergence/repulsion instead of convergence (short below the strike, long above) —
this is well-posed here (unlike the dead sibling, which has no observable sign to invert in the
first place) because construct #2's rule is fully mechanical. A pre-registered Explore pass must
show convergence beats divergence on the same near-expiry displaced population, not merely be
non-zero.

---

## §3 — K and robustness probes (not selection)

- **`K_intrinsic = 1`** — one scored construct class (expiry-OI-strike convergence, MGC).
- **Sweep axes pre-registered as robustness / plateau probes only** (not selection), to be used
  once real data exists:
  - arm-window width N ∈ {1, 2, 3} sessions before expiry (center = 3, frozen default)
  - displacement threshold ∈ {2, 3, 5} points (center = 3, frozen default)
- Any post-freeze widening of instrument / direction / reference-level source / a second story =
  **new K** and a new G0.
- **Forbidden:** treating MCL's illustrative cost arithmetic (`STAGE1.md`) as a second scored
  instrument without its own K spend and card.

---

## §4 — Scoring (EXPLORATION — not run this freeze; named for the future session that does)

**Concrete operationalization: [`EXPLORE_GO.DRAFT.md`](EXPLORE_GO.DRAFT.md)** (drafted 2026-08-21,
after the informal cheap falsifier — see `STAGE1.md` — found the naive fixed-offset control
window trend-confounded). Corrects the design below from a single control-window comparison to an
IAAFT-surrogate null (methodology precedent:
`docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md`), and upgrades the
partitions to properly account for what the cheap falsifier and the operator's TV backtest already
viewed. The abstract limb table below stands as the original frozen intent; the DRAFT token is
where its concrete mechanics live and where any future adjustment gets recorded, append-only.

| Limb | Definition |
|---|---|
| Delete/flip (Req 1a) | Convergence vs. divergence arms, near-expiry displaced population vs. a generic (non-OI-derived) sham reference. Mandatory before any live/TV-informed decision beyond the operator's own step-7 backtest. Concrete sham + gate logic: `EXPLORE_GO.DRAFT.md` §Req 1a. |
| Primary | IAAFT-surrogate significance test on mean displacement reduction (superseded from "mean net R / session-block bootstrap" — no trade-level P&L series exists for this construct at the Explore stage, only a price-displacement statistic; see `EXPLORE_GO.DRAFT.md` §The corrected null) |
| DSR | ≥ **0.650** at `K_intrinsic=1` (disclosure floor) |
| Cost-law | Gross/trade vs **$16.48** at realized stop distances |
| Disclose | Convergence rate alongside the mean · the cheap falsifier's own naive control re-run at full n (non-gating) · per-cycle trend-correlation check · $200/$750 at explored qty |

At G0 freeze: all TNEC N-* limbs **U**. This table is a template for the deferred Explore pass —
none of it has been executed. `EXPLORE_GO.DRAFT.md`'s statistical core
(`explore_confirm_lib.py`) is unit-tested on synthetic fixtures (23/23 passing, incl. a power
check and a false-positive check) but has never touched real data — no live pull has run under
either PREREG.

**Executed 2026-08-21, under `EXPLORE_GO.md` (ISSUED 2026-08-21):** the deferred Explore pass
above has now run —
[`_explore_confirm_2026-08-21_LOG.md`](_explore_confirm_2026-08-21_LOG.md). 75 completed
weekly+monthly cycles, IS-only (CONFIRM never read). **Verdict: `AMBIGUOUS-HOLD`** —
`p_upper=0.5724` (not significant), DELETE weak-PASS, **FLIP FAIL** (divergence beat convergence).
This freeze's own text and constants (`K_intrinsic=1`, DSR floor, cost-law) are unchanged by this
result — this is a disclosed execution record, not a re-freeze.

---

## §5 — Forbidden moves

- Treating the operator's TV backtest (step 7) as a substitute for the deferred Explore-confirm
  delete/flip test if a future session ever does get data access — both are owed, not either/or.
- Silently dropping the arm-window or displacement-threshold sweep axes into selection after
  seeing TV results.
- Treating the `london-range-failed-extension-fade` MGC adjacency as a reason to kill this card
  by resemblance rather than by its own delete/flip evidence.
- Reopening the directional dealer-gamma-sign sibling construct under this id.
- `dry_run=false` / arming / Striker redeploy / any live order.

---

## §6 — Proxy-construction note (parent options → micro futures trade)

The reference *level* (a strike price) needs no rescaling — GC and MGC settle to the identical
underlying gold price, differing only in contract multiplier. What needs standard proxy
discipline is the *traded instrument's* economics (MGC tick value $1.00, already used in §1/§3).
The one **named, not hidden** caveat: does GC's price (where the deep options market's hedging
actually executes) co-move tightly enough with MGC's on the specific days this construct fires
(near-expiry, displaced sessions) for a GC-derived level to be a faithful MGC reference? This is
weaker than the F1-indirect-transmission failures that killed other doors this session (LME
warehouse stock → HG, gold/silver ETF-AP flow → COMEX) because GC and MGC are not
discretionarily-linked instruments the way those were — they are the same commodity's price at two
contract sizes. Still an explicit Explore-stage verification item, not asserted as automatically
fine.

---

## §7 — Path after this freeze

1. **This G0** — FROZEN on introducing commit.
2. **Pine authored CC-solo** (charter step 6, this same session) — [`RUNBOOK.md`](RUNBOOK.md).
3. **Operator TV backtest** (charter step 7) — per the runbook's exact inputs/window/TZ, understanding
   Explore-confirm was deferred (§0a), not run.
4. If a future session gains data access: run the deferred Explore-confirm (§4) before treating any
   TV result as more than the operator's own first look.

---

## §8 — Audit hooks

```text
rg -n "expiry-oi-strike-convergence|K_intrinsic|DEFERRED BY OPERATOR OVERRIDE" \
    lab/analysis/c1/msl_s4_mgc_2026-08/PREREG_G0.md
python3 scripts/instrument_profiles.py cell MGC expiry-oi-strike-convergence
# expected: BINDING BAR still answered CLEAR via R-FRAMING §2.1 in STAGE1 / this §0
PYTHONPATH=lab python3 -c "from research_utils.axis_screen import floor_at_k; assert floor_at_k(1)==0.65"
```
