# ADR 2026-06-16 — Rule 2: Budget Before Acting (scaled to reversibility)

**Path:** `docs/adr/2026-06-16-rule-2-budget-before-acting.md`
**Status:** Accepted — ratified by operator (JA) 2026-08-21, as an explicit override ahead of §4/§6's evidentiary graduation gate (trip-log has not accrued ≥1 entry per active loop class). See Addendum 2026-08-21.
**Decision date:** 2026-06-16
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Date:** 2026-06-16
**Owner:** Joshua
**Author:** Claude (Tech Advisor), authored in claude.ai (briefs/methodology/no-commits role); landed to repo via Claude Code 2026-06-16. **Numeral reconciled at landing: the handoff proposed "Rule 1"; Phase-0 read found "Rule 1" already occupied by the live canon rule "small-cell variance prior" (`inqhiori-canon.md:245`/`:268`). Owner adjudicated the new rule as "Rule 2" on 2026-06-16. See §0/§1.**
**Loop-of-Record:** STRATEGIC — this commits a new constitutional numeral that binds all future artifacts (a governance act on what governs); low-reversibility canon edit. Load-bearing clause: §2 inserts a standing rule into `inqhiori-canon.md`. Switch-gate: N/A (no lower-loop execution component).
**Amends / extends:** the three-loop binding ADR (`docs/adr/2026-06-12-three-loop-methodology-binding.md`, PROPOSED) — Rule 2's magnitude is set by the Loop-of-Record / reversibility class that ADR defines. Canon home: `docs/methodology/inqhiori-canon.md` §15 (full statement) + §12 Hard-rules pointer + §14 loop-budget mirror.

---

## §0 — Reads (Rule 0)

Phase-0 reads executed by Claude Code 2026-06-16 against the live worktree (branch `claude/friendly-tesla-48ee43`, HEAD `af24b1f`) **before** any edit was drafted, per the handoff's §0 ("do not draft the insertion until this is reported"). The reads falsified the handoff's central premise (a free "Rule 1" slot) and forced the numeral reconciliation above.

- `docs/methodology/inqhiori-canon.md` — read in full @ `ecd4e0c` (prior `e122582`, the canon-mirror landing). Findings: (a) heading format is `## N. Title` (numbered sections 1–14); **there is no `## Rule 0` / `## Rule N` heading** — Rule 0 is referenced inline (§3:77, §5:106, §10:244) and as a Hard-rules pointer (§12:267). (b) **"Rule 1 (small-cell variance prior) still binds"** (`:245`), listed as a Hard rule (`:268`) — the numeral was occupied, so the new rule cannot be "Rule 1."
- `docs/adr/2026-06-12-three-loop-methodology-binding.md` — read in full @ `e122582`. Status **PROPOSED**; filename convention is **date-prefixed, not sequential `NNN`** (stated at its line 7 / §6.1). This ADR therefore takes `2026-06-16-...`, not an `NNN`.
- `docs/rule_0.md` — read in full @ `8f84060`. Canonical Rule 0 text ("audit-first"); notes Rule 0 is "the only methodology rule that survived the 2026-04-29 archive" and that "new rules are written only against observed failures during execution phase." The cfg00–12 unbudgeted sweep (§1) is the observed failure this rule is written against.
- `docs/operational_rules.md` — read @ `5baf01f` (§8 region). Carries an **independent** operational Rule 1–8 namespace (Rule 5 Pine-owns-params, Rule 7 one-canonical-owner, Rule 8 §0 sub-rules; "Rule 2" referenced at `:188`). Treated as a distinct namespace from the methodology-canon constitutional rules; this ADR's "Rule 2" lives in the canon namespace (Rule 0 audit-first → Rule 1 small-cell → Rule 2 budget).
- `docs/methodology/regime_robustness_gate.md` — read @ `5b8ff71`. Carries a third meaning of "Rule 1" (partition-hypothesis permutation gate, `:94`). Recorded so the numbering fragmentation is on the record; deconfliction of the three namespaces is explicitly **out of scope** here (§5).

**Rule-0 verdict:** the handoff was authored in a chat that could not read the repo (acknowledged in its own §0); the free-"Rule 1" premise was confabulated. The collision was surfaced and owner-adjudicated before any canon byte changed.

---

## §1 — Context & derivation

