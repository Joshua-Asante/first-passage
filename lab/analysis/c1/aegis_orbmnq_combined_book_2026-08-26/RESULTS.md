# Aegis-6J1 x ORB-MNQ-1 combined book — Tradeify_Select_100K passability (2026-08-26)

> ⚠ **The original 1.51%/0.01% headline bust figures below are SUPERSEDED (2026-08-26b, further
> revised 2026-08-26c/d) — see §9, §10, AND §11.** A proper both-halves regime-robustness bootstrap
> and sizing/measurement corrections (§9.1-§9.5, §10.1-§10.3) revise the picture materially: the
> 1yr flagship fails outright and gets worse under every tested correction, and the 3yr flagship —
> the one cell §9 found survived its own both-halves check — now ALSO fails both halves once a
> tail-risk-consistent sizing ratio and a genuine timestamp-sequenced intraday-honest remeasure are
> compounded together (§10.2). No tested combined-book configuration in this entire campaign, on
> either window, survives a full both-halves + tail-sizing + intraday-honesty gate. Separately,
> §11 closes H4 (the one item §10 left open) with a clean, opposite-direction result on a different,
> solo-Aegis cell — a native 4-contract re-export confirms rather than erodes that cell's own
> originally-reported margin. Read §9, §10, and §11 before citing any number from §1-§8.

**Verdict:** FALSIFIED — no tested combined-book config survives
**Status:** ACTIVE — naive equal-risk Aegis-6J1+ORB-MNQ-1 combined book (each leg fails Tradeify solo, §0) — headline 1.51%/0.01% bust REVISED §9: 1yr fails a proper both-halves regime bootstrap (4.02%), 3yr fails once tail-consistent sizing + intraday-honesty compound (4.34%)
EXPLORATORY — not pre-registered, not lock-grade. A user-supplied-CSV sizing/bootstrap
sweep against this repo's own frozen engine, adversarially spot-checked (independent reimplementation
of the drawdown logic + correlation arithmetic), not a Rule-0 discovery campaign. Treat every figure
below as a **single-path replay or 5-day-block bootstrap over end-of-day equity only** — an EOD-clock
lower bound on true risk, per this repo's own standing posture (`CLAUDE.md`).

**Firm:** `Tradeify_Select_100K` (`core/firm_rules.py`) — $100K, 3.0% ($3,000) EOD trailing DD,
6% profit target, no daily-loss limit, 40% consistency rule, 8-mini/80-micro contract cap,
`dd_lock_offset_usd=1_000_000` (no eval-phase lock).

**Legs:** `Aegis-6J1 v3` (short-JPY mean-reversion, 6J futures) x `ORB-MNQ-1 v6` (long-Nasdaq
opening-range breakout, MNQ futures). Five TradingView "List of Trades" CSVs supplied by the
operator: Aegis 1yr + 3yr, ORB-MNQ 1yr + 3yr + a corrective 6yr export. Engine reused verbatim:
`core/mc/simulation.py::simulate_path`/`run_seed`, `core/mc/preflight.py::firm_kwargs` — no logic
reimplemented except where independently re-derived for adversarial verification.

**Headline finding — REVISED 2026-08-26d, read §9, §10, AND §11 before citing any number below.**
The original 1.51%/0.01% headline (naive equal-risk combined book, Aegis 5.33 : ORB-MNQ 0.29-0.40
contracts) does not survive closer testing, and neither corrected window survives full
compounding. A **proper both-halves regime-robustness bootstrap** (§9) found the 1yr flagship —
the number that looked *safest* — **fails outright**: its second half alone bootstraps to
**4.02% bust**, masked entirely by the pooled full-window figure; §10 finds every tested
correction (§9.2's tail-consistent sizing alone, a genuine timestamp-sequenced intraday-honest
remeasure alone, or both together) makes that second half worse still (4.06% / 5.13% / 5.25%).
§9 found the 3yr flagship **passes both halves at its original basis** (1.87% / 0.54%) — §10
finds it does **not** survive once §9.2's tail-risk-consistent sizing (5.333 Aegis : 0.5708
ORB-MNQ) and a genuine timestamp-sequenced intraday-honest remeasure (superseding §9.3's
trade-level MAE proxy, §10.1) are compounded and the bootstrap re-split by regime half:
**3.29% / 5.37% — both halves fail** (§10.2), reversing the one result §9 had established as
surviving. **Each leg still fails this same eval standalone** at realistic sizing (§0), and as of
§10 no tested combined configuration, at either window or any tried sizing, is a clean,
uncontested PASS under a full both-halves + tail-sizing + intraday-honesty gate. **Separately, §11
closes H4** (the one item §10 left open) with the opposite direction of result, on a different
cell: a native TradingView re-export at exactly 4 Aegis-6J1 contracts (operator-supplied)
reproduces the original linear-rescale bust figure exactly (2.77%, 0.00pp delta) — the
sizing-matched Aegis-6J1 SOLO cell's rescale-bias concern from §6 does not apply, confirmed rather
than eroded, though that solo cell still hasn't been checked against intraday-honesty (§11's own
closing note). See §9, §10, and §11 for the full picture.

---

## §0 — Correction to how this session's finding should be read (read first)

This is **not** "two viable Tradeify strategies." Prior, independently-measured repo record:

- **Aegis-6J1 fails Tradeify solo.** [`aegis_6j_trail_tradeify_2026-07-29/RESULTS.md`](../../aegis/aegis_6j_trail_tradeify_2026-07-29/RESULTS.md)
  (v0.3 panel) found it fails the 3.0% ceiling in every tested arm — best case 3.88% bust at
  roughly cap-8/half-size, full size 10.8-14.7%. This session's v3 panel reproduces that shape
  (§2 below): the sizing-matched cell clears at only 2.77% with a 0.23pp margin that does not
  survive this session's own rescale-bias correction (§6), and full-cap-8 fails outright at
  18.97%.
- **ORB-MNQ-1 fails payability at every `AUTOMATION_FRIENDLY_PROP_FIRMS` venue tested**, including
  Tradeify (T2, closed) and — as of the 2026-08-24 addendum to
  [`docs/pursuits/b3-orb-mnq-payability-line.md`](../../../../docs/pursuits/b3-orb-mnq-payability-line.md) —
  Bulenox/BluSky/MFFU (62-82% bust, 21-27x the ceiling). This session's own solo sweep (§2) finds
  the same instrument is *worse*, not safer, once the full 6-year panel is used: it busts on its
  own single realized path at every tested size over the full history.

What this session actually found is narrower and still genuinely new: **a specific small-weight
combination of the two failing legs** — where the equal-risk formula keeps ORB-MNQ's contribution
down to 0.18-0.40 contracts, a sliver, never a comparably-sized leg — **clears the ceiling in
bootstrap** at both tested windows. That is new payability/cost-geometry evidence at an admissible
venue (Tradeify), relevant to `b3`'s own re-entry clause ("new payability / cost-geometry evidence
at an admissible venue") — addendum filed there (§8 below). It says nothing about `b1`'s re-entry
clause (a live c1-rail seat opening), which this analysis does not touch, and it does **not**
resolve `STATE.md`'s queue item #1 (c1-rail Phase-B mechanism-supply — MES/FX lanes, an unrelated
track). Re-entry/renewal decisions on `b1`/`b3` remain an operator call.

---

## §1 — Data & reconciliation

Per-file headline metrics, as-backtested (no rescaling), commissions modelling Tradeify's real
per-side fees to the cent (`$3.10` 6J, `$0.91` MNQ, both matching `core/firm_rules.py`):

