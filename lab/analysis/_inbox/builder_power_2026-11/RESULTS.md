# Builder whole-stack power calibration: results

One-liner: research input only (K = 0, synthetic). 5c binds at realistic Sharpe. The 5e timing placebo is unreachable on synthetic breakout bars (look-ahead through the realised side). 5g placement rarely clears at latent book correlation 0.3. The whole stack sits 0.1–0.3 below the 5f closed form.

- **Design:** [DESIGN.md](DESIGN.md), frozen at `f5bd556` before any run.
- **Engine:** `main` at `8745b40`, where 5g runs after the holdout as placement (branch B, #1054). Engine sha256 is in each results JSON's `meta`.
- **Engine change after the run:** `31d719f` (no-book placement is `not_evaluated`; the pinned book sha256 is recorded) leaves every measured rule unchanged. The series layer always supplies a book, and the bar layer uses no placement. The harness passes the new `book_sha256` argument.
- **Data:** synthetic only; no vendor, private or real-strategy input was read.
- **Runs:** cloud container, `python -I scripts/fp.py python …`, Python 3.13.18, 4 processes.
  - Series layer: 84 cells in 1,153 s ([`results_series.json`](results_series.json)).
  - Bar layer: 4 cells plus calibration in 1,516 s ([`results_bar.json`](results_bar.json)).
- **VM:** no run was needed.

## Validity

- **V1 passes.** In the series layer, with normal payoffs at q = 0.85, the measured standalone 5f rate stays within 0.034 of `gates.reachability`'s closed form in every (S, n, K) cell, and no cell is outside tolerance. The harness reproduces 5f.
- **V2 misses at S = 0 in the bar layer.**
  - With zero planted drift, the card's net annual Sharpe is **0.68** (SE 0.05), not 0. That row is labelled 0.68, as the design requires. Drift was not re-tuned.
  - Cause: the generator's highs and lows are short wicks beyond the open and close. A bar that touches the breakout level therefore usually closes beyond it, and a stop entry filled at the level starts in profit (+1.39 points on average by that bar's close). Stop exits gain the same way (2.0 points better than the bar's close).
  - On a continuous-path walk both would average zero, so this is a generator artefact, not an engine finding.
  - Targets 0.85 and 1.5 were reached as 0.80 and 1.52 (both within ±0.10).

## Series layer: whole-stack pass probability

The stack here is 5a → 5c → 5f → stage-8 look. 5b is applied, not a gate; 5d and 5e need bars; 5g placement is reported separately. Each entry is the range across the six (trade rate q, payoff shape) cells, with 2,000 paths each. The holdout is a fixed 378 sessions.

| n (development sessions) | K | S = 0 (false pass) | 0.5 | 0.85 | 0.89 | 1.0 | 1.5 | 5f-only closed form at 0.85 / 0.89 |
|---|---|---|---|---|---|---|---|---|
| 1,510 (7.5 y) | 1 | 0.01–0.02 | 0.15–0.24 | 0.39–0.56 | 0.43–0.61 | 0.56–0.70 | 0.87–0.95 | 0.67 / 0.70 |
| 1,510 | 2 | 0.00–0.01 | 0.10–0.13 | 0.33–0.43 | 0.36–0.50 | 0.49–0.59 | 0.86–0.94 | 0.47 / 0.51 |
| 1,510 | 4 | 0.00 | 0.05–0.06 | 0.21–0.27 | 0.24–0.33 | 0.34–0.42 | 0.78–0.91 | 0.27 / 0.30 |
| 2,350 (10.8 y) | 1 | 0.01–0.03 | 0.14–0.31 | 0.46–0.70 | 0.50–0.76 | 0.63–0.83 | 0.92–0.98 | 0.83 / 0.86 |
| 2,350 | 2 | 0.00–0.01 | 0.12–0.21 | 0.44–0.63 | 0.48–0.68 | 0.61–0.79 | 0.92–0.98 | 0.67 / 0.71 |
| 2,350 | 4 | 0.00 | 0.07–0.11 | 0.35–0.47 | 0.40–0.53 | 0.53–0.68 | 0.91–0.97 | 0.46 / 0.51 |

Full per-cell tables come from `summarise.py series`.

**Reading.**
- The stack falls below the 5f closed form whenever 5f is not the only obstacle (K = 1–2). At K = 1, n = 1,510 and S = 0.89 it gives 0.43–0.61, against 0.70.
- At K = 4 the stack can sit slightly above the closed form for skewed or sparse cards. Positive skew lowers the exact DSR's denominator.
- The false-pass rate at S = 0 is 0.7–2.8% at K = 1 and at most 0.9% at K ≥ 2.

## Which gate binds (series layer; first-fail kill share)

The table counts kills at S = 0.85 and 0.89 across all cells and K.

| Gate | Kill share | Verdict |
|---|---|---|
| 5a (≥ 200 trades) | 0–0.029 | It binds only at q = 0.15 on 1,510 sessions, where a card averages about 227 trades. It **cannot fire** at q ≥ 0.40 or on 2,350 sessions, with 0 fails even at S = 0. |
| 5b | 0 by construction | It is applied, not a gate. It cannot fire and never binds. |
| **5c (PF ≥ 1.1 in each half)** | **0.10–0.53** | **This gate binds**: it has the largest share at K = 1–2 in every cell, and at K = 4 for q = 0.85. Its share **rises with trade frequency**: 0.10–0.28 at q = 0.15 and 0.37–0.53 at q = 0.85. A fixed per-trade PF hurdle is harder for frequent, thin-edge cards at the same Sharpe. It is also the main null killer, failing 86–99% of S = 0 cards. |
| 5f (DSR ≥ 0.95) | 0–0.44 | It binds at K = 4 when q = 0.15 (about 0.43 against 5c's 0.28) and ties with 5c at q = 0.40. Its standalone pass at K = 4 on 1,510 sessions and S = 0.89 is 0.29–0.40, so **5f is unreachable** at that K and window. |
| Stage-8 look (net > 0, PF ≥ 1.0) | 0.04–0.12 | It binds modestly. Standalone it passes about 0.85 at S = 0.85 and 0.47–0.52 at S = 0. |

## 5g placement (step 10, after a holdout pass)

The synthetic book is active on 90% of sessions with an annual Sharpe of 1.0, tied to the card through latent correlation ρ.

- **ρ = 0:** P(clear | stack pass) is 0.89–1.00. At S = 0, 48–52% of all paths clear (`mean_on_book_losing_days > 0` is a coin flip at zero edge).
- **ρ = 0.3** (q = 0.40, orb_skew):
  - P(clear | stack pass) is **0.000 at S = 0, 0.002–0.041 at S = 0.85 and 0.06–0.10 at S = 1.5**.
  - `shared_loss_share ≤ 0.50` sits just above the independence baseline. The book loses on about 47% of its active days, so even mild co-movement pushes a card's shared-loss share past 0.50.
  - **5g placement is unreachable** for a card whose losses co-move even mildly with the book.

## Bar layer: 5d and 5e through `compile.py`

The card is a two-sided MNQ 2-bar ORB with a range-opposite stop, flat at 15:45. Each cell has 200 paths, K = 1 in `evaluate` and 5f recomputed at K = 2 and 4. No trade was unresolved.

| True S (achieved) | n | 5c | 5d | 5e | 5f K=1 | Look | Stack K = 1 / 2 / 4 | Kill share 5c / 5d / 5e (K = 1) |
|---|---|---|---|---|---|---|---|---|
| 0.68 (V2 miss; target 0) | 1,510 | 0.35 | 0.61 | 0.07 | 0.57 | 0.77 | 0.010 / 0.010 / 0.010 | 0.65 / 0.14 / 0.20 |
| 0.80 | 1,510 | 0.47 | 0.67 | 0.016 | 0.71 | 0.88 | 0.005 / 0.005 / 0.005 | 0.53 / 0.16 / 0.31 |
| 1.52 | 1,510 | 0.89 | 0.71 | **0.000** | 0.99 | 0.98 | 0.000 / 0.000 / 0.000 | 0.11 / 0.26 / 0.64 |
| 0.80 | 2,350 | 0.50 | 0.59 | **0.000** | 0.86 | 0.83 | 0.000 / 0.000 / 0.000 | 0.51 / 0.21 / 0.29 |

The 5c to 5e columns give the pass rate among paths that reached the gate.

**5e is unreachable on this generator, and the cause is the placebo's design.**
- Each placebo run keeps the trade's realised side and hold, and redraws the entry bar uniformly from the day's live bars.
- A draw at or before the real breakout bar enters at a bar open inside the range, with the side the breakout later revealed, so it rides the move that chose the side.
- Diagnostic, one 1,510-session path, outside the frozen grid:
  - At zero drift, draws before the real entry make 23.7 points gross against 3.9 for the real trade.
  - Over all draws the placebo earns about what the card earns, so the beaten share comes out near 0.5–0.7, against a 0.95 threshold.
  - A post-breakout drift edge is captured by later draws too, so a stronger edge does not help: the pass rate is 0.000 at S = 1.52.
- The mechanism is generic to any breakout card scored with this placebo. Its size on real bars is **not** measured here.

**5d is calibrated only roughly.**
- It kills 14–26% and does not improve with S (0.61–0.71). The planted edge is keyed to exactly the card's 2-bar range, so the neighbours (n_bars = 1 and 3) inherit only part of it.
- The binding of 5d is therefore specific to this generator.

**Bar-layer whole stack:** at most 1% at every true Sharpe tested, almost entirely because of 5e.

## Reading limits

- Every process is stationary, with no regime change and no costs beyond the engine's own. Real cards will do worse in the 5c halves and the holdout.
- The series stack has no 5d or 5e, so it is an **upper bound**. On the bar evidence, 5e would cut it towards zero for breakout cards.
- The bar layer covers one card shape and one planted mechanism. Its generator's fill artefact (see V2) inflates the card's own P&L. That favours the card in 5e, so the true 5e pass rate on real bars may be lower still.
- None of this predicts a registered round, and none of it changes a gate, a threshold or a verdict.
