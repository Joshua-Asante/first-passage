# Q-S5CAP-1 — Does S5's capped concurrency hold at the system level, or only per-packet?

**Status:** `CLOSED-RESOLVED 2026-08-23` — validate_promotion_packet() and refute_promotion_packet() both Pass all 3 synthetic packets sequentially (cumulative concurrency_slots=3 > max_concurrency=2, zero rejections) — capped concurrency is a per-packet self-report, not a system invariant; successor Q-S5CAP-2 named (not opened). Closure: [`closures/Q-S5CAP-1-closure-resolved.md`](closures/Q-S5CAP-1-closure-resolved.md).
**Authored:** 2026-08-18
**Closed:** N/A
**Authors:** Joshua + Claude Code
**Parent question:** N/A — opened from the 2026-08-18 assumption-sweep audit note, finding B3
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q — closure gated on running the supplied cheap-falsifier packets against both admission functions, locally, at $0
**Artifact path:** `docs/briefs/Q-S5CAP-1-capped-concurrency-invariant.md`

---

## Section 0 — Rule 0 reads (production-source verification)

All six paths below share anchor `027a729` (2026-08-14, the public-repo remediation commit — verified `git log -1 --format="%h %ad" -- <path>` this session, each returning `027a729 2026-08-14`).

- `lab/discovery/promotion_packet.py:177` — `validate_promotion_packet()` delegates its only concurrency check to `_check_sandbox_ceilings(sandbox, ceilings)`.
- `lab/discovery/promotion_packet.py:217-246` (`_check_sandbox_ceilings`) — reads `concurrency = int(sandbox["concurrency_slots"])` out of the same packet under validation, then asserts `concurrency > int(ceilings["max_concurrency"])`. No parameter, import, or read touches any counter of candidates already active in the sandbox.
- `lab/discovery/promotion_refuter.py:23-68` (`refute_promotion_packet`) — after re-invoking `validate_promotion_packet` as a precondition, independently re-reads ceilings and re-checks `int(sandbox["concurrency_slots"]) > int(ceilings["max_concurrency"])` at line 68. Same pattern, same self-declared field, still no external counter.
- `lab/discovery/promotion_ceilings.json` — `max_concurrency: 2` is a static integer; the file's own comment: *"Hard ceilings read at promotion time (SPEC S5)."* A ceiling to compare against, not a mechanism that counts anything.
- `docs/adr/2026-08-07-loop-s5-bounded-promotion-lane.md` §1 — names the sandbox as bounded by three factors (`micro size · fixed per-candidate loss/attempt budget · capped concurrency`); capped concurrency is one of the three. §6 Consequences — *"S4 ledger: `PromotionEvent`/`DemotionEvent` TypedDict stubs documented; append wiring waits on M1 `RESOLVED`"* — the cross-packet state carrier this property would need is explicitly not yet wired.
- `tests/test_promotion_packet.py` — `grep -n -i "concurrency"` returns zero hits (re-run this session). No test exercises the concurrency ceiling at all, singly or across packets.
- `tests/fixtures/promotion/clean_packet.json` — the existing committed Pass fixture, `concurrency_slots: 1`, all cited artifact paths present under `tests/fixtures/promotion/artifacts/` (confirmed present this session). This is the fixture the cheap falsifier clones.

---

## Section 1 — Context and motivation

Origin: the 2026-08-18 assumption-sweep audit note (`docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md`), §4 Tier B, finding **B3**. The audit already read the production source directly (spot-checked again in Section 0 above) and found that both admission functions in the S5 bounded-promotion lane check `concurrency_slots` as a field the packet declares about itself, not as a count of anything actually running.

