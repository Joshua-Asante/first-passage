# Q-TNEC-CON-5 — CLOSURE: `AMBIGUOUS-HOLD` (STOP — non-promotable; OHLCV temporal lane paused)

**Verdict:** `AMBIGUOUS-HOLD` — explore scored; neither FALSIFIED nor live-pass; §6 ITERATE → operator **Branch A STOP** elected 2026-08-12
**Closed (explore record):** 2026-08-11 · **Disposition:** STOP (Branch A) 2026-08-12
**Pre-registration:** [`PREREG_G0.md`](../../../lab/analysis/c1/mnq_tnec_con5_impulse_pullback_vwap_2026-08/PREREG_G0.md) frozen `d5fd9fc` · parent [`brief`](../Q-TNEC-CON-5-impulse-pullback-vwap-reclaim-scoping.md)
**Explore GO:** operator in-session 2026-08-11 — [`EXPLORE_GO.md`](../../../lab/analysis/c1/mnq_tnec_con5_impulse_pullback_vwap_2026-08/EXPLORE_GO.md) (window / placebo / aux downgrades declared pre-score)
**Explore commit:** `a1e5ace`
**Spend / K:** $0.00 · `K_intrinsic=1` disclosure only · Cap seat **not claimed**
**Live effect:** none — CONFIRM (2025-09-01→2026-08-05) reserved and **unread forever** for this G0; no rail / Pine / arming
**Artifacts:** [`RESULTS.md`](../../../lab/analysis/c1/mnq_tnec_con5_impulse_pullback_vwap_2026-08/RESULTS.md) · [`RESULTS.json`](../../../lab/analysis/c1/mnq_tnec_con5_impulse_pullback_vwap_2026-08/RESULTS.json) (gitignored machine record)
**Lane:** [`dense-1m entry-mechanism lane`](../../spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md) · consecutive FALSIFIED counter unchanged (**1/3** = CON-1 only) · **OHLCV temporal-selectivity lane default PAUSED** (Branch A)

---

## 1. Verdict against the frozen gate

| Route | Trigger | Actual | Fired? |
|---|---|---|---|
| `FALSIFIED` | both arms n≥100 ∧ CI upper < 0 | CI uppers **+0.1013** / **+0.0390** | — |
| `SHAPE-CLEAR-CANDIDATE` / live pass | arm: CI lo>0 ∧ mean>0 **and** placebo p_emp<0.05 ∧ annSR≥0.650 ∧ halves agree | long −0.1838 CI lo −0.454; short −0.360 CI lo −0.684; both placebo/annSR fail | — |
| `AMBIGUOUS-HOLD` | otherwise (VOID / halves / magnitude as frozen) | both CIs straddle 0; both halves agree negative | ✓ |

H-CON-5 (brief §4: ≥1 arm CI entirely above 0 and DSR ≥ 0.650) is **not confirmed**.

