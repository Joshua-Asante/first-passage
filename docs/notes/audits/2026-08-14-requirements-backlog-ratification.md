# Requirements-prune backlog — ratification pass, 2026-08-14

**Status:** report only at authoring time; **superseded by events before this note ever committed.** All 5 chips this note spawned (§1 "Clean, mechanical") were dispatched and merged into `origin/main` the same session (PRs #824–#826, #828, #829) — confirmed via `git merge-base --is-ancestor` against each. F-2 (§2) was separately closed the same session (`docs/notes/audits/programme-audit/2026-08-14-f2-adr-corpus-disposition.md`, addendum on `docs/adr/2026-08-08-great-prune.md`). **The disposition tables below are kept as the analytical record — they were correct when written — but every "chip spawned" / "still owed" framing in §0–§2 describes a state that no longer holds by the time this file lands on `main`.** Read them as history, not as an open task list.

**Trigger:** operator direction — "question our requirements... only the necessary requirements need to stay." Initial scoping found that a near-identical mandate already ran 2026-08-08 (58-agent pipeline-requirements sweep + Great Prune + same-day conventions-delete-phase-gap-audit), closing with an explicit "further sweeping is diminishing returns" verdict and a named, unexecuted backlog. Per Rule 8 sub-rule 8 (dedup-first before new work) and this session's own clarifying-question round, this note **verifies and ratifies that existing backlog** rather than re-running the sweep.

**Method:** 6-agent parallel verification workflow (766,936 tokens, 202 tool calls) re-checking each of the 29 named backlog items against current repo state, 6 days and ~15 sessions after the original audits. Classified STILL_TRUE / ALREADY_RESOLVED / CHANGED_SINCE / COULD_NOT_VERIFY. One additional finding (CLAUDE.md M1-interlock staleness) surfaced during cross-checking and is recorded in §0.

**Source audits ratified here:**
- [`2026-08-08-pipeline-requirements-question-closing.md`](2026-08-08-pipeline-requirements-question-closing.md) §5
- [`2026-08-08-conventions-delete-phase-gap-audit.md`](2026-08-08-conventions-delete-phase-gap-audit.md) §3, §4, §9

---

## §0 — Finding at authoring time (now resolved): CLAUDE.md overstated a fixed live-safety gap

**At the time this was found**, CLAUDE.md (Live-execution posture) read: *"⚠ The M1 arming interlock reads only the acceptance artifact's `status` field — a 24-byte `{"status":"RESOLVED"}` clears it while the validator fails the same bytes. Hardening is owed before any arming conversation."* This was stale even then — `ops/c1_rail/c1_rail_arm.py:79-106` had already been fixed 2026-08-09 to invoke `validate_c1_monitoring_acceptance.validate(path, require_resolved=True)` and fail closed on a status-only forged artifact.

**Resolved:** the chip spawned for this (§1, Chip 5) was dispatched and merged same-session via PR #829, which rewrote the CLAUDE.md warning to describe the fix rather than the pre-fix vulnerability. `CLAUDE.md` at current `HEAD` already reads correctly — verify with `sed -n '30,40p' CLAUDE.md`, not the stale quote above.

---

## §1 — Disposition table

Legend: **D**=DELETE · **MD**=MARK_DORMANT · **SR**=SIMPLIFY_OR_REPAIR · **OP**=OPERATOR_DECISION_NEEDED · **NA**=KEEP_NO_ACTION

### Already resolved since 08-08 (no action owed)

| ID | Item | Resolved by |
|---|---|---|
| DOC-5 | `fxify-correct-timeout-semantic.md` falsifier limbs dark | Commit `185614d`, 2026-08-08 — dormancy banner + re-arm conditions added same day as the finding |
| DOC-8 | `regime_robustness_gate.md` Pepperstone/52-month reference implementation | Rewritten 2026-08-08/08-11 — points to `core/mc/modes.py::_run_half_panel`, live and verified |
| REPAIR-1 | Gate manifest fail-open parsing | Commit `13c178f`, 2026-08-08 — `load_manifest()` now asserts declared-count == parsed-count, `SystemExit` on mismatch |
| REPAIR-2 | Freeze protection narrow to one prereg store | Commit `4a731eb` — `GOVERNANCE_PREFIXES` widened to the whole frozen-prereg estate in both twinned scripts |
| REPAIR-8a | 4 dead relative-path links in `c1-rail/SKILL.md` | Commits `275601e` + `13c178f`, 2026-08-08 — all links now correct 3-level depth, all targets exist |

### Clean, mechanical — chips spawned (§3), all merged same-session (RESOLVED, not owed)

| ID | Item | Disposition | Chip | Resolved by |
|---|---|---|---|---|
| GATE-3 | `adr-graph` A5 dead glob (`core/strategies/*/LOCK.md` — files live under `_archive/`) | SR | 1 | PR #825 |
| GATE-4 | `adr-graph --enable NOPE` silently no-ops (reproduced live: exit 0, zero checks run) | SR | 1 | PR #825 |
| GATE-6 | `status-consistency` C3 models a retired directory convention; 2 concrete live counter-examples found (`ops/instruments/NAS100.md`, `ops/instruments/NQ.md`) | SR | 1 | PR #825 |
| DOC-2 | `lock_decision.md` template — dead-trigger factory, 2 live references, "loss: none identified" | D | 2 | PR #824 |
| DOC-3 | `1r_estimation.md` — Status:Active asserting a verdict against code deleted 2026-07-24 | MD | 2 | PR #824 |
| DOC-4 | `lean-portfolio-meta-layer.md` — own 8-week falsifier fired 2026-07-30, never discharged, still cited as parent doctrine by 2 ADRs | MD | 2 | PR #824 |
| DOC-6 | `execution_lessons.md` E1–E4 — promotion counters structurally unreachable (feeder retired), doc's own changelog admits it, Status fields never updated | MD | 2 | PR #824 |
| DOC-7 | Rule 10 stale "TV/Pepperstone" label (TV limb still canonical; gate itself works) | SR | 3 | PR #826 |
| DOC-9 | 4 skill-doc sites prescribing dead Pepperstone commands, one never touched, two only cosmetically annotated | SR | 3 | PR #826 |
| DOC-10 | OANDA/Pepperstone ADR reciprocal `Superseded-by` edge missing, invisible to the graph gate due to non-standard field name | SR | 3 | PR #826 |
| REPAIR-3 | `breadth.py --self-test` SKIP exits 0 (same as PASS) — the exact hook named in the 08-08 audit's own promoted lesson | SR | 4 | PR #829 |
| §0 | CLAUDE.md M1-interlock warning stale (describes a fixed vulnerability as open) | SR | 5 | PR #829 |

### Needs your ruling — not chip material (judgment calls, not mechanical fixes)

| ID | Item | The fork | My read |
|---|---|---|---|
| **F-2** | **Great Prune re-accretion falsifier already fired** (not from this workflow — confirmed via `STATE.md`/`SESSIONS.md`, carried open through 9+ sessions today) | ADR-count regrew 400% of the 50%-of-pruned-delta threshold in 6 days. Prescribed action per the ADR's own text: escalate to a hard doc-budget gate — which cuts directly against "fewer gates." Alternative: the HALTED prune classes (docs/briefs, docs/notes, docs/superpowers, docs/spec, docs/methodology) were stopped at 4.3% classifier precision, not because the material was safe — a smarter classifier (inbound-reference index from prose/hook citations, which the ADR names as the prerequisite for a future attempt) might still find real prunable mass there. | This is the single highest-leverage open item and predates this ratification pass. See §2. |
| GATE-1 | `pine-pin-provenance` gates.yml entry — confirmed still unfireable, only live limb is the post-merge hook | Delete the gates.yml entry, keep script + hook | Delete — zero coverage loss, confirmed twice now |
| GATE-2 | `path-liveness` — mostly redundant with `pine-manifest`, but has one narrow residual case `pine-manifest` doesn't cover (directory-existence check when Pine is entirely absent) | Delete as redundant, or keep for the residual case | Lean delete; the residual case is thin |
| DOC-1 | `feed_equivalence_discovery_test_LOCKED.md` — MANDATORY per CLAUDE.md's Firm Expansion section, but its Phase-0 steps require a directory deleted with Pepperstone | Delete (~99 lines) | This is a live gate on a process (firm expansion) that could fire again — needs explicit ruling before deletion, not a chip |
| FORK-1 | 4 independent "Rule N" numbering systems collide (docs/operational_rules.md, INQHIORI canon, futures-anomaly-discovery, databento-data) | Namespace them (`OPS-7`, `INQ-2`, etc.) or accept the ambiguity | Cross-cutting convention change — worth doing but touches every skill file, needs sign-off on the naming scheme first |
| FORK-2 | `check_falsifier_reachability.py` — never wired into gates.yml, warn-tier only, ~25-28% coverage, structurally blind to retirement (its own docstring says so) | Wire it in (as-is, with known limits) or delete it | Neither branch is free — wiring in a 25%-coverage warn-only check adds ceremony without much signal; deleting removes the only instrument for this failure class. Recommend: fix its scope first (extend past docs/adr/, see REPAIR-6), then wire in — but that's a real project, not a chip |
| FORK-3 | "Trigger check schedule" field — 70 ADR instances now (up from 68), zero mechanical owner, directly contradicts Rule 6 ("audit trigger is the lock event, not calendar") | Parse it or drop the field | Given Rule 6 already forbids the pattern the field encodes, I'd lean drop — but that's 70 files' worth of a decision, worth a deliberate ruling |
| REPAIR-5 | W4's additive clause resolves to the empty set for every live campaign (worse than measured at audit time — re-count shows 0 of the live corpus's actual pregs are named by any manifest, not 3) | Make the manifest `prereg` field required+documented, or strike the additive limb from W4 | Binary operator choice, unchanged from audit |
| REPAIR-6 | Rule 11's falsifier-reachability instrument still hard-scoped to `docs/adr/`, excludes the frozen-prereg estate entirely | Extend scope, or record frozen pregs as deliberately out of reach | Same shape as REPAIR-5 |

