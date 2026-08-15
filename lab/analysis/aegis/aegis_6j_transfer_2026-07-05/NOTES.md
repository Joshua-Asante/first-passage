# Aegis→6J transfer lane — 2026-07-05

**Parent:** claude.ai session (Aegis JPY-futures prototype v0.1→v0.3) →
`CC-HANDOFF-AEGIS-6J-2026-07-05` (spawn-executed in this repo; Phase-0 report in
the session log). Program context: futures-prop pivot, subordinate to
[`docs/ltm/briefs/futures_residual_program_2026-07-05.md`](../../../docs/ltm/briefs/futures_residual_program_2026-07-05.md)
(this lane is the Aegis/6J transfer test; residual R-tracks unaffected).

**Transfer architecture:** Aegis USDJPY v4.3 (LOCKED 2026-04-22) → CME 6J via
**synthetic-spot inversion** (s = 1/f, high/low swapped; all v4.3 long-only
logic runs in synthetic space; orders mirror SHORT futures; levels map through
the reciprocal). Direction-toggle transfer rejected (nonlinear reciprocal breaks
BB/ATR meaning; the 0.07¥ vol floor never passes on a ~0.0062 series).
**v4.3 itself is untouched** — the prototype is NON-CANONICAL, do not lock/deploy.

## Artifacts of record (gitignored bytes, hash-pinned here)

| Artifact | Path | SHA256 |
|---|---|---|
| v0.3 prototype Pine | `core/strategies/aegis/aegis_jpy_futures_v0_3_prototype.pine` (also pinned in `core/strategies/PORT_MANIFEST.sha256`) | `30d350283723d0b297c97533793846495152c2c7a93943088f36b2a2f4f895ad` |
| v0.3 deep replay CSV (OF RECORD) | `inputs/Aegis_JPY-Futures_v0.3_PROTOTYPE_(MJY_6J)_CME_6J1!_2026-07-05_8e269.csv` | `c3b341629efbb14d597c3483238298fda64376dc93e644288a23cbb4801946a6` |
| Q-AEGIS-6J-BEPAD-1 test-harness Pine | `core/strategies/aegis/aegis_jpy_futures_v0_3_bepad_prototype.pine` (also pinned in `core/strategies/PORT_MANIFEST.sha256`) | `a318d432c38dce445a108ad329889c0ccaec001182ed9384ab621badff0f62ab` |
| BEPAD replay k=0 (= panel of record, byte-identical) | `inputs/Aegis_JPY-Futures_v0.3_BEPAD_k0_(MJY_6J)_CME_6J1!_2026-07-05.csv` | `c3b341629efbb14d597c3483238298fda64376dc93e644288a23cbb4801946a6` |
| BEPAD replay k=2 | `inputs/Aegis_JPY-Futures_v0.3_BEPAD_k2_(MJY_6J)_CME_6J1!_2026-07-05.csv` | `b7df895e72e0f878947f603e13a2e75465124a34d05285a080bade2f0fe6026d` |
| BEPAD replay k=3 | `inputs/Aegis_JPY-Futures_v0.3_BEPAD_k3_(MJY_6J)_CME_6J1!_2026-07-05.csv` | `49cbc1d388633d33cf0a39669983bcf60e3958279643951f22a1c5011a74f055` |

CSV provenance: TV Deep Backtesting, CME:6J1! 15m back-adjusted, 2022-01-12 →
2026-07-01, $100K initial, $1.30/side/contract placeholder commission, 1-tick
slippage, contract cap 12. Vendor-licensed TV export → gitignored per repo
policy (`lab/analysis/**/inputs/*.csv`); bytes live in the main checkout and
this worktree; the pins above are the integrity anchor (M-9 pattern).

Transience note: v0.1/v0.2 prototype Pines + CSVs (the §3 evolution panels)
exist only in `C:/Users/joshu/Downloads/` — NOT landed (handoff scope = v0.3
only). If the evolution evidence is ever needed repo-side, land it then.

**⚠ Prototype header staleness (2026-07-05 review finding):** the pinned Pine's
header block "Deep-panel replay of record" carries **v0.2** figures (n=130 /
$41,191 / PF 2.364 / +0.226R; also "default 16:55 ET" / "~14 bars" in the RAIL
MAPPING section vs the actual 16:30 input default). The file was frozen before
the final v0.3 replay; its hash is the provenance of the CSV it generated, so
it is deliberately NOT edited/re-pinned. Panel of record = the table above +
`ops/instruments/6J.md` J1/J2. Fix the header text in the v0.4 authoring pass.

