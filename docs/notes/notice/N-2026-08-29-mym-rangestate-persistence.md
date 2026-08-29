# Notice — MYM session-TR range-state persistence (conditioner-role, corrected battery)

**Notice ID:** N-2026-08-29-mym-rangestate-persistence
**Observed:** 2026-08-29
**Author:** Joshua | claude.ai
**Source:** backtest CSV (bar panel) — atheoretical mechanism harvest, MYM Phase 2
**Status:** `DROPPED`
**Lives in:** `docs/notes/notice/N-2026-08-29-mym-rangestate-persistence.md`

---

## §0 — Source anchor

- **Source:** `core/data/bar_data/MYM_M15.csv` (BAR EXPORT v0.2, `CBOT_MINI:MYM1!`, sha256
  `24e169528f7ea6693b75c71c3195edf6a04f3a26c6b6dff0f2e9c623fd597a58` — matches
  `SHA256SUMS`), aggregated to full-trading-day session OHLC (1,551 sessions,
  2020-07-02→2026-07-02). Script:
  `lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c1_rangestate.py`
  (+ shared `load_sessions.py`, `iaaft_battery.py`). Results:
  `lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c1_results.json`.
- **Observed at:** 2026-08-29 (this session).

---

## §1 — The observation

Session-level True Range (Wilder TR on the full Globex trading day, 18:00 ET D-1 →
17:00 ET D) sitting in the trailing top quintile (P80, strictly-prior 60 sessions)
predicts elevated *next*-session TR (> trailing median, through-today 60 sessions) at
**obs = 0.6777** (n_cond = 332 of n_pop = 1,489), CI [0.6028, 0.7445] (60-session
circular block-bootstrap, seed 42), halves (0.6928, 0.6627) — both comfortably above the
0.50 unconditional reference. Run through the **corrected IAAFT normal-scores null**
(`docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md`), reused
verbatim in shape at M=200 (disclosed lighter weight than the frozen M=1,000; diagnostic
gate PASS, Spearman-rank-ACF mismatch med=0.0358/p95=0.0594, both under the frozen
0.04/0.07 tolerance), the observed 0.6777 sits at the **22nd percentile of its own
zero-mechanism surrogate band** (surrogate mean 0.6948, p95 0.7267) — p_upper=0.7811,
p_lower=0.2239.

## §2 — Why it stands out (the N signal)

- **Baseline:** MYM had never been run through this exact class/battery before (MYM.md
  has no `daily-range-state-persistence` cell); the class's two prior scores are GC
  (NULL) and CL (SIGNAL-GENERIC) — both non-index. This session widens the class to an
  index-futures instrument, outside the class's originally-declared "non-index triad"
  scope (`MECHANISMS.md`) — flagged here as a disclosed scope departure, not hidden.
- **Delta:** All three presence limbs PASS (L1 n-floor, L2 CI-lower-bound>0.50, L3
  halves) — a genuine, reliable persistence effect exists on MYM. But attribution is
  **GENERIC**: the magnitude of that persistence is fully explained by (in fact sits
  *below the median of*) what a linear-ACF-matched zero-mechanism surrogate already
  produces. This is the identical shape to CL's own SIGNAL-GENERIC verdict
  (`MECHANISMS.md` — "real, regime-stable, canon-attributed... NOT a mechanism").
- **Frequency check:** first instance on MYM; the class has now been scored on 3
  instruments (GC NULL, CL SIGNAL-GENERIC, MYM SIGNAL-GENERIC) — 2 of 3 land
  SIGNAL-GENERIC, suggesting this may be the modal outcome for the class rather than an
  instrument-specific finding.

## §3 — Candidate mechanisms (informal)

- Ordinary volatility clustering (ARCH/GARCH-class serial dependence) — the canon
  attribution the battery itself assigns; not a distinct "mechanism" beyond this.
- Could also be noise dissolving toward the null median with more data — the 22nd-pct
  placement (below p50) argues against even a favorable read; this is not a near-miss.

## §4 — Routing decision

**DROP.**

Reason: presence is real but attribution is canon-generic (SIGNAL-GENERIC), which per
the class's own routing rule "routes to a conditioner-engineering prereg, never a
mechanism-discovery campaign" and "cannot discharge mechanism-owed." Critically, the
**identical verdict shape has already been chased downstream on the sibling CL
instrument and failed**: `Q-CONDVAL-1` ran the "owed connecting arithmetic" (does a
0.60+-type conditioner rate clear the cost-effectiveness floor to be worth building) on
CL's own SIGNAL-GENERIC and returned `FALSIFIED` (committed C−U 0.130 < frozen L_star
0.423 — `docs/briefs/closures/Q-CONDVAL-1-closure-falsified.md`). Spending a fresh
conditioner-engineering prereg + K on MYM's version of the same statistical shape, with
no reason to expect a materially different cost-effectiveness outcome, is not a good use
of the family's `K_intrinsic` seats. The finding is real and worth keeping as a durable
record (MYM.md cell), just not worth graduating.

---

## §10 — Audit hooks

```bash
python lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c1_rangestate.py
# Expected: VERDICT: SIGNAL-GENERIC (obs=0.6777, p_upper=0.7811)

grep "N-2026-08-29-mym-rangestate-persistence" docs/briefs/Q-*.md
# Expected: no matches (DROPPED, not graduated)
```

---

## Verification

```bash
$ python ~/.claude/skills/brief-authoring/scripts/check_brief.py \
    docs/notes/notice/N-2026-08-29-mym-rangestate-persistence.md --type notice
# Expected: RESULT: well-formed
```
