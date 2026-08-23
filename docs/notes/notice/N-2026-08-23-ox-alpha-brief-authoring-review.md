# Notice — Ox-alpha review of brief-authoring: 8 objections survive reconciliation; 2 claimed BLOCKERs do not

**Notice ID:** N-2026-08-23-ox-alpha-brief-authoring-review
**Observed:** 2026-08-23
**Author:** Cursor Cloud Agent (commission: send a sanitized copy of the brief-authoring skill to ox-alpha via `$OPEN_ROUTER_API` and reconcile objections against the real skill before treating any as findings)
**Source:** `stealth/ox-alpha` chat-completions call (OpenRouter, no tools, no repo access) against a genericized rewrite of `.claude/skills/brief-authoring/SKILL.md`, then a Rule-0 read of the real skill + templates + repo-side checker
**Status:** `HELD` — surviving findings are logged; skill edits are doctrine (ceremony limb 4) and need operator GO
**Lives in:** `docs/notes/notice/N-2026-08-23-ox-alpha-brief-authoring-review.md`

**D-S-A domain:** meta-process (adversarial review of an authoring skill). No production-control change.

---

## §0 — Source anchors

Files read at production fidelity **before** this notice was authored:

- `.claude/skills/brief-authoring/SKILL.md` — `d88e5f22be12ef9b009dcba2bdb07de9f421747c` (2026-08-15; `git log -1` this session)
- `.claude/skills/brief-authoring/references/cc_handoff.md` — `027de84263ac04da947c3caac7e0fc3f9f75eb96` (2026-08-15)
- `.claude/skills/brief-authoring/references/adr.md` — light-tier 5-line contract read this session
- `.claude/skills/brief-authoring/references/closure_record.md` — Iterate field glossary read this session
- `.claude/skills/brief-authoring/references/notice_log.md` / `inquire_brief.md` / `lesson_capture.md` / `audit_note.md` — type-contract spot-checks
- `scripts/check_brief.py` — `fb9fdaa80c73ee797a591960bd5c1c5656ffcfbf` (2026-08-21)
- `scripts/check_closure_disposition.py` — `1d093ce2a038992b50eff7bf9aca7d7e617c496b` (2026-08-21)
- `docs/adr/2026-08-22-ox-alpha-adversarial-lens-scope.md` — `b2e5f15d2b11a72759d3734eba89806c2375c38b` (2026-08-22)
- `docs/lessons/2026-05-27-brief-authoring-traps-13-14-15.md` — CANDIDATE traps still outside the skill
- `docs/templates/lock_decision.md` — present, CFD-era, **not** in the skill `references/` folder
- `docs/spec/TEMPLATE-minimal-spec.md` — lives outside the skill bundle by design
- Workspace skill bundle has **no** `scripts/check_brief.py` (skill-side checker path named by SKILL.md is absent here)

**Call (sanitized only):**

- Model: `stealth/ox-alpha` via `https://openrouter.ai/api/v1/chat/completions`, `$OPEN_ROUTER_API`, no `HTTP-Referer` / `X-Title` (would have named the repo)
- Outgoing payload sha256: `5122b496a9fce5247eec7ebe2f1903a917a3823a37c4727ce0104192b16bd942` (21,921 bytes, 4,824 prompt tokens)
- Response: HTTP 200, 16,308 completion tokens, `$0`, 26 numbered objections (O1–O26)
- Fingerprint sweep on outgoing text: no operator name, no INQHIORI, no `dd_protection`, no strategy/firm names, no dates, no dollar figures, no repo slug

---

## §1 — The observation

A sanitized rewrite of the brief-authoring skill (structure preserved; names, dates, paths, and incident anchors stripped) was sent to ox-alpha with the question “how should we improve this for a one-operator, multi-session decision-artifact program.” It returned 26 numbered objections, two labeled BLOCKER (O1 applicability contradiction; O20 spec-compliance has no object). Reconciling each against the real skill, its seven `references/` templates, `scripts/check_brief.py`, and `scripts/check_closure_disposition.py` — not against the sanitized excerpt — drops both BLOCKERs and leaves eight objections that survive as findings.

---

## §2 — Why it stands out

- **Baseline:** the ox-alpha ADR (`2026-08-22-ox-alpha-adversarial-lens-scope.md` §2/§5) requires every objection be reconciled against the real artifact before it is logged as a finding. The validation addendum already showed mixed-quality “find everything” output (one real hit, one false positive, one sanitization artifact) indistinguishable without ground truth.
- **Delta:** same pattern on a methodology skill. Two claimed BLOCKERs are sanitization artifacts or already-discharged by templates/checker the sanitized body did not carry. Several HIGH/MEDIUM items are real skill-body vs checker/template skew.
- **Frequency:** third named ox-alpha use (validation addendum; DL-2 prereg; this review). Surviving findings mean the §4(b) “three consecutive zero-yield uses” revert trigger does **not** fire.

---

## §3 — Reconciliation (every objection)