| File | Window | N | WR | PF | Net $ | Max DD $ | Commission/side |
|---|---|---|---|---|---|---|---|
| Aegis 1yr | 2025-08-26 -> 2026-08-05 | 32 | 78.13% | 7.459 | $10,962.55 | $1,248.40 | $3.10 |
| Aegis 3yr | 2022-09-07 -> 2025-08-20 | 90 | 63.33% | 2.832 | $22,758.15 | $1,399.20 | $3.10 |
| ORB-MNQ 1yr | 2025-08-26 -> 2026-05-01 | 109 | 64.22% | 1.623 | $11,308.24 | $2,444.48 | $0.91 |
| ORB-MNQ 3yr | 2022-08-25 -> 2025-08-26 | 770 | 61.17% | 1.566 | $66,708.20 | $6,389.20 | $0.91 |
| ORB-MNQ 6yr (corrective) | 2020-08-26 -> 2026-08-21 | 1,503 | - | - | - | - | $0.91 |

The 3yr pair overlaps cleanly. The original 1yr pair did not (ORB-MNQ stopped at 2026-05-01, 96
days short of Aegis's own end) — resolved below.

**Resolved: the ORB-MNQ 1yr/3yr "version discontinuity" was an incomplete export, not a strategy
toggle.** The 6yr export matches the old 3yr file on 766/769 overlapping trades, but the old file
was missing 129 trades (97% scale-in legs), concentrated in exactly the months that looked like
clean 0% scale-in blocks; the old 1yr file was missing 8 trades including a real losing stretch.
Corrected scale-in timeline (6yr, 2020-08-26 -> 2026-08-21): ON Aug-Nov 2020 (declining 50%->33%)
-> OFF Dec 2020-Apr 2022 (17mo, never covered by the old files) -> ON May 2022-Sep 2024 (mostly
33-50%) -> OFF Oct 2024-Feb 2025 -> ON Mar-Jun 2025 -> **OFF since Jul 2025, unbroken through this
file's Aug 2026 end** (two negligible ~5-7% trades Mar/Apr 2026). Whatever is running today has
not pyramided in over a year. Real, recurring, multi-month toggle — not two irreconcilable
versions.

---

## §2 — Solo sizing sweeps

### Aegis-6J1 standalone (3yr, bootstrapped bust rate, 10,000 paths)

| Sizing | Contracts | Bust rate | vs. 3.0% ceiling | vs. prior v0.3 study |
|---|---|---|---|---|
| Best-headroom cell | 2 | 0.00% | clears | improves 3.88pp, not sizing-matched |
| Sizing-matched to v0.3's cap-8 x 0.5x | 4 | 2.77% | clears, 0.23pp margin | improves 1.11pp, but this thin a margin does not survive §6 |
| Full cap-8, no haircut | 8 | 18.97% | **fails** | **worse** by 4.3-8.2pp than v0.3's own full-size range |

v3 is not uniformly safer than v0.3 — safer at low/matched sizing, worse at maximum sizing.
Different underlying trades; read the comparison as directional.

### ORB-MNQ standalone — single-path headroom is the wrong sizing guide

1yr window (pre-correction), single-path headroom vs. bootstrapped bust (2,000 sims x 5 seeds):
1 contract 1.84pp headroom -> 2.08% bust; 2 contracts 1.05pp headroom -> 22.1% bust; **8 contracts
2.96pp headroom (looks safest) -> 69.4% bust (is the most dangerous)**. 8 contracts hits the $6,000
target on realized day 8, before variance shows up; block-resampling the same weekly blocks exposes
that as luck.

**Corrected with the full 6yr export (the largest single revision in this analysis):**

| Window | Contracts | Single-path headroom | Old bust (incomplete data) | Corrected bust |
|---|---|---|---|---|
| 1yr, full & corrected | 1 | 1.83pp | 2.08% | **46.57%** |
| 1yr, full & corrected | 2 | 0.79pp | 22.1% | **66.91%** |
| 1yr, full & corrected | 8 | 2.96pp (largest) | 69.37% | **80.72%** |
| Full 6yr history | 1 | -0.28pp | n/a | busts on the realized path (day 54), before any bootstrap |

Cause: a newly-visible May-Aug 2026 stretch (invisible in the old file) — Net -$3,258/contract, 58%
WR but net losing, $4,642 per-contract drawdown (1.5x the entire $3,000 trail). Over the full 6yr
history, ORB-MNQ solo busts on its own single realized path at every tested size (1-8 contracts).
Cushion-proportional sizing does not cleanly rescue it: re-tested on the corrected 1yr window, it
made 1-contract drawdown *worse* (2.15% vs 1.17% flat, and failed to clear the profit target inside
the window) while helping at 2 contracts (1.74% vs 2.21%) — size-dependent, not a guaranteed rescue.
**The combined-book numbers in §3 still hold** only because equal-risk sizing keeps ORB-MNQ's
weight small enough (0.18-0.40 contracts) that its true risk barely registers in the mix.

---

## §3 — Combined book

### Naive equal-risk sizing — the headline result

Each leg's contract count set so its own single worst historical day contributes roughly equal
dollar risk (Aegis -$156 to -$175/contract vs. ORB-MNQ -$1,222 to -$3,195/contract, depending on
window):

| Window | Aegis | ORB-MNQ | Bust rate | Margin | Sample |
|---|---|---|---|---|---|
| 3-year (original, pre-correction) | 5.33 | 0.29 | 1.19% | 1.81pp | 154 weekly blocks |
| **3-year (corrected)** | 5.33 | 0.40 | **1.51%** | **1.49pp** | 154 weekly blocks |
| 1-year (original, truncated) | 5.33 | 0.68 | 0.01% | 2.99pp | 35 weekly blocks — thin |
| **1-year (corrected, full window)** | 5.33 | 0.18 | **0.01%** | **2.98pp** | 49 weekly blocks |

The corrected 3yr figure moves 1.19% -> 1.51% (still under ceiling); the corrected 1yr figure is
essentially unchanged despite running the full 247 days. Not because ORB-MNQ turned out safer — the
equal-risk formula automatically cuts ORB-MNQ's own weight (0.29->0.40 and 0.68->0.18 contracts) as
its true per-contract risk becomes visible, so the combined book's total exposure barely moves even
as the leg's own risk estimate roughly quadrupled. ORB-MNQ's contribution here is a sliver — 0.18
contracts is not a tradeable lot; it can only appear as a small overlay, never a comparably-sized
leg. The portfolio-level 1.5%/0.40x DD throttle never engaged across any of 12 flat-sizing cells
tested (single-path DD tops out at 1.44%).

**Account-cap consequence (confirmed, not hypothetical — see §8 H1/H9):** with 1 full-size 6J
adopted as 10 micro-equivalents (operator decision, §8), the 1.5x sizing row (Aegis=8.0 +
ORB-MNQ~1.0) totals **80.4-81.0 of the 80 micro-equivalent account-wide cap** in both windows — over
the cap. The 1.0x base pair that produces the headline numbers above is unaffected (53-54 of 80).

### Cushion-proportional sizing — inconclusive by construction

None of 12 tested cells (0.5x-1.5x, flat vs. cushion) busted on the single realized path — there
was no bust to rescue the book from, because the standalone Aegis bust figures above come from
block-bootstrap resampling, not one historical sequence. Isolated max-DD effect (single-path, 3yr):

| Pair | Aegis | ORB-MNQ | Flat max DD | Cushion max DD | Delta | Days-to-pass |
|---|---|---|---|---|---|---|
| 0.5x | 2.5 | 0.2 | 0.44% | 0.52% | +0.08pp (worse) | 214 -> 455 |
| 1.0x base | 5.0 | 0.4 | 0.88% | 0.64% | -0.24pp | 129 -> 148 |
| 1.5x | 7.5 | 0.6 | 1.32% | 0.95% | -0.37pp | 127 -> 131 |

Where it helps, ~25-28% relative max-DD reduction, paid for in up to +62 days to pass. The smallest
pair reverses (cushion sizing made DD worse, more than doubled days-to-pass) — size-dependent, not
a guaranteed rescue, matching this repo's own prior finding on the same mechanism.

### Mutual exclusion (don't trade ORB-MNQ while Aegis is open) — tested, does not help

Actual time-overlap between the legs is minimal (1yr: 17/165 ORB-MNQ trades, 10.3%, overlap an open
Aegis position, 0 would be blocked; 3yr: 78/886, 8.8%, 6 (0.68%, 1.8% of net) would be blocked).
Dropping those 6 overlapping-entry trades and re-running the base-pair bootstrap moved the 3yr bust
rate from 1.51% to **1.55%** — statistically identical, marginally worse (real edge lost, same
risk kept). At a "natural" non-equal-risk-crushed sizing (Aegis=2/ORB-MNQ=1), bust stays
29.6%/18.8% (1yr/3yr) with overlap allowed vs. -/19.3% with overlapping trades removed — both far
above the equal-risk pair's 0.01-1.51%. **The risk this book carries is per-contract dollar
volatility, not clock-time coincidence** — a bad ORB-MNQ trade an hour after Aegis closes hits the
same account floor just as hard. The one place mutual exclusion helps is the account-wide
contract-cap arithmetic (the legs are almost never open simultaneously, so a "defer to Aegis" rule
would in practice avoid breaching the shared cap even at larger sizes) — it does not touch the
$-drawdown economics that force ORB-MNQ's weight down.

---

## §4 — Correlation & diversification

Pearson r on daily per-contract P&L: **+0.06** (1yr), **-0.01** (3yr) — near-independent, as
expected from a short-JPY mean-reversion strategy vs. a long-Nasdaq breakout strategy. Joint
red-day co-occurrence tracks the independence prediction almost exactly (3yr: 8 actual vs. 8.9
expected). Re-checked against the corrected full-window ORB-MNQ data: r moves to +0.056 (1yr) /
-0.025 (3yr) — unchanged in sign and magnitude; correlation was never the part this data correction
touched.

| Sizing (Aegis/ORB-MNQ) | Window | Real | Independence null | Delta | Reading |
|---|---|---|---|---|---|
| 5/2 | 1yr | 6.3-6.8% | 8.7-9.0% | -2.1 to -2.3pp | real is safer |
| 5/2 | 3yr | 40.8-41.0% | 44.7-44.9% | -3.7 to -4.1pp | real is safer |
| 5/4 | 1yr | 44.6% | 43.0% | +1.55pp | real is **riskier** — flips |
| 5/4 | 3yr | 71.5% | 71.5% | -0.08pp | washes out — ORB-MNQ risk saturates |

Neither tested ratio (2.5:1 or 1.25:1) matches the headline combined book's own ~18:1 mix — whether
the flagship number benefits from this effect at all is unmeasured (H8). Echoes an unrelated prior
repo finding ([`Q-COMPOSE-1`](../../../../docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md)):
composing two legs pushed one leg's bust rate 2.65%->38.75% in a different pairing — a diversification
benefit must be measured at the exact sizing proposed, never assumed to transfer.

---

## §5 — Regime robustness

Splitting each leg's own 3yr history into equal thirds: no ORB-MNQ-style dead period for either leg
(every third positive net, PF>1) — but the window sits inside ORB-MNQ's own documented "alive"
2021+ regime and structurally cannot sample the dead 2019-2020 period recorded elsewhere in this
repo. Both legs share a softening signature: WR degrades in the most recent third while PF holds
(Aegis 72%->70%->50%; ORB-MNQ 62%->63%->54%).

A conservative combined pair (Aegis 2/ORB-MNQ 1) never busts starting from any of three points in
the 3yr window (full window, second-third, final-third) — but speed to clear the eval is highly
regime-dependent: 61 days from the start, 175 days from the second third, never (runs out the
window) from the final third. Single deterministic path per scenario, not bootstrapped — an
indication, not a robustness proof.

---

## §6 — Adversarial verification

Independent reviewer re-derived the drawdown logic from scratch (different code, no shared-simulator
import) and re-ran the correlation/sizing arithmetic cold: trailing-locking floor test matched
claimed pass/day/max-DD to within $0.13 across three cells including the boundary case; Pearson
correlation (pure-stdlib, no numpy/pandas) matched to within 0.000033; equal-risk ratios matched to
5+ significant figures; commission/DD-lock parameters checked directly against `core/firm_rules.py`
(confirmed current — the sweep used the corrected no-lock value). New check: a rough intraday-touch
sensitivity from each trade's own recorded adverse excursion — 0/82 trading days come close to the
DD floor at base sizing; 2/81 (2.5%) do at the largest sizing tested.

**Findings that don't survive their own caveats:**

- **Rescale bias is a range, not a point, and flips a cell.** The prior study cited "~0.4pp"
  linear-rescale optimism; it actually reports **0.37-0.61pp**. Applied to the sizing-matched Aegis
  cell (2.77% bust, 0.23pp margin), either end flips it to **~3.1-3.4% — a fail**. The flagship
  combined cell (1.51%/1.49pp 3yr) absorbs the same correction comfortably.
- **EOD-clock lower bound.** This repo's own standing posture treats every close-only bust figure
  as understated vs. Tradeify's actual intraday enforcement. The closest same-geometry repo data
  point moved a comparably-thin cell from 0.11% to 0.72% once measured honestly. Applied by analogy,
  the sizing-matched Aegis cell would fail outright; the flagship number's margin shrinks from a
  comfortable 1.81pp (pre-correction) to somewhere between "still fine" and "under real pressure."
  **Not addressed in the sizing sweeps themselves** — see H2/H3 below.

Also flagged: the inferred 6-contract Aegis cap is load-bearing for nearly every combined-book cell
(now resolved, §8 H1); the excluded 1yr Aegis tail was weak, echoing the regime-softening signal in
§5 (now resolved, §8 H6); the cushion-sizing and regime-robustness sections both drew conclusions
from single-path replay alone — the exact diagnostic §2's own ORB-MNQ sweep proved unreliable.

---

## §7 — Would a third leg help? (synthetic-leg sensitivity)

A synthetic "leg C" was built by circularly shifting an *existing* leg's own daily P&L in time —
preserves its real risk/return distribution (mean, vol, tail, streakiness) while destroying
correlation with the rest of the book (confirmed r ~ 0.02-0.11 against both real legs). Baseline
(2-leg, 3yr window): 1.51% bust.

| Leg C profile | Contracts | Bust rate | vs. 1.51% baseline |
|---|---|---|---|
| Aegis-like (small-tail, ~$150-250/contract DD) | 1 | 1.06% | better |
| Aegis-like | 2 | 1.04% | best tested |
| Aegis-like | 4 | 1.81% | worse than baseline |
| Aegis-like | 8 | 7.63% | much worse |
| ORB-MNQ-like (large-tail, ~$1,200-3,200/contract DD) | 0.25 | 0.40% | better |
| ORB-MNQ-like | 0.5 | 1.22% | roughly neutral |
| ORB-MNQ-like | 1 | 12.54% | much worse |
| ORB-MNQ-like | 2 | 43.45% | catastrophic — busts the single realized path outright |

A genuinely good third leg has a **sweet spot, not a monotonic benefit**: 1-2 contracts of the
small-tail profile cuts bust ~30% relative, but by 4 contracts it's already worse than not adding
it, and by 8 far worse — every leg draws on the same shared $3,000 trail / 80-micro-equivalent
budget, so more legs is never free even when each is individually safe. A leg shaped like ORB-MNQ
is dangerous in anything but token size: the gap between "helps" (0.25 contracts) and "12.5% bust"
(1 contract) is half a contract.

**What a real third leg would need to look like:**

1. **Small per-contract dollar risk**, closer to Aegis's tail than ORB-MNQ's — dominates everything
   else, since a large-tail leg's safe zone is too thin to use in practice.
2. **Genuinely uncorrelated with *both* existing legs, ideally a different macro catalyst
   entirely.** Aegis (short JPY) and ORB-MNQ (long Nasdaq breakout) can both get hit by the same
   risk-off shock even with near-zero day-to-day correlation the rest of the time — a leg in
   commodities or a different session cuts shared-catalyst tail risk more than another rates- or
   equity-sensitive product would.
3. **Real, independently-validated edge**, not added merely for variance-averaging — this repo has
   already found elsewhere that composing legs can balloon bust rate rather than reduce it (§4).
4. **A genuine micro product** (1 micro-equivalent per contract), not another full-size-only
   instrument, so it doesn't burn the shared cap the way an additional full-size leg would.
5. **Sized deliberately, not maximized** — the tested sweet spot was 1-2 contracts, not 8.

One honest caveat: the base 2-leg book already clears the ceiling with real margin (1.51%,
1.49pp headroom), so the case for a third leg isn't "needed to survive" — it's "could buy back
margin the corrections in this report have eaten, or let the existing legs size less
conservatively." Synthetic-leg results quantify sensitivity only; they are not a backtest of any
real strategy and should not be read as evidence a specific instrument would deliver this profile.

### §7.1 — What instrument/mechanism actually comes closest (in-repo survey, 2026-08-26)

Checked this profile against the repo's own current instrument ledgers (`ops/instruments/`) and
discovery record. **Honest headline: nothing in the repo currently satisfies it, and the repo's own
very recent, very systematic search for a diversifying instrument has come up empty on every branch
tried in the last eight days:**

- **MGC (micro gold)** — the obvious macro-orthogonal pick (inflation/safe-haven vs. FX/equity) —
  is **hard-vetoed for `Tradeify_Select_100K` specifically**: 1 micro contract's necessary stop
  costs 6.7% of the $3,000 rope at 2022 gold volatility but **34% at 2026 volatility**; vol-scaled
  sizing tested NULL (implied qty stays 1.00-1.25 contracts every year, no gear below one micro).
  Operator-ratified closure 2026-08-25 ([`MGC.md` W5/G5](../../../../ops/instruments/MGC.md)).
- **6J itself** (same symbol Aegis already trades) — a fresh `orb-ny-breakout` mechanism was
  IS-real (PF 1.317, n=1,013, t+3.34, positive all 6 IS years) then **FALSIFIED on a
  pre-registered one-shot OOS read** (PF 0.846) — landed **2026-08-25**
  ([`6J.md` J16](../../../../ops/instruments/6J.md)).
- **M6A (micro AUD/USD)** — cost geometry clears (RT $2.60/contract, corrected;
  [`ops/instruments/M6A.md`](../../../../ops/instruments/M6A.md)) and a full deep-lane pre-registered
  campaign (`DL-2`, `prior-session-breakout-continuation`, the PDH/PDL family) ran against it — but
  **abandoned 2026-08-22**: all 10 frozen variants net-negative on train
  ([prereg](../../../../docs/briefs/pre-registration/2026-08-22-deep-lane-dl2-m6a-pdhpdl-prereg.md)),
  the second consecutive deep-lane abandonment after MGC's own DL-1.
- **MCL (micro WTI crude oil)** — genuinely macro-orthogonal (energy supply/demand vs. FX/equity),
  no documented granularity wall, geometry-cleared — but **mechanism-owed**: three attempts on
  record, all dead — `daily-range-state-persistence` (SIGNAL-GENERIC, canon-attributed volatility
  clustering, not a real mechanism), `pullback-failure-resumption` (FALSIFIED, N-ACT), a
  TAS-settlement construct (UNSCREENABLE — no admissible cohort δ exists)
  ([`MCL.md`](../../../../ops/instruments/MCL.md)).
- **USD/CAD up-spike fade** — the one place in the repo with an actually-*measured*, real (not
  SIGNAL-GENERIC) directional effect: real but **sub-cost and regime-fragile** (~0.03R/trade vs. a
  0.16-0.19R 4x hurdle; negative in the 2021 CAD-strength regime); tested on the retired Pepperstone
  CFD feed, not CME futures ([`lab/archive/usdcad_fade_2026-06-26/RESULTS.md`](../../../archive/usdcad_fade_2026-06-26/RESULTS.md)).
  Its own re-open bar: "a new mechanism (rate-diff/oil), not a new parameter" — genuinely closer to
  a real edge than anything else surveyed, just not yet clearing cost.

**Closest match, given the above:** **micro WTI crude oil (MCL)**, using the same design-box
discipline the repo already applies to MGC/M6A (rr in [2,3], hard structural stop, first-valid-signal-
per-session, no pyramiding) — genuinely macro-orthogonal to both legs, small-tail per-contract
economics (RT ~$4-5, no granularity wall on record), and not yet tried against the specific
`prior-session-breakout-continuation` (PDH/PDL) mechanism family that was just run — and killed —
on M6A. This is an elimination-based starting point for further (e.g. TradingView) iteration, **not
a validated candidate** — MCL has already produced three dead constructs on other mechanisms, and no
in-repo evidence supports an edge on the PDH/PDL family specifically. The USD/CAD fade is the
closest thing to an *actual measured edge* anywhere in this search, but needs a genuinely new
exogenous regime gate (rate-differential or oil-price conditioning) and a re-base from CFD to CME
futures before it clears cost — not a quick retune.

---

## §8 — Ranked open questions / hypotheses

Ranked by blast radius. H1/H5/H6/H9/H7/H8 are resolved; H2/H3/H10 are partially resolved (a
disclosed proxy, not ground truth — see §9); only H4 remains fully open, handed off in §9.4.

- **H1 (resolved, adopted).** The 6J contract cap was inferred by analogy (no verbatim Tradeify
  source for how a full-size currency future counts against the mini/micro cap). Confirmed
  verbatim from Tradeify's own "Trading Minis and Micros Together" page (operator screenshot,
  help.tradeify.co/en/articles/10495868): "10 micros = 1 mini," 80-micro account-wide cap — but
  that page's scope is minis/micros only and never names full-size-only instruments like 6J.
  **Operator-adopted working assumption** (not Tradeify-published): 1 full-size 6J = 1
  mini-equivalent = 10 micro-equivalents, so the 80-micro cap becomes an 8-contract cap for 6J.
