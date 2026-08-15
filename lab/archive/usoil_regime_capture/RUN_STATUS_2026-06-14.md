# Q-USOIL-1 Gate B — CC run status (2026-06-14)

**Terminal state:** `NEEDS_CONTEXT` (the EXPECTED success state after the Step 2.4
emit, per handoff §6 / pre-reg §10). **No Gate B verdict asserted** — Gate B-0
native parity has not been run (it is operator-manual TradingView), and two
structural divergences additionally block the native run until the parent
resolves them. **No anti-SNAG slot consumed** (no concept run occurred).

**Pre-reg:** `docs/ltm/briefs/pre-registration/PREREG-USOIL-RGC-GATEB-2026-06-14.md`
freeze commit `21c538b` — verified unchanged (`git log -1` == `21c538b`).
**Handoff:** `docs/ltm/briefs/handoffs/2026-06-14-cc-handoff-USOIL-RGC-gateB.md`,
executed §0 → §0.5 → §2.

---

## Per-step gate outcomes

| Step | Gate | Outcome |
|---|---|---|
| 2.1 panel-stage + Step-0 battery | panel present + integrity | **BLOCKED-ON-INPUT.** Panel `…c35c1.csv` is in Joshua's Downloads (SHA `256780f0…` verified ✓, 94,507 bars ✓, 2020-01-01→2023-12-29 ✓) but NOT staged under `core/data/tv_exports/pepperstone/`, and `SHA256SUMS` has no `…c35c1` line. Staging is a vendor-data add coupled to a `SHA256SUMS` commit (vendor-integrity gate) — and the handoff forbids commits. **Deferred to operator** (stage + regen manifest in one commit). Step-0 battery NOT run (no staged panel). |
| 2.2 freeze episode partition | partition built before any PnL | **BLOCKED-ON-INPUT** (depends on 2.1's staged panel). Not built. |
| 2.3 codify candidate | composes · long-short · trailing · lint-clean | **PASS.** Emitted `core/strategies/candidates/concept-usoil-rgc-001.pine` (gitignored). `compose_from_hint` → no raise; `entry=breakoutLong`, `short=breakoutShort` (long-short ✓), `trailing=True`, `exit_tp='na'` (no fixed TP ✓), lint-clean ✓. 31 codifier + numpy-twin tests green. |
| 2.4 emit B-0 config specs | anchor + ≥8-cell sample, frozen | **EMITTED.** `gate_b0_config_spec.md` — anchor `(channelLen=384, stopAtr=3.0, trailAtr=3.5)` confirmed real N=36 cell (idx 13); 10-cell representative sample (all unique, all in-grid). **Native run BLOCKED on D-1/D-2 below.** |
| 2.5 sweep N=36 | requires B-0 PASS + panel | **GATED — out of reach** (no B-0 authority, no staged panel). |
| 2.6 deflation battery B-1…B-6 | requires B-0 PASS + panel | **GATED — out of reach.** |
| 2.N verdict + closure | — | **NO VERDICT** (B-0 not cleared). No corpse, no slot consumed. |

---

## Structural divergences escalated to parent (codifier ↔ frozen §3 mismatch)

Detailed in `gate_b0_config_spec.md`. Summary:

- **D-1 — extra entry filter.** The hint's "volatility"+"atr" tokens make
  `compose_from_hint` attach `atr_expansion_filter` (`signalFilterOK =
  atrExpandOK`). Frozen §3 forces "no entry filter / belt filters deferred". The
  emitted candidate has no input to disable it cleanly.
- **D-2 — collapsed stop axes.** Frozen §3 sweeps entry `stopAtr` {2.5,3.0,3.5}
  AND chandelier trail {2.5,3.5,4.5} as **two independent axes** (the N=36
  source). The emitted `chandelier_exit()` reuses ONE `stopAtr` for both
  entry-stop sizing and the trail ratchet (verified in emitted bytes: lines 190 &
  237 both `exitAtr * stopAtr`). The candidate as emitted can only express
  entry-stop == trail cells, so the N=36 grid is NOT runnable on it.

Both are **codifier↔pre-reg parameterisation mismatches**, not parity-band tunes.
Per handoff §5 / pre-reg §7, CC did NOT (a) edit the frozen grid to fit the
emitter, (b) substitute a degraded archetype, or (c) edit the tracked
`lab/codification/primitives.py` in this run. The capability to express
long-short+trailing is proven (Step 2.3); the *exact frozen parameterisation*
needs a codifier change (separate `trailAtr` param; a no-filter hint or filter
on/off bool) — a parent decision touching tracked `lab/` code.

---

## Discipline / audit hooks (all green this run)

- Frozen pre-reg unchanged: `git log -1 … PREREG-…` == `21c538b` ✓
- Frozen thresholds: `PARITY_NET_PF_BAND = 0.02`, `PREFILTER_RANK_RHO_FLOOR = 0.70` ✓
- USOIL absent from `core/firm_rules.py` ✓
- No tracked `core/` mutation; candidate written only to gitignored
  `core/strategies/candidates/` ✓
- Working-tree changes: only `lab/analysis/usoil_regime_capture/**` (untracked)
  + the gitignored candidate + (pending) the `ops/instruments/USOIL.md` session-log
  append. Nothing committed.

## Next action

Operator: (1) stage `…c35c1.csv` under `core/data/tv_exports/pepperstone/` with a
`SHA256SUMS` regen in the same commit; (2) parent decides D-1/D-2 (codifier change
to express the frozen §3 parameterisation) — until then the B-0 native run cannot
faithfully run the frozen grid; (3) once a §3-faithful candidate exists, Joshua
runs the anchor + sample natively in TV and returns the trade-lists for
`parity_check` / `rank_correlation_falsifier`.

---

## UPDATE 2026-06-14 — D-1/D-2 RESOLVED (WI-5), item (2) above CLEARED

Parent chose "extend the codifier". Both divergences fixed in the pipeline
(TDD-first; full `lab/` **248 passed / 19 skipped / 0 failed**; `check_boundaries`
OK; **zero tracked `core/` mutation**):

- **D-2** — `chandelier_exit()` gains an independent `trailAtr` SweepParam +
  `trail_dist_expr`; `SignalModule.trail_dist_expr`; `SignalArrays.trail_dist`
  (optional, `None` ⇒ WI-3 contract byte-unchanged); engine ratchet, numpy twin,
  and the new scaffold slot `{{SIGNAL_EXIT_TRAIL_DIST}}` all use it. Sizing + the
  initial stop stay on `stopAtr`. The N=36 grid is now emit-expressible
  (params ⊇ {channelLen, stopAtr, trailAtr}).
- **D-1** — `FILTER_REGISTRY` keys now require explicit entry-filter intent
  (`"... filter"`/`"... gate"`); "volatility-targeted sizing"/"ATR exit" no longer
  attach a gate. USOIL candidate now emits `entry:breakout, exit:chandelier_trailing`
  (**no `filter:*`**), lint PASS.

Pre-reg **re-frozen r2** (pre-data §3-table correction; original `21c538b`
superseded). **Item (2) is cleared.** Items **(1) panel-staging and (3) native
B-0 run remain owed** — and the native-parity cert is now **fresh** (the trail
distance is an execution-model change). Gate B still NOT run; 0 anti-SNAG slots
consumed. See codifier spec §8b + `ops/instruments/USOIL.md` session log.
