# ADR 2026-07-10 — R6 NO-GO: the futures-prop residual program closes; self-funded Aegis→M6J is the sole active scale lane, Guardian-MGC parked

**Status:** Accepted (operator executive decision, recorded) — **superseded in part** 2026-07-16 (sole-active self-funded lane only)
**Superseded-by:** none
**Retain-until:** none
**Decision date:** 2026-07-10
**Authors:** Joshua (decision) + Claude Code (recorder)
**Supersedes:** none. **Closes** the futures-prop residual program (`docs/ltm/briefs/futures_residual_program_2026-07-05.md`) at its R6 gate; **refines** the scale-path posture that `docs/adr/2026-06-30-no-manual-trading-cfd-retirement.md` opened (futures as the scale lever) and that the 2026-07-06 P2 ratification demoted (`docs/adr/2026-07-03-hardcore-p2-edge-transfer-gate.md` Addendum).
**Superseded-in-part-by:** `2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md` - sole-active self-funded lane clause only.
**Superseded-in-part-by:** `2026-07-12-prop-portfolio-four-friendly-firms.md` - "no futures-prop operational target" posture replaced by the prop-portfolio program.
**Related:** residual-program R6 (operator-only GO/NO-GO); `docs/adr/2026-07-03-hardcore-{p1,p3,p4,p5}-*.md` (the two-sided gates whose live existence-bars this NO-GO makes dormant); companion addendum on `docs/adr/2026-06-30-no-manual-trading-cfd-retirement.md` (FXIFY formally closed); memories `project_futures_prop_pivot`, `project_dj30_mym_prototype_falsified`, `project_aegis_6j_transfer_state`, `project_us_legal_master_research`.
**Layer:** execution (live-trading venue + scale path) — **not** strategy/risk-control. No locked parameter, allocation, `dd_protection` constant, or Pine source is touched by this ADR.

---

## §0 — Rule 0 reads (production-source verification)

This is a venue/scale-path decision. It changes **no** risk-control code or locked parameter; the §0 reads exist to *prove* that and to anchor the falsification evidence that drives the NO-GO.

- `lab/archive/striker_dj30_mym_prototype_2026-07/RESULTS.md` — anchor `75041aa` (2026-07-10). The R5 B2-edition DJ30→MYM prototype: **Verdict Stage-1 NOT CLEARED**, **Disposition FALSIFIED (operator-accepted 2026-07-09)** — OOS PF ratio **0.559 < 0.8×** edge-preservation bar, miss attributed to *structural* venue costs (commission + slippage on 100+ contract stacks, EOD force-flat truncating trend-day holds, integer/RESERVE pyramid quantization) that the pre-registered free grid cannot touch. This is the residual-program §4 falsifier firing.
- `docs/adr/2026-07-03-hardcore-p2-edge-transfer-gate.md` — anchor `09c7097` (2026-07-06). P2 edge-transfer gate closed **FALSIFIED on the as-mapped CME-micro venue**: NAS100 dead on micros (K2 kill, ~3× the gate); DJ30 out as-scored, "conditionally alive only via the pre-registered R5 B2-edition successor." R5 is now run and falsified (line above), so the sole surviving prop contingency is spent.
- `docs/ltm/briefs/futures_residual_program_2026-07-05.md` — anchor `44a8aa7` (2026-07-05). §4 falsifier: "either R1 fails its ratified gates under the corrected model, or R5's B2 E1 lands < 0.8× — then the futures-prop rail closes **NO-GO for the locked book**." §2 R6: GO/NO-GO is operator-only; §1 standing frame (D14): futures-prop tracks are subordinate to the self-funded track, with the "smallest surviving prop candidate a DJ30-only MYM book at 150K, unconfirmed."
- `docs/adr/2026-06-30-no-manual-trading-cfd-retirement.md` — anchor `189aa96` (2026-07-02). Confirms the standing posture this refines: manual retired, CFD idle, "scale routes through CME-micro futures-prop." That routing is what R6 NO-GO now revises to self-funded-only.
- `core/config/params.toml` — anchor `784a9ab` (2026-06-24). Confirms the locked config this ADR does **not** touch: G 0.34% / DJ30 v4.5 0.70% (pyr 750%) / Aegis 1.50% / NAS100 v1 0.37% (pyr 1000%), `dd_protection` C2 1.5%/0.40×, MC anchor 99.83/0.17/4.37. Unchanged.
- `core/dd_protection.py` — anchor `ce9b69f` (2026-07-10); `core/firm_rules.py` — anchor `4777d9f` (2026-07-10). The live-sizing sources; no constant is touched by this ADR (the Bulenox firm config in `firm_rules.py` remains for provenance — it is no longer a live target).

