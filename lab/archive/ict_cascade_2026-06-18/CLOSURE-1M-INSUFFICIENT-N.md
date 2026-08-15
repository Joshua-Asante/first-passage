# Q-ICT-CASCADE-1 / Layer 1M (Execution) — CLOSURE: INSUFFICIENT-N

**Verdict:** `INSUFFICIENT-N` (claim unfalsifiable on available data; HALT per PREREG-1M).
**Date:** 2026-06-19 · **Layer:** Q-ICT-1M (1M raid→FVG execution strategy)
**Pre-registration:** [`PREREG-1M.md`](PREREG-1M.md) · **Parent:** [`TEST_PLAN.md`](TEST_PLAN.md) (§6 1M row)
**Operator path:** the operator chose **"Override F8, run single-regime"** (AskUserQuestion 2026-06-19) to attempt the 1M layer on the available window. The override ran straight into the wall from two independent directions; the disposition is `INSUFFICIENT-N` regardless of the override.

---

## 1. Verdict — the dual wall

The 1M layer is `INSUFFICIENT-N` on **two independent grounds**, either of which is sufficient:

1. **n = 0 closed trades (0% fill rate).** On the all-gates-off, `useBody=false` run (the most permissive of the 16 ablation cells), the strategy **placed 247 limit orders and filled 0** (`fill rate (lmt) 0% (0/247)`); all 247 were cancelled by **expiry** (`lmt cancel exp/flip 247 / 0`). `closed trades = 0`, `net profit = 0`. The n-floor is **100** (PREREG-1M L69) → `n=0 ≪ 100` → `INSUFFICIENT-N` (HALT).
2. **Single-regime ~2-day 1m window.** Even at "max history loaded," TV serves only ~2 trading days of 1-minute US500 (Pepperstone) — the visible+loaded span was ~2026-06-24→06-26. The F8 BINDING SPEC (PREREG-1M GENUINE CHOICE 3, ratified) requires a window spanning **both the 2020-2023 chop AND the 2023-2026 trend**; ~2 days of recent data is a single benign regime → the spec is unmet → a verdict on it would be void anyway.

---

## 2. Diagnosis — where the chain dies (B4 starvation, live)

