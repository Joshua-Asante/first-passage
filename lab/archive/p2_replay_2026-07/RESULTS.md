# P2 replay — Phase B RESULTS (K2 + E1, scored)

**Disposition:** FALSIFIED — P2 FALSIFIED for this venue — both legs K2-kill

**Date:** 2026-07-03 · **Parent:** [`docs/adr/2026-07-03-hardcore-p2-edge-transfer-gate.md`](lab/archive/../../docs/adr/2026-07-03-hardcore-p2-edge-transfer-gate.md) (#272) · **Harness:** Phase A (#273), rules frozen at fixture-green
**Window (operator §0.5-b pin, one shot):** 2025-07-03 → 2026-07-03 (ET; trades present through 2026-06-30)
**Gates (operator-ratified 2026-07-03, as authored):** K2 kill > 10% signal-set divergence · E1 pass = PF ≥ 0.8× AND net ≥ 0.7× vs paired Pepperstone baseline
**Roll treatment (§0.5-c):** both computed; identical here (ROLL-SEAM bucket = 0 on both legs), so the carve-out decision is moot for this run.

## Verdicts (per frozen rules + ratified gates)

| Leg | K2 divergence (with-roll / ex-roll) | K2 verdict | E1 PF ratio | E1 net ratio | E1 verdict |
|---|---|---|---|---|---|
| DJ30 (US30 ↔ MYM1!) | **20.00% / 20.00%** (10 of 50 union) | **KILL** | 0.619 | 0.256 | **MISS → AMBIGUOUS** |
| NAS100 (NAS100 ↔ MNQ1!) | **35.59% / 35.59%** (21 of 59 union) | **KILL** | 0.584 | 1.468 | **MISS → AMBIGUOUS** (PF floor fails; net passes — both required) |

**Both in-scope legs K2-kill at the ratified 10% threshold.** Per the parent ADR §4 as written, all-legs-hard-kill triggers the "P2 is FALSIFIED for this venue" branch. E1 misses close AMBIGUOUS with the taxonomy below as the written cause — no re-run with a shifted window (§5.5). Disposition (accept the §4 branch vs open a fresh pre-registered question on pairing semantics — see Observations) is operator-owned.

## Divergence taxonomy

All divergences on both legs classified **BASIS** (both feeds have the bar; the entry condition flips). ROLL-SEAM = 0, SESSION = 0, DATA-GAP = 0 on both legs.

DJ30 (10): 2025-11-21 11:15 pep / 11:30 cme · 2025-11-25 14:00 pep / 14:30 cme · 2025-11-28 09:30 cme, 10:15 pep, 11:00 cme · 2025-12-02 10:45 cme · 2025-12-05 09:45 cme / 10:00 pep.
NAS100 (21): 16 pep-only vs 5 cme-only — the CME feed fires materially FEWER signals (n=42 vs 55 trades in-window); full timestamp list in the run log.

## E1 envelope inputs (same-window paired exports)

| Leg | baseline n / PF / net | CME replay n / PF / net |
|---|---|---|
| DJ30 | 44 / 5.642 / $117,349.57 | 46 / 3.491 / $30,097.00 |
| NAS100 | 55 / 4.217 / $147,273.17 | 42 / 2.463 / $216,232.00 |

## Observations (findings for disposition — NOT re-scores; pairing/alignment rules stayed frozen per §5.3)

1. **±1–2-bar offset pairs.** A visible fraction of "divergences" are near-adjacent pep-only/cme-only pairs (DJ30: 11:15↔11:30, 14:00↔14:30, 09:45↔10:00; NAS100: 12:45↔13:00, 12:30↔12:45) — plausibly the *same* signal firing one bar later on the other feed, which exact-timestamp pairing counts as two divergences. The frozen rule scored what it scored; a tolerant-pairing re-score would be a **new pre-registered question** (fresh Pre-Q / ADR amendment), not an edit here. Even generously collapsing all visible adjacent pairs, NAS100's 16-vs-5 pep-only asymmetry survives — the direction (CME fires fewer signals) is not a pairing artifact.
2. **Net ratios are mechanically scaled by point value; PF is the cleaner transfer signal.** MYM = $0.50/pt and MNQ = $2/pt vs the CFD legs' $1/pt. If the locked Pine's sizing does not adapt via `syminfo.pointvalue`, MYM P&L is mechanically ~0.5× and MNQ ~2× per unit qty (NAS100's net ratio 1.468 ÷ 2 ≈ 0.73 — right at the floor; DJ30's 0.256 × 2 ≈ 0.51 — still a miss). The **PF ratios (0.619 / 0.584) are exposure-insensitive and both fail the 0.8× floor decisively** — the per-trade edge quality degrades on the CME continuous feed regardless of the sizing question.
3. **ROLL-SEAM = 0 likely reflects back-adjusted continuous data, not absence of roll effects.** Back-adjustment removes roll price gaps, so the threshold-based seam detector (reused `roll_mask.flag_roll_seams`, 0.5%) finds nothing. The EXPORT_SPEC's adjustment-mode screenshots were not delivered with the exports — recorded as a provenance gap; the with-roll/ex-roll numbers are identical either way for this run.
4. **E2 input note (measured basis delta):** the BASIS-class divergence rates (20% / 35.6% of union signals at exact-timestamp pairing; direction: CME under-fires, especially NAS100) are the measured feed-to-venue delta the parent ADR says should harden E2's envelope from guess to derivation.

## Inputs / provenance

- Trade exports (operator, 2026-07-03, coverage 2020-01 → 2026-06-30, all four parse + 15m-grid clean): `Striker_DJ30_v4.5_PEPPERSTONE_US30_2026-07-03_70416.csv`, `Striker_DJ30_v4.5_CBOT_MINI_MYM1!_2026-07-03_b5a41.csv`, `Striker_NAS100_v1_PEPPERSTONE_NAS100_2026-07-03_490d2.csv`, `Striker_NAS100_v1_CME_MINI_MNQ1!_2026-07-03_45ca6.csv` (local, gitignored-class vendor data — not committed).
- Bar panels (classification aid + seam detection ONLY — staging-only per the 2026-06-12 TV-CSV-canonical ADR): Pepperstone `core/data/bar_data/US30_M15.csv` (2020-01-02 → 2026-07-02) and `NAS100_M15.csv` (2020-01-01 → **2026-06-25** — 3 trading days short of trade coverage; no in-window divergences fell in the uncovered tail). CME side: **E-mini proxies** parsed from operator BAR_EXPORTs `BAR_EXPORT_v0.2_CBOT_MINI_YM1!_2026-07-01_273ea.csv` / `BAR_EXPORT_v0.2_CME_MINI_NQ1!_2026-07-01_833bd.csv` (153,054 / 153,122 bars, 2020-01-02 → 2026-07-02) via `scripts/parse_bar_export.py` — YM1!/NQ1! share the micros' session calendar and roll cycle; acceptable as bar-existence/seam aid, noted as proxy.
- `--point-value 1.0` both runs (first-trade sanity is a ±3× magnitude band targeting the ~153× corruption class; MYM/MNQ offsets of 0.5×/2× sit inside it by design). Both feeds passed first-trade sanity on both legs.

## Reproduction

```bash
python lab/analysis/p2_replay_2026-07/run_p2_replay.py --leg dj30 \
  --pep <US30 export> --cme <MYM1! export> \
  --window-start 2025-07-03 --window-end 2026-07-03 --point-value 1.0 \
  --pep-bars core/data/bar_data/US30_M15.csv --cme-bars <parsed YM1! panel> \
  --cme-symbol 'MYM1!' --score --gates-ratified --k2-kill 10 \
  --e1-pf-floor 0.8 --e1-net-floor 0.7 --k2-treatment with-roll   # and ex-roll
# nas100: swap exports, NAS100_M15.csv, <parsed NQ1! panel>, --cme-symbol 'MNQ1!'
```
