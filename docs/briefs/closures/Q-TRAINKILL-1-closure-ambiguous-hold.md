# Q-TRAINKILL-1 — CLOSURE: `AMBIGUOUS-HOLD` (BOUNDED extremes disagree; scored core MISCALIBRATED)

**Verdict:** `AMBIGUOUS-HOLD` — all-BOUNDED-at-ε reads `MISCALIBRATED`; all-BOUNDED-at-1−ε reads `KILLS-INFORMATIVE`; scored-only n*=8 is `MISCALIBRATED` (g(0)=0.024365 < 0.05; g(+0.10R)=1.807e-05)
**Closed:** 2026-08-18
**Lane:** UNASSIGNED
**Pre-registration:** [`Q-TRAINKILL-1-verdict-preregistration.md`](../pre-registration/Q-TRAINKILL-1-verdict-preregistration.md) — frozen on disk at sha256 `91855ed188e6d5268ef2050e21d9f77649c6f21ac9b19716e181b3cc59981730` (printed by the scorer **before** `TABLE.json` was opened)
**Spend / K:** $0.00 · K consumed: **0** · no manifest
**Live effect:** none on rail / `core/` / `dd_protection`. No gate number moves. B2 priced-spend election is unblocked and must disclose this hold (no named power finding to consume).
**Artifacts:** [parent brief](../Q-TRAINKILL-1-train-gate-power.md) · [prereg](../pre-registration/Q-TRAINKILL-1-verdict-preregistration.md) · [`RESULTS`](../../../lab/analysis/_inbox/q_trainkill_1_2026-08/RESULTS.md)
**Parent notice:** [`N-2026-08-18-iteration2-identify-notice`](../../notes/notice/N-2026-08-18-iteration2-identify-notice.md)

---

