# Frozen 1H DOL target — distance sweep — `AMBIGUOUS` (null across the whole tested range)

**Date:** 2026-08-20 · **Cost:** $0.00 · **K:** 0 (zero-run, disclosure-only counterfactual — no new
entry construct, reuses `Q-ICT-OTE-1`/`Q-ICT-OB-1`'s already-licensed, already-run entry+stop logic
unchanged)
**Class:** excursion-bounded counterfactual (`strategy-validation` skill §3 — the same technique that
killed `ORB-MNQ-1`'s exit-redesign space at zero runs)
**Occasioned by:** operator instruction, 2026-08-20 — following `Q-ICTEXP-1`, `Q-ICT-OTE-1`, and
`Q-ICT-OB-1` all dying anchored to the identical frozen 1H range-extreme DOL target, whether the target
itself (not the entry) is the shared point of failure.
**Runner:** [`run_target_distance_sweep.py`](run_target_distance_sweep.py) · **Raw:**
[`RESULTS.json`](RESULTS.json) (gitignored machine record)

---

## Method

Reuses `Q-ICT-OTE-1`'s sweep→leg→Fib-zone entry and `Q-ICT-OB-1`'s displacement→last-opposing-candle
entry — both already licensed via their own operator-override ADRs and already run to `FALSIFIED` —
byte-verified against the originals (see Defect below). Instead of exiting at the first of {DOL target,
stop, session-flat}, this walks the same identified entries to the earlier of {stop, session-flat} and
records the running **max favorable excursion (MFE)** at every bar. That is sufficient to answer, for
any candidate target distance **≤** what the path could show before truncation, whether that target
would have been hit before the stop — entirely from data already generated, no new panel scan logic,
no new entry rule.

**Explicit limit (stated before any number existed):** this can only test target distances up to what
the observed path (to stop or session-flat) already reveals. A *farther* target than what MFE reached
is not observable this way — not attempted; the grid below (5–300pt) already brackets both entries' own
stop scale (13–15pt) and the DOL target's own measured mean distance (263–285pt), so no meaningful gap
is left untested.

---

## Defect caught before trusting any number (worth keeping)

The first draft of this script's entry-detection reuse for `Q-ICT-OTE-1` **undercounted real entries**
(1,257 vs. the already-recorded 1,675) because it gave up after the *first* qualifying pivot's
touch-search failed, instead of trying every pivot in the session — a genuine transcription error
against `first_ote_trade`'s actual control flow (verified via `inspect.getsource`, not memory: there is
no early `return None` inside that function's outer pivot loop). Fixed before any target-grid number was
trusted; re-verified byte-identical to the original (`mean stop_dist = 13.164776119402985`, matching to
15 significant figures). `Q-ICT-OB-1`'s reuse had no such bug (verified n=995 exact match immediately).
This is the same class of catch this corpus's own pre-data-test discipline exists for — caught here by
cross-checking against the already-recorded result, not by a pre-written unit test, which is itself a
gap worth naming: this script has no dedicated test file, unlike every G0-grade construct in this
corpus. Acceptable for a zero-K disclosure pass; would not be acceptable at G0.

---

## Result — target-distance sweep, both entries, both arms pooled

| Target (pt) | OTE n | OTE mean R | OTE 95% CI | OTE hit rate | OB n | OB mean R | OB 95% CI | OB hit rate |
|---:|---:|---:|---|---:|---:|---:|---|---:|
| 5 | 1675 | −0.434 | [−0.490, −0.377] | 56.4% | 995 | −0.338 | [−0.416, −0.259] | 62.9% |
| 10 | 1675 | −0.392 | [−0.468, −0.306] | 45.1% | 995 | −0.330 | [−0.416, −0.242] | 51.2% |
| 15 | 1675 | −0.402 | [−0.482, −0.319] | 37.7% | 995 | −0.317 | [−0.410, −0.214] | 42.6% |
| 20 | 1675 | −0.399 | [−0.489, −0.305] | 32.4% | 995 | −0.283 | [−0.386, −0.168] | 37.8% |
| 30 | 1675 | −0.405 | [−0.515, −0.287] | 24.8% | 995 | −0.277 | [−0.404, −0.146] | 29.5% |
| 50 | 1675 | −0.422 | [−0.532, −0.305] | 17.6% | 995 | −0.210 | [−0.371, −0.041] | 20.7% |
| 75 | 1675 | −0.423 | [−0.558, −0.287] | 12.5% | 995 | −0.199 | [−0.385, **+0.012**] | 14.6% |
| 100 | 1675 | −0.460 | [−0.600, −0.310] | 9.6% | 995 | −0.205 | [−0.410, **+0.033**] | 10.8% |
| 125 | 1675 | −0.420 | [−0.579, −0.263] | 7.8% | 995 | −0.280 | [−0.472, −0.068] | 7.6% |
| 150 | 1675 | −0.385 | [−0.552, −0.214] | 6.5% | 995 | −0.324 | [−0.523, −0.104] | 6.0% |
| 200 | 1675 | −0.396 | [−0.571, −0.213] | 3.6% | 995 | −0.331 | [−0.535, −0.104] | 3.9% |
| 250 | 1675 | −0.393 | [−0.571, −0.207] | 2.3% | 995 | −0.278 | [−0.496, −0.030] | 2.7% |
| 300 | 1675 | −0.394 | [−0.579, −0.197] | 1.3% | 995 | −0.254 | [−0.480, **+0.002**] | 2.0% |

**Every cell in the OTE column has a 95% CI entirely below zero — no exception, across the full 5–300pt
range.** The OB column has three cells whose CI upper bound crosses fractionally positive (+0.012,
+0.033, +0.002 at 75/100/300pt) — each is noise-level, not a real edge, and the point estimate at each
of those three cells is still clearly negative (−0.199 to −0.254).

Reference: `Q-ICTEXP-1`'s own T1 perfect-foresight ceiling (a different population, the raid→FVG chain,
not these two) measured mean MFE 120.4pt — inside this grid's tested range, for context.

