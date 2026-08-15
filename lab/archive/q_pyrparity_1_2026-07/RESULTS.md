# Q-PYRPARITY-1 Phase 2 — Branch B verification results
#
# Parent brief: docs/briefs/Q-PYRPARITY-1-watch1-pyramid-proportionality.md
# Pre-registration: docs/briefs/pre-registration/Q-PYRPARITY-1-verdict-preregistration.md
# Phase 0: PHASE0.md (Branch B selected; structural proportionality CONFIRMED-IN-SOURCE)
#
# Executed: 2026-07-17 · Cursor (mechanical verification of operator TV exports)

**Overall verdict: `FALSIFIED-NONPROPORTIONAL`**

MYM fails §4 median band hard (base median 0.871 / add 0.916 vs required 0.500 ± 0.005).
MNQ alone would be `AMBIGUOUS-HOLD` (list misalignment + base fill-frac). Overall dominated by MYM.

§6 disposition (brief): apply the documented fallback — WATCH-1 haircut at the
**account-multiplier layer** for the two pyramided legs; Q-RAIL-1 F1 = PASS-via-fallback.
Phase 3 propagation (lifecycle.md:113, Q-RAIL-1 F1, STATE multiplier-spine flag) still owed.

---

## 0. Inputs

| Role | File (local) | sha256 (12) | Notes |
|---|---|---|---|
| MYM r0 (0.70%) | `MYM_r070_f5ecb.csv` | `9acfa29726a9…` | **Byte-identical** to panel-of-record `…15d8b.csv` |
| MYM r0/2 (0.35%) | `MYM_r035_8d6b5.csv` | `fa72ad725764…` | Same 232 base / 35 add timestamps as r0 |
| MNQ r0 (0.37%) | `MNQ_r037_9b6c8.csv` | `8c99a28fde76…` | Not byte-identical to `…beabf.csv` (228/47 vs panel 237/47) |
| MNQ r0/2 (0.185%) | `MNQ_r0185_b2723.csv` | `832d766e53dd…` | 242 base / 49 add — **more** fills than r0 |

Risk-input identity is corroborated by the data (not just filenames):
- MNQ early bases pair at raw qty ratio ≈ 0.50 (38→19, 50→25, …).
- MYM below the ceiling pairs at ≈ 0.50 (12→6); at the ceiling both print 17.

Protocol: Branch B — per-fill `[qty/equity](r½) / [qty/equity](r0)`, add normalized on
**entry-bar** equity (Phase 0 rule). `equity_at_entry = 200000 + (cumPnL − tradeNetPnL)`.
Harness: `verify_phase2.py` → `phase2_report.json`.

---

## 1. Cohort tables vs §4 bands

Accept requires **both** legs × **both** cohorts: ≥95% of paired fills within 0.500 ± 0.02,
median within 0.500 ± 0.005, identical signal timing.

### MYM (DJ30 → MYM1!) — `FALSIFIED-NONPROPORTIONAL`

| Cohort | n_r0 | n_r½ | paired | only_r0 / only_r½ | median Branch B | frac in ±0.02 | raw qty median | Fill band | Median band |
|---|---:|---:|---:|---|---:|---:|---:|---|---|
| base | 232 | 232 | 232 | 0 / 0 | **0.8707** | 0.082 | 0.824 | FAIL | FAIL |
| add  | 35  | 35  | 35  | 0 / 0 | **0.9164** | 0.086 | 0.882 | FAIL | FAIL |

Timestamps pair perfectly (signal path untouched). Medians far outside 0.500 ± 0.02 → reject.

### MNQ (NAS100 → MNQ1!) — `AMBIGUOUS-HOLD` (leg-level)

| Cohort | n_r0 | n_r½ | paired | only_r0 / only_r½ | median Branch B | frac in ±0.02 | raw qty median | Fill band | Median band |
|---|---:|---:|---:|---|---:|---:|---:|---|---|
| base | 228 | 242 | 228 | 0 / **12** | 0.4888 | **0.715** | 0.381 | FAIL | PASS (±0.005) |
| add  | 47  | 49  | 47  | 0 / **2**  | 0.4990 | **1.000** | 0.376 | PASS | PASS |

- Add cohort is textbook-proportional on the paired subset.
- Base median passes the tight band; fill-frac fails — almost all misses are integer-contract
  rounding at small qtys (e.g. 5→2 raw 0.40; Branch B ~0.39). At ±0.05, base frac = 0.978.
