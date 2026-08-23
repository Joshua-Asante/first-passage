# Q-STATVALID-1 — CLOSURE: `FALSIFIED` (Limb C fires on both grids; Limb B independently blocked on missing panel data)

**Verdict:** `FALSIFIED`
**Closed:** 2026-08-23
**Lane:** `UNASSIGNED`
**Pre-registration:** [`Q-STATVALID-1-verdict-preregistration.md`](../pre-registration/Q-STATVALID-1-verdict-preregistration.md) — frozen before either Phase 1 read ran, this session
**Successor:** named, not opened — a DSR/PBO correction-pass packet on the DD-trigger and allocation grids (see Iterate block)
**Spend / K:** $0.00 · K consumed: 0
**Live effect:** none — this closure reads whether prior selections were multiplicity-corrected; per brief §5 it has no authority to move `DD_TRIGGER`, `DD_SCALE`, or any allocation regardless of verdict
**Artifacts:** brief at `docs/briefs/Q-STATVALID-1-mc-resampling-and-constant-multiplicity.md`; pre-registration above; this closure

---

## 1. Verdict (§6 asserted against actual numbers)

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` | Both limbs Reject: B clean (no lag 1-4 breach, Ljung-Box p≥0.05 all lags) AND C clean (both grids' winner margin exceeds noise floor) | B: cannot be read on the panel the brief specifies (unlocatable at $0) — not a clean Reject. C: margin collapses into noise floor on both grids. | — |
| `FALSIFIED` | Either limb Accepts: B any lag-1-4 breach/p<0.05; OR C deflated margin collapses into noise floor, or losing-candidate scores unrecoverable | C fires via **both** independent sub-conditions: (i) DD-trigger grid — only 2 of 5 candidates carry retained exact bust-rate numbers (losing-candidate scores unrecoverable for the other 3); (ii) both grids — winner-vs-runner-up margin collapses to z≈0.8-1.2 against the SE-of-proportion noise floor at N=30,000 MC paths, far under the 2-sigma bar, using only the numbers that *are* retained. | ✓ |
| `AMBIGUOUS-HOLD` | Panel data or logged grid scores for either limb are not locatable at $0/K=0 | Limb B's own panel (the Pepperstone 4-strategy panel behind the DD-trigger ADR and the 99.83%/0.17% MC anchor) is confirmed unlocatable at $0 (retired 2026-08-03, "no offline rollback copy... fresh TradingView re-export, not a restore"). This condition is real and is carried forward as Limb B's own named absence-finding. Per the frozen pre-registration's overall-verdict resolution rule, an unlocatable-data limb converts *that limb* to an absence-finding; it does not override a decisive Accept already reached by the other limb. Limb C's Accept is decisive (rests on computed numbers, not an absence), so the top-level verdict is `FALSIFIED`, not `AMBIGUOUS-HOLD`. | Partially — Limb B only; does not govern the top-level verdict per the pre-registered resolution rule. |

**Mechanical note on why FALSIFIED, not AMBIGUOUS-HOLD, governs:** brief §6's `FALSIFIED` and `AMBIGUOUS-HOLD` rows have literally-overlapping trigger text ("panel data... not locatable" appears as a sub-condition either row could plausibly claim). The pre-registration (authored before either read ran) froze the resolution rule precisely to avoid deciding this after seeing the numbers (Known Trap #12): a blocked limb becomes a named absence-finding, and the overall verdict is set by whichever limb *does* reach a decisive read. Limb C reached a decisive, numerically-grounded Accept on both grids; Limb B did not reach any decisive read (neither Accept nor Reject) because its required data does not exist in this working tree. FALSIFIED is the mechanically correct top-level row.

## 2. What the pre-registration predicted vs what happened

The pre-registration named the exact Ljung-Box threshold and the exact SE-margin proxy formula before either grid's numbers or the panel's autocorrelation structure were read, and explicitly anticipated the possibility that Limb B's panel would be unlocatable (naming that scenario's resolution rule in advance, since the 2026-08-03 Pepperstone retirement predates this brief's 2026-08-18 authoring and was knowable, though not checked, at authoring time). What happened matches that anticipation exactly: Limb B's panel is indeed gone, and the pre-registered resolution rule discharged cleanly without needing a post-hoc decision. Limb C's outcome was not anticipated in direction — the brief left open whether the grids' margins would survive; both grids' margins turned out to collapse well inside the noise floor (z ≈ 0.8-1.2, versus a 2-sigma bar), and one grid additionally failed on the more basic "were the losing scores even kept" question.

## 3. What this closure does NOT license

- Does **not** license re-deriving or re-tuning `DD_TRIGGER`, `DD_SCALE`, or any allocation weight. Both are frozen constants under change-control (pre-registration → re-MC → regime-robustness gate → admitting ADR per CLAUDE.md §Protection); this closure only reads whether the *original* selection was multiplicity-corrected.
- Does **not** license running a fresh MC simulation or a Politis–White block-length selector "to just check" — that is new K/compute spend outside this brief's $0/K=0 scope and outside this closure's authority.
- Does **not** license treating this FALSIFIED verdict as itself widening the block length or adding a multiplicity correction. Per the `concept-not-constant` discipline, any resulting change needs its own pre-registration → re-derivation → admitting ADR (brief §5, 4th forbidden move).
- Does **not** claim the DD_TRIGGER/DD_SCALE or allocation *decisions themselves* were wrong on the merits — only that the search process behind them was never priced for having taken a maximum over several noisy trials, and that the actually-live `DD_TRIGGER=1.5%/DD_SCALE=0.40×` constants (per `core/dd_protection.py:80-81`, the 2026-05-08 C2-relock superseding the 2026-04-17 ADR's 1.0%/0.40× winner examined here) trace through the same uncorrected-grid pattern, not through this specific grid's numbers.
- Does **not** resolve Limb B. It is recorded as an open, independent absence-finding with its own re-test trigger (below) — a future session finding a usable panel does not retroactively make this closure's FALSIFIED verdict wrong; it would simply give Limb B its first-ever decisive read.

## 4. Defects found in the frozen brief (recorded, not repaired)

- **§0 citation drift:** brief cites `core/mc/modes.py:643-658` for `SWEEP_CONFIGS`. That range is actually the DD-trigger sensitivity-grid `_row()` summary function plus the start of the `PRE_SHOCK_1R` dict. The actual `SWEEP_CONFIGS` (the 8-config allocation grid) sits at lines 682-691. Did not change any conclusion — the correct object was located via `grep -n "SWEEP_CONFIGS"` and used.
- **§7 Phase 1a implicit assumption:** "Run `core/mc/ingest.py::build_week_blocks(panel)` on the existing locked panel" presupposes a panel is loadable. The Pepperstone panel behind the actual locked constants was retired 2026-08-03 — a fact already committed to the repo 15 days before this brief's 2026-08-18 authoring, but not checked against at authoring time. The brief's own §6 `AMBIGUOUS-HOLD` row anticipates exactly this class of gap in the abstract, so this is a completeness gap in Phase 1a's design, not a gap in §6's coverage.

## 5. Lesson candidates

**Candidate — "A grid-search FALSIFIED verdict can coexist with a fully-retained-scores grid."** The allocation grid (`SWEEP_CONFIGS`) kept exact numbers for all 8 candidates and still collapsed into the noise floor once an SE-of-proportion read was applied — multiplicity risk is not only a "we didn't log it" problem, it survives even a scrupulously-logged grid when N (MC paths) is held roughly fixed and the winner's margin over the runner-up is thin relative to that N's own sampling noise. Below the two-firing bar (one grid, one brief) — watch, do not promote yet.

## Iterate — loop exit

- **Verdict used:** `FALSIFIED`
- **Model update:** the repo's DSR/multiplicity discipline, which is genuinely rigorous for strategy-candidate discovery (`docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md`, `axis_screen.py` Clause K), was confirmed to have a real, load-bearing gap one layer down: the risk-control layer's own grid-selected constants (`DD_TRIGGER`/`DD_SCALE`, allocation weights) were chosen the same way strategy candidates are screened *before* multiplicity correction existed for them — small grid, same panel scores the winner, thin margins, and (for one of the two grids) most losing scores never even kept. This confirms audit findings B1/C1 rather than surprising against them; the genuine new information is *how thin* the margins are (z≈0.8-1.2, not merely "uncorrected in principle") and that the panel needed to even attempt Limb B's own question is now gone.
- **Next:** ITERATE
- **Routing:** Return to dated packet / operator decision item — name (do not open) two successor items: (a) a formal DSR/PBO correction-pass packet on the DD-trigger and allocation grids (Limb C fired); (b) Limb B's re-test trigger (below), which is not a Politis-White re-derivation packet yet since Limb B never received a decisive read to falsify.
- **Entry packet:** *(required, Next=ITERATE)* — Carries forward: (1) the exact SE-of-proportion formula and N=30,000 proxy assumption frozen in this closure's pre-registration, ready to reuse; (2) the two grids' full retained numbers (DD-trigger: 1.55%/1.66%; allocation: all 8 `SWEEP_CONFIGS` rows via the Q-SWAP-3 closure, retrievable at `git show pre-prune-2026-08-08:docs/ltm/briefs/Q-SWAP-3-closure-ambiguous.md`); (3) forbidden re-opens — no re-deriving `DD_TRIGGER`/`DD_SCALE`/allocations under any successor without its own fresh pre-registration → re-MC → regime-robustness gate → admitting ADR; (4) budget: a closed-form deflation pass on already-logged numbers is $0/K=0 — only a *fresh* MC re-run (if a successor decides the constants must move) would spend K.
- **Stop rule / re-proposal bar:** Limb C's finding re-opens only with new *mechanism* evidence — i.e., a successor DSR/PBO pass that either confirms the winner survives full deflation (closes clean) or confirms it doesn't (feeds a re-derivation packet); it does not soften with time. Limb B's absence-finding re-opens the moment any of: (a) a fresh 4-strategy TradingView re-export is produced (any broker), (b) the MC engine's `dd_protection`-consuming path is next run against any 4-leg (or full replacement) panel for an unrelated reason — piggyback the joint (not single-leg) Ljung-Box read onto that run at $0 marginal cost, (c) the `--panel cme` registry entry is repaired to be "a working 4-leg MC re-run" per its own docstring's current disclaimer.
- **Board write:** `STATE.md` OPERATOR QUEUE — add: "Q-STATVALID-1 CLOSED-FALSIFIED 2026-08-23 — DD-trigger/allocation grid multiplicity confirmed uncorrected (z≈0.8-1.2 vs 2-sigma noise floor on both grids); successor DSR/PBO-pass packet named, not opened. Limb B (resampling-unit autocorrelation) independently AMBIGUOUS — locked Pepperstone panel unrecoverable at $0; re-test triggers on next 4-leg panel availability." *(This closure does not itself commit to STATE.md — the operator/parent session owns that write; the line above is the exact text to add.)*
- **Registry:** `n/a — governance/statistical-validity question about the risk-control layer's own calibration process, not a strategy-candidate mechanism kill; no `rejected_candidates.md` row is owed.`