Rule 2 was derived over a 2026-06-16 session as a new constitutional numeral beside Rule 0. Rule 0 converts assumed premises into checked facts (the *truth* resource). Rule 2 converts open-ended spend into a stakes-scaled budget with a tripwire at the boundary (the *time/resources* resource). Same move — turn a silent slip into an explicit decision — on a different resource.

It earns a numeral because it binds **both** loops: a budget is OODA's time-boundedness restated, and it is the discipline the INNER-less INQHIORI sweeps (cfg00–cfg12 — 13 configs run unbudgeted) visibly lacked. Reversibility-classification is **not** a separate rule — it is the *sizing function* of this one (the loop class sets the magnitude), which is why it earns no numeral of its own. It connects to: the three-loop binding ADR (LoR = reversibility class), the forward-asymmetry doctrine (execution discipline ≫ methodology refinement — Rule 2 is execution discipline), and the CC-handoff hygiene rule (this adds *budget-before-handoff* alongside *correctness-before-handoff*).

Anchor magnitudes, owner-ratified 2026-06-16: **INNER 3 / OUTER 8 / STRATEGIC 3.** OUTER = 8 is anchored to cfg00–12: a checkpoint would have tripped at cfg08, converting cfg09–12 from silent drift into a decision — without killing the eventual leader cfg10. The numbers are set from that history but, per §4, are **validated forward, never re-derived from it.**

**Numeral note.** The handoff named this "Rule 1." Phase-0 (§0) found that slot occupied. Owner adjudicated "Rule 2." The derivation above is unchanged by the rename: it remains the second *new* constitutional numeral authored beside Rule 0 in the 2026-06-16 session.

---

## §2 — Decision

**D1 — Commit Rule 2 to canon (full statement).** Insert the payload below into `docs/methodology/inqhiori-canon.md` as a new `## 15.` section (there is no `## Rule 0` heading to sit "immediately after"; the canon states hard rules as §12 pointers + an integration section, so §15 is the faithful container that also carries the 3/8/3 numbers the audit hooks check). **Payload (verbatim except the numeral reconciliation):**

> **Rule 2 — Budget before acting, scaled to reversibility.**
>
> Before starting a task, declare a spend budget bounded by the cost of being wrong. Time is the intent; the budget is counted in *iterations* — one complete attempt-and-check cycle, mapped to the task's natural unit (config run; drafted-and-reviewed section; hypothesis–edit–test cycle; query-and-read pass). The loop class (LoR, §0) sets the magnitude:
>
> - **INNER** (recoverable/tempo): **3 iterations.** May self-extend once with a stated reason.
> - **OUTER** (structural/low-reversibility/statistical): **8 iterations.** No self-extension.
> - **STRATEGIC** (funding/kill-continue/programme-tier): **3 constituent OUTER investigations.** No self-extension.
>
> The budget is a **tripwire, not a wall.** Hitting it triggers a *structured stop* — spent / remaining / current state / extend-or-stop recommendation tagged with its reversibility — and a deliberate extend-or-stop decision. Never a silent continue; never a silent finish.
>
> Tripwire actions are **asymmetric by reversibility:**
> - Recoverable overrun → **STOP.** The overrun is the rabbit-hole signal.
> - Irreversible overrun → **STOP and RE-AUDIT.** A high-stakes decision blowing its budget means the Rule-0 read was incomplete; return to ground truth before continuing.
>
> Corollaries:
> 1. **Forbidden move.** Budget exhaustion may never resolve to shipping an under-validated irreversible change. The only legal exits from an irreversible tripwire are re-audit-and-continue-on-a-new-budget, or escalate to owner.
> 2. **Extension authority mirrors the three-loop binding.** INNER self-extends once; OUTER/STRATEGIC extension is owner adjudication or a re-audit — never self-granted.
> 3. **A flat budget is a Rule-0 violation in disguise.** Scaled to stakes or it is inert.

**D2 — Canon cross-references.** Add a Hard-rules pointer in `inqhiori-canon.md` §12 ("Rule 2 — budget before acting → this ADR + §15"), beside the existing Rule 0 and Rule 1 pointers. Add one mirror line below the §14 three-loop table noting that Rule 2 (§15) sets each loop's iteration budget (INNER 3 / OUTER 8 / STRATEGIC 3). **No other canon text changes** — the diff is insertion-only.

