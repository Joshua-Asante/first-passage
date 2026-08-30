# Bounded Phase 1 round — frozen plan (PROPOSED)

**Status: PROPOSED — pending Codex review + operator ratification of the two ⚖ items below.**
Authored 2026-08-30, as the concrete instantiation of the operator-ratified Phase 1 path
("I ratify the Phase 1 approach", `Q-RANGEXFER-1` §11: one further round, at most 2 candidate
remedies, hard stop; on failure, disclose a §6 gate-table gap for a fresh operator amendment
rather than force-fitting `AMBIGUOUS-HOLD`; scoped to `Q-RANGEXFER-1`, not `Q-VOLREGIME-1`).
Drafted while reviewing the external (Codex) "MNQ / MYM Mechanism Review" report, whose
critical-path diagnosis (the joint long-memory surrogate null under parameter estimation is the
single blocker for both mechanism families) this plan adopts — with the corrections in §6 below.

Owner brief: [`Q-RANGEXFER-1`](../../../docs/briefs/Q-RANGEXFER-1-overnight-range-gap-magnitude-transfer.md) §7 Phase 1.
Design-exploration record this plan continues: [`RESULTS.md`](RESULTS.md) (Rounds 1–3).

---

## §1 — What this round can and cannot change (decision context)

Three facts, all already on record, jointly determine the round's actual payload:

1. **L4 has already fired on all five hypotheses** ([`rangexfer_byyear_l4_2026-08-30/RESULTS.md`](../rangexfer_byyear_l4_2026-08-30/RESULTS.md),
   Codex-corrected: parents `n_valid=3`, others 4–6, all `< 7`). `RESOLVED` is unreachable for
   every H under this brief at this panel length, regardless of Phase 1's outcome.
2. **Under the currently frozen verdict map, a valid but non-significant attribution limb gates
   nothing.** Pre-registration §C freezes L5 as "NEVER GATES on its own — TYPES the verdict";
   §D's `FALSIFIED` row fires only on outright L1–L3/L4 failure or L5 *VOID*. So with L4 already
   AMBIGUOUS, every reachable verdict (`FALSIFIED` via presence, `AMBIGUOUS-HOLD` via L4) is
   decided by the presence limbs alone — **the certified null, run under the current map, is
   verdict-inert for this brief** (except the degenerate L5-VOID path). It changes only the
   `{MECHANISM | SURVIVAL-ONLY}` typing of whatever the presence limbs establish.
