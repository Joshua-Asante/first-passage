# Q-TNEC-CON-5 — impulse→pullback→VWAP-reclaim (structural pullback stop; first/session)

**Status:** `AMBIGUOUS-HOLD` → **STOP** — [`closure`](closures/Q-TNEC-CON-5-closure-ambiguous-hold.md); **Branch A elected** 2026-08-12 (OHLCV temporal-selectivity lane default paused)
**Stage-0 PREREG:** [`lab/analysis/c1/mnq_tnec_con5_impulse_pullback_vwap_2026-08/PREREG_G0.md`](../../lab/analysis/c1/mnq_tnec_con5_impulse_pullback_vwap_2026-08/PREREG_G0.md)
**Explore RESULTS:** [`RESULTS.md`](../../lab/analysis/c1/mnq_tnec_con5_impulse_pullback_vwap_2026-08/RESULTS.md)
**Authored:** 2026-08-11
**Authors:** Joshua + Cursor
**Parent:** [dense-1m entry-mechanism lane](../spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md) · TNEC-1 intake L4
**Prior:** [`Q-TNEC-CON-4` Branch B](closures/Q-TNEC-CON-4-closure-ambiguous-hold.md) · CON-3 AMBIGUOUS · CON-2 AMBIGUOUS · HTF-bias→LTF `FALSIFIED`
**Loop:** Closed — Branch A STOP; CONFIRM unread forever; Cap unclaimed; lane FALSIFIED counter 1/3 unchanged
**Spend:** $0 · K_intrinsic=1 · Cap not claimed

---

## §0 — Rule 0 reads (verified 2026-08-11)

| Path | Anchor | What it grounds |
|---|---|---|
| [`_mnq_1m.parquet`](../../lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/_mnq_1m.parquet) | present on disk 2026-08-11 | panel ($0 reuse; `volume` present) |
| [`CON-4` closure](closures/Q-TNEC-CON-4-closure-ambiguous-hold.md) | Branch B elected | lane continue → CON-5 non-breakout |
| [`ADR 2026-08-10` temporal selectivity](../adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md) | Accepted | route ① open; hold-time mapped |
| Parent cheap falsifier | `CHEAP_FALSIFIER_OK` | licenses this freeze |
| [`admission_schema.py`](../../lab/discovery/admission_schema.py) | S6 ADMIT 2026-08-11 | catalogue_k=1 |

### Domain-bar consult (executed)

```text
python scripts/instrument_profiles.py cell MNQ impulse-pullback-vwap-reclaim
=== MNQ x impulse-pullback-vwap-reclaim ===
verdict: untested — no prior on this cell.
BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21 -> ../../docs/rejected_candidates.md
```

**Answer:** route **①** — first bias-side VWAP reclaim per RTH session is within-instrument temporal selectivity; hold-time not claimed. Pullback-depth stop is the cost-geometry distinction vs CON-4 day-range stops (not a mapped hold-time lever).

**Door check:** ≠ CON-1–4 · ≠ compression · ≠ fade-to-VWAP · ≠ ORB · ≠ PDH/PDL · ≠ HTF-bias→LTF.

---

## §1 — Context

CON-4 (PDH/PDL through-break) was economically flat at ~257 pt stops. Branch B requires a **new non-breakout** entry causal object with a stated cost-geometry distinction. This Q freezes impulse→pullback→VWAP-reclaim under the same temporal shell (first/session) with a **pullback-extreme** stop.

Pre-Q gate:
  D: through-break θ / hold-time rescue / fade-to-VWAP — deleted (exhausted, mapped, or forbidden)
  S: one trade/session R stream on bias-side VWAP reclaim
  A: MNQSEL-2 panel indexed by session date

---

## §3 — Question

Does a pre-registered **impulse→pullback→VWAP-reclaim** entry (structural pullback-extreme stop; first signal per session; session-flat; Tradeify RT 1.41) clear TNEC N-EDGE + N-SHAPE under explore→confirm discipline, or does the frozen cell fail?

---

## §4 — Falsifiable hypothesis (H-CON-5)

**H-CON-5:** The Stage-0–frozen pullback-reclaim construct produces at least one arm whose EXPLORATION mean net R has trade-weighted session-block 95% CI entirely above 0 (and DSR ≥ 0.650), advancing N-SHAPE toward confirm GO.

**Falsifier:** Both arms fail with CI entirely below 0 at powered n (or typed VOID as pre-registered) → `FALSIFIED`; STOP this construct catalogue; re-proposal = new entry mechanism (not θ-retune; not fade; not return to through-break / compression family).

---

## §5 — Forbidden moves

- Retuning bias window / VWAP / first→N / stop geometry after freeze.
- Through-break θ (CON-1–4); fade-to-VWAP; compression transplant; ORB transplant; HTF-bias→LTF.
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
| Stop / exit / cost | Pullback extreme · session-flat · RT 1.41 |
| Entry | bias → VWAP tag → with-bias reclaim at next 1m open |
| Selectivity | First valid signal per session |
| K | `K_intrinsic=1` |
| S6 | ADMIT ([`ADMISSION.md`](../../lab/analysis/c1/mnq_tnec_con5_impulse_pullback_vwap_2026-08/ADMISSION.md)) |
| Cheap falsifier | `CHEAP_FALSIFIER_OK` (long +0.006 / short −0.427; coverage 90%; stop ≈19 pt) |

---

## §10 — Audit hooks

```bash
test -f docs/briefs/Q-TNEC-CON-5-impulse-pullback-vwap-reclaim-scoping.md
test -f lab/analysis/c1/mnq_tnec_con5_impulse_pullback_vwap_2026-08/PREREG_G0.md
rg -n "CHEAP_FALSIFIER_OK" lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_impulse_pullback_vwap_2026-08-11_LOG.md
rg -n "route" docs/briefs/Q-TNEC-CON-5-impulse-pullback-vwap-reclaim-scoping.md
pytest lab/analysis/c1/mnq_tnec_con5_impulse_pullback_vwap_2026-08/test_construct_lib.py -q
python scripts/instrument_profiles.py cell MNQ impulse-pullback-vwap-reclaim
```

## Verification

```bash
pytest lab/analysis/c1/mnq_tnec_con5_impulse_pullback_vwap_2026-08/test_construct_lib.py -q
python scripts/instrument_profiles.py cell MNQ impulse-pullback-vwap-reclaim
```
