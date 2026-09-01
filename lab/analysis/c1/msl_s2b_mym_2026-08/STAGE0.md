# MSL-S2B Stage-0 — MYM panel/CONFIRM pins + mechanism draft

**Status:** `STAGE-0 PASS` · **PROCEED 2026-08-14** · **$0 · K=0**
**Card:** MSL-S2B · instrument **MYM** · mechanism **`sweep-failure-filtered-continuation`** (NEW; declared here, frozen at Stage-1)
**Parent:** [MSL charter](../../../docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md) step 1 pins · [second slate §MSL-S2B](../../../docs/briefs/programs/2026-08-13-msl-second-slate.md) · [design-box ADR](../../../docs/adr/2026-08-13-msl-slate-2-design-box.md) · [B8 occupancy](../../../docs/adr/2026-08-12-msl-mym-occupancy-release.md)

This record discharges Stage-0 hygiene for S2B: Rule-8 dedup paste, panel/CONFIRM pins, mechanism-id draft, occupancy cite. It is **not** Stage-1. **No SNAG registration** — MYM already carries `index-intraday-ohlcv-directional-timing-2026-07-21`.

---

## §0 — Rule 0 reads (verified this session @ `995b09d3`)

| Source | Anchor (`git log -1`) | What it grounds |
|---|---|---|
| [second slate §S2B](../../../docs/briefs/programs/2026-08-13-msl-second-slate.md) | `0a206373` | Card text; route kill limb #1; filter≠entry; kill list |
| [MSL charter](../../../docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md) steps 1–4 | `8290b895` | Pre-G0 steps; G0 needs B4 |
| [C1 closure](../../../docs/briefs/closures/MSL-C1-closure-falsified.md) · [`RESULTS_g2`](../../archive/msl_c1_mym_2026-08/RESULTS_g2.md) | `0a206373` | DELETE PASS both arms (filter asset); entry FALSIFIED |
| [B8 occupancy ADR](../../../docs/adr/2026-08-12-msl-mym-occupancy-release.md) | `c0d20bd0` | `MYM1!` released for non-Striker MSL/G0 |
| [`rejected_candidates.md`](../../../docs/rejected_candidates.md) raised bar | `0a206373` | `index-intraday-ohlcv-directional-timing-2026-07-21`; continuation exhausted |
| [SLR-MYM-1 closure](../../../docs/briefs/closures/SLR-MYM-1-closure-falsified-stage0.md) | `b2e3eec1` | Route ① CLEAR for MR-at-level only (gate 0-B) |
| [Temporal-selectivity ADR](../../../docs/adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md) | `b2e3eec1` | Within-instrument temporal selectivity outside mapped levers |
| [Q-TNEC-CON-5 closure](../../../docs/briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md) | `b2e3eec1` | Dense-1m OHLCV temporal-selectivity lane default **paused** |
| [`ops/instruments/MYM.md`](../../../ops/instruments/MYM.md) PROFILE / bars / M7 | `b2e3eec1` | Raised bar wired; panel span 2020-07-01→2026-07-03Z |
| [`core/data/bar_data/SHA256SUMS`](../../../core/data/bar_data/SHA256SUMS) | `38de84f7` | `24e169528f7ea6693b75c71c3195edf6a04f3a26c6b6dff0f2e9c623fd597a58 *MYM_M15.csv` |
| [design-box ADR](../../../docs/adr/2026-08-13-msl-slate-2-design-box.md) | `a37dba86` | Slate-2 box; Magdon-Ismail not calibration |

Local check: `core/data/bar_data/MYM_M15.csv` may be **absent** in this clone (vendor CSV gitignored). Hash authority is `SHA256SUMS`, not a re-hash of missing bytes.

---

## Rule-8 dedup paste (before camp scaffold)

Executed this session against `lab/CATALOG.md` + `docs/briefs/INDEX.md` (needles: `msl_s2b` / `s2b` / `sweep-failure` / MYM continuation):

```
# lab/CATALOG.md — msl_s2b / sweep-failure / s2b
(no matches)

# lab/CATALOG.md — msl_c1_mym / continuation (adjacent asset, not collision)
191:| msl_c1_mym_2026-08 | FALSIFIED | … | lab/archive/msl_c1_mym_2026-08/ |

# docs/briefs/INDEX.md — S2B / sweep-failure
(no matches)

# filesystem
lab/analysis/c1/msl_s2b* — No such file or directory (camp created after this paste)
```

**Verdict:** no live S2B camp; C1 archive is the DELETE-PASS asset this card consumes, not a same-theme collision on a new slug.

---

## Three Stage-0 answers

### 1. Mechanism draft (NEW)

Declare **`sweep-failure-filtered-continuation`**: trend-continuation entry on MYM **gated** by a PDH/PDL sweep-failure state — the sweep-failure is a **filter, never the entry**. rr ∈ [2, 3], hard stop, k=1, flat by 16:00 ET. Frozen at Stage-1; registered in `MECHANISMS.md` at card commit.

### 2. Panel pin

Manifest hash `24e169528f7ea6693b75c71c3195edf6a04f3a26c6b6dff0f2e9c623fd597a58` (`MYM_M15.csv`). MYM.md M7: n=141,471 bars, **2020-07-01 → 2026-07-03Z**. Same panel C1 used (1,607 IS sessions).

### 3. CONFIRM / IS (named unread) + occupancy

Proposed split (frozen at Stage-1; unread here): **IS &lt; 2025-09-01**, **CONFIRM 2025-09-01 → panel end** (not “today”). Occupancy: **CLEAR via B8** — `MYM1!` released for new non-Striker MSL research/G0; S1 keep-warm + Striker redeploy bar stand.

---

## What Stage-0 does **not** license

- Route adjudication / BINDING BAR answers (Stage-1 kill limb #1)
- `$0` screens / cheap falsifier (Stage-1)
- Composite clearance (“filter route-① ⇒ continuation entry CLEAR”)
- G0 freeze / B4 / Pine / TV / Cap / CONFIRM peek
- Databento estimate or pull
- Re-running C1 entry-role construct
- Operator un-pause of the dense-1m temporal-selectivity lane
- Magdon-Ismail as `R_max` recalibration

---

## Operator sign

| Field | Value |
|---|---|
| Election | **PROCEED** |
| Date | **2026-08-14** |
| Grounds | SESSIONS “S2B may resume” after C3-K2 explore FALSIFIED; second-slate sequencing; board slot free |
| Discharges | Stage-0 pins only — route remains Stage-1 limb #1 |

---

## Next

**Stage-1** (charter steps 2–4): freeze WHO (filter≠entry); run `msl_preflight` + `instrument_profiles.py cell MYM sweep-failure-filtered-continuation`; adjudicate **route kill limb #1 first** against the two slate-named candidates only; if FAIL → pre-G0 kill at $0 (correct). No G0 until Board **B4**.

**Artifacts not authored this record:** `PREREG_G0.md`.
