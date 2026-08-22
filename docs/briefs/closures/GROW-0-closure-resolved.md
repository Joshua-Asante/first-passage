# GROW-0 — CLOSURE: `RESOLVED` (engine + calibration instrument sound)

**Verdict:** `RESOLVED` — Limb A ∧ Limb B PASS at the PREREG-pinned N=5,500/c=7 design; all
three RED tokens `FAILED_AS_EXPECTED`; machine-readable and independently reproduced
**Closed:** 2026-08-22
**Lane:** UNASSIGNED (GROW-0 is explicitly outside the deep-iteration lane charter's §4
counters — [build-authorization ADR](../../adr/2026-08-22-grow-lane-build-authorization.md) §2.1)
**Pre-registration:** [`2026-08-22-grow-0-synthetic-calibration-prereg.md`](../pre-registration/2026-08-22-grow-0-synthetic-calibration-prereg.md)
`FROZEN`, frozen at `e21e803` (`e21e80334c01e5c3334d997c7afbe158c5015697` — `git log -1` on the
prereg file at run time)
**Spend / K:** $0.00 · K=0 — synthetic data only, no Databento pull, no live-risk surface
**Live effect:** none — rail unaffected, disarmed, no book
**Artifacts:** [`lab/discovery/grow0_harness.py`](../../../lab/discovery/grow0_harness.py) ·
[`grow0_dgp.py`](../../../lab/discovery/grow0_dgp.py) ·
[`grow0_scoring.py`](../../../lab/discovery/grow0_scoring.py) ·
[`grow0_red_patch.py`](../../../lab/discovery/grow0_red_patch.py) ·
[`discovery_manifests/grow0_retry_ledger.jsonl`](../../../discovery_manifests/grow0_retry_ledger.jsonl)
(run_id `grow0-real-20260822T211844Z`) ·
[implementation plan](../../superpowers/plans/2026-08-22-grow0-harness-implementation.md) Task 13
Step 7 (the manual invocation this closure discharges)

---

## 1. Verdict (§6.7 asserted against actual numbers)