- **H2 (partially resolved, §9.3).** A trade-level MAE-proxy intraday-honest remeasure (not the
  bar-level remeasure this hypothesis originally called for — that's handed off, §9.4) confirms
  the direction: the combined book's bootstrap bust rises under intraday-honesty (3yr flagship
  1.50%->2.39%). The specific solo sizing-matched Aegis cell this H originally named was not
  re-tested standalone in §9 (only the combined book was); still owed.
- **H3 (partially resolved, §9.3).** The flagship combined-book number does move materially under
  a (proxy, not bar-level) intraday-honest correction: 1.50%->2.39% at original sizing, and
  2.87%->4.34% (fails) once compounded with H7's sizing correction. Confirms this was a real risk,
  not "probably fine" — narrows the original ~1.8-7.7% uncertainty band to a concrete measurement,
  though still on proxy data pending §9.4.
- **H4 (open, handed off).** The rescale bias alone, with no clock correction, already fails the
  sizing-matched Aegis cell (§6). Needs a native TradingView export re-run at exactly 4 contracts —
  not computable without TradingView access; see §9.4.
- **H5 (resolved).** Answered by the 6yr export (§1): not two strategy versions, one strategy with
  a real recurring multi-month pyramid toggle; the old files' apparent "instantaneous transitions"
  were an artifact of 129 missing trades.
