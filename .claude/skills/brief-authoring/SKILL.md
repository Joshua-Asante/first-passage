---
name: brief-authoring
description: Use this skill whenever Joshua needs to author, structure, or verify a written decision artifact — Pre-Q (Inquire-phase) briefs, ADRs, lock decision briefs, Claude Code handoff/spawn prompts, Notice-phase observation logs, methodology lesson captures, or audit notes. Triggers on phrases like "draft a brief", "write a Pre-Q", "write an ADR", "CC handoff", "spawn prompt", "lock decision", "audit note", "methodology lesson", "is this brief well-formed", or any request to structure a decision as a written artifact. Also fires when reviewing an existing brief for ceremonial-vs-load-bearing classification, or before authoring any artifact destined for `docs/adr/`, `docs/briefs/`. Addresses the pattern where each session re-derives brief structure (§0 Rule-0 reads, §4 falsifiable H, §5 forbidden moves, §6 gate, §10 audit-hooks). Hand off to inqhiori for methodology framing (when to inquire, what gates a question), pinescript-v6 for strategy code, prop-firm-challenge for live-ops decisions.
---

# Brief Authoring

This skill provides the canonical templates and discipline checks for written decision artifacts in Joshua's prop-trading workflow. It exists because brief structure was being re-derived session by session — the same §0/§4/§5/§6/§10 scaffolding emerging fresh each time, with the same failure modes recurring (ceremonial sections, missing falsifiers, briefs prescribing solutions instead of naming questions).

The 04-17 dd_protection retune → reversal → delete-and-retune cycle is the load-bearing anchor. That cycle should have been a single decision; it became three because the brief was authored from assumed semantics rather than verified production code. Rule 0 (read production first) was the lesson; a templated §0 enforces it at the artifact layer.

**Source-of-truth hierarchy:** `references/*.md` (canonical templates) → this SKILL.md body (discipline rules) → recent example briefs in `docs/briefs/` and `docs/adr/` (lineage). When a template here disagrees with a more recent example brief that worked well, the example wins and the template needs updating — flag this.

**Boundary with sibling skills:**
- `inqhiori` — methodology framing (when to inquire, what gates a question, pre-Q routing) and the home of The Algorithm operator (Question / Delete / Simplify / Accelerate). This skill executes the artifact step *after* inqhiori has decided one is needed; briefs authored here should pass The Algorithm before they ship, which this skill enforces at the verification block.
- `prop-firm-challenge` — live ops, allocation locks, dd_protection. This skill records those decisions (as ADRs); it does not make them.
- `pinescript-v6` — strategy code. Decision artifacts may reference Pine source; they do not modify it.
- `trade-csv-reconcile` — produces broker/TV CSV metrics referenced inside briefs; not consumed in reverse. (`live-execution-journal` retired 2026-07-11 with the CFD estate.)

---

## Rule 0 — Production reads BEFORE the brief, not as a Phase 1 check after

Any brief that touches risk controls, locked parameters, or production code must list the production files read **before** the brief was authored. Reading "during Phase 1 of the investigation" is too late — the brief is already framed by then, and re-framing after Rule 0 fires costs more than authoring after Rule 0 succeeded.

**Canonical sub-rules 1–7** live in [`docs/operational_rules.md` §8](../../../docs/operational_rules.md). The three teeth this skill already names are inlined below so a session that never opens §8 still has them. Open §8 for 1–7.

**Sub-rule 8 (paste-search before new work).** Before opening any new `lab/analysis/<theme>/<slug>/` or scoping new `core/`-adjacent work, paste the *literal command output* — not a conclusion — of searches against `lab/CATALOG.md` and `docs/briefs/INDEX.md` (and a cheap `git log --oneline -20` / `python scripts/check_advisor_dedup.py --keywords "..."`). Attestation without executed output is void. Work naming a candidate mechanism for a specific instrument additionally reads `ops/instruments/<SYM>.md` in full.

**Sub-rule 9 (Registry line on every new closure).** A non-grandfathered file under `docs/briefs/closures/` must carry `- **Registry:**` in the Iterate block: `rejected_candidates.md — ### <heading>` or `n/a — <reason>`. Token-only; heading-join quality is judgment.

