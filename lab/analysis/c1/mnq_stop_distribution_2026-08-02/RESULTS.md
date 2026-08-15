**Theme:** c1
**Status:** ACTIVE — MNQ stop distribution vs qty≥1 floor — Monday window realism
# MNQ stop distribution vs the qty≥1 floor — is Monday's MNQ window a real shot?

> ## ⚠ READ [ADDENDUM c](#addendum-2026-08-02c--the-6082-discrepancy-is-resolved-and-it-resolves-against-this-analysis) FIRST — §2 AND §4 ARE SUPERSEDED
>
> This analysis's estimator (median realized loss on stop-outs) was later shown to be the **weaker
> instrument**: it is conditioned on the adverse outcome, trail-truncated, and disagrees with the
> sizing spec's own acceptance-test oracle with **no consistent sign** (0.75×–1.63×). **The "~4 in 5"
> figure in §2/§4 is WITHDRAWN.** Use the oracle instead — MNQ recent-90d `sl_pts` **54.61** against a
> 92.5 cliff (**37.9 pts of headroom**), MYM **60.82** against 87.5. Body kept unedited as the record
> of how the wrong instrument was built and caught.

**Date:** 2026-08-02. **Trigger:** operator — *"measure the MNQ stop distribution against the 92.5
threshold"*, arising from *"I do not want to lock M1 to Striker MYM specifically."* Item 5 needs a
real TV strategy entry at **non-zero** sizing; MNQ is the leg with a Monday window. Read-only over
committed/gitignored TV exports. **No K spend, nothing armed, $0, no gate moved.**

## §0 — The floor, re-derived rather than quoted

`qty = min(floor(185 / (2 × stop_pts)), reserve_cap=1)`, so **`qty ≥ 1` ⟺ `stop_pts ≤ 92.5`** at the
deployed WATCH-1 0.50× rung (**≤ 37.0** if DD-scaled 0.40×). Inputs: `r_eff 0.00185 × $100,000 =
$185` (07-28 ledger), MNQ **$2/point** (independently confirmed — the export's `Size (value)` =
`qty × price × 2`), `reserve_cap = floor(11 / (1 + 1000%)) = 1`.

**Ground truth, n=1** — the only real MNQ payload ever observed at the rail (2026-07-28):
`stop_dist_pts 126.75` at `close 28051.5` = **0.4518% of price** → `qty_out = 0`.

## §1 — Method, and the one thing that would have made this wrong

The exports do **not** carry `stop_dist_pts` (that is a Pine alert field, `close − currentStop`), so
the stop is recovered from realized trades: a passive **"Exit Long" at a loss is a stop-out**, and
`entry − exit` is then the stop distance. Panels: `Striker_NAS100_v1_CME_MINI_MNQ1!` (n=237 base
entries, 2020-01→2026-06) and the venue-native `Striker_NAS100_MNQ` edition (n=37, 2025-09→2026-07).
The FUTURES_LOCK confirms exit constants are **byte-carried** between editions, so both are valid
for stop behaviour.

⚠ **The trap that dominates this measurement: the threshold is ABSOLUTE, the stop is PROPORTIONAL.**
MNQ ran ~10,300 → ~29,600 over the panel. Naively, **97.3%** of historical stop-outs are under 92.5
points — but that is almost entirely because *price was lower*, not because the stop was tight. The
decision statistic is **stop-as-%-of-price, projected onto today's level.** At MNQ 29,600 the
threshold is **0.3125% of price**; at 28,000 it is 0.3304%.

**Estimator validated, not assumed.** For genuine stop-outs, MAE should equal `entry − exit`. It
does: median discrepancy **0.0%** (v1 panel) and **2.8%** (MNQ edition). So the stop-out distance
*is* the stop, and the trailing-bias worry does not materially contaminate this subset.

## §2 — Results

| Panel | n base | stop-outs | median stop | p90 | max | **qualify @ 29,600** |
|---|---|---|---|---|---|---|
| v1 on MNQ1! (2020–26) | 237 | 111 | **0.220%** | 0.437% | 3.315% | **76.6%** |
| MNQ edition (2025-09+) | 37 | 19 | **0.161%** | 0.286% | 0.343% | **94.7%** |
| **Pooled** | 274 | 130 | **0.217%** | — | — | **79.2%** |

**The median stop is 0.69× the threshold** at MNQ 29,600 — comfortably inside it.

