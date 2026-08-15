# Q-ICT-MNQ-1 — RESULTS (Layers D + W, frozen-key confirmation on NQ/MNQ)

**Theme:** _inbox

> **Layers 1H and 1M are in [`RESULTS_1H_1M.md`](RESULTS_1H_1M.md)** (fresh verdicts on
> databento MNQ native data): **1H FALSIFIED** on multi-regime data at ~12× the original's
> power, discharging its re-proposal bar; **1M fill wall NOT CONFIRMED** (59.06% retrace at
> the frozen `retraceK=6`, n=128,089, stable 58–60% across all eight years) — with an
> important scope limit on what that 59% does and does not license.

**Status:** ACTIVE — ICT cascade re-run on NQ/MNQ at $0/K=0/Cap seat unspent: W and D confirm on independent instruments, pools falsified a 3rd time, 1H falsified multi-regime, 1M fill wall not confirmed; no layer licenses a deployable edge
**Date:** 2026-08-03
**Pre-registration:** [`PREREG_D_W.md`](PREREG_D_W.md) — frozen at commit `6ef7577`, **before** any
NQ/MNQ number below was computed.
**Governance:** `CONFIRM-FREE-NODEPLOY-2026-08-03`
([`ruling`](../../../../docs/notes/2026-08-03-ict-instrument-confirmation-nodeploy-ruling.md)) —
free confirmation, **$0 / K=0 / no manifest / no Cap seat**, hard-committed to no deployment.
**Harnesses:** `lab/archive/ict_cascade_2026-06-18/harness_w.py` and `harness_d.py`, both run
**UNMODIFIED** (verified: `git diff HEAD -- lab/archive/ict_cascade_2026-06-18/` is empty).

---

## 1. Headline

**The US500 cascade's two RESOLVED belt findings replicate on independent instruments.**

| Layer | US500 (original, 2026-06) | **NQ (primary)** | MNQ (secondary) |
|---|---|---|---|
| **W** structure-only `gateHitRate` | **RESOLVED** 0.5571, CI [0.5242, 0.5901], eff_N 910 | **RESOLVED** **0.5880**, CI [0.5445, 0.6315], eff_N 483 | **RESOLVED** 0.5751, CI [0.5231, 0.6272], eff_N 346 |
| **D** SSL bear-FVG draw | **RESOLVED** 0.795 vs base 0.712 | **RESOLVED** **0.8630** vs base 0.7494 (n=73) | AMBIGUOUS-HOLD 0.8269 vs base 0.7806 (n=52) |
| **D** BSL bull-FVG draw | FALSIFIED | AMBIGUOUS-HOLD 0.7143 vs base 0.6816 (n=35) | FALSIFIED 0.6957 vs base 0.7234 (n=23) |
| **D** both pool sides | FALSIFIED (both **below** base) | FALSIFIED (both far below base) | FALSIFIED (both far below base) |

**On the primary panel (NQ), both findings under confirmation reproduced at the frozen
thresholds** — W RESOLVED on every limb (CI lower bound, halves, thirds, n-floor), and the
D SSL bear-FVG side RESOLVED (cleared base + CI half-width, stationary across halves,
selectivity-survived). Point estimates are **higher** than US500's, not merely comparable.

**This is a belt-strength upgrade, not a deploy license.** Per the governing ruling and
PREREG-W's own language, a RESOLVED W routes to *continued use + a per-entry transfer probe*,
explicitly **not** to deployment and **not** a 1M-gate license.

---

## 2. Layer W — detail

Runner: [`run_w_layer.py`](run_w_layer.py) → adapter [`build_w_export.py`](build_w_export.py)
→ archived `harness_w.evaluate_weekly()` (unmodified).
Frozen object: `gateBias = vStruct = sign(close − EMA(close, 20))`, scored against
`realized = sign(close − close[1])`, prior-week paired.

| | NQ (primary) | MNQ (secondary) |
|---|---|---|
| weekly bars | 526 (2016-07 → 2026-08) | 378 (2019-05 → 2026-08) |
| roll-excluded weeks | 40 | 29 |
| nGateScored / nGateHit | 483 / 284 | 346 / 199 |
| **point estimate** | **0.5880** | **0.5751** |
| block length `L_W` | 1 | 1 |
| effective N (floor 30) | 483 | 346 |
| 95% moving-block CI | **[0.5445, 0.6315]** | **[0.5231, 0.6272]** |
| halves (both must be > 0.50) | (0.6058, 0.5702) ✓ | (0.5780, 0.5723) ✓ |
| thirds (all must be > 0.50) | (0.6211, 0.5590, 0.5839) ✓ | (0.5826, 0.5913, 0.5517) ✓ |
| **VERDICT** | **RESOLVED** | **RESOLVED** |

