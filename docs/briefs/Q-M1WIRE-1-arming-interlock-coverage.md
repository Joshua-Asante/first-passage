# Q-M1WIRE-1 — Does the M1 arming interlock actually verify everything its own acceptance package and doctrine claim it verifies?

**Status:** `CLOSED — FALSIFIED` — see [`closures/Q-M1WIRE-1-closure-falsified.md`](closures/Q-M1WIRE-1-closure-falsified.md)
**Authored:** 2026-08-18
**Closed:** 2026-08-21
**Authors:** Joshua + Claude Code
**Parent question:** N/A — opened from the assumption-sweep audit note
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q — closure gated on three named $0/K=0 checks (a grep + artifact read, an unannounced operator drill, a validator run + gates.yml grep) returning clean or confirming the gap
**Artifact path:** `docs/briefs/Q-M1WIRE-1-arming-interlock-coverage.md`

---

## Section 0 — Rule 0 reads (production-source verification)

Every path below was read directly (by dedicated sweep/verify/triage agents, several independently spot-checked live) during the 2026-08-18 assumption-sweep workflow; existence re-confirmed 2026-08-18 for this brief. See `docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md` §4 (A2, A4, A5) and §9 for the source citations this section transcribes.

- `ops/c1_rail/c1_rail_telemetry.py:403-430` — `ExecutionStateStore.set_confirmed_base`.
- `ops/c1_rail/c1_sizing_host_reference.py:168-192,255-260,311-316` — `C1SizingHostReference.confirm_executed_base`.
- `tests/ops/test_m1_acceptance_drills.py`, `tests/ops/test_c1_sizing_host_reference.py`, `tests/ops/test_c1_rail_telemetry.py` — the only call sites for either method above.
- `ops/c1_rail/c1_rail_http_server.py:564-565,605-623` — reads the confirmed-base store; never writes it.
- `ops/c1_rail/c1_rail_telemetry.py:157-224` — `LoggingNotifier`, `FileAckNotifier` (M1's only two notification channels, both pull-based).
- `docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json` notes[3], item-10 evidence — the one reachability drill on record (operator fired the alert and immediately read it back).
- `docs/operational_rules.md` ~lines 65-97 — Rule 6 doc/code skew audit; no analogue exists for c1-rail/telemetry code.
- `ops/c1_rail/c1_rail_arm.py:79-117` — `m1_acceptance_reason`; validates the acceptance artifact's schema/status fields only.
- `scripts/gates.yml` — no `validate_c1_monitoring_acceptance` entry on any cadence.

---

## Section 1 — Context and motivation

The 2026-08-18 assumption-sweep audit note (`docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md`) surfaced three Tier-A findings (A2, A4, A5) that share one shape, named explicitly in the audit's own §6 cross-cutting pattern: the M1 acceptance package and its owning ADR describe live-safety capabilities in prose with more rigor than the arm interlock (`c1_rail_arm.py`, `m1_acceptance_reason`) mechanically checks. CLAUDE.md's live-execution posture states the arming interlock "validates the acceptance artifact via `validate_c1_monitoring_acceptance.validate(require_resolved=True)` — a forged or status-only artifact fails closed." That fix (2026-08-09) addressed forgery and missing-status; it did not address whether `RESOLVED` status itself still means what the package's constituent claims say it means. This Q tests exactly that gap, combining the three limbs the audit already scoped as one theme.

---

## Section 2 — Prior art / lineage

- `docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md` §4 (A2, A4, A5) and §6 — origin of all three limbs and the naming of the shared theme; §8 recommends promoting all six Tier-A items to formal Qs, with A2 named as sitting "directly upstream of the M1 arming gate's own credibility."
- Same audit's §3 D-gate deletions (already-covered items) — none overlap this Q's scope: item 4 (Sentinel Tier 2-3 quarterly probe) is a Hermes/Limb-B question, not M1; the CI/gates.yml items concern `check_pine_manifest.py` and session-log gates, not `validate_c1_monitoring_acceptance`. No re-litigation risk.
- Adjacent but explicitly out of scope: A3 (beta-death composition never reaches the sizing formula) and A6 (no per-trade dollar-loss cap) share the audit's §6 "prose vs wired" theme but were not supplied to this brief and are not folded in here — see Section 5.
- `docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md` (M1 ADR) — owns the acceptance package's frozen §10 audit hooks and the doctrine this Q tests against.

---

## Section 3 — Question (Q-M1WIRE-1)

**Q-M1WIRE-1:** Does the M1 arming interlock actually verify everything its own acceptance package and doctrine claim it verifies?

Symptom-only check: the question names no fix (no "should we wire X" or "should we add a push channel") — it asks only whether the existing certification's scope matches its claimed scope.

---

## Section 4 — Falsifiable hypothesis (H-M1WIRE)

**H-M1WIRE:** The arm interlock's `require_resolved=True` check (`c1_rail_arm.py:79-117`) is a sufficient proxy for "every capability the M1 acceptance package and doctrine describe as live is, in fact, wired and reachable" — tested against three named capabilities: (A2) the confirmed-base interlock has a live production write path; (A4) a fired CRITICAL alert reaches an attended-but-not-tailing operator; (A5) the acceptance artifact's pinned fixture-hashes are checked for drift on some cadence before arming. The proxy is sound only if **all three** hold; it is unsound wherever **any one** fails.

**Reject H-M1WIRE (assumption falsified — confirmed gap) if, for any limb:**
- **A2:** `rg -n "set_confirmed_base|confirm_executed_base" --type py` returns 0 hits outside `tests/ops/` **and** at least one of the two dry-fire artifacts (B6 2026-07-20, SIM 2026-07-27) shows a logged fill with `confirmed_base_qty` null/absent.
- **A4:** the unannounced self-drill records time-to-notice ≥ 10 minutes.
- **A5:** `grep -n validate_c1_monitoring_acceptance scripts/gates.yml` returns 0 hits **and** a read of `c1_rail_arm.py`'s arm path confirms it never calls `tree_skew()` / `--check-tree-skew`.

**Accept H-M1WIRE (assumption holds — proxy is sound) if all three clear:** a production call site for confirmed-base exists outside `tests/ops/` (or both dry-fire artifacts show populated `confirmed_base_qty`); the self-drill records time-to-notice < 10 minutes; **and** either `gates.yml` runs `--check-tree-skew` on some cadence or the arm interlock path itself invokes it before certifying `RESOLVED`.

**Ambiguous-hold if:** the A4 unannounced drill cannot be run this cycle without expectation-contamination (no operator window free of foreknowledge) while A2 and A5 both mechanically clear or both mechanically fail cleanly — hold pending a schedulable drill window; **or** A2/A5 return an unanticipated third state (e.g., an undocumented call site found outside both `tests/` and any known ops script) requiring a scoping judgment before that limb can be scored. Re-test window: next M1/c1-rail touch, per the audit note's own stop rule.

---

## Section 5 — Forbidden moves

- **Treating "the acceptance package exists and `require_resolved=True` is checked" as equivalent to "every capability the package describes is live-wired."** This is the exact comfortable-but-wrong move this Q exists to falsify — conflating schema/status validation with functional verification is precisely what the audit's §6 cross-cutting pattern names as the structural gap. Ruled out by definition: it is the null hypothesis under test, not a conclusion available for free.
- **Wiring the confirmed-base call sites (A2) or wiring the skew check into the arm interlock (A5) as a byproduct of this brief.** Tempting because the fix looks small once the gap is confirmed. Ruled out: this Q is diagnostic inventory, not a live-risk-surface change — CLAUDE.md's live-execution posture and the M1 ADR's frozen §10 hooks require any change here to go through its own pre-registration → re-derivation → admitting ADR, and discipline rule 6 forbids this brief from inventing spend beyond the supplied $0/K=0 falsifiers.
- **Running the A4 self-drill announced, or while tailing the log/polling the file.** Tempting because it is easier to schedule and to "prove" reachability cleanly. Ruled out: it would measure prepared attentiveness, not the ordinary-work condition the hypothesis is actually about — the same contamination the one existing drill (`M1_MONITORING_ACCEPTANCE.json` item-10) already committed, which is the reason A4 is unresolved rather than closed.
- **Folding A3 (beta-death composition) or A6 (per-trade cap) into this Q because they share the audit's §6 theme.** Tempting because all six Tier-A items were scored together and the "prose vs wired" pattern is real across all of them. Ruled out: only A2/A4/A5 were supplied to this brief; adding limbs mid-authoring is scope creep that would break the single-combined-H discipline and implicitly spend inventory depth beyond what was commissioned. A3/A6 remain separately promotable per the audit's own §8 routing.

---

## Section 6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition (typed) |
|---|---|---|
| `RESOLVED` | All three limbs (A2, A4, A5) clear per Section 4 Accept conditions | `INTEGRATE` — record the M1 package's confirmed-base/alert-reachability/skew-currency claims as verified-live; close audit findings A2/A4/A5 as stale/no-gap in the audit note's own tracking; no code or doctrine change owed. |
| `FALSIFIED` | ≥1 limb confirms its gap per Section 4 Reject conditions | `STOP` — `require_resolved=True` is confirmed insufficient to certify the failing capability/capabilities; re-proposal bar: any future claim that the M1 package "proves" that capability needs its own wiring evidence, not restated prose. Operator GO owed on whether to wire the confirmed gap(s) before the next arm attempt or to explicitly risk-accept them — that decision is not made by this brief. |
| `AMBIGUOUS-HOLD` | A4 drill unexecutable this cycle while A2/A5 clear (or both fail) cleanly, or an unanticipated third state on A2/A5 | `ITERATE` — name (do not open) a re-test window at the next M1/c1-rail touch per the audit note's stop rule; carry forward whichever limb(s) already resolved so the re-test only re-runs the unresolved limb. |

Pre-registered before any check runs; no amendment mid-investigation (Known Trap #12).

---

## Section 7 — Execution plan (self-executing, $0/K=0 — reuse the cheap-falsifier sketches supplied)

- **Phase 0 — Rule-0 reads.** Done (Section 0).
- **Phase 1a — Limb A2.** `rg -n "set_confirmed_base|confirm_executed_base" --type py` (expect 0 hits outside `tests/`); read the two dry-fire artifacts (B6 2026-07-20, SIM 2026-07-27) for a null `confirmed_base_qty` despite a logged fill.
- **Phase 1b — Limb A4.** Run one unannounced self-drill: fire a test CRITICAL alert through the existing `FileAckNotifier` path while doing ordinary unrelated work (not tailing the log/polling the file); time-to-notice with a stopwatch. Operator-executed; cannot be run by an agent.
- **Phase 1c — Limb A5.** `python scripts/validate_c1_monitoring_acceptance.py --check-tree-skew` (run now, against current `M1_MONITORING_ACCEPTANCE.json`); `grep -n validate_c1_monitoring_acceptance scripts/gates.yml` (expect 0 hits).
- **Phase 2 — Verdict assertion.** Apply Section 6 mechanically across the three limb results; produce the closure per Section 9.

Estimated cost: $0, K = 0. No new data pulls, no backtests — every step above is a grep, an artifact read, or a timed operator drill.

---

## Section 8 — Verdict pre-registration

Owed at operator GO, committed before Phase 1 executes: `docs/briefs/pre-registration/Q-M1WIRE-1-verdict-preregistration.md`, containing the Section 6 table verbatim plus the exact thresholds already stated in Section 4 (10-minute drill bound; 0-hits grep bound). Not yet authored — this Q is named, not opened.

---

## Section 9 — Closure record format

Per `references/closure_record.md`, with the mandatory typed `## Iterate` block, discharging the Section 6 Disposition column per limb.

- **If RESOLVED:** `docs/briefs/closures/Q-M1WIRE-1-closure-resolved.md` (no `recommendation.md` — no promotion action).
- **If FALSIFIED:** `docs/briefs/closures/Q-M1WIRE-1-closure-falsified.md`, naming which limb(s) confirmed and the operator decision owed per Section 6.
- **If AMBIGUOUS-HOLD:** `docs/briefs/closures/Q-M1WIRE-1-closure-ambiguous.md`, naming the unresolved limb(s) and the re-test window.

---

## Section 10 — Audit hooks (runnable)

```bash
# A2 — confirmed-base interlock production callers
rg -n "set_confirmed_base|confirm_executed_base" --type py
# expect: 0 hits outside tests/ops/
# then read the two dry-fire artifacts for a null confirmed_base_qty despite a logged fill
# (B6 2026-07-20 artifact; SIM 2026-07-27 artifact — paths per ops/c1_rail dry-fire records)

# A4 — alert reachability (operator-run, unannounced — not executable by an agent)
# fire a test CRITICAL alert through the existing FileAckNotifier path while doing
# ordinary unrelated work (not tailing the log/polling the file); time-to-notice with a stopwatch

# A5 — M1 tree-skew check, wiring to the arm interlock / any cadence
python scripts/validate_c1_monitoring_acceptance.py --check-tree-skew
grep -n "validate_c1_monitoring_acceptance" scripts/gates.yml
# expect: 0 hits (confirms no gates.yml cadence wiring)
```

---

## Verification

```bash
# Discipline checks (mechanical)
python scripts/check_brief.py docs/briefs/Q-M1WIRE-1-arming-interlock-coverage.md --type inquire
# Expected: all 6 checks PASS

# Production-source verification (Section 0 anchors)
rg -n "set_confirmed_base" ops/c1_rail/c1_rail_telemetry.py
rg -n "confirm_executed_base" ops/c1_rail/c1_sizing_host_reference.py
rg -n "class LoggingNotifier|class FileAckNotifier" ops/c1_rail/c1_rail_telemetry.py
rg -n "m1_acceptance_reason" ops/c1_rail/c1_rail_arm.py
grep -n "validate_c1_monitoring_acceptance" scripts/gates.yml

# Cross-reference verification (audit note is the grounding source)
rg -n "^\*\*A2\.|^\*\*A4\.|^\*\*A5\." docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md
```

If any verification command fails, this brief is not complete.

---

## Pre-Lock Checklist (DRAFT briefs only)

- [x] Section 0 paths read with anchors
- [x] Section 3 passes the symptom-only rephrase
- [x] Section 4 hypothesis binary
- [x] Section 5 forbidden moves genuinely tempting
- [x] Section 6 triggers specific
- [ ] Section 8 pre-registration committed before Phase 1 — owed at operator GO
- [x] Section 10 hooks runnable
- [ ] Operator GO owed before Phase 1 — this brief is named, not opened
