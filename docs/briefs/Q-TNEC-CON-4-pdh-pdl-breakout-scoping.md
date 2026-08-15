# Q-TNEC-CON-4 — PDH/PDL RTH with-break (structural stop; first/session)

**Status:** `AMBIGUOUS-HOLD` — explore scored; [`closure`](closures/Q-TNEC-CON-4-closure-ambiguous-hold.md) ITERATE; **Branch B elected** → CON-5 G0 frozen
**Stage-0 PREREG:** [`lab/analysis/c1/mnq_tnec_con4_pdh_pdl_break_2026-08/PREREG_G0.md`](../../lab/analysis/c1/mnq_tnec_con4_pdh_pdl_break_2026-08/PREREG_G0.md)
**Explore RESULTS:** [`RESULTS.md`](../../lab/analysis/c1/mnq_tnec_con4_pdh_pdl_break_2026-08/RESULTS.md)
**Authored:** 2026-08-10
**Authors:** Joshua + Cursor
**Parent:** [dense-1m entry-mechanism lane](../spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md) · TNEC-1 intake L4
**Prior:** [`Q-TNEC-CON-3` Branch B](closures/Q-TNEC-CON-3-closure-ambiguous-hold.md) · CON-2 AMBIGUOUS-HOLD · HTF-bias→LTF `FALSIFIED`
**Loop:** Inquire — Branch B → CON-5 opened; Cap unclaimed
**Spend:** $0 · K_intrinsic=1 · Cap not claimed

---

## §0 — Rule 0 reads (verified 2026-08-10)

| Path | Anchor | What it grounds |
|---|---|---|
| [`_mnq_1m.parquet`](../../lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/_mnq_1m.parquet) | present on disk 2026-08-10 | panel ($0 reuse) |
| [`CON-3` closure](closures/Q-TNEC-CON-3-closure-ambiguous-hold.md) | Branch B elected | lane continue → CON-4 |
| [`ADR 2026-08-10` temporal selectivity](../adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md) | Accepted | route ① open; hold-time mapped |
| Parent cheap falsifier | `CHEAP_FALSIFIER_OK` | licenses this freeze |
| [`admission_schema.py`](../../lab/discovery/admission_schema.py) | S6 ADMIT 2026-08-10 | catalogue_k=1 |

### Domain-bar consult (executed)

```text
python scripts/instrument_profiles.py cell MNQ pdh-pdl-breakout-rth
=== MNQ x pdh-pdl-breakout-rth ===
verdict: untested — no prior on this cell.
BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21 -> ../../docs/rejected_candidates.md
```

**Answer:** route **①** — first PDH/PDL break per RTH session is within-instrument temporal selectivity; hold-time not claimed. Through-break ≠ N9/C10 attraction.

**Door check:** ≠ CON-1/2/3 · ≠ compression · ≠ ORB · ≠ MNQPROX · ≠ HTF-bias→LTF · ≠ fade.

---

## §1 — Context

CON-3 (HTF-native compression) raised gross vs CON-2 but failed SHAPE. Branch B requires a **new entry causal object**. This Q freezes prior-day extreme through-break under the same temporal shell (first/session) and structural opposite-extreme stop.

Pre-Q gate:
  D: compression-break θ / hold-time rescue / fade — deleted (exhausted or mapped)
  S: one trade/session R stream on PDH/PDL break
  A: MNQSEL-2 panel indexed by session date

---

## §3 — Question

Does a pre-registered **PDH/PDL RTH with-break** entry (structural stop at opposite prior extreme; first signal per session; session-flat; Tradeify RT 1.41) clear TNEC N-EDGE + N-SHAPE under explore→confirm discipline, or does the frozen cell fail?

---

## §4 — Falsifiable hypothesis (H-CON-4)

**H-CON-4:** The Stage-0–frozen PDH/PDL construct produces at least one arm whose EXPLORATION mean net R has trade-weighted session-block 95% CI entirely above 0 (and DSR ≥ 0.650), advancing N-SHAPE toward confirm GO.

**Falsifier:** Both arms fail with CI entirely below 0 at powered n (or typed VOID as pre-registered) → `FALSIFIED`; STOP this construct catalogue; re-proposal = new entry mechanism (not θ-retune; not fade; not return to compression family).

---

## §5 — Forbidden moves

- Retuning PDH/PDL definition / first→N / stop geometry after freeze.
- Compression-break θ (CON-2/3); fade / level-touch attraction; ORB transplant; HTF-bias→LTF.
- Scoring before explore GO; reading CONFIRM before confirm GO.
- Cap claim / Pine / deploy / arming / `LEG_MAP` from this packet.

---

## §6 — Gate criteria

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | Explore clears pre-registered edge limbs; confirm GO later clears N-EDGE+N-SHAPE | `INTEGRATE` — candidate record → operator GO (admits/arms nothing) |
| `FALSIFIED` | Frozen entry fails pre-registered limbs | `STOP` — new mechanism only |
| `AMBIGUOUS-HOLD` | VOID / halves / magnitude as frozen | `ITERATE` — lane packet (not θ-retune) |

---

## §7 — Construct geometry (Stage-0 freeze)

| Element | Frozen value |
|---|---|
| Universe | RTH 09:30–15:59 ET · `MNQ.v.0` · **1m** bars |
| Stop / exit / cost | Opposite prior extreme · session-flat · RT 1.41 |
| Entry | close beyond PDH/PDL → with-break at next 1m open |
| Selectivity | First valid signal per session |
| K | `K_intrinsic=1` |
| S6 | ADMIT ([`ADMISSION.md`](../../lab/analysis/c1/mnq_tnec_con4_pdh_pdl_break_2026-08/ADMISSION.md)) |
| Cheap falsifier | `CHEAP_FALSIFIER_OK` (long −0.005 / short −0.003; CIs straddle; stop ≈279 pt) |

---

## §10 — Audit hooks

```bash
test -f docs/briefs/Q-TNEC-CON-4-pdh-pdl-breakout-scoping.md
test -f lab/analysis/c1/mnq_tnec_con4_pdh_pdl_break_2026-08/PREREG_G0.md
rg -n "CHEAP_FALSIFIER_OK" lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_pdh_pdl_break_2026-08-10_LOG.md
rg -n "route" docs/briefs/Q-TNEC-CON-4-pdh-pdl-breakout-scoping.md
pytest lab/analysis/c1/mnq_tnec_con4_pdh_pdl_break_2026-08/test_construct_lib.py -q
python scripts/instrument_profiles.py cell MNQ pdh-pdl-breakout-rth
```

## Verification

```bash
pytest lab/analysis/c1/mnq_tnec_con4_pdh_pdl_break_2026-08/test_construct_lib.py -q
python scripts/instrument_profiles.py cell MNQ pdh-pdl-breakout-rth
```
