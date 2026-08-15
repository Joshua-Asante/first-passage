# PHAROS — US500 sweep→FVG→draw apparatus (Q-ICT-SWEEPFVG-1)

ICT-style liquidity **sweep → same-direction FVG → opposing-pool draw** test on
Pepperstone US500 15m. **Verdict: FALSIFIED (2026-06-17)** — directional signal is
real (block-permutation p=0.014) but no robust tradeable edge (drop-top-3 −0.152R,
~3-trade-concentrated). See:

- Pre-registration (lock = its introducing commit): [`docs/ltm/briefs/pre-registration/Q-ICT-SWEEPFVG-1-verdict-preregistration.md`](lab/archive/../../docs/ltm/briefs/pre-registration/Q-ICT-SWEEPFVG-1-verdict-preregistration.md)
- Brief: [`docs/ltm/briefs/Q-ICT-SWEEPFVG-1-sweep-fvg-draw.md`](lab/archive/../../docs/ltm/briefs/Q-ICT-SWEEPFVG-1-sweep-fvg-draw.md)
- Closure: [`docs/ltm/briefs/Q-ICT-SWEEPFVG-1-closure-falsified.md`](lab/archive/../../docs/ltm/briefs/Q-ICT-SWEEPFVG-1-closure-falsified.md)
- Ledger: [`ops/instruments/US500.md`](lab/archive/../../ops/instruments/US500.md)

## Files (committed = code only; data stays local per public-clone posture)

| File | Role |
|---|---|
| `pharos_event_parser.py` | Step-0 integrity battery + pivot-lag undo + sweep→FVG→draw assembly → `setups.csv` |
| `pharos_outcome_sim.py` | FROZEN outcome simulator (firewalled; `--selftest` proves resolution logic). **Test object — do not edit.** |
| `pharos_phase2_run.py` | Phase-2 verdict runner: imports `resolve_setup` verbatim, adds the two pre-registered corrections (tradeability floor `max(1pt,cost)` + `fvg_bar` block resampling) |

**Not committed (local / pinned):**
- `setups.csv` — frozen population, **md5 `b1e3ba85a2f77d2f83cef92d0e328a2e` (LF artifact)**. The sim's `assert_population_identity` hashes this; re-minting on Windows yields CRLF (md5 `82ad5808…`) and would falsely HALT — keep the LF file. Regenerable: `python pharos_event_parser.py "<bars>.csv" --out-dir .`
- `PEPPERSTONE_US500, 15_1ca49.csv` — vendor TV export (Pepperstone TOS), **sha256 `e337812ad21f94132c3b9ac048822f1ee795b75e7ffc87eb73e6e8c0af4ed6dd`**. 2,104 bars, 2026-05-14→06-16 ET, 15m. Provenance confirmed Pepperstone US500 15m (Joshua, 2026-06-17).
- `pharos_fvg_pool_sweep_v0_1.pine` — detector, **sha256 `a7ce552f3f7381d121d105be5c177530a5128f335608a2fd4a67eaea543839a2`** (gitignored per `**/*.pine`).

## Reproduce (needs the local data above)

```bash
python pharos_outcome_sim.py --selftest          # test object intact: ALL PASS
python -c "import hashlib;print(hashlib.md5(open('setups.csv','rb').read()).hexdigest())"   # b1e3ba85...
PYTHONUTF8=1 python pharos_phase2_run.py          # VERDICT: FALSIFIED; drop-top-3 -0.152R; perm p=0.0144
```

## Cost lock (conservative)

rt_spread 0.8 + slippage 0.2 = 1.0pt round-trip → hurdle 0.2883R (4×median cost_R)
on the tradeable population (63 setups / 48 FVG-blocks / 23 days). Execution venue
DXTrade `US500.x`; gross-of-swap (long −140.27 pip/day headwind documented, unmodeled).
