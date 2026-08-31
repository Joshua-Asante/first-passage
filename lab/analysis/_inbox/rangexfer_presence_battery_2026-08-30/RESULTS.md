# RESULTS — Presence battery (L1-L3) for Q-RANGEXFER-1's five hypotheses

**Verdict:** MIXED — 4/5 hypotheses AMBIGUOUS-DESIGN, H-RANGEXFER-1.a-MYM FALSIFIED (presence L2 fails).

**Status: COMPLETE, adversarially verified, TRUSTWORTHY-AS-IS.** Computed 2026-08-30, after the
operator ratified (a) Option A for L5 semantics (a certified, valid, non-significant attribution
limb falsifies H — see [`BOUNDED_ROUND_PLAN.md`](../joint_surrogation_null_2026-08-30/BOUNDED_ROUND_PLAN.md)
§2 P2) and (b) the per-hypothesis `AMBIGUOUS-DESIGN` closure row. This diagnostic runs the
presence limbs (L1-L3) the closure plan named as "the verdict-determining computation" — with L4
already `AMBIGUOUS` on all five hypotheses ([`rangexfer_byyear_l4_2026-08-30/RESULTS.md`](../rangexfer_byyear_l4_2026-08-30/RESULTS.md))
and no certifiable L5 design in existence (the hard stop, [`joint_surrogation_null_2026-08-30/RESULTS.md`](../joint_surrogation_null_2026-08-30/RESULTS.md)
Round 4), L1-L3 alone decide every reachable verdict.

## Headline

> **⚠ Corrected 2026-08-31 (two separate defects, both same day).** The two MNQ rows' L2 CIs were
> recomputed after fixing a look-ahead defect in `data_lib.py::overnight_ohlc` (Codex PR #227
> review) — full account:
> [`docs/notes/audits/2026-08-31-mnq-overnight-window-lookahead-defect.md`](../../../../docs/notes/audits/2026-08-31-mnq-overnight-window-lookahead-defect.md).
> **The three MYM rows were also recomputed**, after a follow-up Codex review pass found a separate
> scope-gap defect in `load_sessions.py::overnight_ohlc` (it only ever captured the 00:00–09:29 ET
> early-morning tail, never the 18:00–23:59 ET evening reopen) — full account:
> [`docs/notes/audits/2026-08-31-mym-overnight-window-scope-gap-defect.md`](../../../../docs/notes/audits/2026-08-31-mym-overnight-window-scope-gap-defect.md).
> **Every PASS/FAIL verdict below is unchanged** — `H-RANGEXFER-1.a-MYM` was already the sole FAIL
> and remains so, now failing all three limbs instead of just L2.