### Ambiguous / partial — worth a look, not urgent

| ID | Item | State |
|---|---|---|
| GATE-5 | skill-refs `../`-ref blind spot | Structural gap still real, but the specific "9 dead links" headcount is stale — a 2026-08-10 commit fixed those. 0 currently dead. |
| GATE-7 | pine-manifest/data-manifests worktree warn-skip | Premise doesn't hold in *this* worktree — `data-manifests` actually hard-fails here (partial vendor CSVs present). Confirm whether that's expected before touching. |
| REPAIR-4 | Hook-freshness check | The specific stale-hook symptom was manually fixed (reinstalled 2026-08-09); no structural safeguard was added, and `install_hooks.sh`/`.bat` still distribute by copy not symlink. |
| REPAIR-7 | Venue idle-clock time-binding | Mostly resolved — a surfacing-only cron binding now exists (`daily-repo-truth-sync` + a STATE.md row placed to be visible to it). Correctly stops short of an execution binding, which the no-agent-trades invariant forbids. |
| REPAIR-8b | On-machine skills-cache resync (`make sync-skills` from primary checkout) | Tracked open in sessions 14h/14i, then silently dropped from carry-forward lines in 14j–14o with no resolution note. Possibly done, possibly forgotten — worth a direct check. |
| FORK-4 | "docs/ in retirement-hook greps" | COULD_NOT_VERIFY — the named target script (`journal_review.py`) no longer exists in this worktree; the original claim's mechanism can't be independently re-confirmed. |

