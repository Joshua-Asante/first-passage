# Cursor Handoff — post-batch residue: CLAUDE.md skew fix (a) + HARV lane-ratification ADR draft (b) + D1 successor-risk Pre-Q scaffold (c)

**Date:** 2026-07-13
**Parent session:** claude.ai advisor (Joshua + Claude) — the repo-priorities triage session (2026-07-13). Four independent priority lenses + adversarial synthesis ranked the post-2026-07-13-batch residue; this handoff executes the three lowest-friction items that fell out of that triage — items (a)/(b)/(c) the parent offered.
**Spawn target:** Cursor (docs-only — no research venv needed; no data pull, no MC, no test build)
**Repo:** `multi_firm_operations`
**Brief type:** Cursor handoff (multi-step; three independent steps)
**Parent question:** `N/A` — not executing a Pre-Q or a locked ADR. Two of the three deliverables are themselves *new* decision artifacts (b = an ADR draft; c = a Pre-Q scaffold), authored `Proposed`/`DRAFT` for operator ratification.
**Authority:** Joshua (CEO). claude.ai authored this brief; Cursor executes. **No commit/merge without Joshua's go.** **Docs-only mandate:** the only non-doc file touched is `CLAUDE.md`, and only its **§Firm Expansion prose** — no core executable line, no locked parameter, allocation, `dd_protection` constant, `ACTIVE_FIRM`, test pin, or Pine byte. No `core/` edit. No MC run, no Databento call, no `register_search`.

**Workspace pin (load-bearing):** branch off **`origin/main` @ `53c27fe`** (2026-07-13, "Merge PR #366"). All §0 prereqs are verified present at that commit (None-guards in `dd_protection.py`; Q-HARV-0 closure; no HARV ADR; survivor-scoring prereg). Do **not** build inside the operator session worktree `.claude/worktrees/disc-camp-0-first-pull-ce9c73` (Windows file-lock + collision risk). In Cursor's own workspace: `git fetch origin && git checkout -b cursor/post-batch-doc-artifacts origin/main`.

> **Binding context (read first — this scopes what each step is and is NOT).**
> A large batch landed on `main` 2026-07-13: DISC-CAMP-0 closed FALSIFIED (pipeline proven end-to-end, K=3,177 banked); survivor-scoring harness (PR #366) + frozen pre-registration (PR #358) + engine pre-flight (PR #356) + prop_envelope v1.0 + dd_geometry all merged. These three items are the *residue* that batch left:
> - **(a)** is a confirmed **live doc/code skew** — a clean mechanical fix, the only unambiguous `DONE` on this handoff.
> - **(b)** is a doctrine ADR whose sole blocking condition (DISC-CAMP-0 closing) cleared 2026-07-13. Cursor **assembles the `Proposed` draft from named, already-written sources**; the ratification (`Proposed`→`Accepted`) and the one open doctrine decision are **operator-owned, out of scope** (§0.5-Q).
> - **(c)** is the D1 successor self-funded risk-framework **Pre-Q**. Cursor produces the **structure + the ADR-mandated constraints transcribed verbatim** — it does **NOT author the question's framing or invent any numeric risk objective** (the rescope ADR §5 forbids "numbers before question," and the risk objective — max-DD line, time-under-water, withdrawal model — is Joshua's to define in a later session). Scaffold, not authorship.
>
> **Executor-fit note (honest):** (a) is squarely Cursor-shaped. (b)/(c) are *assembly/scaffold* tasks with hard reserved-for-operator boundaries stated per step — the value delivered is removing the structural boilerplate, not making the decisions. If any step's judgment boundary feels wrong after Phase 0, return `NEEDS_CONTEXT` rather than proceed.

---

## §0 — Rule 0 reads (PHASE 0 — execute BEFORE any edit)

Cursor: read each item and post a read-report in your first response **before** writing anything. If repo state contradicts a §2 assumption (e.g. a None-guard is absent, or a HARV ADR already exists), return `NEEDS_CONTEXT` with the discrepancy quoted.

