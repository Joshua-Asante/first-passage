# Q-TNEC-CON-4 — CLOSURE: `AMBIGUOUS-HOLD` (ITERATE — lane packet; lean A STOP)

**Verdict:** `AMBIGUOUS-HOLD` — explore scored; neither FALSIFIED nor live-pass; §6 → **ITERATE**
**Closed (explore record):** 2026-08-11
**Pre-registration:** [`PREREG_G0.md`](../../../lab/analysis/c1/mnq_tnec_con4_pdh_pdl_break_2026-08/PREREG_G0.md) frozen `57dc638` · parent [`brief`](../Q-TNEC-CON-4-pdh-pdl-breakout-scoping.md)
**Explore GO:** operator in-session 2026-08-11 — [`EXPLORE_GO.md`](../../../lab/analysis/c1/mnq_tnec_con4_pdh_pdl_break_2026-08/EXPLORE_GO.md) (window / placebo / aux downgrades declared pre-score)
**Explore commit:** `f9b33aa`
**Spend / K:** $0.00 · `K_intrinsic=1` disclosure only · Cap seat **not claimed**
**Live effect:** none — CONFIRM (2025-09-01→2026-08-05) reserved and **unread**; no rail / Pine / arming
**Artifacts:** [`RESULTS.md`](../../../lab/analysis/c1/mnq_tnec_con4_pdh_pdl_break_2026-08/RESULTS.md) · [`RESULTS.json`](../../../lab/analysis/c1/mnq_tnec_con4_pdh_pdl_break_2026-08/RESULTS.json) (gitignored machine record)
**Lane:** [`dense-1m entry-mechanism lane`](../../spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md) · consecutive FALSIFIED counter unchanged (**1/3** = CON-1 only)

---

## 1. Verdict against the frozen gate

| Route | Trigger | Actual | Fired? |
|---|---|---|---|
| `FALSIFIED` | both arms n≥100 ∧ CI upper < 0 | CI uppers **+0.0352** / **+0.0568** | — |
| `SHAPE-CLEAR-CANDIDATE` / live pass | arm: CI lo>0 ∧ mean>0 **and** placebo p_emp<0.05 ∧ annSR≥0.650 ∧ halves agree | long −0.0066 CI lo −0.0475; short +0.0053 CI lo −0.0458; both placebo/annSR fail | — |
| `AMBIGUOUS-HOLD` | otherwise (VOID / halves / magnitude as frozen) | both CIs straddle 0; long halves agree negative; short halves flip | ✓ |

H-CON-4 (brief §4: ≥1 arm CI entirely above 0 and DSR ≥ 0.650) is **not confirmed**.

