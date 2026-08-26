# Aegis-6J1 x ORB-MNQ-1 combined book — Tradeify_Select_100K passability (2026-08-26)

> ⚠ **The original 1.51%/0.01% headline bust figures below are SUPERSEDED (2026-08-26b) — see
> §9.** A proper both-halves regime-robustness bootstrap and two sizing/measurement corrections
> (§9.1-§9.5) revise the picture materially: the 1yr flagship fails outright, and the 3yr
> flagship's margin shrinks or fails once corrections compound. Read §9 before citing any number
> from §1-§8.

**Status:** EXPLORATORY — not pre-registered, not lock-grade. A user-supplied-CSV sizing/bootstrap
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

**Headline finding — REVISED 2026-08-26b, read §9 before citing any number below.** The original
1.51%/0.01% headline (naive equal-risk combined book, Aegis 5.33 : ORB-MNQ 0.29-0.40 contracts)
does not survive closer testing. A **proper both-halves regime-robustness bootstrap** (§9) finds
the 1yr flagship — the number that looked *safest* — **fails outright**: its second half alone
bootstraps to **4.02% bust**, masked entirely by the pooled full-window figure. The 3yr flagship
passes both halves at its original basis, but a **trade-level intraday-honest remeasure** (§9)
erodes its margin from 1.49pp to 0.61pp (2.39% bust), and compounding that with a
**tail-risk-consistent sizing ratio** (§9, bootstrapped 95th-percentile DD instead of one
historical worst day) pushes it to **4.34% — a clear fail**. **Each leg still fails this same eval
standalone** at realistic sizing (§0), and no tested combined configuration is now a clean,
uncontested PASS once these checks are applied together. See §9 for the full picture and what
still needs a genuine bar-level remeasure (handed off, not computable in this environment).

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

## Provenance

Originally produced by a 9-agent research workflow against `core/mc/simulation.py` and
`Tradeify_Select_100K` firm rules; updated through a follow-up 6-year ORB-MNQ export (resolving
H5/H6), the H1 contract-cap resolution (operator screenshot + decision), a mutual-exclusion timing
test (§3), a synthetic third-leg sensitivity test (§7), the in-repo third-leg instrument survey
(§7.1), and — same day, follow-up pass 2026-08-26b — closing the H2/H3/H7/H8/H10
analysis-readiness gaps (§9), which **materially revised the headline finding**: the 1yr flagship
fails a proper both-halves regime bootstrap, and the 3yr flagship's margin shrinks or fails
outright once tail-risk-consistent sizing and intraday-honesty are applied together. Published
first as a standalone artifact, saved here per operator request 2026-08-26. Exploratory research
throughout — no Pine-header baseline exists for either candidate strategy to reconcile against;
every bust/pass figure through §8 is a single-path replay or 5-day-block bootstrap over
end-of-day equity only, and §9's intraday figures are a disclosed trade-level proxy, not a
bar-level remeasure (handed off, §9.4). Raw CSVs are TradingView "List of Trades" exports (not raw
OHLCV vendor bar data) and are not committed; derived per-trade tables and daily-P&L panels are
under [`data/`](data/); the reusable simulators are [`combined_sim.py`](combined_sim.py),
[`followup_h7_h8_regime.py`](followup_h7_h8_regime.py), and
[`followup_intraday_mae_proxy.py`](followup_intraday_mae_proxy.py).