The on-chart diagnostic table (the campaign's B4 instrument) localizes the failure precisely:

| Cell | Value | Reading |
|---|---|---|
| `closed trades` | **0** | no completed round-trip — n=0 |
| `fill rate (lmt)` | **0% (0/247)** | 247 orders **placed**, **0 filled** |
| `lmt cancel exp/flip` | **247 / 0** | all 247 expired unfilled; 0 flip-cancels (confirms gates off) |
| `skip: cost/R` | 6 | target-geometry filter rejected only 6 |
| `skip: no draw` | 8 | DOL target invalid on only 8 |
| `last cost hurdle` | 0.163R | cost-law is small, not the constraint |

**The raid → FVG → DOL-target chain works** (only 14 target-rejects vs 247 placements). The failure is **entirely at the entry fill:** the locked entry is `entryMode = limit-on-return`, `fillEdge = mid`, `retraceK = 6` — it places a limit *inside* the FVG expecting price to **retrace to the FVG mid within 6 one-minute bars**. On 1m US500, displacement FVGs **continue rather than retrace** in 6 minutes, so **247/247 expire unfilled.** A 0% fill rate over 247 attempts is not "rare retrace" — the `limit-on-return mid` entry is effectively **non-viable on a 1m index as configured.**

(`closed trades = 0` is TV's strategy-engine count and is authoritative; it corroborates genuine zero fills independent of the known `fillRate`-undercount caveat 1M-E5.)

---

## 3. What PREREG-1M predicted vs what happened

- PREREG-1M **Power disclosure / n-floor:** "n < 100 closed trades after the starvation fix (B4) → `INSUFFICIENT-N` … HALT and re-spec." → **Fired exactly:** n=0.
- PREREG-1M **GENUINE CHOICE 3 (F8 BINDING SPEC):** "data-availability dependent … a window confined to either [regime] alone … voids the verdict." → **The data does not exist** on the canonical 1m feed; the operator could not assert the multi-regime span.
- PREREG-1M **Forbidden #4** (single benign window) and the §7.A B0 dissent anticipated this is the D2-family layer; the dissent's whole purpose was to refuse a single-window pass. Here there is not even a population to pass.

The override did **not** escape the wall — it **demonstrated** it from the strategy side (0% fill) in addition to the data-availability side (single-regime 1m).

---

## 4. Cascade-level summary — Q-ICT-CASCADE-1 CLOSED

| Layer | Verdict | Note |
|---|---|---|
| **LIB** (primitives) | foundation OK | orientation/edges/clocks ratified (B1 standard-ICT) |
| **W** (Weekly bias) | **RESOLVED** | structure-only gateHitRate 0.5571, block-CI lb>0.50; composite vote adds nothing; **does NOT license the gate**; routes to path-independent confirmation, not deploy |
| **D** (Daily DOL) | **SSL bear-FVG RESOLVED / BSL + both pools FALSIFIED** | side-split, single-panel; RESOLVED side routes to confirmation, not deploy |
| **1H** (Premium/Discount) | **FALSIFIED** | de-overlapped prem→down 0.4725 / disc→up 0.5430 both straddle 0.5 after the 9-cell penalty; defect-fixed this session ([`CLOSURE-1H-FALSIFIED.md`](CLOSURE-1H-FALSIFIED.md), lesson M-15) |
| **1M** (Execution) | **INSUFFICIENT-N** | n=0 (0% fill) + single-regime ~2-day 1m → F8 unmet |

**Net:** no layer licenses a deployable edge. The two RESOLVEDs are structure-only / single-side single-panel and route to path-independent confirmation; the 1H is falsified; and the **execution layer — the only layer that would produce a tradeable P&L — is un-runnable on the canonical 1m feed** (0 fills, single-regime). The campaign closes having found **no validated end-to-end edge** for the ICT cascade on US500.

---

## 5. Cross-instrument implications (NAS100 and any other instrument)

**Verdicts do NOT transfer.** Each layer verdict is single-instrument, mostly-single-regime evidence; PREREG path-independence requires confirmation on an *independent instrument/period*. So US500's results say nothing dispositive about NAS100 — NAS100 is **not** "pre-falsified," and US500's W/D RESOLVED sides do **not** carry over.

**But the two BLOCKING findings are instrument-general and would very likely recur on NAS100:**
- **(a) The 0% limit-fill rate is a property of the entry mechanism, not of US500.** `limit-on-return / mid / retraceK=6` needs a pullback into the FVG within 6 one-minute bars. NAS100 is an equally (arguably more) impulsive 1m index; displacement FVGs continue rather than retrace within 6 bars the same way → the execution layer would **very likely be un-fillable on NAS100 too.** (Strong mechanism prior, not a measured fact — but it is the *same* mechanism, not a symbol quirk.)
- **(b) The 1m data wall is platform/feed-general.** TV's 1-minute history cap (~days) is not US500-specific → NAS100 1m on TV hits the same n<100 starvation and the same **F8 multi-regime impossibility** (2020-2023 1m is unreachable for any TV instrument). You could not *validate* the 1M layer on NAS100 on the canonical feed.

**Structural design tensions are also instrument-general:** the 1H premium/discount mean-reversion gate fights the trend bias the 1M needs (premium continues *up* in a trend; bias∧PD becomes near-contradictory in a trend). NAS100 is an even stronger secular trender over 2020-2026, so the same 1H-straddles-0.5 pattern would likely recur.

**Bottom line for deployment:** there is **no evidence supporting deploying the ICT 1M execution system on NAS100 — or any instrument.** The only layer that yields a tradeable edge has **never produced a single filled trade anywhere** (0/247 on US500), and the blocker (entry design + 1m data availability) is instrument-general. Before NAS100 is even a question, two things must hold, and neither does today: (1) the **entry mechanism must be redesigned** (e.g. market-on-FVG, wider `retraceK`, or near-edge fill) and demonstrably fill; (2) a **validatable multi-regime 1m data path** must exist (the canonical TV/Pepperstone feed cannot provide one).

**NAS100-specific governance caveat:** NAS100 is a **live, locked, funded instrument** (Striker NAS100 v1, in the book). Overlaying a concept-stage, execution-unvalidated ICT system on a funded instrument would be premature and high-risk, and NAS100 has **no instrument ledger yet** — a new concept there needs its own ledger + anti-SNAG accounting (operational rule 10) before any test. The locked Striker NAS100 v1 is validated and live; the ICT cascade is validated **nowhere**.

---

## 6. Forbidden moves NOT taken (audit-clean)

- Did **not** change the locked target/gate params (`pvLen=2`, `dispMlt=1.5`, `raidWin=8`, `dolMode=range-extreme`, `minRmult=4`, `minAbsR=2`, `useDOL=true`, `riskPct=0.5`) to manufacture trades (PREREG-1M Forbidden #3/#7).
- Did **not** swap the entry mechanism (`entryMode`/`fillEdge`/`retraceK`) to force fills — that is outcome-conditional tuning of the test object. The strategy as designed yields 0 fills; that is the finding, not a knob to turn.
- Did **not** read the on-chart `$`/winRate/PF table as a verdict (Forbidden #6) — there is no population to read.

---

## 7. Lesson candidates (CANDIDATE — promotion on second firing)

- **A 1-minute execution strategy cannot be falsification-validated on TV's canonical feed.** The 1m-history cap (~days for US500) defeats BOTH the n≥100 power floor AND any multi-regime requirement simultaneously. Any future 1m-execution concept inherits this wall — the *gate-bearing* feed (TV/Pepperstone, tv-csv-canonical) is structurally unable to supply a multi-regime 1m population. Record before re-attempting any 1m execution layer on any instrument.
- **A 0% limit-fill rate over a large order count is a non-viability signal, not a tuning problem.** `limit-on-return mid` + tight `retraceK` on a fast 1m index expects a retrace that displacement FVGs do not deliver. Forward strategy-dev candidate (entry redesign), out of scope for falsification. Filed as **F9** in [`ops/instruments/SPX500.md`](lab/archive/../../ops/instruments/SPX500.md).

---

## 8. Disposition & follow-ups

- **Q-ICT-CASCADE-1 → CLOSED.** All five layers disposed (LIB OK · W RESOLVED · D SSL-RESOLVED/BSL-FALSIFIED · 1H FALSIFIED · 1M INSUFFICIENT-N). No layer licenses deployment.
- **No re-run of the 1M layer on a wider/new-params 1m window** — it would still be single-regime + sub-fill (voids the frozen verdict / re-proposing the same key returns DUPLICATE).
- **The entry-mechanism redesign** (F9) is a separate, optional strategy-dev effort, NOT a continuation of this falsification campaign; it is gated behind a validatable 1m data path that does not currently exist.
- **No `core/` / lock / allocation / dd_protection change.** Lock stands 99.83/0.17/4.37.