## 1. Verdict (§6 asserted against actual numbers)

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` — `KILLS-INFORMATIVE` | g(0)≥0.05 and g(0.10)<0.05; BOUNDED extremes agree | scored g(0)=0.024 < 0.05; hi-extreme only | — |
| `RESOLVED` — `GATES-UNDERPOWERED` | g(0.10)≥0.05 | g(0.10)=1.807e-05 at every bracket | — |
| `MISCALIBRATED` | neither fits; BOUNDED extremes agree | neither fits on the scored core; extremes **disagree** | — |
| `AMBIGUOUS-HOLD` | BOUNDED extremes disagree or n*=0 | lo=`MISCALIBRATED` · hi=`KILLS-INFORMATIVE`; n*=8 | ✓ |

Walked the non-firing rows (required). The predicted `GATES-UNDERPOWERED` class did not fire. The scored residue is the four both-arms FALSIFIED products (P(F\|μ=0)≈0.000625 each under independence) plus CON-4's tight zero-straddle (P(AMB\|μ=+0.10)=0.00272). That mix is what the frozen 0.05 geometric-mean floor rejects for both DGPs.

## 2. What the pre-registration predicted vs what happened

Prereg §F predicted `GATES-UNDERPOWERED` from the class (a +0.10R mean against a few-hundred-trade se typically leaves CI straddling 0). The four CON cells did straddle. The four both-arms FALSIFIED cells did not — they are formal CI_hi<0 on **both** arms, and the frozen independence product makes each almost impossible under μ=0 and vanishing under μ=+0.10. Surprise is on the joint, not on the CON straddles. Floor / product / set were not moved.

## 3. What this closure does NOT license

- Quoting `GATES-UNDERPOWERED` or `KILLS-INFORMATIVE` as the class reading.
- Lowering any gate threshold, or moving 0.05 / μ_bar / the both-arms product after seeing g.
- Rewriting campaign #2 n/panel from a named power finding (there is none).
- Quoting zero-yield streaks as settled supply-drought, or as settled under-power.
- Dropping a named row, or mapping ρ / N-ACT / annSR into +0.10R after this g.
- Treating reachability audits as this answer.
- Opening the named successor (operator GO is a fresh decision).

## 3a. Successor inheritance (disclosure only — does not reopen)

Q-TRAINKILL-2 and Q-TRAINKILL-3 (both closed in this PR, both citing this closure as parent) inherited this packet's bracket/floor/event-map mechanism unchanged. Their own `AMBIGUOUS-HOLD` readings carry the same design-certainty caveat as §4 here (confirmed independently in TK2 §4's DEP-ZERO se-free-constant disclosure and TK3 §4's Block-A foreclosure). Reader-intercept only — does not reopen either successor or change either verdict.

## 4. Defects found in the frozen brief (recorded, not repaired)

**Gate-reachability defect — the lo/hi BOUNDED-bracket disagreement that drives `AMBIGUOUS-HOLD` is design-certain, fixed by the event map alone, before any CI was transcribed.**
At μ=0 the `mu/se` term is `0/se` regardless of `se`, so every row's `P(event\|μ=0)` collapses to one of two se-free constants: `Φ(-1.96)²=0.0006248947618414197` for the 4 both-arms-FALSIFIED rows, `1-2Φ(-1.96)=0.9500042097035593` for the 4 one-arm-AMBIGUOUS rows — giving `g(0)=0.024365` exactly, independent of any transcribed CI (re-derived here, matches `RESULTS.json` to full float precision). That fixes both BOUNDED-extremes regardless of what CI values TABLE.json carried:
- lo (7 BOUNDED→ε): capped at `((1-ε)^8·ε^7)^(1/15) ≈ 1.585e-3 < 0.05` for *any* CI — always `MISCALIBRATED`.
- hi (7 BOUNDED→1-ε): `(g(0)^8·(1-ε)^7)^(1/15) ≈ 0.1379 ≥ 0.05` exactly, for *any* CI — never `MISCALIBRATED`.

lo≠hi therefore holds for every possible `TABLE.json`, not just the one committed: the §6 `RESOLVED` route (extremes agree) was structurally unreachable the moment this 8-scored (4-AMBIGUOUS/4-FALSIFIED)/7-BOUNDED classification froze, before any CI entered the table. `AMBIGUOUS-HOLD` carried zero verdict information beyond that pre-transcription commitment. Verdict unchanged — the hold is real, just not a discovery about the transcribed CIs. Not a Trap-#12 amendment candidate (bar/product/floor are not wrong); it is a §6-route-reachability miss.

## 5. Lesson candidates

Confirmed firing of `[[lesson_gate_reachability_preregistration]]` (cf. `docs/notes/audits/2026-07-12-disccamp0-gate-reachability-audit.md`; siblings M-19/M-20 in `methodology_lessons.md` are the DSR-floor and cost-gate instances of the same pattern, not this one; cf. TK3 §4's identical Block-A foreclosure, TK2 §4's identical DEP-ZERO se-free-constant disclosure) — a §6 route whose reachability is fixed by the committed event map alone, before any CI is transcribed, is not a discovery when it fires. Here: the 4-AMBIGUOUS/4-FALSIFIED/7-BOUNDED classification alone forecloses `RESOLVED` at both BOUNDED extremes (§4) — `AMBIGUOUS-HOLD` was locked in at table-assembly, not learned from the transcribed CIs. Dated: 2026-08-18, this close. Dollar cost: $0 (caught at the cheap falsifier, post hoc — should have been caught at pre-registration §D).

## Iterate — loop exit (MANDATORY)

- **Verdict used:** `AMBIGUOUS-HOLD`
- **Model update:** The lo/hi disagreement is design-certain (§4) — locked in by the 4-AMBIGUOUS/4-FALSIFIED/7-BOUNDED event map alone, before any CI was transcribed; it is not itself evidence about empty vs. +0.10R under-power. Within that design, the transcribed data reject the +0.10R DGP at **both** brackets: `g(0.10)_lo=4.681e-06`, `g(0.10)_hi=2.954e-03`, both ≪ 0.05 (vs. the design-only sup of `g(0)=0.024365`, also < 0.05 — so `GATES-UNDERPOWERED` was unreachable at any bracket, §4). The seven BOUNDED rows move the hold's magnitude, not whether it fires.
- **Next:** ITERATE
- **Routing:** Investigate — recover mean-R CIs for the seven BOUNDED rows from committed closures, **or** accept the scored-only core as `MISCALIBRATED` and name a different DGP (negative-mean and/or both-arms dependence). Do not lower bars. Return is to the named successor's entry packet, not a silent reopen of this brief.
- **Entry packet:** Successor named **Q-TRAINKILL-2** (recover-BOUNDED / alternate-DGP) — **not opened**. Carry: frozen 15-set, μ_0=0, μ_bar=+0.10R, se=CI-width/3.92, both-arms independence product, fit floor 0.05, event map, no bar-lowering. Carry-forward numbers: scored g(0)=0.024365, g(0.10)=1.807e-05; four both-arms P(F\|μ=0)≈0.000625; CON-4 P(AMB\|μ=0.10)=0.00272; BOUNDED ids MSL-S2A · R2VBUCK/FLOW/AGRUN · DL-1 · CAPFLOW · DSTRUCT. Forbidden re-opens: retuning independence, the floor, or μ_bar after seeing this g; dropping a named row; translating ρ to +0.10R. Budget: $0 / K=0 if the successor only recovers already-committed mean-R CIs; new panels are a separate operator GO.
- **Stop rule / re-proposal bar:** new *recoverable mean-R CI* for a currently-BOUNDED row, or a named alternate DGP declared **before** any re-score. θ-moves of 0.05 / μ_bar / the product do not reopen. A one-arm re-read of a both-arms cell is not a re-proposal.
- **Board write:** STATE decision-index 2026-08-18 Q-TRAINKILL-1 line; SESSIONS 18g Open/next drops "Q-TRAINKILL-1 named, not opened" and records B2 unblocked with this hold disclosed; notice packet 3 CLOSED.
- **Registry:** n/a — power census / methodology; not a strategy-grounds seed kill

## §10 audit-hook discharge

```
rg -n "N-2026-08-18-iteration2-identify-notice" docs/briefs/Q-TRAINKILL-1-train-gate-power.md
→ hits (parent cite)

