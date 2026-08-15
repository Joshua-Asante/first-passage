# Q-ICT-CASCADE-1 / Layer 1H (Premium/Discount) — CLOSURE: FALSIFIED

**Layer:** Q-ICT-1H · **Verdict:** `FALSIFIED` · **Date:** 2026-06-19
**Licenses the 1M PD gate:** NO
**Pre-registration:** [`PREREG-1H.md`](PREREG-1H.md) (frozen; see its 2026-06-19 amendment for the run-1-void + faithfulness-fix audit trail)
**Verdict instrument:** [`harness_1h.py`](harness_1h.py) (corrected; `M-ICT-1H-OFFSET`)
**Export of record:** `PEPPERSTONE_US500, 60_a6b6b.csv` (US500 Pepperstone 1H, **3039 bars, 2025-12-11 → 2026-06-18 UTC**; cols `time,open,high,low,close,zone,eq,premHit,discHit,zoneGate,zoneAgree`)

---

## 1. Verdict vs the §6 / PREREG gate

| Gate condition (PREREG-1H §6 RESOLVED needs ALL) | Threshold | Observed | Pass? |
|---|---|---|---|
| effective-N per scored zone | ≥ 30 | prem **151**, disc **92** | ✅ (powered — a decision, not INSUFFICIENT-N) |
| a rate's de-overlapped CI clears 0.5 by ≥2pp under BOTH stride AND block | lb > 0.52 | prem stride 0.5085 / block 0.4725; disc stride 0.5641 / block 0.5430 — **all CIs straddle 0.5** | ❌ |
| real rate beats the placebo (1H-E5) | rate > floor | prem 0.5085 vs floor 0.4656 (beats); disc 0.5430 vs floor 0.5340 (barely) | — (moot once CI fails) |
| winning anchor cell clears 0.5 by ≥2pp AFTER the 9-cell penalty | lb > max(0.52, e_max) | prem winner 0.5085 < e_max 0.5623; **disc winner 0.5798 < e_max 0.5812 (fails by 0.0014)** | ❌ |
| transfer pre-gate clears (both axes) | ≥90% AND ≤3pp | range-LAG agree **0.994** / gap **0.000** clears; price-BASIS **moot** (no PASS to license) | — |

**Trigger fired:** FALSIFIED = *"both premium-down AND discount-up de-overlapped rate CIs straddle 0.5 across anchors after the multiplicity penalty — the split is decorative."*

## 2. What the pre-registration predicted vs what happened

- **Power floor held:** the PREREG's worst-case (~21 independent premium windows) was conservative; the real export yields 151/92 effective windows, so the straddle is a powered negative, not a starvation artifact (`INSUFFICIENT-N` correctly NOT triggered).
- **Direction asymmetry the PREREG did not call:** premium→down is dead (0.47–0.51 — premium does **not** resolve down in this window), while **discount→up is the live-ish side (0.54–0.58)**, failing the multiplicity penalty by **0.0014** (0.5798 vs e_max 0.5812). Economically coherent: in an uptrend, discounts get bought back up (a tailwind), premiums continue up (no reversion). The frozen gate still falsifies — the near-miss does not clear de-overlap + placebo + penalty.
- **Transfer:** the range-LAG axis cleared trivially (agree 0.994, gap 0.000 — the `[1]`-lag barely moves a 60-bar range), confirming the on-chart transfer instrument works; the price-BASIS axis was correctly **not required** (a FALSIFIED has no PASS to license, so the paired 1M export was unnecessary — cheapest-falsifier-first held).

## 3. Instrument defect found + fixed this run (`M-ICT-1H-OFFSET`)

The first scoring was **VOID** — `recompute_hits` had transcribed Pine's historical offset `series[fwdK]` (= fwdK bars BACK, DRAFT L81-86) as a **forward** array index `series[i+fwdK]`, scoring the **complement** of the claim ("price rose into a premium zone" instead of "premium resolves down"). It matched the exported Pine columns only ~36% (the faithful backward form matched 100%) and its rates were the complement of Pine's (0.49/0.44 vs 0.47/0.54). The look-ahead audit fired `ok=False` (~49%) but the harness **mis-handled it** — discarding the correct exported columns for the buggy recompute. Fix = faithfulness correction (decision-bar form, resolution-bar audit, placebo direction, re-pinned tests + a complement-regression guard); **direction-agnostic** (void run and corrected run both FALSIFIED); **no §-criterion moved**. Full audit trail: PREREG-1H 2026-06-19 amendment. Why a "reviewed" pre-registered instrument shipped it: the unit tests were self-referential (encoded the same inversion) and there was no real export to contradict them until now — lesson `M-ICT-1H-OFFSET`.

## 4. "Which nulls remain alive" (per strategy-validation §0 / Appendix D)

- **premium→down (the headline ICT P/D claim):** falsified on this regime — does not beat a coin flip.
- **discount→up:** NOT cleanly alive (fails the gate) but NOT cleanly dead either — a documented **near-miss**, routed to a **forward-watch belt finding**, not an action.
- **Regime null still ALIVE:** this is ONE benign 6.5-month uptrend (TV's 1H history cap for US500). A chop/down regime is untested. Re-proposal bar = **multi-regime / longer 1H data**, not re-tuning the frozen knobs (§5 forbidden).
- **Cascade-licensing:** the 1H layer licenses NOTHING about the 1M PD gate (it is falsified, and the transfer was not completed). The 1M layer must stand or fall on its own end-to-end run.

## 5. Cascade state

3/5 verdicted: **W RESOLVED** · **D SSL-RESOLVED / BSL-FALSIFIED** · **1H FALSIFIED**. Remaining: **1M** (the 16-export gate-ablation × `useBody` on a multi-regime window). The W and D verdicts were independently re-audited this session and are **unaffected** by the 1H defect.

## 6. Lesson candidates

- **`M-ICT-1H-OFFSET`** (dated, dollar-free — methodology-layer): a pre-registered, "adversarially reviewed" offline instrument shipped a verdict-flipping scoring inversion (Pine historical-offset `[fwdK]` transcribed as a forward array index). Self-referential unit tests cannot catch a scoring-direction bug — a real-data anchor (here, the exported Pine columns + the look-ahead audit) is required. Corollary: a look-ahead/faithfulness audit that fires on a mismatch must **halt or surface**, never silently prefer its own recompute over the source-of-truth export. Recorded in `docs/methodology/lessons/methodology_lessons.md` (M-15).
