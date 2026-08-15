# Iterate closure exit — every closure ends in a typed disposition — `2026-08-04-iterate-closure-exit-mandatory`

**D-S-A domain:** meta-process (framework edit — closure-artifact discipline; no data-corpus or system-artifact D/S/A rides this)
**Loop-of-Record:** STRATEGIC — a framework edit governing the OUTER loop's exit, ratified via operator adjudication (canon §14 channel (c)); no Delete verdict rides this, so no switch-gate applies.

**Status:** `Accepted` — ratified 2026-08-04 (operator GO); the mechanical gate (§2 item 6) is now self-armed HARD per §7 Phase 4
**Decision date:** 2026-08-04
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** `2026-08-12-closure-disposition-coverage-hard.md` — advisory-coverage clause only
**Retain-until:** none

---

## §0 — Rule 0 reads (production-source verification)

Read before authoring, in this session (2026-08-04), with `git log -1 --format='%h %cs' -- <path>` anchors:

- `docs/methodology/inqhiori-canon.md` — anchor `032cd64` 2026-07-10. Verified **at that pre-edit anchor**: zero matches for "Iterate"; the loop at line 26 ends `… O → R → I (loop)` with no definition of the terminal phase; §14/§15 establish the pattern for dated canon additions that point at an owning ADR. (This PR's own §16 addition changes that grep — a post-merge re-run finds the §16 matches; re-verify against `032cd64` via `git show`.)
- `docs/methodology/archive/notion/inqhiori-v1-investigation-framework.md` — anchor `ecd4e0c` 2026-06-13. Verified: the only Iterate definition in the corpus is v1 §8 (lines 122–137): "**Iterate** = specify which phase to return to and what new information triggered the loop-back" (:128) and "**Exit criteria (Iterate).** The next phase has a clear entry packet. No dangling state." (:132). Preserved "for definitional content" per canon §12 and the file's own header. **v1's exit is binary (Integrate / Iterate). No stop branch exists in any source** — corpus-wide grep for "entry packet" / "dangling state" returned only v1:132 **at the pre-edit state** (docs/, docs/ltm/ via `rg --no-ignore`; this PR's canon §16 and SESSIONS entry add new mentions by design).
- `docs/methodology/observation_routing.md` — anchor `7196893` 2026-06-24. Verified: three-bucket gate (Closed / Action / Forward) routes *observations*; carries an explicit anti-heaviness failure mode ("Replacing the Notice framework with a heavier framework").
- `.claude/skills/brief-authoring/references/inquire_brief.md` — anchor `c7c3345` 2026-07-06. Verified: §6 gate table already carries a free-text **Disposition** column; §9 closure-record format requires verdict + anchor-numbers-vs-gate + prediction-vs-actual + lesson candidates, and no forward-disposition field.
- `.claude/skills/brief-authoring/SKILL.md` (repo copy) — anchor `c134060` 2026-07-24. Verified: six discipline checks, traps 1–12; Trap #12 = gate criteria amended mid-investigation.
- `scripts/check_supersession_placement.py` — anchor `c271411` 2026-08-03 — and `scripts/githooks/pre-commit` — anchor `755d07f` 2026-08-03. Verified: gate 13 is the template for a deliberately-narrow, environment-independent, token-presence pre-commit gate (M-8 boundary stated in its docstring); the hook currently ends at gate 13.
- `docs/operational_rules.md` — anchor `2345095` 2026-08-03. Verified: Rule 7 owner table assigns carried-forward "open / next" to the top `docs/SESSIONS.md` entry; Rule 14 + gate 13 establish the prose-rule + narrow-mechanical-backstop split; rule-maintenance bar at :581 ("Rules earn their place by being paid for"). No existing rule mandates closure-completeness fields.
- `STATE.md` — anchor `dc7adcc` 2026-08-04. Verified: "Scheduled forward triggers" board is pointer-only ("date/criterion + owner link only, detail stays with the owner"; closed rows deleted, not struck; retention test "open or still owed, and no other home").
- `scripts/check_status_consistency.py` (docstring) — verified: its designed-and-**dropped** C1/C4 checks are the recorded post-mortem of semantic closure-completeness gating; "the reachable fix for this class is a WRITING convention … enforced at authoring time, not a gate."
- Closure corpus (18 files read across a 6-agent verification pass this session, verbatim-quoted): `Q-GEOFIT-1` (`## 8. Forward — what a successor brief must carry`), `Q-INVENTORY-1` (accept-idle + priced-NOT-funded forks), `Q-FUNNEL-1` (residual routed to the 08-08 D1 packet — an operator decision item, neither successor-Q nor HOLD), `Q-ICT-1` ("What survives (named, not opened — parent-Q convention)"), `Q-COSTGEO-2→3` and `Q-6JCOMPOSE-1→2` (successor chains: frozen handoff at the closure, successor opening still an operator act), plus a 10-file structure survey: `Q-RAIL-1`, `Q-BOOKFIT-1`, `Q-COMPOSE-1`, `Q-BUSTGATE-1`, `Q-C1PANEL-1`, `Q-CAPALLOC-2`, `Q-PYRPARITY-1`, `ST-EH-1`, `Q-HARV-0`, `H-FBEIA-1`.

**Measured baseline from those reads (the §1 numbers):** 10/10 surveyed closures carry an explicit forward disposition in some form — zero dangling closures in the sample. The disposition lives under **at least 7 different section names** ("Dispositions", "Disposition", "Operator disposition — DECLINE", "On GO (pre-registered consequences)", "What a fresh brief would need", "Preconditions bound to any re-open", a bare "Re-proposal:" bullet); the words Integrate / Iterate / Stop appear as field names in **0/10**. A board-write pointer (STATE row or SESSIONS Open/next line the closure adds) is explicit in **2/10**. Numbers-vs-§6 assertion: 8/10 (2 justified absences). Stop-rule / re-proposal bar: present on FALSIFIED/AMBIGUOUS/STOPPED closures, legitimately absent on RESOLVED ones (verdict asymmetry).

---

## §1 — Context

Every closure in the sampled corpus already does Iterate-shaped work — the practice exists; the *structure* does not. Three costs follow. (1) **Unfindability:** with 7+ header names and no typed field, neither a reader nor a gate can locate "what happens next" mechanically; the status-consistency gate's dropped C1/C4 checks are the recorded proof that post-hoc joining fails. (2) **The board-write limb is the one that actually drops:** 2/10 closures write their forward pointer to a board. The paid incident of exactly this class is dated 2026-08-04 — the **08-08 board gap** (SESSIONS `2026-08-04a`, audit R9): the 2026-08-08 quarterly programme-audit vehicle had never been scheduled while ~31 ADRs' obligations rode that date, plus four stranded gate falsifiers; closing it took a dedicated repair pass. Closures generate the same class of obligation as ADRs and carry even less board discipline. (3) **Entry-packet quality is verdict-lottery:** the strong form exists in roughly half the corpus, concentrated in named exemplars (Q-GEOFIT-1 §8, Q-COSTGEO-2 §4, Q-HARV-0 "What a fresh brief would need", Q-CAPALLOC-2 §4), and is re-derived per closure rather than templated.

The operator's 2026-08-04 direction: make the Iterate exit mandatory and structured on the closure artifact — without restoring full Investigate→Observe→Reflect ceremony. This ADR is the ratification vehicle for that direction, with three corrections the verification pass forced (see §2 Decision, items 3–5): the STOP branch is **new doctrine** (v1's exit is binary — the "or stop" limb has no textual basis in any source); ITERATE **names, never opens** a successor (parent-Q convention, operator GO still required); and ITERATE's routing targets include **forward-to-dated-packet / operator decision item** (Q-FUNNEL-1's actual residual route, which is neither successor-Q nor HOLD).

