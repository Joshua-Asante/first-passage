# Phase C — The Gauntlet (per-candidate: card → screens → G0 → explore → Pine → TV → survivor MC)

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development or
> superpowers:executing-plans. Checkbox (`- [ ]`) syntax for tracking.

**AUTHORIZATION:** per-candidate. The gauntlet **is** the ratified MSL charter
([`2026-08-12-msl-manual-sourcing-loop-charter.md`](../../spec/2026-08-12-msl-manual-sourcing-loop-charter.md))
— this plan adds one new pre-G0 step (the A2 shape screen), sequences the operator seats, and
does not restate the charter (charter governs on any divergence). Operator gates inside: **B4 GO**
(step 5, G0 freeze — no self-freeze), **EXPLORE_GO token** (step 5a — never self-issued), **TV
seat** (step 7 — operator-only; refused if step 2–5 artifacts are missing), and the standing
per-session GO discipline.
**Cost:** $0 until a lane's own pre-registered pull; every pull needs its Rule-1 estimate first.
**Parent:** [`sequence overview`](2026-08-23-viable-strategy-sequence-overview.md) ·
**Input:** a Phase-B survivor (bar-cleared, falsifier-surviving, shape-prechecked).

**Timeline expectation:** ~1–2 weeks per candidate, dominated by the operator TV seat and any
paper-log calendar time — not by build effort.

---

## Per-candidate checklist (charter steps, with this sequence's additions marked ⊕)

- [ ] **1. Slate card** — idea + mechanism story (WHO loses money and why), **one** construct
  class named by mechanism reasoning with zero data contact, instrument pinned by
  mechanism-independent reasoning. ⊕ Card carries the Phase-B lane's falsifier evidence and the
  operator bar-reading record (B1.3/B2.1) inline — a reader must see the re-proposal bar was
  cleared by ruling, not by silence.
- [ ] **2. Dedup + door-check, executed not asserted** — paste `rg` output over
  `docs/rejected_candidates.md` + `lab/CATALOG.md` + briefs bar-rulings (search by mechanism
  family AND role); declare the mechanism id (nearest class or NEW) in
  `ops/instruments/MECHANISMS.md` at the card commit; run
  `scripts/instrument_profiles.py cell <SYMBOL> <mechanism-id>`; answer every BINDING BAR in
  writing. Non-index ledgers may carry no `bars:` section — domain bars are explicit card line
  items that block G0 independent of tool output.
- [ ] **3. $0 arithmetic screens at one declared design point** — cost-law (gross/trade ≥ 4×
  all-in RT, re-priced from the instrument's own tick/commission schedule); payability (all-win
  day clears $200); survival (worst achievable EOD day ≤ $750). Disclosures per charter
  (implied-SR report-only; σ_d vs the trail; best-day-≤-40% shape; 0.40R inversion line).
  ⊕ **3b. Shape screen (new, additive):** the card's declared design point is scored against
  Phase A2's feasible region — `PASS`/`MARGINAL`/`FAIL` with the region's own SE bars.
  `FAIL` is a pre-G0 kill; `MARGINAL` proceeds only with the margin stated on the card. This
  screen is disclosure-plus-gate on *shape*, and touches no charter threshold.
  ⊕ **3c. Data-read rule reaffirmed:** any pre-G0 measurement runs only on a declared IS
  partition; the CONFIRM window is named in the card before any step-3 read and stays unread
  through step 8.
- [ ] **4. Cheap falsifier before authoring** (<~5 min, parent-side, GENEROUS so failure is
  conclusive) — where Phase B's lane falsifier already discharged this, cite it; do not re-run
  theater.
- [ ] **5. G0 pre-registration freeze — operator B4 GO only.** K_intrinsic per axis declared;
  CONFIRM holdout re-reserved; sweep axes pre-registered as robustness probes (selection
  in-sample only). ⊕ Window-collision sweep against every live reservation (the MNQTAPE-2
  precedent: check `discovery_manifests/burned_segments.json` + standing campaign reservations
  before naming any window).
- [ ] **5a. Explore-confirm — EXPLORE_GO token, never self-issued.** Session-block bootstrap 95%
  CI per pre-registered arm + Req-1a DELETE/FLIP on the pinned IS panel only. Verdict routes per
  the card's own `PREREG_G0.md`: `FALSIFIED` / `SHAPE-CLEAR` (the only route forward) /
  `AMBIGUOUS-HOLD` / `VOID`. A DELETE/FLIP pass never rescues a CI-falsified primary.
- [ ] **6. Pine authored CC-solo** (surface-allocation test 1 — Pine never fleets); `pine_lint`
  green; runbook names exact inputs, date window, chart TZ (America/New_York for ET-based
  session logic). Pine lands gitignored + hash-pinned from a durable machine (the MSL-S4
  ephemeral-pin lesson — never pin from a cloud session).
- [ ] **7. Operator TV backtest** — runbook links the step 2–5 artifacts (dedup block ·
  door-check record · screens table ⊕ shape-screen row · G0 PR#); **operator refuses the seat if
  any is missing** (the chokepoint). Export → local copy → **static-equity recompute before any
  param compare** (TV compounds).
- [ ] **8. Survivor MC is the verdict** — corrected geometry default (`dd_lock_offset_usd`
  unreachable — verify at read, never re-patch); intraday-honest limb only where the daily
  series carries a true intraday low (a close-reconstructed series is labeled LOWER BOUND unless
  TV Run-up/Drawdown columns bound within-trade excursion); emit the TNEC verdict string
  `N-ACT N-SURV N-EDGE N-SHAPE N-SIZE | bust | P(pass) | μ(disclosed)`.
  ⊕ Pass% citations carry the N-SURV magnitude-resampling caveat (N18 discipline).
  Kill → registry entry. Survive → TNEC-1 intake → operator GO chain (M1 + per-session GO
  untouched) → **Phase D**, and in parallel → **§4 scoring** (parallel plan) once the firm-model
  repair has landed.

## Sleeve rule (B3-class candidates)

A sleeve candidate (activity-insufficient alone) may run the gauntlet, but its card must name the
daily mechanism it rides beside; a sleeve reaching step 8 alone parks at TNEC intake until a
daily partner exists. The operator token-trade never substitutes for a sleeve's partner in any
scored artifact.

## Kill hygiene

Every kill lands where the next reader looks: registry row (strategy-grounds kills), instrument
ledger disposition line, CATALOG status, closure with typed Iterate block — same-session, per the
Iterate-closure-exit ADR. Cheap honest kills are wins (S6); the failure mode to avoid is a
half-recorded kill that a future session re-derives.

## Forbidden moves (inherited, restated for this sequence)

Post-hoc filters after seeing results · instrument-hopping after scoring · TV-report metrics as
the verdict · weakening any charter/harvest/EM screen "because manual" · reopening `Q-ORBCUSH-1`
or the ORB target · editing the A2 region to admit a favored candidate (the region changes only
by re-running its harness under its own pre-registration) · self-issuing B4/EXPLORE_GO/TV seats.

## Exit criteria

A candidate emits the TNEC string with bust ≤ 3.0% ∧ P(pass) ≥ 50% intraday-honest and enters
TNEC-1 intake — Phase D begins. Or the candidate set exhausts with recorded kills — Phase B's
exit logic governs.
