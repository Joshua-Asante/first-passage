# NOTICE 2026-08-15 — Blind-channel cost geometry (measured) + MNQ-ANALOGUE-1 killed pre-G0

**Notice ID:** N-2026-08-15-blind-channel-cost-geometry-and-first-candidate-kill
**Observed:** 2026-08-15
**Author:** Claude Code (parent-side computation) + Joshua (route ruling)
**Type:** Notice-phase. Records measurements and one pre-G0 kill; **rules nothing**. **$0 · K=0 · no manifest · no Q-ID.**
**Status:** `HELD` — the channel's feasible set is **empty at $0** after this kill.
**Trigger:** operator direction to plan the first candidate for the [no-counterparty statistical sourcing channel](../../adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md), then to "focus on cost geometry first."

---

## §0 — Source anchors

| Source | Anchor |
|---|---|
| [channel ADR](../../adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md) + K-cap addendum | `91b8344` 2026-08-15 |
| `lab/research_utils/axis_screen.py` (`floor_at_k`, `CAP=1.0`) | `2ef7405` 2026-08-04 |
| `lab/discovery/cost_model.py` (`bp_hurdle`, `resolve_commission`) | read this session |
| `lab/discovery/k_count.py` (K_DSR non-overlap floor) | read this session |
| `core/data/bar_data/*.csv` | primary checkout; MNQ 141,541 bars, 2020-07-01→2026-07-03 |
| Tradeify commission table | help.tradeify.co art. **10468315**, page-dated **2026-04-28**, read in-browser 2026-08-15 |
| index raised bar + route ①| [`rejected_candidates.md:718-744`](../../rejected_candidates.md); scope ruled [ADR 2026-08-10](../../adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md) §2-A |
| CON-5 lane pause | [`Q-TNEC-CON-5 closure`](../../briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md) §Iterate |
| DISC-CAMP-0 (prior wide mine) | [`closure`](../../briefs/DISC-CAMP-0-closure-falsified.md) · `discovery_manifests/disccamp0_gc_2010_18.json` |

---

## §1 — The observation

### (a) Cost geometry, measured per instrument at its own panel-era median (M-20 discipline)

Commission is **primary-sourced**, all-in ("Total Round Trip Cost includes Exchange fees, NFA fees, Clearing fees, and Commissions"). Slip = 1 tick per side. Required capture = `hurdle_4x / median session range` for a **one-trade-per-session** construct.

| Inst | notional | comm RT | slip RT | RT | hurdle_4× | med sess range | range/RT | **req capture** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MNQ | $30,945 | $1.82 | $1.00 | $2.82 | 3.65 bp | 160.3 bp | 175.9 | **2.27%** |
| MGC | $24,673 | $2.12 | $2.00 | $4.12 | 6.68 bp | 127.3 bp | 76.2 | 5.25% |
| MYM | $17,581 | $1.82 | $1.00 | $2.82 | 6.42 bp | 111.9 bp | 69.8 | 5.73% |
| M2K | $10,229 | $1.82 | $1.00 | $2.82 | 11.03 bp | 175.5 bp | 63.7 | 6.28% |
| MCL | $7,676 | $2.12 | $2.00 | $4.12 | 21.47 bp | 268.4 bp | 50.0 | 8.00% |

**Cross-checks that passed:** MCL 21.47 bp reproduces the ledger's recorded 5.3423 bp/RT × 4 = 21.37 bp; the sourced $1.82 index-micro RT reproduces the 2026-07-10 verification independently.

Three properties worth carrying forward:

1. **Ranking is notional-driven.** RT is identical ($2.82) across the index micros; MNQ wins purely on notional.
2. **MGC's penalty is slip, not commission.** Its commission is 16% above the index micros, but its **$1.00 tick value doubles slip** ($2.00 vs $1.00 RT) — slip is 49% of MGC's total RT. A passive entry would cut required capture 5.25% → ~3.97%. ⚠ Not free: [`Q-COSTGEO-3`](../../briefs/closures/Q-COSTGEO-3-closure-ambiguous-needs-depth.md) recorded add-liquidity as `NEEDS-DEPTH` (MYM add ≈12× displayed depth).
3. **The cost wall is a FREQUENCY wall, not an instrument wall.** MNQ required capture: 2.27% @1/session → 13.65% @6/session. CON-2 ran ~6/day and died at 0.65× of the 4× law — arithmetically consistent.

### (b) The DSR floor is set by K, not n — verified

`floor_at_k` re-computed per trade-frequency across {0.5, 1, 2, 4}/day is **flat to ±0.005** (K=441 → 1.835/1.830/1.830/1.830), reproducing M-19 verbatim: *"The floor is set by K, not n (robust across trade-frequency 0.5–4/day; more data does not help)."* Trade frequency is a lever on **power**, not on the floor. Do not conflate.

