# INQHIORI — Investigation framework with D-S-A pre-Q gate (canonical)

**Path:** `docs/methodology/inqhiori-canon.md`
**Status:** CANONICAL as of 2026-06-12 per `docs/adr/2026-06-12-notion-surface-retirement.md` (Notion surface retirement)
**Port provenance:** Faithful port of Notion page `34ddc0b53c1181479d7bdecc61f47078` ("INQHIORI — Investigation framework with D-S-A pre-Q gate (reference)"), fetched live 2026-06-12 via Notion MCP (page content as of its last edit, 2026-05-10). The Notion page is frozen read-only pending migration completion and holds no authority after this file's commit. §14 is new content added at port time (not in the Notion original). Notion page references in the body were tagged at port time and **resolved 2026-06-13** by the Notion Phase-2 migration (per `docs/adr/2026-06-12-notion-surface-retirement.md`) to repo paths / verbatim archive exports / the redirect map at `docs/governance/notion-redirect-map.md`. Four of the referenced pages had already been deleted from Notion (404 on fetch); those are recorded as dead IDs in the redirect map with their repo-history / superseded-ADR resolutions.

> **SEPARATED FROM OODA 2026-05-09.** Canonical reference for INQHIORI as a standalone investigation framework with D-S-A pre-Q gate. OODA's canon lives in the `ooda-loop` skill file (no mirror).
>
> **History.** Archived 2026-04-29 as the unified INQHIORI ⊕ The Algorithm framework (v2). Reactivated 2026-05-01 as the INQHIORI ⊕ OODA dual-loop framework. Separated from OODA 2026-05-09 — the unification scaffolding was not load-bearing; the loops are independent methodologies for different work classes, not components of a single framework.
>
> **Scope.** Use INQHIORI when the decision is structural, low-reversibility, or requires statistical support (lock decisions, MC re-calibrations, parameter changes, framework edits, anomaly investigations, claims requiring N≥100 with permutation gating). For tactical/recoverable/tempo work, use the `ooda-loop` skill. Tiebreaker (in skill files): if you cannot state the falsifiable hypothesis in one sentence, you're not in INQHIORI territory.
>
> Archive reasoning preserved at `docs/methodology/archive/README.md`.

**Purpose.** Canonical definition of INQHIORI with the D-S-A pre-Q gate. Supersedes the prior "orthogonal" framing of INQHIORI and The Algorithm; both predecessor reference pages remain valid for their definitional content.

**What changed.** D-S-A was previously framed as a post-validation system-shaping discipline (apply The Algorithm *after* INQHIORI delivers a finding). It is now also formalized as a **pre-Q gate inside INQHIORI**: D-S-A operates on the I/N corpus to focus questioning before any Q is asked. Same operators, different domain.

**Status.** Codified 2026-04-25. v2 codification 2026-04-27: added Sources Read declaration block (§3) + forbidden patterns; promoted Rule 0 from §10 reference to mandatory brief-header structure. Separated from OODA 2026-05-09; OODA's canon now lives standalone in its skill file. First test case: the in-flight Inquire-phase work (Q1 / Q5 / Q8) and the already-executed Notice-phase compression. The 2026-04-27 Q-meta-a brief is the canonical case study of how Rule 0 in weakened form produces wrong audit verdicts; its gate-audit path (`docs/methodology/gate_audits/2026-04-27_meta_partition_test.md`) was never instantiated — Case B audits that did land are recoverable via `git show pre-prune-2026-06-05:archive/docs/methodology/archive/gate_audits/` (e.g. `2026-04-25_q3_halt_rules_design_skew.md`).

---

## 1. The INQHIORI loop

```
I → N → [ D → S → A ] → Q → H → I → O → R → I    (loop)
              gate
```

The bracket is the gate. **It filters, compresses, and indexes the data surfaced by Identify and Notice before any Question is asked.** Q operates on a sharper corpus. H is correspondingly sharper.

The outer loop and the inner gate share their operator language (D / S / A) but operate on different domains. Confusing the two is the primary failure mode.

## 2. D-S-A operates in three domains (do not conflate)