- **H6 (resolved).** Answered by the 6yr export (§1-§2): the previously-hidden May-Aug 2026 tail was
  worse than the 6 excluded Aegis trades alone suggested (-$3,258/contract ORB-MNQ losing stretch).
  The corrected combined-book bust rate is nonetheless still 0.01% (1yr) because ORB-MNQ's
  equal-risk weight is small enough (0.18 contracts) that even a real rough patch barely moves it.
- **H7 (resolved, §9.2 — material).** Both sizing ratios rested on a single historical worst day
  per leg. Recomputed from each leg's bootstrap-resampled 95th-percentile drawdown: 1yr basically
  unchanged (29.44:1, 0.18->0.1812 contracts), but 3yr shifts materially (9.34:1, 0.40->0.5708
  contracts) because Aegis's own bootstrapped tail risk is ~3x its single realized worst day. Bust
  at the corrected 3yr sizing: 2.87% (was 1.51%) — still clears 3.0% alone, fails once compounded
  with §9.3's intraday-honesty (4.34%).
- **H8 (resolved, §9.1).** Re-ran the real-vs-independence-null bootstrap at the actual flagship
  sizing (5.33-Aegis/0.40-ORB-MNQ, 3yr). Real is genuinely safer than the independence null
  (1.50% vs 4.34%, -2.84pp) — the correlation benefit holds at the sizing that matters, not just at
  the originally-tested proxies. 1yr: both near-zero, negligible either way.
