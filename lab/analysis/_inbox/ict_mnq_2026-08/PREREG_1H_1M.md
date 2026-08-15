# Q-ICT-MNQ-1 / Layers 1H + 1M — VERDICT PRE-REGISTRATION (Part B)

**Registered before any databento MNQ 1H or 1m data is pulled or scored. No criterion
below may move after the first real-population run. The commit of this file is the lock
that lifts the firewall for the 1H and 1M layers.**

**Part B** — companion to [`PREREG_D_W.md`](PREREG_D_W.md) (Part A, D+W, frozen at `6ef7577`,
already **run**: W RESOLVED on NQ/MNQ, D SSL bear-FVG RESOLVED on NQ primary — see
[`RESULTS.md`](RESULTS.md)). Part A's outcomes do **not** relax anything here; every
threshold below is transcribed from the archived `PREREG-1H.md` / `PREREG-1M.md`.

Authored + **RATIFIED 2026-08-03** on this file's introducing commit.

---

## §0 — Governance: these are FRESH verdicts, not confirmations

**Load-bearing distinction, stated first because it changes what may be claimed.**
`CONFIRM-FREE-NODEPLOY-2026-08-03`
([`ruling`](../../../../docs/notes/2026-08-03-ict-instrument-confirmation-nodeploy-ruling.md))
scopes itself to the **W/D confirmation only**, and says so explicitly: 1H and 1M have
**no closed RESOLVED finding to confirm** (US500's 1H was **FALSIFIED**; its 1M was
**INSUFFICIENT-N**), so citing that ruling for them "would be a different, ungrounded claim."

Therefore:

- These layers are run here as **diagnostic measurement on an independent instrument**,
  under the same hard no-deploy commitment, and **still $0 / K=0 / no manifest** (the
  databento pull is metadata-confirmed **$0.00** — see §3).
- **If either returns a RESOLVED-shaped result, that result is a NEW finding**, not a
  confirmation, and it is subject to its own harvest-intake determination **before**
  anything downstream cites it. It does not inherit W/D's free-confirmation standing.
- Nothing here may be cited as licensing deployment, a rail change, or a c1 leg.