rg -n "no gate threshold|bar-lowering" docs/briefs/pre-registration/Q-TRAINKILL-1-verdict-preregistration.md
→ Forbidden regardless of outcome: no gate threshold moves / never bar-lowering

rg -n "91855ed188e6d5268ef2050e21d9f77649c6f21ac9b19716e181b3cc59981730" lab/analysis/_inbox/q_trainkill_1_2026-08/RESULTS.md
→ 10:`91855ed188e6d5268ef2050e21d9f77649c6f21ac9b19716e181b3cc59981730`

python lab/analysis/_inbox/q_trainkill_1_2026-08/score_trainkill.py
→ prereg_sha256 91855ed1…81730
→ n_scored 8  n_bounded 7
→ g(0)=0.024365  g(0.10)=1.80677e-05  floor=0.05
→ verdict AMBIGUOUS-HOLD  named MISCALIBRATED|KILLS-INFORMATIVE
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-18 | Closure authored | Cursor (this session) |
| 2026-08-18 | §4 recorded a gate-reachability defect (lo/hi BOUNDED extremes are design-certain from the 4-AMBIGUOUS/4-FALSIFIED/7-BOUNDED event map alone, independent of any transcribed CI); §5 elevated to a confirmed lesson-class firing; Iterate Model-update line reworded (no longer "does not discriminate empty vs under-power"); §3a successor-inheritance disclosure added; §10 cmd 3 fixed (was a non-matching `prereg_sha256` grep; now matches the hash literal). Verdict unchanged. | Claude (adversarial-review pass) |