**Hard lower bound on the disqualifying side.** A trade that did *not* stop out but ran an adverse
excursion of X **proves** its stop exceeded X, with no assumption about the stop's form. Only
**6–7 of 237 (2.5–3.0%)** and **1 of 37 (2.7%)** base entries provably had a stop above the
current-price threshold. So the wide-stop tail is genuinely thin.

## §3 — The finding that qualifies the answer: the one live reading contradicts the backtest

The single observed live payload — **0.4518%** — sits **above the MNQ edition's measured maximum
(0.343%)** and above the 6-year panel's **p90 (0.437%)**. On the backtest distribution it is a tail
event; it is also 100% of our live evidence.

**The likely explanation is already a known, still-unmeasured gap in this repo: mid-bar ATR.** The
alert fires **intra-bar**, so `currentStop` is computed from a *forming* bar, while the backtest
scores **closed** bars. The RUNBOOK records exactly this mechanism — *"a bad mid-bar ATR cannot
over-size it, only under-size it (7, or 0)"* — and the **§2b clean mid-bar re-measurement is still
owed** (it needs a real entry, and none has come).

**Consequence: the backtest distribution in §2 may systematically understate the live stop**, and by
an amount nobody has measured. The 79–95% qualifying fractions are therefore an **upper** estimate of
Monday's odds, not a calibrated probability.

## §4 — Verdict

**Monday's MNQ window is a reasonable shot, not a long shot — but do not count on it, and do not
treat a `qty_out=0` as a defect.**

- ~~On backtest evidence, roughly **4 in 5** MNQ base entries (and ~19 in 20 on the recent
  venue-native edition) would size to `qty ≥ 1`.~~ **WITHDRAWN — see Addendum c.** The oracle's
  answer: at the recent-90d median stop (**54.61 pts**) MNQ sizes to **qty 1** with **37.9 pts of
  headroom** before the 92.5 cliff.
- Against that, the **only live reading we have floored to zero**, and the mid-bar effect that would
  explain it is unmeasured.
- **If DD-scaling is active (0.40×) the threshold collapses to 37 points** — below the median stop on
  both panels — so a DD-scaled MNQ entry is very unlikely to size non-zero. Check DD state before
  counting the session.
- A zero-floor is **silent**: it produces a complete ledger triad with `qty_out=0` (exactly the
  07-28 event). It must be checked *in* the window, not inferred after.

**This measurement changes no gate and authorizes nothing.** It says only that running Stage 1
unarmed on Monday's MNQ window is worth doing, and that MYM's Tuesday window remains the higher-
probability path for item 5 (MYM is hard-capped at 8 and reaches qty 0 only at absurd stops).

## Reproduction

```bash
python lab/analysis/mnq_stop_distribution_2026-08-02/mnq_stops.py
```

Inputs are **gitignored vendor exports** in the primary tree
(`core/data/tv_exports/cme/`); the script reads them by absolute path and prints a
`MISSING` line rather than failing if they are absent. Deterministic — no sampling.

---

## Addendum 2026-08-02b — MYM measured the same way; the asymmetry is the finding

Extended to MYM on operator direction (*"prepare the Tuesday card the same way"*). Same harness,
same estimator, same validation. MYM: `reserve_cap = ⌊69/(1+750%)⌋ = **8**`, **$0.50/pt** (verified
identically), risk **$350** ⇒ qty holds at 8 while **stop ≤ 87.5 pts**.

| | MYM | MNQ |
|---|---|---|
| `reserve_cap` | **8** | **1** |
| Cap holds while stop ≤ | 87.5 pts | 92.5 pts |
| Just above, qty → | **7** | **0** |
| At the **worst measured** stop | **2** | **0** |
| Median stop | 74 pts (n=69, 2020–26) · 90 pts (n=8, recent) | ≈64 pts equiv. |
| Sizes at cap, current price | **~44%** | **~79%** |
| MAE-vs-(entry−exit) consistency | 0.0% / 2.4% | 0.0% / 2.8% |

**The finding is the asymmetry, and it inverts the naive read.** MNQ sizes at cap *more often*
(79% vs 44%) — but **MYM cannot floor to zero at any stop this book has ever produced**: at the worst
measured stop (0.5401% ≈ 254 pts) MYM still yields qty **2**. MNQ's downside is **no entry at all**,
so **no item-5 evidence**; MYM's downside is **7 instead of 8** — still non-zero, still valid.

