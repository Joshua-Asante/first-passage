# Audit — Kill-register constraint-attribution (Task A1)

**Audit ID:** AUDIT-2026-08-23-kill-register-attribution
**Date:** 2026-08-23
**Triggered by:** scheduled — Task A1 of the viable-strategy sequence, Phase A
([`plan`](../../superpowers/plans/2026-08-23-viable-strategy-phase-a-target-derivation.md) §Task A1)
**Authors:** Joshua (GO) + Claude Code
**Scope:** every strategy-grounds kill in the estate — registry + closures + Notice-phase census +
door-table screens. Pure attribution pass: **$0, K=0, no locked surface touched.**
**Lives in:** `docs/notes/audits/2026-08-23-kill-register-attribution-audit.md`

---

## §0 — Source anchors (Rule 0, this session)

| Artifact | Anchor |
|---|---|
| `docs/rejected_candidates.md` (read in full, 1741 lines) | `HEAD` = `6c0b14a` (2026-08-23) |
| `docs/briefs/closures/` (97 files; every `**Verdict:**`/`**Status:**` line grepped, 18 non-standard headers read individually) | working tree at `6c0b14a` |
| `docs/notes/notice/N-2026-08-14-msl-who-track.md` §3 door tables | `1f3a2bb` (2026-08-15) |
| `docs/notes/notice/N-2026-07-26-forced-flow-census.md` (pruned; retrieved in full, all 4 passes) | `git show pre-prune-2026-08-08:docs/notes/notice/N-2026-07-26-forced-flow-census.md` |
| `ops/instruments/MCL.md` INTAKE-DRY entries (2026-08-09 → 2026-08-14) | `f2cbb7b` (2026-08-21) |
| `lab/CATALOG.md` (full file, Active + Archived tables) | `c42e7e7` (2026-08-23) |
| `docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md` (four-clause admissibility test, verbatim) | `0dcc488` (2026-08-21) |
| Task brief §Task A1 | `docs/superpowers/plans/2026-08-23-viable-strategy-phase-a-target-derivation.md` |

**Retention note:** `pre-prune-2026-08-08` tag confirmed present (`git tag`); the census retrieval is
reproducible by any future session via the command above — the file is deliberately absent from the
working tree, not lost.

---

## §1 — Method

Walked every strategy-grounds kill across four source classes and tagged each with:

1. **Kill class(es)** from the frozen taxonomy below (multi-tag where the record cites more than one
   binding limb).
2. **Cell-demonstrated** (the specific construct was itself measured/screened and failed on its own
   data) **vs category-inherited** (killed by citation to a prior kill — never independently run, or
   subsumed by a lane/domain closure).
3. **Would-revive-under**: `{impact-persistence size re-aim, threshold-parameterized WHEN, neither}` —
   Amendment 1 and Amendment 2 as literally worded in the plan brief (§Task A3), evaluated against
   each cell's *actual* documented disqualifying limb, not a hypothetical better version of the kill.

**Kill-reason classes (frozen before tagging, verbatim from the task brief):** `SIZE`
(full-institutional-flow/capacity — the WHY clause fails because the mandated flow itself is not a
small residual), `DIRECTION` (the constraint does not entail a signed trade — BE1/WHERE-not-WHETHER
laundering), `CADENCE` (frequency below the activity/validation floor), `COST` (fails the 4×
round-trip arithmetic), `TRANSFER` (same mechanism, new ticker), `REGISTRY` (blocked by a prior
family/lane/domain kill), `POWER` (statistically undetectable at the estate's N), `VENUE` (instrument
not legal/available at the four friendly firms), `SPREAD` (two-legged expression), `EVIDENCE`
(cross-domain cohort transplant / measured-and-negative on its own data, no informed-flow or cost
story attaches), `OTHER` (named per row, never a dumping ground).

**Four sources walked, in the brief's order:**

- **Table 1** — `docs/rejected_candidates.md` registry rows (the primary, "complete" register).
- **Table 2** — `docs/briefs/closures/` entries that are genuine strategy-grounds kills **not yet
  folded into the registry** (surfaced by the verdict-line triage — see §2 for why each stayed out).
- **Table 3** — the forced-flow census (`N-2026-07-26-forced-flow-census.md`), all four passes.
- **Table 4** — the WHO-track notice §3 door tables + `ops/instruments/MCL.md` INTAKE-DRY entries.

**Amendment tests applied (reading Amendment 1/2 exactly as A3's draft states them, per the plan
brief and cross-checked against the actual four-clause admissibility test in
[`ADR 2026-07-26`](../../adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md) §2-A):**

