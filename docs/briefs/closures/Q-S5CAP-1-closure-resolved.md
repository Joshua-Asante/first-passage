# Q-S5CAP-1 — CLOSURE: `RESOLVED` (capped concurrency is a per-packet self-report, not a system invariant)

**Verdict:** `RESOLVED` (Accept H-S5CAP) — both Limb-V and Limb-R Pass all N=3 synthetic
packets, sequential, cumulative `concurrency_slots`=3 > `max_concurrency`=2, zero rejections;
Section 0 code inspection confirms neither call path reads or writes any state external to
the single packet argument.
**Closed:** 2026-08-23
**Lane:** UNASSIGNED (governance/mechanism-audit Q, not a strategy-validation lane)
**Pre-registration:** [`Q-S5CAP-1-verdict-preregistration.md`](../pre-registration/Q-S5CAP-1-verdict-preregistration.md)
— `FROZEN`, criteria transcribed verbatim from the brief's own §6 (locked 2026-08-18); frozen
at `52c3648` (repo HEAD at Phase 1 execution time, 2026-08-23)
**Successor:** `Q-S5CAP-2` (working title) — wire a real cross-packet concurrency counter for
S5 admission, or decide the sandbox does not need one; **named, not opened**, gated on M1
`RESOLVED` per the S5 ADR's own §6
**Spend / K:** $0.00 · K=0 — three synthetic packet clones through the existing local
validators, no data pull, no new analysis
**Live effect:** none — rail unaffected, disarmed throughout; no `core/`, allocation,
`dd_protection`, Pine, or rail byte modified; no S5 sandbox candidate exists to be affected
**Artifacts:** the three synthetic clones existed only as in-process `dict` objects during
this session (§5 of the brief forbids repo mutation) — the reproducing script is pasted
verbatim in §10 below; base fixture
[`tests/fixtures/promotion/clean_packet.json`](../../../tests/fixtures/promotion/clean_packet.json)

---

