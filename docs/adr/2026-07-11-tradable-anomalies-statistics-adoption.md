# ADR 2026-07-11 — Adopt "The Statistics of Tradable Anomalies" as the R&D reference layer; Tranche-1 doctrine; deliberate non-adoptions

**Status:** `Accepted`
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Revision:** 2026-10-15 — retention trim (ADR decay audit; operator direction 2026-10-15): §0 body condensed to a pointer, §7 "Landed"/"Held" notes and Verification removed, §10 reduced to its decision-persistence hooks; §7 status note added. Pre-trim text at blob `19d7553cca42c924bf9a6cb473a870b2fc341e5f` (commit `4121e84c95f4990b71962e3b9570c4c3fad88426`).
**Decision date:** 2026-07-11
**Authors:** Joshua (direction) + Claude Code (gap audit + authoring)
**Supersedes:** none. Additive — a reference layer + methodology doctrine.
**Related:** `docs/adr/2026-07-11-discovery-campaign-defaults-ratified.md` (the campaign rules of evidence this reference is the *why* for); `docs/adr/2026-07-10-databento-research-stack.md` (the discovery stack; §5 authorizes the skill amendments here); `docs/adr/2026-07-10-strategies-never-locked-lifecycle-governance.md` (the admission axis the shrinkage prior feeds); `docs/methodology/references/statistics-of-tradable-anomalies.md` (the adopted document).
**Layer:** methodology + research tooling. **No** strategy/risk-control parameter, allocation, `dd_protection` constant, `portfolio_mc.py`, or Pine source is touched. Locked MC anchor 99.83/0.17/4.37 untouched.

---

## §0 — Rule 0 reads (gap audit against production)