**Why run 1H at all, given US500 FALSIFIED it.** The archived closure states the
re-proposal bar in its own words: the US500 1H verdict rested on a **single benign
regime** (TV's 1H cap — 3,039 bars, 2025-12 → 2026-06), and its re-proposal bar is
**"multi-regime 1H data, not re-tuning."** That bar is now dischargeable: databento
serves MNQ 1H from 2019-05 (42,786 bars, spanning 2020 chop, 2022 bear, 2023-26 trend).
This is the *named* condition being met, not a re-litigation.

---

## §1 — Data (pulled only after this file is committed)

| Layer | Product | Symbol | Span | Est. records | **Est. cost** |
|---|---|---|---|---|---|
| 1H | `ohlcv-1h` | `MNQ.v.0` (continuous, volume-lead) | 2019-05-06 → 2026-08-03 | 42,786 | **$0.0000** |
| 1M | `ohlcv-1m` | `MNQ.v.0` | 2019-05-06 → 2026-08-03 | 2,552,025 | **$0.0000** |

Cost dry-run **executed 2026-08-03 before this freeze** (metadata endpoints only; these do
not bill). Both are `$0.00` under the current entitlement — the full-era 1m is free, so the
1M layer gets the genuinely multi-regime span the original campaign could never obtain.
Pull discipline (archived PREREG forbidden move): `--max-cost` hard ceiling set, `--force`
**forbidden**, `--phase oos` (the micro era is the reserved hold-out per MNQ ledger W4).

**MNQ-native only, both layers.** Never parent-NQ-proxied: ledger **W4** reserves the micro
era and forbids inheriting a parent fill model, and the 1M layer is explicitly about fills.

**Roll handling.** `MNQ.v.0` is databento's volume-lead continuous — the TV-`1!` analogue
(ledger **W1**), *not* the `.c.0` calendar roll. The same ±4-day 3rd-Friday exclusion frozen
in Part A §2 applies to event origins on both layers, for the same measured reason.

---

## §2 — Layer 1H: frozen configuration (verbatim from `PREREG-1H.md` / `harness_1h.py`)

Every value inherited; nothing re-derived. Harness `harness_1h.verdict_1h()` runs
**unmodified** — it recomputes hits internally from `(zone, close)`, so it needs only
OHLC-derived zones, and its own look-ahead audit runs as archived.

| Parameter | Value | Status |
|---|---|---|
| Anchor rule (gate-relevant) | `lookback-extremes` | LOCKED |
| `lookN` | **60** (must equal 1M `pdLookN`) | LOCKED |
| `eqBand` | **0.05** (must equal 1M `eqBand`) | LOCKED |
| `fwdK` | **12** (measurement horizon, not a trade knob) | LOCKED |
| Zone polarity | +1 premium → expect DOWN; −1 discount → expect UP; 0 EQ stand-down | LOCKED |
| Margin over 0.5 | **≥ 2pp** (`MARGIN_PP=0.02`) under **both** stride AND block CI | LOCKED |
| n-floor | **30** effective windows per zone | LOCKED |
| De-overlap | stride = `fwdK` = 12; block bootstrap block = 12, B=5000 | LOCKED |
| Selection penalty | 9 cells (`lookN{40,60,80}` × `eqBand{0,0.05,0.10}`), deflated max-stat | LOCKED |
| Placebos | random-EQ + sign-shuffle, B=2000 | LOCKED |
| Transfer pre-gate | agreement ≥ 0.90 **and** gap ≤ 3pp | LOCKED |
| Seed | 20260618 | LOCKED |

**Verdict gate** (archived §6, unchanged): `RESOLVED` needs a rate's de-overlapped CI to
clear 0.5 by ≥2pp under **both** stride and block, **and** beat the placebo floor, **and**
the winning anchor cell to clear ≥2pp **after** the 9-cell penalty, **and** the transfer
pre-gate to clear, **and** effective-N ≥ 30. `FALSIFIED` if both prem and disc CIs straddle
0.5 after penalty. `AMBIGUOUS-HOLD` if the unconditional gate clears but the
bias-conditioned limb fails, or the margin flips across halves. `INSUFFICIENT-N` if
effective-N < 30 in both zones.

**Price-BASIS transfer axis is `NOT-RUN` and declared so now** (not after seeing the
result): it requires a paired 1M export carrying the indicator's own `netBias`/`inKZ`
columns, whose formulas live only in the lost `.pine`. The **range-LAG** axis runs
normally (it is computable from OHLC). This mirrors the original campaign, where the
price-basis axis was likewise moot.

---

## §3 — Layer 1M: fill-mechanics probe (scope deliberately narrow)

**This is NOT the archived 1M execution-strategy test and does not use `harness_1m.py`.**
That harness scores a 16-cell ablation of a full strategy. Running it would be
candidate-generation — K-bound work this campaign's governance does not cover.

**What is measured instead — one order-free question:**

> Given a displacement FVG on MNQ 1-minute bars, what fraction retrace to the FVG **mid**
> within **6** subsequent bars?

This is precisely the mechanism that returned **0 fills on 247 orders** on US500, which the
archived closure flags as a *"strong mechanism prior, not a measured fact"* and characterizes
as instrument-general. It is the cheapest decisive question in the whole cascade: it uses no
strategy engine, no orders, no P&L, and no cost model.

**Frozen parameters** (transcribed from the archived locked 1M entry config — the exact
values that produced 0/247, so the measurement is comparable):

| Parameter | Value | Source |
|---|---|---|
| Entry model | `limit-on-return`, `fillEdge = mid` | 1M locked config |
| `retraceK` | **6** bars | 1M locked config |
| FVG detector | `_ict_offline` bull/bear FVG, **wick basis** (`useBody=false`) | shared module |
| Displacement | `dispMlt = 1.5 × ATR`, `atrLen = 14` | shared with D layer |
| Bars | MNQ 1-minute, `MNQ.v.0`, roll-excluded origins | §1 |

**Pre-registered threshold, frozen BEFORE the pull (this is the load-bearing number):**

| Measured retrace-to-mid rate within 6 bars | Disposition |
|---|---|
| **< 5%** | **WALL-CONFIRMED** — the 0/247 result is instrument-general, as the closure's mechanism prior predicted. Files to the MNQ ledger; forecloses `limit-on-return/mid/retraceK=6` on MNQ. No further 1M work implied. |
| **5% – 20%** | **WALL-CONFIRMED (marginal)** — fills exist but are too rare to reach the archived n≥100 floor at any plausible signal rate. Same disposition, recorded as marginal. |
| **> 20%** | **WALL-NOT-CONFIRMED** — the US500 result does not generalize. **Names, but does not open,** a follow-up decision (a full 1M execution design would need its own pre-registration and likely the last MNQ Cap seat). This session stops at naming it. |

The 5% / 20% boundaries are set now, with no MNQ 1m data pulled, and may not move.

**Reported alongside (diagnostics, never gates):** total FVGs detected, split bull/bear,
retrace-rate at `retraceK ∈ {3, 6, 12, 30}` (a *sensitivity curve*, explicitly **not** a
grid to select from — the verdict reads `retraceK=6` only), and the median bars-to-retrace
among those that do retrace.

---

## §4 — Forbidden moves

1. **Citing any RESOLVED-shaped 1H/1M result as a confirmation** or under the W/D
   free-confirmation ruling — §0; these are fresh findings needing their own intake.
2. **Running `harness_1m.py`'s 16-cell strategy ablation** — that is K-bound
   candidate generation, outside this campaign's governance.
3. **Selecting `retraceK` from the sensitivity curve.** The verdict reads `retraceK=6`.
   The curve is disclosure, and reading a better cell off it is the exact forking-paths
   move the archived ledger exists to prevent.
4. **Moving the 5% / 20% probe boundaries, the 1H `MARGIN_PP`, `lookN`, `eqBand`, `fwdK`,
   or either n-floor** after seeing any number.
5. **Re-tuning the 1M entry mechanism to manufacture fills** — the archived closure
   refused exactly this (`entryMode`/`fillEdge`/`retraceK` are the test object, not knobs).
   A 0%-fill result **is the finding**.
6. **Parent-NQ proxying either layer** — ledger W4; fills especially.
7. **Pulling with `--force`, or without a recorded pre-pull estimate and `--max-cost`.**
8. No `core/`, lock, allocation, `dd_protection`, Pine, or rail change.

---

## §5 — Audit hooks

```bash
git log --oneline -- lab/analysis/_inbox/ict_mnq_2026-08/PREREG_1H_1M.md | tail -1   # lock commit
git diff HEAD -- lab/archive/ict_cascade_2026-06-18/                          # must be EMPTY
grep -n "MARGIN_PP\|LOOKN_LOCK\|EQBAND_LOCK\|FWDK\|N_FLOOR" lab/archive/ict_cascade_2026-06-18/harness_1h.py
grep -n "retraceK\|limit-on-return\|0/247\|247" lab/archive/ict_cascade_2026-06-18/CLOSURE-1M-INSUFFICIENT-N.md
```

## Amendment log (append-only)

- **2026-08-03 — RATIFIED.** Frozen on this file's introducing commit, after the $0.00
  cost dry-run and **before** any 1H/1M bar was pulled. No value changed from the archived
  `PREREG-1H.md`; the 1M probe's 5%/20% boundaries are new and are declared here first.
