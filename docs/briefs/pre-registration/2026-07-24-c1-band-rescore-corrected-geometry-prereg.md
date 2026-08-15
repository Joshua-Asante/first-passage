# Pre-registration — Class-S candidate #1: corrected-geometry re-score of the four defect-carrying band tiers

**Status:** `FROZEN` (operator chat directive 2026-07-24 — "proceed with the two unmeasured arms";
§9 records the authorization verbatim). No item below changes after any band result is seen
(Known Trap #12 — amendments require closing this pre-registration and opening a fresh one).
**What this is:** a pre-registered corrected-geometry **re-measurement** of the already-frozen
Class-S candidate #1 book at the four `firm_rules.py` eval rows that carry the 2026-07-22
drawdown-lock defect and were **never re-scored** after the correction
(`Tradeify_Select_25K`, `Tradeify_Select_50K`, `Tradeify_Select_150K`, `MFFU_Rapid_50K` —
the exact set the withdrawal RESULTS §0 enumerates as identified-but-not-re-scored).
**Parent candidate (unchanged, cited not re-decided):**
[`2026-07-15-existing-strategy-book-candidate-1-prereg.md`](2026-07-15-existing-strategy-book-candidate-1-prereg.md)
(`FROZEN`; its $100K×4 Part A discharge was **WITHDRAWN 2026-07-22** — zero clearers under
corrected geometry).
**Gate of record (unchanged, cited not re-decided):**
[`2026-07-13-prop-survivor-scoring-prereg.md`](2026-07-13-prop-survivor-scoring-prereg.md)
(`be6dda6`, FROZEN) — floor bust ≤ 3.0% + P(pass) ≥ 50%, Run-2 (consistency-on).
**Loop of record:** STRATEGIC.
**Feeds:** the four-firms ADR §4 falsifier's **2026-11-08 demotion clause** ("no clearer on
**any** tier" → research-only). Note the two distinct thresholds: full **discharge** needs ≥2
firms clearing incl. ≥1 `trailing_locking` (G8); the 11-08 **demotion** fires only if *no* tier
clears at all. A single band clearer defeats demotion without discharging §4.
**Authored:** 2026-07-24 · Claude Code (Fable 5), operator-directed.

D-S-A domain: data (tier-set selection + arm set fixed pre-run; no system or framework change).

---

## §0 — Rule-0 reads (production source, verified this session 2026-07-24, HEAD `ca6fb03`)

Per-file anchors (`git log -1 --format='%h %ci'`), all content-read in full this session.
The path [`core/firm_rules.py`](../../../core/firm_rules.py) is the primary read:

- **`core/firm_rules.py` @ `fd95c72`** — the four target rows read verbatim (lines 268–323,
  360–374): `Tradeify_Select_25K` (bal 25K, `max_dd_pct` 4.0 = $1,000, target 6% = $1,500,
  `micro_contract_cap` **10**, consistency 40), `Tradeify_Select_50K` (50K, 4.0% = $2,000,
  $3,000, cap **40**, 40), `Tradeify_Select_150K` (150K, 3.0% = $4,500, $9,000, cap **120**,
  40), `MFFU_Rapid_50K` (50K, 4.0% = $2,000, $3,000, cap **50**, consistency 50,
  `min_trading_days` 2). All four: `dd_type="trailing_locking"`, `dd_lock_offset_usd: 100` —
  the in-file OPEN-DEFECT comment (2026-07-22) confirms the eval rows carry a lock the eval
  phase does not have; direction OPTIMISTIC; constant deliberately not hand-edited.
- **[`lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/remc_g8_discharge_check.py`](../../../lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/remc_g8_discharge_check.py) @ `59c2282`** —
  the correction idiom this run reuses verbatim: runtime patch
  `FIRM_RULES[tier]["dd_lock_offset_usd"] = 1_000_000.0` (engine's own no-lock idiom per
  `tests/core/test_trailing_locking_boundary.py`; **NOT** `None`, which disables the DD branch),
  restore to 100 after. Published corrected 100K pins this run's control must reproduce:
  Tradeify_Select_100K Run-2 bust **4.74%**, MFFU_Rapid_100K **4.25%**.
- **[`lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_scoring.py`](../../../lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_scoring.py) @ `f8f8db1`** —
  panel construction of record (`build_scaled_panel`: $200K-static decompound → `pin_r_basis`
  full_stop_mean → risk%-scale; byte-pinned CME CSVs + 1R pins asserted). **Tier-basis
  handling is harness-native linear scaling:** `scale_panel_to_tier(panel_200k, tier)` =
  `panel × (starting_balance / 200_000)` (L336-339); `book_daily_at_100k` is the same formula
  at 100K (L341-344). The band daily series below are this exact formula at each band's
  balance — no new method is introduced.
- **[`lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_regime_gate.py`](../../../lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_regime_gate.py) @ `163b0b5`** —
  `run_partition_mc` (L87-110): Run-2 semantics = `run_tier_remc(firm_key, blocks, thr,
  consistency=consistency_rule_pct/100)`; `_floor_ok` = bust ≤ ceiling ∧ pass ≥ floor. The
  band runner calls these frozen primitives, not a re-implementation.
- **[`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`](2026-07-13-prop-survivor-scoring-prereg.md) @ `be6dda6`** —
  frozen floor **bust ≤ 3.0% + P(pass) ≥ 50%**, 10K sims × seeds 42/123/2026, horizon 1500,
  Run-2 where consistency exists. **Nothing here re-decides the floor.** The frozen $100K×4
  tier set is that gate's scoring set; this brief scores *additional* tiers under the same
  floor and claims nothing about the frozen set.
- **[`docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md`](../../adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md) @ `59c2282`** —
  current §4 state: **UNDISCHARGED**, hard date 2026-11-08; RESULTS §0 enumerates
  `Tradeify_Select_{25K,50K,150K}` + `MFFU_Rapid_{50K}` as defect-carrying rows
  identified but **not re-scored** — exactly this brief's tier set.

---

## §1 — Context + the question

The 2026-07-22 correction flipped both $100K `trailing_locking` tiers PASS→FAIL and left the
§4 falsifier undischarged with **zero clearers on the frozen $100K set**. But "zero clearers"
is a $100K-basis statement: four other eval rows carry the same phantom-lock defect and were
never re-scored under corrected geometry. The disclosed prior look at 50K (defective
geometry, 2026-07-10/11 futures3 runs) was **0.76% bust for a 2-leg book** — 2.24pp *under*
the ceiling, where the corrected 100K delta was +2.10pp. Whether any band tier clears
corrected Part A is therefore a live, cheap, decision-relevant question: a clearer defeats
the 11-08 demotion clause (though it does not by itself discharge §4).

Symptom-only phrasing: *the program's §4 evidence is currently a four-tier, one-basis
measurement; the remaining defect-carrying tiers are unmeasured.* This brief measures them.
It does not propose re-weighting, new candidates, or gate changes.

---

## §2 — The test (FIXED)

| Item | Fixed value |
|---|---|
| Book | Class-S candidate #1 exactly as frozen: 2 legs Striker→MYM + Striker→MNQ, byte-pinned panels, weights 0.70%/0.37%. **Not re-weighted, not re-composed.** |
| Tier set | **Exactly four:** `Tradeify_Select_25K` · `Tradeify_Select_50K` · `Tradeify_Select_150K` · `MFFU_Rapid_50K` (the withdrawal RESULTS §0 defect-carrying enumeration). Plus `Tradeify_Select_100K` as **reproduction control only** (must reproduce 4.74% ± 0.15pp; never a "clearer"). |
| Geometry | CORRECTED on all scored tiers: runtime patch `dd_lock_offset_usd → 1_000_000.0` (restore after). |
| Arms | **Exactly two:** `1.00×` (candidate basis — the frozen gate's scoring basis; **the gating arm**) · `0.50×` (WATCH-1 deployed rung; **diagnostic, non-gating**). Ratified rungs only. |
| Daily series per tier | `daily_tier = panel_200k.sum(axis=1) × (starting_balance / 200_000)` — the harness-native `scale_panel_to_tier` formula; `× 0.50` for the diagnostic arm. |
| Partitions | **Full panel only** (Part A basis). No bootstrap, no halves in this pass — any 1.00× clearer owes the §7(7) regime rider before any G8-style use (pre-committed follow-on, separately run). |
| Engine | Frozen: `run_partition_mc` → `run_tier_remc`, 10K sims × seeds 42/123/2026, horizon 1500, Run-2 (consistency-on: Tradeify 40%, MFFU 50%), `dd_protection` OFF — inherited, never re-decided. |
| Floor | **bust ≤ 3.0% AND P(pass) ≥ 50%** — the frozen gate floor, unchanged. |
| Feasibility overlay (reported per tier, load-bearing for §6) | Cap check: linearly-scaled aggregate position ≈ 79 micros × (bal/100K) at 1.00× vs the tier's `micro_contract_cap` — 25K ≈ 20 vs cap **10 → INFEASIBLE at 1.00×**; T-50K ≈ 40 vs 40 (borderline); 150K ≈ 119 vs 120; MFFU-50K ≈ 40 vs 50. Granularity: integer flooring at small balances (MNQ base ≈ 2–3 contracts at 25K) makes linear scaling optimistic — any 25K/50K PASS is provisional pending an integer-quantization check (F2-floor pattern). |

**Linear-scaling honesty note (the load-bearing subtlety):** `scale_panel_to_tier` scales
dollar P&L linearly with balance, which assumes positions scale continuously and caps never
bind. At 150K and MFFU-50K that assumption is approximately sound; at Tradeify-50K it is
borderline (cap-exact); at 25K it is **false at 1.00×** (cap-clipped by ~2×). The overlay
column is therefore part of the verdict, not a footnote: a tier "clears" only if Part A
passes **and** the cap check does not exceed the tier cap at the gating arm.

---

## §3 — Inherited unchanged (cited, not re-decided)

- Frozen floor bust ≤ 3.0% + P(pass) ≥ 50%; 10K×3-seed engine; Run-2 gating (gate prereg `be6dda6`).
- The c1 book composition, byte-pinned panels, 1R pins (parent candidate prereg).
- The correction idiom `dd_lock_offset_usd → 1_000_000.0` (correction study, `59c2282`).
- The §4 falsifier's ownership by the withdrawal ADR (UNDISCHARGED; hard date 2026-11-08).

---

## §4 — Falsifiable hypothesis (H-BAND; binary)

**H-BAND — if** at least one tier in {`Tradeify_Select_50K`, `Tradeify_Select_150K`,
`MFFU_Rapid_50K`} (25K excluded from the *clearer* claim by the pre-declared cap
infeasibility; it is still measured and reported) yields `headline_bust ≤ 3.0% AND
pass_rate ≥ 50%` at the **1.00×** arm under corrected geometry with its cap-feasibility
check passing, **then** the prop-portfolio program has a corrected-geometry Part A clearer
outside the $100K band — the 2026-11-08 demotion clause ("no clearer on any tier") is
defeated, and the clearer routes to operator review + the §7(7) regime rider (it does
**not** by itself discharge §4, which needs ≥2 firms incl. ≥1 `trailing_locking`).
**Otherwise** H-BAND is **falsified**: the c1 book has no Part A clearer at any measured
Tradeify/MFFU tier under corrected geometry, the "zero clearers" finding extends from the
$100K basis to every defect-carrying band, and the 11-08 falsifier stands on discovery
alone.

Accept/reject (restated numerically): accept H-BAND if bust ≤ 3.0% and pass_rate ≥ 50%
and cap-check PASS on ≥1 of {T-50K, T-150K, MFFU-50K} at the 1.00× arm; reject if 0 of 3;
the 25K cell and the 0.50× arm are reported diagnostics and can neither accept nor reject.

---

## §5 — Forbidden moves (each genuinely tempting)

- **Widening the tier set after seeing results** (Bulenox/BluSky bands, other firms'
  products) — those rows carry no correction-defect and have no prior look at band basis;
  adding them is a *new* look requiring its own pre-registration, not a correction.
- **Treating a band clearer as a §4 discharge** — discharge needs ≥2 firms clearing incl.
  ≥1 `trailing_locking` (G8); one clearer only defeats the demotion clause. The write-up
  must keep the two thresholds separate.
- **Promoting the 0.50× diagnostic arm to the gating arm** if 1.00× fails everywhere but
  0.50× passes somewhere — the frozen gate scores the candidate basis; whether a
  WATCH-1-sized book can be a §4 candidate is an operator/ADR governance question, not a
  result this brief may claim.
- **Reading a 25K Part A pass as a clearer** — the cap check fails at 1.00× by
  construction (~20 vs 10); linear scaling is invalid there and the pre-declared verdict
  for that cell is capped at AMBIGUOUS-INFEASIBLE.
- **Hand-editing `dd_lock_offset_usd` in `firm_rules.py`** — the constant stays 100 until
  its own amending ADR + three-consumer re-pin (correction-study decision, inherited).
- **Relaxing the 3.0% ceiling / 50% floor, or inventing a band-specific floor** — the
  regime-gate methodology's pre-registered-floor rule binds here identically.
- **Re-weighting MYM/MNQ per band to fit under a cap** — composition is frozen; a
  cap-motivated re-weight is the ADR-forbidden variant-grind.

---

## §6 — Gate criteria (binary dispositions)

| Verdict | Trigger | Disposition |
|---|---|---|
| **RESOLVED-CLEARER-FOUND** | ≥1 tier ∈ {T-50K, T-150K, MFFU-50K} clears the floor at 1.00× with cap check PASS | 11-08 demotion clause defeated; clearer routes to operator review + regime rider + (if a second firm's tier also clears) a G8-shaped discharge question via amending ADR |
| **FALSIFIED-NO-BAND-CLEARER** | No such tier clears at 1.00× | "Zero clearers" extends to all defect-carrying tiers; §4 rests entirely on discovery before 2026-11-08 |
| **AMBIGUOUS** | A decisive cell lands within MC noise of the ceiling (bust ∈ (3.0%, 3.2%]) **or** the 100K reproduction control misses 4.74% ± 0.15pp **or** the only passing tier is cap-borderline (T-50K exactly at cap) | Noise-band: single n-doubling re-run of that cell; control miss: harness defect, no band verdict; cap-borderline: report with the integer-quantization check as the pre-committed follow-on |

---

## §7 — Prior-look disclosure + K accounting

Prior looks on this book at non-100K Tradeify bases (all **defective** geometry, disclosed
in the Class-S ADR §0/§1, from `tradeify_futures3_remc_2026-07-11` +
`tradeify_futures3_bustcut_2026-07-11`, anchor `eba5030`): 3-leg full-Aegis 100K bust
17.70%; 50K 2-leg **0.76%**; 50K Aegis@0.75% variants 2.02%/1.28% (~7 variants examined
pre-Class-S, disclosed at admission). At the frozen $100K set (defective): Tradeify 2.65% /
MFFU 2.64% (PASS) → corrected 4.74% / 4.25% (FAIL). **No tier in this brief's set has ever
been scored under corrected geometry.** K accounting: 4 scored tiers × 2 pre-declared arms
+ 1 control cell; tier set is defined by the withdrawal RESULTS §0 enumeration (zero
researcher DOF on membership); arms are governance rungs (zero DOF on values). No
DSR/Clause-K claim is made (Class S is out-of-screen-scope; the gate of record has no DSR
clause — parent §7).

---

## §8 — Run protocol

1. Runner `lab/analysis/c1/c1_band_rescore_2026-07-24/run_band_rescore.py` (sibling; frozen
   primitives imported, nothing edited in place): patch corrected geometry on the five
   Tradeify/MFFU tiers touched (4 scored + 100K control) → build panel via
   `build_scaled_panel` (Phase-0 + byte pins enforced by the frozen harness) → per tier:
   `daily_tier` per §2 → `run_partition_mc` at 1.00× and 0.50× → restore offsets.
2. Report per (tier × arm): `headline_bust`, `pass_rate`, `floor_ok`, cap-check figures,
   plus the 100K control delta vs 4.74%.
3. RESULTS.md in the same dir; header cites this pre-registration + parent + gate by path.
   Route the verdict to the operator; any clearer additionally owes the regime rider
   (separate run, this brief's §2 pre-commits it) before any G8-shaped use.

---

## §9 — Authorization (operator directive of record)

```
AUTHORIZED / FROZEN: 2026-07-24 / JA (operator chat directive, this session):
"proceed with the two unmeasured arms" — arm 1 = corrected WATCH-1 0.50x full-panel
reference (GO ADR §6 open B7 input; separate runner, same day); arm 2 = THIS brief.
Class-S early-fail branch note: the first candidate's corrected all-four-fail would
require fresh operator authorization for any second candidate; this run is a corrected
re-measurement of the SAME candidate at the enumerated defect-carrying tiers under the
same frozen floor, authorized by the directive above.
```

---

## §10 — Audit hooks (runnable)

```bash
# 1. Tier-set immutability: exactly the four defect-carrying rows + 100K control.
grep -n "Tradeify_Select_25K\|Tradeify_Select_50K\|Tradeify_Select_150K\|MFFU_Rapid_50K" \
  docs/briefs/pre-registration/2026-07-24-c1-band-rescore-corrected-geometry-prereg.md | head

# 2. The scored rows still carry the un-hand-edited defect constant (100) in production.
grep -n "dd_lock_offset_usd" core/firm_rules.py

# 3. Correction idiom is the engine's own no-lock value, not None.
grep -n "1_000_000" lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/remc_g8_discharge_check.py

# 4. Frozen floor unchanged.
grep -n "3.0%\|50%" docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md | head -3

# 5. Reproduction-control pin (4.74%) matches the withdrawal RESULTS.
grep -n "4.74" lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/RESULTS.md | head -3

# 6. Runner exists and imports frozen primitives (no re-implementation).
grep -n "run_partition_mc\|build_scaled_panel\|scale_panel_to_tier" \
  lab/analysis/c1/c1_band_rescore_2026-07-24/run_band_rescore.py
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python scripts/check_brief.py \
  docs/briefs/pre-registration/2026-07-24-c1-band-rescore-corrected-geometry-prereg.md --type inquire

# §0 anchors (Rule-0 confirmation)
git log -1 --format='%h %ci' -- core/firm_rules.py                                                    # fd95c72
git log -1 --format='%h %ci' -- lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/remc_g8_discharge_check.py  # 59c2282
git log -1 --format='%h %ci' -- lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_scoring.py      # f8f8db1
git log -1 --format='%h %ci' -- docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md           # be6dda6

# Cap-check arithmetic spot-check (79 micros at 100K; caps from firm_rules.py)
grep -n "micro_contract_cap" core/firm_rules.py | head -12
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-24 | Drafted + FROZEN under the operator's same-day "proceed with the two unmeasured arms" directive; tier set = the withdrawal RESULTS §0 defect-carrying enumeration; arms = ratified rungs {1.00× gating, 0.50× diagnostic} | Joshua (directive) + Claude Code (Fable 5) |