**For (a) — the skew fix:**
- `CLAUDE.md` §Firm Expansion, **lines 117–121** — report the §Firm Expansion paragraph verbatim (the stale sentence is line 119: *"…divide `daily_loss_pct` by 100 — a `TypeError` for every configured firm with `daily_loss_pct: None` (9 of the 10 current configs)…"*).
- `CLAUDE.md` §Strategy Reference MC-anchor blocks + the "Strategy Reference (LOCKED)" markdown table — report **that these exist and where** (approx. line ranges) so you can confirm you will **NOT** touch them. `scripts/verify_lock_anchors.py` and `scripts/validate_params.py` parse those surfaces; §Firm Expansion prose is not parsed by either, but you must not stray into the parsed surfaces.
- `core/dd_protection.py` lines **72–78** — report the None-guard (`DAILY_LOSS_LIMIT = _F["daily_loss_pct"] / 100 if _F["daily_loss_pct"] is not None else None`) + its "None-tolerant per the engine pre-flight (2026-07-13)" comment.
- `core/mc/modes.py` **53–55**, `core/mc/simulation.py` **18–23**, `core/mc/preflight.py` **104–108** — report each None-guard (all four sites are now None-tolerant; the doc claims they `TypeError`).
- `core/firm_rules.py` lines **14–18** — report the docstring that already carries the corrected framing (*"…now None-tolerant (they divide daily_loss_pct by 100 only when it is not None — byte-identical under ACTIVE_FIRM=FXIFY, no longer a TypeError latent on the None value most prop[-firm tiers]…"*). **Your (a) reframe mirrors this wording.**
- Derive the current tier count: report `python -c "from core.firm_rules import FIRM_RULES; n=len(FIRM_RULES); k=sum(1 for v in FIRM_RULES.values() if v.get('daily_loss_pct') is None); print(n,k)"` (or an equivalent read). This replaces the stale "9 of the 10" — **do not hardcode a count you did not derive.**

**For (b) — the HARV lane-ratification ADR:**
- `docs/briefs/closures/Q-HARV-0-month-end-rebalance-ES.md` — report **the whole file**, especially the section **"Lane observations (for deferred HARV ADR — appendix harvest)"** and **"What a fresh brief would need"**. This is the primary source; the ADR harvests it.
- `docs/adr/2026-07-11-discovery-campaign-defaults-ratified.md` and `docs/adr/2026-07-11-tradable-anomalies-statistics-adoption.md` — report §Decision + the forward-board/§7 sections. These are the standing discovery-campaign governance chain the HARV lane ADR sits **within** (it ratifies a lane, it does not supersede these).
- `docs/adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md` — report §Decision (K-floor + V=1/n pin) — the third governance-chain piece.
- `docs/briefs/DISC-CAMP-0-closure-falsified.md` — report the process-defect log (PD-1…PD-8) + the §verdict. DISC-CAMP-0 (mechanism-blind shakedown) is the **second evidence point** for the lane ADR; Q-HARV-0 (mechanism-first) is the first.
- `git ls-tree origin/main docs/adr/ | grep -i harv` — report the result (expect **empty**; if a HARV ADR exists, `NEEDS_CONTEXT`).

