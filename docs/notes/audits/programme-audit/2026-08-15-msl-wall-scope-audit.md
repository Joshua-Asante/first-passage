# Audit Note — MSL-era wall-stack scope audit + 2026-08-03 gate-stack follow-up verification

**Audit ID:** AUDIT-2026-08-15-wall-scope
**Date:** 2026-08-15 · **Window:** walls applied 2026-08-08 → 2026-08-14 (MSL/WHO-track era); follow-up items dated 2026-08-08/09/2026-09-01 from the prior audit
**Triggered by:** operator directive, in-session ("audit the walls") — following the research-status review that found the generation funnel (MSL) empty on both slates and the WHO-track sweep. Not a scheduled cadence audit.
**Scope:** **Follow-up / delta audit, explicitly narrower than a full programme audit.** Two parts: (a) mechanical re-verification of [`2026-08-03-gate-stack-audit.md`](2026-08-03-gate-stack-audit.md) §5's own follow-up items (F1–F3, R1–R11) plus the [2026-08-09 rejection-register ADR](../../../adr/2026-08-09-rejection-register-topology-and-bar-wiring.md) §10 hooks; (b) a scope-vs-evidence diagnostic (protocol Q1/Q5-shaped) applied to the 14 distinct admission/kill "walls" that fired during the MSL/WHO-track era, with 3-verifier adversarial refutation on every flagged wall. This note does **not** re-run the full seven-diagnostic sweep across G1–G10 — that baseline stands from 2026-08-03 and is not stale enough (12 days, no new programme) to warrant a full re-audit. Layer: **meta** (the walls audited are epistemic admission/screening rules — the same genre as G1–G10 — not portfolio P&L or dd_protection state).
**Authors:** Joshua (operator directive) + Claude Code (22-agent adversarial workflow, this session).
**Lives in:** `docs/notes/audits/programme-audit/2026-08-15-msl-wall-scope-audit.md`

---

## §0 — Source anchors

- [`2026-08-03-gate-stack-audit.md`](2026-08-03-gate-stack-audit.md) — anchor `91137fb` (2026-08-03). The audit whose §5 follow-ups (F1–F3, R1–R11) this note re-verifies.
- [`2026-08-09-rejection-register-topology-and-bar-wiring.md`](../../../adr/2026-08-09-rejection-register-topology-and-bar-wiring.md) — the D2 ratification-and-wiring rule this note uses as the standard for "is a wall operative." §10 hooks re-run below.
- [`N-2026-08-14-msl-who-track.md`](../../notice/N-2026-08-14-msl-who-track.md) — the estate-wide "STILL DRY" sweep whose cited walls are the primary object of §3 below.
- [`N-2026-08-14-msl-slate-3-constraints.md`](../../notice/N-2026-08-14-msl-slate-3-constraints.md) — precedent notice; source of the "Board-lite" underlying rules (unlabeled) found in §3.
- Seven MSL closures (`MSL-S2B`, `MSL-S2A`, `MSL-C1`, `MSL-C3`, `MSL-C2` — each verified against its own file this session), `docs/rejected_candidates.md` (MSL entries), `docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md`, `docs/methodology/strategy_harvest.md`, `docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md`, `ops/instruments/profiles.json`, `ops/instruments/MECHANISMS.md`, `ops/instruments/MCL.md`, `ops/instruments/NG.md`, `ops/prop_envelope_default.md`, `docs/adr/2026-07-25-instrument-profile-index.md` — all read directly this session by the recon + verification agents (per-file anchors quoted inline in §3).
- Method: 22-agent workflow — 4 parallel recon agents → 1 wall-mapping agent (structured output, 14 walls) → up to 3 hostile refuters per flagged wall (default-REFUTE panel, ≥2/3 not-refuted required to survive) → synthesis over surviving findings only. Full per-agent transcripts retained at the workflow run (`wf_5013860c-86a`); this note transcribes the surviving findings, not raw agent prose.

---

## §1 — Context and trigger

The 2026-08-14 WHO-track notice found the MSL sourcing channel's admission door "empty estate-wide" after two consecutive zero-yield passes (slate-3, then the full product-group sweep). Before treating that as evidence the *search* is exhausted, the standing move this repo's own lineage models (the 2026-08-10 temporal-selectivity finding, which found a raised bar mis-scoped narrower than its applied breadth and reopened a route by ruling, not by data) is to check whether the walls doing the rejecting are actually licensed by their own founding evidence at the breadth they were applied. This note is that check, run adversarially rather than by self-report.