---

## §2 — F-2 re-accretion: why it was the load-bearing item (CLOSED same session)

**Resolved, not owed.** F-2 was closed the same session this note was drafted — see [`2026-08-14-f2-adr-corpus-disposition.md`](programme-audit/2026-08-14-f2-adr-corpus-disposition.md) for the full evidence and the addendum on `docs/adr/2026-08-08-great-prune.md` for the ruling. Short version: option 2 below was NOT what was chosen — instead, the full live ADR corpus (126 files) was read against the retention test; 0 of 4 deletion candidates survived adversarial verification; the ruling was that F-2's regrowth reflects genuine decision throughput, not degeneration, and the falsifier's *instrument* was replaced (content-sample re-test at future audits) rather than escalating to a hard doc-budget gate. The three options originally framed below are preserved as the reasoning trail, not as a live decision.

The Great Prune's own falsifier F-2 (`docs/adr/2026-08-08-great-prune.md` §4) reads: *"tracked bytes or ADR count regrow ≥50% of the pruned delta by 2026-11-08 ⇒ the prune treated symptom not cause — escalate to a doc-budget gate (hard, counted, in gates.yml)."*

Per `docs/SESSIONS.md` 2026-08-14h/14l: ADR count has already regrown 400% of that threshold (14 new vs. a 3.5 trigger), just 6 days in — not "trending toward," already fired. This has been carried as an open "Operator F-2 disposition" queue row through at least 9 sessions today without a ruling.

