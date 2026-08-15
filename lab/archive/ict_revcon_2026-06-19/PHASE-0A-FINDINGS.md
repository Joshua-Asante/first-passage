# Q-ICT-1H-REVCON-1 / Phase 0a — EXPLORATORY findings (hypothesis generated, NOT a verdict)

**Status:** `EXPLORATORY-COMPLETE 2026-06-19` — generates the PREREG-0B hypothesis. NOT confirmation.
**Parent:** [`Q-ICT-REVCON-PLAN.md`](Q-ICT-REVCON-PLAN.md) (§3 Q-ICT-1H-REVCON-1, §4 H-1H-REVCON, §7 Phase 0a)
**Firewall:** This note records only the EXPLORATORY 0a result on the data that **already produced the 1H reversion FALSIFIED**. Per parent §5 / [`PREREG-0B.md`](PREREG-0B.md), a second hypothesis scored on that same data is hypothesis-GENERATING; confirmatory evidence is the fresh multi-regime **0b** run, pre-registered before scoring.

---

## §0 — Provenance (Rule 0)

| Artifact | Anchor |
|---|---|
| Probe (NEW) | [`revcon_probe_0a.py`](revcon_probe_0a.py) — imports & REUSES the M-15-fixed cascade primitives; the frozen [`harness_1h.py`](lab/archive/ict_cascade_2026-06-18/harness_1h.py) left **byte-identical** (42/42 still green) |
| Tests (NEW) | [`test_revcon_probe_0a.py`](test_revcon_probe_0a.py) — **18/18 pass**; synthetic fixtures, no vendor data |
| Data of record | `PEPPERSTONE_US500, 60_a6b6b.csv` (gitignored vendor CSV in Downloads): **191660 B / sha256 70d9cc3c… / 3040 rows / 2025-12-11 → 2026-06-18** (TV's 1H cap; single benign uptrend) |
| §0 Pine anchors | 1H `7554 B / 2026-06-18T22:42:04Z`, 1M `22180 B / 2026-06-18T22:42:25Z` (match parent §0); M-15 fix present at `harness_1h.py:255` |
| Adversarial audit | 21-agent diverse-lens Workflow (faithfulness / look-ahead / stats-power / interpretation), each finding independently refuted — verdict below |

## §1 — What 0a did

Built an EXPLORATORY probe on top of the M-15-fixed `recompute_hits` that adds, on the existing 6.5-mo export: (i) **continuation** rates (premium→up, discount→down) alongside reversion; (ii) a **regime-conditional** split by Kaufman efficiency ratio (decision-time-observable, look_n=60); (iii) a **bias-conditioned** split using a close-vs-weekly-EMA20 PROXY (the real `structBias` export was a transient input, now gone). Output is a hypothesis to shape PREREG-0B — it cannot and does not emit a verdict (`exploratory=True` stamped everywhere).

## §2 — The instrument is FAITHFUL (audit verdict)

The M-15 prior (a Pine offset transcribed as a forward index, scoring the *complement* of the claim, masked by self-referential tests) was the load-bearing risk. The audit verified **from first principles, not from my tests**:

- `recompute_continuation` is the **genuine decision-bar complement DIRECTION** of `recompute_hits` — same bar `i`, same outcome bar `i+fwd_k`, only the inequality flipped; reads `zone[i]` never `zone[j]` (proven by a future-zone perturbation, a 6-bar hand trace, and 0 rows being both rev & cont / tie-fraction 0.0011). **NOT** a forward-index inversion.
- `efficiency_ratio` is **decision-time-observable** (perturbing a future bar cannot move a past ER).
- The unconditional reversion rates **reproduce the closure byte-identically** (prem `0.5085`, disc `0.5641`).

**No M-15-class scoring defect exists in the probe.** The confirmed findings are measurement/interpretation/discipline issues (§4), not wrong numbers.

## §3 — The exploratory result (corrected run, post-fix)

**Unconditional** (reproduces [`CLOSURE-1H-FALSIFIED`](lab/archive/ict_cascade_2026-06-18/CLOSURE-1H-FALSIFIED.md)): prem reversion `0.5085` (n_floor 151) / disc reversion `0.5641` (n_floor 92) — both straddle 0.5, as the cascade found.

**Regime-conditional (the actual probe) — runs OPPOSITE the motivating story, and is N-starved where it matters:**

| ER thr | chop-prem | trend-prem | chop-disc | trend-disc |
|---|---|---|---|---|
| 0.20 | cont 0.521 (n_floor 101) | rev 0.529 (n_floor **48**) | rev 0.530 (64) | rev 0.579 (**24** starved) |
| 0.30 | cont 0.531 (129) | rev 0.563 (**21** starved) | rev 0.545 (82) | (**6** starved) |
| 0.40 | cont 0.517 (144) | (**6** starved) | rev 0.558 (88) | (**0** starved) |

- The motivating intuition ("premium reverts DOWN in chop, continues UP in trend") is **contradicted**: where powered, premium *continuation* edges ahead in chop and *reversion* edges ahead in trend — the reverse.
- The **trend** bucket (where the continuation hypothesis lives) is **below the n-floor of 30** at every threshold ≥ 0.30. At the only adequately-powered threshold (0.20, n_floor 48) the rate `0.529` does **not** clear the 2pp margin (CI straddles 0.5).
- **Read:** the regime axis is **not answerable on this single benign window** — a powered NEGATIVE in chop, a STARVED non-result in trend. This is the AMBIGUOUS-shaped outcome PREREG-0B anticipated; it confirms 0b genuinely needs a chop-AND-trend-spanning export sized so each TREND bucket clears 30.

**Bias proxy — the more robust axis, and it SURVIVES the observability fix:**

| | bias +1 | bias −1 |
|---|---|---|
| prem | 0.480 | **0.604** |
| disc | 0.565 | 0.550 |

- premium reverts down under a **bearish** prior-week bias at ~`0.60` — the single strongest directional number.
- The audit caught that my original proxy was a **same-week look-ahead** (stamped a week's Friday-close sign onto its Monday bars). I fixed it to a **prior-week lag** (the live gate's `gateBias[1]` convention). The number moved only `0.6087 → 0.6042` — so the signal is **not** a look-ahead artifact; it is robust to the correction. (Still a PROXY, not the real `structBias`, and n is modest — exploratory only.)

## §4 — Audit findings + dispositions

| ID | Finding | Sev | Disposition |
|---|---|---|---|
| LA-1 | Bias proxy was a same-week look-ahead | MAJOR | **FIXED** — prior-week lag + observability guard test ([`test_…is_decision_time_observable`]); signal survives (0.604) |
| F3/F5 | Two `n_eff` defs under one label (stride-kept 177 vs floor 151; gate uses floor) | MINOR | **FIXED** — report now prints `n_ci` and `n_floor` distinctly; `direction_rates` exposes `n_floor` |
| F6 | `win=` printed a direction word at n_floor 0–2 | NIT | **FIXED** — `win=--` + `STARVED` flag below the floor |
| F4 / SP-1 / F1(stats) | Regime axis starved + flip opposite the motivating story | MINOR | **Noted** — drives PREREG-0B (export sizing, CHOICE #4); regime-flip test annotated as mechanism-only (not a real-data claim) |
| F4(faith) discipline | A green self-referential test encoded the assumed flip direction (M-15 epistemic parallel one layer up) | — | **Mitigated** — test comment added; the *audit*, not the test, established the real-data direction |

**Refuted (correctly):** reproduction-is-correct (not a bug), threshold multiplicity (already firewalled by PREREG-0B Forbidden #2 + threshold 0.30 ratification), noise-floor (expected single-window property; probe makes no clearance claim), row-order assumption (inert on the strictly-sorted real export; pipeline-wide, not proxy-specific).

## §5 — The hypothesis handed to PREREG-0B

1. **Bias-sign is the more promising primary axis.** premium→down under bearish prior-week bias ~0.60 is robust to the observability fix; it is decision-time-observable via the `[1]`-lag. 0b must test it with the **real exported `structBias`** joined with the **prior-week lag**.
2. **The ER regime axis is fragile here** — it fragments n and starves the trend bucket on a benign window, and (weakly) contradicts the motivating direction. 0b should either drop it or size the export so each trend bucket clears 30.
3. **Keep H direction-agnostic.** Do NOT carry the closure's "continue-up-in-trend" economic prior into 0b; 0a contradicts it. H-1H-REVCON already reads "reversion OR continuation in some partition."

## §6 — PREREG-0B ratified (operator-delegated "best judgement", 2026-06-19)

**0b = bias-sign partition ONLY; the ER-regime partition is DROPPED.** 0a found the bias axis robust and observability-clean (with the `[1]`-lag) while the ER-regime axis starves the trend bucket, contradicts the motivating direction, and a chop-spanning 1H export exceeds TV's ≈6.5-mo 1H cap. Family = {prem,disc} × {bias ±1} × {rev,cont} = 8 directional rates at the fixed gate anchor (60/0.05); n-floor 30 per bias bucket per zone on `floor(N/fwdK)`. Recorded in [`PREREG-0B.md`](PREREG-0B.md) (RATIFIED; amendment log).

**Binding 0b feasibility gate (operator-side):** the bias confirmatory still needs a genuinely multi-regime 1H window. The cascade established **TV's 1H chart caps at ≈6.5 months (single benign regime)** — the 0a window IS that cap. If no deeper-history multi-regime 1H US500 source is obtainable, the bias signal is **data-blocked for a confirmatory verdict** and routes to a **forward-watch belt finding** (the cascade's disc→up disposition), NOT a re-tune and NOT a lock. Confirm the available 1H span before scoring 0b.

## §7 — Lesson candidates

- **Self-referential synthetic tests can encode a *directional assumption* even when the scoring is correct.** `test_regime_split_recovers_direction_flip` asserts a flip in the direction my motivating intuition predicted; the real data shows the reverse. The mechanism test is legitimate, but the *direction* it bakes in is not evidence. The adversarial audit (not the green test) established the real-data direction. (Methodology parallel to M-15 one layer up — worth a one-line note in [[feedback_pine_offset_port_faithfulness_anchor]]'s neighborhood, not a new M-lesson: the probe caught it pre-data.)
- **A look-ahead can be a real defect yet immaterial to the number.** The bias proxy's same-week leak was a genuine observability bug (fixed), but the signal barely moved — fix it for correctness, don't assume the magnitude was the artifact.

---

## Verification

```bash
python -m pytest lab/analysis/ict_revcon_2026-06-19/test_revcon_probe_0a.py -q   # 18 passed
python -m pytest lab/analysis/ict_cascade_2026-06-18/test_harness_1h.py -q       # 42 passed (frozen harness untouched)
python scripts/check_boundaries.py                                               # OK
python lab/analysis/ict_revcon_2026-06-19/revcon_probe_0a.py --hour-csv "C:/Users/joshu/Downloads/PEPPERSTONE_US500, 60_a6b6b.csv"
```