This matters because "capped concurrency" is not decoration — it is one of exactly three factors (`docs/adr/2026-08-07-loop-s5-bounded-promotion-lane.md` §1) the S5 ADR uses to bound the sandbox's blast radius, which is the justification for granting automation its one bounded exception to Call 5's "no autonomous promotion" invariant (`docs/methodology/strategy_lifecycle.md` §"Call 5 — The automation boundary"; the S5 ADR's own §0 names `docs/adr/2026-07-10-strategies-never-locked-lifecycle-governance.md` as Call 5's origin, referenced from CLAUDE.md's S5 pointer row). If the cap does not bind across packets, the worst-case exposure the ADR's argument rests on (2 concurrent slots × the \$250 per-candidate loss ceiling in `lab/discovery/promotion_ceilings.json`'s `max_loss_budget_usd` = \$500) is priced on a factor that may not be enforced at all.

---

## Section 2 — Prior art / lineage

- The audit note itself (`docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md` §4 B3) is the sole prior art — this brief transcribes it into governance shape, it does not re-derive it.
- §3 of the audit note ("D-gate deletions") lists the 5 findings the sweep's own adversarial-novelty pass killed with a citation before this brief was drafted. B3 is not among them — no existing ADR, closed Q, or brief already disposes of this finding, so there is no overlap to guard against.
- The S5 ADR (`docs/adr/2026-08-07-loop-s5-bounded-promotion-lane.md`) is the standing decision this Q tests a load-bearing premise of; it is not itself re-litigated here (Section 5).

---

## Section 3 — Question (Q-S5CAP-1)

**Pre-Q gate test (symptom-only rephrase):** the S5 lane's admission path is supposed to keep no more than `max_concurrency` candidates active in the sandbox at once; it is unknown whether that limit is checked against how many candidates are actually active, or only against a number each candidate's own packet asserts about itself. No fix is named — the question does not mention adding a counter, wiring the ledger, or any other remedy.

**Q-S5CAP-1:** When a sequence of promotion packets is run through the S5 admission path (`validate_promotion_packet()` then `refute_promotion_packet()`), does either function's `max_concurrency` check depend on the number of candidates concurrently active in the sandbox, or does each packet's admission decision depend only on the `concurrency_slots` value that packet itself declares?

---

## Section 4 — Falsifiable hypothesis (H-S5CAP)

Two named limbs, one code path each, same defect pattern:

- **Limb-V** (validator): `validate_promotion_packet()` / `_check_sandbox_ceilings()`.
- **Limb-R** (refuter): `refute_promotion_packet()`.

**H-S5CAP:** If **Limb-V holds** (`validate_promotion_packet()` returns `Pass` on all of N≥3 synthetic packets, each self-declaring `concurrency_slots=1`, run sequentially with no shared state between calls) **AND Limb-R holds** (`refute_promotion_packet()` also returns `Pass` on the same N≥3 packets, same sequence) — **then** the "capped concurrency" property is a per-packet self-report only, sequential admits silently exceed the declared `max_concurrency=2`, and the S5 ADR's blast-radius argument is currently missing its third factor as a system invariant. **If either function instead rejects a packet past the second** (i.e., some state persists across calls and the ceiling binds cumulatively), that limb is false and concurrency is enforced at the system level for that function.

**Reject H-S5CAP (defect NOT confirmed) if:** Limb-V or Limb-R Fails any packet beyond the 2nd in the sequence, for a reason attributable to cumulative concurrency (not an unrelated schema defect in the clone).
**Accept H-S5CAP (defect confirmed) if:** both Limb-V and Limb-R Pass all N≥3 packets, and code inspection (Section 0) confirms neither function reads or writes any state external to the single packet it is called with.
**Ambiguous-hold if:** the sequential run cannot complete cleanly at $0 — e.g., an unrelated schema field blocks a clone from validating, or repo state prevents `repo_root`-relative artifact resolution — such that neither Accept nor Reject can be asserted without spend beyond the supplied $0 falsifier.

---

## Section 5 — Forbidden moves

- **Treating `max_concurrency: 2` in `promotion_ceilings.json` as itself the enforcement mechanism.** It is a static input value a real counter would need to check against — not a counter. This is the exact conflation this Q exists to test; assuming the constant's presence proves the property would pre-decide the verdict before Phase 1 runs.
- **Proposing or sketching an EventLedger-backed counter fix under this brief.** The S5 ADR's own §6 already names ledger append-wiring as gated on M1 `RESOLVED`, and §3/§5 forbid automation editing the validator/refuter to change what it admits. A remedy is a superseding-ADR decision on separate authority, not something this Pre-Q — which is closure-only, $0/K=0 — has standing to design.
- **Reading an Accept verdict as "the sandbox has already been over-admitted."** No real (non-synthetic) packet sequence has run S5 admission to date (no discovery manifest under this lane is on record). Accept prices a **mechanism gap**, not a **realized incident** — conflating the two would misstate the finding's severity.
- **Substituting a different concurrency value or a larger N than the supplied N≥3 to "make it more convincing."** The falsifier is designed generous and cheap on purpose; inflating N adds no discriminating power (the mechanism either reads external state or it does not) and would be scope creep on a $0/K=0 brief.

---

## Section 6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition (typed) |
|---|---|---|
| `RESOLVED` (Accept H-S5CAP) | Both Limb-V and Limb-R Pass all N≥3 synthetic packets; Section 0 code reads confirm no cross-packet state anywhere in either call path | `INTEGRATE` — record "capped concurrency" as **per-packet self-report only, not a system invariant** in the S5 lifecycle owner/CLAUDE.md pointer row; name (do not open) a successor decision packet for whether/how a real counter is wired, gated on M1 `RESOLVED` per the ADR's own §6. No code changes under this brief. |
| `FALSIFIED` (Reject H-S5CAP) | Limb-V or Limb-R Fails a packet past the 2nd, for a concurrency-attributable reason | `STOP` — the property already binds at the system level for the failing function; close with the mechanism identified (it was missed by direct source read and needs correction to Section 0), and check whether the other limb still needs a separate verdict. |
| `AMBIGUOUS-HOLD` | Sequential run cannot complete cleanly at $0 (unrelated schema/path failure blocks the clone sequence) | `ITERATE` — record the blocking defect, fix the fixture-clone mechanics only (no production code), and re-run Phase 1 before any verdict is asserted. |

---

## Section 7 — Execution plan (self-executing, $0/K=0 — reuse the cheap-falsifier sketches supplied)

- **Phase 0 — Rule-0 reads.** Done (Section 0).
- **Phase 1 — Run the supplied cheap falsifier.** Clone `tests/fixtures/promotion/clean_packet.json` three times in a scratch file with distinct `candidate_id`/claim `claim_id` per clone (schema requires non-empty strings; no uniqueness constraint is checked by either function per Section 0, so this is cosmetic distinctness, not a confound to control for). Each clone keeps `concurrency_slots=1` (individually within `max_concurrency=2`). Call `validate_promotion_packet()` then `refute_promotion_packet()` on each clone **independently**, in sequence, in a local Python REPL. No repo mutation, no commit, no data pull. Record each call's `.decision`.
- **Phase 2 — Verdict assertion per Section 6.** All-Pass on both functions → Accept/`RESOLVED`. Any Fail attributable to concurrency → Reject/`FALSIFIED`. Anything else → `AMBIGUOUS-HOLD`.

Estimated cost: **$0, K = 0.** No backtest, no data pull, no new analysis beyond what Section 0 already read and Phase 1 runs.

---

## Section 8 — Verdict pre-registration

Owed at operator GO, committed **before** Phase 1 executes. Not yet authored — this brief is named, not opened, per the parent-Q convention stated in the Status line.

---

## Section 9 — Closure record format

Per `references/closure_record.md` (`.claude/skills/brief-authoring/references/closure_record.md`), with the mandatory typed `## Iterate` block. `RESOLVED` → `docs/briefs/closures/Q-S5CAP-1-closure-resolved.md`; `FALSIFIED` → `…-closure-falsified.md`; `AMBIGUOUS-HOLD` → `…-closure-ambiguous-hold.md` with the re-test trigger named.

---

## Section 10 — Audit hooks (runnable)

```bash
# The static ceiling is still what it was read as in Section 0
grep -n "max_concurrency" lab/discovery/promotion_ceilings.json    # expect: "max_concurrency": 2

# No concurrency test coverage exists yet (confirms the Section 0 gap read)
grep -n -i "concurrency" tests/test_promotion_packet.py            # expect: no hits

# Phase 1 — the cheap falsifier itself (run from repo root, local Python REPL)
python - <<'PY'
import json, copy
from pathlib import Path
import sys
sys.path.insert(0, "lab")
from discovery.promotion_packet import validate_promotion_packet
from discovery.promotion_refuter import refute_promotion_packet

base = json.loads(Path("tests/fixtures/promotion/clean_packet.json").read_text())
assert base["sandbox"]["concurrency_slots"] == 1

results = []
for i in range(3):
    pkt = copy.deepcopy(base)
    pkt["candidate_id"] = f"synth-s5cap-{i}"
    pkt["claims"][0]["claim_id"] = f"stage2_clear_{i}"
    pkt["claims"][1]["claim_id"] = f"bust_clear_{i}"
    v = validate_promotion_packet(pkt, repo_root=".")
    r = refute_promotion_packet(pkt, repo_root=".")
    results.append((pkt["candidate_id"], v.decision, r.decision))

for candidate_id, v_decision, r_decision in results:
    print(candidate_id, "validate=", v_decision, "refute=", r_decision)
# Accept H-S5CAP if all three print validate=Pass refute=Pass
PY
```

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/Q-S5CAP-1-capped-concurrency-invariant.md --type inquire
grep -n "max_concurrency" lab/discovery/promotion_ceilings.json
sed -n '217,246p' lab/discovery/promotion_packet.py
sed -n '23,69p' lab/discovery/promotion_refuter.py
grep -n "capped concurrency\|not RESOLVED\|append wiring" docs/adr/2026-08-07-loop-s5-bounded-promotion-lane.md
```

---

## Addendum 2026-08-29 — §0 anchor-provenance correction

**Does not amend §0–§10.** §0 states "All six paths below share anchor `027a729` (2026-08-14)."
Per the closure's own §4 table
([`Q-S5CAP-1-closure-resolved.md`](closures/Q-S5CAP-1-closure-resolved.md) §4), re-verified
per-path at Phase 1 execution (2026-08-23): 2 of the 6 cited paths —
`lab/discovery/promotion_packet.py` and `tests/test_promotion_packet.py` — had moved to commit
`1eb1237` (2026-08-19, an unrelated `discovery_run_id`/K-ledger-backing change; zero new
concurrency coverage). The other 4 cited paths remain at `027a729`. This does not affect the
`RESOLVED` finding — it corrects only the Section 0 provenance claim.

---

## Pre-Lock Checklist (DRAFT briefs only)

- [x] Section 0 paths read with anchors
- [x] Section 3 passes the symptom-only rephrase
- [x] Section 4 hypothesis binary (both limbs Pass ⇒ Accept; either Fails past packet 2 ⇒ Reject)
- [x] Section 5 forbidden moves genuinely tempting
- [x] Section 6 triggers specific
- [ ] Section 8 pre-registration owed at operator GO
- [x] Section 10 hooks runnable
- [x] Operator GO given; Phase 1 ran 2026-08-23 — see [`Q-S5CAP-1-closure-resolved.md`](closures/Q-S5CAP-1-closure-resolved.md)