Separately, the 2026-08-03 gate-stack audit graded the meta-layer gate stack **Stable**, with an explicit warning that "the real risk is not erosion, it is unexecuted self-review" and a named list of follow-up repairs (F1–F3, R1–R11) dated 2026-08-08/2026-09-01. Twelve days on, those items had never been re-checked. This note re-checks them as part of the same pass, since an unexecuted-follow-up finding is itself evidence bearing on whether "the walls are sound" can be trusted at face value.

---

## §2 — Part A: 2026-08-03 follow-up verification (re-run, not re-derived)

Each item re-verified this session against live repo state (commands approximated with Grep/Read/Bash; full detail in the workflow transcript).

| ID | Status | Evidence |
|---|---|---|
| **F1** — ratify/revert the 2026-08-02 regime-gate scope narrowing | **STILL-OWED — 7 days overdue** (due 2026-08-08) | `docs/methodology/regime_robustness_gate.md:32,35` still carries the unratified narrowing verbatim; no ADR/addendum since `cd8b617` (2026-08-02) |
| **F2** — re-arm/release the 2026-05-23 override's safety net | **STILL-OWED — 7 days overdue** (due 2026-08-08) | `docs/adr/2026-05-23-allocation-refresh-2.md` change history ends at the 2026-08-02 addendum ("none taken here"); no successor registered on `STATE.md` |
| **F3** — graduate the regime gate to a library | STILL-OWED (due 2026-09-01, not yet overdue) | no `regime_gate.py` anywhere repo-wide; no frozen Cursor spec found |
| **R1** — `dd_lock_offset_usd` correction + RESULTS re-run | PARTIALLY-DONE | source fix landed (`firm_rules.py`, all six tiers now `1_000_000.0`); RESULTS re-run for four decisions of record still owed per [W1 ADR](../../../adr/2026-08-07-w1-intraday-honest-engine-remeasure.md) |
| **R2** — thread `intraday_low` through `prop_survivor_scoring.py` | PARTIALLY-DONE | threading landed (lines 348–546); only Class-S 0.50× full+halves re-run on the honest clock so far |
| **R3** — `ops/sentinel/scan.py::_corresponds` pairing fix | STILL-OWED | unchanged; `docs/adr/2026-08-07-w4-minimal-gate-set-dormancy.md:74` itself records the repair as still red |
| **R4** — `floor_scan.py:85-89` stale PASS | STILL-OWED | `lab/archive/q_kbudget_1_2026-07/floor_scan.py:85,88` unchanged |
| **R5** — `var_trials` empirical-default fix | STILL-OWED (due 2026-09-01) | `lab/research_utils/universe_gate.py:369-370` unchanged |
| **R6** — retire `DEFAULT_FIRM_KEY = "Bulenox_100K"` | STILL-OWED (due 2026-09-01) | `lab/discovery/cost_mnq.py:23` unchanged |
| **R7** — repair `strategy_lifecycle.md` dangling refs | **DONE** | now cites `ops/c1_rail/c1_sizing_host_reference.py` at both sites |
| **R8** — sweep 2 remaining Rule-11 targets | **DONE** | both sites repaired |
| **R9** — schedule 4 stranded §4 falsifiers + meta audit | PARTIALLY-DONE | the meta-audit vehicle itself ran (2026-08-08 quarterly); the 4 named falsifiers still have no individual STATE.md row |
| **R10** — second G10 harvest-intake §4 limb | STILL-OWED (due 2026-11-08) | single limb unchanged; STATE.md still tracks "0-of-2 counting" |
| **R11** — cite governing ADR in WATCH-1H draft | **DONE** | citation + evidence table now present |

**Tally: 3 DONE / 3 PARTIALLY-DONE / 7 STILL-OWED, two of the seven now overdue.**

