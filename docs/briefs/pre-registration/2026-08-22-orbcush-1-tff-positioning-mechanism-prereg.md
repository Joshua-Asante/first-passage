# Q-ORBPOS-1 — Pre-registration: does a CFTC TFF positioning-extreme classifier explain ORB-MNQ-1's 2021-09-28 cushion-sizing regime break?

**Status:** **Operator GO given** — Joshua, 2026-08-23 chat: "take it up." Authorizes the full §7
execution plan (Phase 0 → Phase 4) in one motion, since §8 carries a single K=0/$0 gate here, not
MNQTAPE-1's staged design/explore/confirm-spend split. As of this Status line, Phase 0 (contingency
resolution) has not yet run and no CFTC TFF position value has been read — execution proceeds from
here in strict phase order per §7/§4's ordering clause.
**Authored:** 2026-08-22
**Authors:** Joshua (direction) + Claude Code (Sonnet 5)
**Parent:** [`Q-ORBCUSH-1`](../Q-ORBCUSH-1-regime-break-mechanism.md), closed `FALSIFIED`
[`2026-08-20`](../closures/Q-ORBCUSH-1-closure-falsified.md) — this opens the **third** candidate
mechanism that closure's own re-proposal bar requires: *"a genuinely different candidate
mechanism... not a re-tuned window on either already-refuted classifier."* Q-ID for this candidate:
**`Q-ORBPOS-1`** (fresh Q, per that closure's own routing: *"a future session naming a third
candidate mechanism... would open a fresh Q, not amend this one"*).
**Loop:** Inquire-phase Pre-Q — gates whether a real, causally-tested positioning mechanism
explains ORB-MNQ-1's 2021-09-28 cushion-sizing pass-rate regime break, before a third trailing
classifier is treated as evidence either way.
**Artifact path:** `docs/briefs/pre-registration/2026-08-22-orbcush-1-tff-positioning-mechanism-prereg.md`

---

## §0 — Rule 0 reads (production-source verification, this document)

| Source | Anchor | Supplies |
|---|---|---|
| [`docs/briefs/Q-ORBCUSH-1-regime-break-mechanism.md`](../Q-ORBCUSH-1-regime-break-mechanism.md) | `b12689c` (2026-08-20) | The break's own definition (~2021-09-28, triple-verified, non-boundary-luck), the frozen falsification discipline this brief reuses (3 pre-registered windows, no post-hoc picking, independent second implementation), and H-ORBCUSH's exact Accept/Reject wording, which this brief's H-ORBPOS mirrors. |
| [`docs/briefs/closures/Q-ORBCUSH-1-closure-falsified.md`](../closures/Q-ORBCUSH-1-closure-falsified.md) | `bcef3e0` (2026-08-20) | Both prior candidates' actual numbers — trailing volatility (sign-flip between 20d and 63d/126d) and trailing mean-R (date-correlation clears **0 of 3** windows) — and the explicit re-proposal bar this brief exists to satisfy. Also the K/registry convention this brief inherits (§8 below): "$0.00 · K consumed: 0 (diagnostic/explanatory question about an already-real pattern, not a strategy-candidate proposal — same class as Q-GEOFIT-1)"; "no `docs/rejected_candidates.md` row." |
| [`docs/briefs/pre-registration/Q-ORBCUSH-1-verdict-preregistration.md`](Q-ORBCUSH-1-verdict-preregistration.md) | `b84544a` (2026-08-20) | The exact three-window design (W1=20 / W2=63 / W3=126 **trades**) and threshold wording (≥75% higher-bucket / ≤40% lower-bucket post-break; zero-tolerance sign-flip rule) this brief decides whether to reuse verbatim or re-express (§2.3, §4). |
| [`ops/instruments/MNQ.md`](../../../ops/instruments/MNQ.md) N17 (+N18/N19, added after Q-ORBCUSH-1 closed — re-checked at draft time; see note) | `1e40b11` (2026-08-22) | The standing record of the break and both refutations (N17). **Re-verification note:** as of this brief's own drafting, `MNQ.md` has advanced past N17 to **N19** (N18 = a skew-sizing/magnitude-resampling probe; N19 = `Q-ORBSURV-1` `FALSIFIED` — cushion-sizing's gate-clear is k-dependent, k=1 full-panel clears pass by only 2.27pp margin, k=2 misses the pass floor). Neither touches the break's mechanism; N19 confirms k=1 (not k=2) is the correct, still-current gate-clearance configuration this brief's §4 measures against. This brief's own closure appends **N20**, not N18, to this ledger regardless of verdict — RESOLVED, FALSIFIED, or AMBIGUOUS-HOLD. |
| [`docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md`](../../adr/2026-08-03-orb-mnq-repark-payability-falsified.md) | `027a729` (2026-08-14) | The frozen survivor-scoring gate (bust ≤3.0% AND P(pass) ≥50%) the gate-clearance-direction limb of H-ORBPOS is measured against; unaffected by this brief's outcome either way (inherited unchanged from Q-ORBCUSH-1 §5). |
| [`lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/run_evalseq_orb_intraday.py`](../../../lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/run_evalseq_orb_intraday.py) | `b84544a` (2026-08-20) | The already-verified gate-clearance harness (`day_loop_intraday` / `build_paths_orb` / `run_policy_orb` / `pol_cushion` / `pol_const`) this brief's Phase 2 imports unchanged, exactly as both prior rounds did. |
| [`docs/briefs/programs/2026-07-14-a4-flow-data-fork-scoping.md`](../programs/2026-07-14-a4-flow-data-fork-scoping.md) | `027a729` (2026-08-14) | This repo's only existing characterization of CFTC TFF mechanics: weekly Tuesday snapshot, Friday ~3:30pm ET publication, free (cftc.gov CSV/Socrata), coverage to 2006-06-13, and — critically — "ES/ZN are TFF, not Disaggregated" (confirms the recon finding that TFF, not the Disaggregated COT report, is the correct free/no-key category for an index future). Also the four structural degradations found scoping TFF for a *different* fork (cadence, off-futures expression, impure category mapping, net-of-gross masking) — reasoned through for transferability in §2.2/§2.3 below rather than assumed to apply or not apply. |
| [`docs/methodology/strategy_harvest.md`](../../methodology/strategy_harvest.md) §1 (five admission requirements), §2.3 rank-4 | `fd0e6ee` (2026-08-18) | Channel taxonomy: "CFTC COT/TFF positioning data — Direct data read — Tier-A positioning-reversal mechanism source; flagged power-marginal at weekly event frequency — check requirement 4 before manifesting." Used in §8 to reason explicitly about whether the four external-mechanism admission requirements bind this brief (conclusion: they gate *strategy-candidate* seeds entering discovery→validation; this brief proposes no strategy, no entry rule, no live feed — see §8). |
| [`lab/analysis/harvest/radar_tier_a_burst_2026-07/CANDIDATE_ROWS.md`](../../../lab/analysis/harvest/radar_tier_a_burst_2026-07/CANDIDATE_ROWS.md) (H-COTREV-6A row) | `2028f36` (2026-08-17) | A CFTC-COT AUD positioning-extreme-reversal candidate, disposed `UNSCREENABLE (Requirement 2)` 2026-08-16. Carries a load-bearing literature caution used in §2.1: Wang (2003/2004) found large-**speculator** sentiment predicts **continuation**, and large-**hedger** sentiment predicts **reversal** — the "commonly-practiced 'extreme non-commercial/leveraged-fund positioning → mean-reversion' framing... runs opposite to that reading," flagged "for any future COT-based candidate on any instrument." This brief is a different question shape (regime-date correlation, not directional price prediction — §2.1) but the caution is read and addressed, not ignored. |
| [`docs/rejected_candidates.md`](../../rejected_candidates.md) (Q-MCLTAS-1 entry) | `027a729` (2026-08-14) | A concrete prior COT rejection instance: "COT weekly and lagged" named as one of three failed {free, signed, price-exogenous, window-aligned} sign sources at Wall A for a 2-minute MCL settlement-window flow proxy (2026-08-11). |
| [`docs/briefs/closures/MNQBASE-1-closure-intake-dry.md`](../closures/MNQBASE-1-closure-intake-dry.md) | `027a729` (2026-08-14) | A second concrete instance: "CFTC COT/TFF — inherited (census P4-2) — weekly density, cross-sectional δ — dead," in the context of sourcing a *live* strategy signal. |
| `C:\Users\joshu\.claude\skills\futures-anomaly-discovery\SKILL.md` (operator-side skill file — not repo-tracked, no git anchor; read in full 2026-08-22) | n/a | "**Explanation is deferred (Simons stage 3).** Discovery does not need a mechanism — a survivor eventually does. Do not buy explanatory data (MenthorQ gamma, SqueezeMetrics GEX/DIX, **COT**) before a candidate has survived validation; explanation is the last stage, not the first." Names COT explicitly. Addressed head-on in §8, not sidestepped. |
| [`lab/analysis/orb/orb_mnq_2026-07/RESULTS.md`](../../../lab/analysis/orb/orb_mnq_2026-07/RESULTS.md) | `027a729` (2026-08-14) | ORB-MNQ-1's own panel span: native `MNQ.v.0` continuous 1m, **2019-05-06 → 2026-07-15**. This fixes the practical pre-break history at ~2.4 years (2019-05-06 → 2021-09-28, ≈125 weeks) — the binding data-availability constraint on this brief's design, not TFF's own 2006 coverage floor (§2.2). |

