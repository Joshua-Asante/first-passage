# ADR 2026-08-27 — SSOT / data-lineage remediation program: Phase 0 ratification

**Status:** `Accepted` — ratified by operator (Joshua) 2026-08-27, in-session ("ratify it, commit and open the pr"). Phase 1's four tasks (§2) are now authorized; Phases 2–4 remain named-but-not-yet-scoped follow-on work per §2/§7.
**Decision date:** 2026-08-27
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Authors:** Claude Code (measurement, verification, draft) — commissioned via the Phase 0 section of the plan file below; ratification is a reserved operator action, not performed here.
**Related:** [`2026-08-09-rejection-register-topology-and-bar-wiring.md`](2026-08-09-rejection-register-topology-and-bar-wiring.md) (D4 — this program's Phase 1 Task 2 discharges it; D1–D3 are read, not reopened) · [`2026-08-22-catalog-hot-vs-disposition.md`](2026-08-22-catalog-hot-vs-disposition.md) (confirmed already `Accepted` and landed — cited for contrast, not reopened) · [`2026-08-09-check-brief-canon-ruling.md`](2026-08-09-check-brief-canon-ruling.md) (Phase 1 Task 1 discharges its unimplemented half) · [`2026-08-08-adr-ceremony-tiering.md`](2026-08-08-adr-ceremony-tiering.md) (limb-4 tier test, applied below) · [`docs/notes/audits/2026-08-21-coherence-campaign.md`](../notes/audits/2026-08-21-coherence-campaign.md) (audit-format precedent this program reuses) · plan file [`docs/superpowers/plans/2026-08-27-ssot-data-lineage-remediation.md`](../superpowers/plans/2026-08-27-ssot-data-lineage-remediation.md) (§7 implementation-plan pointer; also carries this program's Global Constraints and Non-goals)
**Layer:** governance convention (gate authorship + skill-deploy convention over `scripts/gates.yml`, `.claude/skills/`, `docs/rejected_candidates.md`/`ops/instruments/`, `docs/operational_rules.md`). **$0 / K=0.**
**Tier:** full — limb 4 fires (creates/wires gates and a deploy-verification convention that binds future ADR authoring, skill deployment, and discharges a standing doctrine obligation (D4) from a prior ADR).

---

## §0 — Rule 0 reads (executed 2026-08-27, this worktree, verbatim commands + actual output)

**Step 1 — is `scripts/check_brief.py` present under the in-repo skill source?**

```
$ find .claude/skills/brief-authoring -type f
.claude/skills/brief-authoring/references/adr.md
.claude/skills/brief-authoring/references/audit_note.md
.claude/skills/brief-authoring/references/cc_handoff.md
.claude/skills/brief-authoring/references/closure_record.md
.claude/skills/brief-authoring/references/inquire_brief.md
.claude/skills/brief-authoring/references/lesson_capture.md
.claude/skills/brief-authoring/references/notice_log.md
.claude/skills/brief-authoring/SKILL.md
```

