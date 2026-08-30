# Q-VOLREGIME-1 — Verdict pre-registration (H-VOLREGIME-MNQ / H-VOLREGIME-MYM)

**Frozen:** 2026-08-30, before Phase 1 (the 1-bar-lag joint-surrogation null design) has been
written, reviewed, or run, on either instrument. Parent brief:
[`Q-VOLREGIME-1-intraday-bar-volume-regime.md`](../Q-VOLREGIME-1-intraday-bar-volume-regime.md).
Operator GO for Phase 1 design work: **owed, not yet granted** — this freeze does not authorize
Phase 1; it only pins the classification thresholds so Phase 1, once GO'd and reviewed, cannot be
tuned to its own result.

A verdict computed after moving any threshold below, the window/quantile constants, or the
by-year N_valid floor is void.

**Forbidden regardless of outcome:** no threshold moves after Phase 1 results exist. If the
joint-surrogation design (once adapted from `Q-RANGEXFER-1`'s own sketch) cannot be scored against
these frozen limbs without modification, that is a new design decision requiring a fresh freeze —
not an edit to this one.

**Precondition freeze (§A-E and §F below both gated on this, added 2026-08-30):** neither
instrument's L1–L4/L5 limbs may be scored until that instrument's own within-stratum
`circular_shift_null_p` (Phase 0.5 of the parent brief) has actually been computed — the parent
brief's own §1 found this uncomputed on **both** instruments (MYM per PR #207's own review; MNQ
because it has never been reviewed for the identical gap, not because it passed one). A verdict
of `PRECONDITION-UNMET` is not one of L1-L4/L5's own outcomes — it is scored before them and
short-circuits the rest of this file's own limb tables until cleared.

---

## §A — Frozen constants, MNQ (adapted from the same frozen corrected-null-battery spec's D2
table, `docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md`, to the cross-series,
1-bar-lag case; not re-derived, not re-tuned)

- `TRAIL_N = 60` (trailing same-time-of-day-slot occurrence count for the volume baseline —
  carried verbatim from `candidate3_volume_regime.py`'s own `TRAIL_N` constant, not re-chosen
  here. **Corrected 2026-08-30 (Codex review, PR #210):** an earlier draft of this freeze wrote
  `TOD_WINDOW = 20` for MNQ, copying MYM's own `c3_stratified_rerun.py` constant (`TOD_WINDOW`)
  without checking MNQ's own script, which uses a differently-named, differently-valued
  constant (`TRAIL_N = 60`). Freezing 20 for MNQ would have meant Phase 1 tests a baseline
  window MNQ's own cited +20.6pp/+25.6pp stage-1 result never actually used — this instrument's
  own window is now correctly frozen at its own value. See §F.1 for MYM's own, separately-named
  and separately-valued `TOD_WINDOW = 20`.)
- `Q_VOLUME = 0.50` (above-own-slot-median threshold, i.e. `ratio > 1` — matches both scripts'
  own already-run design; **not** a top-quintile threshold like `Q-RANGEXFER-1`'s `Q_BIAS=0.80`,
  since candidate 3's own stage-1 design used a median split, disclosed here rather than silently
  reconciled to a different scheme)
- `alpha = 0.05`
- `N_FLOOR_POP = 400`, `N_FLOOR_COND = 100` (L1 analogue, population and conditional-cell floors
  — both instruments' own stage-1 n's, 130k-140k range, clear this trivially; the floor matters
  once Phase 1 restricts to a by-year or three-way-conditioned sub-panel)
- `YEAR_MIN_NCOND = 20`, `N_valid >= 7` else AMBIGUOUS (L4 analogue — **known risk, disclosed
  ex-ante, not yet computed for this construct on either instrument**: `daily-range-state-persistence`
  and `Q-RANGEXFER-1`'s own H-RANGEXFER-1 both hit N_valid=6 on this identical MNQ panel span for
  their own by-year tables; this construct's own by-year distribution may or may not behave the
  same way, since the conditioning event — above-median same-slot volume — occurs far more
  frequently per year than either of those constructs' own top-quintile/top-decile triggers, and
  a denser per-year trigger count could plausibly clear N_valid where a sparser one didn't)
- CI block-bootstrap: `block = 96` bars (≈1 trading day), consistent with both instruments' own
  already-run stage-1 scripts (`candidate3_volume_regime.py`, `c3_stratified_rerun.py`) — **not**
  `Q-RANGEXFER-1`'s `block = 20 trading days`, since this construct's bias/outcome pairing is at
  bar (not day) granularity; carried verbatim from the already-executed scripts, not re-chosen.

## §B — Presence limbs (L1–L4 analogues, MNQ; GATE, verbatim carry from whichever Phase-1 script
computes them — no re-derivation at verdict time)

| Limb | Content | Role |
|---|---|---|
| L1 | n-floor: n_scored ≥ 400 AND n_cond ≥ 100, both the full stratified panel (n=136,020 already clears trivially) and any three-way-conditioned sub-panel the distinct-WHO check produces | GATES |
| L2 | Block-bootstrap CI lower bound on the minimum stratified incremental lift > 0 | GATES |
| L3 | Both halves (chronological split) of the conditional cases show lift > 0 | GATES |
| L4 | By-year floor: incremental lift > 0 in ≥ N_valid−2 of N_valid qualifying years (n≥20/year); AMBIGUOUS if N_valid < 7 | GATES |

## §C — Attribution limb (L5 analogue, MNQ; NEVER GATES on its own — TYPES the verdict between
RESOLVED-strength and a weaker survival-only reading)

