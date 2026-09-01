# Recommendation — prop survivor scoring + dd_protection concept-not-constant reframe

**Status:** **RATIFIED 2026-07-13 (operator) — §6 `RESOLVED` path, no dial adjustments.** All three §6(i)–(iii) items confirmed as recommended: the 3.0%/1.0%/pass-floor(≥50%) numbers, the four frozen $100K tiers + discharge rule, and the reframe ADR scope. Ratification record: §7. Numbers are now fixed per §6/trap-#12 — any post-ratification change needs a fresh brief.
**Authored:** 2026-07-12 · Claude Code (Opus 4.8), operator-directed
**Operator directives (2026-07-12, verbatim intent):** (a) "make your best recommendation on survivor scoring"; (b) "keep dd_protection as a concept, not as a constant. it is portfolio and prop firm variable"; (c) DISC-CAMP-0 unfrozen; (d) Objective-Map hook retired.
**Loop of record:** STRATEGIC
**Feeds:** the survivor-scoring **pre-registration** (must freeze before the first scored re-MC) and the **dd_protection reframe ADR** (the audit-D2 vehicle). This brief is the recommendation record, not either artifact.
**Verification:** developed + adversarially verified by a 13-agent workflow (2026-07-12): 6 independent design angles (3 scoring, 3 reframe) + consumer map → 2 judge syntheses → 3 adversarial verification passes (pin/anchor lens, actionability lens, scoring-correctness lens). All 3 passes: **no hard-constraint break**. Required fixes folded in (§2.4, §3.4).

---

## §0 — Rule-0 reads (production source, verified this session)

All content-read from the working tree at `344c67b` (2026-07-12); per-file anchors:

- `core/dd_protection.py` @ `99b7854` — DD_TRIGGER=0.015 / DD_SCALE=0.40 literals (L69-70); import-time MVD self-check `_validate_protection_rule()` raises on any drift (L266-275); `calculate_protection` (L174-210) is NOT on the MC engine path; `DAILY_LOSS_LIMIT = _F["daily_loss_pct"]/100` import-time hazard (L63); 2026-07-11 historical-fixture note (L24-33).
- `core/firm_rules.py` @ `0e26a7b` — `ACTIVE_FIRM="FXIFY"` (L320, asserted L321); `AUTOMATION_FRIENDLY_PROP_FIRMS` 4 families (L290-312); all prop tiers carry `daily_loss_pct: None`; dd_type per family: Bulenox/BluSky `trailing`, Tradeify/MFFU `trailing_locking`; $100K tiers all at `max_dd_pct: 3.0` / `profit_target_pct: 6.0` (L88/197/241/275); `cost_per_side_usd` encoded ONLY for Bulenox tiers.
- `core/mc/simulation.py` @ `e9be4ec` — runtime daily-loss gate already `None`-safe (L61-64); dd_type branch chain: trailing %-of-peak (L66-76), trailing_locking fixed-$ + lock (L77-89), static `elif` (L90-94); scale trigger fires off `dd_from_peak` for ALL dd_type (L52).
- `core/mc/modes.py` @ `f2be990` — headline `bust_rate` = daily+static only (L285); `bust_trailing` absent from the return dict (L292-316); argparse defaults thread the literal DD_TRIGGER/DD_SCALE (L1250-1253); import-time `daily_loss_pct/100` (L53).
- `ops/prop_envelope_default.md` @ `802ee60` — E1-E7; §2 DEPLOYABLE-DEFAULT-ENVELOPE YES/NO contract; §5 five open items (PROVISIONAL v0.1).
- `docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md` @ `0e26a7b` — §4 falsifier: "bust rate below an operator-pre-registered ceiling on ≥2 of the four FRIENDLY firm tiers" (ceiling never set); NB §4 internal wording tension (H says bust ceiling, revert trigger says "pass-rate ceiling").
- `docs/ltm/briefs/rnd-pipeline/DISC-CAMP-0-shakedown.md` @ `73d872f` — §6 gate (SPA + DSR≥0.95 + consistency ≥5/7 + MGC realism), §7 Stage-8 breadth.
- Prior-art calibration: `lab/analysis/c1/tradeify_futures3_remc_2026-07-11/RESULTS.md` — falsified locked-book 3-leg transfer on Tradeify trailing_locking 100K: bust 17.70% (%-equity), 13.37% (prior-panel with-costs per RESULTS.md:49). *(Secondary figures cited in an earlier draft — "4.59% integer-micro", "1.05-1.11%" — are NOT in that RESULTS.md; dropped per adversarial verification. The 17.70% primary calibration is confirmed.)*