---

## §1 — The problem this design must solve, stated before anything else

The break is not in question. Q-ORBCUSH-1's own probe triple-verified (halves → thirds →
sub-split) a real, non-boundary-luck regime break in ORB-MNQ-1's cushion-sizing gate-clearance pass
rate at **~2021-09-28**: every sub-window before it fails the frozen survivor-scoring gate badly
(pass 0.5–2.9%), every sub-window from late-Sept-2021 forward clears it independently (pass
54–90%). Two economically-plausible trailing classifiers — realized volatility, then the strategy's
own realized mean-R — were tested against that break under an identical, twice-proven falsification
discipline and **both refuted**: volatility failed on a sign-flip between windows; mean-R failed
because date-correlation never cleared at any of the three pre-registered windows (0/3), despite a
stable direction.

**Neither prior round, nor its closure, makes any claim connecting the break to positioning
extremes.** A TFF-positioning-based explanation is a genuinely new, third candidate mechanism — not
a re-tuned window on volatility or mean-R, and not a re-run of either already-refuted classifier
under new arithmetic. This satisfies Q-ORBCUSH-1's own closure re-proposal bar on its face; §2
states the candidate precisely enough to be wrong, and §8 accounts for it as a third trial against
the same break, not a free re-roll.

**What is different this time, and must be reasoned through, not assumed:**