**D3 — Forward trip-log stood up.** Create `docs/notes/audits/rule-2-trip-log.md`: one table, columns *date · loop class · spent/budget · extend-or-stop · one-line hindsight-correct?*. This is the falsifier of record (§4) and the programme-audit datum source. It is **one table, not a telemetry subsystem** (§5). No existing add-back-rate artifact has a table this joins (the three-loop ADR §10 computes add-back ad hoc from `rejected_candidates.md` + kill records), so a new single-file log is the minimal correct form.

**D4 — Own-ADR.** This is a new numeral, not a clarification of the loops; it is **not** folded into the three-loop binding ADR (§5).

---

## §3 — The Algorithm pass (on this ADR itself)

- **Question:** the requirement ("open-ended spend needs a stakes-scaled budget with a boundary tripwire") originates from a measured failure — the cfg00–12 unbudgeted sweep — not an abstraction.
- **Delete:** could we rely on the existing three-loop LoR discipline alone? Rejected: LoR sets *which authority sizes a decision*; it does not declare a *spend boundary* or a *tripwire action*. The budget is the missing mechanism, not a restatement.
- **Simplify:** smallest sufficient form — one rule, three magnitudes, one asymmetric tripwire, three corollaries, one validation column. Explicitly rejected larger forms (per-domain unit table in canon; minutes-based budgets; a telemetry subsystem — see §5).
- **Accelerate:** nothing accelerated here; the trip-log is the cheap instrument that makes the forward falsifier (§4) runnable at audit cadence.

---

## §4 — Falsifiable hypothesis (the calibration falsifier)

Thresholds are validated **forward, never by retrodiction.** Retrodiction onto past instances (cfg00–12 etc.) is admissible for exactly one purpose — confirming the tripwire fires at the right *moments* (mechanism check) — and is **barred** from tuning the *thresholds* (the numbers were set from that same history; re-deriving them from it is circular and selection-biased toward blessing the status quo).

**H:** If, across the next forward trip-log entries per loop class, the budget wire fires predominantly at moments the owner judges (in hindsight) were the right place to stop, then the 3/8/3 thresholds hold and the rule graduates PROPOSED→ACCEPTED at the first programme audit with ≥1 entry per active loop class.

**Otherwise:** if the wire fires mostly at points that were productive in hindsight, the threshold (or the mechanism) wants revision — logged with the triggering entries; disposition at audit is amend, not silent retention.

**Falsifier:** a trip-log that, at audit, shows the budget wire firing predominantly at hindsight-*productive* moments **falsifies** 3/8/3 as calibrated. Standing bias while learning: **run tight, loosen only on evidence** — too-tight fails loud (visible tripwires; the extension path relieves), too-loose fails silent (the wire never fires, the rule is inert). A trip-log that stays empty across ≥2 audit cycles **falsifies the rule as load-bearing** (ceremony — disposition amend-or-delete). Threshold changes are earned only by trip-log entries, only at programme-audit cadence.

---

## §5 — Forbidden moves (each genuinely tempting; each would corrupt the commit)

1. **Folding Rule 2 into the three-loop ADR.** Tempting (they are adjacent) — but Rule 2 is a new numeral, not a clarification of the loops. Own-ADR. Conflating them buries it.
2. **Expressing the budget in minutes** anywhere in canon or ADR. Neither client can meter wall-clock; minutes evaporate, iteration counts enforce. Iterations only.
3. **Tuning 3/8/3 to match the historical record** during authoring. That is the selection-bias trap §4 exists to bar. The numbers are authored as given; only the forward log moves them.
4. **Auto-killing at budget** (writing the rule as a hard wall). It is a *tripwire* — a forced extend-or-stop decision, asymmetric by reversibility. A wall is a different, worse rule.
5. **"While I'm in here" canon edits.** Editing anything in `inqhiori-canon.md` beyond the Rule 2 insertion points (§15 + §12 pointer + §14 mirror line). The diff must be insertion-only.
6. **Building a Rule-2 telemetry subsystem** (dashboard / logger / metrics module). The validation instrument is one table. Proposing more is itself a Rule-2 violation — over-spending on the rule about not over-spending — and is the explicit tripwire on authoring this commit.
7. **Renaming the existing canon Rule 1 (small-cell variance prior) to free up "Rule 1."** Rejected at adjudication: it edits a live hard rule (not insertion-only) and is the exact "while-I'm-in-here" creep move #5 forbids. The new rule took the next free numeral instead.
8. **Deconflicting the three "Rule N" namespaces here** (canon vs `regime_robustness_gate.md` vs `operational_rules.md`). Out of scope — a separate STRATEGIC act. This ADR only commits Rule 2 into the canon namespace and records the fragmentation in §0.