### (c) MNQ-ANALOGUE-1 — designed, then killed at the pre-G0 cheap falsifier

Construct (train-only, 1,500 slots, 2 per full-26-bar RTH session at 09:30 / 12:45 ET): z-normalized 13-bar M15 log-return window; leave-one-out 1-NN over the train pool; trade `sign(neighbour's forward 13-bar return)`; H=13.

| Test | Measured | Disposition |
|---|---|---|
| Base rate P(F>0) | 0.5453 | — |
| **Analogue hit rate** | **0.5160** | **below base rate** |
| Mean signed return | **+0.837 bp** | always-long is **+1.606 bp** |
| Session-block 95% CI (2,000 resamples) | **[−3.274, +4.871] bp** | **straddles 0** |
| Momentum-relabel corr | +0.0348 | not a relabel — noise |
| σ₁₃ (unstopped) | 84.36 bp = $220.13 | — |

**The kill, stated plainly:** the 4× cost law requires **3.64 bp/trade**. The construct grosses **0.837 bp** — **0.23×**, and below a *single* round trip (0.91 bp). It is net-negative before the 4× law applies, and its direction rule is *less* accurate than always-long while capturing ~half the naive drift.

---

## §2 — Why it stands out

- **The feasible set was one cell wide before this kill, and is empty after it.** Under the N-SHAPE envelope (EM5 flat-by-16:00 + micro-expressible; EM3 hard stops), the only cell whose implied annSR at 4×RT landed inside [floor 0.850, Cap 1.00] was MNQ RTH H=13 at **0.87**. MGC's best legal cell needs **1.15** (over Cap); MYM carries `venue_tradable: false`; M2K is dominated and index-barred; MCL has no callable commission row; 6J is the only bar-free tradable panel but needs **1.79** and fails EM5 micro-expressibility (no micro JPY exists at Tradeify) and N-SIZE (σ $498/trade vs a $3,000 rope).

  > ⚠ **APPENDED CORRECTION 2026-08-15 (same day, operator-raised).** An earlier phrasing of the 6J line glossed 1.79 as *"98% of the estate's best-ever measured edge (1.83)"*, using Aegis as a reachability ceiling. **That gloss is withdrawn.** Per [M-19](../../methodology/lessons/methodology_lessons.md) a floor must be benchmarked against **both** the best in-house edge (1.83) **and** the corrected published top-decile Sharpe (**S_B 0.85**), and is dead only when it exceeds *both*. Aegis 1.83 is cohort-bound (USDJPY · 15m · Pepperstone CFD), **K-undeclared** and **un-deflated**, so it is not placeable on the DSR axis and cannot bound a novel candidate. **The dispositions above are unaffected** — every one of them rests on Cap 1.00, venue legality, EM5, or N-SIZE, none of which involve the 1.83 comparison. Full correction and the relocated constraint: [channel ADR K-cap addendum](../../adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md); counterfactual opened as [`Q-CAPBAND-1`](../../briefs/Q-CAPBAND-1-cap-band-counterfactual.md).
- **An earlier same-session reading recommended MGC and was wrong.** It priced cost geometry correctly but had not applied the N-SHAPE envelope, which forces RTH-aligned holding tiles and pushes MGC's legal cell over Cap. Recorded so the superseded reading is not re-derived.
- **DISC-CAMP-0 already ran the wide mine this channel might otherwise repeat.** GC 1h, K=3,177, `catch22(22) + STUMPY m={30,60,90} + ruptures PELT(1)`: all six motif/discord candidates at p=1.0000, all cost-law FAIL, mean net −2.19 to −0.40 bp. Its ruptures face found **1 segment / 0 breaks** and its closure pre-warns that *"a future campaign reusing this frozen penalty on a different instrument/window should not be surprised by a similarly degenerate segmentation."*

---

## §3 — Operator ruling recorded (2026-08-15)

**Route ①/CON-5 pause — ruled "new modality, proceed."** The operator ruled that a 1-NN analogue forecaster (algorithmic pattern-matching with **no named entry geometry**) is a genuinely different modality from the paused θ-parameterised entry-geometry lane (CON-1…CON-5: compression→break, PDH/PDL, VWAP reclaim), which lifts the CON-5 pause on its own stated terms (*"pending a new modality or non-route-① thesis"*), and that a geometry-sourced direction rule sits outside the mapped price / instrument-selection / hold-time levers.

**This ruling stands even though the construct it authorized is dead** — it is a precedent about the modality class, not about MNQ-ANALOGUE-1. Its own carrying artifact is [`ADR 2026-08-15 new-modality route ruling`](../../adr/2026-08-15-analogue-modality-route-ruling.md).