1. Both prior candidates were computed entirely from ORB-MNQ-1's **own** trade/price series —
   no external data source, no new access mechanics, no new cost/cadence structure. This candidate
   pulls from an **external, never-before-touched-by-this-thread** data source (CFTC TFF), which
   changes three things simultaneously: the classifier's native cadence (weekly, not trade- or
   day-indexed), the number of pre-registration decisions that must be frozen *before* any number is
   read (contingencies §2.4), and whether this repo's general doctrine on buying explanatory data
   applies (§8).
2. CFTC/COT-family data has been tried and rejected multiple times in this repo, always for
   sub-weekly signal-timing mismatch, on **other** instruments and for **recurring/live-signal**
   uses (§0, §2.2). Whether that objection transfers to a **one-time, discrete regime-shift
   correlation check** is reasoned through explicitly in §2.2 — not assumed to transfer, and not
   assumed to be exempt.

---

## §2 — The mechanism, stated precisely enough to be wrong

### §2.1 — Category choice: Leveraged Funds (primary) vs Asset Manager (secondary), and why

CFTC's TFF report splits reportable positions into **Dealer/Intermediary**, **Asset
Manager/Institutional**, **Leveraged Funds**, and **Other Reportables**, plus a residual
non-reportable estimate. Two categories are theoretically defensible index-futures proxies:

- **Leveraged Funds** — hedge funds, CTAs, and other levered money managers. The standard proxy in
  the positioning-extremity literature for **crowding / fast money**: a book that is one-sidedly
  extended is the textbook setup for a violent, liquidity-driven unwind.
- **Asset Manager/Institutional** — pension funds, insurers, long-horizon allocators. The standard
  proxy for **patient, benchmark-driven real-money flow** (this is the same category the
  `2026-07-14-a4-flow-data-fork-scoping.md` doc used as the "real-money rebalancer proxy" for ES/ZN
  month-end).

