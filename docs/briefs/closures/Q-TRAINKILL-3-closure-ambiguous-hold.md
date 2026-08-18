# Q-TRAINKILL-3 — CLOSURE: `AMBIGUOUS-HOLD` (Block F NEG, Block A DEP; split)

**Verdict:** `AMBIGUOUS-HOLD` — Block F winner `NEG` (g 0.246 / 0.025, ratio 9.83 ≥ 2); Block A winner `DEP` (g 0.234 / 0.950, ratio 0.246 ≤ 1/2). Election limb did not fire.
**Closed:** 2026-08-18
**Lane:** UNASSIGNED
**Pre-registration:** [`Q-TRAINKILL-3-verdict-preregistration.md`](../pre-registration/Q-TRAINKILL-3-verdict-preregistration.md) — frozen on disk at sha256 `93c21d21eb0fd2d0e580a384a586dbf10d19d8a23a593dea6e147f63ad57e7f6` (printed by the scorer **before** TK2 `RESULTS.json` was opened)
**Spend / K:** $0.00 · K consumed: **0** · no manifest
**Live effect:** none on rail / `core/` / `dd_protection`. No gate number moves. B2 stays unblocked with no singleton power finding. This TRAINKILL census **stops**.
**Artifacts:** [parent brief](../Q-TRAINKILL-3-neg-vs-dep-discriminator.md) · [prereg](../pre-registration/Q-TRAINKILL-3-verdict-preregistration.md) · [`RESULTS`](../../../lab/analysis/_inbox/q_trainkill_3_2026-08/RESULTS.md)
**Parent:** [`Q-TRAINKILL-2-closure-ambiguous-hold.md`](Q-TRAINKILL-2-closure-ambiguous-hold.md)

---

## 1. Verdict (§6 asserted against actual numbers)

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` — `NEG-FAMILIES` | both blocks `NEG` | F=`NEG`, A=`DEP` | — |
| `RESOLVED` — `KILLS-INFORMATIVE-DEP` | both blocks `DEP` | F=`NEG`, A=`DEP` | — |
| `AMBIGUOUS-HOLD` | split or tie | split; neither block `TIE` | ✓ |
| Election | GO names exactly one DGP | GO named neither | — |

Walked the non-firing rows (required). Both 2:1 bars cleared in opposite directions (F 9.83:1 NEG; A 4.06:1 DEP). Not a pair of ties.

## 2. What the pre-registration predicted vs what happened

§F predicted `AMBIGUOUS-HOLD` (split) from the class (FALSIFIED cells favor NEG; tight-straddle / AMBIGUOUS cells favor DEP). Observed that split. No surprise. The 2:1 bar produced two named winners, not ties — also as the class guess allowed.

## 3. What this closure does NOT license

- A singleton working-model.
- Quoting `GATES-UNDERPOWERED`.
- Q-TRAINKILL-4 on these P vectors.
- A third μ, a one-arm re-read, ρ→R, or any gate-threshold move.
- Treating this GO as an election.
- Reading STOP as a license to skip a power annotation on a *new* panel (a new panel is a new Q).

## 4. Defects found in the frozen brief (recorded, not repaired)

None found.

## 5. Lesson candidates

Below the two-incident bar — watch: a joint g can clear 0.05 for two DGPs while the event-class blocks name opposite winners. Dated: 2026-08-18, this close. Dollar cost: $0.

## Iterate — loop exit (MANDATORY)

- **Verdict used:** `AMBIGUOUS-HOLD`
- **Model update:** The four both-arms FALSIFIED cells look like true −0.10R. The five AMBIGUOUS cells look like zero-edge under Fréchet-hi (driven hard by CON-4). The committed mean-R record does not pick a singleton DGP. +0.10R under independence remains inconsistent with the joint (TK2 carry-forward).
- **Next:** STOP
- **Routing:** This census dies here. Attention returns to B2 (elects on existing evidence + H1 screen, TRAINKILL holds disclosed), S2/S3 as spec-resident obligations, and the 2026-11-08 clock. None of them opened here.
- **Entry packet:** n/a
- **Stop rule / re-proposal bar:** a **new panel** (fresh mean-R CIs, operator GO + K) or an **operator election** naming exactly one of `NEG-FAMILIES` / `KILLS-INFORMATIVE-DEP` as working-model without claiming the other is falsified. A fourth scoring rule on the same nine P vectors, a third μ, or a θ-move of 2:1 / 0.05 / the joints does not reopen.
- **Board write:** STATE decision-index 2026-08-18 Q-TRAINKILL-3 line; SESSIONS 18i Open/next drops Q-TRAINKILL-3 and does not name Q-TRAINKILL-4; notice B2 still unblocked with holds disclosed.
- **Registry:** n/a — power census / methodology; not a strategy-grounds seed kill

## §10 audit-hook discharge

```
rg -n "Q-TRAINKILL-2-closure-ambiguous-hold" docs/briefs/Q-TRAINKILL-3-neg-vs-dep-discriminator.md
→ hits (parent cite)

rg -n "2:1|Block F|election limb" docs/briefs/pre-registration/Q-TRAINKILL-3-verdict-preregistration.md
→ blocks / 2:1 / election limb present

rg -n "prereg_sha256" lab/analysis/_inbox/q_trainkill_3_2026-08/RESULTS.md
→ 93c21d21eb0fd2d0e580a384a586dbf10d19d8a23a593dea6e147f63ad57e7f6

python lab/analysis/_inbox/q_trainkill_3_2026-08/score_trainkill3.py
→ prereg_sha256 93c21d21…ad57e7f6
→ block_F winner NEG  ratio=9.826
→ block_A winner DEP  ratio=0.2462
→ verdict AMBIGUOUS-HOLD  named NEG|DEP
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-18 | Closure authored | Cursor (this session) |