ADR 2026-08-09 §10 hooks — all 5 **substantively PASS** (D2a `instrument_profiles.py check` → OK, 26 ledgers/51 cells; D2b `cell MNQ ict-liquidity` → BINDING BAR + exit 1 as expected; D1/D5's *literal* grep commands are stale relative to legitimate surrounding-text growth but the underlying conditions they check both hold — 3 ratification stamps present, no live restatement of the dead `dedup_check` claim).

---

## §3 — Part B: MSL-era wall-stack scope audit (Q1/Q5-shaped diagnostic, adversarially verified)

**14 distinct walls mapped** from the MSL closures + the WHO-track notice's "Inherited bars" section. **4 flagged** as `OVER-BROAD` or `UNRATIFIED-OR-UNWIRED` on first read; each sent to a 3-agent hostile-refutation panel (default-REFUTE, ≥2/3 not-refuted required to survive).

**Result: 1 of 4 survived.** 13 of 14 walls hold as legitimately scoped, ratified, and (where D2 requires it) machine-wired.

| # | Wall | First-pass verdict | Adversarial result |
|---|---|---|---|
| 1 | Domain raised bar `index-intraday-ohlcv-directional-timing-2026-07-21` | FINE-SCOPED | not flagged |
| 2 | Req-1a four-clause mechanism definition, applied to internally-composed candidates | FINE-SCOPED | not flagged — R-REQSCOPE (2026-08-12 ADR) explicitly ratifies this widening |
| 3 | 2026-08-09 ratification-and-wiring rule (D2/D3) itself | FINE-SCOPED | not flagged |
| 4 | TNEC N-ACT gate | FINE-SCOPED | not flagged — S2A's solo-leg FALSIFIED is the charter's own foreseen fallback pending TNEC-AU-1 |
| 5 | G0-explore CI falsifier (n≥100, CI-upper<0) | FINE-SCOPED | not flagged — shared numeric template across 3 cards is a provenance note, not a scope mismatch |
| 6 | Delete/flip constraint-selection test | FINE-SCOPED | not flagged — direct operationalization of ADR 2026-07-26 §2-A clause (i) |
| 7 | B4 operator-GO gate | FINE-SCOPED | not flagged |
| 8 | Q-TNEC-CON-5 dense-1m default pause | FINE-SCOPED | not flagged — dated, ratified operator election |
| 9 | "Composite clearance forbidden" rule | UNRATIFIED-OR-UNWIRED | **REFUTED, 3/3.** Founding artifact exists one level up (`docs/briefs/2026-08-13-msl-second-slate.md:48`, predates and parents STAGE0/STAGE1); the rule composes two independently-ratified closures, not an invented ad hoc bar. |
| 10 | E1 stop rule (slate-exhaustion gate) applied estate-wide | OVER-BROAD | **REFUTED, ≥2/3.** E1's own text carries no scope qualifier — it bars a slate-4 card unconditionally, full stop. The WHO-track notice's own structure attributes each individual door to its *specific* wall (Req-1a WHY-clause, hedge-breach, matrix-ban), never to E1 generically; E1 only governs the "no card yet" default, which is exactly what fired. |
| 11 | INTAKE-DRY family designation (MCL evidence applied to NG) | OVER-BROAD | **REFUTED, ≥2/3.** NG's own independently-FALSIFIED `NG-EIA-1` finding is reached one citation-hop away via the shared census document; the TAS/settlement kill is a self-declared, contract-count-invariant structural law the census explicitly frames as applicable at entry-drafting time to any settlement/fix/auction mechanism — a different evidentiary category than the per-instrument effect-size transplant Requirement 2 forbids. |
| 12 | Same-group opposing-legs hedge-breach rule | FINE-SCOPED | not flagged |
| 13 | "No complete-the-matrix" ledger-creation ban | FINE-SCOPED | not flagged |
| 14 | "Board-lite" (continuation-entry + third-MR-at-level bars) | UNRATIFIED-OR-UNWIRED | **CONFIRMED, 2/3.** See below. |

### The one confirmed finding — wall #14, "Board-lite"

The label bundling "no index-futures continuation entry" and "no third MR-at-level rr≈1 card" has **no ADR, no closure, and no `BINDING BAR` registry entry anywhere in the corpus.** `git blame` traces its first use to the same commit that authored the slate-3 notice (`c4dc069d`, 2026-08-14 03:48:40 UTC — both underlying rules stated there, unlabeled); the WHO-track notice (`56be680b`, ~57 minutes later) is the first artifact to attach the name "Board-lite" to them and then cites the compound label within the same document as if it were pre-existing doctrine (`N-2026-08-14-msl-who-track.md:67,84,170,225`).

**This does not revive anything.** Both constituent kill-rules are independently, soundly grounded — continuation-entry traces to MSL-S2B's ratified Stage-1 FAIL (resting on the properly-wired `index-intraday-ohlcv-directional-timing-2026-07-21` bar); the third-MR-at-level rule traces to C1/C2/C3's own prior FALSIFIED/operator-kill dispositions. The defect is purely nominal: a compound label with no paper trail of its own, standing in for two rules that each already have one. (One panel vote refuted the finding, arguing the underlying facts don't change the disposition of any candidate; the other two confirmed the label itself is unratified/unwired as a standalone artifact — the majority reading is adopted here since it is the narrower, more defensible claim and does not contradict the refuting vote's own facts.)

---

## §4 — Disposition verdict

**Stable.** Not **Degenerating** — no wall's founding evidence was substituted, no threshold was loosened, and 13 of 14 walls survived (or were never flagged by) hostile re-verification; the D2/D3 ratification-and-wiring rule (§2 above) is itself demonstrated working, not ceremonial — it is precisely what let the panel discriminate a genuine gap (#14) from three plausible-looking but ultimately sound objections (#9, #10, #11). Not **Falsified** — no forbidden move was found crossed and unrepaired. Not fully **Progressive** — this pass produced one dated hygiene finding, not a corroborated prediction. **Watch flag at authoring time, discharged same session (see §5 update notes):** the F1/F2 overdue items were the load-bearing residual — a scope-narrowing to the regime-robustness gate had sat unratified-or-reverted for a week past its own deadline, and an allocation-override safety net had no successor for even longer. Per the D2 rule this note's own §3 relied on to adjudicate walls #9–#11, an unratified change is "inert prose" that should not be cited as binding either way — F1's narrowing was exactly that state. Both, plus the Board-lite label, were ratified via light-tier ADRs the same day this note was authored; the watch flag converts to a closed item, not a carried one.

**What this audit refutes in its own prior framing:** going in, the working hypothesis (stated in the session that commissioned this audit) was that the empty MSL/WHO-track funnel might indicate an over-tight constraint stack, mirroring the 2026-08-10 temporal-selectivity finding. That hypothesis is **not supported** by this pass — 13 of 14 walls are legitimately scoped. The honest reading is that MSL's dryness is a *generation-input* problem (nothing found, not something found and wrongly rejected), which is a materially different next-step implication (see the closing synthesis in this session).

---

## §5 — Follow-ups

| # | Action | Owner | Date |
|---|---|---|---|
| W1 | **Discharge F1** — ratify or revert the 2026-08-02 regime-gate scope narrowing (`docs/methodology/regime_robustness_gate.md:32,35`). Now 7 days overdue against the 08-03 audit's own date. | Operator (ruling) + CC (ADR) | now-owed — **DONE 2026-08-15**, same session: [`ADR`](../../../adr/2026-08-15-regime-gate-scope-ratification.md) ratifies as-is (grounded in the gate's own stated `dd_protection`-class scope) |
| W2 | **Discharge F2** — register a successor forward-monitor for the 2026-05-23 override, or explicitly record its absence as accepted. | Operator | now-owed — **DONE 2026-08-15**, same session: [addendum](../../../adr/2026-05-23-allocation-refresh-2.md) accepts the absence explicitly (successor is blocked — no live-fill route exists per the 2026-08-04 Tradeify de-scope) |
| W3 | **Retire or paper the "Board-lite" label.** Either delete the name and cite the two underlying rules directly in future notices, or author a one-paragraph light-tier ADR/closure pointer giving it the ratification stamp + `profiles.json`-style wire (or an equivalent lane-status registration) it currently lacks. Cheapest, non-urgent — no candidate was wrongly killed. | Next MSL-adjacent session | before next citation of the label — **DONE 2026-08-15**, same session: [`ADR`](../../../adr/2026-08-15-board-lite-label-ratification.md) papers it as shorthand for the two named rules |
| W4 | **R3/R4/R5/R6/R10 remain individually owed** at their existing dates (2026-08-08 retro / 2026-09-01 / 2026-11-08) — not re-dated by this note, carried forward as-is. | Cursor (per 08-03 audit's own assignment) | as previously scheduled |

---

## §6 — Cross-layer contamination self-check (executed)

Re-read §2–§5 hunting for: (a) citation of locked-portfolio P&L, `dd_protection` state, or strategy authorization tiers as evidence for a wall's verdict; (b) citation of the wall stack's own soundness as evidence about portfolio health. **None found.** Every citation in §3 is a wall's own founding artifact vs. its applied instance (methodology-to-methodology); §4's "Stable" verdict cites only the follow-up tally and the adversarial survival rate, not any P&L or bust-rate figure.

---

## §7 — Discipline checklist self-assessment

| Item | Status |
|---|---|
| Evidence-anchored findings (scoped diagnostic, not full 7-question sweep — see header Scope note) | PASS — §3 |
| Adversarial verification executed (not self-report) | PASS — 3-agent hostile-refutation panel per flagged wall, §3 |
| Falsifier/follow-up check executed (grep/diff shown) | PASS — §2 |
| Cross-layer contamination check passed | PASS — §6 |
| Disposition verdict assigned with reasoning that follows the evidence | PASS — §4 (written after §2/§3) |
| Follow-up actions named, owner + date | PASS — §5 |
| §10 audit hooks runnable at next cycle | PASS — below |

---

## §10 — Audit hooks (runnable, next cycle)

```bash
# F1/F2 discharge check
git log --oneline -- docs/methodology/regime_robustness_gate.md | head -3   # expect a commit after cd8b617
grep -n "successor forward monitor\|2026-05-23-allocation" STATE.md         # expect a hit once F2 is discharged

# Board-lite label — has it acquired a ratification stamp / wire, or been retired?
grep -rn "Board-lite" docs/ ops/ scripts/ core/ 2>/dev/null

# Wall-audit re-run trigger: has a new MSL/WHO-track-era wall killed a candidate since this pass?
git log --since=2026-08-15 --oneline -- docs/rejected_candidates.md docs/notes/notice/

# R3/R4/R5/R6/R10 unchanged-since check (re-run the 08-03 audit's own §3.7 falsifier greps)
grep -n "def _corresponds" ops/sentinel/scan.py
grep -n "clause_n=\"PASS: power=0.638" lab/archive/q_kbudget_1_2026-07/floor_scan.py
grep -n "var_trials=None" lab/research_utils/universe_gate.py
grep -n "DEFAULT_FIRM_KEY = \"Bulenox_100K\"" lab/discovery/cost_mnq.py
```

---

## §11 — Closure

- **Status:** `Closed (immediate + W1–W3 structural complete same session; R3–R6/R10 carried forward, not this note's to discharge)`.
- **Immediate repair completed:** 2026-08-15 (this note; registry wiring).
- **Structural repair completed:** 2026-08-15, same session — W1 ([regime-gate ratification](../../../adr/2026-08-15-regime-gate-scope-ratification.md)), W2 ([allocation-refresh-2 addendum](../../../adr/2026-05-23-allocation-refresh-2.md)), W3 ([Board-lite ratification](../../../adr/2026-08-15-board-lite-label-ratification.md)). R3–R6/R10 remain the 08-03 audit's own assigned owners, unchanged.
- **Lessons graduated to standing rule:** none this cycle — the Board-lite finding is a first observation, below the two-incident bar (watch).
- **Follow-up audits triggered:** none automatically. R3–R6/R10 remain the residual "unexecuted self-review" risk for the next quarterly cycle (2026-11-08).

---

## Verification

```bash
python scripts/check_brief.py docs/notes/audits/programme-audit/2026-08-15-msl-wall-scope-audit.md --type audit
python ~/.claude/skills/brief-authoring/scripts/check_brief.py docs/notes/audits/programme-audit/2026-08-15-msl-wall-scope-audit.md --type audit
grep -c "REFUTED\|CONFIRMED" docs/notes/audits/programme-audit/2026-08-15-msl-wall-scope-audit.md
```

Audit notes fail by capturing the trigger without naming the structural cause. The check here: would §10's hooks actually detect an F1/F2 discharge or a Board-lite retirement next cycle? Yes — both are direct greps against the exact artifacts that would change.