**Route ③ was explicitly NOT used** and is arithmetically false on both limbs: the incumbent's DSR on the Tradeify basis is 0.9644 vs this channel's 0.950 floor, and on the headline basis +0.890 vs the 0.850 floor, with `ops/instruments/NQ.md:49` stating "no basis is privileged."

---

## §4 — Disposition of the kill (typed, and a definitional gap this exposes)

**This is a pre-G0 cheap-falsifier kill at $0/K=0 — no manifest opened, no Q-ID spent** — matching the 2026-08-10 dense-1m cell #3 precedent ("no G0 authored, no Q-ID spent").

⚠ **Definitional gap in the channel ADR's §4, surfaced by this kill.** §4 defines `FALSIFIED` as "≥1 candidate reaches **battery-closure** and zero survive", and battery-closure as death at *"cost-law UNREACHABLE, K-cap FAIL, DSR FAIL, or own-series split FAIL"*; `AMBIGUOUS-HOLD` is "zero candidates **sourced** at all." MNQ-ANALOGUE-1 was sourced and died at a pre-registration cheap falsifier that is **none of the four named stages** — so it is neither branch as written.

> ✅ **RULED 2026-08-15 (JA), same day — [`ADR pre-G0 addendum`](../../adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md#addendum-2026-08-15--a-pre-g0-kill-is-not-a-4-strike).** A pre-G0 cheap-falsifier kill (no manifest, no Q-ID) is **not** a §4 strike; the boundary is `register_search open`. Ratified alongside: every pre-G0 kill is **counted and disclosed** with each §4 reading, so "the falsifier never fired" cannot be read as "the channel was productive." Running count: **1**. The addendum names the falsifier-weakening exposure this creates and leaves a consecutive-pre-G0-kill threshold as an explicitly uncovered operator item. This Notice's original "not adjudicated" text above is the state at authoring, retained per forward-only discipline.

---

## §5 — Forbidden moves (this notice)

- Re-running MNQ-ANALOGUE-1 with a different `m`, `H`, `k`, slot pair, or stop — that is θ-retune of a construct whose *information content* was measured at zero, not a cost-geometry problem.
- Reading the (a) cost table as an edge estimate. It compares cost to **range**, never to edge — the exact conflation `ops/instruments/M2K.md` WITHDREW ("it compared the hurdle to the price *range*, not the *edge*").
- Treating the §3 ruling as un-pausing the dense-1m OHLCV temporal-selectivity lane generally. It is scoped to the algorithmic-analogue modality class.
- Citing the superseded MGC recommendation from earlier this session (§2).
- Reusing DISC-CAMP-0's frozen ruptures PELT penalty (10.0) on a new panel without expecting degenerate segmentation.

---

## §6 — Gate

| Verdict | Trigger | This pass |
|---|---|---|
| `RESOLVED` (candidate found) | A K≤3 construct clears the cheap falsifiers and opens a manifest | — |
| `RESOLVED` (measured + killed) | Cost map computed; first candidate designed and killed pre-G0 at $0 | **fired** |
| `FALSIFIED` | A candidate is opened without its cheap falsifier, or a θ-retune revive is authored | — |

**Disposition:** channel feasible set **empty at $0**. The channel ADR's `AMBIGUOUS-HOLD` branch (2026-11-08) is now the live expectation absent a new modality, instrument, or paid-data route.

---

## §10 — Audit hooks

```bash
# The kill is recorded and no manifest was opened for it
ls discovery_manifests/ | grep -i analogue          # expect: no match
rg -n "MNQ-ANALOGUE-1" docs/ | head

# Cost figures reproduce (commission is primary-sourced, re-verify at the page)
python -c "import sys;sys.path.insert(0,'lab');sys.path.insert(0,'core');from discovery.cost_model import bp_hurdle;print(bp_hurdle('MNQ',firm_key='Tradeify_Select_100K',price=15472.5,slip_ticks=1.0,slip_convention='per_side').hurdle_4x_bp)"
# expect ~3.645

# floor_at_k is K-driven, not n-driven (M-19)
python -c "import sys;sys.path.insert(0,'lab');from research_utils.axis_screen import floor_at_k;print([floor_at_k(k) for k in (1,2,3,441)])"
# expect [0.65, 0.85, 0.98, 1.83]

# The §4 definitional gap is still open (or discharged by a dated addendum)
rg -n "battery-closure" docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md
```

---

## Verification

```bash
python scripts/check_brief.py docs/notes/notice/N-2026-08-15-blind-channel-cost-geometry-and-first-candidate-kill.md --type notice
```
