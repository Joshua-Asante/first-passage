---
name: ooda-loop
description: Tempo loop for tactical, recoverable decisions where speed matters more than rigor. Trigger on live trade management, daily dd_protection calls, intra-session adjustments, multi-firm prop sequencing, broker ops, market-condition responses, FIRE-alert handling, and any "should I take/close this" or "what should I do now" question with no falsifiable hypothesis in play. Co-fires with prop-firm-challenge for operational facts. Does NOT modify strategy code, allocations, dd_protection constants, or MC calibration. Sibling: `inqhiori` handles structural/statistical/low-reversibility work; exit this skill if a request needs N≥100, permutation gating, or framework editing. Loop-selection canon: docs/methodology/inqhiori-canon.md (§14 three-loop binding).
---

# OODA — Tempo loop for tactical / recoverable work

Component skill of the **INQHIORI ⊕ OODA dual-loop framework** (reactivated 2026-05-01). This skill scopes to OODA; INQHIORI is the sibling skill `inqhiori`.

**Canonical reference:** `docs/methodology/inqhiori-canon.md` (§14 = the three-loop binding). When this skill disagrees with the canon, trust the canon. The Notion surface was retired 2026-06-12 (ADR `docs/adr/2026-06-12-notion-surface-retirement.md`; dead-ID map `docs/governance/notion-redirect-map.md`). Last reconciliation: 2026-05-01 (post-split codification).

OODA is John Boyd's loop: **Observe → Orient → Decide → Act**, repeat. The point is tempo — getting inside the decision cycle of the situation rather than slowing down to formalize. In Joshua's context, the "situation" is the market and broker stack within his free-window before NDR work starts at 2pm ET, and the failure mode is treating tactical recoverable decisions as if they were structural ones (writing a brief when you should be acting, then re-observing).

---

## 0. Pre-loop gate: Rule 0 (audit-first)

**Before Observe begins, read production state directly.** Not memory, not yesterday's snapshot, not the brief from last week. Current state.

Rule 0 is canonical in `docs/rule_0.md`. For OODA specifically, the instantiation is:

- "Production state" means the things that move tactically: open positions, dd_protection state, current peak/trough, today's strategy eligibility (Mon/Tue/Wed/Thu rules), active broker stack, allocation constants in code, alert log.
- A decision authored before the relevant state has been read in the current session is a Rule-0 violation. Tempo is not an excuse to skip the read — the read should be O(seconds) when state is properly indexed.
- The Observe phase is **derived** from the state read. If state hasn't been read, Observe has nothing trustworthy to work with.

This is the discipline that exists at both layers of the dual-loop. In INQHIORI it instantiates as "read production code before assembling the I/N corpus." Same rule, different cadence.

If a session is about to begin OODA work and Rule 0 has not been honored: stop, read state, then Observe. The cost is seconds; skipping it is the entire reason for the discipline.

---

## 1. The OODA loop in trading-ops context

```
[Rule 0 read] → Observe → Orient → Decide → Act → (re-Observe — loop)
```

**Observe.** Surface the relevant facts of the current moment. Open positions, P&L, current dd_protection scaling state, FIRE-alert log, broker connectivity, news events firing, time of day relative to free-window. No analysis yet — collection only.

**Orient.** Place the observations against the locked context: which strategies are eligible today, what binary events gate trading (BOJ etc.), what the current allocation is, what the multi-firm sequencing dictates, whether we're inside or outside dd_protection scaling. **Orient is the pivot phase** — most OODA failures happen here, where context drift turns a tactical situation into something the locked rules didn't anticipate.

**Decide.** Pick the action from the eligible-action set. Eligible actions are pre-defined by locked rules; OODA does not invent new actions. If no action in the eligible set fits the situation, the answer is usually "no action" — not "improvise."

**Act.** Execute. At system lots. No overrides. No "just this once."

**Re-observe.** Loop closure. Did the action produce the expected state change? If yes, continue. If no, that's an observation worth surfacing — and possibly a hypothesis worth handing off to INQHIORI (§4).

---

## 2. Loop selection — when OODA, when INQHIORI

Use **OODA** when:
- The decision is tactical and recoverable within hours/days.
- Tempo matters more than rigor.
- The action set is bounded by locked rules; you're picking from existing options, not designing new ones.
- No falsifiable hypothesis is in play — just operational reality and pre-defined responses.

Use **INQHIORI** (`inqhiori` skill) when:
- The decision is structural or low-reversibility.
- A claim requires statistical support (N≥100, permutation gating, etc.).
- The work involves parameter changes, framework edits, lock decisions, MC re-calibrations, anomaly investigations, or rule additions/deletions.
- A falsifiable hypothesis can be stated in one sentence and is worth testing.

**Tiebreaker when ambiguous:** if you cannot articulate the falsifiable hypothesis in one sentence, you are not in INQHIORI territory yet. Run OODA, gather observations, let INQHIORI activate when a hypothesis crystallizes.

The selection rule is canonical in `docs/methodology/inqhiori-canon.md` (§14). When this skill and the canon disagree, trust the canon.

---

## 3. Tempo discipline — the failure mode this skill exists to prevent

OODA's value is speed. The failure mode is treating tactical recoverable work as if it were strategic structural work. Symptoms:

- **Brief authoring on tactical decisions.** A decision recoverable in hours does not earn a 2-page document. If you find yourself drafting one, you've left the OODA lane — either return to it or escalate explicitly to INQHIORI with a stated hypothesis.
- **Hypothesizing during Orient.** Orient places observations against locked context; it does not generate new theories. New theories are INQHIORI's job. Hypothesizing inside OODA stalls the loop and produces neither speed nor rigor.
- **Inventing new actions.** The action set is bounded by locked rules. If no action fits, "no action" is the eligible response. Inventing is overlay-creation by another name and triggers the §10 overlay policy from `inqhiori`.
- **Re-deciding settled questions.** Daily dd_protection rules are locked. BOJ pauses are locked. Allocation constants are locked. OODA executes against these; it does not reopen them. Reopening is INQHIORI work, gated by version-bump triggers.

If any of these patterns surface inside an OODA cycle, that itself is an observation. Note it, complete the cycle on the eligible-action set, and surface the pattern in §4 handoff.

---

## 4. Handoff to INQHIORI — when an observation crystallizes

OODA observations are first-class inputs to INQHIORI. The bridge is the **falsifiable hypothesis test**:

> Can this observation be stated as a one-sentence falsifiable hypothesis whose test would meaningfully change a locked rule, parameter, or framework element?

If **yes**, log the observation with the proposed hypothesis and surface it for INQHIORI scheduling. Do not start INQHIORI work mid-OODA-cycle — complete the tactical decision first at system lots, then escalate. Tempo discipline (§3) holds even when an interesting hypothesis surfaces.

If **no**, the observation is operational noise or context the locked rules already handle. Note it in the trading journal if it might recur; otherwise let it go.

Worth naming explicitly: **most OODA observations should NOT promote to INQHIORI.** The dual-loop's value is that they're separate lanes. If every OODA cycle generated an INQHIORI thread, the methodology layer would have rebounded into the failure mode the 2026-04-29 archive was correcting.

---

## 5. Worked example — attended c1 arming day (canonical OODA cycle)

Live execution is the **c1 rail only** (TV → listener → CrossTrade → Tradovate; Option C). Manual FIRE→lots CFD execution is **HISTORICAL/DORMANT** (retired 2026-06-30 / FXIFY closed 2026-07-10). For any arming / disarm / fill question, load the `c1-rail` skill + [`RUNBOOK.md`](../../../docs/notes/rail_build/RUNBOOK.md) §B7 — do not invent a desk playbook here.

**[Rule 0 read]** — open `ops/c1_rail/c1_rail_arm.py` / rail status, `dd_protection.py` sizing path, M1 acceptance pointer, today's `armed_until` if any. Confirm disarmed vs armed in head.

**Observe** — on a B7 arming day only (not every calendar day):
- Rail `dry_run` / arm state and absolute `armed_until`.
- M1 gate status (next `dry_run=false` entry/add send gated on M1 `RESOLVED` + operator GO).
- Open Tradovate positions / recent fills if any.
- Whether a strategy-signal path (not a canned re-POST) is the session intent.

**Orient** — place observations against locked context: Is M1 `RESOLVED`? Is arming still inside `armed_until`? Is disarm scheduled **before** expiry (07-31 self-brick lesson)? Is this an attended session with operator GO?

**Decide** — eligible actions are bounded by the c1-rail skill + RUNBOOK: keep disarmed; arm only under GO + M1; disarm before `armed_until`; take no action. Manual lot entry from a FIRE alert is **not** an eligible action.

**Act** — execute the chosen rail action only. Do not modify SL/TP in the broker. Do not re-POST payloads for "idempotency" (order_id idempotency is DISPROVEN). Do not invent sizing outside `ops/c1_rail/c1_sizing_host_reference.py`.

**Re-observe** — did arm/disarm/status match intent? Any unintended fill? If yes and unexpected, that is an observation — note it and consider §4 handoff / telemetry.

The historical CFD corrective protocol (morning dd_protection → FIRE → system lots → do not touch) remains a useful *discipline* memory, but its **action surface is retired**. Re-deciding settled exit rules during Act is still what §3 prohibits.

---

## 6. What this skill does not change

This skill operates in the gaps between locked rules, not on the rules themselves. It does not modify strategy parameters, allocations, dd_protection constants, re-MC triggers, or binary-event pauses — those live in `core/dd_protection.py` / `core/firm_rules.py` and the allocation ADR `docs/adr/2026-05-23-allocation-refresh-2.md` (canonical), never restated here. (Binary-event pauses are pre-decided in INQHIORI; OODA executes them, doesn't revisit them. Locked rules in the `inqhiori` skill are likewise unchanged.)

---

## 7. Usage notes for Claude (web and Code)

- **Loop selection precedes everything else.** If the work is structural / statistical / low-reversibility, exit to `inqhiori`. See §2.
- **Rule 0 first, every time.** §0 is not optional. The state read is fast; skipping it is the discipline failure.
- **Tempo is the value proposition.** If a response would require authoring a multi-section brief, the skill is being misused — either the work is actually INQHIORI (escalate) or the response should be terse (an action, not a document).
- **Eligible action set is bounded by locked rules.** No invention. "No action" is a valid output.
- **Re-observation closes the cycle.** Don't end on Act. The loop is observe-orient-decide-act-observe, not observe-orient-decide-act-done.
- **Most observations don't promote.** Resist the pull to escalate every OODA cycle to INQHIORI. The lanes are separate for a reason.
- **When INQHIORI is the right lane and Joshua asks an OODA-framed question anyway**, surface the mismatch directly. "This looks like an INQHIORI question framed as OODA — the falsifiable hypothesis is X, and the right path is to gate it through `inqhiori`'s pre-Q gate before acting." Then wait for direction.