**Finding — stronger than either branch the plan posed.** There is no `scripts/` directory under
`.claude/skills/brief-authoring/` at all, in-repo. This is not "sync is stale" (the plan's "redeploy"
branch); it is at least "the file never existed in-repo" (the plan's "author" branch). Pushed further
than the plan's own two scripted steps: `git log --oneline --all -- ".claude/skills/brief-authoring/scripts/check_brief.py"`
returns **zero commits, on any branch, ever** — the file has never existed anywhere in this repo's
version-controlled history, not merely been deleted. This directly bears on
[`2026-08-09-check-brief-canon-ruling.md`](2026-08-09-check-brief-canon-ruling.md)'s own §Reads line,
which cites `scripts/check_brief.py @ 47cc3eb · skill-side checker (untracked; --self-test PASS)`.

**Correction (caught by independent re-verification, not accepted from the first pass):** the drafting
session's first read of `git show --stat 47cc3eb` claimed the commit touches "no `check_brief.py` path
of any kind." Re-run independently: it does — a one-line `REPO_PATH_PREFIXES` tweak to the **repo-side**
`scripts/check_brief.py` (adds `ops/`, `core/`, `lab/`), bundled with an unrelated doc-reference cleanup
in `.claude/skills/brief-authoring/SKILL.md`, inside a routine 2026-07-12 lab-archival housekeeping
commit ("chore: archive 22 closed lab studies…"). Neither touched path is the skill-side script. The
best-supported reading is therefore simpler than "an untracked ghost file existed and vanished": the
2026-08-09 ADR's own §Reads citation most likely **mislabeled the repo-side `scripts/check_brief.py` as
"skill-side"** — a path/label transcription error in that ADR's own Rule-0 read — rather than there
having been a real skill-side file that was authored, used, and then lost. Either reading reaches the
same operative conclusion (the skill-side canonical checker the 2026-08-09 ADR ratified does not exist
today and must be authored, not redeployed), so Task 1's scope is unchanged; only the causal narrative
in this paragraph is corrected.

**Concrete confirmation this is live breakage, not a theoretical gap** (beyond the plan's five scripted
steps, run to corroborate): the exact command from
[`2026-08-09-rejection-register-topology-and-bar-wiring.md`](2026-08-09-rejection-register-topology-and-bar-wiring.md)'s
own `## Verification` block —

```
$ python ~/.claude/skills/brief-authoring/scripts/check_brief.py docs/adr/2026-08-09-rejection-register-topology-and-bar-wiring.md --type adr
C:\Python314\python.exe: can't open file 'C:\Users\joshu\.claude\skills\brief-authoring\scripts\check_brief.py': [Errno 2] No such file or directory
(exit 2)
```

— fails today exactly as this program's motivating table predicted. This is a live instance of "an
unverified claim propagates because nobody re-ran the verification block," on an ADR that itself
already `Accepted`.

**Step 2 — sync-skills drift check**

```
$ python scripts/sync_skills.py --check
(exit 1)
```

Non-zero exit confirmed. `brief-authoring` is named in the diff at **both** configured deploy targets
(the cloud-synced AppData primary, and `~/.claude/skills/` — per `sync_skills.py`'s own docstring
"the bundle Claude Code sessions actually load," i.e. the one the brief cites), with entries including:

```
brief-authoring/SKILL.md  (content differs)
brief-authoring/references/adr.md  (content differs)
brief-authoring/references/audit_note.md  (content differs)
brief-authoring/references/cc_handoff.md  (content differs)
brief-authoring/references/closure_record.md  (content differs)
brief-authoring/references/inquire_brief.md  (content differs)
brief-authoring/references/lesson_capture.md  (content differs)
brief-authoring/references/notice_log.md  (content differs)
brief-authoring/references/lock_decision.md  (extra in deployed)
```

**Limitation confirmed, not assumed:** neither deploy-target diff lists a `check_brief.py` entry under
`brief-authoring` at all — because `sync_skills.py --check` can only diff files that exist repo-side,
and Step 1 confirmed none does. The existing drift checker is structurally unable to surface *this*
specific defect (a canonical script that never landed on either side of the sync boundary). This is
exactly the gap Phase 1 Task 1's proposed `check_skill_deploy_sync.py` (citation-driven, not
diff-driven) exists to close, and the finding independently justifies building a second, differently-
shaped check rather than only re-running `sync_skills.py` harder.

**Step 3 — fresh falsifier-reachability census**

```
$ python scripts/check_falsifier_reachability.py --stats
ADRs scanned              : 166
carrying a falsifier      : 128
with a runnable anchor    : 30 (23%)
  -> 98 falsifiers are prose-only and UNCHECKABLE here
findings                  : 1
exempted                  : 10

check_falsifier_reachability: WARN -- standing falsifier(s) name a missing input

  2026-08-03-orb-mnq-repark-payability-falsified.md
    missing: run_t2_intraday_bust.py  (path missing)

  1 finding(s). Rule 11: append a dated dormancy + re-arm addendum to the affected ADR;
  never edit the falsifier text in place.
(exit 0)
```

