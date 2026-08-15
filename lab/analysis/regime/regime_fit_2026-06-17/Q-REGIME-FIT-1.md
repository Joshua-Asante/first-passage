> **STATUS: CLOSED 2026-06-17 → see [`RESULTS.md`](RESULTS.md).** Verdict: structural decay RULED OUT
> (signal-level +17.12% static-$200K, INSIDE the envelope); disposition **FIX-EXECUTION** (live ECR −10.2%
> all-in / −53.2% behavioral; account −$1,272). §7.1 window-membership pinned to **entry-date** at closure
> (verdict convention-robust). The body below is the frozen pre-registration, **unedited** (no post-hoc
> changes to window / envelope / threshold — §10 audit answer: No).

---

# Q-REGIME-FIT-1 — Pre-Q: Is the locked book still within model, or has it decayed?
**Type:** Inquire-phase brief (Pre-Q) · **Phase:** Inquire (diagnosis before action)
**Loop:** INQHIORI / OUTER — structural, low-reversibility (gates whether the locked 4-strategy book is held, re-executed, or rebuilt). Not an OODA tactical call.
**Epistemic status:** diagnosis. No measurement run as of authoring. This brief freezes the attribution rules *before* any number is seen, because the operator already holds a strong prior ("regime inflection, strategies dead") and the failure mode is acting on that prior without measuring.
**Authored:** 2026-06-17 (session) · **Status:** OPEN — pre-registration.

---

## §0 — Rule 0: production reads (before authoring)
All read directly this session (claude.ai → local repo, read-only):

| Artifact | Path | Anchor / what it fixed |
|---|---|---|
| Locked risk %s + firm rules | `core/firm_rules.py` | `_BASE_RISK` = guardian 0.0034 / striker(DJ30) 0.0070 / aegis 0.0150 / striker_nas100 0.0037; FXIFY $200K, 5% max-DD/daily/target. Lock ADR `docs/adr/2026-05-23-allocation-refresh-2.md`. |
| Locked source versions + hashes | `core/strategies/MANIFEST.sha256` | Guardian Gold v5.5 / Striker DJ30 v4.5 / Aegis USDJPY v4.3 / NAS100 v1; each has a paired `_indicator.pine`. The signal-level backtest MUST use these exact blobs. |
| MC engine | `core/portfolio_mc.py` | Week-block (5-day) bootstrap; anchor pinned in `tests/test_mc_anchors.py` (99.83/0.17/4.37). Source of the envelope. |
| Risk controls | `core/dd_protection.py` | dd_protection constants — read so the signal-level sim applies the live protection layer. |
| Regime gate + log | `ops/regime_gate/gold_gate_shadow.py`, `ops/data/gold_gate_shadow_log.csv` | Last & only reading 2026-04-19 WAIT, gold KER126 0.0841 < THR 0.12. Gate not run since. |
| ECR pipeline | `scripts/run_ecr.py`, `scripts/preprocess_pine_ecr_logs.py` | Execution-capture leg. Consumes a DXTrade fills export. |
| Prior closed work (do-not-rerun) | `lab/analysis/regime_stress_2026-06-15/` | FALSIFIED-FAIRWEATHER: hostile regime = gold chop; perfect-foresight resizing is DEAD (binding constraint = near-zero hostile drift). Forbids the "time-the-regime-with-signals" lever (§5.2). |
| Feed canon | `docs/adr/2026-06-12-tv-csv-canonical-feed-policy.md` | TV/Pepperstone CSV canonical; Dukascopy/Alchemy non-canonical (§7.6). |

---

## §1 — Context & doctrine connection
Live symptom (operator, 2026-06-17): the book has returned ~nothing since mid-April — a ~2-month stretch that *feels* like no winning trades — and the operator's read is a regime inflection that has killed the 4-year edge. This brief gates that build. It is a single attribution question: the flat-period P&L decomposes as `live ≈ signal-level(to-spec) × execution-capture(ECR)`, plus a residual measured against the regime-appropriate MC envelope. The decision (hold / fix-execution / rebuild) hinges on whether a decay residual survives once regime and execution are accounted for.

Doctrine ties: (a) the gold gate already called this regime on 2026-04-19 (WAIT, chop); (b) Q-REGIME-STRESS-1 already characterized gold-chop as the book's designed-weak regime and falsified resizing/detection-timing; (c) the lock MC priced a hostile regime, so a flat chop stretch is closer to anticipated than broken — pending measurement. The decorrelated-leg gap is real but a separate build (§9).

## §2 — Question (symptom, not fix)
The locked 4-strategy book has produced ~no net return for ~2 months. What accounts for it, and does any part indicate the strategies have stopped performing within their locked MC model? Asks for an attribution and a binary decay verdict; prescribes nothing.

## §3 — Facts known at authoring (and the line not crossed)
**Known:** gold gate last reading 2026-04-19 WAIT (chop), idle since; documented execution-leakage history (prior ECR negative 8–23%, ~$14.9K skip + ~$5.7K discretion leakage Apr 13–May 14; one clean week May 25–29); rolling 6-week ECR unassembled; FXIFY DXTrade account never synced; lock MC priced 2020–2023 stress (p99 DD ~5.9%, bust ~3%). **Not crossed:** signal-level vs envelope and the ECR have NOT been computed.