Frozen brief §6 disposition for `AMBIGUOUS-HOLD`: **`ITERATE` — lane packet (not θ-retune)**. This closure discharges that branch (default; not a Trap-#12 amendment).

---

## 2. Predicted vs happened

Cheap falsifier (full-panel, pre-freeze): long +0.0061 / short −0.4268 (short CI entirely &lt;0 alone), coverage 90.3%, mean stop ≈19.1 pt → `CHEAP_FALSIFIER_OK` (formal both-arm kill did not fire).

EXPLORATION (≤2025-08-31): **both arms mean-negative** — long −0.1838 / short −0.360; CIs straddle; coverage 89.9%; mean stop ≈**17.5 pt**; mean signed gross ≈**+0.61 pt**; gross/(4×RT) ≈**0.11×**; WR ≈11–14%. The cost-geometry distinction vs CON-4 held (tight stops); the edge did not. Formal FALSIFIED does not fire because CIs still include 0 (short upper barely positive on the explore window).

---

## 3. What this closure does NOT license

Reading CONFIRM · Cap claim · retuning bias window / VWAP / first→N / stop geometry (Trap #12) · fade-to-VWAP · through-break / compression-family reentry (CON-1–4) · deploy / Pine / arming / `LEG_MAP`.

---

## 4. Defects found in the frozen packet (recorded; repaired at GO, not post-hoc)

None that change the verdict. Placebo / halves / DSR limbs were implemented in the Stage-0 runner at freeze and declared again in `EXPLORE_GO.md` before score.

---

## 5. Lesson candidates

**2026-08-11 — Tightening the stop via pullback-reclaim (non-breakout) does not rescue Tradeify RT 1.41 when WR collapses.** Cost: one explore-GO session. Watch: fourth AMBIGUOUS in the dense-1m OHLCV temporal-selectivity lane (CON-2 STOP · CON-3 residual-gross AMBIGUOUS · CON-4 flat · CON-5 mean-negative). Changing entry object *and* stop geometry still leaves gross ≪ 4×RT. Below the two-incident bar as phrased; watch — lane default should pause pending a non-OHLCV or non-route-① thesis.

---

## Iterate — loop exit (MANDATORY — closure incomplete without it)

- **Verdict used:** `AMBIGUOUS-HOLD` (CI straddles; aux fail live-pass; both means negative; gross 0.11× of 4×RT)
- **Model update:** Moving from through-break / compression to impulse→pullback→VWAP-reclaim **did** deliver the stated cost-geometry distinction (stop ~17.5 vs CON-4 ~257) and **did not** deliver edge. Low WR under tight stops makes RT a large R-tax; mean-negative R on both arms is non-promotable in substance even though the formal FALSIFIED CI limb misses.
- **Next:** STOP
- **Routing:** STOP — Branch **A** elected (operator election via task start, 2026-08-12). Catalogue non-promotable; CONFIRM unread forever for this G0; dense-1m OHLCV temporal-selectivity lane default **paused** pending a new modality or non-route-① thesis. Branch B declined. Consecutive FALSIFIED counter remains **1/3** (CON-1 only; AMBIGUOUS does not fire the lane stop-rule).
- **Entry packet:** *(frozen carry-forwards; election discharged — Branch A)*

  ### Carry-forwards (verified; do not re-derive)

  | Item | Value |
  |---|---|
  | Panel / cost | MNQSEL-2 `_mnq_1m.parquet` · $0 reuse |
  | Explore window | sessions ≤ **2025-08-31**; CONFIRM ≥2025-09-01 **virgin to this cell's selection** |
  | Long | n=679 · mean **−0.1838R** · CI [−0.4541, +0.1013] · WR 0.138 · halves −0.083/−0.279 · placebo 0.894 · annSR −0.532 |
  | Short | n=631 · mean **−0.3600R** · CI [−0.6841, +0.0390] · WR 0.106 · halves −0.353/−0.367 · placebo 0.975 · annSR −0.805 |
  | Geometry | stop_dist ≈ 17.5 pt · gross ≈ +0.61 pt · gross/(4×RT) ≈ **0.11×** |
  | Domain bar | route ① temporal selectivity (ADR 2026-08-10) — answered at G0 |
  | K / Cap | `K_intrinsic=1` disclosure · Cap **unclaimed** |
  | Prior | CON-1 FALSIFIED · CON-2 AMBIGUOUS STOP · CON-3→B · CON-4→B · HTF-bias→LTF FALSIFIED |

  ### Operator election (exactly one; **Branch A elected** 2026-08-12)

  | Branch | What it does | What it forbids |
  |---|---|---|
  | **A — STOP this catalogue (non-promotable)** — **ELECTED** | File addendum / status flip to STOP; CONFIRM unread forever for this G0; **pause dense-1m OHLCV temporal-selectivity lane default** pending a new modality or non-route-① thesis | Treating CI-straddle as a near-miss to “finish” with θ |
  | **B — Lane continue → CON-6** — **declined** | Fresh Q-ID + fresh G0 under lane step 1+1a; **new entry mechanism** with door vs CON-1–5 + DEAD + domain bar + **stated cost-geometry distinction**; parent cheap falsifier before authoring | Bias/VWAP θ · fade-to-VWAP · through-break / compression reentry · unanswered binding bar · another OHLCV first/session cell without a modality or lever outside {price · hold-time · route-① temporal} |

  **Election record:** Branch **A** — operator election via task start, 2026-08-12. Evidence since freeze strengthened the lean: Q-SCORE-1 Block-1 narrative anchor counted **8 consecutive zero-yield closes** on the short-horizon MNQ microstructure thread since 2026-08-08 (Q-R2VBUCK-1, Q-R2FLOW-1, Q-R2AGRUN-1, Q-MNQDTL-CON-1, Q-TNEC-CON-2/3/4/5) against SNAG anchor 3; sole RESOLVED in-window (Q-MNQSEL-2) resolved a capability, not a candidate ([`PREREG` F4](../../../lab/archive/approach_scoreboard_2026-08/PREREG.md); [`Q-SCORE-1 closure`](Q-SCORE-1-closure-falsified.md)). Tail-exhaustion: next experiment in this domain changes level (horizon / unit of analysis / data class), not catalogue. Lane FALSIFIED counter **unchanged at 1/3**.

  ### Forbidden re-opens (both branches)

  - Any edit to frozen CON-5 constants after this record.
  - Scoring CONFIRM on CON-5.
  - Cap / Pine / deploy / arming from this packet.
  - A “CON-5b” that is long-only or N-per-session without a **new** a-priori G0 and K charge.

  ### Budget

  $0 · K=0 for this packet. Any successor outside the paused OHLCV temporal-selectivity default opens at its own `K_intrinsic` (Cap seat separate).

- **Stop rule / re-proposal bar:** Re-open of *this* impulse-pullback-VWAP-reclaim G0 requires new **mechanism** evidence or a materially different cost geometry — not bias/VWAP/first→N/stop-geometry edits, not fade, not through-break / compression transplant. Lane stop-rule (3 consecutive **FALSIFIED**) is **not** fired by this AMBIGUOUS (counter remains **1/3**). OHLCV temporal-selectivity lane default stays paused until a new modality or non-route-① thesis.
- **Board write:** `SESSIONS Open/next: CON-5 Branch A STOP elected; OHLCV temporal-selectivity lane default paused. Carry: CapFLOW join+score; weekly token; S2b; F1 2026-11-08; 8 PARK expiries; EVT-1 dead.` Owner: this closure · [`brief`](../Q-TNEC-CON-5-impulse-pullback-vwap-reclaim-scoping.md) · [`RESULTS`](../../../lab/analysis/c1/mnq_tnec_con5_impulse_pullback_vwap_2026-08/RESULTS.md)

---

## §10 audit-hook discharge

```text
PREREG_G0 introducing commit d5fd9fc precedes explore score a1e5ace     OK
EXPLORE_GO.md declarations precede RESULTS scored_at                     OK
CONFIRM dropped pre-score (runner EXPLORE_END=2025-08-31)                OK
lib tests 7/7 green pre-run                                              OK
$0.00 / K=1 disclosure / Cap unclaimed / no Pine / no arming             OK
Lane consecutive-FALSIFIED counter = 1/3 (CON-1 only)                    OK
```

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md
rg -n "AMBIGUOUS-HOLD" lab/analysis/c1/mnq_tnec_con5_impulse_pullback_vwap_2026-08/RESULTS.md
rg -n "Next: STOP" docs/briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md
rg -n "Operator elected Branch A" docs/briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-11 | Closure filed — AMBIGUOUS-HOLD; Next ITERATE; Entry packet freezes election A/B with **recommended lean A STOP** (pause OHLCV temporal-selectivity lane default) | Cursor + JA |
| 2026-08-12 | **Operator elected Branch A (STOP)** — operator election via task start, 2026-08-12. Branch B declined. CONFIRM unread forever for this G0; dense-1m OHLCV temporal-selectivity lane default **paused** pending new modality / non-route-① thesis. Cite: 8 consecutive zero-yield closes since 2026-08-08 (Q-R2VBUCK-1, Q-R2FLOW-1, Q-R2AGRUN-1, Q-MNQDTL-CON-1, Q-TNEC-CON-2/3/4/5) vs SNAG anchor 3 (Q-SCORE-1 Block-1 / PREREG F4). Lane FALSIFIED counter **unchanged 1/3**. | Cursor + JA |
| 2026-08-20 | **A single, bounded U1 exception carved out of this pause for `Q-TNEC-CON-4` only** — [`ADR`](../../adr/2026-08-20-dense1m-u1-operator-override-con4-reopen.md) (`Accepted`, operator override). This closure's pause **stands unchanged** for `CON-1/2/3/5` and any future `CON-6+`; U2 (default-open) was not marked. | Claude Code (operator-ratified) |
| 2026-08-20 | **U1 exception spent same day.** `CON-4`'s CONFIRM score returned `AMBIGUOUS-HOLD` (short arm mean **−0.0611R**) — [`RESULTS_CONFIRM.md`](../../../lab/analysis/c1/mnq_tnec_con4_pdh_pdl_break_2026-08/RESULTS_CONFIRM.md). `CON-4` reverts to `U0`; this closure's pause is once again unconditional across the whole lane (`CON-1/2/3/4/5`). Ninth consecutive zero-yield close in the thread this closure's own tail-exhaustion citation named. | Claude Code (operator-ratified run) |