This supersedes the plan's stale 2026-08-05 figure (25%, 21/83) — the corpus has grown to 166 scanned
ADRs (roughly double whatever base the old fraction was computed on) and reachable coverage sits at
**23% (30/128)** today, plus one live WARN naming a missing falsifier input
(`run_t2_intraday_bust.py`) that did not exist in the earlier snapshot. Coverage is not simply "still
~25%" — the absolute corpus has grown materially while the checked fraction stayed roughly flat,
which is itself the erosion pattern the script's own docstring self-reports. Confirmed separately:
`grep -n "falsifier_reachability\|falsifier-reachability" scripts/gates.yml` returns **no hits** — the
script is not wired into any gate tier, corroborating the plan's claim.

**Step 4 — D4's current owed status**

```
$ grep -n "D4\|per-direction feed" docs/adr/2026-08-09-rejection-register-topology-and-bar-wiring.md
:37:  Phase — `scripts/gate_manifest.py --list` → 15 gates. **None enforces the per-direction feed.**
:115: discipline collapse** — with one real residual: ledger coverage is itself partial (see D4).
:117:**D4 — The per-direction feed gets an enforcement instrument or an honest downgrade.** Rule (1) is
:118: currently enforced by nothing. Until an instrument exists, no artifact may cite the per-direction feed
:201:- **Phase 2** — the D4 enforcement instrument and the `inherited_bars` hardening are **dispatched as a
      separate packet, not built here** (they are code+tests, and this ADR is the ruling).

$ grep -rn "2026-08-09-rejection-register-topology" docs/adr/ | grep -v "2026-08-09-rejection-register-topology-and-bar-wiring.md"
(no output)
```

Zero hits on the second command: **no superseding or addendum ADR has dispatched D4's enforcement
instrument since 2026-08-09.** D4 is confirmed still owed — Phase 1 Task 2 is not already done and
must be built. (Side confirmation: today's gate roster is 22 entries, not the 15 the 2026-08-09 ADR
cited at ratification — `python scripts/gate_manifest.py --list | grep -c "tier="` → `22`. The corpus
has grown; still none of the 22 is the per-direction-feed check.)

**Step 5 — current row counts, the three rejection registers**

```
$ grep -c "^###" docs/rejected_candidates.md
69
$ grep -c "" docs/methodology/rejected_signals.md
158
$ grep -c "^|" ops/instruments/MNQ.md
58
```

Recorded verbatim, with an honest caveat: these are the blunt proxies the brief's own commands
produce, not verified entry counts. `69` counts every `###`-level heading in
`rejected_candidates.md` (not filtered to closed-candidate entries specifically). `158` is the **total
line count** of `rejected_signals.md` (`grep -c ""` counts all lines, not rows or entries — a weak
proxy). `58` counts every `|`-prefixed line across **all** markdown tables in `ops/instruments/MNQ.md`
(header/separator rows included, and not scoped to the DEAD/REJECTED table specifically). None of
these is yet the number Phase 1 Task 2 needs to size its enforcement instrument correctly — that
requires the real schema read Task 2's own Step 1 commissions (`sed -n '90,110p' ops/instruments/MNQ.md`
+ the closures-directory naming-convention scan). Recording them here only as the current-state anchor
this ADR's §0 owes, not as a sizing input.

**Additional reads (not scripted commands, context confirmation):**

- `docs/adr/2026-08-22-catalog-hot-vs-disposition.md` read in full — `Status: Accepted`, ratified
  2026-08-22, Phase 1 (parser Verdict-wins rewrite, C2 retarget, `hot` column) landed the same GO.
  Confirms the plan's "already fixed" row; not reopened here (§5 below).
