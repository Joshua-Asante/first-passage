# Audit Note — 2026-08-15 governance/documentation belt (meta layer, triggered)

**Audit ID:** AUDIT-2026-08-15-governance-belt
**Layer:** meta (methodology/governance). The belt audited here is a set of **epistemic moves that
generate decisions** — search-before-create rules, closure-disposition gates, retrieval tooling,
liveness sweeps, gate composition. It is not the portfolio.
**Date:** 2026-08-15 · **Window:** 2026-08-08 (prior quarterly cycle) → 2026-08-15
**Repo anchors:** archive tree `f608190` (worktree clean, lineage home);
live tree `Joshua-Asante/first-passage` @ PR #2 merged `2026-08-15T04:33Z`
**Triggered by:** operator direction, following a review of
[PR #2](https://github.com/Joshua-Asante/first-passage/pull/2) — *"Run a programme audit on the
governance belt."* Degeneration signals present at intake: #2 (belt that only grows) and #1
(belt-patch without independent corroboration).
**Not the scheduled quarterly.** Per the 2026-08-08 operator ruling §1.3-a, the consecutive-tally
convention counts **quarterly cycles only**; this triggered audit does **not** contribute to that
count. Next quarterly: 2026-11-08.
**Method:** single-session, evidence-before-verdict (trap #1). §3 was assembled and the ablation
executed before §4 was drafted. No subagents, no workflow.

**Cross-layer discipline:** no portfolio evidence is cited below. No PF, DD, P&L, fill, or
allocation figure appears in this audit. The PR under review touches no `core/`, `dd_protection`,
Pine, or rail surface.

---

## §0 — Rule 0 reads (verified 2026-08-15)

| # | Source | Anchor | What it establishes |
|---|---|---|---|
| 1 | [`2026-08-08-quarterly-audit.md`](2026-08-08-quarterly-audit.md) §1, §1.3-a | archive `f608190` | Prior meta verdict **Stable — watch flag** (from Progressive, ↓). Counting convention fixed to quarterly cycles. **Pre-committed flip condition** quoted verbatim in §3.7. Object q4/q7 graded **RED**. |
| 2 | [`2026-08-03-gate-stack-audit.md`](2026-08-03-gate-stack-audit.md) §4.2 | archive `f608190` | Sibling triggered audit; stack verdict **STABLE**; belt 56 adds / 7 removes (8:1), "zero genuine self-critical prunes". Establishes the belt-churn reporting convention used in §3.2. |
| 3 | [`2026-07-27-fts5-delete-falsifier-prereg-v2.md`](../../../briefs/pre-registration/2026-07-27-fts5-delete-falsifier-prereg-v2.md) | frozen `b04cd15` | **Frozen binary verdict table.** `DELETE-HOLDS` iff `R_fts5@5 ≥ 0.70` **and** `R_fts5@5 > R_rg@5`. `DELETE-FAILS` disposition is verbatim: *"Build nothing."* K=5 frozen; forbidden moves listed. |
| 4 | [`fts5_delete_falsifier_2026-07-27/RESULTS.md`](../../../../lab/analysis/harvest/fts5_delete_falsifier_2026-07-27/RESULTS.md) | archive `f608190` | Recorded verdict `DELETE-HOLDS`; `R_fts5@5` = **0.718** (84/117), `R_rg@5` = 0.222; CI [0.630, 0.792] straddles the floor, disclosed and not rescued. Authorizes "build the sidecar, search + staged write only". |
| 5 | `falsifier_v2.py` | `git show pre-prune-2026-08-08:lab/analysis/harvest/fts5_delete_falsifier_2026-07-27/falsifier_v2.py` | The measured engine ranks with **`ORDER BY bm25(docs)`** (L100). Fixture, exclusions, and engine-parity rules contain "no discretion of its own". |
| 6 | [`2026-08-13-dedup-first-before-new-work.md`](../../../adr/2026-08-13-dedup-first-before-new-work.md) §1, §3, §4 | archive `f608190` | Diagnosis: *"the failure is not a documentation gap"*. §3 **compares** cheap-reflex vs FTS5 sidecar and rules the sidecar out for this purpose. §4 T1–T3 falsifier table. |
| 7 | [`docs/operational_rules.md`](../../../operational_rules.md) §8 + edit log | live tree, PR #2 | Rule 8 sub-rules 1–10; 9 and 10 added 2026-08-15. |
| 8 | `scripts/repo_retrieve.py`, `scripts/sync_liveness_indexes.py`, `scripts/gates.yml`, `tests/test_repo_retrieve.py` | live tree, PR #2 | Full source read. Findings in §3.1 / §3.4 / §3.7. |
| 9 | [`rule-2-trip-log.md`](../rule-2-trip-log.md) | archive `f608190` | Falsifier of record for Rule 2. **1 row, a declared non-trip baseline (2026-06-16).** Own rule: empty across ≥2 cycles ⇒ falsified as load-bearing. |

**Sub-rule 10 attestation (amendment-first).** Executed before creating this file:
`ls docs/notes/audits/programme-audit/` → 13 existing artifacts. The meta-verdict owner is
`2026-08-08-quarterly-audit.md`, but that file is a *scheduled quarterly* in a closed window with
its own §10 hooks dated 2026-11-08; the protocol and the local precedent (08-03 gate-stack, 08-05
claim-alignment, 08-14 MSL — all triggered, all separate dated files) file triggered audits as new
artifacts. **New file is correct; §4 writes back to the 08-08 owner rather than restating it.**

---

## §3 — The seven diagnostics

### §3.1 Hard-core integrity

The hard core of this programme, as stated across CLAUDE.md, W5, and the retention test: **an
artifact earns its place by being load-bearing, and a check earns its place by actually checking.**

**Preserved:** no locked surface was touched. Rule 7 (link, never restate) was honored — P5's Rule 2
propagation is pointer-only, and the `skills-no-constants` gate stayed `always`. The amendment-first
rule was applied *to itself*: PR #2 landed **3 ADR addenda and 0 new ADRs**, which is the rule
working on first use.

**Violated, twice, mechanically:**

1. `scripts/repo_retrieve.py` is presented as the searchable answer to sub-rules 8 and 10 but
   cannot perform retrieval (§3.4, §3.7). Its sole functional test asserts
   `"docs/rejected_candidates.md" in hit_paths or "lab/CATALOG.md" in hit_paths` — and the tool
   returns CATALOG rows first for essentially every query, so **the assertion cannot fail for the
   reason the tool exists** (`lesson_discipline_guards_need_adversarial_tests`).
2. The `path-conditional` re-tier **inverted two triggers**. `path-liveness` fires on
   `^(scripts/|docs/|CLAUDE.md|STATE.md|REPO_MAP.md|PIPELINES.md|README.md)`; `root-doc-liveness` on
   `^(CLAUDE.md|STATE.md|README.md|REPO_MAP.md|PIPELINES.md|docs/)`. Neither matches `lab/`,
   `core/`, or `ops/`. A commit that **moves or deletes the target** of a root-doc link no longer
   runs either liveness gate at pre-commit; only editing the *pointer* does. `make check` retains
   full coverage, but `scripts/githooks/pre-commit` runs `--tier pre-commit`, and CLAUDE.md names
   the hook as the load-bearing path.

**Grade: RED.**

### §3.2 Belt churn — numbers

Window 2026-08-08 (`e0c269f`) → archive HEAD `f608190`, rename-aware (`-M`), over
`docs/adr/ docs/methodology/ docs/spec/ docs/operational_rules.md scripts/ .claude/skills/`:

| | Count |
|---|---|
| ADD | **37** |
| DELETE | **11** |
| MODIFY | 110 |
| Ratio | **3.4 : 1** |

ADRs specifically: **+23 / −10**, net **+13** in 6 days. Corpus **121 → 132**. The 2026-08-08 §10
hook states the target explicitly — *"ADR count (target: live set + tombstone index, not 121)"* —
and the count has moved **away** from it. `TOMBSTONES.md` is 22 lines.

PR #2's own contribution: **+2 scripts, +2 Rule 8 sub-rules, +1 workflow file, 3 ADR addenda,
0 removals.**

**Counterweight, recorded honestly:** the ratio is genuinely improving — 15:1 → 8:1 → 4:1 (prior
cycles) → **3.4:1** — and 11 real deletions is the largest removal count in any recorded window
except the Great Prune itself. P6 is a real *reduction* in gate execution. This is not a belt that
only grows; it is a belt that grows more slowly than it used to.

**Grade: YELLOW.** Net-positive, but trending correctly, and by the fixed convention this triggered
audit does not count toward the quarterly tally.

### §3.3 Progressive evidence

**Real, in-window:**

- **P1 registry feed repairs a dated RED.** The 2026-08-08 object q4 finding was specific and
  counted: *"`rejected_candidates.md` stopped being fed 2026-08-03 — exactly when the densest kill
  run in estate history began (~15 campaigns, zero entries). Both stopping rules non-operative."*
  P1 is the mechanical closure of exactly that, token-gated and forward-only. The diagnosis came
  from a separate process, 7 days earlier, with a number. **This is independently corroborated and
  is the strongest single item in the window.**
- **P4 found real drift**: INDEX Open rows for Q-TNEC-CON-3/CON-4 were stale against their own
  Recently-closed successors, and were repaired.
- PR #2 discloses its own three known-red gates in the PR body rather than hiding them.

**Absent:** no *predicted-and-corroborated* episode. Progressive requires a prediction made before
the outcome, then confirmed. Nothing in this window pre-registered an expectation about the belt and
then tested it. The one artifact in the corpus that did this properly — the 2026-07-27 FTS5
falsifier, which reported a CI straddle against its own interest and refused the post-hoc rescue —
is **outside** this window and its result was then detached from what shipped (§3.4).

**Grade: YELLOW.**

### §3.4 Degeneration evidence — was anything patched to rescue a conclusion?

**The central finding of this audit.**

`DELETE-HOLDS` (2026-07-27) authorized building a retrieval sidecar. That authorization rests on one
number: `R_fts5@5` = **0.718**, measured by `falsifier_v2.py`, whose engine is:

```sql
SELECT path FROM docs WHERE docs MATCH ? ORDER BY bm25(docs) LIMIT ?
```

`scripts/repo_retrieve.py`, shipped 2026-08-15 under that authorization, is:

```sql
SELECT path, heading, snippet(...) FROM chunks WHERE chunks MATCH ? LIMIT ?
```

**`ORDER BY bm25` is absent.** FTS5 without it returns rowid (insertion) order. The corpus was also
narrowed — 5 hot files, ADR bodies truncated to 24 lines, closures to 20 — and the index rebuilds
only `if not args.db.is_file()`, so it never refreshes once created. **No recall measurement was
performed on the shipped artifact**; PR #2 adds no test touching recall, ranking, or the 0.70 floor.

**Executed ablation.** The frozen harness was retrieved from `pre-prune-2026-08-08` and run against
today's tree with the frozen fixture rule, frozen exclusions, and frozen K=5 untouched. The **only**
variable is the retrieval implementation. Fixture N=35 (SESSIONS roll-off shrank it from 117),
corpus 1293 docs. Absolute values are **not** comparable to the 2026-07-27 run; the within-run
contrasts are.

| Arm | `recall@5` | hits | limb 1 (≥0.70) |
|---|---|---|---|
| A — as-authorized (`ORDER BY bm25`) | **0.600** | 21/35 | FAIL |
| B — ranking-ablated only | **0.000** | 0/35 | FAIL |
| C — as-shipped (`repo_retrieve` corpus + query) | **0.086** | 3/35 | FAIL |
| D — `rg` incumbent (frozen baseline) | **0.086** | 3/35 | — |

Removing the ranking clause alone takes the authorized engine from 0.600 to **zero**. The shipped
tool scores **0.086 — identical to the incumbent it was built to beat.** Frozen limb 2 is
`R_fts5@5 > R_rg@5`; 0.086 > 0.086 is false. **By its own frozen verdict table the shipped artifact
returns `DELETE-FAILS`, whose disposition is verbatim: "Build nothing."**

Independent of ranking, the corpus imposes a hard ceiling: only **20/35 = 0.571** of fixture targets
are reachable by `repo_retrieve`'s corpus at all — **below the 0.70 floor by construction**, before
a single query runs.

This is a belt-patch whose corroborating evidence does not attach to the artifact that shipped. The
authorizing number was silently detached from the thing it authorized. Compounding it: Rule 8
sub-rules 8 and 10 require *pasting search output*, so a stale, unranked, or (on Windows, §3.7)
dead index emits `repo_retrieve: no hits for X` — **pasteable, rule-satisfying, and false.**

**Grade: RED.**

### §3.5 Boundary respected

The frozen forbidden-moves list (fixture tuning, per-engine rewriting, post-hoc `k`) was **not**
crossed — `DELETE-HOLDS` was a genuine result, honestly reported. Q-XMEM-1 §5's denylist
(sidecar-as-owner, LTM ingest, §0 citation) is respected: `repo_retrieve` excludes `docs/ltm/` and
`lab/archive/`, verified by test, and is declared "not authority" in three places.

**One erosion.** P5 propagated Rule 2 to **five always-on surfaces** (CLAUDE.md, three skills,
session-discipline.mdc) while the ADR is `PROPOSED` and its falsifier of record — the trip log — has
**one row in 60 days, and that row is a declared non-trip**. The log's own rule is *"An empty table
across ≥2 audit cycles falsifies the rule as load-bearing (inert → amend-or-delete)."* Waiting is
sanctioned until ≈2026-12. **Widening adoption while the falsifier is starved is a different move
from waiting** — it raises the cost of the amend-or-delete the rule has pre-committed to.

**Grade: YELLOW.**

### §3.6 Theory comparison — did the chosen design outperform?

The comparison was made explicitly and recently. [`dedup-first`](../../../adr/2026-08-13-dedup-first-before-new-work.md)
§3 weighed *cheap mandatory reflex* against *FTS5 sidecar* and chose the reflex, on the record:

> *"even a built, working version misses roughly one probe in four. Not a substitute for a cheap
> mandatory reflex, and it has sat unbuilt 17+ days past authorization."*

Two days later the unchosen option was built. §3.4 measures it at incumbent parity. **The original
comparison was correct, and the evidence that confirms it arrived by building the losing option
anyway.** That is a real theory-comparison result — recorded against the programme, not for it.

**Grade: YELLOW.**

### §3.7 Falsifier check — executed

**Thresholds: zero drift.** `RECALL_FLOOR = 0.70` and `K = 5` are byte-identical in the pruned
harness and the frozen pre-registration. `DD_TRIGGER` / `DD_SCALE` untouched (not in scope, verified
absent from the diff). Rule 8's sub-rules 1–8 unedited; 9–10 are additions, logged with a dated edit
entry as the file's own convention requires.

**Inputs: swapped.** The 2026-08-08 audit's own words for the object layer were
*"the drift arrived as **removed inputs, not moved numbers**"* and *"Degeneration arrived through
removed inputs — strictly worse than drifted thresholds."* **The meta layer has now reproduced that
exact mode, seven days later**: the 0.70 floor stands untouched while the engine it was measured on
was replaced without re-measurement.

Two further reachability defects, both verified by execution:

- **`repo_retrieve.py` crashes on Windows.** It prints a hardcoded `→` (L176) and `…` (snippet
  delimiter) to a cp1252 stream. Reproduced: `UnicodeEncodeError` before any output.
  `check_advisor_dedup._fts_companion` invokes it via `subprocess.run(capture_output=True)` and
  gates on `returncode == 0`, so on the operator's primary platform **the FTS companion is a silent,
  permanent no-op** with no error surfaced. This is the same locale-decode defect class the
  2026-08-08 audit's own sentinel hit (*"crashed on the operator host (locale decode defect in
  `_git_lines`)"*) — a repeat, not a novel failure.
- **`sync_liveness_indexes.py` cannot fail.** It returns 0 on every path by design; `--check`
  carries `default=True` and `args.check` is never read. Its green is not evidence
  (`lesson_green_gate_is_not_coverage`).

**Unreachable ADR falsifiers.** [`dedup-first`](../../../adr/2026-08-13-dedup-first-before-new-work.md)
§4 pre-commits T2 (*"≥3 dated instances of a WARN dismissed as noise within one quarter"*) and T3
(*"recurrence rate over the next 90 days … measured at the next quarterly programme audit"*). **No
mechanism in the belt records that it fired.** `grep -rlE "fire_log|gate_log|telemetry" scripts/`
returns nothing. Both triggers are unmeasurable at 2026-11-08 as currently built.

**Grade: RED.**

---

## §4 — Disposition

### Verdict: **DEGENERATING**

The prior cycle's verdict was **Stable — watch flag**, and the operator's 2026-08-08 ruling fixed
the decision rule verbatim:

> *"**Consequence:** no RED remains in the meta layer, so the Degenerating trigger does not fire and
> the meta verdict moves to Stable with a watch flag … **What flips it back to Degenerating at
> 2026-11-08:** a third consecutive net-positive quarterly tally, **or any belt-patch without
> independent corroboration.**"*

Applying that rule as written:

- Trigger 1 — **not fired.** This is a triggered audit; per §1.3-a it does not count toward the
  quarterly tally. Belt churn is net-positive but improving (3.4:1). Next count: 2026-11-08.
- Trigger 2 — **fired.** §3.4 is a belt-patch whose corroborating measurement does not attach to the
  shipped artifact, established by executed ablation rather than by impression: the shipped tool
  scores at incumbent parity and returns `DELETE-FAILS` against its own frozen table.
- Independently, the 08-08 rule keys on RED: **§3.1, §3.4, and §3.7 are RED.** Under the stated
  consequence ("no RED remains ⇒ trigger does not fire"), RED remaining ⇒ it fires.

**Operator boundary — flagged, not resolved.** The clause reads *"What flips it back to Degenerating
**at 2026-11-08**"*. Two readings: (i) both triggers are evaluated at the 2026-11-08 cycle, so this
finding is **banked** and the live verdict stays Stable-watch until then; (ii) the quarterly tally is
dated 11-08 while "any belt-patch without independent corroboration" is a standing condition that
fires when observed. The sentence *"the counting convention is now fixed"* attaches to trigger 1
only. **This audit records the trigger as satisfied on its merits and leaves the fire-now-vs-bank
reading to the operator** — it is a governance call, not a measurement.

**Scope.** Degenerating applies to the governance/documentation belt as audited. It is **not** a
verdict on the portfolio (no object-layer evidence was consulted), and it does not touch any locked
surface.

**What the verdict is not.** Three items argue against a harsher reading and are recorded: P1 is a
genuinely corroborated repair of a dated RED; amendment-first was honored on its own first use
(3 addenda, 0 new ADRs); and the ADD:REMOVE ratio is improving across four measurements. The
programme is not failing at authoring discipline. It is failing at **verifying that the things it
authors do what they claim** — which is why the verdict rests on §3.4's number and not on §3.2's.

---

## §5 — Actions (protocol: every Degenerating verdict names one, with owner and date)

1. **Re-measure or withdraw `repo_retrieve.py`.** Owner: operator (route to Cursor or CC).
   **Due 2026-08-22.** Either (a) restore `ORDER BY rank`, make output ASCII-safe, stamp the index
   with `git rev-parse HEAD` and rebuild when HEAD moves, then **re-run `falsifier_v2.py` and record
   a new RESULTS artifact** against the frozen 0.70 / `> R_rg@5` table; or (b) withdraw the tool and
   the session-discipline instruction that cites it. **Until one of these lands, `repo_retrieve`
   output must not be pasted as a sub-rule 8/10 attestation** — an unranked index makes those
   attestations false. `check_advisor_dedup._fts_companion` must surface a non-zero exit instead of
   swallowing it.
2. **Add the fire log.** Owner: operator. **Due 2026-11-08 (before the quarterly).** One
   append-only JSONL line per advisory invocation — `{ts, tool, trigger, query, n_hits}` — across
   `check_advisor_dedup`, `repo_retrieve`, the `archive_lab_analysis` WARN, and
   `sync_liveness_indexes`. This is the single missing mechanism that makes dedup-first T2/T3
   measurable and answers "which of these ~18 mechanisms has never fired" at the next cycle. It is
   also the only item on this list that **enables pruning** rather than adding.
3. **Reachability pre-registration for `path-conditional`.** Owner: operator. **Due 2026-08-22.**
   For each re-tiered gate, assert its `staged_regex` matches at least one path class that can
   *cause* the violation it detects; widen `path-liveness` / `root-doc-liveness` to include
   `lab/|core/|ops/`. The tests shipped in PR #2 exercise the selector, not coverage — they would
   pass with every regex set to `^zzz`.
4. **Split `REGISTRY_GRANDFATHERED`.** Owner: operator. **Due 2026-11-08.** The 68-name frozenset
   fuses closures that legitimately owe nothing (RESOLVED/governance) with the ~15 strategy-grounds
   kills from the 08-03→08-11 feed-stop that do owe a row. As one set the debt is unenumerable, and
   `rejected_candidates.md` is the re-proposal-bar authority. Split it and put the owed subset on a
   STATE row.
5. **Rule 2: ratify or narrow.** Owner: operator. **Due 2026-11-08.** Either graduate the ADR or
   pull the pointers back to one surface. Five always-on mirrors of a PROPOSED rule with a starved
   falsifier is adoption ahead of evidence.
6. **Write back to the 08-08 owner.** Owner: this audit. Add a dated addendum to
   [`2026-08-08-quarterly-audit.md`](2026-08-08-quarterly-audit.md) §1.3-a recording that trigger 2
   was observed on 2026-08-15, so the 11-08 cycle inherits it rather than re-deriving it.

**Placement defect surfaced by this audit.** `docs/notes/` was omitted from the public seed, so
`docs/notes/audits/programme-audit/` — the protocol's mandated artifact home and the entire audit
lineage — **does not exist on the live tree**. This note is therefore filed in the archive repo. Two
repos now hold two halves of the governance record. Restoring `docs/notes/` is an operator call and
is already adjacent to open [PR #3](https://github.com/Joshua-Asante/first-passage/pull/3).

---

## §10 — Audit hooks (runnable at the 2026-11-08 cycle)

```bash
# 1. Did action 1 land? Re-run the frozen falsifier; a new RESULTS artifact must exist.
git show pre-prune-2026-08-08:lab/analysis/harvest/fts5_delete_falsifier_2026-07-27/falsifier_v2.py > /tmp/fv2.py
python /tmp/fv2.py .        # expect a recorded verdict, not silence

# 2. Is the shipped retriever ranked? (empty output = action 1 not done)
grep -n "ORDER BY" scripts/repo_retrieve.py

# 3. Does anything record that it fired? (empty = dedup-first T2/T3 still unmeasurable)
ls .cache/gate_fires.jsonl 2>/dev/null || grep -rl "fire_log\|gate_fires" scripts/

# 4. Gate reachability: do the liveness gates see lab/ yet?
python scripts/gate_manifest.py --list | grep -A2 "path-liveness\|root-doc-liveness"

# 5. Belt churn tally (quarterly count — compare against 37/11 = 3.4:1 here)
git diff -M --diff-filter=A --name-only <2026-08-15-anchor> HEAD -- docs/adr/ docs/methodology/ docs/spec/ docs/operational_rules.md scripts/ .claude/skills/ | wc -l
git diff -M --diff-filter=D --name-only <2026-08-15-anchor> HEAD -- docs/adr/ docs/methodology/ docs/spec/ docs/operational_rules.md scripts/ .claude/skills/ | wc -l

# 6. ADR corpus against the 08-08 target ("live set + tombstone index, not 121"); 132 at this audit
ls docs/adr/*.md | wc -l

# 7. Rule 2 trip log — 1 row (non-trip) at this audit; ≥2 cycles empty ⇒ amend-or-delete
grep -c "^| 2026-" docs/notes/audits/rule-2-trip-log.md
```

**Discipline check:** seven diagnostics answered with evidence anchors ✓ · belt churn counted
(37/11) ✓ · falsifier check executed, not asserted (4-arm ablation) ✓ · no cross-layer citation ✓ ·
verdict assigned with reasoning ✓ · Degenerating ⇒ six actions named with owner and date ✓ ·
§10 hooks runnable ✓.
