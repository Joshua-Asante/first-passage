# `MNQPROX-2` Phase-0 — power census → `VOID-POWER-anticipated`

**Spec:** [`docs/spec/2026-08-06-mnqprox-2-tod-matched-level-proximity-spec.md`](../../../../docs/spec/2026-08-06-mnqprox-2-tod-matched-level-proximity-spec.md) §7 step 1  
**Operator GO:** 2026-08-06 (*"yes, run Phase 0"*) — Phase-0 only; PREREG/run **not** authorized.  
**Cost:** **$0.00.** Free 1m panel only; no TBBO.  
**Machine record:** [`PHASE0.json`](PHASE0.json)  
**Parent ORB arm:** rebuilt `mnq_orb_flow_substrate_2026-08-05/events.parquet` via unmodified `build_events.py` (gitignored cache; trigger count **255** matches N14 / `events_summary.json`).

---

## Verdict

**`VOID-POWER-anticipated`.** Projected **`n_paired = 15` < 30**.  
Per the frozen Phase-0 gate: **do not open PREREG.** Stop.

---

## Counts

| Quantity | Value |
|---|---:|
| Parent ORB triggers (S2) | 255 |
| Approaches detected (all PDH/PDL re-entries, raw) | 162 |
| After S4a(i)–(iii) (no TBBO / no S4a(iv)) | 154 |
| **Paired under S4′ (`τ = 30`) ∩ S4a(ii)** | **15** |
| Fraction paired | 5.88% |
| Unpaired (incl. no-prev / ToD miss) | 240 |

Eligible ToD band under the frozen joint constraints is **`[15, 30]` minutes** — S4a(ii) drops `|Δtod| < 15`; τ keeps `|Δtod| ≤ 30`. Paired `|Δtod|` median **20**, range **[15, 30]** (exactly that annulus).

---

## S4c projection (disclosure only — Δ not computed)

On the 15 paired triggers, ToD matching **does** collapse the parent W6 split:

| Arm | Median | IQR |
|---|---:|---|
| ORB | 612 | [601, 634.5] |
| Level | 601 | [586.5, 638] |

`|median gap| = 11` min (< 60); IQRs overlap → **W6 would not fire** on this paired set.  
That is **not** a clearance: power fails first, and FM-9 forbids reading τ-overlap as a reason to skip the floor.

---

## What this does / does not

**Does**
- Discharge Phase-0 for the frozen S4′ construct (`τ = 30`, PDH/PDL approaches, S4a(i)–(iii) retained).
- Show the binding wall is **pair rate**, not residual ToD confound: when pairs exist, clocks align; almost no triggers find a legal approach inside the `[15, 30]` band.
- Block PREREG / harness / tbbo reuse under this freeze.

**Does not**
- License editing `τ`, dropping S4a(ii), swapping level class, or patching `MNQPROX-1` (FM-4 / FM-6 / FM-7).
- Reopen N14 as ORB-specific (FM-8) — caveat undischarged.
- Authorize a successor cell; any redesign needs a **fresh** spec + Phase-0 + GO.

---

## Iterate

**Next: STOP** on `Q-MNQPROX-2` as specified.  
N14 limitation 1 (level-proximity uncontrolled) remains open; the ToD-matched PDH/PDL discriminator named by `MNQPROX-1` Iterate is **power-dead under the joint S4a(ii)+τ freeze**. A future proposal needs a different construct (or an explicit, pre-registered change to the exclusion/τ joint — not a silent post-hoc edit), not a re-run of this census.
