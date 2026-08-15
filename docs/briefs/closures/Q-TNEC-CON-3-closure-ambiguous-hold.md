# Q-TNEC-CON-3 — CLOSURE: `AMBIGUOUS-HOLD` (ITERATE — lane packet)

**Verdict:** `AMBIGUOUS-HOLD` — explore scored; neither FALSIFIED nor live-pass; §6 → **ITERATE**
**Closed (explore record):** 2026-08-10
**Pre-registration:** [`PREREG_G0.md`](../../../lab/analysis/c1/mnq_tnec_con3_htf_native_break_2026-08/PREREG_G0.md) frozen `0491284` · parent [`brief`](../Q-TNEC-CON-3-htf-native-compression-break-scoping.md)
**Explore GO:** operator in-session 2026-08-10 — [`EXPLORE_GO.md`](../../../lab/analysis/c1/mnq_tnec_con3_htf_native_break_2026-08/EXPLORE_GO.md) (window / placebo / aux downgrades declared pre-score)
**Explore commit:** `ba83282`
**Spend / K:** $0.00 · `K_intrinsic=1` disclosure only · Cap seat **not claimed**
**Live effect:** none — CONFIRM (2025-09-01→2026-08-05) reserved and **unread**; no rail / Pine / arming
**Artifacts:** [`RESULTS.md`](../../../lab/analysis/c1/mnq_tnec_con3_htf_native_break_2026-08/RESULTS.md) · [`RESULTS.json`](../../../lab/analysis/c1/mnq_tnec_con3_htf_native_break_2026-08/RESULTS.json) (gitignored machine record)
**Lane:** [`dense-1m entry-mechanism lane`](../../spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md) · consecutive FALSIFIED counter unchanged (**1/3** = CON-1 only)

---

## 1. Verdict against the frozen gate

| Route | Trigger | Actual | Fired? |
|---|---|---|---|
| `FALSIFIED` | both arms n≥100 ∧ CI upper < 0 | CI uppers **+0.2256** / **+0.1885** | — |
| `SHAPE-CLEAR-CANDIDATE` / live pass | arm: CI lo>0 ∧ mean>0 **and** placebo p_emp<0.05 ∧ annSR≥0.650 ∧ halves agree | long mean +0.073 but CI lo **−0.073**; placebo 0.165; annSR 0.405; short mean −0.026 | — |
| `AMBIGUOUS-HOLD` | otherwise (VOID / halves / magnitude as frozen) | long halves agree (+0.117/+0.030); short halves flip; both CIs straddle 0 | ✓ |

H-CON-3 (brief §4: ≥1 arm CI entirely above 0 and DSR ≥ 0.650) is **not confirmed**.

