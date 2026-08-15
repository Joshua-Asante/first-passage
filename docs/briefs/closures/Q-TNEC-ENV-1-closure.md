# Q-TNEC-ENV-1 — closure: `NULL` (H_B = 0, STOP per PREREG F7)

**Verdict:** `NULL` (H_B = 0) · 2026-08-11 · $0 · K=0
**Pre-registration:** [`PREREG.md`](../../../lab/archive/tnec_envelope_compile_2026-08/PREREG.md) (FROZEN 2026-08-10)
**H_A:** overall **NON-EMPTY** — MYM / M2K / MCL / M6A **NON-EMPTY** (full); MNQ / MES / MGC
**NON-EMPTY-CONDITIONAL(power)** (UNSCREENABLE-INPUT(panel_N), admitted under F5's generous falsifier)
**H_B:** **0 SEED-GRADE** — 2 authored census entries + 17 prior-census re-scores (19 scored), one taxonomy pass
over the full 8-class × 7-instrument = 56-cell grid (stop rule: taxonomy exhaustion, F6)
**Spend / K:** $0.00 · K=0 · zero panel PnL/returns examined anywhere in either phase (Phase A: arithmetic on
committed constants; Phase B: published literature and market-structure facts only)
**Live effect:** none — no candidate proposed, admitted, scored, or licensed; harvest Req 1–5, DSR-at-K, N-SURV
MC, and the regime gate are untouched and unweakened
**Artifacts:** [`RESULTS.md`](../../../lab/archive/tnec_envelope_compile_2026-08/RESULTS.md) ·
[`RESULTS.json`](../../../lab/archive/tnec_envelope_compile_2026-08/RESULTS.json) ·
[`entries/`](../../../lab/archive/tnec_envelope_compile_2026-08/entries/)

**What survives regardless (documentation, not a candidate — none of this is admitted, proposed, or licensed):**

1. The compiled per-instrument envelope ([RESULTS.md](../../../lab/archive/tnec_envelope_compile_2026-08/RESULTS.md) §2) and its per-instrument "G0 must defend" numbers (required δ, cost tax, qty@frontier, power floor) across the full 7-micro pool.
2. The runner (`run_envelope_compile.py`) and the census entry scorer (`--entry` mode) — reusable at $0 for any future draft's intake screen.
3. The **outright/spread mismatch** finding (RESULTS.md §6.4.1): most mandated flows this taxonomy can name express in **spread** space (front-vs-deferred, cash-vs-futures, hedged-vs-unhedged), while this envelope is **outright single-instrument** framed. It fired on 5 cells across 3 classes and is not a δ question — no citation work fixes it. Any spread-framed envelope is a **new campaign**, not a re-run of this one.
4. The **δ-blindness** finding (RESULTS.md §6.2): the 2026-07-26 forced-flow census forbade quoting δ by construction ("No entry quotes PnL, δ, or any edge number"), so all 17 of its re-scored entries return `UNSCREENABLE(δ)` here by construction — a property of that census's own zero-δ discipline, not a new mechanism finding about those 17 cells.
5. The **MCL TAS δ-probe route** (RESULTS.md §6.4.3): the one cell blocked on δ alone, with a *non-circular* probe — CME publishes TAS settlement-window volumes free, unlike the F1/MOC route which needs gated data. Recorded as a route, not a proposal.

**Flagged for operator ruling — unresolved, not adjudicated by this closure:**

(a) The MGC entry ([`mgc-benchmark-fix-window-r8-rescore`](../../../lab/archive/tnec_envelope_compile_2026-08/entries/mgc-benchmark-fix-window-r8-rescore.json)) re-scores the one-day-old, independently-closed R8 SCREEN-FAIL (2026-08-10) — labeled calibration/known-answer in the entry itself (RESULTS.md §6.4.2: "a known-answer anchor for the `--entry` path"). The operator may rule this row **dropped** if it reads as re-litigation of an already-closed finding rather than an independent cross-check. H_B is 0 either way — the row scored `FAIL`, not `SEED-GRADE`.
(b) The MCL re-open ([`mcl-tas-settlement-window-replication`](../../../lab/archive/tnec_envelope_compile_2026-08/entries/mcl-tas-settlement-window-replication.json)) rests on an inference from the 2026-08-10 L2 scope ruling that the ≥2-independent-events/day law which killed BE3/SFX-1 is a **fade-program** screening law, not a TNEC limb — quoted verbatim in [`N-2026-08-11-daily-auction-settlement-MCL.md`](../../notes/notice/N-2026-08-11-daily-auction-settlement-MCL.md) ("*No ≥N-trades/day floor — that law was fade-scoped; TNEC N-ACT is weekly*"). The operator confirms or vacates that re-open basis; the entry scored `UNSCREENABLE`, not `SEED-GRADE`, regardless.

> **RULED 2026-08-11 / JA — both items, post-closure light record (recommendation adopted):**
> **(a) KEEP.** The row reads as calibration/known-answer, not re-litigation: it kills the same candidate
> **harder** through a second unit system (8.35 ticks vs the 11.6-tick 4× hurdle, concordant with R8's
> 3.21 bp vs 6.34 bp) and thereby **strengthens** the R8 closure. The R8 re-proposal bar stands unmodified.
> **(b) CONFIRMED — narrow.** *BE3's fade-scoped kill does not bar a TNEC-limb-scored TAS settlement
> candidate; the direction re-opens only through a completed δ-extraction probe.* No probe, no candidate.
> The probe route (free CME TAS settlement-window volumes; non-circular) is now a **live, unowned** next
> step — it becomes a candidate only via the full intake chain per the sequencing note below.

**Sequencing note:** this campaign ran **Blocks-1-adjacent $0 screening only** — envelope arithmetic plus one
frozen-taxonomy census pass. Any future seed sourced against this envelope still runs the **full** intake
chain (dedup paste, EM verdict string, harvest Req 1–5) before it is a candidate. Nothing here discharges
that chain.

---

## 1. Verdict against the frozen gate (PREREG F7)

| F7 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `STOP / FALSIFIED` | H_A EMPTY everywhere | H_A **NON-EMPTY** — 4 instruments clear outright, 3 more clear cost and are power-conditional | — |
| `STOP / NULL` | H_B = 0 | H_B **0** SEED-GRADE of 19 scored entries | ✓ |
| `INTEGRATE` | H_B ≥ 1 | — | — |

Both authored entries fail an envelope wall: MGC on **cost**, with a genuinely cited δ (`FAIL`, 8.35 < 11.6
required ticks); MCL on **δ absence** (`UNSCREENABLE`, no published cohort δ and no transplant admissible
under harvest Req 2). All 17 re-scored prior entries return `UNSCREENABLE(δ)` by the re-score protocol's own
construction (RESULTS.md §6.2). Zero cells reach `SEED-GRADE` → F7's NULL branch fires as pre-registered.

## 2. What the pre-registration predicted vs what happened

PREREG gated Phase B on H_A NON-EMPTY without predicting its shape; the actual split — 4 instruments clearing
outright (MYM, M2K, MCL, M6A) vs 3 clearing cost but landing power-conditional on a missing Stage-1 N (MNQ,
MES, MGC) — was not anticipated at freeze time. F6's taxonomy-exhaustion stop rule ("regardless of count")
fired as designed: the pass ran all 56 cells despite 54 resolving to "no entry" early. No surprise on the
H_B side — F7 explicitly reserved the NULL branch as a first-class, pre-registered outcome, not a fallback
read in after the fact.

## 3. What this closure does NOT license

Reading any cell in the envelope as measured edge — every OPEN cell states a requirement, never an achieved
result (RESULTS.md §4.1). Treating either scored census entry (`FAIL`, `UNSCREENABLE`) as a candidate. Reading
the 17 re-scored prior entries as newly falsified mechanisms — they are `UNSCREENABLE(δ)` by the census's own
construction, not by anything this pass discovered about the mechanisms themselves. Loosening Req 1–5,
DSR-at-K, N-SURV MC, or the regime gate under cover of "necessity was screened here." Re-running this taxonomy
over this same 7-instrument pool as a re-proposal. Adjudicating either item in "Flagged for operator ruling"
above — both stay open questions.

## 4. Defects found in the frozen packet (recorded, not repaired)

Two housekeeping gaps surfaced mid-pass, out of this task's touch scope (RESULTS.md §6.4.4):

- `ops/instruments/MGC.md` carries no cell for the 2026-08-10 R8 `SCREEN-FAIL`, so the instrument-profile
  consult under-reports a cell that is already closed.
- M6A has no ledger at all under `ops/instruments/` (27 files, none named M6A) — every M6A cell in the census
  grid (7 of 56) was screened without the profile-consult limb the entry contract names; `cell M6A <mech>`
  exits 2 `FATAL`.

Neither defect changes H_B (no M6A cell earned an entry regardless) or is repaired by this closure.

## 5. Lesson candidates

Below the two-incident bar — watch, no new lesson filed. The δ-blindness finding is a property of a prior
census's own discipline surfacing under a different tool, not a fresh incident against this campaign's own
conduct.

---

## Iterate

- **Verdict used:** `NULL` (H_B = 0), STOP per PREREG F7
- **Model update:** the envelope narrows "is a TNEC-shaped seed structurally possible" from one measured
  instrument (MNQ, K-wall) to a 7-micro pool with per-cell requirement numbers — it does **not** narrow "does
  a mandated-flow mechanism exist that clears those numbers." This pass's own census found none. The
  outright/spread mismatch (§6.4.1 above) is the load-bearing reason: genuine mandated flows mostly name a
  spread direction, and an outright-framed envelope structurally cannot admit them — the surviving
  outright-signed flows are exactly the ones already registry-dead, procurement-gated, or Req-4-dead, which
  is why the grid closed 54/56 empty.
- **Next:** STOP
- **Routing:** STOP — envelope RESULTS stands as documentation for any future draft's intake screen; no
  successor Q is opened by this closure.
- **Entry packet:** n/a — STOP (F7's INTEGRATE branch, the one-line sourcing-pointer proposal, is reached only
  at H_B ≥ 1; not reached here).
- **Stop rule / re-proposal bar:** re-entry requires a genuinely **new** F6-shaped flow class or a **newly
  measured instrument** outside {MNQ, MYM, MES, MGC, M2K, MCL, M6A} — never a re-pass of this taxonomy over
  this pool, and never a retune of the cost/power walls (F3/F4/F5 are owner-derived — `cost_model.py`,
  `floor_scan.py`, the Stage-1 map — not this campaign's to loosen).
- **Board write:** `STATE.md` decision-index line (2026-08-11, filed above the existing Phase-A line) +
  `docs/SESSIONS.md` entry `2026-08-11b` + `lab/CATALOG.md` status row (`ACTIVE` → `HOLD`, archive owed) —
  all in this commit.

## §10 audit-hook discharge

PREREG.md's `Boundary:` clause, discharged against the executed pass:

```text
no pulls · no MC · no PnL reads                                          OK  (RESULTS.md self-reports $0/K=0
                                                                               at both header and §6 preamble)
no edits outside campaign dir + notice logs + board files                OK  (entries/, RESULTS.md, two
                                                                               N-2026-08-11 notice logs, this
                                                                               closure + CATALOG/STATE/SESSIONS)
no re-derived constants (cost_model / floor_scan / firm_rules own them)  OK  (F3/F4/F5 imported, not restated)
no threshold invention                                                   OK  (F4/F5 kill predicates frozen at
                                                                               PREREG time; §6 added no new
                                                                               threshold)
screen the class never a scored list (EM §2.0a)                          OK  (56 class×instrument cells, not a
                                                                               ranked candidate list)
outputs pre-committed K=1-2 (EM0)                                        OK  (K=0 throughout — no candidate
                                                                               scored, K never spent)
no loosening of Req 1-5 / EM0 / regime gate under cover of necessity     OK  (§3 body, above)
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-11 | Closure authored | Claude Code (Task 9) |