| Location | Operator domain | Object | Purpose |
|---|---|---|---|
| **Pre-Q gate** (inside INQHIORI) | Data | The I/N corpus | Focus questioning |
| **Post-H build** (The Algorithm proper) | System | The artefact built from a finding | Optimize implementation |
| **Meta-process** (recursive) | Frameworks | The framework itself | Compress ceremonial scaffolding (Notice phase compression, 2026-04-25) |

Same three operators (D, S, A). Three distinct objects. The discipline of *naming which object is being acted on* is what keeps the framework honest. *(See also §14: a fourth authority dimension — which loop tier a D-S-A pass binds at — added 2026-06-12.)*

## 3. Mandatory brief headers (added v2, 2026-04-27)

A correctly-authored brief or audit places these headers in the following order:

1. Title
2. **D-S-A domain header** (1 line, immediately after title)
3. Context section
4. **Sources Read declaration block** (immediately after Context)
5. **Pre-Q gate header** (immediately after Sources Read)
6. Q, H, Method, Verdict criteria, Cross-references, Recursion note

### Sources Read declaration block

Add a "Sources Read" block immediately after the Context section, before the Pre-Q gate header:

```
Sources read at production fidelity:
  Past chats (conversation_search / recent_chats):
    - <query terms used> → <records read; UUIDs of load-bearing chats>
    [or: N/A — <reason: no historical claim, all-current-context, etc.>]
  Files / artifacts on disk:
    - <paths read in full>
    - <paths read in part: lines, ranges, or sections>
    [or: N/A — <reason>]
  User memory:
    - <used as primary | used as supplementary | not used>
    - if primary: <rationale for not going to source>
  Tools available but unused:
    - <tool name> — <rationale for non-use>
```

The tools-available-but-unused field is mandatory and non-empty. If every available tool was used, state explicitly: "all enumerated tools used." If a tool was unused, the rationale is what makes the non-use auditable.

Rule 0 (originally codified in `prop-firm-challenge` for risk-control decisions) operates here at full strength on the methodology layer. Production-source reads (code, prior chats, prior briefs) come before any analytical claim. Memory is supplementary by default; primary use of memory requires a written rationale in the block.

### Pre-Q gate header

Add a 3-line "Pre-Q gate" header immediately after the Sources Read block:

```
Pre-Q gate:
  D: <items deleted from I/N corpus> — test: <D-test applied>
  S: <compression rationale; what representation remains>
  A: <index / structure used to make Q cheap>
```

If any line reads "no action," state explicitly why the gate didn't engage in that domain. Silence is not.

### D-S-A domain header

Add a 1-line "D-S-A domain" header after the brief title:

```
D-S-A domain: <data | system | meta-process>
```

If the brief operates in more than one domain (legitimate; see the Notice-phase compression example), declare each and call out the cascade explicitly.

### Forbidden patterns in the Sources Read block

Parallel to the forbidden D-tests in §5. If a draft contains any of these, stop and re-source before proceeding to the Pre-Q gate header:

- **"Rule 0 spirit applies in weakened form"** or any synonym ("analogue," "in spirit," "loosely," "approximately"). Rule 0 binds at full strength on the methodology layer. Weakening language is not authorized.
- **"Memory is sufficient for this case"** without a paired statement of which source-tools were checked and what they returned. Sufficiency is established by negative tool calls (e.g., "conversation_search returned no relevant records"), not assumption.
- **"Tools were not relevant"** as a blanket statement covering multiple tools. Each unused tool gets its own rationale.
- **Empty tools-available-but-unused field.** If every tool was used, write "all enumerated tools used" explicitly.
- **Vague time references** ("recent chats," "earlier work") in place of specific UUIDs or paths. Load-bearing claims need locatable sources.

The 2026-04-27 Q-meta-a brief is the canonical case study of how the first pattern produces a wrong audit verdict.

## 4. Operator definitions in the pre-Q domain

### D — Delete

Remove items from the I/N corpus that fail a stated relevance test.

- Every deletion logs the test that killed it.
- The raw I/N corpus is preserved as the Rule 0 anchor; D produces a derived working set.
- D is reversible by re-running the gate with a revised test.

### S — Simplify

Reduce the remaining data to the lowest-dimension representation that **preserves the anomaly Noticed**.

