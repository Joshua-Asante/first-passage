# ADR 2026-06-05 — Parameter Sweep Engine

**Status:** `Accepted`
**Machinery-status:** ⚠ **RETIRED 2026-07-11; the decision is NOT withdrawn.** The tree this ADR
designed (`validation/sweep/` → later `lab/validation/sweep/`) was deleted by
[`2026-07-11-gen1-pipeline-retirement.md`](2026-07-11-gen1-pipeline-retirement.md), which names this ADR as
"the two-tier sweep engine being retired". Read every present-tense claim below — including §2's
scope on `validation/sweep/` — as **historical**. The *doctrine* survives and is live:
**Python never gates deployment; pre-filter and confirm use the same feed** — still cited as the
two-tier [`2026-06-23-tv-backtest-egress-automation.md`](2026-06-23-tv-backtest-egress-automation.md)
builds on ("the Python-prefilter/native-confirm two-tier this builds on").
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** [`2026-07-11-gen1-pipeline-retirement.md`](2026-07-11-gen1-pipeline-retirement.md) (machinery only — the doctrine survives per the Machinery-status line above)
**Retain-until:** none
**Decision date:** 2026-06-05
**Authors:** Joshua (CEO, decider) + Claude (Tech Advisor)
**Related:** `docs/ltm/briefs/rnd-pipeline/CC-HANDOFF-sweep-layer.md` (§0.5-Q1, §2.3 parity gate), `docs/ltm/briefs/rnd-pipeline/CC-HANDOFF-validation-harness.md` (§2.4 DSR / §2.3 PBO, both N-aware), `docs/ltm/briefs/rnd-pipeline/CC-HANDOFF-codification-scaffold.md` (§2.5 sweep sidecar), `docs/notes/2026-06-05-rnd-pipeline-anchor-correction.md` (anchor corrections this ADR rests on)
**Layer:** infrastructure

> **Status: ACCEPTED 2026-06-05** by Joshua (CEO). Drafted by Claude (Tech Advisor); ratified per the §Ratification checklist below. The total-N amendment (§6) has been propagated into the sweep handoff §2.5. Filed under the repo's ISO-date ADR convention.

---

## §0 — Rule 0 reads (production-source verification)

Files read **before** authoring this ADR. Anchors verified on-disk 2026-06-05 (worktree HEAD `7c864aa`). The decision rests on the execution-leakage / feed-divergence doctrine being real and on the harness being N-aware — both confirmed below.

- `CLAUDE.md` — anchor: worktree HEAD `7c864aa` (2026-06-05). Confirms the locked four (Guardian v5.5, Striker DJ30 v4.5, Aegis v4.3, NAS100 v1), the Pepperstone validation panel, and the objective function (portfolio pass-rate, not Sharpe).
- `dd_protection.py` — `DD_TRIGGER=0.015`, `DD_SCALE=0.40` (C2, locked 2026-05-08). The Python pre-filter must replicate these sizing constants for parity; the native tester runs the real Pine.
- `portfolio_mc.py` — `load_trades(path, *, strategy=, apply_swap=) -> DataFrame` (line 243) and `compute_default_config(...)` (line 555). Per-strategy input schema the sweep's trial-set / the harness disposition record must match. Reads the Pepperstone panel CSVs.
- `docs/notes/notice/N-2026-05-29-pepperstone-alchemy-feed-divergence.md` — the feed-divergence finding (Pepperstone↔Alchemy **price-basis** divergence), separately tracked.
- `archive/docs/briefs/preq_eurusd_pattern_enumeration.md:35` and `docs/audits/2026-05-16-inqhiori-programme-audit.md:19` — the **~50% execution-leakage** doctrine (Forward Asymmetry, 2026-05-15). This replaces the unverifiable "~78%" figure the source draft asserted (see anchor-correction note).
- `data/tv_exports/pepperstone/` (+ `SHA256SUMS`) — the validation feed (gitignored CSVs; manifest tracked). No native-Strategy-Tester parity export is committed yet; the parity anchor must be produced manually (sweep §0.5-Q1).
- `validation/` — confirmed **greenfield** (harness + sweep not yet built); this ADR governs the sweep engine they will share.

**Pre-ratification confirmation (Joshua, at ACCEPT time):** re-run the §10 anchor checks; if any cited anchor no longer verifies, correct before flipping status.

---

## §1 — Context

The R&D pipeline needs a parameter-sweep layer between codification and the validation harness. The stated objective is **speed and pass-rate** — and these pull against each other at the engine choice:

