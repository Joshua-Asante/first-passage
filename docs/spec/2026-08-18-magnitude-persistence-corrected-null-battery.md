# SPEC — corrected-null battery for the magnitude-persistence screen class (FROZEN)

**Status:** `FROZEN 2026-08-18` — committed **before** any official scoring surrogate is drawn
(D6 ordering, step 1). Amendments after the official run = new spec, disclosed, never edits.
**Class:** `daily-range-state-persistence` and future magnitude-persistence screens
(Step-0 slate S1 family). **Supersedes** the retired `block_shuffle_conditional_p95` placebo
limb — incident: [audit note](../notes/audits/2026-08-18-block-shuffle-placebo-does-not-control-for-tr-autocorrelation.md).
**Provenance:** 4-lens design panel + synthesis (workflow `wf_ebc728eb-2ef`: surrogate-methods,
doctrine-fit, empirical breaker with live experiments on both panels, decision-consequences;
10 inter-lens disagreements resolved, 5 OPEN items carried honestly — full transcript in the
session task journal). Operator context: JA "take that on now, and identify how this affects
S1a's result" + ultracode re-enabled ("this is an important problem that deserves resources").
**Spend at freeze:** $0 · K unchanged (the S1a/S1b re-scores are re-measurements of already-
disclosed looks, not new looks; anything beyond the pre-named follow-ups here is new K).
**Retention-review:** 2026-11-08 (riding the standing slate date) — if no third
magnitude-persistence screen has consumed this battery by then, it gets a retention
test at the quarterly programme audit. Per
[`N-2026-08-18-iteration2-identify-notice.md`](../notes/notice/N-2026-08-18-iteration2-identify-notice.md)
§4 E(iii).

---

## §1 — D1: The corrected null (replaces the retired placebo limb)

**Method:** IAAFT (Schreiber–Schmitz) surrogates of the exact valid-TR sequence each pipeline
consumes (roll-excluded, weekend-filtered, NaN-dropped; n=2,177 GC / n=2,117 CL), each pushed
through the **byte-identical** frozen pipeline (`rolling_percentile_strict_prior` P80 → bias;
`rolling_percentile_through_today` P50 → outcome; conditional hit rate). The final step is
always a rank-remap onto the sorted original TR values — every surrogate is a reordering of the
actual value multiset (bitwise-exact marginal, asserted per surrogate).

**Generation domain:** **normal scores** (van der Waerden rank-Gaussianization), primary —
measured best rank-ACF fidelity (med max|Δ rank-ACF| lags 1–60: 0.0295 GC / 0.0269 CL), and the
pipeline is rank-based so rank dependence is what must be pinned. log-TR = documented fallback
only if scipy unavailable (scipy 1.17.1 confirmed present). **Raw-TR domain FORBIDDEN** —
empirically disqualified in design: its spike-inflated spectrum puts the entire null support
above both real statistics (GC min 0.6293 / CL min 0.6217), injects +0.11..+0.19 spurious
lag-1 rank-ACF, and flips CL to p_lower=0.005 — the opposite failure direction from the
invalidated shuffle.

**Iterations:** 100 (measured on the convergence floor: 100-vs-1000 paired-seed residuals
bit-identical). Escalation ladder on tolerance failure: 500 iterations → Schreiber end-matching
trim (≤2% of record) → **VOID** (§3 CASE V).

**M:** 1,000 per instrument. `p_upper = (1+#{r_i ≥ obs})/(M+1)`; `p_lower = (1+#{r_i ≤ obs})/(M+1)`.
**No M escalation on a near-miss, ever.** Any p within 0.02 of a referenced line is reported
BORDERLINE, never re-rolled.

**Seeds (official scoring block, provably disjoint from every design-phase draw):** surrogate
`i` for instrument X uses `np.random.default_rng([20260818, X_code, i])`, X_code GC=1 / CL=2,
i=0..999. Burned design-phase seeds (never reused): linear blocks 20260818+i and
+5000/+6000/+7000/+8000/+9000/+9500/+12000; scalars 101/303/777/424242/555/20260818–21; pilot
990000–990119. **Verification runs use pilot spawn-keys `[20260818, X_code, 990000+i]` only.**
CI limb keeps its frozen seed 42; retired placebo seed 7 retires with the old limb.