**Hard constraints these reads establish (any recommendation violating one is void):**
A. FXIFY MC anchor 99.83/0.17/4.37 stays byte-reproducible (needs ACTIVE_FIRM=FXIFY + 0.015/0.40 literals untouched).
B. `_validate_protection_rule()` must keep passing at import — no rebind of the DD_TRIGGER/DD_SCALE literals (both `validate_params.py` and `verify_lock_anchors.py` require `ast.Constant` RHS).
C. `ACTIVE_FIRM` switch requires a firm-onboarding ADR + re-MC.
D. Prop-tier re-MC is blocked until the engine pre-flight handles `daily_loss_pct=None` (import-time sites: `dd_protection.py:63`, `mc/modes.py:53`, `mc/simulation.py:18`, `scripts/inactivity_simulator.py:55` — runtime gate at `simulation.py:61-64` is ALREADY None-safe; the hazard is import-time only, and only if a prop tier ever flows into the module constants).

---

## §1 — Two load-bearing engine findings (surfaced by the verification, must shape both artifacts)

**F1 — the headline-bust trap.** `compute_default_config`'s returned `bust_rate` is daily+static only (`modes.py:285`) and never surfaces `bust_trailing`. For a prop tier, ALL busts route to `bust_trailing` (daily branch skipped on `None`; static is an `elif` never reached under trailing dd_types) — so a naive harness reads ~0% bust for a prop tier. **The prop harness must aggregate `bust_trailing` from `run_seed` outcomes directly** (as `run_tradeify_futures3_remc.py` already does) and assert: headline bust = daily+static+trailing AND all outcome buckets sum to 1.0 per seed.

**F2 — engine faithfulness is not uniform across the four firms.** `trailing_locking` (Tradeify/MFFU) models a fixed-$ EOD trail — engine-FAITHFUL at eval. `trailing` (Bulenox/BluSky) models %-of-peak, but both firms' real rules are fixed-$ trails → the engine's cushion grows with equity → bust UNDERSTATED (optimistic). Bulenox Option-1 is additionally intraday vs the EOD-sum engine — doubly optimistic. Faithfulness at eval: Tradeify/MFFU > BluSky > Bulenox.

---

## §2 — Survivor-scoring recommendation

### §2.1 Staged scorecard (G0–G8)

A DISC-CAMP-0 §6-RESOLVED survivor (with banked K/DSR ledger, CUSUM decay spec, mechanism disposition, Stage-8 breadth read) traverses:

- **G0 Intake** — no firm names attached (envelope §2.4).
- **G1 Deployable-expression reduction (E1)** — decompose to EOD-flat per-session form; record round-trip count R_deploy + deployable/research expectancy ratio; emit `DEPLOYABLE-DEFAULT-ENVELOPE: YES/NO`. NO → research-valid/non-deployable register, STOP (valid outcome, envelope §3).
- **G2 Cost-law kill gate (E5)** — parent→micro 1:10 rescale; micro_contract_cap feasibility; gross-edge vs ≥4× cost hurdle at R_deploy. **Gap:** `cost_per_side_usd` exists only for Bulenox — Tradeify/MFFU/BluSky commissions must be sourced (90-day-fresh) at pre-registration or their cost gate is blocked.
- **G3 Engine pre-flight** — constraint D + the F1 aggregation assertion, GREEN before any re-MC.
- **G4 Per-firm re-MC** — deployable panel, firm_kwargs threaded (never module constants), 10k×3 seeds, inactivity disabled. Run TWICE where eval consistency exists: Run-1 consistency-off, Run-2 consistency-on — **gate on Run-2** (consistency extends exposure; `simulation.py:113-121`).
- **G5 Bust + pass-floor scoring** vs the §2.2 ceiling, per-geometry per §2.3.
- **G6 Standalone-vs-portfolio-slot routing (E2)** — concentrated edges whose Run-2 pass collapses are PORTFOLIO-SLOT-ONLY. Candidate #1 scores STANDALONE (no companion book exists yet; the ADR's book-as-first-class-unit activates when one does).
- **G7 Funded-phase ruin + scaling diagnostic** — funded geometry (intraday for Tradeify/MFFU) + tightest tiers; count of tiers holding bust ≤1% is the dominant score term; does NOT gate §4.
- **G8 Admission** — clear → lifecycle CANDIDATE @1.00× carrying CUSUM spec + DEPLOYABLE annotation; becomes §4-falsifier evidence. Rail/account stay separately gated.