**Amendment-first (sub-rule 10).** Before authoring a new file under `docs/adr/`, `docs/briefs/`, or `docs/notes/`, name the existing owner that should take an addendum, or paste search output showing none exists. Default is amend-in-place. New file only when no owner can hold the decision. This is a cross-cutting pre-condition, not a 7th numbered check.

**Anchor:** 2026-04-17 dd_protection cycle. Three iterations of brief authoring (retune → reversal → delete-and-retune) traced to assumed semantics being reconstructed mid-investigation. The §0 production-read section, when honestly populated, blocks this failure mode at the structural level.

**Sub-rule — §0 must list specific paths and a verification timestamp.** "Read `dd_protection.py`" is not Rule 0; "Read `dd_protection.py` (last `git log --oneline -1` confirmed `bf32aa3` on 2026-04-23)" is. Without the timestamp/anchor, §0 decays to ceremony within weeks.

**Sub-rule — when production isn't directly accessible (no GitHub MCP, no local read), §0 lives in the Claude Code handoff brief, not in the parent brief.** The handoff brief asks Claude Code to `cat` the file as Phase 0 and report contents BEFORE proposing changes. The parent brief then references that report. This is the canonical pattern when the authoring environment can't read the file directly.

---

## The six load-bearing discipline checks

These six are the authoring-side stack. They are **type-scoped** — see the applicability matrix below. `scripts/check_brief.py` automates the mechanical subset for types it models (inquire / full ADR / handoff). The others require human judgment. Amendment-first (sub-rule 10) is a cross-cutting pre-condition, not a 7th numbered check.

**1. §0 Rule 0 reads populated.** At least one production file with a verification anchor (commit hash, timestamp, line range, or `last-modified` date). Empty or "TBD" §0 fails. Light ADRs keep the *read* (tier-independent) but drop the §0 table — the Reads line is the form.

**2. Falsifiable hypothesis stated.** Inquire-phase briefs and full ADRs must contain a specific testable claim, phrased so a future check can determine whether it held. The form: "If [observation], then [conclusion]; otherwise [alternative]." Briefs that conclude "look further" without a binary outcome fail this check.

**3. Forbidden moves explicit and actually forbidden.** §5 must list moves the author genuinely considered or was tempted by — not theatrical lists of things never on the table. The check: would removing this section change behavior? If no, it's ceremony. If yes, it's load-bearing.

**4. Gate criteria binary.** §6 closure criteria must produce a clean RESOLVED / FALSIFIED / AMBIGUOUS verdict. "When we have more data" is not a gate; "when N≥30 trades accumulate AND PF deviation from baseline is within ±0.5σ" is.

**5. Question names a symptom, not a fix.** Pre-Q only. Rephrase the question to mention only what's wrong, not what to do about it. "Should we use K=2 or K=3 in the regime filter?" bakes in K-of-something. "What's the cost of the current pattern, and what alternative architectures exist?" doesn't. If the symptom-only rephrase is impossible, the question itself is the problem — return to inqhiori.

**6. Audit hooks runnable.** §10 must contain commands or checks executable later (grep strings, file paths, specific assertions), not vague "review at quarterly check-in." Audit hooks that nobody can mechanically run will not be checked.

### Type × check applicability

`M` = mechanical (`scripts/check_brief.py` or `scripts/check_closure_disposition.py`). `J` = judgment. `—` = not owed. Repo `check_brief.py` prints `NOT CHECKED` (not a pass) for light ADRs and for `{lock, notice, lesson, audit}`.

| Type | 1 §0 | 2 H | 3 forbidden | 4 gate | 5 Q-shape | 6 hooks | amend-first | 7–10 spawn | Iterate |
|---|---|---|---|---|---|---|---|---|---|
| Inquire / full ADR | M | M+J | J | M+J | J (inquire only) | M | J | — | — |
| Light ADR | Reads line (J; no §0 table) | — | Boundary or `none` (J) | Gate or `none` (J) | — | — | J | — | — |
| CC handoff | M | if executing a Pre-Q else `N/A` | J | status taxonomy M | — | M | J | M+J | — |
| Notice / lesson / audit | type-owned template; repo checker `NOT CHECKED` | — | — | — | — | — | J | — | — |
| Closure | — | — | — | discharged in Iterate | — | parent §10 paste | J | — | M tokens (`check_closure_disposition.py`) |
| Minimal spec | — | — | — | — | — | — | J | — | — |