- `docs/adr/2026-08-08-adr-ceremony-tiering.md:22` — limb-4 text quoted verbatim: "Creates or amends
  doctrine: a rule, gate, falsifier threshold, or convention that binds future work." Applied to this
  ADR's own tier classification above.
- Standing quarterly-programme-audit cadence confirmed against multiple sibling ADRs
  (`2026-05-08-dd-trigger-c2-relock.md:99`, `2026-06-14-rejected-candidate-patterns.md:115`, and
  others): **2026-08-08, 2026-11-08, 2027-02-08, 2027-05-08.** Today is 2026-08-27 → the next
  quarterly slate is **2026-11-08**, the same date D4's own falsifier already targets. Used in §4
  below rather than inventing a new date.
- `scripts/gates.yml` read in full for entry shape (`id` / `tier` / `cmd` list, not the plan's assumed
  `command:` scalar key — Task 1/2/3's exact YAML shape must match this, not the plan's illustrative
  snippet, when Phase 1 lands).

---

## §1 — Context

A cross-repo mining pass (2026-08-27, "Recurrence Ledger") found unverified-claim-propagation,
gate-reachability defects, and missing-SSOT axes among the most-recurring methodology problem
classes in this repo's post-pivot record. The parent plan
(`docs/superpowers/plans/2026-08-27-ssot-data-lineage-remediation.md`) named four concrete,
already-identified gaps and scoped a Phase 1 fix for each, but flagged that several of its own cited
facts (a coverage percentage, a row count, whether a successor ADR already exists) were stale or
unknown at scoping time and needed re-derivation before anything could be ratified — this is that
re-derivation.

**All four gaps are confirmed real, current, and unclosed as of this session** (§0 above), and one is
worse than the plan's own framing assumed: the skill-side `check_brief.py` has never existed in this
repo's git history at all (not "drifted from a prior deploy"), and the 2026-08-09 ADR that ratified it
as canonical cites a commit anchor that does not, on inspection, touch any `check_brief.py` path —
meaning that ADR's own Rule-0 read cannot be corroborated today. The other three gaps (D4 unbuilt,
Q-M1WIRE-1's checker unwired, `check_falsifier_reachability.py` unwired and off-cadence) match the
plan's framing exactly, with updated numbers (166 ADRs scanned vs. the stale 83-ish base, 23%
reachable vs. 25%, 22 gates vs. 15, one live WARN finding that did not exist at the plan's scoping
time).

This repo requires ADR ratification for any decision that "creates or amends doctrine — a rule, gate,
falsifier threshold, or convention that binds future work"
([`2026-08-08-adr-ceremony-tiering.md`](2026-08-08-adr-ceremony-tiering.md) limb 4). All four Phase 1
tasks add or wire a gate (`check_skill_deploy_sync.py`, `check_instrument_rejection_coverage.py`, the
M1 skew-checker's `gates.yml` entry, `check_falsifier_reachability.py`'s cadence entry), so limb 4
fires and the full template applies.

**Decision driver (one sentence):** four already-scoped, freshly-re-verified governance-tooling gaps
are ready to close, each independently shippable, but ceremony-tiering limb 4 requires ratification
before the first line of Phase 1 code lands — and self-implementing them without that ratification
would repeat, inside this very program, the exact "authored but never actually landed/ratified"
failure mode the program exists to fix.

---

## §2 — Decision

**Decision:** Ratify the phased SSOT/data-lineage remediation program described in
`docs/superpowers/plans/2026-08-27-ssot-data-lineage-remediation.md`. **Phase 1's four tasks are the
immediately-authorized scope** once this ADR's Status flips to `Accepted`:

1. **Task 1** — author (not merely redeploy — §0 Step 1 finding) the skill-side `check_brief.py` under
   `.claude/skills/brief-authoring/scripts/`, deploy it via `sync_skills.py`, and add a new
   `check_skill_deploy_sync.py` gate that walks ADR-cited `~/.claude/skills/*/scripts/*.py` paths for
   existence (closes the class of defect `sync_skills.py --check` cannot see, per §0 Step 2).
2. **Task 2** — build `check_instrument_rejection_coverage.py`, discharging D4 of
   [`2026-08-09-rejection-register-topology-and-bar-wiring.md`](2026-08-09-rejection-register-topology-and-bar-wiring.md)
   (walks terminal-negative closures against `ops/instruments/<SYM>.md` DEAD rows; WARN tier pending a
   clean baseline).
3. **Task 3** — wire the already-correct Q-M1WIRE-1 tree-skew checker
   (`scripts/validate_c1_monitoring_acceptance.py`) into `scripts/gates.yml` (a binding fix only — the
   checker itself is not rewritten).
4. **Task 4** — put `scripts/check_falsifier_reachability.py --stats` on the standing quarterly
   programme-audit cadence (`docs/operational_rules.md`), plus a WARN/informational `gates.yml` entry
   so `make validate` surfaces the trend without blocking commits.

**Phases 2–4 are named as follow-on work only** — this ADR does **not** authorize their
implementation, and each has an explicit prerequisite the parent plan states must happen first:

- **Phase 2** (consolidate the repeated hand-rolled canonical/mirror running-count pattern) — needs a
  fresh recon pass (does `check_adr_graph.py` already check running-count freshness; is there a fourth
  instance beyond the three named; is a shared mechanism actually cheaper than three independent
  prose conventions at n=3) before it can be scoped into bite-sized steps.
- **Phase 3** (instrument-profile / cost-model closed-world completeness audit) — needs a fresh Rule-0
  re-read of `docs/adr/2026-07-25-instrument-profile-index.md` and
  `docs/briefs/closures/Q-CAPBAND-1-closure-resolved.md` (5–7 weeks stale) before assuming the cited
  gaps still exist as described.
- **Phase 4** (extend the coherence-campaign cadence to explicitly include lineage/SSOT) — needs
  Phases 0–1 to actually land and clear their own falsifier-review cycle first; writing its detail now
  would presume the outcome of work this ADR has not yet authorized.

**Effective:** upon Status flipping to `Accepted` (operator GO) — Phase 1 implementation may not begin
before that, per this program's own governance note in the plan file.

**Scope:** `scripts/gates.yml`; `.claude/skills/brief-authoring/scripts/` (new) and its deployed
copies; new `scripts/check_skill_deploy_sync.py` and `scripts/check_instrument_rejection_coverage.py`
plus their tests; `docs/operational_rules.md`'s quarterly-checklist section. Explicitly **not**
`core/`, Pine, `dd_protection.py`, `firm_rules.py`, allocations, or the CATALOG / rejection-register-
topology rulings themselves (§5).

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Land Phase 1's four gates directly, no ADR | Ceremony-tiering limb 4 fires (creates/wires gates + a deploy-verification convention binding future ADR authoring and skill deployment). Skipping ratification here would repeat, inside this program, the exact "ratified in prose but never actually implemented" defect §0 found in the 2026-08-09 canon ruling itself. |
| Fold this work into the next scheduled coherence-campaign pass instead of a dedicated program | The parent plan's own Phase 4 explicitly defers this — folding in now would be "prescribing a victory lap before the win" (Phases 0–1 haven't landed or cleared a falsifier-review cycle yet), and would create the second competing audit ritual Phase 4's own "why" section warns against. |
| Re-litigate CATALOG's schema or the rejection-register topology while in the area | §0 confirmed both rulings already correctly landed (`2026-08-22-catalog-hot-vs-disposition.md` Accepted; D1–D3 of the 2026-08-09 ADR intact and un-superseded) — no new evidence surfaced to justify reopening either, and the parent plan names both as explicit non-goals. |
| Status quo — leave all four gaps as prose findings | Second consecutive instance of the same failure class (a checker authored/ratified in prose, never wired or never committed) going unaddressed; §0's own evidence (a live `No such file or directory` on an already-`Accepted` ADR's own Verification block) shows the cost of doing nothing is not hypothetical. |