---

## §1 — Context

The 2026-06-30 no-manual/CFD-retirement ADR routed scale through "CME-micro futures-prop." That pivot was demoted to Rank 2 on 2026-07-03 (behind the self-funded Guardian-MGC track) and its P2 edge-transfer premise closed FALSIFIED on 2026-07-06: NAS100 is dead on micros, and DJ30 survived only as a named contingency — the pre-registered R5 B2-edition MYM backtest, "the definitive powered E1 for DJ30."

That contingency has now been run. The R5 DJ30→MYM prototype was **FALSIFIED (operator-accepted 2026-07-09)**: OOS PF ratio 0.559 against a pre-registered 0.8× edge-preservation bar, with the miss attributed to structural venue costs the free grid cannot repair. The residual program's own §4 falsifier — "R5's B2 E1 lands < 0.8× → the futures-prop rail closes NO-GO for the locked book" — has fired. No prop leg clears at any accessible tier (P4's canonical futures-constrained C5 already showed no Bulenox tier passes both pinned gates; best 150K bust 8.74%).

**Decision driver (one sentence):** every futures-prop leg that could carry the locked book is now falsified or unviable (NAS100 dead on micros, DJ30→MYM falsified on structural cost, no C5 tier clears the gates), so the operator issues the residual program's R6 as **NO-GO** and the futures-prop fan-out closes.

---

## §2 — Decision

**R6 = NO-GO.** The futures-prop residual program is closed. Concretely:

1. **No futures-prop book is deployed.** The Bulenox (or any prop-firm) futures fan-out of the locked four-strategy portfolio is NO-GO. No Bulenox account is registered; no CrossTrade/NinjaTrader-8-via-Rithmic rail is built; no live automated prop execution is initiated. The `core/firm_rules.py` Bulenox config and the P0–P5 gate ADRs remain on record for provenance and for a future re-open under §4, not as live targets.
2. **The sole active scale lane is self-funded Aegis→M6J.** Per operator decision this session, the Aegis USDJPY→micro-JPY-futures (M6J) transfer lane is the surviving active scale path (lineage: `project_aegis_6j_transfer_state`, v0.3 129 trades / +$39K / PF 2.318 / +0.218R ≈ 50% preservation — a self-funded futures book, not a prop fan-out). Its own go-live authorization is a separate operator decision; this ADR authorizes the *lane*, not a live start.
3. **Guardian-MGC (R7, the prior Rank-1 self-funded track) is PARKED.** The self-funded Guardian→micro-gold-futures track is parked, not killed — its R7 granularity-floor work was data-blocked (needs a real GC1!/MGC1! bar-export) and it is set down behind Aegis→M6J. Re-opening it is a fresh operator decision, not a re-run of R7 as-scoped.

**Effective:** immediately upon acceptance (2026-07-10).
**Scope:** the futures-prop scale path and the residual program's R1–R8 tracks. The four locked strategies, allocations, `dd_protection`, and Pine source are **untouched** (Rule 0) — this ADR changes *which venue/path* scales, not *what* is traded.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **GO-CONDITIONAL on a DJ30-only MYM 150K book** (the residual program's "smallest surviving prop candidate") | The one test that gated it — R5's B2 E1 — is the test that just failed (0.559 < 0.8×). A GO-CONDITIONAL would name the failed track as its own blocker, i.e. a NO-GO wearing a softer label. Deploying a below-preservation-but-profitable book is a *different* question needing its own pre-registered gate (`RESULTS.md` §"Separate, still-open") — not this program's edge-preservation gate, which answered no. |
| **Re-run R5 with an exit/cost grid to rescue DJ30→MYM** | Operator declined at the 2026-07-09 falsification: trail width (the only free lever) targets ~10% of the gap and cannot undo commission or the force-flat hold-cap. Re-running a spent one-shot on a shifted spec to manufacture a pass is the family's own forbidden move (P4 §5 trap-12). |
| **Attempt NAS100→MNQ / Guardian-MGC under the same exit-only constraint before deciding R6** | DJ30 was the *strongest* prop-rebuild candidate (base transferred at 0.85×); its falsification on structural venue costs is a strong prior the same cost wall hits the other legs (`RESULTS.md` §Program-note). Spending on them before a scale decision inverts the order; Guardian-MGC survives as a *parked* self-funded track, not a prop attempt. |
| **Keep the residual program open, undecided** | R6 is the program's closure artifact by design (residual brief §6). Leaving it open after its §4 falsifier fired is exactly the "HOLD that dies quietly" the family warns against — the honest move is to record the NO-GO and re-rank the surviving self-funded lanes. |
| **Kill Guardian-MGC outright rather than park** | Its R7 floor work was data-blocked, not adversely resolved — no evidence falsifies it. Killing it would discard a not-yet-tested track; parking preserves it behind Aegis→M6J at zero cost. |

