# Pre-registration — Q-KBUDGET-1 axis-reachability screen (frozen formula)

**Status:** **FROZEN — operator ratified 2026-07-14 (G1).** The commit that lands this status change is the freeze commit; the closure record cites it via `git log --format='%h %ci' -- <this file> | tail -1` (§F hook #1). No item in §B/§C/§D changes after any axis is screened. Screening an axis before the freeze commit voids that axis's screen result.
**Parent brief:** [`docs/briefs/Q-KBUDGET-1-axis-reachability-screen.md`](../Q-KBUDGET-1-axis-reachability-screen.md)
**Loop of record:** OUTER (produces decision inputs; the axis-funding act itself is STRATEGIC-LoR at 2026-08-08)
**Feeds:** 08-08 axis selection → the four-firms ADR §4 primary falsifier runway (hard date 2026-11-08).
**Authored:** 2026-07-14 · Claude Code (Fable 5), operator-directed (successor route chosen after the Q-HARV-1 §R DECLINE).
**Ratified:** 2026-07-14 · Joshua (operator, G1) — "I ratify the screen pre-registration."

---

## §A — Why a frozen screen, not per-axis judgment

Two campaigns died in 48 hours on constraints computable before any data was pulled: DISC-CAMP-0's candidate class was dead at the DSR selection floor (K=3,177 ⇒ floor 2.05 > best-validated edge 1.83 — Q-GATECART-1, M-19), and HARV-2026-002 was DECLINED at §R because its confirm gate had P(pass | true) ≈ 5–6% at the available N. Axis selection for the shared 08-08→11-08 runway currently has no mechanical screen; judging axes one-at-a-time after this file exists would let the anchors drift toward whatever axis is being argued for. The screen is therefore frozen here — formula over already-frozen external anchors — before any axis is measured (the same freeze-before-measure discipline as Q-GATECART-1 §B and the HARV lane HARD gate).

## §B — The screen (two clauses; both must hold; frozen)

> ⚠ **READER INTERCEPT — 2026-08-04. One formula below is superseded; the rest of §B still governs.**
> This is a **frozen** pre-registration and its body is left byte-intact as the record of what was
> registered on `b304f2c`. But live doctrine
> ([`strategy_harvest.md`](../../methodology/strategy_harvest.md)) cites §B as its source of
> truth, so the divergence is flagged here, at the point of reading, rather than only downstream.
> **`K_eff = K_intrinsic + K_banked(family)` is no longer the rule.** Per
> [ADR 2026-08-04](../../adr/2026-08-04-family-k-bank-disclosure-not-gate.md) (`Accepted`),
> **`K_eff = K_intrinsic`** — within-search selection only — and `K_banked(family)` is a
> **mandatory disclosure that no longer gates**. Everything else in §B — Clause N, the floor
> ladder (1→0.65 · 2→0.85 · 3→0.98 · 4→1.06), Cap 1.0, `DSR ≥ 0.95`, `V = 1/n`, the
> generous-inputs rationale, and "a PASS never blesses" — is **unchanged and still in force**.

An axis is screened on the pair **(K_eff, N-power)**. Both clauses are deliberately **generous** (most-permissive frequency; full declared OOS N): a screen **FAIL is strong** (even generous inputs cannot rescue the axis) while a **PASS never blesses** — it only licenses campaign scoping, and the campaign-level HARD gates (§R clause-reachability sim per the HARV lane ADR; DSR-K ADR §2.4 power disclosure) still run at pre-registration. The screen can kill an axis; it can never promote one. This mirrors the A4 diagnostic's DROP-or-DEFER asymmetry.

### Clause K — DSR demonstrability floor vs. the frozen realism band

- **K_eff = K_intrinsic + K_banked(family).** K_intrinsic is counted from the axis's *declared* search design per the DSR-K ADR rules (`docs/adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md` §2.1): non-overlap tiling `Σ⌊T/m⌋` for overlapping-window tools; face value for discrete tools (catch22 = 22; one fixed-penalty ruptures run = 1); mechanism-first = the count of pre-committed hypotheses. K_banked is the program-cumulative K of the axis's instrument family (defaults ADR #2: abandoned campaigns still bank; GC/MGC currently banks **3,177**; families with no closed manifest bank 0).
- **floor(K) = min annualized Sharpe clearing DSR ≥ 0.95 at (K, V = 1/n)** — computed exactly by the Q-GATECART-1 §B S_floor method (production `lab/research_utils/deflated_sharpe.py`: scan annualized SR upward; per-trade SR = SR_ann/√(252·f); n = 252·f·6.5y; most-permissive across f ∈ {0.5, 1, 2, 4}/day; Gaussian moments). Reproduced this session to the published table: K=1→0.65 · 3→0.98 · 30→1.46 · 100→1.64 · 300→1.79 · 441→1.83 · 3,177→2.05 · 10k→2.17.
- **Ceiling = the frozen Q-GATECART-1 realism band, inherited by citation, NOT re-derived.** S_B = 0.85 (corrected top-decile net single-strategy; median 0.3–0.5); S_A = 1.83 (Aegis, gross/friendlier-venue upper bound). **Cap RESOLVED 2026-07-14 at 1.0** ([`Q-GATECART-1 pre-reg §F`](../../ltm/briefs/pre-registration/Q-GATECART-1-verdict-preregistration.md), "Cap (resolved)" row) — the divergence branch's "not a blind max" instruction forecloses the S_A-anchored rung once S_A's inflation is diagnosed as dominant (confirmed in §F's own gap interpretation), and the frozen text supplies no blending mechanism to land anywhere between, leaving S_B's rung (smallest grid rung ≥ 0.85 = 1.0) as the sole surviving anchor. **Per this §B's own pre-committed branch-completion clause (below), the three-band design degenerates to two now that the Cap is resolved:**
  - **PASS:** floor(K_eff) ≤ 1.0. Boundary: **K_eff ≤ 3.**
  - **FAIL:** floor(K_eff) > 1.0 (K_eff > 3). (DISC-CAMP-0-class wide mining at K=3,177 lands here — the retrodiction kill — as does any design above ~3 pre-committed hypotheses.)
- **Consequence flagged, not softened:** at Cap=1.0, Clause K admits only axes expressible as ≤3 non-overlapping pre-committed hypotheses (mechanism-first, near-K=1 designs). This is a real, verified structural tightening — confirmed by the same adversarial workflow that resolved the Cap, which tried and rejected loosening the Cap to preserve a wider PASS band as circular under Q-GATECART-1 §A ("tuning the cap to [a downstream screen's] convenience"). The tightness is consistent with, not contradictory to, M-19 ("≤ typical-anomaly quality (~1.0) needs K ≤ 3") — it is the finding, not a screen defect to patch.
- Report per axis, alongside the PASS/FAIL verdict: the **required-quality percentile context** (floor vs S_B median 0.3–0.5 / top-decile 0.85), so a PASS is read as "requires a top-decile-or-better edge to demonstrate," not as cheap.

### Clause N — confirm-gate power at the axis's available panel

- **P(primary confirm clause passes | mechanism/effect genuinely true) ≥ 0.50**, the §R precedent threshold (Q-HARV-1: joint 5–6% ⇒ DECLINE; H1 power ~24–30% ⇒ unreachable).
- Computed coarse-by-design (screen tier): normal approximation, power = Φ(√N·|δ|/σ − z_α), with α = the campaign-default primary bar (two-sided p ≤ 0.05 ⇒ z ≈ 1.96 unless the axis declares a ratified alternative), **N = the full declared OOS event count** (generous), **δ = the cohort-cited central (not top-of-range) plausible-true effect**, σ from the same cited cohort. Where the axis's confirm design is not event-study-shaped, the nearest analytic analogue is used and recorded on the axis's screen row.
- **Effect priors must be cohort-cited** (in-house measured value where one exists, e.g. HARV's +13 bp; else literature median with citation). **No citable prior ⇒ the axis is UNSCREENABLE on Clause N** — routed per §D, never patched with an invented number (metric-cohort provenance binding; rescope ADR §5 discipline).

## §C — Inventory, ranking, and screen mechanics (frozen)

- **Inventory:** assembled in Phase 1 from the named sources (parent brief §7) and **operator-ratified before any axis is screened.** Each entry declares: instrument family (→ K_banked), search-design class + coarse tool ladder (→ K_intrinsic), OOS era + expected event rate (→ N), cohort-cited effect prior + σ (→ Clause N) or an explicit UNSCREENABLE flag with the missing input named.
- **A screen PASS is void if the eventual campaign's `register_search open` binds a K exceeding the declared K_eff band** — the declaration is the commitment; the manifest is the enforcement point.
- **Ranking (frozen):** PASS axes first (ascending floor); Clause-N power descending as tiebreaker. FAIL and UNSCREENABLE axes listed below the line with reasons — visible, never silently dropped.

## §D — Verdict gate (binary; verbatim in parent §6)

| Verdict | Trigger | Disposition |
|---|---|---|
| **RESOLVED** (fundable set non-empty) | ≥1 ratified-inventory axis PASSES Clause K (floor(K_eff) ≤ 1.0, i.e. K_eff ≤ 3) **and** clears Clause N | Ranked slate → 08-08 packet as pre-assembled axis-selection evidence; each funded axis proceeds to campaign scoping under the standing HARD gates |
| **FALSIFIED** (fundable set empty) | Every screened axis fails ≥1 clause at the frozen anchors, and no axis is UNSCREENABLE | Surface to operator **before** any new campaign pre-registers: the 11-08 §4 falsifier is a-priori unreachable via newly-started discovery; options (accept research-only demotion risk / re-scope 11-08 via its own ADR) are the operator's — ceiling re-derivation, if any, only via Q-GATECART-1-successor close-and-reopen |
| **AMBIGUOUS-HOLD** | All screened axes fail, but ≥1 axis is UNSCREENABLE (verdict flips depending on it) | Hold; name the missing input per unscreenable axis (usually a cheap scoping probe for an effect prior); re-screen when supplied or at 2026-08-08, whichever first |

**Branch exercised 2026-07-14** (before any axis was screened, per this section's own precondition): the operator resolved the Q-GATECART-1 Cap to 1.0, so Clause K's output degenerated from the drafted three-band form to the two-band PASS/FAIL form used throughout §B/§D above — a pre-committed branch completion, not an amendment (§B and §D above reflect the collapsed form directly; this line records that the branch fired and when).

## §E — Results annex (filled at Phase 2, 2026-07-14 — after the freeze commit `b304f2c` and the inventory-ratification anchor `ca02030`; harness `lab/archive/q_kbudget_1_2026-07/floor_scan.py`)

| Axis | Family | K_intrinsic | K_banked | K_eff | floor | Band | N | δ, σ (citation) | Power | Screen |
|---|---|---|---|---|---|---|---|---|---|---|
| D1 GC/MGC successor (any design) | GC/MGC | ≥1 | 3,177 | ≥3,178 | 2.05 | FAIL | — | — | — | **FAIL (K)** |
| D2 wide mining, other GLBX family | ES/NQ/YM | 10³–10⁴ (tiling) | ≤1 | 10³–10⁴ | 1.93–2.17 | FAIL | — | — | — | **FAIL (K)** |
| D3 HARV-class ES month-end mechanism | ES | 1–2 | 1 | 2–3 | 0.85–0.98 | PASS | ~100 monthly 2018+ | +13–19.2 bp (HARV-0 cohort) | 0.24–0.30, joint 0.05–0.06 (inherited, Q-HARV-1 §R `9bddd33`) | **FAIL (N, inherited)** |
| D4 XAU T3b swap-dealer COT (prop expr = GC/MGC) | GC/MGC | 1–2 | 3,177 | ≥3,178 | 2.05 | FAIL | ~10³ weekly | no citable δ (4-bar partial) | — | **FAIL (K; N-moot)** |
| D5 NQ/MNQ intraday-momentum footprint (was: gamma-positioning) | MYM/MNQ | 1–3 | 0 | 1–3 | 0.65–0.98 | PASS | ~10³ daily | Baltussen et al. 2021 *JFE* NQ cohort δ/σ=0.113 ([`d5_clause_n_rescreen.md`](../../../lab/archive/q_kbudget_1_2026-07/d5_clause_n_rescreen.md)); confirm-construct = **intraday-momentum footprint** (operator-ratified 2026-07-15); DJ30 drop/down-weight; gamma-sign construct declined (no NDX/Dow cohort) | 0.947 | **PASS (K+N) — ratified 2026-07-15** |
| D6 eurusd_pattern_enum Phase-4 | 6E/EURUSD | 450 (locked harness) | 0 | 450 | 1.835 | FAIL | — | — | — | **FAIL (K, declared)** |
| D7 JPY month-end mechanism (6J expr) | 6J | 1–3 | 0 | 1–3 | 0.65–0.98 | PASS | ~10² monthly | +13 bp / σ≈90 bp per monthly event — HARV class-analogue, cited per §B's "nearest analytic analogue" provision (Q-HARV-1 §R, `9bddd33`); no non-circular JPY-native δ exists (see [`lab/archive/q_kbudget_1_2026-07/d7_clause_n_screen.md`](../../../lab/archive/q_kbudget_1_2026-07/d7_clause_n_screen.md)) | 0.30 (< 0.50) | **FAIL (N, class-analogue) — screened 2026-07-15** |

**Verdict fired (§D): RESOLVED (2026-07-15)** — D5 PASSES both clauses after operator confirm-construct ratification (intraday-momentum footprint). Screened FAIL: 6/7 · PASS: 1 · UNSCREENABLE: 0. `floor_scan.py` reproduces. Screen PASS licenses campaign scoping only — HARV HARD gate (§R reachability) + DSR-K power disclosure + net-of-cost Sharpe vs Clause-K floor 0.65–0.98 still bind before `register_search open`. Closure: [`docs/briefs/closures/Q-KBUDGET-1-axis-reachability-screen.md`](../closures/Q-KBUDGET-1-axis-reachability-screen.md).

## §F — Audit hooks (runnable)

```bash
# 1. Freeze ordering: this file's ratified commit predates any Phase-2 screen artifact.
git log --format='%h %ci' -- docs/briefs/pre-registration/Q-KBUDGET-1-screen-preregistration.md | tail -1
git log --format='%h %ci' -- lab/archive/q_kbudget_1_2026-07/ 2>/dev/null | tail -1   # must be LATER (or absent pre-Phase-2)

# 2. §B byte-stability vs the freeze commit (Trap-12 guard).
git diff <freeze_hash> -- docs/briefs/pre-registration/Q-KBUDGET-1-screen-preregistration.md | grep -A2 '## §B' && echo "CHANGED — investigate" || echo "stable"

# 3. Reproduce the floor table + band boundaries on the production module (pure arithmetic):
python -c "
import sys, math; sys.path.insert(0, 'lab')
from research_utils.deflated_sharpe import expected_max_sharpe, deflated_sharpe
def floor_at_K(K, years=6.5, freqs=(0.5,1,2,4), t=0.95):
    best=None
    for f in freqs:
        n=int(round(252*f*years)); sr0=expected_max_sharpe(K,1.0/n); s=0.01
        while s<6.0:
            if deflated_sharpe(s/math.sqrt(252*f), n, 0.0, 3.0, sr0)>=t: break
            s+=0.005
        best=s if best is None else min(best,s)
    return round(best,3)
print([ (K, floor_at_K(K)) for K in (1,3,441,2038,3177) ])"
# Expect: floors ≈ 0.65 / 0.98 / 1.83 / ≤2.00 / 2.05

# 4. Anchors inherited, not re-derived: S_A/S_B cited from the GATECART pre-reg §F (freeze 453148a).
grep -n "S_A (max leg annualized Sharpe)\|S_B (top-decile" docs/ltm/briefs/pre-registration/Q-GATECART-1-verdict-preregistration.md
```