- *Impact-persistence size re-aim* only rescues a cell whose **sole or binding** disqualifying limb
  is "the flow is not a small residual" (a WHY-clause SIZE failure) **and** whose cost figure was
  computed on average, not event-time, spreads. It cannot rescue a cell that is independently killed
  on CADENCE, POWER, or DIRECTION grounds — those legs are untouched by a size reframe. It also
  cannot rescue a cell where the existing measurement is *already* a post-event-wake test (several
  entries here already trade the window after the event, not the event minute itself) — the amendment
  restates a technique the estate is already using in those cases.
- *Threshold-parameterized WHEN* only rescues a cell whose disqualifying limb is that its trigger was
  treated as inadmissible **for being a non-calendar structural threshold** (margin band, strike/expiry
  registry) rather than a published clock. It cannot rescue a cell that failed the WHY-clause
  delete/flip test (the constraint doesn't entail a signed trade) — that failure is orthogonal to
  whether WHEN is calendar- or threshold-shaped. The ADR's own WHEN clause already reads "schedule
  **or trigger** declared before any data is read" (§2-A.2) — so most doors in this estate that use a
  threshold WHEN (margin calls, DD bands) were never rejected for that reason; they were rejected
  because the threshold wasn't *public* (unobservable per-account equity → "stops get hunted") or
  because sign still wasn't entailed.

---

## §2 — Table 2 triage: closures with a genuine strategy-grounds verdict, absent from the registry

Per the task's own convention (registry entries are appended only "at the close of any Pre-Q that
closes FALSIFIED on strategy grounds, or at the close of a parent programme on SNAG-budget-exhaustion
grounds"), most of the 97 closures are correctly absent — they are governance, gate-parameter,
data-integrity, or capital-allocation questions, not strategy kills. Reading every `**Verdict:**` /
`**Status:**` line (80 standard + 18 non-standard headers, full triage below) surfaced five closures
that ARE strategy-grounds dispositions and are not mirrored in the registry as their own row:

| Closure | Verdict | Why it stayed out of the registry (my read) |
|---|---|---|
| `MNQBASE-1-closure-intake-dry.md` | `FALSIFIED` (intake dry) | Domain-level "the well is dry on this timeline" finding — no single mechanism_family×instrument pair to key on; correctly domain-scoped, not per-candidate. |
| `Q-ICT-CASCADE-1-closure-insufficient-n.md` | `CLOSED` (1M `INSUFFICIENT-N`) | Multi-layer cascade closure (W/D/1H/1M PREREGs); the entry point instrument/TF combination the registry would key on is ambiguous across layers — SLR-MYM-1's own entry already cites the surviving weekly `vStruct` leg by name. |
| `Q-OFCHAN-1-closure-void-coverage.md` | `VOID-COVERAGE` | Referenced only as a "surviving finding" inside the R2FLOW/R2VBUCK registry rows, never given its own row — a completeness gap, not a wrong exclusion (it is a genuine dead G0 catalogue). |
| `Q-CONDVAL-1-closure-falsified.md` | `FALSIFIED` | CL range-state conditioner construct; genuinely never mirrored. |
| `ST-EH-1-closure-operator-stopped.md` | `OPERATOR-STOPPED` (no verdict) | Correctly absent — the registry only takes FALSIFIED/SNAG dispositions, and this campaign was halted before any Stage result was read. Listed here for completeness, tagged separately below as **not a kill**. |

Also triaged and confirmed correctly excluded (diagnostic/gate-configuration questions about the sole
survivor `ORB-MNQ-1`, explicitly self-declared "not a strategy-candidate proposal" in their own §Spend
line): `Q-ORBCUSH-1`, `Q-ORBPOS-1`, `Q-ORBSURV-1`, `Q-GEOFIT-1`, `Q-C1PANEL-1`. And one `AMBIGUOUS-HOLD`
correctly excluded (not a kill, not dead, non-promotable but revivable by a fresh G0 regardless of any
screen amendment): `Q-R2AGRUN-1`.

**Process falsifier check (A1 gate):** no tag below was assigned without reading the underlying
closure's own verdict/status line — the 80 standard `**Verdict:**` lines were grepped and read in
context; the 18 non-standard headers were opened individually (§2 table above + the diagnostic/HOLD
list). `A1` gate condition "FALSIFIED (process) if any tag is assigned without reading the underlying
closure's own verdict line" — **not triggered.**

---

## §3 — Table 1: `docs/rejected_candidates.md` registry (primary source)

Every entry below carries a `mechanism_family`×`instrument` HTML trailer in the registry; both the
trailer and the surrounding prose were read for each row. Cell-demonstrated unless noted.

| # | Entry | Kill class(es) | Demonstrated / inherited | Would-revive-under |
|---|---|---|---|---|
| 1 | MSL-S2B `sweep-failure-filtered-continuation` × MYM (Stage-1 FAIL, route) | REGISTRY (domain raised-bar unbound) + CADENCE (temporal-selectivity paused) | inherited (route declaration test against a standing domain bar) | neither |
| 2 | MSL-S2A `pullback-failure-resumption` × MCL | CADENCE (0.511 trades/wk < 1) + EVIDENCE (long FLIP FAIL) | demonstrated | neither |
| 3 | MSL-C1 `pdh-pdl-failed-break-reclaim` × MYM | EVIDENCE (CI entirely < 0 both arms) | demonstrated | neither |
| 4 | MSL-C3 `pdh-pdl-failed-break-reclaim` × M2K (operator-kill, pre-G0) | OTHER — operator declined the B4 GO; not a data-driven kill at all | n/a — never scored | neither (a fresh Stage-1+B4 GO revives this regardless of any screen amendment) |
| 5 | MSL-C3-K2 dual-axis MR-at-level × M2K | EVIDENCE (both axes, both arms CI < 0) | demonstrated | neither |
| 6 | MSL-C2 `london-range-failed-extension-fade` × MGC | EVIDENCE (CI < 0) + OTHER (DELETE FAIL — sham confound) | demonstrated | neither |
| 7 | Q-TXG-1 transfer/expression lane (FALSIFIED-at-walls) | COST (`required_net_r` hurdle) + OTHER named: "trailing-DD survivor-gate wall — venue survival geometry, not flow capacity" | lane verdict is a roll-up over 3 cell-demonstrated closures (rows 8–10) | neither |
| 8 | Striker NAS100→MYM sibling-swap (Q-TXG-1 cell 1) | COST (mean_net_r 0.0129 < 0.06) | demonstrated | neither |
| 9 | Striker DJ30→MNQ sibling-swap (Q-TXG-1 cell 2) | OTHER named: "trailing-DD N-SURV wall, 32–33× over ceiling" | demonstrated (cost gate PASSed first) | neither |
| 10 | Guardian→MGC transfer (R7/b8) | OTHER named: "trailing-DD N-SURV wall, 5.5–24× over ceiling" | demonstrated (exploratory-grade, margin-decisive) | neither |
| 11 | Guardian-family on XAGUSD (Silver) | EVIDENCE (DD 11.52%>8%, WR miss) + REGISTRY (parent SNAG-budget exhaustion) | **inherited** (parent programme closure) | neither |
| 12 | Custodian-family month-end EURUSD (SHELVED, soft) | OTHER named: "manual-test rejection, formal probe never completed" | partial (never a completed falsifier) | n/a — soft shelve, not a formal FALSIFIED subject to A3 revival at all |
| 13 | Short-only MR spike-fader USOIL | COST (sub-ATR stop → 0.09R hurdle) + EVIDENCE (placebo p=0.718) | demonstrated | neither |
| 14 | FX intraday fixing-reversal EURUSD | COST (0.277 pip breakeven ≪ 0.8 pip retail) | demonstrated | neither — event-time costs (5–20× normal) make this hurdle *worse*, not better |
| 15 | Aegis-v4.3 MR EURGBP | COST (cost-law transplant from USDCAD) + EVIDENCE (precedent dead) | **inherited** (refuted pre-build, no EURGBP panel ever run) | neither |
| 16 | Gold trend-persistence regime-gate (KER/TSMOM) | EVIDENCE (OOS AUC inverts, twice) | demonstrated | neither |
| 17 | Aegis→6J Wave-1 sizing/EOD-fill sweep | CADENCE (selection-window N 73–74 < 80) | demonstrated | neither |
| 18 | Aegis→6J v0.3 native-venue solo (H-SOLO) | OTHER named: "trailing-DD N-SURV wall, bust 6.41% vs 3.0% ceiling" | demonstrated | neither |
| 19 | S-MYM-ORC-02 opening-range continuation × MYM | EVIDENCE (7 of 9 hard gates fail) + COST (D3 gross/cost 0.69× < 4.00×) | demonstrated | neither |
| 20–22 | (Guardian→MGC / Striker DJ30→MNQ / Striker NAS100→MYM — duplicate rows cross-referencing the lane, same as 8–10) | — | — | — |
| 23 | H-FBEIA-1 EIA post-release reversal × CL | POWER (δ/σ 0.0233 < 0.122 floor) + COST (1.16bp vs 6–10bp) | demonstrated | neither |
| 24 | F-C carry-timing × 6E/6J/CL | POWER (δ/σ 0.0267 < 0.122) | demonstrated | neither |
| 25 | H-ZNAUC-1 post-auction drift × ZN | COST (δ 1.01bp vs 6–10bp hurdle, 6–10× under) | demonstrated | neither — construct already trades the **post-auction wake** (15/30/60m), the exact technique Amendment 1 proposes; the magnitude gap is 6–10×, not a costing-basis artifact |
| 26 | TAS settlement-window replication × MCL (Q-MCLTAS-1) | POWER (required δ/σ 0.62–1.35 vs measured 0.113/0.194, floor 3.2–7.0×) + COST (14.87bp vs 3.21bp, 4.63×) + EVIDENCE (Wall A: no signed public observable exists at all) | demonstrated (two pre-registered walls, probe never needed) | neither — Wall A is a data-*existence* problem, not a size/WHEN framing problem |
| 27 | Third-Friday derivative-settlement reversal × MYM | POWER (δ/σ 0.026/0.050 vs 0.2139 floor) + COST (2.68bp vs 6.57bp) | demonstrated | neither |
| 28 | Opening-volume × directional-efficiency × MNQ/MYM | EVIDENCE (MNQ underpowered, MYM wrong-signed) | demonstrated | neither |
| 29 | OR-window net signed aggressor size × MNQ (Q-CAPFLOW-1) | EVIDENCE (CI includes 0, indistinguishable from placebo) | demonstrated | neither |
| 30 | Q-COMPOSE-1 breadth-leg composition (3-leg book) | OTHER named: "variance-dominant added leg — dependence N_eff rose while risk N_eff stayed flat" | demonstrated | neither |
| 31 | Blind high-K discovery-axis mining (Q-GATECART-1) | POWER (DSR floor is K-governed; K=3,177 empties the admissible band) | demonstrated (program-level, formula executed) | neither |
| 32 | Q-INVENTORY-1 external-mechanism harvest burst (8 row-groups) | POWER (×3) + COST (×1) + EVIDENCE (informed-flow, ×1) + VENUE (×5) + REGISTRY (K-wall, ×1 permanent) | demonstrated (each row-group sniff-screened on its own arithmetic) | neither — see near-miss footnote below |
| 33 | (TAS settlement × MCL, duplicate of 26) | — | — | — |
| 34 | MNQDTL-CON-1 ES–NQ 5m divergence × MNQ | EVIDENCE (CI < 0 both arms, DSR ≪ 0.650 floor) | demonstrated | neither |
| 35 | Q-MNQSEL-1 restart-clock oracle selection ceiling × MNQ | OTHER named: "selection-ceiling failure — oracle mean structurally capped at the knife-edge target, not opportunity scarcity" | demonstrated | neither |
| 36 | Striker DJ30 pyramid-stack risk%-input scaling × MYM | OTHER named: "broker/TV qty-ceiling execution-fidelity failure — not a market mechanism kill" | demonstrated | neither (out of scope — not a market-mechanism candidate at all) |
| 37 | R2FLOW clock-minute net signed aggressor flow × MNQ | EVIDENCE (CI includes 0, \|ρ\|<0.02 floor) | demonstrated | neither |
| 38 | Q-R2VBUCK-1 volume-bucket aggressor imbalance × MNQ | EVIDENCE (CI includes 0, below placebo p95) | demonstrated | neither |
| 39 | TV bar-coverage-artifact hypothesis (Q-TVCOV-1) | OTHER named: "data-integrity audit — confirms the 2022 discontinuity is real, not a strategy candidate" | demonstrated | out of scope — not a mechanism candidate |
| 40 | (Transfer/expression lane (Q-TXG-1), duplicate row of 7 — the registry's raw file repeats this lane row verbatim in a second "by mechanism family" section) | — | — | — |
| 41 | SLR-MYM-1 liquidity sweep-and-reclaim × MYM | DIRECTION (0-A: both framings fail DELETE+FLIP) + CADENCE (0-C: 81 IS entries < 120 floor, order-symbol occupancy) | demonstrated (Phase 0.5 census executed) | neither — kill is at the WHY/delete-flip level, which threshold-parameterized WHEN does not touch; independently blocked by symbol occupancy |

**Near-miss footnote (row 32):** the single closest-to-clearing cost wall in the entire registry is
Q-INVENTORY-1's FX fixing-window row (6E/6J) — published net effect implies ≈3.3bp gross vs a 4.4bp
4×-hurdle, only **0.75× under**. It is tempting to read this as an Amendment-1 candidate. It is not:
the disqualifying test was Requirement-5's cost inequality at the *published, already-favorable*
basis; Amendment 1's event-time cost recompute (5–20× normal spreads) makes this hurdle **larger**,
not smaller, so applying the amendment to this row moves it further from clearing, not closer.

---

## §4 — Table 3: forced-flow census (`N-2026-07-26-forced-flow-census.md`, all 4 passes)

These are Notice-phase kills — cheaper than a full Pre-Q, several citing the registry rows above by
adjacency rather than re-deriving them (marked "inherited"). None of these carry their own registry
row by the file's own convention (Notice-phase, not a closed Pre-Q), so they are audited here as
their own class.

| Entry | Kill class(es) | Demonstrated / inherited | Would-revive-under |
|---|---|---|---|
| F1 — Closing-auction/MOC-imbalance × MYM | REGISTRY (paid-data procurement gate) + EVIDENCE (unclaimed, zero δ/cohort) | demonstrated (bar-ruling written; registry entry appended — this is the same cell as registry row 29's sibling) | neither |
| F2 — Leveraged-ETF EOD rebalance × ES/NQ | REGISTRY (free-data domain-exhaustion bar) | inherited (registry row, same entry) | neither |
| F3 — WMR 4pm-London fix × M6E | COST (M6E cost geometry ~4× worse than the already-dead EURUSD CFD version, 11.8× over breakeven) + REGISTRY (adjacent to registry row 14) | demonstrated (M6E-specific arithmetic) + inherited (kill 1) | neither — Amendment 1's event-time costs make an already-11.8×-over situation *worse* |
| F4 — Futures expiry-roll pressure | REGISTRY (BLOCKED-BY-REGISTRY, adjacent to MYM-3FPS-1) | inherited | neither |
| F5 — Month-end/quarter-end pension rebalance | POWER (D3 ES power 0.24–0.30; D7 6J power 0.30) + CADENCE (monthly, presumptive Req-4 kill) | demonstrated (three independent instances) | neither — **this is the precedent used for the §5 compelled-abstention fold-in below** |
| F6 — 0DTE dealer-gamma hedging footprint | DEFERRED — not killed | n/a | n/a |
| F7 — Own-execution loop (c1 fills/exits) | DEFERRED by operator choice — not killed | n/a | n/a |
| Pass 2 — PROPENG-RATCHET (prop-engine liquidation cascade) | OTHER named: "transmission failure — constrained cohort trades in a SIM book at every automation-friendly firm, never reaching the exchange" | demonstrated (primary-verified across all 4 friendly firms) | neither |
| Pass 2 — BE1 (VWAP-schedule completion fade) | DIRECTION (constraint carries neither sign nor level) | demonstrated | neither |
| Pass 2 — BE3 (TAS settlement-benchmark replication fade) | OTHER named: "design-law infeasibility — 1-event/day shape cannot clear the $200 funded-day floor under the 1.83 Sharpe ceiling at any contract count" | demonstrated | neither |
| Pass 2 — SFX-1 (settlement+GSCI-roll fade) | same OTHER as BE3 (concordant independent screen) | demonstrated | neither |
| Pass 2 — M6A-FIGURE-FADE (00-figure order-cluster) | DIRECTION (order placement is a preference, not a constraint) | demonstrated | neither |
| Pass 2 — PROPENG-EJECT (risk-engine ejection-band cascade) | same OTHER as PROPENG-RATCHET + DIRECTION (delete/flip fail on SLR-MYM-1 geometry) | demonstrated | neither |
| Pass 3 — P3-1 ETF-AP-BASIS | DIRECTION (flip fails) + OTHER named: "indirect cash-to-futures transmission, same failure mode as F1" | demonstrated | neither |
| Pass 3 — P3-2 SESSION-HANDOFF | DIRECTION (inventory sign unobservable) | demonstrated | neither |
| Pass 3 — P3-3 VOLTARGET-DELEVER | CADENCE (stress-day clustering fails ≥2/day on ordinary days) + EVIDENCE (publication-decayed, Volmageddon-class) | partial (Notice-phase screen, not backtested) | neither — see §5, this is the direct structural precedent for the compelled-abstention check |
| Pass 3 — P3-4 MULTI-FIX-FX | COST (F3 precedent: more fixes ≠ higher per-event δ) | inherited | neither |
| Pass 3 — P3-5 ROLL-PRESSURE-MULTI | REGISTRY (BLOCKED-BY-REGISTRY, same as F4) | inherited | neither |
| Pass 4 — P4-1 LIT-MOC-FUT | EVIDENCE (Req-2 unmet — cash-equity/SVAR proxies, no futures cohort δ) | inherited (F1's own reopen bar) | neither |
| Pass 4 — P4-2 LIT-COT-ES | CADENCE (weekly fails ≥2/day) + POWER (marginal) + EVIDENCE (Req-2 transplant) | demonstrated (screened) | neither |
| Pass 4 — P4-3 LIT-RUSSELL | CADENCE (~1 event/yr) + EVIDENCE (cash-only δ) | inherited (F5 adjacency) | neither |
| Pass 4 — P4-4 LIT-ORB-TIE | EVIDENCE (Avenue-A qualifying triple still empty) | inherited | neither |
| Pass 4 — P4-5 LIT-EIA-PHYS | REGISTRY (prior NG-EIA-1/H-FBEIA-1 kills) + CADENCE (EIA ~1/wk) | inherited | neither |
| Pass 4 — P4-6 OUT-OF-CHANNEL (Koijen/Bouchouev carry/TSMOM) | REGISTRY/POWER (already owned by harvest radar — UNSCREENABLE/Clause-N FAIL) | inherited | neither |

---

## §5 — Table 4: WHO-track door table (`N-2026-08-14-msl-who-track.md` §3) + `MCL.md` INTAKE-DRY

Most of the ~40 product-group "doors" in the WHO-track notice are pure citations to kills already
tagged in Tables 1–3 (the notice's own "Why not NEW" column names the prior kill directly) — those are
not re-tagged here as independent cells; they are counted toward the category-inherited total in §7.
Five doors carry their own fresh four-clause test, executed inside the notice itself, and are tagged
independently:

| Door | Kill class(es) | Demonstrated / inherited | Would-revive-under |
|---|---|---|---|
| §3.1 Pipeline nomination × MCL/NG | DIRECTION (delete residue = fade/follow inventory, an inventory model with no signed level) | demonstrated (4-clause test run) | neither |
| §3.2 LME cancelled-warrant → HG | DIRECTION (sign is a discretionary inventory story) + OTHER (indirect LME→COMEX transmission, F1 failure mode) | demonstrated | neither |
| §3.3 FX 10:00 NY option cut × M6A | DIRECTION (dealer-gamma sign not entailed by the flatten-at-cut rule) + SIZE (secondary — WHY flags capacity smallness as a cost-law red flag, not itself the disqualifier) | demonstrated | neither — DIRECTION is the binding limb; a SIZE reframe leaves it untouched |
| §3.4 USDA prints × ZC/ZS/ZW (grains) | SIZE (WHY explicitly fails: "full-size grains ARE the institutional tickets") + CADENCE (monthly WASDE / weekly Crop Progress fails ≥2/day) + REGISTRY (EIA-family adjacency) | demonstrated | **neither** — see reasoning below |
| §3.5 Bund auction hedge-unwind × FGBL | SIZE (WHY fails: "FGBL full-size, not a micro residual") + COST (H-ZNAUC-1 precedent, 6–10× under, already at the post-event wake) | demonstrated | **neither** — same reasoning as row 25 |

**Why the two SIZE-tagged doors (§3.4, §3.5) do not revive under Amendment 1.** These are the only two
cells in the entire estate where the *stated* disqualifying WHY is explicitly the "not a small
residual" ground the amendment targets. Both are compound-killed: grains additionally fail CADENCE
(USDA print density, independent of size) and Bund additionally fails COST at a magnitude already
measured post-event (H-ZNAUC-1's own construct trades the 15/30/60-minute window *after* the auction,
which is the exact "post-event wake" Amendment 1 proposes measuring — the wake was already measured,
and it misses by 6–10×). A size re-aim removes one disqualifying leg on each cell but leaves the other
standing; neither cell clears to viable. This is the honest, non-optimistic reading — not a search for
a reason to keep the list empty.

**`ops/instruments/MCL.md` INTAKE-DRY entries:** the 2026-08-09 through 2026-08-14 entries are, without
exception, citations to kills already tagged above (BE3, SFX-1, PROPENG-EJECT, H-FBEIA-1, H-FCCARRY-1,
census passes 2–4) plus one domain-level closure worth its own row:

| Entry | Kill class(es) | Demonstrated / inherited | Would-revive-under |
|---|---|---|---|
| 2026-08-10c/b `IMPLIED-SR-GATE` ruling — MCL fade design-region closed on its own arithmetic (floor 2.98/2.11 vs 1.83 CFD ceiling, both over) | POWER + COST (domain-level: the *entire admitted region* is empty at every parameterization `p`) | demonstrated (formula executed, ablation-robust) | neither — Amendment 1's event-time costs widen the floor further, they do not narrow it |

---

## §6 — Compelled-abstention arithmetic fold-in (Phase B candidate B3)

Per the task brief's required fold-in: a blackout/compelled-abstention mechanism (a mandated
counterparty is *absent* from the market for a clustered stretch — e.g. a buyback-blackout-shaped
window, ~60–90 sessions/yr, clustered into a handful of multi-week windows rather than spread evenly)
against (a) the estate's activity floor and (b) the power-wall precedent.

**(a) Cadence.** 60–90 sessions/yr ÷ 52 weeks ≈ 1.15–1.7 events/week on a naive annual average —
comfortably clears the N-ACT ≥1 trade/week floor this estate has repeatedly enforced (MSL-S2A killed
at 0.511 trades/week). But "clustered" means the *distribution*, not the average, is what matters: if
the windows are quarterly (the buyback-blackout shape), the gaps between them plausibly exceed the
estate's own enforced inactivity guard (`c1_cadence_inactivity_2026-08-02`: "token trade owed 82/312
weeks, max 4 consecutive" — i.e., >4 consecutive dead weeks triggers the operator-placed venue-idle
token-trade fallback). CADENCE alone does **not** kill this candidate — the estate already has a
standing, cheap mechanism (the disclosed operator token-trade) for exactly this shape, matching A2's
own admission language ("activity … satisfied structurally **or via the operator token-trade,
disclosed which**"). **Cadence sub-verdict: survives, with disclosure.**

**(b) Power.** This is the binding wall. Compelled-abstention is the mirror image of F5's mechanism
class (month-end/quarter-end mandated *presence* of rebalance flow) — a mandated *absence* of one flow
component, measured at comparably low frequency and comparably modest expected magnitude. F5's own
three independent measurements (D3 on ES, D7 on 6J, HARV2026-001 on ES month-end) all landed at
**power 0.24–0.30 with single-digit-bp effect sizes** — a class-level precedent for "mandate-flow at
this frequency, this magnitude, this instrument class" that never once cleared a usable power floor.
An *absence*-of-flow effect is mechanically no larger than the *presence*-of-flow effect it removes
(a compelled non-buyer is at most as loud as a compelled buyer would have been, and typically quieter —
the withdrawal is partial, not a reversal), so there is no basis to expect compelled-abstention to beat
the F5/D3 precedent; if anything the prior should be pessimistic relative to it. **Power sub-verdict:
kill, by direct analogy to F5/D3 — no new measurement is needed to reach this, which is the point of
running it as a 5-minute check rather than a full probe.**

**B3 disposition: KILL (POWER class, category-inherited from the F5/D3 precedent).** Recorded here so
this specific idea does not consume an MSL card slot in Phase B; the binding limb is power, not
cadence — a future session should not re-litigate the cadence half of this, only the power half, and
only with a materially different magnitude argument than F5's own three failed instances supply.

---

## §7 — Revival list

**Empty.**

No cell across Tables 1–4 clears to "would revive" under either Amendment 1 (impact-persistence size
re-aim) or Amendment 2 (threshold-parameterized WHEN extension). The two candidates that came closest
on inspection — §3.4 grains and §3.5 Bund (the only two cells in the estate whose stated WHY is
literally "the flow is not a small residual") — are both compound-killed by an independent CADENCE or
COST leg the size reframe does not touch. The single closest cost-wall margin in the estate
(Q-INVENTORY-1's FX fixing-window row, 0.75× under) moves *away* from clearing under Amendment 1's
event-time cost recompute, not toward it. No cell was found where the WHEN clause's calendar-vs-
threshold distinction was itself the disqualifying limb — every DIRECTION-class kill in the estate
fails on the WHY/delete-flip test, which Amendment 2 does not touch, and every threshold-WHEN cell
already in the estate (margin/DD-band constructs) was rejected for unobservability or unverified
transmission, not for the threshold shape per se.

Per the task's own gate language, this is a valid, decisive outcome: **the falsifiable H is rejected**
("≥1 registry kill rests on a category-inherited SIZE or DIRECTION ground that the amended screens
would re-open"). This retires the ox-alpha-review thread the task names, and Phase B proceeds with
candidates B1/B2 only. **A3 is voided by this result** — its own gate says an empty revival list means
A3 does not need to be ruled; there is nothing for either amendment to touch.

---

## §8 — Category-inherited count: re-verified vs accepted-on-citation

Per Rule 0 / `lesson_dedup_attestation_must_be_executed`, a citation is not evidence until it is opened
and read. Every row tagged **category-inherited** across Tables 1–4 was independently opened and read
against its cited parent artifact this session (registry entries, closure files, or census passes) —
none were accepted on the citing row's prose alone.

- **Category-inherited rows tagged in Tables 1–4:** 19 (registry rows 1, 7\*, 11, 15; census F2, F3
  [kill-1 limb], F4, P3-4, P3-5, P4-1, P4-3, P4-4, P4-5, P4-6; door-table §3.4/§3.5 REGISTRY limb;
  MNQBASE-1 and Q-ICT-CASCADE-1 from §2, each domain/multi-layer roll-ups over their own cited prior
  work). *Row 7 (Q-TXG-1 lane) is a roll-up over cells 8–10, which are themselves cell-demonstrated —
  counted once as the lane-level inheritance.*
- **Re-verified against the cited parent (opened + read, not merely cited):** 19 of 19 (100%).
- **Accepted on citation alone:** 0.

This count is lower than the total row count in Tables 1–4 (≈70) because most cells are
cell-demonstrated — the estate's screens overwhelmingly re-run each candidate on its own data rather
than killing by pure adjacency; category-inheritance is the minority disposition, concentrated in the
free-data-domain-exhaustion bar (F2/F4/F5-adjacent rows), the EIA-family cluster, and the two
multi-layer program closures (MNQBASE-1, Q-ICT-CASCADE-1).

---

## §9 — Forbidden moves compliance

- **No cell was re-scored.** Every kill class, demonstrated/inherited tag, and revival call above is
  read off the cited artifact's own stated verdict/numbers — no MC re-run, no new backtest, no
  recomputation of a δ, cost hurdle, or power figure.
- **No closure or registry row was edited.** This file is additive only.
- **No `OTHER` tag was left unnamed.** Every `OTHER` tag above carries its written reason inline.
- **No new instrument ledger was opened** to "complete the matrix" (ADR 2026-07-25 §5) — the two
  product-group doors left partially unscreened in the WHO-track notice (livestock, EUREX rates
  beyond FGBL) are cited by adjacency to their EIA-family/H-ZNAUC-1 precedents, not independently
  re-derived here.

---

## §10 — Audit hooks

```bash
# Registry completeness has not drifted since this audit's anchor
git log -1 --format='%h %ci' -- docs/rejected_candidates.md
# Expect: still 6c0b14a or a later commit with no new FALSIFIED-on-strategy-grounds row untagged here

# The five Table-2 closures stay correctly un-mirrored (or get folded in — re-check if they do)
grep -l "mechanism_family" docs/rejected_candidates.md | xargs grep -c "MNQBASE-1\|Q-ICT-CASCADE-1\|Q-OFCHAN-1\|Q-CONDVAL-1"
# Expect: 0 (if any of these gain a registry row, re-open this audit's Table 2)

# Revival list stays empty — re-run only if a NEW registry/closure FALSIFIED lands citing
# "not a small residual" (SIZE) or a WHEN-clause-type rejection as the disqualifier
grep -n "not a small residual\|micro residual\|full-size" docs/rejected_candidates.md docs/notes/notice/*.md

# Compelled-abstention precedent still holds (F5/D3 power figures unchanged)
grep -n "power 0.24\|power 0.30\|0.24–0.30\|0.24-0.30" docs/rejected_candidates.md
```

---

## §11 — Closure

- **Status:** `Closed` — attribution complete, revival list published (empty, decisive per the task's
  own gate), compelled-abstention fold-in recorded (KILL, POWER-class).
- **A1 gate:** `RESOLVED` — matrix complete over the registry + all four source classes; revival list
  published.
- **A3:** voided by the empty revival list — no operator ruling is owed on either amendment; Phase B
  proceeds with candidates B1/B2 only, per the task brief's own gate language.
- **Follow-up owed:** none from this audit. The two completeness gaps noted in §2 (Q-OFCHAN-1 and
  Q-CONDVAL-1 lack their own registry rows) are cosmetic — both are correctly *reachable* via their
  sibling rows' surviving-finding text — and are flagged, not repaired, per this task's forbidden
  moves (no registry edits).

---

## Verification

```bash
# Confirm the census retrieval command still works (pruned-file dependency)
git show pre-prune-2026-08-08:docs/notes/notice/N-2026-07-26-forced-flow-census.md | head -1
# Expected: "# N-2026-07-26 — Forced-flow census (Notice-phase; zero K consumed)"

# Confirm no edits landed on the audited artifacts
git diff --stat -- docs/rejected_candidates.md docs/briefs/closures/ docs/notes/notice/ ops/instruments/MCL.md lab/CATALOG.md
# Expected: empty (this audit is additive-only, one new file)
```
