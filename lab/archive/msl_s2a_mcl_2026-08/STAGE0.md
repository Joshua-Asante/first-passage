# MSL-S2A Stage-0 — MCL SNAG bar + panel pin + box election

**Status:** `STAGE-0 PASS` · **PROCEED 2026-08-13** (P3.4 GO = operator election) · **$0 · K=0**
**Card:** MSL-S2A · instrument **MCL** · mechanism **`pullback-failure-resumption`** (NEW; declared here, frozen at Stage-1)
**Parent:** [MSL charter](../../../docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md) step 1 pins · [second slate §MSL-S2A](../../../docs/briefs/2026-08-13-msl-second-slate.md) · [design-box ADR](../../../docs/adr/2026-08-13-msl-slate-2-design-box.md)

This record discharges the slate’s Stage-0 gate: register the SNAG bar on [`MCL.md`](../../../ops/instruments/MCL.md) so the door-check is not vacuous (C2 pattern on MGC), and pin the landed M15 panel. It is **not** Stage-1.

---

## §0 — Rule 0 reads (verified this session @ `af01bf11`)

| Source | Anchor (`git log -1`) | What it grounds |
|---|---|---|
| [`ops/instruments/MCL.md`](../../../ops/instruments/MCL.md) PROFILE / W1–W4 | `7c609ff6` | No `bars:` before this commit; W1 monthly roll; W3 session window open; W4 FOMC; status OPEN geometry-cleared / mechanism-owed |
| [`MGC.md`](../../../ops/instruments/MGC.md) `bars:` | `c0d20bd` lineage / HEAD | SNAG registration pattern to copy |
| [second slate §S2A](../../../docs/briefs/2026-08-13-msl-second-slate.md) | `dc67c164` | Stage-0 = SNAG on MCL; panel sha256; CONFIRM must end at panel |
| [`core/data/bar_data/SHA256SUMS`](../../../core/data/bar_data/SHA256SUMS) | `7c609ff6` | `5aa504567b943ff68506b8b5c21df293c5a553543fdf1ac606adeb0f5bfbbd23 *MCL_M15.csv` |
| [design-box re-derivation](../../../docs/notes/notice/N-2026-08-13-msl-design-box-rederivation.md) §10 | `5dbf8129` | Box election requested; this session elects it |
| [Magdon-Ismail RESULTS](../../mc/mc_mdd_closed_form_2026-08/RESULTS.md) | `d917282c` | MEASURED validation; **not** calibration; `R_max` stays diffusion-approx |
| [hard-stop ruling](../../../docs/notes/notice/N-2026-08-13-external-eval-population-data.md) §10 item 3 | `2b5caeb5` | Hard stop mandatory; binds presence not type |
| [`firm_rules.py`](../../../core/firm_rules.py) `Tradeify_Select_100K` | HEAD | index-micro `$0.91`; comment pin MGC `$1.06` — slate prices MCL RT as MGC-like `$4.12` |

Local check: `core/data/bar_data/MCL_M15.csv` **absent** in this clone (vendor CSV gitignored). Hash authority is `SHA256SUMS`, not a re-hash of missing bytes.

---

## Three Stage-0 answers

### 1. SNAG bar (door-check non-vacuous)

Registered `bars: free-data-5th-leg-snag-closed-2026-07-01` on [`MCL.md`](../../../ops/instruments/MCL.md) PROFILE — same id C2 placed on MGC. Index-intraday OHLCV raised bar **omitted on purpose** (MCL is not an equity-index future; R-FRAMING = §2.1). `instrument_profiles.py build` same commit.

### 2. Panel pin

Committed manifest hash `5aa50456…bbd23` (`MCL_M15.csv`). Slate: 106,261 bars, **2022-01-02T23:00Z → 2026-07-02T00:00Z**. ⚠ CONFIRM window **must end at the panel**, not at “today.” Proposed split (frozen at Stage-1, unread here): **IS < 2025-07-01**, **CONFIRM 2025-07-01 → 2026-07-02**.

### 3. Box election + Magdon-Ismail

[ADR](../../../docs/adr/2026-08-13-msl-slate-2-design-box.md) elects the re-derivation §7 box and sequences S2A now. Magdon-Ismail closed-form vs `simulate_path` **AGREE** (validation). It does **not** re-derive §3 `R_max`. Frontier dollars remain the diffusion approximation. Eval-sprint lane **not elected**.

---

## What Stage-0 does **not** license

- Session-window ruling (W3) — Stage-1 names it **before any read**
- Roll-exclusion application (W1) — declared at Stage-1 / frozen at G0
- Door-check verdicts / BINDING BAR answers (Stage-1)
- `$0` screens / cheap falsifier (Stage-1)
- G0 freeze / B4 / Pine / TV / Cap / CONFIRM peek
- Databento estimate or pull
- Treating CONFIG-B-MCL fade geometry as this mechanism
- Opening the eval-sprint lane

---

## Operator sign

| Field | Value |
|---|---|
| Election | **PROCEED** |
| Date | **2026-08-13** |
| Grounds | P3.4 GO = operator election (design-box ADR Accepted same session) |
| Discharges | “Registering the SNAG bar on the MCL ledger is this card's Stage-0 task” ([second slate](../../../docs/briefs/2026-08-13-msl-second-slate.md)) |

**HOLD** (not taken): wait on Magdon-Ismail calibration before authoring cards.

---

## Next

**Stage-1** (charter steps 2–4): freeze the one named trigger class; answer SNAG + R-FRAMING; name session window (W3) and roll-exclude rule (W1) **before any read**; run `msl_preflight` evidence tables; adjudicate three kill limbs at MCL RT **$4.12** / 4× **$16.48**; entry-rate honesty; implied-SR printed not a kill. No G0 until Board **B4**.

**Artifacts not authored this record:** `PREREG_G0.md`.
