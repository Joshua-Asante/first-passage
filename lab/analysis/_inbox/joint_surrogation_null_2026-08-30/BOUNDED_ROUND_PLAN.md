# Joint-surrogation thread — closure-path plan (post-hard-stop)

**Status: PROPOSED — pending Codex review + operator ratification of the ⚖ items below.
REVISED 2026-08-30, twice in one pass:** (a) merged with `main` after **PR #225 executed the
ratified bounded round in parallel with this doc's authoring** — a disclosed parallel-authoring
collision: this doc's original §3 proposed remedy slots for a round that PR #225 ran the same day
(Round 4, four Codex correction passes: **neither model adequacy nor estimation-aware size/power
clears; hard stop fired as ratified**); (b) revised for Codex's PR #226 review of this doc itself
(9 findings — every one accepted or accepted-as-clarified, dispositions in §7). The original
remedy content is superseded as *execution* guidance and survives only as re-open design
requirements (§3).

What this doc now is: **the concrete proposal for the §6 gate-table gap the fired hard stop
raised to the operator** — the closure path for `Q-RANGEXFER-1`, and the independence case for
`Q-VOLREGIME-1`.

Owner brief: [`Q-RANGEXFER-1`](../../../docs/briefs/Q-RANGEXFER-1-overnight-range-gap-magnitude-transfer.md) §7/§11.
Execution record this plan closes against: [`RESULTS.md`](RESULTS.md) (Rounds 1–4 + four Round-4 correction passes).

---

## §1 — Decision context (all facts already on record)