---

## §4 — Falsifiable hypothesis (this ADR's own falsifier)

The plan's suggested framing ("if this program is load-bearing, then by the next quarterly programme
audit the four Phase 1 items are closed and re-verified clean, and no new instance of the same four
defect classes has been found since") is directionally right but under-specified for the ADR
template's binary-form requirement — it names no date and no concrete "re-verified clean" test. It is
sharpened below; **this is a deliberate change from the plan's wording**, not a restatement.

**H:** If this program is load-bearing, **then** at the **2026-11-08** quarterly programme audit (the
repo's standing cadence — confirmed §0 — and the same date D4's own falsifier already targets), (a)
all four Phase 1 tasks are closed, and (b) the four §10 audit hooks below all show clean/expected
state (or a dated, named exception per task), and (c) no new instance of the same four defect classes
— skill-script cited-but-never-committed, doctrine-obligation authored-but-unbuilt, checker-correct-
but-unwired, decay-audit-script-unwired-and-off-cadence — has been found in the interim.

**Falsifier:** the ADR is **FALSIFIED** if at 2026-11-08 any of — (i) a Phase 1 task remains open with
no dated, named exception; (ii) any §10 hook fails without a dated exception; (iii) a fifth instance
of the same "authored/ratified in prose, never wired or never committed" pattern is found elsewhere in
the corpus. Disposition on falsification is a superseding ADR, not a silent re-scope of this one.

**Revert action:** author a new ADR declaring `Supersedes: 2026-08-27-ssot-data-lineage-remediation-
program.md in part — <clause>` for the specific failed limb, or `full` if the whole program is
ceremony-as-implemented.

**Trigger check schedule:** quarterly programme audit, next **2026-11-08**.

---

## §5 — Forbidden moves (under this ADR)

- **Reopening the CATALOG hot/disposition ruling** (`2026-08-22-catalog-hot-vs-disposition.md`) — §0
  confirmed it `Accepted` and correctly landed this session; re-litigating its schema under cover of
  "SSOT cleanup" is exactly the re-litigation the parent plan's Non-goals rule out.
- **Reopening D1–D3 of the rejection-register topology ruling** — Task 2 discharges **D4 only** (build
  the enforcement instrument the 2026-08-09 ADR already dispatched); it must not re-rule which
  register owns what.
- **Bulk-deleting rejection-register rows** (`rejected_candidates.md`, `rejected_signals.md`,
  `ops/instruments/*.md`) to make coverage/counts look cleaner — a second Great-Prune-style pass is an
  explicit non-goal of the parent plan.
- **Touching Pine, `dd_protection.py`, `firm_rules.py`, or allocations** under cover of "governance
  tooling" — none of the four Phase 1 tasks needs to; the parent plan's Global Constraints forbid it
  outright, and this is governance/doc tooling, not risk-control code.
- **Promoting `check_instrument_rejection_coverage.py` or `check_falsifier_reachability.py` straight
  to a hard/always gate** before a clean real-corpus baseline exists — both must land WARN-tier first,
  per the M-22 lesson `check_falsifier_reachability.py`'s own docstring already cites (a hard gate here
  would block commits on ADRs nobody is touching).
- **Self-ratifying this ADR** — Status stays `Proposed` here; flipping it to `Accepted` is the reserved
  operator GO this Phase 0 dispatch was explicitly told to hold back (Step 7 of the brief, deliberately
  not performed in this session).

---

## §6 — Consequences

**Positive consequences:**
- Closes four freshly-re-verified (not stale) gaps, each independently shippable and independently
  testable, using patterns the repo already trusts (generator-script, `gates.yml` wiring, coherence-
  campaign audit format) rather than new machinery.