**Decision driver (one sentence):** the disposition work is already paid for on every closure but is untyped, unfindable under 7+ names, and its board-write limb — the limb whose ADR-layer failure cost the 08-08 board-gap repair — is missing 8 times out of 10.

---

## §2 — Decision

**Decision:** Every closure artifact filed under `docs/briefs/closures/` from this ADR's acceptance onward ends with a typed **`## Iterate`** block (template: `.claude/skills/brief-authoring/references/closure_record.md`), and every new Pre-Q brief's §6 gate table pre-registers its per-verdict disposition as one of **INTEGRATE | ITERATE | STOP**. Specifically:

1. **The Iterate block (mandatory, closure-resident).** Fields:
   - **Verdict used:** the verdict as filed (filename/status vocabulary stands — RESOLVED / FALSIFIED / AMBIGUOUS[-…] / VOID / MOOT / ABORT / operator-stopped / screen-fail / …; this ADR introduces **no** new verdict taxonomy).
   - **Model update:** 1–3 lines — what the prior framing got wrong or confirmed, beyond restating the §6 numbers.
   - **Next:** `INTEGRATE` | `ITERATE` | `STOP` (exactly one).
   - **Routing:** INTEGRATE → the commit (ADR / state-flip / doctrine edit / wiring) + its re-validation. ITERATE → return to **Q** (reframe) | **H** (§4 rewrite) | **Investigate** (tighter test) | **Identify** (new thread) | **dated packet / operator decision item**. STOP → why the thread dies here.
   - **Entry packet** (required iff Next = ITERATE): successor requirements — frozen constraints **and positive carry-forwards** (verified numbers, passing controls, H + prior verbatim), forbidden re-opens, K/$ budget. **Naming a successor does not open it** — parent-Q convention; operator GO is a fresh decision.
   - **Stop rule / re-proposal bar** (required for ITERATE and STOP; "n/a — integrated" is a legal value for INTEGRATE): what evidence reopens the thread, or when it dies for good. Preserves the measured verdict asymmetry — RESOLVED closures that fully integrate owe no re-proposal bar.
   - **Board write:** the STATE forward-board row or SESSIONS Open/next line this closure adds, verbatim — or `none — STOP, nothing owed`. This is the 2/10 field — the only obligation with a measured pre-ADR gap (the typed Next token and Model-update field are also new as *fields*, but formalize work the corpus already does).
   The Iterate block **replaces** the ad hoc Dispositions / Forward / Re-proposal sections of pre-ADR closures — the content is written once, in the block, not in both.