### §2.2 The numeric ceiling to pre-register (two-part)

- **Part A — §4 eval gate: headline bust ≤ 3.0%** (daily+static+trailing) on the deployable expression, Run-2, at the $100K common band, **paired with a pass floor** (P(pass) ≥ 50% with finite median-days-to-target inside a practical horizon). Discharged iff both hold on ≥2 distinct firms.
- **Part B — funded ruin ceiling: bust ≤ 1.0%** on funded geometry — gates allocation scaling, NOT the §4 falsifier.

**Rationale:** 3.0% is the $100K band's own barrier width (all four firms at max_dd_pct 3.0 — a Schelling point: a deployable edge should bust less often than its barrier is wide). It excludes falsified-book quality (the locked-book Tradeify-100K transfer ran 17.70% bust) while not being null-by-construction (1.0% at eval on trailing geometry would demote every program regardless of edge quality — a degenerate falsifier; FXIFY-parity 1% belongs at the funded tier where busts forfeit real equity, not a cheap reset fee). Under trailing geometry p99-DD collapses into the bust gate (the barrier IS the drawdown), so a single bust ceiling stands in for both old FXIFY lock gates. The pass floor closes the no-trade-grinder loophole AND resolves the ADR §4 bust-vs-"pass-rate" wording tension. **Operator dial:** 2% = more conservative; 5% = too weak (nears falsified-book territory). 3% recommended.

### §2.3 Tier selection for "≥2 of 4"

Pre-register ONE tier per firm at the **$100K common band**, frozen, no post-hoc substitution: `Bulenox_100K`, `Tradeify_Select_100K`, `MFFU_Rapid_100K`, `BluSky_Premium_100K`. All four hold capital ($100K), barrier (3.0%), and target (6.0%) constant — isolating the genuine cross-firm variables (DD geometry 2×trailing/2×locking; consistency none/40/50/34%). At $50K the barriers diverge (4-5%) and integer-micro rounding distorts more. **Discharge rule:** ≥2 distinct firms clear, of which **≥1 must be trailing_locking (Tradeify or MFFU)** — the engine-faithful geometry — so the verdict can't ride entirely on the optimistically-biased %-of-peak firms (F2). Bulenox/BluSky results are labeled optimistic-lower-bounds until a fixed-$ trailing branch and (Bulenox) an intraday-excursion adjustment exist. All other tiers are reported as diagnostics; only the four $100K tiers gate.

### §2.4 Pre-registration freeze list (before the first scored re-MC)

1. Ceiling numbers (3.0% eval / 1.0% funded / pass-floor value + horizon).
2. Headline-bust definition + the F1 bucket-sum assertion.
3. The four frozen tiers + discharge rule + F2 optimism labels.
4. E1 decomposition + R_deploy + ≥4× cost hurdle; **source Tradeify/MFFU/BluSky commissions** (3-of-4 gap).
5. Per-firm consistency_frac (Tradeify's % is NOT in firm_rules — use envelope 40%, flagged); Run-2 gating; seeds 42/123/2026; horizon 1500.
6. dd_protection overlay posture per §3 (default OFF via NO_PROTECTION_TRIGGER; any tuned per-firm (trigger,scale) = pre-registered small grid, K-ledgered).
7. Regime-robustness caveat: run the regime gate on the deployable expression before trusting the ceiling result (panels inherit benign-regime provenance).
8. All-null close (no candidate clears) is a valid, success-eligible §4 outcome (demote-to-research-only is legitimate).
9. A pre-registered non-candidate calibration reference run once through the harness to confirm the ceilings sit in the discriminating band.

---

## §3 — dd_protection reframe recommendation ("concept, not constant")

### §3.1 The invariant vs the variables

**Invariant (the concept):** when the portfolio's remaining room to its **live bust floor** is depleted past a fraction of the firm's DD budget, multiply that day's sizing down; clear on recovery to reference; the factor MULTIPLIES BASE_RISK (compounds with the lifecycle haircut, never edits locked params); ULP rounding before compare; single tier; change-control law = any instance change ⇒ re-MC + regime-robustness gate + freeze record.

**Variables (per portfolio × firm-tier):** exactly three — `trigger`, `scale`, `reference_mode` (which floor DD is measured against, dispatched from `dd_type`).

FXIFY-C2's shipped ratio (trigger 1.5% / budget 5% = **0.30 budget-depletion**) is retained as **provenance-only seed heuristic** — explicitly NOT a validated transferable invariant (FXIFY-C2's own Q-DDP-1 regime-robustness gate FAILED, `dd_protection.py:10-13`). Every new instance's (trigger, scale) must clear its own re-MC + regime gate; it never rides FXIFY's.

