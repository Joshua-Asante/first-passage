# Q-M1WIRE-1 — CLOSURE: `FALSIFIED` (A2 + A5 both confirmed; A4 untested and not required for the verdict)

**Verdict:** `FALSIFIED`
**Closed:** 2026-08-21
**Lane:** UNASSIGNED — diagnostic Q on the M1 arming interlock's own coverage, not a strategy-discovery lane
**Pre-registration:** none authored as a standalone `docs/briefs/pre-registration/` file. Process note (not a threshold change — see §4 below): the parent brief's own Section 4 froze the A2/A4/A5 Accept/Reject thresholds at authoring (2026-08-18), before this session touched it; nothing here was pre-registered *after* seeing results. What was genuinely skipped is the standalone pre-registration artifact and a formal pre-Phase-1 operator GO — the brief's own header still reads `OPEN — DRAFT (pre-lock)`. Operator GO for execution is recorded here: given in-session 2026-08-21 (directing review of PR #75 against this brief, then "discharge the precondition").
**Successor:** none opened by this closure. A scoping spec for the underlying fix (mechanical alert monitor + wired confirmed-base call site) is authored separately as future work — naming it here is not opening it.
**Spend / K:** $0 · K consumed: 0 — every check below is a grep or a direct file read against already-committed artifacts, no data pulls, no backtests.
**Live effect:** none. Rail stays disarmed (`dry_run=true`), M1 stays not-`RESOLVED` (it already was not `RESOLVED` — item 5 was always the last owed item). This closure changes no code and no live state; it makes the record honest about a claim (`require_resolved=True` ⇒ every capability is live-wired) that was never actually true.
**Artifacts:** commands + outputs in §1 below; source anchors — `ops/c1_rail/c1_sizing_host_reference.py`, `ops/c1_rail/c1_rail_telemetry.py`, `ops/c1_rail/c1_rail_arm.py`, `scripts/gates.yml`, `docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json`.

---

## 1. Verdict (§6 asserted against actual numbers)

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` | All three limbs (A2, A4, A5) clear per §4 Accept conditions | Not reachable — A2 and A5 both independently confirm their Reject conditions | — |
| `FALSIFIED` | ≥1 limb confirms its gap per §4 Reject conditions | **A2 confirmed** (both clauses) · **A5 confirmed** (both clauses) — see below | ✓ |
| `AMBIGUOUS-HOLD` | A4 drill unexecutable this cycle while A2/A5 both clear or both fail cleanly | Does not apply — A2 and A5 fired `FALSIFIED` independently before A4 status became relevant to the overall verdict; the Gate is `≥1` limb, not `all three` | — |

**A2 — production write path for confirmed-base.** Both Reject clauses independently confirmed:
- Clause 1: `rg -n "set_confirmed_base|confirm_executed_base" --type py` → every match outside `tests/` is a method *definition* (`c1_sizing_host_reference.py:183`, `c1_rail_telemetry.py:403`) or an in-source comment; zero production **call sites**. Every actual call is inside `tests/ops/test_c1_sizing_host_reference.py`, `tests/ops/test_c1_rail_listener.py`, `tests/ops/test_m1_acceptance_drills.py`, `tests/ops/test_c1_rail_telemetry.py`.
- Clause 2: the SIM 2026-07-27 dry-fire artifact (`M1_MONITORING_ACCEPTANCE.json`, item-6 note) records a real logged fill — entry event `7f80b4be-…`, Filled BUY MYMU6 qty 8 @52,240.00, confirmed via CrossTrade Alert History + Tradovate, reconciled `CHAIN_OK` — and `grep -c "confirmed_base_qty" docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json` returns **0**: the field is entirely absent from the record of a real, broker-confirmed fill. Both required clauses hold.

**A5 — fixture-hash drift checked before arming, or wired into `gates.yml`.** Both Reject clauses independently confirmed:
- `grep -n "validate_c1_monitoring_acceptance" scripts/gates.yml` → 0 hits, no tier, no cadence.
- `rg -n "tree_skew|check.tree.skew" ops/c1_rail/c1_rail_arm.py` → 0 hits; the arm path (`m1_acceptance_reason`, L79–117) validates schema/status fields only and never calls the skew checker.
- Independently re-running the checker itself the same session (`python scripts/validate_c1_monitoring_acceptance.py docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json --check-tree-skew`) showed live drift on all 6 of 6 pinned files against the current worktree — the exact class of gap A5 is testing for, observed directly, not inferred.

**A4 — alert reachability, <10 min, unannounced.** Untested. The one drill on record (`M1_MONITORING_ACCEPTANCE.json` item-10, 2026-07-28: alert fired 12:06:07Z, ack 12:12:23Z, 6m16s) is contaminated per the parent brief's own §5 — the operator knew the drill was happening and went straight to check, which is prepared attentiveness, not the ordinary-work condition A4 tests. No new drill was run this closure. **This does not block the verdict**: the Gate fires `FALSIFIED` on `≥1` confirmed limb, and A2 + A5 already clear that bar independently of A4.

## 2. What the pre-registration predicted vs what happened

No standalone pre-registration file existed (see header). Against the parent brief's own §4 (frozen 2026-08-18): the brief predicted this shape exactly — "the M1 acceptance package and its owning ADR describe live-safety capabilities in prose with more rigor than the arm interlock mechanically checks." Both tested limbs confirm that prediction with no surprises. Nothing here contradicts the brief's own framing; this closure is discharging the branch the brief itself flagged as most likely.

## 3. What this closure does NOT license

- **Does not touch M1's status.** M1 stays not-`RESOLVED`. This closure is orthogonal to, not a substitute for, item 5 (`dry_run_strategy_signal_event_id` from a real strategy signal) and `operator_signoff`, which were always the stated remaining bars.
- **Does not authorize `dry_run=false`.** No arm-path, sizing, or live-risk-surface change is made or implied. Rail stays disarmed throughout.
- **Does not mean A4 was tested and failed.** A4 remains genuinely unknown — untested, not falsified. A future arm decision should not read this closure as "alert reachability is bad," only as "alert reachability was never honestly measured."
- **Does not authorize wiring the A2/A5 fixes as a byproduct.** Per the parent brief's own §5 forbidden moves, any change to `ops/c1_rail/` or `scripts/gates.yml` needs its own pre-registration → re-derivation → admitting ADR path. A separate scoping spec for that fix is being authored, not landed, alongside this closure.

## 4. Defects found in the frozen brief (recorded, not repaired)

None found in the brief's own §4/§5/§6 text. The one process defect is procedural, not textual: the brief's own Pre-Lock Checklist names two items as owed before Phase 1 executes (a standalone pre-registration file; an explicit operator GO) that were not formally discharged before this session's checks ran. The checks themselves used only the thresholds §4 already froze at authoring — nothing was pre-registered after seeing results, so Trap #12 (post-hoc threshold-shopping) is not implicated. The gap is closed retroactively here: this closure records the operator GO that was missing, and treats the absent standalone pre-registration as a genuine, named skip rather than a silently-assumed one.

## 5. Lesson candidates

Below the two-incident promotion bar — watch, not yet a named lesson. The shape (a schema/status validator standing in for full functional verification) already has a name and a promotion in this repo's own registry as `lesson_gate_reachability_preregistration` and the M1-specific instance the 2026-08-09/2026-08-18 audits already tracked; this closure is confirming, not discovering, that pattern on a third occasion, which does not itself clear a fresh promotion bar.

## Iterate — loop exit (MANDATORY — closure incomplete without it)

- **Verdict used:** `FALSIFIED` (A2 + A5 both confirmed per §4; A4 untested, not load-bearing to the verdict)
- **Model update:** `require_resolved=True` on the M1 acceptance artifact is confirmed **not** a sufficient proxy for "every capability the package describes is live-wired" — it was already suspected (that is why this Q was opened) and is now directly observed on two independent limbs, not inferred from prose.
- **Next:** `ITERATE`
- **Routing:** ITERATE → Identify (new thread) — a scoping spec for the actual fix (mechanical alert-log monitor + a wired production confirmed-base call site), authored as a separate artifact under `docs/spec/`, not landed as code. A4 also stays a named, un-opened re-test candidate (the unannounced human drill), independent of the fix spec.
- **Entry packet:** for the fix-scoping spec — carry forward verbatim: A2's confirmed gap (zero production call sites for `confirm_executed_base`/`set_confirmed_base`); A5's confirmed gap (no `gates.yml` wiring, arm path never calls `tree_skew()`); the constraint that any real change needs its own pre-registration → re-derivation → admitting ADR before landing, per the parent brief's §5 and this repo's live-execution posture (CLAUDE.md).
- **Stop rule / re-proposal bar:** this closure does not die — A4 remains a legitimate, cheap ($0/K=0) re-open at any time via an actual unannounced drill; the A2/A5 gaps reopen automatically as "fixed" only once a landed, ADR-admitted change makes the same checks above return the Accept-branch outputs.
- **Board write:** `docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md` (M1 ADR) — item 5 + `operator_signoff` remain the only bars to `RESOLVED`; add: Q-M1WIRE-1 closed `FALSIFIED` 2026-08-21 (A2 + A5 confirmed gaps in what `require_resolved=True` actually certifies) — [`closure`](Q-M1WIRE-1-closure-falsified.md).
- **Registry:** `n/a — governance/diagnostic Q on the M1 interlock's own coverage, not a strategy-grounds kill`

## §10 audit-hook discharge

Parent brief's §10 hooks, re-run this session:

```bash
# A2
rg -n "set_confirmed_base|confirm_executed_base" --type py
# -> 0 hits outside tests/ (confirmed above)
grep -c "confirmed_base_qty" docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json
# -> 0 (confirmed above; SIM 2026-07-27 logged fill has no confirmed_base_qty field anywhere)

# A4 — operator-run, unannounced. NOT executed this closure.

# A5
python scripts/validate_c1_monitoring_acceptance.py docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json --check-tree-skew
# -> tree skew: 6 of 6 pinned file(s) differ from this tree (confirmed above)
grep -n "validate_c1_monitoring_acceptance" scripts/gates.yml
# -> 0 hits (confirmed above)
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-21 | Closure authored — FALSIFIED on A2 + A5, A4 left untested | Claude Code, per operator direction |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/Q-M1WIRE-1-closure-falsified.md
python scripts/check_brief.py docs/briefs/Q-M1WIRE-1-arming-interlock-coverage.md --type inquire
```
