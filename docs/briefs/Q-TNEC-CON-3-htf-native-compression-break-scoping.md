# Q-TNEC-CON-3 — HTF-native 5m compression→expansion break (structural stop; first/session)

**Status:** `AMBIGUOUS-HOLD` — explore scored; [`closure`](closures/Q-TNEC-CON-3-closure-ambiguous-hold.md) ITERATE; **Branch B elected** (lane CON-4); CON-4 mechanism design unpaid
**Stage-0 PREREG:** [`lab/analysis/c1/mnq_tnec_con3_htf_native_break_2026-08/PREREG_G0.md`](../../lab/analysis/c1/mnq_tnec_con3_htf_native_break_2026-08/PREREG_G0.md)
**Explore RESULTS:** [`RESULTS.md`](../../lab/analysis/c1/mnq_tnec_con3_htf_native_break_2026-08/RESULTS.md)
**Authored:** 2026-08-10
**Authors:** Joshua + Cursor
**Parent:** [dense-1m entry-mechanism lane](../spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md) · TNEC-1 intake L4
**Prior:** [`Q-TNEC-CON-2` AMBIGUOUS-HOLD](closures/Q-TNEC-CON-2-closure-ambiguous-hold.md) · HTF-bias→LTF filter cheap-falsifier `FALSIFIED` (no Q-ID) · cell-#3 slate exhausted (stop-width / T-IMB / SWING-1)
**Loop:** Inquire — Branch B elected; CON-4 unnamed until mechanism design + cheap falsifier; Cap unclaimed
**Spend:** $0 · K_intrinsic=1 · Cap not claimed

---

## §0 — Rule 0 reads (verified 2026-08-10)

| Path | Anchor | What it grounds |
|---|---|---|
| [`_mnq_1m.parquet`](../../lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/_mnq_1m.parquet) | present on disk 2026-08-10 | panel ($0 reuse) |
| [`Q-MNQSEL-2` RESULTS](../../lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/RESULTS.md) | RESOLVED C4 | oracle headroom |
| [`CON-2` closure](closures/Q-TNEC-CON-2-closure-ambiguous-hold.md) | AMBIGUOUS-HOLD 2026-08-10 | cost wall; successor = cost geometry / new mechanism |
| HTF-bias→LTF falsifier LOG | `FALSIFIED` 2026-08-10 | do not use HTF as 1m bias filter |
| [`ADR 2026-08-10` temporal selectivity](../adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md) | Accepted | route ① open for first/session |
| [`lane spec`](../spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md) | step 1a repaired | domain-bar consult mandatory |
| [`admission_schema.py`](../../lab/discovery/admission_schema.py) | S6 ADMIT 2026-08-10 | catalogue_k=1 |
| Parent cheap falsifier | `CHEAP_FALSIFIER_OK` | licenses this freeze |

### Domain-bar consult (executed; exit 1 expected)

```text
python scripts/instrument_profiles.py cell MNQ htf-compression-breakout-5m
=== MNQ x htf-compression-breakout-5m ===
verdict: untested — no prior on this cell.
BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21 -> ../../docs/rejected_candidates.md
```

**Answer:** route **①** — within-instrument temporal selectivity (first valid 5m compression-break per RTH session) is outside the mapped cross-instrument levers per ADR §2-A/B; criterion named a priori and frozen here; `K_intrinsic=1`. Price/hold-time levers not claimed as the rescue. Not a CON-2 θ-retune.

**Door check (family):** HTF-native 5m compression break with structural stop ≠ CON-1 ES/NQ divergence ≠ CON-2 1m/G=10 ≠ HTF-bias→LTF filter ≠ Family A fade ≠ T-IMB / SWING-1 ≠ C1–C11 (C10 adjacency: not level-touch attraction).

---

## §1 — Context

CON-2 proved ~1 pt gross that Tradeify RT 1.41 eats. Filtering 1m with-breaks by HTF bias made net worse. Cell-#3 showed stop-width cannot rescue the 1m family; surviving lever is trade count under temporal selectivity (ADR-opened). This Q freezes the Master-Pattern-shaped **HTF-native** cell: trade the 5m break itself, structural stop, first/session.

---

## §3 — Question

Does a pre-registered **HTF-native 5m compression→expansion with-break** entry (structural stop at opposite quiet extreme; first signal per RTH session; session-flat; Tradeify RT 1.41) clear TNEC N-EDGE + N-SHAPE under explore→confirm discipline, or does the frozen cell fail?

---

## §4 — Falsifiable hypothesis (H-CON-3)

**H-CON-3:** The Stage-0–frozen HTF-native construct produces at least one arm whose EXPLORATION mean net R has trade-weighted session-block 95% CI entirely above 0 (and DSR ≥ 0.650), advancing N-SHAPE toward confirm GO.

**Falsifier:** Both arms fail with CI entirely below 0 at powered n (or typed VOID as pre-registered) → `FALSIFIED`; STOP this construct catalogue; re-proposal = new entry mechanism (not θ-retune; not fade; not return to 1m/G=10).

---

## §5 — Forbidden moves

- Retuning K_NARROW / NARROW_MULT / median window / HTF minutes / first→N per session after freeze.
- Reintroducing 1m entry or HTF-as-bias-only layer; fixed G=10 CON-2 retune; sign-invert to fade.
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
| Universe | RTH 09:30–15:59 ET · `MNQ.v.0` · **5m** bars from MNQSEL-2 1m panel |
| Stop / exit / cost | Opposite quiet extreme · session-flat · RT 1.41 · `R=(pts−1.41)/stop_dist` |
| Entry | 2 narrow 5m bars → close beyond quiet+midline → with-break at next 5m open |
| Selectivity | First valid signal per session |
| K | `K_intrinsic=1` |
| S6 | ADMIT ([`ADMISSION.md`](../../lab/analysis/c1/mnq_tnec_con3_htf_native_break_2026-08/ADMISSION.md)) |
| Cheap falsifier | `CHEAP_FALSIFIER_OK` |

---

## §10 — Audit hooks

```bash
test -f docs/briefs/Q-TNEC-CON-3-htf-native-compression-break-scoping.md
test -f lab/analysis/c1/mnq_tnec_con3_htf_native_break_2026-08/PREREG_G0.md
rg -n "CHEAP_FALSIFIER_OK" lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_htf_native_break_2026-08-10_LOG.md
rg -n "route" docs/briefs/Q-TNEC-CON-3-htf-native-compression-break-scoping.md
PYTHONPATH=lab python -c "from discovery.admission_schema import load_admission, evaluate_admission; print(evaluate_admission(load_admission('lab/analysis/c1/mnq_tnec_con3_htf_native_break_2026-08/ADMISSION.json'), registered_k=1).decision)"
pytest lab/analysis/c1/mnq_tnec_con3_htf_native_break_2026-08/test_construct_lib.py -q
python scripts/instrument_profiles.py cell MNQ htf-compression-breakout-5m
```

## Verification

```bash
# Discipline checks
pytest lab/analysis/c1/mnq_tnec_con3_htf_native_break_2026-08/test_construct_lib.py -q
PYTHONPATH=lab python -c "from discovery.admission_schema import load_admission, evaluate_admission; r=evaluate_admission(load_admission('lab/analysis/c1/mnq_tnec_con3_htf_native_break_2026-08/ADMISSION.json'), registered_k=1); assert r.decision=='ADMIT'"
# Domain bar still answered
python scripts/instrument_profiles.py cell MNQ htf-compression-breakout-5m
```
