# Sovereign — CONCEPT-USDCAD-RDM-001 F1 mechanism falsifier

**Concept:** rate-differential momentum × USDCAD (working name **Sovereign**).
When the market reprices US rate expectations hawkishly vs the Bank of Canada,
the widening US–CA 2yr spread plus safe-haven demand appreciates USD vs CAD —
negatively correlated with the Constellation book in exactly the regime where
it chops.

**Brief:** [`docs/ltm/briefs/rnd-pipeline/CC-HANDOFF-USDCAD-RDM-001-stage1-f1.md`](../../docs/ltm/briefs/rnd-pipeline/CC-HANDOFF-USDCAD-RDM-001-stage1-f1.md)
**Concept record:** [`lab/validation/concept_intake/concepts/CONCEPT-USDCAD-RDM-001.yaml`](lab/archive/../validation/concept_intake/concepts/CONCEPT-USDCAD-RDM-001.yaml)
— intake gate **ADMIT 7/7, dedup CLEAR** (2026-06-11; the anticipated
NEAR_MATCH vs Sentinel USDCHF did not fire).

**Pattern precedent:** Helios `oil_carry` F1 (2026-06-06) and NOCT-SPX Stage 1+2
(2026-06-07) — admit through stage-1 intake, then a channel-isolating F1
falsifier as a standalone `lab/analysis/` probe. Mechanism-first; **no strategy
build** until F1 passes.

## Tests (§2.3) and pre-registered thresholds (§3)

Primary horizon 5d (non-overlapping windows); 1d/10d secondary, not gating.
`p < 0.05`, `n_perm = 2000` (house convention, `oanda_stage1.permutation`).
FAIL = any of:

1. **F1(b) mechanism loading** — Δ(US–CA 2yr) beta on USDCAD window returns:
   perm p ≥ 0.05 or sign negative.
2. **F1(a) anti-correlation** — corr(USDCAD daily returns, Constellation
   composite daily P&L) on spread-widening days ≥ 0.
3. **F1(c) channel isolation** — incremental spread loading insignificant after
   lagged-trend + WTI controls (reduction to disguised trend / petro channel).

PASS requires all three to clear; unevaluable criterion → AMBIGUOUS.

## Data (feed policy 2026-06-11: TV CSV canonical, no canonical bar-feed reliance)

Operator executive decision 2026-06-11 (ADR pending, separate PR): canonical
analyses run on TV CSV exports; programmatic bar feeds (Dukascopy/REST) are
staging-only and are not used here at all. The brief's original "Dukascopy
canonical" line for §2.2(a) is superseded by this operator override. Official
rate series (Treasury / BoC) are not bar feeds and are unaffected.

| input | source | file (gitignored `inputs/`) |
|---|---|---|
| USDCAD D1 2018→2026-06 | **TV chart export, operator-supplied** (Pepperstone feed preferred — matches the composite's feed family) | `USDCAD_D1_TV.csv` |
| WTI control D1, same span | **TV chart export, operator-supplied** (operator's WTI symbol, e.g. SpotCrude / TVC:USOIL) | `WTI_D1_TV.csv` |
| US 2yr | treasury.gov daily par-yield CSV (FRED blocked again) | `UST_2Y.csv` |
| CA 2yr | BoC Valet `BD.CDN.2YR.DQ.YLD` | `CA_2Y.csv` |
| USDCAD cross-check | BoC Valet `FXUSDCAD` (official daily rate) | `FXUSDCAD_BOC.csv` |
| Constellation composite | six 2020-01→2026-06 decompound TV exports, static-$200K via `decompound.py` stitch+rebank (operator-selected over 2022+ canonical panels) | `constellation_daily.csv` |

Leak-free as-of join: signal state for day *t* is the latest observation dated
≤ *t−1* (staleness > 5 calendar days dropped, counted). Counts reported, never
silent.

## Reproduce

```bash
python lab/analysis/usdcad_rdm/run_gate.py     # fetch missing inputs + gate
python lab/analysis/usdcad_rdm/gate.py         # gate only (inputs present)
```

Outputs: `gate_result.json` + console; verdict + §6 disposition in
[`verdict.md`](verdict.md).