`L_W = 1` (no week-over-week outcome autocorrelation above the 0.10 cutoff) matches the
original campaign's own `L_W = 1`, so effective N equals scored N on all three panels.

**Vote sub-verdict: `NOT-RUN` on both** — by construction, not by omission. Only `vStruct`
is reconstructable offline; `vSeason`/`vRates`/`vEarn` are line-cited to the lost
`.pine` and never transcribed in prose. `harness_w.evaluate_vote_importance` was called
explicitly and returned `NOT-RUN` through its existing intended path. This leaves the
original campaign's `COMPOSITE-KILLED` sub-verdict **neither confirmed nor challenged here**.

**Roll-exclusion sensitivity (diagnostic, not a verdict):** disabling the pre-registered
exclusion on NQ moves the estimate 0.5880 → 0.5832 (nGateScored 483 → 523) and leaves the
verdict RESOLVED. The exclusion is **not load-bearing for W** — expected, since a weekly
close-vs-EMA bias is not level-anchored the way FVG/pool objects are. Reported so the
declared cost of a quarterly-seasonal exclusion is visible rather than silent.

---

## 3. Layer D — detail

Runner: [`run_d_layer.py`](run_d_layer.py) → archived `harness_d.evaluate()` (unmodified).
Frozen: `drawK=10`, `dispMlt=1.5`, `atrLen=14`, `pvLen=3`, wick basis, radius-matched MC
null ≥5000 draws/side, PASS band `rate > base + 95% CI half-width`, n-floor 30 effective
blocks, verdict **per side**.

> Naming (the archived harness's own R4-6 note): `BSL.fvg` **is** the bull FVG (a downward
> draw); `SSL.fvg` **is** the bear FVG (an upward draw). The BSL/SSL keys are pool-side
> bucket labels; each FVG null is radius-matched *within* its bucket.

### NQ (primary) — 2,537 daily bars, 272 roll-window bars excluded as object origins

| side / object | rate | n (blocks) | base | halves | reads |
|---|---|---|---|---|---|
| BSL pool | 0.5401 | 187 | 0.7756 | (0.585, 0.495) | far **below** base |
| BSL fvg (bull) | 0.7143 | 35 | 0.6816 | (0.667, 0.765) | clears, **non-stationary** (h1 < base) |
| SSL pool | 0.3128 | 211 | 0.6014 | (0.245, 0.381) | far **below** base |
| **SSL fvg (bear)** | **0.8630** | **73** | **0.7494** | **(0.838, 0.889)** | **clears + stationary** |

**VERDICT[SSL] = RESOLVED** — "cleared, stationary, selectivity-survived: `['fvg']`".
**VERDICT[BSL] = AMBIGUOUS-HOLD** — the bull-FVG side clears the PASS band but its first
half (0.667) sits below the base rate (0.6816), so it fails the stationarity limb.

### MNQ (secondary) — 1,823 daily bars, 196 roll-window bars excluded

| side / object | rate | n (blocks) | base | halves | reads |
|---|---|---|---|---|---|
| BSL pool | 0.5303 | 132 | 0.8020 | (0.500, 0.561) | far **below** base |
| BSL fvg (bull) | 0.6957 | 23 | 0.7234 | (0.750, 0.636) | below base; also under n-floor |
| SSL pool | 0.3397 | 156 | 0.6502 | (0.359, 0.321) | far **below** base |
| SSL fvg (bear) | 0.8269 | 52 | 0.7806 | (0.769, 0.885) | clears, **non-stationary** (h1 < base) |

**VERDICT[SSL] = AMBIGUOUS-HOLD**, **VERDICT[BSL] = FALSIFIED**.

MNQ's bear-FVG side is **directionally consistent** with NQ and US500 (0.8269 > base 0.7806)
but its first half (0.769) dips just below base, so the frozen stationarity limb routes it to
AMBIGUOUS-HOLD rather than RESOLVED. Given MNQ is the shorter, wholly-post-2019 panel — and
is the *secondary*, declared before scoring — this does not disturb the NQ-primary verdict.

