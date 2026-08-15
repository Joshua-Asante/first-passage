# Pre-registration — Class-S existing-strategy book candidate #1: 2-leg MYM+MNQ native-futures book

**Status:** `FROZEN` (operator signed §9, 2026-07-15). No item below changes after
signature or after any frozen-tier result is seen (Known Trap #12 — amendments require
closing this candidate and opening a fresh one under the ADR's early-fail / per-candidate
governance).
**Candidate class:** pre-registered existing-strategy book (Class S), admitted by
[`docs/adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md`](../../adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md) (`Accepted` 2026-07-15).
**Gate of record (unchanged, cited not re-decided):**
[`2026-07-13-prop-survivor-scoring-prereg.md`](2026-07-13-prop-survivor-scoring-prereg.md) (FROZEN 2026-07-13).
**Aegis declaration (ADR §5, explicit):** **this candidate contains NO Aegis leg.** The
Aegis prop panel-of-record is nonetheless resolved — operator pinned **ae744** +
decompound `full_stop_mean` 1R **$2,912.96 (n=11)** on 2026-07-15
([`PANEL_OF_RECORD.md`](../../../lab/analysis/aegis/aegis_6j_transfer_2026-07-05/PANEL_OF_RECORD.md)) —
so an Aegis-bearing candidate #2 is unblocked and requires only its own pre-registration
+ operator decision. No sequencing shortcut is being taken.
**Loop of record:** STRATEGIC.
**Feeds:** the four-firms ADR §4 primary falsifier (hard date **2026-11-08**; 08-08
progress check), via the frozen survivor-scoring gate.
**Authored:** 2026-07-15 · Claude Code (Fable 5), operator-directed ("help me make these
two decisions"; SESSIONS 2026-07-15 open item (a)).

---

## §0 — Rule-0 reads (production source, verified this session 2026-07-15)

All content-read from the working tree on branch `claude/operator-class-s-decisions-071750`;
per-file anchors (`git log -1`):

- **[`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`](2026-07-13-prop-survivor-scoring-prereg.md) @ `be6dda6`** —
  read in full. Part A **bust ≤ 3.0%** (daily+static+trailing via
  `preflight.summarize_outcomes`) **+ P(pass) ≥ 50%** with finite median inside horizon,
  **Run-2 gated**, frozen cross-section exactly `Bulenox_100K · Tradeify_Select_100K ·
  MFFU_Rapid_100K · BluSky_Premium_100K`; discharge = **≥2 distinct firms incl. ≥1
  `trailing_locking`**; F2 optimistic-lower-bound labels on Bulenox/BluSky; seeds
  **42/123/2026**, 10k × 3, horizon 1500, inactivity disabled, `dd_protection` default
  OFF (§7(6)); §7(9) non-candidate calibration reference owed. **Nothing here re-decides
  any of it.**
- **[`docs/adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md`](../../adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md) @ `507761a`** —
  `Accepted` 2026-07-15. Claim separation (§2: native-book bust-geometry, never CFD-edge
  transfer; R5/P2 stay FALSIFIED); per-candidate pre-registration + prior-look disclosure
  required; **early-fail branch** (§4): first candidate failing Part A on **all four**
  tiers ⇒ any second candidate needs fresh operator authorization.
- **[`lab/analysis/c1/tradeify_futures3_bustcut_2026-07-11/RESULTS.md`](../../../lab/analysis/c1/tradeify_futures3_bustcut_2026-07-11/RESULTS.md) @ `eba5030`** —
  Test 1 (this candidate's direct prior): 2-leg MYM+MNQ, 50K geometry-only, **pass 99.24%
  / bust 0.76% / p99 3.86% / med 222d**; plus T2/2b/2c Aegis variants (§7 table).
- **[`lab/analysis/c1/tradeify_futures3_remc_2026-07-11/RESULTS.md`](../../../lab/analysis/c1/tradeify_futures3_remc_2026-07-11/RESULTS.md) @ `eba5030`** —
  panel construction of record (decompound static $200K via roe; `pin_r_basis(full_stop_mean)`):
  striker 1R **$2,535.61 (n=8)** scale 0.5521; striker_nas100 1R **$5,899.32 (n=19)**
  scale 0.1254; panel 2020-01-06 → 2026-06-30/07-01; 3-leg 50K→100K deterioration
  10.33% → 17.70% (the ×1.71 coarse factor used, non-bindingly, in §1).
- **[`lab/archive/tradeify_selectflex_remc_2026-07-10/`](../../../lab/archive/tradeify_selectflex_remc_2026-07-10/) @ `47cc3eb`**
  (`RESULTS_tradeify_integer_2026-07-10.md` + `NOTES.md`) — the 2-strat MYM+MNQ
  **integer-micro** arm (C5 sizing, CFD-host panels, 1R striker $4,229 / nas $3,940):
  100K bust **0.80%** at $0 cost ↔ **4.59%** at the superseded $2.22/ctr RT proxy; the
  verified **$1.82** re-run was **operator-stopped 2026-07-10 — UNRESOLVED**; study
  disposition FALSIFIED (vs the then-applied bust<1% gates). Disclosed as §7 look #7.
- **[`lab/analysis/aegis/aegis_6j_transfer_2026-07-05/PANEL_OF_RECORD.md`](../../../lab/analysis/aegis/aegis_6j_transfer_2026-07-05/PANEL_OF_RECORD.md) @ `507761a`** —
  operator pick block filled (ae744; 5274c disqualified on the 1R median-fallback defect);
  §3 guard proposal (1R fallback / thin-cohort hard-fail at the scoring-adapter boundary)
  — adopted as a binding run condition here (§8.3).
- **`core/firm_rules.py` @ `a53ee99`** — all four frozen tier configs present
  (`Bulenox_100K` L102 / `Tradeify_Select_100K` L227 / `MFFU_Rapid_100K` L286 /
  `BluSky_Premium_100K` L336); `ACTIVE_FIRM="FXIFY"` untouched; per-firm
  `cost_per_side_usd` + `consistency_rule_pct` (Tradeify 40 / MFFU 50 / BluSky 34;
  Bulenox none at eval) present.
- **`lab/discovery/prop_survivor_scoring.py` @ `97011c1`** — `score_candidate()` (L427)
  accepts pre-built scaled arrays; **no 1R guard exists on this path** (caller
  responsibility — hence §8.3).
- **`ops/prop_envelope_default.md` @ `6b94032`** — §2 contract: pre-register the
  deployable decomposition + frozen binary `DEPLOYABLE-DEFAULT-ENVELOPE` criterion;
  consistency annotation; excursion reporting; exposure-coordinates annotation (§2.5).
- **Panel bytes** — `core/data/tv_exports/cme/SHA256SUMS` (verified this session):
  `9acfa297…ce01b9e *Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-11_15d8b.csv`;
  `8884e6dd…dc6419 *Striker_NAS100_v1_CME_MINI_MNQ1!_2026-07-11_beabf.csv`.

---

## §1 — Context + composition decision record

The amendment ADR is `Accepted` and its Phase-2 Aegis mechanical (panel-of-record pick)
cleared 2026-07-15. The open step it names: "First Class-S candidate pre-reg is now the
open step." Three book axes were inventoried (Q-KBUDGET-1 Phase-1 inventory §3, `1417b79`):
S1 (3-leg, Aegis ~0.75%-class), S2 (2-leg MYM+MNQ), S3 (Aegis solo).

**Candidate #1 = S2 (2-leg MYM+MNQ), chosen on prior-look arithmetic, recorded here so
the selection is auditable:**

- The discharge rule requires **≥1 `trailing_locking` firm** to clear Part A. The only
  measured 50K→100K deterioration factor on this panel family is ×1.71 (3-leg:
  10.33% → 17.70%). Applied coarsely: S2 0.76% → **≈1.3%** (Run-2 ≈1.5%) — inside the
  3.0% ceiling with ~2× headroom; S1 (bustcut 2b) 2.02% → **≈3.5%** (Run-2 ≈3.6%) —
  *above* the ceiling on exactly the geometry the discharge rule requires. S3 has no
  `trailing_locking` prior at all.
- The ADR's early-fail branch makes candidate #1's failure mode expensive (all-four-tier
  fail ⇒ fresh authorization needed for any second candidate). Leading with the
  highest-headroom book is the K-honest sequencing; S1 remains available as candidate #2
  either way, and its Aegis input (ae744 pin) is already resolved.
- **These extrapolations are coarse and non-binding — the G4 run adjudicates.** They are
  recorded to show the selection used only already-disclosed prior looks (§7), not any
  peek at the frozen surface (the $100K×4 cross-section has never been run for any S-book).

**Claim (ADR §2 claim-separation, restated):** this candidate claims **native-book
bust-geometry at the frozen firm tiers** — panels as measured on CME/CBOT micros, TV-modeled
costs included. It does **not** claim CFD-edge preservation; R5/P2 stay FALSIFIED and this
artifact must never be cited against them.

---

## §2 — The candidate (FIXED — the entire variant set is this one book)

| Item | Fixed value |
|---|---|
| Book | 2 legs: Striker DJ30 v4.5 → **MYM**; Striker NAS100 v1 → **MNQ**. **No Aegis leg. No other leg.** |
| Panels (bytes pinned) | `Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-11_15d8b.csv` (sha256 `9acfa29726a9530d2a3de5fc2290cc67672441fac2c805defd524677cce01b9e`, N=267) · `Striker_NAS100_v1_CME_MINI_MNQ1!_2026-07-11_beabf.csv` (sha256 `8884e6dd56c786e1e59a8ab0b962a70be82f34e06af26a9582554c9f8ddc6419`, N=284) |
| Panel window | 2020-01-06 → 2026-06-30 (1692 bdays) |
| Construction | Decompound static @ $200K via roe → `pin_r_basis(full_stop_mean)` → scale to per-leg risk (identical to the futures3/bustcut construction — **zero new variants**) |
| 1R pins (expected; §8.3 asserts) | striker **$2,535.61 (n=8)** → scale 0.5521 · striker_nas100 **$5,899.32 (n=19)** → scale 0.1254 |
| Per-tier weights (venue variables) | striker **0.70%** · striker_nas100 **0.37%** per trade. These are `(portfolio, firm-tier)` venue variables in the dd-geometry concept-not-constant sense; they are numerically equal to the locked CFD risk values **because that is what every prior look measured** — re-weighting would mint a fresh variant and orphan the §7 disclosure. This is not a deployment of the locked four-strategy CFD book (2 legs, futures venue, futures panels). |
| dd_protection overlay | **OFF** (`NO_PROTECTION_TRIGGER`), per gate §7(6). No tuned `(trigger, scale)` grid is registered for this candidate. |
| Engine params | 10,000 sims × seeds **42/123/2026**; horizon **1500**; inactivity disabled; tiers threaded via `preflight.firm_kwargs` (never module constants; `ACTIVE_FIRM` untouched) |
| Runs | Run-1 (consistency-off) + Run-2 (consistency-on) for Tradeify (40%) / MFFU (50%) / BluSky (34%); Bulenox has no eval consistency → its single run gates. **Part A reads Run-2 wherever consistency exists.** |
| Tiers | Exactly the four frozen: `Bulenox_100K` · `Tradeify_Select_100K` · `MFFU_Rapid_100K` · `BluSky_Premium_100K`. All other tiers, if printed, are diagnostics only. |

**Deployable vs research expression (envelope §2.1):** they coincide for this book — the
TV exports are already EOD-flat per-session (0% overnight holds; Tradeify force-flat
noted in the remc run), inside the E1 16:00 ET build target (binding min MFFU 16:10 ET).
The known residual gap to live execution is **integer-micro granularity + verified
per-contract costs** (disclosed as §7 look #7, UNRESOLVED bracket); the scaled %-equity
panel above is the G4 form of record, and granularity/cost sensitivity is reported at
G7 as a diagnostic, never swapped in as a post-hoc gate form (§5).

**`DEPLOYABLE-DEFAULT-ENVELOPE` criterion (frozen, binary; annotated YES/NO at closure):**
per-leg gross edge per round trip ≥ **4×** the per-firm RT cost (`2 × cost_per_side_usd`
from `core/firm_rules.py`) at the deployable expression's measured round-trip count
`R_deploy` (G1 output, pyramid entries counted as fills).

**Envelope §2 emissions at G1 (computed from panel bytes, declared at closure; describe,
never filter):** `R_deploy` + deployable/research expectancy ratio (expected ≈1.0 —
expressions coincide); consistency annotation (trade frequency ≈551 trades/6.5y,
P&L-bearing days/yr + expected max-day profit share); per-trade excursion stats vs E3
intraday-trail posture; exposure coordinates {side; entry session windows (ET);
in-market minutes/yr; MYM×MNQ structural overlap = simultaneous-in-market minutes/yr ×
sign-agreement}.

---

## §3 — Calibration-reference registration (gate §7(9) rider — non-candidate)

The frozen gate owes one pre-registered **non-candidate** calibration reference. Registered
here, before any frozen-tier result is seen: **the 3-leg native full-Aegis book exactly as
run in futures3 remc** (ae744 @ 1.50% + MYM 0.70% + MNQ 0.37%, same construction) — the
falsified-book quality the 3.0% ceiling was explicitly calibrated to exclude (known prior:
Tradeify_Select 100K geometry-only 17.70%; its other three frozen cells are unseen). It is
run once through the identical §2 harness. Per the gate's §4/§6: **if it clears 3.0% on ≥2
tiers, the ceiling fails to discriminate** → the gate closes AMBIGUOUS and the ceiling is
re-derived in a fresh brief; this candidate's result is then quarantined with it. The
reference is not a candidate, cannot discharge anything, and its result is reported in the
same session as candidate #1's scoring.

---

## §4 — Falsifiable hypothesis (H-C1; binary)

**H-C1 — if** the §2 book clears Part A (**bust ≤ 3.0%** by `summarize_outcomes`
daily+static+trailing **and P(pass) ≥ 50%** with finite median ≤ 1500d), Run-2 where
consistency exists, on **≥2 of the four frozen tiers including ≥1 `trailing_locking`**
(Tradeify_Select_100K or MFFU_Rapid_100K), **then** the four-firms ADR §4 falsifier is
**discharged** and the candidate routes to G8 (lifecycle CANDIDATE @ 1.00×, carrying the
G1 envelope annotations; decay monitoring rides the existing lifecycle Call-1 machinery) —
rail build, account registration, and go-live stay separately gated, a cleared candidate
produces falsifier evidence and an intake, nothing more; **otherwise** H-C1 is falsified
for this candidate and it **closes** (no iteration in place), disposition per §6.

**Reject/accept thresholds (restated numerically):** accept iff, on ≥2 frozen tiers with
≥1 `trailing_locking`, Run-2 headline bust ≤ 3.0% AND P(pass) ≥ 50% AND median ≤ 1500d;
reject on any other pattern of per-tier results.

---

## §5 — Forbidden moves (each genuinely tempting)

- **Swapping the panel form after a marginal Run-2 result** — to integer-micro sizing (the
  $0-cost bracket point reads 0.80%) if the %-equity form fails, or away from it if
  granularity diagnostics look bad. The §2 form is fixed; a sizing-model change is a NEW
  candidate requiring its own pre-registration + operator decision.
- **Re-weighting 0.70/0.37 after seeing per-tier results** — gate-layer tuning; the ADR
  names it; a failed candidate closes.
- **Adding the Aegis leg mid-stream because the ae744 pin now exists** — that is candidate
  #2 (S1), own pre-registration, own operator decision.
- **Citing MYM/MNQ absolute PF (~2) against P2 edge-transfer** — the temptation the moment
  a tier clears. P2 measured ratio-to-CFD and stays FALSIFIED; this candidate's claim is
  bust-geometry only.
- **Counting a Bulenox+BluSky-only pair as discharge** — F2 optimistic-lower-bound
  geometry; the ≥1 `trailing_locking` clause is frozen.
- **Reading `compute_default_config()['bust_rate']` for any tier** (F1) — headline bust
  comes from `preflight.summarize_outcomes` only.
- **Running any frozen-tier G4 cell before the §9 signature lands** — the prior 50K looks
  are visible and the temptation to "just peek at one tier" is real; an unsigned run
  voids this pre-registration.

---

## §6 — Gate criteria (binary dispositions)

| Verdict | Trigger | Disposition |
|---|---|---|
| **RESOLVED** (H-C1 holds — DISCHARGED) | Part A on ≥2 frozen tiers incl. ≥1 `trailing_locking` | ADR §4 falsifier discharged; candidate → G8 admission (lifecycle CANDIDATE @ 1.00×); rail/account/go-live still gated |
| **FALSIFIED — partial (NOT-DISCHARGED)** | Clears Part A on ≥1 tier but the discharge rule is unmet (e.g. a trailing-only pair, or exactly one tier) | Candidate closes; per-tier evidence recorded toward 11-08; any next candidate = normal ADR per-candidate operator decision (early-fail branch NOT triggered) |
| **FALSIFIED — early-fail** | Fails Part A on **all four** frozen tiers | Candidate closes; ADR §4 early-fail branch arms — any second candidate requires fresh operator authorization |
| **AMBIGUOUS (gate-level)** | The §3 calibration reference clears 3.0% on ≥2 tiers | Ceiling-mis-set per the frozen gate §4/§6: gate closes; ceiling re-derived in a fresh brief; this candidate's result is quarantined (neither discharge nor early-fail is asserted from a non-discriminating ceiling) |

Regime-robustness rider (gate §7(7)): before the DISCHARGED verdict is *trusted* into G8,
run the regime gate (6mo block bootstrap + half-panel split per
`docs/methodology/regime_robustness_gate.md`) on this book's scaled panel; a both-halves
FAIL does not overturn the mechanical Part A read but is reported alongside it and rides
into the G8 intake as a standing caveat.

---

## §7 — Prior-look disclosure (complete; the ADR's condition for this artifact)

All looks on this panel family / book-composition layer, in date order. The frozen
$100K×4 cross-section has been run for **no** S-book; of the four frozen cells for this
candidate, all four are unseen (the 07-10 integer arm's 100K cells were a different
sizing model + panel source; the 07-11 native looks were 50K only).

| # | Date | Run (path) | Book / form | Numbers seen |
|---|---|---|---|---|
| 1 | 07-10 | selectflex %-equity arm (`lab/archive/tradeify_selectflex_remc_2026-07-10/`) | 3-strat, CFD-host DJ30+NAS + 6J prototype, %-equity | Tradeify geom 25K 7.57% / 50K 7.40% / 100K 13.37% / 150K 13.29% (p99 4.86/4.89/4.51/4.52) |
| 2 | 07-10 | selectflex integer arm, $0-cost bound (same archive) | **2-strat MYM+MNQ**, C5 integer sizing, CFD-host panels, 1R $4,229/$3,940 | 25K 0.06% / 50K 0.09% / **100K 0.80%** / 150K 0.92% |
| 3 | 07-10 | selectflex integer arm, $2.22/ctr RT proxy (same) | same | 25K 1.05% / 50K 1.11% / **100K 4.59%** / 150K 5.02% — integer sizing read LOWER than %-equity at same cost (100K 4.59% vs 7.04%, `NOTES.md` L68) |
| 4 | 07-10 | selectflex integer arm @ verified $1.82 — **operator-stopped, never completed** | same | **UNRESOLVED**: 100K bracket 0.80% ↔ 4.59%; NOTES notes $1.82 sits 82% of the way toward the $2.22 proxy |
| 5 | 07-11 | futures3 remc (`lab/analysis/c1/tradeify_futures3_remc_2026-07-11/`) | 3-leg native (ae744 @ 1.50% + MYM + MNQ) | Tradeify geom 25K 10.58% / 50K 10.33% / **100K 17.70%** / 150K 17.61%; +40% consistency 10.83/10.56/17.88/17.79 |
| 6 | 07-11 | bustcut Test 1 (`lab/analysis/c1/tradeify_futures3_bustcut_2026-07-11/`) | **THIS candidate** (2-leg native, %-equity) | **50K geom: bust 0.76%, pass 99.24%, p99 3.86%, med 222d** |
| 7 | 07-11 | bustcut Test 2 | 3-leg, 5274c @ 0.75% (spurious 1R median-fallback, scale ~9×) | 50K 39.43% (artifact; 5274c since disqualified) |
| 8 | 07-11 | bustcut 2b | 3-leg, **ae744 @ 0.75%** (= S1's direct prior) | 50K 2.02%, p99 4.10%, med 152d, Aegis attr 47.8% |
| 9 | 07-11 | bustcut 2c | 3-leg, 5274c @ 0.75% size-adj (1R $1,869) | 50K 1.28% |

**Freeze-order transparency (inventory §3 note, carried forward):** the 3.0% ceiling was
frozen 2026-07-13, *after* rows 1–9 were visible. The ceiling's rationale is structural
(barrier width; excludes row-5's falsified-book quality) and the operator declined dial
adjustments — but selection-on-prior-looks is hereby on the record: candidate #1 was
chosen *because* row 6 is the strongest prior. That is exactly what this disclosure
exists to make legible.

**K accounting:** composition-layer variants examined to date ≈ 8 (rows above, ex-artifact
row 7 counted once with its correction 2c). This candidate adds **zero** new variants —
it is row 6's book re-run on the unseen frozen surface. Class S is routed
out-of-screen-scope (inventory §6.2): no DSR/Clause-K claim is made or needed; the gate
of record has no DSR clause.

---

## §8 — Run protocol (G0–G8 mapping)

1. **G0 intake:** this artifact + §9 signature.
2. **G1 (E1 reduction + envelope emissions):** confirm EOD-flat per-session from panel
   bytes (expect 0% overnight holds); emit `R_deploy`, expectancy ratio,
   consistency/excursion/exposure annotations (§2). Emit
   `DEPLOYABLE-DEFAULT-ENVELOPE: YES/NO` per the frozen §2 criterion at closure.
3. **G2 (cost-law kill gate) + 1R guard:** per-leg gross-edge ≥ 4× RT cost at `R_deploy`
   (per-firm `cost_per_side_usd`). **Binding adapter guard (PANEL_OF_RECORD §3, adopted):**
   the scoring adapter hard-fails if `pin_r_basis` returns a FALLBACK method or n<5
   full-stops for either leg — expected striker n=8 / nas n=19; a violation means the
   panel bytes changed and the run STOPS (`NEEDS_CONTEXT`), it does not proceed on a
   different 1R basis.
4. **G3:** `preflight.assert_engine_ready` GREEN on all four tiers before any sim.
5. **G4:** the §2 engine params, four frozen tiers, Run-1 + Run-2. The §3 calibration
   reference runs in the same session, same harness.
6. **G5:** Part A read per tier via `summarize_outcomes` (Run-2 where consistency
   exists); §6 verdict assigned mechanically.
7. **G6:** candidate #1 scores STANDALONE (no companion book exists yet).
8. **G7 (diagnostics, never §4-gating):** funded-geometry ruin read; integer-micro
   granularity + verified-cost ($0.91/side Tradeify-class) sensitivity note against the
   row-2/3/4 bracket.
9. **G8 (only from DISCHARGED):** lifecycle CANDIDATE @ 1.00× intake with annotations +
   regime-gate rider caveat if any.

Results land in `lab/analysis/` under a dated slug; the RESULTS header must cite this
pre-registration **and** the frozen gate pre-registration by path (gate §10 hook 6).

---

## §9 — Operator signature (the ADR §4 per-candidate decision; DRAFT until filled)

```
SIGNED / FROZEN: 2026-07-15 / JA
Authorized as Class-S candidate #1 under ADR 2026-07-14 (Accepted 2026-07-15).
Composition: 2-leg MYM+MNQ (no Aegis leg) — §2 fixed as drafted.
No frozen-tier G4 cell may run before this block is filled.
```

---

## §10 — Audit hooks (runnable)

```bash
# 1. Signature-before-run: confirm §9 is signed (not the placeholder), and that no G4
#    results exist yet if this hook is run before the scoring session.
grep -n "SIGNED / FROZEN: 2026-07-15 / JA" docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-1-prereg.md \
  || echo "VIOLATION: signature block not in expected signed form"

# 2. Variant-set immutability: the fixed weights/seeds/1R pins never edited post-freeze.
grep -n "0.70%\*\* · striker_nas100 \*\*0.37%\|42/123/2026\|2,535.61\|5,899.32" \
  docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-1-prereg.md

# 3. Panel bytes unchanged since registration.
grep -n "15d8b\|beabf" core/data/tv_exports/cme/SHA256SUMS   # expect the two pinned hashes

# 4. The no-Aegis declaration is explicit (ADR §5 requirement).
grep -n "contains NO Aegis leg" docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-1-prereg.md

# 5. ADR §10 filename hook matches (existing-strategy | book-candidate).
ls docs/briefs/pre-registration/ | grep -i "existing-strategy\|book-candidate"

# 6. The scoring session cites both pre-registrations (Trap #10 guard).
grep -rn "2026-07-15-existing-strategy-book-candidate-1-prereg\|2026-07-13-prop-survivor-scoring-prereg" docs/SESSIONS.md

# 7. R5/P2 never cited-against (claim-separation honesty).
grep -n "FALSIFIED" docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md | head -3

# 8. Calibration reference ran in the same session as candidate #1 (§3).
grep -rn "calibration reference\|17.70" lab/analysis/*/RESULTS*.md 2>/dev/null | grep -i "candidate\|class" || echo "no scoring session yet (expected while DRAFT)"
```

---

## Verification

```bash
# Discipline checks (mechanical)
PYTHONIOENCODING=utf-8 python scripts/check_brief.py \
  docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-1-prereg.md --type inquire

# §0 anchors
git log -1 --format='%h %ci' -- docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md   # be6dda6
git log -1 --format='%h %ci' -- docs/adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md        # 507761a
git log -1 --format='%h %ci' -- lab/analysis/c1/tradeify_futures3_bustcut_2026-07-11/RESULTS.md              # eba5030
git log -1 --format='%h %ci' -- lab/archive/tradeify_selectflex_remc_2026-07-10/                          # 47cc3eb
git log -1 --format='%h %ci' -- core/firm_rules.py                                                        # a53ee99

# Panel bytes
grep -c "15d8b\|beabf" core/data/tv_exports/cme/SHA256SUMS    # expect 2

# Engine pre-flight importable (G3 dependency)
python -c "import sys; sys.path.insert(0,'core'); from mc.preflight import summarize_outcomes, firm_kwargs; print('preflight OK')"
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-15 | Drafted (`DRAFT — awaiting operator signature`); composition S2 selected per §1 record | Joshua (direction) + Claude Code (Fable 5) |
| 2026-07-15 | **Signed / FROZEN** (§9) — operator ratified the S2 recommendation as-drafted, no redraft requested. No item above changed at signature. | Joshua (JA) |
