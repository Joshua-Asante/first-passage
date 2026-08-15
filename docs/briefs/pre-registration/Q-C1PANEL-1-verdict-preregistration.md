# Pre-registration — Q-C1PANEL-1: c1 both-halves regime re-MC on the launch-date-extended panel

**Status:** `FROZEN` — operator signed §9 on 2026-07-23 (chat: *"i sign §9. proceed"*). No item below changes after any number is seen (Known Trap #12); an amendment requires closing this pre-registration and opening a fresh one.
**Freeze semantics:** once signed, no item below changes for any reason after any number is seen (Known Trap #12). An amendment requires closing this pre-registration and opening a fresh one.
**Parent brief:** [`Q-C1PANEL-1-c1-regime-panel-start-boundary.md`](../Q-C1PANEL-1-c1-regime-panel-start-boundary.md)
**Authorizing ADR:** [`2026-07-23-c1-rung-selection-ev-objective.md`](../../adr/2026-07-23-c1-rung-selection-ev-objective.md) @ `9ab2e8b` — §Trigger 1 ("a **new** pre-registered both-halves regime re-MC"), §Trigger-check schedule ("**on demand**… no calendar gate").
**Gate of record (cited, not re-decided):** [`2026-07-13-prop-survivor-scoring-prereg.md`](2026-07-13-prop-survivor-scoring-prereg.md) @ `be6dda6` — bust ≤ 3.0% **AND** P(pass) ≥ 50%.
**Loop of record:** STRATEGIC.
**Authored:** 2026-07-23 · Claude Code (Opus 4.8), operator-directed.

---

## §0 — Rule-0 reads (production source, verified 2026-07-23)

Full §0 with content notes lives in the parent brief; anchors restated here so this file stands alone.

- **[`lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_regime_gate.py`](../../../lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_regime_gate.py) @ `163b0b5`** — gate harness. `part_b_half_panel` (L127) splits at the **panel index midpoint**, so extending the start **moves both halves**; `part_a_bootstrap` `N_PANELS_DEFAULT=100` (L74); panel sha256 assertion (L533-536).
- **[`lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_scoring.py`](../../../lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_scoring.py) @ `f8f8db1`** — `PANEL_FILES` pins the panel to **TradingView List-of-Trades exports** (`…MYM1!_2026-07-11_15d8b.csv` `9acfa297…`, `…MNQ1!_2026-07-11_beabf.csv` `8884e6dd…`); `C1_ALLOCS`; `EXPECTED_1R`.
- **[`lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md`](../../../lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md) @ `d85c10c`** — incumbent verdict pair + the §4a reproduction targets.
- **[`docs/methodology/regime_robustness_gate.md`](../../methodology/regime_robustness_gate.md) @ `f2be990`** — pre-registered-floor rule: the gate floor must equal the brief's full-panel floor; no separate regime floor.
- **[`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`](2026-07-13-prop-survivor-scoring-prereg.md) @ `be6dda6`** — frozen floor bust ≤ 3.0% AND P(pass) ≥ 50%.
- **[`docs/adr/2026-07-23-c1-rung-selection-ev-objective.md`](../../adr/2026-07-23-c1-rung-selection-ev-objective.md) @ `9ab2e8b`** — authorizes this instrument; §5 forbids reading ADR acceptance as a rung flip.
- **[`docs/adr/2026-07-11-discovery-campaign-defaults-ratified.md`](../../adr/2026-07-11-discovery-campaign-defaults-ratified.md) @ `ba943a1`** — read to **rule out** as authority: Default #1's 2019-05-06 OOS boundary governs discovery campaigns; Class-S is out of screen scope. The panel boundary here rests on the **contract-launch date**, not this ADR.

**Declared §0 gap (Trap #13):** the two byte-pinned panel CSVs are gitignored and absent from the authoring worktree (`core/data/tv_exports/cme/` holds only `SHA256SUMS`). The panel's true first trade date was **not read** and is a Phase-0 blocking read (§8 P0.1). If it already reaches 2019-05-06, this instrument closes `AMBIGUOUS` (moot).

**Databento coverage + cost, measured 2026-07-23 (free metadata endpoints; no data pulled):** `MNQ.v.0` / `MYM.v.0` `ohlcv-1m` GLBX.MDP3, 2019-05-06→2020-07-01 → **$0.0000**, 398,906 / 373,146 records; dataset floor 2010-06-06.

---

## §1 — What is under test, in one line

**Exactly one input changes: the panel start date.** Floor, split rule, bootstrap parameters, tiers, engine, seeds, allocations, and 1R pins are all inherited byte-unchanged from the incumbent configuration.

---

## §2 — Frozen panel definition

| Item | Frozen value |
|---|---|
| Extended start | **2019-05-06** — the CME contract-launch date for MYM and MNQ. **Exactly one admissible start date.** Not tuned, not selected from candidates, not derived from Campaign-Default #1 (which does not bind Class-S — §0). |
| Extended end | Unchanged from the incumbent panel's last trade. No forward extension in this instrument. |
| Legs | Unchanged: Striker→MYM (`striker`) + Striker→MNQ (`striker_nas100`). None added, removed, or re-weighted. |
| Allocations | Unchanged: `C1_ALLOCS = {striker: 0.0070, striker_nas100: 0.0037}`. |
| 1R pins | Unchanged: `EXPECTED_1R` striker $2,535.61 (n=8) / striker_nas100 $5,899.32 (n=19), asserted after `pin_r_basis` as today. |
| Source | Decided at Phase 0 (§8 P0.3). **TradingView re-export preferred** where it reaches 2019-05-06 (native engine = arbiter, no port). Databento `MYM.v.0` / `MNQ.v.0` `ohlcv-1m` is the **fallback** and binds the §4b parity gate. |
| Manifests | Any re-sourced or newly landed panel file re-pins `SHA256SUMS` in the **same commit** as the data change (vendor-data integrity gate). |

---

## §3 — Frozen gate configuration (all inherited; listed so drift is detectable)

| Item | Frozen value |
|---|---|
| Arms | **Exactly two**: `1.00×` (AUTHORIZED) and `0.50×` (WATCH-1), plus the §4a reproduction control. No 0.25× arm unless `FALSIFIED-RUNG-UNSUPPORTED` fires, and then only under a fresh pre-registration. |
| Floor | **bust ≤ 3.0% AND P(pass) ≥ 50%** (`be6dda6`). **No separate "regime floor"** may be introduced (methodology `f2be990`). |
| Partitions | Full panel · H1 · H2 · 6mo-block bootstrap. |
| Split rule | **Index-midpoint**, unchanged. Extension moves **both** halves; accepted and pre-registered here, and **not** grounds to re-decide the split. RESULTS must report realized H1/H2 boundary dates on both panels. |
| Bootstrap | `n_panels=100`, `block=126` bd, `BOOT_SEED=20260715` — unchanged. |
| Tiers | `Tradeify_Select_100K` · `MFFU_Rapid_100K` — unchanged. |
| Engine | 10,000 sims × seeds 42/123/2026, horizon 1500, inactivity disabled, `dd_protection` OFF, Run-2 (consistency-on) where consistency exists — unchanged. |
| Reported per (arm × tier × partition) | `headline_bust`, `pass_rate`, `median_days_to_pass` (**diagnostic, non-gating**), `floor_ok`; bootstrap adds `pass_5th` / `bust_95th`. |

---

## §4 — Falsifiable hypothesis (H-C1PANEL) and its preconditions

**H-C1PANEL — if**, on the extended panel (start = 2019-05-06, every other input inherited byte-unchanged per §2–§3), the both-halves regime gate returns **the same verdict pair** as the incumbent — **1.00× FAIL and 0.50× PASS** — **then** the H1 verdict is panel-robust, the incumbent rung selection stands on strengthened evidence, and **no rung change is licensed in either direction**.

**Accept H-C1PANEL if:** extended-panel verdict pair == {1.00× FAIL, 0.50× PASS}, all partitions × both discharge tiers, with §4a satisfied.

**Falsifier — H-C1PANEL is FALSIFIED if** either arm's verdict flips on the extended panel. **Two-sided by construction:**
- `1.00× FAIL → PASS` (with 0.50× still PASS) ⇒ the panel was too short to *admit* the higher rung → `RESOLVED-ADMITS-HIGHER`.
- `0.50× PASS → FAIL` ⇒ the panel was too short to *reject* the live rung → `FALSIFIED-RUNG-UNSUPPORTED`, and the live rung moves **down** to 0.25×.

A falsifier that could only pay in one direction would not be a falsifier; the two-sidedness is the structural defence against panel-shopping.

**AMBIGUOUS if:** §4a deviates, **or** §4b fails, **or** P0.1 shows the panel already starts ≤ 2019-05-06.

### §4a — Reproduction control (always required)

Re-run both arms on the **unchanged incumbent panel**. Every seed is fixed (`42/123/2026`, `BOOT_SEED=20260715`), so this must reproduce the incumbent **exactly at reported precision (2 dp)** — not merely "within noise":

| Cell | Must reproduce |
|---|---|
| 1.00× Tradeify — H1 bust / bootstrap-95th | **4.37% / 10.37%** |
| 1.00× MFFU — H1 bust / bootstrap-95th | **4.36% / 10.33%** |
| 0.50× — H1 bust / bootstrap-95th / pass-5th | **0.14% / 0.77% / 95.76%** |
| Verdict pair | **1.00× GATE FAIL, 0.50× GATE PASS** |

**Any deviation at 2 dp is a harness defect, not noise ⇒ `AMBIGUOUS`, stop.**

### §4b — Source-fidelity parity gate (databento branch only; skipped if Phase 0 selects TV)

The offline port must reproduce the byte-pinned TV panel on the **overlap window** (incumbent start → last trade) before the extension window is run. Binding statistic is the series the gate actually consumes, `book_daily_at_100k(panel)`:

| Check | Threshold |
|---|---|
| Daily-$ series Pearson r (overlap) | **≥ 0.99** |
| \|Δ total P&L\| (overlap) | **≤ 2%** |
| \|Δ worst 1-day loss\| (overlap) | **≤ 5%** — the loss tail drives bust; a looser band here would defeat the gate |
| Trade count, per leg | **exact match** |
| Trade direction | **100% match** |
| Entry bar-time | **exact on ≥ 99%**; remainder within ±1 bar (15m) |

**Fail any row ⇒ `AMBIGUOUS`, stop; the extension window is never run.** **No operator-override path on §4b** — unlike the F3 Step-2 CFD parity override (which had an identified size→state coupling mechanism), a port/source mismatch has no benign explanation ([[lesson_offline_port_needs_real_source_anchor]]).

---

## §5 — Forbidden moves (binding at execution)

- **Any second panel start date.** 2019-05-06 or nothing. Running 2018 / 2020 / "earliest available" and reporting the best is best-of-K on the panel axis ([[lesson_snag_best_of_k_anchor_graveyard]]).
- **No-repeat clause.** This question gets **exactly one** executed run. `RESOLVED-PANEL-ROBUST` closes the panel axis permanently for c1; re-opening requires genuinely new data (not a new window over the same data) under a fresh brief.
- **Relaxing the 3.0% / 50% floor, or introducing a regime-specific floor** — forbidden by the regime-gate methodology.
- **Re-deciding the index-midpoint split** because extension moved the halves — pre-registered as accepted in §3.
- **Editing the frozen 2026-07-16 haircut pre-registration** to add a panel arm — it stays byte-unedited (Trap #12); this is a fresh instrument.
- **Promoting `median_days_to_pass` to a gate** — diagnostic only.
- **Overriding §4b parity by operator judgement** — no override path exists on that gate.
- **Reading `RESOLVED-ADMITS-HIGHER` as authorization to arm at 1.00×** — it authorizes a *packet*, not a rung flip; the EV-ADR §Phase-2 chain (admitting ADR + B6 dry-fire re-run + B7) still runs in full.
- **Bundling the `cost_mnq.SLIPPAGE_TICKS_PER_SIDE` measurement** into this run — separate question, separate gate (Trap #11).

---

## §6 — Frozen verdict table

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED-PANEL-ROBUST` | Extended-panel verdict pair == {1.00× FAIL, 0.50× PASS} | Rung stays **0.50×** on strengthened evidence. **Panel axis closed** — no further panel re-run licensed (§5 no-repeat). |
| `RESOLVED-ADMITS-HIGHER` | 1.00× clears bust ≤3.0% **and** pass ≥50% on **all** of {full, H1, H2, bootstrap-95th} × **both** tiers, **AND** 0.50× still clears | A fresh both-halves PASS exists → decision-ready packet → EV-ADR §Phase-2 chain. **No live sizing change from this pre-registration.** |
| `FALSIFIED-RUNG-UNSUPPORTED` | 0.50× fails the floor on any partition × either tier | Live rung unsupported on the better-powered panel → open the admitting decision at **0.25×** under a fresh pre-registration; flag before any B7 arm. |
| `AMBIGUOUS` | §4a deviation, **or** §4b failure, **or** P0.1 mootness | Defect/premise failure — **no panel verdict, no rung movement in either direction.** Record which fired. |

---

## §7 — Prior-look disclosure

The only prior look at this book's regime surface is the incumbent 2026-07-17 run on the **incumbent panel** (§4a numbers), which produced the FAIL/PASS pair this instrument re-tests on a different panel. **No arm has been run at any partition on any extended panel.** Databento coverage/price for the extension window was queried 2026-07-23 via free metadata endpoints — **coverage and price only; no price series was pulled, inspected, or analysed.** K accounting: 2 pre-declared arms on a governance-pinned ladder (`TIER_MULTIPLIER`), one panel boundary fixed by contract-launch date; **zero researcher degrees of freedom.** No DSR/Clause-K claim is made or needed (Class-S is out of screen scope).

---

## §8 — Run protocol (post-signature)

- **P0.1** — Read both byte-pinned panel CSVs in the primary checkout; report first/last trade timestamp + count per leg. **If the panel already starts ≤ 2019-05-06 ⇒ `AMBIGUOUS` (moot), close.**
- **P0.2** — Record *why* the panel starts where it does (TV history depth / account bar cap / export-time choice).
- **P0.3** — **Source selection.** Can TradingView export `MYM1!`/`MNQ1!` 15m List-of-Trades back to 2019-05-06? **YES → TV branch** (re-export, re-pin, §4b skipped — no port is built). **NO → databento branch** (§4b binds).
- **P0.4** — Databento branch only: build the port, run §4b. Fail ⇒ stop.
- **P1** — Land the extension window; re-pin `SHA256SUMS` in the same commit.
- **P2** — Run §4a reproduction control. Deviation ⇒ stop.
- **P3** — Run both arms on the extended panel, all partitions × both tiers.
- **P4** — Adjudicate §6 against this file; land `RESULTS.md` under `lab/analysis/c1_panel_extension_2026-07-<dd>/`; produce the closure artifact.

Execution may be delegated to a frozen-spec executor per the CC/Cursor surface-allocation ADR; **adjudication (§6) returns to CC.**

---

## §9 — Operator signature (gates everything; DRAFT until filled)

```
SIGNED / FROZEN: 2026-07-23 / JA
Authorized: Q-C1PANEL-1 both-halves regime re-MC on the launch-date-extended c1 panel.
Panel start fixed at 2019-05-06 (contract launch); arms fixed at {1.00x, 0.50x};
floor, split rule, bootstrap, tiers, engine, seeds, allocations all inherited unchanged.
Phase 0 is blocking: if TradingView reaches 2019-05-06, TV is the source and no port is built.
Two-sided: a 0.50x FAIL on the extended panel moves the live rung DOWN to 0.25x.
No pull, no port, no arm runs before this block is filled.
```

---

## §10 — Audit hooks (runnable)

```bash
# 1. Signature gate.
grep -n "SIGNED / FROZEN: ____" docs/briefs/pre-registration/Q-C1PANEL-1-verdict-preregistration.md \
  && echo "STILL DRAFT — nothing may run" || echo "signed"

# 2. Exactly one panel start date is admissible; confirm no second date crept in.
grep -oE "20(1|2)[0-9]-[0-9]{2}-[0-9]{2}" docs/briefs/pre-registration/Q-C1PANEL-1-verdict-preregistration.md \
  | sort -u

# 3. Reproduction-control targets match the incumbent RESULTS.
grep -n "4.37\|10.37\|4.36\|10.33\|0.14\|0.77\|95.76" \
  lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md | head

# 4. Floor unmoved.
grep -n "3.0%\|50%" docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md | head -3

# 5. Inherited config unchanged in the harness.
grep -n "N_PANELS_DEFAULT\|BLOCK_SIZE_BDAYS\|BOOT_SEED\|DISCHARGE_TIERS" \
  lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_regime_gate.py

# 6. Freeze-before-result: this file's commit must predate any extension artifact.
git log --oneline --reverse -- docs/briefs/pre-registration/Q-C1PANEL-1-verdict-preregistration.md | head -1
git log --oneline --reverse -- lab/analysis/c1_panel_extension_2026-07-* 2>/dev/null | head -1

# 7. No-repeat clause: at most one extension run directory may ever exist.
ls -d lab/analysis/c1_panel_extension_* 2>/dev/null | wc -l   # 0 pre-run, 1 post-run, never >1

# 8. Incumbent pre-reg still byte-unedited.
git log --oneline -- docs/briefs/pre-registration/2026-07-16-class-s-c1-lifecycle-haircut-regime-remc-preregistration.md
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python scripts/check_brief.py \
  docs/briefs/pre-registration/Q-C1PANEL-1-verdict-preregistration.md --type inquire

git log -1 --format='%h %ci' -- lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_regime_gate.py  # 163b0b5
git log -1 --format='%h %ci' -- lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_scoring.py      # f8f8db1
git log -1 --format='%h %ci' -- lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md                 # d85c10c
git log -1 --format='%h %ci' -- docs/methodology/regime_robustness_gate.md                                        # f2be990
git log -1 --format='%h %ci' -- docs/adr/2026-07-23-c1-rung-selection-ev-objective.md                             # 9ab2e8b
git log -1 --format='%h %ci' -- docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md           # be6dda6
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-23 | Drafted `DRAFT — awaiting operator signature`. Panel start fixed at contract launch 2019-05-06; arms {1.00×, 0.50×}; falsifier made **two-sided** (a 0.50× flip moves the live rung down); reproduction control tightened from "within MC noise" to **exact at 2 dp** (seeds are fixed); §4b parity gate bound to the daily-$ series the gate consumes, with no override path; no-repeat clause added. | Joshua (direction) + Claude Code (Opus 4.8) |
| 2026-07-23 | **Signed / FROZEN** (§9) — operator chat authorization *"i sign §9. proceed"*. Phase 0 authorized. **No item above changed at signature**; the only edits in this commit are the §9 block, the status line, and this row. | Joshua (JA) |
