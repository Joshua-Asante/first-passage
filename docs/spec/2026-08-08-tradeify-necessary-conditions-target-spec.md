# SPEC: TNEC-1 — Tradeify-compatible construct or book: necessary conditions only

Status: RATIFIED · 2026-08-08 / JA · authorizes nothing ($0 · K=0) · depends: [ADR 2026-08-08 edge-cohort correction + necessity retarget](../adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md) (§8 filled; atomic with this flip)
Objective: Replace MNQDTL-1's elective target (D1 daily cadence · D2 $325 · μ-gate · MNQ-only) **as the intake gate** with the venue/program-**necessary** condition set for admitting a strategy — or a book of strategies scored jointly — to the incumbent `Tradeify_Select_100K` eval. MNQDTL-1 remains `RATIFIED` as historical target record; closed doors C1–C11 stand.

> ⚠ **Reader-intercept 2026-09-03 — N-SURV's ceiling moved.** The live Part A eval bust ceiling is
> **5.0%**, not the 3.0% item 2 names ([`prereg v2`](../briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md) §3, 2026-08-26,
> an operator risk-tolerance override; `prop_survivor_scoring.DEFAULT_PREREG` resolves to it). The
> pass floor (≥50%), the intraday-honest clock, and every other limb below are **unchanged**. Body
> frozen at ratification (Trap #12); read item 2's threshold as **bust ≤ 5.0%**.

Necessary set (single construct, or book jointly; **nothing else gates intake**):

1. **N-ACT** — ≥1 trade per Mon–Fri week by construction (book: jointly, co-idleness measured and disclosed — correlated idleness is the failure mode). Operator token trade remains the fallback until a candidate lands (STATE row 0; R8 still owed).
2. **N-SURV** — pre-registered survivor-scoring at the frozen gate: **intraday-honest bust ≤ 3.0% ∧ P(pass) ≥ 50%** ([2026-07-13 prereg](../briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md), unedited) at deployable integer sizing on the incumbent eval. Book: composed, and the regime both-halves gate applies.
3. **N-EDGE** — net expectancy > 0 after Requirement-5 costs (screen $0.95/side; Tradeify actual $0.91), 95% CI excluding 0 at the pre-registered unit, and DSR ≥ `floor_at_k(K_intrinsic)` (EM0 unchanged: catalogue ≤3, working K=1–2). The 0.40R line survives as **disclosure only**: below it frequency cannot raise μ (inversion) — quote as arithmetic, never as admissibility.
4. **N-SHAPE** — EM3 independence + hard-stop integrity (no pyramiding/scale-ins; gap tail disclosed) and EM5 session/slot legality (flat by 16:00 ET build target inside the 16:45 venue print · micro-expressible · Product-Group sign constraint across co-legs (§4a) · S7 order-symbol occupancy where an account is shared).
5. **N-SIZE** — risk/trade ≤ the candidate's **own** measured-edge frontier at a stated bust tolerance (EM2 principle, edge-indexed). The published $325 @ 0.85R cell is void as provenance (phantom cohort — ADR §1); cells re-derive per candidate.

Demoted to recorded preferences (report, never gate): daily cadence (ex-D1) · income shape (μ* ≈ $250/day — funded-phase design preference; re-election as a gate is a fresh ratification against the corrected cohort table) · any daily-loss constant (ex-D2 — a daily stop-down stays available as an ops control; its value, if used, derives from the candidate's own frontier) · pass speed (venue has no time limit).

Steps:
1. ~~Operator ratifies the ADR §8 — this spec's Status flips PROPOSED → RATIFIED in the same commit.~~ **DONE 2026-08-08 / JA.**
2. Intake resumes under N-ACT…N-SIZE: sourcing per ADR §2-C L2 (previously-unrun channels only; Req 1–5 unchanged); instrument pool per L3 (MES/MGC re-entered; M2K one-shot + W4 dry-run rules stand; MCL open); book candidates per L4.
3. Every candidate closes with the verdict string `N-ACT N-SURV N-EDGE N-SHAPE N-SIZE | bust | P(pass) | μ(disclosed)` so the failing limb is never lost to a summary word.

Gate: RESOLVED if a candidate (or book) clears N-ACT…N-SIZE at pre-registered scoring on the incumbent eval → routes to operator GO (admits nothing, arms nothing — M1 + per-session GO + `LEG_MAP` release ruling remain the deploy chain). FALSIFIED if 2026-11-08 passes with no N-clear candidate — the [four-firms ADR §4](../adr/2026-07-12-prop-portfolio-four-friendly-firms.md) demotion clause governs; this spec adds no second clock.
Boundary: MNQDTL §3.1 closed doors C1–C11 stand (ledger facts) · no Striker-leg redeploy · no ORB unpark outside re-park R2/R3 · no arming · income aspiration must not re-enter as a gate without explicit re-election · no loosening of harvest Req 1–5, EM0, or the regime gate under cover of "necessity".
Reads: `core/firm_rules.py` Tradeify_Select_100K @ `45e3cea` · seed-target RESULTS @ `5ebee58` · survivor-scoring prereg @ `91137fb` · EM screen @ `d93dafd` · MNQDTL-1 @ `27c7943` · MNQBASE-1 §1.3 @ `d08537a` · re-park ADR @ `9b5ce43`
Owner: [ADR 2026-08-08 edge-cohort correction + necessity retarget](../adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md)
