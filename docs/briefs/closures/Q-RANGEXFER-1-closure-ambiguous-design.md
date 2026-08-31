# Q-RANGEXFER-1 — CLOSURE: `MIXED` (4× `AMBIGUOUS-DESIGN`, 1× `FALSIFIED`)

**Verdict:** `MIXED` — parent hypothesis (H-RANGEXFER-1, MNQ) lands `AMBIGUOUS-DESIGN`; per §9's
own filename rule this closure files under that verdict. Full per-hypothesis breakdown in §1.
**Closed:** 2026-08-30
**Lane:** UNASSIGNED
**Pre-registration:** [`Q-RANGEXFER-1-verdict-preregistration.md`](../pre-registration/Q-RANGEXFER-1-verdict-preregistration.md) — frozen `2026-08-29` (§A–§G); §H (L5 semantics + `AMBIGUOUS-DESIGN` row) filed `2026-08-30`, same-day operator ratification, before any certified L5 result existed or could exist (hard stop already fired)
**Spend / K:** $0.00 · K consumed at this closure: 0 (the presence battery re-derives already-cited panels; the pre-existing `K_fresh=2`/`K_fresh=2`/+1 declarations on `H-RANGEXFER-1.a-MYM`/`H-RANGEXFER-1.b-MYM`/the exploratory 0.785 look remain disclosed but were never spent — no Phase 3 execution ever ran)
**Live effect:** none — conditioner-role research only; no entry/sizing construct was ever in scope (§5 forbidden moves); no `core/`, Pine, allocation, `dd_protection`, or rail change
**Artifacts:**
[`joint_surrogation_null_2026-08-30/RESULTS.md`](../../../lab/analysis/_inbox/joint_surrogation_null_2026-08-30/RESULTS.md) (Rounds 1–4, the hard-stop record) ·
[`BOUNDED_ROUND_PLAN.md`](../../../lab/analysis/_inbox/joint_surrogation_null_2026-08-30/BOUNDED_ROUND_PLAN.md) (closure-path plan, Codex-reviewed) ·
[`rangexfer_byyear_l4_2026-08-30/RESULTS.md`](../../../lab/analysis/_inbox/rangexfer_byyear_l4_2026-08-30/RESULTS.md) (L4, Codex-corrected) ·
[`rangexfer_presence_battery_2026-08-30/RESULTS.md`](../../../lab/analysis/_inbox/rangexfer_presence_battery_2026-08-30/RESULTS.md) (L1–L3, adversarially verified — the decisive computation for this closure)

---

## 1. Verdict (§6 asserted against actual numbers, per hypothesis)

L4 (by-year, `N_valid<7` on all five) and the joint-surrogation design's hard stop (no certified
L5 exists) are common to all five and established before this closure; only L1–L3 (the presence
battery) and the corrected §6/§H routing table were newly computed to reach these verdicts.

> **⚠ Corrected 2026-08-31 (two separate defects, both found via Codex PR #227 review, both fixed
> same day).** First: the two MNQ rows' L2/L4 figures were recomputed after fixing a look-ahead
> defect in `data_lib.py::overnight_ohlc` — the frozen `bias_overnight` predictor partly
> incorporated bars from after the outcome it was meant to lead. Second: the three MYM rows' L1/L2/L4
> figures were recomputed after fixing a separate scope-gap defect in `load_sessions.py::overnight_ohlc`
> — that function only ever captured the 00:00–09:29 ET early-morning tail, never the 18:00–23:59 ET
> evening reopen (an inherited "DELETE sham" placeholder from a different campaign, not a look-ahead
> issue — nothing future leaked in, but roughly 9 of the ~15.5-hour overnight session was silently
> excluded). **Every §6 route below is unchanged** — full account:
> [`docs/notes/audits/2026-08-31-mnq-overnight-window-lookahead-defect.md`](../../notes/audits/2026-08-31-mnq-overnight-window-lookahead-defect.md)
> (MNQ) and
> [`docs/notes/audits/2026-08-31-mym-overnight-window-scope-gap-defect.md`](../../notes/audits/2026-08-31-mym-overnight-window-scope-gap-defect.md)
> (MYM).

