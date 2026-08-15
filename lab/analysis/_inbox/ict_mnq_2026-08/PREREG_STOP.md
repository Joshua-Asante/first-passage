# `Q-ICTSTOP-1` — VERDICT PRE-REGISTRATION (stop-lever space-kill, native MNQ 1m)

**FROZEN ON THIS FILE'S INTRODUCING COMMIT. No criterion below may move after the first
real-population stop-counterfactual number exists. Zero stop-space expectancy figures have
been computed at freeze time — ICTEXP's stop-free T2 (−1.039 pt on n=32,355) is known; no
MAE-conditioned or raid-scaled stop P&L has been computed on this chain.**

**Scope:** [`Q-ICTSTOP-1` scoping](../../../../docs/briefs/rnd-pipeline/Q-ICTSTOP-1-ict-stop-space-kill-scoping.md).
**K:** `0` — **operator-affirmed 2026-08-06** via plan ratification (*"Implement the plan as
specified"*, plan locks K=0), discharging scope §9.
**Cost:** `$0.00` (MNQ 1m regenerable at $0.0000). **No manifest. Cap seat untouched.**
**Class:** order-free, zero-run, zero-K — ORB §2a stop space-kill on the ICTEXP population.
**Authored:** 2026-08-06 · Cursor (Composer), operator-directed.

---

## §0 — Rule-0 reads

All read in full this session. Load-bearing:

- **`RESULTS_EXP.md` @ `d627a53`** — stop-free T2 null; §6.1 open lever.
- **`PREREG_EXP.md` @ `30c79c9`** — population, BAR 5.640 pt, FM-4 no invented stop.
- **`run_exp.py` @ `d627a53`** — helpers reused; MAE + raid_dist are new.
- **`RESULTS_tv_export_realism.md` §2a @ `92abdbb`** — method template (`f×` construct range).
- **`PREREG-1M.md` @ `47cc3eb`** — stop rule still absent; `raidSellPx`/`raidBuyPx` are scale
  hints only.

**Consequence — raid distance is a SCALE, not a reconstructed locked stop.** Absolute-points
or ATR grids are forbidden as verdict axes (scope FM-3).

---

## §1 — Frozen design

### 1.1 Population

Identical to ICTEXP §1.1–1.3: raid-paired displacement FVGs, fill at FVG mid within
`retraceK=6`, `noDraw`, DOL `range-extreme` (`lookN=60`), hold to target touch or E1 16:00 ET.
Stop-free T2 signed is the no-stop baseline per event.

**Additional filter:** `raid_dist > 0` where `raid_dist` is fill→paired raid extreme distance
(bull: `fill − raid_ssl_px`; bear: `raid_bsl_px − fill`). Non-positive distances dropped and
counted. No invented tradeability floor beyond this geometric requirement.

### 1.2 Raid extreme attachment

Enrich pairing: each paired FVG carries the swept pool price on its paired raid bar
(SSL price for bull / BSL price for bear). When multiple pools sweep the same bar, take the
extreme relevant to stop placement (SSL: minimum swept price that bar; BSL: maximum).

### 1.3 MAE

Over bars from `fill+1` through the natural T2 exit bar (target-touch index if touched, else
E1 deadline index): long `fill − min(low)`; short `max(high) − fill`.

### 1.4 Counterfactual at f

Frozen grid: **`F_GRID = (0.5, 0.75, 1.0, 1.25, 1.5, 2.0)`**.
`s = f × raid_dist`.

- If `MAE < s`: signed = T2 signed (both E_best and E_worst).
- If `MAE ≥ s` and target **not** touched: signed = **−s** (both).
- If `MAE ≥ s` and target **touched**: E_worst = **−s**; E_best = T2 signed (target credit).

Kill / FALSIFIED reads **E_best** only.

### 1.5 Bar and uncertainty

**BAR = 5.640 pt** (identical to ICTEXP §1.5; Tradeify basis; basis-invariance of ICTEXP
verdict already recorded — not re-opened here).

95% CI by **day-block bootstrap** on entry-event blocks, `B = 2000`, **`seed = 20260806`**.

### 1.6 Disclosure (never verdict)

MAE quartiles for target-touched vs not-touched legs; per-f stop-out rate; n dropped for
non-positive `raid_dist`.

---

## §4 — Falsifiable hypothesis

**H-ICTSTOP-1.** Every f in `F_GRID` has E_best mean-signed day-block CI **upper** bound
**< 5.640 pt**, on **n ≥ 100** events after the raid_dist filter.

| # | Trigger | Threshold | Verdict |
|---|---|---|---|
| X1 | n after raid_dist filter | **< 100** | `INSUFFICIENT-N` |
| X2 | ∀ f: E_best CI upper | **< 5.640** | `FALSIFIED` (space-kill) |
| X3 | max_f CI upper ≥ 5.640 and ∀ f: CI lower < 5.640 | — | `AMBIGUOUS` |
| X4 | ∃ f: E_best CI lower ≥ 5.640 | — | `NOT-KILLED` (licenses nothing) |

---

## §5 — Forbidden moves

- **FM-1** — Reading X4 as GO or as license to reconstruct the Pine stop without a new
  K-bound pre-registration.
- **FM-2** — Treating raid extreme as *the* locked stop rule in a verdict.
- **FM-3** — Densifying `F_GRID` or switching to ATR / absolute-points after seeing results.
- **FM-4** — Grids on entry, DOL, `retraceK`, `pvLen`, or holding window.
- **FM-5** — Reopening Q-ICTNF near-field under this probe.
- **FM-6** — `core/`, lock, rail, Pine, K-ledger, manifest, or `lab/archive/` edits.
- **FM-7** — Quoting E_worst alone as the kill, or quoting a single f without the full grid.

---

## §6 — Verdict gate

| Verdict | Trigger | Consequence |
|---|---|---|
| `INSUFFICIENT-N` | X1 | NO-GO stands; method failed |
| `FALSIFIED` | X2 | Stop lever dead; ICT 1M expectancy closed incl. §6.1 residual; seat preserved |
| `AMBIGUOUS` | X3 | NO-GO stands |
| `NOT-KILLED` | X4 | NO-GO stands on reasons 1/2/4; stop reconstruction remains K-bound if pursued |

**No GO state.**

---

## §10 — Audit hooks

```bash
git log --format='%h %cs' -- lab/analysis/_inbox/ict_mnq_2026-08/PREREG_STOP.md
git log --format='%h %cs' -- lab/analysis/_inbox/ict_mnq_2026-08/RESULTS_STOP.md
git --no-pager diff HEAD -- lab/archive/ict_cascade_2026-06-18/
python -c "print(4*(2*0.91/2.00 + 0.5))"
```

---

## Amendment log

- **2026-08-06 — RATIFIED/FROZEN** on this file's introducing commit. Zero stop-space
  expectancy numbers existed at freeze. K=0 per operator plan-implementation directive.
