# Q-RANGECOND-1 — CLOSURE: `RESOLVED` (with a disclosed panel-vintage caveat)

> ## ⚠ RETRACTED 2026-08-31 — DO NOT CITE THIS VERDICT
>
> The `RESOLVED` verdict below rests on `data_lib.py::overnight_ohlc`'s own look-ahead defect
> (Codex PR #227 review, independently re-verified and quantified same day) — the frozen
> `bias_overnight` conditioner partly incorporated bars from *after* the outcome it was meant to
> predict. Under the corrected conditioner, the entire effect vanishes: WR diff +24.75pp → +0.75pp
> (CI now includes 0), mean-win diff +0.711R → -0.058R (CI now includes 0, sign-flipped). The
> corrected verdict is `FALSIFIED` —
> [`Q-RANGECOND-1-closure-falsified.md`](Q-RANGECOND-1-closure-falsified.md) is now authoritative.
> The addendum this closure's own routing filed on
> [`b3-orb-mnq-payability-line.md`](../../pursuits/b3-orb-mnq-payability-line.md) is itself
> retracted there. Full account:
> [`2026-08-31-mnq-overnight-window-lookahead-defect.md`](../../notes/audits/2026-08-31-mnq-overnight-window-lookahead-defect.md).
> This file is preserved below, unedited, as frozen historical record (Trap #12) — not as a
> live verdict.

**Verdict:** `RESOLVED`
**Closed:** 2026-08-30
**Lane:** UNASSIGNED
**Pre-registration:** [`Q-RANGECOND-1-verdict-preregistration.md`](../pre-registration/Q-RANGECOND-1-verdict-preregistration.md) — frozen 2026-08-30, before Phase 1 ran
**Live effect:** none — conditioner-role/filter research only; no entry, sizing, or timing construct is licensed by this closure alone (§5); no `core/`, Pine, allocation, `dd_protection`, or rail change
**Spend / K:** $0.00 · `K_intrinsic=1` (disclosure only, per §8) · Cap seat not claimed
**Artifacts:** [`rangecond_1_2026-08-30/RESULTS.md`](../../lab/analysis/_inbox/rangecond_1_2026-08-30/RESULTS.md) · [`phase1_2_3_conditioned_orb.py`](../../lab/analysis/_inbox/rangecond_1_2026-08-30/phase1_2_3_conditioned_orb.py) · [`RESULTS.json`](../../lab/analysis/_inbox/rangecond_1_2026-08-30/RESULTS.json)

---

## 1. Verdict (§6 asserted against actual numbers)

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` | L1 (n≥30) AND L2 (WR-diff CI excludes 0, +) AND L3 (mean-win-diff CI excludes 0, +) AND L4 (conditioned WR ≥55%) | L1: n_conditioned=340 ✓ · L2: WR diff +24.75pp, CI `[+18.30pp,+31.31pp]` ✓ · L3: mean-win diff +0.711R, CI `[+0.543R,+0.887R]` ✓ · L4: conditioned WR=66.47% ✓ | ✓ |
| `FALSIFIED` | Diffs indistinguishable from/worse than unconditioned, OR L4 fails while L2/L3 clear | Neither condition fired | — |
| `AMBIGUOUS-HOLD` | L1 fails (n<30) | n_conditioned=340 ≫ 30 | — |

All four pre-registered limbs cleared cleanly — this is not a borderline call on any single limb.

## 2. What the pre-registration predicted vs what happened

Pre-reg §D, corrected on adversarial review before Phase 1 ran, predicted "RESOLVED or FALSIFIED
is the more likely outcome than AMBIGUOUS-HOLD" (power grounds: `ORB-MNQ-1`'s own 99%+
entry-trigger rate means the conditioner's ~20%-of-days flag rate translates almost directly into
conditioned trade count, expected ≈280-300, roughly 10× the 30-trade floor). **Confirmed
essentially exactly**: n_conditioned=340, close to the corrected ex-ante estimate. §D also
predicted "directionally favorable... but WITHOUT a confident prediction on whether L2-L4 clear
decisively" — this held too: L2-L4 cleared, but not as a foregone conclusion the pre-registration
asserted in advance (the mechanism story itself was flagged, correctly, as only a plausible prior,
not a settled explanation — see §1's own correction and the NAS100 counter-example in §2, neither
of which predicted this specific direction with confidence).

**One genuine surprise, disclosed not smoothed over:** the panel-vintage discrepancy (§11 of the
parent brief; full account in `RESULTS.md`'s own "Caveat" section). This was not anticipated in
the pre-registration, which assumed (without stating it explicitly) that Phase 1 would reproduce
`ORB-MNQ-1`'s own previously-published headline figures closely. It does not. The
conditioned-vs-unconditioned COMPARISON is unaffected (both legs use the identical panel), but the
absolute population-level stats are a fresh measurement on a shorter, more recent panel than
`ORB-MNQ-1`'s original G8 admission used.

## 3. What this closure does NOT license

- **No re-entry into the parked pursuit by this closure alone.** Per §5's own forbidden move and
  `b3-orb-mnq-payability-line.md`'s own established practice (the Aegis-6J1 precedent this brief
  cited): this closure is evidence toward the pursuit's own re-entry clause, filed as an
  addendum (§9); the re-entry decision itself, and any resulting Pine/re-MC/spend, are separate,
  operator-gated steps.
- **No claim that the conditioner is a certified causal mechanism.** `Q-RANGEXFER-1` closed
  `AMBIGUOUS-DESIGN` on mechanism attribution; this closure's own RESOLVED verdict is about
  whether the presence-verified predictive relationship is USEFUL for `ORB-MNQ-1`'s payoff shape,
  which is a different (and now confirmed) claim, not a mechanism certification. The disclosed,
  uncertified `p_upper=0.785` lead (parent brief §5) — pointing toward "shared-regime artifact" —
  is not retired by this result; a useful filter and a certified mechanism are different things,
  and this closure only established the former.
- **No claim that `ORB-MNQ-1`'s original G8 admission headline figures are reproduced.** The
  panel-vintage caveat (§2 above, `RESULTS.md`'s own "Caveat" section) means the unconditioned
  population's own summary stats in this run are a fresh, ~300-day-shorter-panel measurement, not
  a byte-for-byte reproduction of the original admission pipeline's numbers.
- **No parameter change to `ORB-MNQ-1`'s own locked entry/exit construct.** The conditioner is an
  external day-selection gate, not a retuned SL/TP/ATR/session parameter (§5, D-S-A gate).
- **No claim this generalizes to any other conditioner, threshold, or construct.** §5's own
  forbidden move bars a post-hoc search over conditioners/thresholds; only the single,
  pre-registered `bias_overnight` definition was tested, once.

## 4. Defects found in the frozen brief (recorded, not repaired)

None in the frozen brief/pre-registration text itself (both were adversarially reviewed and
corrected BEFORE Phase 1 ran — see the parent brief's own commit history). One real defect was
found and fixed DURING Phase 1 execution, in the analysis script (not the frozen brief): a
pandas-2.x `datetime64[us]`-vs-`[ns]` epoch-conversion bug (the same class of defect this repo
already documented once, Q-ICTEXP-1) produced a garbage 3-trade first run before being caught and
fixed. Disclosed in `RESULTS.md`, not silently corrected — the pre-fix and post-fix behavior are
both on record in the script's own docstring and this closure.

## 5. Lesson candidates

**2026-08-30 — a strategy's own headline admission figures can silently drift from the current
canonical panel without anyone noticing, if the two are never cross-checked.** `ORB-MNQ-1`'s own
G8 admission pipeline (2026-07-16) used a native-databento panel spanning back to 2019-05-06;
`MNQ_M15.csv` (the current canonical TV-sourced panel this entire `Q-RANGEXFER-1` research line is
built on) starts 2020-07-01. Nobody had previously flagged this ~300-day, panel-vintage gap
because no prior work joined the two panels' own outputs directly against each other the way this
brief's own conditioner-join did. Below the two-incident bar as phrased (first occurrence of this
specific cross-panel drift) — watch for a second instance before promoting to a standing gate
(e.g., a periodic "does `ORB-MNQ-1`'s own headline reproduce on the current canonical panel"
check).

---

## Iterate — loop exit (MANDATORY — closure incomplete without it)

- **Verdict used:** `RESOLVED`, with the panel-vintage caveat carried forward explicitly into all
  downstream citations of this result.
- **Model update:** The overnight-range conditioner, already presence-verified as an incremental
  predictor of same-day RTH-range magnitude (`Q-RANGEXFER-1`), is now ALSO shown to materially
  improve `ORB-MNQ-1`'s own realized payoff shape on the exact axis Tradeify's own payability
  floor cares about — win rate lifts +24.75pp to 66.47% (clearing the measured 55-60% floor with
  real margin) and mean win nearly doubles (+0.711R). This is the first concrete, measured link
  between a presence-verified (not mechanism-certified) conditioner and an admitted strategy's own
  payability problem in this repo. It does not resolve whether the underlying relationship is a
  genuine same-day transmission mechanism or a shared-regime artifact (`Q-RANGEXFER-1`'s own
  unresolved question) — it establishes that, mechanism aside, the filter is USEFUL for this
  specific purpose.
- **Next:** `INTEGRATE`
- **Routing:** File an addendum on
  [`docs/pursuits/b3-orb-mnq-payability-line.md`](../pursuits/b3-orb-mnq-payability-line.md)
  citing this closure as new payability/cost-geometry evidence per that pursuit's own re-entry
  clause (filed as part of this same commit — see that document's own new addendum). Name (do
  not authorize) a full Tradeify re-MC — using the conditioned trade population at real Monte
  Carlo scale, not just the observed-sample WR/mean-win split this brief computed — as the natural
  next step. That re-MC needs its own operator GO and its own explicit panel-vintage choice
  (standardize on one panel, do not blend `MNQ_M15.csv` and the original databento-native panel).
  No Pine, no rail, no spend from this closure alone.
- **Entry packet** *(for the named, not-yet-opened re-MC)*: frozen constraints — the conditioner
  definition (`WINDOW=60, Q_BIAS=0.80`, unmodified), `ORB-MNQ-1`'s own locked entry/exit
  parameters (unmodified, external gate only), the Tradeify cost basis (`rt_cost_pt=1.41`).
  Positive carry-forwards — the conditioned-vs-unconditioned split itself (n=340/1,141, WR/mean-win
  figures and CIs above) stands and does not need re-derivation for a first-pass re-MC design.
  Forbidden re-opens: retuning the conditioner's own threshold or window in response to this
  result; searching over alternative conditioners; blending panel vintages without disclosure.
- **Stop rule / re-proposal bar:** n/a — INTEGRATE.
- **Board write:** `SESSIONS Open/next: Q-RANGECOND-1 closed RESOLVED 2026-08-30 (conditioned
  ORB-MNQ-1 WR 66.47% vs unconditioned 41.72%, mean win +0.711R lift) -- addendum filed on
  b3-orb-mnq-payability-line.md; a full Tradeify re-MC on the conditioned population is named as
  the next step for STATE queue #1 (Acceptable strategy on the ruled host), needing its own
  operator GO + fresh K + explicit panel-vintage standardization. Panel-vintage drift
  (ORB-MNQ-1's own 2019-05-06-start admission panel vs the current 2020-07-01-start
  MNQ_M15.csv) is a new, disclosed watch-item, not yet a standing gate.` Owner: this closure.
- **Registry:** `n/a — governance, not a strategy-grounds kill (RESOLVED, not FALSIFIED)`.

## §10 audit-hook discharge

```text
$ python lab/analysis/_inbox/rangecond_1_2026-08-30/phase1_2_3_conditioned_orb.py
n_trades=1541, n_conditioned=340, WR conditioned=0.6647 / unconditioned=0.4172,
mean-win conditioned=+1.5714 / unconditioned=+0.8603, WR-diff CI=[+0.1830,+0.3131],
mean-win-diff CI=[+0.5430,+0.8868], VERDICT=RESOLVED                                   OK

$ grep -n "2019-05-06" lab/analysis/orb/orb_mnq_2026-07/RESULTS.md
line 15: full confirm panel 2019-05-06->present                                        OK

$ python -c "print(2.0*(0.91+0.50)/2.0)"
1.41                                                                                    OK
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-30 | Closure authored — Phase 1-3 executed under the operator's Route ① ruling, verdict RESOLVED with a disclosed panel-vintage caveat | Claude Code |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/Q-RANGECOND-1-closure-resolved.md
```