**Convergence diagnostic (gating, two-phase — written to disk BEFORE any surrogate hit rate is
computed):** ensemble median of per-surrogate max|Δ rank-ACF| over lags 1–60 ≤ **0.04** AND
p95 ≤ **0.07** (1.4× headroom over measured). Keep ALL surrogates (no selective discard — it
biases the band). Per-surrogate sorted-multiset identity assert. Signed per-lag median-deviation
table at lags {1,2,3,5,10,20,60} published. Gate failure after the full ladder → CASE V VOID;
the pre-named remedy is a different surrogate class (ARFIMA/FGN or GARCH-fitted) as a fresh
design decision with its own review (O5) — a VOID cannot be resolved opportunistically.

**Positive control (design-phase, cited not re-run):** 20 zero-mechanism AR(1) replicates each
scored against its own IAAFT band → 1/20 at p_upper ≤ 0.05 (correct nominal size), vs the
invalidated block-shuffle's 20/20 false-clear.

## §2 — D2: The corrected battery (standing for the class; presence GATES, attribution TYPES)

| Limb | Content | Certifies | Role |
|---|---|---|---|
| L1 | n-floors (pop ≥400 / cond ≥100) | measurability | GATES (verbatim carry) |
| L2 | 60d circular block-bootstrap CI lb > 0.50 (seed 42, 4000 draws) | existence + precision | GATES (verbatim carry) |
| L3 | both halves > 0.50 | coarse stability | GATES (verbatim carry) |
| L4 **NEW** | by-year floor: conditional rate > 0.50 in ≥ N_valid−2 of N_valid years (years with n_cond<20 excluded; N_valid ≥7 else AMBIGUOUS) | annual regime stability — the axis the incident exposed | **GATES**. Power reproduced at freeze: per-year n≈47, true 0.60 → P(≥7 of 9)=0.968; null false-pass 0.090 (exact binomial). Calm/crisis bucket read (median annual mean log-TR) = mandatory DISCLOSURE, not a gate |
| L5 **NEW** | IAAFT attribution limb per §1 | beyond-linear-ACF excess vs the series' own marginal+linear benchmark | **NEVER GATES — TYPES** |

**Verdicts:** **SIGNAL-EXCESS** (all presence limbs + p_upper ≤ 0.05; "mechanism" wording only
after the D22 GARCH(1,1)-on-log-TR sensitivity, M≥200, pre-registered seeds — IAAFT bounds
attribution to *linear* ACF, and the class grounding itself carries nonlinear ARCH dependence) ·
**SIGNAL-GENERIC** (presence passes, attribution doesn't — real, regime-stable, canon-attributed;
SURVIVAL-ONLY-class durability language; cannot discharge "mechanism-owed"; routes to a
conditioner-engineering prereg, never a mechanism-discovery campaign; still counts toward slate
§4 RESOLVED) · **NULL** (any presence limb fails; verdict line names the driving limb; an
L4-only NULL is a regime-instability kill, distinct from no-effect) · **AMBIGUOUS** · **VOID**
(diagnostic gate fails; no number from the run may be quoted; cells stay UNMEASURED).
**Flags (non-gating, mandatory when firing):** SUB-LINEAR (p_lower ≤ 0.05 — reads
"regime-concentration signature / extracts less than its own linear benchmark," never
"clustering absent"; bars canon-confirmed-at-canon-strength language) · ATTRIBUTION-FRAGILE
(p_att ∈ [0.03, 0.07]) · BORDERLINE (within 0.02 of a line).
**Excluded nulls:** AR(1) (strawman — measured +13pp band displacement vs full-spectrum;
lag-60 real ACF 0.19–0.27 vs AR(1) ~0); parametric nulls admissible only if their implied ACF
passes the same lag-set tolerance; HAR = optional RESULTS effect-size comparator, never the null.
**Anti-rescue guard:** both class verdicts sit at test-invalid; this battery supplies a FIRST
valid verdict only — it can never upgrade a standing kill.

## §3 — D3: Pre-registered interpretation for the S1a/S1b re-scores

Frozen observed (never re-derived): obs_GC = 0.5299334811529933 (n_cond 451; L2 lb 0.4545
**FAIL**) · obs_CL = 0.6282352941176471 (n_cond 425; L2 lb 0.5651 PASS). L1–L3 carried verbatim
from the committed results JSONs.

**Frozen predictions — the redesign predictably downgrades; it rescues nothing:**
**S1a re-scores NULL** (L2 fails in every non-VOID case). **S1b re-scores NULL** (L4 known-fail:
6 of 9 years > 0.50). Both then count as one valid NULL each toward the slate §4 tally
(2026-09-15 inertness date unchanged).

