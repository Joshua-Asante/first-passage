# Phase B Lane B2 (London-fix wake, 6E/6B) — placebo battery results (B2.2)

**Date:** 2026-08-24
**Plan:** [`Phase B mechanism supply`](../../superpowers/plans/2026-08-23-viable-strategy-phase-b-mechanism-supply.md) — Lane B2, task B2.2
**Owner artifacts:** [`N-2026-08-24-b2-london-fix-wake-cost-arithmetic.md`](../notice/N-2026-08-24-b2-london-fix-wake-cost-arithmetic.md)
(B2.0/B2.1, the mechanism definition in §4, and the B2.1 ADMIT ruling this task is licensed by) ·
[`lab/analysis/_inbox/b2_london_fix_wake_2026-08-24/`](../../../lab/analysis/_inbox/b2_london_fix_wake_2026-08-24/)
(harness, raw log, and the detailed per-symbol numeric record — `RESULTS.md`) ·
[`nas100_orb_gex_gate.py`](../../../lab/analysis/orb/orb_universe_2026-06-22/) (gamma-family
orthogonality-partial precedent this task's regression is adapted from — pruned from the worktree
by the 2026-08-08 Great Prune, retrieved via `git show pre-prune-2026-08-08:lab/analysis/orb/orb_universe_2026-06-22/nas100_orb_gex_gate.py`)
**Authorization:** licensed this session — B2.0 (cost arithmetic) and B2.1 (operator bar-reading,
ruled `ADMIT` scoped to both 6E and 6B) both already passed. This task applies the plan's own
frozen B2.2 kill criterion; no new operator bar-reading is asked here (the criterion is
mechanical, see below).

Catalog attestation (this session, before writing): `lab/CATALOG.md` / `docs/briefs/INDEX.md` /
`docs/rejected_candidates.md` carried no B2/London-fix-wake/6E/6B harness slug before this task —
nothing duplicated. (The registry's existing "FX intraday fixing-reversal... on EURUSD" entry, F3,
is the *adjacent* dead family this lane's own honest posture already names — the fix-print event
itself, cash EURUSD, a different mechanism (event-time, not wake) and a different instrument; see
the N-2026-08-24 notice §4 for the full B2.1 reasoning on why that did not itself kill this lane.)

---

## B2.2 — placebo battery

**Task text (plan, verbatim):** "2 years of hourly 6E bars (Databento `ohlcv-1h`, $0-class —
Rule-1 estimate first). Mean 11:10→13:00 return conditioned on impulse sign vs 1,000 placebo
windows matched on day-of-week + trailing vol; plus the orthogonality regression (trailing-vol +
prior-hour-return controls — the gamma-family precedent). Kill if the fix dummy adds nothing over
generic reversal or sits ≤ placebo 60th percentile."

Scope carried forward from B2.1's ruling: **both 6E and 6B**, scored separately, never pooled (one
could survive while the other dies — the task brief's own instruction, restated from the B2.1
scope decision).

### Data pulled (own Rule-1 estimates run before pulling; both $0.0000)

The task context named a prior dry-run for `ohlcv-1h` 6E+6B combined (2yr, ~1.3MB, 23,619
records, $0.0000) as already covering the exact hourly request — re-estimated anyway per Rule 1
discipline (own estimate before any pull), reproduced identically. A second schema escalation was
needed and separately estimated: hourly bars cannot resolve the literal 10:58–11:04 ET 6-minute
fix cluster (it straddles the 10:00–11:00 and 11:00–12:00 hourly bars) or a precise 11:10 ET entry
anchor, so `ohlcv-1m` (full 2-year range, both symbols) was estimated ($0.0000, ~75MB, 1,337,317
records) and pulled, giving a precise impulse/entry measurement rather than relying solely on the
brief's coarser example proxy. Both pulls: continuous `.v.0` (volume-rolled — **never** `.c.0` for
these FX futures, the repo's own roll-rule lesson: `.c.0` maps CME currency futures to a near-dead
front monthly serial after each quarterly expiry). Roll integrity confirmed on `instrument_id`
(not the `symbol` alias column, which never changes): 9 distinct contracts per symbol over the
2-year span, each holding a full quarter's worth of hourly bars — no `6J.c.0`-style
undercounting.

### Clock-resolution choice (stated and justified, per the task brief's explicit ask)

Both of the brief's offered options were used, in different roles, rather than picking one:

- **Precise (primary):** impulse = open(11:04 1m bar) − open(10:58 1m bar) [literal 10:58–11:04
  ET]; target = open(13:00 1m bar) − open(11:10 1m bar) [literal 11:10–13:00 ET]. This is the
  primary point estimate and feeds the decisive orthogonality regression.
