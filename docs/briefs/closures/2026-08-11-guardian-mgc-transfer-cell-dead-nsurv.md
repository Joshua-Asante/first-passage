# Guardian→MGC transfer cell — CLOSURE: `DEAD(N-SURV)` (exploratory grade; margin-decisive)

**Verdict:** `DEAD(N-SURV)` · 2026-08-11 · **$0.00 new spend · K=1 cell score already landed · no manifest · no pull**
**Pre-registration:** [`2026-08-11-guardian-mgc-transfer-cell-prereg.md`](../pre-registration/2026-08-11-guardian-mgc-transfer-cell-prereg.md) — **retroactive** (authored after the score; ordering disclosed in the PREREG header)
**Pursuit:** [`b8`](../../pursuits/b8-guardian-mgc-transfer-lane.md) — Standing flipped **PARK → SUBTRACT** by this closure
**Parent shape:** [Q-TXG-1 §5 Phase B](../../superpowers/specs/2026-08-11-transfer-expression-grid-design.md) cell kill-chain (per-cell closure; **not** a grid-level H_A / election decision)
**Precedent:** [`ops/instruments/6J.md`](../../../ops/instruments/6J.md) J4b — same trailing-survival failure class at Tradeify Select 100K; this cell's overshoot is larger (best half 16.5% vs J4b best cell 3.88%)
**Live effect:** none on the rail or locked book. Cell is dead as a transfer candidate under the frozen N-SURV floor. No `core/` / Pine / allocation / `dd_protection` / firm_rules / Q-TXG-1 compile change by this closure.
**Artifacts:** v0.1–v0.3 CARDs + hash-pinned prototypes (measurement session); N-SURV via `lab/research_utils/nsurv_channel.py` on the v0.3 panel (N=329 / daily n=276)

---

## 1. Verdict against the frozen gate (PREREG §5)

| §5 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `CANDIDATE-proposal` | bar-derived N-SURV clears bust ≤3.0% ∧ P(pass)≥50% on full + both halves | not reached (exploratory inputs; all partitions fail bust) | — |
| **`DEAD(N-SURV)`** | any partition fails §2.2 bust or pass floor | Full **42.2%** bust / 57.8% pass; H1 **72.4%** / 27.6%; H2 **16.5%** / 83.5% — bust ceiling missed on **every** partition (5.5×–24×) | **✓** |
| `AMBIGUOUS` | bar-derived bust in (3.0%, 3.2%] noise band | not reached | — |

Frozen floors (cited, not re-decided): [`2026-07-13-prop-survivor-scoring-prereg.md`](../pre-registration/2026-07-13-prop-survivor-scoring-prereg.md) — bust ≤ **3.0%** ∧ P(pass) ≥ **50%** at `Tradeify_Select_100K`.

**Pass-floor note:** H2 clears P(pass) (83.5%) and full clears it (57.8%); H1 fails it (27.6%). The binding kill is the **bust ceiling** on all three partitions — including the better half at 16.5%.

## 2. What the pre-registration predicted vs what happened

The retroactive PREREG's disclosed prior was already `DEAD(N-SURV)`. Measurement matched that prior. No surprise on direction.

**Two caveats remain named (epistemic grade, not verdict-rescue):**

1. **Half-boundary 2024-07-02** was an unpre-registered midpoint-by-day-count split, not a pre-registered regime date.
2. **`intraday_low`** was approximated from each trade's Adverse-Excursion figure (attributed to entry date), not genuine bar-level daily equity troughs — the input `nsurv_channel.py` wants and W1 used.

**Settled vs still-formalizable:**

| Settled by margin | Not settled as decision-grade instrumentation |
|---|---|
| Qualitative kill: trailing-DD survival fails this cell at the frozen ≤3.0% ceiling on every partition | Exact bust point estimates under true bar-derived `intraday_low` |
| Parameter-retune rescue is forbidden and would not be "transfer" | A genuine bar-derived re-run could *formalize* the FAIL (or, remotely, flip it) |

The margin (H2 5.5× over ceiling; full ~14×; H1 ~24×) is large enough that no plausible refinement of the AE→trough approximation is expected to produce a PASS. A bar-derived re-run is the honest way to make the FAIL instrumentation-grade; it is **not** owed as a rescue attempt, and a FAIL-confirming re-run would not reopen the cell.

## 3. What this closure does NOT license

