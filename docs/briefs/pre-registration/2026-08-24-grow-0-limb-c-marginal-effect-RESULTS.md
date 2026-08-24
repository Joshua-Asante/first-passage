# GROW-0 Limb C — RESULTS: composite P(accept) at realistic and boundary-admissible target_sr

**Verdict (per condition, design note §4.3/§6):** as-run `CORROBORATED` · boundary `DIVERGED`
(measured **below** the closed-form estimate — the direction that *sharpens*, not softens, §1's
flagged boundary-power concern).
**Executed:** 2026-08-24 · Claude Code (Fable 5), execution-task session (see
[Authorization provenance](#authorization-provenance) below).
**Design note:** [`2026-08-24-grow-0-limb-c-marginal-effect-prereg.md`](2026-08-24-grow-0-limb-c-marginal-effect-prereg.md)
(`Status: PROPOSED`, unedited by this document or this session).
**Run artifacts:** [`lab/discovery/grow0_limb_c.py`](../../../lab/discovery/grow0_limb_c.py) ·
[`tests/test_grow0_limb_c.py`](../../../tests/test_grow0_limb_c.py) ·
[`discovery_manifests/grow0_limb_c_retry_ledger.jsonl`](../../../discovery_manifests/grow0_limb_c_retry_ledger.jsonl)
(run_id `grow0-limb-c-real-20260824T185851Z`) · additive `edge_dollars` extension in
[`grow0_dgp.py`](../../../lab/discovery/grow0_dgp.py) /
[`grow0_scoring.py`](../../../lab/discovery/grow0_scoring.py) (design note §9 items 1–2).
**Spend / K:** $0.00 · K=0 — synthetic data only, no Databento pull, no live-risk surface.
**Docks:** nowhere new. Outside the deep-iteration lane charter's §4 counters (same posture as
GROW-0 itself, design note header). Not a lane campaign; strikes nothing, resets nothing.

---

## Authorization provenance

**Stated explicitly, not silently assumed.** The design note's own Status line reads `PROPOSED`
and states the companion execution task awaits "a separate operator GO before the execution task
fires any draw." This document's own draws were executed under the explicit, itemized direction
of the task dispatch that spawned this session — which itself quoted the design note's
`PROPOSED`/no-GO status verbatim in its own orientation summary and then, with that status in
full view, issued an explicit numbered instruction to build the code and "Run both conditions for
real, at the frozen panel counts." That dispatch is read here as the "separate operator GO" the
design note's own header names as the precondition for execution — mirroring how GROW-0's own
harness build/run followed its prereg's GO by a separate step (design note header, same
language). No literal in the design note was changed, added to, or re-derived to make this run
happen (every frozen number was consumed exactly as pinned — verified in
[Verification](#verification)) and the design note file itself is untouched by this session
(`git log -1` on it, below, pre-dates this document). This section exists so a reader does not
have to infer the authorization chain from context — it is recorded here explicitly, for the
operator's own visibility, not resolved unilaterally.

---

## 1. Reporting table (design note §6, template now filled — every number below is a real
measured count from the frozen N=1,150-per-condition run, not a re-derived or hand-picked figure)

Run: `PYTHONPATH=lab;core python -m discovery.grow0_limb_c --run-id grow0-limb-c-real-20260824T185851Z --started-at 2026-08-24T18:58:51Z --prereg-commit e8f348d4177e6e44d1aa190273d7f9a25d8f7d12` — real wall-clock **10.19s** for both conditions combined (2,300 panels total).

| Quantity | Limb A (anchor, cited) | Limb B (anchor, cited) | Limb C (a) as-run (target_sr=1.8, N=1,150) | Limb C (b) boundary (target_sr=1.265, N=1,150) |
|---|---|---|---|---|
| P(nominee=5) | 100% (N=1) | N/A | **0.995652** [0.989862, 0.998142] (1,145/1,150) | **0.940870** [0.925713, 0.953091] (1,082/1,150) |
| P(gates pass\|nominee=5) | ≈100% | N/A | **1.000000** [0.996656, 1.0] (1,145/1,145) | **1.000000** [0.996462, 1.0] (1,082/1,082) |
| P(confirm clears\|nominee=5,gates pass) | real: 3.8200 cleared (≈3× margin) | N/A | **0.904803** [0.886425, 0.920475] (1,036/1,145) | **0.460259** [0.430753, 0.490046] (498/1,082) |
| **Composite P(accept)** | ≈1.0 (N=1) | real: 0.000909 (5/5,500) | **0.900870** [0.882240, 0.916830] (1,036/1,150) | **0.433043** [0.404675, 0.461858] (498/1,150) |
| False-abandonment rate | n/a | n/a | **0.0** [0.0, 0.003329] (0/1,150) | **0.0** [0.0, 0.003329] (0/1,150) |
| **§4.3 verdict** | n/a | n/a | **`CORROBORATED`** (closed-form 0.9095 ∈ CI) | **`DIVERGED`** (closed-form 0.4656 ∉ CI — above the CI's own upper bound) |

Every row above is population-scoped per the design note's own §8 discipline, restated here
explicitly: **P(nominee=5)** is measured over *all* 1,150 panels of the condition (every panel
plants the true edge as variant 5, by construction — this is the Limb C population, distinct from
Limb B's pure-null population). **P(gates pass\|nominee=5)** and **P(confirm
clears\|nominee=5,gates pass)** are conditioned on the `nominee==5` subset only (denominators
1,145 / 1,082, not 1,150). **Composite P(accept)** and **false-abandonment rate** are both
measured back over the full N=1,150 denominator — composite P(accept) counts only panels that
are `nominee==5 AND gates-pass AND confirm-clears` (the identical three-conjunct definition
Limb A's own PASS verdict uses); false-abandonment counts *any* gate-(a)/(b) failure on the
argmax nominee, **unconditional on which variant that nominee is** (per §8, a null variant that
wins the argmax and is then itself gated out is a false-abandonment event exactly as much as
variant 5 itself being gated out — both mean the true edge, which is present in every panel of
this population, never reaches a confirm read).

**Composite P(accept) telescopes exactly**, both conditions (0.995652×1.0×0.904803=0.900872≈0.900870
as-run; 0.940870×1.0×0.460259=0.433047≈0.433043 boundary; the 4th-decimal drift is round-trip
display rounding on the per-factor point estimates, not a measurement discrepancy — `accept_count`
is counted directly off the same three-conjunct filter, not computed by multiplying the rounded
factors).

---

## 2. Gaussian `deep_lane_power` cross-check (dispatch step 5 — the boundary condition, plus
as-run for contrast; the ACTUAL production function, not a hand re-derivation)

```
as-run:   deep_lane_power(target_sr=1.8,   floor_sr=1.265, years=6.5) = 0.913714
          measured P(confirm clears|nominee=5,gates pass) = 0.904803, CI [0.886425, 0.920475]
          0.913714 ∈ CI  ->  AGREES (formula's point value sits inside the measured CI;
          relative gap -0.975%)

boundary: deep_lane_power(target_sr=1.265, floor_sr=1.265, years=6.5) = 0.500000  (exact, z=0)
          measured P(confirm clears|nominee=5,gates pass) = 0.460259, CI [0.430753, 0.490046]
          0.500000 NOT in CI (CI's own upper bound 0.490046 < 0.500000)  ->  DIVERGES;
          relative gap -7.948% (measured sits below the Gaussian prediction)
```

**Explicit answer to the cross-check question:** at the as-run condition the Gaussian formula's
prediction agrees with direct measurement (small, CI-contained gap). **At the boundary condition
it does not** — the measured confirm-clear-given-nomination rate sits measurably (≈7.95%
relative, CI-excluding) below the Gaussian `z=0 → power=0.500` prediction. This is the same
directional pattern (Gaussian approximation overstates the true rate) GROW-0's own v2→v3 history
found for the pure-null population at a *different* operating point (`target_sr=0`, deep tail);
here it recurs for the edge-variant population at the z=0 boundary point specifically, and both
measurements are consistent with the same underlying cause the v3 prereg names for its own
population — the null DGP's win/loss mixture carries real skew (≈+0.34), and the CONFIRM
statistic's own sampling distribution is not exactly Gaussian, an effect that bites hardest
exactly where the target sits closest to the floor (least separation between the planted mean
shift and the null shape's own variance/skew structure), which is precisely the boundary
condition's own design point. **Per the instruction not to silently prefer one figure: the
Gaussian approximation is corroborated at as-run and refuted (measured-low) at boundary — stated
as measured, not asserted from the formula alone.**

Note the layering: this cross-check is on the **narrower per-§2 conditional power figure only**
(confirm-clear given nomination+gates). §1's own composite verdict (below) is a **separate,
independently-measured** quantity (accept_count/N, not derived by multiplying this figure by
anything) — both happen to diverge in the same direction at boundary, but that is a substantive
finding (both components of the story move the same way), not a definitional identity.

---

## 3. Interpretation — direct implications for the two named ox-alpha concerns

**Scope, stated precisely (mirrors the design note's own §6 framing):** this section reports
direct mathematical implications of the measured numbers above for the two concerns the ox-alpha
notice named (rows 2 and 14). It draws no conclusion about whether the deep-iteration lane charter
should be amended, whether a future campaign should be permitted to open at the boundary, or
whether the lane should continue — those are operator calls, informed by (not resolved by) the
numbers below.

### Row 14 — composite acceptance probability (previously never computed)

**Now measured, both operating points named in the design note.** At a realistic,
already-observed-in-practice target (as-run, target_sr=1.8 — DL-1/DL-2's own actual declared
target), the composite P(accept | true edge exists) is **0.9009** [0.8822, 0.9168] — high, and its
own closed-form pre-estimate (0.9095) is statistically consistent with the measurement
(`CORROBORATED`). At the charter's exact `POWER_MIN=0.50` admissible boundary, the composite is
**0.4330** [0.4047, 0.4619] — **below** both the naive "power=0.50 ⇒ accept≈0.50" reading *and*
the design note's own more careful closed-form pre-estimate (0.4656), which itself already sat
below 0.50 (`DIVERGED`, measured lower still). Population: Limb C's own boundary condition (a true
edge, planted at exactly `target_sr=floor`, present in every one of 1,150 panels) — not GROW-0's
own Limb A (SR=4.0, a different, far-more-generous population) or Limb B (no edge, the opposite
population).

### Row 2 — the falsifier's error rate at the admissible power boundary

Ox-alpha's own row 2 computed "up to 0.25" for two consecutive true-premise campaigns both missing
the confirm read, **using the charter's own declared `POWER_MIN=0.50` figure directly as if it
were the campaign's own accept probability.** The measured numbers above let this same
two-consecutive-miss arithmetic be recomputed with each successively more accurate accept-rate
input, all describing the identical boundary population (target_sr=floor):

| Accept-rate input | Source | P(a single campaign misses) | P(2 consecutive true-premise campaigns both miss) |
|---|---|---|---|
| 0.500000 | ox-alpha row 2, as sent (naive: power treated as accept rate) | 0.500000 | **0.250000** |
| 0.4656 | design note §4.1 closed-form composite pre-estimate | 0.534400 | **0.285583** |
| 0.433043 | **this run's measured composite point estimate** | 0.566957 | **0.321440** |
| 0.461858 | measured composite CI upper bound (most favorable end of the actual measurement) | 0.538142 | **0.289597** |
| 0.404675 | measured composite CI lower bound (least favorable end of the actual measurement) | 0.595325 | **0.354412** |

**Direct implication:** every measured value — including the *most favorable* end of the 95% CI —
produces a two-consecutive-miss probability **higher** than ox-alpha's own 0.25 figure. The
measured point estimate (0.3214) is ≈28% relatively higher than 0.25. This empirically confirms
what §1 of the design note flagged as an unvalidated projection ("ox-alpha's own '0.25' is itself
an understatement once nomination accuracy is priced in") — now stated as a measured finding, not
a flagged prediction. The mechanism is visible in the reporting table above: nomination accuracy
alone is *not* the problem at the boundary (P(nominee=5)=0.9409, closed-form-consistent) — the
composite is pulled down primarily by the confirm-clear-conditional rate sitting below its own
Gaussian prediction (§2 above), compounding with the (small, same-direction) fact that even a
correctly-nominated boundary-edge panel only clears the floor a little under half the time.

**What this does not say:** it does not say the charter's falsifier *should* be power-conditioned,
does not say a boundary-admissible campaign should be barred, and does not say the two real
campaigns to date (DL-1/DL-2, both declared at power≈0.96, nowhere near this boundary) are
affected by this finding at all — both real campaigns sit at the *well-margined* as-run-like
operating point, where this run's own numbers `CORROBORATE` the design's assumptions rather than
diverge from them.

---

## 4. False-abandonment: measured rate and an explicit scope caveat

**Measured: 0 abandonments in 2,300 panels (both conditions combined), Wilson upper bound 0.333%
per condition at 95% confidence.** Population: Limb C's own two conditions, where a true edge
(variant 5) is planted in *every* panel by construction — so this is a direct measurement of "how
often does GROW-0's own gate battery discard a panel that contains a real, marginal-or-realistic
edge," the exact quantity DL-1/DL-2's real abandonments could not answer (neither campaign's
family is known to carry a true edge — design note §1 item 2).

**Scope caveat, stated explicitly because it materially bounds what this number can support:**
GROW-0's harness — reused unmodified here, per the design note's own §9 contract — implements only
nomination gates (a) TRAIN net annSR > 0 and (b) average weekly active-day cadence ≥ 1/week
(`grow0_scoring.gate_a_passes` / `gate_b_passes`). **DL-1 and DL-2's own real abandonments were
driven by a wider battery** — gate 2a (net annSR, the same shape as GROW-0's gate (a)), gate 2b
(SPA consistent-p ≤ 0.10 over the full variant universe), and gate 2d (M-16 +1-tick
slippage-stressed re-scoring) — none of which GROW-0's harness implements, by the v3 prereg's own
explicit, deliberate design election (§5: "Adding an SPA/StepM ... gate to TRAIN nomination... was
genuinely considered ... and ruled out" specifically to keep Limb B's null-rate measurement
uncontaminated). **This measured ≈0% false-abandonment rate is therefore a statement about gates
(a)/(b) in isolation, at these two effect sizes — it is not a measurement of DL-1/DL-2's own full
abandonment battery, and must not be read as "a real marginal edge would rarely be abandoned by
the actual deep-lane gate set."** The mechanism for why (a)/(b) alone essentially never fire on an
argmax nominee — a positively-biased order statistic over 9–10 draws virtually always clears both
a >0 threshold and a cadence floor that is itself edge-invariant (§4.1) — is the *same* mechanism
GROW-0's own v3 prereg already established for its own populations (§6.1 step 4); this run adds
the edge-present-at-marginal-size population to that same finding, not a new mechanism.

---

## 5. What this does NOT license

- No charter amendment, no falsifier redesign, no ruling on whether `POWER_MIN=0.50` is "safe" —
  design note §6's own scope line, restated: this run tests only whether §4.1's closed-form
  approximation predicts the measured composite, at two points; it does not rule on lane policy.
- No re-classification of DL-1/DL-2's own abandonments — those remain what the deep-iteration
  lane charter's running-count line already records; this document adds a *different*,
  population-scoped measurement, not a reinterpretation of the two real campaigns.
- No claim about a *full* DL-1/DL-2-shaped false-abandonment rate (§4 above) — only gates (a)/(b)
  in isolation were measured, per GROW-0's own harness scope.
- No amendment to GROW-0's own `RESOLVED` closure, its frozen v3 prereg, `STATE.md`, or
  `SESSIONS.md` — none of these files are touched by this document or this session (verified
  below).
- No lane-continuation recommendation, per this task's own explicit scope boundary.

---

## Verification

Every command below was actually executed this session; output is pasted verbatim, not invented
or back-filled from expectation.

```bash
$ git rev-parse HEAD   # base_sha, captured as this session's first action
e8f348d4177e6e44d1aa190273d7f9a25d8f7d12

$ PYTHONPATH="lab;core" python -c "
from discovery.grow0_harness import run_limb_a
verdict, result = run_limb_a()
print('verdict:', verdict, 'nominee:', result.nominee, 'confirm_stat:', round(result.confirm_stat,4))
"
verdict: PASS nominee: 5 confirm_stat: 3.82
# Matches the GROW-0 closure's own cited number (confirm_stat=3.8200) exactly -- confirms the
# additive edge_dollars kwarg added to draw_daily_pnl / _score_all_variants / _nominate_and_gate /
# run_panel did not alter GROW-0's own frozen results (design note §5 forbidden-move check).

$ PYTHONPATH=lab;core python -m pytest tests/test_grow0_dgp.py tests/test_grow0_scoring.py \
    tests/test_grow0_harness.py tests/test_grow0_red_patch.py tests/test_grow0_grammar_file.py -q
39 passed in 15.81s
# GROW-0's own full existing suite, unchanged, run after the additive edit.

$ PYTHONPATH=lab;core python -m pytest tests/test_grow0_limb_c.py -q
21 passed in 3.35s
# This document's own new test suite (determinism, brentq edge-shape round-trip against BOTH
# frozen Limb C literals plus a sanity check against Limb A's own EDGE_DOLLARS=64.4412->SR 4.0,
# a new-root-vs-GROW0-root seed-collision spot-check, population-scoping hand-built fixtures,
# Wilson CI known-value check, retry-ledger append-only check).

$ time PYTHONPATH="lab;core" python -m discovery.grow0_limb_c \
    --run-id grow0-limb-c-real-20260824T185851Z \
    --started-at 2026-08-24T18:58:51Z \
    --prereg-commit e8f348d4177e6e44d1aa190273d7f9a25d8f7d12
# Full JSON output (both conditions) -- see §1's reporting table above for the extracted numbers;
# real wall-clock: 10.188s.

$ wc -l discovery_manifests/grow0_limb_c_retry_ledger.jsonl
1 discovery_manifests/grow0_limb_c_retry_ledger.jsonl
# Exactly one line, covering both conditions (design note §7) -- a separate file from GROW-0's
# own grow0_retry_ledger.jsonl (never commingled).

$ PYTHONPATH="lab;core" python -c "
from discovery.deep_lane_admission import deep_lane_power
print(round(deep_lane_power(target_sr=1.8, floor_sr=1.265, years=6.5), 6))
print(round(deep_lane_power(target_sr=1.265, floor_sr=1.265, years=6.5), 6))
"
0.913714
0.5
# The real production function, both conditions -- §2's cross-check.

# GROW-0's own frozen v3 prereg, RESOLVED closure, STATE.md, SESSIONS.md, and the Limb C design
# note itself are all untouched by this session -- each hash below is a real commit that pre-dates
# (or, for the design note, exactly equals) this session's own base_sha, none created by this task:
$ git log -1 --format=%H -- docs/briefs/pre-registration/2026-08-22-grow-0-synthetic-calibration-prereg.md
e21e80334c01e5c3334d997c7afbe158c5015697
$ git log -1 --format=%H -- docs/briefs/closures/GROW-0-closure-resolved.md
70029e6ccbe41e0b955ece7a7f210268e85ca7a7
$ git log -1 --format=%H -- STATE.md
447311f782fff0d35d4fd05d20023d072171df5d
$ git log -1 --format=%H -- docs/SESSIONS.md
4cee28f26153fe0b3dc259ca74aeccbf5aedec8b
$ git log -1 --format=%H -- docs/briefs/pre-registration/2026-08-24-grow-0-limb-c-marginal-effect-prereg.md
e8f348d4177e6e44d1aa190273d7f9a25d8f7d12   # the design-freeze commit; untouched by this session
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-24 | Results authored — first real execution of Limb C, both conditions, at the frozen N=1,150/condition design. as-run `CORROBORATED`, boundary `DIVERGED` (measured composite below the closed-form estimate) | Claude Code (execution-task session) |
