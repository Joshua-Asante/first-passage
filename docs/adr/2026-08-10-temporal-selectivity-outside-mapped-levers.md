# ADR 2026-08-10 — Within-instrument temporal selectivity is OUTSIDE the mapped cost-ratio levers; dense-1m lane door-check repaired

**Status:** `Accepted` — operator ruling in-session 2026-08-10 / JA ("I rule it open" + "proceed with the step 1 repair"). Ruling ID **`TEMPORAL-SELECTIVITY-OPEN-2026-08-10`**.
**Decision date:** 2026-08-10
**Authors:** Joshua (ruling) + Claude Code (Opus 5, evidence trace)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [index-intraday-OHLCV raised bar](../rejected_candidates.md) (the bar being read) · [cross-index RV closure](../rejected_candidates.md) (the mapping's actual provenance) · [dense-1m lane spec](../spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md) (repaired here) · [cell-#3 falsifier](../../lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_cost_geometry_2026-08-10_LOG.md) (surfaced both items) · [CON-2 closure](../briefs/closures/Q-TNEC-CON-2-closure-ambiguous-hold.md) · [rejection-register topology](2026-08-09-rejection-register-topology-and-bar-wiring.md)
**Layer:** research-doctrine reading + gate-wiring repair. **$0 / K=0.** No `core/`, Pine, allocation, `dd_protection`, lifecycle, `LEG_MAP`, or rail change; nothing armed; no candidate admitted.

---

## §1 — Context

The 2026-07-21 raised bar admits a new single-instrument index-futures intraday **OHLCV directional-timing**
candidate only via route ① *a mechanism outside the mapped cost-ratio-lever set (**price · instrument-selection
· hold-time**)*, ② a different modality/venue, or ③ beating incumbent ORB-MNQ net-of-cost.

The 2026-08-10 cell-#3 cheap falsifier established two things at $0: **stop width cannot rescue the dense-1m
family** (0.02–0.10× the 4× cost bar across the entire ratified 5–20 pt band), and **the surviving cost-geometry
lever is trade count** — a once-per-session rule needs only **3.3%** of the ~170 pt/session perfect-foresight
oracle, against ~20% for CON-2's ~6/day. It also found that the lane spec, the CON-2 brief and its `PREREG_G0`
**never cite the bar at all**, so CON-1 and CON-2 both ran unbound by a live `tier=always` gate
(`lesson_gate_reachability_preregistration`, unbinding form, **5th firing**).

## §2 — Decision

**2-A — Reading (the ruling).** The mapped lever **"instrument-selection" means CROSS-instrument selection**.
Its provenance is the cross-index RV-ranking closure, whose measured finding was *dilution across a universe*
(+2.64 bp RV-ranked vs **+5.19 bp always-MNQ**) — a statement about choosing among **instruments**, not among
**moments within one instrument**. **Within-instrument temporal selectivity — which moment of a session to
take — was never mapped and never measured for cost-ratio effect.** It is therefore **outside** the mapped set,
and **route ① is OPEN** to it.

**2-B — Conditions of the opening (binding; the opening is not a weakening).** A temporal-selectivity cell is
the single highest-risk laundering shape in this estate — it is the same family the **F2 guard** exists to
catch (*"the ORB filter slices that look better in-sample — Friday / Monday / OR-hi / same_bar"*). Accordingly:

1. The selection criterion is **causally named a priori** and frozen at G0 — never chosen after seeing which
   moments performed, and never read off a scored list (EM screen §2.0a: *screen the class, not the winner*).
2. **Every axis charges `K_intrinsic`** — each candidate moment-criterion, threshold, and window is a cell;
   EM0 ≤3 with a working budget of 1–2 stands unchanged.
3. Nothing downstream is weakened: harvest Req 1–5, DSR-at-K, the cost law, the regime gate, and the
   EXPLORATION/CONFIRM discipline all bind exactly as before.

**2-C — What this does NOT open.** The **price** and **hold-time** levers stay mapped and exhausted
(hold-time additionally re-falsified empirically by the 08-10 stop-width sweep). **Cross-index selection stays
closed** at its own bar. Routes ② and ③ are unchanged. No C1–C11 door, no DEAD-list row, and no frozen CON-1/
CON-2 constant is reopened; a successor is a **fresh Q-ID with a fresh G0**, never a retune.

**2-D — Step-1 repair (gate wiring).** The dense-1m lane spec's step-1 door check is amended from
"C1–C11 + MNQ DEAD list" to additionally require the **executed profile consult**
(`python scripts/instrument_profiles.py cell <SYM> <mechanism-id>`), which **exits nonzero when a prior binds**
(verified 2026-08-10: exit 1 on a `BINDING BAR` cell, 0 on a clean cell — doctrine and code agree), with **every
`BINDING BAR` line answered in the brief's §0 by naming the route that clears it**. An unanswered binding bar
blocks the G0 freeze.

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Read "instrument-selection" broadly to include temporal selection | Would bar the one lever the falsifier showed has headroom, on a mapping derived from a measurement (cross-index dilution) that never tested it. Barring on unmeasured grounds is the "unreachable gate" failure in its other form. |
| Leave the lane spec's door check as-is and rely on reviewer diligence | Two campaigns already ran unbound. The consult is mechanical and already exits nonzero — declining to wire it is choosing the failure again. |
| Close the dense-1m lane outright | The oracle headroom (3.3% needed) is measured and real; the lane's own stop-rule (3 consecutive FALSIFIED) has not fired — CON-1 FALSIFIED, CON-2 AMBIGUOUS-HOLD. |

## §4 — Falsifier

**H:** *the mapped-lever set, as now read, bars exactly the exhausted moves and no live one.*

| # | Trigger | Threshold | Action |
|---|---|---|---|
| T1 | The opening laundered a re-tune | a temporal-selectivity cell is admitted whose criterion is traceable to a post-hoc read of scored CON-1/CON-2 output | void that cell; re-close route ① for temporal selectivity by superseding ADR |
| T2 | The reading was wrong | a temporal-selectivity cell clears the bar and then dies on precisely the cross-index dilution mechanism | fold temporal into the mapped "selection" lever; supersede 2-A |
| T3 | The repair is still unbinding | any lane G0 freezes with an unanswered `BINDING BAR` | escalate the door check from spec prose to a `gates.yml` limb |

**Trigger check schedule:** T1/T2 on each dense-1m cell scored · T3 at each G0 freeze and the next quarterly audit.

## §5 — Forbidden moves

- **Reading 2-A as a licence for a filter sweep.** Route ① being open is an *entry permit for one named cell*, not for a family of moment-filters; the F2 guard is unchanged and 2-B(2) prices every axis.
- **Treating the 3.3%-of-oracle headroom as an expected value.** It is a fraction of a max-order-statistic; random entry captures ≈0 or negative (MNQSEL-2 S1 ≈ −0.036).
- **Re-opening hold-time under cover of "cost geometry."** It is mapped *and* empirically re-killed on 08-10.
- **Skipping the consult because the answer is remembered.** It is executed output or it did not happen (`lesson_dedup_attestation_must_be_executed`).
- **Reading this ADR as a GO** for any campaign, Cap claim, deploy, Pine, or arming.

## §6 — Consequences

- The dense-1m lane reopens for **one** kind of successor: a causally-named, K-charged, once-per-session-class temporal-selectivity cell aimed at trade-count cost geometry. It remains unauthored; a fresh Q-ID + G0 + operator explore GO is the path.
- The lane's door check now reaches domain-level bars, and the failure that let CON-1/CON-2 run unbound is closed at the surface where it is read.
- `lesson_gate_reachability_preregistration` stands at **5 firings**; promotion to a standing gate remains an open operator question, unchanged by this ADR.

## §8 — Ratification

```
RATIFICATION:    2-A within-instrument temporal selectivity ruled OUTSIDE the mapped
                 cost-ratio-lever set; route 1 OPEN to it, under the 2-B conditions.
                 2-C scope guards affirmed (price / hold-time / cross-index stay closed).
                 2-D dense-1m lane step-1 door check repaired to require the executed
                 profile consult with every BINDING BAR answered by route.
DATE / INITIALS: 2026-08-10 / JA
```

## §10 — Audit hooks (runnable)

```bash
# 1. The consult still exits nonzero when a prior binds (the repair's whole basis).
python scripts/instrument_profiles.py cell MNQ compression-gated-breakout; echo "expect 1: $?"
python scripts/instrument_profiles.py cell MCL trend-following;            echo "expect 0: $?"

# 2. The lane spec's step 1 now names the consult and the answer-every-bar requirement.
rg -n "instrument_profiles|BINDING BAR" docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md
# Expected: step 1 + the reader-intercept.

# 3. The mapped-lever provenance claim is still what 2-A rests on.
rg -n "2.64 bp|5.19 bp|dilutes" docs/rejected_candidates.md | head
```