---

## §6 — Gate (binary adoption criteria)

**Commit gate (all must hold for the landing to be DONE):**

1. This ADR committed to `docs/adr/` (date-prefixed filename), Status PROPOSED, §0 lists the Phase-0 reads with commit anchors.
2. `inqhiori-canon.md` contains the Rule 2 statement (§15) + the §12 Hard-rules pointer + the §14 mirror line; **no other canon text changed** (diff insertion-only).
3. `docs/notes/audits/rule-2-trip-log.md` exists with the five-column table.
4. The 3/8/3 magnitudes read identically across ADR §2, canon §15, canon §14, and the trip-log seed (no cross-artifact drift).

**Graduation:** PROPOSED→ACCEPTED at the first programme audit where §4 H holds (≥1 trip-log entry per active loop class, wire firing at hindsight-correct stops). **FALSIFIED / AMENDED** per the §4 otherwise-branch (wire fires at productive moments) or the inert-rule branch (empty trip-log across ≥2 audit cycles). If neither has accrued evidence by the audit, disposition is **AMBIGUOUS** — hold PROPOSED one more cycle, do not silently retain.

---

## §7 — Consequences

- Every future artifact may now declare a Rule-2 budget in its header alongside its Loop-of-Record; the magnitude follows directly from the LoR. This very ADR carried one (OUTER, 8 iterations — landed at iteration ~3, no overrun).
- The programme-audit checklist gains one item: read `docs/notes/audits/rule-2-trip-log.md`; confirm ≥1 entry per active loop class (else flag the rule inert per §4) and check whether the wire fired at hindsight-correct stops.
- The trip-log becomes the calibration data source; no new artifact type beyond the single table is licensed.
- Rule-numbering fragmentation (§0) is now documented but unresolved; a future STRATEGIC pass may deconflict the three namespaces (forbidden to do so here, §5.8).

---

## §10 — Audit hooks (runnable)

```bash
# 1. ADR present, Accepted (operator override 2026-08-21, not a §4 graduation), own-file (date-prefixed convention)
ls docs/adr/ | grep -i "rule-2-budget-before-acting"
grep -n "Status:\*\* Accepted" docs/adr/2026-06-16-rule-2-budget-before-acting.md

# 2. Rule 2 is in canon as a section, beside the Rule-0/Rule-1 pointers
grep -n "Rule 2 — Budget before acting" docs/methodology/inqhiori-canon.md
grep -n "Rule 0\|Rule 1\|Rule 2" docs/methodology/inqhiori-canon.md | head   # adjacency in §12

# 3. The 3/8/3 magnitudes match across the three artifacts (no drift)
grep -rn "3 iterations\|8 iterations\|3 constituent OUTER" \
  docs/methodology/inqhiori-canon.md docs/adr/2026-06-16-rule-2-budget-before-acting.md
```

## Addendum 2026-08-15 — pointer propagation narrowed to inqhiori only