**BEPAD export landing convention (makes the pre-reg §10 glob runnable):** when
Joshua's three Q-AEGIS-6J-BEPAD-1 replays are landed here, name them
`..._BEPAD_k0_...csv` / `..._BEPAD_k2_...csv` / `..._BEPAD_k3_...csv` (TV's
default export name won't contain "BEPAD" — rename at landing, pin sha256 here).

**How to run the three BEPAD replays (Joshua, TradingView):**

1. Open `core/strategies/aegis/aegis_jpy_futures_v0_3_bepad_prototype.pine`
   (compile-verified via `scripts/pine_check.py`, byte-identical to the pinned
   v0.3 prototype except the title, one new input, and its single consumption
   site — diffable, see the pre-reg §Frozen-config). Paste into a new Pine
   Editor tab on the CME:6J1! 15m back-adjusted chart, same Deep window as the
   panel of record (2022-01-01 start / open end; `backtestMode` ON).
2. Find the new input **"BE Pad Floor, ticks (Q-AEGIS-6J-BEPAD-1 arm k)"**
   under the STOP/TP/BE group. Run Deep Backtesting three times, changing
   **only** this one input, everything else at defaults:
   - k=0 (control) → export CSV, rename `Aegis_JPY-Futures_v0.3_BEPAD_k0_(MJY_6J)_CME_6J1!_<date>_<id>.csv`
   - k=2 → `..._BEPAD_k2_...csv`
   - k=3 → `..._BEPAD_k3_...csv`
3. Drop the three CSVs in `inputs/` (or Downloads — I'll land + pin them).
4. **Sanity check before you send them:** the k=0 run should reproduce the v0.3
   panel of record exactly (N=129, Net $39,056.10, PF 2.318, maxDD 3.12%) — if
   it doesn't, something about the paste/chart/window differs from v0.3 and we
   should find that before trusting k=2/k=3.

I'll ingest all three (identity check + the k=0 integrity gate first, per the
pre-reg §6/§7), then read the §6 table and report the verdict.

## 2.1 ingest gate — PASS (2026-07-05)

Independent reproduction via the extended reconcile tooling
(`.claude/skills/trade-csv-reconcile/scripts/reconcile.py`, futures identity
check added this session):

```
python .claude/skills/trade-csv-reconcile/scripts/reconcile.py \
  'lab/analysis/aegis_6j_transfer_2026-07-05/inputs/Aegis_JPY-Futures_v0.3_PROTOTYPE_(MJY_6J)_CME_6J1!_2026-07-05_8e269.csv' \
  --strategy aegis --account 100000 --pointvalue 12500000 --tick 0.0000005 --commission 1.30
```

| Metric | Computed | Gate | Verdict |
|---|---|---|---|
| N | 129 | 129 exact | ✓ |
| Net | $39,056.10 | $39,056 ± $5 | ✓ |
| PF | 2.318 | 2.318 ± 0.005 | ✓ |
| WR | 35.66% | 35.7 ± 0.1pp | ✓ |
| maxDD | 3.12% ($3,135.45) | 3.12 ± 0.05% (bar-close, $100K) | ✓ |
| 1R (full-stop mean, n=10) | $1,385.74 | handoff R = $1,386 | ✓ |
| Futures P&L identity | 129/129, max dev $0.00, 0 off-grid fills | all pass | ✓ |

Expectancy check: $39,056.10 / 129 / $1,385.74 = **+0.218R** — matches the
handoff §3 decomposition.

## Lane contents

- `inputs/` — gitignored CSV(s), pinned above.
- `trail_survival_mc.py` — Bulenox Option-2 trail-survival MC (2.5); see
  `RESULTS_trail_mc.md`.
- `RUNSPEC_EOD_OFF.md` — one-page EOD-OFF counterfactual run spec (2.4);
  operator-run, one export owed back to `inputs/`.
- Pre-registration (2.3): [`docs/ltm/briefs/Q-AEGIS-6J-BEPAD-1.md`](../../../docs/ltm/briefs/Q-AEGIS-6J-BEPAD-1.md)
  — committed BEFORE any BEPAD replay export exists (timestamp order is the audit).
- Instrument ledgers (2.7): [`ops/instruments/6J.md`](../../../ops/instruments/6J.md),
  [`ops/instruments/MJY.md`](../../../ops/instruments/MJY.md).