## §4 — Falsifiable hypothesis
> **H:** If the signal-level (locked-blob, to-spec) portfolio over the frozen window (§7.1) falls INSIDE the regime-appropriate MC envelope (≥ p25 of §7.3), then the locked book has NOT decayed — the flat run is (regime + execution capture), disposition HOLD or FIX-EXECUTION per §6;
> **Falsifier:** otherwise (signal-level below p10) the book underperformed its own model even accounting for the hostile regime — the decay/regime-shift hypothesis is supported (NOT falsified), and structural review (decorrelated-leg / rebuild) is warranted.

A 2-month window cannot prove decay (§8 power); a clear sub-p10 result supports decay, an inside result leaves it falsified-as-cause.

## §5 — Forbidden moves
1. Acting on the regime narrative before §7 returns (rebuild / abandon / build "regime signals"). Headline forbidden move.
2. Re-running the closed resizing/detection-timing path (Q-REGIME-STRESS-1: resizing DEAD, drift-bound).
3. Cherry-picking the window start. Frozen at 2026-04-13 (§7.1).
4. Switching envelope (E1↔E2) or threshold (p10/p25) post-result.
5. Blaming the strategies for decay without computing the ECR first.
6. Concluding "dead for an extended period" from this sample (low power).
7. Non-canonical feed (Dukascopy/Alchemy) for the signal-level backtest.

## §6 — Gate (binary closure)
- **HOLD-REGIME** — signal-level ≥ p25 AND ECR ≥ 0.70.
- **FIX-EXECUTION** — signal-level ≥ p25 AND ECR < 0.70.
- **STRUCTURAL-DECAY** — signal-level < p10.
- **AMBIGUOUS** — signal-level in [p10, p25); OR ECR uncomputable; OR E1/E2 disagree across the threshold.

## §7 — Frozen measurement protocol
**7.1 Window.** 2026-04-13 → 2026-06-17 (frozen). Record trading-day count D.
**7.2 Signal-level.** Each locked-blob strategy to spec on canonical Pepperstone TV-CSV, locked `_BASE_RISK` %s, `dd_protection.py` applied; aggregate to portfolio cumulative R.
**7.3 MC envelope.** Via `portfolio_mc.py` week-block bootstrap, distribution of cumulative portfolio R over D. E1 unconditional (2020–2026); E2 regime-honest (gold-chop blocks). Contingency: re-run the gold gate first; WAIT/chop → E2 primary; DEPLOY/trend → E1 primary.
**7.4 Threshold.** < p10 OUTSIDE (decay-supported); [p10, p25) AMBIGUOUS; ≥ p25 INSIDE. Per-strategy: flag any leg below its own p10.
**7.5 ECR.** `ECR = actual live net R / signal-level net R` via `run_ecr.py`, per strategy + aggregate, from a DXTrade fills export. ≥0.70 adequate / <0.70 material leakage. If sync failure blocks the export, execution leg is AMBIGUOUS.
**7.6 Feed.** Canonical TV/Pepperstone CSV only. Dukascopy/Alchemy forbidden.

## §8 — Power & data-sufficiency disclosure
~9-week window → small per-strategy trade counts; low-power, conservative about declaring decay. Hard dependency: ECR needs the DXTrade export; absent it, execution axis is AMBIGUOUS.

## §9 — Advancement path
HOLD-REGIME → maintain lock; resume gold gate; decorrelated-leg build non-urgent. FIX-EXECUTION → execution-capture track; no strategy rebuild. STRUCTURAL-DECAY → structural-review Pre-Q; decorrelated-leg search urgent (needs a new mechanism — Silver/USOIL-RGC failed). The decorrelated-leg search is worth opening in parallel regardless; the verdict sets only its urgency.

## §10 — Audit hooks
```bash
# 1. Window frozen (forbidden move §5.3)
grep -n "2026-04-13" lab/analysis/regime_fit_2026-06-17/*.py    # assert window start unchanged
# 2. Envelope + threshold frozen (§5.4)
grep -n "E1\|E2\|p10\|p25\|W0\|W1" lab/analysis/regime_fit_2026-06-17/*.py
# 3. Locked blobs used, not drafts (§7.2)
python scripts/verify_lock_anchors.py
# 4. Feed canon — Pepperstone, not Alchemy (§7.6)
grep -n "PEPPERSTONE" lab/analysis/regime_fit_2026-06-17/signal_level.py
# 5. ECR input is the DXTrade export for the window (§7.5)
grep -n "dxtrade\|fills\|statement" lab/analysis/regime_fit_2026-06-17/ecr_reconcile.py
# 7. Brief discipline (mechanical)
python scripts/check_brief.py lab/analysis/regime_fit_2026-06-17/Q-REGIME-FIT-1.md --type inquire
```
**Append-only audit question (voids the verdict on any "yes"):** Was the window, envelope choice, or threshold moved after the signal-level number or the ECR was seen? — Authoring-time answer: No. **Closure answer: No** — window/envelope/threshold unchanged; §7.1 entry-vs-exit dating (left unspecified at authoring) pinned to entry-date at closure and recorded in RESULTS.md, with the verdict shown convention-robust.