**Primary = Leveraged Funds net position as a percent of open interest (%OI).** Reasoning: the thing
being explained is a break in **bust-rate / tail-risk survival** under a fixed-stop breakout
strategy — a mechanism story about "what changed in late-Sept-2021" is more plausibly connected to a
crowding extreme (which is specifically implicated in squeeze/violent-unwind dynamics that would
threaten a breakout strategy's worst-day stop-out risk) than to a shift in patient long-horizon
allocation, which is smoother and less obviously connected to an abrupt date-localized break. This
also keeps the candidate legible against this repo's own standing caution (`H-COTREV-6A`, §0): that
row already flagged "extreme leveraged-fund positioning" as *the* commonly-attempted CFTC-positioning
framing, so testing it here — rather than picking a fresh, unprecedented category — lets this
brief's result stand alongside that caution instead of past it.

**The `H-COTREV-6A` sign-direction caution is read and addressed, not ignored.** Wang's finding —
large-speculator sentiment predicts continuation, not reversal — is a caution about **directional
price prediction** from a positioning extreme. **This brief predicts no price direction.** H-ORBPOS
(§4) never claims "LF-extreme buckets have higher/lower mean-R" or any directional payoff; it claims
only that a bucket split by LF-extremity **date-correlates** with the already-known break and
produces a **stable-sign** gate-clearance split across windows — structurally the same
sign-agnostic test the volatility and mean-R rounds already ran, chosen specifically *because* it
sidesteps needing to commit to Wang's contested sign a priori. This is not a coincidence: it is the
correct test shape for a candidate whose own literature disputes its directional sign.

**Secondary/fallback = Asset Manager net %OI**, same causal-window discipline, invoked **only** by
the pre-registered Ambiguous-hold triggers in §4 — never by "the primary result wasn't clean."

**Normalization: %OI, not raw net contracts.** MNQ/NQ aggregate open interest structurally grew
over 2019–2023 as the micro contract matured. A raw-net-contracts classifier would be dominated by
that secular growth trend and would trivially date-correlate with almost anything monotonic across
the sample — the same circularity trap that made the long-window volatility and mean-R results
suspect. %OI is normalized against the contemporaneous book size and is frozen as the sole unit
before any TFF row is read.

### §2.2 — Data-structure contingencies, decided now, before any TFF row is read

- **MNQ may not be separately reported.** CFTC's TFF category structure predates Micro E-mini
  Nasdaq-100's 2019-05-06 launch (per `RESULTS.md`, §0). If CFTC reports a combined NQ+MNQ line
  rather than MNQ standalone, that combined line is used as the proxy **only if** MNQ's own share of
  combined exchange-published volume or open interest (sourced from CME's own public contract
  statistics — **not** TFF, and not pulled as part of this pre-registration) is documented at **≥10%**
  over the test span. Below that, the combined line is judged too diluted by NQ (the much larger,
  older contract) to carry MNQ-specific signal, and the AMBIGUOUS-HOLD route in §4 fires. The 10%
  bar is chosen now, blind to the actual share, as a conservative floor for "MNQ's own flow could
  plausibly move the combined read at all" — not tuned to whatever the real share turns out to be.
- **TFF's 2006-06-13 general coverage floor is not the binding constraint here — MNQ's own
  2019-05-06 launch is** (§0, `RESULTS.md` anchor). The practical pre-break history is ~2.4 years
  (~125 weeks), which comfortably contains the W3 window below (§2.3) roughly 4–5 times without
  overlap, but is not large.
- **Reporting-lag convention.** TFF is a Tuesday snapshot published the following Friday ~3:30pm ET
  (§0, A4 doc). A given week's classifier value may use only TFF prints **already published** as of
  that week — the Tuesday-to-Friday lag is itself respected, not treated as same-week-available. This
  mirrors the `.shift(1)`-equivalent causal discipline both prior rounds used.
- **Exact category/column names** (e.g., whether CFTC's published column is literally "Lev Money
  Positions Long/Short" and whether %OI needs to be derived or is a published field) are confirmed
  against the CFTC TFF explanatory notes at **Phase 0**, before any position number is read — not
  assumed correct here. This is due diligence, not evidence, and does not touch position data.

### §2.3 — Window design: re-expressed in TFF's own native cadence, not reused byte-for-byte

The prior two rounds used **trade-indexed** windows (W1=20 / W2=63 / W3=126 trades) because their
classifiers (volatility, mean-R) are naturally computed from ORB-MNQ-1's own trade/day sequence. TFF
publishes **weekly**, independent of ORB-MNQ-1's own trading calendar — a trade-count window is
undefined for a series that does not tick with trades. Two choices were considered:

1. **Reuse 20/63/126 verbatim, re-interpreted as weekly counts.** Rejected: this would silently
   change what a "window" means (20 *weeks* is a materially longer real-time span than 20 *trades*,
   given ORB-MNQ-1 triggers on ~99% of sessions — Q-ORBCUSH-1 §4), breaking comparability with the
   prior rounds' own stated rationale for each window length (short-window instability check,
   quarter, two-quarter).
2. **Calendar-convert to weeks, preserving each window's real-time span** (adopted). Since
   ORB-MNQ-1 triggers on ~99% of sessions, trading sessions and weekdays are nearly interchangeable
   for this purpose: 20 sessions ≈ 4 calendar weeks, 63 sessions ≈ 13 weeks (≈1 quarter), 126
   sessions ≈ 26 weeks (≈2 quarters). This keeps the **rationale** for each window identical to the
   prior rounds (short window to catch instability the long windows would smooth over; a quarter;
   two quarters flagged for circularity risk) while honestly changing the **unit** to the one TFF's
   own publication cadence actually supports.

| Window | TFF weekly observations | Real-time span | Carries forward from prior rounds |
|---|---|---|---|
| W1 | ~4 | ~1 month | The short window included specifically because a real short-window instability (the volatility round's own sign-flip) must not be dodged by only testing longer windows. At only ~4 observations this window is also the one most exposed to the sparsity Ambiguous-hold guard below (§4) — a new concern §4's mean-R round did not have to name, because ORB-MNQ-1 trades on ~99% of sessions and never got that thin. |
| W2 | ~13 | ~1 quarter | Matches the primary window from both prior rounds. |
| W3 | ~26 | ~2 quarters | Matches the long window from both prior rounds, where date-purity risked circularity (re-smoothing toward the calendar cut) in the volatility round. Checked directly here too, not assumed absent. |

**All three windows are pre-registered and all three are reported in the verdict — none dropped
after seeing a result. This is the single non-negotiable inherited unchanged from both prior
rounds** (§0, §6).

### §2.4 — The weekly-cadence objection: does it transfer to a one-time regime-shift check?

Reasoned explicitly, not assumed either way.

**What the prior rejections actually objected to.** Re-reading the concrete instances (§0):

- `2026-07-14-a4-flow-data-fork-scoping.md` (ES/ZN month-end): the event under test is a **3-day**
  T-3→T-1 window; weekly TFF "can only see the end-of-month *week*, not the window" — a **timing-
  resolution** failure, the report's snapshot interval is coarser than the event it needed to see.
- `Q-MCLTAS-1` (MCL settlement-window flow, `docs/rejected_candidates.md`): the event is a
  **2-minute** settlement print; weekly-and-lagged COT is even more mismatched — same resolution
  failure, more severe.
- `H-COTREV-6A` (AUD positioning-reversal, `CANDIDATE_ROWS.md`): proposed as a **live, tradable**
  entry-timing signal; "power-marginal at weekly event frequency" is partly a resolution complaint
  and partly a **statistical-power** complaint — too few independent weekly events accumulate over
  any realistic backtest span to power a trading rule.
- `MNQBASE-1` intake-dry closure: "weekly density, cross-sectional δ — dead," again in the context
  of sourcing a **live signal**, i.e. the same power/resolution bundle as `H-COTREV-6A`.

**In every documented instance, the objection's substance is a mismatch between the report's
snapshot interval and the timescale of the thing being measured or acted on** — either an event
lasting days-to-minutes (resolution), or a live decision needing to fire faster than weekly
(power/cadence for trading).

**This brief's question is neither.** It asks whether a **persistent regime state** (weeks-to-months
on either side of 2021-09-28) correlates with a **discrete, already-known calendar split** — it does
not need to see inside any single week, and it proposes no live decision to fire at any cadence.
A regime lasting months is exactly the class of phenomenon a weekly series is well suited to
resolve — coarse cadence is not blind to a slow-moving state the way it is blind to a 3-day flow
burst or a 2-minute print. **On the resolution dimension specifically, the objection does not
mechanically transfer.**

**What does transfer, honestly, and is not waved away:**

1. **Category impurity** (Asset Manager ≠ only "informed," Leveraged Funds ≠ only "crowd" — A4
   doc §2 point 3) is a **generic** concern about what the category actually contains, independent
   of cadence. It transfers unchanged and is disclosed as a scope limitation on any RESOLVED verdict
   (§5).
2. **Net-of-gross masking** (a real positioning shift can be buried in much larger gross category
   totals — A4 doc §2 point 4) is likewise cadence-independent and transfers unchanged.
3. **Off-futures expression** (A4 doc §2 point 2) is flagged as **genuinely unresolved, not
   dismissed**: the A4 fork's concern was instrument-specific (ES/ZN month-end rebalancing runs
   heavily through TRS/cash/dealer books). There is no established prior, positive or negative, for
   whether *whatever* drove ORB-MNQ-1's 2021-09-28 break similarly under-represents on MNQ futures
   TFF lines. This is carried as an open caveat on any RESOLVED verdict, not resolved by assumption
   in either direction.