- **H9 (confirmed).** Under the H1-adopted account-wide conversion rule, 8 full 6J contracts alone
  consume the entire 80-micro-equivalent budget. Both §3 "1.5x" rows total **80.4-81.0 of 80**
  micro-equivalents — genuinely over the cap. The headline 1.0x base pair (53-54 of 80) is
  unaffected. Practical note: a real deployment at the 1.5x ratio should cap that tier below
  Aegis=8 whenever ORB-MNQ is held alongside it.
- **H10 (partially resolved, §9.3).** Confirmed and quantified with a systematic (not "rough")
  trade-level MAE-proxy bootstrap, superseding the original single-path spot-check: the
  EOD-clock blind spot is real and material at the flagship sizing (3yr bootstrap bust +0.89pp
  intraday-honest, or +1.47pp compounded with H7). A genuine bar-level remeasure is still owed —
  see §9.4 — this proxy establishes direction and rough magnitude, not ground truth.
- **New (2026-08-26b, §9.5) — the both-halves regime-robustness gate, not previously run as a
  bootstrap, FAILS the 1yr flagship.** Its second half alone (2026-02-13→2026-08-05) bootstraps to
  4.02% bust, entirely masked by the pooled full-window 0.01% figure. The 3yr flagship clears both
  halves at its original basis. **This — not any of H1-H10 — is now the single largest open item**:
  the 1yr cell this report's own §3 table called the safer of the two windows should not be relied
  on without a halves-consistent remeasure.

---

## §9 — Follow-up (2026-08-26b): closing the analysis-readiness gaps

Addresses H2/H3/H7/H8/H10 directly (all four were "this analysis isn't decision-grade yet"
concerns, not structural/authorization gaps). H4 is handed off — see §9.4. Scripts:
[`followup_h7_h8_regime.py`](followup_h7_h8_regime.py),
[`followup_intraday_mae_proxy.py`](followup_intraday_mae_proxy.py); raw results:
[`data/followup_h7_h8_regime_results.json`](data/followup_h7_h8_regime_results.json),
[`data/followup_intraday_mae_proxy_results.json`](data/followup_intraday_mae_proxy_results.json).
**Uses the CORRECTED ORB-MNQ series throughout** (sliced from `orbmnq_6yr.json` to match each
Aegis window exactly) — the committed `orbmnq_1yr.json`/`orbmnq_3yr.json` files are the original
pre-H5/H6-correction data, kept only for the §1 reconciliation record. Reproduced the original
1.51%/0.01% headline from this corrected slicing before extending it (bit-exact to within bootstrap
seed noise) — the revision below is a genuine finding, not a data-basis artifact.

### §9.1 — H8: correlation benefit at the real flagship sizing (RESOLVED)

Re-ran the real-vs-independence-null bootstrap at the actual proposed sizing (5.33 Aegis :
0.40/0.18 ORB-MNQ), not the 2.5:1/1.25:1 proxies §4 originally tested.

| Window | Sizing | Real bust | Independence-null bust | Delta |
|---|---|---|---|---|
| 3yr | 5.33 / 0.40 | 1.50% | 4.34% | **-2.84pp — real is safer** |
| 1yr | 5.33 / 0.18 | 0.01% | 0.00% | +0.01pp — negligible, both near-zero |

The correlation-diversification benefit genuinely holds at the sizing that matters for the 3yr
window — it is not an artifact of testing the wrong ratio. This is the one correction in this
follow-up that does **not** erode the original finding.

### §9.2 — H7: sizing ratio from bootstrapped tail risk, not one worst day (RESOLVED — material)

Recomputed each leg's own tail drawdown via block-bootstrap (weekly blocks, same convention as the
engine's own resampling) and took the 95th percentile instead of the single historical worst day,
then re-derived the equal-risk ratio and re-ran the combined bootstrap at that sizing.

| Window | Aegis 95th-pct DD/contract | vs. single worst day | ORB-MNQ 95th-pct DD/contract | vs. single worst day | New ratio | ORB-MNQ contracts (H7 vs original) | Re-run bust |
|---|---|---|---|---|---|---|---|
| 1yr | -$192.90 | -$156.05 (1.24x) | -$5,678.29 | -$4,642.14 (1.22x) | 29.44:1 | 0.1812 vs 0.18 | 0.01% (unchanged) |
| 3yr | -$742.85 | -$249.70 (**2.98x**) | -$6,940.71 | -$3,313.08 (2.09x) | 9.34:1 | **0.5708 vs 0.40** | **2.87% (was 1.51%)** |