So the correct operational statement is not *"MYM sizes better"* (it doesn't) but **"MYM cannot fail
in the way that matters."** That is why MYM stays the target leg and MNQ is a genuine but
coin-flip-shaped second path.

## Addendum 2026-08-02c — the 60.82 discrepancy is RESOLVED, and it resolves AGAINST this analysis

**Verdict: 60.8201 is correct, correctly labelled, and better-sourced than my estimator. The
"7 or 8" correction I proposed for the 08-04 desk card is WITHDRAWN.**

**What 60.8201 actually is.** Traced through the corpus to
[`lab/analysis/q_rail_1_2026-07/f2_floors.json`](../q_rail_1_2026-07/f2_floors.json), the Q-RAIL-1 F2
oracle that `docs/spec/c1_nt8_sizing_host_impl.md` §7 names as its acceptance-test oracle. Its
`method` field is explicit:

> `roll-seam-masked RMA ATR(11)×1.20; floor=(sl*$/pt)/risk%; WATCH-1=0.50× risk`

and its MYM `recent_90d` block reads `atr_median_pts 50.6834` → `sl_pts 60.8201`
(**50.6834 × 1.20 = 60.8201**), over **141,446** masked bars. So it **is** a recent-90d median — of
**ATR**, pushed through the Pine stop construction. The desk card's label was accurate.

**Why my number differed, and why mine is the weaker instrument.** The two estimators answer
different questions:

| | f2 oracle | this analysis |
|---|---|---|
| Measures | stop implied by the **median ATR bar** | median **realized loss on stop-outs** |
| Sample | 141,446 bars | 8–111 trades |
| Conditioning | none | **conditioned on the adverse outcome** |
| Biases | direct computation of the Pine formula | trail pulls **down**, volatility-selection pulls **up** |

Stop-outs are not a random sample of entries — a trade stops out precisely when the market moved
against it, which selects high-volatility bars; and the trail truncates realized loss below the
initial stop. **Two opposing biases, on small samples.** The evidence that this is fatal rather than
correctable is the ratio table:

| Leg | Window | f2 `sl_pts` | my stop-out median | ratio |
|---|---|---|---|---|
| MYM | full | 45.28 | 74.0 | **1.63×** |
| MYM | recent | 60.82 | 90.0 | **1.48×** |
| MNQ | full | 28.84 | 34.25 | **1.19×** |
| MNQ | recent | 54.61 | 41.0 | **0.75×** |

**The sign is not even consistent.** A clean selection effect would bias one way; this wanders from
0.75× to 1.63×. That is the signature of two competing biases on thin samples, not of a usable
estimator of the initial stop. **For "what stop will the next entry carry?", use f2. Not this.**

**What this analysis still contributes** — the oracle gives a point estimate and no spread, and two
things here survive:

1. **The tail is real and has already fired once.** The 07-28 live MNQ payload was **126.75 pts**
   against a recent-90d median of **54.61** — **2.3×**. That is an observed instance, not a modelled
   one, and it floored to `qty_out=0`.
2. **That 2.3× sharpens the mid-bar ATR hypothesis.** A mid-bar ATR read on a volatile *forming*
   bar plausibly runs ~2× the median *closed*-bar ATR, which is exactly the gap observed. The §2b
   clean re-measurement remains the way to settle it.

**Corrected expectations — from the oracle, at the deployed rung:**

| Leg | recent-90d `sl_pts` | ideal base | cap | **expected qty** | headroom to the cliff |
|---|---|---|---|---|---|
| MYM | 60.82 | 11.509 | 8 | **8** | drops to 7 above **87.5 pts** (26.7 pts) |
| MNQ | 54.61 | 1.694 | 1 | **1** | drops to 0 above **92.5 pts** (37.9 pts) |

Both legs size non-zero at the median, with real headroom. **The 08-04 card's "expect entry 8 / add
60" was right; the 08-03 card's "MNQ is a reasonable shot" was right for the wrong reason** — the
right reason is 37.9 pts of headroom at the oracle median, not a percentile of stop-out losses.

**Lesson (methodology).** I built an estimator from realized outcomes when a **direct computation of
the governing formula already existed in the repo**, then used the estimator to question the number
the formula produced. Search for the oracle before constructing a proxy — and when a proxy disagrees
with a direct computation, suspect the proxy first.

Exit-signal hygiene checked: MYM's panel separates `DD Limit` / `Max Hold` / `EOD Flat` from
`Exit Long`, and only `Exit Long` losses are counted — so forced-close exits do **not** inflate the
estimator. That check was sound; it just was not the binding problem.