---

## §4 — Falsifier (revert trigger)

This ADR accepts a real cost (§6): it closes the futures-prop scale path the 2026-06-30 pivot opened, leaving a single self-funded lane active.

**Revert trigger (binary, event-driven):** the futures-prop path re-opens **only** on **new mechanism evidence** that a locked leg transfers to a prop-micro venue with edge-preservation ≥ 0.8× under realistic (commission + slippage + force-flat) modeling — a *dated, pre-registered* result, not a re-run of any spent gate (P2 K2/E1 or R5 B2) on a shifted window. Absent that, the NO-GO holds. (This mirrors the `docs/rejected_candidates.md` re-proposal discipline: re-proposal requires new mechanism evidence, not new parameters.)

**Revert action:** supersede this ADR with a fresh one citing the new pre-registered edge-preservation result as the anchor; re-open R6 as a fresh operator GO/NO-GO. Never edit §2 or §4 in place.

**Trigger check schedule:** event-driven; reviewed at each quarterly programme audit / regime trigger — next **2026-08-08**, then 2026-11-08, 2027-02-08, 2027-05-08.

---

## §5 — Forbidden moves (under this ADR)

- **Re-running R5's DJ30→MYM E1 on a shifted exit/cost grid to overturn the NO-GO.** The one-shot is spent and operator-accepted FALSIFIED; the free lever cannot reach the gap. Re-opening requires §4's new-mechanism trigger, not a re-fit.
- **Relabeling the NO-GO as GO-CONDITIONAL on the DJ30-only book.** The gate that would have made it conditional is the gate that failed; a conditional-with-named-blocker where the blocker is the failed test is a NO-GO in disguise.
- **Standing up the CrossTrade/NinjaTrader-8-via-Rithmic rail "so it's ready."** The rail is dormant under NO-GO; building transport for a closed book is sunk effort and re-opens the automated-prop-execution surface this decision closes.
- **Treating Aegis→M6J's lane authorization as a live-start authorization.** This ADR authorizes the *lane* as the surviving scale path; the go-live is a separate operator decision with its own venue/parity checklist. "The lane is open so I'll start it" skips that gate.
- **Silently promoting Guardian-MGC back ahead of Aegis→M6J after the go-dark gets uncomfortable.** The re-rank is a recorded operator decision; changing it is a fresh operator decision, not a drift. The discomfort of a single-lane scale path is the cost this ADR names, not grounds to un-park.
- **Letting any futures re-mapping touch locked strategy parameters.** The Aegis→M6J sizing translation (spot %-risk → integer micro contracts) is validated with parity discipline; it is forbidden from changing any SL/TP/ATR/risk%/pyramid/session constant (Rule 0).

---

## §6 — Consequences

**Positive consequences:**
- Closes the futures-prop program at its designed decision point instead of leaving a falsified HOLD open; the R6 ADR the D-register noted "never existed" now exists.
- Narrows scale to one lane with real transfer numbers (Aegis→M6J ≈ 0.5× preservation, PF 2.318) rather than a fan-out where three of four legs are dead/unviable.
- Purely subtractive at the strategy layer: no parameter/allocation/`dd_protection`/Pine change, so the locked MC anchor (99.83/0.17/4.37) is untouched and needs no re-MC.
- Renders the P1/P3/P5 futures-prop *existence bars* dormant (no rail to build, no funded month to run), so the ~500 lines of not-yet-built rail/matrix/fixture work (P5-K matrix, golden-path fixtures, K1 primitive matrix) are correctly not started.

