# Q-TRAINKILL-2 — CLOSURE: `AMBIGUOUS-HOLD` (both named alternates fit)

**Verdict:** `AMBIGUOUS-HOLD` — Limb 1 no-fire (MSL-S2A promoted; 6 remain BOUNDED; extremes still disagree). Limb 2: `NEG` g(−0.10)=0.239 and `DEP-ZERO` g=0.189 both ≥ 0.05
**Closed:** 2026-08-18
**Lane:** UNASSIGNED
**Pre-registration:** [`Q-TRAINKILL-2-verdict-preregistration.md`](../pre-registration/Q-TRAINKILL-2-verdict-preregistration.md) — frozen on disk at sha256 `86049b89b413b33430e7dfe31d9fc5de5cc46b81c0f23f3ea7877d78c7605b5d` (printed by the scorer **before** `TABLE.json` was opened)
**Spend / K:** $0.00 · K consumed: **0** · no manifest
**Live effect:** none on rail / `core/` / `dd_protection`. No gate number moves. B2 stays unblocked with no singleton power finding.
**Artifacts:** [parent brief](../Q-TRAINKILL-2-bounded-recovery-alt-dgp.md) · [prereg](../pre-registration/Q-TRAINKILL-2-verdict-preregistration.md) · [`RESULTS`](../../../lab/analysis/_inbox/q_trainkill_2_2026-08/RESULTS.md)
**Parent:** [`Q-TRAINKILL-1-closure-ambiguous-hold.md`](Q-TRAINKILL-1-closure-ambiguous-hold.md)

---