4. **A new concern this brief must name, that the prior rounds did not have**: TFF-observation
   sparsity. The mean-R round never needed a trade-sparsity guard in practice because ORB-MNQ-1
   trades on ~99% of sessions; W1 here has only **~4** independent weekly observations before a
   rolling causal statistic is even well-defined. This is addressed as its own Ambiguous-hold
   trigger in §4, by the same logic (not the same numeric floor) as the mean-R round's `n<30` guard.

**Conclusion, stated plainly:** the weekly-cadence objection is a real, repeatedly-fired, and
correctly-applied doctrine in this repo for recurring/live-signal and sub-weekly-event use cases —
and it does not mechanically carry over to a one-time discrete-regime correlation check on a
months-long state. That does not make this candidate cadence-free: category impurity, net-of-gross
masking, and (newly) observation sparsity remain live, cadence-independent risks, named and gated
below rather than assumed away.

---

## §3 — Question (Q-ORBPOS-1)

**Pre-Q gate test:** symptom-only rephrase — "does a positioning-extremity classifier explain the
already-real pass-rate break, or does the break remain mechanistically unexplained" — names the
symptom (the break) and the missing thing (a tested positioning mechanism), not a specific fix or
deployment action. Passes, on the same basis Q-ORBCUSH-1's §3 passed.

**Q-ORBPOS-1:** Does a trailing, causally-computed classifier of CFTC TFF Leveraged Funds (primary)
or Asset Manager (secondary, fallback-only) net-position-as-%-of-open-interest — a candidate never
tested against this break, and not a re-tuned window on either already-refuted internal classifier
— produce regime buckets whose date composition and gate-clearance direction track the observed
2021-09-28 break, or does the break remain mechanistically unexplained after a third, genuinely
different candidate?

---

## §4 — Falsifiable hypothesis (H-ORBPOS) and frozen thresholds

**H-ORBPOS:** If a trailing (strictly causal — a given week's classification uses only TFF prints
already *published*, not merely dated, as of that week; no full-sample or global-percentile
threshold — the bucket-split threshold is the trailing series' own expanding, causal median, exactly
as the mean-R round used) percentile classifier of Leveraged Funds net %OI (primary) or Asset
Manager net %OI (secondary, fallback-only per the Ambiguous-hold clause below) produces two regime
buckets such that, at **at least 2 of the 3 pre-registered windows** (§2.3): (a) the higher-extremity
bucket's post-2021-09-28 date fraction is **≥75%**, (b) the lower-extremity bucket's post-2021-09-28
date fraction is **≤40%**, and (c) the gate-clearance direction (higher-extremity bucket clears the
frozen bust≤3.0%/pass≥50% gate under cushion sizing at k=1; lower-extremity bucket does not) is the
**same sign at every window tested, no exceptions** — **then** the mechanism is SUPPORTED;
**otherwise** (date-correlation fails at ≥2 of 3 windows, OR the direction sign-flips between any two
windows) the mechanism is REFUTED.

**Reject H-ORBPOS if:** the gate-clearance direction sign-flips between any two of the three
pre-registered windows (a single sign-flip anywhere is disqualifying, full stop — the identical
criterion that correctly refuted the volatility candidate), OR date-correlation fails the (a)/(b)
thresholds at 2 or more of the 3 windows (the identical criterion that refuted mean-R).

**Accept H-ORBPOS if:** date-correlation clears (a)/(b) at ≥2 of 3 windows AND direction is stable
(no sign-flip) across all three.

**Ambiguous-hold if any of:**

1. **TFF-observation sparsity** — W1 (~4 weekly observations) has fewer than **4** independent
   published TFF prints available in the covered pre-break span, or the trailing expanding-median in
   that window is degenerate (constant / zero variance, i.e. no actual split is possible).
2. **MNQ-not-separately-reported and combined-line share <10%** — the §2.2 contingency fires:
   MNQ's documented share of combined NQ+MNQ exchange volume/OI is under the pre-registered 10%
   floor, making the combined line judged unusable as an MNQ-specific proxy.
