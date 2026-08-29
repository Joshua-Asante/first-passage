# Methodology Lessons Registry

This file is the canonical anchor for **methodology** lessons (M-class) — the
counterpart to [`execution_lessons.md`](execution_lessons.md)
which holds **execution** lessons (E-class). Both registries follow the same
shape; the distinction is which layer the lesson lives at:

- **E-class — execution layer.** Lessons about live trading behavior (skips,
  decompositions, sizing deviations). Anchored to a specific dated trade with
  a P&L counterfactual or execution gap in dollars. Watch-points historically fired from
  `live_journal/scripts/journal_review.py` (**RETIRED 2026-07-11** with the CFD estate —
  retrieve via git history; execution lessons now live in [`execution_lessons.md`](execution_lessons.md)).
- **M-class — methodology layer.** Lessons about how Claude Code (or Joshua)
  authors briefs, runs §0 reads, applies pre-Q gates, classifies observations,
  or routes findings. Anchored to a specific dated decision artefact with an
  audit-instance cost (mis-stated production fact, wrong verdict, wrong
  routing) — usually instance count rather than dollars, but dollars where the
  methodology failure caused a measurable P&L mistake. Watch-points fire from
  brief-authoring discipline (Rule-0 reads, pre-Q gate audit, regime-robustness
  gate, etc.) rather than from a runtime script.
- **F-class — fixture-caught defect.** Counterfactual lessons: a defect that
  *would have* corrupted brief evidence had a fixture test not pinned the
  anchor invariant. Introduced 2026-05-16 alongside
  `docs/adr/2026-05-16-fixture-test-requirement.md`. Anchored to a specific
  dated investigation; cost is the counterfactual brief that would have been
  corrupted (dollar estimate when P&L-acting, audit-instance count
  otherwise). Watch-point fires during §0 of brief authoring when an analysis
  script is listed as a production read.

Both registries are durable canon. Memory entries that overlap with a
registered lesson exist only as compact pointers; the lesson itself lives here.

---

## Format spec

**Lightened 2026-08-29** — this is a solo-operator error journal, not an org's audit trail; the
8-field template + dollar-threshold promotion state machine below was sized for the latter. Existing
entries (M-7 through the last one authored before this change) keep their original 8-field format
unedited — this is not a retroactive rewrite. **New entries use this light format:**

```
## M-N — short title

**Date:** YYYY-MM-DD · **Anchor:** the dated brief/ADR/commit/finding that surfaced this
**What broke:** the incident and its cost (dollar figure or audit-instance count), in 1-3 sentences.
**Rule:** imperative, one sentence — "Always X." / "Never Y." / "Before Z, do W."
**Mechanism (optional):** one line on why this fails, if not obvious from the rule alone.
**Link:** the anchor artifact.
```

A lesson is added when a real incident earns it — no promotion ceremony, no dollar threshold, no
CANDIDATE→PROMOTED state machine to track separately. Once written, it's in force. A superseded
lesson stays (history-preserving, never deleted), marked `[SUPERSEDED — see M-N]` at its own top.

**Legacy 8-field format** (M-7 onward, pre-2026-08-29): Status (`CANDIDATE`/`PROMOTED`/`DEMOTED`) ·
Anchor incident · Cost (dollar / audit-instance / wrong-verdict count) · Rule · Mechanism ·
Connection to standing doctrine · Watch-point · Output trigger, plus optional Forbidden moves /
Reproducer / Sibling lessons — see any existing M-7+ entry below for the pattern; not restated here.

### File ownership and sync

