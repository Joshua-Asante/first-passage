# Q-TNEC-CON-2 — compression→expansion break on dense RTH 1m opens (G=10)

**Status:** `CLOSED — AMBIGUOUS-HOLD (non-promotable)` 2026-08-10 — explore GO paid (operator in-session); EXPLORATION scored; CONFIRM reserved+unread. [closure](closures/Q-TNEC-CON-2-closure-ambiguous-hold.md)
**Stage-0 PREREG:** [`lab/analysis/c1/mnq_tnec_con2_compression_break_2026-08/PREREG_G0.md`](../../lab/analysis/c1/mnq_tnec_con2_compression_break_2026-08/PREREG_G0.md)
**Authored:** 2026-08-09
**Authors:** Joshua + Cursor
**Parent:** [dense-1m entry-mechanism lane](../spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md) · TNEC-1 intake L4
**Prior kill:** [`Q-MNQDTL-CON-1` FALSIFIED](closures/Q-MNQDTL-CON-1-closure-falsified.md) (ES/NQ divergence) · Family A displacement fade cheap-falsifier kill (no Q-ID)
**Loop:** Inquire — freeze named entry family before EXPLORATION path score
**Spend:** $0 · K_intrinsic=1 · Cap not claimed

---

## §0 — Rule 0 reads (verified 2026-08-09)

| Path | Anchor | What it grounds |
|---|---|---|
| [`_mnq_1m.parquet`](../../lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/_mnq_1m.parquet) | present on disk 2026-08-09 | dense-1m panel |
| [`Q-MNQSEL-2` RESULTS](../../lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/RESULTS.md) | RESOLVED C4 | S3 ≈ 0.858; licenses construct universe |
| [`CON-1` closure](closures/Q-MNQDTL-CON-1-closure-falsified.md) | FALSIFIED 2026-08-09 | STOP scope = new entry mechanism; no sign invert |
| [`MNQDTL-1` §3.1](../spec/2026-08-06-mnq-daily-cadence-tight-daily-loss-target-spec.md) | C1–C11 | closed doors |
| [`MNQSR-1` RESULTS](../../lab/archive/mnq_sr_structure_2026-08-06/RESULTS.md) | 0/14 | C10 level families — not this entry class |
| [`TNEC-1` body](../spec/2026-08-08-tradeify-necessary-conditions-target-spec.md) | `N-EDGE` @ L10 | intake limbs |
| [`lane spec`](../spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md) | `b262a81` | step 1–6 + stop-rule |
| [`admission_schema.py`](../../lab/discovery/admission_schema.py) | S6 ADMIT dry-run 2026-08-09 | catalogue_k=1 |
| Family B cheap falsifier log | 2026-08-09 | `CHEAP_FALSIFIER_OK` (CI straddles) |

**Door check (family, not parameterization):** compression→expansion with-break entry is distinct from CON-1 ES/NQ divergence, from Family A displacement fade, and from C1–C11 as frozen in PREREG_G0 §2 (C10 adjacency disclosed: MNQSR-1 tested level attraction/reaction, not this entry).

---

## §1 — Context

MNQSEL-2 proved oracle headroom on dense 1m @ G=10. CON-1 (relative ES−NQ divergence) died on explore. Family A (displacement fade) died at the parent cheap falsifier. This Q freezes Family B — narrow-bar compression then close-break, enter with the break — under the same trade geometry.

---

## §3 — Question

Does a pre-registered **compression→expansion with-break** entry on dense RTH 1m opens (G=10, session-flat) clear TNEC N-EDGE + N-SHAPE under explore→confirm discipline, or does the frozen cell fail?

---

## §4 — Falsifiable hypothesis (H-CON-2)

**H-CON-2:** The Stage-0–frozen compression-break construct produces at least one arm whose EXPLORATION mean net R has trade-weighted session-block 95% CI entirely above 0 (and DSR ≥ 0.650), advancing N-SHAPE toward confirm GO.

**Falsifier:** Both arms fail with CI entirely below 0 at powered n (or typed VOID as pre-registered) → `FALSIFIED`; STOP this construct catalogue; re-proposal = new entry mechanism (not K_NARROW / NARROW_MULT / G retune; not sign-invert to fade).

---

## §5 — Forbidden moves

- Retuning K_NARROW / NARROW_MULT / median window / G after freeze.
- Sign-invert to fade-the-break (Family A killed).
- Scoring before explore GO; reading CONFIRM before confirm GO.
- Oracle selection; ORB filter laundering (F2); C10 level-family reopen.
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
| Universe | RTH 09:30–15:59 ET 1m opens `MNQ.v.0` (MNQSEL-2 panel) |
| Stop / exit / cost | G=10 · session-flat · RT 1.41 |
| Entry | 2 narrow bars (≤1.0× med20 range) → close beyond quiet range → **with-break** at next open |
| K | `K_intrinsic=1` |
| S6 | ADMIT ([`ADMISSION.md`](../../lab/analysis/c1/mnq_tnec_con2_compression_break_2026-08/ADMISSION.md)) |
| Cheap falsifier | `CHEAP_FALSIFIER_OK` — means negative, CI straddles (not conclusive kill) |

---

## §10 — Audit hooks

```bash
test -f docs/briefs/Q-TNEC-CON-2-compression-expansion-break-scoping.md
test -f lab/analysis/c1/mnq_tnec_con2_compression_break_2026-08/PREREG_G0.md
rg -n "CHEAP_FALSIFIER_OK" lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_compression_break_2026-08-09_LOG.md
rg -n "N-EDGE" docs/spec/2026-08-08-tradeify-necessary-conditions-target-spec.md
PYTHONPATH=lab python -c "from discovery.admission_schema import load_admission, evaluate_admission; print(evaluate_admission(load_admission('lab/analysis/c1/mnq_tnec_con2_compression_break_2026-08/ADMISSION.json'), registered_k=1).decision)"
pytest lab/analysis/c1/mnq_tnec_con2_compression_break_2026-08/test_construct_lib.py -q
```