Frozen brief §6 disposition for `AMBIGUOUS-HOLD`: **`ITERATE` — lane packet (not θ-retune)**. This closure discharges that branch (default; not a Trap-#12 amendment).

---

## 2. Predicted vs happened

Cheap falsifier (full-panel, pre-freeze): long +0.063 / short −0.035, both CIs straddle, coverage 91.6% → `CHEAP_FALSIFIER_OK`.

EXPLORATION (≤2025-08-31, n powered): **same shape at the frozen cell** — long +0.073 CI straddles; short −0.026; coverage 92.1%. What the falsifier could not see under the explore split:

- Structural stops ≈ **29.2 pt** (vs CON-2 fixed G=10) → RT 1.41 is a smaller R-tax; mean signed gross ≈ **+4.14 pt** (CON-2 was ~+0.9–1.0 pt).
- Still **gross/(4×RT) ≈ 0.73×** — cost-law bar uncleared.
- Long halves **agree** positive (CON-2 both arms flipped) — temporal + structural geometry moved stability, not SHAPE-clearance.
- Declared aux: placebo and annSR both fail the live-pass bar on the long arm even before CI.

---

## 3. What this closure does NOT license

Reading CONFIRM · Cap claim · retuning `K_NARROW` / `NARROW_MULT` / median-20 / HTF minutes / first→N (Trap #12) · post-hoc **long-only** slice of this panel as a free pass · sign-invert to fade · reintroducing 1m / fixed G=10 · deploy / Pine / arming / `LEG_MAP`.

---

## 4. Defects found in the frozen packet (recorded; repaired at GO, not post-hoc)

G0 named placebo / halves / DSR limbs the Stage-0 runner did not implement. Gaps closed **at explore GO, before any score**, in `EXPLORE_GO.md`: EXPLORATION end 2025-08-31; within-session R-shuffle declared degenerate under `FIRST_PER_SESSION` → **sign-randomized R** (1000 reps, seed 20260810); annSR ≥ 0.650; live-pass = primary ∧ aux. Defect recorded here; not a limb edit after looking.

---

## 5. Lesson candidates

**2026-08-10 — HTF-native structural-stop + first/session raises gross and half-stability vs dense-1m G=10, without clearing SHAPE or the 4× cost-law bar.** Cost: one explore-GO session on MNQSEL-2 cache. Watch: a CON-4 that only rephrases compression-break under a new θ is the exhausted move; the residual wall is still **cost geometry / new mechanism**, not CI rescue by retune. Below the two-incident bar as phrased; watch (pairs with CON-2's ~1 pt gross lesson).

---

## Iterate — loop exit (MANDATORY — closure incomplete without it)

- **Verdict used:** `AMBIGUOUS-HOLD` (CI straddles; aux fail live-pass; long point+/halves agree)
- **Model update:** Trading the **5m break itself** with a structural quiet-extreme stop and first/session selectivity is a real geometric upgrade on CON-2 (gross ~4 pt vs ~1 pt; long halves stable) but still fails every SHAPE limb that gates promotion. The cell is not dead by the FALSIFIED trigger; it is also not promotable. The lane's binding residual remains **cost geometry or a new entry mechanism** — not θ, not fade, not arm-slice.
- **Next:** ITERATE
- **Routing:** ITERATE → **dated packet / operator decision item** (this section's Entry packet). Return target chosen at operator election below — naming ≠ opening. CONFIRM stays unread until a separate confirm GO on a *promoted* cell (none exists).
- **Entry packet:** *(frozen carry-forwards + election; operator GO required to open either branch)*

  ### Carry-forwards (verified; do not re-derive)

  | Item | Value |
  |---|---|
  | Panel / cost | MNQSEL-2 `_mnq_1m.parquet` · $0 reuse |
  | Explore window | sessions ≤ **2025-08-31**; CONFIRM ≥2025-09-01 **virgin to this cell's selection** |
  | Long | n=713 · mean **+0.0733R** · CI [−0.0732, +0.2256] · WR 0.303 · halves +0.117/+0.030 · placebo 0.165 · annSR 0.405 |
  | Short | n=610 · mean **−0.0255R** · CI [−0.2249, +0.1885] · WR 0.228 · halves flip · placebo 0.592 · annSR −0.101 |
  | Geometry | stop_dist ≈ 29.2 pt · gross ≈ +4.14 pt · gross/(4×RT) ≈ **0.73×** |
  | Domain bar | route ① temporal selectivity (ADR 2026-08-10) — answered at G0 |
  | K / Cap | `K_intrinsic=1` disclosure · Cap **unclaimed** |
  | Prior kills | CON-1 FALSIFIED · CON-2 AMBIGUOUS-HOLD non-promotable · HTF-bias→LTF filter FALSIFIED ($0 / no Q-ID) |

  ### Operator election (exactly one; unpaid)

  | Branch | What it does | What it forbids |
  |---|---|---|
  | **A — STOP this catalogue (non-promotable)** | File addendum / status flip to STOP; CONFIRM unread forever for this G0; consecutive AMBIGUOUS closes accumulate; lane may still open CON-4 as a *fresh* Q | Treating long +0.073 as a near-miss to “finish” with θ |
  | **B — Lane continue → CON-4** | Fresh Q-ID + fresh G0 under lane step 1+1a; **new entry mechanism** (door check vs CON-1/2/3 + DEAD + domain bar); parent cheap falsifier before authoring | θ-retune of CON-3 · long-only post-hoc · fade · 1m/G=10 reentry · unanswered binding bar |

  **Default lean (non-binding):** Branch **B** if the operator still wants a TNEC construct on this universe — CON-3's gross upgrade is evidence the *geometry class* can move, not that *this cell* clears. Branch **A** if the operator judges two AMBIGUOUS compression-family cells enough to pause the lane pending a cost-geometry thesis that is not another breakout flavor.

  ### Forbidden re-opens (both branches)

  - Any edit to frozen CON-3 constants after this record.
  - Scoring CONFIRM on CON-3.
  - Cap / Pine / deploy / arming from this packet.
  - A “CON-3b” that is long-only or N-per-session without a **new** a-priori G0 and K charge.

  ### Budget

  $0 · K=0 for this packet. Any CON-4 opens at `K_intrinsic` = its own catalogue size (Cap seat separate).

- **Stop rule / re-proposal bar:** Re-open of *this* HTF-native 5m compression-break G0 requires new **mechanism** evidence or a materially different cost geometry — not `K_NARROW`/`NARROW_MULT`/median/HTF-min/first→N edits, not fade, not long-only cherry-pick on the scored panel. Lane stop-rule (3 consecutive **FALSIFIED**) is **not** fired by this AMBIGUOUS.
- **Board write:** `SESSIONS Open/next: Operator elect CON-3 ITERATE branch A (STOP non-promotable) or B (lane CON-4 fresh mechanism) — packet frozen in this closure. Carry: CapFLOW join+score; weekly token; S2b; F1 2026-11-08; 8 PARK expiries; EVT-1 cell-#3 dead.` Owner: this closure · [`brief`](../Q-TNEC-CON-3-htf-native-compression-break-scoping.md) · [`RESULTS`](../../../lab/analysis/c1/mnq_tnec_con3_htf_native_break_2026-08/RESULTS.md)

---

## §10 audit-hook discharge

```text
PREREG_G0 introducing commit 0491284 precedes explore score ba83282     OK
EXPLORE_GO.md declarations precede RESULTS scored_at                     OK
CONFIRM dropped pre-score (runner EXPLORE_END=2025-08-31)                OK
lib tests 8/8 green pre-run                                              OK
$0.00 / K=1 disclosure / Cap unclaimed / no Pine / no arming             OK
Lane consecutive-FALSIFIED counter = 1/3 (CON-1 only)                    OK
```

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/Q-TNEC-CON-3-closure-ambiguous-hold.md
rg -n "AMBIGUOUS-HOLD" lab/analysis/c1/mnq_tnec_con3_htf_native_break_2026-08/RESULTS.md
rg -n "Next: ITERATE" docs/briefs/closures/Q-TNEC-CON-3-closure-ambiguous-hold.md
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-10 | Closure filed — AMBIGUOUS-HOLD; Next ITERATE; Entry packet freezes operator election A/B (named, not opened) | Cursor + JA |
| 2026-08-10 | **Operator elected Branch B** — lane continue → CON-4 (fresh mechanism). Branch A declined. CON-4 unnamed until mechanism design GO; this election does not open CON-4's G0. | Cursor + JA |