3. **Primary structurally unreliable and secondary also unreliable or itself
   Ambiguous-hold-triggering** — mirrors Q-ORBCUSH-1's own Ambiguous-hold shape: if (1) or (2) fires
   on the LF primary, re-run the identical three-window/threshold discipline on the AM secondary
   within this same brief (no fresh Q needed); if that also fails to produce a usable classifier,
   the whole candidate is Ambiguous-hold, not silently dropped or silently upgraded to a verdict.

**Order of operations is part of the pre-registration**, mirroring `Q-DRIFTEX-1`'s discipline
(§0): the §2.2 contingencies (separate-reporting check, 10% share check, category/column-name
confirmation) are resolved and **written into the RESULTS file** at Phase 0, strictly before any
position-value row is read. A RESULTS artifact that resolves a contingency and reads position data
in the same pass, without the frozen intermediate step, is void.

---

## §5 — Forbidden moves

- **Picking the reported window after seeing which one "works."** All three windows (§2.3) are
  pre-registered before Phase 1 runs; the verdict uses all three, never the best of three. The exact
  SNAG best-of-K pattern this repo already has a graveyard for (`lesson_snag_best_of_k_anchor_graveyard.md`).
- **Switching TFF category (Leveraged Funds ↔ Asset Manager) after seeing an initial null on the
  primary.** The **only** licensed route to the Asset Manager secondary is the §4 Ambiguous-hold
  trigger (sparsity or the combined-line-share contingency) — never "LF didn't show it, try AM."
- **Using a full-sample or global-percentile threshold to define the regime buckets.** Every
  classifier here must be strictly trailing (causal, respecting the TFF publication lag), verified
  by a second, independent implementation — not a re-read of the first — before any verdict is
  trusted, matching both prior rounds' own standard.
- **Retreating from %OI to raw net contracts, or vice versa, after seeing which one correlates
  better.** %OI is frozen as the sole normalization in §2.1, before any data is read, specifically to
  avoid the secular-open-interest-growth circularity trap.
- **Treating a SUPPORTED verdict as license to open `Q-POLFRONT-1`, propose re-opening the
  `Accepted` 2026-08-03 re-`PARK` ADR, buy a live TFF/positioning feed, or take any
  deployment-adjacent action.** Inherited verbatim from Q-ORBCUSH-1 §5 — this Q is explanatory only.
  A RESOLVED verdict establishes a mechanism for a **historical** pattern; it licenses nothing past
  what §6 states. This bar is if anything stronger here, since the A4 scoping doc (§0, §7) already
  ruled positioning data out-of-bounds as a **live tradable input** for this repo's discovery
  pipeline generally, independent of this brief's outcome.
- **Treating a REFUTED verdict here as casting doubt on the break's own reality or on the
  bust-elimination finding.** Both are separately, already triple-verified (Q-ORBCUSH-1 probe) and
  do not depend on this candidate's outcome.
- **Treating three clean nulls (volatility, mean-R, positioning) as automatic license to open a
  fourth ad hoc candidate at the same low bar.** §8 names this explicitly: a FALSIFIED verdict here
  raises, without yet mandating, an operator review of whether continuing to search for *any*
  mechanism behind this specific break is worth further K, ever.
- **Forbidden D-test:** filtering to only the TFF weeks/dates that fit a preferred positioning
  story, or restricting the sample to a sub-period chosen after seeing which sub-period correlates.
  Categorically forbidden — it encodes the conclusion into the analysis.
- **Reading this brief's cadence reasoning (§2.4) as blanket license to use TFF for any other,
  recurring or live-signal purpose on MNQ or any other instrument.** Scoped strictly to this
  one-time regime-correlation check. It does not reopen `Q-MCLTAS-1`, `H-COTREV-6A`, the
  `MNQBASE-1` intake-dry finding, or the general strategy-harvest channel-4 caution.
