# Conventions friction — Delete-phase gap audit — 2026-08-08

**Status:** report only. **$0 / K=0.** No doctrine minted, nothing deleted, no ADR
authored. Every disposition below is a *proposal* pending operator ruling.

**Builds on:** [`ADR 2026-08-08 — stakes-tiered ADR ceremony`](../../adr/2026-08-08-adr-ceremony-tiering.md)
and its 118-ADR retrospective sweep. That session ran The Algorithm's **Question**
step on conventions and landed a **Simplify** move (tier the ceremony by stakes).
This audit runs the **Delete** step that strict order places *before* Simplify.

**Why this file exists.** The prior sweep's classification annex lived only in a
session transcript (`SESSIONS.md` 2026-08-08c records "annex in session"); its
headline datum was therefore unreproducible until re-derived here. Persisting the
measurement is the cheapest fix for that class, and applies to this audit too.

**Method.** Direct reads + measured commands in this worktree, three parallel
background audits (gate coverage · dead-trigger doctrine · doctrine census), and a
20-agent adversarial verification pass over the dead-trigger findings. Findings are
labelled **[verified-here]** (I ran the command / read the line) or **[reported]**
(agent finding, adversarially verified but not personally re-run).

---

## §1 — The structural finding: Delete produced zero deletions

**[verified-here]** The entire conventions/complexity work product — branch
`claude/conventions-design-complexity-8eca79`, PR #685, commit `2a790d0` — is:

```
added: 93   deleted: 1
```

The single deleted line is one word in `docs/spec/TEMPLATE-minimal-spec.md`.

An audit whose operator direction was *"conventions may be introducing undue
friction"* shipped a **net addition of convention**. The ADR minting it is itself
limb-4 doctrine, so the audit of doctrine-minting friction incremented the
doctrine-minting rate by one.

This is not a criticism of the tiering decision, which is sound on its own terms.
It is the observation that **Delete was skipped**, and everything in §3–§7 is what
a Delete pass surfaces.

---

## §2 — Two measurement corrections to the prior sweep

| Claim | Where | Status |
|---|---|---|
| "pre-commit battery timed 137 s" | ADR §Reads | **Does not reproduce.** [verified-here] `python scripts/gate_manifest.py --tier pre-commit` → exit 0, **35.5 s**. Independent measure: 25.0 s this worktree, 39.3 s primary. ~13 s of any total is 15 separate Python interpreter starts. |
| "65 limb-4 ADRs / 5 months" | `SESSIONS.md` only — **not in the ADR** | **Reproduces.** [reported] Independent re-classification: 69/120 = 57.5% vs 65/118 = 55.1%. Number holds; it was simply unrecorded. |

**A sharper reading of the same census** [reported]: the doctrine-minting rate is
not a 5-month average, it is **a step change at 2026-06**.

| Month | ADRs | Doctrine-minting | Rate |
|---|---:|---:|---:|
| 2026-04 | 8 | 1 | 13% |
| 2026-05 | 15 | 5 | 33% |
| 2026-06 | 22 | 16 | **73%** |
| 2026-07 | 46 | 31 | 67% |
| 2026-08 (7 d) | 28 | 16 | 57% |

August is running at ~68 minting/month — **5.2× the headline rate**. The tier test
cannot touch this: limb 4 forces FULL tier precisely on doctrine-minting ADRs.

**Scale the tiering does not address** [verified-here]: 121 ADRs / **265,650 words**;
`methodology_lessons.md` 18,213 words; `operational_rules.md` 6,447; `STATE.md` 8,418;
`SESSIONS.md` 36,911. The 300-word light cap applies to ~19% of *future* ADRs.

**The ADR's own adoption hook returns 0** [verified-here]:
`grep -rl '^\*\*Tier:\*\* light' docs/adr/ | wc -l` → `0`. No light record has landed.

---

## §3 — Gap A: the gate battery has never been audited

[reported, key item verified by execution] `docs/adr/2026-08-07-w4-minimal-gate-set-dormancy.md`
covers *research* gates; `2026-08-03-gate-stack-audit.md` covers *admission* gates
G1–G10. **No artifact has ever audited `scripts/gates.yml`.**

### DELETE candidates

1. **`pine-pin-provenance` — provably unfireable.** Not inferred: a fabricated
   staged diff adding a genuine gitignored pin returned **PASS**.
   `check_pine_manifest.py:380-387` discriminates on committer identity / CI env,
   both negative on this machine, and returns before examining any pin. Its own
   docstring concedes it "cannot see the case it was written for", and
   `scripts/githooks/post-merge:41-42` states post-merge is "the ONLY live limb of
   that guard" — and that limb calls the script directly, not via `gates.yml`.
   Removing the manifest entry costs **zero** coverage. Keep script + post-merge hook.