| §6.7 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` | Limb A PASS ∧ Limb B PASS ∧ all three RED tokens `FAILED_AS_EXPECTED` | Limb A `PASS` (nominee=5, confirm_stat=3.8200 ≥ floor 1.265) · Limb B `PASS` (sum_clears=5/5500, c=7) · red_leak `FAILED_AS_EXPECTED` (sum_clears=29/5500 ≥ c=7) · red_blind `FAILED_AS_EXPECTED` · red_patch `FAILED_AS_EXPECTED` | ✓ |
| `FALSIFIED` | Any RED control reports its own check `PASSED_UNEXPECTEDLY` (no power), **or** with all three RED green-side, Limb A `FAIL` or Limb B `FAIL` | None of these — every RED control fired correctly and both limbs passed | — |

Raw command + output (`PYTHONPATH=lab python -m discovery.grow0_harness --run-id
grow0-real-20260822T211844Z --started-at 2026-08-22T21:18:44Z --prereg-commit
e21e80334c01e5c3334d997c7afbe158c5015697`, 27.8s wall-clock):

```json
{
  "run_id": "grow0-real-20260822T211844Z",
  "started_at_arg": "2026-08-22T21:18:44Z",
  "prereg_commit": "e21e80334c01e5c3334d997c7afbe158c5015697",
  "limb_b_n": 5500,
  "limb_b_c": 7,
  "limb_a": "PASS",
  "limb_b": "PASS",
  "red_leak": "FAILED_AS_EXPECTED",
  "red_blind": "FAILED_AS_EXPECTED",
  "red_patch": "FAILED_AS_EXPECTED",
  "overall": "RESOLVED"
}
```

Appended once, verbatim, to `discovery_manifests/grow0_retry_ledger.jsonl` (prereg §6.6 — the
first line that file has ever contained; the harness's own `run_grow0` writes exactly one entry
per invocation, confirmed by the ledger having exactly one line after this run).

## 2. What the pre-registration predicted vs what happened

No surprises against the frozen §3/§4 design; every limb's actual count sits inside the
distribution the prereg's own pre-run calibration named:

- **Limb A** (§3 "Why SR=4.0"): predicted confirm-clear probability ≈1.00000000 at the planted
  SR=4.0 edge (deterministic-in-practice). Actual: nominee correctly recovered θ\* (index 5),
  confirm statistic 3.8200 cleared the floor with ~3× margin. No surprise.
- **Limb B** (§4): predicted null-clear rate `nominal_p0=0.00059070` implies an expected
  ≈3.25 clears across 5,500 panels (`0.00059070 × 5500`). Actual: **5** clears — within one
  standard deviation of that expectation (binomial sd ≈ 1.80 at this n/p) and comfortably under
  the `c=7` FAIL threshold. No surprise; PASS as designed.
- **RED-LEAK** (§6.3): predicted closed-form leak rate `p_leak = 1-(1-nominal_p0)^10 = 0.005891`
  implies an expected ≈32.4 clears (`0.005891 × 5500`). Actual: **29** clears — within one sd
  (≈5.68) of expectation, and far above `c=7`, so the rigged run correctly makes Limb B's own
  binomial check report FAIL (`FAILED_AS_EXPECTED`, i.e. the calibration check has power to
  detect a real leak). No surprise.
- **RED-BLIND** and **RED-PATCH** fired exactly as their v3/standalone mechanisms are designed to
  (structural impossibility for RED-BLIND; the M-23 parent-only-patch bug reproduced and was
  caught by the attestation guard for RED-PATCH) — both deterministic-by-construction, so a
  single frozen-seed run is sufficient per the prereg's own design (§6.4/§6.5), not a
  probabilistic claim needing repeat draws.
- All five results were **independently re-derived** in this session by calling
  `run_limb_a`/`run_limb_b`/`run_red_leak`/`run_red_blind`/`run_red_patch` directly (bypassing
  `run_grow0`'s aggregation) — the frozen `SeedSequence` root (`20260822`) makes the whole design
  deterministic, and the re-derivation reproduced every token and the exact Limb B / RED-LEAK
  counts bit-for-bit. This is a genuine second, independent computation of the same frozen inputs,
  not a re-read of the first run's own output.

**Amendment-first / dedup (re-run this session):**
```
$ grep -rlniE "grow-?0.*real|grow0.*resolved|grow0.*falsified" docs/briefs/closures/ docs/SESSIONS.md
(no output before this closure was authored — no prior GROW-0 real-scale verdict on record)
```

## 3. What this closure does NOT license

- Opening a GROW-1 (or any) real deep-lane campaign — that is a fresh operator GO under the
  charter's own Q-ID/prereg/confirm-read discipline; this closure validates the *engine*, not any
  strategy family.
- Filing the Part B "two-ledger K question" ADR — the GROW spec v2 Part B gate names this
  closure's RESOLVED verdict as the *precondition* for that filing decision to go to the operator,
  not as the filing itself. No Part B ADR is authored here.
- Treating any future `--lane deep` campaign as exempt from its own fresh
  `deep_lane_admission.py` check (build ADR §5, imported verbatim — GROW-0 validates the engine
  once; every campaign still runs the admission check itself).
- Claiming N-SHAPE or N-SURV coverage — the prereg's own §1 scope boundary (a single daily P&L
  value has no intraday position object to violate; N-SURV's bust/pass channel answers a
  different question) is unchanged by this run.
- Reading the CRLF/`.gitattributes` fix (§4 below) as a change to any frozen prereg number — the
  grammar file's *content* (K=10, the 10 `session_offset_min` values) never differed from what
  the prereg §2 pins; only the on-disk line-ending bytes of a Windows checkout did.

## 4. Defects found (recorded, not repaired against the frozen prereg text)

**Not a prereg defect — a build-artifact defect, found and fixed before the real run, recorded
here since it directly gated whether this closure could be authored honestly.** Running the
grow0 test suite pre-invocation (`PYTHONPATH=lab pytest tests/test_grow0_*.py`) surfaced 1 of 39
tests failing: `test_grow0_grammar_matches_prereg_section_2` reported a SHA256 mismatch against
`discovery_manifests/grow0_grammar.json`. Root cause: this Windows checkout has
`core.autocrlf=true`, which rewrites the committed LF-blob bytes to CRLF on checkout — the exact
class of bug `.gitattributes` already carries four prior pins for (test fixtures, M1 acceptance,
WAVE1 CSVs, the container-build files). `git show HEAD:discovery_manifests/grow0_grammar.json`
confirmed the repo-stored blob is byte-identical in content to the working-tree file, differing
only in `\n` vs `\r\n`. Fixed by adding a fifth pin
(`discovery_manifests/grow0_grammar.json text eol=lf`) to `.gitattributes` and renormalizing the
working-tree file to LF — hash now matches the prereg-pinned literal
(`89383a593a3a5c80f6e1973c3c3cffdfa65a0d0c620fccd92c3a1f9c031f499f`) exactly, all 39 tests green.
**No content of the frozen grammar (K=10, the `session_offset_min` value list) was ever wrong or
touched.**

## 5. Lesson candidates

Below the two-incident-or-$3K bar for this specific file, but the **class** is now a 5th
occurrence in this repo's own `.gitattributes` history (test fixtures 2026-07-31 · M1 acceptance
· WAVE1 CSVs · container-build files · this file). Watch, not yet load-bearing: any new
hash-pinned artifact (a frozen grammar, a manifest, a fixture) should get its `eol=lf` pin
authored in the **same commit** that introduces the hash pin, not discovered reactively on the
next Windows checkout that runs the test. If a sixth instance fires, this graduates.

## Iterate — loop exit

- **Verdict used:** `RESOLVED`
- **Model update:** The GROW-0 harness build (2026-08-22, session `l`) shipped 37–39 unit tests
  green at small-N scale but had never exercised its own frozen N=5,500/c=7 design — this was
  the one gap named explicitly in that session's own Open/next line. That gap is now closed: the
  search→confirm plumbing (grammar → DGP → nomination → gate → confirm → ledger) is validated at
  its real frozen scale, with an independent re-derivation confirming the result is not an
  artifact of `run_grow0`'s own aggregation code.
- **Next:** INTEGRATE
- **Routing:** commit (a) the `.gitattributes` CRLF-pin fix + renormalized grammar file, (b) the
  real ledger entry (`discovery_manifests/grow0_retry_ledger.jsonl`, one line), (c) this closure,
  (d) a `docs/SESSIONS.md` entry recording the real verdict, (e) the build-authorization ADR's
  §7 implementation log (GROW-0 harness slice now includes its own real-run discharge) — each a
  state-flip against a decision this repo's own doctrine already made (the build ADR and the
  GROW spec v2 Gate), not a fresh decision itself. Re-validation: §10 below.
- **Entry packet:** n/a (Next = INTEGRATE)
- **Stop rule / re-proposal bar:** n/a — integrated. (GROW-0 itself does not reopen absent a
  future defect in the harness code discovered post-hoc — per the prereg's own §5, a post-GO
  defect found later supersedes with a fresh ledgered PREREG and fresh run, it does not revise
  this closure in place.)
- **Board write:** `SESSIONS Open/next: GROW-0 RESOLVED at real scale (run_id
  grow0-real-20260822T211844Z, 2026-08-22) — engine + calibration instrument validated. First
  real deep-lane campaign (GROW-1 or later) may now open via --lane deep. GROW spec v2 Part B's
  two-ledger K question filing decision is unlocked for the operator (not decided here; no ADR
  filed).` Owner: this closure · [build ADR](../../adr/2026-08-22-grow-lane-build-authorization.md)
  · [GROW spec v2](../../spec/2026-08-22-grow-lane-generate-refine-spec.md) Part B.
- **Registry:** n/a — RESOLVED / engine-validation gate, not a strategy admission or a
  campaign-grounds kill; no `lab/CATALOG.md` / `docs/rejected_candidates.md` entry owed.

## §10 audit-hook discharge

```bash
$ PYTHONPATH=lab pytest tests/test_grow0_dgp.py tests/test_grow0_scoring.py \
    tests/test_grow0_harness.py tests/test_grow0_red_patch.py tests/test_grow0_grammar_file.py -q