- **Running any part of Phase 0 onward without the separate, explicit operator GO named in §8.**
  This document is frozen and proposed; it authorizes nothing by itself.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` | H-ORBPOS's Accept condition fires (§4) | `INTEGRATE — record the mechanism (LF or AM positioning-extremity regime) in ops/instruments/MNQ.md as N20 (next open slot at draft time — re-check at closure time; N18/N19 are already taken, see §0), cross-referenced from this closure; disclose the category-impurity, net-of-gross-masking, and off-futures-expression caveats (§2.4) alongside the finding; does NOT reopen Q-POLFRONT-1 or the re-PARK ADR by itself, and does NOT license procuring a live TFF/positioning feed (§5)` |
| `FALSIFIED` | H-ORBPOS's Reject condition fires (§4) | `STOP — the 2021-09-28 break stays recorded as a real, triple-verified, mechanistically-unexplained historical pattern, now refuted against a third distinct candidate under the identical falsification discipline; ops/instruments/MNQ.md N20 (next open slot at draft time — re-check at closure time) records it; re-proposal bar = a genuinely different fourth candidate mechanism, not a re-tuned window/threshold/category on this one — and per §8, a fourth candidate should carry an explicit operator review of continued search value given three clean nulls` |
| `AMBIGUOUS-HOLD` | Any §4 Ambiguous-hold trigger fires and the AM secondary fallback also fails to produce a usable classifier | `ITERATE — return target: resolve the specific data-structure blocker (MNQ separate-reporting status, or a longer pre-break history if a future data vintage extends coverage); re-test window 2026-11-08, co-scheduled with the quarterly programme audit, same cadence Q-ORBCUSH-1 used for its own Ambiguous-hold route` |

---

## §7 — Execution plan (not authorized to run by this document — see §8)

- **Phase 0 — Rule-0 re-verify + contingency resolution.** Re-confirm §0 anchors still resolve.
  Resolve the §2.2 contingencies (MNQ separate-reporting status; combined-line share vs the 10%
  floor if applicable; exact CFTC column/category names) and **write the resolution to the RESULTS
  file before any position value is read** (§4 order-of-operations clause). Confirm the reporting-lag
  convention against the current CFTC TFF explanatory notes.
- **Phase 1 — Pull.** A single, narrowly-scoped CFTC TFF pull (free, no key) for the resolved
  MNQ-or-combined-NQ+MNQ line, Leveraged Funds and Asset Manager categories, full available history
  from contract launch (2019-05-06) through the current panel end (2026-07-15, per `RESULTS.md`).
  No other category, instrument, or date range is pulled under this brief.
- **Phase 2 — Classifier + gate-clearance check.** Build the trailing, causal %OI percentile
  classifier at the three §2.3 windows. Re-run the cushion-sizing gate-clearance check per bucket,
  per window, at k=1 — importing `day_loop_intraday` / `build_paths_orb` / `run_policy_orb` /
  `pol_cushion` / `pol_const` from the existing probe harness (§0) unchanged, exactly as both prior
  rounds did.
- **Phase 3 — Verification.** Independent, adversarial re-derivation of the classifier (a second,
  separate implementation, not a re-read) and a fresh end-to-end re-run, before any verdict is
  trusted — matching both prior rounds' standard.
- **Phase 4 — Verdict assertion.** Apply §6 against the actual §4-frozen thresholds; author the
  closure artifact (§9) and append `ops/instruments/MNQ.md` at the next open slot (**N20** at draft
  time — `MNQ.md` already carries N18/N19 from unrelated probes; re-check the ledger's current tail
  at closure time rather than trusting this number).

---

## §8 — Operator gate, K-accounting, and the Simons-stage-3 question

**Nothing in §7 may run without a separate, explicit operator GO recorded in this file's Change
History (or a superseding note) before Phase 0 begins.** This document is `FROZEN` and `PROPOSED`
only — the same posture `Q-DRIFTEX-1` used for its own unrun mechanism pre-registration (§0).

**K-accounting.** This is the same *class* of question as `Q-ORBCUSH-1` and `Q-GEOFIT-1`: a
diagnostic/explanatory probe into the mechanism behind an **already-real** historical pattern on a
**`PARKED`, non-live** legacy construct — not a strategy-candidate proposal entering the
discovery→validation pipeline. Following that precedent exactly:

- **K=0, $0.** No `discovery_manifests/` entry, no `register_search open` call. This is not a mined
  candidate with a search space to bind K over — like both prior rounds, it is a single, fully
  pre-specified classifier (two categories, three windows, one normalization, frozen before any data
  is read), the same shape `register_search` is not used for in Q-ORBCUSH-1 or its predecessor.
- **No `docs/rejected_candidates.md` row on FALSIFIED** — same convention as Q-GEOFIT-1 and
  Q-ORBCUSH-1: "mechanism-search null on an already-real pattern, not a strategy-mechanism
  rejection."
- **The external-mechanism harvest-intake admission requirements do NOT bind this brief.**
  `docs/methodology/strategy_harvest.md` §1's four requirements (economic grounding, cohort-cited
  δ/σ, family K-bank disclosure, confirm-power ≥0.50) gate a *seed entering the discovery→validation
  pipeline for live deployment* (§0). This brief proposes no strategy, no entry rule, no live feed,
  and — per §5 — is explicitly forbidden from being read as licensing one even on a SUPPORTED
  verdict. The channel-4 taxonomy note ("flagged power-marginal at weekly event frequency — check
  requirement 4 before manifesting") is read as applying to a *live signal* seed, which this is not;
  it does not silently exempt this brief from any live-signal use later, which would need its own
  fresh admission pass.
- **The trial is still tracked, honestly, as a trial.** This is the **third** candidate mechanism
  tested against the same regime break (volatility, mean-R, now positioning). Two clean nulls are
  already on record (Q-ORBCUSH-1 closure §5: "below the two-incident bar — watch... raises, without
  yet confirming, the possibility that this break is driven by something the estate doesn't have a
  good trailing-classifier vocabulary for yet"). A third null recorded here would not itself cross
  any hard N, but is pre-committed **now**, before the result, as a trigger for an explicit operator
  review of continued search value — not a silent fourth attempt at a lower bar (§5, §6).

**The Simons-stage-3 question, addressed directly.** `futures-anomaly-discovery/SKILL.md` (§0)
states plainly: *"Do not buy explanatory data (... COT) before a candidate has survived
validation; explanation is the last stage, not the first."* This names COT explicitly and cannot be
sidestepped. Reasoned resolution:

1. **The thing being explained has already survived the frozen gate.** ORB-MNQ-1 clears the
   bust≤3.0%/pass≥50% survivor-scoring gate in every post-break sub-window tested (the 2026-08-03
   re-`PARK` ADR re-`PARK`ed it on exactly this bar). This is not "explain a not-yet-validated
   mined candidate's edge to justify shipping it" — the failure mode Simons stage 3 exists to
   block. It is explanatory research on an **already-surviving** construct's own historical record.
2. **Even a SUPPORTED verdict cannot be used to justify shipping anything** — §5 forbids reading any
   result here as license for redeployment, reopening the re-PARK ADR, or procuring a live feed.
   The specific harm the doctrine guards against (explanation-as-cover for premature deployment) is
   independently blocked here regardless of outcome.
3. **The data is free.** "Buy" is not literally applicable — no $ decision is being made, and the
   cost-discipline half of the doctrine's rationale does not bind. This is not used as an excuse to
   skip the doctrine's *substance* (points 1–2 carry the actual argument); it is noted because the
   literal word "buy" in the source clause does not describe this action.
4. **Net:** the doctrine's concern — explanation used to rationalize shipping something unvalidated
   — does not fire here, because the candidate is already `PARKED` on its own validated (post-break)
   merits and no result from this brief can license redeployment regardless. Flagged and reasoned,
   not silently ignored, per Rule 0's extension to reading production doctrine as carefully as
   production code.

---

## §9 — Closure record format

- **If RESOLVED:** `docs/briefs/closures/Q-ORBPOS-1-closure-resolved.md`
- **If FALSIFIED:** `docs/briefs/closures/Q-ORBPOS-1-closure-falsified.md`
- **If AMBIGUOUS-HOLD:** `docs/briefs/closures/Q-ORBPOS-1-closure-ambiguous.md`, explicit re-test
  trigger 2026-11-08

Closure must include the mandatory typed `## Iterate` block per
`docs/adr/2026-08-04-iterate-closure-exit-mandatory.md`, and must append to `ops/instruments/MNQ.md`
at its then-current next open slot (**N20** at draft time; re-check — do not trust this number at
closure time) regardless of verdict (§6).