**Negative consequences (real cost):**
- **Forfeits the futures-prop scale path** the 2026-06-30 pivot was built to open — after real work (P0–P5 gates, C4/C5 re-MC, R5 prototype). The prop fan-out of the 99.83%-book is abandoned on structural venue economics.
- **A single-lane, go-dark scale posture:** with Guardian-MGC parked and no prop book, live scale rides entirely on Aegis→M6J, which has not gone live. Until it does there is no live automated execution anywhere.

**Risks (probabilistic):**
- Aegis→M6J may itself fail a go-live parity/granularity check (micro-JPY contract granularity vs the locked 1.50% sizing); its ≈0.5× preservation is itself a haircut. **Mitigation:** its go-live is a separate gated decision, not carried by this ADR.
- Parking Guardian-MGC risks it being forgotten; **Mitigation:** it is carried on `STATE.md`'s dormant-threads register with the R7 data-block named.

**Downstream artifacts that need updating (this session):**
- `CLAUDE.md` — Live-execution posture: DEMOTED → NO-GO; remove "R5 DJ30/MYM edition alive" and "Guardian-MGC Rank-1"; record Aegis→M6J active / Guardian-MGC parked.
- `docs/adr/2026-07-03-hardcore-{p1,p3,p5}-*.md` — pointer addendum: live existence-bars dormant under this NO-GO.
- `STATE.md` — dormant-threads + forward board: futures-prop closed; Aegis→M6J active; Guardian-MGC parked.
- `docs/SESSIONS.md` — this session's entry.
- Memory: `project_futures_prop_pivot` (NO-GO), `project_dj30_mym_prototype_falsified` (fed R6), `project_aegis_6j_transfer_state` (now the active lane).

---

## §7 — Implementation plan

Policy + documentation only — no risk-control code edit.

- **Phase 0** — §0 reads verified this session (params.toml unchanged; RESULTS.md FALSIFIED confirmed at `75041aa`; residual §4 falsifier confirmed).
- **Phase 1** — write this ADR; add the CLAUDE.md posture revision; pointer addenda on P1/P3/P5.
- **Phase 2** — `STATE.md` + `docs/SESSIONS.md` entries; memory updates.
- **Phase 3** — verification block (check_brief.py + `verify_lock_anchors.py` + grep sweep) executes; status `Accepted`.

---

## §10 — Audit hooks (runnable)

```bash
# Discipline check
python scripts/check_brief.py docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md --type adr

# The falsification evidence is pinned and unchanged
grep -n "Disposition — FALSIFIED\|0.559" lab/archive/striker_dj30_mym_prototype_2026-07/RESULTS.md

# This ADR changed NO locked constant
git diff --stat HEAD -- core/config/params.toml core/dd_protection.py core/firm_rules.py
# Expected: empty

# Locked MC anchor unchanged (no re-MC under this ADR)
grep -n "99.83\|0.17\|4.37" core/config/params.toml

# No live prop rail was built (NO-GO holds)
ls ops/ | grep -i "bulenox\|crosstrade\|rithmic" && echo "UNEXPECTED: rail artifact present" || echo "OK: no rail (NO-GO)"

# Lock-anchor verification still Closed
python scripts/verify_lock_anchors.py   # Expected: ROUTING: Closed (exit 0)

# §4 trigger reminder — next programme audit / regime check: 2026-08-08
```

---

## Verification

```bash
# Discipline checks (mechanical)
python "C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py" docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md --type adr
# Expected: all 6 checks PASS

# Production-source verification (§0 anchors)
git log -1 --format='%h %ci' -- lab/archive/striker_dj30_mym_prototype_2026-07/RESULTS.md   # 75041aa 2026-07-10
git log -1 --format='%h %ci' -- core/config/params.toml                                       # 784a9ab 2026-06-24

# No risk-control source touched
git diff --stat HEAD -- core/ | grep -E "dd_protection|firm_rules|params.toml" || echo "none (expected)"
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-10 | Initial authoring + acceptance (operator executive decision: R6 = NO-GO; Aegis→M6J active, Guardian-MGC parked) | Joshua + Claude Code |
