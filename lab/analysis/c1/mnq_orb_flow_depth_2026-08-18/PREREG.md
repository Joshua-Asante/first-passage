# `MNQFLOW-1-DEPTH` — does ORB-MNQ-1's L1 book-tilt survive at MBP-10 depth?

**Status:** `FROZEN — PULL NOT AUTHORIZED.` MNQFLOW-1's own stop-rule (`RESULTS.md` L177-180) bars
re-cutting its frozen L1 design and explicitly lists "**MBP-10 arm**" among the forbidden re-cuts —
that passage is a **prohibition, not a designation**; it does not name or pre-authorize this
document. What it *does* say (its parent's own FM-4, quoted and answered in §5) is that any such
arm needs its **own fresh authorization** — this document is the **pre-registration through which
that fresh authorization is requested**, not the authorization itself and not something already
granted by the stop-rule it is bound by. The durable sign-off record — signer, timestamp, and
authorized scope — lives in §9.1, not here; nothing in this document is a substitute for it. Two
adjacent briefs independently
corroborate that MBP-10 escalation on this construct was left as "**needs its own decision**"
(§0), not flatly barred forever — that is the actual textual basis for treating a fresh PREREG as
the right container, argued explicitly in §3 and §5, not asserted from the stop-rule itself. The
remaining gate is an operator sign-off, which this document does not grant and is not self-issued
(MNQFLOW-1's own precedent, PREREG.md line 5).
**Date:** 2026-08-18 · **Authorization to design:** operator, *"start with item 1"* (Phase-1 plan,
this session).
**Cost of everything so far:** **$0.00** (estimates only; `metadata.get_cost` does not bill).
**Cost if authorized:** **≤ $125.00**, inside the untouched Avenue-A credit — MNQFLOW-1's own pull
used the free `tbbo` schema; no MBP-10 spend has ever occurred against this credit.
**K_intrinsic = 0** — reasoned fresh in §6, not inherited from MNQFLOW-1.

---

## §0 — Rule-0 reads (this session, at the line level, via a recon workflow + direct reads)

| Source | What it pins |
|---|---|
| [`docs/briefs/2026-07-24-avenue-a-microstructure-scoping.md`](../../../../docs/briefs/2026-07-24-avenue-a-microstructure-scoping.md) **read in full** | §6 frozen qualifying triple (verbatim in §3 below) + the 2026-08-05 addendum giving condition 3 a second route (Route A survivor-tied / Route B generate-confirm). **Route A is used here** — same as MNQFLOW-1, no Route B apparatus needed. §2's fork table: "Discovery: depth-shape... only live sliver — but unjustified without a specific pre-registered feature." This document supplies that feature. |
| [`lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/PREREG.md`](../mnq_orb_flow_substrate_2026-08-05/PREREG.md) **read in full** | The parent construct's own frozen design, its qualifying-triple argument (mirrored, not copied, below), and its FM-4 stop-rule (which this document is the named, separately-authorized exception to). |
| [`lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/RESULTS.md`](../mnq_orb_flow_substrate_2026-08-05/RESULTS.md) **read in full** | The L1 result under test at depth: diff **−0.009367**, CI95 **[−0.013430, −0.005354]**, placebo p_emp **0.000** (p95 threshold 0.004166), coverage **100.0% (255/255)**, halves agree (H1 −0.008133, H2 −0.010592). Depth-census counterargument (§2): L1 total size both sides p50=7 contracts, 99.98% of quotes fall in a tie-group, exactly-zero-imbalance 14.08% of the time — the coarseness this document tests whether depth resolves or inherits. |
| [`ops/instruments/MNQ.md`](../../../../ops/instruments/MNQ.md) F2 GUARD + N1/Stage-7 | F2 GUARD (outcome-conditioned ORB filter slices barred from any findings tier) — inherited via FM-1 below. N1: ORB-MNQ-1 full-pipeline PASS, K_eff=2, DSR 0.9754; Stage-7 rider: full-window clears only at Bulenox ≤1 tick — Tradeify (the former, now de-scoped, deployment venue) fails the full-window limb. Not itself under test here, carried as context. |
| [`lab/analysis/orb/orb_mnq_2026-07/RESULTS_decay_monitor.md`](../../orb/orb_mnq_2026-07/RESULTS_decay_monitor.md) | The PF-CUSUM decay-monitor seed (2021+ baseline PF 1.1691, floor 1.0855) this depth check would inform, never gate — ADR `2026-08-06-capa-tripwire-pfcusum-companion-registration` is the standing precedent for registering a structural observable beside it without arming anything. |
| Dedup check (this session): `STATE.md`, `docs/briefs/` full-text, `docs/rejected_candidates.md`, `lab/CATALOG.md`, and the pre-prune governance note (`git show pre-prune-2026-08-08:docs/notes/2026-08-05-order-flow-probe-governance-question.md`) | **No prior MBP-10 depth-escalation cell for N14/ORB-MNQ-1 has ever been proposed, drafted, or killed.** Two adjacent documents explicitly name it as deferred, not attempted: [`Q-CAPA-1-cap-seat-route-a-n14-tripwire.md`](../../../../docs/briefs/Q-CAPA-1-cap-seat-route-a-n14-tripwire.md) L99 ("MBP-10 / MBO escalation without fail-clause + GO... still requiring their own decision") and [`Q-OFCHAN-1-orderflow-channel-route-b-scoping.md`](../../../../docs/briefs/Q-OFCHAN-1-orderflow-channel-route-b-scoping.md) L102 ("Schema escalation to `mbp-10`/`mbo`... needs a later campaign pre-register"). **This is that later campaign.** |
| Live cost dry-run (this session, 2026-08-18) | See §4 — re-verified, not reused from the 2026-08-05 figures. |

**Dedup attestation (executed).** No entry in `rejected_candidates.md`, `STATE.md`, or `docs/briefs/`
proposes or kills this exact construct. Nearest adjacent priors are both explicit deferrals, cited above.

---

## §1 — The question, and why depth (not a re-cut)

MNQFLOW-1 found a real, small, `RESOLVED` L1 size-asymmetry tilt at ORB-MNQ-1's own trigger
boundary. But its own RESULTS documented, as mandatory disclosed context, that top-of-book alone is
coarse: at the median trigger, only 7 contracts sit on either side of the book, 99.98% of quotes tie,
and the imbalance reads exactly zero 14% of the time. A structure that thin could either (a) be a
genuine, if faint, resting-liquidity signature that a fuller view of the book would confirm and
sharpen, or (b) be an artifact of top-of-book granularity that a deeper view would reveal as noise
concentrated at the touch and absent further into the book. MNQFLOW-1's own text names this as the
one binding limitation a depth escalation would need to address (§4.1) and explicitly reserves it as
a gated, separately-authorized re-proposal route (FM-4) — never a re-cut of the frozen L1 design.

**H-MNQFLOW-1-DEPTH.** On a bounded subsample of ORB-MNQ-1's own trigger moments, the full 10-level
book asymmetry agrees in sign with, and is not dramatically diluted relative to, the same subsample's
own top-of-book asymmetry.

---

## §2 — The frozen construct

### §2.1 — Why a subsample, and why *this* subsample

MBP-10 costs far more than the free `tbbo` schema MNQFLOW-1 used. At today's re-verified rate
(§4), the full untouched $125 credit reaches roughly one RTH day per ORB-MNQ-1 trigger — nowhere
near the full 255-trigger panel. This document does not pretend otherwise: it is a **bounded,
descriptive depth cross-check on a subsample**, not a fresh independently-powered replication of the
n=255 L1 result. §8 states this plainly as the pre-registered expectation, not a caveat added after
seeing a number.

| # | Element | Frozen value | Source |
|---|---|---|---|
| S1 | Instrument / schema / window | `MNQ.v.0`, **`mbp-10`**, same panel as MNQFLOW-1: 2025-08-06 → 2026-08-04 | MNQFLOW-1 PREREG S1 |
| S2 | Event set | **30 of the 255 frozen ORB-MNQ-1 triggers**, selected by **full-range systematic sampling** over MNQFLOW-1's own chronologically-ordered trigger list: 0-indexed positions `round(i × 254/29)` for `i = 0..29` — a linspace-style sample spanning the entire `[0, 254]` index range inclusive (first and last chronological triggers both eligible), never a convenience or outcome-informed subset. A naive fixed-stride-8-from-0 scheme was considered and rejected at freeze time: it only ever reaches indices 0-232 (91.4% of the range), silently excluding the ~22 most recent triggers — an undisclosed recency bias this document does not carry | MNQFLOW-1 RESULTS.md trigger table (re-used, not re-derived) |
| S3 | Feature (depth) | **10-level size-weighted imbalance** `A_depth = (Σ bid_size_0..9 − Σ ask_size_0..9) / (Σ bid_size_0..9 + Σ ask_size_0..9)` at the touch, direction-normalized identically to MNQFLOW-1's `A`, averaged over the **60s preceding** the trigger | extends MNQFLOW-1 S3 |
| S3' | Feature (L1 comparator) | `A_L1`, **recomputed on this same 30-event subsample** (not reused from the full-255 figure) — the comparison must be apples-to-apples within the subsample | new, required for §7's agreement test |
| S4 | Control | Same design as MNQFLOW-1: k=5 matched control moments per trigger, same session, ≥15 min away, time-of-day matched — computed at both L1 and depth, from the same day-pull (no additional cost; MBP-10 billing is per calendar day, not per event) | MNQFLOW-1 S4 |
| S5 | Statistic | Mean `A_depth,trigger` − mean `A_depth,control`, session-block bootstrap 95% CI (10,000 reps, **new seed 20260818**, blocks = the 30 selected sessions); reported **alongside**, never in place of, the sign/ratio agreement test against S3' | extends MNQFLOW-1 S5 |
| S6 | Placebo | Within-session sign-shuffle, 1,000 reps, same seed, on the depth statistic | MNQFLOW-1 S6 |
| S7 | Coverage guard | Fraction of the 30 selected days with ≥1 MBP-10 quote in every trigger/control window; <90% → the coverage limitation is the headline | MNQFLOW-1 S7 |
| S8 | Agreement statistic (primary) | `ratio = abs(A_depth diff) / abs(A_L1(subsample) diff)`, and `sign_agree = sign(A_depth diff) == sign(A_L1(subsample) diff)`. **Denominator floor, frozen now:** `EPS_RATIO = 0.001` (matching the L1 study's own coarseness — its full-255 effect was 0.009367, so a subsample denominator below a tenth of that is treated as numerically unstable, not a real reference point) — if `abs(A_L1(subsample) diff) < EPS_RATIO`, `ratio` is **undefined by design**, not computed | new — this is the construct's actual question; the floor exists because the L1 statistic is tie-saturated (RESULTS.md §2: 99.98% tie-group, 14.08% exactly-zero) and a 30-event subsample of it can plausibly land near zero |

**Outputs (closed list):** trigger count, coverage fraction, `A_depth` / `A_L1(subsample)` means and
diff, `ratio`, `sign_agree`, the depth CI and placebo p, and the by-half split of the 30 selected
days. **Nothing else** — no per-trade table, no win/loss split, no MFE/MAE surface (FM-1, inherited).

### §2.2 — Cost/budget guard (inherits Q-COSTGEO-3's own P0 discipline)

**Phase P0 (blocking, at run time, before any pull):** re-estimate `metadata.get_cost` for the
*actual* 30 selected calendar days (not a generic single-day figure). **Abort if the re-estimated
total exceeds $125.00.** Even at the stale, higher 2026-08-05 figure ($3.97/day), 30 days = $119.10
— inside the ceiling with margin; at today's re-verified rate ($3.3304/day), 30 days ≈ $99.91. The
16% day-to-day variance measured in §4 means the actual 30-day total could land anywhere in that
range or slightly outside it — **P0's re-estimate, not either single-day figure, is the real gate.**

### §2.3 — Invalid-window and control-selection handling (frozen now, not left to runner defaults)

**Missing levels / zero-denominator quotes (S3, S3').** An MBP-10 record legitimately has fewer than
10 populated levels sometimes — a level with no resting order contributes size 0, that is real
information, not missing data. The degenerate case is different: `Σ bid_size_0..9 + Σ ask_size_0..9
= 0` at a given quote instant (no size anywhere in the book). That quote is **excluded** from the 60s
pre-trigger window's average — not silently treated as `A_depth = 0` (which would assert a false
balanced-book reading) and not left to divide-by-zero. **If every quote in a trigger's or a control's
60s window is degenerate this way, that trigger/control is `NO-DATA`** for this construct — it counts
against S7 coverage identically to a window with zero quotes at all (never silently dropped from the
denominator of anything downstream). S5/S6/S8 compute only over non-`NO-DATA` triggers/controls, and
the valid count actually used is reported alongside every number these produce, not implied from the
nominal 30.

**Control-selection algorithm (S4, frozen before any pull).** MNQFLOW-1's own S4 specifies session +
"≥15 min away" + time-of-day matching, but not the matching tolerance, candidate ordering, or
shortfall disposition — those gaps do not carry into this document; they are frozen here instead of
inherited unresolved:
- **Tolerance:** an eligible candidate falls within **±30 minutes** of the trigger's own
  session-clock time-of-day (minutes since session open), in addition to being ≥15 min from the
  trigger and in the same session.
- **Selection:** among all eligible candidates, take the **5 closest in absolute time-of-day
  distance** to the trigger; ties broken by earliest session-clock time. Deterministic and
  reproducible — no randomness anywhere in control selection.
- **Overlap:** a given moment may serve as a control for more than one trigger in the same session
  (each trigger's 5-control set is chosen independently of every other trigger's). This does not bias
  any single trigger's own trigger-vs-its-controls comparison; it does mean the full 150-control pool
  across the 30-trigger sample is not fully independent of itself — disclosed here, not hidden.
- **Shortfall:** if fewer than 5 eligible candidates exist for a trigger, use however many exist,
  down to a floor of **2**. Below 2, that trigger is `NO-DATA` for control purposes (same coverage
  disposition as above). The actual per-trigger control count achieved is reported — never assumed to
  be 5 throughout.

---

## §3 — The Avenue-A §6 qualifying triple, cleared condition by condition (Route A)

> *"1. Depth-shape, not category ... 2. Not fill-trivial ... 3. Either (Route A) survivor-tied ...
> or (Route B) generate→confirm."* — [`Avenue-A brief`](../../../../docs/briefs/2026-07-24-avenue-a-microstructure-scoping.md) §6 + 2026-08-05 addendum.

**1 — Depth-shape, not category. ✓** `A_depth` is resting-size geometry summed across ten book
levels. Exactly like MNQFLOW-1's L1 `A`, it attributes nothing to participant class — the a4 prior
(non-identifying for *categories*) does not reach it.

**2 — Not fill-trivial. ✓** This construct makes no fill, slippage, or execution claim. It is
measured on the same 60s *pre-trigger* window as MNQFLOW-1, before any fill exists, and its output
(a sign/ratio agreement statistic) cannot inform a fill-price question. The 07-21 realism audit and
this construct remain disjoint quantities.

**3 — Survivor-tied, Route A. ✓, argued on its own terms, not by analogy.** MNQFLOW-1's L1 verdict
is closed and `RESOLVED` — this document does not re-open or re-adjudicate that verdict, which stands
on its own frozen record regardless of what this cell finds (FM-4b below makes that explicit). What
is genuinely open is a **narrower, forward-looking question the L1 result could not answer**: whether
the coarse top-of-book instrument that produced it (median 7 contracts, 99.98% tie-saturated, per
RESULTS.md §2) is a faithful measure of the underlying book structure, or an artifact of measuring
only the touch. That is a monitoring question about the *reliability of an already-registered
watchlist observable*, not a re-test of whether the observable exists — the same distinction the
existing PF-CUSUM companion (ADR `2026-08-06-capa-tripwire-pfcusum-companion-registration`) already
draws between "does a signature exist" (MNQFLOW-1's question, closed) and "how much should it be
trusted" (this document's question, open). **Why the design deliberately mirrors MNQFLOW-1's** (same
trigger subsample's parent set, same control logic, same window, same bootstrap/placebo machinery):
that similarity is what makes this a valid apples-to-apples robustness check on the *instrument*
rather than a fresh fishing expedition with a different design — the one axis that changes is the
schema (`tbbo` → `mbp-10`), which is exactly the axis FM-4 gates and exactly the axis this
pre-registration seeks authorization for (§9.1), not something it grants itself. Route B's
generate→confirm apparatus is not needed and is not invoked.

**F2 guard — carried forward.** This construct never conditions on trade outcome. Triggers are
compared to non-trigger control moments, at both L1 and depth, identically to MNQFLOW-1. FM-1 below
makes that a forbidden move, not merely an omission.

---

## §4 — Cost dry-run (re-verified 2026-08-18, not reused from the stale 2026-08-05 figures)

```
python lab/databento_fetch/db_fetch.py estimate --symbols MNQ.v.0 --stype continuous \
  --schema mbp-10 --start 2025-08-06 --end 2025-08-07
```

| Schema | Window | Cost | Bytes | Records |
|---|---|---:|---:|---:|
| `mbp-10` | 1 RTH day (2025-08-06) | **$3.3304** | 7.1519 GB | 19,434,630 |

⚠ **This is ~16.1% below the 2026-08-05 PREREG's own $3.97/8.52GB single-day figure** for
`mnq_orb_flow_substrate_2026-08-05` — cost and bytes moved together by the same proportion, consistent
with one underlying driver (most likely day-specific book-update volume; possibly a Databento-side
change) rather than independent noise. **This document does not claim a repriced schema** — it
reports what was actually measured today and flags the drift rather than silently treating either
number as canonical. At today's rate, the full $125 credit reaches **~37 single-day pulls**; at the
stale higher rate, **~31** — both comfortably above this document's 30-event target (§2.2).

**The $125 Avenue-A credit is fully untouched.** MNQFLOW-1's own executed pull used the free `tbbo`
schema ($0.00 actual spend) — no prior MBP-10 spend exists anywhere in this program.

---

## §5 — Forbidden moves

- **FM-1 (inherited) — Reading ORB trade outcomes at any point.** No win/loss split, no PnL join, no
  outcome-conditioned cell — identical to MNQFLOW-1's own FM-1, the F2 guard's operative content.
- **FM-2 (inherited) — Emitting any per-trade or excursion surface** a successor could tune a filter on.
- **FM-3 (inherited) — Re-framing a positive as tradeable.** Any verdict below routes to the existing
  watchlist + forward tripwire, never an overlay or gate.
- **FM-4 (inherited, quoted verbatim — the rule this document exists to satisfy, not evade).**
  MNQFLOW-1's own FM-4 (`PREREG.md` L148-149): *"Any second cell: no MBP-10 arm, no alternate
  window/threshold/normalization sweep, no second instrument. Each is a new axis needing fresh
  authorization."* **This document is the request for that fresh authorization**, filed through the
  same pre-registration mechanism FM-4 itself describes — it does not claim FM-4 permits an MBP-10
  arm on request, and it does not claim to already carry that authorization. The authorization
  itself, when and if granted, lives only in §9.1's signed block — nowhere in this document,
  including this clause, self-issues it (FM-6).
- **FM-4b — Treating this subsample's result as a substitute for, or an overturn of, the n=255 L1
  `RESOLVED` verdict.** A `FALSIFIED-DEPTH-DILUTES` branch below is an important caveat *on* the
  existing watchlist companion, not a re-adjudication of MNQFLOW-1 itself — that verdict stands on
  its own frozen record regardless of this cell's outcome.
- **FM-5 — Widening the 30-event subsample post-hoc** if it "isn't enough" once P0's re-estimate
  runs, or cherry-picking which sample positions to keep after seeing partial data. The sample and
  count are frozen in S2; a wider sample is a fresh axis, not a mid-run adjustment.
- **FM-6 — Pulling before operator sign-off.** Avenue-A §6's final clause. Not mine to waive, same as
  MNQFLOW-1's own precedent.
- **FM-7 — Adjusting the `ratio` bands in §7, the seed, the control design, or the placebo after data.**
- **FM-8 — Using this document's ratio or sign-agreement output to set, tune, or calibrate any live
  numeric threshold** (the PF-CUSUM companion's eventual fire threshold, or any other) **without its
  own fresh pre-registration and K accounting.** §7's `RESOLVED-DEPTH-AMPLIFIED`/`-ATTENUATED`
  branches are descriptive findings about this instrument's behavior, not a calibration input —
  naming a plausible future consumer of the number is not the same as authorizing that use here.

---

## §6 — K accounting (reasoned fresh, not inherited)

**K_intrinsic = 0**, same posture as MNQFLOW-1's own reasoning: this measures a structural property
via a sign/ratio agreement statistic, never a strategy — FM-1 removes outcome data from the design, so
no edge estimate exists to be selection-inflated. If any future result here is ever converted into a
gate or filter, that conversion is its own fresh K-bound axis, exactly as MNQFLOW-1's §6 already states
for itself.

**K_banked(MNQ) disclosure — honest, not resolved here, and the uncertainty is larger than a rounding
error.** MNQFLOW-1's own record discloses `K_banked(MNQ) = 5` as of 2026-08-05. This session's recon
found the ledger (`ops/instruments/MNQ.md`) has not been updated since: **Q-TXG-1's striker×MNQ cell**
(closed 2026-08-12, DEAD(N-SURV)) self-declares "banked K=1" in its own closure doc but appears
nowhere in `ops/instruments/MNQ.md` — taking that closure's own words at face value, **the honest
current floor is K_banked(MNQ) ≥ 6.** That +1 is the *small* correction. A second, separately-closed
campaign, **MNQSR-1** (K=14, closed 2026-08-06, Notice-phase structure screen, "0/14 BH-FDR
survivors"), is also completely absent from the ledger — and whether a Notice-phase screen counts
toward the family harvest-intake K bank is not settled by the family-K-bank ADR's own text. **If it
counts, the floor is not ≥7 or ≥8 — it is ≥20.** A third item, Q-CAPA-1's already-ledgered "Cap seat
SPENT," is a further, smaller ambiguity (double-counts toward the family tally, or is a dedicated
seat — unresolved). **This document discloses the honest range (≥6, plausibly ≥20 depending on an
unsettled doctrinal question) and does not pick a convenient number from inside it** — resolving the
range, and reconciling the ledger for both undisclosed closures, is a separate ledger-maintenance
task flagged to the operator outside this pre-registration. K_banked is disclosure-only (ADR
`2026-08-04-family-k-bank-disclosure-not-gate`), so this ambiguity does not block signing this
document — it would matter to a reader assessing how "dry" the MNQ family search really is, not to
whether this cell's own K_intrinsic=0 is correctly reasoned.

---

## §7 — Verdict gates (frozen; precedence as listed)

| # | Condition | Verdict | Disposition |
|---|---|---|---|
| W6 | coverage < 90% of the 30 selected day-windows (S7) | `VOID-COVERAGE` | Report coverage only; no effect quoted |
| W5 | `abs(A_L1(subsample) diff)` < `EPS_RATIO` (S8) | `VOID-RATIO-UNDEFINED` | Report `sign_agree` and the depth CI/placebo only — no ratio-based verdict. Pre-registered now, not decided after seeing the number; a fragile subsample denominator is an expected possible outcome given the L1 statistic's own tie-saturation, not a design failure |
| W4 | `sign_agree` = **false** (depth and L1-subsample diffs disagree in sign) | `FALSIFIED-DEPTH-DILUTES-OR-REVERSES` | The likely concerning branch: the L1 tilt may not reflect true resting-liquidity structure. Attach as a caveat to the existing watchlist companion (FM-4b); does not itself demote or re-adjudicate MNQFLOW-1 |
| W3 | `sign_agree` = true, but depth CI (S5) includes 0 | `AMBIGUOUS-UNDERPOWERED` | **The most likely branch (§8)** — n=30 is a real, pre-disclosed power cut from n=255; this outcome is uninformative about the true depth signature, not a null finding. No demotion of anything |
| W2 | `sign_agree` = true, CI excludes 0, `ratio` ∈ [0.5, 2.0] | `RESOLVED-CONSISTENT` | Depth confirms the L1 tilt is not a top-of-book-only artifact on this subsample — strengthens confidence in the existing watchlist companion; opens nothing new (FM-3) |
| W1a | `sign_agree` = true, CI excludes 0, `ratio` > 2.0 | `RESOLVED-DEPTH-AMPLIFIED` | A descriptive finding: the depth-weighted tilt is larger than the L1-only reading on this subsample. **Not a calibration input** (FM-8) — reported as an instrument-behavior fact, nothing more, pending its own fresh pre-registration if anyone later wants to use it that way |
| W1b | `sign_agree` = true, CI excludes 0, `ratio` < 0.5 | `RESOLVED-DEPTH-ATTENUATED` | A descriptive finding: the depth-weighted tilt is smaller than the L1-only reading. Same FM-8 constraint as W1a — not a calibration input |

Every branch reports to the same watchlist companion record; **none opens a new gate, filter, or
K-bound campaign** (FM-3, FM-4b, FM-8).

---

## §8 — Pre-registered expectation

**W3 (`AMBIGUOUS-UNDERPOWERED`) is the most likely single branch, recorded now so it reads as a
discharged prediction rather than an excuse if it happens.** MNQFLOW-1's own effect was only ~2.25×
the placebo p95 threshold at n=255 with 10,000-rep bootstrap precision; cutting the event count to 30
(≈12% of the original) is a severe power reduction with no compensating design change. A wide CI that
includes 0 at n=30 says nothing about whether the true depth signature is absent — it says the budget
this document can spend is not enough to resolve the question on its own. That is disclosed as the
expected outcome, not discovered as a disappointing one.

---

## §9 — Protocol order (violations void the run)

1. **This file committed = freeze** — done before any book-state quantity has been computed for this
   construct. **Not yet operator-signed.**
2. **OPERATOR SIGN-OFF on the pull** — Avenue-A §6's remaining clause, recorded durably in §9.1 below.
   **Not granted here; not self-issued**, same posture as MNQFLOW-1's own PREREG line 5.
3. **P0 — blocking cost re-estimate** on the actual 30 selected calendar days (§2.2). Abort if it
   exceeds $125.00.
4. Harness + hand-computed unit tests; all pass before the runner reads a real quote.
5. Single run. RESULTS discharges exactly one §7 branch. Board write owed in every branch (mirrors
   MNQFLOW-1's own discipline).

### §9.1 — Operator signature block (DRAFT until filled; gates step 2 above)

```
SIGNED / FROZEN: ____ / ____   (date / initials)
Authorized: MNQFLOW-1-DEPTH — the MBP-10 depth escalation on ORB-MNQ-1's own frozen trigger
subsample (S2: 30 of 255, full-range systematic sample), schema mbp-10, window
2025-08-06 -> 2026-08-04, ceiling <= $125.00 subject to §2.2's P0 re-estimate gate.
CONFIRMS: every §5 forbidden move stands as written, including FM-8 (no threshold calibration
from this document's output without its own fresh pre-registration and K); K_intrinsic=0 as
reasoned in §6; K_banked(MNQ) disclosed as >= 6 (possibly >= 20, genuinely unresolved — §6),
acknowledged at signature time, not hidden.
No pull runs before this block is filled.
```

---

## §10 — Audit hooks

```bash
# Freeze ordering
git log --oneline -- lab/analysis/c1/mnq_orb_flow_depth_2026-08-18/PREREG.md | tail -1

# The triple this clears, and the addendum giving condition 3 a second (unused) route
grep -n "Route A\|Route B\|qualifying triple" docs/briefs/2026-07-24-avenue-a-microstructure-scoping.md

# The parent construct's own stop-rule this document is the named exception to
grep -n "MBP-10 arm" lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/RESULTS.md

# The F2 guard FM-1 exists to satisfy
grep -n "F2 GUARD" ops/instruments/MNQ.md

# Cost dry-run reproduction (FREE; never add `pull`) — re-run and compare to §4's $3.3304 anchor
python lab/databento_fetch/db_fetch.py estimate --symbols MNQ.v.0 --stype continuous \
  --schema mbp-10 --start 2025-08-06 --end 2025-08-07

# K_banked(MNQ) disclosure honesty check — confirm the ledger is still stale at read time
grep -n "bank " ops/instruments/MNQ.md | tail -5
grep -n "TXG" ops/instruments/MNQ.md   # expect: no hits (the undocumented +1 this doc discloses)

# Signature gate — confirm no pull is authorized until §9.1 is actually filled
grep -n "SIGNED / FROZEN: ____" lab/analysis/c1/mnq_orb_flow_depth_2026-08-18/PREREG.md \
  && echo "STILL DRAFT — no pull" || echo "signed"
```

---

## Amendment log (append-only — the frozen §§1-9 above are never edited, Trap #12)

- **2026-08-18 — FROZEN, after an adversarial verify pass caught real problems in the first draft.**
  Authored before any book-state quantity existed for this construct. Recon executed via a 5-agent
  workflow (Avenue-A governance text, MNQ.md F2 guard + K ledger, MNQFLOW-1's exact prior numbers, a
  dedup check, and a live cost dry-run) plus direct reads of the Avenue-A brief and its own stop-rule
  text. A second, independent 5-agent adversarial workflow then reviewed the drafted document against
  its cited sources and found two real problems in the first pass, corrected before this freeze: (1)
  the header mischaracterized MNQFLOW-1's stop-rule prohibition list as naming/authorizing an MBP-10
  arm, and silently omitted the parent's actual FM-4 text — both fixed by quoting FM-4 verbatim and
  arguing this document as its fresh-authorization instance, not as something the stop-rule already
  granted; (2) the original stride-8-from-0 event sample silently excluded the ~22 most recent
  triggers (91.4% range coverage), and the ratio statistic (S8) had no guard against a near-zero
  denominator given the L1 feature's own tie-saturation — both fixed (full-range systematic sample;
  `EPS_RATIO` floor + `VOID-RATIO-UNDEFINED` verdict branch, W5). Two further, smaller findings also
  applied: §6's K-banked disclosure now states the MNQSR-1 swing explicitly (≥6 -> possibly ≥20, not
  a 1-2-unit residual), and FM-8 was added barring the ratio/sign-agreement output from calibrating
  any live threshold without its own fresh K accounting (§7's W1a/W1b language softened to match).
  Pull **not** authorized at freeze time. $0/K=0 at authoring. Disclosed, not resolved:
  `K_banked(MNQ)` ledger staleness (separately flagged to the operator, outside this document).

- **2026-08-18 — Revised after a CodeRabbit review on the opened PR caught six real issues.**
  (1) "This document is that fresh authorization" (header + FM-4) was self-contradictory against the
  `PULL NOT AUTHORIZED` status — reworded throughout to "the pre-registration through which that
  fresh authorization is requested," and a durable, auditable operator-signature block (§9.1) was
  added so a sign-off has a concrete place to land (signer, timestamp, authorized scope), mirroring
  Q-COSTGEO-3's own §9 convention. (2) S3/S4/S7/S8 never defined what happens with missing MBP-10
  levels or a zero-size book at a given quote, nor the control-selection algorithm's exact tolerance,
  ordering, overlap, or shortfall behavior — both frozen now in a new §2.3 rather than left to runner
  defaults. (3) The `abs(x)` ratio/EPS_RATIO notation used literal `|x|` bars inside Markdown table
  cells, breaking table parsing (`markdownlint-cli2` MD056/MD038, confirmed: expected 4 columns,
  actual 10) — replaced with `abs(...)` throughout. Sibling fixes on the same PR: Q-FILLTAX-1's
  verdict pre-registration had its §3 table assign `RESOLVED` to the synthetic-only battery result
  while its own prose said the opposite — reworded to require the Phase 2 pinned-anchor run; the
  parity-mutation test suite now pins `EPS_DENOM` alongside the other frozen band constants.