## 1. Verdict (§6 asserted against actual numbers)

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` — Limb-1 TK1 reading | ≥1 promotion and extremes agree | 1 promotion; lo=`MISCALIBRATED` · hi=`KILLS-INFORMATIVE` | — |
| `RESOLVED` — `NEG-FAMILIES` | Limb 2: only NEG fits | NEG fits (0.239); DEP-ZERO also fits | — |
| `RESOLVED` — `KILLS-INFORMATIVE-DEP` | Limb 2: only DEP-ZERO fits | DEP-ZERO fits (0.189); NEG also fits | — |
| `AMBIGUOUS-HOLD` | both alternates fit, or n*=0 | both fit; n*=9 | ✓ |
| `MISCALIBRATED` | neither alternate fits | both fit | — |

Walked the non-firing rows (required). Inherited bar still misses (g(+0.10)=0.000961) — disclosed, not a Limb-2 fire. Fréchet-lo disclosed at 0.00208, not a fire.

**Disclosure — Limb-2 cell space was pre-narrowed.** DEP-ZERO's per-row likelihood is a se-free constant of each row's already-committed `event` label — `mu/se` is 0/se regardless of se, so p_event(event, 0, se) collapses to one of two values: ≈0.025 (FALSIFIED/CLEARED) or ≈0.950 (AMBIGUOUS), never a function of the transcribed CI. Confirmed against all 9 `P_dep_zero` entries in RESULTS.json — exactly two distinct values appear (0.9500042097035593 ×5, 0.024997895148220373 ×4). The geometric mean clears the 0.05 floor whenever ≥~19% of scored rows carry AMBIGUOUS; this census clears it at 5/9 (55.6%), fixed at table-assembly time, before any μ/joint was chosen. So NEG-FAMILIES-as-sole-winner and MISCALIBRATED — the two outcomes §F actually predicted for Limb 2 — were dead cells before this packet ran: `AMBIGUOUS-HOLD` was the only reachable Limb-2 reading. Verdict unchanged.

## 2. What the pre-registration predicted vs what happened

§F predicted 0 promotions. Observed **1** (MSL-S2A mean-R CIs were on the page; the binding kill was N-ACT, but §B promotes on the interval's existence). Limb 1 still no-fire — the six non-R rows keep the extremes disagreeing. §F predicted Limb-2 `MISCALIBRATED` or `NEG-FAMILIES`. Observed **both** named alternates fit. The miss on the singleton prediction is the hold, not a retune.

## 3. What this closure does NOT license

- Picking `NEG-FAMILIES` or `KILLS-INFORMATIVE-DEP` after seeing both g's.
- Quoting `GATES-UNDERPOWERED` (bar still misses).
- Lowering any gate, or moving 0.05 / μ / the product.
- A one-arm re-read of a both-arms cell.
- ρ→R on the six remaining BOUNDED rows.
- Naming a third μ to break the tie.
- Opening the named successor (operator GO is a fresh decision).

## 4. Defects found in the frozen brief (recorded, not repaired)

§F's "0 promotions" class-prior missed MSL-S2A. The recovery rule as written promoted it. No brief amendment.

`score_trainkill2.py`'s `geo_mean()` floors each log-input at `EPS=1e-6` (`max(EPS, p)`); the parent `score_trainkill.py`'s (TK1) `geo_mean()` has no such floor — undeclared against the prereg's "Inherited, not retuned" pledge. Effect, re-derived: `g(+0.10)` published clamped at 0.000961192 vs 5.904343e-05 unclamped (≈16.3× inflation — four rows, MSL-C1/C2/C3-K2/Q-MNQDTL-CON-1, land below 1e-6 pre-floor); both read far under the 0.05 floor, so `reading()`'s output is unchanged either way — decision-inert. The disclosed Fréchet-lo value (0.00208137) is entirely a clamp artifact: under `frechet_lo` four rows (`max(0, p_l+p_s-1)`) evaluate to an exact `0.0`, so the unclamped geometric mean is undefined (`math.log(0.0)`) — without the clamp it does not read as a small positive number, it does not compute. g0/gneg/gdep_zero(frechet_hi) are unaffected by the clamp (every row-level input to those three is already ≥ EPS from `p_event`'s own clamp). Not a fire on any cell; disclosure only.

## 5. Lesson candidates

Below the two-incident bar — watch: a cadence kill can still quote a mean-R CI, and a recovery rule that keys on interval *existence* will promote it. Dated: 2026-08-18, this close. Dollar cost: $0.

## Iterate — loop exit (MANDATORY)

- **Verdict used:** `AMBIGUOUS-HOLD`
- **Model update:** Recovery does not resolve the {0, +0.10} pair. The scored core is consistent with *either* true −0.10R families *or* zero-edge under Fréchet-hi dependence, and still inconsistent with +0.10R under independence. The two named stories were not discriminated.
- **Next:** ITERATE
- **Routing:** Identify — a discriminator the two surviving DGPs predict differently, declared before any new g, **or** an operator election that names one DGP as working-model without claiming the other is falsified. Do not name a third μ.
- **Entry packet:** Successor named **Q-TRAINKILL-3** (NEG-vs-DEP discriminator) — **not opened**. Carry: frozen 15-set, inherited constants, MSL-S2A promoted, six still-BOUNDED, g(NEG)=0.239, g(DEP-ZERO)=0.189, g(+0.10)=0.000961, both-alternates-fit hold. Forbidden re-opens: picking one of the two after this g; retuning 0.05 / μ / product; one-arm re-read; ρ→R; a third μ. Budget: $0 / K=0 for an operator election; a new-panel discriminator is a separate operator GO.
- **Stop rule / re-proposal bar:** a pre-declared measurement the two DGPs split, or an operator election naming exactly one working-model. θ-moves and a third μ do not reopen.
- **Board write:** STATE decision-index 2026-08-18 Q-TRAINKILL-2 line; SESSIONS 18h Open/next names Q-TRAINKILL-3 not opened; notice B2 still unblocked with no singleton power finding.
- **Registry:** n/a — power census / methodology; not a strategy-grounds seed kill

## §10 audit-hook discharge

```
rg -n "Q-TRAINKILL-1-closure-ambiguous-hold" docs/briefs/Q-TRAINKILL-2-bounded-recovery-alt-dgp.md
→ hits (parent cite)

rg -n "Fréchet-hi|one-arm re-read" docs/briefs/pre-registration/Q-TRAINKILL-2-verdict-preregistration.md
→ Fréchet-hi named; one-arm re-read forbidden

rg -n "86049b89b413b33430e7dfe31d9fc5de5cc46b81c0f23f3ea7877d78c7605b5d" lab/analysis/_inbox/q_trainkill_2_2026-08/RESULTS.md
→ 10:`86049b89b413b33430e7dfe31d9fc5de5cc46b81c0f23f3ea7877d78c7605b5d`

python lab/analysis/_inbox/q_trainkill_2_2026-08/score_trainkill2.py
→ prereg_sha256 86049b89…7605b5d
→ n_scored 9  n_promoted 1  limb1_fire False
→ g(-0.10)=0.239  g(DEP-ZERO)=0.189
→ verdict AMBIGUOUS-HOLD  named NEG-FAMILIES|KILLS-INFORMATIVE-DEP
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-18 | Closure authored | Cursor (this session) |
