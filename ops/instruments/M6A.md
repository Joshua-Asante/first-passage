# INSTRUMENT LEDGER — M6A

**Symbol:** CME Micro AUD/USD futures (M6A; Globex, Databento `GLBX.MDP3`) · **Parent:** 6A (standard AUD/USD — **un-ledgered**) · **Asset class:** FX futures (micro)
**Contract facts in committed record:** `tick_value` **$1.00** (via Stage-1 RT connecting arithmetic: RT 1t **$2.82** = 2×**$0.91**/side commission + $1.00); Stage-2 derived point value **$10,000.00**/pt (`tick_value_usd / tick_size`). Do not invent tick size or multiplier beyond those citations.
**Status:** **Research/discovery only — geometry-documented, no mechanism cell, no candidate.** Stage-1 Currencies **SURVIVOR** (`FLAG-COSTBIND`); Stage-2 ex-FOMC surface measured; Q-TNEC-ENV-1 envelope **NON-EMPTY** at 20/40/80/160-tick cells. Census produced **no M6A entry**. Not a live leg; no allocation; no K spend.
**Last updated:** 2026-08-11

**Purpose:** single source of instrument-level truth (operational rule 10, [`docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md`](../../docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md)). Created **2026-08-11** as the operator follow-up named by [`Q-TNEC-ENV-1-closure.md`](../../docs/briefs/closures/Q-TNEC-ENV-1-closure.md) §4 — ADR [`2026-07-25-instrument-profile-index.md`](../../docs/adr/2026-07-25-instrument-profile-index.md) §5 (creation-on-touch). Closes the unconsultable gap: `python scripts/instrument_profiles.py cell M6A <mech>` exited 2 FATAL because no ledger existed; 7 of 56 ENV-1 census cells ran without the mandatory consult limb.

## PROFILE (machine-readable)

```yaml
symbol: M6A
asset_class: fx-futures
family: []
venue_tradable: true
venue_note: "Tradeify Currencies Product Group lists 6E/M6E/6B/6J/6A/M6A/6C/6S (see MJY.md venue_note). Withdrawn Striker legs no longer reserve cap headroom for new non-Striker research (MSL B8 occupancy release 2026-08-12); Striker redeploy still barred; LEG_MAP code untouched."
k_bank_source: "../../discovery_manifests/"
cost_hurdle:
  value: 2.82
  units: "USD/round-trip (1-tick slip)"
  basis: "Stage-1 third-leg map Inputs: commission $0.91/side; RT 1t $2.82 / 2t $3.82; cost-tax 1t r=1 = 0.0902 (FLAG-COSTBIND vs own-panel floor 0.0891)"
  source: "#A1"
structure:
  - claim: "Stage-1 Currencies SURVIVOR under FLAG-COSTBIND — cost-tax binds before the own-panel Clause-N floor on the pooled panel; Stage-2 ex-FOMC flips the binding constraint COST->POWER."
    source: "#A1"
  - claim: "Q-TNEC-ENV-1 envelope NON-EMPTY at 20/40/80/160-tick cells (8-tick DEAD on cost); census authored no M6A entry; published FX-fix delta refused as cross-instrument transplant under strategy_harvest Requirement 2."
    source: "#A4"
```

---

## STANDING WARNINGS (read first)

- **W1 — Parent 6A is un-ledgered.** Creating `6A.md` without a live touching session on 6A itself would be the "complete the matrix" motive ADR 2026-07-25 §5 forbids. M6A therefore inherits **no** bars via `family`; class-level or cross-instrument claims must be cited here from their own records, not assumed from the standard.
- **W2 — `ohlcv-1d` UTC-day bucketing → phantom weekend bars.** Drop settle-date weekday > 4. Feed-general.
- **W3 — Stage-2 primary surface excludes pinned FOMC Wednesdays.** Operational N and power floor are the **ex-FOMC** figures (N=450 / floor 0.0924), not the Stage-1 pooled-panel floor. `FOMC_DATES_ET` in the Stage-2 runner is hand-pinned (best-effort provenance) — see [`RESULTS_stage2.md`](../../lab/analysis/c1/c1_thirdleg_instrument_map_2026-07-27/RESULTS_stage2.md).
- **W4 — Envelope OPEN ≠ edge.** Every OPEN cell in the ENV-1 ladder states a **requirement** only; harvest Req 1–5, DSR-at-K, N-SURV MC, and the regime gate remain independent and unweakened ([`RESULTS.md`](../../lab/archive/tnec_envelope_compile_2026-08/RESULTS.md) §4).

---

## DURABLE FINDINGS