| Hypothesis | L1 | L2 | L3 | L4 | L5 | §6 route fired |
|---|---|---|---|---|---|---|
| H-RANGEXFER-1 (MNQ parent) | PASS | PASS CI[+0.164,+0.307] (corrected; was [+0.300,+0.473]) | PASS | AMBIGUOUS (N_valid=4; corrected; was 3) | no certified design exists | **`AMBIGUOUS-DESIGN`** |
| H-RANGEXFER-1.a (MNQ gap, overnight-calm) | PASS | PASS CI[+0.074,+0.261] (corrected; was [+0.024,+0.187]) | PASS | AMBIGUOUS (N_valid=3; corrected; was 5) | no certified design exists | **`AMBIGUOUS-DESIGN`** |
| H-RANGEXFER-1-MYM (MYM parent) | PASS | PASS CI[+0.121,+0.307] (corrected; was [+0.110,+0.310]) | PASS | AMBIGUOUS (N_valid=3; unchanged) | no certified design exists | **`AMBIGUOUS-DESIGN`** |
| H-RANGEXFER-1.a-MYM (MYM gap, overnight-calm) | **FAIL** (n_cond=96; corrected; was PASS at n_cond=124) | **FAIL** CI[-0.093,+0.115] (corrected; was [-0.008,+0.180]) | **FAIL** (half2 lift negative; corrected; was PASS both halves) | AMBIGUOUS (N_valid=3; corrected; was 4) | not reached | **`FALSIFIED`** (presence limb fails outright — L4/L5 moot; failure widened, verdict unchanged) |
| H-RANGEXFER-1.b-MYM (MYM gap, bprime=0) | PASS | PASS CI[+0.057,+0.219] (unaffected — predictor/restriction do not touch `on_range`) | PASS | AMBIGUOUS (N_valid=6; unaffected) | no certified design exists | **`AMBIGUOUS-DESIGN`** |