- Makes the "authored/ratified in prose but never actually wired or committed" failure mode visible
  going forward via new gates, instead of relying on a human re-reading prose at each quarterly audit.
- Discharges a named, dated doctrine obligation (D4) before its own 2026-11-08 falsifier date, rather
  than at the last minute.

**Negative consequences (real cost, not theatrical):**
- Two new WARN-tier gates (`skill-deploy-sync`, `instrument-rejection-coverage`) add roster
  maintenance and pre-commit/`make check` runtime.
- Task 1 requires authoring the skill-side `check_brief.py` close to from scratch (copy repo-side +
  patch against the canon ruling's decision text), not a one-line redeploy — more work, and carries
  re-implementation risk of diverging from the 2026-08-09 decision text again.
- Task 2's real coverage number is unknown until its own Step 1 schema read happens — this ADR
  authorizes building the instrument without knowing today whether the corpus is already compliant or
  carries a large backlog.

**Risks (probabilistic, distinct from costs):**
- The two skill-deploy targets can diverge independently (`sync_skills.py`'s own docstring: the
  AppData primary is cloud-synced and "the sync layer can still clobber," so drift there is advisory,
  not enforceable) — `check_skill_deploy_sync.py`'s citation-based check is a partial mitigation, not a
  guarantee that both targets stay in sync.
- §0 Step 5's three row counts (69 / 158 / 58) are blunt proxies (heading count / total line count /
  all-table row count) — using them directly to size Task 2's matcher, instead of re-deriving the real
  schema per Task 2's own Step 1, would risk under- or over-counting the obligation.

**Downstream artifacts that need updating:**
- `docs/adr/INDEX.md` — `check_adr_graph.py`'s A6 check hard-fails the moment this file exists on
  disk (INDEX drift is detected pre-stage, independent of what gets committed), so `--regenerate-index`
  was run as part of landing this file — a one-line mechanical addition (the new `Proposed` row),
  produced by the designated generator, not a hand-edit. Included in this commit alongside the ADR
  file itself, since the repo's own pre-commit gate makes the two inseparable for any new ADR.
- `STATE.md` — add a forward-obligation line for Phase 1 execution once (and only once) Status flips
  to `Accepted`; not added while `Proposed`.

---

## §7 — Implementation plan

Points at the plan file rather than re-deriving it: full task-by-task detail (files, interfaces,
failing-test-first steps, exact commit messages) lives in
[`docs/superpowers/plans/2026-08-27-ssot-data-lineage-remediation.md`](../superpowers/plans/2026-08-27-ssot-data-lineage-remediation.md)
Phases 1–4. This ADR's own phases:

- **Phase 0** — §0 reads above (done, this document). No mechanical edits beyond authoring this ADR.
- **Phase 1** — the four tasks enumerated in §2, each an independent commit/PR per the plan file, may
  land in any order once Status = `Accepted` (plan file notes Task 1 is cheapest and should go first).
