# ADR 2026-08-15 — No-counterparty statistical/geometric sourcing channel: Req-1a jurisdiction clarified, not weakened

**Status:** `Accepted` — ratified by operator (JA) 2026-08-15, in-session election ("admit a weaker evidentiary grade for candidate sourcing"); CC drafted and adversarially stress-tested (3 independent rounds) before ratification
**Decision date:** 2026-08-15
**Authors:** Joshua (direction) + Claude Code (Rule-0 recon, design, 3-round adversarial hardening — workflow `wf_995c8be8-c14`)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [`2026-08-12-msl-sourcing-channel-ratification.md`](2026-08-12-msl-sourcing-channel-ratification.md) (R-CHANNEL/R-FRAMING/R-REQSCOPE — governs MSL composition specifically; this ADR is a **sibling** channel, not an MSL amendment) · [`2026-07-26-mechanism-counterparty-constraint-boundaries.md`](2026-07-26-mechanism-counterparty-constraint-boundaries.md) (Req-1a's four-clause definition, left untouched) · [`2026-07-15-external-mechanism-harvest-intake.md`](2026-07-15-external-mechanism-harvest-intake.md) (scoped to externally-published seeds only — does not reach this channel) · `.claude/skills/futures-anomaly-discovery/SKILL.md` (owns the `--lane blind` pipeline this channel runs inside) · [`N-2026-08-14-msl-who-track.md`](../notes/notice/N-2026-08-14-msl-who-track.md) (the sweep motivating this ADR) · [`2026-08-15-msl-wall-scope-audit.md`](../notes/audits/programme-audit/2026-08-15-msl-wall-scope-audit.md) (today's independent audit of MSL's admission walls) · [`2026-08-15-regime-gate-scope-ratification.md`](2026-08-15-regime-gate-scope-ratification.md) (today's scope ruling — load-bearing for Forbidden move 5) · [`2026-08-14-msl-yield-falsifier-survival-limb.md`](2026-08-14-msl-yield-falsifier-survival-limb.md) (MSL's own falsifier, correctly distinguished here from harvest-intake's)
**Layer:** methodology (research rules of evidence only). No strategy/risk-control parameter, allocation, `dd_protection` constant, or Pine source is touched. **$0 / K=0.** **Tier:** FULL (ceremony-tiering limb 4 — creates a new admission channel binding future candidate sourcing).

---

## §0 — Rule 0 reads (production/methodology-source verification)

Files read in full, this session, before drafting (anchors as of 2026-08-15):

- `docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md` — `185614d` (2026-08-08). Req-1a's four clauses (WHO/WHEN/WHY/HOW, L42–45); scope line "research rules of evidence; harvest/discovery intake and ledger semantics only" (L59). No "delete/flip" mechanics found in this file — that lives elsewhere (a lesson-registry artifact, not this ADR); not load-bearing here.
- `docs/adr/2026-08-12-msl-sourcing-channel-ratification.md` — `c0d20bd` (2026-08-12). R-REQSCOPE (§2.3, L26): Req 1b/Req 2 do **not** bind MSL composition; Req 1a **does**, unchanged. Silent on any future non-constraint channel.
- `docs/adr/2026-07-15-external-mechanism-harvest-intake.md` — `5563cf4` (2026-08-10, path-repair; content ratified 2026-07-15). Scope line: "all externally-sourced strategy/anomaly seeds... Out of scope: ... Gen-2 internally-mined candidates." §4 idle-guard trigger ("zero screen-PASS seeds beyond D5 by 2026-11-08") — confirmed this guard's ledger structurally excludes MSL.
- `docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md` — `f203b78` (2026-08-14). Objective line: "operator+Claude composition loop (idea → $0 screens → Pine → operator TV backtest → survivor MC)." Step 1: "idea + mechanism story (who loses money and why)" — MSL structurally requires a counterparty claim at intake.
- `docs/adr/2026-08-14-msl-yield-falsifier-survival-limb.md` — `103b084` (2026-08-14). MSL's own two-rung falsifier: Rung A (soft) at 6 consecutive G0-freezes-without-Pine; Rung B (hard FALSIFIED) at 10 consecutive freezes with zero survivors, or 8 calendar weeks from 2026-08-12 (≈2026-10-07) with ≥4 freezes and zero survivors.
- `docs/methodology/strategy_harvest.md` — `d1eca05` (2026-08-13). Title: "sourcing + admission of externally-published mechanisms." Requirement 2 (L27) is a single unified clause — cohort-citation and cross-instrument-transplant-ban are not severable.
- `lab/research_utils/axis_screen.py` — `2ef7405` (2026-08-04). Frozen constants `CAP=1.0, DSR_MIN=0.95, POWER_MIN=0.50, Z=1.96`, no CLI/env override (L7–8, 29–34); schema permits `delta_citation: null` (L107, 115–116).
- `.claude/skills/futures-anomaly-discovery/SKILL.md` — `d1eca05` (2026-08-13). L215–218: "Discovery does not need a mechanism — a survivor eventually does... Mining without a mechanism is fine; deploying without one is not." L84–157: K-accounting (`register_search open`/`close`, Bonferroni/BH-FDR/K·α). L102–103: `--lane blind`, "no admission gate... `--prereg` omittable... unbound by design." L166–169, 184–188: the rigorous universe-level correction (Reality Check/SPA/Romano-Wolf) is **dormant (W4)** — the cheap Bonferroni/BH-FDR triage is not a substitute for it.
- `docs/notes/notice/N-2026-08-14-msl-who-track.md` — `14d71c9` (2026-08-14). §6: `RESOLVED (STILL DRY)`. §5 forbidden moves explicitly bars citing `FALSIFIED(yield)` — "it has not fired." §3.1–3.5: five doors walked; three die on WHO's sign-not-entailed defect (BE1), two die on WHY's institutional-ticket-size defect — majority-killed on WHO, not WHY.
- `docs/briefs/closures/MSL-S7-closure-resolved-e1-hold.md` — `ef48b01` (2026-08-14). Confirms disposition is `RESOLVED (E1 HOLD)`, an operator-marked pause pending a new WHO — not a fired falsifier.
- [`2026-08-15-msl-wall-scope-audit.md`](../notes/audits/programme-audit/2026-08-15-msl-wall-scope-audit.md) and [`Q-BUSTGATE-2-closure-resolved.md`](../briefs/closures/Q-BUSTGATE-2-closure-resolved.md) — both authored earlier this same session. The wall audit's independent conclusion ("13 of 14 walls legitimately scoped... MSL's dryness is a generation-input problem") is the actual grounding for why this ADR opens a new channel rather than loosening an existing one; the bust-ceiling closure confirms N-SURV is unmoved and this ADR must not touch it.