1. **The hard stop has fired.** Round 4 (PR #225, the ratified bounded round) ran two
   model-adequacy remedies plus the production-grade size re-certification; after four Codex
   correction passes: corrected null false-positive rate **26%** (95% CI [15.9%, 39.6%], p≈0 vs
   nominal 5%), model adequacy failing **both** channels on the df-corrected absolute
   residual-whiteness check, and a disclosed scope limitation (neither remedy tested the
   production rank-based construction). Per the ratified mandate: no further design rounds; the
   §6 gate-table gap is disclosed and raised to the operator. The corpus-insufficiency
   conclusion is now **measured, not hypothesized**.
2. **L4 already fired on all five hypotheses** ([`rangexfer_byyear_l4_2026-08-30/RESULTS.md`](../rangexfer_byyear_l4_2026-08-30/RESULTS.md),
   Codex-corrected: parents `n_valid=3`, others 4–6, all `< 7`). `RESOLVED` was unreachable at
   this panel length even before the hard stop.
3. **Under the frozen map, a valid but non-significant attribution limb gates nothing.**
   Pre-registration §C freezes L5 as "NEVER GATES on its own — TYPES the verdict"; §D's
   `FALSIFIED` fires only on outright L1–L3/L4 failure or L5 *VOID*. So the presence limbs alone
   decide every reachable verdict: `FALSIFIED` on outright presence failure, `AMBIGUOUS-HOLD`
   (or the new row proposed in §4) otherwise.
4. **The frozen texts contradict each other on L5 semantics.** The brief's own §4 ("otherwise
   the incremental lift is an artifact of the shared same-day regime") and sibling
   `Q-VOLREGIME-1`'s §6 (Codex-corrected, PR #210) treat valid-but-non-significant attribution
   as the falsification branch; pre-reg §C says the opposite. A documented internal
   inconsistency between frozen artifacts, not a new design choice.

---

## §2 — The three live steps

**P1 — Complete the presence battery (L1–L3) for all five hypotheses.** Same class as the L4
diagnostic (PR #224): frozen limb definitions (pre-reg §B/§F.2/§G.2), computed from the cached
joint frames, K-free re-derivation of already-scored panels. **This is now the
verdict-determining computation**: with L4 AMBIGUOUS everywhere and no certifiable L5 in
existence, an outright L1–L3 failure routes that hypothesis to `FALSIFIED`; a full L1–L3 pass
routes it to the §4 closure row. Per-hypothesis outcomes are recorded separately and never
overwritten by the design-level closure (§4).
*Environment precondition (Codex #226 finding 4):* the two exact-panel MYM re-runs owed from
PR #224 (frozen 1,307-day panel; the `H-RANGEXFER-1.b-MYM` 2026 boundary case, exactly 20
conditional cases) require hash-verified vendor bars in the executing environment — gitignored
bytes travel with no checkout, so runnability is environment-relative. In the authoring worktree
both CSVs are present and were hash-verified against the tracked `SHA256SUMS` this session
(`MNQ_M15.csv` → `6c86f41a…`, `MYM_M15.csv` → `24e16952…`, both match). Any other executing
environment must re-verify or declare the re-runs blocked pending vendor data.

**P2 — ⚖ Operator ruling: L5 semantics, frozen at closure time.** Does a certified, valid,
non-significant L5 falsify H (Option A — matches §4's own text and the sibling brief; recommended)
or only type it (Option B — pre-reg §C as frozen)? The hard stop makes this ruling *cheaper*, not
moot: no certified L5 exists or can exist now, so freezing the semantics today fixes the
**re-open contract** (what a future certified design's result would do) at the one moment nobody
can be choosing a verdict by choosing the rule. Disclosed in the ruling record: the exploratory,
uncertified p_upper=0.785 lead already points at this cell. Under Option A, also freeze
precedence — **FALSIFIED > AMBIGUOUS-HOLD when both fire** — on both briefs (the sibling's §6
carries the same dual-fire ambiguity).

**P3 — `Q-VOLREGIME-1` by-year L4 qualifying-year count.** Cheap, parallel, K-free, from vendor
bars (same environment precondition as P1). Bar-level panels span 7 calendar years with enormous
per-year n — `N_valid ≥ 7` may PASS, making `RESOLVED`/`FALSIFIED` genuinely reachable there,
which would materially change the value of any future certification attempt (§5).

---

## §3 — Original remedy slots: SUPERSEDED as execution, retained as re-open requirements

This doc's original R1 (HAR(1,5,22) cascade generator) and R2 (ARFIMA with fast estimation +
parameter-uncertainty handling) were authored without visibility into PR #225's same-day
execution of the ratified round. They are **not** licensed as additional rounds — that would be
the forbidden third remedy under the fired hard stop. They stand only as candidate design
classes for re-open trigger (b) of the §4 closure row, and any future candidate must now meet
the following **certification requirements**, consolidated from Codex's #226 review (findings
1–3, 5–7) and Round 4's own corrections — recorded now so a future session inherits the full
bar, not a diluted memory of it:

1. **Adequacy = relative AND absolute.** A relative gate (beat naive benchmark, separate from a
   known-inadequate comparator) cannot detect "every candidate is inadequate"; require in
   addition an absolute real-data check — df-corrected residual-whiteness (the check that killed
   Round 4's remedy 2) and/or direct post-generation dependence checks. Synthetic criterion
   validation does not substitute: it tests panels where the candidate is true by construction.
2. **Certify the deployed construction, not a proxy.** Adequacy and size/power must be scored on
   the final post-coupling, post-rank-remap surrogate pairs — the transformations can change
   exactly the dependence the null must preserve. (Round 4's third correction pass hit the same
   wall from the other side: both its remedies tested a log-Pearson proxy, not the production
   rank-based construction.)
3. **Per-N integer acceptance cutoffs, or one N everywhere.** The original shared `[0.01, 0.08]`
   band was not a valid binomial region across replicate counts (N=200: accept counts 4–16,
   coverage 96.7%; N=100: accept 1–10, coverage 98.3% — computed exactly this session). Freeze
   integer cutoffs per N at freeze time, or use the same N for every battery.
4. **Certify every (instrument × predictor-pair × panel-restriction) actually scored.** The
   parent hypotheses use (overnight range, RTH range); the `.a`/`.b` hypotheses use (gap
   magnitude, RTH range) on restricted panels with different marginals and dynamics — a
   certification at one pair licenses nothing about another.
5. **Zero-safe frozen transforms.** `c24_joint_frame.csv` contains `gap == 0` rows (5 obs), so
   any log-space fit on gap channels is invalid as written; the transform (offset, `log1p`, or a
   rank/normal-scores formulation) must be frozen before fitting, per channel, not improvised
   after a fit fails.
6. **No naive parameter-bootstrap null.** Drawing surrogate parameters from the bootstrap
   distribution of estimates reproduces the estimator's bias (acute for `d̂` near the 0.5
   boundary) and is not conservative, contrary to this doc's original claim — corrected. A
   future size fix must use a calibrated confidence-distribution construction or a full nested
   parametric bootstrap (simulate → refit → recompute the complete procedure per replicate).

---

## §4 — Closure mechanics (the §6 gap proposal, per-hypothesis)

Scored **per hypothesis**, on P1's outcomes — a P1 falsification is never overwritten by the
design-level closure (Codex #226 finding 9):

- **Any outright L1–L3 failure → `FALSIFIED`** for that hypothesis under the existing frozen
  row, no null needed. Mixed outcomes file per the brief's own §9 convention.
- **All presence limbs pass (L4 AMBIGUOUS) → the new row, proposed for operator ratification:**

  **`AMBIGUOUS-DESIGN`** — *"presence limbs pass but no certifiable joint-surrogation
  attribution design exists at current panel length (4 rounds + 4 correction passes, 9
  constructions, 2 ratified remedies — all failed certification; RESULTS.md is the evidence
  record). Presence-level evidence stands as typed by stage-1; every L5-class limb — including
  the two frozen counter-stratum rejection branches (H-RANGEXFER-1.a's overnight-hot
  generalization check, H-RANGEXFER-1.b-MYM's `bprime=1` reversal check) — is design-blocked
  and explicitly not evaluated (Codex #226 finding 8). ITERATE with re-open triggers: (a) the
  panel reaches ≥7 qualifying years under the corrected per-stratum L4 gate, (b) a genuinely
  different design class arrives meeting every §3 requirement, (c) an externally validated
  method for joint long-memory surrogation under estimation becomes available. On re-open, a
  certified valid non-significant L5 disposes per the ⚖ P2 ruling. No calendar-dated re-test."*

`Q-VOLREGIME-1` is **not** closed by inheritance — assessed independently per §5, consistent
with the ratification's scoped-to-`Q-RANGEXFER-1`-only clause.

---

## §5 — Where a future certification's value actually lands

The largest expected payoff of a certified joint long-memory null was never `Q-RANGEXFER-1`
(ceiling `AMBIGUOUS-HOLD`/`FALSIFIED` regardless) but: (1) `Q-VOLREGIME-1`, where L5-gating
semantics are already frozen, both day-level failure mechanisms are materially weaker at
n≈135k–140k bars (estimation noise in `d` shrinks; the L4 wall may not exist per P3), and
`RESOLVED` may be genuinely reachable; and (2) every future S2-shaped cross-series question —
the D5/O1 "UNRESOLVED-NEEDS-DESIGN" debt is a standing instrument gap. The hard stop closes this
*attempt*, not the instrument gap: §3's requirements are the inherited spec for whoever next
picks it up, at bar-level n first (where certification is most likely to succeed and most
valuable), not day-level.

---

## §6 — Corrections to the external Codex mechanism-review report (adopted with adjustments)

The report's critical-path diagnosis and Priorities 1/3/5 were adopted; Round 4 has since
executed the substance of Priorities 1–3. Standing corrections:

1. "Attribution failure produces FALSIFIED" is wrong for `Q-RANGEXFER-1` as frozen — only L5
   *VOID* falsifies; valid-but-non-significant gates nothing (pre-reg §C/§D). True for
   `Q-VOLREGIME-1` only. This is the ⚖ P2 ruling.
2. Its §5.A panel-length section was stale: the L4 wall already fired on all five hypotheses
   (PR #224), corrected parents' `n_valid=3` — `RESOLVED` already unreachable.
3. Its "close the thread AMBIGUOUS" fallback must route through the ratified mechanism — §6 gap
   disclosure + fresh operator gate amendment (§4 above) — not the existing L4-specific
   `AMBIGUOUS-HOLD` row (already ruled, PR #223).
4. Its K section was partially stale: amounts already declared and corrected (K_fresh=2/2, +1
   for the reused real-data look; batch K=5 non-stacking, operator-ratified); what remains owed
   is formal registration at any future Phase-3 execution.
5. "Volume transitively blocked" is right for sequencing but wrong as a verdict coupling —
   `Q-VOLREGIME-1` is assessed on its own panel (§5).

---

## §7 — Codex review of this doc (PR #226): 9 findings, dispositions

| # | Finding | Disposition |
|---|---|---|
| 1 (P1) | Relative-only adequacy gate can pass when all models are inadequate; synthetic validation doesn't close it | **Accepted — and empirically vindicated the same day:** Round 4's correction added exactly this absolute check (df-corrected Ljung-Box residual whiteness) and it flipped the adequacy verdict to FAIL on both channels. Folded into §3 req 1. |
| 2 (P1) | Adequacy must be scored on the final post-coupling, post-remap surrogates, not per-channel fits | **Accepted** — §3 req 2; independently mirrored by Round 4's third-pass scope disclosure (both its remedies tested a log-Pearson proxy, not the production construction). |
| 3 (P2) | Shared [0.01,0.08] band is not a valid binomial region for both N=200 and N=100 | **Accepted** — exact per-N integer regions computed (N=200 → [4,16]; N=100 → [1,10]); §3 req 3 freezes per-N cutoffs or one N everywhere. |
| 4 (P2) | Vendor bars absent from the reviewed tree; MYM cache is 1,304 not 1,307 days — "runnable" overstated | **Accepted as clarified** — runnability is environment-relative (gitignored bytes travel with no checkout). Both CSVs are present in the authoring worktree and were hash-verified against `SHA256SUMS` this session; §2 P1 now states the precondition explicitly and the blocked-pending-vendor-data fallback. |
| 5 (P1) | One battery at MNQ-fitted overnight-pair parameters does not certify the gap-magnitude pairs | **Accepted** — §3 req 4: certification per (instrument × predictor-pair × panel-restriction) actually scored. |
| 6 (P1) | log-space HAR fit is invalid on gap channels (`gap==0` rows exist in the committed frame) | **Accepted** — §3 req 5: zero-safe transform frozen per channel before fitting. |
| 7 (P1) | Drawing θ* from the bootstrap distribution of estimates reproduces estimator bias; "errs conservative" was wrong | **Accepted — original claim retracted.** §3 req 6 replaces it with calibrated confidence-distribution or full nested parametric bootstrap. |
| 8 (P1) | The two frozen counter-stratum rejection branches (§4 of the brief) were never scheduled | **Accepted** — they are L5-class limbs, so under the hard stop they are design-blocked like the primary attribution limbs; the §4 closure row now names them explicitly as not-evaluated rather than silently omitted. On any re-open they enter the mandatory execution set. |
| 9 (P1) | The unconditional fail branch would overwrite P1 falsifications with `AMBIGUOUS-DESIGN` | **Accepted** — §4 is now per-hypothesis: `AMBIGUOUS-DESIGN` applies only to presence-passers; P1 `FALSIFIED` outcomes stand; mixed outcomes file per the brief's §9. |

Findings 1–3 and 5–7 targeted the remedy sections that PR #225's parallel execution has since
superseded — they are dispositioned as **re-open design requirements** (§3), not as changes to
work that will still run under this thread.

## Audit hooks

```bash
# The facts §1 rests on
grep -n "NEVER GATES" docs/briefs/pre-registration/Q-RANGEXFER-1-verdict-preregistration.md
grep -n "n_valid" lab/analysis/_inbox/rangexfer_byyear_l4_2026-08-30/RESULTS.md
grep -n "p_upper > 0.05" docs/briefs/Q-VOLREGIME-1-intraday-bar-volume-regime.md
grep -n "hard stop fires\|26%" lab/analysis/_inbox/joint_surrogation_null_2026-08-30/RESULTS.md

# The corrected production-grade size figure (Round 4, third correction pass)
python lab/analysis/_inbox/joint_surrogation_null_2026-08-30/_refit_per_replicate_positive_control_v2.py
# Expected: null false-positive 13/50 = 26% (95% CI [15.9%,39.6%]) vs nominal 5%

# Vendor-bar precondition check (any executing environment, before P1/P3)
python - <<'PY'
import hashlib
for f in ("MNQ_M15.csv", "MYM_M15.csv"):
    h = hashlib.sha256(open("core/data/bar_data/" + f, "rb").read()).hexdigest()
    print(f, h[:16])
PY
# Expected: 6c86f41a17b7dfce / 24e169528f7ea669 (match SHA256SUMS), else P1/P3 are blocked

# Per-N binomial acceptance regions (§3 req 3)
python -c "
from math import comb
def cdf(n,p,k): return sum(comb(n,i)*p**i*(1-p)**(n-i) for i in range(k+1))
for n in (200,100):
    lo = next(k for k in range(n) if cdf(n,0.05,k) > 0.025)
    hi = next(k for k in range(n) if cdf(n,0.05,k) >= 0.975)
    print(n, lo, hi)
"
# Expected: 200 4 16 / 100 1 10
```