Three real options, not just the ADR's prescribed one:

1. **Escalate to a hard gate**, as the ADR's text prescribes — adds a new requirement, which is the opposite of what this session is for.
2. **Finish the HALTED prune classes** (`docs/briefs`, `docs/notes`, `docs/superpowers`, `docs/spec`, `docs/methodology`) with the better classifier the ADR itself says is the prerequisite (an inbound-reference index built from prose/hook citations, not markdown links — the first attempt found 66/69 reviewed "dead" files were actually live at 4.3% precision). This is real, scoped, owed work, not new doctrine.
3. **Reconsider the threshold itself.** The conventions audit measured August's doctrine-minting rate at ~68 ADRs/month, 5.2× the headline average, driven substantially by genuine limb-4 (risk-relevant) decisions the ceremony-tiering ADR correctly routes to full tier. A 50%-in-90-days regrowth bar may simply be miscalibrated against this repo's actual decision cadence, in which case F-2 firing isn't evidence of degeneration — it's evidence the falsifier was set assuming a slower pace than this operation actually runs at.

This needs your ruling, not a chip. My lean: option 2 (finish the halted prune with the better classifier) directly serves "only necessary requirements stay" without adding new gates or accepting unbounded growth — but it's real work, and only you can weigh it against option 3's read that some of this growth is legitimate.

---

## §3 — Cursor chips spawned (all merged — see §1 "Resolved by" column)

See chat response for the 5 chip summaries as originally drafted. All 5 merged into `origin/main` same-session (PRs #824–#826, #828, #829); the original chip prompts are historical record, not open dispatch material.

---

## Verification

```bash
# Confirm F-2 is closed (queue row removed, not present) — expect ZERO matches, that is the resolved state
grep -n "F-2" STATE.md

# Confirm the M1 interlock fix landed and reads correctly in CLAUDE.md itself (not just in code)
sed -n '30,40p' CLAUDE.md
sed -n '79,106p' ops/c1_rail/c1_rail_arm.py

# Confirm all 5 chip PRs are ancestors of HEAD
git merge-base --is-ancestor <PR-824-merge-sha> HEAD && echo "824 landed"
git log --oneline --grep="824\|825\|826\|828\|829" --merges -5

# Re-run this note's own original backlog verification (full item set, evidence, tool trace)
# Transcript: subagents/workflows/wf_b3804e49-e60/journal.jsonl (this session)
```
