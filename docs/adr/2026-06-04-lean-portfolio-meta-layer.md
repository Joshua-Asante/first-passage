# ADR 2026-06-04 — Lean Portfolio Meta-Layer Over SCRUM Delivery

> ⚠ **DISCHARGE ADDENDUM 2026-08-14 — §4 falsifier FIRED 2026-07-30; meta-layer DORMANT / CEREMONIAL.**
>
> **(a) Limb and retiring event.** §4 pre-registered: *"if at 8 weeks no allocation
> decision references realized ECR … the meta-layer is **ceremonial** and is
> deleted."* Eight weeks from 2026-06-04 expired **2026-07-30** (15 days expired
> as of this addendum).
>
> **(b) Why the input can no longer accrue.** No allocation decision referenced
> realized ECR. After the ECR engine (`journal_review.py`) was retired 2026-07-11
> with the CFD estate, none structurally could. The condition fired in its
> strongest form: not "did not happen" but "could not happen".
>
> **(c) Re-arm.** The allocation meta-layer re-arms only if a producing
> edge-captured-ratio surface exists again **and** an allocation decision
> actually cites it. Absent both, allocation reverts to OODA + ad-hoc, as §4
> prescribes.
>
> **(d) Surviving coverage / why this is not a deletion.** Two ratified ADRs
> cite this file as parent doctrine —
> [`2026-06-05-concept-admissibility`](2026-06-05-concept-admissibility.md) and
> [`2026-06-12-three-loop-methodology-binding`](2026-06-12-three-loop-methodology-binding.md).
> Deleting the parent would strand both. The **meta-layer as an allocation
> apparatus is dormant/ceremonial**; the **three-loop hierarchy that descends
> from it is live and independently ratified**. Historical decision text below
> is byte-unedited (Trap #12 / Rule 14 frozen-artifact convention).
>
> **Status recorded by this addendum:** CEREMONIAL-BY-OWN-FALSIFIER. Not
> `Superseded` — no successor decision replaces it; its own gate retired it.
> Header `Status: Accepted` / `Superseded-by: none` below are the 2026-06-04
> ratification record and stay unedited.

**Status:** Accepted - ratified 2026-06-04 by PO (Joshua); Rule-0 anchors confirmed on-disk (see blockquote header below for the full ratification note).
**Decision date:** 2026-06-04
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

> **Status:** ACCEPTED 2026-06-04 — §0 confirmed on-disk; anchor 6 re-pointed, ADR landed. §0-NOTES resolved.
> **Date authored:** 2026-06-04 (rev. 4 — ACCEPTED; status flip staged by CC re-dispatch after §0-NOTES resolution. rev. 3 — §0 upgraded memory-tier → on-disk-confirmed via CC pass; anchor 6 re-pointed to real artifacts, phantom-note claim dropped; anchor 3 / §2.4 reworded: ECR engine assembled, production not yet running. rev. 2 — Copygram/ECR unified in §2.6; §7 reframed; §8 kill-switch added).
> **Author:** Claude (Tech Advisor) — drafted for PO (Joshua) review.
> **Supersedes / relates to:** allocation-refresh-2 ADR (2026-05-23); dd_protection C2 relock ADR (2026-05-08); 2026-04-29 operational-ground-truth audit.
> **Provenance note:** Built from the `brief-authoring` SKILL.md body discipline structure (§0/§1/§4/§5/§6/§10), **not** the canonical `references/adr.md` template, which is not accessible in the authoring environment. Diff against the canonical template and run `scripts/check_brief.py 2026-06-04-lean-portfolio-meta-layer.md --type adr` before lock.

---

## §0 — Rule 0: Production reads (CONFIRMED ON-DISK 2026-06-04)

Authored without direct repo access (anchors were memory-tier). Confirmed on-disk via the §0 CC confirmation pass on 2026-06-04 (NEEDS_CONTEXT return; five MATCH with cited commits, one anchor re-pointed below). Provenance is now **on-disk-confirmed** for anchors 1–5; anchor 6 corrected to point at the artifacts that carry its substance. This satisfies the on-disk > web > memory hierarchy for PROPOSED → ACCEPTED, pending the two PO actions in §0-NOTES.

| Claim this ADR relies on | On-disk confirmation | Provenance |
|---|---|---|
| Current allocation locks | DJ30 0.70%/750%, NAS100 0.37%/1000%; MC Pass 99.83 / Bust 0.17 / p99-DD 4.37 — allocation-refresh-2 ADR L72,74,82–87 | commit `5b8ff71` (2026-05-23) — **MATCH** |
| dd_protection guardrail | `DD_TRIGGER = 0.015`, `DD_SCALE = 0.40` — `dd_protection.py:50-51`; constants set by `dc75ffa` (2026-05-08); `0efdfba` (2026-06-04) touched only Notion-pointer comments | commit `dc75ffa` — **MATCH** |
| ECR engine state | ECR engine assembled & functional (`journal_review.py`, edge-captured-ratio logic; PR #100 ingest; counterfactual datasets in `live_journal/`). **Rolling-6-week production not yet running end-to-end** — no rolling runner, no `reports/` output, no live DXTrade fills (only test fixtures). Live-fills export in flight on `feat/dxtrade-notion-reconciler` (`dxtrade_pdf_to_csv.py`) | `live_journal/scripts/` — **MATCH** (wording corrected; §2.4 precondition holds — a *producing* ECR still doesn't exist) |
| Leakage measurement | "Execution leakage Apr 13–May 14: realized −$1,673 vs counterfactual +$7K–$20K" — `tweaks note:13`; ~50% corroborated `programme-audit:19` | **MATCH** |
| Behavioral falsifiers open | E1 PROMOTED 2026-04-29, E2 PROMOTED 2026-04-29, E3 CANDIDATE — none closed/retired — `execution_lessons.md:25,68,117` | **MATCH** |
| Live-vs-spec gap finding | Substance ("briefs reference projections; zero reference live state") confirmed on-disk: registry seeded 2026-04-29 (`execution_lessons.md:215`), `trade-capture design:25`; also the 7-week edge gap ~3%/$18K. **No discrete 04-29 audit note exists** — phrasing originated in the live-execution-journal skill framing, not a repo artifact. Anchor re-pointed to the real artifacts; the phantom-note claim is dropped | `execution_lessons.md:215`, `trade-capture design:25` — **substance-confirmed, re-pointed** |

**§0-NOTES — two PO actions, both RESOLVED 2026-06-04 (status flipped after both cleared):**
1. **Anchor 6 ruling applied:** re-pointed to real artifacts (not accepting skill-encoded provenance as a general standard — that would lower the post-`eb6d6db` on-disk bar; and not back-dating a note, which would manufacture provenance). The finding stands on `execution_lessons.md:215` + `trade-capture design:25`.
2. **ADR landed:** committed at `docs/adr/2026-06-04-lean-portfolio-meta-layer.md`. The `docs/adr/` convention is date-prefixed (`YYYY-MM-DD-title`) with no `NNN`/numeric-sequence pattern, so no number-assignment step applies.

**Window note (anti-conflation):** anchors 4 and 6 are *different* windows — Apr 13–May 14 (~50%, −$1,673 vs counterfactual) and the 7-week edge gap (~3%/$18K). Both confirmed; keep distinct downstream.

---

## §1 — Context & doctrine linkage

The operation runs two workstreams on two clocks. SCRUM (ADR-pending, prior turn) was adopted to govern the **build** workstream. This left an ungoverned layer *above* project management: how scarce resources are allocated across the whole operation, and how delivery feedback revises that allocation. This ADR installs that layer.

The framework is SAFe Lean Portfolio Management — value streams over projects, outcomes over outputs (OKRs), guardrails over micro-management (lean budgeting / Epic MVP funding). It is adopted as **recognition of structure already operating**, not new machinery. The discipline this ADR adds is naming the layers so they stop being conflated, and installing the one loop that makes the framework agile rather than waterfall.

Standing doctrine this connects to: `fxify-challenge` Core Principles (MC + dd_protection as the live-ops guardrails); `live-execution-journal` (ECR as the load-bearing falsifier); `programme-audit` (ceremonial-vs-load-bearing discipline); on-disk > web > memory provenance hierarchy; The Algorithm (delete → simplify → automate).

---

## §2 — Decision

Adopt a four-layer governance hierarchy. The top two layers (Strategic + Governance) are the meta-layer this ADR installs; the bottom two (Program + Team) are governed by the pending SCRUM ADR.

```
1. STRATEGIC      Self-funded life (~$10M NW, ~$20K/mo). Multi-firm prop scaling
                  as primary income + compounding vehicle. CTA track deprecated.
                          │
2. GOVERNANCE     ← META-LAYER (this ADR)
   (Lean Portfolio) Allocates two currencies across two value streams; sets
                    outcome measures (ECR); funds Epics at MVP budget; holds
                    the upward feedback loop that revises 1 from live data.
                          │
   ─────────────── delivery framework begins ───────────────
                          │
3. PROGRAM        Outer loop. Roadmap / dependency mapping across build tracks.
                  (Governed by pending SCRUM ADR.)
                          │
4. TEAM           Inner loop. Sprints, increments, conditional sync.
                  (Governed by pending SCRUM ADR.)
```

**2.1 — Two value streams, two currencies.** The framework's single-corporate-dollar assumption is adapted: this operation allocates two scarce resources with different guardrails, horizons, and falsifiers.

| | Operational value stream | Development value stream |
|---|---|---|
| **What it delivers** | Captured edge → P&L → compounding AUM | The platform that lets the operational stream scale |
| **Permanent tracks** | Guardian, Striker, Aegis, NAS100 v1 | Copygram pipeline, `multi_firm_operations`, methodology infra |
| **Currency allocated** | Real capital | Attention / hours |
| **Clock** | Continuous / daily | Build (2-week sprint) |
| **Governing loop** | OODA + `live-execution-journal` | SCRUM |
| **Lean budget / guardrails** | MC framework + allocation ADRs + dd_protection C2 | Epic MVP budget (Copygram = current Epic) |
| **Outcome measure** | ECR (rolling 6-week) | Downstream ECR delta it enables — not features shipped |

**2.2 — Value streams over projects.** The four strategies are not projects; they are permanent tracks. Capital flows to them; they are not assembled-and-disbanded. Q-CORR-1 closing Degenerating and Guardian-on-XAGUSD routed to rejected-candidates is the framework's "hypothesis failed → pivot early" already in practice on real capital.

**2.3 — Outcomes over outputs.** Success is measured by ECR (outcome), not by "ADR authored on time" or "feature shipped" (output). The development stream earns attention only by the operational-stream ECR delta it produces. This is the 2026-04-29 audit finding (briefs reference projections, zero reference live state) installed as a governance rule rather than a recurring lesson.

**2.4 — The upward loop is the agility mechanism, and it is currently broken.** What separates this framework from Water-Scrum-Fall is one loop: realized live data revises capital allocation. That loop's load-bearing artifact is a **producing** rolling 6-week ECR. The engine is assembled and functional (`journal_review.py` with edge-captured-ratio logic, PR #100 ingest, counterfactual datasets) — but it is **not yet producing end-to-end**: no rolling-6-week runner, no `reports/` output, and no live DXTrade fills to drive it (that export is in flight on `feat/dxtrade-notion-reconciler`). Until ECR is *producing*, the strategic layer allocates on MC projection, not realized edge — the live-vs-spec gap at portfolio scale. Therefore:

> **ECR assembly is the precondition for any strategic-layer pivot.** No capital reallocation may claim to be data-driven until rolling 6-week ECR is producing. Until then, allocation changes are explicitly projection-driven and labelled as such.
>
> **Tightened by §2.6:** the same instrument now also gates automation trust. **No automated execution path is trusted with size until ECR verifies that path reproduced its strategy's backtest signal.** Pivot-precondition and automation-acceptance are the same discipline at two scales.

**2.5 — Single-operator role collapse.** Strategic + Governance + PO collapse into one person. In an enterprise, that separation is an epistemic check — executives *cannot* micromanage, so they must trust bottom-up data. Here, the substitute for that forced separation is the provenance/audit discipline (on-disk > web > memory; session-assertion; `programme-audit`). The meta-layer's job is therefore not coordinating people — it is coordinating one operator's attention across two value streams, and specifically preventing the high-engagement development stream from cannibalizing the operational one.

**2.6 — Copygram and ECR are one operational-stream objective (supersedes the §7 tradeoff framing).** The original §7 framed Copygram and ECR as competing for attention. That was wrong, and this subsection corrects it. The measured ~50% leakage is overwhelmingly *behavioral* — signal skips (E1), anticipation entries before bar-close (E2), hand-sizing drift, out-of-envelope trades, timing slippage. Every one is a human-in-the-loop failure. Automation does not *measure-and-correct* those; it *eliminates the loop they live in*. A webhook does not skip a signal, size by feel, or enter early. For the behavioral categories, automation is therefore a **structural** fix, not an incremental one — which is exactly why Copygram serves the operational stream's outcome (gap closure) rather than competing with it.

This **upgrades ECR's role rather than deprecating it.** ECR stops being a behavioral coach for a human and becomes the **acceptance test for the automation**: the instrument that determines whether the automated path actually reproduced the backtest signal. Copygram is the *output*; gap-closure is the *outcome*; ECR is the only thing that distinguishes them — a clean instance of §2.3.

Three rules follow, and they are load-bearing:

1. **Sequencing is per-strategy, not build-then-measure.** For each strategy: automate → ECR-verify that strategy's automated path reproduces its backtest → only then trust it with size. Automation done wrong *introduces* gaps (see open Copygram items: unverified close-all-by-symbol, two unverified DXTrade ticker mappings). If close-all-by-symbol misfires on the pyramiders (Striker, NAS100), you have automated reliable *opens* and unreliable *closes* — a new gap, invisible precisely because the automation was trusted. **The pyramiding strategies are the high-risk path** and must not be sized up before ECR confirms their close logic.

2. **ECR runs NOW, on current manual trades, as the control.** Pre-Copygram ECR is the baseline the automated path must beat; post-Copygram ECR is the proof it did. Same instrument, two readings; the delta between them is the entire business case for the automation. This removes any "wait for Copygram to start measuring" sequencing — the control reading is available today.

3. **E1/E3 do not die at automation — they migrate to the kill switch.** E1 (macro-skip) and E3 (skip-rationale) were never about the entry mechanic; they were about *deciding not to take a signal*. Any discretionary override ("pause the bot before FOMC") rebuilds that exact decision point one layer up. Automation eliminates E1/E3 only to the degree discretion is not reintroduced at the override. This forces a conscious design decision — see §8.

---

## §3 — SCRUM nesting (delivery framework, governed below the meta-layer)

From the prior-turn SCRUM adoption, fixed here as it sits under the meta-layer:

- SCRUM governs the **development value stream only**. Firewalled from the trading clock.
- **Sprint Review** → DoD check + PO acceptance (no external stakeholders; no staged demo).
- **Sprint Retrospective** → maps onto existing `programme-audit` cadence + F-class/M-class lesson registry (not a new artifact).
- **Daily Scrum** → **conditional**: exists only on dates with active parallel build work to coordinate. Absent that, it is ceremony the programme-audit doctrine hunts.
- **Roles:** PO = Joshua. "Scrum Master" = Claude, but hybrid — the label must not strip the Tech Advisor advisory half. "Developers" = CC (Analyst/Tactical Ops, delegated) + Cursor (Engineering, self-organizing) — distinct functions, not interchangeable.
- **Product Backlog** = single ordered source of truth, to stand up in Notion Command Center.

---

## §4 — Falsifiable hypothesis

**H:** If this meta-layer is load-bearing, then within **8 weeks** of ACCEPTED status (a) rolling 6-week ECR is assembled and producing, AND (b) at least one capital-allocation OR attention-allocation decision is made that cites **realized ECR** as its basis rather than MC projection or feature-completion.

**Falsifier:** if at 8 weeks no allocation decision references realized ECR — i.e., the framework was adopted as vocabulary while allocation behavior is unchanged — the meta-layer is **ceremonial** and is deleted per The Algorithm, reverting to OODA + ad-hoc allocation.

This is binary and checkable. The form: *adopting SAFe-speak with zero behavioral delta is the failure mode, and this H detects exactly that.*

---

## §5 — Forbidden moves (genuinely tempting, ruled out)

1. **Forcing the operational stream into sprint cadence.** Tempting because the symmetry is clean. Forbidden: it colonizes the trading clock, which is continuous and regime-/shift-gated.
2. **Defining a "Definition of Done" or "shippable increment" for a trading week.** Category error — the operational increment is captured edge measured over a rolling window, not a shippable artifact.
3. **Letting Daily Scrum become a fixed daily ritual** absent active parallel build. Ceremony; see §3.
4. **Allocating real capital on MC projection alone once ECR exists.** Re-creates the 04-29 output-vs-outcome gap at portfolio scale. (Before ECR exists, projection-driven allocation is permitted but must be *labelled* projection-driven — §2.4.)
5. **Treating "ADR authored / feature shipped" as a success metric.** Output worship; the development stream's only success metric is operational-stream ECR delta.
6. **Adopting the framework as vocabulary with no behavioral change.** The deepest ceremony risk. §4's falsifier exists specifically to catch this.
7. **Claiming "it's automated, therefore the gap is closed."** Forbidden move #5 in automation's disguise — its most convincing costume. Automation makes gap-closure *plausible*; only ECR makes it *known*. No automated path is declared gap-closing on the basis of being automated; the claim requires an ECR reading (§2.6 rule 1).
8. **Reintroducing discretion at the kill switch without recognizing it rebuilds E1/E3.** A human pause-button override *is* E1/E3 with better tooling. Forbidden only in its *unexamined* form — the §8 open question forces the choice to be made consciously; making it consciously (even choosing a human pause) is permitted, sleepwalking into it is not.

---

## §6 — Gate / closure criteria

Evaluated at the 8-week mark (or sooner if ECR assembles early):

- **RESOLVED (Progressive):** ECR assembled AND ≥1 allocation decision cites realized ECR. Meta-layer is load-bearing; retain, fold review into `programme-audit` cadence.
- **FALSIFIED (Degenerating):** 8 weeks elapsed, no allocation decision references realized ECR. Delete the meta-layer; revert to OODA + ad-hoc allocation. Capture as a methodology lesson with dollar/counterfactual anchor.
- **AMBIGUOUS:** ECR assembled but no allocation decision yet *needed* one (no regime change, no drift signal). Hold; re-gate at +4 weeks. Do not amend criteria mid-window (anti-p-hack, brief-authoring trap 12).

**Per-strategy automation-acceptance gate (§2.6 rule 1, separate from the meta-layer gate above).** For each strategy independently, the automated path is trusted with size only when:
- ECR for that strategy's automated fills is within tolerance of its backtest signal (define the σ tolerance per strategy at acceptance time — do not leave as "close enough"), AND
- for the pyramiders (Striker, NAS100): close-all-by-symbol is independently verified to fire correctly, since automated reliable-open + unreliable-close is a *new* gap, not a closed one.

Until both conditions pass for a given strategy, that strategy runs at minimum size or stays manual. This gate is per-strategy and does not wait on the portfolio-level meta-layer gate.

---

## §7 — Consequences & the governance call this ADR forces

**Reframed by §2.6.** The earlier draft framed Copygram and ECR as competing for attention and called to reprioritize *away* from Copygram toward ECR. §2.6 corrects that: they are a **single operational-stream objective**, with ECR as Copygram's acceptance test. The §7 tension dissolves — in the operator's favor, since automation is a structural fix for the behavioral leakage that constitutes most of the ~50% gap.

What this ADR forces is therefore not a Copygram-vs-ECR reprioritization but a **sequencing and instrumentation discipline**:

1. **Assemble ECR now, on current manual trades** — it is the control reading and the baseline Copygram must beat (§2.6 rule 2). This does not wait on Copygram.
2. **Sequence automation per-strategy with ECR as the acceptance gate** (§2.6 rule 1, §6) — never build-all-then-measure; never size up a strategy before ECR confirms its automated path, pyramiders especially.
3. **Decide the kill-switch design consciously** before automation carries size (§8), because that decision determines whether E1/E3 survive automation or migrate intact to the override.

This is recorded as **decisions the ADR forces**, not recommendations to revisit later. The Water-Scrum-Fall failure this prevents is unchanged: without the ECR control reading, "Copygram closed the gap" is an unfalsifiable output claim, and a year of build could pass before the operator learns the automated path never reproduced the backtest.

---

## §8 — Open question this ADR forces (kill-switch design)

This ADR does not decide this — it forces it into the open as the one genuinely undecided thing in the automation design. It must be resolved before any automated path carries size.

**Q: Is the kill switch a hard circuit-breaker on coded conditions, or a human pause button?**

- **Hard circuit-breaker** — drawdown limits, news-window lockout coded in Pine / the pipeline. No discretionary decision point. E1 (macro-skip) and E3 (skip-rationale) are genuinely eliminated because there is no moment where a human decides not to take a signal.
- **Human pause button** — the operator can halt the bot (e.g., before FOMC). This rebuilds the exact E1/E3 decision point one layer up; the behavioral failures survive automation, better-tooled. Permitted *only if chosen consciously* with that cost acknowledged (§5 forbidden move #8).

**Routing:** this is a structural, low-reversibility design choice with a behavioral falsifier attached — it belongs in `inqhiori`, not OODA. Recommend opening a Pre-Q (e.g., Q-KILLSWITCH-1) before automation carries size. The falsifier is ready-made: if a human-pause design is chosen, ECR should show E1/E3-class leakage persisting at the override; a hard-circuit-breaker design should show it eliminated. ECR adjudicates the choice either way.

This question is the dependency gate on §6's per-strategy automation-acceptance: a strategy cannot be "trusted with size" (§2.6 rule 1) while the kill-switch design under which it runs is undecided.

---

## §10 — Audit hooks (runnable)

```bash
# 1. ECR precondition: does the rolling 6-week ECR script exist and produce output?
ls -la scripts/*ecr* 2>/dev/null && echo "EXISTS" || echo "MISSING — §2.4 precondition unmet"

# 2. Behavioral falsifier: is the H falsifier checkable — any allocation decision post-dating
#    this ADR that cites realized ECR (not MC projection)?
grep -rl "realized ECR\|ECR-driven\|edge-captured ratio" docs/adr/ docs/briefs/ \
  | xargs -r grep -l "2026-0[6-9]\|2026-1[0-2]" 2>/dev/null \
  || echo "NONE YET — H not yet satisfied"

# 3. Forbidden-move #2 guard: no 'Definition of Done' attached to a trading week
grep -ri "definition of done" docs/ | grep -i "trading\|week\|execution\|increment" \
  && echo "VIOLATION — forbidden move #2" || echo "clean"

# 4. Forbidden-move #3 guard: Daily Scrum entries only on dates with active build
#    (manual: cross-check daily-sync log dates against sprint-active dates)

# 5. Provenance: confirm §0 anchors were on-disk confirmed before lock
git log --oneline -1 -- docs/adr/*allocation-refresh-2* 2>/dev/null || echo "CONFIRM §0"

# 6. §2.6 control reading: is manual-trade ECR being produced NOW (pre-Copygram baseline)?
ls -la reports/ecr/*manual* 2>/dev/null && echo "BASELINE EXISTS" \
  || echo "MISSING — §2.6 rule 2 control reading not yet running"

# 7. Per-strategy automation gate: any strategy sized up on an automated path
#    without a recorded ECR acceptance reading? (§6 per-strategy gate, §2.6 rule 1)
#    (manual: cross-check each strategy's live size against its ECR acceptance artifact;
#     pyramiders Striker/NAS100 additionally require verified close-all-by-symbol)

# 8. §8 kill-switch dependency gate: is the design decided before any sized automation?
grep -rl "Q-KILLSWITCH\|kill.switch design\|circuit-breaker" docs/briefs/ docs/adr/ 2>/dev/null \
  && echo "DECISION TRACKED" \
  || echo "UNDECIDED — §8 gate blocks sized automation"
```

**Re-check cadence:** at 8-week gate (§6), then folded into `programme-audit` cycle. If two audit cycles pass without hook #2 ever firing, the meta-layer is decaying — flag in the next methodology audit (brief-authoring trap 10).

---

## Verification (run before declaring complete)

```bash
# Discipline checks (mechanical)
python scripts/check_brief.py docs/adr/2026-06-04-lean-portfolio-meta-layer.md --type adr
# Expected: all 6 checks PASS

# §0 confirmation pass (REQUIRED — moves PROPOSED → ACCEPTED)
cat docs/adr/*allocation-refresh-2*    # confirm allocation figures
cat <dd_protection config path>        # confirm C2 1.5%/0.40×
ls -la scripts/*ecr*                    # confirm ECR script state
```