`--type lock` remains an unmodeled alias so old verification blocks do not argparse-die. Do not author new lock-decision briefs; that type was deleted 2026-08-08.

---

## Additional checks for CC handoff briefs (patterns 7–10)

The six checks above apply to inquire / full ADR / handoff per the matrix. The four below apply when the brief is a Claude Code handoff (i.e., it spawns a fresh execution session). They were extracted from `obra/superpowers:subagent-driven-development` after evaluation against this skill's existing structure; the patterns they encode are spawn-specific failure modes that the six general checks did not catch.

**7. Clarifying questions surfaced before §2 execution.** The handoff template includes a §0.5 block where the spawn must list ambiguities and ask before running the plan. The check at brief authoring time: does §0.5 instruct the spawn to halt on ambiguity, or does it implicitly assume the §1/§2 statements are complete? Implicit-completeness handoffs fail this check — the spawn will guess rather than ask, and a guess that misreads the task wastes the entire session. Anchor: any CC session that ran the wrong analysis because the brief was ambiguous and the spawn defaulted instead of asking.

**8. Status return taxonomy.** §6 reporting format must use the four-state return: `DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT` / `BLOCKED`. The two-state success/failure shape (or the older COMPLETE/HALTED/FAILED) collapses two distinct epistemic states the spawn needs to surface:
- `DONE_WITH_CONCERNS` — the work completed but the spawn flagged correctness or scope doubts the parent should resolve before accepting. This state captures the case where every gate passed but the spawn noticed something off-pattern.
- `NEEDS_CONTEXT` vs `BLOCKED` — a missing input that can be supplied (`NEEDS_CONTEXT`, re-dispatch) is structurally different from an unresolvable obstruction (`BLOCKED`, escalate or decompose). Conflating them as "FAILED" loses the disposition.

`BLOCKED` further decomposes into four sub-cases: context-problem (re-dispatch with more context), capability-problem (re-dispatch with stronger model or human), scope-problem (decompose into smaller tasks), plan-itself-wrong (escalate to parent session). Without these sub-cases the spawn surfaces "I'm stuck" without disposition guidance.

**9. Spec-compliance audit separate from quality audit.** Parent-session review of returned work is two passes, not one:
- **Spec compliance:** did the spawn build EXACTLY what §1/§2 specified — nothing missing, nothing added? This is the scope-creep check. The spawn that quietly added a "while I was in there" refactor or a "just to be safe" extra check has failed spec compliance even if the work is good.
- **Quality:** is what the spawn built methodologically and structurally sound? This is the existing audit-hooks discipline.

The two passes catch different failure modes. Quality review with no spec-compliance pass cannot detect scope creep — the audit just evaluates what's there. Spec-compliance review with no quality pass cannot detect methodologically-sound-but-spec-wrong implementations. Both are required for any non-trivial CC handoff.

**10. Final consolidated read after multi-step work.** When a CC handoff executed >1 step (i.e., §2 had multiple Step 2.x blocks), the parent-session review includes a final read across ALL changes together, not just the per-step verifications. Per-step gates catch local correctness; they do not catch integration issues — two correct steps producing an inconsistent combined state. The DJ30 / Aegis / Guardian inter-strategy interactions are the canonical area where this matters: each strategy's lock decision is sound in isolation, the portfolio-MC view is what reveals inter-strategy interaction effects.

---

## Convergence notes

The six general checks plus patterns 7–10 are the union of two independently-derived disciplines:
- §0–§6 came from the 04-17 dd_protection cycle and the live-execution audit lessons.
- §7–§10 came from `obra/superpowers:subagent-driven-development`.

The two stacks overlap in spirit (both treat the brief as a structural artifact, both are skeptical of ceremony), but they catch different failure classes. The general checks catch authoring-side failures (ceremonial sections, solution-baked questions, vague gates). The CC additions catch spawn-side failures (ambiguity defaulting, conflated status returns, scope-creep in the diff, integration drift across steps). Both are load-bearing.