- **Hourly-proxy (the brief's own suggested fallback, e.g. sign of the 10:00–11:00 ET hourly
  bar):** used for two purposes only — (a) the placebo-comparable statistic (the placebo null is
  built entirely from cheap hourly data, so comparing like-for-like requires the real statistic to
  use the same hourly clock family), and (b) a sign/magnitude cross-check on the precise version.
  It could **not** be used as the orthogonality regression's own fix-dummy regressor: it is
  numerically identical to the `prior_hour_return` control (both are "open(11:00h) −
  open(10:00h)"), which would make that regression degenerate (perfect collinearity between the
  tested variable and one of its own controls). This collinearity is itself informative: it is the
  concrete reason hourly resolution "cannot answer this" for the decisive gate, beyond the
  literal 6-minute-window argument in the task brief.

CME's daily Globex trading halt (16:00–17:00 CT = 17:00–18:00 ET) was discovered empirically while
building the placebo grid — the `h17` hourly column is absent for all 624 calendar dates in the
panel. One placebo candidate hour (14:00 ET, whose 2-hour-later outcome window would need `h17`)
was dropped from the menu for this reason; the remaining 6 candidates (06,07,08,09,12,13 ET) are
all clear of both the real fix window and the halt.

### Results (full numeric detail in the lab/analysis RESULTS.md; summary here)

**Step 3 (conditional means, not pooled):**

| Symbol | n | fade-strategy R_precise: mean / t | fade-strategy R_hourly: mean / t |
|---|---|---|---|
| 6E.v.0 | 469 | +0.000065 / +0.97 | −0.000030 / −0.43 |
| 6B.v.0 | 447 | −0.000131 / −1.65 | −0.000094 / −1.09 |

Neither symbol clears even a bare `\|t\|≈2` before any control or placebo. 6E's two clock
resolutions **disagree in sign** — a fragility signal on its own (a real mechanism should not flip
sign under a ~10-minute clock perturbation). 6B's two versions agree (both negative — the raw
relationship is momentum-continuation, not reversal, opposite the fade hypothesis).

**Step 5 (orthogonality regression, the decisive gate — adapted from the gamma-family precedent's
`partial_out_t`, sign-flipped because this lane is a reversal/fade hypothesis, not the precedent's
momentum-continuation one):**

`target_precise ~ 1 + trailing_vol + prior_hour_return + imp_sign`

| Symbol | coef(imp_sign) | t(imp_sign) | correct sign? | \|t\|≥2? | Orthogonal? |
|---|---|---|---|---|---|
| 6E.v.0 | −0.000060 | −0.90 | yes (negative) | no | **NO** |
| 6B.v.0 | +0.000130 | +1.63 | no (positive = momentum) | no | **NO** |

**Step 4/6 (placebo null, 1,000 replicates, hourly-clock family, day-of-week + trailing-vol
matched by construction — every replicate draws a random non-fix clock hour independently per
trading day, applied to the identical set of real trading days, so the matching is exact identity,
not approximate resampling; verified programmatically against differential NaN-dropping, see the
lab RESULTS.md):**

| Symbol | real stat | null p60 | real's percentile rank | ≤ p60? |
|---|---|---|---|---|
| 6E.v.0 | −0.000030 | +0.000054 | 20.9th | **YES — kill** |
| 6B.v.0 | −0.000094 | +0.000113 | 3.9th | **YES — kill** |

Both real fix-window statistics sit **below the null distribution's own median**, not just below
its 60th percentile — 6B's real statistic is worse than 96% of random-clock placebo draws. Both
day-of-week and trailing-vol matching were verified to hold (not merely assumed): max day-of-week
frequency deviation ≤0.2 percentage points, trailing-vol quartile relative deviation ≤0.3%, for
both symbols.

**A side finding, not decision-relevant but worth recording:** the placebo null itself is centered
comfortably above zero for both symbols (mean +0.000036 / +0.000086) — some generic "fade the
prior hour's move" pattern has positive gross expectancy at *various* clock times across this
panel. The fix-specific window is not merely unremarkable against that backdrop; it *underperforms*
the generic version. (Caveat carried from the lab RESULTS.md: bar opens are trade prints, not
midpoints, so part of this generic-reversal magnitude — on the order of a single 6E/6B tick — could
be bid-ask-bounce microstructure rather than pure economic reversion; this does not change the kill
verdict either way.)

No post-hoc subset or direction search for a rescuing cut was run after the whole-sample test
failed (`lesson_snag_best_of_k_anchor_graveyard`) — the frozen kill criterion is applied exactly as
written, once, on the pre-specified full sample.

---

## Frozen kill criteria — self-clears

