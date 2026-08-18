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

## 4. Defects found in the frozen brief (recorded, not repaired)

None found. The prediction miss is a §F class-prior miss, not a Trap-#12 amendment candidate.

## 5. Lesson candidates

Below the two-incident bar — watch: a both-arms FALSIFIED gate under an independence product is a different statistical object from a one-arm straddle. Joint power questions that mix the two will tend to `MISCALIBRATED` at a 0.05 geometric-mean floor even when the straddles look like the predicted class. Dated: 2026-08-18, this close. Dollar cost: $0 (caught at the cheap falsifier).

## Iterate — loop exit (MANDATORY)

- **Verdict used:** `AMBIGUOUS-HOLD`
- **Model update:** The 15-row kill record does not discriminate empty families from +0.10R under-power. The eight mean-R cells are jointly too extreme for either DGP (four both-arms products + one tight zero-straddle). The seven BOUNDED rows can flip the reading if they are treated as P≈1, which is why the hold exists.
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

rg -n "prereg_sha256" lab/analysis/_inbox/q_trainkill_1_2026-08/RESULTS.md
→ 91855ed188e6d5268ef2050e21d9f77649c6f21ac9b19716e181b3cc59981730

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