If a CC handoff brief passes its applicable 1–6 checks but fails 7–10, the spawn will produce work the parent can't trust even if the brief looks well-formed. If it passes 7–10 but fails its applicable 1–6 checks, the brief itself is malformed and the spawn is being asked the wrong thing. The two layers compose; they do not substitute.

---

## Brief type selection

| Triggering need | Use type | Lives in |
|---|---|---|
| Opening structured investigation | **Inquire-phase brief** (Pre-Q) | `docs/briefs/Q-X-name.md` |
| Locking a structural decision (architecture, doctrine, methodology rule) | **ADR** | `docs/adr/YYYY-MM-DD-slug.md` (the filename slug **is** the identifier — `ADR-NNN` numbering was dropped) |
| Spawning Claude Code for an execution task | **CC handoff brief** | Inline (passed to Claude Code) |
| Recording an observation that may graduate to inquiry | **Notice-phase observation log** | `docs/notes/notice/` |
| Adding a methodology/execution lesson to the registry | **Lesson capture** | Inline-edit the relevant `references/*lessons.md` |
| Documenting a methodology failure or unexpected outcome | **Audit note** | `docs/notes/audits/` |
| Closing any Q | **Closure record** | `docs/briefs/closures/` per `references/closure_record.md` |
| Commissioning steps that decide nothing (PROPOSED, $0/K=0) | **Minimal spec** | `docs/spec/` per `docs/spec/TEMPLATE-minimal-spec.md` (standing style, ratified JA 2026-08-07) |

**When the type is unclear:** if the artifact will gate a future investigation → Inquire brief. If it locks a decision → ADR. If it captures past learning → lesson capture or audit note. When in doubt, default to ADR — the structure forces falsifier and forbidden moves, which catch most ceremony.

**ADR ceremony is stakes-tiered** ([ADR 2026-08-08](../../../docs/adr/2026-08-08-adr-ceremony-tiering.md), ratified): full §0–§7 apparatus only when a limb fires (spends K/money · live-risk surface · LOCKED/frozen surface or non-regenerable deletion · creates/amends doctrine). Otherwise a **light decision record** — standard header field block + `**Tier:** light` + ≤300-word body in the minimal-spec style. Ambiguous tier → full; escalation = supersede, never pad. Rule 0 reads are tier-independent (the read always happens; only the §0 table is dropped). `scripts/check_brief.py` detects `**Tier:** light` and prints `NOT CHECKED` — that is the ratified shape, not a skip of the Reads line. Header fields still go through `scripts/check_adr_graph.py`.

**When NOT to author a brief:**
- Casual conversation / quick decisions with low reversibility cost — OODA loop, no artifact.
- Code authoring without a structural decision behind it — handoff to `pinescript-v6` or just write the code.
- Active investigation in progress — handoff to `inqhiori`; the brief is the *output*, not the workspace.

---

## Canonical templates

Each template lives in `references/`. The skill ships seven templates; copy and fill rather than re-deriving.

| Template | File | When to use |
|---|---|---|
| Inquire-phase brief (Pre-Q) | `references/inquire_brief.md` | Opening a structured investigation — Q-X format, gates closure |
| ADR | `references/adr.md` | Locking a structural/architectural decision |
| Claude Code handoff | `references/cc_handoff.md` | Spawn prompt for fresh Claude Code session with verification gates |
| Notice-phase observation log | `references/notice_log.md` | Lighter-weight pre-investigation observation capture |
| Lesson capture | `references/lesson_capture.md` | New entry for a lessons registry (execution_lessons.md, behavioral lessons, etc.) |
| Audit note | `references/audit_note.md` | Methodology audit / unexpected outcome analysis |
| Closure record | `references/closure_record.md` | Closing any Q — carries the mandatory typed `## Iterate` block (ADR `2026-08-04-iterate-closure-exit-mandatory`) |