- Whatever joint-surrogation design Phase 1 produces (post-review), its two-sided p_upper against
  the observed minimum stratified lift is the L5 analogue. `p_upper ≤ 0.05` → attribution clears;
  same never-re-roll discipline as the frozen spec's §2 and `Q-RANGEXFER-1`'s own §C.
- The distinct-WHO three-way check (§4 of the parent brief) is **disclosed alongside** L5, not
  folded into it — it types the mechanism-attribution question, it does not gate RESOLVED/FALSIFIED.

## §D — Verdict map (mirrors the parent brief's §6 table exactly; restated here as the frozen,
pre-Phase-1 form)

| Verdict | Trigger | Applies to |
|---|---|---|
| `PRECONDITION-UNMET` | The within-stratum `circular_shift_null_p` precondition (Phase 0.5) cannot be *computed at all* — no vendor bars, no cached scored frame | H-VOLREGIME-MNQ — **current disposition pending Phase 0.5** |
| `PRECONDITION-CLEARED-NULL` (added 2026-08-30, Codex review — distinct from PRECONDITION-UNMET) | Phase 0.5's within-stratum `circular_shift_null_p` **is computed** but does not clear `alpha` (p > 0.05) — the construct fails at the cheap gate, before Phase 1's expensive joint-surrogation design is ever built | H-VOLREGIME-MNQ — `STOP`: DROP this instrument's own H at the $0 gate; do not proceed to Phase 1 on it. Re-proposal bar: a different within-stratum design, not a retune of this one. |
| `RESOLVED` | Precondition clears (p ≤ alpha) AND L1–L4 all pass AND L5 is valid (not VOID) AND clears (p_upper ≤ 0.05) | H-VOLREGIME-MNQ |
| `FALSIFIED` | Precondition clears, then any of L1–L3 fails outright, OR L4 fails outright (N_valid ≥ 7 but fewer than N_valid−2 years clear), OR L5's diagnostic gate VOIDs after the full escalation ladder, **OR L5 is valid (not VOID) but does not clear (p_upper > 0.05)** (added 2026-08-30, Codex review — an earlier draft of this table had no disposition for an ordinary, non-VOID non-significant L5 outcome, which would have let the verdict be chosen after seeing results rather than pre-registered) | H-VOLREGIME-MNQ |
| `AMBIGUOUS-HOLD` | Precondition clears, L1–L3 pass but L4 cannot resolve (N_valid < 7) | H-VOLREGIME-MNQ |

## §E — Pinned ex-ante expectation, MNQ