- **Speed** requires running large grids cheaply, which requires programmatic execution.
- **Fidelity** requires that swept metrics describe the *deployable* strategy on a deployment-consistent feed.

The binding constraint: **there is no first-class programmatic Pine sweep API.** A Pine strategy runs one config at a time on TradingView; the platform's own multi-config workflow is manual export-and-compare. Any automated sweep therefore either (a) drives the native tester through automation, (b) runs many configs inside one Pine script, or (c) re-implements the strategy outside Pine.

**The governing doctrine:** execution leakage runs at ~50% of modeled edge (Forward Asymmetry, 2026-05-15), and feed divergence between backtest and deployment is a documented, separately-tracked contributor (Pepperstone↔Alchemy price-basis divergence, Notice N-2026-05-29), addressed by the same-source discipline (running the backtest and deployment off a single feed). Implementation divergence — validating one artifact and trading another — is the same disease at the validation layer. Any engine that scores a strategy differently than the deployed Pine reintroduces that error class.

**Decision driver (one sentence):** the sweep is the join between codification and the harness, and choosing its engine *is* choosing what "validated" means — so it must be decided structurally before the sweep handoff runs, not defaulted inside it.

---

## §2 — Decision

**Two-tier sweep engine:**

1. **Pre-filter (fast, NO gate authority):** a Python re-implementation runs the full grid on the Pepperstone feed and produces a ranked shortlist.
2. **Authoritative gate:** the shortlist is re-run on the **native TradingView Strategy Tester** (the real Pine, real engine, same feed). Only native-tester results gate deployment.

**The invariant that makes this safe: Python never gates deployment.** It proposes; native Pine disposes. A Python↔Pine mismatch can only ever produce a false shortlist entry (caught at the confirm step) or a missed candidate (a recall cost, never a fidelity-of-deployed-strategy cost). Nothing is ever deployed on Python numbers.