Disposition vocabulary: **SURVIVES** = treat as a finding against the real skill; **PARTIAL** = residue after a real template/checker already covers the claim; **DISCHARGED** = sanitization artifact or already implemented; **DECLINED** = claim is false or the skill’s stated tradeoff holds.

| ID | Ox-alpha claim | Disposition | Ground |
|---|---|---|---|
| O1 | Six checks are simultaneously universal, subject-scoped, and tier-exempt | **SURVIVES** (HIGH, not BLOCKER) | SKILL.md still says “Every brief, regardless of type, must pass these.” The repo checker already refuses that contract for light ADRs and for `{lock, notice, lesson, audit}` (`_UNMODELED_CONTRACT_TYPES`, `_LIGHT_TIER_RE`, added 2026-08-09 after false-MALFORMED fires). The defect is **skill-body / checker skew**, not a missing matrix in the checker. |
| O2 | “Six” vs unnumbered amendment-first vs nine checklist boxes vs “all 6 PASS” | **SURVIVES** (MEDIUM) | Literal in SKILL.md. Checker and closure extras are a different N. |
| O3 | Light tier unspecified; no `--tier` | **PARTIAL** | `references/adr.md` specifies the 5-line light body; `check_brief.py` auto-detects `**Tier:** light` and returns `NOT CHECKED` (no `--tier` flag because detection is header-driven). Residue: light has **zero** mechanical content checks. |
| O4 | Type table ↔ templates ↔ CLI bijection broken | **PARTIAL** | Lock template was **deleted from the skill** on purpose (2026-08-08 conventions audit); `docs/templates/lock_decision.md` is a stale CFD-era leftover. Minimal spec lives at `docs/spec/TEMPLATE-minimal-spec.md` by standing style. **Surviving residue:** closure has a template and a denser checklist than any type-table row, and `--type` has no `closure`. |
| O5 | Teeth live in operational_rules and are optional | **PARTIAL** | Amendment-first is already inlined in SKILL.md. Sub-rules 8/9 still require opening `docs/operational_rules.md` §8 — the skill already says so. Not new. |
| O6 | No lifecycle header standard | **DISCHARGED** | Per-type headers exist; `check_adr_graph.py` owns ADR status vocabulary. No `author-session-id` — NIT only. |
| O7 | Trap 12 has repair advice, no detection | **SURVIVES** (HIGH) | No gate-section hash. Closure template forbids editing a frozen brief; nothing flags a quiet §6 rewrite. |
| O8 | Closure furniture undefined | **DISCHARGED** | `closure_record.md` + inquire-brief Disposition column define producer/consumer. Skill already says read the template. |
| O9 | No append-only / concurrent-edit protocol | **SURVIVES** (MEDIUM) | ADR Change-history is convention, not a lock. Concurrent worktrees are the normal mode. |
| O10 | “Read BEFORE framing” is unenforceable | **SURVIVES** (HIGH) | §0 anchors prove a read happened, not that it preceded framing. Inquire/ADR templates do not require a production quote inside §3/§4. (The *deleted* lock template’s paste-literal blocks were closer to the proposed fix.) |
| O11 | No lesson → skill amendment path | **SURVIVES** (MEDIUM) | Traps #13/#14/#15 remain CANDIDATE in `docs/lessons/2026-05-27-brief-authoring-traps-13-14-15.md` and are still not in SKILL.md. |
| O12 | One-incident overfit; frequency ranking uninstrumented | **PARTIAL** | More incidents exist than the sanitized copy showed. “Ranked by observed frequency” is still not regenerated from checker tallies. |
| O13 | “Default to ADR” corrupts typology | **DECLINED** | Light tier + `docs/adr/INDEX.md` are the mitigation. Forcing a falsifier on type-uncertainty is a stated tradeoff, not an accident. |
| O14 | Doctrine-amend limb vs inline lesson capture undrawn | **SURVIVES** (MEDIUM) | Lesson template has Candidate vs Standing; SKILL.md never ties that to ceremony limb 4. |
| O15 | Judgment checks have no owner or second-session cadence | **SURVIVES** (HIGH) | `fable-judge`, the pre-ratification panel, and this ox-alpha lane exist and are **not referenced** from brief-authoring as the judgment performer. |
| O16 | Anti-strawman test is unfalsifiable | **PARTIAL** | ADR/handoff templates already require a rejection reason. Temptation-trigger + revival-condition are not required. The “would removing this change behavior?” line stays ceremonial. |
| O17 | Verification block accepts commands with no transcript | **SURVIVES** (MEDIUM) | Closure §10 says paste outputs; the skill-wide verification shape does not. |
| O18 | Audit hooks runnable but unscheduled | **SURVIVES** (MEDIUM) | Quarterly cadence is named for Iterate *content*; individual §10 greps have no due date. |
| O19 | “Example wins” contradicts anti-drift | **DECLINED** | The next clause is “and the template needs updating — flag this.” Residue is O11 (no amendment procedure), not a contradiction. |
| O20 | Spec-compliance has no object (claimed BLOCKER) | **DISCHARGED** | `cc_handoff.md` already has a deliverables list, an explicit NOT-to-do, a return `Diffs (files touched):` line, and Pass 1 item “Diff list contains ONLY files §2 named.” Residue: the skill *body* does not name that contract; the checker does not diff it. |
| O21 | Ambiguity answers not written back; no re-dispatch cap | **SURVIVES** (MEDIUM) | Template says re-dispatch the same plan; answers may live only in chat. |
| O22 | `DONE_WITH_CONCERNS` has no per-concern disposition | **SURVIVES** (MEDIUM) | Parent action is “review; accept or re-dispatch.” No required accept-with-rationale / fix / escalate record. |
| O23 | Partial progress undefined | **PARTIAL** | Return format has per-step `pass/concern/skip`. No resume packet. |
| O24 | MECHANICAL/JUDGMENT never tagged per check | **SURVIVES** (HIGH) | Checker docstring distinguishes the split; success output is `well-formed`, not “N judgment checks remain.” Light/unmodeled paths honestly print `NOT CHECKED`. |
| O25 | Closure gate is token-only; compensating audit unnamed | **PARTIAL** | Token-only is confessed in SKILL.md and in `check_closure_disposition.py` (M-8). Quarterly methodology cadence **is** named. “No interval” is false. |
| O26 | Repair-guidance quality unverifiable | **DISCHARGED** | Repo checker prints per-violation section + reason. Skill-side checker is absent from this workspace bundle (separate residue, not ox-alpha’s claim). |