39 passed in 13.23s

$ PREREG_COMMIT="$(git log -1 --format=%H -- docs/briefs/pre-registration/2026-08-22-grow-0-synthetic-calibration-prereg.md)"
$ PYTHONPATH=lab python -m discovery.grow0_harness --run-id grow0-real-20260822T211844Z \
    --started-at 2026-08-22T21:18:44Z --prereg-commit "$PREREG_COMMIT"
# → overall: RESOLVED (full JSON in §1 above); real wall-clock 27.8s

$ cat discovery_manifests/grow0_retry_ledger.jsonl
# → exactly one line, matching the printed JSON above verbatim

# Independent re-derivation (separate process, same frozen seed tree):
$ PYTHONPATH=lab python -c "
from discovery.grow0_harness import run_limb_a, run_limb_b, run_red_leak, run_red_blind
from discovery.grow0_red_patch import run_red_patch
print(run_limb_a()[0])            # PASS
print(run_limb_b()[:2])           # ('PASS', 5)
print(run_red_leak())             # FAILED_AS_EXPECTED
print(run_red_blind())            # FAILED_AS_EXPECTED
print(run_red_patch())            # FAILED_AS_EXPECTED
"
# → bit-identical to the run_grow0 aggregate above

python scripts/check_closure_disposition.py docs/briefs/closures/GROW-0-closure-resolved.md
# Expected: OK — Iterate block tokens present.
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-22 | Closure authored — first real full-scale GROW-0 run, `RESOLVED` | Claude Code (operator session) |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/GROW-0-closure-resolved.md
```