---

## §1 — Context

**What actually happened, precisely stated.** MSL's WHO-track sweep — an estate-wide zero-data walk across every Tradeify product group plus the census backlog — closed `RESOLVED (STILL DRY)` on 2026-08-14. This is the *only* estate-wide pass; the preceding slate-3 notice was scoped narrowly to the reopened fade-geometry region on one instrument (MCL), not the estate — "two estate-wide sweeps" would overstate the record. Five doors were formally walked against the Req-1a four-clause test: **three die on clause WHO** — sign-not-entailed (BE1): the constraint obliges an *action* (file a nomination, take metal out of a warehouse, be delta-flat at a cut) but never a *signed direction*, so there is no hypothesis to test statistically in the first place — and **two die on clause WHY** — institutional-ticket-size: the residual asserted is full-size, not sub-institutional, a binary categorization no evidentiary-strength threshold changes.

**The disposition this triggers is `RESOLVED (E1 HOLD)`, not a fired falsifier.** MSL's own charter states, in the same notice reporting the dryness: "Cite FALSIFIED(yield) — it has not fired." Critically, **the harvest-intake ADR's idle guard is the wrong instrument for measuring MSL's dryness at all**: that guard's scope line reads "all externally-sourced strategy/anomaly seeds... Out of scope: ... Gen-2 internally-mined candidates." MSL — an operator+Claude *composition* loop — is neither externally-sourced nor covered, and never was inside that guard's ledger. MSL carries its own, separately-ratified two-rung falsifier (Rung A soft-WATCH at 6 consecutive G0-freezes-without-Pine, currently 4/4 observed; Rung B hard-FALSIFIED at 10 consecutive freezes or 8 calendar weeks from 2026-08-12, landing ≈**2026-10-07**). That date — not 2026-11-08 — is the real clock this ADR is racing.

**Why a new channel, not a Req-1a amendment.** MSL's charter requires a WHO/WHY narrative *at intake*: step 1 is "idea + mechanism story (who loses money and why)." MSL structurally cannot host a candidate that never carries a counterparty claim — that is not a gap in MSL, it is what MSL is *for*. The five dead doors above would not have been saved by loosening the evidentiary bar: three fail on a categorical WHO defect no evidentiary relaxation touches, and the other two fail a binary size test, not a marginal evidence-strength call. Today's independent wall-scope audit confirms this directly: 13 of 14 audited MSL-era admission walls survived adversarial re-verification, refuting the working hypothesis that the funnel is dry because gates are over-tight. **The honest reading is that MSL's dryness is a generation-input problem, not an evaluation problem.** This ADR does not respond to a tripped gate and does not weaken Req-1a for anyone. It opens a genuinely separate, narrower-scope channel for a candidate class MSL was never built to carry: constructs whose own claim never names a counterparty at all.

---

## §2 — Decision

**Open a formally-chartered channel owned by `futures-anomaly-discovery`, not by MSL.** It runs entirely inside that skill's existing `--lane blind` intake (`register_search open --lane blind` → `close` → `stage24_runner`), a pipeline structurally distinct from MSL's 8-step G0/explore/Pine/TV chain. No MSL R-CHANNEL/R-FRAMING/R-REQSCOPE election is cited as authority here — those rulings bind MSL composition specifically; this channel is a sibling, standing on this ADR's own authority. Req-1a is **not** weakened for any candidate whose own claim names a counterparty — full four clauses, unchanged, via MSL or the harvest intake as applicable.

**Channel boundary.** Does the candidate's own claim name an identifiable counterparty? If yes → Req-1a, unmodified. If no counterparty claim is made at all — not merely "none was written down," but the construct is genuinely narrative-free by kind (a motif, a change-point, a fitted expression) → this channel.

**Substitute gate, run in full per candidate, no new machinery invented:**