3. **The frozen texts contradict each other on exactly this point.** The brief's own §4 states
   "otherwise the incremental lift is an artifact of the shared same-day regime" — attribution
   failure IS the hypothesis's own falsification branch as written — and the sibling
   `Q-VOLREGIME-1` §6 (Codex-corrected, PR #210) explicitly routes "L5 valid but p_upper > 0.05"
   to `FALSIFIED`. Pre-reg §C says the opposite. This is a documented internal inconsistency
   between two frozen artifacts, not a new design choice.

Consequence: **the round's expected value hinges on an operator ruling (§2 P2) that must land
before the remedies run**, and the presence limbs L1–L3 — cheap, surrogate-independent,
computable today — determine most of the verdict surface either way.

---

## §2 — Pre-round steps (before any remedy work)

**P1 — Complete the presence battery (L1–L3) for all five hypotheses.** Same class of work as
the L4 diagnostic (PR #224): frozen limb definitions (pre-reg §B/§F.2/§G.2), computed from the
cached joint frames (`candidate24_joint_frame.csv`, `c24_joint_frame.csv`, the `bprime=0`
scored subset), K-free re-derivation of already-scored panels. Vendor bars are present in this
worktree (hash-verify against `SHA256SUMS` before use), so the two owed MYM re-runs (frozen
1307-day panel; the `H-RANGEXFER-1.b-MYM` 2026 boundary case) are runnable in the same pass.
Ex-ante consequences, stated now: any outright L1–L3 failure routes that hypothesis to
`FALSIFIED` under the frozen map with no null needed; if all five pass L1–L3, then under the
current map all five verdicts are already determined (`AMBIGUOUS-HOLD`) and only P2 can make the
remedy work verdict-bearing.

**P2 — ⚖ Operator ruling: does a certified, valid, non-significant L5 falsify H, or only type
it?** Two coherent options; the frozen corpus supports both readings, so this is an operator
call, requested with full disclosure that the exploratory (uncertified) `p_upper=0.785` lead is
already on record pointing at this exact cell:

- **Option A — L5 gates (recommended):** amend `Q-RANGEXFER-1` §6 + pre-reg §D to add "L5 valid
  (not VOID) but does not clear (p_upper > 0.05)" to the `FALSIFIED` trigger, mirroring the
  PR #210 fix on `Q-VOLREGIME-1`; amend pre-reg §C's "NEVER GATES" line to match; freeze the
  precedence rule **FALSIFIED > AMBIGUOUS-HOLD when both fire** (attribution failure is
  dispositive regardless of panel length) on both briefs (the same dual-fire ambiguity exists on
  `Q-VOLREGIME-1`). Rationale: §3's Question is attribution-shaped ("beyond what a null
  preserving shared-regime structure would produce"); §4's own "otherwise… artifact" text says
  the same; the sibling brief already rules this way; and Option B leaves a
  known-failed-attribution mechanism parked as re-openable `AMBIGUOUS-HOLD` — standing
  zombie-thread risk. Under Option A the bounded round is verdict-bearing: a certified null +
  the 0.785-class result would close the thread `FALSIFIED`, terminally and cleanly.
- **Option B — L5 types only:** keep pre-reg §C as frozen. Then every reachable verdict at this
  panel is presence-determined; the day-level certification buys only the
  `{MECHANISM | SURVIVAL-ONLY}` annotation on an `AMBIGUOUS-HOLD`, and the certification
  effort's real customer becomes `Q-VOLREGIME-1` (§5 below), with the day-level frame kept only
  as the cheaper certification testbed.

Ruling this before the remedies run is what keeps it honest: after a certified L5 result exists,
choosing between A and B would be choosing the verdict.

**P3 — `Q-VOLREGIME-1` by-year L4 count (cheap, parallel, informative for §5).** Bar-level
panels span 7 distinct calendar years (2020-07→2026-07) with enormous per-year n — unlike the
day-level frames, `N_valid ≥ 7` may actually PASS at bar level, making `RESOLVED`/`FALSIFIED`
reachable there. Compute the qualifying-year count from the vendor bars (mirroring the PR #224
convention, including its per-stratum floor correction) before assuming the day-level wall
transfers. No K (presence-limb re-derivation of an already-scored construct).

---

## §3 — The two remedy slots (frozen; hard stop after both)

Both remedies keep the frozen statistic (min stratified incremental lift), frozen `alpha=0.05`,
and the existing generate → score → p_upper machinery (verified bug-free, RESULTS.md Round 2).
What changes per remedy is the null generator and how estimation uncertainty is handled. No
third remedy; no tolerance/band retunes after results exist; failure of both ⇒ §4 fail branch.

**R1 — HAR-family generator (new model class; primary).** Per channel, fit a HAR(1,5,22)
cascade on log-range by OLS (the literature-standard quasi-long-memory model for realized
range/volatility — a restricted AR(22) whose daily/weekly/monthly cascade is the standard
parsimonious approximation to exactly the "fast decay then plateau" ACF shape Round 2
diagnosed); couple channels via correlated Gaussian innovations, correlation
bisection-calibrated to the real lag-0 cross-correlation (machinery exists); rank-remap onto
each channel's real marginals. Why it attacks the actual root cause: the 25% Type-I inflation
comes from surrogates generated at a noisy point estimate (SMM-fitted `d` near the 0.5 boundary
at n=1487 has large sampling error); HAR's OLS parameters at n=1487 are tight, and refits are
essentially free — so the refit-per-replicate calibration study can run at full production
grade, N=200+, at laptop cost.

**R2 — ARFIMA kept, estimation made honest and propagated (secondary).** Keep
`longmemory_copula.py`'s ARFIMA(1,d,0)+copula generator, but (a) replace the SMM grid with a
fast two-step estimator (local-Whittle `d̂` + CSS/profile AR term) so per-replicate refits are
cheap enough for a real calibration study, and (b) propagate parameter uncertainty into the
null: estimate the estimator's own sampling distribution by parametric bootstrap (simulate at
`θ̂`, refit R times), then draw `θ*` per surrogate from that distribution instead of generating
every surrogate at the plug-in point estimate. Plug-in composite-null bootstraps are
anti-conservative in exactly the way Round 3 measured; parameter-uncertainty propagation is the
standard corrective and errs conservative.

**Preference rule, frozen now:** if both certify, R1 is the deployable design and R2 becomes a
disclosed robustness annex — decided before either result exists, so there is no pick-the-winner
degree of freedom.

### Certification gates (both remedies, all three required)

1. **Model adequacy — mechanism-independent, criterion validated before use.** Replace the
   failed ACF-percentile gate with a multi-horizon out-of-sample predictive comparison
   (rolling-origin log-score or QLIKE at h=1, 5, 22 per channel): the candidate must beat the
   naive benchmark and must separate from VAR(20) — the known-inadequate comparator that the
   ensemble gate failed to reject — at the long horizon, where short-memory models' forecasts
   revert too fast. **Meta-requirement:** before touching real data, the criterion itself is
   validated on synthetic panels (where adequacy is known by construction): it must reject
   VAR(20) and accept the true generator with frozen thresholds set there. If no criterion in
   this family can discriminate at n=1487, adequacy is undecidable at this panel length — that
   counts as remedy failure and feeds §4's fail branch as a corpus-insufficiency finding.
   Cross-model verdict agreement may be reported as a disclosed annex but can NEVER substitute
   for size control (option (a) is operator-rejected; the Codex report's "cross-model
   robustness" adequacy option is admitted only in this annex role).
2. **Estimation-aware size.** Refit-per-replicate positive control at production-grade
   estimation, N=200 replicates: empirical size at nominal α=0.05 must land in **[0.01, 0.08]**
   (binomial 95% acceptance around 0.05 at N=200, floor kept above zero so a degenerate
   never-rejects null cannot pass). Full battery at the MNQ-fitted parameters; N=100 spot-check
   at the MYM-fitted parameters; both must pass. No known-true-parameter shortcut counts.
3. **Power floor.** At the same frozen injected alternative the existing positive controls
   already implement: power ≥ **0.50**. If size certifies but power fails the floor, the test
   cannot support a falsifiable attribution verdict at this panel length — remedy failure,
   corpus-insufficiency finding, §4 fail branch.

---

## §4 — Outcome fork

**A remedy clears all three gates →** Phase 2: fresh independent adversarial review of the
certified design (`pre-ratification-adversarial-panel` class — checking it against the
retired-block-shuffle failure mode: does it pass regardless of whether a real effect exists?),
including whether one design soundly serves both instruments. Then Phase 3: formally register
the already-declared K (`H-RANGEXFER-1.a-MYM` K_fresh=2, `H-RANGEXFER-1.b-MYM` K_fresh=2, +1
for re-scoring the statistic the exploratory 0.785 look already touched; non-stacking per the
2026-08-30 ratification), obtain execution GO, run per instrument per hypothesis, Phase 4 score
under the P2-ruled map. Expected terminal states at this panel length: `FALSIFIED` (Option A +
a 0.785-class certified result, or any presence failure from P1) or `AMBIGUOUS-HOLD` — never
`RESOLVED`. Only after the day-level design is certified: adapt (not port) to bar level for
`Q-VOLREGIME-1` — transfer re-certification at bar-level n plus its distinct-WHO three-way
check, per that brief's §7.

**Neither remedy clears (or adequacy undecidable / power floor unmet) →** the ratified fail
branch: no more design rounds. File the §6 gate-table gap disclosure and propose the fresh
verdict row for operator ratification — draft text: **`AMBIGUOUS-DESIGN`** — *"no certifiable
joint-surrogation attribution design exists at current panel length (three rounds + one bounded
remedy round, 9 constructions, all failed certification — see RESULTS.md); presence-level
evidence stands as typed by stage-1; ITERATE with re-open triggers: (a) panel reaches ≥7
qualifying years under the corrected per-stratum L4 gate, (b) a genuinely different design
class arrives with its own certification evidence, (c) an externally validated method for
joint long-memory surrogation under estimation becomes available. No calendar-dated re-test."*
Close `Q-RANGEXFER-1` under the amended gate. `Q-VOLREGIME-1` is then assessed independently,
NOT closed by inheritance — both day-level failure mechanisms (estimation noise in `d` at
n≈1.5k; the 6-year L4 wall) are materially weaker at bar level (n≈135k–140k; possibly 7
qualifying years per P3), so the same verdict does not automatically transfer.

---

## §5 — Where the certification effort's value actually lands

Under Option B (P2), and even partially under Option A, the largest expected payoff of a
certified joint long-memory null is **not** `Q-RANGEXFER-1` (whose ceiling is `AMBIGUOUS-HOLD`
/ `FALSIFIED` regardless) but: (1) `Q-VOLREGIME-1`, where L5-gating semantics are already
frozen, per-year n is enormous, and `RESOLVED` may be genuinely reachable if P3 finds ≥7
qualifying years; and (2) every future S2-shaped cross-series question — the D5/O1
"UNRESOLVED-NEEDS-DESIGN" debt is a standing instrument gap the MECHANISMS program keeps
hitting, and a certified design retires it once for the whole class. This is why the bounded
round is worth running even though it cannot produce a `RESOLVED` on the brief that chartered it.

---

## §6 — Corrections to the external Codex report (adopted with these adjustments)

The report's critical-path diagnosis and its Priorities 1/3/5 are adopted. Corrections:

1. Its claim "attribution failure produces FALSIFIED" (report §2.E) is **wrong for
   `Q-RANGEXFER-1` as frozen** — only L5 *VOID* falsifies; valid-but-non-significant gates
   nothing (pre-reg §C/§D). True for `Q-VOLREGIME-1` only. This is the P2 ruling.
2. Its §5.A ("the repo can still perform the other limbs and determine whether the by-year wall
   actually fires… may prevent final certification later") is **stale**: the wall already fired
   on all five hypotheses (PR #224), with corrected `n_valid=3` (not ~6) for both parents —
   `RESOLVED` is already unreachable, which inverts the round's cost-benefit rather than merely
   qualifying it.
3. Its recommended fallback ("close the thread AMBIGUOUS") must route through the ratified
   mechanism — §6 gap disclosure + fresh operator gate amendment (§4 above) — not through the
   existing `AMBIGUOUS-HOLD` row, whose trigger is L4-specific (already ruled, PR #223).
4. Its K section is partially stale: the amounts are already declared and corrected
   (K_fresh=2/2, +1 for the reused real-data look; batch K=5 non-stacking, operator-ratified);
   what remains owed is formal registration at Phase 3, not fresh derivation.
5. Its "volume transitively blocked" framing is right for sequencing but wrong as a verdict
   coupling — the day-level design's two failure mechanisms are both n-dependent and materially
   weaker at bar level (§4/§5), so `Q-VOLREGIME-1` must be assessed on its own panel either way.

## Audit hooks

```bash
# The three facts §1 rests on
grep -n "NEVER GATES" docs/briefs/pre-registration/Q-RANGEXFER-1-verdict-preregistration.md
grep -n "n_valid" lab/analysis/_inbox/rangexfer_byyear_l4_2026-08-30/RESULTS.md
grep -n "p_upper > 0.05" docs/briefs/Q-VOLREGIME-1-intraday-bar-volume-regime.md

# The ratified bound this plan instantiates
grep -n "I ratify the Phase 1 approach" docs/briefs/Q-RANGEXFER-1-overnight-range-gap-magnitude-transfer.md

# The measured Type-I inflation both remedies must clear
python lab/analysis/_inbox/joint_surrogation_null_2026-08-30/_refit_per_replicate_positive_control.py
# Expected: null reject rate 2/8=0.25 (coarse) vs nominal 0.05
```