| # | Finding | Evidence | Confidence |
|---|---|---|---|
| **A1** | **Stage-1 Currencies SURVIVOR, `FLAG-COSTBIND`.** Own-panel N **484**, Clause-N power floor **0.0891**; RT **1t $2.82 / 2t $3.82**; cost-tax 1t r=1 **0.0902** (> floor ⇒ COST binds first on the pooled panel). Inputs pin commission **$0.91**/side. Connecting arithmetic for tick value: RT 1t $2.82 = 2×$0.91 + **$1.00** ⇒ `tick_value` **$1.00**. | [`RESULTS.md`](../../lab/analysis/c1/c1_thirdleg_instrument_map_2026-07-27/RESULTS.md) (Currencies row + Inputs meta) | **HIGH** (committed Stage-1 table). |
| **A2** | **Stage-2 ex-FOMC surface: N 450 / floor 0.0924; binding-constraint FLIP COST→POWER.** Cost-tax 0.0902 sits above Stage-1 floor 0.0891 but below the ex-FOMC floor 0.0924 — so a leg that skips announcement days is power-bound, not cost-bound. Stage-1's `FLAG-COSTBIND` remains correct for the pooled panel it describes. | [`RESULTS_stage2.md`](../../lab/analysis/c1/c1_thirdleg_instrument_map_2026-07-27/RESULTS_stage2.md) joint table + Cost 1 prose | **HIGH** (committed Stage-2). |
| **A3** | **Primary `tau_max` (wed_thu ex-FOMC, σ ≤ $125.00):** 09:30/10:00/10:30 **360**; 11:00/12:00 **240**; 13:00 **180**; 14:00 **120**; 15:00 **90** (min). Exclusion does **not** change any start's `tau_max` vs pooled (costs power only on this instrument). Joint-table headline cell: largest measured tau_max ties include **360min @ 09:30** (with MYM and others). Point value derived **$10,000.00**/pt; IS cache coverage **56/56** chunks for its own window. | [`RESULTS_stage2.md`](../../lab/analysis/c1/c1_thirdleg_instrument_map_2026-07-27/RESULTS_stage2.md) §M6A + joint table | **HIGH** (measured surface). |
| **A4** | **Q-TNEC-ENV-1: envelope NON-EMPTY; census produced no M6A entry; FX-fix δ transplant REFUSED.** Ladder: 8-tick `DEAD(cost)`; **20/40/80/160-tick `OPEN`** against power floor 0.0891 (H_A NON-EMPTY). Across the 8-class × 7-instrument grid, every M6A cell is **no entry** (unconsultable at pass time because this ledger was missing). The daily-auction/settlement M6A row discloses only that the hurdle is **11.6 ticks = 11.6 pips** against a ~2 bp-scale cited FX-fix effect (**>7× short** at any plausible AUD level) and re-scores **P3-4 MULTI-FIX-FX** `UNSCREENABLE(δ)` — cross-instrument transplant of that δ is **REFUSED** under strategy_harvest Requirement 2 (same refusal class as the MCL entry's explicit Req-2 bar). | [`RESULTS.md`](../../lab/archive/tnec_envelope_compile_2026-08/RESULTS.md) §2 M6A · §6 grid · §6.4.4 · [`prior-p3-4-multi-fix-fx-m6a.json`](../../lab/archive/tnec_envelope_compile_2026-08/entries/prior-p3-4-multi-fix-fx-m6a.json) · [`mcl-tas-settlement-window-replication.json`](../../lab/archive/tnec_envelope_compile_2026-08/entries/mcl-tas-settlement-window-replication.json) (Req-2 refusal wording) · [closure §4](../../docs/briefs/closures/Q-TNEC-ENV-1-closure.md) | **HIGH** on envelope + no-entry accounting; **disclosure-only** on the FX-fix magnitude comparison (not a scored M6A entry). |

## DEAD / REJECTED (instrument-specific)

| Rejection | Discriminator | Source |
|---|---|---|
| P3-4 MULTI-FIX-FX (Tokyo + London WMR + NY fix cluster) as an M6A seed | Re-score `UNSCREENABLE(δ)`; prior census forbade quoting δ; ENV-1 authored **no entry**. FX-fix effect cited only as Req-2-inadmissible cross-instrument disclosure (>7× short of the 11.6-tick hurdle). | [`RESULTS.md`](../../lab/archive/tnec_envelope_compile_2026-08/RESULTS.md) §6 daily-auction/settlement × M6A · [`prior-p3-4-multi-fix-fx-m6a.json`](../../lab/archive/tnec_envelope_compile_2026-08/entries/prior-p3-4-multi-fix-fx-m6a.json) |

No mechanism×instrument PROFILE `cells` row is registered yet — consult returns `untested` until a dated verdict is authored against a `MECHANISMS.md` id.

## ACTIVE / OPEN

- **Consult limb restored** by this ledger's existence. Any future M6A intake must run `python scripts/instrument_profiles.py cell M6A <mechanism-id>` and append a dated disposition here.
- **No candidate, no election, no K spend.** Envelope NON-EMPTY admits nothing (A4 / RESULTS §4).
- **Parent 6A remains un-ledgered** (W1).

## SESSION LOG

- **2026-08-14n** — **MSL WHO-track `STILL DRY`.** FX leftover doors (option-cut, Asia-range fade, iron-ore beta, RBA) died on sign / C2–C3 transfer / event-window / preference. Envelope still NON-EMPTY; still no mechanism cell. [notice](../../docs/notes/notice/N-2026-08-14-msl-who-track.md). $0 / K=0.
- **2026-08-11** — **Ledger created** as the named ENV-1 operator follow-up ([closure](../../docs/briefs/closures/Q-TNEC-ENV-1-closure.md) §4). Seeded A1–A4 from committed Stage-1 / Stage-2 / ENV-1 artifacts only; no invented history. Regenerated `profiles.json` / `PROFILES.md` via `instrument_profiles.py build`. No pull, no K, no election, no `core/` / Pine / allocation / `dd_protection` / rail change.