2. **`path-liveness` — subsumed by `pine-manifest`.** After its `params.toml` leg
   retired it is a 4-directory existence check on dirs holding *tracked* files;
   `pine-manifest` hard-fails `MISSING` on the same 8 entries and additionally reads
   `PORT_MANIFEST`, which `path-liveness` ignores.
3. **`adr-graph` A5 — dead code.** 0 candidate ADRs; cannot fire before ~2026-09-01
   by arithmetic. Its inbound-ref scan globs `core/strategies/*/LOCK.md` → **zero
   matches** (LOCK files moved to `_archive/` in the cold-store), so arming it
   as-is would false-positive.

### Coverage holes (not deletions — repairs)

- **`skill-refs` cannot hard-fail `../`-prefixed refs.** `_hard_failable` rejects
  them; **9 dead ones exist right now** while the gate prints *"OK: every cited repo
  path resolves (all skills)."*
- **`status-consistency` C3** evaluates 89 unresolved links and fires on **0** — it
  models the retired `analysis→archive` move, not the live `flat→theme-nest` one.
- **`adr-graph --enable NOPE`** prints `OK (enabled=['NOPE'])` and exits 0. A typo
  silently converts the gate into a green no-op.
- **`adr-graph` A2 silently drops unparseable edges** — no "unparseable edge"
  finding exists, the same shape as the 2026-07-22 incident its own comment records.
- **`pine-manifest` / `data-manifests` warn-skip to exit 0 in every worktree**, and
  Rule 9's own remedy (`sync_pine_to_worktree.py --check`) is **not** in `gates.yml`.

### Performance (subordinate to coverage)

`boundaries` walks 33,680 paths and discards 32,997 (98%) *after* the walk —
`.venv-research` 13,771, `.venv` 7,326, `.worktrees` 7,244. Pruning at walk time
recovers ~13 s of the 39.3 s primary total.

---

## §4 — Gap B: dead-trigger doctrine (Rule 11 back-propagation misses)

Ten findings, each adversarially verified by an independent agent instructed to
**refute** it. Result: **10/10 CONFIRMED-WITH-CORRECTION, 0 refuted, all still
written as binding.** Every one required narrowing — the core claim held in all ten,
the supporting detail was overstated in all ten.

| # | Item | Verdict | Proposed disposition |
|---|---|---|---|
| 1 | `docs/spec/feed_equivalence_discovery_test_LOCKED.md` — MANDATORY onboarding pre-flight per `CLAUDE.md:92`; Phase-0 steps require deleted `data/tv_exports/pepperstone/` | CONFIRMED | **DELETE** (~99 lines) — *operator decision* |
| 2 | `.claude/skills/brief-authoring/references/lock_decision.md` — template manufacturing dead triggers into every future lock brief | CONFIRMED | **DELETE** (~241 lines) — loss: **none identified** |
| 3 | `docs/methodology/1r_estimation.md` — `Status: Active`, canonical per CLAUDE.md, asserts *"Verdict: live calibration confirmed"* against `ops/accounts.py::calc_multiplier`, deleted 2026-07-24 (`ff3510d`) | CONFIRMED | MARK-DORMANT (~281 lines) |
| 4 | `docs/adr/2026-06-04-lean-portfolio-meta-layer.md` — see §7 | CONFIRMED | MARK-DORMANT (~221 lines) |
| 5 | `docs/adr/2026-05-16-fxify-correct-timeout-semantic.md` — all four falsifier limbs dark | CONFIRMED | MARK-DORMANT |
| 6 | `execution_lessons.md` — E1–E4 promotion counters unreachable; demotion clock will auto-demote ~2027-04 for venue retirement, not pattern death | CONFIRMED | MARK-DORMANT |
| 7 | Rule 10 Phase-0 cost-geometry pre-gate — "canonical TV/**Pepperstone**" label | CONFIRMED, **materially narrowed** | REPAIR (see below) |
| 8 | `regime_robustness_gate.md` — MANDATORY in the only `dd_protection` change-control chain; keys on "52-month Pepperstone"; reference impl evicted 2026-06-05 | CONFIRMED | REPAIR |
| 9 | Skills prescribing raising commands (`fable-judge:23`, `code-defect-debugging:110,128,163`) | CONFIRMED | REPAIR |
| 10 | OANDA reciprocal supersession edge missing | CONFIRMED | REPAIR |

