# GROW-0 Limb C — marginal-planted-effect extension: composite P(accept) at realistic and boundary-admissible target_sr

**Status:** `PROPOSED` — every design parameter below is pinned as a literal (design frozen);
**no panel has been drawn**. This document is the design-freeze step only, per this repo's own
G0-before-explore discipline (the same discipline GROW-0's own prereg followed) — awaiting a
separate operator GO before the execution task fires any draw. The originating operator
direction this session ("run the GROW-0 Limb C computation") is discharged *by* this
design-freeze step, not by a draw; the draw is a distinct, subsequent act with its own GO mark,
mirroring how GROW-0's own harness build/run followed its prereg's GO by a separate step.
**Authored:** 2026-08-24 · Claude Code (Fable 5), operator direction this session.
**Lane:** Same posture as GROW-0 itself — a synthetic calibration/measurement exercise, **outside**
the [deep-iteration lane charter](../../adr/2026-08-16-deep-iteration-lane-charter.md)'s §4
counters. Not a lane campaign; consumes no K, strikes nothing, resets nothing.
**Relationship to GROW-0 (additive, not a mutation):** [GROW-0's own v3 prereg](2026-08-22-grow-0-synthetic-calibration-prereg.md)
is `FROZEN` and its harness run is [`RESOLVED`](../closures/GROW-0-closure-resolved.md) (closed
2026-08-22) — **neither is touched, amended, or reopened by this document.** Limb C is a new,
separate measurement built on top of the same, unmodified `grow0_dgp.py`/`grow0_scoring.py`
primitives (extended additively per §9, never edited in their frozen constants). Limb A/B and
RED-LEAK/RED-BLIND/RED-PATCH are not re-run. **This document's own §6 verdict vocabulary is
deliberately distinct from GROW-0's own RESOLVED/FALSIFIED** (see §6) precisely so the two can
never be confused on a future grep.
**Authorizes:** nothing beyond this design freeze. No code is written or executed by this
document (no `.py` file, no draw). The companion execution task — separate, its own operator GO —
builds the §9 interface extension and performs the actual panel draws.
**Spend:** $0 / K=0 — synthetic data only, no Databento pull, no live-risk surface (identical
posture to GROW-0 itself).

---

## §0 — Rule-0 reads (this session @ `bcaaaa5`, 2026-08-24)

| Source | Anchor | Supplies |
|---|---|---|
| [GROW-0 prereg v3](2026-08-22-grow-0-synthetic-calibration-prereg.md) | full read, this session | §2 frozen grammar (K=10, θ\*=index 5); §3 frozen DGP (`NULL_PARAMS`, edge = pure location shift, `EDGE_DOLLARS=64.4412` solved via `brentq`); §4 N-sizing discipline (measure, don't extrapolate) — this document's own §4 mirrors that section's dual job (N-sizing **and** the falsifiable H together, same template shape); §6.1/§6.2 procedure (argmax nomination, gates a/b, one CONFIRM read); Revision record (the v1/v2/v3 error classes named in the dispatch) |
| [`grow0_harness.py`](../../../lab/discovery/grow0_harness.py) / [`grow0_dgp.py`](../../../lab/discovery/grow0_dgp.py) / [`grow0_scoring.py`](../../../lab/discovery/grow0_scoring.py) / [`grow0_red_patch.py`](../../../lab/discovery/grow0_red_patch.py) | full read, this session | Actual code, not the prereg's prose gloss: `draw_daily_pnl(seed, *, n_days, edge: bool)` reads a **module-level** `EDGE_DOLLARS` constant, not a caller-supplied value (§9 below is the direct consequence); `build_root_branches`/`spawn_panel_streams`'s exact hierarchical `SeedSequence` shape (§7 below reuses it verbatim); `_nominate_and_gate`/`run_panel`'s three-return-tuple shape and gate order |
| [Deep-iteration lane charter](../../adr/2026-08-16-deep-iteration-lane-charter.md) | full read, this session | §2.2(iii): `POWER_MIN=0.50` binding refusal floor, Gaussian approx `se≈1/√years`, worked example "target at-the-bar → power 0.50 → boundary-admissible" — the exact concept §2(b) below instantiates at GROW-0's own K=10/6.5y point; §4 yield limb counts confirm-read failures **and** post-confirm N-SURV/fragility deaths as strikes, with no power-conditioning anywhere in the falsifier text (verified: `grep -n "POWER_MIN"` and the yield-limb clause both read directly, not from a summary) |
| [DL-1 prereg](2026-08-16-deep-lane-dl1-mgc-orc-prereg.md) §0/§4 | full read, this session | Declared `target_sr=1.8` for the nominee; power **0.959** at the *campaign's own* 7.62y confirm (`floor_at_k(10,7.62)=1.170`) — a different (longer) window/floor than GROW-0's own 6.5y/1.265, so DL-1's own power figure is **not** reused numerically here (§2 recomputes at GROW-0's own point); both real campaigns ran well-margined, not at the boundary |
| [DL-2 prereg](2026-08-22-deep-lane-dl2-m6a-pdhpdl-prereg.md) §0/§4 | full read, this session | Same `target_sr=1.8` design point (charter's own GO-2 point cited up to 1.83); power **0.9592** at 7.6386y (`floor_at_k(10,7.6386)=1.170`); both DL-1 and DL-2 died at the **train gate** (abandonment), confirm never read either time — the real-world instance of the "does a real signal get killed at the train gate" question this Limb measures |
| [ox-alpha deep-lane design review](../../notes/notice/N-2026-08-24-ox-alpha-deep-lane-design-review.md) | full read, this session | Row 2 (falsifier error-rate coupled to per-campaign power, up to 0.25 mutual-miss at the POWER_MIN boundary — genuinely new finding); row 3 (selection-adjusted/winner's-curse power never computed — declared power is for a random variant, not the argmax survivor); row 14 (composite acceptance probability through the full stacked gate set never computed) — §2 of that notice names the concrete follow-up this document discharges |
| [GROW-0 closure](../closures/GROW-0-closure-resolved.md) | read this session (not a Rule-0-listed source in the dispatch, read because this document's own §6 anchors on its actual numbers, not the prereg's predictions) | Real executed numbers, not predictions: Limb A (N=1) nominee=5, `confirm_stat=3.8200` (PASS); Limb B (N=5,500) `sum_clears=5` (PASS, `<c=7`) — both independently re-derived, bit-for-bit reproducible off the frozen `SeedSequence` root `20260822` |
| [`lab/research_utils/axis_screen.py`](../../../lab/research_utils/axis_screen.py) | executed this session (§10) | `floor_at_k(10, years=6.5)` reproduces **1.265** — reused verbatim, not re-derived |

**Executed dedup / amend-first search (Rule 8.8/8.10, pasted):**

```
$ grep -rlniE "limb.c|limb_c|marginal.planted|grow0_limb_c|grow-0.*limb" \
    lab/discovery/ lab/research_utils/ tests/ docs/spec/ docs/briefs/pre-registration/ \
    docs/adr/ docs/notes/audits/ docs/notes/notice/ docs/briefs/closures/
docs/briefs/INDEX.md
```

(1 hit, checked and disambiguated — **not** a prior GROW-0 Limb C: `docs/briefs/INDEX.md` lines
62/106 use "Limb C" as the third sub-test of two unrelated Q-briefs, `Q-STATVALID-1` and
`Q-DATAFIDELITY-1`, each numbering its own H's sub-limbs independently — same label, disjoint
subject matter, no relation to GROW-0. No prior GROW-0 Limb C artifact exists on any of the
searched surfaces.)

Owner: this file. Docks nowhere new — no counter, no clock, no K (§ "Lane" above).

---

## §1 — Context: what Limb C measures (the named gap, not a re-test of GROW-0 itself)

GROW-0's own Limb A plants `SR=4.0` — deliberately generous, confirm-clear probability
≈1.00000000 by design (prereg §3: "GROW-0 is not testing whether the engine can detect a
*marginal* edge... A generous, unambiguous edge makes Limb A a near-deterministic test of
plumbing correctness"). That is explicitly out of Limb A's own scope, named as such in the
prereg it extends. Three questions that generous-edge design cannot answer, all flagged by the
ox-alpha review (§0 above) and none previously measured by any artifact in this repo:

1. **Selection/nomination accuracy at a realistic effect size.** Does `argmax` over 9 nulls +
   1 real-but-marginal edge actually find the edge, or does it sometimes lose to noise? (ox-alpha
   row 3: declared power is computed for "a random variant," not the argmax survivor's own
   winner's-curse-shrunk detection odds.)
2. **False-abandonment rate under a marginal true edge.** DL-1 and DL-2 both died at the train
   gate (nominee failed gate 2a/2b, confirm never read) — real instances of a real family's
   candidate never reaching a confirm read. Neither campaign's family is known to have carried a
   true edge, so those deaths cannot answer "does the train gate kill *real* signal at a
   comparable rate" — only a planted-true-edge harness can.
3. **Composite end-to-end P(accept | true edge exists)** through the full nominate → gate →
   confirm stack, at target_sr values a real campaign would actually declare — not the
   near-certain SR=4.0 case (ox-alpha row 14).

**Sharpened by ox-alpha row 2, the concrete trigger for this Limb:** the charter's own §2.2(iii)
admits a campaign at `POWER_MIN=0.50`, and §4's yield limb ("2 consecutive completed lane
campaigns whose nominated survivor fails the confirm read... ⇒ FALSIFIED") carries **no
power-conditioning** — at the admissible boundary, two true-premise campaigns can both miss with
probability up to 0.25 **if** the campaign's own confirm-clear probability really is 0.50. That
figure assumes the declared power *is* the correct-nominee's true detection odds. §4's own
closed-form pre-estimate below (not yet measured) suggests it may not be — the boundary
condition's estimated composite P(accept) sits **below** 0.50, which, if confirmed by direct
measurement, means ox-alpha's own "0.25" is itself an **understatement** once nomination accuracy
is priced in. Stated here as a flagged projection from an unvalidated closed form, exactly the
class of claim this document's own methodology (§2/§4) refuses to assert without the follow-on
measurement.

**Tempered, not eliminated, by the real record (§0 rows 4/5):** DL-1 and DL-2 both declared
`target_sr=1.8` (up to the charter's own 1.83 point) at power **0.959–0.9592** — comfortably
inside the well-margined regime, nowhere near the 0.50 boundary. Nothing in the charter is
currently pushing campaigns toward the boundary. But nothing structural in the charter *prevents*
a future campaign from opening there either — §2.2(iii)'s refusal rule is a **floor**, not a
target, and the boundary case is explicitly named as "admissible" in the charter's own worked
example. This Limb measures the engine's actual behavior at both points so that if a future
campaign ever does open near the boundary, the operator has a measured number instead of a
theoretical one.

**Explicit scope boundary (named, not silently dropped, mirroring GROW-0's own §1 discipline):**
Limb C does **not** re-run RED-LEAK/RED-BLIND/RED-PATCH — GROW-0's own `RESOLVED` closure already
establishes the plumbing/calibration is sound; re-testing it here would be redundant, not
additive. Limb C does **not** sweep additional `target_sr` values beyond the two named in §2 (a
denser sweep is a natural follow-up, out of this design's scope). Limb C does **not** change `K`
(stays fixed at GROW-0's own frozen 10-variant grammar) or touch `floor_at_k`'s constants. Limb C
does **not** amend, waive, or rule on the charter's own `POWER_MIN=0.50` floor or two-strike
falsifier — §6's gate tests only whether a closed-form approximation held up under measurement; any
consequent charter change is a separate, future, operator-elected act under its own ADR process,
not this document.

---

## §2 — Two target_sr conditions

Both evaluated against **GROW-0's own frozen `floor_at_k(10, 6.5) = 1.265`** (reproduced live,
§10) — **not** the real campaigns' 7.6-year window. This is a deliberate choice, stated
explicitly: reusing GROW-0's own 6.5-year confirm convention keeps Limb C's numbers directly
comparable to Limb A's and Limb B's own already-measured figures (§6's anchor table) on the same
floor/years basis. Switching to the real campaigns' `floor_at_k(10,7.6)=1.170` would require
re-deriving a different floor and lose that comparability — the whole point of calling this an
*extension* of GROW-0 rather than a freestanding measurement.

**(a) "As-run": `target_sr = 1.8`** — the real campaigns' actual declared target (DL-1/DL-2, §0).

**(b) "Boundary": `target_sr = 1.265`** — exactly GROW-0's own floor, i.e. `z=0` under the
Gaussian approximation, i.e. the charter's own §2.2(iii) `POWER_MIN=0.50` admissible edge,
instantiated at GROW-0's own K=10/6.5y point rather than the charter's own K=33 illustrative
example (the underlying identity — target=floor ⇒ Gaussian power=0.500 exactly — is K/years
-invariant, so this is a direct instance of the same named concept, not an analogy).

**Gaussian-approximation power (same formula the charter's §2.2(iii) and GROW-0's own prereg use
— `z=(target_sr−floor)×√years`, `power=Φ(z)` — computed live, §10):**

| Condition | target_sr | z | power (Gaussian, CONFIRM-side conditional-clear only) |
|---|---|---|---|
| (a) as-run | 1.8 | 1.363988 | **0.913714** |
| (b) boundary | 1.265 (= floor) | 0.000000 | **0.500000** (exact, by construction) |

**This formula answers a narrower question than "P(accept)."** It is the probability CONFIRM
clears the floor **given** the true-edge variant was correctly nominated and passed the gates —
exactly the quantity ox-alpha row 3 says is misleadingly reported as "declared power" when what
actually matters is the *composite*, selection-inclusive rate. **Per the known-error-class
guidance this document is bound by (GROW-0's own v2→v3 lesson): this Gaussian figure is stated
here, then set aside as a planning input, not trusted as the answer.** §4's panel-count arithmetic
uses a closed-form *composite* pre-estimate (P(nominee=5) × P(gates pass) × this power figure,
derived in §4 by numerical quadrature — still no RNG draw, a deterministic integral, not a
simulation) purely for **sizing and as the falsifiable H's own target value**; the execution
task's job is to **measure** all three factors and the composite directly via the panel Monte
Carlo, exactly as GROW-0's own v3 measured `nominal_p0` directly rather than trusting
`deep_lane_power`'s far-tail extrapolation. This applies with the most force at the boundary
condition (z=0), the same shape of far-from-validated tail point that burned GROW-0's own v2.

---

## §3 — Edge shape (identical construction to Limb A, brentq-solved)

Identical to the prereg's own §3 "Edge shape": a pure location shift of the same null DGP
(`NULL_PARAMS` in `grow0_dgp.py`, read verbatim, not re-typed from memory) — `edge_dollars` added
to both `win_mean` and `loss_mean` on active days, leaving the active-day null variance
(`var_y = 37,580.7276`, `sd = 193.857493`, matching the prereg's own cited `193.86`, confirming
identical parameterization) unchanged. Solved via `scipy.optimize.brentq` against the target SR,
on the **same closed-form annualization** the prereg's own §10 audit hook uses (`daily_mean =
p_active × edge_dollars`; `daily_var = p_active × var_y + p_active(1−p_active) × edge_dollars²`;
`ann_sr = daily_mean/√daily_var × √252`) — same deliberate <0.03%-relative simplification the
prereg itself disclosed (dropping the null shape's own +$0.02/day contribution), reused for
consistency, not re-litigated. Round-trip-verified (§10): `ann_sr(edge_dollars)` reproduces each
target to 5 decimal places after rounding to the frozen 4-decimal literal.

| Condition | target_sr | `edge_dollars` (frozen) |
|---|---|---|
| (a) as-run | 1.8 | **28.5002** |
| (b) boundary | 1.265 | **19.9857** |

(For scale: Limb A's own frozen `EDGE_DOLLARS=64.4412` solves `ann_sr→4.0000`. Both Limb C
conditions are smaller shifts, monotonically, as expected for smaller target SRs against the same
variance structure.)

---

## §4 — Panel count and falsifiable H

Three sub-parts, mirroring GROW-0's own §4 dual job (N-sizing **and** the falsifiable H in one
section): a closed-form composite pre-estimate used only for sizing (§4.1), the panel-count
arithmetic it feeds (§4.2), and the falsifiable H that pre-estimate itself becomes the target
value for (§4.3) — the same "measure, don't just trust the closed form" discipline GROW-0's own
v3 applied to `nominal_p0`, applied here to a genuinely new pair of operating points.

**§4.1 — Composite pre-estimate (planning input, deterministic — no draw).**

`P(nominee=5)` is estimated by treating each variant's TRAIN annualized-Sharpe statistic as
approximately Gaussian with `se = 1/√6.5 = 0.392232` (the same se-approximation the charter and
every prereg in §0 use throughout) — the edge variant ~ N(target_sr, se²), the 9 null variants ~
N(0, se²) iid (null population mean SR = 0.0013 per the prereg's own §3, negligible against
se=0.392, treated as 0). `P(nominee=5) = P(edge draw > max of 9 iid null draws)`, evaluated by
deterministic numerical quadrature (`scipy.integrate.quad`, not a simulation — §10 pastes the
exact command). `P(gates pass | nominee=5)` is bounded analytically: gate (a) fails only if **all
10** variants' TRAIN stats are simultaneously ≤0, which factors as `P(9 nulls≤0) × P(edge≤0) =
0.5⁹ × Φ(−target_sr×√6.5)` — negligible at both conditions; gate (b) is edge-invariant (cadence
is governed by `p_active=0.60` alone, untouched by a location shift on win/loss magnitude, so its
near-100% pass rate carries over unchanged from the prereg's own measured figure). Composite
pre-estimate = product of the three factors:

| Condition | P(nominee=5) [quadrature] | P(gates pass\|nominee=5) [analytic] | power (§2) | composite pre-estimate |
|---|---|---|---|---|
| (a) as-run | 0.995415 | 0.99999998 | 0.913714 | **≈0.9095** |
| (b) boundary | 0.931110 | 0.99999877 | 0.500000 | **≈0.4656** |

These are closed-form planning estimates, explicitly not trusted as ground truth (§2) — they are
**the target value §4.3's falsifiable H tests against**, not a claimed result.

**§4.2 — Panel count (SE-of-proportion, worst-case-anchored).**

For **sizing**, panel count is anchored to the **worst case** `p=0.5` (the proportion value that
maximizes `p(1−p)`, hence the required N, for *any* target SE) — this sidesteps reliance on
§4.1's own possible error for the one place (the statistical guarantee on achieved precision)
where being wrong would matter: at N sized this way, the achieved SE is `≤` the target
**regardless of where the true composite rate actually lands**, for either condition.

`N = p(1−p)/SE_target²` at `p=0.5`, target SE = 0.015 (1.5 percentage points — tight enough to
resolve the two conditions' own composite estimates, ≈44 points apart, and either of them from
Limb A's real ≈1.0 or Limb B's real ≈0.0006/0.0009 anchor, with enormous margin):

```
N_raw = 0.25 / 0.015² = 1,111.11  ->  ceil = 1,112
```

Rounded up for cleanliness (a small additional pad, in the same spirit as GROW-0's own
5,000→5,500 round-up, though here the worst-case anchor already carries its own margin):

**N = 1,150 panels per condition (2,300 total across both Limb C conditions)** — achieved
worst-case SE at N=1,150: `√(0.25/1150) = 0.01474 ≤ 0.015` ✓. Far fewer than Limb B's 5,500 (as
expected: P(accept) at a real marginal edge is far from Limb B's tiny null rate, so far less
replication is needed for comparable precision) — per-condition N here is about **1/5th** of
Limb B's, and even the combined two-condition total (2,300) is well under half.

Each condition is sized and run independently (own N, own seed branch, §7) — mirroring GROW-0's
own precedent of sizing each limb to its own statistical demand (Limb A: N=1, near-deterministic;
Limb B: N=5,500, a tiny rate needing many trials), not forcing one N onto structurally different
measurement problems.

**§4.3 — Falsifiable H (per condition).**

**H:** the panel Monte Carlo's measured composite P(accept) for a condition has a 95% Wilson CI
(§6 formula) that **contains** §4.1's own pre-registered closed-form estimate for that condition
(as-run: ≈0.9095; boundary: ≈0.4656) — i.e., the Gaussian-approximation-plus-quadrature planning
estimate is a statistically consistent predictor of the directly measured rate, the same
"does the closed form match reality" question GROW-0's own v1→v2→v3 history was fundamentally
about, applied here to two operating points (a realistic target and the exact admissible
boundary) neither previously measured by any artifact in this repo.

**H fails** (per condition, independently) if the measured composite's own Wilson CI **excludes**
§4.1's closed-form estimate. This is a genuine, disclosure-worthy finding either way, not a
project failure — direction matters and must be reported: measured-below-estimate **sharpens**
the boundary-power concern named in §1; measured-above-estimate **softens** it. (Mirrors exactly
what GROW-0's own v2→v3 transition discovered — the Gaussian formula *was* found to diverge from
the measured rate at a far tail point, and that divergence was the substantive finding, not a
defect in the exercise.)

**H holds** if the CI contains the estimate — reported as evidence the planning-time
approximation was trustworthy at that operating point.

Evaluated independently for each condition — a divergence at the boundary condition does not
imply one at as-run, or vice versa (they are separate populations, separate seed branches, §7).

---

## §5 — Forbidden moves

- **Reading a CONFIRM draw before its paired TRAIN nomination completes**, or re-drawing CONFIRM
  after seeing a result. One nominee, one CONFIRM draw, per panel, ever — same rule as GROW-0's
  own §5, imported verbatim.
- **Touching this document's frozen literals** (target_sr values, edge_dollars, N, root seed)
  after any panel has been drawn. A defect found post-draw supersedes with a fresh ledgered
  document, never an in-place edit — same discipline as GROW-0's own §5.
- **Editing `grow0_dgp.py`'s or `grow0_scoring.py`'s existing frozen constants or existing call
  sites' behavior.** §9's interface extension must be additive-only (new optional parameters,
  default-preserving) — GROW-0's own Limb A/B/RED-LEAK/RED-BLIND results (already `RESOLVED`,
  closed) must remain bit-for-bit reproducible off the unmodified `20260822` root after Limb C's
  code lands.
- **Reusing or perturbing GROW-0's own root SeedSequence (`20260822`) or any of its five existing
  branch names.** Limb C's root (`20260824`) and its two condition branches are new and separate
  (§7).
- **Blending false-abandonment with selection failure**, or reporting either as a proxy for the
  other (§8) — the population-mislabeling error class this document is explicitly bound to avoid.
- **Treating §4.1's closed-form numbers as measured results, or §4.3's H as a policy verdict.**
  They are planning estimates and a methodological consistency test, respectively — every
  reporting cell in §6 is `TBD` until the panel Monte Carlo actually runs, exactly per the
  known-error-class guidance (GROW-0's own v2→v3 lesson).
- **Amending, waiving, or ruling on the charter's `POWER_MIN=0.50` floor or its two-strike
  falsifier from this document.** Limb C produces numbers and a narrow approximation-validity
  verdict (§6); any consequent charter action is a separate, future, operator-elected ADR act.
- **Confusing this document's own §6 verdict vocabulary with GROW-0's own RESOLVED verdict.**
  GROW-0's closure is untouched and unaffected by anything in this document (header block).
- **Touching `STATE.md`, `SESSIONS.md`, or GROW-0's own frozen v3 prereg file.** Not in scope for
  this task; not touched by it.

---

## §6 — Gate / verdict criteria

**Scope, stated precisely (not a policy verdict):** this gate tests only whether §4.1's
closed-form approximation is a trustworthy predictor of the directly measured composite rate at
each of the two operating points (§4.3's H). It does **not** rule on whether the charter's own
`POWER_MIN=0.50` floor is "safe," whether a boundary-admissible campaign should be permitted, or
whether the falsifier should become power-conditioned — those are policy questions for the
operator, informed by (not resolved by) the measured numbers this Limb produces.

**Verdict vocabulary (per condition; deliberately distinct from GROW-0's own top-level
RESOLVED/FALSIFIED so the two can never be conflated on a future grep — mirroring DL-1's own
SURVIVOR/STRIKE/ABANDONMENT→RESOLVED/FALSIFIED/AMBIGUOUS mapping convention):**

| This document's verdict | Trigger | Maps to (cross-document convention only) |
|---|---|---|
| `CORROBORATED` | Measured composite's 95% Wilson CI contains §4.1's closed-form estimate | `RESOLVED` |
| `DIVERGED` | Measured composite's 95% Wilson CI excludes §4.1's closed-form estimate (direction must be reported — §4.3) | `FALSIFIED` |

No `AMBIGUOUS` row — like GROW-0's own Limb B, this is an exact CI-containment test at a frozen
(N, target) pair per condition; no third state is reachable. Evaluated independently per
condition (§4.3) — the two conditions may land on different verdicts.

**Reporting formulas (measured from the N=1,150-per-condition panel counts, §4.2):**

```
P(nominee=5)                              = nominee5_count / N
P(gates pass | nominee=5)                 = gatespass_count / nominee5_count
P(confirm clears | nominee=5, gates pass) = clears_count / gatespass_count
composite P(accept)                       = accept_count / N   (= product of the three factors above)
false-abandonment rate                    = abandoned_count / N
```

**CI method:** Wilson score interval at 95% confidence (`z=1.96`), the same convention GROW-0's
own §4 used for `nominal_p0`'s CI — reused, not reinvented:

```
center     = (p̂ + z²/(2n)) / (1 + z²/n)
half-width = z/(1+z²/n) × √(p̂(1−p̂)/n + z²/(4n²))
```

**Reporting table (template — every cell below is `TBD` until the execution task runs; Limb A/B
columns are already-measured real numbers, cited not re-derived, serving as the anchors §4.2's
sizing argument was built against):**

| Quantity | Limb A (SR=4.0, N=1) — anchor | Limb B (null, N=5,500) — anchor | Limb C (a) as-run (target_sr=1.8, N=1,150) | Limb C (b) boundary (target_sr=1.265, N=1,150) |
|---|---|---|---|---|
| P(nominee=5) | 100% (single real draw; separately, a dedicated n=5,000 design-time diagnostic in the parent prereg §6.1 step 4 measured 0/5,000 gate-a failures on this exact population, i.e. θ\* won the argmax in 100% of 5,000 trials) | N/A — no edge variant exists in this population | TBD ± Wilson CI | TBD ± Wilson CI |
| P(gates pass\|nominee=5) | ≈100% (implied by the same 0/5,000 diagnostic) | N/A | TBD ± Wilson CI | TBD ± Wilson CI |
| P(confirm clears\|nominee=5,gates pass) | predicted ≈1.00000000; real single draw: `confirm_stat=3.8200` (cleared, ≈3× margin) | N/A | TBD ± Wilson CI | TBD ± Wilson CI |
| **Composite P(accept)** | ≈1.0 (single real draw: accepted) | real: `sum_clears=5/5500=0.000909` (this is Limb B's own **false**-accept rate under the null — the floor Limb C's composite must clear by an overwhelming margin to be meaningful; predicted `nominal_p0=0.00059070`) | **TBD ± Wilson CI** | **TBD ± Wilson CI** |
| False-abandonment rate | not applicable at N=1 (design-time diagnostic only, not this document's own metric) | not applicable (no true edge exists to falsely abandon) | TBD ± Wilson CI | TBD ± Wilson CI |
| **§4.3 verdict** | n/a (not this document's own H) | n/a | TBD: `CORROBORATED` / `DIVERGED` | TBD: `CORROBORATED` / `DIVERGED` |

**What "TBD" resolves, when the execution task runs:** whether the boundary condition's measured
composite sits at, above, or (per §1's flagged closed-form projection) measurably below the naive
`power=0.500` reading — the number that would directly speak to ox-alpha row 2's "0.25" two-miss
figure being accurate, conservative, or an understatement for this engine's own nomination
dynamics — reported as evidence, with §4.3's `CORROBORATED`/`DIVERGED` verdict stating plainly
whether the closed-form planning estimate itself could be trusted here.

---

## §7 — Seeding (new root, GROW-0's own hierarchical pattern reused verbatim)

**A new, separate top-level root — not a reuse or perturbation of GROW-0's own frozen
`20260822`:**

```python
GROW0_LIMB_C_ROOT_SEED = 20260824  # dated per repo convention (this document's own authoring date)
limb_c_root = np.random.SeedSequence(GROW0_LIMB_C_ROOT_SEED)
as_run_seq, boundary_seq = limb_c_root.spawn(2)   # fixed order: (a) as-run, then (b) boundary

# Per condition (identical shape to grow0_dgp.spawn_panel_streams, called N times):
panel_seqs = condition_seq.spawn(N)               # N = 1,150 (§4.2), per condition
for panel_seq in panel_seqs:
    train_children, confirm_children = spawn_panel_streams(panel_seq, 10)  # REUSED, not re-implemented
    # variant 5 uses the condition's own edge_dollars (§3); variants 0-4,6-9 use the null shape,
    # identical to how Limb A/Limb B already draw their own null variants.
```

`spawn_panel_streams` (from `grow0_dgp.py`, read this session) already produces exactly this
`panel_seq.spawn(2) -> {train,confirm}_seq.spawn(10)` shape — Limb C's execution task calls it
directly, unmodified, once per panel per condition; it does **not** hand-roll a new spawn
function. `np.random.SeedSequence(20260824)` draws from an entirely independent entropy pool from
`np.random.SeedSequence(20260822)` — no shared lineage, no possibility of the two roots' spawn
trees colliding, by `SeedSequence`'s own construction (distinct entropy inputs).

**Runtime diversity assertion, reused:** the execution task must apply the same
`assert_seed_diversity`-shaped check (`grow0_harness.py`, read this session) to Limb C's own
consumed leaves per condition — `min_distinct = N × 20` (train + confirm, 10 variants each,
matching Limb B's own `n*20` convention) — for the same reason GROW-0's own §3 names: the
design-time spawn tree being collision-free does not prove the *consuming* loop reads a distinct
`panel_seqs[i]` per panel.

**Retry ledger — separate file, not commingled with GROW-0's own:** `discovery_manifests/
grow0_limb_c_retry_ledger.jsonl`, append-only, one JSON line per Limb C invocation (covering both
conditions' full N-panel runs together, mirroring how `run_grow0` aggregates its own five tokens
into one line): `{"run_id", "started_at_arg", "prereg_commit", "as_run": {"target_sr",
"edge_dollars", "n", "nominee_5_count", "gates_pass_given_nominee5_count",
"confirm_clears_given_nominee5_gatespass_count", "accept_count", "verdict"}, "boundary": {same
shape}}`. Kept separate from `grow0_retry_ledger.jsonl` precisely because Limb C is additive, not
a mutation of the frozen v3 design or its own single-line ledger history.

---

## §8 — What each panel measures

Per panel (either condition): draw TRAIN for `v=0..9` (`v=5` = the condition's own edge shape,
others null) via `spawn_panel_streams` + `draw_daily_pnl` (§9 extension); nominate via the **same
`argmax` rule** and **same gates (a)/(b)** GROW-0 uses (`_nominate_and_gate`, unmodified call);
record exactly three outcomes:

1. **`nominee == 5`** (selection correctness) — boolean.
2. **Gate (a)/(b) pass/fail on the nominee, whichever variant it is** (abandonment) — boolean. If
   either gate fails, the panel is `abandoned`: CONFIRM is never drawn, and it is recorded as a
   non-accept, exactly mirroring Limb B's own `clears[i]=0`-on-abandon convention (§6.2 of the
   parent prereg).
3. **Only if `nominee==5` AND gates pass:** does the CONFIRM draw clear
   `floor_at_k(10,6.5)=1.265`?

**False-abandonment, defined precisely (population-scoped, per the known-error-class guidance):**
in **Limb B's own population**, every panel is pure null — no true edge exists anywhere in it — so
an abandonment there is *correct* behavior (there was nothing to find), not "false" anything.
**In Limb C's own population, a true edge (variant 5) exists in *every* panel by construction** —
so **any** abandonment event on a Limb C panel is, by definition of that population, a case where
the train gate discarded a panel that contained a real edge, **regardless of which variant won the
argmax and was the one gated** (whether the discarded nominee was variant 5 itself, killed
directly, or a null variant that outcompeted variant 5 on TRAIN and was *then* itself gated out —
both routes mean the true edge never reaches a confirm read). **False-abandonment rate for a Limb
C condition ≡ (count of panels where gate a or b fails on the argmax nominee) / N** — unconditional
on which variant that nominee is. This is the *same* mechanical event GROW-0's own §6.1/§6.2 call
"abandonment"; only the word "false" is added, and it is added because of what the *population*
guarantees (a real edge is always present here), not because the event itself is redefined. Kept
strictly distinct from, and reported alongside (not blended with), **selection failure**
(`nominee != 5`, §6's table) — a panel can have the wrong nominee without abandoning (the wrong
nominee passes gates and proceeds to a confirm read that will not clear, since it is drawn from
the null shape) and can abandon without a selection failure (variant 5 wins the argmax and is then
itself gated out) — these are two different failure mechanisms and neither is a proxy for the
other.

---

## §9 — Implementation contract (binding on the execution task; not built here)

No code is written in this task. The execution task must satisfy this interface exactly, so that
GROW-0's own frozen results stay byte-identical and no DGP/scoring/nomination logic is
reimplemented (per the dispatch's own Rule-0 finding: `draw_daily_pnl` currently reads a
**module-level** `EDGE_DOLLARS` constant, not a caller-supplied value — verified by reading the
actual function this session, §0):

1. **`grow0_dgp.draw_daily_pnl`** gains one new optional keyword parameter,
   `edge_dollars: float = EDGE_DOLLARS` (the existing frozen module constant as the default) — every
   existing call site (Limb A/B/RED-LEAK/RED-BLIND, none of which will pass this new kwarg) is
   behaviorally unchanged.
2. **`grow0_scoring._score_all_variants`, `_nominate_and_gate`, `run_panel`** each gain the same
   optional `edge_dollars` passthrough (default-preserving, threading down to `draw_daily_pnl`) —
   additive signature extension only, no logic reimplemented, no existing call site's behavior
   altered.
3. **A new module, `lab/discovery/grow0_limb_c.py`**, holds Limb C's own orchestration only (root
   seed, per-condition N-panel loop, ledger write, §4.3's CI-containment verdict computation) —
   imports and calls the extended functions above; contains no DGP/scoring/nomination logic of
   its own.
4. **Frozen literals this module must hardcode** (from §2/§3/§4.2/§7 above, not re-derived at
   runtime except where §10 shows the reproduction): `LIMB_C_ROOT_SEED=20260824`;
   `AS_RUN_TARGET_SR=1.8`, `AS_RUN_EDGE_DOLLARS=28.5002`, `AS_RUN_N=1150`,
   `AS_RUN_COMPOSITE_ESTIMATE=0.9095`; `BOUNDARY_TARGET_SR=1.265`, `BOUNDARY_EDGE_DOLLARS=19.9857`,
   `BOUNDARY_N=1150`, `BOUNDARY_COMPOSITE_ESTIMATE=0.4656`; `FLOOR=1.265` (imported from
   `grow0_harness.FLOOR`, not re-typed).

---

## §10 — Audit hooks (every command below executed live this session; output pasted, not invented)

```bash
# floor_at_k(10, 6.5) reproduces (reused, not re-derived):
python -c "import sys; sys.path.insert(0,'lab'); from research_utils import axis_screen as a; print(round(a.floor_at_k(10, years=6.5),3))"
# Actual output: 1.265

# Dedup / amend-first search (re-run live, not copy-edited):
grep -rlniE "limb.c|limb_c|marginal.planted|grow0_limb_c|grow-0.*limb" \
    lab/discovery/ lab/research_utils/ tests/ docs/spec/ docs/briefs/pre-registration/ \
    docs/adr/ docs/notes/audits/ docs/notes/notice/ docs/briefs/closures/
# Actual output: docs/briefs/INDEX.md  (checked: unrelated "Limb C" usage in two other Q-briefs, §0)
```

**Deterministic (no-RNG) derivation — edge_dollars via brentq, Gaussian power, P(nominee=5) via
quadrature, panel-count arithmetic (full script, run this session):**

```python
import math
from scipy.stats import norm
from scipy.integrate import quad
from scipy.optimize import brentq

YEARS = 6.5; FLOOR = 1.265
P_ACTIVE = 0.60; P_WIN = 0.45
WIN_MEAN = 200.0; WIN_SD = 80.0; LOSS_MEAN = -163.60; LOSS_SD = 60.0

mu_y = P_WIN*WIN_MEAN + (1-P_WIN)*LOSS_MEAN
e_y2 = P_WIN*(WIN_SD**2+WIN_MEAN**2) + (1-P_WIN)*(LOSS_SD**2+LOSS_MEAN**2)
var_y = e_y2 - mu_y**2   # -> 37580.7276, sd 193.857493 (prereg cites 193.86)

def ann_sr(edge):
    daily_mean = P_ACTIVE*edge
    daily_var = P_ACTIVE*var_y + P_ACTIVE*(1-P_ACTIVE)*edge**2
    return daily_mean/math.sqrt(daily_var)*math.sqrt(252)

# sanity check: ann_sr(64.4412) -> 4.0000 (Limb A's own frozen edge; confirms identical formula)

def solve_edge(target_sr):
    return brentq(lambda e: ann_sr(e)-target_sr, 1e-6, 10000.0, xtol=1e-12, rtol=1e-14)

se = 1/math.sqrt(YEARS)   # 0.392232

for label, target_sr in (("as-run",1.8), ("boundary",FLOOR)):
    edge = round(solve_edge(target_sr), 4)
    z = (target_sr-FLOOR)*math.sqrt(YEARS)
    power = norm.cdf(z)
    mu = target_sr/se
    p_nominee, err = quad(lambda y: norm.pdf(y-mu)*norm.cdf(y)**9, -14, 14, limit=400)
    gate_pass = 1 - (0.5**9)*norm.cdf(-mu)
    composite = p_nominee*gate_pass*power
    print(label, target_sr, edge, round(z,6), round(power,6), round(p_nominee,6),
          round(gate_pass,8), round(composite,6))

for label, p in (("as-run",0.909525), ("boundary",0.465555)):
    for se_t in (0.03,0.02,0.015,0.01):
        print(label, se_t, math.ceil(p*(1-p)/se_t**2))
print("worst-case p=0.5:", [math.ceil(0.25/s**2) for s in (0.03,0.02,0.015,0.01)])
```

```
Actual output:
as-run   1.8   28.5002   1.363988   0.913714   0.995415   0.99999998   0.909525
boundary 1.265 19.9857   0.0        0.5        0.93111    0.99999877   0.465555
as-run   0.03  92 / 0.02  206 / 0.015  366 / 0.01  823
boundary 0.03  277 / 0.02  623 / 0.015  1106 / 0.01  2489
worst-case p=0.5: [278, 625, 1112, 2500]
```

(matches every literal frozen in §2/§3/§4 above, including the `edge_dollars` round-trip:
`ann_sr(28.5002)=1.79999762`, `ann_sr(19.9857)=1.26500267` — both within 3×10⁻⁶ SR of target, an
immaterial rounding artifact of the same class the parent prereg accepted for its own
`EDGE_DOLLARS=64.4412`.)

```bash
# GROW-0's own real, already-measured anchor numbers (§6 table), pulled from its closure + ledger,
# not re-simulated:
grep -n "sum_clears=5/5500\|confirm_stat=3.8200\|nominal_p0=0.00059070" docs/briefs/closures/GROW-0-closure-resolved.md
cat discovery_manifests/grow0_retry_ledger.jsonl
```

```
Actual output (grep, both matching lines in full):
28:| `RESOLVED` | Limb A PASS ∧ Limb B PASS ∧ all three RED tokens `FAILED_AS_EXPECTED` | Limb A `PASS` (nominee=5, confirm_stat=3.8200 ≥ floor 1.265) · Limb B `PASS` (sum_clears=5/5500, c=7) · red_leak `FAILED_AS_EXPECTED` (sum_clears=29/5500 ≥ c=7) · red_blind `FAILED_AS_EXPECTED` · red_patch `FAILED_AS_EXPECTED` | ✓ |
63:- **Limb B** (§4): predicted null-clear rate `nominal_p0=0.00059070` implies an expected

Actual output (cat, the ledger's one line verbatim):
{"run_id": "grow0-real-20260822T211844Z", "started_at_arg": "2026-08-22T21:18:44Z", "prereg_commit": "e21e80334c01e5c3334d997c7afbe158c5015697", "limb_b_n": 5500, "limb_b_c": 7, "limb_a": "PASS", "limb_b": "PASS", "red_leak": "FAILED_AS_EXPECTED", "red_blind": "FAILED_AS_EXPECTED", "red_patch": "FAILED_AS_EXPECTED", "overall": "RESOLVED"}
```

```bash
# GROW-0's own frozen v3 prereg and RESOLVED closure are untouched by this document (must both
# show zero diff / zero new commits touching them from this task):
git log --oneline -1 -- docs/briefs/pre-registration/2026-08-22-grow-0-synthetic-calibration-prereg.md
git log --oneline -1 -- docs/briefs/closures/GROW-0-closure-resolved.md
```

```
Actual output:
e21e803 Draft and freeze GROW-0 synthetic calibration harness pre-registration
70029e6 grow0: run full-scale harness for real -- Gate RESOLVED
```

(both pre-date this session's own commit — this task added neither a new commit touching either
path nor any diff to them; verified again immediately before commit, §ledger below.)

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/pre-registration/2026-08-24-grow-0-limb-c-marginal-effect-prereg.md --type inquire
```

Actual output, final run (repo-side mechanical subset; the note about the skill-side checker
being authoritative is the script's own standing disclaimer, printed on every invocation
regardless of type, not specific to this document):

```
check_brief: docs\briefs\pre-registration\2026-08-24-grow-0-limb-c-marginal-effect-prereg.md  (type=brief)

Summary: 0 HARD violation(s), 0 WARN violation(s)
RESULT: well-formed
```

This is the third of three actual runs this session, not the first — the prior two both found
real, disclosed issues (Revision record below), each fixed and re-verified by running the checker
again, never by asserting clean without checking:

1. First run (against the initial draft's non-canonical section numbering — panel-count/
   seeding/measurement content spread across §2–§9 with no §4-numbered H, no §5-numbered forbidden
   moves): **3 HARD violations** (`no hypothesis statement`, `no falsifier clause` at §4;
   `no forbidden moves listed` at §5) + 1 WARN (§6, no binary-verdict keyword). Root cause: the
   checker's `REQUIRED_SECTIONS` contract is keyed to literal section *numbers* (§4=H/falsifier,
   §5=forbidden moves, §6=gate), not just content presence anywhere in the document — this
   document's structure did not match it.
2. Second run (after renumbering to §0/§1/§4/§5/§6/§10 and adding §4.1/§4.2/§4.3 as `###`
   sub-headings under §4): **0 HARD, 1 WARN** (`§4 | section present but empty / placeholder`).
   Root cause, found by reading `check_brief.py`'s own `_SECTION_RE` and `_split_sections`
   (§0-style production-code read, not guessed): the regex matches a numbered heading at **any**
   `#`-`####` level, so `### §4.1` opened its own section entry and terminated §4's body at zero
   length — confirmed by running the same checker against GROW-0's own real, `well-formed`-passing
   prereg as a control (§10-style live comparison) and finding its own §6 avoids this exact trap
   by placing prose directly under `## §6` before its `### §6.1` sub-headings begin.
3. Third run (this one, after converting the three `### §4.x` sub-headings to bold paragraph
   labels — `**§4.1 — ... .**` — matching GROW-0's own §4 style of bold-label sub-parts with no
   numbered sub-headings at all, and adding a short intro paragraph directly under `## §4`):
   **0 HARD, 0 WARN**, as pasted above.

§0's dedup search was re-run live this session (not copy-edited) and its one hit checked and
disambiguated, not silently dropped ✓ · §2/§3/§4's closed-form numbers were computed by an actual
executed script this session (§10 pastes the full script and its actual output), not hand-derived
or asserted ✓ · the `edge_dollars` round-trip check and the `ann_sr(64.4412)→4.0000` sanity check
against Limb A's own frozen constant were both executed, not assumed ✓ · §6's anchor table cites
GROW-0's own real, already-measured closure numbers (`confirm_stat=3.8200`, `sum_clears=5/5500`),
pulled by grep from the closure file and the retry ledger this session, not transcribed from
memory ✓ · every quantity in §6's Limb C columns is explicitly `TBD` — no result is claimed before
any draw, consistent with the Status line and the dispatch's own "no random draw happens in this
task" constraint ✓ · §8's false-abandonment definition is scoped to Limb C's own population
(true edge always present) and explicitly distinguished from Limb B's population (no true edge) and
from selection failure, per the known-error-class guidance ✓ · §4's falsifiable H and §6's verdict
vocabulary (deliberately distinct from GROW-0's own RESOLVED/FALSIFIED) are substantive content,
not keyword-stuffing to satisfy the checker — the H tests a genuine methodological question (is
the closed-form approximation trustworthy here) that this document would need regardless of any
mechanical gate ✓.

---

## Revision record

| Date | Change |
|---|---|
| 2026-08-24 | v1 drafted with a non-canonical section numbering (Rule-0 reads at §0, but panel-count/seeding/measurement/gate content spread across §2–§9 without a §4-numbered falsifiable H or §5-numbered forbidden moves) — self-caught by actually running `scripts/check_brief.py` this session (3 HARD violations: no §4 hypothesis/falsifier, no §5 forbidden-moves list, plus a §6 WARN for no binary-verdict keyword), not asserted well-formed without checking. |
| 2026-08-24 | Restructured to the canonical §0/§1/§4/§5/§6/§10 contract: added a genuine falsifiable H (closed-form composite estimate vs. measured CI, per condition) and a `CORROBORATED`/`DIVERGED` verdict vocabulary (explicitly mapped to, but kept textually distinct from, GROW-0's own `RESOLVED`/`FALSIFIED` so the two can never be conflated), placed under `### §4.1`/`§4.2`/`§4.3` sub-headings. Re-ran the checker: 0 HARD, but a new WARN (`§4 | section present but empty`) — self-caught, not asserted clean without re-checking. |
| 2026-08-24 | Root-caused the new WARN by reading `check_brief.py`'s own section-splitting regex (Rule-0-style: read the actual checker code, not guess) — it treats **any** numbered `#`-`####` heading as a new section boundary, so `### §4.1` was silently terminating §4's own body at zero length. Confirmed against GROW-0's own real prereg (which passes this checker clean) as a live control: its §6 avoids the trap by placing prose directly under `## §6` before `### §6.1` begins, and its own §4 uses bold paragraph labels for sub-parts, never numbered sub-headings. Fixed by converting `### §4.1/§4.2/§4.3` to bold labels (`**§4.1 — ... .**`) and adding a short intro paragraph directly under `## §4` — matching GROW-0's own §4 style exactly. Re-ran the checker: **0 HARD, 0 WARN**. No numeric literal (target_sr, edge_dollars, N, seeds) or substantive claim changed across any of these three rows — only structure, and the H/verdict content added in the second row. This is the version at freeze. |
