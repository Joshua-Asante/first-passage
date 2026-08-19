# [Q-SIZECOMP-1] — Does the live c1 sizing formula compose the way doctrine says it does?

**Status:** `OPEN — DRAFT (pre-lock)` — execution requires a separate operator GO (parent-Q convention: naming is not opening)
**Authored:** 2026-08-18
**Closed:** N/A
**Authors:** Joshua + Claude Code
**Parent question:** N/A — opened from the [2026-08-18 assumption-sweep audit note](../notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md), findings A3 + D4
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q — closure gated on a $0/K=0 grep + local-arithmetic read of two already-cited production call paths
**Artifact path:** `docs/briefs/Q-SIZECOMP-1-sizing-composition.md`

---

## Section 0 — Rule 0 reads (production-source verification)

Every path below was read directly this session (spot-check against the audit note's citations, all matched byte-for-byte) or by the audit note's own dedicated sweep/verify agents. Anchors are `git log -1 --format="%h %ad" -- <path>`.

- `ops/c1_rail/c1_sizing_host_reference.py` — anchor `027a729` (2026-08-14). `:55` imports `from lifecycle import TIER_MULTIPLIER` only — no `get_effective_multipliers`, no `beta_death_assessment`. `:203-216` `_read_lifecycle_multiplier()` does a bare `TIER_MULTIPLIER[tier]` lookup. `:231` calls `calculate_protection(float(current_equity), effective_peak)["multiplier"]` — 2 positional args, no `lifecycle=` kwarg. `:270-280` `r_eff = base_risk * dd_scale * lifecycle_m` — no beta term in the formula, confirmed live this session.
- `core/lifecycle.py` — anchor `027a729` (2026-08-14). `:100-120` `beta_death_assessment()`. `:123-134` `get_effective_multipliers()`, docstring verbatim: *"This is what the live sizing path consumes."* Composes per-leg lifecycle × Call-4 portfolio beta multiplier.
- `core/dd_protection.py` — anchor `027a729` (2026-08-14). `:190-226` `calculate_protection(equity, peak, lifecycle=None)` — `scaled_risk[k] = BASE_RISK[k] * multiplier * lifecycle[k]`, `multiplier` is `DD_SCALE` when DD-triggered. `:449-452` and `:471-476` `main()` CLI — **confirmed live this session**: both the update-mode and status-mode branches call `beta = beta_death_assessment(get_lifecycle_multipliers(...))` and `calculate_protection(equity, peak, get_effective_multipliers(BASE_RISK.keys()))` — the diagnostic CLI's production call chain **does** reach the full triple-compound (DD_SCALE × per-leg-lifecycle × beta-death), asymmetric with the rail above.
- `tests/test_lifecycle.py` — anchor `027a729` (2026-08-14). `:90-99` `test_lifecycle_compounds_multiplicatively_with_dd_scale` — pairwise DD×lifecycle only (asserts the ratified 0.20× = 0.50×0.40 case). `:188-201` `test_effective_multipliers_fold_beta_derisk_when_3of4` — pairwise lifecycle×beta only. **Confirmed live this session: no test in this file constructs the three-way DD-triggered + WATCH-tier + beta-death case together.**
- `docs/methodology/strategy_lifecycle.md` — anchor `89d3e46` (2026-08-18). `:55-59` Call 2, the canonical formula `risk_pct_live[strategy] = BASE_RISK[strategy] × DD_SCALE × lifecycle_multiplier[strategy]`, plus the ratified "Integration layer" correction (08-03/08-06) that `dd_protection.py` and the c1 rail "never meet in one expression" — a *different*, already-closed question about which module computes what, not about whether beta composes into `lifecycle_multiplier` before it reaches either. `:61` ratifies the two-way 0.20× compound as intended. `:78-84` Call 4 — beta-death trigger, 3-of-4 legs → portfolio-wide 0.50×, described explicitly as *"a beta-level lifecycle multiplier across all legs."* `:123` — "the four current legs are one beta... Call 4 is what bites" for the live book today.
- `docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md` — this session's own commit (untracked at authoring time). §4 A3, D4 (the two findings this brief combines); §3 item 1 (adjacent, scoped out below); §6 (cross-cutting pattern naming the c1-rail prose-vs-code gap this Q sits inside).

---

## Section 1 — Context and motivation

The 2026-08-18 assumption-sweep audit note (`docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md`) surfaced two findings on the same sizing surface: **A3** (the live c1 rail never composes the Call-4 beta-death multiplier, despite `lifecycle.py`'s own docstring claiming it does) and **D4** (a real, reachable production call chain composes three multiplicative de-risk factors — `DD_SCALE`, per-leg lifecycle, and beta-death — into a triple-compound that the test suite only ever exercises pairwise). Both are read directly off `strategy_lifecycle.md` Call 2/Call 4 doctrine, which states the intended formula and ratifies the two-way 0.20× compound as by-design. The audit's own §6 names this the repo's dominant cross-cutting pattern: c1-rail live-safety interlocks described in prose with more rigor than they are wired in code. CLAUDE.md's live-execution posture section is the reason this matters now rather than later — the c1 rail is built and disarmed, `dry_run=false` is gated on M1, and every live sizing decision this rail will ever make runs through exactly the formula these two findings interrogate.

---

## Section 2 — Prior art / lineage

- **Audit note §3 item 1** (D-gate deletion) — a related but distinct question: whether the DD-protection multiplier itself is correctly derived for non-FXIFY firm `dd_type`s. Already closed with citation (`docs/adr/2026-07-13-dd-protection-concept-not-constant.md`). This brief does not re-open it — it holds `DD_SCALE`/`DD_TRIGGER` frozen and asks only about *composition* of already-frozen multipliers.
- **`docs/methodology/strategy_lifecycle.md`'s own "Integration layer (ratified — corrected against production)" note** (08-03, corrected 08-06) — already established that `dd_protection.py` and the c1 rail are two separate expressions that never merge into one. That correction is about *module boundary*; this brief is about whether the beta-death *term*, specifically, reaches the rail's expression at all. No overlap in claim, adjacent in surface.
- No prior Q in `docs/briefs/INDEX.md` touches beta-death composition specifically — this is the first.

---

## Section 3 — Question (Q-SIZECOMP-1)

**Pre-Q gate test (symptom-only rephrase):** "two code paths both claim to implement the sizing law `BASE_RISK × DD_SCALE × lifecycle_multiplier`; it is unknown whether they compute the same value for the same inputs, and unknown whether the one reachable production call chain that can exercise all three de-risk factors at once has ever been checked against its own doctrine." No fix is named — the question does not mention wiring, adding, or changing any call site.

**Q-SIZECOMP-1:** Does the live c1 sizing host's `r_eff` computation, and the one production call chain capable of composing `DD_SCALE`, per-leg lifecycle, and Call-4 beta-death together, actually match what `strategy_lifecycle.md`'s own Call 2/Call 4 doctrine and the diagnostic CLI's own code state that composition should be?

---

## Section 4 — Falsifiable hypothesis (H-SIZECOMP-1)

**H-SIZECOMP-1** (two named limbs, one verdict):

- **Limb-A (rail composition, A3):** the live rail (`ops/c1_rail/c1_sizing_host_reference.py`) never calls `core.lifecycle.get_effective_multipliers` or `core.lifecycle.beta_death_assessment` anywhere under `ops/` — its `r_eff` formula structurally cannot include the beta-death term doctrine says it should.
- **Limb-B (triple-compound reachability + coverage, D4):** the diagnostic CLI's production call chain (`dd_protection.py main()`) *can* reach the full triple-compound in one call, computes it exactly as `BASE_RISK × DD_SCALE × (lifecycle × beta)`, and no test in `tests/test_lifecycle.py` exercises that three-way case — only the two pairwise cases are asserted.

**Reject H-SIZECOMP-1 if:** EITHER (a) a call to `get_effective_multipliers` or `beta_death_assessment` exists anywhere under `ops/` (Limb-A false — the rail already composes beta), OR (b) the local triple-compound arithmetic check (§7/§10) does **not** return `BASE_RISK[k] × 0.40 × 0.25` exactly for a DD-triggered + WATCH-1 + beta-death input (Limb-B false — doctrine's own compound math is wrong, a distinct and larger defect than the one this brief tests for).

**Accept H-SIZECOMP-1 if:** Limb-A confirms (zero `ops/` hits, `:55` imports only `TIER_MULTIPLIER`) **and** Limb-B confirms (arithmetic checks out exactly **and** no existing test constructs the three-way case).

**Ambiguous-hold if:** the two limbs disagree in a way §6 does not pre-anticipate — e.g. Limb-A confirms but the triple-compound arithmetic in Limb-B does not check out cleanly (surfacing a second, deeper `calculate_protection` defect this $0-scope brief cannot triage), or a grep hit under `ops/` turns out to be dead/test-only code whose reachability is a judgment call this brief does not pre-authorize.

---

## Section 5 — Forbidden moves

- **Assuming the CLI and the rail compute the same `r_eff` because both import from `core/lifecycle.py` / `core/dd_protection.py`.** This is the tempting move flagged going into this brief, and it is already falsified by §0: the rail imports only `TIER_MULTIPLIER` (`:55`) and computes `r_eff` inline (`:270-280`); the CLI imports and calls `get_effective_multipliers` + `beta_death_assessment` (`:449-476`). Shared module imports are not a shared call path — verified directly, not assumed.
- **Reading a confirmed Limb-A hold as license to wire `get_effective_multipliers` into the rail under this brief.** That is a fix, not a finding. The rail's own header doctrine deliberately diverges from `lifecycle.py`'s read-only default ("fail toward zero size" vs. a display-safe `AUTHORIZED` fallback) — whether and how beta composition belongs in a fail-safe live path is a separate design decision this $0/K=0 brief has no authority to make.
- **Treating the CLI's triple-compound call chain as evidence live money has ever been sized this way.** `main()` is a read-only, operator-invoked local-state status/update tool, never wired to the c1 rail's execution path. No strategy is deployed on c1 (CLAUDE.md live-execution posture). Conflating "the diagnostic path can compute it" with "live risk has ever included it" would misstate the posture.
- **Re-deriving `DD_TRIGGER`/`DD_SCALE`/`BETA_DEATH_COUNT`/`BETA_DEATH_DERISK` as part of this Q.** All four are frozen constants guarded at import (`dd_protection.py`'s MVD self-check; `lifecycle.py`'s own spec-pin at `:193`). This Q asks only whether already-frozen multipliers compose the way doctrine says — never whether the constants themselves are correctly set.

---

## Section 6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition (typed) |
|---|---|---|
| `RESOLVED` | Limb-A confirms (0 `ops/` hits; `:55` imports `TIER_MULTIPLIER` only) **and** Limb-B confirms (arithmetic exact **and** no 3-way test exists) | `INTEGRATE` — record the rail/CLI composition asymmetry as an evidence-ratified fact and file the missing-test gap against `tests/test_lifecycle.py`; name (do not open) a successor decision packet for the operator on whether/how the rail should compose beta-death before `dry_run` is ever considered. No code change under this brief. |
| `FALSIFIED` | Limb-A **or** Limb-B does not confirm as stated (rail already calls `get_effective_multipliers`/`beta_death_assessment`, **or** the triple-compound arithmetic diverges from `BASE_RISK × 0.40 × 0.25`) | `STOP` — the composition-asymmetry claim as stated is wrong; re-proposal needs a fresh grounding read, not a re-run of the same grep/arithmetic. |
| `AMBIGUOUS-HOLD` | Limb-A confirms but Limb-B's arithmetic does not check out cleanly (a deeper `calculate_protection` defect surfaces), or a grep hit's reachability is ambiguous (dead/test-only code) | `ITERATE` — name (do not open) a successor Q scoped to whichever limb produced the ambiguity; carry forward the confirmed limb's result verbatim. |

**Pre-registered before either limb is read against these numbers.** §6 is not amended to match what the read returns.

---

## Section 7 — Execution plan (self-executing, $0/K=0 — reuse the cheap-falsifier sketches supplied)

- **Phase 0 — Rule-0 reads.** Done (Section 0).
- **Phase 1 — Limb-A (rail composition).**
  ```bash
  grep -n "get_effective_multipliers\|beta_death_assessment\|BETA_DEATH" ops -r    # expect 0 hits
  ```
  Cross-check `ops/c1_rail/c1_sizing_host_reference.py:55` imports (expect only `TIER_MULTIPLIER`) against `core/dd_protection.py:449-476` (expect it DOES call `get_effective_multipliers`), confirming the asymmetry.
- **Phase 1 — Limb-B (triple-compound arithmetic + coverage).**
  ```python
  from dd_protection import calculate_protection, BASE_RISK
  lc = {k: 1.0 for k in BASE_RISK}
  lc["Guardian"] = 0.50 * 0.50   # WATCH-1 (0.50) x beta-death (0.50) = 0.25
  equity = 200_000.0 * (1.0 - 0.020)   # DD triggered
  result = calculate_protection(equity=equity, peak=200_000.0, lifecycle=lc)
  assert result["scaled_risk"]["Guardian"] == BASE_RISK["Guardian"] * 0.40 * 0.25
  ```
  Plus: `grep -n "def test_" tests/test_lifecycle.py` read against the two pairwise tests at `:90-99`/`:188-201` — confirm no third test constructs this exact case.
- **Phase 2 — Verdict assertion.** Apply Section 6 mechanically. Produce the closure per Section 9.

Estimated cost: **$0, K = 0.** Both phases are a grep and a ~5-line local Python snippet against already-committed code; no new data, no new backtest, no manifest.

---

## Section 8 — Verdict pre-registration

Owed at operator GO, committed before Phase 1 executes: `docs/briefs/pre-registration/Q-SIZECOMP-1-verdict-preregistration.md`, containing the Section 6 table plus the exact threshold numbers, frozen before either falsifier is run. Not yet authored — this Q is named, not opened.

---

## Section 9 — Closure record format

Per `references/closure_record.md`, with the mandatory typed `## Iterate` block. `RESOLVED` → `docs/briefs/closures/Q-SIZECOMP-1-closure-resolved.md`; `FALSIFIED` → `…-closure-falsified.md`; `AMBIGUOUS-HOLD` → `…-closure-ambiguous-hold.md` with the re-test trigger named. Closure must walk both limbs' routes explicitly, not just the one that fired.

---

## Section 10 — Audit hooks (runnable)

```bash
# Limb-A — rail never composes beta-death (A3)
grep -n "get_effective_multipliers\|beta_death_assessment\|BETA_DEATH" ops -r
# expect 0 hits

# Limb-A cross-check — rail imports vs CLI imports
sed -n '53,55p' ops/c1_rail/c1_sizing_host_reference.py
# expect: only `from lifecycle import TIER_MULTIPLIER`
sed -n '449,452p;471,476p' core/dd_protection.py
# expect: get_effective_multipliers(...) and beta_death_assessment(...) both called

# Limb-B — the missing three-way test (D4)
python -c "
from dd_protection import calculate_protection, BASE_RISK
lc = {k: 1.0 for k in BASE_RISK}
lc['Guardian'] = 0.50 * 0.50
equity = 200_000.0 * (1.0 - 0.020)
result = calculate_protection(equity=equity, peak=200_000.0, lifecycle=lc)
expect = BASE_RISK['Guardian'] * 0.40 * 0.25
assert result['scaled_risk']['Guardian'] == expect, (result['scaled_risk']['Guardian'], expect)
print('Limb-B triple-compound OK:', result['scaled_risk']['Guardian'], '==', expect)
"

# Limb-B coverage check — confirm no existing test builds the 3-way case
grep -n "def test_" tests/test_lifecycle.py
```

---

## Verification

```bash
# Discipline checks (mechanical; repo-side tool — canon vs skill-side tool UNRULED per MEMORY.md)
python scripts/check_brief.py docs/briefs/Q-SIZECOMP-1-sizing-composition.md --type inquire

# Production-source verification (Section 0 anchors)
git log -1 --format="%h %ad" -- ops/c1_rail/c1_sizing_host_reference.py core/lifecycle.py core/dd_protection.py tests/test_lifecycle.py docs/methodology/strategy_lifecycle.md

# Cross-reference verification (cited facts match canonical sources)
sed -n '203,216p;231p;270,280p' ops/c1_rail/c1_sizing_host_reference.py
sed -n '100,134p' core/lifecycle.py
sed -n '90,99p;188,201p' tests/test_lifecycle.py
```

If any verification command fails, the brief is not complete.

---

## Pre-Lock Checklist (DRAFT briefs only)

- [x] Section 0 paths read with anchors
- [x] Section 3 passes the symptom-only rephrase
- [x] Section 4 hypothesis binary
- [x] Section 5 forbidden moves genuinely tempting
- [x] Section 6 triggers specific
- [ ] Section 8 pre-registration owed at operator GO — not yet committed
- [x] Section 10 hooks runnable
- [ ] Operator GO owed before Phase 1 — this brief is named, not opened