---

## Interpretation

**No target distance rescues either entry.** The sweep brackets everything from near-stop-scale (5pt,
below both entries' own ~13–15pt stops) through the actual DOL target's own measured mean distance
(263pt OTE-eligible, 285pt OB-eligible) to well beyond it (300pt) — mean R stays negative throughout,
with no rising trend as target distance approaches or exceeds the DOL's own scale. If the DOL target
itself were the shared point of failure — too far, systematically mispriced relative to what these
entries can reach — a nearer target should have shown a materially better (even if still negative)
number. It doesn't. The entries themselves lack directional edge, independent of what they're pointed
at.

**This refutes the hypothesis from the prior session note** (that the shared DOL target was "the more
informative candidate point of failure" across `Q-ICTEXP-1`/OTE/OB). That framing doesn't survive this
test — worth recording as a correction, not quietly dropped. The honest conclusion is closer to the
one this whole corpus has reached repeatedly on this instrument: raid/sweep/displacement-based entry
timing on MNQ shows no measurable directional edge, at any of the exit distances checked here.

**What this does not test:** exit *style* changes (trailing stops, partial profit-taking, a
time-decayed target) rather than exit *distance* — those are different, untested levers. Also does not
test whether a fundamentally different entry family (not sweep-based, not displacement-based) would
fare differently against this or any target — that's a new-mechanism question, not an exit-redesign
one.

---

## Consequence

- `Q-ICT-OTE-1` and `Q-ICT-OB-1`'s own re-proposal bars (new mechanism evidence, not a parameter
  retune — already stated in each scoping doc) are unchanged and now additionally supported: a target
  retune specifically would not have helped either construct.
- No further target-swapping experiment is warranted on either construct without new mechanism
  evidence for the entry itself.
- The prior session's "shared DOL target" framing in `docs/SESSIONS.md` (`2026-08-20d`) and
  `ops/instruments/MNQ.md`'s DEAD-list row for `Q-ICT-OB-1` is corrected by this result, not silently
  left standing — see the addenda filed alongside this result.

## Audit hooks

```bash
# Byte-parity check against the already-recorded OTE result (must match exactly):
python -c "
import json
d = json.load(open('lab/analysis/c1/ict_target_investigation_2026-08-20/RESULTS.json'))
print(d['ote_stop_dist_mean'])
"
# Expected: 13.164776119402985 (matches _cheap_falsifier_ict_ote_1_2026-08-20_LOG.md's mean stop_dist)

# Original entry+stop logic files unmodified by this investigation:
git diff HEAD -- lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_ict_ote_1_2026-08-20.py lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_ict_ob_1_2026-08-20.py
# Expected: empty
```
