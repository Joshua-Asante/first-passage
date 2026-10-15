# ADR 2026-08-13 — `implied_annualized_sr` demoted to report-only; fade design-region reopened

**D-S-A domain:** meta-process (doctrine — freeze-time admission limb; no data-corpus or system-artifact D/S/A rides this)
**Loop-of-Record:** STRATEGIC — gate-severity doctrine; operator-directed reversal of a 2026-08-10 limb-4 ruling.

**Status:** `Accepted` — operator ruling 2026-08-13. Ruling ID **`IMPLIED-SR-REPORT-ONLY-2026-08-13`**.
**Decision date:** 2026-08-13
**Authors:** Joshua (ruling) + Cursor (recorder)
**Supersedes:** `2026-08-10-implied-sr-plausibility-gate.md` full
**Supersedes:** `2026-08-12-msl-implied-sr-disclosure-not-kill.md` full — interim MSL-only kill-list amend absorbed by this estate-wide demotion
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Revision:** 2026-10-15 — retention trim (ADR decay audit; operator direction 2026-10-15): §0 read detail (one decisive read kept), the §6 downstream-artifact list, §7 implementation, §10 hooks other than the charter and preflight checks (the predecessor-stub and archived-slate hooks no longer apply), and the Verification block removed; the §6 Gate line notes the predecessor's removal and the Related line's dead frozen-rulings link is pinned to the archive. No decision text changed. Pre-trim text at blob `fef84c4acf7ca0aa0a55d51bfe8c7789e0d3f9c2` (commit `4121e84c95f4990b71962e3b9570c4c3fad88426`).
**Related:** [predecessor + interim MSL-only ADR (removed)](TOMBSTONES.md#2026-10-15-adr-decay-audit-removals) · [frozen rulings + Finding 2026-07-31b](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/docs/notes/2026-07-31-fade-stage1-frozen-rulings.md) · [MSL charter](../spec/2026-08-12-msl-manual-sourcing-loop-charter.md) · [ceremony tiering](2026-08-08-adr-ceremony-tiering.md) (full record — limb 4 fires: amends a gate)
**Layer:** research-doctrine. **$0 / K=0.** No `core/`, Pine, allocation, `dd_protection`, rail, or K ledger is touched; nothing armed; no mechanism admitted.

---

## §0 — Rule 0 reads (production-source verification)

Read before authoring, this session (2026-08-13), with `git log -1 --format='%h %cs'` anchors at `a2f57674`:

- `docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md` — anchor `c0d20bd0` 2026-08-12. Step 3 wires implied-SR > **1.83** as a **pre-G0 FAIL** on every MSL card. That is the live kill on new strategy candidates.
- The other reads (the predecessor ADR, `msl_preflight.py`, the fade RESULTS, the frozen rulings, the MSL slate, `MCL.md`) and the $0 cheap falsifier are at the pre-trim blob (see **Revision:**).

---

## §1 — Context

The 2026-08-10 ADR promoted `implied_annualized_sr` from a reported column to a freeze-time admission limb: any assumed-edge (p, rr, n) cell whose implied annualized Sharpe exceeded the Aegis CFD-era cohort **1.83** was inadmissible. That emptied the Tradeify-native fade region (floor **2.98** as-ruled, **2.11** after ablating elective limbs). The same limb was then wired into the MSL charter as a pre-G0 FAIL, so a new card whose designed geometry implied SR > 1.83 died before measurement.

The predecessor's own scope boundary is the load-bearing remainder: the gate bound **assumed-edge design regions**; **measured** results already gate on DSR-at-K. Using 1.83 as a kill — on freeze-time cells or on new candidates — punishes a design for implying (or later measuring) a Sharpe above the estate's historical best. That is not a selection correction; DSR-at-K is.

**Decision driver (one sentence):** the operator will not let an SR over 1.83 kill new strategy candidates, and the fade cells closed solely by that limb are reinstated.

---

## §2 — Decision

**Decision:** `implied_annualized_sr` is **report-only**. A Sharpe above the Aegis 1.83 cohort is not a FAIL. Specifically:

1. **Demote the limb.** Any assumed-edge feasible-region screen (fade-class design law, MSL step 3, or successor) **states** `implied_annualized_sr = per_trade_sharpe(p, rr) × √(n·252)` at freeze time. It does **not** admit or reject on that number. The Aegis **1.83** (CFD-era) and futures-native **≈0.89** figures remain **cohort disclosures** beside the print, not ceilings.
2. **Reopen the fade design-region.** The Tradeify-native fade admitted region (4× · `CONFIG-B-MCL` · rr∈{0.66, 1.0}) is **OPEN** again as geometry. Frozen Rulings 1–4 stand. The three MCL cells in RESULTS (n=4/5/6, still `feasible=True`) are reinstated. **No mechanism is admitted** — a feasible region is not an edge; Stage-2 / TNEC / DSR-at-K still require a pre-registered mechanism.
3. **Measured-edge boundary (kept, restated).** Measured results (Route B, TNEC intake, CON-*, MSL step 8 survivor MC) continue to gate on **DSR-at-K**. This ADR does not weaken DSR, cost-law, payability, worst-day, or harvest Req 1a. A measured SR above 1.83 is not a kill.

**Effective:** immediately upon acceptance.
**Scope:** freeze-time implied-SR admission and the 2026-08-10 fade-region close only.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Keep the 1.83 FAIL; apply it only to fade, not MSL | The operator's objection is the kill itself ("punishing a strategy for being too good"), not the MSL wiring. Leaving the fade close in place would ignore the reinstatement ask. |
| Raise the ceiling (e.g. to 2.98 or the portfolio-of-4 2.80) | Still a freeze-time Sharpe kill. The defect is using a historical-best as an admission ceiling, not the particular number. |
| In-part supersede (kill the FAIL, keep 2026-08-10 Accepted for the scope boundary) | After the FAIL dies, the predecessor's remaining content is the DSR-at-K boundary, which this ADR restates. A hollow Accepted ADR is a second owner. |
| Status quo | MSL step 3 currently FAILs new cards at implied SR > 1.83. That is the live harm. |

---

## §4 — Falsifier (revert trigger)

**H:** after this ADR, no candidate is killed solely because implied or measured annualized Sharpe exceeds 1.83; DSR-at-K and the three remaining $0 screens (cost-law, payability, worst-day) continue to bind; the fade region is treated as geometry-open, not as an admitted mechanism.

**H is falsified — and this decision reverts (superseding ADR, never an in-place edit) — if any limb fires:**

- **Kill-on-SR limb:** a candidate or fade cell is rejected with implied or measured SR > 1.83 as the sole stated reason.
- **DSR-skip limb:** a measured-edge campaign skips DSR-at-K citing this ADR.
- **Mechanism-launder limb:** a fade (or other) mechanism is treated as admitted solely because the design-region reopened.

**Revert action:** author a superseding ADR; never silently restore the 1.83 FAIL in the charter or slate.
**Trigger check schedule:** at each MSL pre-G0 screen and the next quarterly methodology audit.

---

## §5 — Forbidden moves (under this ADR)

- **Reading reopen as a fade mechanism GO** — Q-INVENTORY-1 and four subsequent sourcing passes staged zero admissible seeds; the region is geometry, not an edge. Ruled out because that is the laundering move the 2026-08-10 close was trying (wrong instrument) to prevent.
- **Reopening BE3 / SFX-1 / other registry kills** — those are mechanism-family deaths, not the design-region close. This ADR does not clear them.
- **Weakening DSR-at-K, cost-law 4×, payability, or worst-day** — those limbs are untouched. "High SR is allowed" is not "skip selection correction."
- **Silent in-place restoration of the 1.83 FAIL** in the MSL charter, slate kill lists, or a new screen — Trap #12. If the demotion is wrong, supersede this ADR.
- **Applying 1.83 as a FAIL to measured results** — the predecessor already forbade this; restated so a misread of "assumed-edge only" cannot be used to kill a measured SR.

---

## §6 — Consequences

**Positive:** freeze-time (p, rr, n) cells that imply SR > 1.83 remain admissible as geometry; MSL cards are not pre-killed for a designed Sharpe above Aegis; fade cells return to the pre-2026-08-10 feasible set; DSR-at-K stays the measured gate.

**Negative:** the 2026-08-10 "wish not a design" warning is now disclosure only — a region can again assume an SR nobody here has measured, and that assumption will not stop freeze. Cost is paid at scoring (DSR / TNEC / cheap falsifier), not at design-region admission.

**Risks:** a campaign manager treats reopen as mechanism admission (mitigation: §5 + MCL ACTIVE still "mechanism-owed"). A later screen re-introduces 1.83 as FAIL without superseding (mitigation: §10 grep).

**Gate:** RESOLVED when this ADR is Accepted, the predecessor is retired (stubbed 2026-08-13; removed 2026-10-15), and the MSL charter no longer FAILs on implied SR > 1.83. FALSIFIED per §4.

---

## §10 — Audit hooks (runnable)

```bash
# Charter must not FAIL on implied SR > 1.83
rg -n "implied-SR|> \*\*1\.83\*\*.*= FAIL" docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md
# Expected: disclosure wording; no "= FAIL" on the implied-SR line

# Formula pin still holds (report, not gate)
PYTHONPATH=lab python -c "from research_utils.msl_preflight import implied_annualized_sr; assert round(implied_annualized_sr(0.654, 0.66, 3), 2) == 2.98"

# Preflight still exits 0 on the fade-region fixture
PYTHONPATH=lab python -m research_utils.msl_preflight lab/research_utils/fixtures/msl_preflight/fade_region.yaml >/dev/null; echo $?
# Expected: 0
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-13 | Initial authoring; Accepted same session (operator-directed reversal) | Joshua (ruling) + Cursor (recorder) |
