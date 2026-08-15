# Q-REGIME-AEGIS-1 — USDJPY-trend vs Aegis outcomes (2026-06-16)

**Verdict: FALSIFIED.** USDJPY trend-persistence does not separate Aegis's win/loss regime at the
per-trade level; the gold gate's already-logged `aegis_flag` is a non-signal. Pre-registration `81d529f`
(before analysis). Brief: [`../../../docs/ltm/briefs/Q-REGIME-AEGIS-1.md`](lab/archive/../../docs/ltm/briefs/Q-REGIME-AEGIS-1.md);
closure: [`Q-REGIME-AEGIS-1-closure-falsified.md`](lab/archive/../../docs/ltm/briefs/Q-REGIME-AEGIS-1-closure-falsified.md).

## Headline

- 149 Aegis trades (WR 58.4%). **AUC(USDJPY KER_126 vs loss) = 0.499** — chance. ex-2022 0.485, LOYO-min 0.485.
- **Frozen `aegis_flag` ON/OFF:** loss-rate 42.5% vs 41.3% (+1.2pp); mean PnL $1,732 (ON) vs $1,154 (OFF) — the flag is uninformative, if anything mildly favorable (long-biased mean-reverter + USDJPY up-trend).
- The detector-screen USDJPY "inversion" was an **aggregate period coincidence** (2020-22), not a per-trade signal.

## Disposition

- Demote/remove `aegis_flag` from `ops/regime_gate/gold_gate_shadow.py` (logs a validated non-signal) — follow-up, flagged not done.
- 2nd consecutive FALSIFIED detector on the blind-spot thread (after Q-REGIME-RATEVOL-1). INQHIORI §6: do **not** author a 3rd same-level detector. The non-gold legs' regime degradation isn't per-unit detectable; the detectable regime is gold-carried.

## Reproduce

```
PYTHONPATH=core python lab/analysis/regime_aegis_2026-06-16/aegis_screen.py
```

Needs the gitignored Aegis Pepperstone export (`lab/analysis/decompound_remc_2026-06-07/inputs/Aegis_USDJPY*.csv`)
+ `core/data/bar_data/USDJPY.csv` (OANDA, gitignored). No `core/` / locked-config change — research only.
