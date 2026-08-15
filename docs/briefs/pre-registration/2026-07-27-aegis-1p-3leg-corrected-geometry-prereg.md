# Pre-registration — Aegis@1.00% 3-leg corrected-geometry re-MC (DD-geometry question only)

**Status:** `FROZEN` (operator chat directive 2026-07-27 — "Run the fresh pre-registered
Aegis @ 1% test on corrected geometry"; §9 records it verbatim). No item below changes after
any bust number is seen (Known Trap #12 — amendments require closing this pre-registration
and opening a fresh one).
**What this is:** the never-measured **1.00% Aegis arm** bracketed by the 2026-07-11 futures3
looks (1.50% → 10.33%/17.70% bust; 0.75% → 2.02%/1.28%), now run under **corrected**
`trailing_locking` eval geometry with a **fresh native-1% export** (cap-native sizing).
**What this is NOT:** a clearer/§4 run. The cap-feasibility pre-check (§2) fails on every
cell at native sizing, so **no outcome of this run can produce a Part A "clearer" claim** —
the run answers the DD-geometry survival question only.
**Parent gate of record (unchanged, cited not re-decided):**
[`2026-07-13-prop-survivor-scoring-prereg.md`](2026-07-13-prop-survivor-scoring-prereg.md)
(`be6dda6`, FROZEN) — floor bust ≤ 3.0% + P(pass) ≥ 50%, Run-2 (consistency-on).
**Sibling of record:** [`2026-07-24-c1-band-rescore-corrected-geometry-prereg.md`](2026-07-24-c1-band-rescore-corrected-geometry-prereg.md)
(engine, correction idiom, control pins inherited verbatim).
**Loop of record:** STRATEGIC.
**Authored:** 2026-07-27 · Claude Code (Fable 5), operator-directed.

D-S-A domain: data (one pre-declared risk arm on a fixed tier set; no system/framework change).

---

## §0 — Rule-0 reads (production source, verified this session 2026-07-27)

- **`core/firm_rules.py`** — target rows read verbatim this session: `Tradeify_Select_100K`
  (100K, `max_dd_pct` 3.0 = $3,000, target 6%, cap **80 micro-equiv** "8 mini / 80 micro",
  consistency 40, `dd_lock_offset_usd` 100 with the in-file OPEN-DEFECT comment),
  `Tradeify_Select_50K` (50K, 4.0% = $2,000, cap **40**, consistency 40), `MFFU_Rapid_50K`
  (50K, 4.0% = $2,000, cap **50**, consistency 50, `min_trading_days` 2). All
  `dd_type="trailing_locking"`; constant deliberately not hand-edited.
- **[`lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_scoring.py`](../../../lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_scoring.py)** —
  panel construction of record (`build_scaled_panel`: $200K-static decompound via roe →
  `pin_r_basis(full_stop_mean)` → risk%-scale; §8.3 guard: FALLBACK or n<5 hard-fails).
- **[`lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_regime_gate.py`](../../../lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_regime_gate.py)** —
  `run_partition_mc` (Run-2 = consistency-on), `part_b_half_panel`, `part_a_bootstrap`
  (block 126 bd, n=100, seed 20260715) — frozen primitives, called not re-implemented.
- **Correction idiom** — runtime patch `FIRM_RULES[tier]["dd_lock_offset_usd"] = 1_000_000.0`
  (engine's own no-lock value per `tests/core/test_trailing_locking_boundary.py`; **NOT**
  `None`), restore to 100 after — inherited from
  [`lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/remc_g8_discharge_check.py`](../../../lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/remc_g8_discharge_check.py).
- **Published corrected 2-leg pins (controls)** —
  [`lab/analysis/c1/c1_band_rescore_2026-07-24/band_rescore_report.json`](../../../lab/analysis/c1/c1_band_rescore_2026-07-24/band_rescore_report.json):
  `Tradeify_Select_100K` bust **4.74%** / `Tradeify_Select_50K` **1.06%** / `MFFU_Rapid_50K`
  **0.96%** (Run-2, corrected). Rider (same dir): 50K halves PASS, boot-95th 4.54%/4.49% ⇒
  standing regime-fragile caveat.
- **Fresh Aegis export inventory (no-MC, this session)** —
  [`lab/analysis/c1/aegis1p_3leg_rescore_2026-07-27/inventory_aegis1p.json`](../../../lab/analysis/c1/aegis1p_3leg_rescore_2026-07-27/inventory_aegis1p.json):
  Step-0 PASS (15m grid; session 10:15–13:45 ET; Mon/Tue/Wed only; 0 exits later than
  16:45); native full-stop fraction ≈ **1.05%** (confirms native-1% export); 1R pin
  full_stop_mean **$2,163.57 (n=7)**, scale **0.924398** to the 1.00% target; daily-$-std
  at 100K: Aegis@1% **$227** vs 2-leg book **$272** (ratio **0.833** — sub-dominant;
  contrast ORB's 1.61× in Q-COMPOSE-1).
- **[`ops/instruments/6J.md`](../../../ops/instruments/6J.md)** — J5 sizing throttle; 6J
  offered at Tradeify ($3.10/side) + MFFU ($2.56/side), both primary-verified 2026-07-13;
  M6J at **no** FRIENDLY firm; export cost model $1.30/side placeholder.

---

## §1 — Context + the question

The 1.00% Aegis arm was never measured: 1.50% (locked) busted 10.33%/17.70% (50K/100K,
defective geometry, Aegis ~71% of bust attribution); 0.75% gave 2.02%/1.28% (clean
sensitivity arms 2b/2c; the headline Test-2 cell is the known 9× pin-fallback artifact).
The operator has produced a **fresh native-1% export** (cap-12 sizing modeled in-engine,
so the cap-binding non-linearity is captured natively rather than by linear halving of a
1.5% export). Question: **does the c1 2-leg book + Aegis@1.00% survive corrected
`trailing_locking` DD geometry at the decision-relevant tiers?** Symptom-only phrasing:
*the 1% cell of the Aegis-risk bracket is unmeasured under corrected geometry.*

---

## §2 — The test (FIXED)

| Item | Fixed value |
|---|---|
| Book | 3 legs: Striker→MYM **0.70%** + Striker→MNQ **0.37%** (byte-pinned panels `15d8b`/`beabf`, 1R pins 2535.61/n8/scale 0.5521 + 5899.32/n19/0.1254) + **Aegis→6J @ 1.00%** from `Aegis_6J1_CME_6J1!_2026-07-27_ac331.csv` sha256 `cbf57ac2…e848f`, 1R pin **$2,163.57/n7/scale 0.924398** (frozen from the no-MC inventory; drift > $0.50 or n≠7 at run time = HALT). |
| Panel | Frozen harness idiom: $200K-static decompound (roe) per leg → risk%-scale → union-bday panel. 3-leg span ≈ 2020-01-06→2026-07-15 (Aegis contributes nothing before 2020-07-27 — front-truncated export, disclosed; ae744 panel-of-record starts 2020-02-24). |
| Tier set | **Exactly three scored cells:** `Tradeify_Select_100K` (live c1 account) · `Tradeify_Select_50K` · `MFFU_Rapid_50K` (the two corrected Part A clearers whose headroom an Aegis add would consume). |
| Controls | 2-leg reproduction at all three tiers vs published pins **4.74% / 1.06% / 0.96%**, tolerance ±0.15pp each. T-100K control miss ⇒ harness defect, **no verdict**. |
| Geometry | CORRECTED on all scored+control tiers: `dd_lock_offset_usd → 1_000_000.0`, restore to 100 after. |
| Arm | **One gating arm: 1.00×** book basis (tier daily = `panel_200k.sum × bal/200K`). No 0.50× arm this pass. |
| Partitions | **Full panel = the gating partition.** H1/H2 (bday-midpoint halves) reported as diagnostics on all scored cells. Bootstrap (n=100, block 126 bd, seed 20260715) runs **only** for cells whose full-panel floor passes (band-rescore precedent), diagnostic. |
| Cost arm (diagnostic, non-gating) | **COST-TRUE:** Aegis-leg trade P&L reduced by `(3.10 − 1.30) × 2 × qty` per trade (Tradeify 6J actual vs modeled placeholder; worst of the two firms) before decompounding; full-panel only, all three tiers. |
| Engine | Frozen: `run_partition_mc` → `run_tier_remc`, 10K sims × seeds 42/123/2026, horizon 1500, Run-2 (consistency-on: Tradeify 40%, MFFU 50%), `dd_protection` OFF — inherited, never re-decided. |
| Floor | **bust ≤ 3.0% AND P(pass) ≥ 50%** — the frozen gate floor, unchanged. |
| Feasibility pre-declaration (verdict ceiling) | **Cap check FAILS on every cell at native sizing, by construction:** Tradeify/MFFU caps count micro-equivalents (mini = 10 micro); standard 6J = 10× M6J ⇒ Aegis cap-12 ≈ **120 micro-equiv** vs T-100K cap 80 already ~79-filled by MYM+MNQ (50K: ~60 equiv at halved sizing vs caps 40/50, on top of ~39.5). M6J exists at no FRIENDLY firm. Therefore the **maximum available verdict is GEOMETRY-PASS/GEOMETRY-FAIL**; "clearer", §4, and 11-08 vocabulary are out of scope. |

---

## §3 — Inherited unchanged (cited, not re-decided)

Frozen floor + engine + Run-2 gating (gate prereg `be6dda6`); MYM/MNQ byte pins + 1R pins
(candidate #1 prereg); correction idiom (`59c2282` study); published corrected pins
(band rescore 2026-07-24); §4-falsifier ownership (withdrawal ADR — untouched by this run).

---

## §4 — Falsifiable hypothesis (H-AEGIS1P; binary, geometry-only)

**H-AEGIS1P — if** the 3-leg book (Aegis@1.00%) yields `bust ≤ 3.0% AND pass ≥ 50%` on the
full panel (corrected Run-2) at **≥1** of the three scored tiers, **then** Aegis@1% is
**geometry-viable** in the c1 book — the binding blocker becomes product/cap feasibility
(no M6J; 6J = 10 micro-equiv), a venue fact, not a risk fact — and any follow-on (e.g.
reduced-size expression) is a **new** operator-authorized pre-registration.
**Otherwise** H-AEGIS1P is **falsified**: Aegis fails corrected trailing-DD geometry at 1%
even at the friendliest measured tier, the 0.75%→1.50% bust bracket closes with all three
measured points, and the prop-side 6J lane is dead at **both** layers (geometry AND
feasibility) with no further risk-arm measurement owed.

Numerically: accept if ≥1 of {T-100K, T-50K, MFFU-50K} clears both floor limbs at the
gating arm; reject if 0 of 3. H1/H2, bootstrap, and COST-TRUE cells are diagnostics and
can neither accept nor reject.

---

## §5 — Forbidden moves (each genuinely tempting)

- **Any clearer/§4/11-08 claim from any outcome** — the cap pre-check fails every cell;
  the vocabulary is pre-capped at GEOMETRY-PASS/FAIL.
- **Risk-arm iteration after data** (0.9%? 1.1%? re-weight Strikers?) — the bracket
  {0.75%, 1.00%, 1.50%} closes with this run; a new arm needs new operator authorization
  and a fresh pre-registration.
- **Promoting COST-TRUE or H1/H2 or bootstrap to gating** — one gating cell type was
  declared; diagnostics stay diagnostics.
- **Re-pinning Aegis 1R after seeing results** (the $2,163.57/n7 pin is frozen above;
  the 5274c 9×-fallback incident is the standing reason this is load-bearing).
- **Hand-editing `dd_lock_offset_usd` or any `firm_rules.py` constant** — runtime patch +
  restore only.
- **Widening the tier set** (25K/150K/Bulenox/BluSky) — no decision rides on them here.
- **Treating the fresh export as the ae744 panel of record** — different span (front-
  truncated), different sizing; the panel-of-record pin is untouched by this run.

---

## §6 — Gate criteria (binary dispositions)

| Verdict | Trigger | Disposition |
|---|---|---|
| **GEOMETRY-PASS (feasibility-blocked)** | ≥1 scored tier clears both floor limbs at 1.00× | Aegis@1% survives corrected DD geometry; lane remains blocked on product/cap facts; any reduced-size or M6J-contingent follow-on = new pre-reg + operator GO |
| **GEOMETRY-FAIL** | 0 of 3 tiers clear | Bracket closed (0.75/1.00/1.50 all measured); prop-side 6J lane dead at both layers; no further risk-arm run owed |
| **AMBIGUOUS** | Any T-100K control miss (±0.15pp) ⇒ harness defect, no verdict; or a decisive cell lands bust ∈ (3.0%, 3.2%] ⇒ single n-doubling re-run of that cell only |

---

## §7 — Prior-look disclosure + K accounting

Prior looks on Aegis-in-book at Tradeify bases (all defective geometry, `eba5030`):
1.50% → 10.33% (50K) / 17.70% (100K), Aegis attr ~71%; 0.75% → 2.02% (ae744) / 1.28%
(5274c size-adj); the corrupted Test-2 cell 39.43% (9× pin fallback); ~7 variants examined
pre-Class-S (disclosed at admission). Corrected-geometry 2-leg pins: 4.74%/1.06%/0.96%.
**Chat-level prior look (2026-07-26, disclosed):** an interpolation guess "1% lands ~3–5%
at 50K on defective geometry" was stated in conversation before this brief; it is a prior
look and is disclosed, not laundered. **No 1.00% cell has ever been measured under any
geometry.** K accounting: 1 arm × 3 tiers, tier set fixed by decision-relevance (live
account + the two corrected clearers; zero researcher DOF after freeze); pre-registered
single-arm portfolio re-MC — no discovery-manifest K consumed (Q-COMPOSE-1 precedent).

---

## §8 — Run protocol

1. Runner `lab/analysis/c1/aegis1p_3leg_rescore_2026-07-27/run_aegis1p_rescore.py`: register
   the fresh Aegis file beside the frozen harness (runtime `PANEL_FILES` entry; file
   local-only, gitignored tree) → `build_scaled_panel` 2-leg (controls) + 3-leg (scored)
   with frozen 1R expectations → patch corrected geometry → controls (3 cells) → scored
   full-panel (3 cells) → H1/H2 (6 cells) → COST-TRUE full-panel (3 cells) → bootstrap
   only on full-panel passers → restore offsets.
2. Report per cell: `headline_bust`, `pass_rate`, `floor_ok`, plus control deltas vs pins
   and the pre-declared cap-infeasibility line per tier.
3. RESULTS.md + JSON in the same dir; verdict routed to operator. Smoke (`--smoke`,
   n_sims=200) is a wiring check only — its numbers are not read against §6.

---

## §9 — Authorization (operator directive of record)

```
AUTHORIZED / FROZEN: 2026-07-27 / JA (operator chat directive, this session):
"Run the fresh pre-registered Aegis @ 1% test on corrected geometry"
— accompanied by the fresh native-1% export Aegis_6J1_CME_6J1!_2026-07-27_ac331.csv.
Bracket context: the 2026-07-26 session established 1.50%/0.75% as the measured
bracket ends and 1.00% as the unmeasured cell; this directive authorizes exactly
that cell, one arm, corrected geometry.
```

---

## §10 — Audit hooks (runnable)

```bash
# 1. Aegis input immutability: sha256 of the export this brief froze.
sha256sum "lab/analysis/c1/aegis1p_3leg_rescore_2026-07-27/Aegis_6J1_CME_6J1!_2026-07-27_ac331.csv"
# expect cbf57ac29a26bcfba2efed62fc3a30ab9309c4f51802e9765557d05b5e1e848f

# 2. Production defect constant untouched (100).
grep -n "dd_lock_offset_usd" core/firm_rules.py

# 3. Frozen floor unchanged.
grep -n "3.0%\|50%" docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md | head -3

# 4. Control pins match the published band-rescore report.
python -c "import json;r=json.load(open('lab/analysis/c1/c1_band_rescore_2026-07-24/band_rescore_report.json'));print(r['control']['headline_bust'],[ (k,c['headline_bust']) for k,c in r['cells'].items() if '1.00x' in k])"

# 5. Runner imports frozen primitives (no re-implementation).
grep -n "run_partition_mc\|build_scaled_panel\|part_b_half_panel\|part_a_bootstrap" \
  lab/analysis/c1/aegis1p_3leg_rescore_2026-07-27/run_aegis1p_rescore.py

# 6. 1R pin frozen pre-run (inventory JSON predates any MC output).
python -c "import json;print(json.load(open('lab/analysis/c1/aegis1p_3leg_rescore_2026-07-27/inventory_aegis1p.json'))['one_r_pin'])"
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-27 | Drafted + FROZEN under the operator's same-day directive; single 1.00% arm; three-tier set; geometry-only verdict vocabulary pre-capped by the cap-feasibility pre-check | Joshua (directive) + Claude Code (Fable 5) |