**Effective:** immediately upon acceptance.
**Scope:** all parameter sweeps in the R&D pipeline (`validation/sweep/`); the native tier is the only deployment-gating authority.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **(A) Native-tester only (browser-driven)** | Zero divergence — the swept artifact IS the deployable one. Rejected as *sole* engine: tester throughput caps grid width, starving the speed objective for wide exploration. **Retained as the authoritative tier** in the chosen design. |
| **(B) In-Pine multi-config optimizer** | Stays in Pine but carries documented fill-accuracy caveats for crossover/crossunder exits vs. the native tester — i.e., least faithful on exactly the order type the SNAG strategies use. Rejected on fidelity: divergence lands precisely where the strategies live. |
| **(C) Python re-implementation only** | Fastest and fully programmable, but gates deployment on a divergent artifact — the implementation-divergence version of the feed-divergence error. Rejected as sole gate. |
| **(D) Two-tier: C pre-filters, A confirms — CHOSEN** | Buys speed where it is cheap (narrowing) and pays for fidelity only where it gates (a small confirmed shortlist). Consistent with The Algorithm (automate the cheap step; keep the authoritative gate faithful) and forward-asymmetry (the cheap engine's errors are bounded and recoverable; the expensive engine owns anything irreversible). |
| **Status quo — no sweep layer** | Leaves codified candidates with no path to the harness; the pipeline cannot close. Worse than choosing. |

---

## §4 — Falsifier (revert trigger)

> **If**, across a representative sample of configs, the Python pre-filter's rank-ordering disagrees with the native Strategy Tester's beyond the stated threshold (Spearman ρ below the agreed floor), **then** Python is not a valid pre-filter — its shortlists would discard configs native Pine would keep — and the decision reverts to **(A) native-tester-only**, accepting the speed cost.
> **And if** the total-N accounting cannot be honestly maintained through the two-tier emitter, the harness's correction is compromised and the design must collapse to single-engine.

Both are binary and runnable: a rank-correlation script on a config sample, and an emitter unit test asserting reported N == expanded grid size.

**Revert action:** supersede this ADR; sweep §2.2 engine adapter switches to native-only.
**Trigger check schedule:** re-run the rank-correlation falsifier on each new strategy family added to the pipeline (sweep §10 hook).

---

## §5 — Forbidden moves (under this ADR)

1. **Reporting N = shortlist instead of N = total examined to the harness.** Silently breaks the overfitting correction — the single most important rule in this ADR. The harness's DSR and PBO scale their bar with N = number of trials examined in selecting the winner; in the two-tier design that is the **full pre-filter grid**, not the confirmed shortlist.
2. **Letting Python results gate deployment directly.** The no-authority invariant is the whole safety argument; if it bends, the decision collapses to rejected option (C).
3. **Tuning the parity or rank-correlation thresholds after seeing results** to make the pre-filter "pass." Methodology-layer p-hacking (Known Trap #12); threshold changes route through `programme-audit`, manually.
4. **Skipping the authoritative confirm** because a shortlist is small or "obviously good." Every deployment-bound config passes native Pine.
5. **Different feed for pre-filter vs. confirm.** Reintroduces feed divergence — the dominant historical leakage class.
6. **Re-proposing a rejected §3 alternative without new evidence.** Options A-as-sole / B / C are ruled out for stated reasons; reviving one requires new evidence that invalidates the §3 reason, not a casual revival.

---

## §6 — Consequences

**Load-bearing — trial-count accounting (do not miss this).** The harness's DSR and PBO scale their bar with N = number of trials examined in selecting the winner. In the two-tier design that is the **full pre-filter grid**, not the confirmed shortlist. If a 5,000-config Python pre-filter narrows to a 50-config confirm, the multiple-testing exposure is 5,000 — reporting N = 50 understates selection intensity and renders the correction too weak. **Therefore:**
- The sweep emitter (amends `CC-HANDOFF-sweep-layer.md` §2.5) must report **total examined N = pre-filter count**, and tag each trial as pre-filter vs. authoritative-confirm.
- DSR inputs: cross-trial Sharpe variance from the **full pre-filter set** (the actual search distribution); the selected config's point Sharpe from the **authoritative confirm** run.
- The pre-filter does not escape the multiple-comparisons accounting by virtue of running on a cheaper engine.

**Two fidelity bars for two roles (clarifies sweep §2.3).**
- *Pre-filter (Python):* the job is ranking, so the fidelity requirement is **rank-order agreement** with native Pine (Spearman ρ across a representative config sample above a stated floor), not exact P&L parity.
- *Authoritative (native tester):* this is the deployed artifact, so the bar is **exact-ish parity** — trade count exact, net profit/PF within a tight band (sweep §2.3 / §0.5-Q3).

**Positive consequences:**
- Speed and fidelity both retained; divergence contained by construction; the authoritative number is always the deployable one.

**Negative consequences (real cost):**
- Two engines to build and keep in parity; total-N bookkeeping adds emitter complexity.

**Risks (probabilistic):**
- The rank-correlation falsifier must be monitored, not assumed (mitigation: §10 per-family re-check).

**Sub-decision — how the native tier is driven. RESOLVED 2026-06-05 (deferral ratified):** the **first cut is locked as Python pre-filter + documented manual confirm** of the native Strategy Tester — the option this ADR already named valid. The two automation paths are dispositioned, not merely deferred:
- *Vetted third-party optimizer* — **rejected** on the repo's own security posture: it hands private Pine strategy logic and account access to an external party, which directly contradicts the "Pine held privately to protect the live edge" doctrine (CLAUDE.md §Public-clone posture). Re-proposal requires a posture change, not just a faster vendor.
- *Own Claude-in-Chrome Strategy-Tester automation* — **deferred, not rejected.** Building it now is premature: stage 3 (sweep) is not yet built, so there is no live pre-filter shortlist to drive, and the manual-confirm volume that would justify automation is zero. **Revisit trigger:** once the sweep layer is built AND manual native confirmation of pre-filter shortlists becomes a measured throughput bottleneck (or the shortlist cadence exceeds what manual confirm can clear), open a follow-up ADR for the in-house driver. Until then, manual confirm is the authority path.

**Downstream artifacts that need updating on ACCEPT:**
- `CC-HANDOFF-sweep-layer.md` §2.5 — propagate the total-N amendment before that handoff is dispatched.

---

## §7 — Implementation plan

- **Phase 0** — at ACCEPT time, re-verify §0 anchors (§10 checks).
- **Phase 1** — propagate the §6 total-N amendment into `docs/ltm/briefs/rnd-pipeline/CC-HANDOFF-sweep-layer.md` §2.5.
- **Phase 2** — flip status `Proposed` → `Accepted` (done 2026-06-05); native-tier-driver sub-decision resolved 2026-06-05 (deferral ratified — Python pre-filter + manual confirm; see §3).
- **Phase 3** — sweep handoff dispatched only after the harness (§2.7 trial-set contract) and codification sidecar (§2.5) exist as built artifacts.

---

## §10 — Audit hooks (runnable)

```bash
# Rank-order fidelity of the pre-filter vs native (the §4 falsifier)
# script: spearman(python_ranks, native_ranks) over a representative config sample; assert >= floor

# Total-N honesty (forbidden move #1)
# test: emitter reports N == full pre-filter grid size, not shortlist size

# No-authority invariant (forbidden move #2)
grep -rn "deploy\|gate\|authoritative" validation/sweep/*.py   # python tier carries no deploy/gate path

# Corrected anchors still verify (the doctrine this ADR rests on)
grep -rn "execution leakage" archive/docs/briefs/preq_eurusd_pattern_enumeration.md docs/audits/2026-05-16-inqhiori-programme-audit.md
ls docs/notes/notice/N-2026-05-29-pepperstone-alchemy-feed-divergence.md

# No stale 78% anchor in this ADR or the staged briefs
grep -rn "78%" docs/adr/2026-06-05-sweep-engine.md docs/briefs/rnd-pipeline/ ; echo "expected: no matches"

# Schedule: re-check rank-correlation falsifier on each new strategy family added to the pipeline
```

---

## Verification

```bash
# Discipline checks (mechanical)
python "C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py" docs/adr/2026-06-05-sweep-engine.md --type adr
# Expected: all checks PASS

# §0 anchors real
git -C . log --oneline -1
grep -n "load_trades\|compute_default_config" portfolio_mc.py
grep -n "DD_TRIGGER\|DD_SCALE" dd_protection.py
```

---

## Ratification

- [x] Joshua reviews and sets status `Accepted` / `Amended` / `Rejected` — **ACCEPTED 2026-06-05**
- [x] On `Accepted`: propagate the §6 total-N amendment into `CC-HANDOFF-sweep-layer.md` §2.5 before that handoff is dispatched — **done 2026-06-05**
- [x] Resolve the open sub-decision (native-tier driver) as a follow-up — **RESOLVED 2026-06-05**: deferral ratified. First cut locked = Python pre-filter + documented manual confirm; third-party optimizer rejected on security posture; in-house automation deferred with a revisit trigger (see §3).

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-06-05 | Initial authoring (PROPOSED); anchors corrected per `docs/notes/2026-06-05-rnd-pipeline-anchor-correction.md` | Joshua + Claude |
| 2026-06-05 | Ratified **ACCEPTED**; §6 total-N amendment propagated into sweep handoff §2.5 | Joshua |
| 2026-06-05 | Native-tier-driver sub-decision RESOLVED (deferral ratified: Python pre-filter + manual confirm; third-party optimizer rejected on security posture; in-house automation deferred w/ revisit trigger) | Joshua + claude.ai |
| 2026-06-13 | **Execution-model extended to LONG-SHORT** (+ Donchian breakout entry primitive) in lockstep across the scaffold (`scaffold.pine.tmpl`) and the Python pre-filter (`engine._simulate`); the short side is OPTIONAL — the Python engine's long-only path is byte-for-byte unchanged (`short_signal=None` → original 4-array validation + long-only branch), while emitted long-only *Pine* gains a constant `shortSignal = false` + a dead short block + a `position_size != 0`/`close_all` stale-exit that **compile but never fire** (behaviorally equivalent for long-only, not byte-identical text). **Also added a TRAILING ATR/chandelier exit** (`SignalArrays.trailing`, `chandelier_exit()`, scaffold `useTrailing` ratchet) — optional, default fixed-stop+TP unchanged; selected by a `trail`/`chandelier` hint. **No ADR invariant changes:** Python still carries no gate authority (§2/§5 #2), total-N accounting is unaffected (§6), and the new long-short + trailing family must clear the §4 rank-ρ falsifier + the §6 native-parity bar before it can gate — which the §4 per-family re-check schedule already requires (NOT yet run for this family). Scope/design: [`docs/spec/2026-06-13-codifier-breakout-longshort-trailing-extension.md`](../spec/2026-06-13-codifier-breakout-longshort-trailing-extension.md). | Joshua + Claude Code |

## Addendum 2026-08-14 — machinery retired; two-tier invariant remains live

**Type:** dated correction under Rule 14. **§2 decision text is not edited.** Header `Machinery-status` is the reader-intercept (same pattern as [`2026-06-05-concept-admissibility.md`](2026-06-05-concept-admissibility.md)).

[`2026-07-11-gen1-pipeline-retirement.md`](2026-07-11-gen1-pipeline-retirement.md) retired `validation/sweep/` / `lab/validation/sweep/` and named this ADR as the two-tier sweep engine being retired. The core invariant — Python never gates deployment; pre-filter and confirm use the same feed — is **not** withdrawn and remains live doctrine.

| Date | Change | By |
|---|---|---|
| 2026-08-14 | Addendum 2026-08-14 — machinery retired, doctrine live. §2 body byte-unchanged. | claim-alignment reconciliation |