This file is the **durable canon** for M-class lessons. The `brief-authoring` skill bundle's
SKILL.md may reference these lessons; the skill is downstream — edit this file first, propagate on
next session install (same repo-wins convention as `operational_rules.md` §8's sync clause).

---

## Migration plan (M-1..M-6)

**Decision (2026-05-08):** the lesson-registry on-disk format spec above is
confirmed. M-1..M-6 (currently in user memory entries + Notion lesson page)
migrate to this file when next a brief or §0 cites them and the format
mismatch surfaces. Until then, the Notion / memory pointers remain
authoritative for those six and this file holds only newly-authored or newly-
PROMOTED methodology lessons (M-7 onward).

This is a deliberate "grow on evidence" choice: porting six lessons cold is
cheap-but-ceremonial; porting on first cite is load-bearing. The migration
order will be the order in which they are next cited.

If a future brief authors a fresh M-class lesson before any of M-1..M-6 are
cited, that fresh lesson lands here directly under its own M-N tag (using the
next free integer above the highest currently-pointed-to in memory; check
both Notion and `~/.claude/projects/.../memory/` before claiming a number).

---

## Index — standalone-file lessons (dual-pattern, candidate)

Some lessons are authored as standalone files rather than fitting the per-section M-N format above — typically multi-trap captures, candidate-status meta-methodology, or lessons whose internal structure doesn't compress cleanly to the eight canonical fields. The dual-pattern is provisional pending evidence of recurrence; if more standalone-file lessons accumulate, the `brief-authoring` SKILL.md will canonize it formally.

- **Traps #13/#14/#15 (brief-authoring meta) — CANDIDATE 2026-05-27.** Anchor: Q-JOINT-TAIL-1 brief sequence (revs 1–3 + Phase 0 BLOCKED-RETIRED). Detail: [`docs/lessons/2026-05-27-brief-authoring-traps-13-14-15.md`](../../lessons/2026-05-27-brief-authoring-traps-13-14-15.md). Promotion criteria: 2 additional firings in independent brief sequences (E2 floor) OR single ≥$3K incident (E1 floor).

---

## M-7 — Anticipation-alert audit before lock declaration

**Status:** CANDIDATE 2026-05-08 (~$103 single-incident anchor on the
2026-05-07 Guardian late fill; Route A backfill scheduled 2026-05-11 morning
will measure cumulative cost across the 2026-04-22 → 2026-05-07 union
exposure window and decide promotion).

**Anchor incident:** 2026-05-07 Guardian XAUUSD entry late-filled because
the indicator was emitting via `alertcondition()` only (no `alert()` call),
so TradingView fired the alert one bar later than the strategy logic
expected. Patched same day across Guardian, DJ30, NAS100; Aegis was patched
2026-04-27 already.

**Cost:** ~$103 entry slippage on the single 2026-05-07 Guardian fill.
Cumulative cost across the union exposure window (Aegis 5d / Guardian 14d /
DJ30 2d / NAS100 2d bugged) is to be measured by
[ops/live_journal/scripts/m7_anticipation_gap_backfill.py](../../../ops/live_journal/scripts/m7_anticipation_gap_backfill.py)
(**RETIRED 2026-07-11** — path historical; retrieve via `git show` / pre-deletion commit)
on 2026-05-11. Promotion threshold (≥$3K cumulative) clears the backfill
gate.

**Rule:** Before declaring a Pine strategy LOCK complete, audit the alert
plumbing: every signal-emitting condition MUST have a paired `alert()` call
(not just `alertcondition()`), and the active-window guard must wrap both.
The lock checklist (§7 sub-rule #5: "operational-tooling integration phase")
extends with an "anticipation alerts wired" item.

**Mechanism (why this fails):** `alertcondition()` declares an alert template
that the user must manually wire in TV's UI. `alert()` fires immediately at
bar close. A strategy locked with only `alertcondition()` requires manual UI
wiring per chart — easy to forget on a fresh chart load, and silent when
forgotten (no error; just no fill until the trader notices). The
slippage-vs-signal-bar accumulates per missed bar.

**Connection to standing doctrine:** Reinforces §7 sub-rule #5 (lock
procedures need an operational-tooling integration phase). Pine + manifest +
MC ≠ live; alert plumbing is part of "live", not part of "Pine". Also
reinforces Rule 0 audit-first discipline at lock time: read the actual
`alert(...)` call in the locked Pine source, not the docstring claim that
alerts are wired.

**Watch-point:** During lock-event hook (`scripts/lock_event_hook.py`) and
during §0 of any "lock complete" brief — grep the locked Pine source for
`alert(` calls and confirm one fires inside each entry-condition branch.

**Output trigger:** When the watch-point catches missing `alert()` plumbing,
halt the lock, patch in same-session, and update this lesson's Cost section
with the audit-instance count (third firing → cumulative-firing route to
PROMOTED).

**Forbidden moves:**
- Do NOT declare a lock complete on the strength of an `alertcondition()`-
  only audit. The `alert()` call is the load-bearing surface; the
  `alertcondition()` is decoration.
- Do NOT defer alert-plumbing fixes "to next lock cycle"; same-session patch
  preserves the audit window cleanly.

**Reproducer / worked example:** Backfill script at
[ops/live_journal/scripts/m7_anticipation_gap_backfill.py](../../../ops/live_journal/scripts/m7_anticipation_gap_backfill.py)
(**RETIRED 2026-07-11** — path historical; retrieve via `git show` / pre-deletion commit).
Per-strategy patch dates documented in the script's `PATCH_DATES`.

**Sibling lessons:** §7 sub-rule #5 (operational-tooling integration phase);
E1 (Trust the design through macro) — both reinforce that lock declarations
are load-bearing only against the live execution surface.

---

## M-8 — Mechanical thresholds need a qualitative override channel

**Status:** CANDIDATE 2026-05-10 (single near-miss anchor on GH #54 ULP audit;
DONE_WITH_CONCERNS taxonomy caught the gap before any wrong verdict landed —
no flip incurred, but the brief's §2.3 *would* have prescribed ceremonial work
under strict mechanical reading).

**Anchor incident:** GH [#54](https://github.com/Joshua-Asante/multi_firm_operations/issues/54)
ULP-precision audit on risk-control comparison sites (CC walk-away spawn,
2026-05-10). Brief §2.3 disposition rule: *"Count instances where current
treatment = NONE AND risk ≥ MED ... If count ≥ 3 → recommend opening
Q-DDP-PRECISION-SWEEP Pre-Q."* Spawn returned 5 hits — **all** in
`analysis/oanda_stage1/` (archived research code per CLAUDE.md 2026-04-29
archive; 90-day review gate 2026-07-29). Zero hits in production
risk-control sites: `dd_protection.py:92` was patched by PR
[#53](https://github.com/Joshua-Asante/multi_firm_operations/pull/53), all 6
`portfolio_mc.py` decision sites already on the precision-by-scale rule, and
`accounts.py` ratio/dollar comparisons fed by `round(_, 2)` properties.

**Cost:** Wrong-verdict count = 0 (verdict flip *prevented* by
DONE_WITH_CONCERNS surfacing; not an actual flip). Counterfactual cost if the
brief had been read mechanically: ~1 session of Pre-Q authoring + closure
overhead, $0 P&L impact, reinforcement of the ceremonial-artifact failure
mode the parallel-work doctrine is trying to suppress. Tracked as a
near-miss; promotion gated on second occurrence (a future brief whose
mechanical threshold prescribes ceremony under qualitative re-read).

**Rule:** Brief authoring must pair count-only disposition thresholds with at
least one qualitative gate (e.g., *"≥ 3 production risk-control sites"*
rather than *"≥ 3 sites"*), OR explicitly flag the threshold as
mechanical-only and rely on the spawn's `DONE_WITH_CONCERNS` channel to
surface the qualitative gap for parent-review override.

**Mechanism (why this fails):** A pure count threshold is shape-blind — it
treats live-risk-control sites and archived-research backtest filters as
equally weighted. The defect generator is a brief author writing
"sites" / "instances" / "hits" without scoping the count to the
production surface that motivated the audit in the first place. Under
mechanical reading, the threshold trips on shape-mismatched evidence and
prescribes ceremony. The cost is small per incident but compounds: each
ceremonial Pre-Q normalises the artifact-without-target pattern.

**Connection to standing doctrine:** Reinforces the brief-authoring discipline
already encoded in `brief-authoring` SKILL.md (falsifiable §4 hypothesis,
§5 forbidden moves, §6 named gate). The qualitative-gate refinement extends
§6 — gate construction must specify *what kind of evidence* the count is
counting, not just the count itself. Also reinforces the four-state status
taxonomy (DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED) as the
load-bearing recovery channel when a brief turns out to be over-restrictive
in flight.

**Watch-point:** During §6 of brief authoring, when writing any disposition
rule of the form *"if count ≥ N → action X"*. Read the rule back asking:
*"Could 5 hits in archived / dormant / out-of-spirit code trip this without
a single hit in the actual target surface?"* If yes, scope the count
qualitatively or flag mechanical-only.

**Output trigger:** When the watch-point fires, either (a) rewrite the
threshold to scope the count to the audit's intended surface (e.g.,
"production risk-control sites" not "sites"), or (b) leave the count
mechanical and add an explicit §6 line: *"Threshold is mechanical;
DONE_WITH_CONCERNS expected if hits cluster outside the audit's target
surface — parent-session override decides."* Update this lesson's Cost
section with the new instance.

**Forbidden moves:**
- Do NOT bake unscoped count thresholds into a brief's disposition rule
  without checking the qualitative re-read.
- Do NOT treat `DONE_WITH_CONCERNS` as a brief-authoring failure mode — it
  is the recovery channel that earned this near-miss its non-cost. The
  failure mode is the brief that *forces* a wrong verdict by leaving the
  spawn no concerns-channel to use.

**Reproducer / worked example:** GH [#54](https://github.com/Joshua-Asante/multi_firm_operations/issues/54)
spawn return (transcript 2026-05-10): mechanical count = 5, qualitative
re-read = 0 production hits, status = `DONE_WITH_CONCERNS`, parent disposition
= CLOSE without opening Pre-Q. The full spawn-return survey table and
disposition reasoning are in the issue's closing comment.

**Sibling lessons:** None yet at M-class. Cross-feeds the parallel-work
doctrine post-mortem (2026-05-XX) as one datapoint for the brief-authoring
skill v-next refinement (discipline check #4: "qualitative gate alongside
count thresholds").

---

## M-9 — Gitignored vendor-data manifests need a local pre-commit hash gate

**Status:** PROMOTED 2026-05-10 (GH [#62](https://github.com/Joshua-Asante/multi_firm_operations/issues/62)
Phase B — manifest drift between PR #59 and sync 93865f8; NAS100USD missing-on-disk
caught by manifest vs reality mismatch).

**Anchor incident:** Phase A RCA
`2026-05-10-pr59-manifest-drift-rca.md` (evicted 2026-06-05; retrieve via `git show pre-prune-2026-06-05:archive/docs/briefs/2026-05-10-pr59-manifest-drift-rca.md`)
§3 verdict **H2** — *"Manifest correct at b71e4a4 11:12 EDT; on-disk CSVs were
modified between 11:12 EDT and the spawn pre-flight ~12:10 EDT (or the sync at
12:21 EDT)."* (quoted from §1 H2 hypothesis as adopted in the aggregate verdict.)

**Cost:** Audit-instance count — silent manifest vs on-disk skew across five
vendor files in one session; one conclusive missing-file case (NAS100USD.csv)
that a commit-time **MISSING** check would have surfaced immediately.

**Rule:** Gitignored vendor-data manifests need a local pre-commit hash gate.
CI cannot replace it when the bytes aren't in the repo. Manual regen drifts
silently.

**Mechanism (why this fails):** Tracked manifests without an automated
validator only reflect whatever bytes existed the last time someone ran
`sha256sum`. Re-exports, CRLF normalization, and file deletes happen on disk;
CI on GitHub never sees the bytes, so **hash validation in CI is infeasible**
under the public-clone vendor-data contract. Without a local hook, drift
stays silent until a human runs a manual reconcile.

**Connection to standing doctrine:** Reinforces Rule 0 (read production +
on-disk reality before verdicts) and the public-clone posture in `CLAUDE.md`.
Complements E-class execution lessons: this is methodology-layer **data
integrity**, not fill quality.

**Watch-point:** Any PR touching `data/**/SHA256SUMS`, any spawn brief
mentioning vendor panels, or any "re-export" workflow — confirm hook installed
and regen landed in the same commit as the CSV change.

**Output trigger:** Run `python scripts/check_data_manifests.py --check`;
if it fails, run `--regenerate --dry-run` then `--regenerate`. Reference this
lesson + [`docs/adr/2026-05-10-manifest-integrity-gate.md`](../../adr/2026-05-10-manifest-integrity-gate.md).

**Forbidden moves:**
- Do NOT treat `.github/workflows/manifest-check.yml` as byte-level integrity
  coverage — it is format + tracked-path enforcement only.
- Do NOT `git commit --no-verify` for routine vendor-data work; reserve for
  exceptional bypass with explicit rationale.

**Reproducer / worked example:** Phase A drift table and NAS100USD timeline in
`2026-05-10-pr59-manifest-drift-rca.md` (evicted 2026-06-05; retrieve via `git show pre-prune-2026-06-05:archive/docs/briefs/2026-05-10-pr59-manifest-drift-rca.md`)
§2–§3.

**Sibling lessons:** None yet at M-class.

---

## M-10 — FXIFY ops integration: validator routing beats parallel display layers

**Status:** PROMOTED 2026-05-10 (multi-layer FXIFY integration review before merge;
pytest green did not catch display-layer contradictions).

**Anchor incident:** FXIFY challenge tooling shipped as a **parallel layer**: simplified
`dd_remaining_pct` / `target_remaining` remained on `status`, `cmd_update`, and
`Account.flags` alongside `fxify_rule_validator`, plus `prior_eod_equity =
initial_balance` on `add_account`, defeating skip semantics; `phase_complete`
surfaced only as a volatile flag string with no persisted audit timestamp.

**Cost:** Audit-instance cluster — five contradiction surfaces (flag merge,
status table adjacency, `cmd_update` duplicate metrics, silent daily-loss
reference, phase-complete persistence ambiguity); instance count over dollars.

**Rule:** For firm-specific rule validators, **route display and failure through the
validator exclusively** for that firm; keep simplified accounting properties only
for firms that do not use the validator. Never default fake inputs that defeat
explicit skip paths. Persist audit-worthy completion (`phase_completed_at` per-phase
dict of ISO timestamps) when adopting completion semantics.

**Mechanism (why tests missed it):** Integration tests exercised validator math;
they did not assert **single-truth UI** (no adjacent contradictory columns) or
**serialization of persisted audit fields** (`to_dict` drift vs in-memory set).

**Connection to standing doctrine:** Reinforces Rule 0 (read production paths end-to-end)
and The Algorithm (**Delete/Simplify** cross-wiring before layering features).

**Watch-point:** Any PR touching `accounts.py` FXIFY branches, `cli.py status/update`,
or `accounts.json` schema — confirm one routing path per firm and JSON round-trip
for new persisted fields.

**Output trigger:** Human review checklist for validator/display coupling; optional
UX snapshot test for FXIFY row shape.

**Forbidden moves:**
- Do not ship parallel DD semantics for the same firm on `status` / `flags` /
  `update` without explicit operator doctrine.
- Do not default `prior_eod_equity` to synthetic values that replace explicit skip.

**Reproducer / worked example:** Pre-fix `python cli.py status` showed DD Left %
next to FXIFY column; `cmd_update` printed simplified DD lines above validator
lines for FXIFY.

**Sibling lessons:** Complements M-9 (integrity drift); same theme — green tests
≠ aligned operator truth.

---

## M-11 — Falsifier-scope shadow when patching inherited infrastructure

**Status:** CANDIDATE 2026-05-28 (single $2,600 ECR-delta anchor on 2026-05-19
Aegis USDJPY silent-zone trade; below $3K promotion threshold. Pattern surfaced
2026-05-19; brief landed retroactively 2026-05-28 per Path A of Q-PARITY-1
§0-grounding review). Slot allocated as the next free integer above M-10 per
the [§Migration plan](#migration-plan-m-1m-6) registry rule; Appendix B of the
landed brief originally targeted M-8, which was already taken (mechanical
thresholds need a qualitative override channel, PROMOTED 2026-05-10).

**Anchor incident:** 2026-05-19 Aegis USDJPY trade (signal 12:15 close, fill
12:18, exit 12:45 BE-stop, realized −$2,299.50; counterfactual at
signal-correct fill ≈ +$300; single-trade ECR delta ≈ −$2,600). Pattern
documented in
`2026-05-19-cc-handoff-anticipation-gating-refactor.md` (evicted 2026-06-05; retrieve via `git show pre-prune-2026-06-05:archive/docs/briefs/2026-05-19-cc-handoff-anticipation-gating-refactor.md`)
Appendix B. Failure shape: the 2026-04-27 and 2026-05-07 `alert()` patches
added anticipation alerts on top of `strictApproach`/`approachZone`
predicates that were originally PLOT conditions correctly gated on
fireable-bar state. Reusing them as ALERT conditions inherited the wrong
gate. The patches' pre-registered falsifier (*"do alerts fire on the
any-alert-function-call subscription"*) passed by construction because it
tested delivery, not timing correctness. Silent zone went undetected until
the cost manifested as one $2,600 trade — and was found by reasoning, not by
the mechanical instrument.

**Cost:** Dollar cost $2,600 (single-trade ECR delta on 2026-05-19 Aegis;
below $3K E1/E2 promotion threshold). Latent cross-strategy exposure across
Guardian/DJ30/NAS100 silent-zone windows (4 distinct windows total per
landed brief §1 grep-sweep table) un-quantified pre-patch because no further
silent-zone trade occurred before the 2026-05-19 patch shipped.

**Rule:** When patching infrastructure that inherits structural conditions
from existing code, the patch's pre-registered §4 falsifier must include a
test of the *interaction* between new behavior and the inherited gating —
not only a test of the new behavior in isolation.

**Mechanism (why this fails):** Inherited-infrastructure patches reuse
existing predicates whose original semantic intent differs from the new
behavior's required semantic intent. A falsifier that tests the new
behavior against its own semantic intent (e.g., *"alerts deliver when
called"*) passes by construction; it fails to surface the inherited-gate
mismatch. The failure shape is invisible in isolation testing because both
the new behavior and the inherited gate are individually correct against
their own original specifications — the defect lives at the interaction
surface. M-7's falsifier covered alert *delivery*; this patch series needed
a falsifier covering alert *timing correctness against silent-zone
scenarios*, which would have required exhibiting a bar where the inherited
gate's blocking intent diverged from the alert's anticipation intent.

**Connection to standing doctrine:** Direct extension of M-7
(anticipation-alert audit before lock declaration) — M-7 added "anticipation
alerts present" to the Rule-0 read checklist; M-11 adds "interaction-test
scenario in §4 falsifier" to the brief-authoring discipline. Reinforces
brief-authoring SKILL.md check #2 (falsifiable hypothesis stated) by
specifying scope when the hypothesis covers inherited infrastructure.
Cross-feeds Rule 0 sub-rule *"architecture truth before edit prescription"*
— both name the failure mode of reasoning about new code without grounding
in existing code's actual semantics.

**Watch-point:** During §4 authoring of any brief whose §2 scope adds
behavior on top of existing infrastructure (alert calls on plot predicates,
ADR clauses that inherit prior-ADR gating, lock-decision criteria that
inherit prior-lock anchors, CC handoffs whose pre-conditions inherit
prior-handoff post-conditions). Specifically when the existing
infrastructure was authored for a different purpose than the new behavior is
reusing it for.

**Output trigger:** Add to §4 of any inheritance-extending brief: (a) a
specific scenario where the inherited gating's original semantic intent
diverges from the new behavior's required semantic intent, (b) an assertion
that the new behavior fires (or correctly does not fire) in that scenario,
(c) confirmation that the scenario exhibits the divergence (not just that
the new behavior works in some unrelated scenario). Reference this lesson +
cost; do not re-derive the discipline.

**Forbidden moves:**
- Do NOT scope a falsifier to *"does the new behavior work"* when the new
  behavior reuses predicates authored for a different purpose. That
  falsifier passes by construction and surfaces the interaction defect only
  in production.
- Do NOT defer the interaction-scenario authoring to the spawn ("CC will
  figure out what to test"). The scenario is brief-authoring work; the
  spawn verifies, it does not author.
- Do NOT treat *"the existing infrastructure already works"* as evidence
  that the patched behavior works. The patched behavior IS the interaction,
  which is novel even when both sides are individually mature.

**Promotion criteria (per landed brief Appendix B):** Graduates from
CANDIDATE to PROMOTED if either (a) a backward-discovered silent-zone trade
in the 2026-04-27 → 2026-05-19 pre-patch window adds ≥$1K to the anchor
cost, pushing total ≥$3K, OR (b) a pattern-match instance of this failure
mode appears in a future patch unrelated to alerts (e.g., an ADR whose
gating inherits from a prior-ADR's gating with mismatched original intent).

**Reproducer / worked example:**
`2026-05-19-cc-handoff-anticipation-gating-refactor.md` (evicted 2026-06-05; retrieve via `git show pre-prune-2026-06-05:archive/docs/briefs/2026-05-19-cc-handoff-anticipation-gating-refactor.md`)
§1 mechanism analysis and Appendix B pattern statement.

**Sibling lessons:** M-7 (direct prior; same alert infrastructure, prior
falsifier covered delivery but not timing correctness — M-11 is the
falsifier-shape lesson that M-7's prior patch series would have needed).
Brief-authoring traps #13/#14/#15 (sibling brief-authoring discipline
lessons captured 2026-05-27 in
[`docs/lessons/2026-05-27-brief-authoring-traps-13-14-15.md`](../../lessons/2026-05-27-brief-authoring-traps-13-14-15.md))
— shared root principle: briefs encode implicit assumptions about
reality, and those assumptions need explicit verification at authoring
time. M-11's specific assumption: the inherited predicate's original
semantic intent.

---

## M-12 — Gitignored-target CC handoffs need post-execution verification beyond CC's own return status

**Status:** CANDIDATE 2026-05-28 (single workstream-class anchor on the
2026-05-19 → 2026-05-28 anticipation-gating deployment failure: original
CC handoff dispatched 2026-05-19 to ship Pine patches to all 4 locked
indicators, but the patches never actually landed on any of them.
Absence undetected for 9 days until Joshua's TV-side grep 2026-05-28
during Q-PARITY-1 Phase 0 audit-doc authoring surfaced it). Cost: $0
(no silent-zone trade fired during the 9-day no-patch window — Poisson
coincidence on infrequently-firing strategies, not patch success).

**Anchor incident:** The 2026-05-19 anticipation-gating refactor CC handoff (`2026-05-19-cc-handoff-anticipation-gating-refactor.md`, evicted 2026-06-05; retrieve via `git show pre-prune-2026-06-05:archive/docs/briefs/2026-05-19-cc-handoff-anticipation-gating-refactor.md`)
(landed retroactively 2026-05-28 at commit `30215a1`) specified Pine-level
patches to all 4 locked indicators (Aegis v4.3, Guardian v5.5, Striker
DJ30 v4.5, Striker NAS100 v1) to separate the anticipation gate from the
signal-fire gate. The handoff was dispatched to CC but the patches never
actually landed on any indicator on TradingView. Joshua confirmed via
direct TV-side grep for `anticip_pass` on 2026-05-28 that none of the
four indicators contained the variable. Discovery occurred during
Q-PARITY-1 Phase 0 audit-doc authoring when the indicator paste showed
pre-patch state across all four files (originally pasted as the canonical
indicator source for the [Aegis audit doc](../../audits/2026-05-28-aegis-v43-indicator-strategy-diff.md)).
Patches re-shipped same day via [diff-generation-only handoff](../../briefs/handoffs/2026-05-28-cc-handoff-anticipation-gating-reship.md)
(commit `c92de94`) + parent-side TV application by Joshua + post-application
audit hook 4× OK (per [closure](../../briefs/handoffs/2026-05-28-cc-handoff-anticipation-gating-reship-closure.md),
commit `1a1aba1`).

**Cost:** Dollar cost = $0 (no silent-zone trade fired during the 9-day
no-patch window 2026-05-19 → 2026-05-28). Workstream-class wrong-state
count = 4 (the same handoff failure spanned all 4 strategy targets;
counted as 1 instance per the M-class convention since it was a single
workstream-class failure, not 4 independent strategy-level failures).
Latent counterfactual cost: each silent-zone trade per the May 19 brief
§1 grep-sweep table is ~$2,600 ECR delta (anchor: the original Aegis
2026-05-19 trade that motivated the handoff in the first place); zero
such trades fired in the 9-day window by Poisson coincidence on
infrequently-firing strategies.

**Rule:** When a CC handoff dispatches changes to a gitignored target
(Pine, sealed configs, vendor binaries, etc.), the parent session MUST
verify the deployment via the system that owns the target (TradingView
UI for Pine; vendor-system manifest for sealed configs; binary-checksum
for binaries). CC's own return status (`DONE`) is necessary but NOT
sufficient — `git diff` cannot reproduce changes to gitignored files,
so neither subsequent CC sessions nor the parent session can audit
what was actually done. Post-execution verification must be parent-side,
system-of-record-side, and explicit.

**Mechanism (why this fails):** Gitignored files exist outside git's
audit surface. CC can edit them locally (gitignored ≠ unwritable), but
those edits don't appear in `git status` or `git diff`. The parent
session reads CC's return status as the truth-claim about what
happened; CC's return status reads as `DONE` because CC's perspective
is *"I did the work I was asked to do."* But there is no shared
third-party witness — no commit hash, no diff, no log entry that
survives across sessions. If CC's edits actually happened locally, they
go undetected by git. If CC's edits didn't happen (or were silently
overwritten, or never applied because the dispatched files were
elsewhere), there's no evidence either way. The system that *does*
hold the truth is the one that owns the target — TradingView for Pine,
vendor portal for sealed configs, etc. Parent-side verification against
the system-of-record is the only reliable trust gate.

**Connection to standing doctrine:** Reinforces Rule 0
(production-source verification before assertions) extended to
deployment artifacts: not only must the brief be authored against
verified production source, the post-execution state must be verified
against the system that owns deployment. Distinct from M-11 (M-11 is
about whether the *test* of new behavior catches inherited-gate defects;
M-12 is about whether the *deployment* of new behavior actually
happened). Sibling to M-9 (gitignored-vendor-data manifest gate — same
fundamental problem: gitignored bytes can't be reconciled by git
alone) but distinct domain (M-9 is data; M-12 is deployment).

**Watch-point:** During CC handoff authoring + post-CC return review
for any handoff that touches:

- Pine source (`**/*.pine` per `.gitignore:50`)
- Sealed configs (vendored, encrypted, or otherwise not git-tracked)
- Vendor binaries
- Any target where `git diff` cannot reconstruct CC's claimed work

**Output trigger:** When the watch-point fires, the handoff brief
must include:

1. A `§5 Forbidden moves` entry forbidding CC from editing the
   gitignored target locally
2. A scoped *"diff generation only"* execution mode (CC reads target,
   outputs diffs for parent-side application)
3. A `§7 Parent-side review` item that includes system-of-record
   verification (e.g., TV-side grep for Pine)
4. An audit hook in `§10` that runs against the system-of-record state
   (e.g., post-application grep for the expected change)

The 2026-05-28 re-ship handoff
([`docs/ltm/briefs/handoffs/2026-05-28-cc-handoff-anticipation-gating-reship.md`](../../briefs/handoffs/2026-05-28-cc-handoff-anticipation-gating-reship.md),
commit `c92de94`) is the worked example for all four elements above.

**Promotion criteria:** Promotes from CANDIDATE to PROMOTED on EITHER:

- (a) **Second-occurrence instance** — a new gitignored-target CC
  handoff fails its post-execution verification in a future workstream.
- (b) **≥$3K cost** — a silent-zone trade (or analogous
  deployment-failure-class cost) fires during the latency window between
  a future CC handoff dispatch and its post-execution verification.

The 2026-05-28 incident anchor is single workstream-class (count = 1
instance covering 4 targets); the no-trade outcome was Poisson
coincidence, not the discipline working. Promotion gated on either
next firing of the pattern or a measured cost.

**Forbidden moves:**

- Do NOT treat CC's `DONE` return as sufficient evidence of deployment
  to gitignored targets. CC's perspective is *"I did the work"*; the
  system-of-record's perspective is the only reliable witness.
- Do NOT defer system-of-record verification to *"we'll check next
  time."* The 2026-05-19 → 2026-05-28 window was 9 days of latent
  exposure that surfaced only by accidental Q-PARITY-1 §0 grounding
  work.
- Do NOT bundle CC's local-edit role with diff-generation role for
  gitignored targets. Local edits and diff generation are distinct
  execution modes; mixing them creates the same audit gap CC's
  solo-edit role does.

**Reproducer / worked example:** The 2026-05-28 anticipation-gating
re-ship workstream — handoff at commit `c92de94` (with the four
discipline elements above) + closure at commit `1a1aba1` (CC return
with diffs for parent-side TV application) + Joshua's TV-side
post-application grep + post-patch audit-doc landings
(`d98e727`, `d6ddbb6`, `dda4fd8`) + Q-PARITY-1 §1 retraction at commit
`98a53c8`.

**Sibling lessons:** M-11 (falsifier-scope shadow — same family of
handoff failure but at the design layer, not the deployment layer; the
two together cover the brief→deployment chain).
M-9 (gitignored-vendor-data manifest gate — same fundamental
gitignored-bytes-not-reconcilable-by-git principle, different domain).
M-AHF (audit hooks check storage form not human-readable property —
distinct concern, but reinforces the broader principle that audit
instruments must match the artifact-storage layer; M-12 says the
post-deployment audit must match the deployment-storage layer
specifically).

---

## M-13 — Pine parameter-lock changes must update BOTH the strategy and indicator .pine

**Status:** CANDIDATE 2026-05-28 (single workstream-class anchor: the
2026-05-23 allocation-refresh-2 updated the four strategy `.pine` files but
not their indicator siblings, leaving live alerts on stale 2026-05-14 values
for ~5 days until surfaced 2026-05-28 during the 8-file Pine drop + divergence
audit).

**Anchor incident:** [`docs/adr/2026-05-23-allocation-refresh-2.md`](../../adr/2026-05-23-allocation-refresh-2.md)
re-locked DJ30 pyramid 500→750 and NAS100 risk 0.45→0.37. Those edits landed
in the **strategy** `.pine` (backtest/MC source) — `validate_params.py`,
`params.toml`, and the MC anchors all reflect 750 / 0.37. But the **indicator**
`.pine` (the live signal/alert/lot-sizing source) was never touched: on
2026-05-28 the divergence audit across all 8 dropped Pine files found
`striker_dj30_v4.5_indicator.pine` still at `pyramidSize = 500` (maxval also
capped at 500 — structurally unable to reach 750) and
`striker_nas100_v1_indicator.pine` still at `riskPerTrade = 0.45`. The
strategy files were correct (750 / 0.37); only the live-alert files lagged.
Fixed same session (indicator values → 750 / 0.37, maxval → 1000); manifest
regen commit `53f65da`.

**Cost:** Workstream-class wrong-state count = 1 (two params — DJ30 pyramid +
NAS risk — across two strategies, counted as one workstream failure per the
M-class convention). Latent live-execution exposure for the 5-day window
2026-05-23 → 2026-05-28: live NAS ~22% over-risk (0.45 vs 0.37) and live DJ30
pyramid ~33% under-sized (500 vs 750). Dollar cost unmeasured (depends on
whether NAS/DJ30 fired live in-window); no measured loss isolated, so anchored
on instance count, not dollars.

**Rule:** Every Pine parameter-lock change (allocation refresh, risk / pyramid /
contract-value / day-stop / hour-block edit) must be applied to BOTH the
strategy `.pine` AND the indicator `.pine`, and both must be re-exported to
TradingView. A refresh applied to only one file silently splits backtest from
live. The `params.toml` 5-step same-commit workflow gains a step: "update the
indicator `.pine` alongside the strategy `.pine`."

**Mechanism (why this fails):** Each strategy ships as two Pine files with
duplicated parameter inputs — the strategy (`strategy.*`, the backtest/MC
engine) and the indicator (`indicator()`, the live alert + lot-sizing source).
A refresh that edits only the strategy file leaves the indicator on the prior
values, and that drift evaded the repo gates for two compounding reasons:
(1) `.pine` is gitignored, so the files are absent on CI / public clones — and
were absent from this clone until 2026-05-28; when absent, `validate_params`
emits only a "no Pine present" WARN and checks nothing. (2) Even when the files
ARE present, the pre-2026-05-28 Pine check resolved BOTH the strategy and the
`_indicator.pine` (via `_resolve_pine_targets`) but compared only the **risk**
input — `pyramidSize` was checked on neither file, so the DJ30 indicator
pyramid 500-vs-750 drift had no gate that could catch it. (The NAS indicator
risk 0.45-vs-0.37 drift *would* have been caught by the existing risk check had
the validator run while the indicator was present — but the indicators only
entered this clone on 2026-05-28, after the refresh. So the genuinely
uncoverable case was the pyramid, not the risk.)

**Connection to standing doctrine:** Extends M-12 (gitignored-target
post-execution verification) — M-12 says verify the deployment *happened*;
M-13 says the change-set must include *both files* in the first place. Sibling
to M-7 / M-11 (same dual-file alert infrastructure). Reinforces Rule 0
(production-source-first) and the `params.toml` same-commit workflow. Tooling
fix landed 2026-05-28 (same commit as this correction): `check_pine_opportunistic`
now cross-checks the `pyramidSize` input against the manifest's `pyramid_pct`
on BOTH the strategy and indicator files — risk was already covered on both via
`_resolve_pine_targets`, so no `indicator_path` field was needed (contrary to
this lesson's original draft, which wrongly claimed the validator never
inspected the indicator). `tests/test_validate_params.py` pins the
pyramid-drift-is-HARD invariant.

**Watch-point:** During any allocation-refresh ADR or Pine parameter-lock
change, before declaring it complete: grep BOTH the strategy and indicator
`.pine` for each changed parameter and confirm both updated; then verify both
re-exported to TV per M-12.

**Output trigger:** When the watch-point fires, diff strategy-vs-indicator for
the changed params (`grep -nE '<param> = input' strategies/<s>/<s>.pine
strategies/<s>/<s>_indicator.pine`). If they diverge, the refresh is
incomplete — patch the indicator + re-export. Reference this lesson + cost; do
not re-derive. The `validate_params.py` `pyramidSize`-coverage extension landed
2026-05-28 — a half-applied refresh that leaves either file's `pyramidSize`
stale now HARD-fails the gate WHEN Pine is present locally. Residual structural
gap: the gate is blind when Pine is absent from the clone (gitignored) — that
case is covered by M-12 (deployment verification) + the manifest hash gate.
Not yet covered by the gate: `contractValue` / `maxTradesDay` (future extension).

**Forbidden moves:**
- Do NOT declare an allocation refresh / Pine lock change complete after
  editing only the strategy file.
- Do NOT treat `validate_params.py` 0/0 as evidence the indicators are
  current when Pine is ABSENT from the clone — it emits a "no Pine present"
  WARN and checks nothing. When Pine IS present it now covers risk +
  `pyramidSize` on both files (but still not `contractValue` / `maxTradesDay`).
- Do NOT assume the indicator and strategy agree because they share a
  shorttitle; they have independent `input.float` defaults (see
  `MEMORY.md/feedback_audit_doc_unreliable_for_pine_defaults.md`).

**Reproducer / worked example:** 2026-05-28 divergence audit (this session) —
`grep` across all 8 Pine files showed strategy pyramid 750 / NAS risk 0.37 vs
indicator pyramid 500 / NAS risk 0.45; day-stop strategy −2 vs indicator −1.15
(left as a documented backtest-vs-live split, separate issue). Indicator value
fixes + manifest regen at commit `53f65da`.

**Sibling lessons:** M-12 (deployment-layer verification — M-13 is the
change-set-completeness counterpart), M-7 / M-11 (dual-file alert
infrastructure), M-9 (gitignored bytes not git-reconcilable).

---

## M-14 — Empty strategy-tester ≠ indicator↔strategy divergence; check the Pine backtest `endDate` first

**Status:** CANDIDATE 2026-06-01 ($0 same-session near-miss; phantom-divergence conclusion prevented by a Rule-0 Pine read before a Pre-Q opened).

**Anchor incident:** Weekly execution review 2026-06-01. The Striker DJ30 v4.5 and NAS100 v1 **strategy** backtests returned "This report requires trade data" (zero trades) for May windows that fully covered live fires (DJ30 29 May, NAS100 26 May) — on BOTH Alchemy and OANDA feeds. Cross-feed reproduction ruled out a chart-config artifact, and the working hypothesis escalated to "real indicator↔strategy firing divergence" (live indicators firing trades the locked strategies don't sanction — which would have impugned every live Striker signal plus the MC/baseline edifice). The operator reasonably endorsed hypothesis B. Rule-0 read of the strategy `.pine` found the actual cause: a stale `endDate = input.time(timestamp("2026-04-17"))` (DJ30) / `2026-04-20` (NAS100) gating `longSignal` via `inDateRange`, excluding every post-April bar by construction → zero trades on any feed. Guardian populated because its strategy `endDate` was far-future. Fix: bumped both to `2026-12-31` + Pine-manifest regen.

**Cost:** $0. Wrong-verdict count = 0 (the phantom-divergence conclusion was *prevented* by the Pine read, not incurred). Counterfactual if accepted: ~1+ session opening/closing a phantom Pre-Q on indicator↔strategy firing divergence, plus unwarranted doubt cast on live signal validity.

**Rule:** An empty strategy-tester (zero trades) over a window that should contain trades is NOT evidence of indicator↔strategy divergence until the strategy `.pine` backtest-window inputs are read. Check the `endDate` / `startDate` `input.time` defaults FIRST: a stale `endDate` silently gates out recent bars via `inDateRange`, on every feed. Cross-feed reproduction does NOT distinguish a Pine-internal date gate from a real divergence — both reproduce across feeds identically.

**Mechanism (why this fails):** The strategy `.pine` BACKTEST group defaults `endDate` to the last lock/anchor date and it is rarely bumped. `longSignal` includes `inDateRange = time <= endDate`, so the gate is invisible in the tester UI (the tester's date-range picker is independent of the Pine input). The empty result is surface-indistinguishable from a genuinely non-firing strategy, and reproduces across feeds because the gate is feed-agnostic — making cross-feed reproduction a *false corroborator* of "divergence." The indicator `.pine` has a far-future `endDate` (it runs live), so indicator-fires-but-strategy-empty mimics divergence when it is really a strategy-only date cap.

**Connection to standing doctrine:** Direct application of Rule 0 / "Rule 0 extends to Pine code" (read the actual strategy source before concluding) and `MEMORY.md/feedback_audit_doc_unreliable_for_pine_defaults.md` (strategy vs indicator inputs diverge). Reinforces verify-before-concluding even against an operator-endorsed hypothesis.

**Watch-point:** Any time a strategy-tester returns zero/empty trades for a window where trades are expected — before classifying as divergence, off-spec live signals, or strategy failure. Also during any weekly execution review that pulls strategy-tester counterfactuals.

**Output trigger:** `grep -nE 'endDate\s*=\s*input\.time' strategies/<s>/<s>.pine` — if the default predates the test window, bump it (Settings → Inputs → End Date for a one-off, or the Pine default + manifest regen for a permanent fix) and re-run before drawing any divergence conclusion. Reference this lesson; do not re-derive.

**Forbidden moves:**
- Do NOT escalate "empty strategy-tester" to "indicator↔strategy divergence" without reading the strategy `.pine` `endDate` / `startDate` inputs.
- Do NOT treat cross-feed reproduction of an empty result as evidence of real divergence — a Pine-internal date gate reproduces across all feeds.
- Do NOT accept an operator-endorsed divergence hypothesis as license to skip the Rule-0 Pine read; the read is cheap and decisive.

**Promotion criteria:** CANDIDATE → PROMOTED on second independent firing (a future empty-tester misread, caught or missed) OR a measured ≥$3K cost from acting on a phantom-divergence conclusion.

**Sibling lessons:** M-13 (strategy-vs-indicator `.pine` field drift — same divergence class, different field: `endDate` backtest-window vs risk/pyramid). M-12 (gitignored-target verification). Rule 0 + `feedback_audit_doc_unreliable_for_pine_defaults.md`.

---

## M-15 — A pre-registered offline instrument needs a real-data faithfulness anchor; self-referential tests can't catch a scoring inversion (a.k.a. `M-ICT-1H-OFFSET`)

**Status:** CANDIDATE 2026-06-19 ($0, `lab/`-only research instrument; verdict-flipping defect caught on the first real export, before any wrong verdict was recorded). Promotion gated on a second independent firing (any future offline port-of-Pine — or port-of-any-source — verdict instrument whose self-referential tests pass while it mis-scores the source's event).

**Anchor incident:** Q-ICT-CASCADE-1 Layer-1H verdict run. `harness_1h.recompute_hits` transcribed Pine v6's HISTORICAL offset `series[fwdK]` (= `fwdK` bars **BACK**; DRAFT L81-86: `premHit = zone[fwdK]==1 and close < close[fwdK]`) as a **forward** array index `prem[i] = zone[i+fwdK]==1 and close[i] < close[i+fwdK]`. It therefore conditioned each hit on the FUTURE zone and reversed the price comparison — scoring "price ROSE INTO a premium zone" (the COMPLEMENT of the claim "premium resolves DOWN"). On the first real export (`PEPPERSTONE_US500, 60_a6b6b.csv`, 3039 bars) a backward reconstruction of Pine's formula matched the EXPORTED `premHit`/`discHit` columns **100%**; the harness recompute matched only **~36%**, and its rates were the exact complement of Pine's (1−0.5226=0.4774 vs 0.4725; 1−0.4525=0.5475 vs 0.5430) — the fingerprint of measuring the opposite direction, not noise. The cont.7 20-finding adversarial review ("every finding independently refuted") did NOT catch it.

**Cost:** $0 dollar / 0 wrong-verdict recorded (the buggy first scoring was declared VOID before any verdict landed; the corrected verdict is FALSIFIED). Counterfactual if undetected: a recorded 1H verdict on the COMPLEMENT of the claim — and, because every 1H estimator (main verdict, bias-conditioned, anchor sweep, both transfer axes) routes through `recompute_hits`, a fully inverted layer feeding the cascade's 1M-gate licensing decision. Caught only because the first real export let the look-ahead audit compare recompute against ground-truth Pine output.

**Rule:** A pre-registered OFFLINE instrument that re-ports a source-of-truth computation (Pine indicator, vendor engine, another script) MUST be pinned against a REAL artifact from that source — the exported columns, a hand-computed ground truth, or a captured reference run — NOT only against its own output. Self-referential unit tests (fixtures generated by the instrument under test, asserted by the same instrument) prove internal consistency, never faithfulness; a scoring-direction/offset inversion is invisible to them. Corollary: any look-ahead / faithfulness audit that detects a source-vs-recompute mismatch must **halt or surface as a blocker** — never silently prefer its own recompute over the source of truth.

**Mechanism (why this fails):** Two compounding failures. (1) **Self-referential tests.** `test_recompute_hits_*` built fixtures with the same forward-index convention and asserted it (`test_recompute_hits_prem_down` literally built a rising close and asserted a premium hit) — so a green suite confirmed the instrument agreed with itself. With no real source artifact in the loop until the operator ran TV, there was nothing to contradict the convention. (2) **Backwards audit disposition.** `audit_exported_hits` DID fire `ok=False` (~49% mismatch vs the exported Pine columns), but its disposition was "exported disagrees with recompute → discard exported, trust recompute" — exactly inverted when the recompute is the buggy side. The audit had the ground truth in hand (the exported columns) and threw it away. The defect-generator is the language-mismatch trap: Pine's `[n]` is a historical (backward) offset; a naive 0-indexed Python port reads `[i+n]` as the "same" offset and silently flips the time arrow.

**Connection to standing doctrine:** Extends Rule 0 / "Rule 0 extends to Pine code" (read the actual locked Pine close-out/offset logic; don't infer) to the AUDIT layer — the offline port must be validated against the production source's real output, not its own. Sibling in spirit to M-9 (a gate blind to ground truth — CI that can't see gitignored bytes — gives false assurance; here the false assurance is from self-referential tests). Sibling to M-AHF (audit instruments must match the artifact's real form/layer). Reinforces `strategy-validation` (a green suite ≠ a faithful instrument) and the campaign's own §5 forbidden "reading the table as the verdict." The fix being direction-agnostic (the void run and the corrected run BOTH returned FALSIFIED) is the M-EC-style proof that a post-data fix was not outcome-motivated.

**Watch-point:** Whenever building or reviewing an offline harness that REIMPLEMENTS a source-of-truth computation (Pine detector port, vendor-engine twin, parity reconstruction) — especially any series offset (`[k]`, `shift`, `i±k`), any "[1]-lag", or any premHit/outcome pairing. Also at the moment a real export FIRST arrives for a previously synthetic-only instrument: re-read every offset against the source's indexing convention before trusting the verdict.

**Output trigger:** (a) Add a regression test that pins the port against the REAL source artifact (or a hand-built ground truth encoding the claim direction), asserting the rate is the claim — not its complement (worked example: `test_recompute_hits_scores_event_not_complement`, period=2·fwd mean-reverting fixture → premium→down ≈ 1.0). (b) Make any faithfulness/look-ahead audit a blocker: on `ok=False`, halt/surface, do not auto-prefer the recompute. (c) For Pine ports specifically: write `series[k]` as `arr[i-k]` (BACK), never `arr[i+k]`, and review every offset against `series[n] = n bars back`. Reference this lesson; do not re-derive.

**Forbidden moves:**
- Do NOT validate an offline source-port instrument solely against fixtures it generated — pin it to a real source artifact or hand-computed ground truth.
- Do NOT let a faithfulness audit silently discard the source-of-truth artifact in favor of its own recompute on a mismatch; the mismatch is the signal.
- Do NOT transcribe a Pine `series[fwdK]` historical offset as a forward array index `arr[i+fwdK]`; that flips the time arrow.
- Do NOT treat a "fully reviewed, all-findings-refuted" adversarial pass as faithfulness coverage when the instrument has not yet been run against real source data.

**Reproducer / worked example:** `lab/archive/ict_cascade_2026-06-18/CLOSURE-1H-FALSIFIED.md` (§3) + the PREREG-1H 2026-06-19 amendment (void/fix audit trail). Empirical fingerprint: backward Pine reconstruction 100% vs exported columns, harness ~36%, rates = 1−Pine. Fix commits land on branch `claude/elastic-ride-4e45ed` (`harness_1h.py` `recompute_hits` decision-bar form + `_pine_resolution_hits` resolution-bar audit + `placebo_sign_shuffle` direction; `test_harness_1h.py` re-pinned + `test_recompute_hits_scores_event_not_complement` guard).

**Sibling lessons:** M-9 (ground-truth-blind gate gives false assurance), M-AHF (audit instrument must match the artifact's real form), M-14 (empty-tester divergence misread — same "read the Pine before concluding" family), Rule 0 / `feedback_rule0_pine_code_check`.

---

## M-16 — Realistic entry-fill slip is the cheapest falsifier for a stop-entry edge; run it before any exit/sizing/MC

**Status:** CANDIDATE 2026-06-22 ($0, `lab/`-only US500 discovery; near-miss caught before any recommendation landed). Promotion gated on a second firing — any stop/break-entry candidate whose cost-net edge survives a spread-cost charge but not a ≥1-tick break-bar fill slip.

**Anchor incident:** US500 widest-net discovery (`lab/analysis/legacy/us500_discovery_2026-06-22/`). The lone survivor — a 30-min opening-range breakout (ORB-30) — showed cost-net **+0.058R** after a 1pt round-trip spread charge, all-years-positive, both-sides-positive, within-day placebo p=0.012: a genuinely real structural effect. The cost-law pre-flight (`strategy-validation` §2) computed the round-trip cost-in-R and judged the ~0.07R hurdle clearable — but it modelled the entry as a perfect fill *at* the trigger level. Charging just **+1pt of break-bar slippage** (a generous stop-order assumption on an 18.8pt median range) flipped cost-net expectancy **NEGATIVE (−0.031R)**; the edge crosses zero at **~0.9pt** of slip. The process error: I had already built the first-passage MC and commissioned an exit-policy sweep on this entry *before* running the one-parameter slip test that killed it.

**Rule:** For any candidate entered via a stop / market-on-break order, realistic entry-fill slippage is a **distinct and typically larger tax than spread cost**, and it is the single cheapest falsifier (one parameter). Run a fill-slip sweep — meanR vs entry slip ∈ {0, 0.5, 1, 1.5} ticks — and confirm the cost-net edge survives ≥1 realistic tick **before** building any exit design, sizing frontier, or first-passage MC. Per `strategy-validation` §0 (rank tests by P(changes verdict)÷cost), the slip test sorts to the top: near-zero cost, frequently decisive.

**Mechanism (why this fails):** the cost-law pre-flight charges spread/commission round-trip but treats the entry as a *limit* fill at the signal level. A breakout/stop entry fills on momentum, slightly *through* the level — and for a thin edge the per-trade expectancy (here ~1pt on an 18.8pt range) can be smaller than one tick of that slip. **Spread-cost-clearable ≠ fill-robust.** The seduction: the spread-net result looks tradeable and its stability screens pass, so downstream tooling gets built on an entry that does not survive the order type it requires.

**Forbidden moves:**
- Do NOT build first-passage MC, exit sweeps, or sizing frontiers on a stop-entry candidate before its fill-slip sweep clears ≥1 realistic tick.
- Do NOT treat a spread-only cost charge as the fill model for a stop/break entry.
- Do NOT let stability screens (all-years-positive, both-sides-positive) substitute for the fill-robustness check — they screen for robustness *conditional on the effect being real and fillable*.

**Sibling lessons:** sharpens `strategy-validation` §2 (cost-law pre-flight) and §0 (test-ordering); sibling to the USDCAD/USOIL/fixing-reversal cost-wall closures (there the spread is the binding constraint; here it is fill-slip on a thin edge); Rule 0 (read the order mechanics, don't assume the fill).

**Worked example:** `lab/analysis/legacy/us500_discovery_2026-06-22/RESULTS.md` (ORB fill cliff: meanR `+0.058 → −0.006` at 0→1pt slip); `us500_orb_verdict.png` panel B; `orb_robustness.py` (gapslip run), `plot_frontier.py` (slip sweep).

---

## M-17 — The honest null for a time-of-day-anchored setup is a same-day time-placebo

**Status:** CANDIDATE 2026-06-22 ($0, `lab/`-only). Promotion gated on a second use validating a clock/session-anchored signal.

**Anchor incident:** testing whether the US500 opening-range break carries information specific to the *opening*. Two intuitive nulls were degenerate: **(1) direction-flip** (flip the realized breakout side) tested stop-placement, not direction-information — the anti-break is mechanically catastrophic (−1.06R) so it "rejected" trivially (p≈0.0001); **(2) cross-day rotation** (apply one day's OR levels to another day's path) was degenerate from price-scale mismatch (a 2022 ~4000 level on a 2025 ~5800 path → huge PnL over a tiny range denominator; null mean +74R). The honest null: **slide the range-defining window to a random non-opening time on the SAME day**, then re-run the identical break/stop/exit rule. This holds that day's price scale, volatility, range distribution, and cost fixed, isolating "is the *opening* anchor special." Observed +0.058R sat at placebo **p=0.012** — the opening range is genuinely special vs arbitrary intraday windows (which lose money chopping around stale levels).

**Rule:** To test whether a time-anchored intraday setup (opening range, session open, a fixed clock window) carries *anchor-specific* edge, the null must hold everything about the day constant and vary only the **anchor time** — a same-day window-slide placebo. Cross-day permutations break price scale; direction permutations test the stop geometry, not the anchor. **Name the null and verify it is non-degenerate (sane mean/variance) before reading its p-value.**

**Forbidden moves:**
- Do NOT use a cross-day / cross-instrument rotation as the null for a price-level-anchored intraday setup (scale mismatch makes it degenerate).
- Do NOT use a direction-flip as the null for a stop-based setup (it tests stop placement, not the signal).
- Do NOT report a permutation p before confirming the null distribution is non-degenerate.

**Sibling lessons:** extends `strategy-validation` §5 (selection/permutation) with anchor-specific null construction; sibling to F09's cyclic-rotation-preserves-autocorrelation null and the BPC within-day placebo (`strategy-validation` provenance).

**Worked example:** `lab/analysis/legacy/us500_discovery_2026-06-22/orb_validate.py` (placebo dist mean −0.042R, p95 +0.030R, obs +0.058R → p=0.0123; rejected the two degenerate nulls first).

---

## M-18 — A deadline-capped challenge is a Sharpe race, not a symmetric first-passage; screen on the edge×frequency ceiling and prefer information-ratio exits

**Status:** CANDIDATE 2026-06-22 ($0, `lab/`-only). **Domain:** prop-firm-challenge · strategy-validation · portfolio. Promotion gated on a second use OR application to a live challenge-sizing decision.

**Anchor incident:** US500 discovery, first-passage analysis of the ORB candidate. **(a)** A Sharpe-~0.6, ~1-trade/day edge caps at **~58% challenge pass-rate regardless of risk sizing** — low risk times out before +5%, high risk busts at −5%. That ceiling is computable a-priori from (per-trade edge × frequency) vs the ±5% barrier geometry; no 20k-path MC is needed to see it. **(b)** An exit-policy sweep showed a low-variance, high-information-ratio **give-back-33%-of-open-profit** trailing exit (WR 0.755, std 0.49) **beats** a max-positive-skew lottery exit (breakeven@+0.5R, skew +2.52) for the 120-day-capped FXIFY challenge — the deadline rewards reaching +5% fast with controlled variance, not waiting for a fat right tail.

**Rule:** The FXIFY objective ("reach +5% before −5% within a horizon") is a **Sharpe-race-with-a-deadline**, not a symmetric first-passage where skew dominates. Two consequences: **(1)** screen candidates early on the **analytic pass-ceiling** — a thin single-setup edge (low edge×frequency vs the barrier) has a computable ceiling near coin-flip and is dead-for-the-objective even when the edge is genuinely real; this is *why* "more independent setups per day" beats "a fatter single edge." **(2)** Among exits, prefer the **highest information ratio** (drift/variance) over the highest skew; truncating variance to reach the target faster lowers bust within the horizon. Applies to every leg's challenge-phase sizing, not just new candidates.

**Forbidden moves:**
- Do NOT optimize a challenge exit for maximum positive skew; optimize for information ratio + time-to-target under the horizon cap.
- Do NOT commission a full first-passage MC before computing the analytic edge×frequency-vs-barrier ceiling (it may already disqualify the candidate).
- Do NOT treat a "real, positive-expectancy" edge as challenge-viable without its frequency-scaled pass-ceiling.

**Sibling lessons:** extends `prop-firm-challenge` (challenge MC / first-passage) and the portfolio first-passage framing [[project_decompound_remc_canonical_shift_2026_06_07]]; sibling to the single-setup frequency-starvation note in `ops/instruments/SPX500.md`.

**Worked example:** `lab/analysis/legacy/us500_discovery_2026-06-22/` — `frontier.py` (pass-ceiling ~58%), `orb30_exit_sweep.py` (give-back-33% dominates), `us500_orb_verdict.png` panel A.

---

## M-19 — The DSR selection floor, not the bust/pass gate, is a discovery axis's binding reachability constraint — and it is governed by K, not sample size

**Status:** CANDIDATE 2026-07-14 ($0, docs/`lab`-only). **Domain:** futures-anomaly-discovery · strategy-validation · programme-audit. Promotion gated on a second use OR application to an axis-selection / campaign-K decision.

**Anchor incident:** Q-GATECART-1 survivor-gate cartography. Mapping the frozen prop survivor gate's feasible region, the reachability question was answered *upstream* of the survivor geometry: at the banked GC/MGC **K = 3,177**, the DSR demonstrability floor (min annualized Sharpe clearing DSR ≥ 0.95, V = 1/n) = **2.05** — *above* the best single edge the programme has ever validated (**Aegis 1.83**; all four locked legs 1.11–1.83) and ≈ 2.4× the corrected published top-decile net single-strategy Sharpe (**S_B 0.85**, median single-strategy ~0.3–0.5). The floor is set by **K, not n** (robust across trade-frequency 0.5–4/day; more data does not help). K-sweep from the production `deflated_sharpe`: floor ≤ Aegis needs **K ≤ 441**; ≤ Guardian **K ≤ 33**; ≤ typical-corrected-anomaly (~1.0) **K ≤ 3**. The realistic-and-demonstrable band was therefore empty at the banked K — a FALSIFIED verdict delivered by the realism anchors alone, before the cartography grid ran.

**Rule:** Before committing a discovery axis, compute its **DSR floor at the axis's intrinsic K** and benchmark it against (a) the best in-house validated edge and (b) the corrected published top-decile net single-strategy Sharpe. If the floor exceeds both, the axis is **dead at the DSR admission gate regardless of how forgiving the downstream bust/pass (survivor) geometry is** — the survivor gate is never the binding constraint. Because the floor is K-governed, the lever is **search size**: low-K, mechanism-first axes (a handful of pre-specified hypotheses) can pull the floor below plausible edge quality; high-K blind mining (matrix-profile over thousands of subsequences) cannot. This is an **a-priori screen** (arithmetic on K, n, V), not a campaign you run and see.

**Forbidden moves:**
- Do NOT select a discovery axis on downstream-gate (bust/pass, cost-law) reachability alone; screen the DSR floor at the axis K first — it dominates.
- Do NOT treat the banked campaign K as free; K is the reachability budget, and a larger search raises the floor toward the overfit-suspect zone (SR > 2).
- Do NOT set a *felt* realism ceiling; anchor it to the best in-house edge + corrected literature. Q-GATECART-1 froze the ceiling as a **formula over external data before measuring** — the felt cap SR ≤ 2.0 sat exactly between S_A (1.83) and S_floor (2.05) and would have masked the floor > ceiling inversion.

**Sibling lessons:** the DSR-specific, quantified instance of [[lesson_gate_reachability_preregistration]]; K-is-the-cost sharpens [[lesson_snag_best_of_k_anchor_graveyard]]. The K-lever is the quantitative case *for* the mechanism-first HARV lane (`docs/adr/2026-07-13-harv-discovery-lane-ratification.md`) over blind mining (DISC-CAMP-0, K=3,177, closed FALSIFIED); complements the DSR K/V-rule ADR (`docs/adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md`).

**Worked example:** [`docs/briefs/closures/Q-GATECART-1-survivor-gate-cartography.md`](../../briefs/closures/Q-GATECART-1-survivor-gate-cartography.md) + pre-registration §F (freeze `453148a`); anchors reproduce from `breadth.load_baseline_panel` (S_A) and `research_utils.deflated_sharpe` (S_floor / K-sweep).

---

## M-20 — Reachability must be simulated per-gate, in the gate's own units, at the adjudication panel's price basis

**Status:** CANDIDATE 2026-07-16 (two same-day firings, D5 + H-OD-1; dollar cost ≈ $0 data but two full freeze→GO→register→pull→screen cycles + 2 family-K banked — NQ/MNQ 1, ES 2 — spent on gates arithmetic already decided). Promotion per registry rule on a third firing or a measured ≥$3K instance. **Domain:** futures-anomaly-discovery · brief-authoring (§R attestations) · strategy-validation.

**Anchor incidents (both 2026-07-16):** the first two mechanism-first campaigns after the HARV lane ADR both died at the **Stage-2 cost-law (bp space)** while their §R reachability attestations argued in **annualized-Sharpe space against the Stage-6 confirm floor**. D5: §R attested Stage-6 (gross 1.79 vs floor 0.65) and never simulated Stage-2 — cohort-implied edge ≈2.97bp vs hurdle 11.06bp, unreachable ~3.7×. H-OD-1: §R did simulate Stage-2 but in the wrong basis (recent index ~4400 vs the IS panel median 1942 that Stage-2 actually scores on — ~2.3× the cost fraction) with a ×10 commission mis-scaling ("≤0.03bp" vs actual 0.27bp @4400 / 0.62bp @IS) — corrected, the true world (cohort +1.5bp) passes at **no** commissions-included basis (hurdle 5.05bp IS / 2.23bp @4400). H-OD-1's mechanism meanwhile CONFIRMED in-sample (+1.444bp, t≈5.0, 9/9 years positive) — the gate, not the transfer premise, was the failure. HARV lane ADR §4 falsifier FIRED (both conjuncts, twice); amending ADR `Proposed` ([`2026-07-16-harv-attestation-same-units-supersession.md`](../../adr/2026-07-16-harv-attestation-same-units-supersession.md)).

**Rule:** a §R attestation discharges a gate only when simulated **in that gate's own units** (a Sharpe-space argument does not discharge a bp-space cost gate), **at the basis the gate is scored on** (IS panel for Stage-2, OOS for Stage-6 — never a present-day or convenience basis), **with commissions divided out explicitly** (never waived as "negligible" without showing the division). For cost-law clauses the mandatory inequality is [`docs/methodology/strategy_harvest.md`](../strategy_harvest.md) §1 Requirement 5's — **derived mirror, not restated here**; that section is the sole authority for its exact form. Run it at admission too — seeds whose event-scale cannot clear it die for the cost of one division (both anchor campaigns would have).

**Forbidden moves:**
- Do NOT attest "REACHABLE" from the confirm-floor argument alone when the campaign carries an upstream cost/kill gate — every gate the campaign can die at gets its own same-units simulation.
- Do NOT price reachability at current market levels when the gate adjudicates on a historical panel; the tick-to-notional ratio is era-dependent (~2–3× across 2010–2026 index levels).
- Do NOT hand-wave commissions into a rounding error — the two firings show commission ≈ the slip itself under passive models, and a ×10 scaling slip survived a frozen, GO-signed pre-reg.

**Sibling lessons:** per-gate/bp-space instance of [[lesson_gate_reachability_preregistration]] (Q-HARV-0 placebo-geometry scar → generalized beyond placebo clauses to cost clauses); complements M-19 (DSR floor screens the *selection* gate a-priori; M-20 screens the *cost* gate a-priori — together they make "which gates can a true world actually pass?" a pure Stage-0 arithmetic question).

**Worked example:** [`lab/analysis/harvest/h_od_1_es_overnight_drift_2026-07/RESULTS.md`](../../../lab/analysis/harvest/h_od_1_es_overnight_drift_2026-07/RESULTS.md) (reachability recompute table + D5 recount; reproduce commands inline).

---

## M-21 — Against a dollar-trailing drawdown barrier, correlation breadth (dependence N_eff) is not admissibility; risk breadth (covariance N_eff) is — and the daily-$-std ratio is the cheapest falsifier

**Status:** CANDIDATE 2026-07-17 (single composed-candidate firing — ORB-MNQ-1; $0 realized, near-miss caught by the downstream frozen engine, not by the breadth gate meant to catch it). Promotion gated on the next composed-candidate evaluation carrying both a breadth verdict and a frozen-engine bust verdict (the schedule the codifying ADR §4 already binds). **Domain:** strategy-validation · futures-anomaly-discovery · portfolio · prop-portfolio.

**Anchor incident:** Q-COMPOSE-1 closure ([`docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md`](../../briefs/closures/Q-COMPOSE-1-closure-falsified.md), commit `4de8085`). The discovery factory's only admitted survivor, ORB-MNQ-1, was admitted to lifecycle CANDIDATE on a flattering breadth read — Stage-8 dependence **N_eff 1.9948 → 2.9502** (+0.96, "near-independent diversifier"), realized weekly corr with the same-instrument MNQ-Striker leg only +0.15. Composing it at that admitted **0.37%** weight into the live 2-leg MYM+MNQ book detonated the composed bust to **38.75%** (Tradeify full) — **67.63%** (BluSky H1) versus a ~**2.65%** 2-leg baseline, 15–23× over the 3.0% ceiling, `FALSIFIED` on every firm tier via both limbs. The killer was not the anticipated regime-common-mode contest but plain **variance dominance**: ORB's daily-$std at the $100K basis (**$438**) exceeds the *entire* 2-leg book's (**$273**); the composed series runs ~$539/day against an unchanged $3,000 trailing barrier. The signal was already in the Stage-8 tool's own output — **risk N_eff 1.96 → 1.96 (flat, +0.00)** while dependence N_eff rose — but only the dependence/ENB figure was decision-binding, so the risk-space read never gated. Codified into a Stage-8 gate by ADR [`2026-07-20-stage8-variance-dominance-risk-neff-gate.md`](../../adr/2026-07-20-stage8-variance-dominance-risk-neff-gate.md) (`Proposed`).

**Cost:** $0 realized (the frozen-engine MC caught the composition before any live weight). The load-bearing measure is a **wrong-characterization the breadth gate licensed:** ORB was carried as a diversifier its already-computed `n_eff_risk_delta ≈ +0.00` showed it is not, spending a signed compose pre-registration + a 1.5 h frozen-engine run to reach a reject the risk-space statistic implied in seconds. Counterfactual if the engine had not been the backstop: a composed book at **38.75% bust on a $100K eval** — a near-certain account/eval loss the breadth gate existed to prevent.

**Rule:** When admitting a candidate as a leg of a book adjudicated by a **dollar-denominated trailing drawdown barrier**, admissibility is a **risk-space** property: require the candidate to lift **risk N_eff** (`participation_ratio` of the weekly *covariance* matrix — `n_eff_risk_delta > 0`), never merely dependence N_eff (PR of the *correlation* matrix). A positive dependence-delta / high ENB is necessary context, **never** the admission grant. Screen the cheapest falsifier first: `ρ = candidate daily-$std / existing-book daily-$std` at the intended weight and the adjudication panel's $-basis, computable in seconds at panel-build; `ρ ≥ 1.0` is a presumptive reject that does not proceed to the expensive engine on that weight.

**Mechanism (why this fails):** a trailing dollar barrier is owned by the **dominant-variance** leg, and `PR(corr)` is scale-invariant — it is blind to whose dollar variance owns the tail. So correlation breadth can rise to near-max (dependence N_eff +0.96, +0.955 of a possible +1.0) while `PR(cov)` stays flat, because the added leg's covariance contribution is dominated by its own outsized variance rather than shared with the book. The seduction: N_eff-up reads like a free risk reduction and a −0.10/+0.15 correlation reads like independence, so the diversification statistic *licenses* the composition — but the barrier feels dollars, not correlations, and a leg carrying more $-variance than the whole book collapses bust geometry on **every** partition, including the trend half the book otherwise passes. **Correlation breadth without risk-weight balance is anti-help against a $-trailing barrier, not neutral.**

**Connection to standing doctrine:** codified by ADR [`2026-07-20-stage8-variance-dominance-risk-neff-gate.md`](../../adr/2026-07-20-stage8-variance-dominance-risk-neff-gate.md); consumes the already-shipped `lab/research_utils/breadth.py` `n_eff_risk_delta` (commit `d83e0f9`). Extends the decompound-HOLD "no static counterbalance" finding from a *sizing* lever to a *breadth* lever (Q-COMPOSE-1's first non-sizing extension). Respects `docs/methodology/strategy_lifecycle.md`'s admission-≠-composition split — a leg can stay a standalone CANDIDATE @1.00× (ORB does) while failing book composition.

**Watch-point:** during Stage-8 breadth admission of any candidate proposed as a **prop-book leg**, and during the compose pre-registration §7/§9 where `ρ` and the `τ_risk` floor are bound (before any frozen-engine run).

**Output trigger:** compute `n_eff_risk_delta` and `ρ` first; if `n_eff_risk_delta ≤ 0` or `ρ ≥ 1.0`, reject as a book leg (the candidate may retain standalone CANDIDATE standing) and do **not** run the frozen engine on that weight. Cite M-21 by name + the $438-vs-$273 anchor; do not re-derive.

**Forbidden moves:**
- Do NOT treat a positive `n_eff_dependence_delta` / low pairwise correlation as sufficient for a composed book-leg add — the exact error that admitted ORB.
- Do NOT iterate a *failed* composed candidate's weight to squeak it past the screen or the engine (Q-COMPOSE-1 §5: a failed composed candidate closes; it does not iterate weight — p-hacking the composition).
- Do NOT read `ρ` or `τ_risk` only after seeing MC output; both are bound a-priori in the compose pre-registration (Trap #12).

**Sibling lessons:** the composition/portfolio-tail analogue of [[M-16]] (realistic-fill slip is the cheapest single-parameter falsifier — here the daily-$std ratio is that seconds-cost falsifier for composition); joins [[M-19]] (DSR selection-gate reachability, a-priori) and [[M-20]] (cost-gate reachability, a-priori) as the third "answer the gate with Stage-0 arithmetic before spending the expensive run" screen — M-21 answers the *portfolio-composition bust* gate; sibling to `lesson_market_neutral_not_regime_neutral` (correlation-space ≠ the operative risk space).

**Worked example:** [`docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md`](../../briefs/closures/Q-COMPOSE-1-closure-falsified.md) (anchor table: 2-leg vs composed-3-leg bust per tier/partition; §"breadth decomposition" for the N_eff split); [`lab/analysis/orb/orb_mnq_2026-07/ADMISSION.md`](../../../lab/analysis/orb/orb_mnq_2026-07/ADMISSION.md) caveat 3 (the pre-composition read); reproduce N_eff from `lab/research_utils/breadth.py` (`n_eff_dependence` / `n_eff_risk` / their deltas).

---

## M-22 — Freshness/integrity gates over gitignored-generated content must presence-degrade the disk-derived field (WARN, exit 0), not hard-fail, on a bare worktree / clone

**Status:** PROMOTED 2026-07-24 (three-surface structural recurrence per promotion criterion (b); load-bearing cost = the `archive_lab_analysis` regression below, which hard-failed **every** commit from any worktree/clone lacking the gitignored heavy files). **Domain:** governance-tooling · pre-commit gates · public-clone / worktree posture.

**Anchor incident:** `scripts/archive_lab_analysis.py --check --catalog-only` — the always-on `lab/CATALOG.md` freshness gate ([`scripts/githooks/pre-commit`](../../../scripts/githooks/pre-commit) line 60) — hard-failed with `CATALOG.md stale vs scan` on the `competent-euler-52ef3a` worktree, and on any clone lacking `lab/analysis/*/inputs/` + `*.pkl`. Root cause: `_heavy_note()` derived the CATALOG `heavy` column from **disk presence** of gitignored artifacts (`inputs/` dir, `*.pkl`), while `check_catalog_stale()` did a whole-catalog byte-diff. A worktree never materializes the gitignored bytes, so the fresh scan downgraded `heavy` (`inputs gitignored` / `pkl gitignored` → `—`), the diff differed, and the gate blocked every commit. The printed auto-fix hint (`--regenerate-catalog`) would have "fixed" it by stripping the correct annotations — **corrupting** CATALOG for the primary tree. Fixed 2026-07-24 by a per-row presence-aware compare (`_compare_catalog`) that tolerates a heavy downgrade only when committed ∈ {annotations} AND the scan sees `—`, warns per tolerated row, and still hard-fails all real drift.

**Cost:** Audit-instance / blast-radius (tooling gate, no dollars). The regression blocked **every** commit from any worktree or clone missing the gitignored heavy files — worktrees are used routinely in this repo, so the failure is *total* for the affected tree — and its remediation hint actively corrupts the canonical catalog. Three-surface recurrence is the generality evidence; only the third surface was an actual regression — the first two were solved at authoring time, which is precisely why this reads as a standing design requirement rather than a one-off (registry precedent: M-AHF counts handled/absorbed instances toward promotion):

| Date | Gate | Disk-presence-derived field | Handling |
|---|---|---|---|
| 2026-05-10/13 | `check_data_manifests.py` | vendor CSV bytes vs `SHA256SUMS` | soft-degrade by design (empty-manifest tolerance; conditional invocation; CI is format-only) — [[M-9]] |
| 2026-07-17 | `check_pine_manifest.py` | `*.pine` presence vs MANIFEST / PORT_MANIFEST | explicit presence gate (nothing resolved AND none on disk ⇒ WARN, exit 0; any present ⇒ full verify) |
| 2026-07-24 | `archive_lab_analysis.py --check` | CATALOG `heavy` column | **MISSED** ⇒ hard-failed every commit ⇒ fixed (this anchor) |

**Rule:** Any always-on freshness/integrity gate over generated or manifest-tracked content must, at authoring time, audit whether **any field it compares derives from disk-presence of a gitignored artifact**. If one does, that field must **presence-degrade** — WARN and exit 0 (never hard-fail) when the artifact is gitignored-and-absent from this checkout — while every non-disk-derived field, and real drift in the disk-derived field when the artifact IS present, still hard-fails. Absence of never-checked-out bytes is not drift.

**Mechanism (why this fails):** A git worktree / fresh clone / public clone shares the object DB but does not materialize gitignored files. A gate that derives a compared field from `.is_dir()` / `.glob()` / `.exists()` on those paths silently produces a *different* value than the committed artifact (generated on the primary tree, where the bytes exist). A whole-artifact exact compare then reports drift for a difference the environment cannot avoid. Because the gate is always-on in pre-commit, the false positive is **total** for that tree — it blocks unrelated commits — and the naive "regenerate" remediation propagates the environment-specific downgrade back into the canonical artifact. The failure is invisible on the primary tree (all bytes present ⇒ gate passes), so it ships and only bites on the first bare worktree/clone.

**Connection to standing doctrine:** Same gitignored-bytes-outside-git's-audit-surface family as [[M-9]] (gitignored vendor-data needs a *local* hash gate because CI can't hash absent bytes) and [[M-12]] (gitignored-target deployment can't be reconciled by git) — M-22 is the corollary that governs how a *gate* must behave when it meets those absent bytes. Reinforces the CLAUDE.md public-clone posture ("Vendor-data integrity gate" / "Parameter manifest gate" both already document the soft-degrade) and Rule 0 (the fix required reading the actual `_heavy_note` / `check_catalog_stale` source, not the docstring).

**Watch-point:** During authoring or review of any new (or newly-always-on) `scripts/check_*.py` / pre-commit gate, and during its design spec under `docs/superpowers/specs/`. The decisive question: *"Does any compared field come from disk-presence of a gitignored path? If yes, does the gate WARN-and-pass when that path is absent, while still hard-failing everything else?"*

**Output trigger:** When the watch-point fires, require the gate to ship with a **bare-worktree / absent-gitignored-bytes test case** asserting `exit 0` (+ a WARN) for the disk-derived-field-absent scenario, plus tests that real drift still hard-fails. The `tests/test_archive_lab_analysis.py` pair `test_catalog_only_tolerates_absent_gitignored_heavy` + `test_catalog_only_still_fails_on_real_drift_with_heavy_absent` (+ the one-directional `..._fails_when_heavy_present_but_uncommitted`) is the template. Cite M-22 by name + the "every commit blocked" cost; do not re-derive.

**Recommendation on a mechanical pre-flight (2026-07-24):** Do **not** add a standalone mechanical CI/pre-commit detector for this. Deciding "does a compared field derive from gitignored-and-absent disk state" is a **semantic** property of a gate's comparison logic, not a syntactic one — a grep for `.is_dir()` / `.glob()` + `exit(1)` is heavily false-positive-prone (most such calls are legitimate), and a new always-on meta-gate policing the other gates is exactly the "belt only grows" degeneration the programme-audit warns against. The right-sized, genuinely cheap enforcement is the **test-authoring convention** in Output trigger (every disk-reading always-on gate carries a bare-worktree test), enforced at gate authoring/review via this Watch-point. That is the canonical enforcement point; it needs no new runtime code.

**Forbidden moves:**
- Do NOT run `--regenerate` / `--regenerate-catalog` (or any "just re-sync the manifest") to clear an integrity-gate failure on a worktree/clone lacking the gitignored bytes — it strips the correct annotations and corrupts the canonical artifact for the primary tree.
- Do NOT `git commit --no-verify` past such a false positive; fix the gate to presence-degrade instead (the defect is the gate's, not the commit's).
- Do NOT conclude a gate is worktree-safe because it passes on the primary tree — the false positive is invisible where all gitignored bytes are present; test the absent-bytes case explicitly.

**Reproducer / worked example:** On a worktree lacking `lab/analysis/*/inputs/` + `*.pkl`: pre-fix `python scripts/archive_lab_analysis.py --check --catalog-only; echo $?` → `CATALOG.md stale vs scan` / `1`; post-fix → six `WARN lab/CATALOG heavy-column unverified: …` lines + `lab/CATALOG check: OK` / `0`. Structured diff pre-fix = 12 lines / 6 rows / `heavy`-column-only. Design + test plan: [`docs/superpowers/specs/2026-07-24-lab-catalog-check-heavy-column-worktree-tolerance-design.md`](../../superpowers/specs/2026-07-24-lab-catalog-check-heavy-column-worktree-tolerance-design.md).

**Sibling lessons:** [[M-9]] (gitignored-vendor-data local hash gate), [[M-12]] (gitignored-target deployment verification), [[M-13]] — the informative contrast: `validate_params` is a gate too *lax* when Pine is absent (WARNs, checks nothing → risks a false negative), whereas M-22 is a gate too *strict* when bytes are absent (hard-fails → a false positive); the unifying rule is presence-degrade the disk-derived field to WARN-and-pass, never silently pass everything and never hard-fail.

---

## M-AHF — Audit hooks check storage form, not human-readable property

**Status:** PROMOTED 2026-05-10 (third instance auto-graduation per registry rule *"auto-graduates on third instance regardless of dollar cost"*)
**Domain:** brief-authoring · ADR authoring · methodology audit
**Sibling lessons:** M-EC (Execution Commit) · Rule 0 (audit-first) · Rule 0-T (test-call-graph)

### Pattern

Mechanical audit hooks (grep regexes, count assertions, presence checks) are repeatedly authored against the **author's mental form** of the value being inspected, rather than against the **storage form** in the artifact under audit. The hook tests *"is this string present in the form I'm thinking of"* when it should test *"is this property held in whichever form the artifact uses."*

Mental form ≠ storage form. The hook author imagines the value as it reads in conversation or specification; the artifact stores it in whichever form the storage convention dictates. When the two diverge, the hook silently passes or fails on the wrong property.

### Anchors (four instances: three 2026-05-10, one 2026-07-06)

| # | Round | Hook intent | Author's mental form | Storage form | Failure mode |
|---|---|---|---|---|---|
| 1 | GH #55 ratification, round 1 (commit `50664cd` predecessor) | Verify ADR content stability across commits | *"Commit hasn't been amended"* | File contents at commit ref | Commit metadata used as proxy for content; missed actual content drift |
| 2 | GH #55 ratification, round 2 (commit `50664cd`) | Verify MC anchor pins in test file | `98.09% / 0.36% / 4.73%` (percent form) | `0.9809 / 0.0036 / 0.0473` (decimal form) | Hook matched zero pins; required round-trip correction |
| 3 | PR #73 hook 4 (CC handoff for feed-equivalence-brief-commit) | Verify trashed Notion page ID doesn't leak outside §Lock metadata | `notion.so/358dc0b53c11818085d0cc36692e0185` (URL form) | `358dc0b53c11818085d0cc36692e0185` (bare page ID) | CC correctly used bare-ID grep to verify the property; surfaced hook over-scoping as a defect rather than a content failure |
| 4 | Q-MECH-1 review, 2026-07-06 (`docs/ltm/briefs/Q-MECH-1_identify_notice_question.md` §H hooks 1–3) | Verify (a) exactly 4 Pre-Q gate blocks, (b) no causal language after Notices, (c) no hypothesis leakage | *"Grep the file, get the count/emptiness I saw pre-commit"* | The §H "audit hooks — outputs" block quotes the hook commands verbatim inside the same file it audits | Once committed, re-running hooks 1–3 self-matches on the quoted command text (`"Pre-Q gate:"`, `"because"` inside the causal-language pattern, `"hypothesis:"` inside the leak pattern) — claimed 4/empty/empty reproduces as 5/non-empty/non-empty. Hook 4 unaffected (its pattern text doesn't self-match). Substance underneath was independently re-verified clean by eye; only the hooks' post-commit re-runnability broke. |

Instance 3 differs from 1 and 2 in cost: CC's autonomy absorbed the form-fidelity gap by interpreting the hook's *intent* (property: page ID does not leak) rather than its *expression* (form: URL string present). No round-trip, no dollar cost. The pattern still fired — CC's report flagged the discrepancy explicitly as a handoff-authoring defect.

Instance 4 is a distinct sub-shape worth naming: the storage form didn't drift because of an *encoding* choice (percent vs decimal, URL vs bare ID) — it drifted because **the hook's own output became part of the artifact it audits**. Any audit-hook block that echoes "`$ <command>` / `<expected output>`" verbatim into the same file, committed, changes that file's own grep-able content. The counter-measure below (property assertions, form-agnostic scoping) already covers this if applied at authoring time; the new failure mode is specifically "hooks must be designed assuming their own committed output text will be back in-corpus on the next re-run," which the original three anchors didn't surface.

### Counter-measure

When authoring an audit hook, before committing the regex or assertion:

1. **State the property in plain language**, not as a grep expression. *"Page ID does not leak outside §Lock metadata"* is the property. `grep 'notion.so/358dc0b...'` is one mechanization. Many other mechanizations exist; pick whichever covers the property.
2. **`cat` the target file** (or echo its expected content) and confirm the regex matches the literal storage form. If the property could be held in alternate forms (URL vs bare ID; percent vs decimal; commit metadata vs file content), cover all forms or restate the property to make form irrelevant.
3. **Prefer property assertions over form matches** when storage form is variable or under author control. Example: instead of `grep 'notion.so/PAGE_ID' <file>`, use a form-agnostic ID match scoped to the section that should/shouldn't contain it:
   ```bash
   # Property: bare page ID appears exactly once, inside §Lock metadata
   awk '/^## §Lock metadata/,/^## /' <file> | grep -c '358dc0b53c11818085d0cc36692e0185'  # expect 1
   grep -c '358dc0b53c11818085d0cc36692e0185' <file>                                       # expect 1 (total)
   ```
   Two assertions, one property, form-irrelevant.

### Promotion provenance

- **Round 1** (GH #55, 2026-05-10): single instance, candidate registry, log-entry status.
- **Round 2** (GH #55, 2026-05-10): second instance same day, sharper two-layer formulation, log-entry status. Pre-registered rule: *"third instance auto-graduates regardless of dollar cost."*
- **Round 3** (PR #73, 2026-05-10): third instance. CC correctly interpreted intent, surfaced over-scoping. Auto-promotion triggered per the pre-registered rule.

The rule is what fired the promotion, not a fresh judgement. If the rule hadn't existed, instance 3 would have stayed log-entry status because CC absorbed the cost — and the lesson would have been understated. Pre-registration is what made the third instance count.

### Related candidates (not promoted)

- **Count-expectation pinned at authoring time before final artifact existed.** PR #73 hook 3 (`prop_firm_pipeline` count expected 1, brief retained 2 — second retention is operationally legitimate). First instance. Stays log-entry status; re-check on next instance.

### Cross-reference

- **Rule 0** (audit-first) reads production state before authoring decisions. M-AHF extends Rule 0 to authoring time of the audit hooks themselves.
- **Rule 0-T** (test-call-graph) verifies that a test reaches the changed path. M-AHF is the sibling for audit hooks: verifies that a hook matches the stored form. Both attack indirection; Rule 0 against doc indirection, Rule 0-T against test-coverage indirection, M-AHF against form-mismatch indirection.
- **M-EC** (Execution Commit) is the *result* discipline — forward-binding the lock to a live signal. M-AHF is the *audit-mechanization* discipline — forward-binding the hook to the storage form. Both belong to the brief-authoring discipline-checks bundle.

---

## F-1 — TradingView <30-day JPY P&L inflation (~153× at USDJPY ~150)

**Status:** CANDIDATE 2026-05-16 (retroactive seed; defect predates F-class infrastructure)
**Domain:** brief-evidence integrity · analysis-script output validation
**Sibling lessons:** M-AHF (audit hooks check storage form) · Rule 0 (audit-first) · code-defect-debugging skill (canonical anchor)

### Pattern

TradingView reports JPY-quoted instrument P&L in raw JPY (not USD) on holds
strictly under 30 calendar days, while reporting USD on longer holds. The
short-horizon JPY figure looks like a plausible USD value at first read but
is inflated by the quote rate (~153× at USDJPY ~150). Any brief that cited
TV-reported P&L on a sub-30-day USDJPY trade as USD evidence would silently
overstate by two orders of magnitude.

### Anchor incident

- **Investigation:** Q-MT5-TV equivalence.
- **Defect surface:** TV display layer; JPY→USD conversion omitted on
  short-horizon JPY-quoted holds.
- **Discovery path:** noticed manually during equivalence cross-check; not
  caught by any fixture suite (none existed at the time).
- **Canonical fix:** `tv_mt5_pnl_reconciliation.py` (commit `8e2a2d6`,
  2026-05-16) encodes the independent USD formula and a `compute_pnl_tv_buggy`
  regression helper that reproduces the defect. Fixture suite at
  `tests/test_tv_mt5_pnl_reconciliation.py` pins the canonical, inverse, and
  30-day boundary cases against independently derived expected values.

### Cost

**Audit-instance count: 1** (retroactive seed). The Q-MT5-TV equivalence work
was diagnostic rather than P&L-acting, so the counterfactual is
re-investigation cost (~1 session) rather than direct dollar loss. The lesson
seeds the registry; future fixture-caught defects accumulate alongside.

### Rule

Before citing an analysis-script output as brief evidence, confirm the script
has a fixture test under `tests/` pinning its anchor invariant against an
independently derived expected value, and that `pytest tests/` returns green.
(The covering test need not be named `test_<basename>.py` — the repo's
convention is topical, e.g. `portfolio_mc.py` → `tests/core/test_mc_anchors.py`.)

### Mechanism (why this fails)

Order-of-magnitude defects in numeric output escape eyeballing when the
incorrect magnitude is *plausible at first glance*. The TV JPY figure on a
sub-30-day USDJPY hold reads as a reasonable percentage; only the
side-by-side comparison against an independently derived USD value reveals
the ~153× inflation. Fixture tests with expected values derived by hand (not
by the same code path) catch this class because the comparison is between
two independent derivations, not a self-check.

### Connection to standing doctrine

- `docs/adr/2026-05-16-fixture-test-requirement.md` — codifying ADR;
  extends Rule 0 from "production code read" to "production code read AND
  fixture-tested where output is load-bearing."
- `docs/rule_0.md` — canonical Rule 0 text being extended.
- `code-defect-debugging` skill — canonical JPY 153× anchor (TV <30-day JPY
  ~153× P&L inflation) lives in the skill's defect catalogue.

### Watch-point

During §0 of brief authoring, when listing an analysis script as a production
read. The check fires at the brief-authoring time, not at script-edit time.

### Output trigger

If a cited load-bearing evidence script lacks an anchor-invariant fixture test
under `tests/` OR its suite is red, block brief authoring until the test lands
and `pytest tests/` is green. This is a human check at §0-authoring time backed
by the always-on `pytest tests/` suite. The ADR's former mechanical Hook 1
(`scripts/check_brief_evidence_coverage.py`) was **retired 2026-06-08** — see
`docs/adr/2026-05-16-fixture-test-requirement.md` Amendment — because its
`tests/test_<basename>.py` basename heuristic did not match the repo's
test-naming convention and it was all-false-positive.

### Promotion criteria for F-class

Same shape as M-class:
- (a) single instance with dollar cost ≥ $3,000 OR
- (b) three separate fixture-caught defects across the registry.

F-1 stays CANDIDATE as a retroactive seed; PROMOTION fires on the second
genuinely fixture-caught defect (i.e. one where the fixture suite, not
manual inspection, surfaced the defect first).

---

## M-SWAP-1 — Risk-normalized MC absorbs additive-cost shocks via implied_1r recalibration

**Status:** PROMOTED 2026-05-26 (dollar-cost anchor + **wrong-verdict anchor** — Q-SWAP-2 closed AMBIGUOUS-HOLD 2026-05-26, calibration mode shifted the verdict band)
**Domain:** portfolio MC · lock-decision authoring · additive-cost-shock impact assessment
**Sibling lessons:** Rule 0 (audit-first) · regime-robustness gate · M-AHF (mechanism: instrument tests a different property than the author thinks)

### Pattern

Risk-normalized MC pipelines that compute per-strategy `implied_1r` from the CSV's own losses absorb additive-cost shocks (swap, slippage, commission inflation, broker-fee changes) into scale-factor recalibration. Mechanism: any cost that grows per-trade losses also grows the median (or full-stop-mean) loss → `implied_1r` increases → `scale_factor = target_risk / implied_1r` shrinks → MC simulates a smaller-per-trade strategy with the same fixed-target dollar risk. Verdict gates (bust rate, p99 DD) read as approximately-unchanged because the per-trade dollar magnitude is normalized.

This is correct **only if live execution also adapts position sizing to the cost shock**. For Pine strategies sized by ATR (not by median loss), live sizing does NOT adapt — swap is purely additive on top of ATR-sized P&L. The MC's verdict therefore underrepresents live cost impact.

### Anchor incident

- **Investigation:** Q-SWAP-1 (`docs/ltm/briefs/Q-SWAP-1-portfolio-swap-impact.md`), CLOSED-FALSIFIED 2026-05-25.
- **Closure:** [`docs/ltm/briefs/Q-SWAP-1-closure-falsified.md`](../../briefs/Q-SWAP-1-closure-falsified.md) §"Methodology finding".
- **Defect surface:** `portfolio_mc.py` `implied_1r` + `build_daily_panel` pipeline.
- **Discovery path:** Phase 3 swap-aware MC (commit `aafdd23`) returned 99.84/0.16/4.38 (Δ ≤ 0.01pp on all verdict gates) despite Phase 1 cheap-falsifier showing Guardian Net -10.34%, DD +2.29pp at the trade-distribution level. The mismatch was traced to Guardian's `implied_1r` recalibrating $1,208 → $1,359 (+12.5%) when swap was applied, shrinking the scale factor 0.563 → 0.500 (-11.2%). Bust attribution shifted (Guardian 41.2% → 31.9%, striker 19.6% → 27.7%) but aggregate moved within MC sampling noise.

### Cost

**Dollar cost: $59,153 hidden per panel-year-equivalent** (Guardian-only swap exposure across the canonical 2026-05-24 Pepperstone panel; -10.34% of raw Net, -3.81% at portfolio Σ level). MC pipeline reported Δbust 0.01pp and Δp99 DD 0.01pp — implying "swap is immaterial." Reality: swap costs ~$59K of unmodeled live exposure across the panel — material to live P&L even if not to the MC verdict under adaptive-1R modeling.

This is **counterfactual cost** (failure hides the cost from the verdict; whether it would FLIP the verdict is outstanding). Q-SWAP-2 (`docs/ltm/briefs/Q-SWAP-2-fixed-1r-swap-impact.md`, authored 2026-05-26) is the sister Pre-Q that tests whether fixed-1R MC produces a verdict flip. If Q-SWAP-2 RESOLVES with lock-criteria-fail, that's the verdict-flip evidence and this lesson upgrades from dollar-anchor to wrong-verdict anchor.

### Wrong-verdict anchor (added 2026-05-26 — Q-SWAP-2 closure)

Q-SWAP-2 ran the same question (swap impact on portfolio MC) under fixed-1R modeling and produced **AMBIGUOUS-HOLD** where adaptive-1R produced FALSIFIED:

| Calibration mode | Δbust | Δp99 DD | Verdict |
|---|---:|---:|---|
| Adaptive-1R (Q-SWAP-1) | 0.01pp | 0.01pp | FALSIFIED |
| Fixed-1R (Q-SWAP-2) | 0.03pp | 0.18pp | AMBIGUOUS-HOLD |

Adaptive-1R's absorption is not just a magnitude understatement — it shifts the verdict band. Going forward, additive-cost-shock questions (swap, slippage, commission inflation, broker fee changes) must run BOTH calibration modes and the more conservative verdict is canonical. The 2026-05-23 ADR lock claim "criteria clear with margin" is provisionally retracted on the p99 DD gate under fixed-1R modeling pending Q-SWAP-3 resolution (Q-SWAP-3 = allocation re-evaluation under fixed-1R swap-aware MC; spawned 2026-05-26).

Closure: [`docs/ltm/briefs/Q-SWAP-2-closure-ambiguous.md`](../../briefs/Q-SWAP-2-closure-ambiguous.md).

### Rule

When a Pre-Q tests the lock-decision impact of an additive cost shock (swap, slippage, commission, fee changes), verify whether `implied_1r` shifts materially under the shock. If it does, the adaptive-normalization MC will absorb the shock; the literal MC verdict will underreport live impact. **Use a fixed `implied_1r` reference (pre-shock baseline) to propagate the cost through verdict gates faithfully.**

### Mechanism (why this fails)

`implied_1r` in `portfolio_mc.build_daily_panel` derives the per-strategy 1R from the CSV's own loss distribution. This is correct for *signal calibration* — converting CSV trades into fixed-target-risk simulation — but it confounds *signal calibration* with *cost-shock measurement*. When CSV trades change (e.g., swap subtracts ~$57.49/lot/night), the calibration constant changes too, masking the cost as a position-size reduction.

Live Pine `calcSize` uses ATR-based sizing, not median-loss-based. Live position sizes do not shrink when swap is applied; swap is purely additive cost. The MC's adaptive normalization is therefore an idealization that diverges from live execution under cost-shock conditions.

### Connection to standing doctrine

- **Rule 0** (audit-first) — reads production state. M-SWAP-1 extends Rule 0 from "read production source" to "verify the MC pipeline's calibration assumptions match live execution under the question being asked."
- **regime-robustness gate** — validates lock decisions across regime splits. M-SWAP-1 is parallel: validates lock decisions across calibration-mode (adaptive vs fixed-1R) when the question is cost-shock impact.
- **Q-SWAP-2** — sister Pre-Q testing whether this lesson produces a verdict flip on the swap-specific question.

### Watch-point

During Pre-Q authoring (§3, §4) when the question is "what does additive-cost-shock X do to the MC verdict?" Specifically: any question about swap, slippage, broker-fee changes, commission inflation, or any per-trade cost that doesn't change Pine `calcSize` logic.

### Output trigger

If the watch-point fires, the brief's Pre-Q gate must specify both adaptive-1R MC (current pipeline) AND fixed-1R MC (reference baseline frozen at pre-shock `implied_1r` values). The §6 verdict triggers should be expressed against the fixed-1R MC, not the adaptive. If only adaptive-1R MC is run, the verdict will FALSE-FALSIFY by absorption — Q-SWAP-1 is the canonical worked example.

### Forbidden moves

- **Cite a FALSIFIED adaptive-1R MC as proof that an additive-cost shock is immaterial.** Q-SWAP-1 is this exact failure shape; cite it as worked example. The cost is real even when adaptive-1R MC absorbs it.
- **Use adaptive-1R MC to set `dd_protection` calibration in the presence of a known additive-cost shock.** dd_protection was tuned assuming MC bust attribution reflects live risk; hidden costs invalidate that assumption.
- **Tweak swap rates / cost magnitudes to make adaptive-1R MC produce a verdict-meaningful delta.** This is p-hacking through cost calibration. The right fix is fixed-1R MC, not rate tweaking.
- **Treat M-SWAP-1 as falsifying the swap question** — it falsifies the *adaptive-1R MC's answer* to the swap question; the swap question itself is open until Q-SWAP-2 RESOLVES or FALSIFIES.

### Reproducer / worked example

- **Q-SWAP-1 closure:** `docs/ltm/briefs/Q-SWAP-1-closure-falsified.md` §"Methodology finding"
- **Analysis script:** `lab/analysis/portfolio_swap_impact.py` (per-leg swap totals; adaptive-1R behavior visible in `scale_info`) — evicted 2026-06-07 with the retired Q-SWAP domain; retrieve via `git show 226aea1:lab/analysis/portfolio_swap_impact.py` (same git-history convention as the MC-patch commit below)
- **MC patch:** `portfolio_mc.py` `_compute_per_trade_swap` + `apply_swap` (the patch that surfaces the absorption when compared to fixed-1R reference run; commit `aafdd23`)

### Sibling lessons

- **M-AHF** (audit hooks check storage form): both are "the instrument tests a property the author thinks it does, but actually tests a different one." M-AHF is in form-space (grep regex vs storage form); M-SWAP-1 is in calibration-space (adaptive `implied_1r` vs fixed reference).
- **M-7** (anticipation-alert audit): both extend a Rule 0 read; M-7 to "anticipation alerts present," M-SWAP-1 to "calibration assumptions match live execution."
- **F-1** (TV <30-day JPY P&L inflation): both are "numeric output looks plausible but is wrong by an order of magnitude or qualitative pattern." F-1 is single-script-level; M-SWAP-1 is pipeline-level.

---

## M-Q-SWAP-3-2 — Regime-robustness gate floor doctrine: headline criteria, never relaxed strict-lock

**Status:** CANDIDATE 2026-05-26 (first worked example after gate-doctrine codification; promotion gated on second independent firing)
**Domain:** regime-robustness gate authoring · inquire-phase brief §6/§7 specification · methodology-doctrine clarification
**Sibling lessons:** Rule 0 (audit-first) · M-SWAP-1 (wrong-verdict anchor; co-firing investigation)

### Pattern

When an inquire-phase brief's §4/§6 headline criteria are NOT a simple pass-rate (e.g., multi-metric: p99 DD + bust + median triple-threshold), the §7 Phase 4 regime-robustness floor must be specified as the SAME headline criteria — NOT a relaxed strict-lock floor. Bootstrap 5th-percentile AND H1 AND H2 must each clear all headline conditions independently. The relaxed reading lets a config "pass" Phase 4 just by not breaking the strict lock under regime variance, defeating the gate's robustness purpose.

This was implicit in the gate doctrine (`docs/methodology/regime_robustness_gate.md` §"Pre-registered floor": "floor = brief's full-panel pass-rate floor") and explicit in Q-DDP-1 (2026-05-06) which used the headline floor. But for briefs whose headline criteria are multi-metric rather than pass-rate, the doctrine's wording ("pass-rate floor") doesn't translate mechanically — the natural authoring slip is to default to "strict lock criteria" which is the wrong floor.

### Anchor incident

- **Investigation:** Q-SWAP-3 (`docs/ltm/briefs/Q-SWAP-3-allocation-rebalance-under-fixed-1r.md`), CLOSED-AMBIGUOUS-HOLD 2026-05-26.
- **Closure:** [`docs/ltm/briefs/Q-SWAP-3-closure-ambiguous.md`](../../briefs/Q-SWAP-3-closure-ambiguous.md) §"Phase 4 — regime-robustness at GA-4 (failure-deciding)".
- **Defect surface:** Original Q-SWAP-3 brief §6 RESOLVED row + §7 Phase 4 description specified "clear strict lock criteria (bust < 1%, p99 DD < 5%) under fixed-1R swap-aware modeling" — the relaxed floor. Phase 0 dispatch agent surfaced as §0.5 (4) ambiguity (NEEDS_CONTEXT). Parent session amended brief at commit `36f9fd5` to specify headline criteria (p99 DD < 4.50%, bust < 1.00%, median ≤ 30d) per gate doctrine.
- **Counterfactual cost:** Under the relaxed (5%, 1%) floor, GA-4's Bootstrap (4.91/0.48) and H1 (4.90/0.49) would have PASSED Phase 4 → false-RESOLVED verdict → unjustified ADR superseding 2026-05-23 allocation lock. The headline-floor doctrine produced the correct AMBIGUOUS-HOLD.

### Rule

When authoring an inquire-phase brief whose §4/§6 headline criteria are NOT a simple pass-rate (e.g., multi-metric thresholds), §7 Phase 4 (regime-robustness) must EXPLICITLY state: "regime floor = (a) ∧ (b) ∧ (c) per gate doctrine; bootstrap 5th-percentile AND H1 AND H2 must each clear all headline conditions independently." Do NOT default to "strict lock criteria" language. The relaxed-floor reading is the trap.

### Mechanism (why this fails)

The regime-robustness gate doctrine was written for pass-rate-floor briefs (Q-DDP-1 worked example: 97.5% pass-rate floor uniformly across full panel + regime checks). When a brief's headline floor is multi-metric, the doctrine's "floor = brief's full-panel pass-rate floor" doesn't mechanically apply — the author has to translate. The natural-but-wrong translation is "use the strict lock criteria as the regime floor" (because they're the closest single-number reference). The correct translation is "use the same multi-metric headline criteria the brief evaluates on the full panel."

### Connection to standing doctrine

- **`docs/methodology/regime_robustness_gate.md`** §"Pre-registered floor": "floor = brief's full-panel pass-rate floor." M-Q-SWAP-3-2 extends this to multi-metric headline criteria.
- **Q-DDP-1 (2026-05-06)** worked example: pass-rate floor applied uniformly. Q-SWAP-3 is the second worked example, multi-metric variant.
- **M-SWAP-1**: co-firing investigation. M-SWAP-1's fixed-1R rule produced the 4.55% p99 DD reading that made Q-SWAP-3 a question; M-Q-SWAP-3-2's floor doctrine produced the correct AMBIGUOUS-HOLD verdict on that question.

### Watch-point

During Pre-Q authoring (§4 headline criteria specification + §6 RESOLVED/AMBIGUOUS-HOLD rows + §7 Phase 4 description), if the brief's headline criteria are multi-metric rather than pass-rate, explicitly state Phase 4 floor = headline criteria. Also during brief review of existing inquire briefs that have Phase 4 sections (Q-SWAP-2 specifically had the same latent defect — Phase 4 didn't fire there because verdict was AMBIGUOUS-HOLD before Phase 4 was invoked).

### Promotion criteria

Promote from CANDIDATE → PROMOTED on second independent firing — a third inquire brief with multi-metric headline criteria that explicitly specifies headline-floor Phase 4 (validating the rule has propagated to brief-authoring practice), OR a counterfactual where a brief failed to specify the floor correctly and produced a wrong verdict.

### Forbidden moves

- **Use "strict lock criteria" as the Phase 4 floor when headline criteria are multi-metric.** Even if the strict-lock floor is more permissive (and tempting because it makes RESOLVED verdicts easier to reach), it defeats the gate's purpose.
- **Skip the Phase 4 floor specification on the assumption "doctrine handles it."** The doctrine handles pass-rate-floor briefs; multi-metric requires explicit translation.

### Reproducer / worked example

- **Q-SWAP-3 closure:** `docs/ltm/briefs/Q-SWAP-3-closure-ambiguous.md` §"Phase 4 — regime-robustness at GA-4 (failure-deciding)" + §"Methodology lesson candidates" M-Q-SWAP-3-2.
- **Pre-Q brief amendment:** commit `36f9fd5` (fix(q-swap-3): clarify Phase 4 floor = headline criteria — not strict-lock).
- **Phase 0 agent flag:** §0.5 (4) ambiguity in the original Phase 0 read-report that triggered the brief amendment.

### Sibling lessons

- **M-SWAP-1** (wrong-verdict anchor on swap question): co-firing investigation; M-Q-SWAP-3-2 governs how to evaluate M-SWAP-1's verdict consequences under regime splits.

---

## M-Q-REGIME-1 — The 2024-04-30 panel-temporal boundary is a structural regime inflection, not a sample-size artifact

**Status:** CANDIDATE 2026-05-26 (first formal test of the N≥3 accumulating-signal hypothesis; PROMOTED if Q-REGIME-2 lands mechanism evidence, OR fourth corroborating investigation, OR first invocation in brief-authoring practice)
**Domain:** regime-robustness gate interpretation · H1/H2 split assessment when boundary lands at 2024 · MC verdict framing for portfolio-level investigations · accumulating-signal-hypothesis discipline
**Sibling lessons:** M-Q-SWAP-3-2 (Phase 4 floor doctrine) · M-SWAP-1 (wrong-verdict anchor)

### Pattern

When an investigation's half-panel split lands within ±2 months of 2024-04-30 and the H1/H2 spread on the relevant verdict statistic is materially different from spreads at neighboring boundary dates, the spread is **structural (priors-shifting)** — NOT sample-size variance to be discounted. The "H2-shorter-than-H1 → spread is just smaller-sample noise" discount is unfalsified pending Q-REGIME-2 mechanism findings, but the multi-boundary discriminator at GA-4 rejected the null at +2.06σ.

### Anchor incident

- **Investigation:** Q-REGIME-1 (`docs/ltm/briefs/Q-REGIME-1-2024-boundary-h1-h2-split-artifact.md`), CLOSED-FALSIFIED 2026-05-26.
- **Closure:** [`docs/ltm/briefs/Q-REGIME-1-closure-falsified-structural.md`](../../briefs/Q-REGIME-1-closure-falsified-structural.md) §"Phase 4 — Verdict computation".
- **Trigger investigations (N=3 that motivated Q-REGIME-1):** Q-DDP-1 (2026-05-06, dd_protection C2 candidate, H1 86.78% / H2 99.67% pass-rate at boundary 2024-05-01); Q-GDN-DDcap (2026-05-21, Max DD direction flip at boundary 2024-02-29 / 2024-03-01); Q-SWAP-3 (2026-05-26, allocation rebalance at GA-4, H1 p99 DD 4.90% / H2 3.81% at boundary 2024-04-30). All three boundaries within a ~2-month window.
- **Verdict-deciding statistic:** boundary-sweep over 5 dates {2023-07-31, 2024-01-31, 2024-04-30, 2024-07-31, 2025-01-31} produced |H1 p99 DD − H2 p99 DD| spread = {0.95, 0.83, 1.10, 0.89, 0.60}pp. Mean of 4 non-2024 boundaries = 0.817pp; population σ (ddof=0, n=4) = 0.133pp; **2024-04-30 z = +2.056σ** → FALSIFIED σ-clause fires (pre-reg threshold +1.5σ).
- **Pattern shape:** 2024-04-30 is a *local maximum* (lower spreads on both sides: 0.83pp at 2024-01-31, 0.89pp at 2024-07-31), NOT a tail of a smooth gradient. Spearman ρ over boundary-ordinal vs spread = −0.500 (non-monotone). Two independent falsification signals (z-score AND non-monotone pattern) point the same direction.

### Rule

When an investigation's half-panel split (regime-robustness or otherwise) lands within ±2 months of 2024-04-30:

1. Treat the H1/H2 spread as priors-shifting; do NOT discount as sample-size noise.
2. Reference `MEMORY.md/project_2024_regime_shift_accumulating_signal.md` (PROMOTED) explicitly in the brief's §1 / §4.
3. If the spread is verdict-deciding (FALSIFIED / AMBIGUOUS-HOLD turns on it), consider running `portfolio_mc.py --boundary-sweep --ga4` (or analogous multi-boundary sweep) as a cheap-falsifier check — even when the canonical mid-panel boundary is the only one specified. The sweep takes ~5 minutes and discriminates "specifically 2024-04-30" from "any boundary."
4. If the brief frames the spread as artifact-vs-structural, the search-space MUST include ≥3 non-2024 boundary dates with ≥18 months per side (or document the narrowing per the Q-REGIME-1 2025-01-31 precedent).

### Mechanism (why this matters)

The 2024-04-30 inflection appears across three unrelated research domains (dd_protection trigger, single-strategy DD cap, allocation rebalance) AND across the multi-boundary verdict-deciding sweep. The pattern is robust to investigation type, allocation config, and verdict statistic. The unfalsified-as-of-Q-REGIME-1 claim is that mid-2024 marks a structural change in the joint distribution of strategy-portfolio drawdowns. Candidate mechanisms (Q-REGIME-2 scope): (a) COVID-recovery / pandemic-supply-chain resolution effect on commodity + index volatility; (b) mid-2024 Fed rate-regime shift; (c) late-H1-2024 cohort discreteness from a specific event (geopolitical, monetary, structural).

### Connection to standing doctrine

- **`docs/methodology/regime_robustness_gate.md`** — Q-REGIME-1 extended the gate's half-panel split methodology to multiple boundary dates as a discriminator. The gate's standard mid-panel split was the verdict input for the three anchor incidents (Q-DDP-1 / Q-GDN-DDcap / Q-SWAP-3).
- **M-Q-SWAP-3-2 (Phase 4 floor doctrine)** — co-firing. M-Q-SWAP-3-2 governs which floor the regime-robustness gate uses on multi-metric headlines; M-Q-REGIME-1 governs how to interpret the gate's H1/H2 verdict when the split lands at 2024.
- **`MEMORY.md/project_2024_regime_shift_accumulating_signal.md`** — PROMOTED 2026-05-26 on this lesson's anchor incident. The memory holds the operational rule for application; this methodology lesson holds the structural finding.
- **`MEMORY.md/feedback_phase_4_floor_specification.md`** — the gate-floor specification rule that produced two of the three anchor incidents (Q-SWAP-3, Q-GDN-DDcap) in load-bearing form.

### Watch-point

During Pre-Q authoring (§4 H1/H2 hypothesis specification + §6 verdict triggers) when the brief's half-panel boundary lands within ±2 months of 2024-04-30. Also during closure-artifact review when the verdict trigger is sensitive to the H1/H2 split direction. Also when an investigation explicitly considers "the H1/H2 spread is just sample-size variance" as a candidate explanation — that hypothesis is now rebuttable evidence rather than free move.

### Promotion criteria

Promote from CANDIDATE → PROMOTED on the first of:
- Q-REGIME-2 lands a mechanism finding that explains the 2024-04-30 inflection (validating the structural-not-artifact claim).
- A fourth independent investigation surfaces the same inflection pattern (n=4 corroboration extending the original N≥3 threshold).
- An investigation explicitly invokes M-Q-REGIME-1 to interpret its own H1/H2 split (validating the rule propagates to brief-authoring practice).

### Forbidden moves

- **Discount a verdict-deciding H1/H2 spread as "H2-shorter sample-size variance" without running the multi-boundary sweep.** The sample-size confound is real (it was the original `accumulating_signal.md` flagged confound), but Q-REGIME-1 ran the discriminator and rejected the null at +2.06σ. Future investigations cannot reach for the discount unfalsified.
- **Open Q-REGIME-2 (or any mechanism follow-up) as a fishing expedition without mechanism hypotheses.** Anti-p-hacking commitment from Q-REGIME-1 §5 forbids solution-baked Pre-Q authoring; Q-REGIME-2 must specify (a)/(b)/(c) candidate mechanisms in §4 before it spawns.
- **Treat M-Q-REGIME-1 as confirming a specific mechanism.** It confirms that *some* structural inflection exists at 2024-04-30; the mechanism is unfalsified pending Q-REGIME-2.

### Reproducer / worked example

- **Q-REGIME-1 closure:** `docs/ltm/briefs/Q-REGIME-1-closure-falsified-structural.md` (verdict aggregation script in §"Verdict aggregation script (appended verbatim per pre-reg)" reproduces μ / σ / z / ρ from per-boundary spreads).
- **Sweep code:** `portfolio_mc.py` `mode_boundary_sweep` (CLI `python portfolio_mc.py --panel pepperstone --boundary-sweep --ga4`), committed at `62bf406`.
- **Pre-registration:** `docs/ltm/briefs/pre-registration/Q-REGIME-1-verdict-preregistration.md` (commit `62bf406`, predates Phase 3 sweep).
- **Memory anchor:** `MEMORY.md/project_2024_regime_shift_accumulating_signal.md` (PROMOTED 2026-05-26).

### Sibling lessons

- **M-Q-SWAP-3-2** (Phase 4 floor doctrine): co-firing. The Q-SWAP-3 Phase 4 result at 2024-04-30 was one of the N=3 anchor incidents.
- **M-SWAP-1** (wrong-verdict anchor): co-firing. Q-REGIME-1's verdict input was fixed-1R MC per M-SWAP-1's doctrine; adaptive-1R would have produced different boundary-sweep readings.

---

## M-23 — A parent-process config patch does not cross a process pool: parallel workers re-import from disk and silently score the WRONG configuration

**Incident (dated).** The 2026-07-24 band re-score rider
(`lab/analysis/c1_band_rescore_2026-07-24/run_band_regime_rider.py:54`) applied the
corrected eval geometry (`dd_lock_offset_usd → 1_000_000.0`) by mutating the
**parent process's** `FIRM_RULES` dict. Its full-panel and half-panel arms ran
in-parent and were correct. Its **bootstrap** arm fanned out through
`Parallel(prefer="processes")` passing only a **firm-key string**; each worker
re-imported `firm_rules` from disk, rebuilt config from the still-defective on-disk
`dd_lock_offset_usd: 100`, and returned plausible numbers. Published boot-95th
**4.54% / 4.49%** were therefore defective-geometry values. Re-measured under
worker-local patching with per-panel attestation: **6.69%** (T-50K) and **17.79%**
(100K @ 1.00×) — the error was ~1.5–7pp and **optimistic**. Detected 2026-07-28,
four days later, only because a successor harness attested the value it actually used.
Record: `lab/analysis/c1/c1_band_rescore_2026-07-24/RESULTS.md` §Addendum 2026-07-28;
corrected run `lab/analysis/c1/eval_shape_diagnostics_2026-07-28/`.

**Why it is invisible.** Nothing errors. The defective path produces well-formed,
in-range, plausibly-ordered output; the *same script's* serial arms are correct, so
partial reproduction of published pins (full/halves MATCH) reads as whole-harness
validation. A reproduction control only catches this if the control itself runs
**through the pool** — an in-parent control certifies nothing about worker state.

**Enforcement (the general rule, not the joblib special case).** Any run whose
correctness depends on a **mutated module-level constant** must (a) apply the
mutation **inside the worker**, after its own re-import; (b) **read the value back
from the object the engine will actually consume** and emit it into the report
(`geometry_offset_used`, `..._attested`); and (c) assert the attested set is a
singleton across every unit of work (`unique_offsets_observed == [expected]`).
Configuration passed as a **key** rather than a **resolved value** is the smell —
the key is re-resolved against whatever the worker's disk says. This is the
process-boundary sibling of Rule 0 (read production, don't assume semantics): here
the production value is read, then silently discarded at a process boundary.

**Blast-radius rule.** When this is found, the defect invalidates only the arms that
crossed the boundary — say which, re-measure what is load-bearing, and mark
un-re-measured cells **impeached** rather than quietly leaving the old number in
circulation (MFFU-50K's 4.49% remains impeached-not-re-measured at time of writing).
Siblings: M-9 / M-12 / M-22 (gitignored-bytes-outside-git family — same shape:
on-disk state diverging from what an artifact asserts).

## M-24 — When a venue fact is corrected in config, sweep for INDEPENDENT re-encodings of it; a config fix does not reach a hard-coded reimplementation

**The pattern (three dated encodings of one venue fact).** Tradeify evaluation accounts have
**no drawdown locking** (article 10495897; locking is Sim-Funded-only). That single fact was
encoded wrongly in three independent places, each found separately:

1. **Config** — `core/firm_rules.py` eval rows carry `dd_lock_offset_usd: 100` (found
   2026-07-22; cost +2.10pp bust at 1.00×, flipped Part A PASS→FAIL on both
   `trailing_locking` tiers). **The fix is still unapplied** pending re-MC + amending ADR.
2. **Config, re-resolved across a process boundary** — the 2026-07-24 rider's bootstrap
   workers re-imported the defective config despite a parent-side patch (M-23; boot-95th
   4.54% → 6.69%).
3. **Hard-coded literals in a second harness** — `gap_stage2_capbound.eval_sim`
   (`FLOOR_LOCK_BAL/FLOOR_LOCKED = 103_100/100_100`) applies the funded-only lock during the
   eval, inherited by `c1_capalloc_2026-07-27` via a direct `G.eval_sim` call (found
   2026-07-28; contaminates eval pass 63%, median 8.2 mo, and the `$339/acct-mo` chain rate).

Encoding 3 **does not read the config at all**, so shipping the encoding-1 fix would have
left it defective — and would have created the worse state where the config is right, the
docs say "corrected," and a live decision input is still wrong.

**Why the sweep gets skipped.** A corrected config feels like a corrected *fact*. The
config's own consumer list is easy to enumerate (`grep dd_lock_offset_usd`) and reads as
complete; an independent reimplementation shares **no identifier** with it, so it is
invisible to every search anchored on the config's names.

**Enforcement.** On correcting any venue fact, run a **mechanic sweep, not a symbol sweep**:
search for the *numbers* and the *behavior* (`103_100`, `100_100`, "lock", "freeze",
"floor"), not just the config key; enumerate every harness that simulates the affected
phase, including ones importing another study's primitives; and check that each phase-scoped
mechanic is scoped in code the way the venue scopes it (here: correct in `funded_sim`, wrong
in `eval_sim`, in the same file). Record the result as an explicit list of *checked* surfaces
— "config fixed" is not a blast-radius statement.

**Corollary for scheduled re-runs.** A pending re-run specified as "re-run the harness
unchanged" silently inherits every defect found after it was specified. When a defect lands
on a harness with a queued re-run, **amend the re-run's specification in the same motion**
(done here: STATE.md operator-queue item 4). Otherwise the fix and the re-run race, and the
re-run usually wins. Siblings: M-23 (the process-boundary case), M-9 / M-12 / M-22
(on-disk-state-vs-asserted-state family).

---

## Versioning & change-log

Relocated here 2026-08-29 (was drifting mid-file, above M-23/M-24, contrary to this section's own
"maintained at the bottom" convention) — content unedited by the move.

- **2026-08-29:** Format spec lightened for entries going forward: light 5-field format (Date /
  Anchor / What broke / Rule / optional Mechanism / Link) replaces the 8-field template + dollar-
  threshold CANDIDATE→PROMOTED state machine, sized for org memory rather than a solo journal.
  M-7 through M-24 keep their original 8-field format unedited — not a retroactive rewrite.
- **2026-05-08:** Registry seeded. Format spec authored. M-7 added as
  CANDIDATE on the 2026-05-07 Guardian late-fill anchor. M-1..M-6 remain in
  Notion / memory pending first-cite migration.
- **2026-05-10:** M-8 added as CANDIDATE on the GH #54 ULP-audit near-miss
  anchor. No wrong-verdict flip occurred (DONE_WITH_CONCERNS taxonomy caught
  the gap); promotion gated on second occurrence.
- **2026-05-10:** M-9 added as PROMOTED on GH #62 Phase B / PR #59 manifest
  drift RCA (H2 verdict); encodes local pre-commit hash gate + format-only CI.
- **2026-05-10:** M-10 added as PROMOTED on FXIFY validator/display routing review
  (parallel-layer contradiction cluster + `phase_completed_at` persistence).
- **2026-05-10:** M-AHF added as PROMOTED on third-instance auto-graduation per
  registry rule (audit hooks check storage form, not human-readable property;
  three same-day instances: GH #55 round 1, GH #55 round 2, PR #73 hook 4).
- **2026-05-16:** F-class introduced (fixture-caught defect). F-1 added as
  CANDIDATE on the Q-MT5-TV JPY ~153× anchor (retroactive seed; defect
  predates F-class infrastructure). F-class definition added to registry intro.
  Codifying ADR: `docs/adr/2026-05-16-fixture-test-requirement.md`.
- **2026-05-26:** M-SWAP-1 added as PROMOTED on Q-SWAP-1 closure
  (`docs/ltm/briefs/Q-SWAP-1-closure-falsified.md`); dollar-cost anchor $59,153
  hidden Guardian swap exposure; verdict-flip cost outstanding pending Q-SWAP-2.
  Pattern: risk-normalized MC absorbs additive-cost shocks via `implied_1r`
  recalibration; live Pine sizes by ATR, so the absorption diverges from live.
- **2026-05-26:** M-SWAP-1 upgraded to **wrong-verdict anchor** on Q-SWAP-2
  closure (`docs/ltm/briefs/Q-SWAP-2-closure-ambiguous.md`). Adaptive-1R produced
  FALSIFIED (Δbust 0.01pp, Δp99 DD 0.01pp); fixed-1R produced AMBIGUOUS-HOLD
  (Δbust 0.03pp, Δp99 DD 0.18pp; p99 DD lock-margin 0.45pp < 0.5pp tier).
  Calibration mode shifts the verdict band, not just the magnitude. New rule:
  additive-cost-shock questions require both calibration modes; conservative
  verdict canonical. 2026-05-23 ADR "criteria clear with margin" claim
  provisionally retracted on p99 DD gate under fixed-1R modeling pending
  Q-SWAP-3 (allocation re-evaluation under fixed-1R swap-aware MC).
- **2026-05-26:** M-Q-SWAP-3-2 added as CANDIDATE on Q-SWAP-3 closure
  (`docs/ltm/briefs/Q-SWAP-3-closure-ambiguous.md`). Pattern: when an inquire
  brief's headline criteria are multi-metric (not pass-rate), Phase 4
  regime-robustness floor must be explicitly stated as the SAME headline
  criteria — never a relaxed strict-lock floor. Counterfactual cost
  surfaced: under the relaxed floor, GA-4's Phase 4 Bootstrap + H1 would
  have falsely PASSED → unjustified ADR. Brief amendment at commit
  `36f9fd5` (fix(q-swap-3): clarify Phase 4 floor) is the doctrine fix.
  Promotion gated on second independent firing.
- **2026-05-26:** M-Q-REGIME-1 added as CANDIDATE on Q-REGIME-1 closure
  (`docs/ltm/briefs/Q-REGIME-1-closure-falsified-structural.md`). Pattern: the
  2024-04-30 panel-temporal boundary is a structural regime inflection (not
  sample-size artifact); investigations whose half-panel split lands within
  ±2 months of 2024-04-30 must treat H1/H2 spread as priors-shifting. Verdict
  evidence: z = +2.056σ on the 5-boundary sweep at GA-4 fixed-1R swap-aware
  (mean spread 0.817pp, σ 0.133pp; 2024-04-30 spread 1.10pp is local-maximum
  with lower spreads on both sides — non-monotone, opposite of artifact
  pattern). Q-REGIME-2 (mechanism investigation: COVID-recovery / Fed
  rate-regime / late-H1 cohort discreteness) registered, not auto-spawned.
  `MEMORY.md/project_2024_regime_shift_accumulating_signal.md` promoted to
  PROMOTED status. Promotion to PROMOTED gated on Q-REGIME-2 mechanism finding
  OR fourth corroborating investigation OR first invocation in brief practice.
- **2026-05-28:** M-11 added as CANDIDATE on retroactive landing of the
  2026-05-19 anticipation-gating refactor CC handoff
  (`2026-05-19-cc-handoff-anticipation-gating-refactor.md`, evicted 2026-06-05; retrieve via `git show pre-prune-2026-06-05:archive/docs/briefs/2026-05-19-cc-handoff-anticipation-gating-refactor.md`).
  Pattern: when patching infrastructure that inherits structural conditions
  from existing code, the patch's pre-registered §4 falsifier must include a
  test of the *interaction* between new behavior and the inherited gating —
  not only a test of the new behavior in isolation. Cost anchor $2,600
  (single-trade ECR delta on 2026-05-19 Aegis USDJPY); below $3K promotion
  threshold. Direct extension of M-7 — same alert infrastructure, prior
  patch series falsifier covered delivery but not timing correctness.
  Origin context: surfaced during Q-PARITY-1 §0-grounding review when the
  cited anchor brief was discovered to be orphaned (authored in claude.ai
  thread, dispatched to CC for execution, never committed to `docs/briefs/`).
  Path A landing committed both the brief (audit-trail anchor) and this
  lesson (methodology canon). Slot M-11 used because Appendix B's original
  M-8 routing target was already taken; next free integer per §Migration
  plan rule. Promotion gated on (a) backward-discovered silent-zone trade in
  pre-patch window adding ≥$1K cost, OR (b) pattern-match instance in a
  future patch unrelated to alerts.
- **2026-05-28:** M-12 added as CANDIDATE on the 2026-05-19 → 2026-05-28
  anticipation-gating workstream-class deployment failure (CC handoff
  dispatched 2026-05-19, patches never shipped to any of 4 indicators,
  surfaced 2026-05-28 by Joshua's TV-side grep during Q-PARITY-1 Phase 0
  audit-doc authoring; same-day re-ship via diff-generation-only handoff
  + parent-side TV application + post-application audit hook 4× OK).
  Pattern: gitignored-target CC handoffs need post-execution verification
  beyond CC's own return status. Cost: $0 (no silent-zone trade fired
  during the 9-day no-patch window — Poisson coincidence on infrequently-
  firing strategies, not patch success). Promotion gated on
  second-occurrence OR ≥$3K cost. Distinct from M-11 (design-layer
  falsifier-scope shadow) — M-12 is deployment-layer; sibling to M-9
  (gitignored-vendor-data manifest gate, same gitignored-bytes principle
  different domain). Worked example: re-ship handoff commit `c92de94`,
  closure commit `1a1aba1`, Q-PARITY-1 §1 retraction commit `98a53c8`.
- **2026-05-28:** M-13 added as CANDIDATE on the 2026-05-23 allocation-refresh-2
  half-application (strategy `.pine` updated to DJ30 pyramid 750 / NAS risk
  0.37; indicator `.pine` left at the 2026-05-14 values pyramid 500 / NAS 0.45,
  surfaced 2026-05-28 during the 8-file Pine drop + strategy-vs-indicator
  divergence audit). Pattern: Pine parameter-lock changes must update BOTH the
  strategy and indicator `.pine`, and both must be re-exported to TV — a
  one-file refresh silently splits backtest from live. Mechanism: gitignored
  Pine is absent on CI/public clones (gate WARNs, checks nothing); even when
  present, the pre-fix Pine check covered only the risk input on both files —
  `pyramidSize` was unchecked, so the DJ30 indicator 500-vs-750 drift had no
  catching gate (the NAS 0.45 risk drift would have been caught by the existing
  risk check, but the indicators only entered the clone 2026-05-28). Cost:
  workstream-class wrong-state count = 1 (2 params / 2 strategies); 5-day latent
  live exposure (NAS ~22% over-risk, DJ30 pyramid ~33% under-sized); dollars
  unmeasured. Tooling fix landed same day: `validate_params` now cross-checks
  `pyramidSize` on both strategy + indicator, pinned by
  `tests/test_validate_params.py`. Extends M-12 (deployment verification →
  change-set completeness). Indicator value fixes + manifest regen at commit
  `53f65da`. Promotion gated on second independent firing OR a measured ≥$3K
  in-window cost.
- **2026-07-06:** M-AHF fourth anchor added (already PROMOTED, no re-graduation
  needed) from an independent parent-session-equivalent review of
  `docs/ltm/briefs/Q-MECH-1_identify_notice_question.md`. Three of its four §10
  audit hooks (Pre-Q-gate count; causal-language leak; hypothesis-leak) no
  longer reproduce their claimed pre-commit output once re-run against the
  committed file — the §H "outputs" block quotes each hook's own command text
  verbatim, and that quoted text self-matches on re-run (`"Pre-Q gate:"`
  inflates 4→5; the causal/hypothesis patterns contain "because" /
  "hypothesis:" as literal substrings of themselves). New sub-shape: hook
  output embedded in the same artifact it audits, not an encoding-form
  mismatch. Substance independently re-verified clean by eye (4 real Pre-Q
  gates, no genuine causal/hypothesis leakage in the Notice text). Non-blocking
  to the brief's four MECHANISM-TRACTABLE verdicts; flagged for future
  audit-hook authoring (design hooks assuming their own output text will
  re-enter the corpus).
- **2026-07-20:** M-21 added as CANDIDATE on the Q-COMPOSE-1 closure
  (`docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md`, `4de8085`).
  Against a dollar-trailing DD barrier, dependence N_eff (correlation breadth)
  is not admissibility; risk N_eff (covariance breadth) is, and ρ = leg/book
  daily-$std is the seconds-cost falsifier. $0 realized (frozen engine caught
  the composition); anchor = ORB-MNQ-1 admitted on dependence N_eff +0.96 while
  risk N_eff +0.00, composed bust 2.65%→38.75%. Promotion gated on the next
  composed-candidate evaluation. Codifying ADR (`Proposed`):
  `docs/adr/2026-07-20-stage8-variance-dominance-risk-neff-gate.md`. Siblings
  M-16 / M-19 / M-20 (Stage-0-arithmetic-before-the-expensive-run family).
- **2026-07-24:** M-22 added as PROMOTED (three-surface structural recurrence per
  criterion (b); load-bearing cost = the `archive_lab_analysis` regression that
  hard-failed every commit from any worktree/clone lacking the gitignored heavy
  files, and whose `--regenerate` hint would have corrupted the canonical
  catalog). Pattern: always-on freshness/integrity gates over gitignored-
  generated content must presence-degrade the disk-derived field (WARN, exit 0)
  on a bare worktree/clone, while still hard-failing real drift and
  present-artifact drift. Surfaces: `check_data_manifests` (soft-degrade by
  design — M-9), `check_pine_manifest` (explicit presence gate, 2026-07-17),
  `archive_lab_analysis --check --catalog-only` (MISSED → hard-failed → fixed
  2026-07-24). Mechanism: worktrees/clones don't materialize gitignored bytes,
  so a disk-presence-derived field diverges from the committed artifact and a
  whole-artifact exact compare reports unavoidable "drift" — a total false
  positive on an always-on gate. Enforcement: test-authoring convention (every
  disk-reading always-on gate ships a bare-worktree absent-bytes test);
  recommended AGAINST a new mechanical meta-gate (semantic detection,
  belt-inflation risk). Siblings M-9 / M-12 (gitignored-bytes-outside-git
  family); M-13 (gate too lax when absent — M-22 is the too-strict counterpart).
  Design + fix: `docs/superpowers/specs/2026-07-24-lab-catalog-check-heavy-column-worktree-tolerance-design.md`;
  regression tests `tests/test_archive_lab_analysis.py`.
- **2026-08-01 (approx.):** M-23 added — parent-process config patch does not cross a process
  pool (2026-07-22 `dd_lock_offset_usd` boot-95th 4.54%→6.69% incident).
- **2026-08-01 (approx.):** M-24 added — a config fix does not reach an independent hard-coded
  reimplementation (`gap_stage2_capbound.eval_sim` 2026-07-28 incident).