**For (c) — the D1 successor-risk Pre-Q scaffold:**
- `docs/adr/2026-07-11-challenge-era-claims-rescope.md` — report **§4 (Falsifier / completion falsifier)**, **§5 (Forbidden moves)**, and **§7 Deferred (D1 line)** verbatim. These are transcribed into the scaffold's gate + forbidden-moves; do not paraphrase.
- `docs/notes/audits/programme-audit/2026-07-11-core-fxify-anchoring-audit.md` — report **§5.2 / D1** (the successor-risk-framework question as the audit framed it).
- Confirm the decompound/withdrawal-model machinery exists (the rescope ADR's "closest existing instrument"): `git ls-files | grep -i decompound` and report `lab/analysis/regime/decompound_remc_2026-06-07/` presence — the scaffold's §0 names it as the reference instrument.

**Templates (read before authoring b and c):**
- `.claude/skills/brief-authoring/references/adr.md` (for b) and `.claude/skills/brief-authoring/references/inquire_brief.md` (for c) — copy-and-fill; do not re-derive structure from memory.

**Anchors:**
- `git log -1 --format='%h %ci' -- CLAUDE.md` and `-- docs/briefs/closures/Q-HARV-0-month-end-rebalance-ES.md` — report commit + date.

After Phase 0: post the read-report; proceed to §2 only once §0.5 is resolved.

---

## §0.5 — Clarifying questions (HALT-ON-AMBIGUITY)

Parent-recommended defaults stated; confirm or challenge in the Phase-0 response. Set `Status: NEEDS_CONTEXT` until resolved.

- **(P) HARV lane ADR — new ADR vs amendment?** **Recommended default:** a **new** ADR (`docs/adr/2026-07-13-harv-discovery-lane-ratification.md`, status `Proposed`) that ratifies the **mechanism-first discovery lane** as standing doctrine and **cross-references** (does not supersede) the 2026-07-11 defaults + statistics ADRs and the 2026-07-12 DSR-K ADR. If Phase-0 reading shows the lane is already fully specified inside the defaults ADR (making a new ADR redundant), ASK.
- **(Q) HARV lane ADR — the gate-reachability step is the central OPEN decision; Cursor must NOT resolve it.** The Q-HARV-0 closure's load-bearing lane lesson is that RESOLVED was structurally unreachable *before any data arrived* (placebo window ⊂ conditioning window). The ADR's core proposal is a **mandatory pre-registration reachability simulation of every bundled clause under a plausible-true world**. Whether that becomes a **HARD gate** (blocks `register_search open`) or a **recommended step** is an operator call. **Cursor writes both options into §3 (Alternatives) and states the recommendation as the §2 Decision, but leaves status `Proposed`** — the operator ratifies. Do not pick.
- **(R) D1 Pre-Q — confirm scaffold-only.** **Recommended default:** Cursor fills §0 (reads), §1 (context), §5 (forbidden moves, transcribed from rescope §5), §6/§4-gate (completion falsifier, transcribed from rescope §4), §10 (audit hooks). Cursor writes §4 (the falsifiable question) and the risk-objective dimensions as **`[OPERATOR INPUT REQUIRED]` placeholders with guardrail notes** (symptom-not-fix framing; no numeric target). Status `DRAFT`. Confirm this split, and confirm the filename/ID: default `docs/briefs/Q-SFRISK-1-successor-self-funded-risk-framework.md` (contains "successor" + "self-funded" so the rescope ADR §10 hook fires).

---

## §1 — Context

The 2026-07-13 batch closed the prop-portfolio program's tooling gap (scoring harness, pre-registration, engine pre-flight, envelope v1.0). Three residue items remain, each independent:

**What Cursor is asked to produce:**
- **(a)** An edited `CLAUDE.md` §Firm Expansion paragraph — the stale present-tense `TypeError` claim reframed to past tense, citing the 2026-07-13 engine pre-flight (PR #356) that made the four division sites None-tolerant; the `daily_loss_pct=None` **pre-flight doctrine preserved**; the "9 of the 10" count replaced by the Phase-0-derived count (or the "most prop-firm tiers" framing mirroring `firm_rules.py:17`).
- **(b)** `docs/adr/2026-07-13-harv-discovery-lane-ratification.md` — status **`Proposed`** — harvesting the Q-HARV-0 lane observations + the DISC-CAMP-0 defect log into a standing mechanism-first-discovery-lane doctrine ADR, with the gate-reachability step as the central decision (both options in §3).
- **(c)** `docs/briefs/Q-SFRISK-1-successor-self-funded-risk-framework.md` — status **`DRAFT`** — the D1 Pre-Q **structure** with the rescope-ADR-mandated constraints transcribed and the risk objective left as operator-input placeholders.

**What Cursor is NOT asked to do:**
- Ratify (b): status stays `Proposed`. Resolve §0.5-Q's gate-reachability decision. Set (c) to anything past `DRAFT`.
- **Author (c)'s question framing or any numeric risk objective** (max-DD line, withdrawal rate, time-under-water tolerance) — that is Joshua's, in a later session; inventing it violates rescope ADR §5.
- Touch the `CLAUDE.md` MC-anchor blocks or the Strategy Reference (LOCKED) table (parser-load-bearing).
- Touch any `core/` executable line, locked parameter, allocation, `dd_protection` constant, `ACTIVE_FIRM`, test pin, or Pine; run any MC / Databento pull / `register_search`; add deps.
- The "while I was in there" refactor of anything outside these three files.

---

## §2 — Execution plan

Three independent steps + a closure. No TDD (docs-only); the gates are grep/parser checks, not tests.

### Step 2.1 — (a) CLAUDE.md §Firm Expansion skew fix
- **Inputs:** the §Firm Expansion paragraph; the four None-guard sites; `firm_rules.py:14–18`; the Phase-0-derived tier count.
- **Action:** reframe **only** the stale clause. From present-tense *"divide `daily_loss_pct` by 100 — a `TypeError` for every configured firm with `daily_loss_pct: None` (9 of the 10 current configs)"* to past-tense that (i) states the sites **were** a latent `TypeError` on `daily_loss_pct=None`, (ii) records that the **2026-07-13 engine pre-flight (PR #356)** made `dd_protection.py` / `mc/modes.py` / `mc/simulation.py` / `mc/preflight.py` None-tolerant (byte-identical under `ACTIVE_FIRM=FXIFY`), (iii) **keeps the standing doctrine** ("run an engine-support pre-flight; the 'everything downstream adapts automatically' doctrine was falsified"), and (iv) uses the derived count or "most prop-firm tiers carry `daily_loss_pct: None`". Leave the `bust_trailing`/`trailing_locking` bespoke-branch clause and the `ACTIVE_FIRM` historical-fixture sentence intact.
- **Expected output:** one edited paragraph in `CLAUDE.md`; no other line changed.
- **Per-step gate:** `python scripts/verify_lock_anchors.py` → `ROUTING: Closed`; `python scripts/validate_params.py` → `0 HARD` (proves the MC-anchor/table parsers are untouched). `git diff --stat CLAUDE.md` shows only §Firm Expansion lines.

### Step 2.2 — (b) HARV lane-ratification ADR draft (`Proposed`)
- **Inputs:** `references/adr.md` template; the Q-HARV-0 closure (esp. "Lane observations" + "What a fresh brief would need"); the DISC-CAMP-0 closure defect log; the three governance-chain ADRs.
- **Action:** author `docs/adr/2026-07-13-harv-discovery-lane-ratification.md` (status `Proposed`). §0 = the reads above with anchors. §1 = context (two campaigns run: Q-HARV-0 mechanism-first AMBIGUOUS on a structurally-unreachable placebo; DISC-CAMP-0 mechanism-blind FALSIFIED clean — the lane is proven, the doctrine is owed). §2 = the Decision: ratify the mechanism-first discovery lane + **the parent recommendation** that a pre-registration gate-reachability simulation of every bundled clause become mandatory. §3 = Alternatives incl. **both** §0.5-Q options (hard gate vs recommended step) with the trade-off. §4 = a falsifiable success bar for the lane doctrine (e.g. "the next mechanism-first campaign's bundled clauses are all reachability-simulated pre-freeze; FALSIFIED if a clause again proves structurally unreachable post-hoc"). §5 = forbidden moves (harvested honestly). §10 = runnable hooks. **Every load-bearing claim traces to a Phase-0 read — no invented lane doctrine.**
- **Expected output:** the `Proposed` ADR file.
- **Per-step gate:** `python scripts/check_brief.py docs/adr/2026-07-13-harv-discovery-lane-ratification.md --type adr` → all checks PASS; status line reads `Proposed`; §3 contains both gate-reachability options.

### Step 2.3 — (c) D1 successor-risk Pre-Q scaffold (`DRAFT`)
- **Inputs:** `references/inquire_brief.md` template; rescope ADR §4/§5/§7; audit §5.2/D1; the decompound machinery path.
- **Action:** author `docs/briefs/Q-SFRISK-1-successor-self-funded-risk-framework.md` (status `DRAFT`). Fill: §0 (reads — rescope ADR, audit §5.2, decompound instrument, with anchors); §1 (context — P(pass) retired with the venue; self-funded capital has no risk-acceptance criterion; decompound/withdrawal-model machinery is the closest instrument); §5 (forbidden moves — **transcribe rescope §5 verbatim**, esp. "numbers before question" + "reusing 99.83/0.17/4.37 as a live number" + best-of-K); §6 gate + §4 completion falsifier (**transcribe rescope §4 verbatim**: pre-registered by **2026-11-08** else the re-scope is incomplete and D1 escalates to a **mandatory blocker on any Aegis→M6J go-live**); §10 (audit hooks — include the rescope §10 hook `ls docs/briefs/ docs/briefs/pre-registration/ | grep -i "self-funded\|successor"` which this file must now make fire). **Leave as `[OPERATOR INPUT REQUIRED]` with guardrail notes:** §4's falsifiable question (guardrail: name the *symptom* — "self-funded capital has no risk-acceptance criterion" — not a fix; do not bake in a max-DD number) and the risk-objective dimensions (operator max-DD line, time-under-water tolerance, withdrawal model — **placeholders only, no values**).
- **Expected output:** the `DRAFT` Pre-Q scaffold file.
- **Per-step gate:** `python scripts/check_brief.py <file> --type inquire` → passes the mechanical checks OR flags only the intentionally-empty operator-input §4 (report which); **grep confirms zero numeric risk targets were invented** (no `%`-DD figure, no withdrawal rate, no month count in §4/risk-objective placeholders); the rescope §10 hook now returns a hit instead of "NOT YET".

### Step 2.4 — Closure report
Post the §6-format closure report. Do **not** commit; do **not** ratify (b) or advance (c). List each file touched + each per-step gate result.

---

## §4 — Falsifiable hypothesis

**H:** `N/A — this handoff executes doc authoring, no hypothesis is under test.` (a) is a mechanical doc fix; (b) authors a *new* `Proposed` ADR whose own §4 success bar Cursor writes; (c) **transcribes** a parent completion falsifier rather than testing one. That transcribed falsifier is restated below so Cursor asserts against it verbatim, not a re-derived one:

**Completion falsifier (rescope ADR §4, verbatim target):** *"if by 2026-11-08 no successor risk-framework Pre-Q has been pre-registered (audit §5.2 / D1), the re-scope is judged incomplete … and D1 escalates to a mandatory blocker on any Aegis→M6J go-live decision."* The (c) scaffold's §6/§4 must reproduce this; a paraphrase that softens the 11-08 hard date or the go-live-blocker escalation is a defect.

---

## §5 — Forbidden moves (each genuinely tempting)

- **Filling in the D1 risk objective "to make the scaffold look complete."** The single cardinal forbidden move. Rescope ADR §5: numbers-before-question is the family's own pre-registration violation; the max-DD line / withdrawal model / time-under-water tolerance are the operator's frozen question, authored later. Cursor writes placeholders, never values.
- **Ratifying the HARV ADR** (setting status `Accepted`, or resolving §0.5-Q's gate-reachability decision). Both options go in §3; status stays `Proposed`.
- **Editing the CLAUDE.md MC-anchor blocks or Strategy Reference table.** `verify_lock_anchors.py` / `validate_params.py` parse those; the (a) fix is confined to §Firm Expansion prose. If the reframe tempts you toward the anchor blocks, stop — it doesn't need them.
- **Hardcoding a tier count you did not derive.** "9 of 10" was already wrong; do not replace it with another guessed integer. Derive it in Phase 0 or use the "most prop-firm tiers" framing.
- **Inventing HARV lane doctrine beyond the harvested sources.** Every load-bearing ADR claim traces to a Phase-0 read (Q-HARV-0 closure / DISC-CAMP-0 defect log / governance-chain ADRs). No new "best practice" from general knowledge.
- **The "while I was in there" refactor** of any `core/` file, or a second CLAUDE.md fix elsewhere. Log observations under `DONE_WITH_CONCERNS`; touch nothing outside the three named files.
- **Amending §6/§2 mid-build.** If a step is structurally wrong, return `BLOCKED — plan-itself-wrong`.
- **Re-deriving a §0 fact.** If a None-guard is absent on `main`, or a HARV ADR already exists, do not proceed on the inconsistent premise — return `NEEDS_CONTEXT`.

---

## §6 — Gate + status return taxonomy

Report EXACTLY one of: `DONE` | `DONE_WITH_CONCERNS` | `NEEDS_CONTEXT` | `BLOCKED — <context-problem | capability-problem | scope-problem | plan-itself-wrong>`.

A `DONE` here means all three artifacts are authored to spec and every per-step gate is green — it is **not** a ratification of (b) or a completion of (c); those are operator acts downstream. This handoff carries **no** RESOLVED / FALSIFIED / AMBIGUOUS verdict of its own — those belong to (b)'s eventual ratification and (c)'s eventual pre-registration, not to this docs build.

```
Status: <...>
Per-step gates: 2.1 [pass/concern], 2.2 [pass/concern], 2.3 [pass/concern]
Diffs (files touched): <list — expect exactly 3: CLAUDE.md + the two new files>
§0.5 resolutions applied: P=<new|amend>, Q=<both-options-in-§3, status Proposed>, R=<scaffold-only, filename>
Concerns surfaced (if any): <list>
Next action recommended: <one sentence — expect: parent review, then operator ratifies (b) + authors (c)'s risk objective>
```

---

## §7 — Parent-session review (after Cursor returns)

**Pass 1 — Spec-compliance.** Diff list contains ONLY `CLAUDE.md` + the two new files; no `core/` executable change; (b) status is `Proposed`; (c) status is `DRAFT` with §4/risk-objective as placeholders; no MC-anchor/table edit in CLAUDE.md.
**Pass 2 — Quality.** (a) preserves the pre-flight doctrine + cites PR #356 + derived count; (b)'s every load-bearing claim traces to a named source and §3 holds both gate-reachability options; (c)'s §5/§6 transcribe rescope §5/§4 verbatim (11-08 + go-live-blocker intact) and **no numeric risk target was invented**.
**Pass 3 — Consolidated read** (multi-step): the three artifacts are mutually consistent (the (a) reframe's doctrine framing matches `firm_rules.py:17`; (c)'s filename makes the rescope §10 hook fire; nothing in (b) pre-empts an operator ratification).

Only after all three passes does the parent recommend Joshua accept. **Then the reserved-for-operator work begins: ratify (b) `Proposed`→`Accepted` (after deciding §0.5-Q), and author (c)'s frozen question + risk objective before 2026-11-08.**

---

## §10 — Audit hooks (runnable)

```bash
# (a) skew fixed: no present-tense TypeError-for-every-firm claim survives; pre-flight doctrine kept
grep -n "TypeError for every" CLAUDE.md || echo "(a) present-tense claim gone — good"
grep -n "engine-support pre-flight" CLAUDE.md            # doctrine preserved (expect >=1)
grep -n "9 of the 10" CLAUDE.md || echo "(a) stale count gone — good"
python scripts/verify_lock_anchors.py                    # ROUTING: Closed  (anchor parsers unbroken)
python scripts/validate_params.py                        # 0 HARD

# (b) HARV lane ADR exists, is Proposed, holds both gate-reachability options
test -f docs/adr/2026-07-13-harv-discovery-lane-ratification.md && echo present
grep -n "^\*\*Status:\*\* \`Proposed\`" docs/adr/2026-07-13-harv-discovery-lane-ratification.md
python scripts/check_brief.py docs/adr/2026-07-13-harv-discovery-lane-ratification.md --type adr

# (c) D1 Pre-Q scaffold exists, DRAFT, makes the rescope §10 hook fire, invents no numbers
test -f docs/briefs/Q-SFRISK-1-successor-self-funded-risk-framework.md && echo present
ls docs/briefs/ docs/briefs/pre-registration/ 2>/dev/null | grep -i "self-funded\|successor"   # now a hit (was "NOT YET")
grep -nE "\b[0-9]+(\.[0-9]+)?%|\bmax-dd *= *[0-9]|withdrawal.*[0-9]" docs/briefs/Q-SFRISK-1-successor-self-funded-risk-framework.md \
  && echo "INVESTIGATE — a numeric risk target may have been invented" || echo "(c) no invented numbers — good"
grep -n "2026-11-08" docs/briefs/Q-SFRISK-1-successor-self-funded-risk-framework.md   # completion falsifier transcribed

# Scope wall: only the three intended files changed
git diff --name-only origin/main   # expect: CLAUDE.md + the two new files, nothing else
```

---

## Verification (parent-side, before declaring handoff complete)

```bash
# Mechanical discipline check on THIS handoff brief
python scripts/check_brief.py docs/briefs/handoffs/2026-07-13-cursor-handoff-post-batch-doc-artifacts.md --type cc_handoff

# §0 anchors resolve on main
git log -1 --format='%h %ci' -- docs/briefs/closures/Q-HARV-0-month-end-rebalance-ES.md
git ls-tree origin/main docs/adr/ | grep -i harv || echo "no HARV ADR pre-build (expected)"

# Cursor's closure report uses the four-state taxonomy
grep -E "^Status: (DONE|DONE_WITH_CONCERNS|NEEDS_CONTEXT|BLOCKED)" <cursor-return>
```

If Cursor returns `NEEDS_CONTEXT` or `BLOCKED`, this handoff is not complete; re-dispatch per §6.

---

## Related
- Parent triage (this session): repo-priority ranking — the 2026-11-08 collision (prop §4 falsifier + D1 successor Pre-Q) is the binding constraint; these three are the low-friction residue, not the critical-path work.
- Prior Cursor handoff (structure + §0.5 conventions): [`2026-07-13-cursor-handoff-stage-4-7-drivers.md`](../rnd-pipeline/2026-07-13-cursor-handoff-stage-4-7-drivers.md).
- (b) sources: [`Q-HARV-0 closure`](../closures/Q-HARV-0-month-end-rebalance-ES.md) · [`DISC-CAMP-0 closure`](../DISC-CAMP-0-closure-falsified.md).
- (c) parent: [`rescope ADR §4/§5/§7`](../../adr/2026-07-11-challenge-era-claims-rescope.md) · audit §5.2/D1.
