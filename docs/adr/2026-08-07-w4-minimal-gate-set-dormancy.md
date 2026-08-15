# ADR 2026-08-07 — W4: minimal gate set with dormancy

**Status:** `Accepted` — plan GO (Posture-A); dormancy + named re-arm conditions
**Decision date:** 2026-08-07
**Authors:** Joshua (Posture-A direction) + Cursor (drafter)
**Supersedes:** `2026-07-20-stage8-variance-dominance-risk-neff-gate.md` in part — sole-producer status of risk-breadth coordinates while breadth is tombstoned (coordinates remain doctrine; producer dormant)
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [SPEC S7](../spec/2026-08-07-loop-s7-repo-alignment-spec.md) · [alignment manifest](../notes/2026-08-07-posture-a-alignment-manifest.md) · [gate-stack audit R3/R5/R6](../notes/audits/programme-audit/2026-08-03-gate-stack-audit.md) · [survivor-scoring prereg](../briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md) (frozen — close+reopen only)
**Layer:** research-gate composition. **$0 / K=0** — no campaign open, no K spend, no frozen-prereg body edit.

---

## §0 — Rule 0 reads (verified 2026-08-07)

| Source | Anchor | What it pins |
|---|---|---|
| `lab/research_utils/universe_gate.py` | SPA/StepM + DSR + PBO orchestrator; `var_trials` default still empirical | Live composition today |
| `lab/research_utils/breadth.py` + skill launcher | Stage-8 5th-column tool | Sole producer of envelope §2 item 6 coordinates |
| Survivor-scoring prereg Trap #12 | frozen body | G6/G7/tier changes only via close+reopen |
| Gate-stack audit R3/R5/R6 | 2026-08-03 | Sentinel pairing · `var_trials=1/n` · `DEFAULT_FIRM_KEY` |

---

## §1 — Context

Posture-A collapses the research gate surface to a **minimal live set** and puts the heavy universe-correction stack in named dormancy so skills and REPO_MAP stop advertising dead or producer-less protocols as live.

---

## §2 — Decision

### Live (minimal)

- Mechanism-first admission / EM0–EM5 corridor + DSR-cap refuse at `register_search open` (S6).
- Temporal-consistency battery where a campaign prereg still requires it.
- Realism / Stage-7 limbs named by the active campaign prereg.
- Prop survivor-scoring **G0–G5 + G8** (and any limb a campaign’s own frozen prereg still binds) — **G6/G7 shape changes only via close+reopen** of the survivor-scoring prereg (this ADR does **not** edit that frozen body; it records the constraint).

> **Addendum 2026-08-08 — the additive limb resolves to the EMPTY SET today; the live floor is G0–G5 + G8 only.**
> Measured, not inferred: of 17 live `lab/analysis/**/PREREG*.md` bodies, only **3** are named by any
> `discovery_manifests/*.json`; the `prereg` field is **optional and undocumented** (9 of 13 manifests carry it,
> 1 dangles); and the most-cited machine-bound body — `lab/archive/mnq_sr_structure_2026-08-06/PREREG.md` —
> has **no §6 gate and no audit hooks at all**, so it binds nothing to add. "Which prereg is active for this
> campaign" is therefore not answerable from the corpus, and a reader cannot evaluate the parenthetical above.
> **Until a campaign names its prereg mechanically, read the live minimal set as G0–G5 + G8.** Two clarifications
> so the clause cannot be over-read: *"campaign prereg"* means the **seeking campaign's own** frozen body, not any
> body in the corpus; and *"operator GO"* in the re-arm conditions below means a GO **dated after 2026-08-07** —
> a closed campaign's frozen text (e.g. `DISC-CAMP-0`, which names SPA/StepM/PBO thresholds *and* carries an
> operator-confirmed-at-freeze line) must not re-arm a dormant family by standing text alone.
> **No bytes struck from §2 or from the re-arm table.** See also the Rule-11 dormancy record on the
> [substrate retirement ADR](2026-07-22-challenge-era-substrate-retirement.md), which documents why the
> survivor-scoring prereg's own §0 anchor and §10 hook 7 no longer resolve.

### Dormant (code retained; not the default path)