**Does not amend §2 / §4 / §6.** This is a propagation-scope correction, not a
verdict on the ADR — §4's own gate is unmet either way: the trip-log carries one
non-trip baseline row at ~60 days post-authoring, short of the ≥2-audit-cycle
window the falsifier needs before the empty-log branch can even fire (§10.3
still passes; the numerals haven't drifted).

The 2026-08-15 governance-belt programme audit (§3.5) flagged the gap between
this ADR's evidence state and its footprint: between authoring and this date,
pointers requiring every task to "declare the loop class" were added to five
always-on surfaces — `CLAUDE.md`, `brief-authoring`, `inqhiori`, `cursor-fleet`
skills, and `.cursor/rules/session-discipline.mdc` — none of which is this
ADR's own text, all reachable on effectively every session. §4's forward-only
validation discipline exists precisely so evidence, not adoption breadth,
decides graduation; five always-on mirrors of a still-unvalidated rule moves
in the opposite direction from what §4 protects.

**Narrowed:** the four non-`inqhiori` pointers above are removed outright (not
redirected — a "see inqhiori" stub in four places would still be four places
carrying Rule-2 content, which doesn't address the adoption-ahead-of-evidence
concern). `docs/methodology/inqhiori-canon.md` §15 remains the full statement;
canon §12/§14 mirrors are untouched (§5.5 forbids editing them outside this
ADR); the `.claude/skills/inqhiori/SKILL.md` pointer stays, since INQHIORI-loop
work is this rule's most specific applicable context and canon §15 is already
its natural home. Declaring a Rule-2 budget is no longer instructed from
brief-authoring, cursor-fleet dispatch, or general session-start discipline —
only from INQHIORI-loop entry.

**Not a repeal.** The ADR stays `PROPOSED`; §4's graduation path is unchanged.
Re-widening propagation is available once the trip-log actually accrues
evidence at the next programme audit — narrower footprint until then, per the
same "run tight, loosen only on evidence" bias §4 already states.

## Addendum 2026-08-19 — §0 "third meaning" is the Rule 1 extension

**Does not amend §2 / §4 / §6 / §5.8.** Citation repair only.

The §0 note that `regime_robustness_gate.md` "carries a third meaning of
Rule 1 (partition-hypothesis permutation gate)" is incomplete: that row is
the 2026-04-24 extension of the same small-cell-variance-prior Rule 1
([owner](../methodology/archive/notion/rule-1-small-cell-variance-prior.md)).
Pointer expanded at
[`2026-08-19-rule-1-citation-not-three-meanings.md`](2026-08-19-rule-1-citation-not-three-meanings.md)
and on the gate doc. Full four-namespace deconflict (`OPS` / `INQ` /
skill-local) remains out of scope per §5.8 and the
[2026-08-08 conventions audit](../notes/audits/2026-08-08-conventions-delete-phase-gap-audit.md) §5.

## Addendum 2026-08-21 — Operator ratification (explicit override, not §4 graduation)

**Does not amend §2 / §4 / §6.** §4's falsifier and §6's gate criteria stand as written and are
**not** met on their own terms: the trip-log carries one non-trip baseline row (OUTER,
2026-06-16); INNER and STRATEGIC have zero entries; the ≥1-entry-per-active-loop-class bar for
PROPOSED→ACCEPTED graduation (§6) is unreached.

**Ratified anyway**, by explicit operator instruction ("ratify Rule 2"), 2026-08-21, during a
review of this repo's governance-growth pattern (belt-churn evidence: 56 adds / 7 removes per the
2026-08-03 gate-stack audit; ADR corpus 121→132 in 6 days against the 2026-08-08 audit's own
stated target). Operator reasoning, recorded rather than folded into a fabricated "H holds":
**Rule 2 would have caught earlier errors** — a forced stop-and-decide point beats open-ended
drift. This is retrodiction-as-mechanism-check, which §4 explicitly permits (barred only from
*tuning the 3/8/3 thresholds* on past instances, never from justifying the mechanism itself on
them). Two concrete cases stand behind that judgment: (1) the cfg00–12 sweep this ADR's own §1 is
already anchored to — a checkpoint at cfg08 would have converted nine further configs of silent
drift into an explicit decision; (2) discovered in this same session, Rule 2's *own* ratification
history — PROPOSED for over two months, deferred three times (2026-08-08 slate write → 2026-08-09
correction → "rule at 2026-11-08, do not infer now") with no forced stop-and-decide point — which
is itself exactly the failure shape a STRATEGIC-class budget exists to catch. A third deferral
would have repeated that pattern rather than resolved it.