## §10 audit-hook discharge

All of the brief's own §10 hooks were run or their equivalent confirmed this session:

```
$ grep -n "def build_week_blocks" core/mc/ingest.py
191:def build_week_blocks(panel: pd.DataFrame) -> np.ndarray:

$ sed -n '215,255p' core/mc/simulation.py   → confirmed line 249:
249:        indices = rng.integers(0, n_blocks, blocks_per_sim)

$ grep -n -B2 -A2 "Politis" docs/methodology/references/statistics-of-tradable-anomalies.md
→ line 96-98 confirmed verbatim (Politis-White 2004 named as "automatic selector," never run)

$ sed -n '30,45p' docs/adr/2026-04-17-dd-trigger-calibration.md
→ confirmed: 5-candidate "Alternatives considered" grid, only 2 with exact bust-rate numbers

$ sed -n '640,660p' core/mc/modes.py   → citation drift found (see §4 above); correct
  SWEEP_CONFIGS location confirmed at lines 682-691 via `grep -n "SWEEP_CONFIGS"`

$ git show pre-prune-2026-08-08:docs/adr/2026-04-17-dd-trigger-calibration.md
→ not needed; this ADR was never pruned, live at its normal path

$ grep -n -i "DSR\|PBO\|multiplicity" docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md docs/methodology/regime_robustness_gate.md
→ regime_robustness_gate.md: 0 hits (confirmed).
→ K-bank ADR: many hits, all scoped to "discovery/harvest intake and the K-ledger semantics
  that feed DSR" (line 62, explicit scope statement) and explicitly excluding any
  `dd_protection`/allocation/`core/` change (§5 forbidden moves). Matches expectation exactly.
```

Additional Phase-1-proper commands run beyond the §10 hooks (Ljung-Box execution, Pepperstone-retirement confirmation, Q-SWAP-3 pre-prune retrieval, SE-margin arithmetic) are cited in full in this session's Phase-1 findings; not repeated here for length.

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-23 | Closure authored (Phase 1 executed same session, operator GO) | Claude Code |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/Q-STATVALID-1-closure-falsified.md
grep -c "Fired?" docs/briefs/closures/Q-STATVALID-1-closure-falsified.md
```