---

## §10 — Audit hooks (runnable)

```bash
# Confirm §0 anchors still resolve
git log -1 --format='%h' -- docs/briefs/Q-ORBCUSH-1-regime-break-mechanism.md            # expect b12689c
git log -1 --format='%h' -- docs/briefs/closures/Q-ORBCUSH-1-closure-falsified.md         # expect bcef3e0
git log -1 --format='%h' -- docs/briefs/pre-registration/Q-ORBCUSH-1-verdict-preregistration.md  # expect b84544a
git log -1 --format='%h' -- ops/instruments/MNQ.md                                        # expect 1e40b11 or later
git log -1 --format='%h' -- docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md     # expect 027a729
git log -1 --format='%h' -- lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/run_evalseq_orb_intraday.py  # expect b84544a
git log -1 --format='%h' -- docs/briefs/programs/2026-07-14-a4-flow-data-fork-scoping.md            # expect 027a729
git log -1 --format='%h' -- docs/methodology/strategy_harvest.md                          # expect fd0e6ee or later

# Freeze-before-run: this pre-registration predates any result artifact
ls lab/analysis/c1/q_orbpos_1_2026-08/ 2>/dev/null || echo "no results yet, as expected pre-run"
ls discovery_manifests/ | grep -i "orbpos\|tff" && echo "VIOLATION: seat spent before GO" || echo "OK: K unspent"

# No TFF/CFTC/COT data file has entered the repo under this brief
find core/data -iname "*tff*" -o -iname "*cftc*" -o -iname "*cot*" 2>/dev/null | grep -q . \
  && echo "CHECK: a TFF-shaped file exists — verify it predates or postdates operator GO" \
  || echo "OK: no TFF/CFTC/COT file present"

# No docs/rejected_candidates.md row exists for this candidate yet (expected until/unless FALSIFIED
# under the same no-registry-row convention as Q-GEOFIT-1/Q-ORBCUSH-1, in which case still none expected)
grep -i "orbpos" docs/rejected_candidates.md && echo "CHECK: unexpected registry row" || echo "OK: none, as expected"

# This brief's own operator-GO gate has not been exercised
grep -n "operator GO" docs/briefs/pre-registration/2026-08-22-orbcush-1-tff-positioning-mechanism-prereg.md
```

---

## Verification

```bash
python scripts/check_brief.py \
  docs/briefs/pre-registration/2026-08-22-orbcush-1-tff-positioning-mechanism-prereg.md --type inquire

# §0 anchors (see §10 for the full set)
git log -1 --format='%h' -- docs/briefs/Q-ORBCUSH-1-regime-break-mechanism.md
git log -1 --format='%h' -- docs/briefs/closures/Q-ORBCUSH-1-closure-falsified.md
git log -1 --format='%h' -- docs/briefs/pre-registration/Q-ORBCUSH-1-verdict-preregistration.md
git log -1 --format='%h' -- ops/instruments/MNQ.md
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-22 | Pre-registration authored and frozen. Phase 0 has not run. No operator GO recorded. | Claude Code (Sonnet 5), drafting on direction — **awaiting operator signature before any Phase 0 action** |
| 2026-08-23 | **Operator GO given** — Joshua, in chat: "take it up." Authorizes the full §7 execution plan (Phase 0 through Phase 4); K=0/$0 throughout per §8, no separate spend gate applies here (unlike MNQTAPE-1). | Joshua (GO) + Claude Code (execute) |