---

## §4 — Routing decision

**Decision:** HOLD until operator GO
**Reason:** surviving items are real methodology findings; editing the skill (or promoting any of them into checks) is ceremony-limb-4 doctrine and is out of scope for this send-and-reconcile turn.

---

## §5 — If HOLD: re-check trigger

- **Re-check date:** next operator pass on this notice, or the next quarterly methodology audit, whichever first
- **Trigger condition:** operator GO to amend `brief-authoring` (or to open a Pre-Q that picks a subset). Highest-leverage surviving cluster, ranked post-reconciliation:
  1. **O1** — write the type × check matrix the checker already implements into SKILL.md (stop claiming “every brief, six checks”)
  2. **O10** — require a production quote (`path:line`) inside the question/hypothesis, so Rule 0 ordering is structural
  3. **O15 + O24** — tag each check `[MECHANICAL]` / `[JUDGMENT]`; name `fable-judge` / the panel / ox-alpha as the judgment performer; make a green checker print judgment-outstanding
  4. **O7** — detect Trap-12 gate rewrites (hash or equivalent), not just advise
  5. **O4 residue + O2** — add closure to the type table; fix the “six” count drift
  6. **O21 / O22 / O9 / O11 / O14 / O17 / O18** — spawn answer-addenda + concern dispositions; amendment protocol; lesson→skill path; verification transcripts; hook triggers
- **Drop trigger:** operator NO-GO, or a skill amendment ADR that accepts/declines each surviving row so this notice is not the owner
- **Calendar entry:** none minted — board write is the SESSIONS Open/next line

**Not in scope this turn:** no SKILL.md edit, no new checker, no template rewrite.

---

## §10 — Audit hooks

```bash
# Outgoing payload was sanitized (fingerprint tokens must stay absent)
grep -E 'Joshua|INQHIORI|dd_protection|first-passage|Tradeify|Guardian|Striker' \
  /opt/cursor/artifacts/ox_alpha_brief_authoring_outgoing_sanitized.md
# Expected: empty

# Payload identity
sha256sum /opt/cursor/artifacts/ox_alpha_brief_authoring_outgoing_sanitized.md
# Expected: 5122b496a9fce5247eec7ebe2f1903a917a3823a37c4727ce0104192b16bd942

# This notice exists and names the disposition vocabulary
grep -c 'SURVIVES\|DISCHARGED\|DECLINED\|PARTIAL' \
  docs/notes/notice/N-2026-08-23-ox-alpha-brief-authoring-review.md
# Expected: table + this grep both populated

# Skill body still carries the O1 universal claim (until a GO amends it)
grep -n 'Every brief, regardless of type' .claude/skills/brief-authoring/SKILL.md
# Expected: one hit (the skew this notice records)

# Checker already declines the universal contract
grep -n '_UNMODELED_CONTRACT_TYPES\|_LIGHT_TIER_RE' scripts/check_brief.py
# Expected: both present
```

---

## Verification

```bash
python scripts/check_brief.py docs/notes/notice/N-2026-08-23-ox-alpha-brief-authoring-review.md --type notice
# Expected: RESULT: NOT CHECKED — notice contract not modeled in the repo-side subset
# (this is the O1/O4 residue: skill says run the checker; repo checker refuses the type)

git log -1 --format='%H %ad' --date=short -- .claude/skills/brief-authoring/SKILL.md
# Expected: d88e5f22be12ef9b009dcba2bdb07de9f421747c 2026-08-15
```
