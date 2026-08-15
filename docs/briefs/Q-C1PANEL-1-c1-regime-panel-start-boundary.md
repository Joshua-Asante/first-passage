# Q-C1PANEL-1 — What sets the c1 regime gate's panel start, and is the H1 verdict panel-limited?

**Status:** `CLOSED-AMBIGUOUS` (2026-07-23) — **premise failure at P0.1, pre-run.** §5's void clause fired: the added window is benign 2019, not chop/crisis (the COVID crash is already in the panel), and the index-midpoint split biases extended-H1 toward PASS. Panel axis closed for c1 by data physics. **$0.00 spend, no pull, no port, no arm, no K, no live effect** — closure: [`closures/Q-C1PANEL-1-closure-ambiguous.md`](closures/Q-C1PANEL-1-closure-ambiguous.md).
**Authored:** 2026-07-23
**Closed:** N/A
**Authors:** Joshua (direction) + Claude Code (Opus 4.8)
**Parent question:** N/A (successor instrument authorized by [`docs/adr/2026-07-23-c1-rung-selection-ev-objective.md`](adr/2026-07-23-c1-rung-selection-ev-objective.md) §Trigger 1 / §Phase 2)
**Loop:** Inquire-phase Pre-Q — closure gates on a two-sided both-halves re-MC verdict on an extended panel (§6).
**Artifact path:** `docs/briefs/Q-C1PANEL-1-c1-regime-panel-start-boundary.md`
**Companion pre-registration:** [`pre-registration/Q-C1PANEL-1-verdict-preregistration.md`](pre-registration/Q-C1PANEL-1-verdict-preregistration.md) (`DRAFT` — must be signed + committed before Phase 1)

---

## §0 — Rule 0 reads (production source, verified 2026-07-23, worktree `claude/databento-subscription-strategy-14235a`)

Per-file anchors via `git log -1 --format='%h %ci'`, all content-read this session:

- **[`lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_regime_gate.py`](../../lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_regime_gate.py) @ `163b0b5`** — the gate harness. `build_scaled_panel(C1_STRATS, C1_ALLOCS, expect_1r=EXPECTED_1R)` (L523-524) → `book_daily_at_100k(panel_c1)` (L551) → `part_b_half_panel` (L127, **index-midpoint** split) + `part_a_bootstrap` (`N_PANELS_DEFAULT=100`, L74). Panels are loaded from `PANEL_FILES` under `core/data/tv_exports/cme/` with a hard sha256 assertion (L533-536). **Load-bearing:** the H1/H2 boundary is derived from the panel's own index midpoint — so extending the panel start **moves both halves**, it does not merely lengthen H1.
- **[`lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_scoring.py`](../../lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_scoring.py) @ `f8f8db1`** — `PANEL_FILES` pins the two c1 legs to **TradingView List-of-Trades exports**: `Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-11_15d8b.csv` (`9acfa297…`) and `Striker_NAS100_v1_CME_MINI_MNQ1!_2026-07-11_beabf.csv` (`8884e6dd…`); `C1_ALLOCS = {striker: 0.0070, striker_nas100: 0.0037}`; `EXPECTED_1R` pins ($2,535.61 n=8 / $5,899.32 n=19). **The panel is a strategy trade list produced by TV's backtest engine — not raw bars.** This is the fact that sets the real cost of any extension (§7 P0.3).
- **[`docs/methodology/regime_robustness_gate.md`](methodology/regime_robustness_gate.md) @ `f2be990`** — Part A (6mo-block bootstrap) + Part B (half-panel split) + Part C acceptance; the **pre-registered-floor rule**: the gate's floor must equal the brief's full-panel floor, "no separate 'regime floor' is permitted — that would be a hidden parameter through which post-hoc fitting could enter."
- **[`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`](pre-registration/2026-07-13-prop-survivor-scoring-prereg.md) @ `be6dda6`** — frozen floor **bust ≤ 3.0% AND P(pass) ≥ 50%**. Not re-decided here.
- **[`docs/adr/2026-07-23-c1-rung-selection-ev-objective.md`](adr/2026-07-23-c1-rung-selection-ev-objective.md) @ `9ab2e8b`** — §Trigger 1: "Admitting 1.00× (or any rung above 0.50×) requires a **new** pre-registered both-halves regime re-MC showing that rung PASSES **both** halves." §Trigger-check schedule: "regime re-MC **on demand** when a higher rung is proposed (**no calendar gate**)." §Phase 2 names the full downstream chain (admitting ADR + B6 re-run + B7). **This brief is the instrument that ADR authorizes; it is not a new licence.**
- **[`lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md`](../../lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md) @ `d85c10c`** — the incumbent result the reproduction control must match: **1.00× GATE FAIL** (Tradeify H1 bust 4.37% / bootstrap-95th 10.37%; MFFU 4.36% / 10.33%), **0.50× GATE PASS** (H1 4.37%→0.14%; boot-95th 10.37%→0.77%; pass-5th 95.76%).
- **[`docs/adr/2026-07-11-discovery-campaign-defaults-ratified.md`](adr/2026-07-11-discovery-campaign-defaults-ratified.md) @ `ba943a1`** — Default #1 (temporal OOS axis: IS 2010-01-01→2018-12-31 parent; **statistical OOS 2019-05-06→present**). **Read specifically to rule it OUT as authority here:** this ADR governs *discovery campaigns*; Class-S existing-strategy books are out of screen scope (haircut pre-reg §7: "Class S is out-of-screen-scope"). Default #1 therefore does **not** bind the c1 panel — §1 states the boundary this brief actually relies on.
- **[`lab/discovery/cost_mnq.py`](../../lab/discovery/cost_mnq.py) @ `e1c51f0`** — read for the sibling finding only (`SLIPPAGE_TICKS_PER_SIDE = 1.0`, L24, unmeasured). **Out of scope for this brief**; recorded in §2 so it is not silently bundled.