Every other §6 route (`RESOLVED`, plain `AMBIGUOUS-HOLD` with L1–L3 passing and only L4 blocking)
was checked and did not fire: `RESOLVED` requires L4 to pass, which it cannot at this panel length
on any of the five (confirmed, not assumed — `rangexfer_byyear_l4_2026-08-30`); plain
`AMBIGUOUS-HOLD` requires a certified L5 design to exist and simply be unable to resolve L4 —
no such design exists, which is why §H added `AMBIGUOUS-DESIGN` as the correct route rather than
force-fitting `AMBIGUOUS-HOLD` (the PR #223 ruling this closure discharges).

## 2. What the pre-registration predicted vs what happened

§E/§F.4/§G.3 predicted, ex-ante (2026-08-29/30, before any Phase 1 numeric result): presence
limbs (L1–L3) PASS on the two parent hypotheses and on `H-RANGEXFER-1.b-MYM`; L4 lands AMBIGUOUS
on power grounds on all five; `H-RANGEXFER-1.a-MYM` was separately flagged as the most likely to
fail on effect-strength grounds ("already the weakest, least-decisive cell in the whole batch").

**All three predictions confirmed exactly.** L4 landed AMBIGUOUS on all five, as predicted (the
by-year diagnostic even sharpened WHY: the two parents fail purely on panel length with unanimous
per-year sign, not effect inconsistency — a stronger, more favorable finding than the pre-reg's
own bare "AMBIGUOUS on power grounds" prediction). Presence passed on four of five exactly as
predicted. The one hypothesis flagged ex-ante as the weakest — `H-RANGEXFER-1.a-MYM` — is the one
that failed, and it failed for the reason predicted (marginal effect strength, not sample-size
starvation: its own restricted subpanel, n=991, is actually LARGER than the sibling `.a`
hypothesis's n=973, which passed comfortably). No surprise reversed a prediction in either
direction. The one item pre-reg §E/§F.4 explicitly declined to predict — L5's own behavior — was
never reached; the joint-surrogation design's own hard stop (a separate, upstream finding this
closure inherits, not one this closure discovered) made that limb design-blocked rather than
resolved either way.

## 3. What this closure does NOT license

- **No entry, sizing, or timing construct on any surviving conditioner.** All four
  `AMBIGUOUS-DESIGN` hypotheses stay conditioner-role research, not tradeable findings — the
  brief's own §5 forbidden-moves list already barred this before certification and nothing here
  changes that; `AMBIGUOUS-DESIGN` is weaker than even the `RESOLVED`-but-conditioner-only
  disposition this thread never reached.
- **No reading of `H-RANGEXFER-1.a-MYM`'s FALSIFIED as evidence against the parent
  `H-RANGEXFER-1-MYM` finding, or against `H-RANGEXFER-1.b-MYM`.** These are three genuinely
  distinct estimands on three different (sub)panels (full panel min-stratified; overnight-calm
  restricted; day-history/`bprime=0` restricted) — the brief's own §5 already forbade conflating
  them, and the presence battery's own result (the other two clear comfortably) is direct evidence
  they do not share a fate.
- **No reading of the `AMBIGUOUS-DESIGN` verdict as "probably real, just untested."** The
  exploratory, uncertified `p_upper=0.785` lead on record (`joint_surrogation_null_2026-08-30/RESULTS.md`
  Round 2) points the other way — toward the parent effect looking unremarkable once shared
  long-memory regime dynamics are accounted for — but that lead was never certified and is not
  being promoted to a finding here either. `AMBIGUOUS-DESIGN` means genuinely undetermined, not a
  euphemism for either direction.
- **No reuse of the joint-surrogation design work (Rounds 1–4, 9 constructions, 2 ratified
  remedies) as a certified instrument for any OTHER cross-series question in this repo** (the
  D5/O1 "UNRESOLVED-NEEDS-DESIGN" debt stays open for the whole class) — only as a documented,
  Codex-reviewed record of what has already been tried and failed, per `BOUNDED_ROUND_PLAN.md` §3's
  own certification requirements for whoever picks this up next.
- **No inheritance of this closure by `Q-VOLREGIME-1`.** That brief's own bar-level Phase 1 was
  never attempted (blocked upstream, never reached its own positive control) and operates on a
  structurally different panel (~135,000–140,000 bars vs ~1,300–1,500 days) where both of this
  closure's binding failure mechanisms (estimation noise in a near-boundary long-memory `d`; the
  L4 wall) are materially weaker — it is assessed independently, per the ratification's own
  scoped-to-`Q-RANGEXFER-1`-only clause.

## 4. Defects found in the frozen brief (recorded, not repaired)

**One genuine drafting defect, corrected via the §H addendum rather than a Trap-#12 edit to the
frozen §A–§G text:** the pre-registration's own §C ("L5 NEVER GATES on its own") contradicted this
brief's own §4 hypothesis text and the sibling `Q-VOLREGIME-1`'s frozen §6 — three co-authored,
same-day, cross-referencing artifacts disagreed on a load-bearing semantic. Caught only because
this closure's own review of an external advisor report prompted a full re-read of the frozen
texts side by side; a routine execution pass would likely have inherited whichever reading was
convenient at the moment a certified L5 result first existed — precisely the failure mode §H's
own framing was written to prevent by ruling before any such result could exist.