- Killing **MGC the instrument** (ENV-1 / instrument-lane posture is separate; event-window-reversal is already DEAD on its own record).
- Killing **Guardian v5.5** on XAUUSD or any non-MGC expression.
- A Q-TXG-1 grid H_A EMPTY / transfer-lane-exhausted board write (this is one cell; the grid's compile + election process is untouched).
- Treating Aegis→6J's PARKED residual as also SUBTRACT (different margin; different standing).
- Re-tuning locked Guardian parameters, loosening the 3.0% floor, or shopping firms to launder the bust.
- Reading the exploratory score as a CANDIDATE or as a live-sizing input.

## 4. Defects found in the frozen brief (recorded, not repaired)

- **Ordering defect, disclosed:** PREREG authored after measurement. Recorded in the PREREG header; not repaired by back-dating. Future Q-TXG-1 Phase-B cells must freeze the cell PREREG *before* panel scoring (design §5 step 1).
- **Pre-reg-before-search limb (b8 re-entry):** v0.1–v0.3 execution-mechanics work preceded any cell PREREG. Charitably Class-S-allowed (no locked parameter touched — CARD record); formally the limb was open until this artifact. Discharged here for closure purposes only.

## 5. Lesson candidates

**Candidate (watch):** *margin-decisive exploratory FAIL can close a cell without waiting for instrumentation-grade inputs when every partition clears the ceiling by ≥5× and the approximation's plausible bias cannot reach the floor.* Below the two-incident bar as a standalone lesson — one cell, one session. The Aegis→6J J4b case (1.3× over) correctly stayed measurement-PARKED; this case (5.5×+) justifies DEAD/SUBTRACT. Watch for a second firing before promoting.

No new methodology lesson filed.

---

## Iterate — loop exit (MANDATORY)

- **Verdict used:** `DEAD(N-SURV)` (bust ceiling; all partitions)
- **Model update:** R6 parked Guardian-MGC because it was **data-blocked**, not adversely resolved. The bar-export limb is now discharged and the survival limb fails decisively — the parked-optionality reading no longer holds. Same kill class as Aegis→6J J4b (trailing geometry at Tradeify Select 100K), more severe: best half 16.5% vs J4b's best cell 3.88%. Transfer without locked-parameter edits is not a survival free lunch.
- **Next:** STOP
- **Routing:** STOP — cell dead; pursuit SUBTRACT. Q-TXG-1 may still compile/elect *other* OPEN cells under its own Block-1/2 process; that is not a successor of this cell.
- **Entry packet:** n/a — STOP.
- **Stop rule / re-proposal bar:** **new mechanism evidence** for a Guardian-family metals expression (or a different mechanism × MGC cell under a fresh Q-TXG-1 election + cell PREREG) — **not** a locked-parameter retune, **not** a re-read of the AE-approximated score, **not** firm-shopping, **not** amending the 3.0% floor. A genuine bar-derived N-SURV re-run that somehow cleared ≤3.0% on full + both halves would be the only instrumentation path that could challenge this verdict; given the 5.5×–24× margin it is not treated as an open rescue ticket.
- **Board write:** `docs/pursuits/b8-guardian-mgc-transfer-lane.md` Standing PARK→SUBTRACT · `STATE.md` forward-trigger line · `docs/SESSIONS.md` `2026-08-11z` · `docs/rejected_candidates.md` registry row — this pass.

- **Registry:** rejected_candidates.md — ### Guardian→MGC transfer cell (R7 / b8) — DEAD(N-SURV)

## §10 audit-hook discharge

```text
lab/analysis Guardian-MGC N-SURV after 2026-08-11          NONE  (exploratory numbers stand)
PREREG ordering honesty present                           OK    header block
CARD port mapping = execution-mechanics only              OK    v0_1/v0_2/v0_3 CARD provenance
frozen floors unmoved (bust≤3.0%, pass≥50%)               OK    2026-07-13 prereg cited
numbers cited (42.2 / 72.4 / 16.5)                        OK    pursuit Residuals + this closure
Iterate tokens                                            OK    check_closure_disposition.py
core/ / firm_rules / dd_protection / Pine untouched       OK    docs-only pass
Q-TXG-1 grid compile/election untouched                   OK    per-cell closure only
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-11 | Closure authored; b8 SUBTRACT; registry + STATE + SESSIONS | Cursor (operator-directed) |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md
rg -n "Standing:" docs/pursuits/b8-guardian-mgc-transfer-lane.md   # SUBTRACT
rg -n "DEAD\(N-SURV\)|42\.2%" docs/briefs/closures/2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md
```