### The correction worth recording (finding 7)

The verifier **falsified two sub-claims** of the strongest-looking finding:

- `core/data/bar_data/EURGBP_M15.csv` was **never in the repo** —
  `git log --all -S"EURGBP_M15"` returns only the pregate's own authoring commit and
  the audit citing it. It is a hypothetical worked example, absent from the
  2026-08-03 deletion tombstone. *The error was inherited from an existing audit row
  (`2026-08-05-claim-alignment` A28), which is likewise wrong.*
- "No canonical M15 series for any other instrument" is **overstated**: the
  constraint is disjunctive ("TV/Pepperstone") and the TV limb is the standing
  canonical family. The gate exits 0 today.

Disposition is **REPAIR, not DELETE** — the pre-gate's realized-vs-assumed-stop
discipline (the USOIL trap: assumed stop reads comfortable, realized stop is sub-ATR
at ~8× the hurdle) has **no successor anywhere** —
`rg -i "realized.stop|sub-ATR|stop_atr" docs/methodology/strategy_harvest.md` → 0 hits.
Blast radius is **three** surfaces, not two: the owning ADR
`2026-06-22-cost-geometry-pregate.md:44,89` carries the same dead label.

### The instrument for this class is itself dark

**[verified-here]** `scripts/check_falsifier_reachability.py` — written for exactly
this failure class — is **not in `gates.yml`** (never runs at pre-commit, `make
check`, or `make validate`), is warn-tier (always exits 0), reaches 24/96 = **25%**
of ADR falsifier sections, and documents its own dominant blind spot:

> BLIND TO RETIREMENT. Path existence catches DELETION, not REVOCATION OF DUTY. …
> Retirement is this repo's DOMINANT darkening mode, and this script cannot see it.

Every finding in this section sits in that blind spot. **72 of 96 ADR falsifiers are
prose-only and mechanically uncheckable.**

### ⚠ Highest-stakes item — live-risk surface

> **⚠ PARTIALLY OVERTAKEN — update 2026-08-08 (post-merge with `origin/main`).** A
> concurrent session ran the quarterly dd_protection/regime review the same day and
> confirmed item 1 (C2→C0 revert check) **dead**, removing it from the
> `fwd-quarterly-regime-ddrevert` cron — verified there by direct execution
> (`time_to_pass.py --regime-check` hard-errors). See the `STATE.md` decision-index row
> dated 2026-08-08 and commit `bc8ffe7`. **What that discharged:** the recurring *cron
> obligation*. **What it did not:** the ADR itself — `git show origin/main:docs/adr/2026-05-08-dd-trigger-c2-relock.md`
> still contains **zero** dormancy or re-arm language. The Rule 11 discharge below
> therefore remains owed, and the "first scheduled review is today" framing should be
> read as "the review ran; the ADR was not amended." That commit states "no `core/`
> edits" and touched only `STATE.md`.

**[verified-here]** [`ADR 2026-05-08 — dd_protection C2 relock`](../../adr/2026-05-08-dd-trigger-c2-relock.md)
§"Forward revert trigger (load-bearing)":

> If rolling 6-month MC pass-rate on the live-extended **Pepperstone** panel falls
> below 95% for two consecutive 6-month windows … re-open the C0/C2 question.
>
> **Operationalization (2026-05-08):** quarterly cadence; … implemented in
> `analysis/time_to_pass.py` (`--regime-check` mode) and reported during the next
> four quarter-end reviews (**2026-08-08**, 2026-11-08, 2027-02-08, 2027-05-08).

The constants this trigger guards are **in force** — canonical owner
[`core/dd_protection.py:78-79`](../../../core/dd_protection.py), mirrored in `CLAUDE.md`
§Protection; re-derive, do not quote from here. This trigger was the
compensation offered for the relock consciously accepting a *failed*
regime-robustness gate. Pepperstone retired 2026-08-02; `PANELS_BY_BROKER = {}`.
The file contains **zero** dormancy or re-arm language, and its first scheduled
review is **today**.

The sibling `2026-05-23-allocation-refresh-2.md` received its dormancy addendum on
2026-07-01. Same class, same week — one swept, one missed.

---

## §5 — Gap C: duplication and namespace saturation, not dead doctrine

[reported] The corpus is **~188 discrete binding items across 8 surfaces**.
Firing rate is healthier than expected: **68% FIRED**, 13% self-cited-only,
8% never-cited, 8% structurally unmeasurable. The real friction is elsewhere.