### §3.2 Reference generalization (verified against `simulation.py:51-94`)

Today the scale trigger fires off `dd_from_peak` for ALL dd_types while the bust check branches per geometry. Generalize the de-risk reference to **remaining-room-to-live-floor** in budget units:
- **static (FXIFY):** FREEZE the byte-identical dd_from_peak proxy — do NOT re-express as distance-to-fixed-floor (that changes arithmetic and drifts the anchor). Honest asymmetry: the concept is stricter for trailing types than its own seed instance.
- **trailing (Bulenox/BluSky):** peak-relative fractional DD already IS distance-to-floor in budget units — needs only a budget-scaled trigger (e.g. 0.30×3% = 0.9% at 100K).
- **trailing_locking (Tradeify/MFFU):** the generalization strictly bites POST-lock (floor freezes while peak rises → dd_from_peak over-de-risks); the correct reference reuses the SAME `floor(t)` already computed at `simulation.py:80-82`.

### §3.3 Pin preservation (constraints A/B/C hold by construction)

The load-bearing architecture decision: **one-way pin, not rebind.** `dd_protection.py:69-70` literals stay byte-unchanged (both lock gates require `ast.Constant` RHS — a `DD_TRIGGER = REGISTRY[...]` rebind fails `validate_params.py` AND `verify_lock_anchors.py`). The MVD self-check is left entirely alone. A new pure module `core/dd_geometry.py` (NOT on the anchor import path) holds: a frozen `ProtectionPolicy` dataclass; a `POLICY_REGISTRY` whose only frozen seed row is `FXIFY-C2 = ("static", 0.015, 0.40)`, import-asserted equal to `dd_protection.DD_TRIGGER/DD_SCALE` (one-way); a side-effect-free resolver; a `dd_type→reference_mode` helper reading dd_type only (immune to the None hazard). For scoring runs, dd_protection-as-concept = `(dd_trigger, dd_scale)` passed as ARGUMENTS to `run_seed`/`simulate_path` (default OFF or per-instance), never edits to module globals.

### §3.4 Sequencing (adversarial-verification trims applied)

