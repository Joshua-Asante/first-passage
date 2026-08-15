# Closure record — Q-KBUDGET-1 axis-reachability screen — **RESOLVED** (2026-07-15; was AMBIGUOUS-HOLD 2026-07-14)

**Verdict (current):** `RESOLVED` per frozen pre-registration §D — ≥1 axis (D5 NQ/MNQ intraday-momentum footprint) PASSES both clauses after operator confirm-construct ratification 2026-07-15. Historical `AMBIGUOUS-HOLD` (2026-07-14) preserved below as the session path.
**Verdict (historical):** `AMBIGUOUS-HOLD` 2026-07-14 — all screened fail; ≥1 verdict-relevant UNSCREENABLE (then D5+D7).
**Parent:** [`Q-KBUDGET-1-axis-reachability-screen.md`](../Q-KBUDGET-1-axis-reachability-screen.md) · frozen screen `b304f2c` (G1) · ratified inventory [`Q-KBUDGET-1-phase1-inventory.md`](../Q-KBUDGET-1-phase1-inventory.md) (`ca02030`, G2) · Phase-2 artifacts [`lab/archive/q_kbudget_1_2026-07/`](../../../lab/archive/q_kbudget_1_2026-07/RESULTS.md) (postdate the anchor — §F hook #1 ordering holds).
**Loop accounting:** OUTER, iterations used 3 of 8 (author/freeze → inventory/ratify → screen/verdict). Zero pulls, zero K consumed (no `Q-KBUDGET` manifest exists — parent §10 hook confirms).

---

## §1 — The §E table as measured vs the frozen bands

Reproduced in full in the pre-reg §E annex (filled 2026-07-14) and [`RESULTS.md`](../../../lab/archive/q_kbudget_1_2026-07/RESULTS.md). Which clause killed each excluded axis:

| Axis | Killed by |
|---|---|
| D1 GC/MGC successor | **Clause K — family bank.** K_banked 3,177 ⇒ floor 2.05 for even a single pre-committed hypothesis; > Cap 1.0. |
| D2 wide mining, any other family | **Clause K — design class.** Tiling K 10³–10⁴ ⇒ floor 1.93–2.17. |
| D3 HARV-class ES mechanism | **Clause N — inherited cohort.** Clause K passes (K_eff 2–3, floor ≤ 0.98) but P(primary\|true) ≈ 0.24–0.30 at N ≈ 100 month-ends (Q-HARV-1 §R DECLINE, `9bddd33`) < 0.50. |
| D4 XAU T3b (prop expression) | **Clause K — family bank** (any GC/MGC expression inherits 3,177); its missing δ is moot — cannot flip. |
| D6 eurusd_pattern_enum Phase-4 | **Clause K — declared K.** The locked harness pre-registers K=450 ⇒ floor 1.835. |
| D5 gamma-positioning · D7 JPY month-end | **Not killed — UNSCREENABLE.** Both pass Clause K in range (K_eff ≤ 3 possible, families bank 0); both lack a screenable Clause-N input. These two hold the verdict at AMBIGUOUS rather than FALSIFIED. |

## §2 — Named missing inputs + re-screen trigger (the §D disposition)

- **D5 (verdict-relevant):** vendor gamma/dealer-positioning dataset for DJ30/NAS + a cohort-cited central δ, σ. A procurement decision — deliberately NOT folded into the closed A4 flow-data DEFER (different question; a fresh scoping artifact would be required).
- **D7 (weakly verdict-relevant):** δ/σ extraction from the Q-MECH-1 JPY leg artifacts + JPY futures symbology resolution; power at N ≈ 10² monthly events then computes in seconds (expected HARV-shaped, but the re-screen says, not this note).
- **Re-screen trigger:** either input supplied, or **2026-08-08** (rides the quarterly packet), whichever first.

## §3 — What the verdict means for the 11-08 runway (delivered into the 08-08 packet)

**Newly-started discovery cannot currently be shown reachable for the four-firms ADR §4 falsifier (hard date 2026-11-08).** No ratified discovery axis clears both frozen clauses on current inputs; the two UNSCREENABLE rows are input-supply questions, not ready axes. This is the H-KBUDGET "otherwise" branch in its AMBIGUOUS form — program planning should treat the discovery route as **not fundable today** rather than discovering that at 11-08.

**The live alternative route is Class S (operator directive, 2026-07-14): existing-strategy books at the frozen survivor-scoring gate.** Ratified out-of-screen-scope (inventory §6): their governing gate is the already-frozen survivor-scoring pre-registration (`be6dda6` — Part A bust ≤ 3.0% + P(pass) ≥ 50%, Run-2, $100K×4 frozen tiers, ≥2 firms incl. ≥1 `trailing_locking`). Best priors (Tradeify Select 50K, geometry-only): 2-leg MYM+MNQ bust 0.76%; 3-leg with Aegis@0.75% bust 2.02% — inside the frozen ceiling on an unscored surface (the frozen $100K×4 cross-section has never been run for any S-book). Gated on: the four-firms ADR amendment (authorized for drafting 2026-07-14, `Proposed` on landing), the Aegis panel-of-record resolution (Cursor handoff), and a candidate pre-registration with prior-look disclosure BEFORE any frozen-tier G4 run.

## §4 — Lesson candidates (dated anchors; candidate-status until they re-fire)

- **L-cand-1 (2026-07-14, this screen):** family K-banking forecloses a *family*, not just a budget — GC/MGC's banked 3,177 puts floor 2.05 on even a K=1 mechanism/transfer axis (D1/D4). Corollary: mine a family last, not first; a family you might want for a mechanism axis should not host a wide-mining shakedown.
- **L-cand-2 (2026-07-14):** the screen converted "which axis do we fund?" into "which input do we buy/extract?" — both surviving rows are input-supply questions. The a-priori screen's real product is a cheaper decision class, not a slate.
- **L-cand-3 (2026-07-14):** M-19 confirmed at the axis-portfolio level: with the realism Cap at 1.0, the only Clause-K-passable design class is ≤3 pre-committed hypotheses on an unmined family — and every such axis in the current inventory then dies or stalls on Clause N. The binding constraint on discovery has fully moved from statistics machinery to *effect-prior supply*.

## §10 — Audit hooks (runnable)

```bash
# Verdict reproduces from the committed harness
python lab/archive/q_kbudget_1_2026-07/floor_scan.py   # expect: 6 FAIL / 1 PASS (D5) / 0 UNSCREENABLE → RESOLVED (historical path: 2026-07-14 AMBIGUOUS-HOLD → §5 hinge → §6 ratification)

# Freeze/ratification/screen ordering (three strictly increasing commits)
git log --format='%h %ci' -- docs/briefs/pre-registration/Q-KBUDGET-1-screen-preregistration.md | tail -1   # b304f2c
git log --format='%h %ci' -- docs/briefs/Q-KBUDGET-1-phase1-inventory.md | tail -1                          # ca02030
git log --format='%h %ci' -- lab/archive/q_kbudget_1_2026-07/ | tail -1                                    # later than both

# No K consumed by the screen
grep -rn "Q-KBUDGET" discovery_manifests/ 2>/dev/null && echo "REVIEW" || echo "no manifest entry (expected)"

# Re-screen obligation is visible on STATE (must survive until it fires)
grep -n "Q-KBUDGET-1" STATE.md
```

---

## §5 — Addendum: D7/D5 re-screen (2026-07-15) — verdict unchanged, D5 hinge narrowed to a ratification ask

**This addendum does not alter the §1–§10 verdict above; it records what changed since.** The original AMBIGUOUS-HOLD (2026-07-14) is preserved as the closure's historical record. The frozen pre-registration §B/§C/§D are untouched by this addendum — only §E (its explicitly-designed-to-be-filled results annex) was updated, per §D's own "re-screen when [the missing input is] supplied… or 2026-08-08" disposition.

**D7 — discharged, screened-FAIL.** The Q-MECH-1.JPY leg's endogenous mechanism (MECHANISM-NAMED-ENDOGENOUS close, `docs/ltm/briefs/Q-MECH-1.JPY_h_register.md`) yields no non-circular standalone-entry δ — the P-cohort (n=8) is the same data that motivated the mechanism close and is forbidden as discriminating evidence; the excluded-vs-permitted loss-avoidance contrast is category-mismatched (conditional-on-loser, not an entry mean). Screened instead via the HARV class-analogue (Q-HARV-1 §R, `9bddd33`, δ/σ=0.144) per §B's "nearest analytic analogue" provision: power = Φ(√100·0.144 − 1.96) = 0.30 < 0.50 → **FAIL (Clause N)**. Full derivation: [`lab/archive/q_kbudget_1_2026-07/d7_clause_n_screen.md`](../../../lab/archive/q_kbudget_1_2026-07/d7_clause_n_screen.md), reproduced by [`d7_power.py`](../../../lab/archive/q_kbudget_1_2026-07/d7_power.py). This settles D7 — it is no longer a re-screen trigger.

**D5 — candidate PASS computed, held on an operator ratification, not a data gap.** The B4/B5 procurement research found the "missing vendor dataset" framing overtaken by events: a free/cheap, cohort-cited δ already exists in the peer-reviewed literature (Baltussen, Da, Lammers & Martens 2021, *JFE*, "Hedging demand and market intraday momentum" — per-index NQ futures β=6.36, t=7.97, OOS-R²=3.76%; YM futures β=5.02, t=4.12). Plugging the t-scaled central reading (δ/σ=0.113) at the declared N≈1,000 daily events: power = Φ(√1000·0.113 − 1.96) = 0.947 → **PASS (Clause N)**; Clause K independently PASSES at every declared K_eff (floor 0.65–0.98 ≤ Cap 1.0, construct-independent). **What is actually open is not a procurement decision but a confirm-construct pin:** the axis's "gamma-positioning" label is ambiguous between (i) the intraday-momentum footprint (screens PASS, citable per-index) and (ii) the gamma-*sign* mechanism (no NDX/Dow cohort exists in the literature — stays UNSCREENABLE). This choice is verdict-determining (§D's RESOLVED trigger requires only "≥1 axis PASSES both clauses") and is deliberately left to the operator — the §E annex row and `floor_scan.py`'s D5 entry are **intentionally left UNSCREENABLE** pending that ratification, not silently flipped. Full derivation + the DJ30-leg recommendation (drop or down-weight; DIA/YM proxy is ~25–60× thinner than QQQ/NQ) + the downstream net-of-cost caveat (Baltussen's own Sharpe is gross; only SPX-futures shown to survive tick costs): [`lab/archive/q_kbudget_1_2026-07/d5_clause_n_rescreen.md`](../../../lab/archive/q_kbudget_1_2026-07/d5_clause_n_rescreen.md), reproduced by [`d5_power.py`](../../../lab/archive/q_kbudget_1_2026-07/d5_power.py).