### The pool finding replicates hardest of all

On **all three instruments**, both pool sides sweep **substantially less often than a
radius-matched random walk** (NQ SSL 0.3128 vs 0.6014; MNQ SSL 0.3397 vs 0.6502) — the same
direction and rough magnitude as US500's original (0.55/0.34 vs 0.76/0.61). "Old highs/lows
act as draw-on-liquidity attractors" is now **falsified on three independent instruments**,
and it is the most robust result in this study.

---

## 4. What was found *about the instruments*, not the mechanism

**BAR_EXPORT v0.2 breaks the archived D loader (caught, fixed at the schema-adapter layer).**
`harness_d.SIGNAL_PIPE_RE` anchors on `…|volume$`, matching **v0.1** only; the delivered v0.2
files append `|epoch2|N|M|SYMBOL|futures|USD||tick|pointval|tz|tf`, so **every row was dropped**
and the harness reported a spurious `INSUFFICIENT-N` at 0 bars on both panels. This was caught
**only** because the archived loader emits a loud WARN naming the drop count
(`dropped 2537 of 2537 Entry rows`) — a silent loader would have produced a clean-looking,
entirely false null. Fixed by loading through the v0.2-tolerant `build_w_export.load_bar_export_ohlc`
and handing the arrays to the archived, unmodified `HD.build_bars` — the schema-adapter path
the campaign README prescribes for TV format drift. **No verdict logic was touched.**

**TV `1!` continuous series are not back-adjusted (measured, pre-registration).** 17 quarterly
gaps of +0.8–1.6% cluster within ±4 days of 3rd-Friday CME expiry, every quarter from 2022-09
through 2026-03. The exclusion rule this motivated removed 272 NQ / 196 MNQ daily bars and
40 NQ / 29 MNQ weekly bars as object origins.

---

## 5. Scope limits (read before citing any number above)

1. **No deploy license.** `CONFIRM-FREE-NODEPLOY-2026-08-03` bars re-framing a RESOLVED
   result here as a deployability gate. Any tradable expression needs a fresh, separate,
   K-bound proposal that pays its own K and re-runs reachability against the family bank
   *at that time*.
2. **W's scope is leg (a) only** — the weekly-close structure-only hit rate. PREREG-W is
   explicit that per-entry gate accuracy (leg b) is a *separate* probe, **not settled** by
   this verdict. `SLR-MYM-1` §2.1 records the overclaim to avoid here.
3. **1H and 1M are untouched** and are explicitly outside the governing ruling — they are
   fresh verdicts (US500's 1H was FALSIFIED, 1M INSUFFICIENT-N; there is no closed RESOLVED
   finding to "confirm"). They need `PREREG_1H_1M.md` frozen before the databento pull.
4. **Structural persistence ≠ tradability.** The ICT family's own record on this repo's data
   is otherwise negative — `SPX500 × ict-liquidity` is **DEAD**, `pharos_us500_sweepfvg`
   FALSIFIED on robustness (drop-top-3 −0.152R), and the 1M execution layer has never
   produced a single filled trade anywhere (0/247). Two structurally-real components do not
   make a system.
5. **The vote sub-verdict is unmeasurable here** — `NOT-RUN` is neither support for nor
   evidence against the original `COMPOSITE-KILLED` finding.
6. **MNQ's D-SSL is AMBIGUOUS-HOLD, not a second RESOLVED.** Do not quote MNQ's 0.8269 as a
   confirmation; the primary/secondary split was declared before scoring precisely so this
   could not be reframed after the fact.

---

## 6. Reproduce

```bash
python -m pytest lab/analysis/_inbox/ict_mnq_2026-08/ -q      # 28 passed (adapter unit tests)
python lab/analysis/_inbox/ict_mnq_2026-08/run_w_layer.py     # Layer W, both panels + roll diagnostic
python lab/analysis/_inbox/ict_mnq_2026-08/run_d_layer.py     # Layer D, both panels
git diff HEAD -- lab/archive/ict_cascade_2026-06-18/   # must be EMPTY (harnesses unmodified)
```

Inputs are the four operator TV exports of 2026-08-03 in `C:/Users/joshu/Downloads/`
(vendor data, gitignored — not committed):
`..._NQ1!_..._a9506.csv` (W), `..._NQ1!_..._74b3d.csv` (D),
`..._DL_MNQ1!_..._03862.csv` (W), `..._MNQ1!_..._88b46.csv` (D).
