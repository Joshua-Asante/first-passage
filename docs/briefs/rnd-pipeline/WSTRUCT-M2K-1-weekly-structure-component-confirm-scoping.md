# WSTRUCT-M2K-1 — weekly-structure component confirmation on M2K (scoping)

**Status:** `SUPERSEDED-ON-COST 2026-07-28 — no pre-registration authored, no K bound, no pull, no GO.`

> **⚠ COST-LAW CORRECTION 2026-07-28 — §2.2 is WITHDRAWN. Read this before anything below.**
>
> §2.2 concluded "the cost wall … is **not binding** at weekly frequency" from `~10 bp hurdle vs
> 100–300 bp weekly range = 10–30× margin`. That comparison is wrong **twice**, both in the same
> direction:
>
> 1. **Hurdle compared to the price RANGE, not the EDGE.** Under this brief's own model (§2.4:
>    hit-rate 0.5571, symmetric payoff) expected edge is `(2p−1) × move = 0.1142 × move` — 11.4%
>    of the scale, not the scale. Overstates margin ~8.8×. §2.4 does the Sharpe-space arithmetic
>    correctly and never converts it to bp to meet the cost gate.
> 2. **Costed at the RESEARCH round-trip count (1/week), not the deployable one.**
>    `ops/prop_envelope_default.md` §2 item 1 requires, verbatim, *"cost hurdle computed at the
>    deployable expression's round-trip count."* E1 forbids overnight **and** weekend holds, so a
>    weekly thesis decomposes to 5 RT/week (or 2 if restricted to Wed+Thu) — never 1.
>
> This is **harvest Requirement 5 / the same-units attestation rule** (ADR 2026-07-16), recorded
> there as having already killed **D5** and **H-OD-1** at Stage-2 cost-law.
>
> **Measured correction** ([`lab/analysis/c1/wstruct_cost_geometry_2026-07-28/RESULTS.md`](../../../lab/analysis/c1/wstruct_cost_geometry_2026-07-28/RESULTS.md),
> 243 weeks of real M2K data, 2019-05-06→2024-01-01): panel-era median price **1,897.20** →
> `hurdle_4x` **11.89 bp/RT** (not 9.81). Weekly range median **425.7 bp** (the illustrative
> 100–300 bp was *low*, which cuts in this brief's favour) — but weekly `|open→close|` move is
> **181.9 bp** and the Wed+Thu-reachable portion only **157.3 bp**, and *move* is the scale a
> directional bet captures.
>
> **Cost law at deployable RT counts:** 2 RT/week fails at the median week on both honest scales
> (`|move|` **0.87×**, Wed+Thu-reachable **0.76×**), clearing only at p75. 5 RT/week fails
> everywhere. **1 RT clears — and is the weekly hold E1 forbids.**
>
> **Consequence: no deployable expression clears the 4× cost law, so no pre-registration was
> authored against this brief.** M2K's K bank (0, floor 0.650 — the widest in the repo) is
> **NOT spent**; this closed at $0.00 and zero K, before any `register_search open`.
> Reopening requires an **asymmetric-payoff** mechanism claim with its own warrant — not a re-tune
> of the round-trip count, the day set, or the instrument.
>
> Everything below is preserved as authored, including §2.2's withdrawn conclusion, so the
> correction is auditable rather than silently overwritten.
**Date:** 2026-07-27 · **Type:** brief (Pre-Q scoping) · **Lane:** mechanism-first (harvest intake)
**Base:** `origin/main` @ `dea505d`
**Proposes:** ONE pre-committed component confirm, `K_eff = 1`, on a K-clean instrument.
**Does NOT propose:** re-opening Q-ICT-CASCADE-1, re-gating its M=65 survivors, or any
composition into the c1 book.

---

## §0 — Rule 0 reads (production + artifact source, verified this session)

Every number below was read from source at `dea505d`, not from memory. Path first:
`discovery_manifests/`.

```
discovery_manifests/*.json            LIVE K ledger, all 7 committed manifests:
                                        d5_nq_intraday_mom        K=1     closed  (NQ/MNQ)
                                        orb_mnq_intraday_breakout K=1     OPEN    (MNQ)
                                        h_od_1_es_overnight_drift K=1     closed  (ES)
                                        harv2026_001_es_monthend  K=1     closed  (ES)
                                        fb_eia_cl_reversal        K=1     closed  (CL)
                                        fc_carry_6e6j6cl          K=1     closed  (6E/6J/CL)
                                        disccamp0_gc_2010_18      K=3177  closed  (GC/MGC)
                                      => RTY / M2K bank = 0. No manifest touches it.
lab/archive/q_kbudget_1_2026-07/floor_scan.py::floor_at_k
                                      DSR floor annSR vs family bank K (computed, not quoted):
                                        K=1 -> 0.650   K=2 -> 0.850   K=3 -> 0.980
                                        K=5 -> 1.115   K=86 -> 1.620  K=3177 -> 2.050
                                      Cap = 1.0 (Q-GATECART-1, S_B-anchored, 4-way adjudicated).
lab/archive/ict_cascade_2026-06-18/CLOSURE-1M-INSUFFICIENT-N.md
                                      Cascade instrument = "1-minute US500 (Pepperstone)" -- a
                                      CFD on the RETIRED venue.
lab/archive/ict_cascade_2026-06-18/PREREG-W.md
                                      W verdict scope, verbatim: "a verdict on the weekly-close
                                      structure-only hit-rate, no more." Leg (b) (per-entry gate
                                      accuracy) explicitly NOT settled by that verdict.
core/firm_rules.py:205,222            Tradeify all-in $1.82 (MNQ/MYM/MES/M2K) -> $0.91/side.
                                      Equity Index Product Group = ES/MES/NQ/MNQ/YM/MYM/RTY/M2K/
                                      EMD/... => M2K IS tradable at the live firm.
lab/discovery/cost_model.py           Landed this cycle (PR #515). Used for the §2 cost screen.
ops/instruments/                      NO RTY or M2K ledger exists (un-ledgered instrument).
```

**Live-state checks performed:** `origin/main` synced (`dea505d`, 17 commits forward of the prior
read). `st_eh_supertrend_grid.json` (ST-EH-1, K=84) is **NOT** on `main` — that branch is
unpushed — but see §3.1, it counts anyway.

**Provenance note on §2's arithmetic.** The author's first hand-computation of the M2K hurdle was
wrong by a factor of 10 (~98 bp instead of 9.81 bp). It was caught by running
`lab/discovery/cost_model.py` rather than trusting the mental arithmetic. Every hurdle in §2 is
tool-computed. This is the `borrowed-numbers-need-the-connecting-arithmetic` failure mode firing
on the author, and it is why §6 requires the panel-era median price rather than an assumed level.

---

## §0.5 — Decisions (operator-resolved 2026-07-27: "proceed with your recommendations")

All four open questions were put to the operator and resolved in favour of the author's
recommendation. Recorded here as decisions, with the reasoning that earned each, so a later
session does not re-litigate them.

1. **Instrument-independence is REQUIRED, not merely period-independence.** The cascade's W
   structure was found on **US500** — an S&P-tracking CFD on the retired venue. MES/ES is the
   *same underlying* through a different wrapper, so a confirm there would be period-independent
   only. **M2K (Russell 2000, small-cap) is the instrument.** This is the stricter reading and it
   costs K headroom nothing (M2K's bank is 0 vs MES's 2).
2. **The confirm is a NEW mechanism-first hypothesis that CITES the W structure as warrant** —
   not a continuation of the cascade. `PREREG-W` settled leg (a) only ("the weekly-close
   structure-only hit-rate, no more"), so any confirm necessarily specifies an expression the
   original verdict did not cover. Framing it as a new hypothesis is what keeps it out of
   forking-paths territory; framing it as a continuation would make it a re-gate of M=65
   survivors and therefore a DUPLICATE.
3. **M2K ledger creation is licensed and DONE** — `ops/instruments/M2K.md`, created 2026-07-27 as
   the live touching session ADR 2026-07-25 §5 requires. It was also **load-bearing, not tidy**:
   `instrument_profiles.py cell M2K <mech>` returned `FATAL: no ledger for 'M2K'`, so without it
   stage 0a cannot produce a consult and `register_search open` on the mechanism-first lane would
   abort. RTY (the parent) is deliberately left un-ledgered — creating it absent its own touching
   session is the "complete the matrix" motive §5 forbids.
4. **Target is the prop-portfolio §4 falsifier** (undischarged; hard date 2026-11-08), **not** a
   c1 book leg. Q-COMPOSE-1 established that composition rescues nothing, and M2K shares
   Tradeify's account-aggregate Equity Index Product Group cap with the live MYM+MNQ legs.

---

## §1 — Context

The strategic bind, stated by the operator: the arithmetic favours **stated mechanisms over blind
mining** (the DSR floor is K-governed, so one campaign forecloses a family), but publicly stated
mechanisms are old and have usually decayed by the time we test them — D5/Baltussen was RANK #1 of
the archetype deep-search and measured **−0.327 bp OOS** on modern MNQ, with gross Sharpe −0.13.
The proposed escape: **framework-level constructs decay, but components of them may persist**;
piece together what survives and discard what does not.

**Our own record already tests that hypothesis, and splits along exactly that line.**
Q-ICT-CASCADE-1 (closed per-layer 2026-06-18/19 under a pre-registered joint **M=65** DSR/PBO
ledger, `lab/archive/ict_cascade_2026-06-18/DSR_PBO_LEDGER.md`) found:

| layer | verdict | detail |
|---|---|---|
| **Weekly** | **RESOLVED** | structure-only hit-rate **0.5571**, moving-block CI lb > 0.50, stationary, eff_N 910 — survived M=65. Routed "path-independent confirmation, NOT deploy." |
| **Daily** | split | SSL bear-FVG **RESOLVED** (0.795 vs base 0.712); BSL + both pools FALSIFIED. Single-panel. |
| 1H | FALSIFIED | 9-cell penalty |
| 1M | INSUFFICIENT-N | 0/247 fills; TV 1m data wall |

So "framework dies, components persist" is not a conjecture here — **it is the literal shape of our
own closure.** Two components are structurally real; the cascade as a deployable system is not.
The closure names one licensed forward route in its own words: the W/D RESOLVED sides are
single-instrument / mostly-single-regime and want **independent-instrument / independent-period
confirmation**.

Counter-evidence to hold: one ICT component *pairing* already died as a trade
(`lab/archive/pharos_us500_sweepfvg`, sweep+FVG, FALSIFIED). **Structural persistence is not
tradability.**

---

## §2 — The zero-data screens (all $0.00, all run this session)

### 2.1 K / DSR reachability — decides the instrument

`floor_at_k` vs Cap 1.0. A family's bank governs, not a campaign's own `K_eff` — that is how
Q-KBUDGET-1 axes D1/D4 died FAIL-K **without their effect sizes ever being examined**.

| family | bank today | floor | band vs Cap 1.0 |
|---|---|---|---|
| GC/MGC | 3,177 | 2.050 | **closed** (dead family) |
| NQ/MNQ/YM/MYM | 2 committed, **+84 pending** (§3.1) | 0.850 -> **1.620** | **closing** |
| ES/MES | 2 | 0.850 | open (0.15) |
| CL | 1 | 0.650 | open, but cost-dead (§2.2) |
| **RTY/M2K** | **0** | **0.650** | **open (0.35) — widest in the repo** |

At `K_eff = 1` on a zero-bank family the total bank becomes 1 -> floor **0.650**, headroom
**0.35** under the Cap. At `K_eff = 2` the bank becomes 2 -> floor 0.850, headroom 0.15. **One
component is affordable with margin; two is affordable only marginally; three closes the band.**

### 2.2 Cost law — decides the frequency, and it is not binding

Tool-computed (`cost_model.py`, Tradeify `$0.91`/side, 1 tick/side crossing). Index levels are
**ILLUSTRATIVE** — a pre-registration must use the panel-era median (M-20):

| instrument | notional | `hurdle_4x` | commission share |
|---|---|---|---|
| MNQ | $40,000 | 2.82 bp | 65% |
| MYM | $22,000 | 5.13 bp | 65% |
| MES | $29,500 | 5.86 bp | 42% |
| M2K | $11,500 | **9.81 bp** | 65% |

A weekly hold on an index micro faces a **~10 bp** 4x hurdle against typical weekly ranges of
**100-300 bp** — a **10-30x margin**. The cost wall that killed every daily and intraday axis in
the graveyard (D5 11.06 bp, H-OD-1 5.05 bp, H-ZNAUC 6-10 bp, NG 29.6 bp) **is not binding at
weekly frequency.** M2K is the most cost-expensive index micro (smallest notional) and still
clears comfortably.

### 2.3 Frequency geometry — why weekly, specifically

The graveyard's two walls are anti-correlated in event frequency and **the middle is
unoccupied**:

- **Daily / intraday** axes clear power, die on cost (D5, H-OD-1, H-ZNAUC-1, NG-EIA-1).
- **Monthly** axes clear cost, die on power at Default-#1's N≈86 (H-TSMOM-1, Clause-N 0.34).
- **Weekly** — N≈375 in the native-micro era (2019-05-06 -> present), ~52 RT/yr of cost drag.
  The only mid-band axis ever measured (ZN auctions, ~quarterly) died on cost for
  instrument-specific reasons (94% slippage-dominated hurdle — a Treasury property, not a
  frequency property).

**Weekly on an index micro is the best a-priori geometry this programme has left**, and the W
component is natively weekly. That alignment is the actual reason to prefer W over D-SSL, not a
preference for its magnitude.

### 2.4 Order-of-magnitude plausibility (NOT a forecast)

At `K_eff=1` the DSR floor is annSR **0.650**. A 0.5571 weekly hit-rate at symmetric payoff
implies per-trade Sharpe ≈ 0.114, annualising ≈ **0.82** at 52/yr — above the floor. Power at
N≈375 needs roughly δ/σ ≈ 0.10 (scaling the N≈86 / 0.211 convention by √(86/375)), i.e. annSR
≈ 0.73 — also below 0.82.

**Read this as reachability, not as an expectation.** It says the gate is not vacuous. It says
nothing about whether the structure transfers: the magnitude is borrowed from a *different
instrument*, a *different venue* (retired CFD), a *structure-only* metric, and D5's lesson is
that borrowed magnitudes decay — often to zero or negative. §6 requires the confirm be scored on
M2K's own measured effect, never on this figure.

---

## §3 — Why M2K, and the one route that is closed

### 3.1 The index-micro family is already foreclosed — and racing it is forbidden

**ST-EH-1** (Supertrend grid, NQ/YM parents + MNQ/MYM micros) **bound K=84 at
`register_search open` on 2026-07-26** (`discovery_manifests/st_eh_supertrend_grid.json`, open;
on an unpushed branch). Binding at `open` **is** the pre-registration act, so chronologically
those 84 trials precede any confirm authored now. Family bank ~2 -> **~86** -> floor **1.620** —
**0.62 above the Cap**. Any NQ/MNQ/YM/MYM component confirm authored today is **FAIL-K before its
effect size is examined**, exactly as D1/D4 were.

**Explicitly forbidden (§5):** freezing a brief before ST-EH-1 closes in order to record a
smaller denominator. That is K-laundering. The multiplicity is real whether or not the manifest
has closed; the GC/MGC precedent (DISC-CAMP-0's 3,177 killing later axes) is cumulative and
chronological.

### 3.2 M2K clears all four constraints simultaneously

| constraint | M2K |
|---|---|
| K-clean | bank **0** -> floor 0.650, headroom 0.35 |
| venue-live | Tradeify Equity Index Product Group, `$0.91`/side (`firm_rules.py:205,222`) |
| instrument-independent | Russell 2000 small-cap vs the S&P-tracking US500 the W structure came from |
| cost-viable | 9.81 bp 4x hurdle vs 100-300 bp weekly range |

MES fails only instrument-independence (same underlying as US500) and has a smaller K headroom
(0.15). Treasuries (ZB/ZN/ZF, bank 0) are **venue-dead at Tradeify** — `firm_rules.py:237-239`,
research-only, cannot serve a §4 candidate. GC/MGC is K-dead. CL/NG are slippage-dominated.

**M2K is the only instrument in the repo that is simultaneously K-clean, venue-live,
instrument-independent of the source finding, and cost-viable at weekly frequency.**

### 3.3 Cost of choosing M2K

- **Un-ledgered** — needs a ledger created (§0.5 Q3) and a PROFILE block, then a regenerated view.
- **No panel exists.** M2K/RTY bars are not in `core/data/bar_data/` or any databento cache. A
  pull must be cost-estimated first (dry-run mandatory; likely `$0.00` at `ohlcv-1d`/`ohlcv-1h`
  under the entitlement window, but **estimate, never extrapolate** — the Q-COSTGEO-2 lesson).
- **Liquidity is thinner than MNQ/MES.** For a weekly single-contract construct this is unlikely
  to bind, but displayed depth vs order size is a Phase-0 admissibility item now
  (`Q-COSTGEO-3`), not a Stage-7 refinement.
- **Shares the Equity Index Product Group cap** with the live MYM+MNQ legs — relevant only if
  this ever composes, which §0.5 decision 4 rules out.

### 3.4 Standing bars and priors this brief must clear (ADDED 2026-07-27)

The instrument-profile index surfaced three priors the brief's first draft did not address. They
were found by running the tooling, not by reasoning — which is the index layer working as designed
(ADR 2026-07-25 §1: "non-binding class-level bars" was one of the three failure modes it exists to
fix). None is fatal; all must be named and addressed in the pre-registration, not here.

**(a) BINDING CLASS BAR — `index-intraday-ohlcv-directional-timing-2026-07-21`.** Declared on
every ledgered equity index (ES/NQ/YM/MYM, inherited by MNQ/MES) and now carried directly on
`M2K.md` as finding **M1**, because M2K has no ledgered parent to inherit from. Origin: OPENPRESS-1.
Its addback condition is explicit: *"new modality / mechanism evidence — NOT an RV threshold,
alternate opening window, weekday slice, single-instrument selection after seeing the pair, or
re-pin to a newer BAR EXPORT panel,"* and its machine comment is blunter: *"NOT
threshold/window/instrument rescue on same OHLCV."*

**How this brief clears it, and the honest weakness.** Two arguments, one strong and one weak:
the bar's id and rejection scope are **intraday** (an opening-session mechanism on M15 panels)
whereas this construct is **weekly** — a different analysis level, not a window re-tune; and the
mechanism warrant is **independent prior evidence** (a layer that survived a pre-registered M=65
ledger on a different instrument and venue), which is what "new mechanism evidence" means. The
weakness: this is still OHLCV-derived directional timing on an equity index, and the bar's
addback explicitly refuses "instrument rescue on same OHLCV." **A reviewer could reasonably read
the bar as binding.** The pre-registration must argue this limb explicitly and record the consult
output; if the operator reads the bar as binding, the brief dies here and that is a legitimate
outcome.

> **⚠ RAISED-BAR TEXT CORRECTION 2026-07-29 — §3.4(a) argued against a non-canonical paraphrase. Read this before treating the quoted addback above as governing.**
>
> The addback text quoted in §3.4(a) (*"new modality / mechanism evidence — NOT an RV threshold,
> alternate opening window…"* / *"NOT threshold/window/instrument rescue on same OHLCV"*) and the
> attribution **"Origin: OPENPRESS-1"** are **not** the governing text of bar id
> `index-intraday-ohlcv-directional-timing-2026-07-21`. They are the **OPENPRESS-1 candidate**
> re-proposal bar ([`docs/rejected_candidates.md`](../../rejected_candidates.md) §Opening-volume ×
> directional-efficiency), miscopied onto the domain bar id when M2K.md **M1** and this §3.4(a)
> were authored (`a78cb85`, 2026-07-26). **False at source:** the domain bar was raised by the
> [2026-07-21 programme audit](../../notes/audits/programme-audit/2026-07-21-index-futures-intraday-ohlcv-domain-audit.md)
> on a four-closure basis (D5 / D5-RECOST / H-TSMOM-1 / cross-index-RV), not by OPENPRESS-1 alone.
>
> **Canonical test** (do not paraphrase further — read the registry):
> [`docs/rejected_candidates.md`](../../rejected_candidates.md) §"Single-instrument index-futures
> intraday OHLCV directional timing — RAISED BAR (tail-exhaustion; NOT a SNAG closure) 2026-07-21"
> — three-route disjunction: (1) mechanism outside the mapped cost-ratio-lever set {price,
> instrument-selection, hold-time}; OR (2) different modality / venue relaxing a binding wall; OR
> (3) beats incumbent ORB-MNQ net-of-cost. Surfaced by SLR-MYM-1 adversarial review
> ([`SLR-MYM-1` §2.7.1](SLR-MYM-1-liquidity-sweep-reclaim-scoping.md) "Separate ledger defect";
> ledger fix: M2K.md **M1** this session).
>
> **This brief's own verdict is unaffected.** It died independently on cost-law (see the
> 2026-07-28 correction banner at the top of this file) — no pre-registration was authored, no K
> spent. The §3.4(a) clearance argument above is preserved as authored so the defect is auditable;
> any future reader scoring this bar id must use the three-route test, not the OPENPRESS paraphrase.

**(b) RTY carries a DEFER-procurement flag with an explicitly poor prior** (`M2K.md` **M3**). The
cross-index RV selection candidate (ES/NQ/YM/**RTY**) was rejected 2026-07-21 and its re-proposal
bar names "a scoped **ES + RTY intraday pull**" as a DEFER-procurement trigger with a poor prior.
**Scope limit:** that rejection is of a *selection/rotation* mechanism across a universe, not of
single-instrument M2K work, and a **weekly**-bar pull is a materially smaller procurement than the
intraday pull that flag was written about. Still: the flag exists, this brief needs M2K data, and
§6 stage 1 inherits it. Estimate the pull; do not assume `$0.00`.

**(c) Mechanism vocabulary — declaration DEFERRED to the pre-registration, by rule.** The nearest
existing class is **`ict-liquidity`**, and the vocabulary growth rule is explicit that a `NEW`
entry "lands as a `MECHANISMS.md` entry **in the same commit as the pre-registration** that
introduced it." A scoping brief is not a pre-registration, so no vocabulary entry is added here —
and `cell M2K weekly-structure` correctly still returns `FATAL: unknown mechanism`. The pre-reg
author must choose and defend one of:

- **`ict-liquidity`** — nearest existing class, but its definition is *sweep → FVG →
  opposing-pool-draw geometry used as an entry signal*, which is **not** what the W layer is (a
  higher-timeframe structural bias). Declaring it inherits a cell verdict of **DEAD** on SPX500.
- **`NEW`** (e.g. `htf-structural-bias`) — arguably the honest class, and permitted; it must land
  with the pre-registration commit.

**Adjacent negative evidence that must travel with the mechanism warrant.** The `ict-liquidity`
class finding is worse than this brief's first draft implied, and it is the same family of work:
the sweep→FVG→pool-draw direction *is* real on SPX500 (block-permutation **p=0.0144**) but
**fails robustness** — drop-top-3 = **−0.152R**, 95% block-CI straddles 0 — and `SPX500 ×
ict-liquidity` is recorded **DEAD** (2026-06-17). The W-layer warrant survives this (different
layer, different metric, and W's own moving-block CI lb > 0.50 was the robustness check it
passed), but **the ICT family's overall track record on our own data is negative**, and the
pre-registration must state that rather than citing only the one RESOLVED layer. One point cuts
the other way and is worth keeping: the class finding notes the 1M 0%-fill execution wall is
**feed-general** ("would recur on NAS100 or any fast 1m index") — which is an argument *for* a
weekly construct, since that wall is a 1-minute-execution property this design does not touch.

---

## §4 — Falsifiable hypothesis

**H-WSTRUCT-M2K-1:** the weekly-close structural regularity that survived M=65 on US500
(hit-rate 0.5571) is an **instrument-general** property of equity-index weekly structure, and
therefore reproduces on M2K over the native-micro era at a magnitude clearing both the
`K_eff=1` DSR floor (annSR 0.650) and the 4x cost law (~10 bp/RT at the panel-era median price).

**FALSIFIED if any of:**
1. Measured M2K weekly structure hit-rate CI upper bound ≤ 0.50 (no structure), or
2. the tradable expression's gross edge < 4x RT cost at the panel-era median (cost-law KILL), or
3. realised annSR < 0.650 (DSR floor / demonstrability), or
4. Clause-N power at realised N < 0.50.

**RESOLVED** requires all four cleared **plus** a both-halves regime split (chop / trend) —
non-negotiable per the regime-robustness gate, and per this session's Finding #6, scored against
a **1.00x control arm partitioned identically**.

**AMBIGUOUS** if N is insufficient or the panel cannot be constructed — a legitimate terminal
state, not a licence to widen.

This hypothesis is **falsifiable at zero data cost on limb 1** (structure hit-rate needs only
weekly bars) and that limb should run first.

---

## §5 — Forbidden moves

- **No K-laundering.** Do not freeze ahead of ST-EH-1's close to record a smaller denominator
  (§3.1). Do not select the instrument *after* seeing which one has the friendliest bank — this
  brief fixes M2K on the four stated constraints, before any M2K data is read.
- **No re-gating the cascade's M=65 survivors on their own panel.** That is forking-paths
  re-entry and is a DUPLICATE per the Q-ICT-1 MOOT closure. This is a new hypothesis on a new
  instrument that *cites* W as mechanism warrant.
- **No component shopping.** `K_eff = 1`. If W fails, D-SSL is **not** a free second try — that
  is best-of-K with narrative cover. A second component needs a fresh operator GO and pays its
  own K (bank 1 -> 2, floor 0.650 -> 0.850).
- **No decomposing ICT further** to generate candidates. Dozens of nameable components at
  K=20+ makes the floor unreachable for any realistic edge. The selection was already paid for
  under M=65 in June; only the two survivors are pre-committed.
- **No borrowing the 0.5571 magnitude** into any gate, threshold, or expectation. It is
  cross-instrument, cross-venue, and structure-only.
- **No widening**: no window shopping, no threshold drift, no "just one more expression" after a
  FALSIFIED limb.
- **No composition** into the c1 book (Q-COMPOSE-1; §0.5 Q4).
- **No pull without a cost dry-run** recorded pre-pull, with a hard `--max-cost` and `--force`
  forbidden.
- No `core/`, allocation, `dd_protection`, Pine, or live-sizing change. Lock HELD.

---

## §6 — Gate criteria and staging

**Verdict taxonomy:** `RESOLVED` / `FALSIFIED` / `AMBIGUOUS`, per §4. Status reporting uses
`DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT` / `BLOCKED`.

Staged so the cheapest falsifier runs first and each stage can kill the brief:

| stage | cost | gate | kills brief if |
|---|---|---|---|
| **0a** | $0 | profile-consult (M2K cell) + K-ledger re-read at freeze time | bank ≠ 0 |
| **0b** | $0 | reachability attestation, per-clause `{value, units, basis, source}`, non-empty — now mechanically enforced (PR #516) | any clause undeclared |
| **0c** | $0 | cost-law hurdle at the **panel-era median** M2K price via `cost_model.py`, `firm_key` named | expression's δ < 4x RT |
| **0d** | $0 | Clause-N power at realised N | power < 0.50 |
| **1** | pull, est. first | weekly-bar structure hit-rate + moving-block CI | CI ub ≤ 0.50 |
| **2** | $0 | tradable expression, both-halves regime split, 1.00x control arm | either half fails |
| **3** | $0 | DSR at `K_eff=1` (floor 0.650) | annSR < 0.650 |

**Pre-registration must precede stage 1** and must bind `K=1` at `register_search open` with the
attestation and profile-consult attached. Stages 0a-0d are authoring-time screens, not results.

---

## §10 — Audit hooks (runnable)

```bash
# K ledger: RTY/M2K bank must be 0 at freeze time (re-read; do not trust this brief)
python -c "import json,glob;[print(json.load(open(f))['run_id'], json.load(open(f))['K'], json.load(open(f))['status']) for f in glob.glob('discovery_manifests/*.json')]"

# DSR floor vs Cap 1.0 at the K this brief claims
python -c "import sys;sys.path.insert(0,'lab/archive/q_kbudget_1_2026-07');import floor_scan as fs;print('K=1 floor',fs.floor_at_k(1));print('K=2 floor',fs.floor_at_k(2))"

# Cost hurdle must be recomputed at the panel-era median, firm named, no default
python -c "import sys;sys.path.insert(0,'lab');from discovery import cost_model as cm;print(cm.bp_hurdle('M2K', 2300, firm_key='Tradeify_Select_100K', slip_ticks=1.0, slip_convention='per_side'))"

# M2K tradability + commission at the live firm
grep -n "M2K\|Equity Index Product Group" core/firm_rules.py

# The cascade closure this brief cites -- confirm scope is structure-only, and do NOT re-gate it
grep -n "structure-only hit-rate" lab/archive/ict_cascade_2026-06-18/PREREG-W.md

# Forbidden-move check: ST-EH-1 must be CLOSED (or its K counted) before any freeze
ls discovery_manifests/st_eh_supertrend_grid.json 2>/dev/null && python -c "import json;d=json.load(open('discovery_manifests/st_eh_supertrend_grid.json'));print('ST-EH-1',d['K'],d['status'])"
```
