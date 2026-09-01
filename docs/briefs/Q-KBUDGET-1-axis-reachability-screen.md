# Q-KBUDGET-1 — K-budget as an a-priori axis-selection gate: is the fundable axis set non-empty?

**D-S-A domain:** data (the screen operates on the candidate-axis corpus; the axis-funding act itself is STRATEGIC-LoR at 08-08 — no cascade: this brief authorizes no funding, no deletion of any axis's evidence, and no campaign freeze).

**Status:** **`RESOLVED` (§6 re-fired 2026-07-15)** — fundable set non-empty: D5 (NQ/MNQ intraday-momentum footprint) PASSES both clauses after operator confirm-construct ratification. Historical path: `AMBIGUOUS-HOLD` 2026-07-14 → D7 FAIL + D5 hinge narrowed 2026-07-15 morning → D5 ratified afternoon. Chain: pre-reg FROZEN `b304f2c` (G1) → inventory RATIFIED `ca02030` (G2) → screen ([`lab/archive/q_kbudget_1_2026-07/`](../../lab/archive/q_kbudget_1_2026-07/RESULTS.md)). Closure: [`closures/Q-KBUDGET-1-axis-reachability-screen.md`](closures/Q-KBUDGET-1-axis-reachability-screen.md).
**Authored:** 2026-07-14 · **Closed:** 2026-07-15 (RESOLVED — D5 axis ranked for 08-08; campaign HARD gates still bind)
**Authors:** Joshua (authority) + Claude Code (Fable 5)
**Parent question:** Q-GATECART-1 (CLOSED-FALSIFIED 2026-07-14) — this is its registered fork ("K-budget as an a-priori axis-selection gate", STATE forward board)
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q, OUTER (Rule-2 budget: 8 iterations, no self-extension) — closure gated on the §6 verdict firing against the operator-ratified axis inventory under the frozen screen
**Artifact path:** `docs/briefs/Q-KBUDGET-1-axis-reachability-screen.md`

---

## §0 — Rule 0 reads (production-source verification)

All read in full this session (2026-07-14, worktree `q-harv-1-successor-preq` off `origin/main` @ `e8c75c3`) before authoring:

- [`docs/briefs/closures/Q-GATECART-1-survivor-gate-cartography.md`](closures/Q-GATECART-1-survivor-gate-cartography.md) — anchor `1367265` (closure commit; file last touched `fad8984` LTM move). The parent verdict, M-19, the K-sweep, and the fork this brief opens.
- [`docs/ltm/briefs/pre-registration/Q-GATECART-1-verdict-preregistration.md`](../ltm/briefs/pre-registration/Q-GATECART-1-verdict-preregistration.md) — freeze `453148a`; §B (S_floor method, anchors), §F (S_A=1.83 Aegis / S_B=0.85 / floor(3,177)=2.05; divergence branch FIRED, Cap ∈ [1.0, 2.0] pending operator).
- [`docs/adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md`](../adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md) — `Accepted`; §2.1 K-counting rules (non-overlap tiling / face value), §2.2 K_SPA≠K_DSR, §2.3 V=1/n pin, §2.4 standing per-campaign power disclosure.
- [`docs/adr/2026-07-11-discovery-campaign-defaults-ratified.md`](../adr/2026-07-11-discovery-campaign-defaults-ratified.md) — `Accepted`; default #2 two-level K (program-cumulative per instrument-family feeds DSR; abandoned campaigns still bank).
- [`docs/adr/2026-07-13-harv-discovery-lane-ratification.md`](../adr/2026-07-13-harv-discovery-lane-ratification.md) — `Accepted` 2026-07-14; §2.2/§2.4 HARD §R clause-reachability gate blocking `register_search open`.
- [`docs/ltm/briefs/Q-HARV-1-month-end-rebalance-successor.md`](../ltm/briefs/Q-HARV-1-month-end-rebalance-successor.md) — DECLINE commit `9bddd33`; §R reachability table (joint P(RESOLVED|true) ≈ 5–6% at 2018+ N; "HARV cannot carry the 11-08 program").
- `lab/research_utils/deflated_sharpe.py` — anchor `48b8cef`; `expected_max_sharpe(k, var_trials)` / `deflated_sharpe(sr, n, skew, kurt, sr0)` signatures verified; published K-sweep **reproduced exactly this session** (K=1→0.65 … 3,177→2.05).
- `.claude/skills/futures-anomaly-discovery/scripts/register_search.py` — anchor `48b8cef`; the K-declaration enforcement point a screen PASS binds against (§5).
- [`docs/briefs/programs/2026-07-12-08-08-packet-pretriage.md`](programs/2026-07-12-08-08-packet-pretriage.md) — RATIFIED slate + the 11-08 resource-collision finding; this brief pre-assembles evidence and changes no slate class.
- [`STATE.md`](../../STATE.md) forward board + [`lab/CATALOG.md`](../../lab/CATALOG.md) actives + [`PIPELINES.md`](../../PIPELINES.md) P1 — the inventory sources §7 Phase 1 enumerates from.

**Sources read declaration** (INQHIORI canon §3): past chats N/A — all evidence is current-session repo reads listed above. User memory: supplementary only (`lesson_dsr_floor_k_governed`, `lesson_gate_reachability_preregistration`); every load-bearing number re-verified against the repo sources above. Tools available but unused: WebSearch/WebFetch — no external claim is authored here (S_B inherited by citation from the already-verified GATECART research note); Workflow — single-session arithmetic + enumeration, no fan-out warranted; databento tools — zero pulls, the screen is pre-data by construction.

**Pre-Q gate** (D-S-A on the I/N corpus):
- **D:** deleted closed-campaign re-litigation (DISC-CAMP-0, Q-HARV-1 retained *only* as calibration citations — test: duplicated by a higher-fidelity source, their operator-accepted closures); deleted flow-data axis candidates (test: known measurement artefact with a documented cause — A4 scoping §2's structural confound); deleted per-campaign gate mechanics from scope (test: outside the temporal/instrument scope of the question class — owned downstream by §R and DSR-K §2.4).
- **S:** the reachability question compresses to two per-axis scalars — floor(K_eff) vs the frozen band, and P(primary | true) — the exact pair on which the two campaigns died; nothing about the anomaly is lost at this dimension.
- **A:** floor(K) is monotone in K → the band boundaries are precomputed once (K ≤ 3 / ≤ ~447 / ≤ 2,038), so each axis screens in O(seconds) as a lookup + one power formula.

---

## §1 — Context & motivation

Within 48 hours, both live discovery lanes closed with zero admissible candidates on constraints that were computable **before any data was pulled**: Q-GATECART-1 (2026-07-14) found the DSR demonstrability floor at the banked wide-mining K=3,177 sits at 2.05 — above the best edge the programme has ever validated (Aegis 1.83) — killing the blind-mining class a-priori (M-19); Q-HARV-1/HARV-2026-002 (2026-07-14) was DECLINED at the §R HARD gate because its confirm bundle had P(RESOLVED | mechanism true) ≈ 5–6% at the available 2018+ N. Meanwhile the four-firms ADR §4 primary falsifier hard-dates **2026-11-08** (≥1 pre-registered candidate clearing the bust ceiling on ≥2 of 4 tiers, else the prop program demotes to research-only), sharing its runway with the Q-SFRISK-1 obligation. Axis selection for that runway currently has **no mechanical reachability screen** — the next axis would be picked the same way the last two were. This brief operationalizes the fork Q-GATECART-1 registered: screen every candidate axis's DSR floor at its intrinsic K, plus its confirm-gate power at its available N, **before** any authoring/scoping/K/pull is committed.

## §2 — Prior art / lineage

- **Q-GATECART-1** (CLOSED-FALSIFIED 2026-07-14) — parent; supplies the frozen floor method, the ceiling anchors (S_A/S_B, Cap ∈ [1.0, 2.0] pending), M-19, and the fork condition ("feeds 08-08 axis selection").
- **Q-HARV-1 §R DECLINE** (2026-07-14) — supplies Clause N's precedent (power < ~50% ⇒ unreachable) and the demonstration that mechanism-first K=1 axes can still die on N.
- **DSR-K ADR** (`Accepted` 2026-07-12) — supplies the K-counting rules and the *per-campaign* power-disclosure requirement (§2.4); this brief lifts the same test to the *axis-selection* tier (earlier, comparative, portfolio-of-axes).
- **HARV lane ADR** (`Accepted` 2026-07-14) — the downstream HARD §R gate a screen PASS explicitly does not discharge.
- **Campaign-defaults ADR** (`Accepted` 2026-07-11) — default #2 family-banked K, which makes K_eff family-dependent (GC/MGC banks 3,177).
- **Lessons:** M-19 (DSR floor is K-governed — dated 2026-07-14, quantified 2.05 vs 1.83); `lesson_gate_reachability_preregistration` (unreachable gates waste K — Q-HARV-0's structurally un-passable placebo); pre-triage §1 (11-08 resource collision — every hour on an unreachable axis is runway lost).

## §3 — Question (Q-KBUDGET-1)

Symptom-only form (no fix baked in): **two consecutive campaigns closed null on constraints computable before data; the 08-08 axis-selection decision has no a-priori reachability screen — which candidate discovery axes, if any, are reachable at the frozen anchors, and is the fundable set non-empty?**

## §4 — Falsifiable hypothesis (H-KBUDGET)

**H-KBUDGET:** If the frozen two-clause screen (paired pre-registration §B: floor(K_eff) within the frozen realism band, AND confirm-gate power ≥ 0.50 at the axis's declared panel) is applied to the operator-ratified candidate-axis inventory, **then at least one axis clears both clauses** (the fundable set is non-empty) and a ranked slate feeds the 08-08 axis-selection decision; **otherwise** the 11-08 four-firms §4 falsifier is a-priori unreachable via newly-started discovery, and program planning must treat it so *now* rather than discovering it at 11-08.

**Accept (RESOLVED) if:** ≥1 ratified-inventory axis is Clause-K PASS-invariant (floor ≤ 1.0, i.e. K_eff ≤ 3) or OPERATOR-BAND with floor ≤ the operator-resolved Cap, AND has Clause-N power ≥ 0.50 on cohort-cited inputs.
**Reject (FALSIFIED) if:** every screened axis fails ≥1 clause at the frozen anchors and no axis is UNSCREENABLE.
**Ambiguous-hold if:** all screened axes fail but ≥1 axis is UNSCREENABLE (missing declared design or missing citable effect prior) such that the verdict depends on it.

## §5 — Forbidden moves (each genuinely tempting)

- **Re-litigating the frozen anchors (S_A, S_B, the Cap range, DSR ≥ 0.95) to un-empty a failing fundable set** — the temptation if FALSIFIED fires. Ceiling amendment goes only through Q-GATECART-1-successor close-and-reopen (its closure carries the same bar); the DSR threshold's graded-admission alternative is an explicitly separate, unauthored Pre-Q (DSR-K ADR §2.5).
- **Treating a screen PASS as discharging the campaign-level gates** — the §R clause-reachability sim (HARV lane HARD gate) and the DSR-K §2.4 power disclosure still run at campaign pre-registration. The screen kills; it never blesses (pre-reg §B asymmetry).
- **Inventing an effect prior for an axis with no citable cohort** so Clause N can compute — UNSCREENABLE is the honest routing; the fix is a cheap scoping probe, not a number (rescope ADR §5 discipline; metric-cohort provenance binding).
- **Under-declaring K_intrinsic to land in a friendlier band** — a screen PASS is void if the campaign's eventual `register_search open` binds K above the declared band (pre-reg §C); the manifest is the enforcement point. Choosing a genuinely lower-K *design* is legitimate (that is M-19 working); declaring one and running another is not.
- **Using the screen to reopen DISC-CAMP-0 or Q-HARV-1** — both are operator-accepted closures cited as calibration kills only.
- **Letting the ranked slate become the funding decision** — the screen outputs reachability facts; axis funding is a STRATEGIC-LoR act at 08-08 (three-loop binding §14 no-borrowing rule). This brief delivers evidence, not a verdict on any axis's worth.

## §6 — Gate criteria (closure verdict)

Verbatim from the paired pre-registration §D (frozen there; restated for the reader):

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | Fundable set non-empty: ≥1 axis PASS-invariant, or OPERATOR-BAND ≤ resolved Cap, with Clause-N power ≥ 0.50 | Ranked slate → 08-08 packet (pre-assembled evidence); funded axes proceed to campaign scoping under the standing HARD gates |
| `FALSIFIED` | Fundable set empty across the full ratified inventory; zero UNSCREENABLE | Operator escalation **before** any new campaign pre-registers: 11-08 discharge cannot come from newly-started discovery — accept demotion risk or re-scope via the four-firms ADR's own amendment path |
| `AMBIGUOUS-HOLD` | All screened fail; ≥1 UNSCREENABLE flips the verdict | Name the missing input per axis; re-screen on supply or at 2026-08-08, whichever first |

Pre-registered before any axis is screened; amending mid-screen is Trap-12 → close AMBIGUOUS and reopen fresh.

## §7 — Execution plan (self-executing, CC-side; no Cursor handoff — adjudication-shaped work per the surface-allocation ADR)

- **Phase 0 — Rule-0 reads.** DONE parent-side (§0).
- **Phase 0.5 — Freeze.** Operator ratifies the paired pre-registration (G1); freeze commit recorded in §8. **No axis screened before this commit.**
- **Phase 1 — Inventory assembly + ratification.** Enumerate candidate axes from: STATE forward board; the 08-08 pretriage; `lab/CATALOG.md` actives (e.g. `tom_spx`, `eurusd_pattern_enum`, `orb_universe`, `us500_discovery`, `usoil_regime_capture` — status-checked, not assumed live); the GLBX instrument families in the databento skill; the Q-MECH-1 family synthesis (mechanism candidates); operator additions. Each entry carries the pre-reg §C declaration set (family, design class, tool ladder → K_intrinsic; era + event rate → N; cohort-cited δ, σ or UNSCREENABLE). **Operator ratifies the inventory before Phase 2** — the screen must not run on a self-serving axis list.
- **Phase 2 — Screen.** Compute per-axis {K_eff, floor, band, N, power}; artifacts to `lab/archive/q_kbudget_1_2026-07/` (floor scan script + the §E results annex row-fill). Pure arithmetic; zero pulls; zero K consumed.
- **Phase 3 — Verdict + slate.** Fire §6 against the table; write the closure record (§9); deliver the ranked slate (or the FALSIFIED escalation) into the 08-08 packet; update the STATE forward-board fork line.

## §8 — Verdict pre-registration (mandatory before Phase 2)

[`docs/briefs/pre-registration/Q-KBUDGET-1-screen-preregistration.md`](pre-registration/Q-KBUDGET-1-screen-preregistration.md) — the frozen screen (§B), inventory/ranking mechanics (§C), and the §6 table (§D).
Pre-registration commit hash: `b304f2c` (2026-07-14 — the commit landing the pre-reg's FROZEN/G1-ratified status; verified via §F hook #1 this session)
Pre-registration date: 2026-07-14 (FROZEN; G1 ratified)

## §9 — Closure record format

- **If RESOLVED:** `docs/briefs/closures/Q-KBUDGET-1-axis-reachability-screen.md` + the ranked slate table (the 08-08 deliverable).
- **If FALSIFIED:** same path, FALSIFIED verdict + the operator-escalation memo (no recommendation.md).
- **If AMBIGUOUS-HOLD:** same path + named missing inputs + re-screen trigger (date or input-supply event).
Closure must include: the §E table as measured vs. the frozen bands; which clause killed each excluded axis; lesson candidates with dated anchors.

## §10 — Audit hooks (runnable)

```bash
# §0 anchors still resolve
git log -1 --format='%h' -- lab/research_utils/deflated_sharpe.py            # expect 48b8cef (or later with §B re-verified)
git log -1 --format='%h' -- docs/ltm/briefs/Q-HARV-1-month-end-rebalance-successor.md

# Freeze ordering: pre-reg ratified commit predates any Phase-2 artifact
git log --format='%h %ci' -- docs/briefs/pre-registration/Q-KBUDGET-1-screen-preregistration.md | tail -1
git log --format='%h %ci' -- lab/archive/q_kbudget_1_2026-07/ 2>/dev/null | tail -1

# Floor table + band boundaries reproduce on the production module (see pre-reg §F hook #3 for the full command)
# Expect: K=1→0.65 · 3→0.98 · 441→1.83 · 2038→≤2.00 · 3177→2.05

# The fork line on STATE points here (no orphan fork)
grep -n "Q-KBUDGET-1" STATE.md

# No K consumed, no pulls, by this brief (screen is pre-data)
grep -rn "Q-KBUDGET" discovery_manifests/ 2>/dev/null && echo "REVIEW: screen consumed K?" || echo "no manifest entry (expected)"

# Downstream gates not weakened: HARD §R still present in the lane ADR + template
grep -n "HARD gate" docs/adr/2026-07-13-harv-discovery-lane-ratification.md
```

## Verification

```bash
# Discipline checks (mechanical)
PYTHONIOENCODING=utf-8 python scripts/check_brief.py docs/briefs/Q-KBUDGET-1-axis-reachability-screen.md --type inquire
# Expected: all checks PASS

# Rule-0 confirmation — cited constants match canonical sources
grep -n "2.05\|1.83\|0.85" docs/ltm/briefs/pre-registration/Q-GATECART-1-verdict-preregistration.md | head -5
grep -n "5–6%\|DECLINE" docs/ltm/briefs/Q-HARV-1-month-end-rebalance-successor.md | head -3
grep -n "non-overlapping tiling\|V = 1/n" docs/adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md | head -3

# Pre-registration exists and is paired
test -f docs/briefs/pre-registration/Q-KBUDGET-1-screen-preregistration.md && echo paired
```

*Pre-lock checklist removed at lock (2026-07-14): §8 freeze recorded above (`b304f2c`); verification block executed at lock — skill-side `check_brief --type inquire` 6/6 PASS.*