- Trade lists **misalign**: half-risk run adds 12 bases + 2 adds. Consistent with the
  dollar-fixed day-stop / halt gates binding less often at smaller $ risk — risk input
  touches the *effective* signal path. §4 → AMBIGUOUS-HOLD (not add-clipping; counts rose).

---

## 2. Mechanism (MYM) — binding contract ceiling, not risk-input non-linearity

Pine is linear in `riskPerTrade` (Phase 0). The TV observation shows a **hard qty ceiling**:

| Slice (MYM base) | n | Branch B median | raw qty median |
|---|---:|---:|---:|
| both at qty **17** | 87 | 1.042 | 1.000 |
| r0 at 17, r½ below | 123 | 0.764 | 0.706 |
| r0 **below** 17 | 22 | **0.502** | **0.500** |

| Slice (MYM add) | n | Branch B median | raw qty median |
|---|---:|---:|---:|
| both at qty **127** (= 17 × 7.5, floored) | 14 | ~1.0 | 1.000 |
| r0 at 127, r½ below | 16 | (mixed) | (mixed) |
| r0 **below** 127 | 5 | **0.496** | **0.495** |

**Below the ceiling, H-PYRPARITY-1 holds.** Above it, halving risk cannot halve size — r0 is
already clipped — so the realized stack ratio collapses toward 1.0. r0 histogram: **210 / 232**
base fills sit at exactly 17; adds **30 / 35** at exactly 127. No `floor`/`cap` exists in the
locked Pine sizing path (Phase 0); this ceiling is a **TV / symbol-runtime** behavior on
`CBOT_MINI:MYM1!` at `$200K` initial capital — exactly the class of invisible non-linearity
§7 Phase 1 was required to observe.

MNQ shows no analogous hard ceiling in-range (base max 149 at r0; half tracks ~0.5).

---

## 3. Gate assertion (§6)

| Verdict | Trigger | Fired? |
|---|---|---|
| `RESOLVED-PROPORTIONAL` | both legs × both cohorts meet bands + timing | **No** |
| `FALSIFIED-NONPROPORTIONAL` | any cohort median outside 0.500 ± 0.02, OR add count drops | **Yes — MYM both cohorts** |
| `AMBIGUOUS-HOLD` | misaligned lists (non-add-clip) / undecidable rounding | MNQ only (subordinate) |

**Overall: `FALSIFIED-NONPROPORTIONAL`.**

Documented fallback (brief §6 + `strategy_lifecycle.md:113`): apply WATCH-1 haircut at the
**account-multiplier layer** for DJ30/MYM and NAS100/MNQ; do **not** rely on risk%-input
scaling to realize the c1 WATCH-1 book-level ×0.5. Q-RAIL-1 F1 = PASS-via-fallback.
Also re-opens the multiplier-spine forward-relevance flag (STATE 08-08) in the affirmative.

Lesson candidate: source-linear Pine + TV symbol ceiling = “proportional in code,
non-proportional in fills” — the §0 OPEN item’s exact risk. Uncapped-slice evidence
shows the *input* path is fine; the *runtime ceiling* is the falsifier.

---

## 4. Phase 3 checklist

- [x] Flip `docs/methodology/strategy_lifecycle.md:113` OPEN → CONFIRMED-FALLBACK (dated) with link here
- [x] Mark Q-RAIL-1 F1 = PASS-via-fallback
- [x] Affirm multiplier-spine STATE forward-board flag
- [x] Closure file `docs/briefs/closures/Q-PYRPARITY-1-closure-falsified-nonproportional.md`
- [x] Land Phase 0+2+3 onto a main-tracking branch (`cursor/q-pyrparity-1-phase3`)

---

## 5. Audit hooks

```bash
python lab/archive/q_pyrparity_1_2026-07/verify_phase2.py
python lab/archive/q_pyrparity_1_2026-07/diagnose_phase2.py
# MYM r0 still byte-identical to panel of record:
python -c "import hashlib, pathlib; p=pathlib.Path('core/data/tv_exports/cme/Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-11_15d8b.csv'); n=pathlib.Path('lab/archive/q_pyrparity_1_2026-07/MYM_r070_f5ecb.csv'); print(hashlib.sha256(p.read_bytes()).hexdigest()==hashlib.sha256(n.read_bytes()).hexdigest())"
```