| Component | Status | Re-arm condition |
|---|---|---|
| **SPA / StepM** (`arch` via `universe_gate`) | **Dormant** | Campaign prereg explicitly names SPA/StepM thresholds **and** operator GO to leave dormancy |
| **PBO / CPCV** (`skfolio` via `universe_gate`) | **Dormant** | Same — prereg + GO; time-series leakage risk must be argued in the prereg |
| **Universe-gate orchestrator as default promote/reject** | **Dormant** | Re-arm only when SPA+DSR+PBO are all re-armed for that family |
| **Plateau protocol** (`plateau_tracker`) | **Archived** (skill banner) | Fresh pre-reg with same-feed baseline rule; not the standing validation path |
| **Breadth / risk-N_eff** (`breadth.py`) | **Tombstoned as live producer** | Envelope §2 item 6 coordinates stay doctrine but are **report-optional / no sole producer** until a re-arm ADR restores a producer; skill launcher not the default path |

### `var_trials` / audit R5

`universe_gate.py` still defaults to the empirical `Var(col_sr)` estimator (self-tests depend on it). **Do not flip the module default in this PR.** Campaigns should continue to **pass `var_trials=1/n`** (or pin V) until a separate change lands with green self-tests. Audit R5 schedule **2026-09-01** stands unless absorbed by that later change.

### Audit board absorption (pointers)

| Audit row | Disposition under W4 |
|---|---|
| **R3** (`sentinel` prereg↔RESULTS pairing) | Absorbed-or-redated by two-tier / closed-loop PREREG discipline; sentinel repair remains its own owner if still red — dated pointer, not silent drop |
| **R5** (`var_trials=1/n` default) | Absorbed as **standing caveat** (pass V explicitly); schedule 09-01 left standing for the code default flip |
| **R6** (`DEFAULT_FIRM_KEY` in `cost_mnq.py`) | Schedule 09-01 left standing — not discharged by dormancy alone |

### Envelope §2 item 6

While breadth is tombstoned, item 6 loses its sole live producer. Change-control: this ADR. Coordinates remain the Stage-8 **doctrine** for book-leg admission when a producer is re-armed; they are not silently deleted from `ops/prop_envelope_default.md`.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Delete SPA/PBO/breadth code | Loses self-tests and re-arm path |
| Flip `var_trials` default here | Breaks empirical self-tests; deferred |
| Edit frozen survivor-scoring prereg G6/G7 | Trap #12 — close+reopen only |

---

## §4 — Falsifier

**H:** Skills + REPO_MAP + harvest front-door describe the minimal/dormant split; no campaign treats dormant SPA/PBO/breadth as mandatory without a re-arm GO.

**FALSIFIED if:** a campaign is rejected solely for skipping a dormant gate without prereg requiring it; or the frozen survivor-scoring prereg body is edited without close+reopen.

---

## §5 — Forbidden moves

- Editing `docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md` body under this ADR.
- Deleting `universe_gate` / `breadth` modules.
- Claiming envelope item 6 is discharged while no producer exists.

---

## §6 — Gate

Propagation sweep (REPO_MAP · strategy-validation skill · futures-anomaly var_trials note · strategy_harvest · prop_envelope §2 item 6 · variance-dominance Superseded-in-part-by · audit R3/R5/R6 pointers) lands in the same PR. **RESOLVED** for plan GO when those pointers refresh; re-arm of any dormant limb needs its own dated note.

---

## §7 — Audit hooks

```bash
grep -n "Dormant\|tombstoned\|archived" REPO_MAP.md .claude/skills/strategy-validation/SKILL.md
grep -n "Superseded-in-part-by" docs/adr/2026-07-20-stage8-variance-dominance-risk-neff-gate.md
grep -n "W4\|dormant\|tombston" ops/prop_envelope_default.md docs/methodology/strategy_harvest.md
```

---

## Addendum 2026-08-15 — audit R3 / R5 / R6 discharged

W4 deferred the code flips and left the 09-01 / sentinel-repair dates standing. The 2026-08-15 gate-stack repair pass executed them:

| Audit row | Disposition |
|---|---|
| **R3** (`_corresponds` prereg↔RESULTS) | **DONE** — body Q-ID + RESULTS-cites-prereg pairing; path-only tests unchanged |
| **R5** (`var_trials=1/n` default) | **DONE** — module default flipped; self-tests rewritten against `1/n` |
| **R6** (`DEFAULT_FIRM_KEY` in `cost_mnq.py`) | **DONE** — `firm_key` required; cheapest-firm default retired |

R10 now lives as an **Accepted** second §4 limb on the [harvest-intake ADR](2026-07-15-external-mechanism-harvest-intake.md) (operator GO 2026-08-15). The historical-kill pin is still unmarked — not fired. Dormancy table above is unchanged.
