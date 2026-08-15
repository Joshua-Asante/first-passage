# Audit Note — Pipeline requirements sweep: Question-phase closing brief

**Audit ID:** AUDIT-2026-08-08-pipeline-requirements-question
**Date:** 2026-08-08
**Triggered by:** operator-directed sweep — "question the requirements at each chokepoint of the end-to-end research and deployment pipeline"
**Authors:** Joshua + Claude Code
**Scope:** framework layer — the entire requirement estate across generate → evaluate → deploy → measure → update-generator, plus the cross-cutting enforcement layer
**Lives in:** `docs/notes/audits/2026-08-08-pipeline-requirements-question-closing.md`
**Phase:** Question only (The Algorithm step 1). Delete is operator-gated and is recommended separately, not executed here.

---

## §0 — Source anchors

Read at audit time, all at merge `e0c269f` (PR #681, 2026-08-08) unless a different anchor is named. Every claim in §2 traces to one of these; every finding in the underlying passes carries its own `file:line`.

- `CLAUDE.md`, `STATE.md`, `docs/operational_rules.md`, `docs/rule_0.md` — the standing-doctrine surfaces the sweep judged everything against.
- `docs/adr/2026-08-07-loop-s1-environment-ratification.md`, `-loop-s2-signal-host-fork.md`, `-loop-s5-bounded-promotion-lane.md`, `-w1-intraday-honest-engine-remeasure.md`, `-w4-minimal-gate-set-dormancy.md`, `-w5-governance-diet.md`, `-w6-rail-infra-closures.md` — the seven decisions ratified 2026-08-07 that re-based the sweep mid-flight.
- `scripts/gates.yml` (15 gate ids) + `scripts/gate_manifest.py` + `scripts/githooks/pre-commit` (8-line thin caller) — the enforcement composition layer as rewritten by W5.
- `scripts/validate_c1_monitoring_acceptance.py` + `ops/c1_rail/c1_rail_arm.py:78` + `docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json` — the arm interlock and its nominal instrument.
- `docs/briefs/pre-registration/` (48 files) + `lab/analysis/**/PREREG*.md` (17) + `docs/ltm/briefs/pre-registration/` (30) + `docs/spec/PREREG-*.md` (3) + `discovery_manifests/*.json` (13) — the frozen-contract estate, five stores.
- `tests/` (103 modules), `pyproject.toml`, `requirements-ops.lock`, `requirements-research.txt`, `.github/workflows/*.yml` (4, all inert), `.gitattributes` — the non-prose requirement classes.
- `.claude/settings.json`, the 12 `.claude/hookify.*.local.md` rules, the 19 `.claude/skills/*/SKILL.md`, and the auto-memory corpus at `C:/Users/joshu/.claude/projects/C--Users-joshu-multi-firm-operations/memory/` (155 files) — the agent-side requirement stores.
- `C:/Users/joshu/.claude/scheduled-tasks/` — the out-of-repo time layer.

**Verification anchors.** Tree state `git rev-parse HEAD` = `e0c269f`. GitHub Actions confirmed disabled repo-wide (in-file note at `.github/workflows/manifest-check.yml:82-88`, verified 2026-07-31; no workflow run since ~2026-07-16). Installed hook on the primary checkout confirmed at `C:/Users/joshu/multi_firm_operations/.git/hooks/pre-commit`, dated Aug 3, 6079 bytes, zero `gate_manifest` occurrences.

**Method note.** Findings were produced by five fan-out passes (~58 subagents). Every pass paired a mapper with an adversarial questioner instructed to re-read cited locations and re-run wiring greps rather than accept the mapper's word; questioners corrected mappers on roughly one finding in six. Claims of the form "nothing invokes X" were required to survive an independent grep across `scripts/gates.yml`, `Makefile`, `.github/workflows/`, `scripts/githooks/`, `.claude/settings*.json`, and `.claude/hookify.*`. Claims of absence were required to survive `rg --no-ignore` (the LTM and lab-archive trees are excluded from default search).

---

## §1 — Trigger

The operator directed a repo-wide sweep to question the requirements at each chokepoint of the research-and-deployment pipeline, explicitly scoped to the first three INQHIORI steps — identify, notice, question — and explicitly asked for "the dumbest requirements." No specific failure prompted it; this is a scheduled-cadence structural audit landing on the 2026-08-08 quarterly checkpoint.

The sweep ran in five passes as its own critics found what earlier passes had missed:

| Pass | Scope | Agents | DUMB |
|---|---|---|---|
| 1 | Six pipeline stages + cross-cutting process gates | 13 | 17 |
| 2 | Instrument ledgers, venue obligations, availability substrate, memory corpus | 13 (4 lost to API errors) | 36 |
| 2b | Loop specs, agent hooks, all 19 skills, data procurement, venue re-run | 15 | 49 |
| 3 | Frozen contracts, test suite, infrastructure, time, enforcement-shape lens, landed-code-vs-ADR | 15 | 66 |
| 3b | Bounded: four non-canonical prereg stores + 21 non-`check_*` scripts | 2 | ~13 |

**Total: ~58 agents, ~180 DUMB findings** (pass-2's venue packet is superseded by pass-2b's re-run and is not double-counted), ~150 QUESTIONABLE, and ~230 requirements verified SOUND with live rationale.

**Failure class:** source-of-truth fracture, compounded by methodology failure — the discipline that should have caught most of this (Rule 11 falsifier-reachability, Rule 7 owner tables, the blast-radius sweep) exists and did not fire, in several cases because the checker cannot see the failure class it was written for.

---

## §2 — What actually happened

**1. The estate is larger and more fractured than any single index describes.** Every governed artifact class turned out to exist in more than one store, and each enforcement surface covers one store. Pre-registrations live in five stores; specs in three (`docs/adr/`, `docs/spec/`, `docs/superpowers/`); ADRs in two (`docs/adr/`, `docs/ltm/adr/`); K ledgers in two; agent rule stores in two (`.claude/`, `.cursor/`). Freeze protection (`session_divergence_hook.py:24`, `check_push_collision.py:45-48`) covers exactly one prereg store — the one holding the fewest active campaigns. **0 of 17 live campaign prereg bodies are guarded.**

**2. The program state moved twice mid-sweep.** PR #678 landed the S1–S7 ADRs and the W-stream during pass 2; PR #681 landed the implementation during pass 3b. Both required re-basing. This produced a finding class of its own (S7 attested-ahead-of-merge: docs and a gating JSON attesting code that existed only on unmerged branches) — which PR #681 then closed within hours, and which is recorded here as resolved rather than open.

**3. The dominant defect shape inverted between the first pass and the last.** Pass 1 found stale documents. Pass 3b found **gates that are correctly wired, run on every commit, return green, and cannot see the failure class they were built for.** Measured instances: `check_skill_refs.py` returned "OK: every cited repo path resolves" over four dead links; `Q-GATECART-1`'s only audit hook prints `SKIP` and exits 0 forever; `validate_c1_monitoring_acceptance.py` prints its strongest assurance sentence when `fixture_hashes` is empty.

**4. The single irreversible action in the program has no machine gate.** `ops/c1_rail/c1_rail_arm.py:78` reads the `status` field and never invokes the validator. Measured: a 24-byte `{"status": "RESOLVED"}` file returns `None` from `m1_acceptance_reason` (arm proceeds) while the validator returns FAIL with 19 errors on the same bytes. The 2026-07-28 operator declined to populate an inadmissible item-5 event **by hand**; no code stopped him.

**5. W4 defined the live validation floor in terms of a corpus that cannot answer.** Accepted 2026-08-07, W4 sets the live minimal gate set as "G0–G5 + G8, and any limb a campaign's own frozen prereg still binds." Measured: only 3 of 17 live prereg bodies are named by any manifest; the `prereg` field is optional and undocumented (9 of 13 manifests carry it, 1 dangles); and the single most-cited machine-bound body has no §6 gate and no audit hooks at all. **The additive clause resolves to unknown or empty for every live campaign.**

**6. The composition layer W5 introduced fails open.** `gate_manifest.py:54` uses a whitespace-exact hand-rolled parser with `if cur is None: continue`. One extra space on the first gate drops it silently — 14 of 15 parsed — and a real `--tier pre-commit` run still exits 0. Nothing asserts parsed-count equals declared-count. Separately, `--tier validate` ignores the manifest entirely in favour of a hardcoded allowlist, so `gates.yml` is not the owner of `make validate` despite W5's claim.

**7. None of it is running on the operator's machine anyway.** The installed `.git/hooks/pre-commit` predates W5 by four days and predates the 2026-08-04 closure-disposition ADR. `install_hooks.sh` distributes by `cp`, not symlink, so no hook change propagates, and no surface tells a reader to re-install.

---

## §3 — Discipline checks that should have caught it

| Check | Should have caught | Actual behavior |
|---|---|---|
| Rule 0 (read production first) | Yes — most stale-restatement findings are documents describing code | Fired correctly *within* the sweep; the sweep is itself the Rule-0 read that had not happened at estate scale |
| Rule 7 (doc-ownership / no restatement) | Yes — owner tables are exactly this | **Failed on itself**: Rule 7's own owner table still named the retired `core/config/params.toml` until PR #678 struck it |
| Rule 11 (falsifier reachability) | Yes — this is its stated job | **Structurally cannot**: `check_falsifier_reachability.py:60` hard-scopes `docs/adr`, excluding the frozen preregs, which are the artifacts that *cannot* be amended by addendum. Its own docstring caps coverage at ~25% and declares itself blind to retirement |
| blast-radius sweep (skill + hookify rule) | Yes — the propagation findings are its exact class | Fired partially: ADR 2026-08-04's amendment sweep updated code and the canonical doc but missed two downstream restatements, one of which (`strategy_harvest.md:79`) survived three separate edit passes |
| §10 audit hooks on frozen artifacts | Yes — self-checks are the class's only defence | **Never run by anything**, and four of the ones executed during this sweep were broken: one false-GREEN off a line headed `⚠ SUPERSEDED`, one false-RED from a comment wrap, two `git diff` a deleted path and return clean |
| CI as backstop | Yes | Disabled repo-wide since ~2026-07-16 with known-red workflows behind the switch; obligation to re-enable recorded only on 2026-08-07 |

The pattern across the table: **the checks that failed did not fail by being skipped. They ran and returned green.**

---

## §4 — Root cause analysis

- **Immediate cause.** Requirements outlive their substrate. Feeds, venues, tools, and consumers were retired on a well-documented cadence; the obligations denominated in them were not swept at the same time, because nothing enumerates obligations by their *inputs*.

- **Contributing factor.** Enforcement was built by accretion — each gate written for the incident that motivated it, scoped to the surface where that incident occurred. That is correct engineering at the moment of writing and becomes wrong the moment the artifact class grows a second store or the substrate moves underneath. No gate in the repo is re-validated against its own failure class when its target relocates; `check_path_liveness.py` resolves path literals only under `MANIFEST.sha256` parent dirs, which is why a `.gitattributes` selector, five `M1` fixture keys, and eight brief-template invocations could all silently unbind.

- **Structural cause.** **The repo has no requirement that a requirement be checkable, and no inventory of what is enforced versus what is merely written.** W5's `gates.yml` is the first artifact that makes "what is enforced" readable at all — and the test suite, the frozen preregs, the memory corpus, the scheduled tasks, and the venue clock are all absent from it. Where an enforcement surface does exist, nothing verifies that it can observe its own failure mode, so a green result carries whatever assurance the reader infers from the gate's *name*. That is the load-bearing repair target: **assurance is currently inferred from nomenclature rather than from coverage.**

---

## §5 — Repair plan

### Immediate

- [ ] Re-install the git hooks on the primary checkout — `bash scripts/install_hooks.sh`. Until this runs, `gates.yml` composes no commits and the 2026-08-04 closure gate is off.
- [ ] Confirm the 08-03→08-07 activity week was covered at the venue; the coverage table still reads "in progress; the first week with no coverage yet". This is the only requirement in the estate whose breach is unrecoverable.
- [ ] Before today's rider walk, run `make sentinel ASOF=2026-08-08` — the enumeration last ran 08-03 and the board's count (36 + ~10) is measured at 59 (46 field-form, 13 prose-only).
- [ ] Rule on the two scheduled tasks firing today onto dead targets, in particular `fwd-quarterly-regime-ddrevert`, which instructs a cold session to consider reverting `DD_TRIGGER` under a check retired 2026-07-22.
- [ ] Consume the book-segregation revert trigger due today: its arithmetic is already computed CROSSED (27.04% ≥ 25%) inside a suspended spec that nothing reads.
- [ ] Fix the four dead `../../docs/` links in `.claude/skills/c1-rail/SKILL.md`.

### Structural

- [x] **Decide the arm gate's nature.** **Ruled validate-path (2026-08-09):** `m1_acceptance_reason` invokes `validate(..., require_resolved=True)` and refuses on any error (branch `fix/m1-arm-validate-acceptance`); acknowledgement cannot clear an invalid/forged artifact. Historical measurement in §2.4 stands as the pre-fix record.
- [ ] **Make the gate manifest fail closed.** Assert `len(gates) == text.count('- id:')` in `load_manifest`, and either give `soft` a caller or strike it from the header.
- [ ] **Widen freeze protection** to `lab/analysis/**/PREREG*.md` and `docs/ltm/briefs/pre-registration/`, or rule explicitly that live campaign freezes are unguarded.
- [ ] **Resolve W4's additive clause** — either a manifest `prereg` field becomes required and documented, or W4 is amended to mean "G0–G5 + G8 only" with the additive limb struck.
- [ ] **Require SKIP to exit non-zero** in any artifact self-check, so "could not verify" never renders as verified.
- [ ] **Add a hook-freshness check** — the installed hook must invoke `gate_manifest.py` or hash-match `scripts/githooks/pre-commit`.
- [ ] **Extend Rule 11's instrument** past `docs/adr/`, or record that frozen preregs are deliberately outside reachability checking and name what covers them instead.
- [ ] **Bind at least one time obligation to a mechanism.** The environment has cron, calendar, and scheduled-task connectors; the venue idle clock is bound to none of them.

Deletion-shaped repairs are deliberately excluded here — they belong to the Delete pass and are operator-gated.

---

## §6 — Lessons to capture

- **Candidate lesson — a green gate is not evidence; coverage is.** Assurance in this repo is inferred from a gate's name rather than from what its predicate can observe. Anchor: this audit. Cost: counterfactual — a `check_skill_refs` green over four dead links, a `--check-tree-skew` green with five of six pinned files orphaned, and a `breadth.py --self-test` green that is a SKIP. Registry: `docs/methodology/lessons/methodology_lessons.md`. Promotion: three independent firings measured in one audit; argues for immediate promotion rather than candidate status.
- **Candidate lesson — every governed artifact class has more than one store.** Enumerating one store and treating it as the class produced a wrong conclusion at least once during the sweep (a packet concluded no idle-clock instrument exists while a full spec sat in `docs/superpowers/`). Anchor: this audit. Registry: methodology lessons. Extends the existing `absence_in_known_location_is_not_absence` lesson from files to *classes*.
- **Candidate lesson — freezing an artifact freezes its self-check against a moving repo.** A frozen §10 hook cannot be repaired by the same rule that makes it valuable, so it decays into false GREEN/RED. Anchor: four measured broken hooks. Registry: methodology lessons. New; no existing lesson covers it.
- Already covered by existing lessons, cited rather than duplicated: `lesson_corrections_land_where_read` (the reader-intercept findings), `lesson_gate_reachability_preregistration` (unreachable-or-unbinding gates — this audit is its fourth firing and by its own promote-on-third rule it should already have promoted), `lesson_dedup_attestation_must_be_executed`, `lesson_verify_content_not_path_or_id`.

---

## §7 — Programme-audit signal check

- [ ] Belt-patches without independent corroboration? — **No.** Findings are individually measured.
- [x] **Belt that only grows, never prunes?** — **Yes.** 15 always-tier gates guard document hygiene; the count has only increased, and no gate has ever been retired. This audit exists partly to enable the first prune.
- [ ] Falsifier thresholds drifting toward "we'd never hit this"? — **No**, but adjacent: several falsifiers are *structurally* unreachable rather than drifted (P4 by construction, Rule 11 by scope, W4's additive clause by corpus).
- [ ] Methodology invoked to rationalize a decision already made? — **No.**
- [ ] SNAG pattern? — **No.** Findings are heterogeneous and each pass found a different class.
- [ ] Cross-layer contamination? — **No.**
- [x] **Negative heuristic crossed without repair?** — **Yes.** "A registry appended-to but never read is a graveyard" is stated verbatim in `docs/rejected_candidates.md` as forbidden move #4, and now literally describes that file's own machine-readable limb, whose consumer was deleted 2026-07-11.

Two boxes checked. Per the protocol this note becomes an input to the 2026-08-08 programme audit rather than closing independently; the meta-layer disposition is that audit's call.

---

## §10 — Audit hooks (forward-looking)

```bash
# 1. Installed hook is current (the finding that makes every other gate moot)
grep -c gate_manifest "$(git rev-parse --git-common-dir)/hooks/pre-commit"
# Expected: >= 1.  Actual at audit time: 0

# 2. Gate manifest parses every declared gate (fail-open detector)
python -c "import pathlib,re; t=pathlib.Path('scripts/gates.yml').read_text(); \
print('declared', t.count('- id:'), 'parsed', len(re.findall(r'^  - id:', t, re.M)))"
# Expected: equal.  Any inequality means a gate is silently dropped.

# 3. The arm interlock consults its validator
grep -c "validate_c1_monitoring_acceptance\|validate(" ops/c1_rail/c1_rail_arm.py
# Expected: >= 1 if the gate was made machine-enforced.  Actual at audit time: 0

# 4. Freeze protection covers live campaign bodies
git ls-files | grep -c 'lab/analysis/.*PREREG'          # live bodies (17 at audit time)
grep -n "GOVERNANCE_PREFIXES" scripts/check_push_collision.py scripts/session_divergence_hook.py
# Expected: the prefix tuple names lab/analysis/ or an explicit ruling exists that it should not.

# 5. Frozen self-checks cannot green off a SKIP
rg -n "self-test|--check" docs/briefs/pre-registration/ lab/analysis/*/*/PREREG*.md | wc -l
# Then execute a sample and confirm SKIP paths exit non-zero.

# 6. Rider enumeration is not truncated by archival
rg --no-ignore -l "Trigger check schedule" docs/adr/ docs/ltm/adr/ | wc -l
grep -n "docs.*adr" ops/sentinel/scan.py | grep -i "glob\|iterdir"
# Expected: the sentinel's iteration reaches docs/ltm/adr/ or an explicit ruling exists that it should not.

# Recurrence check schedule
# 2026-11-08 programme audit — re-run hooks 1-6 against current state.
```

---

## §11 — Closure

- **Status:** `Open` — Question phase complete; repair and Delete both outstanding.
- **Question phase completed:** 2026-08-08.
- **Immediate repair completed:** —
- **Structural repair completed:** —
- **Lessons graduated to standing rule:** — (three candidates in §6 await promotion)
- **Follow-up triggered:** 2026-08-08 programme audit (two §7 signals checked); Delete-stage recommendation ledger (separate artifact, operator-gated).

## Iterate

**Next: ITERATE** — the Question phase closes; the Delete stage opens on its findings.

- **Entry packet:** this note's §2 (seven measured conditions), §4 (structural cause), and the ~180 finding records in the five pass outputs.
- **Stop rule:** the Delete stage closes when every Tier-1 and Tier-2 recommendation is either executed or explicitly declined by the operator, with the declines recorded. Tier-3 items exit to their own ADRs rather than blocking closure.
- **Board write:** `STATE.md` forward board — one row, "Delete-stage ledger from AUDIT-2026-08-08-pipeline-requirements-question", pointing here.
- **Not opened:** no successor Question is opened. The saturation verdict across five passes is that the document and gate axes are exhausted; further sweeping is diminishing returns. The one named residual — that every artifact class has multiple stores — is a repair, not an investigation.

---

## Verification

```bash
# Discipline checks (mechanical)
python scripts/check_brief.py docs/notes/audits/2026-08-08-pipeline-requirements-question-closing.md --type audit

# §0 anchor confirmation
git rev-parse HEAD                                    # expect e0c269f...
grep -c gate_manifest "$(git rev-parse --git-common-dir)/hooks/pre-commit"   # expect 0 (the finding)
grep -n "^  - id:" scripts/gates.yml | wc -l          # expect 15

# Cross-reference verification (cited facts match canonical sources)
sed -n '37,39p' docs/adr/2026-08-07-w4-minimal-gate-set-dormancy.md          # the additive clause
sed -n '78p'    ops/c1_rail/c1_rail_arm.py                                   # status-only read
git ls-files | grep -c 'lab/analysis/.*PREREG'                               # expect 17
```