**Databento availability + cost, measured this session (2026-07-23, free metadata endpoints, no billing):**

| Query (`MNQ.v.0` / `MYM.v.0`, continuous, GLBX.MDP3) | Result |
|---|---|
| `ohlcv-1m`, 2019-05-06 → 2020-07-01 | **$0.0000** — MNQ 398,906 records; MYM 373,146 records |
| dataset floor, all bar/quote schemas | 2010-06-06 (so native micro coverage from contract launch is present) |
| `tbbo` / `mbp-1`, 1 instrument-month | **$0.0000** (mbp-1 = 58.4 GB, still $0) |
| `mbp-10`, 1 instrument-month | **$115.36** — the billing boundary; out of scope here |

**§0 gap — declared, not papered over (Trap #13).** The two byte-pinned panel CSVs are gitignored vendor data and are **absent from this worktree** (`core/data/tv_exports/cme/` contains only `SHA256SUMS`). I therefore **could not read the panel's actual first trade date.** The widely-cited "panel starts 2020-07-01" is Tier-3 ([`STATE.md`](../../STATE.md), which describes the *BAR EXPORT* panels, a different artifact from the List-of-Trades panels pinned above). **The panel's true first trade date is a Phase-0 blocking read (§7 P0.1), not an input to this brief.** Every claim below is conditioned on it; if P0.1 shows the panel already reaches 2019-05-06, this brief closes immediately as moot.

---

## §1 — Context & motivation

On 2026-07-23 the operator closed Q-BUSTGATE-1 `FALSIFIED`, ratified **EV/dollar-day** as the c1 rung-selection objective (fork B), and then — because the already-run both-halves regime gate **FAILS 1.00×** (H1 chop bust 4.37%, bootstrap-95th 10.37%, both above the frozen 3.0% floor) and **PASSES 0.50×** — chose *"keep 0.50× / accept NO-GO"*. The 08-08 calendar dependency was removed: the regime result, not a date, was the real gate.

So a single number — the **H1 chop-half bust on a ~3-year panel** — is the sole blocker on a rung the ratified EV objective otherwise prefers, and which Q-FUNNEL-1 measured as materially better on 2 of 4 RESOLVED trigger points. That number deserves to be load-bearing on its own merits and not on an accident of tooling.

It may be exactly that. The panel is a TradingView List-of-Trades export (§0); **its start date was set by how far TradingView's export reached, not by any methodological choice anyone recorded.** No brief, ADR, or pre-registration in the repo selects that boundary — it is a vendor artifact. Meanwhile the H1 bootstrap-95th of 10.37% against a 3.0% floor is a very wide band, which is what a noise-dominated estimate on a short single-episode partition looks like.

The non-arbitrary boundary for these two instruments is not a vendor's reach — it is **2019-05-06, the date MYM and MNQ began trading.** That date cannot be shopped: it is the first instant the instruments existed. Databento carries both natively from launch, at $0.00 (§0).

**This brief does not assume databento is the answer.** If TradingView can itself export back to 2019-05-06, TV is the correct source — native engine, no port, no parity risk ([[lesson_offline_fill_port_inflates_native_tv_arbiter]]). Source selection is a Phase-0 determination (§7 P0.3), not a premise.

---

## §2 — Prior art / lineage

- **[`docs/adr/2026-07-23-c1-rung-selection-ev-objective.md`](adr/2026-07-23-c1-rung-selection-ev-objective.md)** (`Accepted`) — authorizes exactly this instrument (§Trigger 1, §Phase 2), on demand, with no calendar gate. Its §5 forbids treating the ADR itself as authorization to flip to 1.00×; this brief inherits that constraint verbatim (§5).
- **[`class_s_c1_haircut_regime_remc` pre-reg](pre-registration/2026-07-16-class-s-c1-lifecycle-haircut-regime-remc-preregistration.md)** (`FROZEN`, signed 2026-07-16) + [RESULTS](../../lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md) — the incumbent verdict. **Byte-unedited and not re-opened** (Trap #12): this is a *fresh* pre-registration on a *different panel*, not an amendment.
- **[`docs/adr/2026-06-07-decompound-remc-hold.md`](adr/2026-06-07-decompound-remc-hold.md)** — the standing precedent that this book family's risk is **regime-split**, and that the chop half is where every candidate dies. Establishes the prior that extending the panel backward into more chop should make the gate *harder*, not easier (§5).
- **Q-COMPOSE-1** (`FALSIFIED`) — H1 killed the breadth lever too (bust 54–68%). H1 is the program's universal binding partition; that is why its sample length is worth interrogating once, properly.
- **[[lesson_offline_fill_port_inflates_native_tv_arbiter]]** + **[[lesson_offline_port_needs_real_source_anchor]]** — govern the databento branch: an offline port must be anchored on a real-source overlap before its extension window is trusted. Encoded as the §6 `AMBIGUOUS` route and §7 P0.4.
- **[[lesson_full_panel_masks_regime_split]]** / **[[lesson_snag_best_of_k_anchor_graveyard]]** — the failure mode this brief is most at risk of. Addressed structurally in §4 (two-sided hypothesis) and §5 (first forbidden move).
- **Out of scope, recorded so it is not bundled:** [`lab/discovery/cost_mnq.py`](../../lab/discovery/cost_mnq.py) `SLIPPAGE_TICKS_PER_SIDE = 1.0` is an unmeasured constant carrying ~35–45% of the round-trip cost hurdle, now measurable at $0 via `tbbo` (§0). It is a **separate question** and must not ride this brief — bundling it would make two verdicts share one gate (Trap #11).

---

## §3 — Question

**Pre-Q gate test:** the symptom-only rephrase is *"the number blocking the rung rests on a panel whose start date nobody chose"* — no fix is baked in; source and disposition are both left open. Passes.

**Q-C1PANEL-1:** What determines the c1 regime gate's panel start date, and does the H1 partition verdict — the sole blocker on any rung above 0.50× — survive extension of the panel to the MYM/MNQ contract-launch date?

---

## §4 — Falsifiable hypothesis (H-C1PANEL)

**H-C1PANEL — if**, on the extended panel (start = **2019-05-06**; every other gate input inherited byte-unchanged per §3 of the pre-registration), the both-halves regime gate returns **the same verdict for both arms** as the incumbent 2026-07-17 result — **1.00× FAIL and 0.50× PASS** — **then** the H1 verdict is panel-robust, the incumbent rung selection stands on strengthened evidence, and **no rung change is licensed in either direction**.

**Otherwise** the verdict is panel-sensitive, and the *direction* of the change fixes the disposition:
- 1.00× PASSES all partitions × both tiers **and** 0.50× still PASSES → a fresh both-halves PASS exists; emit the decision-ready packet for the EV-ADR §Phase-2 chain (admitting ADR + B6 re-run + B7). **This brief does not itself change live sizing.**
- 0.50× FAILS any partition → the **live rung is unsupported on the better-powered panel** and must be reconsidered **downward** to 0.25×.

**Accept H-C1PANEL if:** extended-panel verdicts == {1.00×: FAIL, 0.50×: PASS}, with the reproduction control matching §0's incumbent numbers exactly at reported precision (seeds are fixed — see pre-registration §4a).

**Falsifier — H-C1PANEL is FALSIFIED if:** either arm's verdict flips on the extended panel. The falsifier is **two-sided by construction**: it fires on `1.00× FAIL → PASS` (panel was too short to admit the higher rung) and equally on `0.50× PASS → FAIL` (panel was too short to *reject* the live rung, which then moves down to 0.25×). A falsifier that can only pay in one direction would not be a falsifier — this is the structural defence against the panel-shopping trap ([[lesson_snag_best_of_k_anchor_graveyard]]).

**Ambiguous-hold if:** the reproduction control fails to reproduce the incumbent exactly, **or** the §7 P0.4 source-fidelity parity gate fails, **or** P0.1 shows the panel already reaches 2019-05-06 — the first two indicate a harness/port defect and the third moots the premise; none licenses a panel verdict.

---

## §5 — Forbidden moves

- **Running this as "re-run the gate until 1.00× passes."** The single most tempting move here, and the one that would void the brief. Three structural defenses, all binding: (1) the hypothesis is **two-sided** — a panel-sensitive result can force the live rung *down* to 0.25×, so the test can cost rather than pay; (2) the panel boundary is the **contract-launch date**, a fact that cannot be shopped, not a tuned start; (3) the added window is 2019-05→2020-07 — pre-COVID grind plus the March-2020 crash — which on the decompound-HOLD prior should make the chop half **harder**. If any of the three is weakened during execution, the run is void.
- **Choosing the panel start by trying candidates.** Exactly one start date is admissible: **2019-05-06**. Testing 2019-05 and then 2018 or 2020 and reporting the best is best-of-K on the panel axis ([[lesson_snag_best_of_k_anchor_graveyard]]).
- **Citing Campaign-Default #1 as the authority for 2019-05-06.** It is not — Class-S is out of its screen scope (§0). The justification is the contract-launch date and nothing else; borrowing a ratified-sounding rule that does not apply would be false grounding.
- **Amending the frozen 2026-07-16 haircut pre-registration** to add a panel arm. Trap #12 — that pre-reg stays byte-unedited; this is a fresh instrument.
- **Moving the floor, the split rule, the bootstrap parameters, the tiers, the engine seeds, or `C1_ALLOCS`.** Only the panel start changes. In particular the split stays **index-midpoint** even though extension moves *both* halves — re-deciding the split rule while the panel changes would confound the two.
- **Re-weighting the 0.70%/0.37% book** to help H1 — forbidden by the parent candidate §5 and unchanged here.
- **Trusting a databento-derived extension without the overlap parity gate.** The port must reproduce the byte-pinned TV trade list on 2020-07→2026-07 before the 2019-05→2020-07 window counts ([[lesson_offline_port_needs_real_source_anchor]]). No operator-override path on this one: unlike F3's CFD-vs-futures size-coupling, a port/source mismatch has no benign mechanism.
- **Bundling the `SLIPPAGE_TICKS_PER_SIDE` measurement into this run** (§2) — separate question, separate gate.
- **Treating any verdict here as go-live authorization.** Rail arm (B7) stays gated on M1 `RESOLVED` and its own operator GO, independent of this brief.

---

## §6 — Gate criteria

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED-PANEL-ROBUST` | Extended-panel verdicts == {1.00× FAIL, 0.50× PASS}, all partitions × both discharge tiers, reproduction control matching | Rung stays **0.50×**. The 1.00× question is **closed on strengthened evidence**; no further panel re-runs licensed absent a new instrument or new data. |
| `RESOLVED-ADMITS-HIGHER` | 1.00× clears floor on **all** partitions × **both** tiers on the extended panel **AND** 0.50× still clears | A fresh both-halves PASS exists. Emit decision-ready packet → EV-ADR §Phase-2 chain (admitting ADR + B6 re-run + B7). **No live sizing change from this brief.** |
| `FALSIFIED-RUNG-UNSUPPORTED` | 0.50× fails the floor on any partition × either tier on the extended panel | Live rung unsupported on the better-powered panel → open the admitting decision at **0.25×**; notify before any B7 arm. |
| `AMBIGUOUS` | Reproduction control misses the incumbent beyond MC noise, **or** P0.4 parity gate fails, **or** P0.1 shows the panel already starts ≤2019-05-06 (question moot) | Harness/port/premise defect — **no panel verdict**. Close with the defect recorded; no rung movement in either direction. |

Exact numeric thresholds, noise bands, and the parity tolerance are pinned in the companion pre-registration (§8) and are **frozen before Phase 1**.

---

## §7 — Execution plan

**Phase 0 — blocking, free, no pull and no port.** Any P0 failure closes the brief before spend.

- **P0.1 — panel truth.** Read the two byte-pinned CSVs in the primary checkout; report first/last trade timestamps and trade counts per leg. **If the panel already reaches 2019-05-06, close `AMBIGUOUS` (moot) immediately.**
- **P0.2 — boundary cause.** Determine *why* the panel starts where it does: TV data-history depth for `MYM1!`/`MNQ1!`, account-tier bar cap, or an export-time choice. Record the finding — it is the evidence that the boundary is an artifact rather than a decision.
- **P0.3 — source selection (operator-verifiable, decides the whole cost profile).** Can TradingView export `MYM1!`/`MNQ1!` 15m List-of-Trades back to 2019-05-06?
  - **YES → TV is the source.** Re-export, re-pin sha256 + `SHA256SUMS`, done. **No port, no parity gate, no databento.** Cheapest and highest-fidelity — native engine is the arbiter.
  - **NO → databento is the source**, and P0.4 binds.
- **P0.4 — (databento branch only) parity gate.** Build the offline port of the two venue editions; reproduce the byte-pinned TV trade list on the **2020-07→2026-07 overlap** to the pre-registered tolerance. **Fail ⇒ `AMBIGUOUS`, stop — the extension window is never run.**

**Phase 1 — extension.** Source the 2019-05-06→panel-start window (TV re-export, or the two $0.00 databento pulls estimated in §0), extend the panel, re-pin manifests in the same commit per the vendor-data integrity gate.

**Phase 2 — reproduction control.** Re-run the gate on the **incumbent** panel at 1.00× and 0.50×; assert it reproduces §0's numbers within the pre-registered noise band. Mismatch ⇒ `AMBIGUOUS`, stop.

**Phase 3 — the two arms.** Run 1.00× and 0.50× on the extended panel, all partitions × both discharge tiers, engine/floor/split inherited unchanged.

**Phase 4 — verdict.** Adjudicate §6 against the frozen pre-registration; land `RESULTS.md` under `lab/analysis/c1_panel_extension_2026-07-<dd>/` citing this brief and the pre-registration by path; produce the §9 closure artifact.

Execution may be delegated to a frozen-spec executor per the CC/Cursor surface-allocation ADR; **adjudication (§6) returns to CC.**

---

## §8 — Verdict pre-registration

[`docs/briefs/pre-registration/Q-C1PANEL-1-verdict-preregistration.md`](pre-registration/Q-C1PANEL-1-verdict-preregistration.md) — carries the §6 table plus exact thresholds, the frozen panel definition, the noise band, and the parity tolerance.

Pre-registration commit hash: **`6674c32`** (2026-07-23 17:55:25 -0400)
Pre-registration date: **2026-07-23** (signed §9 / JA)
**No Phase-1 step ran.** The freeze commit predates every Phase-0 read — the audit property held, and P0.1 halted the instrument before any spend.

---

## §9 — Closure record format

- `RESOLVED-*` → `docs/briefs/closures/Q-C1PANEL-1-closure-resolved.md`
- `FALSIFIED-RUNG-UNSUPPORTED` → `docs/briefs/closures/Q-C1PANEL-1-closure-falsified.md`
- `AMBIGUOUS` → `docs/briefs/closures/Q-C1PANEL-1-closure-ambiguous.md`, with the defect (parity / reproduction / mootness) named explicitly

Every closure records: verdict, extended-panel numbers vs the frozen floor, incumbent-vs-extended verdict pair for both arms, the P0.2 boundary-cause finding, the source actually used, and — if the databento branch ran — the realized parity numbers.

---

## §10 — Audit hooks (runnable)

```bash
# 1. Signature-before-run: no Phase-1 step may run while the pre-reg is unsigned.
grep -n "SIGNED / FROZEN: ____" docs/briefs/pre-registration/Q-C1PANEL-1-verdict-preregistration.md \
  && echo "STILL DRAFT — no pull, no port, no arm" || echo "signed"

# 2. Incumbent pre-reg is byte-unedited (Trap #12).
git log --oneline -- docs/briefs/pre-registration/2026-07-16-class-s-c1-lifecycle-haircut-regime-remc-preregistration.md

# 3. Incumbent numbers the reproduction control must match.
grep -n "4.37\|10.37\|0.14\|0.77" lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md | head

# 4. Frozen floor unmoved by this brief.
grep -n "3.0%\|50%" docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md | head -3

# 5. Only the panel changed — allocs/split/bootstrap untouched.
grep -n "C1_ALLOCS\|N_PANELS_DEFAULT\|BLOCK_SIZE_BDAYS\|BOOT_SEED" \
  lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_regime_gate.py \
  lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_scoring.py | head

# 6. Panel pins moved only if the panel was legitimately re-sourced (expect delta ONLY post-Phase-1).
grep -n "MYM1!\|MNQ1!" core/data/tv_exports/cme/SHA256SUMS | head

# 7. No extension RESULTS exist yet (expected while DRAFT).
ls lab/analysis/ | grep -i "c1_panel_extension" || echo "no extension run yet (expected pre-signature)"

# 8. Databento cost re-check — the two Phase-1 pulls must still estimate $0.00.
PYTHONPATH=lab .venv-research/Scripts/python -m databento_fetch.db_fetch estimate \
  --symbols MNQ.v.0 --stype continuous --schema ohlcv-1m --start 2019-05-06 --end 2020-07-01 | grep cost
```

---

## Verification

```bash
# Discipline checks — repo-side mechanical subset
PYTHONIOENCODING=utf-8 python scripts/check_brief.py \
  docs/briefs/Q-C1PANEL-1-c1-regime-panel-start-boundary.md --type inquire

# §0 anchors (Rule-0 confirmation)
git log -1 --format='%h %ci' -- lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_regime_gate.py  # 163b0b5
git log -1 --format='%h %ci' -- lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_scoring.py      # f8f8db1
git log -1 --format='%h %ci' -- lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md                 # d85c10c
git log -1 --format='%h %ci' -- docs/methodology/regime_robustness_gate.md                                        # f2be990
git log -1 --format='%h %ci' -- docs/adr/2026-07-23-c1-rung-selection-ev-objective.md                             # 9ab2e8b
git log -1 --format='%h %ci' -- docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md           # be6dda6

# Cross-reference: the EV ADR really does authorize an on-demand fresh re-MC
grep -n "fresh both-halves\|on demand" docs/adr/2026-07-23-c1-rung-selection-ev-objective.md
```

---

## Pre-Lock Checklist

- [x] §0 paths read and anchored; the one unread artifact (gitignored panel CSVs) declared as a Phase-0 blocking read, not assumed
- [x] §3 passes the symptom-only rephrase test
- [x] §4 hypothesis binary **and two-sided** (can force the rung down)
- [x] §5 forbidden moves genuinely tempting — the first one is the move this brief most resembles
- [x] §6 gates have specific triggers; numerics deferred to the frozen pre-registration
- [ ] §8 pre-registration signed + committed BEFORE Phase 1 — **open**
- [x] §10 audit hooks runnable
- [ ] Verification block executed — **run at freeze**

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-23 | Drafted `OPEN — DRAFT (pre-lock)`. Panel start identified as an unrecorded vendor artifact; boundary fixed at the MYM/MNQ contract-launch date 2019-05-06; hypothesis made two-sided; source selection (TV vs databento) deferred to a blocking Phase 0. Campaign-Default #1 explicitly ruled out as authority. | Joshua (direction) + Claude Code (Opus 4.8) |