- Compression test = preservation of N's signal, not byte-count.
- If S removes the signal, S has failed. Revert.

### A — Accelerate

Index / structure the simplified corpus so each subsequent Q costs O(seconds), not O(reload-the-corpus).

- This is what makes the Q–H iteration loop cheap enough to iterate.
- A is bounded. Expensive Accelerate on data you might not query is premature optimization.

## 5. The relevance test for D (most failure-prone step)

The test must satisfy:

> **A datum stays if its presence could contradict a hypothesis you haven't formed yet.**

If answering the test requires forming the hypothesis first, the datum stays. This prevents D from silently encoding the conclusion the loop is supposed to reach.

### Forbidden D-tests (each begs the question or encodes a model the loop hasn't validated)

- "Does this have a known physical / causal mechanism?"
- "Does this fit my model?"
- "Is signal-to-noise high?" (assumes you already know the signal)
- "Has this been useful before?"

### Permitted D-tests

- "Is this a known measurement artefact with a documented cause?"
- "Is this duplicated by a higher-fidelity source already in the corpus?"
- "Is this outside the temporal / instrument scope of the question class?"
- "Is this a literal copy / encoding of something already retained?"

If the test you want to apply is not on the permitted list and not trivially equivalent to one, write the test, declare it new, and log it in the gate audit trail.

## 6. Guardrails

1. **Time budget.** Gate effort ≤10% of I/N effort (default; tune empirically). Exceeding the budget signals **I/N was wrong**, not that the gate needs more time. Restart the outer loop.
2. **Audit on regret.** Anything deleted that later proves to matter triggers a gate audit — criterion review, not just data restoration. Log the failed criterion in `docs/notes/audits/YYYY-MM-DD_gate_<slug>.md`.
3. **S preserves N.** S that removes N is not S. Compression that loses the anomaly is failure.
4. **Bounded A.** A must be cheaper than the queries it enables, in expectation. If A is the costly step, the gate has been misapplied.
5. **Recursion logging.** INQHIORI loops; the gate loops with it. Each iteration may surface I/N data the prior gate deleted. That's the criterion updating, which is fine — but log every such case explicitly. Repeat occurrences of the same criterion failing are the signal that the D-test class is too aggressive.

## 7. Worked example — Iran-Hormuz overlay (counterfactual)

The overlay episode is a clean test case. A properly applied D-S-A pre-Q gate would have refused to build the regime overlay.

**I:** Iran-Israel conflict, June 2025. Strait of Hormuz threatened.
**N:** Gold spiking, USDJPY whipsawing, Guardian / Aegis exhibiting unusual signal density. Physical traffic through Hormuz: continuous.

### 7.1 Failed gate (what the overlay actually did)

D-test implicitly applied: *"Does this price action have a physical / causal mechanism in the conflict zone?"*

- Physical ground-truth (channel open, traffic continuous) → conclusion that the price action "lacked a mechanism."
- Price action flagged as noise relative to the physical regime model.
- Overlay built that conditioned position sizing on physical conditions.
- Overlay later deactivated 2026-04-23 after revert conditions were met. Hard lesson logged.

This D-test is **forbidden** under the formal gate. It encodes the hypothesis ("physical conditions drive price") inside the relevance test. The conclusion was therefore baked in before Q ever ran.

### 7.2 Properly-applied gate

D-test applied: *"Could this datum contradict a hypothesis I haven't formed yet?"*

Two streams in the I/N corpus:

1. Physical ground-truth (Hormuz traffic, tanker AIS).
2. Price action timestamped to headline events.

Both pass D. The **divergence** between them is the unformed hypothesis. Neither is deletable without pre-judging.

**S:** collapse both streams to a single comparison object — headline timestamp vs price reaction within an N-minute window. Preserves the anomaly (the divergence). The physical-state stream is retained as a low-dimensional state variable for the same windows.

**A:** index by headline timestamp; Q-cost drops to seconds.

**Q (now sharper):** *Why does price react to headlines without corresponding physical follow-through?*

**H:** Market participants price expectations and tail-risk premia, not physical state. Headlines move the expectation distribution; physical state is downstream and slow.

This H is the lesson actually paid for. The properly-gated loop reaches it **without building the overlay**. That is the specific value the gate adds.