The adoption rests on an 8-reader gap audit of the repo at anchor `509f6b5` — the 8-domain → repo gap map, plus two incidental findings. That audit describes July state (several paths it names, e.g. `lab/validation/`, were later retired) and is historical; read it in the [prior revision](https://github.com/Joshua-Asante/first-passage/blob/4121e84c95f4990b71962e3b9570c4c3fad88426/docs/adr/2026-07-11-tradable-anomalies-statistics-adoption.md).

---

## §1 — Context

The field guide "The Statistics of Tradable Anomalies" is a bespoke inference manual
for this operation (it references this program's own Q-DECAY-1, rejected-candidates
registry, joint week-block MC, and accept-beta fork). Its 8 statistical domains + a
staged pipeline map cleanly onto the R&D machinery; an audit established that the
document's center of gravity (Domain 4 multiplicity, pre-registration) is what we've
already built best, and the genuine gaps cluster in Stage-1 scan instrumentation,
portfolio-admission tooling, kill-line operating characteristics, and null-model
texture.

Separately and in parallel, the operator's discovery-campaign governance chain
(campaign template + defaults ADR + CC-handoff + DISC-CAMP-0 pre-registration, landed
same day) independently reached for much of the same machinery — corroboration that
the gaps are real. This ADR records the reference adoption, the doctrine that lands
now (Tranche 1), what is deliberately *not* adopted, and what is deferred.

**Decision driver (one sentence):** adopt the field guide as the standing statistical
*rationale* layer, land the cheap high-value doctrine now, and record on the same page
the four prescriptions we consciously reject — so the rejections are not silently
re-litigated later.

---

## §2 — Decision

**(1) Adopt** `docs/methodology/references/statistics-of-tradable-anomalies.md` as a
**REFERENCE** layer — not canonical, not gating. Pine + `docs/adr/` stay canonical for
behavior/decisions (Rule 0); `dd_protection.py` / `firm_rules.py` stay canonical for
live-sizing constants. The reference is the *why* the methodology skills and the
discovery-campaign pipeline cite.

**(2) Land Tranche-1 doctrine** (this commit):

| Addition | Where | Gap it closes |
|---|---|---|
| Null hygiene — name the null; permutation drift-handling | `strategy-validation` SKILL §5 | Domain 1/3 — the joint-hypothesis + drift traps were undocumented |
| hmmlearn filtered-vs-smoothed lookahead | `futures-anomaly-discovery` tool-discipline | Domain 5 — regime-label leak was uncovered |
| Pre-mining vol-U-shape hygiene | `futures-anomaly-discovery` tool-discipline | Domain 1/7 — scanner would rediscover the vol hump |
| Back-adjustment / CME clock / bid-ask-bounce data hygiene | `futures-anomaly-discovery` tool-discipline §Pre-mining data hygiene (was `databento-data` schemas-and-symbology; moved by #860) | Domain 7 — the futures-microstructure hygiene layer was entirely missing |
| Discovery ledger anchored to `<repo-root>/discovery_manifests` | `register_search.py` | Cwd-scatter; databento ADR §4/§10 hook intent |
| Backtest→live shrinkage convention (30–70% band, ex-ante prior) | `docs/methodology/backtest_live_shrinkage.md` | Domain 5 — no ex-ante decay haircut existed (ECR is ex-post) |

**(3) Deliberate NON-adoptions** — recorded so they are not re-proposed as gaps:

| Field-guide prescription | Verdict | Why (each already litigated here) |
|---|---|---|
| **Kelly / fractional-Kelly / posterior-ramp sizing** | **Reject** | Conflicts with locked fixed-fraction allocation + down-only automation. The lifecycle ladder (1.00/0.50/0.25/0.00) is the repo's *discrete* robustness analog; lifecycle Call-2 already rejected a smooth confidence-sizing curve as "tinkering in a lab coat." The shrinkage convention captures the spirit (shrink the edge, size on a lower bound) without importing continuous Kelly. |
| **SPRT** as the decay detector | **Reject** | Q-GUARDIAN-DECAY-1 DP-resolution litigated it: heavy-tailed per-trade R breaks SPRT's parametric density. CUSUM was chosen for exactly that robustness and is the ratified Guardian detector; the campaign battery's Stage-6d monitor is CUSUM for the same reason. |
| **Ledoit–Wolf shrinkage + covariance optimizers** | **Reject** | The field guide *itself* (Domain 6) says refusing precision — coarse buckets, capped weights, MC-verified tails — beats optimization at our 4–10-strategy / 1–3-year sample sizes. That is exactly what we do; adopting LW would feed an optimizer we deliberately don't run. |
| **Numeric π / PPV as tracked bookkeeping** | **Reject (retain as rationale)** | The qualitative mechanism-named / NO-MECH lane discipline (Q-MECH-1 verdict structure) does the π work; ADR 2026-05-11 explicitly ruled Bayesian model comparison out of scope. The PPV arithmetic is kept as the *argument* for mechanism-first + pre-registration, not converted to a tracked number. |

**(4) Defer** (Forward — see §7 forward board): the remaining Tranche-2/3/4 tooling
gaps the discovery-campaign chain does not already cover.

**Effective:** immediately. **Scope:** methodology + research-tooling doctrine only.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Adopt the guide wholesale, including Kelly / SPRT / Ledoit-Wolf / numeric-π | Each conflicts with a decision already made here for a stated reason; wholesale adoption would silently reverse them. Recorded as explicit non-adoptions instead. |
| Restate the doctrine inside `CLAUDE.md` | `CLAUDE.md` is the operational index, not a statistics manual; a reference doc + skill amendments keep the *why* out of the operational surface and next to the tools that use it. |
| Land the full detector kit / event-study harness / GARCH calibration now | Real gaps, but code — they need the research venv recreated + tests, and part is already being built by the operator's CC-handoff (Track B/C). Deferred to their own gated work, not this doc-layer commit. |
| Do nothing (the machinery mostly exists) | The audit found the strongest domain built and the rest scattered as one-offs; the cheap doctrine (null hygiene, futures-microstructure hygiene, the shrinkage prior) is high-value and was genuinely absent. |

---

## §4 — Falsifier (revert trigger)

**H:** These are the right doctrine additions + the right non-adoptions for this
operation's R&D.

**Falsifier (a non-adoption is wrong):** a closed campaign or a live post-mortem
demonstrates that a rejected prescription would have changed a verdict the existing
machinery got wrong — e.g. a decay a CUSUM missed that SPRT would have caught at
acceptable false-alarm rate, or a book-tail an optimizer would have avoided that
capped weights did not. On that evidence the specific non-adoption is revisited by a
superseding ADR citing the dated incident (the `rejected_signals.md` re-proposal bar
generalized: a dated miss, not a restated plausibility argument).

**Falsifier (the reference drifts to canonical):** if any gate or decision starts
citing this reference doc as *authority* for a locked-parameter change, that violates
its REFERENCE status — Pine + ADRs are canonical. Revert = restate the status.

**Trigger check schedule:** rides the quarterly programme audit (next **2026-08-08**).

---

## §5 — Forbidden moves (under this ADR)

- **Treating the reference doc as canonical or gating** — it is rationale; it overrides no locked parameter and no landed ADR.
- **Silently importing a rejected prescription** (Kelly sizing, SPRT detector, LW optimizer, tracked numeric π) because "the field guide says so" — each is a recorded non-adoption; reversing one needs a superseding ADR with dated evidence.
- **Restating a locked risk constant** in the shrinkage convention or any Tranche-1 doc — the shrinkage page is a planning prior, introduces no number the MC pins or `validate_params` would see.
- **Letting the reference doc and `docs/adr/` drift** — if a decision changes, the ADR moves; the reference is updated only as external-material re-adoption, never as a decision surface.

---

## §6 — Consequences

**Positive:** the statistical *why* is now in-repo, next to the tools; the discovery
lane gains the futures-microstructure hygiene layer it entirely lacked; the go-live
underwriting has an explicit ex-ante shrinkage prior; the four non-adoptions are on the
record with reasons, closing them to silent re-litigation.

**Negative (real):** a reference doc is maintenance surface — it can drift from the
code it describes. Mitigated by its explicit REFERENCE status (it asserts nothing the
gates check) and the §4 drift falsifier. The doctrine additions widen the skills;
each is short and cited.

**Risks:** the deferred Tranche-2/3/4 tooling (event-study harness, detector kit,
GARCH/surrogate calibration, kill-line operating characteristics) stays a gap until
built — the honest residual, tracked on the forward board, not silently closed.

---

## §7 — Implementation plan / forward board

**Forward (deferred, tracked in `STATE.md`):**

> **Status 2026-10-15 (no decision change).** T2's originally scoped tools landed 2026-08-23 (`lab/research_utils/event_study.py`, `detector_kit.py`); Addendum (b) reopened T2 for four null primitives that still live only in `lab/analysis/_inbox/{mym_mechanism_harvest,mnq_dailygeom_notice}_2026-08-29/` and are not carried in `STATE.md`. T3: a GARCH-fitted null and ENB are in `lab/research_utils/breadth.py`. T4: synthetic Call-1 OC landed 2026-08-23 ([record](../notes/research/2026-08-23-call1-oc-synthetic.md)); the live σ-source stays fill-gated and the Task-3 writer is not authorized (`STATE.md` No fixed date). The 2026-08-08 board date has passed.

- **T2 — Stage-1 scan instrumentation:** reusable **event-study harness** (constraint/flow family — highest persistence prior; our only mechanism-named finding, JPY month-end, lives there); **cheap detector kit** — promote Lo–MacKinlay VR to a tool, add Ljung-Box on r vs |r|, HAC-t, an autocorrelation-corrected n_eff helper (all via already-installed `arch`/`statsmodels`).
- **T3 — scanner calibration + admission tooling:** GARCH-fitted-null / surrogate-data pipeline calibration (also upgrades the corpus-FDR IID-Gaussian null); promote ENB + downside-correlation + with/without-candidate marginal-delta into committed tools (the operator's CC-handoff Track C covers the ENB breadth column — recover the Q-NEFF-1 computation into it).
- **T4 — riding the 2026-08-08 board:** compute the production Call-1 kill-line operating characteristics (false-kill rate, detection lag vs horizon) *before* the first decay review; build the owed rolling-PF σ-source harness + tier-demotion state writer.

---

## §10 — Audit hooks (runnable)

```bash
# Reference doc present + flagged REFERENCE (not canonical)
grep -n "Status: REFERENCE" docs/methodology/references/statistics-of-tradable-anomalies.md

# Tranche-1 doctrine present
grep -n "Null hygiene" .claude/skills/strategy-validation/SKILL.md
grep -n "Filtered, not" .claude/skills/futures-anomaly-discovery/reference/tool-discipline.md
grep -n "Pre-mining data hygiene" .claude/skills/futures-anomaly-discovery/reference/tool-discipline.md   # moved from databento-data schemas-and-symbology by #860
grep -n "Backtest → live shrinkage" docs/methodology/backtest_live_shrinkage.md

# Non-adoptions recorded
grep -nE "Kelly|SPRT|Ledoit|numeric π|numeric-π" docs/adr/2026-07-11-tradable-anomalies-statistics-adoption.md
```

---

## Addendum — 2026-08-29

**Does not amend §2's REFERENCE (not canonical/gating) status, the four recorded non-adoptions, or
§5's forbidden moves.**

**(a) — Tranche-2 doctrine: pre-registration completeness rule.** The D5 magnitude-persistence
spec's "matched day-session-history conditioning" prose
(`docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md` §4) was frozen, then
independently implemented as a **marginal** comparison in three scripts across two sessions (MYM
candidates 2, 3, 4) before adversarial review caught the divergence and corrected each to the
**within-stratum** reading the spec intended (`db91a21`, `aa3584b`) — the prose permitted two
mutually-exclusive readings, and both were tried before either author noticed.

| Addition | Where | Gap it closes |
|---|---|---|
| Pre-registration completeness — a frozen spec's prose passes completeness only if two independent implementers would compute identical numbers from it alone; if not, the freeze ships reference code or a worked numeric example on synthetic data | `strategy-validation` SKILL §5 (beside Null hygiene); mirrored at `.claude/skills/brief-authoring/references/inquire_brief.md` §8 | A spec frozen in prose alone can still admit divergent implementations — nothing previously required a determinism check before freezing |

Applies forward to every `docs/spec/` FROZEN battery and `docs/briefs/pre-registration/` file; does
**not** retroactively fault D5 or reopen its landed verdicts.

**(b) — T2 extends to frozen null-construction primitives; promote out of per-campaign
duplication.** `circular_shift_null_p`, `roll_other_within_stratum`,
`block_bootstrap_min_lift`/`block_bootstrap_p`, and `stratified_lifts`/`min_stratified_lift` were
each hand-written, near-identically, inside `c2_c4_stratified_rerun.py`, `c3_stratified_rerun.py`,
and `candidate24_joint_gate.py` (`ab34aa6`, retrofitting a null-calibrated circular-shift p into
three 2026-08-29 scripts) — no shared implementation existed, only the prose doctrine above (Null
hygiene). `lab/research_utils/` already is the retained, W4-protected home for exactly this class of
primitive (`permutation.py`, `deflated_sharpe.py`, `selection_tests.py`, each with its own
adversarial-test file) — this reopens T2 ("promote one-off tooling into committed tools," executed
2026-08-23 for its originally-scoped items) to direct these four functions into it, tested the same
way, rather than leaving T2 read as fully closed.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-11 | Initial authoring + acceptance (adopt reference; Tranche-1 doctrine; non-adoptions) | Joshua + Claude Code |
| 2026-08-29 | Addendum: (a) Tranche-2 pre-registration completeness rule; (b) T2 reopened to promote duplicated null-construction primitives into `lab/research_utils/`. | Claude Code |
| 2026-10-15 | §0 body, §7 Landed/Held, Verification removed; §10 reduced to decision-persistence hooks; §7 status note; prior body pinned | ADR decay audit |