> "B2.2 placebo/orthogonality fail → dead, registry row citing F3 lineage." (plan, Lane B2 kill
> criteria, verbatim)
>
> Applied criterion (B2.2 task text): "Kill if the fix dummy adds nothing over generic reversal or
> sits ≤ placebo 60th percentile."

Both legs fail independently, for **both** symbols — not a knife-edge single-leg call requiring
judgment:

| Symbol | Orthogonality leg | Placebo leg | Verdict |
|---|---|---|---|
| 6E.v.0 | FAIL | FAIL | **DEAD** |
| 6B.v.0 | FAIL | FAIL | **DEAD** |

This is a self-clearing outcome — zero judgment left, per the task's own framing. A
`docs/rejected_candidates.md` row is added (this note) citing the F3 lineage the plan's own kill
text names, and `lab/CATALOG.md` is updated for the new `lab/analysis/_inbox/b2_london_fix_wake_2026-08-24/`
campaign directory.

---

## Disposition

**DEAD — both 6E and 6B, at B2.2.** Lane B2 (London-fix wake) does not proceed to B2.3 (shape
pre-check) for either symbol — B2.3 does not fire, mirroring how Lane B3's B3.1/B3.2 did not fire
after B3.0's arithmetic kill. No card was opened, is being opened, or will be opened for this
lane. The plan's own Phase-B-wide exit criteria (≥1 lane hands a surviving candidate to Phase C,
or all lanes record honest kills/parks) is **not** evaluated here — Lane B1 is still open
(B1.5's forward paper-log is in progress, spans real calendar time) and Lane B4 depends on Phase
A1's revival list; a whole-phase disposition is the controller's call once every lane has reported,
not this task's.

---

## Verification

```bash
# Reproduce the Rule-1 dry-runs (both $0.0000)
PYTHONPATH=lab python -m databento_fetch.db_fetch estimate \
    --symbols 6E.v.0,6B.v.0 --stype continuous --schema ohlcv-1h --start 2024-08-24 --end 2026-08-24
PYTHONPATH=lab python -m databento_fetch.db_fetch estimate \
    --symbols 6E.v.0,6B.v.0 --stype continuous --schema ohlcv-1m --start 2024-08-24 --end 2026-08-24

# Pull both (cache-hit / no re-billing if the estimates above already ran once on this machine)
PYTHONPATH=lab python -m databento_fetch.db_fetch pull \
    --symbols 6E.v.0,6B.v.0 --stype continuous --schema ohlcv-1h --start 2024-08-24 --end 2026-08-24 \
    --max-cost 0.01 --out lab/analysis/_inbox/b2_london_fix_wake_2026-08-24/data/6E_6B_ohlcv1h_2y.parquet
PYTHONPATH=lab python -m databento_fetch.db_fetch pull \
    --symbols 6E.v.0,6B.v.0 --stype continuous --schema ohlcv-1m --start 2024-08-24 --end 2026-08-24 \
    --max-cost 0.01 --out lab/analysis/_inbox/b2_london_fix_wake_2026-08-24/data/6E_6B_ohlcv1m_2y.parquet

# Run the full battery -- reproduces lab/analysis/_inbox/b2_london_fix_wake_2026-08-24/run_output.txt
# byte-identically (fixed SEED=20260824; both legs fail for both symbols, as tabulated above)
python lab/analysis/_inbox/b2_london_fix_wake_2026-08-24/run_b22_placebo_battery.py

# Roll-rule discipline: confirm .v.0 is genuinely rolling (instrument_id, never the symbol alias)
python -c "
import pandas as pd
df = pd.read_parquet('lab/analysis/_inbox/b2_london_fix_wake_2026-08-24/data/6E_6B_ohlcv1h_2y.parquet').reset_index()
for sym in ['6E.v.0','6B.v.0']:
    print(sym, df[df['symbol']==sym]['instrument_id'].nunique(), 'distinct contracts over 2y')
"
# Expected: 9 and 9 -- a clean quarterly roll cadence, not a stuck/dead contract.

# Confirm the gamma-family precedent this task's regression is adapted from
git show pre-prune-2026-08-08:lab/analysis/orb/orb_universe_2026-06-22/nas100_orb_gex_gate.py | grep -n "def partial_out_t" -A 10

# Confirm the registry row and CATALOG row this task adds
grep -n "b2_london_fix_wake\|london-fix wake" docs/rejected_candidates.md
grep -n "b2_london_fix_wake" lab/CATALOG.md

# Confirm the plan checklist reflects the B2.2 outcome
grep -n "B2.2\|B2.3" docs/superpowers/plans/2026-08-23-viable-strategy-phase-b-mechanism-supply.md
```