**Predicted: presence limbs (L1–L3) PASS, L4 outcome genuinely uncertain (not simply predicted
AMBIGUOUS by analogy)** — unlike `Q-RANGEXFER-1`'s own top-quintile/top-decile triggers, this
construct's above-median volume trigger fires roughly half of all bars, which could plausibly
produce enough qualifying observations per calendar year to clear N_valid≥7 even on a panel that
failed that bar for sparser conditioning events. This is disclosed as a genuine, not merely
formal, uncertainty — the prediction is deliberately non-committal rather than assuming the
by-year wall recurs by pattern-matching to two unrelated constructs' own results on the same
panel.

Substituting real Phase-1 numbers to confirm or refute this prediction is the compute step, not
this freeze.

---

**Freeze note (§A-E, MNQ):** this file exists on disk, committed in the same commit as the parent
brief, before Phase 1 has been designed, reviewed, or run — same discipline as `Q-RANGEXFER-1` /
`Q-CONDVAL-1` / `Q-TRAINKILL-1` (freeze-then-score, verified via the parent brief's own `git log`
audit hook).

---

## §F — MYM freeze (same discipline: before MYM's own Phase 1 exists)

### §F.1 — Frozen constants (MYM panel: `core/data/bar_data/MYM_M15.csv`, 2020-07→2026-07)

- `TOD_WINDOW = 20` (MYM's own constant name and value in `c3_stratified_rerun.py` — **not**
  the same numeral as MNQ's own `TRAIL_N = 60` per §A; the two instruments' trailing-window
  lengths are genuinely different in the already-run scripts and are frozen separately here,
  each carried verbatim from its own script, not reconciled to a shared number). Same
  `Q_VOLUME`, `alpha` as §A.
- `N_FLOOR_POP = 400`, `N_FLOOR_COND = 100` — unchanged.
- `YEAR_MIN_NCOND = 20`, `N_valid >= 7` else AMBIGUOUS — same disclosed, genuinely uncertain
  prediction as §E, not assumed to replicate MNQ's own eventual result.
- CI block-bootstrap: `block = 96` bars, `seed = 20260829`, `draws = 4000` — carried verbatim
  from `c3_stratified_rerun.py`'s own already-executed design (the same script and seed that
  produced the +0.1648 mean / CI [+0.1537,+0.1761] figure cited in the parent brief).
- Total scored pairs available: n=139,605, comparable in order of magnitude to MNQ's own
  n=136,020.

### §F.2 — Presence limbs (L1–L4 analogues, MYM; same structure as §B, MYM's own panel)

| Limb | Content | Role |
|---|---|---|
| L1 | n-floor: n_scored ≥ 400 AND n_cond ≥ 100 (n=139,605 total clears trivially; both `bias_hist` strata, n=71,492/68,113, clear independently) | GATES |
| L2 | Block-bootstrap CI lower bound on the minimum stratified incremental lift > 0 | GATES |
| L3 | Both halves (chronological split) of the conditional cases show lift > 0 | GATES |
| L4 | By-year floor: incremental lift > 0 in ≥ N_valid−2 of N_valid qualifying years (n≥20/year); AMBIGUOUS if N_valid < 7 | GATES |

### §F.3 — Attribution limb (L5 analogue, MYM) and verdict map

Identical definition and verdict map to §C/§D, scored against MYM's own Phase 1 output — the
**same adapted design** (§7 of the parent brief), run a second time against MYM's own cached
panel rather than a MYM-specific redesign. **MYM's current disposition is `PRECONDITION-UNMET`**,
per `N-2026-08-29-mym-bar-volume-regime.md`'s own UNRESOLVED status (PR #207) — this is not a
prediction, it is the recorded state as of this freeze.

### §F.4 — Pinned ex-ante expectation, MYM

**Predicted: same genuine (non-committal) L4 uncertainty as MNQ (§E), for the identical reason**
— MYM's own above-median volume trigger has the same roughly-half-of-all-bars firing rate as
MNQ's, so whatever L4 outcome MNQ's own panel produces is not assumed to transfer to MYM's
independently-scored verdict. **Distinct-WHO three-way check:** predicted direction unknown on
either instrument — neither notice's own §3 took a position on which mechanism (A: same
phenomenon as daily-TR persistence, finer grain; B: genuinely incremental) is more likely,
disclosing it as a live, undecided question rather than a soft-predicted one.

Substituting real Phase-1 numbers to confirm or refute this prediction is the compute step, not
this freeze.
