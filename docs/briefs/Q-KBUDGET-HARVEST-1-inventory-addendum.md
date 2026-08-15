# Q-KBUDGET-HARVEST-1 — Inventory addendum (Phase-2 ratification)

**Status:** **RATIFIED 2026-07-16 (operator)** — both harvested rows **ACCEPT**; **Phase-3 SCREENED PASS** (both). **H2's PASS superseded same day — see §4 post-ratification correction** (campaign scoping pinned the OOS event-count fork to the ratified default's strict reading; H2 now **FAILs Clause N**).  
**Parent Pre-Q:** [`Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md`](Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md) (`CLOSED-RESOLVED` 2026-07-16)  
**Phase-3 RESULTS:** [`lab/analysis/harvest/q_kbudget_harvest_1_2026-07/PHASE3_RESULTS.md`](../../lab/analysis/harvest/q_kbudget_harvest_1_2026-07/PHASE3_RESULTS.md)  
**Phase-2 record:** [`lab/analysis/harvest/q_kbudget_harvest_1_2026-07/PHASE2_RATIFICATION.md`](../../lab/analysis/harvest/q_kbudget_harvest_1_2026-07/PHASE2_RATIFICATION.md)  
**Does not rewrite** [`Q-KBUDGET-1-phase1-inventory.md`](Q-KBUDGET-1-phase1-inventory.md) D1–D7 (addendum only).  
**Screen extension:** **DONE** — append-only in `floor_scan.py` + `phase3_screen_manifest.json` via `axis_screen`.

---

## §0 — Rule-0 anchors (ratification session)

| Source | Anchor | Supplies |
|---|---|---|
| Parent harvest Pre-Q + frozen pre-reg | Phase-1 tip on `cursor/kbudget-harvest-phase1-5808` | §C four fields; Path 1a/1b pre-check; §B verdict needs Phase-3 for RESOLVED |
| Phase-1 candidate rows | [`CANDIDATE_ROWS.md`](../../lab/analysis/harvest/q_kbudget_harvest_1_2026-07/CANDIDATE_ROWS.md) | H-OD-1 + H-TSMOM-1 declarations |
| Parent floor scan (pre-extension) | `python3 lab/archive/q_kbudget_1_2026-07/floor_scan.py` → **RESOLVED**, PASS 1 (D5) | Harvest must not reopen parent; extension is additive |

---

## §1 — Addendum rows (Class D extensions)

Declarations per harvest pre-reg §C. **No screen verdict here** — Phase 3 fills PASS/FAIL/UNSCREENABLE.

| # | Axis | Family → K_banked | Design → K_intrinsic | Era → N | δ/σ (cohort) | Path 1 | Pre-screen posture |
|---|---|---|---|---|---|---|---|
| **H1** | `H-OD-1` overnight-drift inventory-risk (02:00–03:00 ET) | **ES → 1** | mechanism-first confirm; H1 unconditional OD hour; optional H2 BtD (RSV\<0) → **(1, 2)** | daily OD events, ~6.5y OOS → **N = 1000** | **0.093** (Boyarchenko/Larsen/Whelan FRBNY SR917 Table I, t-scaled) | **1a** | **PASS** — Clause K (K_eff 2–3, floor 0.85–0.98); Clause N power=0.837 |
| **H2** | `H-TSMOM-1` Moskowitz–Ooi–Pedersen 12m/1m TSMOM confirm (S&P 500 / ES) | **ES → 1** | mechanism-first confirm of frozen 12m/1m vol-scaled sign → **(1, 1)** | monthly events, post-pub OOS ≈2010–2025 → **N = 192** | **0.167** (Fig. 2 S&P 500 gross SR=0.58 → SR/√12; [`H_TSMOM_1_fig2_scrape.md`](../../lab/analysis/harvest/q_kbudget_harvest_1_2026-07/H_TSMOM_1_fig2_scrape.md)) | **1b PASS** (see Phase-2 record) | **PASS** — Clause K (K_eff=2, floor 0.85); Clause N power=0.638 @ N=192 |

**Family pin:** both rows are **ES**. NQ / MNQ re-expression requires a separate axis with its own cohort δ (Moskowitz has no NQ; OD cross-contract notes are not δ transplants).

**Honesty riders (campaign-layer, not ratification kills):**
- H1: unconditional OD Sharpe collapses net of bid–ask (Table IX); 2021+ fade via RSV-dispersion compression (Liberty Street 2026-07).
- H2: gross Sharpe only; monthly event rate; haircut SR=0.45 fails Clause N at N=192.