- **Phase 2 (grep-sweep, Known Trap #7)** — this ADR supersedes no predecessor and de-scopes nothing,
  so there is no stale-reference limb to sweep for. The pre-decision-vocabulary limb: a scan for
  documents asserting any of the four Phase 1 gaps are *already* closed
  (`grep -rln "check_falsifier_reachability" docs/ scripts/gates.yml`,
  `grep -rln "check_skill_deploy_sync\|check_instrument_rejection_coverage" docs/`) returns no hits
  today beyond this ADR and the parent plan itself — confirming no other document needs correcting
  ahead of Phase 1 landing. Each Phase 1 task carries its own downstream-consumer list in the plan
  file's per-task `Files`/`Interfaces` sections; this ADR does not duplicate them.
- **Phase 3** — verification block below executes; Status moves to `Accepted` only on operator GO
  (Step 7 of the originating brief — explicitly not performed by this session).

---

## §10 — Audit hooks (runnable, one per Phase 1 task)

```bash
# Task 1 — skill-deploy-sync (once landed)
python scripts/sync_skills.py --check
python scripts/check_skill_deploy_sync.py
# Expected once Task 1 lands: check_skill_deploy_sync.py exits 0 (ADR-cited skill scripts present at
# ~/.claude/skills/); sync_skills.py --check drift against the cloud-synced AppData target stays
# advisory-only per its own docstring caveat, not a hard-fail condition.

# Task 2 — D4 rejection-register coverage
python scripts/check_instrument_rejection_coverage.py
# Expected: 100% ledger-coverage rate for in-window instrument-scoped terminal-negative closures, or a
# dated, named exception (discharges docs/adr/2026-08-09-rejection-register-topology-and-bar-wiring.md
# D4's own 2026-11-08 falsifier question).

# Task 3 — Q-M1WIRE-1 tree-skew wiring
python scripts/gate_manifest.py --list | grep -i skew
# Expected: an entry present. A real failure when run against the live worktree is a legitimate,
# separately-named finding (per the plan's own Task 3 Step 4 instruction) — not to be suppressed to
# make this task look done.

# Task 4 — falsifier-reachability cadence
python scripts/check_falsifier_reachability.py --stats
grep -n "check_falsifier_reachability" docs/operational_rules.md scripts/gates.yml
# Expected: the coverage trend is recorded at each quarterly programme audit (not just the point
# figure); a `gates.yml` entry (`falsifier-reachability-census`, `tier: always`) runs it report-only
# on every `make check` invocation and the CI-required `skills (3.12)` job, always exiting 0 (--stats
# alone, no --strict) -- NOT `make validate`, which is a narrower hardcoded historical selector
# (data-manifests + pine-manifest only, per gate_manifest.py's select_gates()) that Task 4's file
# scope could not extend without editing gate_manifest.py itself. This corrects this hook's original
# "make validate" wording -- see Change history.
```

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-08-27-ssot-data-lineage-remediation-program.md --type adr
python ~/.claude/skills/brief-authoring/scripts/check_brief.py docs/adr/2026-08-27-ssot-data-lineage-remediation-program.md --type adr
# ⚠ the second command is EXPECTED to fail today (`No such file or directory`) — that failure is the
# exact defect §0/§1 document and Task 1 exists to fix. Do not read it as a defect in this ADR; read it
# as corroborating evidence for the decision it ratifies.
python scripts/check_adr_graph.py
# Expected: OK (A2 edge-reciprocity is skipped while this ADR's Status is Proposed, since it declares
# no Supersedes edge at all; A6 passes because docs/adr/INDEX.md was regenerated in the same commit —
# see §6).
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-27 | Initial authoring (Phase 0, Steps 1–6 of the originating brief); Status `Proposed`; Step 7 (operator ratification) deliberately not performed this session | Claude Code |
| 2026-08-27 | §0 Step 1 correction: independent re-verification of `git show --stat 47cc3eb` found it touches repo-side `scripts/check_brief.py`, not "no check_brief.py path" as first drafted — corrected the causal narrative; the operative finding and Task 1 scope are unchanged | Claude Code |
| 2026-08-27 | Operator `Accepted` (in-session GO: "ratify it, commit and open the pr"). Phase 1 (Tasks 1-4) authorized to begin. STATE.md operator-queue row #3 + decision-index entry added same commit | Joshua (in-session) + Claude Code |
| 2026-08-28 | Review fix: §10 Task 4 audit hook corrected — the built gate (`falsifier-reachability-census`, `tier: always` in `scripts/gates.yml`) surfaces under `make check`/CI, not `make validate` (a hardcoded 2-gate historical selector Task 4's file scope could not extend); narrow text correction only, no change to §2/§6 decision or rationale | Claude Code |
