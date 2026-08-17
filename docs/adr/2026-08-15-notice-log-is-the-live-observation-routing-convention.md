# Notice-log governs narrative observations; the three-bucket gate survives only as one mechanical gate's routing codes — `notice-log-is-live-observation-routing-convention`

**Status:** `Accepted`
**Decision date:** 2026-08-15
**Supersedes:** none — `observation_routing.md` is not an ADR (no six-field header, not in the ADR graph); this decision corrects its status claim by cross-reference, not by a graph-checked supersession edge.
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Tier:** full — limb 4 fires (amends doctrine: `observation_routing.md`'s standing claim that it replaced the prior Notice/Inquire framework, cited as active/current by at least six other methodology docs and ADRs).

---

## §0 — Rule 0 reads (production-source verification)

- `docs/methodology/observation_routing.md` — anchor `7196893` (2026-06-24, last touch — link-rot fix only; created `d1774a6` 2026-04-25, never substantively re-touched since). Read in full.
- `docs/methodology/inqhiori-canon.md` §8/§10/§16 (L219, L247, L350) — read in full this session. Confirmed: cites the three-bucket gate as current/composing at §10/§16; the only mention of the Notice/Inquire replacement itself is framed as a closed 2026-04-25 retrospective at §8, not a live claim about §10/§16's own currency.
- `.claude/skills/brief-authoring/SKILL.md` (L96, L121, L224) and `references/notice_log.md` (full) — read this session. Names `docs/notes/notice/` as the live target for "Notice-phase observation log," no mention of `observation_routing.md` or Closed/Action/Forward anywhere in either file.
- All 20 files under `docs/notes/notice/` — enumerated and read this session (headers + §4/§6 decision fields) via a 4-agent evidence sweep, cross-verified against `git log --oneline --diff-filter=A -- docs/notes/notice/` (18 creation commits, 20 files, zero before 2026-04-25, continuous through 2026-08-15).
- `docs/methodology/strategy_harvest.md:79` — cites `N-2026-07-26-forced-flow-census.md` as the live artifact format for a 2026-07-26 finding, three months after `observation_routing.md`'s claimed replacement date.
- `docs/methodology/regime_robustness_gate.md:199`, `docs/methodology/strategy_lifecycle.md:25,104`, `docs/adr/2026-07-10-strategies-never-locked-lifecycle-governance.md:23`, `docs/adr/2026-08-04-iterate-closure-exit-mandatory.md:21` — each cites `observation_routing.md`'s Closed/Action/Forward doctrine as settled/current; none flags the Notice-log convention as conflicting or superseded.
- `scripts/verify_lock_anchors.py` (anchor `0356be2`, 2026-08-11) + `.claude/commands/lock-check.md` — read and **run** this session: `python scripts/verify_lock_anchors.py` → `ROUTING: Closed`, exit 0, live and correct today. This is a real, currently-functioning application of the Closed/Forward/Error vocabulary (Action excluded — `lock-check.md`'s own text: "unused after the 2026-08-03 params.toml retirement... never emitted"). Not wired into `scripts/gates.yml`, CI, or `Makefile` (grepped, zero hits) — invoked only via the `/lock-check` slash command.

---

## §1 — Context

`observation_routing.md` (2026-04-25) declares `Status: Active. Replaces the prior Notice / Inquire two-phase framework` and describes a lighter three-bucket gate (Closed / no artifact; Action / code-change with owner; Forward / numbered open question) as its replacement, motivated by a 2026-04 audit finding the old framework "producing analysis, not protection" (12 JSON + 5 figures + 6 CSV + a script for threads that mostly returned "no action").

That claim has not held. `docs/notes/notice/N-YYYY-MM-DD-slug.md` — the artifact and template the doc claims it replaced — has been the estate's continuous, sole practice for recording observations since at least 2026-05-25, three months into the claimed replacement window, with zero gap and zero slowdown through today (2026-08-15, two notices filed this session alone). The Closed/Action/Forward vocabulary the doc prescribes was concretely applied in only 4 of 20 real files, all in a five-week window (2026-06-20 to 2026-07-26), always layered on top of — never replacing — the Notice-log template's own `GRADUATE / DROP / HOLD` decision vocabulary (`.claude/skills/brief-authoring/references/notice_log.md`), and that partial usage has not recurred in any of the six most recent notices (2026-08-11 through 2026-08-15).

Meanwhile `docs/methodology/inqhiori-canon.md` — the entry-point methodology doc per `CLAUDE.md` — cites the three-bucket gate as live and composing at §10/§16, as do `regime_robustness_gate.md`, `strategy_lifecycle.md`, and two ADRs. None of these citations point at a Notice-log file routed through Closed/Action/Forward as its primary mechanism; every concrete citation of "where a narrative observation actually lives" (e.g. `strategy_harvest.md:79`) points at a Notice-log file instead.

**The one real exception, and why it does not save the blanket claim.** `scripts/verify_lock_anchors.py` (wired to `/lock-check`) is a genuinely live, currently-correct application of Closed/Forward/Error routing (run this session: `ROUTING: Closed`, exit 0) — Action explicitly excluded as dead within that gate too. But it checks one mechanical fact (is Guardian's risk% inside its documented safe band), not a human-noticed "market observation, bar-data finding, anomaly, or interesting thing" — `observation_routing.md`'s own stated scope. A machine safe-band check and a researcher noticing something odd in a chart are different kinds of event; conflating them is what let the "replaces Notice/Inquire" claim stand unexamined for three months while the two practices quietly diverged — mechanical checks kept the three-bucket vocabulary, narrative observations kept Notice-log.

**Decision driver:** a Notice-phase observation filed this session (`N-2026-08-15-nsurv-single-history-magnitude-blindspot.md`) surfaced the doc/practice skew directly — `observation_routing.md` was read as part of authoring that notice and found to contradict the artifact being produced. The skew has stood, uncorrected, for the same three-plus months the Notice-log convention has continued operating.

---

## §2 — Decision

**Decision:** `observation_routing.md`'s blanket claim — a three-bucket gate "replaces the prior Notice / Inquire two-phase framework," full stop — is withdrawn as a description of current practice, and replaced with a scoped ruling that matches what each convention is actually doing:

1. **Narrative observation capture** (findings, anomalies, "interesting things" a person or agent notices between decision points — `observation_routing.md`'s own stated scope) is governed by the Notice-log convention: `docs/notes/notice/N-YYYY-MM-DD-slug.md` per `.claude/skills/brief-authoring/references/notice_log.md`, with its own `GRADUATE / DROP / HOLD [until date]` routing vocabulary. This has been the estate's continuous, sole practice for this class since before 2026-04-25.
2. **Mechanical/automated gate checks** — a single numeric fact checked by a script, not a narrative finding — may continue to use the Closed/Forward/Error vocabulary where it is already wired to real, runnable code (`scripts/verify_lock_anchors.py`). This is not "the three-bucket gate governing observation routing" in the sense `observation_routing.md` claims; it is one gate's exit-code contract that happens to share the doc's vocabulary. Action stays formally dead (unused since the 2026-08-03 `params.toml` retirement, per the gate's own text).

The three-bucket classification is not deleted or declared worthless for narrative use either — it saw real, if partial and now-dormant, organic adoption as a supplementary tally inside individual notices (4/20, 2026-06-20 to 2026-07-26) — but for that use it is downgraded from "the governing routing convention" to "an optional supplementary tag a notice's author may add," matching how it has actually been used.

**Effective:** immediately upon acceptance.
**Scope:** all future narrative observation-capture routes via Notice-log. `verify_lock_anchors.py`'s existing Closed/Forward/Error contract is unaffected by this ADR — it is not being re-routed, only correctly re-classified as a mechanical gate rather than evidence for `observation_routing.md`'s narrative-routing claim. No retroactive re-filing of any of the 20 existing notices.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Enforce the three-bucket gate going forward, treat the 20 Notice-log files as three months of non-compliant drift to correct | The evidence runs the other way: zero files predate the claimed replacement, the artifact has been used with perfect continuity since, and the six most recent files (including two filed today) show zero three-bucket adoption. Declaring three months of unbroken, still-accelerating practice "non-compliant" would be optimizing the map to match a doctrine the territory never adopted. |
| Declare both conventions equally valid, let authors choose per observation | Already tried, in effect — this is what the 4/20 partial-adoption window looks like from the inside. It produced inconsistent artifacts (some notices carry a Closed/Action/Forward tally, most don't) with no discernible rule for which observations got which treatment, and the practice self-selected back to Notice-log-only within five weeks. Codifying free choice would ratify the confusion rather than resolve it. |
| Delete `observation_routing.md` outright | The three-bucket framing (Closed = no artifact needed / Action = code change with owner / Forward = numbered question) is not wrong as a classification lens — it saw real use and may still be useful as an optional tag. Deleting the doc destroys that lens along with the false claim; correcting the status line preserves the useful part. |
| Status quo — leave `observation_routing.md` claiming "Active. Replaces..." | This is the state that produced the skew this ADR corrects. Every methodology doc that cites it (inqhiori-canon.md, regime_robustness_gate.md, strategy_lifecycle.md, two ADRs) currently asserts something the estate's own 20-file practice record contradicts — exactly the "verdicts are trustworthy, indexes are not" pattern this session's broader audit found elsewhere in the estate. |
| Treat `verify_lock_anchors.py`'s live Closed/Forward/Error routing as proof the blanket "replaces Notice/Inquire" claim held after all | The gate checks one mechanical fact (Guardian's risk% inside a safe band); `observation_routing.md`'s own scope line names "market observation, bar-data finding, anomaly, or interesting thing" — narrative findings a person or agent notices, not a numeric safe-band pass/fail. Treating a single mechanical gate's exit-code contract as evidence for a claim about narrative-observation routing conflates two different event classes, which is the specific error this ADR corrects rather than one it should repeat. |

---

## §4 — Falsifier (revert trigger)

**Revert trigger:** if Closed/Action/Forward tally usage reappears and becomes the dominant §4/§6 decision vocabulary across ≥3 consecutive newly-filed notices (superseding, not merely accompanying, GRADUATE/DROP/HOLD), that would indicate organic re-adoption and this ADR's characterization of the three-bucket gate as dormant would be wrong.

**Revert action:** author a new ADR superseding this one, documenting the re-adoption evidence with the same rigor (file-by-file, dated).

**Trigger check schedule:** no calendar date set — checked opportunistically at the next quarterly methodology audit (per `docs/notes/audits/programme-audit/` cadence), or sooner if a future Notice-log file's authoring session notices the pattern directly, the way this ADR's own trigger incident worked.

---

## §5 — Forbidden moves (under this ADR)

- **Retroactively re-labeling any of the 20 existing notices' decision fields to match one convention or the other** — the historical record stays as authored; this ADR governs future practice only.
- **Deleting the three-bucket-gate concept from `observation_routing.md` entirely** — tempting for a clean fix, ruled out because the classification lens saw genuine (if partial) organic use and destroying it along with the false status claim would lose real signal, not just noise.
- **Silently editing `inqhiori-canon.md` §10/§16's own doctrine text to remove the three-bucket-gate reference** without this ADR's cross-reference — those sections describe how the gate composes with other loop mechanics in the abstract; that description is not itself false, only `observation_routing.md`'s standing-practice claim is. Editing canon prose without the correcting ADR in place would be the same undocumented-flip failure mode this ADR exists to fix, one level up.
- **Treating this ADR as authorizing a rewrite of the notice_log.md template** — the template is already the thing that's actually working; this ADR recognizes that, it does not commission changes to it.
- **Editing `scripts/verify_lock_anchors.py` or `.claude/commands/lock-check.md` under this ADR** — their Closed/Forward/Error contract is live, correct, and out of scope; this ADR reclassifies what they are (a mechanical gate, not evidence for narrative-observation routing), it does not touch their code or behavior.

---

## §6 — Consequences

**Positive consequences:**
- Methodology docs (inqhiori-canon.md, regime_robustness_gate.md, strategy_lifecycle.md) can be corrected to cite what's actually load-bearing, closing a doc/practice skew that has stood for three-plus months.
- Future observation-capture sessions no longer face two contradictory sets of instructions (the brief-authoring skill's notice_log.md vs. observation_routing.md's three-bucket claim) with no ruling on which wins.
- The three-bucket lens is preserved as an optional supplementary tag rather than lost, for the notices where an author finds it useful.

**Negative consequences (real cost, not theatrical):**
- `observation_routing.md`'s original design intent (radically reduce Notice-phase ceremony) is formally acknowledged as not-adopted rather than fixed — the underlying complaint that motivated it (heavy 2026-04 Notice threads producing "analysis, not protection") is not re-litigated here. If that complaint still has merit against the CURRENT notice_log.md template (which is already lighter than the 2026-04 predecessor it itself replaced), that is a separate, unaddressed question.
- Six-plus files across the methodology/ADR corpus now need their own citations corrected (§7); this ADR does not itself edit all of them.

**Risks:**
- The dormancy of three-bucket usage in the six most recent notices (2026-08-11 through 2026-08-15) is a five-file, five-day window — thin evidence for "dormant" versus "the small sample of recent notices happened not to need it." Mitigated by the §4 revert trigger, which re-opens this if the pattern reverses.

**Downstream artifacts that need updating:**
- `docs/methodology/observation_routing.md` — Status line corrected, cross-reference to this ADR added (this session).
- `docs/methodology/inqhiori-canon.md` §8/§10/§16 — citation corrected to reflect this ADR's finding (this session, where cheap; flagged if not).
- `docs/methodology/regime_robustness_gate.md:199`, `docs/methodology/strategy_lifecycle.md:25,104` — citation corrected or flagged.
- `docs/adr/2026-07-10-strategies-never-locked-lifecycle-governance.md:23`, `docs/adr/2026-08-04-iterate-closure-exit-mandatory.md:21` — these are themselves ADRs; per this repo's own discipline (`Material amendment... is never a silent edit`), a citation inside an already-`Accepted` ADR's body is prose, not a locked decision text, so a corrective annotation is legal without a superseding ADR — but only if the citation itself isn't load-bearing to that ADR's own decision. Dispositioned per-file in §7/blast-radius sweep, not assumed here.
- `.claude/skills/inqhiori/SKILL.md:197,229`, `.claude/skills/fable-method/SKILL.md:40`, `.claude/commands/lock-check.md:15` — skill/command doc citations, corrected or flagged.

---

## §7 — Implementation plan

- **Phase 0** — §0 reads verified current at authoring time (this session, 2026-08-15).
- **Phase 1** — edit `docs/methodology/observation_routing.md`: Status line corrected from `Active. Replaces the prior Notice / Inquire two-phase framework` to reflect this ADR's finding; cross-reference added.
- **Phase 2** — grep-sweep in two limbs (blast-radius skill, this session): **(i)** every file citing `observation_routing.md` as current/active doctrine (16 files found in the evidence sweep); **(ii)** every file describing the Notice/Inquire replacement as settled without qualification. Each hit dispositioned (edited / bannered / explicitly ruled unaffected with reason) — see the commit that lands alongside this ADR for the executed disposition table, since the full 16-file sweep is mechanical repair work done via the blast-radius skill immediately after this ADR, not enumerated line-by-line here.
- **Phase 3** — verification block executes; this ADR's Status is `Accepted` at authoring (light-touch decision, no K/live-risk/locked-surface limb — only the doctrine limb fires, and the correction itself is the acceptance).

---

## §10 — Audit hooks (runnable)

```bash
# The core evidence claim: zero Notice files predate the claimed replacement date
git log --oneline --diff-filter=A --until=2026-04-24 -- docs/notes/notice/
# Expected: empty

# Continuity through today
git log --oneline --diff-filter=A --since=2026-08-01 -- docs/notes/notice/
# Expected: non-empty (this session's own two notices, plus MSL WHO-track etc.)

# observation_routing.md's status line no longer claims unqualified replacement
grep -n "^\*\*Status:\*\*" docs/methodology/observation_routing.md
# Expected: does not read "Active. Replaces the prior Notice / Inquire two-phase framework" verbatim

# §4 trigger check — three consecutive recent notices' decision vocabulary
for f in $(ls -t docs/notes/notice/*.md | head -3); do grep -m1 "Decision:\|Status:\*\*" "$f"; done
# Expected (at authoring): GRADUATE/DROP/HOLD dominant, no 3-in-a-row Closed/Action/Forward reversal

# The one live mechanical exception stays live and untouched by this ADR
python scripts/verify_lock_anchors.py
# Expected: exit 0, prints "ROUTING: Closed" (or Forward/Error per current Guardian state) -- unchanged by this ADR
```

---

## Verification

```bash
# ADR lifecycle graph
python scripts/check_adr_graph.py
# Expected: exit 0

# Production-source verification (Rule 0 confirmation)
git log --format='%h %cs %s' -- docs/methodology/observation_routing.md
git log --oneline --diff-filter=A -- docs/notes/notice/ | wc -l
# Expected: 4 commits / 2026-04-25 creation; 18 creation commits, 20 files

# Downstream artifact update verification
grep -rln "observation_routing" docs/ .claude/ scripts/ 2>/dev/null
# Expected: this ADR's own file, plus every corrected downstream citation pointing at it
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-15 | Initial authoring — corrects `observation_routing.md`'s "Active. Replaces..." claim against three months of continuous, unbroken Notice-log practice | Joshua (direction: "decide which convention wins") + Claude Code (Opus 5) |
