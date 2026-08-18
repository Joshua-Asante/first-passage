# Q-FILLTAX-1 V2 — mutation battery freeze (FROZEN before Phase 2)

**Frozen:** 2026-08-18, operator-directed ("proceed with Freeze the Q-FILLTAX-1 mutation
battery"); authored + run by Claude Code (Sonnet 5).
**Parent brief:** [`../Q-FILLTAX-1-fill-realism-and-parity-scoping.md`](../Q-FILLTAX-1-fill-realism-and-parity-scoping.md)
§7 Track V2 Phase 1 / §8.
**Scope:** **V2 only.** V1 (fill-realism tax) is a separate, not-yet-sequenced limb per the
parent brief's §7 — this freeze says nothing about V1 and does not advance it.
**Rule:** nothing in §2 changes after any family TV-anchor result is seen (Known Trap #12).
Amendment = close this freeze + author a fresh one; the harness gets repaired, never the
tolerance (H-V2).

---

## §0 — Rule-0 reads (this session, with what was verified)

| # | Claim | Verified how | Result |
|---|---|---|---|
| 1 | Parent brief §7 Phase 1 = "freeze the mutation battery (§8)"; §8 names this file's path | Read `docs/briefs/Q-FILLTAX-1-fill-realism-and-parity-scoping.md` in full | ✓ |
| 2 | Harness bands `RANK_RHO_FLOOR=0.75`, `NET_REL_BAND=0.02`, `PF_REL_BAND=0.02`, `MIN_TRADES=30`, FROZEN-PRE-RUN, and "no mutation battery is frozen in this scaffold" | Read `lab/analysis/c1/parity_gen2_2026-08/PREREG.md` §1-§2 | ✓ |
| 3 | Harness scoring surface: `evaluate(engine_pnl, tv_pnl)` (positional/id-aligned pnl only) + `align_series`/`load_trade_series` (trade_id join, else time-sort, else positional) | Read `lab/analysis/c1/parity_gen2_2026-08/parity_gate.py` in full | ✓ |
| 4 | Existing `test_parity_gate.py` covers harness arithmetic (Spearman/PF/net, band checks, one full-inversion case, one trade_id-mismatch case) but **no** named Pine↔Python defect-class battery | Read `lab/analysis/c1/parity_gen2_2026-08/test_parity_gate.py` in full | ✓ 11 tests, none framed as a defect-class battery |
| 5 | This repo's established mutation-battery convention: `tests/core/test_planted_defects.py` — "each row applies one mutation and asserts a named pin turns RED... a row that stays green means the fixture is insufficient" | Read `tests/core/test_planted_defects.py` in full | ✓ pattern mirrored below |
| 6 | Lab-analysis code is pytest-gated from `tests/lab/` via a `sys.path` insert to the lab body, not from inside the lab directory itself | Read `tests/lab/test_funded_scaling_ladder.py` in full | ✓ pattern mirrored below |
| 7 | `pytest.ini_options.testpaths = ["tests"]`; the parent brief's §10 audit hook `pytest tests/ -k "parity" -q` requires the battery to live under `tests/`, not under `lab/analysis/c1/parity_gen2_2026-08/` | Read `pyproject.toml` `[tool.pytest.ini_options]` | ✓ |
| 8 | Striker DJ30's real, historical contractValue defect (default 1 vs required 10, "~7% risk") — cited as M3's precedent | `CLAUDE.md` strategy table; `core/firm_rules.py` L572 comment | ✓ |
| 9 | STEP2_PARITY's real, still-open MYM exit-lag finding — cited as M6's precedent | Read `lab/analysis/c1/q_rail_1_2026-07/STEP2_PARITY.md` (cited in parent brief §0) | ✓ |
| 10 | Q-SIGID-1's real, still-OPEN signal-identity gap — cited as M7's precedent | Read `docs/briefs/Q-SIGID-1-intra-bar-signal-identity.md` in full | ✓ Status `OPEN`, no closure file exists |

---

## §1 — What this freeze does and does not do

Freezes a synthetic, named-defect-class mutation battery that the Gen-2 harness must detect
before it is trusted to score any real family. **This is Phase 1 only.** It does not run
against, or grant engine research authority for, any real strategy family — that is Phase 2
(first family manual TV anchor, operator) and Phase 3 (assert the §6 row), both still owed.
No vendor CSV, no live data, no arming, no spend. $0 · K=0.

---

## §2 — The battery (frozen)

Eight rows: seven named Pine↔Python parity defect classes (M1–M7, each must **FAIL**) plus one
sanity companion (M8, must **ADMIT**) proving detection isn't achieved by a gate that just fails
everything. Baseline is a fixed, deterministic 40-trade synthetic series (16 wins ~$300–339 /
24 losses ~-$100 to -$119.50, every value distinct so Spearman ties never mask a mutation's
effect). Executable form: [`tests/lab/test_q_filltax_1_parity_mutations.py`](../../../tests/lab/test_q_filltax_1_parity_mutations.py).

| Row | Defect class | Precedent / motivation | Mutation | Detection axis (predicted) |
|---|---|---|---|---|
| M1 | Partial direction/side-logic flip | Generic port risk (distinct from the harness's own full-inversion test) | 30% of trades sign-flipped | rho |
| M2 | Uniform per-trade tax omission | The V1 fill-optimism gap itself (SS1) | +$15/trade constant shift | net (rank-preserving) |
| M3 | Proportional contractValue mis-port | **Striker DJ30 default=1 vs required=10**, CLAUDE.md strategy table | ×0.1 scale on every trade | net only (PF is scale-invariant) |
| M4 | Missing trades (port drops a subset) | Generic session/filter port-completeness risk | 5 of 40 trades absent from engine | alignment FAIL (trade_id) |
| M5 | Duplicate trade (port double-counts) | Generic pyramid/re-entry counting risk | 1 trade fires twice in engine | alignment FAIL (trade_id) |
| M6 | Asymmetric exit-timing inflation | **STEP2_PARITY's measured MYM exit lag** (up to +10 bars/2.5h vs CFD), `q_rail_1_2026-07/STEP2_PARITY.md` | winners ×1.20, losers untouched | PF (rank among winners preserved) |
| M7 | Rank decorrelation (tick-level re-evaluation) | **Q-SIGID-1's OPEN signal-identity gap** (`calc_on_every_tick` / mid-bar close mismatch) | 50% block positionally permuted vs TV | rho |
| M8 | Sanity: near-identical pair | "0 false passes" complement (SS6) | ±$0.01 sub-tick noise | must ADMIT |

### Measured result at freeze (2026-08-18, synthetic baseline, this run)

| Row | Verdict | rho | net_rel | pf_rel | Reason(s) |
|---|---|---:|---:|---:|---|
| M1 | FAIL | 0.5816 | 0.9963 | 0.4787 | all three bands miss |
| M2 | FAIL | 1.0000 | 0.2457 | 0.2121 | net_rel, pf_rel (rho exactly invariant, as predicted) |
| M3 | FAIL | 1.0000 | 0.9000 | **0.0000** | net_rel only — PF exactly scale-invariant, empirically confirmed |
| M4 | FAIL | — | — | — | `align:` tv_anchor has 5 trade_id(s) absent from engine |
| M5 | FAIL | — | — | — | `align:` duplicate id resolves as "present in engine but not tv_anchor" (correct FAIL, imprecise message — see §5 note) |
| M6 | FAIL | 1.0000 | 0.4167 | 0.2000 | net_rel, pf_rel (rho exactly invariant, as predicted) |
| M7 | FAIL | 0.3505 | **0.0000** | **0.0000** | rho only — permutation cannot move net/PF (same value multiset), cleanest isolation in the battery |
| M8 | **ADMIT** | 1.0000 | 0.0000 | 0.0000 | no reasons — sanity holds |

**9/9 pytest tests pass** (M1–M8 + one band-literal pin test), reproducible via:

```bash
python -m pytest tests/lab/test_q_filltax_1_parity_mutations.py -v
```

---

## §3 — Verdict rule (verbatim from parent brief §6, V2 row)

| Trigger | Disposition |
|---|---|
| 100% detection (M1–M7 all FAIL), 0 false passes (M8 ADMITs) | `RESOLVED` — land the parity harness as a standing local pre-commit / `make validate` gate (skip-if-missing on clean clones; not GitHub Actions CI) |
| Any missed mutation or false pass | `FALSIFIED` — `ITERATE`: repair the harness, never the tolerance; re-run this battery |

**This freeze's own battery run is 8/8 (100% detection, 0 false passes) — but this satisfies
the harness's synthetic self-test only.** The parent brief's §6 V2 `RESOLVED` row is not fired
by this document alone; Phase 2 (first family manual TV anchor) and Phase 3 (assert the row)
remain owed and operator-gated.

---

## §4 — Forbidden moves

- **Tuning any row above, or the harness's bands, after seeing a family TV-anchor result** —
  this freeze predates any real family data; nothing here may be adjusted post-hoc (Known
  Trap #12). Amendment = close this freeze + author a fresh one.
- **Reading this document's 8/8 result as family-level parity evidence.** It proves the gate's
  discriminating power on synthetic mutations, nothing about any real strategy's Pine↔Python
  behavior. Phase 2 is a separate, still-owed step.
- **Weakening a row to make it pass** if a future re-run of this battery shows a miss — the
  brief's own rule is explicit: repair the harness, never the tolerance.
- **Treating M5's imprecise diagnostic message as a defect requiring a harness code change** —
  detection (FAIL) is what H-V2 gates; message wording is a documented rough edge (§5), not a
  gate failure, and fixing it is optional polish outside this freeze's scope.

---

## §5 — Notes for a future harness maintainer (non-blocking)

- **M5's error message is misattributed.** A duplicate trade_id on the *engine* side is not
  explicitly guarded (the harness's upfront duplicate check is written for `tv_anchor` only,
  `parity_gate.py` L101-103). The second occurrence still fails correctly — its id was already
  popped from `tv_map` by the first occurrence — but the raised message reads "present in engine
  but not tv_anchor," which is confusing since the id *was* in tv_anchor. Detection is intact;
  a future polish pass could add a `seen_ids` check on the engine side for a clearer message.
- **M3 empirically confirms profit factor is exactly scale-invariant** under a uniform
  multiplicative defect (`pf_rel == 0.0000` to displayed precision) — worth remembering before
  ever proposing PF alone as a parity check; net is the only tripwire for pure position-sizing
  defects like the historical Striker DJ30 contractValue bug.

---

## §6 — Audit hooks (runnable)

```bash
# Battery passes (this freeze's own claim).
python -m pytest tests/lab/test_q_filltax_1_parity_mutations.py -v

# The parent brief's own §10 audit hook now finds a real battery (was previously empty).
python -m pytest tests/ -k "parity" -q

# Existing harness unit tests untouched by this freeze.
python -m pytest lab/analysis/c1/parity_gen2_2026-08/test_parity_gate.py -q

# Freeze-before-result: this file predates any family TV-anchor artifact.
git log --oneline --diff-filter=A -- "lab/analysis/c1/parity_gen2_2026-08/*family*" 2>/dev/null | tail -1
# expect empty — no family run has ever landed

# Bands this battery is pinned to (drift here should fail test_battery_bands_still_match_prereg_literals).
rg -n "RANK_RHO_FLOOR|NET_REL_BAND|PF_REL_BAND|MIN_TRADES" lab/analysis/c1/parity_gen2_2026-08/PREREG.md
```

---

## Verification

```bash
python -m pytest tests/lab/test_q_filltax_1_parity_mutations.py lab/analysis/c1/parity_gen2_2026-08/test_parity_gate.py -q
# 2026-08-18: 9 passed (battery) + 11 passed (existing harness unit tests) = 20 passed, 0 failed
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-18 | **Frozen.** Battery authored (8 rows: M1-M8), run against synthetic baseline, 8/8 as designed (9/9 including the band-pin test). Q-FILLTAX-1 Pre-Lock Checklist item "Mutation battery frozen" ticked. Phase 2 (first family TV anchor) and Phase 3 (assert §6 row) remain owed and operator-gated — not advanced by this freeze. | Claude Code (Sonnet 5), operator-directed |