2. **§6 pre-registration.** New Pre-Q briefs type the existing §6 Disposition column: each verdict row pre-registers `INTEGRATE — <action>` / `ITERATE — <return target>` / `STOP — <re-proposal bar>`. Amending a disposition mid-investigation is Trap #12; its cross-brief form — re-opening a sibling Q with the same H and looser gates — is equally forbidden. **Bindingness at closure:** the closure discharges the pre-registered branch by default; electing a different branch at closure time is legitimate closure judgment, **not** a Trap-#12 amendment — the frozen row stands in the record, and the Iterate block must quote it and state why the other branch fired. For verdicts whose routing is unknowable at pre-registration (AMBIGUOUS especially), coarse pre-registration is blessed: fix the branch, choose the return target at closure.
3. **STOP is ratified as a third branch,** extending v1 §8's binary Integrate/Iterate exit. STOP = Iterate with budget zero: the loop exit that records why no re-entry is warranted and what bar a re-proposal must clear. This is new doctrine owned by this ADR, not a restatement of canon.
4. **Verdict → default-disposition map** (guidance, not law — the closure may argue a different branch): RESOLVED → INTEGRATE (+ ITERATE only for named residuals); FALSIFIED → STOP with re-proposal bar (ITERATE only when the failure forces a new question); AMBIGUOUS / VOID / ABORT → ITERATE (successor inherits the frozen record); MOOT / operator-stopped → STOP (naming what remains motivated, without opening it).
5. **Three-surface ownership split (Rule 7):** the closure Iterate block **owns** the per-Q forward disposition; a STATE forward-board row is the cross-session **pointer mirror** (one line + owner link, per STATE's own charter); the SESSIONS Open/next block is the **session-level carry**. The Board-write field records which pointer was written, keeping the three surfaces joined at authoring time — the only join the dropped-C4 post-mortem says is reachable. Rule 7's owner table is deliberately **not** extended while this ADR is `Proposed`; the ratification commit adds its one-line row ("Per-Q forward disposition → closure Iterate block; STATE row = labeled pointer mirror") with a dated edit-log entry (§7 Phase 4).
6. **Enforcement:** authoring-time discipline (brief-authoring skill + closure template) plus pre-commit **gate 14** (`scripts/check_closure_disposition.py`) — token-presence only (Iterate heading, `Next:` branch token, `Board write:` token), scoped to `docs/briefs/closures/*.md`, the 34 pre-existing files grandfathered by name. The gate runs WARN-only while this ADR is `Proposed` and hard-fails once `Accepted` (self-arming; no second wiring step).

**Effective:** 2026-08-04, immediately upon acceptance. Forward-only — no retroactive editing of existing closures.
**Scope:** closure artifacts under `docs/briefs/closures/` and §6 of newly authored Pre-Q briefs. Lab `RESULTS*.md` and adjudication notes are **out of scope** (deliberate — see §5).

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Restore Observe/Reflect as standing phases or per-Q documents | The three-bucket gate replaced exactly this class of ceremony and carries an explicit anti-heaviness failure mode (`observation_routing.md`); the Notice-phase compression already paid the audit that killed forward-loaded phase artifacts. Observe is already mandated by §9's numbers-vs-§6 requirement (8/10 compliance); Reflect+Iterate collapse into two closure fields. |
| New numbered operational rule (Rule 15) mandating closure completeness | The rule-maintenance bar (`operational_rules.md` :581) requires a rule to be paid for by a specific failure. The paid incident (08-08 board gap) is ADR-layer, and 10/10 closures already carry dispositions — the closure-layer failure is heterogeneity + a missing board pointer, which the template + gate address without a new rule. If the gate fires on real closure omissions post-acceptance, that record funds a Rule 15 then. |
| Semantic completeness gate (does the entry packet actually bind? is the disposition consistent with §6?) | The status-consistency gate's designed-and-dropped C1/C4 checks are the recorded graveyard of this idea: closure completeness has no mechanical join anchor. Token presence is the mechanizable subset (M-8); content quality stays authoring-side judgment. |
| Enforce via gate 12 (`roll_sessions.py`) on the SESSIONS Open/next block | Wrong layer — that convention is per-session and already universally followed; the obligation being created is per-closure-artifact. |
| Enforce via a STATE.md join (every closure must have a board row) | No join anchor exists between a closure file and a board row (dropped-C4 post-mortem). The reachable version is the Board-write field written at authoring time. |
| Status quo (keep ad hoc dispositions) | The disposition stays unfindable under 7+ names, unauditable mechanically, and the board-write limb stays at 2/10 — the exact limb whose ADR-layer failure just cost a repair pass. |

---

## §4 — Falsifier (revert trigger)

**H:** typing the disposition and mandating the board-write pointer converts existing ad hoc practice into an auditable exit at near-zero marginal authoring cost; the block stays load-bearing, not ceremonial.

**H is falsified — and this decision reverts — if any limb below fires** (checked at the first methodology audit ≥3 months after acceptance, then quarterly):
- **Ceremony limb:** ≥3 post-acceptance closures whose Iterate block is vacuous — Model update merely restates the verdict, or an ITERATE closure's entry packet restates §6 with no successor-binding constraint. (Fires → the block is demoted to optional by a superseding ADR; the §6 typed column may survive on its own evidence.)
- **Friction limb:** ≥2 legitimate closure commits resolve the gate by `--no-verify` or by gutting the block to satisfy tokens. (Fires → supersede **in part**: keep the authoring discipline, drop or re-shape gate 14.)
- **Drift limb:** ≥2 post-acceptance successor Qs open without the packet their predecessor's Iterate block promised (the exact drift the mandate exists to kill persisting despite it). (Fires → the closure-resident placement is wrong; re-design at the pre-registration layer instead.)

**Revert action:** author a superseding ADR per the limb notes; never edit this decision text in place.
**Trigger check schedule:** ride the standing quarterly methodology-audit cadence (programme-audit vehicle); first eligible check = first audit ≥3 months post-acceptance.

---

## §5 — Forbidden moves (under this ADR)

- **Retro-editing the 34 grandfathered closures to add Iterate blocks** — tempting for corpus consistency; forbidden. Closed artifacts are read in reading order and their dispositions are already consumed; retrofitting rewrites record (Rule 14 / Trap #12 territory) for zero forward value. The grandfather list in gate 14 is the permanent record of the boundary.
- **Extending gate 14's scope now to `lab/analysis/*/RESULTS*.md` or adjudication notes** — tempting for coverage; deferred until the first post-acceptance audit shows the block earns its keep on `docs/briefs/closures/`. Scope extension is an ADR edit (supersede in part), not a flag — same posture as gate 13's scope clause.
- **Treating `Next: ITERATE` as authorization to open the successor** — forbidden. ITERATE freezes the packet; opening is an operator GO (parent-Q convention: "named, not opened"). Both verified successor chains (Q-COSTGEO-2→3, Q-6JCOMPOSE-1→2) show the terminal closure deliberately naming **no** successor and routing to a separate operator decision — that remains legal and correct.
- **Adding semantic checks to gate 14** ("is the entry packet sufficient?") — forbidden per the dropped-C1/C4 post-mortem; vacuous assurance. Content quality is owned by the skill's authoring checklist and the audit cadence.
- **Inventing a closure-verdict taxonomy** (normalizing the observed verdict vocabulary to the six tokens in the Verdict-used field's example list) — forbidden; verdict-as-filed stands. The typed surface is the *disposition*, not the verdict.
- **Amending a §6 disposition (or the Iterate block of a signed closure) mid-flight** — Trap #12 and its cross-brief form (sibling Q, same H, looser gates). If the disposition is wrong, the successor artifact says so; the frozen record stands.

---

## §6 — Consequences

**Positive:**
- The loop exit becomes findable and auditable: one heading, one typed branch token, one board pointer — greppable across the corpus.
- The board-write limb (2/10 today) becomes a structural field, closing the closure-layer instance of the class that produced the 08-08 board gap at the ADR layer.
- Entry-packet strength stops being verdict-lottery: the template carries the Q-GEOFIT-1-§8 / Q-COSTGEO-2 / Q-HARV-0 pattern so every ITERATE closure inherits it.
- Compressed Pre-Qs get the v1 Iterate exit semantics without any restored phase ceremony — two fields on an artifact that already exists.

**Negative (real cost):**
- Every closure grows ~8 lines, including ops closures where the disposition is trivial ("INTEGRATE — state-flip landed; none — nothing owed").
- An 8th tracked template surface (closure_record.md) that can drift from practice and needs the same example-wins maintenance as the other seven.
- Gate 14 adds one more pre-commit scan (bounded: one glob + token greps over a small directory).

**Risks:**
- The block decays into ceremony (the exact §4 ceremony limb) — mitigated by making only tokens mechanical and auditing content quarterly.
- The grandfather list ossifies: a legacy closure that gets a *material* addendum could dodge the discipline — accepted; Rule 14 owns addenda placement, and the addendum's own board obligations route through the session's SESSIONS entry.

**Downstream artifacts updated by this ADR (same PR):**
- `docs/methodology/inqhiori-canon.md` — new §16 (canon-side statement; this ADR wins on disagreement).
- `.claude/skills/brief-authoring/references/closure_record.md` — new template (8th).
- `.claude/skills/brief-authoring/references/inquire_brief.md` — §6 typed Disposition column; §9 references the closure template + Iterate block.
- `.claude/skills/brief-authoring/SKILL.md` (repo copy) — templates table row, closure-discipline paragraph, checklist line.
- `.claude/skills/inqhiori/SKILL.md` (repo copy) — one pointer line to canon §16.
- `scripts/check_closure_disposition.py` (new) + `scripts/githooks/pre-commit` gate 14 + `tests/scripts/test_check_closure_disposition.py`.
- `docs/adr/INDEX.md` — regenerated.
- `docs/SESSIONS.md` — session entry; ratification owed rides its Open/next.

---

## §7 — Implementation plan

Same-PR mechanical edits (all listed in §6 downstream); no CC spawn needed.

- **Phase 0** — §0 anchors re-verified at implementation time (this session; anchors above).
- **Phase 1** — author canon §16, closure template, template/skill edits.
- **Phase 2** — land `check_closure_disposition.py` (WARN while `Proposed`) + gate 14 hook line + tests with a deliberate failing-case fixture (discipline guards need adversarial tests).
- **Phase 3** — regenerate ADR INDEX; verification block below executes; SESSIONS entry lands with the closing commit.
- **Phase 4 (operator)** — ratification: flip Status to `Accepted` (header edit per Rule 8 stamping convention) and, in the same commit, add the Rule 7 owner-table row per §2 item 5 (with dated edit-log entry) and update canon §16's status word if stated there. The gate self-arms; no further wiring.

---

## §10 — Audit hooks (runnable)

```bash
# The canon §16 exists and points here
grep -n "iterate-closure-exit-mandatory" docs/methodology/inqhiori-canon.md

# The closure template exists and carries the typed branch line
grep -n "INTEGRATE | ITERATE | STOP" .claude/skills/brief-authoring/references/closure_record.md

# Gate 14 wired and self-arming severity implemented
grep -n "check_closure_disposition" scripts/githooks/pre-commit
grep -n "Proposed" scripts/check_closure_disposition.py

# Checker self-run (WARN-tier while this ADR is Proposed; exit 0)
python scripts/check_closure_disposition.py

# Ceremony-limb audit input: the post-ADR (non-grandfathered) closure set
python -c "import scripts.check_closure_disposition as c; print('\n'.join(p.name for p in c.in_scope()) or '(none yet)')"

# Board-write coverage trend. Baseline 2/10 pre-ADR was measured on FREE-FORM
# pointers — the literal token below has 0 pre-ADR matches by design; expect
# every non-grandfathered file listed above, and nothing else.
grep -rln "Board write" docs/briefs/closures/ || true
```

---

## Verification

```bash
# Discipline checks (mechanical; repo-side subset)
python scripts/check_brief.py docs/adr/2026-08-04-iterate-closure-exit-mandatory.md --type adr
# Expected: RESULT: well-formed

# ADR lifecycle graph — header fields, INDEX sync
python scripts/check_adr_graph.py
# Expected: exit 0

# New checker passes on the current corpus (all 34 grandfathered; WARN tier)
python scripts/check_closure_disposition.py
# Expected: exit 0

# Checker's adversarial tests (failing fixture included)
python -m pytest tests/scripts/test_check_closure_disposition.py -q
# Expected: all pass
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-04 | Initial authoring (Proposed); verification pass: 6-agent fan-out over canon, v1 archive, 18 closures, boards, enforcement surfaces | Joshua + CC |
| 2026-08-04 | Adversarial pre-ratification review (4-skeptic fan-out, 0 BLOCKERs); fixes applied — checker fence-blindness + prose-Next false-passes, §6-disposition bindingness clarified, Loop-of-Record header added, §0 pre-edit qualifiers | Joshua + CC |
| 2026-08-04 | **Ratified — Status → `Accepted`.** Gate 14 self-armed HARD; Rule 7 owner-table row + canon §16 status wording updated same commit (§7 Phase 4) | Joshua |
| 2026-08-07 | **§4 friction-limb datum #1 logged at observation** (Rule-11 standard — the input must accrue): gate 14 exits 1 at HEAD on `docs/briefs/closures/Q-CAPA-1-closure-resolved.md` — the closure merged 2026-08-06 past the self-armed HARD gate via a hookless surface, carrying `Routing: Board writes` prose but no literal `Board write:` token. Token line added to the closure same day (substance unchanged). Count toward the §4 friction limb: **1** | CC (blast-radius sweep) |
| 2026-08-12 | **Superseded in part** by `2026-08-12-closure-disposition-coverage-hard.md` — advisory-coverage clause only (coverage limb severity now owned by that ADR; Iterate limb unchanged) | Operator GO via task |
