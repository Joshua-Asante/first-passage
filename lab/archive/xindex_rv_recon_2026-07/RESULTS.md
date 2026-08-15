# Cross-index relative-volume ranking — necessary-condition pre-screen RESULTS

**Thread:** 2026-07-21 prop-fundable-archetype deep-search, open question #3 — recover the Zarattini "Stocks in Play" cross-sectional ORB selection edge by ranking US equity-index futures (ES/NQ/YM/RTY) on opening relative volume and trading the ORB only on the most "in-play" index each day.
**Type:** cheapest-falsifier reconnaissance (Notice-phase, cached data, one pre-specified necessary condition, **no K bound**) — routes DROP / DEFER-procurement / GO; does not formally close a Pre-Q.
**Script:** [`run_probe.py`](run_probe.py) · **Data:** `core/data/bar_data/{MNQ,MYM}_M15.csv` (2020-07→2026-07, UTC).

**Verdict: FALSIFIED — DROP (lean): selection dilutes edge; strictly dominated by incumbent ORB-MNQ.**

---

## Verdict — **DROP (lean)**: the selection *dilutes* edge; strictly dominated by incumbent ORB-MNQ


The universe we hold intraday is **2 distinct indices** — Nasdaq (MNQ) and Dow (MYM), the widest-spread US large-cap pair. No ES or RTY intraday exists in cache (only daily ES). Tested on 1,534 common RTH sessions:

### (A) Dispersion — compressed but non-zero
| Metric | Value | Read |
|---|---|---|
| `corr(RV_nq, RV_ym)` | **0.717** | high — indices go in-play/quiet together |
| frac days RV within ±25% | **0.680** | most days a near-tie — ranking picks noise |

~28% independent variation exists, so there is *some* material — not the degenerate 0.95 that would kill it outright. Partial pass.

### (B) Predictiveness (higher-RV index, paired within-day) — **fails on the metric that matters**
| Test | Win rate | Mean diff | sign-p | |
|---|---|---|---|---|
| higher-RV → bigger \|move\| | 0.534 | +1.86 bp | 0.008 | faint in-play signal (significant, tiny) |
| **higher-RV → better ORB edge** | **0.487** | **+0.22 bp** | **0.329** | **null, slightly wrong-signed** |

The in-play index moves *more* but not more *predictably* — bigger range in both directions is whipsaw, not breakout edge. The core Stocks-in-Play claim (in-play → better directional follow-through) **does not fire across index futures.**

### Killer stat — the rotation is dominated by the incumbent
| Selection rule | Mean ORB edge |
|---|---|
| RV-rank selection (the thread) | **+2.64 bp** |
| alternating / random | +2.39 bp |
| **always trade MNQ alone (incumbent ORB-MNQ)** | **+5.19 bp** |
| always trade MYM alone | −0.35 bp |

RV-selection captures **half** the edge of always trading Nasdaq — because ~half the days RV says "trade Dow," and Dow ORB is ~zero. **The cross-index selection strictly dominated by the single-instrument ORB-MNQ we already run: the rotation dilutes, not concentrates.**

---

## Interpretation & disposition

**Mechanism corroborated on our own data:** index aggregation compresses the idiosyncratic dispersion that makes Stocks-in-Play work (1,000-stock cross-section → 4–6 co-moving broad baskets); a small-universe RV ranking harvests weak factor-rotation noise and picks the weaker index ~half the time. This is the deep-search's "no analogue for a lone index future," measured.

**Venue-wall specialization (load-bearing):** the *strong* documented intraday edge (Stocks-in-Play, Sharpe 2.8) needs a **single-stock cross-section the futures-prop venue cannot host** (futures-only) — same class as crypto-trend (venue-walled) and dispersion/short-vol (options-free venue). The recurring graveyard theme: the real edges need modalities/venues our automation-friendly futures-prop rail doesn't provide.

**Caveats (why "lean," not hard-falsified):** 2-index test, not the 4–6-way ES/NQ/YM/RTY the thread named; one RV definition (opening-30m / 14-session median, un-swept); one un-tuned first-break ORB. Adding **ES** would only add a *more homogeneous* instrument (it sits between Nasdaq and Dow). The sole thing that could add real dispersion is **RTY (small-cap)**, which decouples from large-caps — but it needs a real databento pull and the prior is now poor.

**Re-proposal / DEFER trigger:** a scoped **ES + RTY intraday pull** showing (i) small-cap idiosyncrasy raises cross-sectional RV dispersion AND (ii) higher-RV then predicts a *better* ORB edge (the (B) limb that failed here). DEFER-procurement, poor prior — NOT an RV-window / ORB / 2-index re-tune (exhausted moves); ES-alone inadmissible.

Reproduce:

```bash
python lab/archive/xindex_rv_recon_2026-07/run_probe.py
```