**Closure discipline (2026-08-04; header fields ratified 2026-08-11).** Every closure filed under `docs/briefs/closures/` carries machine-readable header lines `**Closed:** YYYY-MM-DD` and `**Lane:** <F2 slug|UNASSIGNED>` (PREREG F3 grammar — aliases `Closed (explore record):` / `Date:` are non-compliant; forward-only, no retro-edits) and ends with a typed `## Iterate` block — Verdict used / Model update / **Next: INTEGRATE | ITERATE | STOP** / routing / entry packet / stop rule / **board write** — discharging the §6 Disposition column the brief pre-registered. A closure without it is incomplete, same weight as a missing §6 assertion. Three invariants: STOP is Iterate-with-budget-zero and records the re-proposal bar; ITERATE **names** a successor's entry packet but never opens one (operator GO is a fresh decision — parent-Q convention); the Board-write field records the STATE forward-board row or SESSIONS Open/next line the closure adds (or `none — STOP, nothing owed`) — this is the field that was measured missing 8/10 pre-mandate. Verdict asymmetry is preserved: RESOLVED-and-integrated closures may write "n/a — integrated" for the stop rule. Pre-commit gate 14 (`scripts/check_closure_disposition.py`) checks token presence only; content quality is audited at the quarterly methodology cadence.

Read the relevant template at brief-authoring time. Do NOT inline the template structure from memory — it drifts.

---

## Verification block (mandatory)

Every authored brief ends with a verification block that the author runs before declaring the brief complete. Format:

```
## Verification

# Modeled types (inquire / full ADR / handoff)
$ python scripts/check_brief.py <brief.md> --type inquire|adr|cc_handoff
# Expected: RESULT: well-formed  (applicable mechanical checks for this type)

# Light ADR / notice / lesson / audit (unmodeled here)
$ python scripts/check_brief.py <file.md> --type notice
# Expected: RESULT: NOT CHECKED — fill the type template; this is not a pass

# Closure
$ python scripts/check_closure_disposition.py <closure.md>
# Expected: exit 0 (Iterate tokens present)

# Production-source verification (Rule 0 confirmation)
$ <grep / cat / git log commands that confirm §0 / Reads anchors>

# Cross-reference verification (cited facts match canonical sources)
$ <grep commands that verify cited numbers / commit hashes / page IDs>
```

If a verification command fails, the brief is not complete. Re-author the section that broke; do not handwave.

---

## Known traps

Failure modes that recur, ranked by frequency:

**1. Ceremonial sections.** Applicable discipline checks formally present, content is "TBD" / "any improvement is acceptable" / "review later." Looks like discipline; isn't. The script catches mechanical instances (empty §0, no falsifier in §4); judgment catches the rest.