## 8. Worked example — Notice phase compression (2026-04-25, retrospective)

The Notice phase compression that landed (commits `a05e9f3` → `cfea4a2`) was an unconscious application of the gate, framed at the time as "applying The Algorithm to the framework itself."

**Reframing under the INQHIORI framework:**

| Step | Domain (where the operator was acting) | What happened |
|---|---|---|
| Q (in The Algorithm sense) | Meta-process | "Is the Notice / Inquire bifurcation load-bearing or ceremonial?" |
| D | Meta-process AND Data | Deleted A3 / C3 threads from the framework AND deleted the JSON / figure / CSV intermediates from the corpus they produced |
| S | Meta-process | Replaced two-phase ceremony with three-bucket routing gate |
| (no A) | — | The simplified gate didn't need acceleration |

The interesting part: **the D step here operated on both domains simultaneously**. The framework-level deletion (drop A3 / C3 as standing artefacts) cascaded into a corpus-level deletion (drop the JSON / figures / CSVs those threads produced). That cascade is the unified framework operating implicitly.

> ⚠ **Historical record, not current practice.** The S step's replacement did not hold for narrative-observation routing in the three-plus months since — see [`ADR 2026-08-15`](../adr/2026-08-15-notice-log-is-the-live-observation-routing-convention.md). The D-step lesson two paragraphs below is unaffected; only the specific S-step outcome ("three-bucket routing gate" as the standing replacement) is corrected.

The lesson: when D acts on a meta-process (a framework), it implicitly authorizes corpus-level D on the data that framework was producing. When D acts on data alone (the pre-Q gate), it does **not** authorize framework changes — frameworks are governed by the meta-process domain, which has its own discipline.

## 9. First conscious test — Inquire-phase work (closed 2026-04-29; preserved as worked example)

These were the first conscious applications of the unified framework. All three closed during the 2026-04-29 archive sweep; they're preserved here as worked examples of how the gate runs end-to-end:

1. **Q1 — Guardian 1R reconciliation.** I/N corpus: Guardian v5.5 OANDA backtest CSV + Pine sizing line + canonical 1R doc. Pre-Q gate: Delete the bar-data findings (out of scope), Simplify to the per-trade equity-normalized loss measurement, Accelerate by precomputing running equity. Q: equity-compounding artefact or sizing problem? Cheapest falsification first.
2. **Q5 — XAU-USDJPY break window P&L.** I/N corpus: B2 finding + strategy P&L during 2025-10-30 → 2026-01-27. Pre-Q gate already partially run (Q5 selected over Q3 specifically because Q5 is the cheaper falsification — that's the gate's *Simplify* step on the question set, not just the data).
3. **Q8 — Doc / code skew postmortem.** I/N corpus: ADR change log + recent decision briefs. Pre-Q gate: Delete (Q8a only audits the last 60 days, not all-time; that's a D-test on temporal scope), Simplify (single audit table), Accelerate (grep-friendly).

Each of these is an opportunity to **explicitly run the gate and log the audit trail**. If a gate audit reveals a forbidden D-test was applied, that's the framework working as intended.

**Update 2026-05-05 — second conscious test (post-reactivation).** The Q-NAS series for Striker NAS100 v1 production clearance. 5 Inquire-phase questions (Q-NAS-1 through Q-NAS-5), 0 forbidden D-tests detected, mandatory §3 headers authored on every brief. Two memory drifts surfaced and resolved before propagation (DJ30 v4.4 → v4.5; Striker NAS100 B_15 → FINAL_LOCK). One methodology assumption verified on first principles (NAS 1R Striker-class branch confirmed at `portfolio_mc.py:122-127` with full-stop n=25, well above the n=5 fallback). Production lock cleared with comfortable margin on every gate (Pass 98.13% / Bust 0.22% / p99 DD 4.49%). This is the framework's first multi-turn dual-loop deployment with web Claude in the Inquire role and Code in the executor role; the handoff held without canon corruption. Reflect entry (carried into the 2026-07-29 rebound check): Reflect — Striker NAS100 v1 dual-loop closure (Notion `357dc0b53c118124a3ddf811d1d50745`; page retired/404 — resolved in `docs/governance/notion-redirect-map.md`; closure summary in §9 above).

### Backfill discipline (added v2, 2026-04-27)

Q1, Q5, and Q8 were drafted before the v2 Sources Read declaration block was codified. Each must add the §3 Sources Read block before its execution audit fires. The drafting Sources Read block is paired with an execution-time Sources Read block in the audit. The 2026-04-27 Q-meta-a brief is retrospectively annotated rather than re-run; its cited gate-audit path was never instantiated (see §Status) — related Case B audits: `git show pre-prune-2026-06-05:archive/docs/methodology/archive/gate_audits/`.

## 10. Integration with existing infrastructure

- **Rule 0 (audit-first for source-fidelity)** — originally codified in `prop-firm-challenge` skill for risk-control decisions, now operative across all methodology work via the §3 Sources Read declaration block. Production-source reads (code, prior chats, prior briefs) come before any decision brief or audit. The gate operates on what Rule 0 surfaces, not memory. Weakening language ("spirit," "weakened form," "analogue") is not authorized; see §3 forbidden patterns. The 2026-04-17 risk-control incident chain (Notion `346dc0b53c11816085bbf2292be934cc`; page retired/404 — superseded by `docs/adr/2026-04-17-dd-trigger-calibration.md` + `docs/adr/2026-04-17-equity-tier-deletion.md`; see redirect map) and the 2026-04-27 methodology-layer Q-meta-a incident establish two domain instances of the same failure pattern.
- **Rule 1 (small-cell variance prior) still binds.** Small cohorts trigger caution at the Observe / Reflect phase regardless of how the gate filtered the corpus.
- **Overlay policy is unchanged.** No overlays without full INQHIORI. The gate is the front of that loop, not a relaxation of the back.
- **Observation routing** operates *after* the pre-Q gate — observations that pass the gate get routed to a decision. The two gates compose; they don't compete. ⚠ **Corrected 2026-08-15** ([`ADR`](../adr/2026-08-15-notice-log-is-the-live-observation-routing-convention.md)): narrative observations (findings, anomalies, "interesting things") route via the Notice-log convention (`docs/notes/notice/N-YYYY-MM-DD-slug.md`, `GRADUATE / DROP / HOLD`) — `observation_routing.md`'s Closed/Action/Forward vocabulary did not displace it in practice and now governs only one mechanical gate (`scripts/verify_lock_anchors.py`), not narrative routing.
- **Trade journal** entries that derive from a gated INQHIORI loop reference the gate audit slug.
- **Audit trail location:** `docs/notes/audits/YYYY-MM-DD_gate_<slug>.md`. Required fields: deleted items, D-test applied, S-compression rationale, A-index used, regret events. Historical Case B audits (pre-2026-06-05 archive): `git show pre-prune-2026-06-05:archive/docs/methodology/archive/gate_audits/`.

## 11. What this does not change

- Strategy parameters / versions / risk%: owners are Pine + gated [`CLAUDE.md`](../../CLAUDE.md) §Strategy Reference (this canon does not restate them).
- Allocations: [`docs/adr/2026-05-23-allocation-refresh-2.md`](../adr/2026-05-23-allocation-refresh-2.md) · live authority `core/firm_rules.py` `_BASE_RISK`.
- `dd_protection` literals / rule: [`core/dd_protection.py`](../../core/dd_protection.py) · human summary [`CLAUDE.md`](../../CLAUDE.md) §Protection · C2 relock [`docs/adr/2026-05-08-dd-trigger-c2-relock.md`](../adr/2026-05-08-dd-trigger-c2-relock.md).
- Re-MC triggers: unchanged (see prop-firm-challenge skill / owning ADRs — not restated here).
- BOJ binary-event pause for Aegis around 2026-04-28: unchanged.

This document codifies methodology. It governs how future loops are run, not what current production does.

## 12. Cross-references

- **Parent frameworks** (canonical for their respective layers; both remain valid for definitional content):
  - INQHIORI — the investigation framework — `docs/methodology/archive/notion/inqhiori-v1-investigation-framework.md` (Notion `34cdc0b53c11812d96f8f6e9ee500d5e`)
  - The Algorithm — default problem-solving framework — `docs/methodology/archive/notion/the-algorithm.md` (Notion `34ddc0b53c11811eb6a0d9192b63d252`)
- **Hard rules:**
  - Rule 0 — read production code before any risk-control decision (codified in prop-firm-challenge skill)
  - Rule 1 — small-cell variance prior — `docs/methodology/archive/notion/rule-1-small-cell-variance-prior.md` (Notion `34cdc0b53c11812cbb4ff637ba44736e`)
  - Rule 2 — budget before acting, scaled to reversibility — `docs/adr/2026-06-16-rule-2-budget-before-acting.md` (full statement at §15 below)
- **Hard lesson:** Iran-Hormuz overlay deactivation — Notion `34bdc0b53c1181fe9dc3fd93eadf3e8e` (page retired/404; repo history `git show pre-prune-2026-06-05:archive/docs/methodology/archive/overlays/guardian_conflict_risk.md`; see redirect map)
- **First test case:** Claude Code brief — 1R diagnosis + Open Questions reorder + Notice phase compression — 2026-04-25 — Notion `34ddc0b53c1181199976c9b1b4effb17` (page retired/404 — superseded by `docs/methodology/observation_routing.md`; see redirect map)
- **Repo touchpoints:**
  - Gate-audit write-target (live): `docs/notes/audits/YYYY-MM-DD_gate_<slug>.md`. Historical directory `docs/methodology/gate_audits/` was archived 2026-04-29 and evicted 2026-06-05 — recover via `git show pre-prune-2026-06-05:archive/docs/methodology/archive/gate_audits/` (Case B example: `2026-04-25_q3_halt_rules_design_skew.md`)
  - `CLAUDE.md` — update at commit to reference THIS FILE as the primary methodology entry point (previously referenced the Notion page)
  - This file supersedes the unexecuted `docs/methodology/inqhiori_dsa_gate.md` mirror plan noted in the archive README.

## 13. Usage notes for Claude Code and web Claude

- **Both clients reference this file for INQHIORI work**, not the orthogonal-framing predecessors. The predecessor pages are kept (as migrated archives) for their definitional content, but the operational discipline is here. For tactical/recoverable/tempo work, both clients use the `ooda-loop` skill instead.
- **Every brief that authors Inquire-phase questions** should declare what its pre-Q gate did. "Pre-Q gate: deleted X under test Y; simplified to representation Z; accelerated via index W." Three lines, mandatory header.
- **Every brief that proposes a structural change** to a framework or system should declare which of the three D-S-A domains it is operating in (data / system / meta-process). Conflating domains is the failure mode this page is built to prevent.
- **The gate is user-gated at D.** Claude Code and web Claude both propose deletions; Joshua authorizes. Same discipline as The Algorithm proper.
- **When a forbidden D-test is detected**, stop, log, and surface to the user before retrying. Don't quietly substitute a permitted test that produces the same deletion — that's the Iran-Hormuz failure replayed.

## 14. Methodology-to-Loop Binding (added 2026-06-12, port-time)

**Canonical source:** `docs/adr/2026-06-12-three-loop-methodology-binding.md` (ADR of record) + companion map `docs/governance/systematic-trading-lifecycle.md`; GRAND row added 2026-08-09 per `docs/adr/2026-08-09-grand-tier-quintessentials-binding.md` (its ADR of record). This section is the canon-side statement; if it and the ADRs ever disagree, the ADR wins.

| Loop | Cadence | Governing methodology | Core question |
|---|---|---|---|
| GRAND | Quarterly gate / off-cycle only on a tripped falsifier | **The Quintessentials** (Aim · Measure · Anchor · Survive · Subtract → Update) | Should this pursuit exist at all? |
| STRATEGIC | Quarterly / audit-triggered | **The Algorithm** (Q → D → S → A) | Should this exist and deserve resources? |
| OUTER | Per-investigation | **INQHIORI** (this document) | Is this true? |
| INNER | Per-session / real-time | **OODA** (`ooda-loop` skill) | What do I do right now? |

Key rules (full statement in the ADR): The Algorithm is a **fractal operator** — D-S-A passes run at any loop with declared Loop-of-Record (consistent with the three-domain table in §2; the loop tier is the authority dimension, the §2 domain is the object dimension — declare both). **Delete verdicts at programme / track / instrument tier are STRATEGIC-LoR acts**, valid only via programme-audit cadence, a fired pre-registered stopping rule, or explicit owner adjudication. No-borrowing: lower-loop sessions propose Strategic Deletes; they do not execute them on local momentum. **Add-back rate** — the deletion-calibration metric — is tracked at programme audits in **two layer-segregated forms, never pooled** (split 2026-07-01, governed by `docs/adr/2026-07-01-add-back-metric-layer-split.md`, **Accepted 2026-08-21 — operator override, §4's graduation trigger never fired; see the ADR's Addendum 2026-08-21**; the two-layer rule forbids cross-citation): **(a) meta-layer signal add-back** = rejected *methodology signals* (`docs/methodology/rejected_signals.md`) re-accepted on a dated incident ÷ issued — the metric a **methodology** audit uses (no object-layer anchor; **registry-scoped**, currently 0/1; other governance-surface Delete reversals are meta-layer too but reviewed *qualitatively* at audit, not pooled into this rate); **(b) object-layer strategy add-back** = strategy/track/instrument Deletes (`docs/rejected_candidates.md`) later reversed on new mechanism evidence — the metric a **portfolio** audit uses, **object-layer anchor** = Guardian Silver re-open (beTriggerAtr=4.8 RF gate, 2026-05-14 Q-CORR-1 closure). A methodology audit cites only (a); a portfolio audit only (b). The ~10% deletion-calibration band is judged **per-instrument**, never on a pooled figure.

**GRAND (added 2026-08-09):** the tier above STRATEGIC; object class = **pursuits** (whole
commitments — campaigns, lanes, standing explorations, meta-belt items, aim-scale branches).
Lifecycle `OPEN → { KEEP | PARK(re-entry, expiry) | MERGE | SUBTRACT(re-entry armor) }`; opening
a pursuit requires an entry record (Aim, Measure, Survive bound, review date); dispositions are
operator-gated (the D user-gate, one tier up); **Subtract (pursuits) hands off to The Algorithm's
Delete (parts within surviving pursuits)** — pursuit is a fourth operator domain alongside
data/system/meta-process (§2), and domain conflation remains the guarded failure mode. Full
statement: `docs/adr/2026-08-09-grand-tier-quintessentials-binding.md`.

**Rule 2 budget (per §15).** Each loop tier carries an iteration budget set by Rule 2: **INNER 3 / OUTER 8 / STRATEGIC 3 constituent OUTER investigations.** This is the reversibility-scaled *spend* boundary that complements the LoR *authority* dimension — same loop tiers, different resource. Full statement + forward falsifier: §15.

Lifecycle overlay: STRATEGIC funds stage 1 (alpha research) and owns kill/scale verdicts from stage 5 (post-trade analytics); OUTER runs stages 1–2; INNER runs stage 3 (execution); stage 4 (telemetry/TCA) is the membrane routing each signal to its consuming loop. Full five-stage map: `docs/governance/systematic-trading-lifecycle.md`. Authorization axis (stage-5 capital-authorization mechanism): `docs/methodology/strategy_lifecycle.md`.

## 15. Rule 2 — Budget before acting (added 2026-06-16)

**Canonical source:** `docs/adr/2026-06-16-rule-2-budget-before-acting.md` (ADR of record, **Accepted 2026-08-21 — operator override, ahead of §4/§6's evidentiary graduation gate; see the ADR's Addendum 2026-08-21**). This section is the canon-side statement; if it and the ADR ever disagree, the ADR wins. **Numeral note:** the originating handoff proposed "Rule 1"; that slot is held by the small-cell-variance-prior rule (§10/§12), so this is **Rule 2** (owner-adjudicated 2026-06-16). It binds both loops (the test for earning a numeral): a budget is OODA's time-boundedness restated, and it is the discipline the unbudgeted cfg00–12 sweep visibly lacked. Reversibility-classification is its *sizing function*, not a separate rule — which is why it earns no numeral of its own.

**Rule 2 — Budget before acting, scaled to reversibility.**

Before starting a task, declare a spend budget bounded by the cost of being wrong. Time is the intent; the budget is counted in *iterations* — one complete attempt-and-check cycle, mapped to the task's natural unit (config run; drafted-and-reviewed section; hypothesis–edit–test cycle; query-and-read pass). The loop class (LoR, §0) sets the magnitude:

- **INNER** (recoverable/tempo): **3 iterations.** May self-extend once with a stated reason.
- **OUTER** (structural/low-reversibility/statistical): **8 iterations.** No self-extension.
- **STRATEGIC** (funding/kill-continue/programme-tier): **3 constituent OUTER investigations.** No self-extension.

The budget is a **tripwire, not a wall.** Hitting it triggers a *structured stop* — spent / remaining / current state / extend-or-stop recommendation tagged with its reversibility — and a deliberate extend-or-stop decision. Never a silent continue; never a silent finish.

Tripwire actions are **asymmetric by reversibility:**
- Recoverable overrun → **STOP.** The overrun is the rabbit-hole signal.
- Irreversible overrun → **STOP and RE-AUDIT.** A high-stakes decision blowing its budget means the Rule-0 read was incomplete; return to ground truth before continuing.

Corollaries:
1. **Forbidden move.** Budget exhaustion may never resolve to shipping an under-validated irreversible change. The only legal exits from an irreversible tripwire are re-audit-and-continue-on-a-new-budget, or escalate to owner.
2. **Extension authority mirrors the three-loop binding.** INNER self-extends once; OUTER/STRATEGIC extension is owner adjudication or a re-audit — never self-granted.
3. **A flat budget is a Rule-0 violation in disguise.** Scaled to stakes or it is inert.

**Falsifier (forward-only).** 3/8/3 is validated forward via `docs/notes/audits/rule-2-trip-log.md`, never re-derived from the cfg00–12 history that set it (circular / selection-biased). The wire firing predominantly at hindsight-*productive* moments falsifies the thresholds; an empty trip-log across ≥2 audit cycles falsifies the rule as load-bearing. See ADR §4.

## 16. Iterate exit — closure-resident, typed (added 2026-08-04)

**Canonical source:** `docs/adr/2026-08-04-iterate-closure-exit-mandatory.md` (ADR of record, `Accepted` 2026-08-04; gate 14 self-armed HARD). This section is the canon-side statement; if it and the ADR ever disagree, the ADR wins.

The loop in §1 ends `… O → R → I`, but this file never defined the terminal phase — the only definition lives in the v1 predecessor (`docs/methodology/archive/notion/inqhiori-v1-investigation-framework.md` §8, preserved per §12 for definitional content): *Iterate = specify which phase to return to and what new information triggered the loop-back*; exit criteria *"The next phase has a clear entry packet. No dangling state."*

For compressed Pre-Q work, that exit is discharged **on the closure artifact**, not as a standing phase: Observe is the closure's numbers-vs-§6 assertion (already required by the closure-record format), and Reflect + Iterate collapse into a mandatory typed **`## Iterate`** block — Verdict used / Model update / **Next: INTEGRATE | ITERATE | STOP** / routing / entry packet / stop rule / board write. Template: `.claude/skills/brief-authoring/references/closure_record.md`.

Three rules the ADR fixes that this loop's users must not un-learn:

1. **STOP is a ratified extension, not v1 restatement.** v1's exit is binary (Integrate / Iterate). STOP — Iterate with budget zero, recording the re-proposal bar — is new doctrine owned by the ADR.
2. **ITERATE names a successor; it never opens one.** Parent-Q convention ("named, not opened"): the entry packet freezes what a successor must carry; opening it is a fresh operator GO. Automation never promotes here, same asymmetry as the authorization lifecycle.
3. **Ownership split (Rule 7):** the closure Iterate block owns the per-Q forward disposition; a STATE forward-board row is the cross-session pointer mirror; the SESSIONS Open/next block is the session-level carry. The block's Board-write field records which pointer was written.

This composes with observation routing (§10) rather than competing: narrative-observation routing (Notice-log, per §10's 2026-08-15 correction) routes *observations* between decision points; INTEGRATE / ITERATE / STOP routes *closure verdicts* at the loop exit, pre-registered per verdict in the brief's §6.