Frozen brief §6 disposition for `AMBIGUOUS-HOLD`: **`ITERATE` — lane packet (not θ-retune)**. This closure discharges that branch (default; not a Trap-#12 amendment).

---

## 2. Predicted vs happened

Cheap falsifier (full-panel, pre-freeze): long −0.0048 / short −0.0028, both CIs straddle, coverage 88.0%, mean stop ≈279 pt → `CHEAP_FALSIFIER_OK`.

EXPLORATION (≤2025-08-31): **same near-zero shape** — long −0.0066 / short +0.0053; CIs straddle; coverage 87.8%; mean stop ≈**256.8 pt**; mean signed gross ≈**+1.50 pt**; gross/(4×RT) ≈**0.27×**. The cell is economically flat at the point estimate; the formal FALSIFIED trigger does not fire because CIs still include 0.

---

## 3. What this closure does NOT license

Reading CONFIRM · Cap claim · retuning PDH/PDL definition / first→N / stop geometry (Trap #12) · fade / level-touch attraction · compression-family reentry (CON-2/3) · deploy / Pine / arming / `LEG_MAP`.

---

## 4. Defects found in the frozen packet (recorded; repaired at GO, not post-hoc)

None that change the verdict. Placebo / halves / DSR limbs were implemented in the Stage-0 runner at freeze and declared again in `EXPLORE_GO.md` before score.

---

## 5. Lesson candidates

**2026-08-11 — PDH/PDL through-break with opposite-prior-extreme stops is economically dead under Tradeify RT 1.41 despite clearing the FALSIFIED CI limb.** Cost: one explore-GO session. Watch: third AMBIGUOUS in the dense-1m lane (CON-2 STOP · CON-3 AMBIGUOUS with residual gross · CON-4 flat); another OHLCV breakout flavor is the exhausted move. Below the two-incident bar as phrased; watch.

---

## Iterate — loop exit (MANDATORY — closure incomplete without it)

- **Verdict used:** `AMBIGUOUS-HOLD` (CI straddles; aux fail live-pass; means ≈0; gross 0.27× of 4×RT)
- **Model update:** Changing the entry object from compression-break to PDH/PDL through-break did **not** rescue cost geometry. Wide structural stops (~257 pt) make RT a tiny R-tax, so near-zero net R is near-zero gross — the cell is flat, not a near-miss. Formal non-FALSIFIED is not promotability.
- **Next:** ITERATE
- **Routing:** ITERATE → **dated packet / operator decision item** (this section's Entry packet). Return target chosen at operator election below — naming ≠ opening. CONFIRM stays unread.
- **Entry packet:** *(frozen carry-forwards + election; operator GO required to open either branch)*

  ### Carry-forwards (verified; do not re-derive)

  | Item | Value |
  |---|---|
  | Panel / cost | MNQSEL-2 `_mnq_1m.parquet` · $0 reuse |
  | Explore window | sessions ≤ **2025-08-31**; CONFIRM ≥2025-09-01 **virgin to this cell's selection** |
  | Long | n=737 · mean **−0.0066R** · CI [−0.0475, +0.0352] · WR 0.532 · halves −0.0035/−0.0096 · placebo 0.623 · annSR −0.128 |
  | Short | n=541 · mean **+0.0053R** · CI [−0.0458, +0.0568] · WR 0.481 · halves flip · placebo 0.435 · annSR +0.085 |
  | Geometry | stop_dist ≈ 256.8 pt · gross ≈ +1.50 pt · gross/(4×RT) ≈ **0.27×** |
  | Domain bar | route ① temporal selectivity (ADR 2026-08-10) — answered at G0 |
  | K / Cap | `K_intrinsic=1` disclosure · Cap **unclaimed** |
  | Prior | CON-1 FALSIFIED · CON-2 AMBIGUOUS-HOLD non-promotable · CON-3 AMBIGUOUS-HOLD → Branch B · HTF-bias→LTF FALSIFIED |

  ### Operator election (exactly one; unpaid)

  | Branch | What it does | What it forbids |
  |---|---|---|
  | **A — STOP this catalogue (non-promotable)** — **recommended** | File addendum / status flip to STOP; CONFIRM unread forever for this G0; pause lane default pending a non-breakout thesis | Treating CI-straddle as a near-miss to “finish” with θ |
  | **B — Lane continue → CON-5** | Fresh Q-ID + fresh G0 under lane step 1+1a; **new entry mechanism** (door vs CON-1–4 + DEAD + domain bar); parent cheap falsifier before authoring | PDH/PDL θ · compression reentry · fade · unanswered binding bar · another OHLCV breakout flavor without a stated cost-geometry distinction |

  **Default lean (recommended):** Branch **A**. Means ≈0 and gross 0.27× of the 4× bar make this cell non-promotable in substance; CON-2 already closed STOP on a similar wall. Branch **B** only if the operator still wants a TNEC construct that is **not** another through-break / compression-break OHLCV cell (hold-time mapped; OF modality paused).

  ### Forbidden re-opens (both branches)

  - Any edit to frozen CON-4 constants after this record.
  - Scoring CONFIRM on CON-4.
  - Cap / Pine / deploy / arming from this packet.
  - A “CON-4b” that is long-only or N-per-session without a **new** a-priori G0 and K charge.

  ### Budget

  $0 · K=0 for this packet. Any CON-5 opens at `K_intrinsic` = its own catalogue size (Cap seat separate).

- **Stop rule / re-proposal bar:** Re-open of *this* PDH/PDL RTH with-break G0 requires new **mechanism** evidence or a materially different cost geometry — not PDH/PDL / first→N / stop-geometry edits, not fade, not compression transplant. Lane stop-rule (3 consecutive **FALSIFIED**) is **not** fired by this AMBIGUOUS.
- **Board write:** `SESSIONS Open/next: Operator elect CON-4 ITERATE branch A (STOP non-promotable — recommended) or B (lane CON-5 fresh non-breakout mechanism) — packet frozen in this closure. Carry: CapFLOW join+score; weekly token; S2b; F1 2026-11-08; 8 PARK expiries; EVT-1 dead.` Owner: this closure · [`brief`](../Q-TNEC-CON-4-pdh-pdl-breakout-scoping.md) · [`RESULTS`](../../../lab/analysis/c1/mnq_tnec_con4_pdh_pdl_break_2026-08/RESULTS.md)

---

## §10 audit-hook discharge

```text
PREREG_G0 introducing commit 57dc638 precedes explore score f9b33aa     OK
EXPLORE_GO.md declarations precede RESULTS scored_at                     OK
CONFIRM dropped pre-score (runner EXPLORE_END=2025-08-31)                OK
lib tests 8/8 green pre-run                                              OK
$0.00 / K=1 disclosure / Cap unclaimed / no Pine / no arming             OK
Lane consecutive-FALSIFIED counter = 1/3 (CON-1 only)                    OK
```

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/Q-TNEC-CON-4-closure-ambiguous-hold.md
rg -n "AMBIGUOUS-HOLD" lab/analysis/c1/mnq_tnec_con4_pdh_pdl_break_2026-08/RESULTS.md
rg -n "Next: ITERATE" docs/briefs/closures/Q-TNEC-CON-4-closure-ambiguous-hold.md
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-11 | Closure filed — AMBIGUOUS-HOLD; Next ITERATE; Entry packet freezes election A/B with **recommended lean A STOP** | Cursor + JA |
| 2026-08-11 | **Operator elected Branch B** — lane continue → CON-5 (fresh **non-breakout** mechanism). Branch A declined. CON-5 unnamed until mechanism design GO; this election does not open CON-5's G0. | Cursor + JA |