**2. Solution-baked questions.** "Should we add an X filter?" instead of "What's the cost of the current pattern?" Pre-Q gate (check #5) catches this if applied honestly. The signal: if rephrasing to symptom-only is hard, the question is the problem.

**3. Reconstructed §0 (post-hoc Rule 0).** §0 lists files claimed to be read but no commit/timestamp anchor. Verification: ask the author to paste the `git log -1 -- <file>` output. If they can't, the read didn't happen.

**4. Missing forbidden moves.** §5 is empty or lists strawman moves. The repair: ask "what was tempting but ruled out?" If nothing was tempting, the brief may not need authoring (no real choice point).

**5. Vague gate criteria.** "When we know more" / "after live data accumulates" — non-binary. Repair: name the specific N, the specific σ tolerance, the specific time window.

**6. Audit hooks no one can run.** §10 says "review quarterly" with no command. Repair: write the actual grep / file path / assertion. If you can't write it, the audit hook is theater.

**7. Stale Notion page IDs.** Cited Notion anchors (`32cdc0b53c...`) are reused across briefs without re-verifying. Repair: include a verification grep in §10 that confirms the cited page exists with the cited title.

**8. Briefs floating from doctrine.** New brief that doesn't reference standing doctrine (prop-firm-challenge Core Principles, lessons registries, prior ADRs). Repair: §1 Context must connect to existing doctrine where any exists. Orphan briefs accumulate as noise.

**9. Lessons captured without dollar anchor.** Methodology lesson entries that name a pattern but no measurable cost or counterfactual. These do not graduate to load-bearing. Repair: name the dated incident AND the dollar figure (or counterfactual). Below the threshold (E1/E2 standard: single-incident >$3K, OR three firings across separate windows), the lesson stays candidate-status.

**10. Brief authored but never re-read.** §10 audit hooks exist but no one returns to them. The discipline only earns its existence if the hooks fire on quarterly review. If multiple quarters pass without §10 ever being re-checked, the discipline is decaying — flag in the next methodology audit.

**11. Multi-question briefs.** A single brief trying to gate two or three questions at once. Each question needs its own Pre-Q. Repair: split. If the questions are tightly coupled, name the parent question and fork ungated sub-questions per Lesson #5 (parent-Q convention).

**12. Briefs that change the rules during investigation.** §6 gate criteria amended mid-investigation to match emerging evidence. This is `p`-hacking at the methodology layer. Repair: if gate criteria need to change, close the current brief AMBIGUOUS, capture why in the closure note, and open a fresh brief with the new criteria stated up front.

---

## Discipline check summary

```
[ ] Amendment-first: existing owner named or search output showing none (every new file)
[ ] Applicable checks for this type (matrix above) — do not run the inquire/ADR six on a notice
[ ] Verification block executed; the command that applies to this type passed (or printed NOT CHECKED)

If inquire / full ADR:
[ ] §0 Rule 0 reads populated with file paths + verification anchors
[ ] Falsifiable hypothesis stated in §4
[ ] Forbidden moves explicit and genuinely tempting (not strawmen)
[ ] Gate criteria binary (RESOLVED / FALSIFIED / AMBIGUOUS each have specific triggers)
[ ] Question names symptom not fix (inquire only)
[ ] Audit hooks runnable

If light ADR:
[ ] Reads line populated (the read happened; no §0 table)
[ ] Decision / Grounds / Gate / Boundary filled (Boundary and Gate may be `none`)
[ ] `check_brief.py` printed NOT CHECKED; `check_adr_graph.py` still applies to headers

If the artifact is a closure record, also:
[ ] Typed `## Iterate` block present (Next: INTEGRATE | ITERATE | STOP)
[ ] Entry packet populated iff ITERATE (frozen constraints + carry-forwards + forbidden re-opens + budget); successor named, not opened
[ ] Stop rule / re-proposal bar present for ITERATE and STOP ("n/a — integrated" legal for INTEGRATE)
[ ] Board write line present (verbatim pointer, or "none — STOP, nothing owed")
[ ] `Registry:` line present (`rejected_candidates.md — ### <heading>` or `n/a — <reason>`)

If brief is a CC handoff, also:
[ ] §0.5 instructs spawn to surface ambiguities BEFORE §2 execution
[ ] §6 reporting uses DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED taxonomy
[ ] BLOCKED sub-cases (context / capability / scope / plan-wrong) explicit in §6
[ ] Parent-session review section (§7) requires spec-compliance pass distinct from quality pass
[ ] If §2 has >1 step, §7 requires final consolidated read across all diffs
```

---

## Reference files

- `scripts/check_brief.py` — mechanical subset for modeled types. Run as:
  ```
  python scripts/check_brief.py <brief.md> [--type inquire|adr|cc_handoff|notice|lesson|audit|lock|closure]
  ```
  Modeled: inquire / adr / cc_handoff → well-formed or MALFORMED. Unmodeled notice / lesson / audit / lock / light ADR → `NOT CHECKED`. `--type closure` delegates to `scripts/check_closure_disposition.py` (prints the command; exit 0). `--type lock` is a back-compat alias, not a live authoring type.

- `references/inquire_brief.md` — Pre-Q template (§0–§10 structure)
- `references/adr.md` — ADR template
- `references/cc_handoff.md` — Claude Code spawn template
- `references/notice_log.md` — Notice-phase observation template
- `references/lesson_capture.md` — lesson registry entry template
- `references/audit_note.md` — methodology audit template
- `references/closure_record.md` — Q-closure template (mandatory `## Iterate` block)

Related skills:
- `inqhiori` — when to author (this skill is the how, given inqhiori has decided), and the Algorithm operator (Q/D/S/A); briefs authored here pass The Algorithm before shipping
- `prop-firm-challenge` — produces the live-ops decisions that lock decision briefs document
- `trade-csv-reconcile` — produce data referenced inside briefs (`live-execution-journal` retired 2026-07-11)