---

## §2 — Ratification record

Operator (Joshua) **2026-07-16**, in-session directive **"accept both"**:

1. **H-OD-1 → ACCEPT** into inventory addendum as **H1** (Path 1a; N=1000; family ES).
2. **H-TSMOM-1 → ACCEPT** into inventory addendum as **H2** (Path 1b scored PASS; **N=192**; family ES).

**Done:** Phase 3 — floor scan extended; [`PHASE3_RESULTS.md`](../../lab/analysis/harvest/q_kbudget_harvest_1_2026-07/PHASE3_RESULTS.md); harvest §6 **RESOLVED**.

---

## §3 — Audit hooks

```bash
# Addendum exists and names both rows
grep -n 'H-OD-1\|H-TSMOM-1\|ACCEPT' docs/briefs/Q-KBUDGET-HARVEST-1-inventory-addendum.md | head -20

# Phase-2 record present
test -f lab/analysis/harvest/q_kbudget_harvest_1_2026-07/PHASE2_RATIFICATION.md && echo OK

# Parent screen still RESOLVED before Phase-3 extension
python3 lab/archive/q_kbudget_1_2026-07/floor_scan.py | tail -3
# expect: PASS: 3 · … RESOLVED

# Phase 3 not yet silently done (AXES still D1–D7 only until Phase-3 commit)
grep -c 'H-OD-1\|H-TSMOM' lab/archive/q_kbudget_1_2026-07/floor_scan.py \
  && echo "Phase-3 rows present (expected)" || echo "FAIL: Phase-3 missing"
```

---

## §4 — Post-ratification correction (2026-07-16, same day — H2 screen verdict superseded)

**Does not edit §1's row H2 in place** — the Phase-3 PASS at N=192 was an accurate computation given that declaration; it is superseded here, not erased, per the standing no-in-place-edit convention for ratified verdicts (mirrors how the Campaign-defaults ADR and the H-OD-1 pre-reg carry corrections as dated annotations, never rewritten cells).

**What happened:** H2's campaign scoping ([`H-TSMOM-1-ES-tsmom-scoping.md`](rnd-pipeline/H-TSMOM-1-ES-tsmom-scoping.md)) found that row H2's declared **N = 192** ("post-pub OOS ≈2010–2025") does not derive from the ratified [Campaign-defaults ADR](../adr/2026-07-11-discovery-campaign-defaults-ratified.md)'s Default #1 (temporal-not-instrument OOS axis: statistical OOS starts **2019-05-06**, not 2010). Three readings were named (N=192/175/86 → power 0.638/0.598/0.34); the operator pinned **N≈86, the strict Default-#1-compliant reading**, same day.

**Corrected verdict:** at N≈86, **Clause N FAILS** (power 0.34 < 0.50 threshold; break-even N≈138). H2 moves from **PASS** to **FAIL (Clause N)** — joining D3/D7's class in the extended screen, not the PASS set with D5/H-OD-1.

**Consequence:** the harvest's Phase-3 "3 PASS" figure (§1 note above the row table, and `PHASE3_RESULTS.md`) is **superseded for H2** by this correction. Combined with D5 and H-OD-1's independent Stage-2 cost-law closures, **the ratified inventory's fundable set (H1 + H2 + D5) now has zero survivors.** This correction is a **screen-stage** reversal (H2 never reached `register_search open` or Stage-2) — distinct from D5/H-OD-1's Stage-6-pipeline closures, and it does **not** feed the harvest-intake ADR's §4 doctrine falsifier (Stage-6-confirm-scoped only).

**Not re-run in `floor_scan.py` / `phase3_screen_manifest.json` / `phase3_results.json`** — those machine artifacts still show H2 PASS at N=192 and are not edited by this correction (append-only convention); a future maintenance pass may add a superseding manifest row if the harness needs the corrected verdict machine-readable.

```bash
# This correction exists and names the superseding scoping brief
grep -n 'Post-ratification correction' docs/briefs/Q-KBUDGET-HARVEST-1-inventory-addendum.md

# The scoping brief it points to exists and carries the FAIL disposition
grep -n "Clause-N FAIL\|P1 pinned" docs/briefs/rnd-pipeline/H-TSMOM-1-ES-tsmom-scoping.md | head -5

# Machine artifacts are unchanged (still show the pre-correction N=192 PASS — expected,
# append-only; this correction is a doc-layer annotation, not a harness re-run)
grep -n "H-TSMOM" lab/analysis/harvest/q_kbudget_harvest_1_2026-07/phase3_screen_manifest.json
```
