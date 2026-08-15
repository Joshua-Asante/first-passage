# ADR 2026-07-11 — Adopt "The Statistics of Tradable Anomalies" as the R&D reference layer; Tranche-1 doctrine; deliberate non-adoptions

**Status:** `Accepted`
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Decision date:** 2026-07-11
**Authors:** Joshua (direction) + Claude Code (gap audit + authoring)
**Supersedes:** none. Additive — a reference layer + methodology doctrine.
**Related:** `docs/adr/2026-07-11-discovery-campaign-defaults-ratified.md` (the campaign rules of evidence this reference is the *why* for); `docs/adr/2026-07-10-databento-research-stack.md` (the discovery stack; §5 authorizes the skill amendments here); `docs/adr/2026-07-10-strategies-never-locked-lifecycle-governance.md` (the admission axis the shrinkage prior feeds); `docs/methodology/references/statistics-of-tradable-anomalies.md` (the adopted document).
**Layer:** methodology + research tooling. **No** strategy/risk-control parameter, allocation, `dd_protection` constant, `portfolio_mc.py`, or Pine source is touched. Locked MC anchor 99.83/0.17/4.37 untouched.

---

## §0 — Rule 0 reads (gap audit against production)

The adoption is grounded in an 8-reader parallel audit of the actual repo (Rule 0 —
production code opened, not doc references), anchor `509f6b5`. Verified state, by
domain of the field guide:

- **Strongest already-built:** Domain 4 (multiplicity). K-ledger (`register_search.py`), DSR/PSR (`lab/validation/dsr.py` + skill CLI, control-tested), PBO/CSCV (`lab/validation/pbo.py`), CPCV (`lab/validation/cpcv.py`), native White-RC + Romano–Wolf with known-truth FWER calibration (`lab/validation/corpus/reality_check.py`), Storey q-values, corpus-FDR. Pre-registration discipline is the repo's best-built capability (template + 28 committed pre-regs + git freeze-ancestry rule).
- **Available zero-install:** `arch` 8.0.0 + `statsmodels` 0.14.6 import in the ops venv today — SPA/StepM/MCS, `arch.unitroot.VarianceRatio`, GARCH `simulate`, `cov_hac`, `acorr_ljungbox` all live-verified. The research venv (stumpy/tsfresh/hmmlearn/skfolio/databento) is pinned in `requirements-research.txt` but not currently on disk (recreate before those tools run).
- **Weakest domain:** Domain 2 (classical inference). No HAC/Newey–West in code; Ljung-Box/runs/BDS absent; Lo–MacKinlay VR exists only as one-off lab code; no reusable event-study harness.
- **One-offs never promoted to tooling:** VR, ENB (Q-NEFF-1 computed in an *uncommitted* scratchpad; nearest in-repo is `decompound_ddprot_2026-06-21/analyze_part1.py`), the Guardian CUSUM decay gate (built, calibrated, dormant), the joint-MC candidate-admission driver (hand-rolled per study).
- **Incidental findings surfaced by the audit (noted, not fixed here):** (a) `guardian_signal.py` + its tests are absent from disk in *both* this worktree and the main checkout (README-documented loss mode fired; recovery verified: `git show dc07898:…` bytes match the `PORT_MANIFEST.sha256` pin — restore not yet run); (b) the COT gold CSV has a live manifest hash mismatch, already tracked in `docs/notes/notice/N-2026-07-10-vendor-csv-manifest-drift.md`.

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
| Back-adjustment / CME clock / bid-ask-bounce data hygiene | `databento-data` schemas-and-symbology | Domain 7 — the futures-microstructure hygiene layer was entirely missing |
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

**Landed this commit (Tranche 1 + the discovery-campaign chain):** the reference doc;
the six doctrine additions in §2(2); the campaign template + defaults ADR + shakedown +
DISC-CAMP-0 pre-registration + pipeline-hardening handoff (the operator's chain, §0
anchors resolved, missing linchpin authored).

**Forward (deferred, tracked in `STATE.md`):**

- **T2 — Stage-1 scan instrumentation:** reusable **event-study harness** (constraint/flow family — highest persistence prior; our only mechanism-named finding, JPY month-end, lives there); **cheap detector kit** — promote Lo–MacKinlay VR to a tool, add Ljung-Box on r vs |r|, HAC-t, an autocorrelation-corrected n_eff helper (all via already-installed `arch`/`statsmodels`).
- **T3 — scanner calibration + admission tooling:** GARCH-fitted-null / surrogate-data pipeline calibration (also upgrades the corpus-FDR IID-Gaussian null); promote ENB + downside-correlation + with/without-candidate marginal-delta into committed tools (the operator's CC-handoff Track C covers the ENB breadth column — recover the Q-NEFF-1 computation into it).
- **T4 — riding the 2026-08-08 board:** compute the production Call-1 kill-line operating characteristics (false-kill rate, detection lag vs horizon) *before* the first decay review; build the owed rolling-PF σ-source harness + tier-demotion state writer.
- **Held (operator-gated):** the CC-handoff's 3 code tracks (db_fetch date-cap, `temporal_consistency.py`, breadth column) await the §0.5 answers (flag names; Track-B home; the — now-confirmed unnecessary — `portfolio_mc` extraction).

---

## §10 — Audit hooks (runnable)

```bash
# Reference doc present + flagged REFERENCE (not canonical)
grep -n "Status: REFERENCE" docs/methodology/references/statistics-of-tradable-anomalies.md

# Tranche-1 doctrine present
grep -n "Null hygiene" .claude/skills/strategy-validation/SKILL.md
grep -n "Filtered, not" .claude/skills/futures-anomaly-discovery/reference/tool-discipline.md
grep -n "Data hygiene" .claude/skills/databento-data/reference/schemas-and-symbology.md
grep -n "Backtest → live shrinkage" docs/methodology/backtest_live_shrinkage.md

# Ledger anchored (no cwd-relative default)
grep -n "parents\[4\]" .claude/skills/futures-anomaly-discovery/scripts/register_search.py

# Non-adoptions recorded
grep -nE "Kelly|SPRT|Ledoit|numeric π|numeric-π" docs/adr/2026-07-11-tradable-anomalies-statistics-adoption.md

# Changed NO locked constant (expect empty)
git diff --stat HEAD -- core/config/params.toml core/dd_protection.py core/portfolio_mc.py core/firm_rules.py
```

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-07-11-tradable-anomalies-statistics-adoption.md --type adr
python scripts/check_skill_refs.py --all
python scripts/check_path_liveness.py
python scripts/check_boundaries.py
python scripts/validate_params.py
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-11 | Initial authoring + acceptance (adopt reference; Tranche-1 doctrine; non-adoptions) | Joshua + Claude Code |