This is an **override**, not a claim the evidentiary bar was met — logged as such per the same
convention already used elsewhere in this repo for an operator call against an unmet or adverse
gate (the regime-robustness-gate C2 override; the Guardian Silver admission override, "logged as
such"). The gate result is recorded honestly here; the operator's separate judgment sits alongside
it, not inside it.

**Trip-log discipline is unchanged.** Still one table, still no fabricated rows (§5.6), still
validated forward only (§4). Ratification does not retroactively manufacture trip-log evidence —
the log stays exactly as sparse as it is, and future audits should read it as such, not as
"already validated."

# 4. Forward trip-log exists (the falsifier is live, not theater)
ls docs/notes/audits/ | grep -i "rule-2-trip-log"
# at each programme audit: confirm >=1 entry per active loop class, else flag the rule inert
```

---

## Addendum 2026-08-22 (Status: PROPOSED — pending operator ratification) — audit-cycle counting convention for the §4 empty-log falsifier

**Does not amend §2 / §4's 3/8/3 thresholds / §5 / §6's per-loop-class graduation bar.** This
addendum proposes a counting *convention* for reading §4's "empty across ≥2 audit cycles"
falsifier when a scheduled cycle's own review is disputed — it resolves a genuinely open
ambiguity the trip-log's own text (`docs/notes/audits/rule-2-trip-log.md:59-64`) flags and
explicitly defers ("Rule at the 2026-11-08 gate, and state the counting convention there rather
than inferring one now"). **Tier: FULL** under `docs/adr/2026-08-08-adr-ceremony-tiering.md`
limb 4 (states a convention binding future audit-cadence counting, not just this file) — and,
per that ADR's own escalation rule, an ambiguous tier defaults to FULL regardless. Landed as an
**addendum to this ADR**, not a sibling file, per the 2026-08-15 amend-in-place convention
(`2026-08-08-adr-ceremony-tiering.md` Addendum 2026-08-15): the dispute is entirely about how
*this* ADR's own §4 falsifier counts, so this file is already the correct owner — a new ADR would
duplicate reasoning this file already carries in its 2026-08-15/-19/-21 addenda.

**Reads (this run, 2026-08-22, full text unless noted):**
- `docs/adr/2026-08-22-ox-alpha-adversarial-lens-scope.md` — `b2e5f15d2b11a72759d3734eba89806c2375c38b` (2026-08-22). Scopes the sanitized second-opinion lens this task originated from as candidate-objection input only, carrying zero authority over a governing decision — the framing this addendum honors in the next paragraph.
- `docs/notes/audits/rule-2-trip-log.md` — `f6f92dce914c9a36780de29b14e07e22d79174b7` (2026-08-20). The 2026-08-09 correction block (its own lines ~44–64) is the primary artifact for this dispute; the 2026-08-20 STRATEGIC trip row (added by the same commit that is this file's last touch) is load-bearing new evidence the correction block predates.
- `docs/adr/2026-06-16-rule-2-budget-before-acting.md` (this file) — `d060698a3519737e9b9ed53dab542a8dbc599d25` (2026-08-21), i.e. the version immediately prior to this addendum. §4 (empty-log ≥2-cycle clause), §6 (per-loop-class graduation gate), and the 2026-08-21 addendum's own "override, logged as such, not a claim the gate was met" framing — the precedent this addendum reuses for landing PROPOSED rather than silently inferring a convention.
- `docs/notes/audits/programme-audit/2026-07-01-methodology-belt-scoped-audit.md` — `937b9a23869f347a4eee015fcc2632e3e30e3361` (2026-08-15). §3 Q-B and §11 confirm this audit *did* execute a reasoned Rule-2 disposition (AMBIGUOUS-on-schedule, correctly reasoned as <2 cycles elapsed) — the positive control for "what an executed cycle looks like."
- `docs/notes/audits/programme-audit/2026-08-08-quarterly-audit.md` — `937b9a23869f347a4eee015fcc2632e3e30e3361` (2026-08-15). Directly re-verified this run: `grep -c "Rule 2\|trip log"` returns **0** — confirms the trip-log's own claim that this slate's Rule-2 checklist item was never executed, not merely under-documented.
- `docs/adr/2026-08-09-rejection-register-topology-and-bar-wiring.md` — `027a729589c815fda8286f3d74f1306f121dd7ac` (2026-08-14). D2's "ratification-and-wiring rule" (a bar is operative only when both a stamp and a machine consult exist) is the closest existing doctrine, cited by the trip-log as the disposition mechanism for the phantom-discharge class generally — confirmed by this read to resolve *that* class (false-record correction) but **not** to state any audit-cycle-counting convention; D2 governs bar operativeness, not cycle tallies. This addendum fills that specific residual gap, not a re-litigation of D2.
- `docs/rejected_candidates.md` — `027a729589c815fda8286f3d74f1306f121dd7ac` (2026-08-14), lines 692–705. Confirmed the twin phantom-discharge correction cited by the trip-log is real, same shape, same 2026-08-09 date, same "same sweep" attribution — corroborates rather than resolves the counting question.
- `docs/adr/2026-08-08-adr-ceremony-tiering.md` — `91e6caad0993e59b1ca79471de708a91d6ea9a15` (2026-08-15). Supplies the tier test applied above and the amend-in-place addendum it names.
- `docs/adr/2026-08-16-ambiguous-hold-counts-toward-null-run-thresholds.md` — `b4768601213cfaadc4bc34f5617cfdfe7ec3a021` (2026-08-16). Read as the closest structural precedent for a repo counting-convention ADR (full tier, limb 4, patches counting mechanisms via dated addenda rather than in-place rewrites) — its shape is followed here; its *content* (zero-yield disposition counting) is unrelated and not extended by this addendum.
- Also confirmed by direct search this run: no ADR or `docs/SESSIONS.md` entry dated after 2026-08-09 states a Rule-2 counting convention or otherwise closes this question (`git log` on the trip-log file shows exactly one post-2026-08-09 touch, `f6f92dce9`, 2026-08-20, which added the STRATEGIC trip row and left the counting-ambiguity block byte-unchanged — confirmed via `git show f6f92dc -- docs/notes/audits/rule-2-trip-log.md`).

**Context — what changed since the 2026-08-09 correction was written.** That correction (still
current text) leaves the cycle-count "not determinable" because the 2026-07-01 audit named
"~2026-09" and "~2026-12" as the 1st/2nd post-codification audits, but the real quarterly gates
are 2026-08-08 (whose Rule-2 item never executed) and 2026-11-08. Two things the correction block
itself could not have known when written: (1) the 2026-08-08 quarterly audit *did* happen as a
real, substantive audit event (`2026-08-08-quarterly-audit.md` exists and runs seven other
diagnostics) — the defect is a skipped checklist item inside a real audit, not a missing audit;
(2) on 2026-08-20, a genuine STRATEGIC-class trip fired and was recorded with a fully reasoned,
hindsight-correct disposition (`rule-2-trip-log.md`'s second table row). Neither fact is reflected
in the still-standing "not determinable" text.

**Proposed convention.** An audit cycle counts toward an audit-cadence falsifier (here, §4's
empty-log clause) if and only if that cycle's audit artifact contains an **executed,
disposition-recording** review of the specific item — a null or negative disposition still
counts, but a checklist item that was never touched does not, regardless of whether some other
audit activity occurred on or near the scheduled date. This extends the same principle
`2026-08-09-rejection-register-topology-and-bar-wiring.md` D2 already applies to bars (a stamp
and a wire, not proximity to one, make it operative) into the audit-cadence-counting domain, and
matches how `2026-07-01-methodology-belt-scoped-audit.md` §3 Q-B is plainly a genuine cycle
(reasoned disposition present) while `2026-08-08-quarterly-audit.md` plainly is not (zero
occurrences, confirmed above).

**Applying it.** Exactly **one** genuine post-codification cycle has executed to date —
2026-07-01. 2026-08-08 does not count under this convention. Read narrowly, that would put the
§4 empty-log clock at 1 of the required ≥2 cycles, not 2 — i.e. **one tick, not two, and not
"indeterminate."** But this narrow reading is now moot in practice: the trip-log is no longer
"empty" under any plain reading of §4 regardless of cycle count — the 2026-08-20 genuine
STRATEGIC trip (reasoned, hindsight-correct, correctly following owner-adjudication-only
extension authority) means the inert-rule branch of §4 has nothing to fire on today. The
residual value of stating the convention is forward (the next disputed phantom-discharge, not
this one) and for §6's separate per-loop-class graduation gate, which the STRATEGIC trip does
not satisfy on its own (INNER still carries zero entries).

**One-sentence note on the originating review lens.** A sanitized, genericized restatement of
this exact counting ambiguity was run this session through the stateless, zero-authority external
second-opinion lens scoped by `2026-08-22-ox-alpha-adversarial-lens-scope.md`; per that ADR's §2/§5
its output is candidate-objection input only and carries no authority here — the convention and
resolution above are derived independently from the primary sources listed, not from that lens's
output.

**Falsifier (of this convention, distinct from §4's own 3/8/3 falsifier).** This convention is
miscalibrated if it is later invoked to let an audit-cadence falsifier be indefinitely deferred by
repeatedly, unaccountably skipping the checklist item while other diagnostics in the same audit
run normally — i.e., if "the item wasn't executed" becomes a standing excuse rather than a
single-cycle miss. Check: at the 2026-11-08 quarterly audit, does the Rule-2 trip-log checklist
item (parent ADR §7) actually execute? A second consecutive skip is no longer a "single-cycle
miss" (the framing the 2026-08-09 correction used) and escalates to a process-compliance defect
in its own right, separate from anything about Rule 2's calibration.

**Gate.** This addendum stays `PROPOSED` until operator ratification (mirrors the parent ADR's
own 2026-08-21 addendum: an explicit, logged operator call, not a silent CC inference — ratifying
early does not itself violate the trip-log's "rather than inferring one now," since that text
guards against an *unratified* inference, not against an *operator-ratified* one landing ahead of
the named gate). If ratified before 2026-11-08, that gate becomes the first live test of the
convention (does the checklist item execute this time) rather than the moment the convention is
authored. If left unratified, it holds as a dated proposal and the operator may instead state a
convention fresh at 2026-11-08, exactly as the trip-log's own text anticipates.

**Forbidden moves.**
- Counting 2026-08-08 as a completed Rule-2 cycle solely because a real audit note exists dated
  near it — under this convention, proximity is not execution.
- Backfilling a disposition into `2026-08-08-quarterly-audit.md` now to make the tally come out
  even — that would manufacture the exact after-the-fact-record shape the 2026-08-09 correction
  exists to name, applied to the same slate a second time.
- Treating the 2026-08-20 STRATEGIC trip as satisfying §6's graduation gate — that gate needs
  ≥1 entry **per active loop class**; INNER remains unexercised. The empty-log question and the
  graduation question are separate counts and must not be conflated.
- Treating this addendum's authorship, on its own, as discharging the trip-log's "state the
  counting convention... at the 2026-11-08 gate" instruction — it is a proposal awaiting the
  operator's own ratification (see Gate above), not a unilateral resolution.
- Generalizing this convention repo-wide (e.g. to the ceremony-tiering ADR's own quarterly-review
  trigger, or to `2026-08-09-rejection-register-topology-and-bar-wiring.md`'s 2026-11-08
  falsifier) without a dedicated sweep and its own ADR, in the shape
  `2026-08-16-ambiguous-hold-counts-toward-null-run-thresholds.md` used for streak-counters. Named
  here as a plausible future generalization, not assumed or executed by this addendum.

**Consequences.** No mechanical edits required beyond this text (policy-only, like the parent
ADR's other addenda). A `docs/SESSIONS.md` entry noting this proposal is owed at land time per
this repo's session-log discipline, not included here. If ratified, the natural downstream
artifact is a one-line addition to the parent ADR's own §7 audit-checklist item, making explicit
that "confirm the item was executed, not merely that an audit note exists near the date" — not
drafted here, since this addendum is `PROPOSED`, not yet a landed decision.

**Audit hooks (runnable).**

```bash
# Confirm the 2026-08-08 slate still shows zero executed Rule-2 review (the fact this addendum turns on)
grep -c "Rule 2\|trip log" docs/notes/audits/programme-audit/2026-08-08-quarterly-audit.md
# Expected: 0

# Confirm the 2026-08-20 genuine trip is still on record and the counting-ambiguity block is unmodified since
git log --format="%H %ad %s" --date=short -- docs/notes/audits/rule-2-trip-log.md
git show f6f92dce9 -- docs/notes/audits/rule-2-trip-log.md   # expect: +1 line only (the STRATEGIC row)

# At the 2026-11-08 gate: did the checklist item actually execute this time?
grep -c "Rule 2\|trip log" docs/notes/audits/programme-audit/2026-11-08*.md 2>/dev/null

# §6 graduation is still separately gated on a per-loop-class basis (not satisfied by the STRATEGIC trip alone)
grep -n "INNER" docs/notes/audits/rule-2-trip-log.md
```

---

## Verification

```bash
# Mechanical well-formedness (repo-side subset; skill-side checker governs)
python scripts/check_brief.py docs/adr/2026-06-16-rule-2-budget-before-acting.md --type adr
# Expected: RESULT: well-formed

# §0 anchors resolve
git log --oneline -1 -- docs/methodology/inqhiori-canon.md   # ecd4e0c
git log --oneline -1 -- docs/adr/2026-06-12-three-loop-methodology-binding.md   # e122582

# Canon diff is insertion-only
git diff --stat docs/methodology/inqhiori-canon.md   # expect +N / -0

# Numbers consistent across ADR + canon
grep -c "8 iterations" docs/adr/2026-06-16-rule-2-budget-before-acting.md docs/methodology/inqhiori-canon.md
```

If any check fails, the landing is not complete — re-author the broken section; do not handwave.
