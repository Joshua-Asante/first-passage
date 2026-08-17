# Q-POLFRONT-1 — CLOSURE: `RESOLVED-QUANTIFIED` (policy lever material for admission, EOD-clock caveat load-bearing)

**Verdict:** `RESOLVED-QUANTIFIED` — median R_max ratio (policy/flat) = 5.107× ≥ the frozen 1.25× bar; pass-floor met in every counted cell by construction; no reversal at any tested quantum
**Closed:** 2026-08-16
**Lane:** UNASSIGNED
**Pre-registration:** [frozen brief](../Q-POLFRONT-1-policy-augmented-seed-frontier.md) §4/§6 byte-unedited + [camp OPERATIONALIZATION](../../lab/analysis/c1/q_polfront_1_2026-08/OPERATIONALIZATION.md) (frozen pre-read; sweep-range amendment recorded pre-read)
**Spend / K:** $0 · K=0 · no manifest · no candidate · no deployment surface
**Artifacts:** [RESULTS](../../lab/analysis/c1/q_polfront_1_2026-08/RESULTS.md) · `out/polfront_results.json`

---

## 1. Verdict (frozen §4/§6 asserted)

| §4 route | Trigger | Actual | Fired? |
|---|---|---|---|
| RESOLVED-QUANTIFIED (H holds) | median ratio ≥ 1.25× AND pass-floor met in every counted cell | median **5.107×**, min **1.526×**; pass-floor met by construction (24/24 defined cells) | ✓ |
| FALSIFIED-IMMATERIAL | median ratio < 1.10× OR pass-floor fails in ≥ half the headroom cells | did not fire | — |
| AMBIGUOUS-ABSTRACTION | quantized arm reverses the headline direction | quantized medians 5.107/5.322/5.000 at Q=$25/50/85 — no reversal | — |

## 2. What this measures, exactly

Whether cushion-proportional sizing (Q-EVALSEQ-1's winner, generalized to cap 1.0) widens the
admissible base-R frontier on candidate-independent `(w,b,r,k)` geometry at the frozen floors.
It does — by a median factor of 5×, across 24 of 30 frozen cells, with 2 more cells newly
admitted where flat sizing clears nothing. Discovery en route: the policy's true admissible
ceiling is theoretically bounded below `ROPE=$3,000` for every cell (a single full-cushion
losing trade at `R_base ≥ ROPE` breaches by itself) — recorded as a sweep-range amendment
before any grid number was read, not a post-hoc rationalization.

## 3. The load-bearing caveat (NOT a footnote — carries forward)

The mandatory intraday-sensitivity disclosure arm shows the policy's bust rate is far more
sensitive to the EOD-vs-intraday clock gap than the flat arm's: median bust increase under a
doubled-excursion stress is **+55.2pp for the policy vs +1.63pp for the flat arm**. The
headline 5.1× ratio is an EOD-clock number. Per the standing lesson (bust figures are lower
bounds; the venue enforces breach intraday), **this ratio should not be read as a usable
sizing multiplier for any real candidate without an intraday-honest remeasurement of the
policy arm specifically** — the same clock discipline Q-EVALSEQ-1's own book-level result
carried, but sharper here because the policy operates by design close to the barrier.

## 4. What this closure does NOT license

- Reading any cell, or the 5.1× ratio itself, as an admission, a candidate, or a WATCH-rung
  change (§5, frozen).
- Using the headline ratio for deep-lane family selection (GO-1) without the intraday-honest
  caveat carried forward explicitly — see routing below.
- Extending the grid, adding a third arm, or re-tuning the policy shape under this brief
  (§5 forbidden — schedule search happened in Q-EVALSEQ-1 and was priced there).

## 5. Lesson candidates

Below the two-incident bar — watch: a state-dependent policy's headroom gain and its
EOD-clock fragility can move in the *same* direction (both scale with how close to the barrier
the policy operates by design); the disclosure-arm discipline in Q-EVALSEQ-1's frozen brief
generalized cleanly to a second instrument (seed-target geometry) without modification, which
is some evidence the mandatory-disclosure-arm pattern is worth keeping as standing practice for
any future policy-scoring brief.

## Iterate — loop exit

- **Verdict used:** `RESOLVED-QUANTIFIED`
- **Model update:** state-dependent sizing materially widens the admissible geometric region
  for candidates — the diagnostic's central hypothesis is now confirmed on a second,
  candidate-independent instrument, not just the barred book. But the gain is EOD-clock-fragile
  in a way flat sizing is not; any downstream use of this frontier for family selection must
  carry that caveat, not just the headline ratio.
- **Next:** INTEGRATE
- **Routing:** feeds deep-iteration lane **GO-1** ([charter](../../adr/2026-08-16-deep-iteration-lane-charter.md)) directly — the first lane campaign's family selection may now consult the policy-augmented frontier, **with the intraday-clock caveat carried into the campaign's own prereg as a named risk**, not silently. No further Q-POLFRONT-1 work is owed; an intraday-honest remeasurement of the policy arm specifically is a **named but unopened** fork (below), not blocking GO-1.
- **Entry packet:** n/a — integrated, not iterated as its own successor Q
- **Stop rule / re-proposal bar:** n/a — integrated
- **Board write:** `SESSIONS Open/next: deep-lane GO-1 unblocked (frontier landed); Databento parent-era dry-run next; intraday-honest policy remeasurement named as an open fork, not opened.` Owner: this closure · [RESULTS](../../lab/analysis/c1/q_polfront_1_2026-08/RESULTS.md)
- **Registry:** n/a — policy-lever measurement, not a strategy-mechanism rejection

## §7 — Fork named (not opened)

**Intraday-honest policy remeasurement.** Re-run the policy arm (not the flat arm — its
stress-sensitivity is already an order of magnitude smaller) on an intraday-honest clock
(same discipline as the W1 ADR / `RESULTS_INTRADAY_W1.md` precedent for the book), to learn how
much of the 5.1× ratio survives. Not opened here — a future deep-lane campaign whose family
selection leans materially on the policy frontier should open this first.

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-16 | Frozen run executed under operator GO; RESOLVED-QUANTIFIED recorded; intraday-clock caveat routed to GO-1 as a named risk, and a remeasurement fork named but not opened | Claude Code (JA GO) |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/Q-POLFRONT-1-closure-resolved-quantified.md
python lab/analysis/c1/q_polfront_1_2026-08/run_polfront.py   # reproduces (same-seed CRN design)
```