### Four independent `Rule N` namespaces

| Namespace | Rule 1 | Rule 2 | Rule 3 |
|---|---|---|---|
| `docs/operational_rules.md` | macro-vol override | audit production code | DXTrade contractValue |
| INQHIORI canon | small-cell variance prior | budget before acting | — |
| `futures-anomaly-discovery` | declare K | least-overfit tool first | outputs are candidates |
| `databento-data` | estimate before pull | coarsest schema | symbology deliberately |

Plus **two distinct `Rule 0`s** (audit-first; "file paths are not data provenance").

A bare "Rule 2" citation is ambiguous across four systems. **This is why operational
Rules 1–4 measure as never-cited — the token is saturated, not the rule unused.**
Any citation-based governance metric on this corpus is unreliable without prefixes.

### 11 duplication clusters

Worst: **audit-first stated on ≥10 surfaces** (`rule_0.md`, op-Rule 2, op-Rule 8
sub-rules 1–4, op-Rule 10 ledger clause, INQHIORI §3+§10, `rule-0` skill,
brief-authoring check #1 + §Rule 0, Trap #3, three more skills). **Gitignored-bytes-need-a-hash-gate
carries four M-lessons** (M-9, M-12, M-13, M-22) for one mechanism.

### Orphan and phantom doctrine [verified-here]

- **`Rule 0-T`** — cited across **9 files / 14 lines**, including three production
  test files (`test_mc_fp_boundaries.py:3,33,36,50`, `test_trailing_dd_boundary.py:73`,
  `test_mc_bustday_maxdd.py:14`) with **no canonical defining section anywhere**.
  Its only definition is a fragment inside another lesson's sibling-line
  (`methodology_lessons.md:1037`). Binding production tests for 3 months, no owner —
  the inverse of the Rule 7 failure this repo guards against.
- **M-1…M-6 are phantom.** `rg "^#+ *M-[1-6]"` → **zero headings**.
  `methodology_lessons.md:114-130` declares *"the Notion / memory pointers remain
  **authoritative** for those six"* (Notion retired 2026-06-12) and instructs the
  next author to *"check both Notion and `~/.claude/.../memory/` before claiming a
  number."* **M-number assignment is gated on consulting a dead surface.**

### Registry hygiene

[reported] `methodology_lessons.md:98-102` mandates a changelog entry per lesson.
Measured: **14 of 23** have one — a **39% miss rate on the registry's own rule**.
M-23 and M-24 carry no `Status` field at all, violating format-spec field 1.

---

## §6 — Gap D: 36 pure-calendar reviews land today, unowned

**[verified-here]**

```
ADRs with a Trigger check schedule field : 68
  ... naming 2026-08-08                  : 44
  ... of those, event-driven + quarterly :  8
  ... of those, PURE CALENDAR            : 36
```

Further clusters: 29 due 2026-11-08, 10 due 2027-02-08, 6 due 2027-05-08.

Three things make this a Delete-phase finding:

1. **The estate's own doctrine forbids the pattern.** `operational_rules.md:87`
   (Rule 6): *"Calendar audits (weekly, monthly) produce mostly no-ops between locks
   and miss the high-risk zero-day-after-lock window. **Audit trigger is the lock
   event itself**, not calendar."*
2. **The field is unenforced and unindexed.** `check_adr_graph.py:31-32` parses only
   `Status | Decision date | Supersedes | Superseded-by | Superseded-in-part-by |
   Retain-until`. `Trigger check schedule` is not among them — which is why
   `STATE.md:59` says *"Nothing on this board booked it"* and *"Enumerate the riders;
   do not trust the number."*
3. **Many riders are retirement ADRs** whose subject surfaces are already gone —
   OANDA, Dukascopy, CFD-estate, FXIFY-ops, gen1-pipeline, params.toml-gate,
   challenge-era-substrate. Their recurring checks are near-guaranteed no-ops,
   exactly the failure Rule 6 names.

The convention was minted **two days before** the friction audit (commit `0f802c6`,
2026-08-06, "land Phase 0 R-B2a trigger-schedule fields"), retro-applied across the
hard-core ADRs. The audit that asked whether conventions cause friction ran 48 hours
after a convention was stamped onto 68 files and never examined it.

**Also unenforced:** `Supersedes-in-part:` is used by 3 ADRs and parsed by nothing
(`check_adr_graph.py:31`), so all 3 edges are invisible to the graph gate; and
reciprocity check A5 is not in `DEFAULT_ENABLED_CHECKS`.

---

## §7 — The one deletion the estate already ordered, and never executed

**[verified-here]** [`ADR 2026-06-04 — Lean Portfolio Meta-Layer`](../../adr/2026-06-04-lean-portfolio-meta-layer.md)
is the **only ADR in the 121-file corpus that pre-registers its own deletion**:

> **Falsifier:** if at 8 weeks no allocation decision references realized ECR — i.e.
> the framework was adopted as vocabulary while allocation behavior is unchanged —
> the meta-layer is **ceremonial** and is deleted per The Algorithm, reverting to
> OODA + ad-hoc allocation.

The ADR calls this *"binary and checkable."*

Its condition fired in the strongest available form: the ECR engine
(`journal_review.py`) was retired 2026-07-11, making it **structurally impossible**
for any allocation decision to reference realized ECR — and there were no allocation
decisions regardless. The 8-week deadline expired **2026-07-30**.

Nine days later the friction audit ran, added 93 lines, and did not execute the one
deletion already ordered. Status still reads `Accepted`; `Superseded-by: none`; and
it is cited as **parent doctrine** by `2026-06-05-concept-admissibility.md` and
`2026-06-12-three-loop-methodology-binding.md`.

Verifier disposition: **MARK-DORMANT, not DELETE** — the three-loop binding that
descends from it is live and independently ratified, so a bare deletion would strand
two children. The falsifier firing is real; the remedy is a dated discharge, not
a `git rm`.

---

## §8 — Restraint: what this audit deliberately does NOT propose

Per `feedback_visible_restraint_in_closing_brief`, recorded at equal prominence:

- **No new rule, gate, convention, or ADR.** The failure mode under study is
  doctrine-minting; answering it with doctrine would be self-refuting. Every
  structural suggestion below is framed as an operator fork, not a proposal to adopt.
- **`dd_protection` constants, allocations, Pine, lifecycle state, and the c1 rail
  are untouched.** §4's dd-relock finding is about a *dormant falsifier*, not the
  constants — `DD_TRIGGER` / `DD_SCALE` stay exactly as they are.
- **No deletion executed.** Both DELETE dispositions are proposals; the
  feed-equivalence one is explicitly flagged operator-decision.
- **The tiering ADR is not re-litigated.** It is sound on its own terms. The finding
  is that it is a Simplify move standing where a Delete pass had not run.
- **Rules 1, 3, 4 are NOT proposed for deletion** despite measuring never-cited —
  the operator directive is *"retire, but do not over-retire"*, and a dormancy banner
  (Rule 3's existing form) preserves the safety fact at near-zero read cost.

---

## §9 — Structural forks for the operator (not proposals)

Ranked by leverage. Each would beat any individual deletion; none should be adopted
without a ruling, and adopting all four would itself be a doctrine-minting event.

1. **Namespace the numbered rules** (`OPS-7`, `INQ-2`, `DBN-1`). Four independent
   `Rule N` systems make citation-based governance unmeasurable — this is the root
   cause of the never-cited measurements in §5, and it makes "did this rule ever
   fire?" answerable by grep.
2. **Wire `check_falsifier_reachability.py` into `gates.yml`, or delete it.** It is
   currently the worst of both: written for the dominant failure class, never run,
   and green by construction.
3. **Give the `Trigger check schedule` field a parser, or drop the field.** 68
   instances, 0 mechanical owner, 36 unowned obligations landing today.
4. **Add `docs/` to retirement-ADR audit-hook greps.** Both the Rule 9 and the
   `execution_lessons.md` misses trace to hooks that swept `scripts/` and `ops/`
   but not `docs/`.

---

## Audit hooks

```bash
# §1 — the net-addition measurement (merge-commit form; the branch is merged,
# so `main...branch` is empty and would print nothing — a vacuous green)
git diff --numstat 08be62c^1 08be62c | awk 'NF==3{a+=$1;d+=$2}END{print "added",a,"deleted",d}'
# expect: added 93 deleted 1

# §2 — battery timing + light-tier adoption
python scripts/gate_manifest.py --tier pre-commit
grep -rl '^\*\*Tier:\*\* light' docs/adr/ | wc -l

# §6 — trigger-check census
grep -c '^\*\*Trigger check schedule:\*\*' docs/adr/*.md | grep -v ':0' | wc -l

# §5 — phantom + orphan doctrine
grep -rn '^#\+ *M-[1-6][^0-9]' docs/ ; echo "expect: zero"
grep -rn 'Rule 0-T' docs/ tests/ | grep -c ''
```