Aegis's own bootstrapped tail risk is proportionally far worse than its single realized worst day
(3yr: 3x, driven by its small trade count — 90 trades over 3 years gives resampling real room to
cluster unluckily). That shrinks the Aegis:ORB-MNQ gap and licenses materially more ORB-MNQ
(0.57 vs 0.40 contracts) under a tail-risk-consistent sizing rule — at the cost of the 3yr bust
rate nearly doubling, to 2.87% (0.13pp margin). Still technically clears the ceiling, but the
margin the original headline advertised (1.49pp) was real only under the single-worst-day
convention; it is a Trap-#13-shaped derivation issue this repo's own third-leg spec has already
named elsewhere ("only two (σ, bust) points exist; treat as a pre-screen, never a substitute for
the run") — here the ratio *is* being treated as more than a pre-screen. 1yr is essentially
unaffected (thin trade sample dominated by inactive days either way).

### §9.3 — H2/H3/H10: trade-level MAE-proxy intraday-honest remeasure (PARTIALLY RESOLVED)

**Not a true bar-level reconstruction.** The real `6J_M15.csv`/`MNQ_M15.csv` panels exist in this
repo's own provenance (`core/data/bar_data/SHA256SUMS`) but the bytes are gitignored vendor data
and are not present in this container ("usable but not regenerable" per that directory's own
README) — a genuine tick/bar-level remeasure needs those bytes or a fresh CME BAR EXPORT and is
handed off (§9.4), not attempted here. Instead: each trade's own recorded `mae_usd` (TradingView's
own per-trade adverse-excursion figure, already committed in `data/*_trades.csv`) is used to build
a disclosed, conservative per-day `intraday_low` series — same-leg same-day multi-trades (ORB-MNQ
pyramid scale-ins) take that day's single most-negative per-trade MAE, not a fabricated sum;
cross-leg same-day overlap (only ~9-10% of days, per §3's own mutual-exclusion finding) sums both
legs' worst-day MAE, the conservative assumption absent intraday timestamps. Fed into
`simulate_path`'s `intraday_low` / `run_seed`'s `intraday_blocks` — the same mechanism ORB-MNQ-1's
own W1/T2 studies used, reused verbatim, just built from a trade-level proxy instead of real bars.

| Config | Flat (EOD-only) bust | Intraday-honest (MAE-proxy) bust | Delta |
|---|---|---|---|
| 1yr flagship (5.33/0.18) | 0.01% | 0.11% | +0.10pp — still very safe |
| 3yr flagship (5.33/0.40) | 1.50% | **2.39%** | +0.89pp — margin shrinks 1.50pp -> 0.61pp |
| 3yr at H7-corrected sizing (5.33/0.5708) | 2.87% | **4.34%** | +1.47pp — **fails the 3.0% ceiling** |

The single-path outcome never changes (still `pass`, same day, same max-DD%) — the effect is
purely on the bootstrap tail, exactly where a lower-bound correction is expected to bite. The
compounded cell (H7 sizing + intraday-honesty together) is the first configuration in this entire
analysis to fail outright under a correction that is more rigorous than the original methodology,
not merely a sensitivity check. Given this is a proxy, not ground truth, read the direction (real
risk is understated by EOD-only bootstrap, worse at H7-consistent sizing) as the trustworthy part;
treat the exact magnitude as directional pending §9.4.

### §9.5 — Regime robustness: proper both-halves bootstrap (RESOLVED — the largest single finding)

Replaces §5's single-deterministic-path thirds check with a genuine both-halves block-bootstrap
per this repo's own methodology
([`docs/methodology/regime_robustness_gate.md`](../../../../docs/methodology/regime_robustness_gate.md)):
split the window in half, block-bootstrap **within each half independently** (never resampling
across the boundary), require the bust rate to stay low in **both** halves, not just pooled.

| Window | Sizing | Full-window bust (pooled) | H1 bust | H2 bust | Both halves clear 3.0%? |
|---|---|---|---|---|---|
| 1yr | 5.33/0.18 | 0.01% | 0.00% (2025-08-26→2026-02-13) | **4.02%** (2026-02-13→2026-08-05) | **NO** |
| 3yr | 5.33/0.40 | 1.50% | 1.87% (2022-09-07→2024-02-28) | 0.54% (2024-02-28→2025-08-20) | YES |

**The 1yr flagship — the number that looked safest in the entire report (0.01% bust, 2.98pp
margin) — fails the both-halves regime-robustness gate outright.** Its second half, which contains
the previously-hidden May-Aug 2026 ORB-MNQ rough patch (§2, H6), bootstraps to 4.02% bust entirely
on its own; the pooled full-window statistic hid this completely because the first half's 0.00%
swamps it in the blended figure. This is exactly the masking failure mode a both-halves gate exists
to catch, and it fired on the cell this report's own §3 table flagged as the safer of the two
windows. The 3yr flagship does clear both halves at its original (pre-§9.2/§9.3) basis — a real,
independently-confirmed result, not yet re-tested under the §9.2/§9.3 corrections in combination
(a further compounding check, not done here — see §9.4).

### §9.4 — What's left, handed off

Not computable in this container; next step for a local session with TradingView / real market-data
access:

1. **H4 — native TradingView re-export at exactly 4 Aegis contracts.** The rescale-bias correction
   (§6) needs a native re-run, not a linear rescale of the 8-contract data. No workaround exists —
   this needs an actual TV backtest export.
2. **A genuine bar-level intraday-honest remeasure**, superseding §9.3's trade-level MAE proxy —
   either restore the gitignored `6J_M15.csv`/`MNQ_M15.csv` bytes (repo provenance says they exist;
   this container doesn't have them) or pull a fresh CME BAR EXPORT for both instruments over the
   analysis windows, then thread real intrabar excursions through `intraday_low` the way this
   repo's own W1 ADR did for a different book.
3. **The 3yr both-halves gate re-tested under the §9.2 (H7 sizing) and §9.3 (intraday-honest)
   corrections in combination**, and the 1yr window's own H7/intraday sensitivity at its
   now-failing regime-split basis — neither compounding check was run here; §9.2-§9.3 only
   compounded on the 3yr window.
4. Given §9.5's finding, **the 1yr window should not be cited as the safer cell going forward**
   without a halves-consistent remeasure — the original report's own framing (§3: "the corrected
   1-year figure is essentially unchanged... [and] reassuring") is superseded by this section.

---

## §10 — Follow-up (2026-08-26c, local session): closing §9.4's handoff

Local-session follow-up to §9.4's three owed items. Reuses `combined_sim.py` throughout — no
barrier logic reimplemented; Task 3 reuses §9.2's own H7-derived sizing ratios and §9.5's own
both-halves split dates verbatim, not re-derived. Script:
[`followup_s10_bar_level_and_compounding.py`](followup_s10_bar_level_and_compounding.py); raw
results: [`data/followup_s10_bar_level_and_compounding_results.json`](data/followup_s10_bar_level_and_compounding_results.json)
(the 1yr fully-compounded cell in §10.3's last row:
[`data/followup_s10_1yr_both_corrections_combined.json`](data/followup_s10_1yr_both_corrections_combined.json)).

### §10.0 — Why timestamp-sequencing, not a literal bar-panel match (methodology)

§9.4 asked for a genuine bar-level (M15 OHLC) remeasure using `core/data/bar_data/6J_M15.csv` /
`MNQ_M15.csv`. This worktree's own copy was missing `6J_M15.csv` (present in a sibling worktree of
the same clone — gitignored files are per-worktree, not shared; copied across and sha256-verified
against `SHA256SUMS` before use). Two problems surfaced before a literal bar-match could be
executed as specified:

1. **6J's own committed M15 panel is 51.4% degenerate** (`O==H==L==C`, zero range) — a fine-tick
   (mintick 5e-7) 5-decimal-place rounding artifact, independently discovered the same day in an
   unrelated sibling session (memory `lesson_bar_export_ohlc_degenerate_fine_tick`; that session's
   own figure was 67% on a different sample of the same defect, same instrument). Recovered via
   that session's documented method (bar close = the raw export's own 7dp "Price USD" field;
   high/low from the adjacent synthetic trade's Favorable/Adverse excursion columns,
   direction-aware) from the raw `BAR_EXPORT_v0.2_CME_6J1!_2026-07-13_99781.csv` harness export —
   0% degenerate post-recovery, 0 bracket violations, median 9-tick range (externally consistent
   with that sibling session's own independently-measured figure for the same instrument).
   Recovery script: [`recover_6j_bars.py`](recover_6j_bars.py).
2. **The recovered panel does not align tick-for-tick with Aegis-6J1's own chart feed.** A
   spot-check against Aegis's own reported entry price at a matching timestamp showed a ~9-tick
   discrepancy — larger than that specific trade's entire recorded `mae_usd` (5.5 ticks). Aegis's
   own risk profile is tight enough (single-digit-tick MAE on most trades) that cross-feed
   alignment noise of this size would swamp the signal being measured. Using the bar panel for
   tick-level magnitude matching was rejected as LESS trustworthy than the strategy's own
   TradingView-computed `mae_usd`, not more — this repo's own standing posture is to prefer a
   disclosed, real number over a fabricated-precision one.

What made a genuine improvement possible instead: this is a **local session**, and the operator's
Downloads folder holds the **raw, un-reduced TradingView "List of Trades" exports** for both legs,
dated today (`Aegis_6J1_CME_6J1!_2026-08-26_{06813,073cd}.csv`,
`ORB-MNQ-1_recon_v2_CME_MINI_MNQ1!_2026-08-26_{857de,297a4,97090}.csv`) — confirmed to reproduce
the committed trade counts and windows exactly (90/32/1503, same 2022-09-07→2025-08-20 /
2025-08-26→2026-08-05 / 2020-08-26→2026-08-21 bounds) and, on a spot-check of trade 1 in each file,
exact per-trade net_pnl/mae/mfe/duration to the cent. Unlike the committed derived CSVs, these
carry each trade's real ENTRY timestamp, not just `exit_date`. That is the one genuinely new, real
ingredient available locally that the original cloud container didn't have: not finer price
resolution, but real trade-sequencing information.

**Confirmed first: every Aegis-6J1 trade (122/122 across both windows) and all but 3 of 1,503
ORB-MNQ-1 trades have `entry_date == exit_date`** — both legs are almost entirely same-session
intraday (this revises this session's own initial working assumption, made before the raw exports
were located, that Aegis might hold multi-day — it does not; Aegis's own multi-day count is 0/122).
The gap §9.3's proxy left open is therefore mostly about SAME-DAY sequencing and overlap
(including ORB-MNQ's own same-day pyramid scale-ins). The 3 genuinely multi-day ORB-MNQ trades
(2 of which fall inside the tested 3yr window) are a real, if tiny, exception: §9.3's proxy — and
an earlier draft of this section's own construction — attributed 100% of a multi-day trade's risk
to its exit day, which understates a multi-day hold's own interim exposure. The construction below
carries a multi-day trade across every day it spans; the correction is negligible in dollar terms
here (qty 2, ~$9-13/contract-scaled after sizing, against $1,000+ day floors) but is handled
correctly, not merely dismissed as absent.

**Construction** (sweep-line over real entry/exit timestamps, per day, both legs combined): process
each day's trades as timestamped open/close events, carrying any multi-day trade's own `mae`
across every day it spans; at EVERY event (open or close), the candidate day-floor = (realized P&L
of trades already closed so far) + (sum of `mae` of every trade currently open, including the one
in the event just processed) — concurrently-open trades are conservatively assumed capable of
hitting their own worst point simultaneously, a losing trade earlier in the day correctly lowers
the floor for a later, otherwise-unrelated trade (a real effect §9.3's single-MAE-per-day rule
missed), and checking at close events too catches trades whose own `net_pnl` realizes worse than
their own recorded `mae` (TradingView's Adverse Excursion field excludes exit-side commission;
Net PnL does not — observed on 6-11% of trades across both legs). The day's `intraday_low` = the
minimum candidate floor across the day's events. This is still a conservative worst-case
construction, not a literal reconstruction of what happened intraday (concurrently-open trades are
assumed capable of coinciding at their worst, which real price paths need not do) — but it is now
exact given each trade's own known entry/exit timing, mae, and net_pnl, and every window's
reconstruction was checked against the committed `daily_pnl` series before any bootstrap was run
and **matches to $0.00 exactly**, not approximately, in all six window/config combinations tested.

### §10.1 — Task 2: timestamp-sequenced intraday-honest remeasure (supersedes §9.3)

| Config | Flat (EOD) bust | §9.3 MAE-proxy bust | §10 timestamp-sequenced bust | Delta vs §9.3 proxy |
|---|---|---|---|---|
| 1yr flagship (5.333333/0.18) | 0.01% | 0.11% | **0.11%** | 0.00pp — exact agreement |
| 3yr flagship (5.333333/0.40) | 1.50% | 2.39% | **2.68%** | +0.29pp — more severe |
| 3yr at §9.2 H7 sizing (5.333333/0.5708) | 2.87% | 4.34% | **5.03%** | +0.69pp — more severe |

The 1yr result reproduces §9.3's proxy exactly — cross-validation, not coincidence, since the 1yr
window has few overlapping/pyramided days. The 3yr result is genuinely worse than the proxy found:
margin at original sizing shrinks from 1.50pp (proxy) to **0.32pp** (timestamp-sequenced); at
§9.2's tail-consistent sizing the cell fails by a wider margin than the proxy showed (5.03% vs
4.34%, both already over the 3.0% ceiling). On the 3yr window, 384 of the 538 days carrying any
intraday risk show a true floor below what the single worst per-trade MAE that day alone would
suggest — driven mostly by ORB-MNQ's own same-day pyramid scale-ins stacking exposure, not
primarily cross-leg overlap (§3's own mutual-exclusion finding already showed cross-leg overlap is
rare: 6-17 trades per window). None of this moved any reported bust-rate figure at the precision
shown — an initial version of the sweep-line construction (checking the floor only at trade-open
events, and bucketing every trade under its exit day) was adversarially reviewed before this
section was finalized and found to understate the floor on 8.4% of 3yr days by up to $16.53 (a
trade's own `net_pnl` can be worse than its own recorded `mae`, since TradingView's own Adverse
Excursion field excludes exit-side commission while Net PnL includes it) and to mis-attribute the
2 multi-day ORB-MNQ trades inside this window entirely to their exit day. Both are fixed in the
construction actually used (checks the floor at close events too; multi-day trades carry across
every day they span) — see the script's own docstring — but the fix moved no bootstrap figure at
2-decimal precision; it is recorded here because the review is part of this section's record, not
because it changed a conclusion.

### §10.2 — Task 3a: 3yr both-halves under §9.2 (H7 sizing) + §10.1 (intraday-honest) COMPOUNDED

| Basis | Full-window bust | h1 (22-09-07→24-02-28) | h2 (24-02-28→25-08-20) | Both halves clear 3.0%? |
|---|---|---|---|---|
| §9.5 original basis | 1.50% | 1.87% | 0.54% | **YES** |
| §10 H7 sizing + intraday-honest, compounded | 5.03% | **3.29%** | **5.37%** | **NO** |

§9.5 called the 3yr flagship's both-halves pass "a real, independently-confirmed result, not yet
re-tested under the §9.2/§9.3 corrections in combination" — this is that test, and **it reverses
the result**. The cell §9 spent its own analysis establishing as the one surviving,
both-halves-robust configuration fails BOTH halves once its own already-identified corrections
(tail-risk-consistent sizing, genuine intraday-honesty) are applied together and the bootstrap is
re-split by regime. Neither half is a near-miss — both sit well clear of the 3.0% ceiling in the
same direction.

### §10.3 — Task 3b: 1yr both-halves under each §9 correction alone, and combined

| Basis | Full-window bust | h1 (25-08-26→26-02-13) | h2 (26-02-13→26-08-05) | Both halves clear 3.0%? |
|---|---|---|---|---|
| §9.5 original basis | 0.01% | 0.00% | 4.02% | NO |
| §9.2 H7 sizing alone (0.1812 contracts) | 0.01% | 0.00% | 4.06% | NO |
| §10.1 intraday-honest alone (0.18 contracts) | 0.11% | 0.00% | 5.13% | NO |
| Both compounded (0.1812 contracts + intraday-honest) | 0.11% | 0.00% | **5.25%** | NO |

The 1yr window was already failing at its §9.5 original basis (§9.5's own headline finding); this
closes the one gap §9.4 flagged — neither correction had been tested on the 1yr window's own
regime-split. Both individually make the already-failing second half worse (4.02% → 4.06% / 5.13%
respectively), and together worse still (5.25%). The last row was not explicitly requested by the
handoff (which scoped 1yr to each correction alone, matching how §9.2/§9.3 were originally tested
separately) but was cheap to compute with the same code and closes the natural next question.

### §10.4 — What's still owed

Only one item from §9.4's list remained genuinely open at this point:

1. **H4 — native TradingView re-export at exactly 4 Aegis-6J1 contracts.** Not computable in this
   session up to here: this repo's standing policy prohibits automating TradingView login
   (`project_tv_egress_automation.md`), and no raw export found locally — including three dated
   today — is a fixed-4-contract run; all are variable-qty (4-8 contracts), position-sized,
   cap-8-style backtests matching the committed data's own basis, not the flat `max_contracts=4`
   configuration H4 needs. Requires operator action. **Resolved same day — see §11.**

Everything else §9.4 named is now resolved: the bar-level remeasure (§10.0-§10.1, in the
timestamp-sequenced form justified in §10.0, not a literal OHLC-bar match, for the reasons given
there), the 3yr both-halves-under-full-compounding check (§10.2), and the 1yr window's own
H7/intraday sensitivity at its regime-split basis (§10.3).

**Bottom line as of §10:** no tested configuration of this combined book — at either window, at any
sizing this campaign has tried — survives a full both-halves-regime + tail-risk-consistent-sizing +
intraday-honesty gate applied together. The 3yr flagship was the last cell standing after §9; §10
closes it. §11 (below) resolves H4, the one remaining open item, on a separate, solo-Aegis cell that
this both-halves finding does not touch.

---

## §11 — Follow-up (2026-08-26d): H4 closes — native re-export confirms the linear rescale exactly

Operator-supplied native TradingView export, provided directly to this session:
`Aegis_6J1_CME_6J1!_2026-08-26_c59e9.csv` — a genuine flat `max_contracts=4` backtest (every one of
154 trades has `Size (qty)==4`, not the variable 4-8 cap-8-style sizing behind the committed
`aegis_3yr_trades.csv`), spanning 2020-02-24 → 2026-08-05. Sliced to the campaign's own 3yr window
(2022-09-07 → 2025-08-20, 90 trading days — the same count as the committed data) and run through
the identical bootstrap methodology that produced the original 2.77% linear-rescale figure
(`data/aegis_solo_supplementary_bootstrap.json` key `"c4"`: `n_sims=2000`, seeds 1-5, weekly
blocks, `Tradeify_Select_100K`, `consistency=0.40`, reused verbatim via
`combined_sim.bootstrap_block_sweep`, no barrier logic reimplemented). Script:
[`followup_h4_native_4contract.py`](followup_h4_native_4contract.py); raw result:
[`data/followup_h4_native_4contract_results.json`](data/followup_h4_native_4contract_results.json).

**Result: 2.77% bust — an EXACT match to the linear-rescale figure, 0.00pp delta.** The single-path
result is byte-identical too (day 376, max_dd 0.9983%, matching `solo_recheck_results.json`'s own
`contracts=4` entry exactly). This is not a coincidence: cross-checking individual trades shows
Aegis-6J1's own signal generation is fully qty-independent — the 2022-09-07 trade, for example, has
an identical entry price, exit price, and timing in both exports, with `net_pnl_usd` scaling
exactly linearly (cap-8 export: $12.55/contract × 4 = $50.20; native 4-contract export: $50.20,
exact) — and commission scales linearly with qty in both ($3.10/side/contract). A linear rescale is
therefore mathematically exact for this specific strategy, at this specific sizing, on this
specific window. §6's rescale-bias concern (the borrowed "0.37-0.61pp" figure that would have
flipped this cell to a fail) was carried over by analogy from a different prior study — never
measured on Aegis-6J1 itself. This is the first direct measurement, and it finds the concern
doesn't apply here.

**H4 is closed: the sizing-matched Aegis-6J1 solo cell clears the 3.0% ceiling with its
originally-reported 0.23pp margin, confirmed rather than eroded.** This is the one figure in this
entire campaign's own scrutiny that survives cleanly — rescale bias specifically, on this one solo
cell. Two things this does NOT do: it does not retest §6's OTHER flagged correction for this same
cell (EOD-clock intraday-honesty — §6 estimated by analogy that this cell "would fail outright"
under that correction; still untested for Aegis-6J1 SOLO, since only the COMBINED book got a
genuine intraday-honest remeasure, §10.1), and it says nothing about the combined-book conclusion
above — §10's both-halves finding is about the COMBINED book at its own flagship sizings (5.333
Aegis contracts, not 4), an entirely different cell. 0.23pp is thin enough that this solo cell
should still not be read as robustly clearing without the intraday-honesty check too.

---

## Provenance

Originally produced by a 9-agent research workflow against `core/mc/simulation.py` and
`Tradeify_Select_100K` firm rules; updated through a follow-up 6-year ORB-MNQ export (resolving
H5/H6), the H1 contract-cap resolution (operator screenshot + decision), a mutual-exclusion timing
test (§3), a synthetic third-leg sensitivity test (§7), the in-repo third-leg instrument survey
(§7.1), and — same day, follow-up pass 2026-08-26b — closing the H2/H3/H7/H8/H10
analysis-readiness gaps (§9), which **materially revised the headline finding**: the 1yr flagship
fails a proper both-halves regime bootstrap, and the 3yr flagship's margin shrinks or fails
outright once tail-risk-consistent sizing and intraday-honesty are applied together. A further
same-day local-session follow-up (2026-08-26c, §10) closed §9.4's remaining handoff — a genuine
(timestamp-sequenced, not literal bar-panel) intraday-honest remeasure superseding §9.3's proxy,
and the compounding checks §9 didn't run split by regime half — and **reversed §9's own surviving
result**: the 3yr flagship, which §9.5 found cleared both regime halves, fails both once its own
identified corrections are actually compounded together (§10.2). A same-day closing follow-up
(2026-08-26d, §11) resolves H4 — the one item §10 left open — with an operator-supplied native
4-contract TradingView export that reproduces the original linear-rescale bust figure exactly
(2.77%, 0.00pp delta), on a different, solo-Aegis cell §10's both-halves finding does not touch.
Published first as a standalone artifact, saved here per operator request 2026-08-26. Exploratory
research throughout — no Pine-header baseline exists for either candidate strategy to reconcile
against; every bust/pass figure through §8 is a single-path replay or 5-day-block bootstrap over
end-of-day equity only; §9's intraday figures are a disclosed trade-level proxy; §10's are a
timestamp-sequenced reconstruction from the raw, un-reduced trade exports (real entry/exit
timestamps, not sub-trade bar resolution — §10.0 explains why a literal bar-panel match was
rejected); §11 is the first cell in this campaign to use a genuinely native (not rescaled or
proxied) export end to end. Raw CSVs are TradingView "List of Trades" exports (not raw OHLCV
vendor bar data) and are not committed; derived per-trade tables and daily-P&L panels are under
[`data/`](data/); the reusable simulators are [`combined_sim.py`](combined_sim.py),
[`followup_h7_h8_regime.py`](followup_h7_h8_regime.py),
[`followup_intraday_mae_proxy.py`](followup_intraday_mae_proxy.py),
[`followup_s10_bar_level_and_compounding.py`](followup_s10_bar_level_and_compounding.py), and
[`followup_h4_native_4contract.py`](followup_h4_native_4contract.py).