**Net effect on §3's "not fundable today" reading.** Unchanged at time of §5 (still AMBIGUOUS-HOLD; hinge = construct pin). **Superseded same day by §6.** Was still AMBIGUOUS-HOLD with no ratified PASS — but the shape of the hold has narrowed from two input-supply questions to one construct-pin decision that a short review can resolve. If ratified toward the intraday-momentum-footprint construct, the KBUDGET verdict flips to **RESOLVED**, and D5 (NAS100/NQ-anchored, DJ30 dropped or down-weighted) becomes a ranked candidate for the 08-08 packet — with its fundability then gated by the campaign HARD gate (does the *net* MNQ intraday-momentum Sharpe clear the Clause-K floor of 0.65–0.98 at K_eff 1–3?), not by this screen.

**Lesson candidate — L-cand-4 (2026-07-15):** an axis's "missing input" label can silently conflate two different gaps — a genuine data-procurement gap (buy/collect) and a construct-definition gap (which of several plausible confirm designs does the axis's plain-language name actually mean?). The latter is often resolvable for free from existing literature; screening it open is a research task, not a procurement one, and the two should not be filed under the same disposition without checking which is which.

## §6 — Addendum: D5 confirm-construct ratified → RESOLVED (2026-07-15)

**Operator decision (2026-07-15, quad-track Day 0):** confirm-construct = **intraday-momentum footprint** (Baltussen et al. 2021 *JFE* NQ cohort); **gamma-sign mechanism declined**; DJ30 drop/down-weight. Harness `floor_scan.py` re-run → D5 **PASS**, verdict **RESOLVED** (6 FAIL / 1 PASS / 0 UNSCREENABLE).

**What this licenses:** D5 is ranked onto the 08-08 axis-selection slate and may proceed to **campaign scoping** under standing HARD gates (HARV §R reachability attestation before `register_search open`; net-of-cost Sharpe vs Clause-K floor 0.65–0.98 at K_eff ≤ 3). Screen PASS never blesses a candidate and never authorizes a Databento pull by itself.

**Scoping artifact:** [`docs/briefs/rnd-pipeline/D5-NQ-intraday-momentum-scoping.md`](../rnd-pipeline/D5-NQ-intraday-momentum-scoping.md).