| Hypothesis | L1 (n-floor) | L2 (bootstrap CI lower bound > 0) | L3 (both chrono halves lift > 0) | Presence |
|---|---|---|---|---|
| H-RANGEXFER-1 (MNQ parent) | PASS | PASS — CI [+0.164, +0.307] (corrected; was [+0.300, +0.473]) | PASS | **PASS** |
| H-RANGEXFER-1.a (MNQ gap, overnight-calm) | PASS | PASS — CI [+0.074, +0.261] (corrected; was [+0.024, +0.187]) | PASS | **PASS** |
| H-RANGEXFER-1-MYM (MYM parent) | PASS | PASS — CI [+0.121, +0.307] (corrected; was [+0.110, +0.310]) | PASS | **PASS** |
| H-RANGEXFER-1.a-MYM (MYM gap, overnight-calm) | **FAIL** (n_cond=96; corrected; was PASS at n_cond=124) | **FAIL** — CI [-0.093, +0.115] (corrected; was [-0.008, +0.180]) | **FAIL** (half2=-0.038; corrected; was PASS both halves) | **FAIL** |
| H-RANGEXFER-1.b-MYM (MYM gap, bprime=0) | PASS | PASS — CI [+0.057, +0.219] (byte-identical — predictor/restriction don't touch `on_range`) | PASS | **PASS** |

**Disposition:** H-RANGEXFER-1.a-MYM fails presence outright — routes to `FALSIFIED` under the
brief's existing frozen §6 row with no null needed. The other four pass presence; with L4
AMBIGUOUS and no certifiable L5, they route to the newly-ratified `AMBIGUOUS-DESIGN` closure row.

## Method

Script: [`presence_l1_l3.py`](presence_l1_l3.py). Reused, verbatim, the exact per-hypothesis
panel-restriction convention already reviewed once in [`byyear_l4.py`](../rangexfer_byyear_l4_2026-08-30/byyear_l4.py)
(confirmed there to reproduce the brief's own cited pooled figures exactly) — no fresh restriction
logic authored. Implemented L1/L2/L3 fresh from the frozen pre-registration text
(`docs/briefs/pre-registration/Q-RANGEXFER-1-verdict-preregistration.md` §A/§B/§F/§G), at the
FROZEN block-bootstrap constants (`block=20` trading days, `draws=4000`, `seed=42`) — deliberately
not reusing any exploratory script's own ad hoc bootstrap seed/block (e.g.
`c2_c4_stratified_rerun.py`'s `block=60, seed=20260829`), which were never the frozen L2
construction. No vendor bars needed — both cached joint frames
(`candidate24_joint_frame.csv`, `c24_joint_frame.csv`) are git-tracked. No K spent: re-derives
L1-L3 from already-scored, already-cited panels only.

A pooled-figure cross-check (run before trusting the restriction logic, same discipline
`byyear_l4.py` applied) reproduced the brief's own cited numbers exactly or within the
already-disclosed 3-day MYM cache gap (1,304 vs the frozen 1,307-day panel).

## Adversarial verification (4-lens workflow + synthesis, same day)

Given this computation determines FALSIFIED/AMBIGUOUS-DESIGN routing across five hypotheses in a
months-long thread, it was independently verified before being trusted, mirroring this repo's own
standing Codex-review discipline for every prior artifact in this thread. Four independent
reviewers, each with a distinct lens, all with tool access to re-run the script and the source
CSVs directly (not just read the code):

1. **Bootstrap fidelity (L2).** No coding bugs found. The circular block-bootstrap is correctly
   implemented (chronological ordering, correct modulo wraparound, frozen constants correctly
   threaded through both call sites, min-stratified variant correctly takes the min WITHIN each
   draw). For the decisive H-RANGEXFER-1.a-MYM case, an independently-written from-scratch
   bootstrap (different code structure, same frozen algorithm) reproduced the CI bit-exactly:
   `[-0.008144, +0.180413]`. Stress-tested 8 alternate seeds + 4 alternate-RNG-engine seeds under
   the frozen circular algorithm — 12/12 kept the lower bound negative. Under a genuinely
   different but still-defensible non-circular/truncated block construction, 1 of 5 tested seeds
   flipped the lower bound to a barely-positive `+0.00128` — confirming the FAIL is a real,
   borderline feature of the data under the frozen definition, not a coding artifact, but
   genuinely fragile to the exact bootstrap variant.
2. **Restriction/column semantics.** No mismatches found for any of the five hypotheses. Confirmed
   the two `.a` hypotheses restrict on `bias_overnight==0` (not `bias_dayhist`, the exact
   conflation the brief's own §4 "Estimand correction" already warns about once) and
   `H-RANGEXFER-1.b-MYM` restricts on `bias_dayhist==0` (not swapped with the `.a-MYM` variable).
   Every pooled-figure cross-check figure verified against the brief's own text directly (not the
   script's self-claim). `N_FLOOR_POP=400`/`N_FLOOR_COND=100`/`block=20`/`draws=4000`/`seed=42`
   confirmed verbatim against the frozen pre-registration, not invented or re-tuned. Two
   non-blocking disclosure items surfaced (both verdict-inert): (a) L1's n-floor check for the
   two parent hypotheses uses the POOLED `bias_overnight==1` count, not a per-`bias_dayhist`
   -stratum floor a literal reading of §F.2's own phrasing could imply — both instruments' actual
   per-stratum counts (MNQ 213/126, MYM 191/122) clear 100 comfortably either way; (b) L3's frozen
   text ("both halves... of the conditional cases show lift > 0") is genuinely ambiguous for a
   two-group lift statistic — addressed by lens 3 below.
3. **L3 halves interpretation.** Sound. The literal transplant of candidate1's own convention
   (compare each half's raw rate against a fixed 0.50 baseline) was tested directly and gives a
   WRONG answer on this design — for H-RANGEXFER-1.a, both halves come back apparent-FAIL
   (rate<0.50 in both) even though the true incremental lift is clearly positive in both halves,
   because these restricted panels' reference-group baseline rate sits well below 0.50, unlike
   candidate1's own rolling-median-pinned-near-0.50 construct. This is not a competing valid
   interpretation — it silently changes the null being tested. The script's own resolution
   (restrict first, split the already-restricted panel chronologically by row count, recompute
   the lift independently in each half) was independently re-derived and stress-tested against
   three alternatives (split-then-restrict order, swap-the-middle-row for odd-length panels,
   date-midpoint vs row-count split) — none flip any of the five hypotheses' L3 verdict.
   `H-RANGEXFER-1.a-MYM` carries the smallest half-lifts in the whole battery (half1=+0.117
   n_hi=59, half2=+0.055 n_hi=65) — comfortably positive so it does not fail L3 on its own, but
   flagged as a second, currently-moot fragility (moot only because L2 already fails this
   hypothesis independently).
4. **L1 + holistic pass.** L1 confirmed correct for all five hypotheses by independent
   recomputation from the raw CSVs. Cross-checking against the pre-registration's own stated n's
   found one real, non-verdict-affecting mismatch: `H-RANGEXFER-1.b-MYM`'s script output is
   `n_scored=1008` vs the pre-registration §G.1's stated `n=1,010` — the same disclosed 2-3-row
   MYM cache-vintage gap already on record (PR #224), not a new defect; 1,008 still clears
   `N_FLOOR_POP=400` by a wide margin. Independently re-derived the decisive CI via two further
   methods (naive i.i.d. bootstrap: `[-0.006, +0.176]`; normal-approximation SE: `[-0.009,
   +0.179]`) — both closely match the block-bootstrap CI, a fifth independent confirmation the
   FAIL is real. Noted that this failure lands exactly on the cell the brief itself has repeatedly
   flagged as the weakest in the batch (stage-1 null-calibrated p=0.0495, barely clearing 0.05)
   and the one hypothesis the L4 by-year diagnostic already found non-unanimous (3/4 positive
   years) — three independent diagnostics converging on the same weak cell, not a coincidence.
   Full script re-run reproduced the committed JSON exactly (deterministic, `seed=42`).

**Synthesis verdict: `TRUSTWORTHY_AS_IS`.** No code fix required. Zero coding defects found across
L1/L2/L3 by four independent audits, each re-running the script and cross-checking against source
data or the frozen text directly (not code-reading alone). Two disclosure items carried into the
closure (both verdict-inert, both stated explicitly rather than silently omitted):

- The `H-RANGEXFER-1.b-MYM` n-count gap (1,008 here vs 1,010 in the pre-registration) — the same
  disclosed MYM cache-vintage difference already on record.
- `H-RANGEXFER-1.a-MYM`'s L2 FAIL is statistically borderline: robust to 12/12 seed/RNG-engine
  trials under the frozen circular block-bootstrap and to two independently-derived CI methods,
  but flips sign under 1/5 tested seeds of a different-but-defensible non-circular bootstrap
  variant. This is why the closure treats it as a clean `FALSIFIED` under the frozen procedure
  while naming the borderline-ness explicitly, rather than overstating confidence.

## Audit hooks

```bash
python lab/analysis/_inbox/rangexfer_presence_battery_2026-08-30/presence_l1_l3.py
# Expected (deterministic, seed=42): reproduces presence_l1_l3_results.json exactly; pooled-figure
# cross-check matches the brief's own cited numbers (or the disclosed 1304-vs-1307 MYM gap).

# The decisive CI, independently reproducible
python -c "
import json
d = json.load(open('lab/analysis/_inbox/rangexfer_presence_battery_2026-08-30/presence_l1_l3_results.json'))
r = d['H-RANGEXFER-1.a-MYM']
print(r['L2']['ci'], r['presence_pass'])
"
# Expected (post-2026-08-31 correction): [-0.092948..., 0.114652...] False
# (pre-correction value was [-0.008144..., 0.180413...] -- see the headline correction banner)
```