## 1. Verdict (§6 asserted against actual numbers)

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` (Accept H-S5CAP) | Both Limb-V and Limb-R Pass all N≥3 synthetic packets; Section 0 code reads confirm no cross-packet state anywhere in either call path | Limb-V: Pass/Pass/Pass (3/3); Limb-R: Pass/Pass/Pass (3/3); code inspection of `_check_sandbox_ceilings()` (`promotion_packet.py:234-262`), `validate_promotion_packet()` (`promotion_packet.py:112-231`), and `refute_promotion_packet()` (`promotion_refuter.py:23-98`) finds only immutable module-level constants, zero `global`/`nonlocal`, zero file writes, zero counters/caches/registries in either module | ✓ |
| `FALSIFIED` (Reject H-S5CAP) | Limb-V or Limb-R Fails a packet past the 2nd, for a concurrency-attributable reason | Zero Fails occurred at all, on either function, on any of the 3 packets | — |
| `AMBIGUOUS-HOLD` | Sequential run cannot complete cleanly at $0 | Ran clean on the first attempt, from repo root, no schema/path failure, all cited fixture artifacts present | — |

Raw output (brief's own §10 script, run verbatim this session, repo root):
```
synth-s5cap-0 validate= Pass () refute= Pass ()
synth-s5cap-1 validate= Pass () refute= Pass ()
synth-s5cap-2 validate= Pass () refute= Pass ()
```

## 2. What the pre-registration predicted vs what happened

No surprises. The pre-registration (and the brief's own §4/§6, frozen 2026-08-18) named
`RESOLVED` as the mechanically-expected route given the Section-0 source reads already on
record; this session's Phase 1 run exists to convert "read the source and infer" into "ran it
and watched." It confirmed exactly what the static reads implied: `_check_sandbox_ceilings()`
and its refuter counterpart each independently re-derive the same two facts — the packet's
own declared `concurrency_slots` and the static `max_concurrency` ceiling — and compare them,
with nothing in between to remember packet N-1 by the time packet N is checked. Cumulative
concurrency across the 3-packet sequence (3, versus a ceiling of 2) was never computed by
either function, so nothing rejected it.

## 3. What this closure does NOT license

- **Reading this as a realized over-admission incident.** No real (non-synthetic) promotion
  packet has ever run S5 admission — confirmed this session: zero files matching
  `*promotion*packet*.json` exist outside `tests/fixtures/`, zero `discovery_manifests/`
  entries reference the S5 lane, and `PromotionEvent(`/`DemotionEvent(` are never
  instantiated anywhere outside their own `TypedDict` class bodies. This closure prices a
  **mechanism gap**, exactly as the brief's own §5 forbidden-move #3 requires.
- **Proposing or sketching the counter fix itself.** Per §5 forbidden-move #2 and the S5
  ADR's own §6, ledger append-wiring is gated on M1 `RESOLVED`; this closure names a
  successor packet (above) and stops there.
- **Treating `promotion_ceilings.json`'s `max_concurrency: 2` as itself an enforcement
  mechanism.** It remains exactly what §0/§5 said it was — a static comparison value, not a
  counter — confirmed by the §1 table row above.
- **Treating the brief's Section 0 "shared anchor `027a729`" line as still accurate.** See §4
  below — two of the six cited paths have moved since the brief was authored. The finding
  itself is unaffected; the provenance line is stale and is recorded, not silently carried
  forward.

## 4. Defects found in the frozen brief (recorded, not repaired)

**Section 0 anchor staleness (cosmetic to the verdict, real as a provenance claim).** The
brief states "All six paths below share anchor `027a729` (2026-08-14)." Re-verified this
session via `git log -1 --format="%h %ad" -- <path>` run **per-path** (a single multi-path
call silently collapses to the latest touch across all paths and would have masked this):

| Path | Brief's claimed anchor | Actual anchor (this session) |
|---|---|---|
| `lab/discovery/promotion_packet.py` | `027a729` 2026-08-14 | `1eb1237` 2026-08-19 |
| `lab/discovery/promotion_refuter.py` | `027a729` 2026-08-14 | `027a729` 2026-08-14 (unchanged) |
| `lab/discovery/promotion_ceilings.json` | `027a729` 2026-08-14 | `027a729` 2026-08-14 (unchanged) |
| `docs/adr/2026-08-07-loop-s5-bounded-promotion-lane.md` | `027a729` 2026-08-14 | `027a729` 2026-08-14 (unchanged) |
| `tests/test_promotion_packet.py` | `027a729` 2026-08-14 | `1eb1237` 2026-08-19 |
| `tests/fixtures/promotion/clean_packet.json` | `027a729` 2026-08-14 | `027a729` 2026-08-14 (unchanged) |

Root cause: commit `1eb1237` ("feat(discovery): Option E — deterministic
pre-registration/promotion gates for a3/a4", 2026-08-19) added an unrelated optional
`discovery_run_id`/K-ledger-backing check to `promotion_packet.py` (lines 181-194, gated on
`raw.get("discovery_run_id")` — none of the 3 synthetic clones declare that optional field,
so this path never triggers here) plus 4 new paired tests to `tests/test_promotion_packet.py`,
all about `discovery_run_id`/K-ledger backing, zero new concurrency coverage (re-confirmed:
`grep -n -i concurrency tests/test_promotion_packet.py` still returns zero hits post-`1eb1237`).
**The finding is not affected; the anchor-provenance line in Section 0 is now wrong and
should be corrected if this brief is ever re-read as a citation source**, per this repo's own
`verify_content_not_path_or_id` discipline.

## 5. Lesson candidates

Below the two-incident bar — watch, not yet load-bearing. A brief's own multi-path Section-0
"shared anchor" line can go stale between authoring and execution without the brief's
factual claims going stale. If a second dated instance of this specific pattern surfaces,
this graduates: **re-verify Section-0 anchors per-path (not one multi-path `git log` call)
immediately before Phase 1, not only at authoring time.**

## Iterate — loop exit

- **Verdict used:** `RESOLVED`
- **Model update:** The 2026-08-18 audit note's B3 finding (source-read only) is now
  execution-confirmed: "capped concurrency" in the S5 bounded-promotion lane is a per-packet
  self-report, not a system invariant, on both the validator and refuter paths. The S5 ADR's
  blast-radius argument (2 slots × $250 = $500 worst case) currently rests on a factor
  (`max_concurrency`) that is checked but never counted across packets — the $500 figure
  describes what a *single* admitted packet is capped at, not what a *sequence* of admitted
  packets is capped at.
- **Next:** INTEGRATE
- **Routing:** (a) this closure; (b) the pre-registration file (frozen before Phase 1 per its
  own process note); (c) a `docs/briefs/INDEX.md` row move from Open to Recently-closed
  (drafted separately); (d) two doc pointer-row edits per the frozen §6 `RESOLVED`
  disposition — `docs/methodology/strategy_lifecycle.md` (the Call-5 capped-sandbox
  description, near its "capped concurrency" phrase) and `CLAUDE.md`'s S5 pointer row — both
  get a short parenthetical: *"capped concurrency is a per-packet self-report only, not a
  cross-packet system invariant (Q-S5CAP-1, RESOLVED 2026-08-23)."* Exact edit text not
  applied in this session (read-only checkout); owed as a follow-up docs commit. (e)
  `docs/SESSIONS.md` entry recording the verdict. (f) name (do not open) `Q-S5CAP-2` as the
  successor counter-or-decline decision packet, gated on M1 `RESOLVED`. No code changes —
  none owed, none made.
- **Entry packet:** *(for the named-not-opened `Q-S5CAP-2` successor)* — carry forward: this
  closure's §1 numbers (Pass/Pass/Pass ×3, zero cross-packet state found); the S5 ADR's §6
  gate on ledger wiring (M1 `RESOLVED` precondition); the confirmed absence of any real S5
  promotion packet to date (§3 above, so no urgency argument from a realized incident);
  forbidden re-opens: do not re-run this Q's own N=3 falsifier at a larger N (§5
  forbidden-move #4 — it would add no discriminating power); budget for the successor is
  undetermined (governance-design decision, not yet costed).
- **Stop rule / re-proposal bar:** n/a — integrated. The underlying mechanism gap does not
  resolve itself; `Q-S5CAP-2` (or an operator decision to accept the gap permanently) is the
  only thing that changes this finding, and that is a fresh operator GO, not a re-proposal
  bar on this closure.
- **Board write:** `SESSIONS Open/next: Q-S5CAP-1 RESOLVED 2026-08-23 — S5's "capped
  concurrency" is a per-packet self-report on both validate_promotion_packet() and
  refute_promotion_packet(), not a cross-packet system invariant; zero real S5 promotions
  exist to date so this is a mechanism gap, not a realized incident. Successor Q-S5CAP-2
  (wire a real counter, or decide not to) named, not opened, gated on M1 RESOLVED.` Owner:
  this closure · [S5 ADR](../../adr/2026-08-07-loop-s5-bounded-promotion-lane.md) §6.
- **Registry:** n/a — RESOLVED / governance-mechanism-audit verdict, not a strategy admission
  or a strategy-grounds kill; no `lab/CATALOG.md` / `docs/rejected_candidates.md` entry owed.

## §10 audit-hook discharge

```bash
$ grep -n "max_concurrency" lab/discovery/promotion_ceilings.json
6:  "max_concurrency": 2,

$ grep -n -i "concurrency" tests/test_promotion_packet.py
# -> no hits (re-confirmed post-2026-08-19 "Option E" commit 1eb1237; see §4 above)

$ python - <<'PY'
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
PY
synth-s5cap-0 validate= Pass refute= Pass
synth-s5cap-1 validate= Pass refute= Pass
synth-s5cap-2 validate= Pass refute= Pass

$ grep -n "capped concurrency\|not RESOLVED\|append wiring" docs/adr/2026-08-07-loop-s5-bounded-promotion-lane.md
33:...(micro size (dot) fixed per-candidate loss/attempt budget (dot) capped concurrency)...
112:- S4 ledger: `PromotionEvent` / `DemotionEvent` TypedDict stubs documented; append wiring waits on M1 `RESOLVED`.
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-23 | Closure authored — Phase 1 run under operator GO, `RESOLVED` | Claude Code (subagent session) |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/Q-S5CAP-1-closure-resolved.md
python scripts/check_brief.py docs/briefs/Q-S5CAP-1-capped-concurrency-invariant.md --type inquire
```
