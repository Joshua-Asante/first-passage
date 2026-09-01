# 2026-07-27 — Hermes Agent adoption ruling (third agent surface) + two design-salvage dispositions

**Status:** `CLOSED — RESOLVED-NO-GO` 2026-07-27 (ratified by the operator, chat directive "ratify the NO-GO")
**Canonical decision record:** [`docs/adr/2026-07-27-hermes-agent-adoption-nogo.md`](../../adr/2026-07-27-hermes-agent-adoption-nogo.md) (`Accepted`) · [closure](../closures/2026-07-27-hermes-agent-adoption-closure-resolved.md)
**Authored:** 2026-07-27
**Closed:** 2026-07-27
**Authors:** Joshua (operator) + CC (evaluation + authoring)
**Parent question:** `N/A` — this **is** the parent. Two salvage limbs (A, B) are dispositions under one ruling, not independent Pre-Qs (Known Trap #11: the limbs share a single decision — whether a third agent surface earns a place — and neither is separately gate-able without it).
**Loop:** Ruling — closure gates on the operator accepting or rejecting the NO-GO and dispositioning limbs A and B.
**Artifact path:** `docs/briefs/programs/2026-07-27-hermes-agent-adoption-ruling.md`

---

## §0 — Rule 0 reads (production-source verification)

All anchors verified `git log -1 --format='%h %ci' -- <path>` on 2026-07-27 in worktree `hermes-agent-improvements-80a3b3`. The load-bearing reads are the last two: both **overturned** a premise this evaluation had been running on.

- `docs/adr/2026-07-14-cc-cursor-surface-allocation.md` — anchor `ba943a1` (2026-07-17). Read §2 routing test **Q0** (line 46) and the **2026-07-16 ratified Addendum** (lines 167–190) in full, not the line in isolation (§0 surrounding-context sub-rule). **Premise overturned — see §1(a).**
- `docs/spec/2026-06-23-inqhiori-sentinel-design.md` — anchor `f2be990` (2026-07-11). Read the Tier-1/2/3 pipeline diagram, the **v1 implementation scope** paragraph, §4.3, §6 cadence, §7.5 token budget. **Premise overturned — see §1(b).**
- `docs/briefs/pre-registration/Q-XMEM-1-verdict-preregistration.md` — anchor `a6a0eef` (2026-07-16). Frozen §6 table, allowlist/denylist, hosting-preference paragraph. Status `ARCHITECTURE FROZEN`, **T0 not started**.
- `docs/briefs/Q-XMEM-1-cross-surface-memory-sidecar-pilot.md` — anchor `a6a0eef` (2026-07-16). §5 exposure-boundary clause (line 104).
- `ops/sentinel/scan.py` — anchor `abb12ae` (2026-07-16). Tier-1 scanner exists; `ROUTING = ("Action", "Forward", "Closed")` is already a strict record type.
- `docs/notes/sentinel/queue.md` — anchor `9c849f9` (2026-06-23). Exactly **1** run block. Operator states (2026-07-27, chat) the cadence was never scheduled and has since been fixed — recorded as operator attestation, not independently verified here.
- `scripts/check_advisor_dedup.py` — anchor `1ee6f4c` (2026-07-25). Docstring self-declares it is a search assistant, not a gate.
- `.claude/workflows/` — **directory does not exist** (verified `ls`). `rg --no-ignore -l "inqhiori-probe"` returns only doc references (spec, plan, `docs/notes/sentinel/README.md`, `SESSIONS-2026-Q2.md`) — **no workflow artifact is committed anywhere in the repo.**

**Product-side evidence** is the 30-claim verified ledger from workflow run `wf_78a079de-889` (2026-07-27; 28 CONFIRMED / 1 REFUTED / 1 UNVERIFIABLE, each re-checked against primary sources by an independent verifier). Not a repo path; cited as session apparatus. Load-bearing entries reproduced in §2.

---

## §1 — Context & motivation

The operator asked how Nous Research's **Hermes Agent** (`github.com/NousResearch/hermes-agent`, MIT, launched 2026-02-25) could improve this repo. A 14-agent evaluation (4-modal research → 3 adversarial verifiers → 4 brainstorm lenses → 3-judge panel) produced 19 candidate applications. The judge panel killed or conditioned every candidate that placed Hermes inside the operating perimeter, and three candidates survived unanimously — two of which are *design imports*, not adoptions.

Two premises the evaluation ran on were then falsified by §0 reads, and both corrections **narrow** the case for adoption:

**(a) "Question 0 categorically bars CC and Cursor from tasks touching Pine source / vendor CSVs, so a local model is the only permitted automation."** False. The ratified Addendum's root cause is *dispatch-environment blindness*: a Cursor **cloud** checkout structurally cannot hold gitignored bytes, and a key configured for one session is not evidence it is present in another. The remedy routes such tasks to **`local`** — i.e. Claude Code running locally, where the bytes are present — and those bytes still reach the Anthropic API. Q0 is a *where-does-this-dispatch* test, not an egress rule. Four candidates (#4/#6/#10/#17) and the interim summary given to the operator rested on the false reading; all are corrected here.

**(b) "Sentinel Tier-2/Tier-3 were designed but never built."** Imprecise in a way that changes the fix. The spec's **v1 implementation scope** states Tiers 2–3 "are **not new code** — they are the saved probe workflow (`inqhiori-probe-iteration-1-wf_*.js`), promoted to a named, reusable workflow and documented as the quarterly full-run procedure." §7.5 prices the full run at ~728K tokens and calls it "acceptable quarterly, not weekly, **which is exactly why Tier-1 is deterministic**." So the design never wanted a weekly LLM tier — and every candidate proposing one contradicted the ratified design's own reasoning. What is actually missing is the **promotion step**: no workflow artifact is committed (§0). §6 of the spec also already contemplates `/schedule` or a cron cloud agent for Tier-1, i.e. the incumbent stack.

Standing doctrine bearing on this: the CC/Cursor surface-allocation ADR (`Accepted` 2026-07-14) names exactly two agent surfaces; `STATE.md` records operator-hours as the binding resource while agent-hours are cheap and budgeted; the lifecycle doctrine permits automation to move authorization **down only**.

---

## §2 — Prior art / lineage

- **`docs/adr/2026-07-14-cc-cursor-surface-allocation.md`** (`Accepted`; Addendum ratified 2026-07-16) — the governing allocation. Any third standing agent surface requires an amendment; its dual-limb falsifier already rides 2026-08-08.
- **`docs/spec/2026-06-23-inqhiori-sentinel-design.md`** — Tier-1 shipped (`ops/sentinel/`); Tier-2/3 = unpromoted quarterly workflow. §7 guardrails (human-gated D, forbidden-D audit trail, degeneration tripwire, not-an-alpha-engine, token budget) bind anything built here.
- **`Q-XMEM-1`** (`OPEN`, architecture frozen 2026-07-16, **T0 not started**) — limb A touches its frozen pre-registration; see §3(A) for why this is a routing decision, not a free substitution.
- **Verified product ledger** (`wf_78a079de-889`) — load-bearing entries: model-agnostic over any OpenAI-compatible endpoint incl. local (**the one capability CC/Cursor lack**); Windows Tier-1 no-admin install; first-class prompt-free cron with fail-closed model snapshot and always-alert-on-failure; MCP client+server; FTS5 verbatim session search with **no LLM in the retrieval path**. Against those: default approver is *an auxiliary LLM* (`approvals.mode: smart`); `local` backend has **no sandbox**; container backends **skip approvals entirely** (sandbox XOR approvals, never both); **no token or dollar spend cap exists in configuration**; loop hard-stop, checkpoints, and memory write-approval all default **OFF**; independent security audit [issue #7826](https://github.com/NousResearch/hermes-agent/issues/7826) (4 Critical / 9 High, "ALLOW-ALL" default posture, filed 2026-04-11) remains open and unanswered; a maintainer edited a third party's plagiarism-allegation issue down to "." and closed it not-planned (GitHub edit log confirms the edit). Adoption-relevant engagement anomaly: ~221K stars against 843 watchers, single-digit independent hands-on accounts, and the one identified user of both tools preferred Claude Code.
- **Memory lesson `feedback_verify_source_not_label`** — open the source before acting. Both §1 corrections are instances; the interim operator summary shipped before the source was opened.

---

## §3 — Question

**Pre-Q gate test (symptom-only rephrase):** *"Judgment-shaped work in this repo is done by hand and consumes the binding resource; a third-party agent product was proposed as relief. What does that product actually offer that the current surfaces do not, and what — if anything — transfers?"* Passes: names the cost and the uncertainty, prescribes no tool.

**Q-HERMES-1:** Does Hermes Agent offer this operation any capability that the ratified CC + Cursor allocation cannot deliver, and if not, which of its design properties are worth importing without the dependency?

Two forked dispositions, both downstream of the ruling:
- **Limb A** — how should the FTS5-verbatim-retrieval design interact with the frozen `Q-XMEM-1` pre-registration?
- **Limb B** — what closes the Sentinel Tier-2/3 gap, given it is a promotion step rather than a build?

---

## §4 — Falsifiable hypothesis

**H-HERMES-1:** Hermes Agent's candidate value to this operation reduces entirely to (a) transferable design patterns and (b) a local-inference lane whose uniqueness depended on Question 0 being an egress rule. Since §0 verified Q0 is a dispatch-environment test — CC-local is the *prescribed* surface for gitignored-byte tasks, and those bytes already reach the Anthropic API by accepted practice — limb (b) collapses, and **no candidate application requires adopting the product**. Disposition: **NO-GO for any standing surface, with design salvage.**

**H-HERMES-1 is falsified if** a candidate application is named that simultaneously: (i) delivers measurable operator-hour relief; (ii) cannot be delivered by CC-local, Cursor, the cursor-agent bridge, or a plain script; **and** (iii) does not require protected bytes to reach an external endpoint or a third-party agent to hold host execution rights inside the perimeter. Any one of the three failing leaves H standing.

**Accept H-HERMES-1 (RESOLVED-NO-GO) if** the operator reviews the 19-candidate slate and names no such candidate, and both salvage limbs are dispositioned per §6.

**Ambiguous-hold if** the operator judges the residual zero-egress argument (bytes reaching Anthropic at all) to be live doctrine rather than settled practice — that reopens limb (b) on a *policy* basis, not a capability one, and requires an operator ruling on egress posture before this brief can close.

---

## §5 — Forbidden moves

Each of these was genuinely tempting in this session; several were actually committed before §0 reads caught them.

- **Reporting the judge panel's conclusions as findings without opening the sources they rest on.** Committed: the interim summary told the operator that Q0 "categorically barred" CC/Cursor and that Tier-2/3 were "never built." Both were wrong, and both were cheap to check. This is `feedback_verify_source_not_label` and `feedback_run_cheap_falsifier_before_authoring` firing together.
- **Substituting FTS5 for Mem0 inside the frozen `Q-XMEM-1` pre-registration and calling the question closed.** Ruled out: the frozen contamination limb is *defined around* an extraction LLM that paraphrases (Trap M-AHF is cited by name in the pre-registration). A deterministic retriever satisfies that limb vacuously, so the gate would pass without measuring what it was built to measure. Pre-T0 amendment is permitted; silent instrument substitution is not (Known Trap #12).
- **Proposing a weekly LLM Sentinel tier.** Ruled out by the spec's own §7.5 token-budget reasoning — quarterly is a deliberate design choice, not an unmet ambition. Several killed candidates proposed exactly this.
- **Building limb B against a cadence failure that no longer exists.** The operator fixed the scheduling gap on 2026-07-27; any design premised on "the cadence is dead" is now premised on a false state.
- **Letting an autonomous agent hold write access to a governance surface** (`STATE.md`, ADRs, ledgers, `lab/CATALOG.md`) — barred by the Sentinel spec's own §7.1 human-gated-D guardrail regardless of which product is used.
- **Running Hermes anywhere inside the perimeter on the strength of a "no telemetry" claim.** That claim is vendor self-report in primary docs only; no independent packet-level audit exists, and the claim is narrower than it reads (web tools, Portal, MCP servers all reach third parties when configured).
- **Outcome-conditional D-tests** — categorically forbidden; they encode the conclusion into the analysis.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED-NO-GO` | Operator reviews the 19-candidate slate and names **no** candidate meeting all three §4 falsifier conditions, **and** limbs A + B are dispositioned below | Record the scoped negative ruling (§7 limb B2); close this brief; no third surface |
| `FALSIFIED` | Operator names ≥1 candidate meeting §4 (i) **and** (ii) **and** (iii) | Open a dedicated Pre-Q for that candidate with its own pre-registration; allocation-ADR amendment becomes a prerequisite, not an afterthought |
| `AMBIGUOUS-HOLD` | Operator rules the zero-egress question live doctrine (§4 ambiguous limb) | Hold; requires an egress-posture ruling first. Re-test window: co-schedule with the allocation ADR's dual-limb falsifier review, **2026-08-08** |

**Limb A gate (Q-XMEM-1 routing) — operator picks exactly one:**

| Option | What it means | Consequence |
|---|---|---|
| **A1 — Amend pre-T0** | Broaden the frozen architecture to admit a deterministic-retrieval arm, with a **rewritten** contamination limb that is non-vacuous for a retriever (a retriever cannot paraphrase, so the limb must instead test *what the writer stores*) | Permitted: T0 has not started, and the v1.1 precedent establishes pre-T0 revision is not Trap #12. Requires a new pre-registration commit before any index is built |
| **A2 — Fork** | Leave `Q-XMEM-1` frozen; open a separate Pre-Q for deterministic cross-surface retrieval | Cleanest on discipline; costs a second brief and leaves `Q-XMEM-1` open and unstarted |
| **A3 — Delete (The Algorithm)** | Treat FTS5 retrieval as a *Delete* move: if verbatim search over session logs plus the 904-file corpus removes the felt cost, the sidecar question is **mooted**, not answered | Strongest if it holds. Requires a stated pre-condition: `Q-XMEM-1` may only be closed `MOOT` if the operator confirms the original cost no longer bites — not merely that a new tool exists |

**A-limb falsifier (binds under A1 and A3):** FTS5 keyword retrieval under-recalls paraphrase relative to embeddings. Pre-register a recall spot-check against known `lab/CATALOG.md` cross-references **before** building the writer; if recall on that fixture set is materially worse than the incumbent, the deterministic route fails on its merits and the extraction-sidecar question returns intact.

> **Threshold defect corrected at pre-registration (2026-07-27).** As first drafted this falsifier read "materially worse than the operator's own manual-search baseline" — unmeasurable, and a Known-Trap-#5 vague gate in a brief that flags Trap #5. The comparator is now the **incumbent retrieval that exists today (ripgrep literal search)**, which is the thing a Delete must actually beat, with binary thresholds frozen in [`docs/briefs/pre-registration/2026-07-27-fts5-delete-falsifier-prereg.md`](pre-registration/2026-07-27-fts5-delete-falsifier-prereg.md).

**OPERATOR RULING 2026-07-27 — limb A resolved as `A3` (Delete).** FTS5 verbatim retrieval is treated as a *Delete* move against `Q-XMEM-1`, not as a substitute instrument inside its frozen architecture. Consequences, binding:

- `Q-XMEM-1` is **not** amended and **not** re-instrumented; its frozen v1.1 architecture stands untouched. It closes `MOOT` only on the §6 A3 pre-condition — the operator confirming the original cost no longer bites — and **never** merely because a retriever shipped.
- The A-limb falsifier runs **first**, against the pre-registered thresholds, **before** any writer or index is built for production use.
- If the falsifier fires, the Delete has failed on its merits: `Q-XMEM-1` returns intact and un-mooted, and A1/A2 become live options again.

**Limb B gate (Sentinel Tier-2/3):**

| Verdict | Trigger |
|---|---|
| `B-RESOLVED` | The quarterly full-run exists as a **committed, named workflow artifact** (`.claude/workflows/`), producing the spec's two artifacts — a routed queue entry in `docs/notes/sentinel/queue.md` and a non-empty `docs/notes/audits/sentinel-gate-audit.md` whenever it routes anything `Closed` — and has been exercised once against the 2026-08-08 slate |
| `B-FALSIFIED` | The first real run produces a Forward-queue burst rather than the spec's expected near-silence, indicating the tool is generating directions rather than hygiene (spec §7.3 degeneration tripwire) |

---

## §7 — Execution plan

Self-executing; no CC handoff required. **Nothing below runs before §6 limb A is dispositioned by the operator.**

- **Phase 0 — Ratification.** Operator accepts/rejects `RESOLVED-NO-GO` and picks A1 / A2 / A3.
- **Phase A1 — Recall falsifier first.** Build the `lab/CATALOG.md` cross-reference fixture and measure FTS5 recall **before** writing any indexer. Falsifier fires here or not at all.
- **Phase A2 — Sidecar (only if A-limb falsifier passes).** Deterministic FTS5 index over CC/Cursor session logs + the 904-file corpus, explicitly including the cold store (`lab/archive/`, `docs/ltm/`) that `.rgignore` excludes from default search — this also closes the documented empty-Grep-over-LTM trap. Rule-7 denylist implemented as a **mechanical reject-list in the writer**, not a review obligation. Scope frozen at *search + staged write*: no summarization (that path re-creates the retired weekly-review-feeder).
- **Phase B1 — Promote the workflow.** Author the quarterly full-run as a committed named workflow implementing the spec's Tier-2 (D-S-A gate, forbidden-D flagging, C/A/F routing) and Tier-3 (adversarial candidate kill) passes. Report-only; writes confined to `docs/notes/sentinel/` and the gate-audit log per spec §5. Budget-capped per §7.5; **quarterly, not weekly.**
- **Phase B2 — Record the negative ruling.** One paragraph, scoped to *rail-adjacent and credentialed surfaces*, so the adoption question is not re-litigated per session — and scoped no wider, so it does not foreclose a future isolated experiment. Placement (ADR vs a rejected-tooling registry entry) is an operator call under Rule 7; this brief does not create a governance surface unilaterally.

**Salvage carried out of the killed candidates:** add a deterministic **alert-shadowing lint** to `scripts/check_pine_manifest.py` targeting the informational-`alert()`-shadows-JSON defect class that cost the 2026-07-21 first-fire. This is independent of the ruling and worth doing either way — the failing candidate (#10, a local-model Pine auditor) was killed, but its diagnosis was sound.

---

## §8 — Verdict pre-registration

This brief **is** the pre-registration for the ruling (§4 + §6 written before any limb executes). Limb A additionally requires its own pre-registration file at `docs/briefs/pre-registration/` **before** Phase A2 builds anything, containing the recall-fixture threshold — under A1 that file supersedes the frozen `Q-XMEM-1` architecture and must record the supersession explicitly.

Pre-registration commit hash: `<populated at commit>`
Pre-registration date: 2026-07-27

---

## §9 — Closure record format

- **If `RESOLVED-NO-GO`:** `docs/briefs/closures/2026-07-27-hermes-agent-adoption-closure-resolved.md` — records the ruling, both limb dispositions, and the two §1 premise corrections as lesson candidates.
- **If `FALSIFIED`:** closure names the surviving candidate and opens its Pre-Q.
- **If `AMBIGUOUS-HOLD`:** closure states the egress-posture question as the blocking input, re-test 2026-08-08.

Closure must record: which A-option was chosen and why; whether the A-limb recall falsifier fired; whether limb B's first run tripped the §7.3 degeneration tripwire; and the disposition of the `check_pine_manifest.py` lint salvage.

---

## §10 — Audit hooks (runnable)

```bash
# §0 anchors still resolve (re-verify before citing this brief downstream)
git log -1 --format='%h %ci' -- docs/adr/2026-07-14-cc-cursor-surface-allocation.md   # expect ba943a1
git log -1 --format='%h %ci' -- docs/spec/2026-06-23-inqhiori-sentinel-design.md      # expect f2be990
git log -1 --format='%h %ci' -- docs/briefs/pre-registration/Q-XMEM-1-verdict-preregistration.md  # expect a6a0eef

# §1(a) correction holds: Q0 is a dispatch-environment test, not an egress rule
rg -n "dispatch environment|structurally cannot have those bytes|local\*\*, full stop" \
   docs/adr/2026-07-14-cc-cursor-surface-allocation.md

# §1(b) correction holds: Tiers 2-3 are a promotion, not a build
rg -n "not new code|acceptable quarterly, not weekly" docs/spec/2026-06-23-inqhiori-sentinel-design.md

# Limb B open/closed: does a committed named workflow exist yet?
ls .claude/workflows/ 2>/dev/null || echo "LIMB B OPEN - no workflow artifact committed"

# Limb B guardrail: gate-audit log must have DATA ROWS whenever an LLM run routes anything Closed.
# NB: `test -s` is the wrong hook here (Trap M-AHF) - the file ships with a header and a table
# skeleton, so byte-nonempty reads as "populated" while zero forbidden-D-tests are logged.
# Count date-led table rows instead. Verified 2026-07-27: 0 rows (no LLM tier has ever run).
rg -c '^\| 20[0-9]{2}-' docs/notes/audits/sentinel-gate-audit.md || echo "gate-audit has ZERO data rows"

# Sentinel cadence actually firing (operator reports fixed 2026-07-27 - verify, do not assume)
rg -c "^## " docs/notes/sentinel/queue.md   # was 1 run block on 2026-07-27; expect growth

# Q-XMEM-1 still frozen and unstarted (limb A has not silently moved)
rg -n "ARCHITECTURE FROZEN|T0 not started" docs/briefs/pre-registration/Q-XMEM-1-verdict-preregistration.md
ls docs/notes/pilots/q-xmem-1/TALLY.md 2>/dev/null && echo "T0 HAS STARTED - limb A options changed"

# Salvage item landed?
rg -n "alert" scripts/check_pine_manifest.py | rg -i "shadow|informational" || echo "lint salvage NOT landed"
```

---

## Verification

```bash
# Discipline checks (mechanical)
python scripts/check_brief.py docs/briefs/programs/2026-07-27-hermes-agent-adoption-ruling.md --type brief
# Expected: exit 0, no HARD violations

# Repo gates (this brief adds a docs/ file only; no code, data, or Pine surface touched)
python scripts/check_root_doc_liveness.py
python scripts/check_path_liveness.py
```

---

## Pre-Lock Checklist

- [x] §0 paths read and anchored with commit hashes, verified 2026-07-27
- [x] §0 read with surrounding context, not line-isolation (both corrections came from this)
- [x] §3 question passes the symptom-only rephrase test
- [x] §4 hypothesis falsifiable with a three-condition falsifier
- [x] §5 forbidden moves genuinely tempting — two were actually committed this session
- [x] §6 gates binary; limb A is an enumerated operator choice, not "decide later"
- [x] §10 audit hooks runnable
- [x] Operator ratification (Phase 0) — 2026-07-27, chat directive "ratify the NO-GO" (see header and [closure](../closures/2026-07-27-hermes-agent-adoption-closure-resolved.md))
- [x] Limb A pre-registration committed before Phase A2 — committed 2026-07-27 as [`pre-registration/2026-07-27-fts5-delete-falsifier-prereg.md`](pre-registration/2026-07-27-fts5-delete-falsifier-prereg.md); Phase A2 sidecar built (`ops/recall/`) per closure