1. **K-accounting (Rule 1).** `register_search open --lane blind` before results are seen; `close` computes the Bonferroni floor, BH-FDR survivors, and K·α expected false positives. Unlike the blind lane's normal posture ("blind opens stay unbound by design"), **this channel makes `--prereg` mandatory** — a tightening specific to this channel, not a repeal of the general default. ⚠ **A declared-K ceiling also binds at open — see the [2026-08-15 K-cap addendum](#addendum-2026-08-15--declared-k-ceiling-at-open-k--3) below; do not read this item as licensing an uncapped blind mine.**
2. **Mandatory frozen train/confirm partition**, named in that `--prereg` file *before* the mining pass runs. The mining/selection step reads only the train partition. Every confirmatory number below computes only on the confirm partition, which the search never touched. This is the channel's disclosed answer to having no external cohort to supply independence against.
3. **DSR ≥ 0.95** at the declared K on the confirm partition, frozen constants, no override.
4. **SPA/PBO universe-level correction is dormant repo-wide (W4).** This channel does not claim that correction is running. The frozen train/confirm split above is the explicit, weaker, disclosed substitute for this channel specifically — never cited as equivalent to a Reality-Check/SPA pass.
5. **Cost-law reachability** (Req 5's ≥4× round-trip inequality), with the candidate's own confirm-partition measured effect substituted for cohort δ — the schema already permits this (`delta_citation: null`).
6. **Own-series half-split DSR check** — deliberately renamed away from "regime-robustness" to avoid the canonical name. Its split point and floor must be frozen in the same `--prereg` file, before scoring, by analogy to (never invocation of) the canonical gate's no-hidden-parameter principle.
7. **N-SURV, unchanged.** The TNEC-1 limb (bust ≤3.0% ∧ P(pass) ≥50%), reconfirmed unchanged today. A channel survivor must clear N-SURV on the incumbent eval separately — the battery above never substitutes for it.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Weaken Req-1a's WHY clause directly, for constraint-based candidates.** | The dead-door breakdown shows this would not have helped: 3/5 fail on WHO's categorical sign-not-entailed defect (immune to any evidentiary-strength threshold), and the other 2/5 fail a binary size test, not a marginal call. A WHY-only relaxation solves a problem the evidence doesn't show exists. |
| **Route the new channel through MSL, citing R-REQSCOPE as authority.** | MSL's own charter mandates a mechanism story at step 1 — it structurally cannot host a no-counterparty candidate. Citing MSL's already-ratified elections (which govern *composition*, not sourcing modality) as authority for an unrelated pipeline would conflate two chains with different falsifiers, different gate criteria, and different intake mechanics — caught explicitly on adversarial review. |
| **Anchor the falsifier to harvest-intake's idle-guard date/mechanism.** | That guard's own scope line excludes internally-mined candidates by name; borrowing its date without borrowing its jurisdiction produces a falsifier anchored to a clock that isn't actually under pressure from this decision. |
| **Do nothing — accept exhaustion under current doctrine.** | The operator's own election (2026-08-15, in-session) chose against this. Recorded here as the declined branch, not vacated: if this channel also falsifies, the honest fallback is the source-class post-mortem this ADR's §6/§7 name, not a third channel. |

---

## §4 — Falsifiable hypothesis

**H:** the no-counterparty statistical/geometric channel, screened through the full substitute battery (§2) on each candidate's own instrument panel, produces ≥1 candidate that clears the battery **and** N-SURV out-of-sample by the next standing quarterly programme-audit date, **2026-11-08**.

**Battery-closure, defined explicitly** — the gap a stress-tested prior draft of this ADR left open: a candidate counts as a **zero-survivor closure** the moment it dies at *any* named stage (cost-law UNREACHABLE, K-cap FAIL, DSR FAIL, or own-series split FAIL), not only after a full run-through. This is load-bearing: the cheapest, most common kill mode in this pipeline is a one-division cost-law death (D5 / H-OD-1 / Q-MCLTAS-1 precedent), and a definition that counted only full runs would let unlimited cheap deaths accumulate without ever registering a strike — the identical defect shape the 2026-08-03 gate-stack audit found in harvest-intake's own §4 routing-exemption clause, closed here by definition rather than repeated.

**Accept H → `RESOLVED` if:** ≥1 candidate clears the full battery + N-SURV OOS by 2026-11-08.
**Reject H → `FALSIFIED` if:** ≥1 candidate reaches battery-closure and zero survive by that date.
**`AMBIGUOUS-HOLD` if:** zero candidates are *sourced* at all (not merely zero finished) by 2026-11-08 — re-test at 2027-02-08, no change to terms.

⚠ **A third case exists and is ruled below — see the [2026-08-15 pre-G0 addendum](#addendum-2026-08-15--a-pre-g0-kill-is-not-a-4-strike). A candidate killed at a pre-G0 cheap falsifier is neither branch above.** Do not classify such a kill against this section without reading that addendum.

---

## §5 — Forbidden moves

1. Tuning K-accounting/DSR/cost-law/split-DSR constants inside this channel to admit a marginal seed.
2. Skipping `register_search open` before results are seen, or closing a search without the Bonferroni/BH-FDR/K·α computation.
3. **Routing a nameable-counterparty candidate through this channel to dodge Req-1a — including by omission.** Authoring a candidate write-up that avoids articulating a plausible counterparty story specifically so it qualifies for the cheaper battery is the same forbidden move as active re-routing after the fact.
4. Cross-instrument transplant of any battery result — grounded in the MSL charter's own "no instrument-hopping after scoring" boundary line, **not** in harvest Requirement 2 (R-REQSCOPE released the whole of Req 2 from binding MSL-adjacent composition; citing "Req 2" here would contradict that ruling's plain text).
5. **Citing this channel's own half-split DSR check as satisfying, superseding, or being interchangeable with the canonical `regime_robustness_gate.md` bootstrap+half-panel test.** That gate remains mandatory only for `dd_protection`-class Pareto sweeps (per the same-day scope ratification) and uses a different acceptance floor. Deliberately different name, deliberately different jurisdiction.
6. Treating passage through this battery as deployment authorization, or reclassifying a survivor as Req-1a-authorized for the S5 bounded sandbox-up lane or any lifecycle-promotion privilege gated on named-mechanism status.
7. Computing DSR/cost-law/split-DSR on data the mining pass already read — i.e., skipping the mandatory frozen train/confirm partition.
8. Citing MSL's R-CHANNEL/R-FRAMING/R-REQSCOPE elections as authority for this channel — they govern MSL composition only; this channel is not MSL.

---

## §6 — Consequences

**Positive:** names a candidate class (no-counterparty statistical/geometric patterns) that MSL structurally cannot carry and that the dead-door evidence shows a Req-1a relaxation would not have helped either — closing the actual gap rather than loosening the wrong gate. Reuses existing machinery end-to-end (K-accounting, DSR, cost-law, N-SURV); invents nothing except the mandatory `--prereg` + frozen train/confirm partition for this channel specifically, both of which are tightenings, not loosenings, relative to the blind lane's normal default. Races MSL's real, closer falsifier clock (≈2026-10-07) rather than an unrelated, farther one.

**Negative / watched:** the SPA/PBO universe-level correction being dormant (W4) means this channel's multiplicity control is genuinely weaker than the repo's own stated ideal for large searches — disclosed explicitly (§2 item 4) rather than papered over, and the frozen train/confirm partition is the load-bearing compensating control, not a decoration. The "own-series half-split DSR check" deliberately mirrors the canonical regime-robustness gate's shape and could be mistaken for it despite the rename — Forbidden move 5 exists specifically because this repo has a same-day precedent (the "Board-lite" finding) for exactly this kind of name-collision drift. The channel-boundary test ("does the candidate's own claim name a counterparty") is verifiable only at authoring time; Forbidden move 3's omission clause narrows but does not eliminate this risk — a future audit should watch for it.

---

## §7 — Implementation plan

- **Phase 0** — §0 reads (done, this ADR).
- **Phase 1** — this ADR ships as the channel's charter; no code changes required (the `--lane blind` pipeline, `register_search`, and `axis_screen.py` machinery already exist and are unmodified).
- **Phase 2** — first candidate sourced under this channel must open with `register_search open --lane blind --prereg <file>` naming the frozen train/confirm split before any mining runs.
- **Phase 3** — verification block below, run at authoring time and at the 2026-11-08 falsifier check.

---

## §10 — Audit hooks (runnable, next quarterly check — 2026-11-08)

```bash
# Has any candidate been sourced under this channel yet? (AMBIGUOUS-HOLD check)
grep -rl "no-counterparty-statistical-sourcing-channel\|2026-08-15-no-counterparty" discovery_manifests/ lab/analysis/ 2>/dev/null

# Battery-closure tally — any zero-survivor closures logged?
grep -rn "battery-closure\|zero-survivor closure" docs/rejected_candidates.md ops/instruments/*.md 2>/dev/null

# MSL's real falsifier clock (Rung B, ~2026-10-07) — has it fired independently of this channel?
grep -n "Rung B\|FALSIFIED" docs/adr/2026-08-14-msl-yield-falsifier-survival-limb.md

# Req-1a is still untouched for named-counterparty candidates (no scope creep)
grep -n "WHO pays" docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md

# No candidate from this channel cites Req 2 as its no-transplant authority (Forbidden move 4)
grep -rln "Req 2" docs/briefs/ | xargs grep -l "no-counterparty\|blind lane" 2>/dev/null
# Expected: empty

# N-SURV / dd_protection untouched
grep -n "eval_bust_ceiling\|DD_TRIGGER\|DD_SCALE" lab/research_utils/nsurv_channel.py core/dd_protection.py

# Consecutive-pre-G0-kill threshold (N=3) — canonical count line present; not still "uncovered"
grep -n "Running consecutive pre-G0 kill count (canonical)" docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md
# Expected: one canonical line. Generation-dry fires at count == 3.

# Threshold must not still read as an open election
grep -n "currently uncovered" docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md
# Expected: only the historical pre-G0-addendum sentence, immediately followed by a Discharged pointer.
```

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md --type adr
python scripts/check_adr_graph.py --regenerate-index
python scripts/check_adr_graph.py
```

---

## Addendum 2026-08-15 — Declared-K ceiling at open (K ≤ 3)

**Status:** ratified same day by operator ("add the K cap addendum to the ADR"). **Tightening only** — nothing in §2 is withdrawn or loosened; this addendum adds a refusal condition that did not previously exist. No live-risk surface touched. $0 / K=0.

### The gap this closes

§2 requires DSR ≥ 0.95 at the declared K but placed no ceiling on K **at open**. The mechanism-first lane refuses an open when `floor_at_k(K) > Cap` (K ≥ 4); the blind lane this channel runs in has **no admission gate at all** (`SKILL.md`: "blind opens stay unbound by design"). So as originally written, a wide mine would open cleanly, consume compute and bank family K, and only die later at DSR — an expensive death the mechanism-first lane catches for free at open. The asymmetry was unintended.

### Measured arithmetic (computed 2026-08-15, `lab/research_utils/axis_screen.py::floor_at_k`)

| K | required annualized Sharpe (DSR ≥ 0.95, V=1/n) | vs Cap 1.00 | vs best in-house edge 1.83 |
|---:|---:|---|---|
| 1 | 0.650 | clears | clears |
| 2 | 0.850 | clears | clears |
| 3 | 0.980 | clears | clears |
| 5 | 1.115 | **over** | clears |
| 22 (catch22 face) | 1.410 | over | clears |
| 441 | 1.830 | over | **at the ceiling** |
| 3,260 (STUMPY, 50/50 split, ~106k-bar M15 panel) | 2.050 | over | **unreachable** |
| 6,499 (STUMPY, full panel) | 2.120 | over | **unreachable** |

> ⚠ **APPENDED CORRECTION 2026-08-15 (same day, operator-raised — not a strike; the table above stands unedited and D-K1/D-K2/D-K3 are unaffected).**
> **The fourth column carries only ONE of M-19's two required anchors, and the word "unreachable" overstates what it licenses.**
> [M-19](../methodology/lessons/methodology_lessons.md) mandates benchmarking a floor against **both** *(a)* the best in-house validated
> edge (Aegis **1.83**; all four locked legs 1.11–1.83) **and** *(b)* the corrected published top-decile net single-strategy Sharpe
> (**S_B 0.85**, median single-strategy ~0.3–0.5) — and its rule fires only when *"the floor exceeds **both**."* M-19's own K-sweep gives
> all three anchor crossings: floor ≤ Aegis needs **K ≤ 441**; ≤ Guardian **K ≤ 33**; ≤ **typical-corrected-anomaly (~1.0) K ≤ 3**.
>
> Consequences for reading this table:
> 1. **K ≤ 3 is not "barely survivable" — it is the band calibrated to the corrected-literature anchor.** `CAP = 1.0` sits at M-19's
>    typical-corrected-anomaly crossing by construction, not by coincidence. A K ≤ 3 candidate must be top-decile-published quality;
>    that is demanding and entirely ordinary, **not** "better than anything ever achieved."
> 2. **Aegis 1.83 cannot bound a novel candidate's achievable Sharpe.** It is cohort-bound to (Aegis · USDJPY · 15m · Pepperstone CFD ·
>    that panel), its **K was never declared**, and it is **un-deflated** — so it is not placeable on the DSR axis at all, and comparing it
>    to a K-corrected floor is the same-units defect the [harvest ADR](2026-07-16-harv-attestation-same-units-supersession.md) records as
>    having killed D5 and H-OD-1. Annualized Sharpe also scales with √(trades/yr), so a construct class with a different trade count is not
>    bounded by what a 15m swing strategy achieved.
> 3. **What is genuinely foreclosed is unchanged**: K in the thousands requires ≈2.4× the corrected published top decile, which exceeds
>    *both* anchors and is dead by M-19's own rule. The addendum's decision stands on that, not on the 1.83 comparison.
>
> **Relocated constraint, recorded here because this is where the reader meets it:** the operative bound on search size is `CAP = 1.0`
> (`axis_screen.py:31`), not the in-house edge. Whether Cap belongs at 1.0 or 2.0 is a **recorded open question** — the
> [2026-08-03 gate-stack audit](../notes/audits/programme-audit/2026-08-03-gate-stack-audit.md) §5.4 lists it under what it *cannot*
> establish, naming D6 (floor 1.835) and D2-low (1.925) as the axes that would price the counterfactual. Opened as
> [`Q-CAPBAND-1`](../briefs/Q-CAPBAND-1-cap-band-counterfactual.md) — **which prices the counterfactual and does not propose a Cap change.**

Two properties of this table are load-bearing and were verified, not assumed:

1. **The floor is set by K, not by n.** Re-computed per-frequency across {0.5, 1, 2, 4} trades/day, the floor is flat to ±0.005 (e.g. K=441 → 1.835/1.830/1.830/1.830). This reproduces M-19's own finding — *"The floor is set by K, not n (robust across trade-frequency 0.5–4/day; more data does not help)"* ([`methodology_lessons.md`](../methodology/lessons/methodology_lessons.md) M-19). **Trade frequency is not a lever on the floor.** (It remains a lever on *power* — ADR 2026-07-12's n ≥ 500 requirement — which is a different quantity; do not conflate them.)
2. **A train/confirm split does not rescue a wide mine.** Halving T moves the STUMPY-class floor only 2.120 → 2.050, because K enters the floor logarithmically. Splitting is a bias control, not a K control.

### Decision

**D-K1 — Declared-K ceiling.** A `register_search open` under this channel must declare a K for which `floor_at_k(K) ≤ CAP` (`CAP = 1.0`, frozen at `axis_screen.py:31`) — i.e. **K ≤ 3** at the current frozen constants. An open declaring K ≥ 4 is **refused**, mirroring the mechanism-first lane's existing refusal rather than inventing a new threshold. The ceiling is expressed as the *predicate* (`floor_at_k(K) ≤ CAP`), not the literal 3, so it tracks the frozen constants if they ever move by ADR.

**D-K2 — Bracket disclosure.** The pre-registration must report the K bracket `{binding, raw}` per ADR 2026-07-12 §2.1 — "never report only the value that happens to pass." A construct whose honest raw count exceeds its binding floor must show both.

**D-K3 — The ceiling is a channel property, not a candidate property.** It may not be waived per-candidate by argument. Widening it requires a superseding ADR that re-derives the Cap, not a per-run exception.

### What this forecloses, stated plainly

**Wide matrix-profile / full-tsfresh / deep-symbolic-regression mining is not fundable in this channel** at the current frozen constants — not "discouraged," arithmetically refused at open. This is the same wall M-19 already recorded (*"the realistic-and-demonstrable band was therefore empty at the banked K"*); this addendum makes the channel refuse it at the cheapest possible moment instead of discovering it after the spend. The channel's viable candidates are **K ≤ 3 fully pre-specified constructs**, where every parameter is fixed in the `--prereg` before the mining pass runs and no parameter is searched.

### Consequence for §4's falsifier

Unchanged in wording, sharper in meaning: if the channel's `AMBIGUOUS-HOLD` branch (zero candidates *sourced*) fires at 2026-11-08 because no K ≤ 3 construct could be authored at all, that is itself the informative result — it would mean the no-counterparty channel is viable only in a band too narrow to populate, which is a finding about the channel and should be recorded as such rather than treated as a null.

### Forbidden moves added by this addendum

- Declaring an artificially low K at open that does not honestly count the search actually performed (K under-declaration is the same defect as K inflation, in the direction that flatters).
- Splitting one logical search into several sub-K-3 opens to evade the ceiling — the ceiling binds the *search*, not the invocation count.
- Reading D-K1 as licensing a K ≤ 3 construct that was in fact *selected* from a wider informal exploration; the wider exploration is the K.

| Date | Change | By |
|---|---|---|
| 2026-08-15 | Addendum: declared-K ceiling at open (`floor_at_k(K) ≤ CAP` ⇒ K ≤ 3), bracket disclosure, no per-candidate waiver. Closes the blind-lane no-admission-gate asymmetry. Tightening only; §2 unmodified. Verified floor-vs-frequency flatness and the split-does-not-rescue property by direct computation. | Joshua (operator direction) + Claude Code |

---

## Addendum 2026-08-15 — A pre-G0 kill is not a §4 strike

**Status:** ratified by operator (JA) 2026-08-15, in-session ("a pre-G0 kill is not a §4 strike — record that ruling"). Resolves the definitional gap surfaced by `MNQ-ANALOGUE-1` and flagged, unadjudicated, in notice (`git show dea3af9:docs/notes/notice/N-2026-08-15-blind-channel-cost-geometry-and-first-candidate-kill.md` — private-class, not in the public seed) §4 and STATE queue row 3. **$0 / K=0.** No live-risk surface.

### Ruling

**A candidate killed at a pre-G0 cheap falsifier — before `register_search open`, with no manifest written and no Q-ID spent — does not count as a strike against §4.** It is neither `FALSIFIED` (which requires a candidate to have *reached battery-closure*) nor evidence against `AMBIGUOUS-HOLD` (which asks whether candidates were sourced at all).

### Why the boundary is principled, not merely convenient

The distinction is what got tested. The four battery stages (cost-law, K-cap, DSR, own-series split) test **the candidate's economics** — they are the channel's substantive claim. A pre-G0 cheap falsifier tests something upstream: **whether the candidate is worth running the battery on at all.** "We never ran the battery" is a different epistemic state from "we ran the battery and it failed," and only the latter is evidence about whether the channel can produce a survivor.

Worked instance: `MNQ-ANALOGUE-1` died because its 1-NN analogue direction rule carried **no forward information** (leave-one-out hit rate 0.5160 against a 0.5453 base rate, session-block CI straddling zero). That is a finding about one construct's information content, measured on train, at $0. It says nothing about whether a *different* K≤3 construct could clear the battery — which is precisely what §4's hypothesis is about.

This also matches standing precedent: the 2026-08-10 dense-1m cell #3 died at a cheap falsifier "at $0; **no G0 authored, no Q-ID spent**" and was recorded as a falsifier kill, not a campaign closure.

### ⚠ The exposure this creates, named rather than left implicit

**This ruling makes §4 harder to fire.** Combined with the ratified `AMBIGUOUS-HOLD` branch, a channel in which *every* candidate dies pre-G0 would run indefinitely with its falsifier never advancing — the same "absorb unbounded cheap deaths without reaching strike one" shape that the [2026-08-03 gate-stack audit](../notes/audits/programme-audit/2026-08-03-gate-stack-audit.md) found in harvest-intake's §4 routing exemption, and that this ADR's own K-cap addendum closed *for battery-closure* by defining death at any named stage as a strike. It is adjacent to programme-audit **degeneration signal #3** (falsifier thresholds drifting toward "we'd never hit this anyway").

The ruling is still correct on its merits — the alternative (counting pre-G0 kills as strikes) would fire the falsifier on evidence that does not bear on its hypothesis, which is the mirror-image defect. But the exposure is real and must not be discovered later as a surprise.

**Mandatory disclosure (ratified with this ruling):** every pre-G0 kill in this channel is **counted and disclosed** in the channel's record even though it strikes nothing. The count is reported at each quarterly audit alongside the §4 reading, so "the falsifier never fired" can never be read as "the channel was productive." Running count as of this addendum: **1** (`MNQ-ANALOGUE-1`, 2026-08-15).

**Open, NOT ratified here — flagged for operator election:** whether a threshold on *consecutive pre-G0 kills* should trigger a disposition of its own (e.g. N consecutive ⇒ the channel reports generation-dry at the quarterly audit irrespective of §4). This addendum deliberately does not invent that threshold; it records that the gap exists and is currently uncovered.

> **Discharged 2026-08-15** by the [N=3 addendum](#addendum-2026-08-15--consecutive-pre-g0-kill-threshold-n--3) below. The paragraph above is the historical flag, not current state.

### Forbidden moves added

- **Re-classifying a battery-stage death as "pre-G0" to dodge a strike.** The boundary is `register_search open`: once a manifest exists, death at any of the four named stages is a battery-closure strike per the K-cap addendum, unchanged.
- Reporting a §4 reading without the accompanying pre-G0 kill count.
- Reading this addendum as licensing an unbounded series of pre-G0 kills as costless — each is $0 in spend but not free in calendar, and the 2026-11-08 clock does not pause.

### What is unchanged

The K-cap addendum's battery-closure definition (death at **any** named stage = one strike) stands untouched. §2's battery, §4's three branches, and the 2026-11-08 date are unmodified.

| Date | Change | By |
|---|---|---|
| 2026-08-15 | Addendum: pre-G0 cheap-falsifier kills are not §4 strikes; boundary is `register_search open`. Mandatory pre-G0 kill counting + disclosure ratified alongside. Names the falsifier-weakening exposure and the uncovered consecutive-kill threshold as an open operator item, not self-adjudicated. Battery-closure definition untouched. | Joshua (operator ruling) + Claude Code |

---

## Addendum 2026-08-15 — Consecutive-pre-G0-kill threshold (N = 3)

**Status:** ratified by operator (JA) 2026-08-15 via accepted plan election ("N = 3" + counting machinery (a)–(d); not light). Discharges the open item the [pre-G0 addendum](#addendum-2026-08-15--a-pre-g0-kill-is-not-a-4-strike) flagged and deliberately left unratified. **Limb 4** of the [ceremony-tiering ADR](2026-08-08-adr-ceremony-tiering.md) fires (creates a disposition-bearing falsifier threshold). Amend-in-place on this file — same form as the K-cap and pre-G0 addenda; not a sibling ADR; not a light record. **$0 / K=0.** No live-risk surface. `CAP` / `DSR_MIN` / `axis_screen.py` untouched.

### Rule 0 reads (this addendum)

- This file @ `ab303d07` (2026-08-15) — pre-G0 addendum L230–268: kill ≠ §4 strike; mandatory count; running count **1**; threshold "Open, NOT ratified here."
- [`2026-08-08-adr-ceremony-tiering.md`](2026-08-08-adr-ceremony-tiering.md) @ `91e6caad` — limb 4 ("creates or amends doctrine… falsifier threshold"); 08-14 addendum banks two light-that-should-have-been-full records as a candidate incident against the two-incident `FALSIFIED` threshold; 08-15 addendum: amend-in-place beats a sibling.
- [`STATE.md`](../../STATE.md) @ `fd251e3b` — decision-index line still said "Consecutive-kill threshold left uncovered"; operator queue is rows 0–2 (the pre-G0 addendum's "STATE queue row 3" pointer is already gone).
- [`docs/SESSIONS.md`](../SESSIONS.md) top Open/next (2026-08-15i) — same uncovered item.
- Amendment-first search (no sibling minted): `lab/CATALOG.md` / `docs/briefs/INDEX.md` / `docs/rejected_candidates.md` have no N=3 election; `check_advisor_dedup.py --keywords "blind channel consecutive pre-G0 kill threshold N=3"` returned no slug and only keyword-overlap on unrelated audits. Owner is this ADR.

### Ruling

**N = 3 consecutive countable pre-G0 kills ⇒ the channel reports generation-dry at the next quarterly programme audit, irrespective of §4.**

N is a channel property. It may not be waived per-candidate. Changing N requires a superseding addendum on this file, not a per-run exception.

### Why 3, not 6

Each countable kill is a **distinct construct**, not a noisy draw. Variants are barred from counting separately (D-K1: the wider exploration is the K). Three distinct constructs dead at the information screen is class evidence.

The disposition is an audit report, not a channel close — a premature firing costs almost nothing; a late one lets the channel absorb calendar silently (the exposure the pre-G0 addendum already names).

MSL's 6-count is a different cohort (post-G0 freezes without Pine, later-stage, across families). Borrowing it imports a number without its denominator.

Count is already 1. N = 6 would almost certainly never fire before the 2026-11-08 §4 reading — a decorative threshold ([`lesson_gate_reachability_preregistration`](../methodology/lessons/methodology_lessons.md)). N = 3 fires after two more distinct kills.

### Counting machinery (without this, N is unbinding)

**(a) Authoritative surface.** The running-count line in this addendum is canonical. `STATE.md` is a mirror only. STATE rows are deleted when items close; do not treat a missing STATE row as a reset or as "the count was never kept."

**(b) What increments.** A **distinct construct** killed at an **executed** pre-G0 cheap falsifier (information screen and/or cost-law arithmetic, before `register_search open`), recorded on a dated surface. On this public seed, `docs/notes/notice/` is excluded (PR #5); the public recording surface is a dated paragraph on this ADR, optionally plus a `git show <sha>:docs/notes/notice/…` pointer if the notice lives only in the private archive. **Do not increment for:** a `register_search open` refused because declared K ≥ 4 / `floor_at_k(K) > CAP`; a variant, retune, transplant, or relabel of a prior construct (D-K1 — the wider exploration is the K); a naming-pass that never executes a screen (no construct was specified, so nothing was killed).

**(c) What resets "consecutive".** A candidate that **survives** its pre-G0 screen **and** opens a manifest (`register_search open --lane blind --prereg …`). A battery-closure strike after that open is a §4 strike (K-cap addendum), not a pre-G0 increment, and it **does** reset the consecutive pre-G0 count because a candidate was sourced.

**(d) Disposition when N fires.** At the next quarterly programme audit, report **generation-dry** alongside the §4 reading and the pre-G0 kill count. This is **not** `FALSIFIED` (the battery never ran on those kills). It is **not** a license to open a third sourcing channel (§3: if this channel also falsifies, the fallback is the source-class post-mortem, not a third door). §4's three branches and the 2026-11-08 date are unmodified: zero *sourced* candidates by that date remains `AMBIGUOUS-HOLD` (re-test 2027-02-08). Generation-dry and `AMBIGUOUS-HOLD` can both be true at once; they answer different questions (can we even name constructs worth screening vs. did any sourced candidate survive the battery).

**Running consecutive pre-G0 kill count (canonical):** 1 / 3 (`MNQ-ANALOGUE-1`, 2026-08-15).

| # | Construct | Date | Recording surface | Increments? |
|---|---|---|---|---|
| 1 | `MNQ-ANALOGUE-1` | 2026-08-15 | `git show dea3af9:docs/notes/notice/N-2026-08-15-blind-channel-cost-geometry-and-first-candidate-kill.md` | yes — executed pre-G0 information screen |

### Named exposure

This threshold makes the pre-G0-≠-strike ruling **reachable**. It does not make cheap kills free: each still burns calendar toward 2026-11-08. It does not convert pre-G0 deaths into §4 strikes — that would fire §4 on evidence that does not bear on its hypothesis (the mirror-image defect the pre-G0 addendum already refused).

### Forbidden moves added

- Writing a light record (or a sibling ADR) for this threshold to dodge limb 4. The 08-14 ceremony-tiering addendum already banks two such incidents as a candidate against that ADR's two-incident `FALSIFIED` threshold.
- Incrementing the count for a K ≥ 4 refusal, a retune/variant, or a naming-pass with no executed screen.
- Resetting "consecutive" on anything other than a manifest-opening survivor (including on a STATE row deletion).
- Reading generation-dry as `FALSIFIED` or as authority for a third channel.
- Reporting a §4 reading after this addendum without both the pre-G0 kill count **and** whether N has fired.

### What is unchanged

§2's battery, §4's three branches, the 2026-11-08 date, the K-cap addendum (D-K1/D-K2/D-K3), and the pre-G0-≠-strike ruling (boundary still `register_search open`) are unmodified.

| Date | Change | By |
|---|---|---|
| 2026-08-15 | Addendum: consecutive-pre-G0-kill threshold N = 3; counting machinery (a) canonical ADR line (b) increment = distinct construct + executed pre-G0 screen (c) reset = manifest open (d) generation-dry at next quarterly audit, not FALSIFIED, no third channel. Running count 1/3. Limb 4; amend-in-place; not light. | Joshua (plan election) + Cursor |

---

## Addendum 2026-08-15 — First post-election generation attempt: naming set empty

**Status:** recorded 2026-08-15. This is a **dated finding**, not a new threshold. It executes the one generation attempt the N=3 addendum's reachability argument assumed, then stops. **$0 / K=0.** No screen executed. No manifest. No Q-ID. Count **unchanged at 1/3** — a naming-pass is not a kill (N=3 addendum (b)). No Databento pull (would need a cost dry-run + separate GO; this packet stayed on the frozen `$0` posture).

### Rule 0 reads (this addendum)

- This file's N=3 addendum (same commit-parent) — (b) does not increment for a naming-pass with no executed screen; (d) generation-dry is **not** this outcome.
- [`2026-08-15-analogue-modality-route-ruling.md`](2026-08-15-analogue-modality-route-ruling.md) @ `ab303d07` — analogue **class** still live; first candidate dead; CON-5 pause lifted for this class only; θ-parameterised entry-geometry stays paused; relabel forbidden.
- [`Q-TNEC-CON-5-closure-ambiguous-hold.md`](../briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md) — Branch A STOP; dense-1m OHLCV temporal-selectivity default **paused**.
- [`rejected_candidates.md`](../rejected_candidates.md) L718–743 — index raised bar `index-intraday-ohlcv-directional-timing-2026-07-21`; route ① is outside mapped levers or a new modality.
- Channel ADR §5 forbidden move 3 — do not route a nameable-counterparty candidate here by omission.
- Feasible cell (kill notice, `git show dea3af9:docs/notes/notice/N-2026-08-15-blind-channel-cost-geometry-and-first-candidate-kill.md`): **MNQ RTH, once-per-session-class**. Not re-derived.

### The attempt

The channel's viable set is K ≤ 3 fully pre-specified constructs. One distinct write-up was authorized. Every door that could have produced one was walked against standing bars **before** any look at returns. None cleared. No construct was named, so no information screen was run (running one would have required picking a rule — that pick is the K).

| Door | Why it does not yield a nameable construct this packet |
|---|---|
| Retune `MNQ-ANALOGUE-1` (k, window, distance, embedding) | D-K1 — the wider exploration is the K. Sequential search after seeing the kill. |
| Same analogue on MGC / MYM / M2K / MCL | Forbidden move 4 (no instrument hop); also outside the $0 feasible cell. |
| A second analogue algorithm without an independent a-priori justification | Same sequential-search defect. "Try DTW / centroid / a different embedding because 1-NN died" is shopping. |
| CON-1…CON-5 sibling or θ-parameterised entry-geometry | CON-5 pause; analogue-modality test is *absence* of named entry geometry, not the word. |
| Dense-1m OHLCV temporal-selectivity | Branch A pause stands (U0). |
| Once-per-session lagged-return / 1-day TSMOM | Harvest Path 1b (momentum-class). Routing it here by omitting the story is forbidden move 3. Also classic single-instrument index OHLCV directional timing. |
| catch22 / ruptures / HMM / PySR as the direction rule | Tool-discipline: covariates or conditioning variables, or K explodes past 3. A one-feature catch22 pick after looking is K = 22. |
| Other instruments / new series | $0 feasible cell is MNQ RTH. New Databento data needs a cost dry-run + separate GO — not authorized here. |

### Disposition

**Stop generating this session.** Count stays **1/3**. N has **not** fired. This is **not** generation-dry.

Zero *sourced* candidates by 2026-11-08 remains §4 `AMBIGUOUS-HOLD` (re-test 2027-02-08). That trajectory is accepted as first-class: the K-cap addendum already said an empty-through-11-08 outcome would mean the channel is viable only in a band too narrow to populate.

The [analogue-modality ruling](2026-08-15-analogue-modality-route-ruling.md)'s own re-test still rides 2026-11-08 ("if no algorithmic-analogue construct ever opens a manifest, this ruling was inert"). This attempt makes that reading more likely; it does not retire the ruling early.

### Forbidden moves this finding does not license

- Treating this empty naming-pass as a second countable kill.
- Treating it as generation-dry (N = 3 not reached).
- Immediately authoring a sibling analogue "to have something to screen."
- Opening `register_search` so the emptiness "counts" as a §4 strike.
- Re-opening Cap / waiving K ≤ 3 on the back of this dryness (Q-CAPBAND-1 forbidden move 5).

| Date | Change | By |
|---|---|---|
| 2026-08-15 | Addendum: one post-election generation attempt; naming set empty against standing bars; no screen; count remains 1/3; stop generating; AMBIGUOUS-HOLD trajectory accepted; not generation-dry. | Cursor (plan execution) |