> ⚠ **Reader-intercept (2026-08-18, pre-official — see ADDENDUM-1 A1/A2 below):** the S1b
> prediction line above is a **prediction-miss** — the frozen L4 rule's own n_cond<20 exclusion
> (never applied by the "6 of 9" arithmetic) yields L4 PASS 6-of-8 on the actual per-year
> sample sizes, and the official verdict landed **SIGNAL-GENERIC**, per the addendum's
> mechanically-extended interpretation row. The S1a prediction held (NULL, CASE A). Rules
> govern; do not quote this §3 line without the addendum.

**S1a characterization rows (the operator's question):** CASE A (obs ≤ surrogate p50) — the
near-miss **dissolves**: 0.5299 is no more than GC's own marginal + linear ACF produces with
zero mechanism; MGC.md cell AMBIGUOUS-PARKED → NULL (measured, corrected null, p quoted).
CASE B (p50 < obs ≤ p95) — survives only as "above center, not significant" (quote the
percentile). CASE C (obs > p95) — "imprecise excess signature"; before citing anywhere, run the
pre-named crisis/calm decomposition (2011 = 0.7377 is GC's strongest year) under the corrected
null; remedy is precision (longer panel, re-open prereg + operator GO), never lane routing.
SUB-LINEAR flag possible (known-at-freeze: log-domain design preview p_lower 0.0180; ns M=150
0.0795 — the official ns M=1000 placement decides; the flag changes wording only, never verdict).

**S1b rows:** every non-VOID case reads NULL; the regime-concentration finding (crisis>calm
near-perfect ordering; drop-{2011,2014,2016} flips pooled; calm-subset independent NULL) stands
and is quoted in every cell. CASE A/B → typed-GENERIC wording ("predictability real at pooled
construction but canon-attributed AND crisis-carried"); MCL cell AMBIGUOUS-PARKED → NULL;
mechanism-owed UNCHANGED; the pooled L2 pass may never be quoted as a conditioner license — a
"canon-clustering conditioner" is a different claim (fresh prereg, new K, must confront the
calm-year NULL first). CASE C → annotate "beyond-linear excess signature, regime-unstable";
pre-frozen re-entry machinery for any future EXCESS: calm-subset re-score vs same-calendar-mask
surrogate p95 → drop-{2011,2014,2016} re-score → D22 GARCH sensitivity — all before any
beyond-canon wording; even a full pass licenses only a lane prereg.

**KNOWN-AT-FREEZE disclosure (every number seen before this freeze):** S1b per-year table; the
AR(1) audit band 0.72–0.80 (20/20 false-clear); obs values above; design-phase previews —
log-domain M=999: GC p_lower 0.0180 / CL p_upper 0.368 (real CL ≈ 63rd percentile of its band);
normal-scores M=150: GC p_lower 0.0795 / CL p_upper 0.3311; raw-TR M=200 verdict-flip; AAFT
inferior (spectrum-flattening, med log-ACF mismatch 0.018–0.030 vs IAAFT 0.010); iid-shuffle
band centers 0.499/0.500; burned-seed inventory (§1). **O4:** GC's per-year conditional table
is deliberately NOT in evidence at freeze — computed at scoring (L4's threshold cannot have
been tuned to it; verdict-irrelevant for S1a since L2 fails regardless).

**O2 disclosure — the 0.60 anchor is DECLARED-NOT-DERIVED.** L4's power derivation uses a
minimum-useful conditional rate of 0.60. No lens produced the connecting arithmetic from the 4×
cost hurdle to a required conditional rate (that arithmetic is owed to the conditioner-
engineering lane prereg that SIGNAL-GENERIC routes to, alongside O3's out-of-sample calibration-
lift gate). Its numeric proximity to obs_CL (0.6282) is disclosed. It anchors a power
calculation only; it gates nothing by itself.

> **Reader-intercept (2026-08-18, Q-CONDVAL-1):** the owed connecting arithmetic ran and
> **missed** — [`Q-CONDVAL-1-closure-falsified`](../briefs/closures/Q-CONDVAL-1-closure-falsified.md).
> `L_star`=0.4226 at the N-EDGE cell; measured C−U=0.1297. O2 is discharged. The 0.60 figure
> remains DECLARED-NOT-DERIVED (never an input). Conditioner-engineering branch PARKED.

## §4 — D5: S2/S3 un-pause conditions (replaces the blanket pause)

**S2 (overnight→day-session transmission): the S1 null does NOT port** — bias and outcome are
different series sharing a slow common vol state; joint surrogation preserves the effect under
test, independent surrogation deletes the mundane common-state confound (O1:
UNRESOLVED-NEEDS-DESIGN). Un-pause requires ALL of: (1) this spec's official re-score landed
with diagnostic PASS on ≥1 instrument; (2) S2 reframed INCREMENTAL with a stage-1 $0 cheap
falsifier first — does overnight-state conditioning beat matched day-session-history
conditioning (`bias' = 1{DS_{d−1} ≥ P80 trailing}`) on the same days? No increment → S2 dies
for $0; (3) if an increment exists, the stage-2 null design passes its own adversarial review;
plus the slate's operator GO. **S3 (EIA-day concentration): decoupled from IAAFT entirely** —
cross-sectional claim; un-pause = its prereg adopts a matched-day design (event days matched to
non-event comparators on trailing-60d TR percentile band) + paired median-ratio test with
year-block inference (weekly event spacing sits on raw ACF lag-5 ≈ 0.35, so iid tests stay
contaminated), and passes design review. Not gated on IAAFT.

## §5 — D6: Ordering, disclosures, propagation

Freeze (this commit) → implementation + adversarial verification on **pilot seeds only** →
official run (single execution per instrument; diagnostics to disk before any hit rate; no
parameter movement after results) → RESULTS addenda labeled RE-MEASUREMENT with old-battery vs
corrected-battery side by side, citing §3 case IDs, no extra characterization → propagation:
MECHANISMS.md → MGC.md/MCL.md cells + session logs → slate §2/§4 + pause lines per §4 → audit
note §5/§11 closure → strategy-validation §5 clause (panel D4 text) via the authoring path →
futures-anomaly-discovery battery-reuse note → memory updates → SESSIONS. Mandatory per-run
disclosures: multiset-identity assert; rank-ACF + log-ACF mismatch med/p95/max + tolerance
verdict; signed per-lag median-dev table; band summary (mean, sd, pct[2.5,5,50,95,97.5], M,
iterations, seeds); both one-sided p's + real percentile; per-year conditional table +
calm/crisis read; surrogate bands of bias=1 share and unconditional P(y=1) bracketing the real
values; AR(1) size-check citation.

---

# ADDENDUM-1 — 2026-08-18, pre-official (append-only; no frozen line above is edited)

**Provenance:** pilot run on sanctioned verification seeds surfaced a spec-internal conflict;
4-lens pre-official verification (workflow `wf_e06ebc90-c3e`: implementation-fidelity,
independent bit-exact reimplementation, freeze-integrity adjudication, statistical sanity) +
synthesis ruled **FIX-THEN-RUN** with the fork adjudicated **rules-govern**. This addendum
lands with the official seed block `[20260818, X_code, 0..999]` still undrawn (attested by
every lens; all draws to date used verification spawn-keys). Amending before the official run
is the one window where this is clean, per this spec's own header rule.

**A1 — The conflict, verbatim.** §2 L4 rule: *"by-year floor: conditional rate > 0.50 in
≥ N_valid−2 of N_valid years (years with n_cond<20 excluded; N_valid ≥7 else AMBIGUOUS)"*.
§3 prediction: *"S1b re-scores NULL (L4 known-fail: 6 of 9 years > 0.50)"*. Applied to actual
per-year n_cond (CL: 2010=14, 2011=55, 2012=42, 2013=42, 2014=66, 2015=37, 2016=51, 2017=47,
2018=71 — independently re-derived from the raw parquet by two lenses), the rule excludes 2010
(a failing year, rate 0.4286) → N_valid=8, required=6, n_pass=6 (2013 at 0.4762 and 2017 at
0.4681 fail) → **L4 PASS**, and the pilot verdict lands SIGNAL-GENERIC — a case with no §3 row.

**A2 — The ruling: rules govern; predictions are not gates.** The prediction-miss is disclosed
as such: "6 of 9" was correct arithmetic on rates alone but never applied the rule's own
exclusion clause; per-year n_cond was not in evidence at freeze (the committed
`s1b_results.json` by_year table carries rates only).

**A3 — Provenance defense.** The exclusion clause was design-panel consensus, appears verbatim
in the frozen D2 table, and was frozen before per-year n_cond existed anywhere in evidence —
the n<20 threshold cannot have been tuned to admit CL.

**A4 — Interpretation-table extension (mechanical from frozen D2 text; nothing here exceeds
it).** S1b case "presence passes + attribution GENERIC" → **SIGNAL-GENERIC**: SURVIVAL-ONLY-
class durability language; cannot discharge mechanism-owed; routes to a conditioner-engineering
prereg (never a mechanism-discovery campaign); counts toward slate §4 RESOLVED.

**A5 — L4 boundary-placement disclosure (three parts; no verdict modifier, no BORDERLINE flag —
a discrete count at threshold is not "a p within 0.02 of a line").** (a) n_pass=6 of required 6;
2013/2017 fail; 2010 excluded at n_cond=14; one flipped year flips the verdict — equally true
of the predicted FAIL. (b) Frozen operating characteristic (false-pass 0.090 / power 0.968 at
the representative profile) quoted beside the **realized 6-of-8 profile: false-pass 0.1178 /
power 0.9757**; the 2010-kept counterfactual (false-pass 0.0626 / power 0.9391; realized
verdict would be FAIL); per-excluded-year laxity ladder 0.0898 → 0.1445 → 0.2266. (c) Any
desire to tighten L4 routes to a forward-only new-spec decision for future class screens,
explicitly barred from re-scoring this run (symmetric anti-rescue: post-pilot tightening that
restores the predicted NULL is outcome-conditional test-hardening).

**A6 — Semantic guard-rails for the S1b official RESULTS addendum.** MAY: presence limbs pass
as frozen; attribution GENERIC; SIGNAL-GENERIC per D2 with SURVIVAL-ONLY durability; counts
toward slate §4 RESOLVED; conditioner-engineering routing only. MAY NOT: "regime-robust" or
"regime-stable" in any wording beyond *"L4 passed at its frozen threshold (6 of 8 valid years,
boundary-exact)"*; any "mechanism" wording (bar: D22 GARCH sensitivity first); citing the OLD
calm-subset placebo in either direction (it was the retired block-shuffle — VOID both ways; the
frozen §3 phrase "calm-subset independent NULL" is provenance-split: its CI component survives,
its placebo component is VOID); discharging mechanism-owed; quoting the pooled L2 pass as a
conditioner license; any magnitude-adequacy claim (O2 stands). The drop-cluster diagnostic and
the per-year table are co-quoted in every cell carrying the verdict.

**A7 — Calm/crisis bucket divergence.** The frozen disclosure buckets by LEVEL (median annual
mean log-TR); the 2026-08-18 adversarial review's split bucketed by crisis-event identity. They
disagree on transition years (2014/2016), moving CL's calm-bucket rate 0.537 → 0.617. The
disclosure bucket is non-gating by design; neither partition's read may be quoted without its
year list and definition attached; the calm-regime question is OPEN and is a named
confrontation item for any conditioner-engineering prereg.

**A8 — Anti-rescue guard, applied.** The guard bars upgrading a standing KILL; S1b's standing
NOT-CONFIRMED was a statement that the OLD test was invalid, not a valid NULL — the corrected
battery supplies the FIRST valid verdict, so no rescue occurs. Claim-strength ordering: the
voided raw SIGNAL claimed more than SIGNAL-GENERIC does — the battery downgraded the claim even
where the verdict string upgraded from the predicted NULL (obs_CL sits INSIDE its own null band,
72.5th pct at pilot, p_upper 0.2786).

**A9 — Rejected options, recorded.** (b) VOID-and-re-freeze: the frozen VOID pathway is CASE V
(diagnostic-gate failure), which PASSED; a discretionary VOID now would be outcome-visible.
(c) Hold-AMBIGUOUS: N_valid=8 ≥ 7 leaves no frozen AMBIGUOUS trigger. Both rejected as
injecting outcome-visible discretion.

**A10 — Convention ratifications (from the bit-exact reimplementation lens).**
(i) *Tie convention:* ordinal-stable (temporal tie order via stable argsort) RATIFIED — it is
what was frozen at 12877c4 and pilot-verified; the spec's "effectively continuous" rationale is
struck as factually false (tie share: GC 89.3%, CL 85.9% of observations share a value). Both
readings' numbers disclosed so the choice is demonstrably not outcome-shopped (mid-rank: GC
p_upper 0.9005 / p_lower 0.1045, obs 10.0th pct; ordinal: 0.9104 / 0.0945, 9.0th pct; CL
p_upper 0.2736 vs 0.2786). Verdicts and flags invariant under either.
(ii) *Diagnostic domain:* the gating tolerance was calibrated on **Spearman rank-ACF** (spec's
quoted 0.0295 reproduces only under that reading; 0.04/0.0295 = the stated 1.4× headroom) —
FIX-2 re-points the gate accordingly, tolerances untouched; z-domain kept as non-gating
auxiliary. Post-fix pilot: GC med 0.0308 / p95 0.0486 PASS; CL 0.0282 / 0.0415 PASS.
(iii) *p_att := p_upper* (FIX-1) — the attribution-typing p; the lower tail is separately owned
by SUB-LINEAR. (iv) *BORDERLINE:* broad reading ("within 0.02 of a referenced line" includes
0.03/0.07) assessed in the RESULTS addendum from the published p's; the runner's coded flag
remains 0.05-only, documented as such. (v) FIX-3: log-ACF mismatch now reports med/p95/max.

**A11 — Escalation-ladder execution recipe (pre-named, not improvised).** On official
diagnostic-gate FAIL: re-invoke with IAAFT_ITER=500 on the SAME official seeds → if still FAIL,
Schreiber end-matching trim ≤2% of record → if still FAIL, VOID per §3 CASE V.

**A12 — Seed-form disclosure.** Burned design-phase blocks were a mix of scalar
`default_rng(n)` and spawn-key forms as inventoried in §1; pilot spans `[20260818, X_code,
990000..990199]`, of which 990000–990119 deliberately duplicate design-phase draws
(deterministic re-verification); the official block `[20260818, X_code, 0..999]` is disjoint
from every burned form.

**A13 — Pre-named expected construction-sanity bracket failures at M=1000 (+ diagnosis).**
GC unconditional P(y=1) expected to fall BELOW its surrogate band (pilot: 0th pct, −3.74 SD)
and CL bias1-share marginal (0.5th pct, −2.23 SD): phase-locked panel-scale vol decline +
time-irreversibility — structure IAAFT cannot represent by construction; net effect biases the
GC conditional band UP ~+0.02 via the base rate. The lift-percentile line — real GC lift
(+0.0521 conditional-minus-unconditional) sits at the **41st percentile** of the surrogate lift
band, dead center — is attached wherever SUB-LINEAR wording could fire. CL clustering
under-match caution (~1.6 SD residual; implied band shift +0.013; obs plausibly ~45th pct under
a clustering-matched null): the 72.5th percentile is never quoted as near-excess evidence.

**A14 — SUB-LINEAR pre-commitment (GC official).** GC's official p_lower placement is reported
wherever it lands; the flag changes wording only, never verdict. P(flag fires by seed variation)
pre-estimated at **1.3–1.5%** (Jeffreys posterior predictive from pilot 0.0945 at M=200;
SE(p_lower) ≈ 0.009 at M=1000). If it fires, the wording MUST carry (a) the A13 lift-percentile
line (the low raw placement is predominantly a base-rate artifact of the band's upward bias)
and (b) the frozen guard: "regime-concentration signature," never "clustering absent." If
p_lower lands within 0.02 of 0.05/0.03/0.07, broad-BORDERLINE is reported. Report-never-re-roll
stands; no M escalation on any placement, ever. GC pilot summary: prediction-consistent, CASE A
(obs ≤ p50, 9th pct — the near-miss dissolves), no adjudication needed.

**A15 — Sequencing attestation.** FIX-1/2/3 + this addendum + refreshed pilot artifacts are
committed with the official seeds undrawn; the post-fix pilot re-run asserted every scoring
quantity bit-identical to the pre-fix pilot (generation and scoring untouched by the fixes).

**A16 — Operator election (PROCEED / HOLD only).** The fork materially changes the commissioned
consequence surface: S1b was represented as predicted-NULL (zero toward slate §4 RESOLVED); it
will now count toward RESOLVED and put the H-SLATE RESOLVED trigger live. Election is PROCEED /
HOLD; any request to edit L4 or re-freeze is declined and recorded as a forward-only new-spec
decision that cannot apply to this run. HOLD cannot un-know the pilot; this addendum stands
regardless of the election. Non-election items adjudicated as-is: verdict-precedence latent
path (L4-AMBIGUOUS ordering — unreachable here: GC N_valid=9, CL N_valid=8; recorded for any
future class spec); hard-coded verbatim-carry limbs (correct for this re-score; reuse hazard if
the runner outlives it).
