# Q-KBUDGET-1 — Phase-1 candidate-axis inventory (ratification artifact)

**Status:** **RATIFIED 2026-07-14 (operator, G2)** — see §6. The commit landing this status is the Phase-2 unblock anchor (screen artifacts must postdate it).
**Parent:** [`Q-KBUDGET-1-axis-reachability-screen.md`](Q-KBUDGET-1-axis-reachability-screen.md) §7 Phase 1 · frozen screen: [`pre-registration/Q-KBUDGET-1-screen-preregistration.md`](pre-registration/Q-KBUDGET-1-screen-preregistration.md) (freeze commit `b304f2c`, G1 ratified 2026-07-14)
**Authored:** 2026-07-14 · Claude Code (Fable 5), operator-directed ("pick up Q-KBUDGET-1, and use existing strategies as a survivor path")
**D-S-A domain:** data (inventory composition on the axis corpus; no funding act, no evidence deletion, no campaign freeze)
**Hypothesis:** none authored here — this is the parent brief's §7 Phase-1 execution artifact; the falsifiable hypothesis (H-KBUDGET) lives in the parent §4 and is not restated (single-owner rule).

---

## §0 — Rule-0 reads (this session, 2026-07-14, main checkout @ `ff8a51e`)

| Source | Anchor | What it supplies |
|---|---|---|
| Parent brief + frozen pre-reg (both in full) | `b304f2c` 2026-07-14 | Clause K (K_eff ≤ 3 at Cap 1.0), Clause N (power ≥ 0.50, cohort-cited), §C declaration set, UNSCREENABLE routing |
| [`discovery_manifests/disccamp0_gc_2010_18.json`](../../discovery_manifests/disccamp0_gc_2010_18.json) / [`harv2026_001_es_monthend.json`](../../discovery_manifests/harv2026_001_es_monthend.json) | `c783533` / `8784d32`; parsed this session: `status: closed, K: 3177` / `status: closed, K: 1` | K_banked: GC/MGC = 3,177 · ES = 1 · all other families = 0 |
| Floor table reproduced on production module (`lab/research_utils/deflated_sharpe.py`, pre-reg §F hook #3) | run 2026-07-14: K=1→0.65 · 2→0.85 · **3→0.98** · 4→1.06 · 8→1.22 · 450→1.835 · 3,178→2.05 | Row-level floor(K_eff) values below |
| [`docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md`](../adr/2026-07-12-prop-portfolio-four-friendly-firms.md) (full) | `fad8984` (content `0e26a7b`) | §2 R6 boundary ("builds **new** prop-envelope portfolios; does not re-open R5/P2"); §5 forbidden move ("Deploying the locked four-strategy portfolio to prop firms under this ADR"); §4 falsifier + amendment path ("never edit §2 in place") |
| [`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`](pre-registration/2026-07-13-prop-survivor-scoring-prereg.md) (full) | `be6dda6` FROZEN 2026-07-13 | Part A bust ≤ 3.0% + P(pass) ≥ 50%, Run-2, frozen $100K×4 tiers, ≥2 firms incl. ≥1 `trailing_locking`; G0–G8; ceiling rationale "excludes falsified-book quality (17.70%)" |
| [`lab/analysis/c1/tradeify_futures3_remc_2026-07-11/RESULTS.md`](../../lab/analysis/c1/tradeify_futures3_remc_2026-07-11/RESULTS.md) (full) | `eba5030` | 3-leg full-Aegis book: 100K bust **17.70%** (Aegis attr 70.7%); 50K 10.33%; blockers list (BEPAD-TEST file; P2 stands; MYM abs PF~2 does not overturn) |
| [`lab/analysis/c1/tradeify_futures3_bustcut_2026-07-11/RESULTS.md`](../../lab/analysis/c1/tradeify_futures3_bustcut_2026-07-11/RESULTS.md) (full) | `eba5030` | Test 1 drop-Aegis 2-leg: 50K bust **0.76%** / pass 99.24% / med 222d · 2b Aegis@0.75% (ae744): 50K bust **2.02%** / pass 97.98% / med 152d · 2c size-adj: **1.28%** · ae744↔5274c material delta + 1R pin-fallback artifact |
| [`ops/instruments/6J.md`](../../ops/instruments/6J.md) (full) | `fad8984` | J1 panel of record (n=129, PF 2.318, +0.218R); J4 Bulenox trail 11–12% / 5–8% ramped; J5 venue throttling; **M6J at no FRIENDLY firm** (prop JPY = full 6J); commissions verified |
| [`lab/CATALOG.md`](../../lab/CATALOG.md) actives, status-checked per-slug | `900364b` + per-slug reads this session | tom_spx **RESOLVED-ABSENT**; us500_discovery **NO ROBUST STANDALONE EDGE**; usoil_regime_capture **NON-RUNNABLE** (Gen-1 imports); eurusd_pattern_enum Phase-3 LOCKED **K=450**, Phases 4–7 not started; orb_universe = CFD-universe screen (FXIFY venue) |
| [`docs/briefs/2026-07-12-08-08-packet-pretriage.md`](2026-07-12-08-08-packet-pretriage.md) (full) | ratified 2026-07-12 | Slate classes; 11-08 collision; A4 flow-data DEFER-procurement precedent |
| Q-MECH-1 family synthesis ([`Q-MECH-1_SC-XLEG_family_synthesis.md`](Q-MECH-1_SC-XLEG_family_synthesis.md), via memory + STATE cross-check) | merged PR #292 | Mechanism candidates: JPY month-end endogenous (overlay-class, parked); XAU T3b (4-bar partial, not yet opened); DJ30/NAS gamma (vendor-grade, unprocured) |

**Pre-Q gate (D-S-A on the inventory corpus):**
- **D:** operator-accepted closures enter only as calibration/inheritance citations (DISC-CAMP-0, Q-HARV-1, tom_spx, us500_discovery) — test: duplicated by a higher-fidelity source (their closure records). Nothing else deleted; dead axes are listed below-the-line, not dropped (§C requirement).
- **S:** each axis compresses to the §C declaration 5-tuple (family→K_banked, design→K_intrinsic, era→N, cohort-cited δ/σ or UNSCREENABLE, blockers). Nothing about reachability is lost at this dimension.
- **A:** floors precomputed at the row-relevant K values (§0 row 3), so Phase 2 is a table fill.

---

## §1 — Scope note: the operator directive and what it adds

Q-KBUDGET-1's verdict is scoped to **newly-started discovery** (parent §4: FALSIFIED ⇒ "the 11-08 four-firms §4 falsifier is a-priori unreachable *via newly-started discovery*"). The operator directive (2026-07-14, this session) adds **existing strategies as a survivor path** — book expressions of already-validated legs routed toward the §4 falsifier without any new discovery. These enter this inventory as the named "operator additions" source (parent §7), classed separately (**Class S**, §3) because they raise a routing question (§5 ask #2) the frozen screen text did not anticipate: they never traverse the DSR universe gate — their confirm gate is the already-frozen survivor-scoring gate — so Clause K's Sharpe-demonstrability floor is a category mismatch for them, while Clause N's power logic applies naturally.

## §2 — Class D: discovery axes (screenable under the frozen two clauses)

Declarations per pre-reg §C. Floors from the reproduced table (§0). **No axis is screened here** — the table records declarations; Phase 2 fills verdicts after ratification.

| # | Axis | Family → K_banked | Design class → K_intrinsic | Era → N | δ, σ (cohort citation) | Pre-declaration status |
|---|---|---|---|---|---|---|
| D1 | Any GC/MGC successor campaign (mining or mechanism) | GC/MGC → **3,177** | any (even K_intrinsic=1) → K_eff ≥ 3,178, floor 2.05 | — | — | **FAIL-invariant by family bank** (the pre-reg §B retrodiction row); recorded as calibration |
| D2 | Wide mining on any other GLBX family (ES/NQ/YM, DISC-CAMP-0-class ladder) | ES → 1; NQ/YM → 0 | overlap-tool tiling Σ⌊T/m⌋ ≈ 10³–10⁴ on any multi-year hourly panel (DISC-CAMP-0 bound 3,177 on 51,659 bars) | — | — | **FAIL-invariant by design class** (floor ≥ ~2.0) |
| D3 | Month-end/HARV-class mechanism successors on ES | ES → 1 | mechanism-first, ≤2 new hypotheses possible (K_eff ≤ 3) | monthly events, 2018+ ⇒ N ≈ 100 | +13→19.2 bp, σ per HARV-0 cohort; **P(primary\|true) ≈ 24–30%, joint 5–6%** (Q-HARV-1 §R, inherited — not re-litigated) | Clause K PASS-able / **Clause N FAIL by inherited cohort** ("HARV cannot carry the 11-08 program") |
| D4 | XAU T3b — swap-dealer COT expansion confirm | prop expression requires GC/MGC → **3,177** (K FAIL-invariant); non-futures expression is venue-dead (no CFD venue) | mechanism-first 1–2 | COT weekly 2006+ ⇒ N ≈ 10³ | **no citable tradeable-effect δ** (T3 partial = 4 bars) | **UNSCREENABLE on Clause N + family-blocked on Clause K** — missing input: cohort δ from a scoping probe *and* a venue that isn't GC-banked |
| D5 | DJ30/NAS gamma-positioning mechanism (MYM/MNQ expression) | MYM/MNQ → 0 | mechanism-first 1–3 (K_eff ≤ 3 possible) | daily-frequency ⇒ N ≈ 10³ (adequate if δ real) | **no dataset, no citable δ** (vendor-grade positioning data unprocured; A4 DEFER-procurement precedent) | **UNSCREENABLE** — missing inputs: vendor dataset + cohort-cited δ; the one Class-D row whose missing input is a *procurement decision*, not a dead end |
| D6 | eurusd_pattern_enum Phase-4 resumption | 6E/EURUSD → 0 | **locked harness pre-registers K=450** (README Phase-3 row) → floor 1.835 | — | — | **FAIL-invariant by declared K** (also venue: authored for FXIFY CFD; would need 6E re-expression — moot given K) |
| D7 | JPY/6J-family mechanism discovery (incl. any prop-side expression of the Q-MECH-1 month-end mechanism) | 6J → 0 | mechanism-first 1–3 (K_eff ≤ 3 possible) | month-end events ⇒ N ≈ 10² (HARV-shaped N problem) | δ extractable from the Q-MECH-1 JPY leg artifacts — **not yet extracted** | **UNSCREENABLE pending declaration** — missing inputs: extracted cohort δ/σ; JPY micro symbology resolution (proxy-discipline); note M6J absent at FRIENDLY firms ⇒ prop expression = full 6J |

**Reading:** under the frozen anchors, no Class-D axis is currently a clean double-PASS candidate. D5 (and D7, weaker) are the only rows where a *supplied input* could change the verdict — which is exactly the AMBIGUOUS-HOLD shape the pre-reg §D anticipates.

## §3 — Class S: existing-strategy survivor-path axes (operator addition, 2026-07-14)

Book expressions of already-validated legs, targeted directly at the frozen survivor-scoring gate (Part A: bust ≤ 3.0% + P(pass) ≥ 50%, Run-2, $100K tiers, ≥2 firms incl. ≥1 `trailing_locking`). Families MYM/MNQ/6J all bank K=0. **Honest K disclosure:** ~7 book-composition variants have already been examined (selectflex %-equity + integer arm; futures3 3-leg; bustcut T1/T2/2b/2c) — under a literal Clause-K reading, K_intrinsic ≈ 8 → floor 1.22 → FAIL; see the §5 routing ask.

> ⚠ **SUPERSEDED — see Addendum 2026-08-29** (end of file). The 3.0% ceiling this table benchmarks S1/S2/S3 against is no longer the live Part A ceiling.

| # | Book axis | Prior looks (all Tradeify Select, geometry-only) | Coarse Clause-N-analogue read | Blockers before any scored run |
|---|---|---|---|---|
| S1 | 3-leg MYM+MNQ+6J, Aegis at reduced weight (~0.75%-class) | 50K: bust **2.02%** (2b, ae744) / **1.28%** (2c size-adj), pass ≈ 98%, med ≈ 152d | vs 3.0% at the harsher 100K geometry: the full-Aegis book deteriorated 10.33→17.70% from 50K→100K; a ~1.7× factor puts 2b at ≈3.4% — **genuinely uncertain, the G4 run adjudicates**; MFFU (2nd `trailing_locking`) untested | Aegis panel-of-record defect (BEPAD-TEST CSV; ae744↔5274c material delta; 1R pin-fallback trap); four-firms ADR amendment (§4 below); candidate pre-registration with prior-look disclosure |
| S2 | 2-leg MYM+MNQ (drop Aegis) — incl. the **integer-micro sizing variant at verified $1.82 RT, whose re-run was operator-stopped 2026-07-10 (bracket 0.80%↔4.59%, UNRESOLVED)** | 50K: bust **0.76%**, pass 99.24%, med 222d (pass-floor form: P(pass) ≥ 50% + finite median — met) | strongest prior of the three; 100K untested; p99 3.86% has headroom | R5/P2 tension strongest here (both legs are falsified *CFD-transfers*; native MYM abs PF ~2 — the candidate claim must be re-framed as native-book bust-geometry, never edge-transfer); ADR amendment; pre-registration with prior-look disclosure |
| S3 | Aegis→6J solo book | none on `trailing_locking`; J4 Bulenox `trailing` 11–12% full / 5–8% ramped (fails 3.0% on Bulenox geometry) | weakest prior; Aegis drove 70%+ of 3-leg bust attr at full weight, and 0.5× helped dramatically — solo-at-reduced-weight on Tradeify/MFFU is an open cell | governance-cleanest leg (6J transfer VALIDATED, J1; never P2-falsified) but still a locked-book leg → amendment; same panel-of-record defect |

> ⚠ **SUPERSEDED — see Addendum 2026-08-29** (end of file). Guardian→MGC (R7) is no longer data-blocked/re-armable — it was data-procured, scored, and killed.

**Below-the-line (Class S):** Guardian→MGC (R7) — data-blocked (no GC1!/MGC1! bar export), transfer unvalidated, GC/MGC family bank poisons any Clause-K reading, operator-parked. Re-arm = data procurement + R7 unpark; not ratifiable now.

**Transparency note (freeze-order):** the survivor-scoring ceiling (3.0%) was frozen 2026-07-13, *after* the 2026-07-11 bustcut numbers were visible. The ceiling's rationale is structural (barrier width; excludes the 17.70% falsified-book quality) and the operator declined dial adjustments — but any S-axis candidate pre-registration must disclose the prior 50K looks so selection-on-prior-looks is on the record (the frozen $100K×4-tier cross-section itself has never been run for any S-book — that surface is unseen).

## §4 — Governance flags common to all Class-S axes (surfaced, not resolved here)

These flags condition the escalation branch of the parent hypothesis (H-KBUDGET, parent §4 — not restated here): if the discovery screen lands FALSIFIED/AMBIGUOUS, Class S is the surviving route to the 11-08 falsifier *only if* the items below are cleared.

1. **Four-firms ADR §5** forbids "deploying the locked four-strategy portfolio to prop firms under this ADR," and §2 scopes the program to "new prop-envelope portfolios… does not re-open R5/P2." Pursuing any S-axis to an actual §4 discharge therefore requires an **amendment/supersession ADR** (the ADR's own pattern: never edit §2 in place). The amendment's honest shape: permit *pre-registered existing-strategy book candidates* through the frozen survivor gate, with R5/P2 falsifiers left standing — the candidate claim is native-book bust-geometry at firm tiers, **not** CFD-edge-transfer (which stays falsified).
2. **Parameter axis untouched:** every S-axis re-weights *allocation/sizing* at the firm tier (venue variables per the dd-geometry concept-not-constant ADR); no Pine, no locked SL/TP/ATR, no locked CFD allocations change.
3. **The survivor gate is already frozen** — S-axes need no new gate. What they need is: the ADR amendment (#1), a resolved Aegis panel-of-record, and a candidate pre-registration (variant set fixed BEFORE the frozen-tier G4 runs).

## §5 — Ratification asks (each blocks Phase 2 in part)

1. **Ratify Class D (D1–D7) as the complete discovery-axis inventory** for the frozen screen, or name additions. (Below-the-line exclusions, §7, ride along as recorded non-candidates.)
2. **Route Class S** — pick one:
   - **(i) Screen them under the frozen rules literally.** Honest K_intrinsic ≈ 8 (prior variants counted) → Clause K FAIL rows; they'd be excluded from the fundable set while their real path proceeds outside the screen anyway. Mechanically clean, category-dishonest.
   - **(ii) Record them as out-of-screen-scope (recommended).** They are not "newly-started discovery"; their governing gate is the frozen survivor-scoring pre-registration. The Q-KBUDGET-1 verdict stays discovery-scoped; the closure record cites Class S as the live alternative route that conditions the FALSIFIED-branch escalation. No Trap-12 amendment — inventory composition is exactly the operator's Phase-1 act.
3. **Authorize drafting the four-firms ADR amendment** (§4 flag #1) as a separate artifact — required before any S-axis can discharge the 11-08 falsifier.
4. **Order the S-axis pre-run mechanicals** (independent of 1–3): resolve the Aegis panel-of-record (of-record J1 CSV vs BEPAD-TEST ae744/5274c) and pin the 1R basis, so a candidate pre-registration has a clean input.

## §6 — Ratification record

Operator (Joshua) ratified 2026-07-14, in-session, all four asks answered:

1. **Class D ratified as-is (D1–D7)** — the complete discovery-axis inventory for the frozen screen; below-the-line exclusions ride as recorded non-candidates.
2. **Class S routed out-of-screen-scope** (recommended option taken): S-axes are recorded here but not screened — they are not newly-started discovery; their governing gate is the frozen survivor-scoring pre-registration. The Q-KBUDGET-1 verdict stays discovery-scoped; the closure record cites Class S as the live alternative route conditioning the FALSIFIED/AMBIGUOUS-branch escalation.
3. **Four-firms ADR amendment authorized for drafting now** (separate artifact, `Proposed` status; operator acceptance is a separate act).
4. **S-axis pre-run mechanicals ordered as a Cursor handoff** (Aegis panel-of-record CSV resolution + 1R basis pin; frozen-spec handoff per the CC/Cursor surface-allocation ADR).

## §7 — Below-the-line: excluded non-candidates (visible, with reasons — §C requirement)

| Item | Reason excluded |
|---|---|
| DISC-CAMP-0, Q-HARV-1/HARV-2026-002 | operator-accepted closures; reopening via the screen is a parent-§5 forbidden move |
| tom_spx | Layer A RESOLVED-ABSENT on canonical feed (frozen battery hard-fail) |
| us500_discovery / orb_universe | NO ROBUST STANDALONE EDGE; ORB survivor not tradeable at realistic fills — and both are FXIFY-CFD-universe work (venue closed) |
| usoil_regime_capture (Q-USOIL-1) | NON-RUNNABLE (retired Gen-1 imports); operator-parked to 08-08; re-open needs Gen-2 re-point — that re-point, if proposed, enters a future inventory as a fresh axis |
| xauusd_cgb | HOLD/AMBIGUOUS, CFD overlay class — not a prop-candidate axis |
| Q-MECH-1 JPY guard-band overlay Pre-Q | overlay on the locked Aegis leg, parked, gated on fresh-period evidence — not a new-leg axis |
| Guardian→MGC (R7) | see §3 below-the-line |

## §10 — Audit hooks (runnable)

```bash
# Freeze ordering: pre-reg freeze (b304f2c) predates this inventory; inventory ratification predates any Phase-2 artifact
git log --format='%h %ci' -- docs/briefs/pre-registration/Q-KBUDGET-1-screen-preregistration.md | tail -1
git log --format='%h %ci' -- docs/briefs/Q-KBUDGET-1-phase1-inventory.md | head -2
git log --format='%h %ci' -- lab/archive/q_kbudget_1_2026-07/ 2>/dev/null | tail -1   # must be LATER or absent

# K_banked claims reproduce from the manifests
python -c "import json; print([(p, json.load(open(p))['status'], json.load(open(p))['K']) for p in ('discovery_manifests/disccamp0_gc_2010_18.json','discovery_manifests/harv2026_001_es_monthend.json')])"
# expect: closed/3177 and closed/1

# Row-cited priors match their sources
grep -n "17.70%" lab/analysis/c1/tradeify_futures3_remc_2026-07-11/RESULTS.md
grep -n "0.76%\|2.02%\|1.28%" lab/analysis/c1/tradeify_futures3_bustcut_2026-07-11/RESULTS.md
grep -n "K=450" lab/analysis/legacy/eurusd_pattern_enum/README.md || grep -n "450" lab/analysis/legacy/eurusd_pattern_enum/README.md
grep -n "no FRIENDLY firm offers M6J" ops/instruments/6J.md

# The four-firms §5 forbidden move is still standing until an amendment ADR lands (Class-S gate)
grep -n "Deploying the locked four-strategy portfolio" docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md

# No screen ran pre-ratification (screen artifacts must not exist yet)
ls lab/archive/q_kbudget_1_2026-07/ 2>/dev/null && echo "REVIEW: Phase-2 artifacts exist — check ratification ordering" || echo "clean (pre-Phase-2)"
```

## Verification

```bash
# §0 anchors resolve
git log -1 --format='%h %ci' -- docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md   # expect be6dda6
git log -1 --format='%h %ci' -- lab/analysis/c1/tradeify_futures3_bustcut_2026-07-11/RESULTS.md              # expect eba5030
git log -1 --format='%h %ci' -- ops/instruments/6J.md                                                     # expect fad8984

# Floor table reproduces (pre-reg §F hook #3 command; expect 1→0.65 · 3→0.98 · 8→1.22 · 450→1.835 · 3178→2.05)
```

---

## Addendum — 2026-08-29 (decay-audit correction)

**Does not edit §3 or §7 above in place** — this file is a ratified G2 body (§ Status line, RATIFIED 2026-07-14) and stays byte-unedited per the standing no-in-place-edit convention for frozen/ratified artifacts. Two live-state claims below the line in §3 have decayed; both are flagged upstream (⚠ SUPERSEDED banners above the §3 Class-S table and above the §3 Guardian→MGC below-the-line line) and corrected here.

**(1) Guardian→MGC (R7) is no longer data-blocked/re-armable.** §3's below-the-line entry and §7's pointer row both describe R7 as data-blocked (no GC1!/MGC1! bar export) and operator-parked, pending re-arm via data procurement. That is stale: R7 was subsequently data-procured, scored, and killed by [`docs/briefs/closures/2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md`](closures/2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md) — verdict `DEAD(N-SURV)`, bust ceiling missed on every partition (Full 42.2%, H1 72.4%, H2 16.5% vs the then-3.0% ceiling). Pursuit [`b8`](../../pursuits/b8-guardian-mgc-transfer-lane.md) flipped `PARK → SUBTRACT` as a result. Current canonical status is confirmed at [`docs/adr/2026-08-19-cme-broker-panel-admission-for-breadth-revival.md:97`](../adr/2026-08-19-cme-broker-panel-admission-for-breadth-revival.md) ("Guardian (MGC) is `SUBTRACT`/DEAD"). Re-proposal of this axis now requires new *mechanism* evidence per the closure's own stop rule — not a data-procurement re-arm.

**(2) The Part A eval ceiling §3's table benchmarks against (3.0%) is no longer the live ceiling.** It was superseded 2026-08-26 by [`docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md`](pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md), which raises the Part A eval ceiling from 3.0% to 5.0%. Under the current 5.0% ceiling, all three §3 rows clear the bar: S1 (~3.4% projected at the 100K geometry, 2.02%/1.28% priors at 50K) and S2 (0.76%). §3's "genuinely uncertain" / marginal framing for S1 and its 3.0%-denominated readings for S2/S3 no longer reflect the live ceiling.

**Unaffected:** the D1–D7 Class-D inventory, the S1–S3 classification structure itself, the §4 governance flags, the §5 asks, and the 2026-07-14 §6 ratification record are all unaffected by this correction and remain historical record as ratified. Only the two live-state claims above are corrected.

```bash
# The superseding closure and its verdict figures
grep -n "DEAD(N-SURV)\|42.2\|72.4\|16.5" docs/briefs/closures/2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md

# Current canonical Guardian(MGC) status
grep -n "Guardian (MGC) is" docs/adr/2026-08-19-cme-broker-panel-admission-for-breadth-revival.md

# The superseding ceiling change
grep -n "3.0% → 5.0%\|bust ≤ 5.0%" docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md
```