- **ADR now (the D2 vehicle):** record the concept, the three variables, FXIFY-C2 as frozen instance, θ=0.30 as provenance-only, the calibration governance (pre-registered objective: minimize P(bust vs THAT firm's barrier) at least intervention subject to a productivity floor + mandatory half-panel regime gate + K accounting), forbidden moves.
- **SAFE-NOW code (byte-identity provable):** `core/dd_geometry.py` + `tests/test_dd_geometry.py` + full gate set green (test_mc_anchors, MVD, boundaries, validate_params, verify_lock_anchors). That is the WHOLE safe-now deliverable.
- **DEFERRED (verification-mandated trim — do not author yet):** the `simulate_path` reference_mode branch, `seed_policy` heuristics, harness swaps, low-n shrinkage floor, integer-micro snapping, retry-EV objective. All design-ahead-of-data for instances that don't exist, under a program with its own 2026-11-08 NO-GO falsifier. Gated on: engine pre-flight (constraint D) + a real pre-registered candidate.
- **Open per-firm objective question (11-08 D1 material):** FXIFY bust<1% encodes one-shot economics; prop evals allow cheap retries — the per-firm objective must be re-derived to reset/retry EV, not inherited.

---

## §4 — Falsifiable hypotheses

**H-SCORE:** If a DISC-CAMP-0 survivor traverses G0–G5 and clears bust ≤3.0% + pass floor on ≥2 distinct $100K firm tiers (≥1 trailing_locking), then the four-firms ADR §4 falsifier is discharged and the survivor routes to G8 admission; otherwise (no pre-registered candidate clears any tier by 2026-11-08) the prop program demotes to research-only. **Reject H-SCORE (ceiling mis-set) if** the §2.4(9) non-candidate calibration reference clears the 3.0% ceiling on ≥2 tiers — the ceiling then fails to discriminate and must be re-derived in a fresh brief (not tightened in place).

**H-REFRAME:** If `core/dd_geometry.py` (one-way pin, registry, resolver) lands, then all five gates {`test_mc_anchors`, MVD import self-check, `validate_params.py`, `verify_lock_anchors.py`, `check_boundaries.py`} stay green and the anchor reproduces byte-identically; **reject (FALSIFIED) if** any gate goes red — revert the module and re-design; the reframe never proceeds by weakening a gate.

## §5 — Forbidden moves (genuinely tempting)

- Rebinding `DD_TRIGGER`/`DD_SCALE` to a registry lookup (clean-looking; breaks both AST lock gates).
- Re-expressing FXIFY-static as distance-to-fixed-floor "for consistency" (drifts the anchor).
- Naming θ=0.30 a validated "budget-depletion invariant" (FXIFY-C2's own regime gate failed — provenance only).
- Reading `compute_default_config()['bust_rate']` for a prop tier (reports ~0%; F1).
- Counting a Bulenox/BluSky-only pair as "≥2 of 4" without the locking-firm requirement (optimistic-geometry cherry-pick; F2).
- Setting the eval ceiling at FXIFY-parity 1% (null-by-construction falsifier on trailing geometry).
- Post-hoc tier substitution after seeing per-tier results (best-of-K at the gate layer).
- Switching `ACTIVE_FIRM` to run prop tiers "conveniently" (breaks anchor byte-repro).
- Authoring the deferred §3.4 machinery now "since we're set up" (built-but-unexercised ceremony under a live NO-GO falsifier).

## §6 — Gate criteria (binary)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` | Operator ratifies (i) 3.0%/1.0%/pass-floor numbers, (ii) the four $100K tiers + discharge rule, (iii) reframe ADR scope — with or without dial adjustments recorded here first | Freeze §2.4 into the pre-registration; author the reframe ADR + safe-now `dd_geometry` module; this brief closes as the recommendation-of-record |
| `FALSIFIED` | Operator rejects the bust-first framing or the $100K-band cross-section wholesale, OR H-SCORE's calibration-reference reject fires, OR H-REFRAME's gate-red reject fires | Fresh brief with the replacement framing (no in-place criteria edits — trap #12); safe-now code reverted if landed |
| `AMBIGUOUS` | Operator ratifies the architecture but defers the numbers pending prop_envelope v1.0 (B1) or the 3-of-4 commission sourcing | Architecture work (reframe ADR + dd_geometry) proceeds; the pre-registration freeze BLOCKS until the deferred inputs land; re-present numbers at 08-08 |

Pre-registration freeze is additionally blocked (regardless of verdict) until prop_envelope v1.0 ratifies AND Tradeify/MFFU/BluSky commissions are sourced. Safe-now code merges only with the full §4 H-REFRAME gate set green.

## §7 — Ratification record (operator, 2026-07-13)

Operator ratified the full recommendation — §6 `RESOLVED` trigger, **no dial adjustments** ("ratify everything", recorded in the same PR as the brief itself, [#352](https://github.com/Joshua-Asante/multi_firm_operations/pull/352)):

- **(i) Numbers CONFIRMED:** §4 eval gate **bust ≤ 3.0% + pass floor P(pass) ≥ 50%** (Run-2, deployable expression, $100K band); **funded ruin ≤ 1.0%** (scaling gate, not §4). The 2%/5% operator dials were declined — 3.0% stands.
- **(ii) Tier cross-section + discharge rule CONFIRMED:** `Bulenox_100K` / `Tradeify_Select_100K` / `MFFU_Rapid_100K` / `BluSky_Premium_100K`, frozen, no post-hoc substitution; discharge = ≥2 distinct firms with ≥1 trailing_locking; Bulenox/BluSky labeled optimistic-lower-bounds (F2).
- **(iii) Reframe ADR scope CONFIRMED:** concept-not-constant per §3 — one-way-pin `core/dd_geometry.py` architecture, FXIFY-C2 frozen instance, θ=0.30 provenance-only, safe-now deliverable trimmed to module + test + ADR, deferred machinery stays deferred.

**Per the `RESOLVED` disposition, now authorized (follow-on work, separate PRs):**
1. Author the **survivor-scoring pre-registration** freezing §2.4 verbatim — still BLOCKED until prop_envelope v1.0 ratifies (B1) and Tradeify/MFFU/BluSky commissions are sourced; the numbers themselves are no longer open.
2. Author the **dd_protection reframe ADR** (the audit-D2 vehicle) + the safe-now `core/dd_geometry.py` + `tests/test_dd_geometry.py`, merged only with the full §4 H-REFRAME gate set green.

This brief closes as the **recommendation-of-record**; the §10 hooks remain live against the follow-on artifacts.

## §10 — Audit hooks (runnable)

```bash
# Anchor integrity after ANY reframe work lands (all must stay green)
python -c "import sys; sys.path.insert(0,'core'); import dd_protection; print('MVD OK')"
python scripts/validate_params.py && python scripts/verify_lock_anchors.py
python -m pytest tests/core/test_mc_anchors.py -q

# The literals were never rebound (expect both lines, ast.Constant form)
grep -n "^DD_TRIGGER = 0.015\|^DD_SCALE = 0.40" core/dd_protection.py

# F1 assertion present in any prop harness before its results are trusted
grep -rn "bust_trailing" lab/ --include="*.py" | grep -i "assert\|sum"

# The frozen tier cross-section never silently changes (expect exactly these four in the pre-reg)
grep -n "Bulenox_100K\|Tradeify_Select_100K\|MFFU_Rapid_100K\|BluSky_Premium_100K" docs/briefs/pre-registration/*.md

# theta=0.30 never promoted to "invariant" without the provenance caveat
grep -rn "0.30" docs/adr/*ddp* docs/adr/*dd-protection* 2>/dev/null | grep -vi "provenance\|seed\|heuristic" && echo "CHECK PROMOTION" || echo "clean"
```

## Verification

```bash
python ~/.claude/skills/brief-authoring/scripts/check_brief.py docs/briefs/programs/2026-07-12-survivor-scoring-and-ddp-reframe-recommendation.md
# §0 anchors
git log -1 --format='%h %ci' -- core/dd_protection.py       # expect 99b7854
git log -1 --format='%h %ci' -- core/firm_rules.py           # expect 0e26a7b
git log -1 --format='%h %ci' -- ops/prop_envelope_default.md # expect 802ee60
# Ceiling calibration source
grep -n "17.70\|17.7" lab/analysis/c1/tradeify_futures3_remc_2026-07-11/RESULTS.md
```

---

## Addendum 2026-08-29 — H-REFRAME gate-set correction (brief-decay-audit)

**H-REFRAME gate-set correction:** as of 2026-08-29, 2 of the 5 named gates (§4) no longer exist
as files and cannot be evaluated — `scripts/validate_params.py` was retired 2026-08-03
([`docs/adr/2026-08-03-params-toml-gate-retirement.md`](../../adr/2026-08-03-params-toml-gate-retirement.md),
Shape 1) and `tests/core/test_mc_anchors.py` was deleted (confirmed absent — no file at that path
anywhere in the tree). The remaining three gates — the MVD import self-check,
`scripts/verify_lock_anchors.py`, `scripts/check_boundaries.py` — were independently re-run
2026-08-29 and **all pass**:

```
$ python -c "import sys; sys.path.insert(0,'core'); import dd_protection; print('MVD OK')"
MVD OK
$ python scripts/verify_lock_anchors.py
ROUTING: Closed
$ python scripts/check_boundaries.py
check_boundaries: OK — 24 first-party modules, no illegal edges, no name collisions
```

Per the retirement ADR's own §Addendum-2026-08-08(d), the surviving substitute coverage for the
retired `validate_params` limb is `git diff --stat HEAD -- core/ ops/c1_rail/c1_sizing_host_reference.py`;
the byte-identical-anchor claim's successor pin is `tests/core/test_mc_synthetic_engine.py` +
`docs/mc_anchor_history.md`. The §3.3 `POLICY_REGISTRY`/FXIFY-C2-seed point remains separately
and adequately discharged elsewhere — no further action needed there.

H-REFRAME itself is **not** judged `FALSIFIED` by this correction (no gate went red; two ceased
to exist under a separately-ratified, unrelated governance-diet decision), but the falsifier's
own text (§4) is now only mechanically checkable against 3 of its 5 named gates.