**Two named limbs never reached execution, disclosed here rather than silently dropped:** §4's own
counter-stratum rejection branches — `H-RANGEXFER-1.a`'s "does the overnight-hot negative point
estimate generalize under the joint-surrogation null" and `H-RANGEXFER-1.b-MYM`'s "does the
`bprime=1` stratum's own non-significant result indicate a real negative/reversal" — are L5-class
limbs and are therefore equally design-blocked by the hard stop. They were never evaluated in
either direction; a future re-open under `BOUNDED_ROUND_PLAN.md` §3's certification path inherits
them in its mandatory execution set (per Codex's PR #226 review, finding 8).

## 5. Lesson candidates

**2026-08-30 — a verdict-map semantic (does a limb gate or only type?) needs a same-session
cross-artifact consistency check at FREEZE time, not discovered at close time.** Three
co-authored, same-day artifacts (this brief's §4, its own pre-registration §C, and the sibling
`Q-VOLREGIME-1`'s §6) disagreed on whether a valid-but-non-significant attribution limb falsifies
or merely types a verdict — caught only incidentally, during an unrelated external-report review,
many amendment rounds after all three were frozen. Below the two-incident bar as phrased (this is
the first occurrence of this specific class of cross-artifact freeze inconsistency on record) —
watch for a second instance before promoting to a standing brief-authoring check.

---

## Iterate — loop exit (MANDATORY — closure incomplete without it)

- **Verdict used:** `MIXED` — 4× `AMBIGUOUS-DESIGN` (H-RANGEXFER-1, H-RANGEXFER-1.a,
  H-RANGEXFER-1-MYM, H-RANGEXFER-1.b-MYM), 1× `FALSIFIED` (H-RANGEXFER-1.a-MYM). Scored
  independently per hypothesis per this brief's own §6/§9 convention — not force-collapsed to one
  value.
- **Model update:** Overnight-range and, on both instruments' day-history-restricted subpanels,
  gap-magnitude carry a large, presence-robust incremental signal over matched day-history
  conditioning that survives every cheap test this repo can currently run — but whether that
  signal is genuine same-day transmission or an artifact of a shared, hard-to-surrogate
  long-memory regime remains genuinely undetermined: not because the evidence is weak, but because
  no null model this repo could build, across 4 rounds and 9 constructions, controls its own
  Type-I error rate once fitted from data (measured 26% vs nominal 5%, the load-bearing Round 4
  finding). The one sub-claim that DID fail — gap magnitude restricted to the overnight-calm
  stratum on MYM — failed on ordinary presence grounds (a bootstrap CI crossing zero on an
  already-marginal effect), a fully separate and much more mundane finding than the joint-
  surrogation question; its failure says nothing about the joint-surrogation problem or about the
  three hypotheses that did pass presence.
- **Next:** `MIXED` — `STOP` on H-RANGEXFER-1.a-MYM; `ITERATE` on the other four (see Routing).
- **Routing:**
  - `H-RANGEXFER-1.a-MYM` → **STOP.** Presence-level `FALSIFIED`; the re-proposal bar below applies.
  - `H-RANGEXFER-1`, `H-RANGEXFER-1.a`, `H-RANGEXFER-1-MYM`, `H-RANGEXFER-1.b-MYM` → **ITERATE**,
    return target: (a) the panel reaches ≥7 qualifying years under the corrected per-stratum L4
    gate (`rangexfer_byyear_l4_2026-08-30`'s own convention), or (b) a genuinely different design
    class clears every certification requirement in `BOUNDED_ROUND_PLAN.md` §3 (relative AND
    absolute model adequacy; certified on the final deployed post-coupling/post-remap
    construction, not a proxy; per-N-matched binomial size cutoffs; per-(instrument ×
    predictor-pair × panel-restriction) certification; zero-safe frozen transforms; no naive
    parameter-bootstrap null), or (c) an externally validated method for joint long-memory
    surrogation under estimation becomes available. No calendar-dated re-test on any of the four.
- **Entry packet** *(for the four `ITERATE` hypotheses)*: frozen constraints — the pre-registration
  (§A–§H) and this closure's §6-route table stay binding; the certification requirements in
  `BOUNDED_ROUND_PLAN.md` §3 are mandatory, not optional, for any successor design. Positive
  carry-forwards — all four hypotheses' presence-battery PASS results (L1–L3, adversarially
  verified) stand and do not need re-derivation; the cached joint frames
  (`candidate24_joint_frame.csv`, `c24_joint_frame.csv`) and the by-year script
  (`byyear_l4.py`) are reusable as-is. Forbidden re-opens: retrying the exact log-Pearson
  ARFIMA(1,d,0) construction Round 4 already falsified at production-grade calibration; treating
  cross-model agreement among miscalibrated designs as a substitute for size control (explicitly
  rejected, PR #223/#225). K/$ budget: none pre-committed by this closure; a successor design's
  own K (model-adequacy work stays K-free per the standing ruling; any real-data attribution look
  needs its own fresh K declaration, per the K_fresh=2/2/+1 precedent already on record) is a
  fresh decision at that time, not inherited.
- **Stop rule / re-proposal bar** *(for `H-RANGEXFER-1.a-MYM`)*: new mechanism evidence — a
  materially different construct or a longer panel that changes the underlying data, not a
  retuned bootstrap block length, seed, or significance threshold on this exact statistic. The
  verification record (`rangexfer_presence_battery_2026-08-30/RESULTS.md`) already found the FAIL
  robust to 12 alternate seed/RNG-engine trials and to two independently-derived CI methods — a
  re-run under the identical frozen procedure would not be new evidence.
- **Board write:** `SESSIONS Open/next: Q-RANGEXFER-1 closed 2026-08-30 (4x AMBIGUOUS-DESIGN, 1x
  FALSIFIED) — joint-surrogation null hard-stopped at Round 4 (measured 26% Type-I vs nominal 5%);
  D5/O1's cross-series joint-surrogation instrument gap stays open for the whole mechanism class,
  not just this Q. Carry: Q-VOLREGIME-1 independently assessed on its own bar-level panel, not
  closed by inheritance; its own by-year L4 count (bar-level, possibly >=7 qualifying years) is
  the next cheap step on that thread.` Owner: this closure.
- **Registry:** `n/a — docs/rejected_candidates.md` per its own current governing text
  ([`ADR 2026-08-09`](../../adr/2026-08-09-rejection-register-topology-and-bar-wiring.md) D3):
  "per-direction instrument-scoped mechanism rejections belong in
  `ops/instruments/<SYM>.md`... this file owns domain-level and cross-instrument bars." This
  rejection is single-instrument (MYM) and single-direction — registered instead at
  [`ops/instruments/MYM.md`](../../../ops/instruments/MYM.md), new cell
  `overnight-gap-magnitude-range-conditioning-overnight-calm`, verdict `DEAD`, source this
  closure (H-RANGEXFER-1.a-MYM only — the other four hypotheses are not strategy-grounds kills
  and are not registered anywhere).

## §10 audit-hook discharge

The brief's own §10 hooks that reproduce the underlying stage-1 statistics and joint-gate figures
were already discharged in prior same-day amendment rounds (PRs #210/#211/#223/#224) and are
unaffected by this closure (no threshold, panel, or stage-1 script changed since). Discharged
fresh this session:

```text
$ python lab/analysis/_inbox/rangexfer_presence_battery_2026-08-30/presence_l1_l3.py
Pooled-figure cross-check reproduces the brief's own §0/§4 cited numbers exactly (or within the
already-disclosed 1304-vs-1307-day MYM cache gap).                                        OK

$ grep -n "H-RANGEXFER-1.b-MYM\|H-RANGEXFER-1.a-MYM" \
    docs/briefs/Q-RANGEXFER-1-overnight-range-gap-magnitude-transfer.md
Both hypotheses present and textually distinct (different restriction variables:
bias_overnight==0 vs bias_dayhist==0).                                                    OK

$ grep -n "NEVER GATES" docs/briefs/pre-registration/Q-RANGEXFER-1-verdict-preregistration.md
§C's original line still present verbatim (Trap #12 — not edited); §H's correction is an
addendum, not a rewrite.                                                                  OK
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-30 | Closure authored — presence battery scored (adversarially verified, `TRUSTWORTHY_AS_IS`), §H ratification applied, five-way verdict routed | Claude Code |
| 2026-08-31 | Corrected — MNQ look-ahead defect (`data_lib.py`) then MYM scope-gap defect (`load_sessions.py`), both found via Codex PR #227 review, both re-derived same day. All five §6 routes unchanged; `H-RANGEXFER-1.a-MYM`'s FALSIFIED now fails L1 too (not just L2/L3) under the corrected window | Claude Code |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/Q-RANGEXFER-1-closure-ambiguous-design.md
grep -c "Fired?" docs/briefs/closures/Q-RANGEXFER-1-closure-ambiguous-design.md
```
