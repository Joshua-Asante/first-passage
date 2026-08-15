# ADR — Bust-path max_dd includes the breach day (portfolio_mc semantic correction)

**Status:** `Accepted`
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Decision date:** 2026-07-06
**Authors:** Joshua + Claude Code
**Supersedes:** — (corrects an undocumented `_simulate_path` semantic; no prior ADR claimed the exclusion as intended)
**Related:** 2026-07-06 external code audit (Cursor) Issue 3, adversarially verified in-session; companion closure [`docs/ltm/briefs/Q-DDTRIG-1-finding1-daily-loss-denominator-closure.md`](../ltm/briefs/Q-DDTRIG-1-finding1-daily-loss-denominator-closure.md) (Issue 10 / MC-audit Finding #1, closed no-action same session)
**Layer:** portfolio (MC lock-gate metric semantics; no allocation, dd_protection, or Pine constant touched)

---

## §0 — Rule 0 reads (production-source verification)

Read **before** authoring the change and this ADR, in-session:

- `core/portfolio_mc.py` — anchor: `5bd5f31` (verified `git log -1 -- core/portfolio_mc.py` 2026-07-06). `_simulate_path` lines 355-434 read in full pre-edit: bust returns at 402-408 preceded the underwater update at 421-426, so the returned `max_dd` on every bust path was the pre-breach value. `run_seed` 437-484: `max_dds.append(max_dd)` unconditional for all outcomes (line 475); `compute_default_config` pools all paths (`all_dds`) and takes `np.percentile(all_dds, 99)`.
- `tests/test_mc_anchors.py` — anchor: `784a9ab`. Pins `pass_rate 0.9983 / bust_rate 0.0017 / p99_dd 0.0437` at `abs=1e-4`; no test asserted bust-path `max_dd` (the direct-call Rule 0-T test asserts outcome/day/culprit only).
- `docs/mc_anchor_history.md` — current canonical anchor block + prior-anchor lineage (this ADR appends an entry).
- Runtime falsifiers (pre-fix, this session): day-1 single-shot −5.5% path returned `("bust_daily", 1, 0.0, 0)` — `max_dd` literally 0.0; −0.9%/day grind returned `("bust_static", 6, 0.045, 0)` vs true breach-day DD 5.4%.

---

## §1 — Context

The 2026-07-06 external code audit (Cursor) flagged (Issue 3) that `_simulate_path` returns on `bust_daily`/`bust_static`/`bust_trailing` before the underwater update runs, so the breach day's drawdown never enters `max_dd`. Adversarial verification confirmed the mechanism exactly and established the blast radius: `p99_dd` — one of the two lock gates (bust <1%, p99 DD <5%) — pools `max_dd` across **all** sims including busts, so the metric was biased downward, with the bias growing with bust rate — largest in exactly the 2020-23 chop regime the 2026-06-07 decompound-re-MC HOLD decision worries about. The same pooling feeds the DD-trigger sweep and the quarterly regime-check tooling (next firing 2026-08-08). No docstring, test, or ADR documented the exclusion as intended — it reads as an oversight, not a semantic choice. Verification also proved a bound: at the canonical anchor (51 busts across 30K sims) the bias provably cannot flip either gate (51 < the ~300-path p99 window), and every recorded high-bust regime cell already breached gates on bust rate alone — so no historical decision flips; this is a forward-correctness fix.

**Decision driver (one sentence):** the quarterly regime trigger (2026-08-08) and any future futures-venue lock evaluation consume `p99_dd` from this code path, and an anti-conservative bias in a lock-gate risk metric with zero test coverage should not survive contact with a verified defect report.

---

## §2 — Decision

**Decision:** `_simulate_path` records the breach day's drawdown-from-peak into `max_dd` before every bust return. Implementation: the underwater update (`dd_new = (peak - eq_new) / peak`; fold into `max_dd`) is hoisted above the bust checks; the old post-update block is removed. Peak only advances after that point, so the arithmetic is identical for every surviving day — pass/bust/days-to-pass/attribution are byte-identical by construction, and only bust-path `max_dd` values change.

**Effective:** immediately (landed with this ADR's PR, same commit series).
**Scope:** all `_simulate_path` consumers — canonical anchor, DD-trigger sweep, fixed-1R tooling, regime-cell tooling, Bulenox trailing-DD runs.

**Gate-coupling semantic (decided here, explicitly):** with breach-day inclusion, every static-bust path records `max_dd ≥ 5%` mechanically (peak ≥ starting equity), so `bust_rate ≥ 1%` now **implies** `p99_dd ≥ 5%` — the two lock gates are coupled at and above 1% bust. This is accepted as intended: the p99 gate becomes a strictly conservative superset signal, and the two gates remain independently informative in the regime that matters for locks (bust < 1%). The pre-fix "independence" was an artifact of under-recording, not a design property.

### Evidence — anchor re-run (10K × 3 seeds, Pepperstone canonical panel, this session)

| Metric | Pre-fix (HEAD `6fe00d2`) | Post-fix | Δ |
|---|---|---|---|
| pass_rate | 0.9983000000000001 | 0.9983000000000001 | 0 (byte-identical) |
| bust_rate | 0.0017000000000000001 | 0.0017000000000000001 | 0 (byte-identical) |
| p50_dd | 0.01382060767014933 | 0.01382060767014933 | 0 (byte-identical) |
| p95_dd | 0.034477407571447294 | 0.034477407571447294 | 0 (byte-identical) |
| **p99_dd** | 0.04372372844379036 | **0.0437338806967903** | **+1.02e-5** |
| median days-to-pass | 26 | 26 | 0 |

p50/p95 byte-identity is the empirical proof of surviving-path invariance at scale. The +1.02e-5 p99 shift is inside the `tests/test_mc_anchors.py` pin tolerance (`0.0437 ± 1e-4`): **the canonical 99.83/0.17/4.37 anchor stands, no re-pin, no CLAUDE.md anchor-block change.** The tiny shift at this anchor is expected: the panel's 51 busts are grind-style static busts whose pre-breach `max_dd` already sat near or above the p99 threshold; the correction matters materially only in high-bust regimes (decompound 2020-23 cells: ~9-14% of pooled values were understated by up to ~1pp).

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Status quo (exclude breach day) | Undocumented, untested, anti-conservative in a lock-gate metric; grows with bust rate in exactly the regime the 2026-06-07 HOLD worries about; no artifact claims it as intended. |
| Survivor-only `max_dd` pooling (drop bust paths from `all_dds`) | Larger semantic change: discards bust-path DD information entirely, would move the pins materially, and makes p99 blind to the tail it exists to watch. |
| Report both pooled-corrected and survivor-only quantiles | More information, but two governed numbers where one gate exists; deferred — becomes the supersede path if §4's coupling trigger fires. |
| Fix + immediately re-baseline all historical analyses | Retro-editing published RESULTS is forbidden by standing doctrine; historical figures get a one-line caveat in `docs/mc_anchor_history.md` instead. |

---

## §4 — Falsifier (revert trigger)

**Revert trigger:** if a future gate evaluation observes `bust_rate ≥ 1%` while the p99-DD gate is being read as an *independent* second criterion, the coupling makes that reading invalid — the evaluation must treat the bust gate as primary and report a survivor-only p99 as the DD diagnostic. If that situation occurs on **two consecutive quarterly regime checks**, this ADR is superseded by a two-metric reporting standard (pooled + survivor-only quantiles, both pinned).

**Revert action:** supersede with a new ADR adding the survivor-only quantile to `compute_default_config` output and tests; do NOT silently revert breach-day inclusion (that re-introduces the bias).

**Trigger check schedule:** each quarterly regime check (next 2026-08-08, then 2026-11-08), alongside the standing C0-revert and regime-caveat checks.

---

## §5 — Forbidden moves (under this ADR)

- **Widening the `test_mc_anchors.py` tolerance to absorb future semantic drift** — tempting since this fix happened to land inside `1e-4`; any future change that breaches the pin takes the full re-run + ADR path, not a tolerance edit.
- **"Fixing" the `bust_inactivity` return for symmetry** — genuinely tempting for completeness; it is a zero-effect change (an idle day has `pnl == 0`, DD unchanged) that would churn the locked file for nothing. Ruled out.
- **Extending into DD-definition unification across the codebase** (the external audit's architecture recommendation) — refuted in verification: static-from-start (FXIFY rule), peak-to-trough (protection trigger / this metric), and %-of-notional (regime_bootstrap gate convention) are intentionally distinct semantics; unification would be a correctness regression.
- **Retro-editing historical p99 figures** (decompound 5.93%/5.32%/7.58%, Q-SWAP-2 4.55%, prior anchors) — they are mild underestimates under the old semantic; they stay as published, caveated once in `docs/mc_anchor_history.md`.

---

## §6 — Consequences

**Positive:**
- `p99_dd` is no longer biased downward; the bias was worst precisely where the metric is most load-bearing (high-bust regime cells feeding the quarterly trigger and any futures-venue re-MC).
- All `_simulate_path` consumers (DD-trigger sweep, fixed-1R, regime-cell, Bulenox trailing runs) inherit the fix from the single shared code path.
- Zero anchor churn: pins, CLAUDE.md anchor block, and lock margins all stand unchanged at published precision.

**Negative (real cost):**
- Cross-semantic comparability: any future high-bust MC compared against a pre-2026-07-06 published figure carries a semantic component in the delta; comparisons must footnote it (hook in §10).
- Historical published p99 figures are now known mild underestimates — a permanent asterisk on the 2026-06-07 decompound RESULTS numbers (which, note, already breached gates without the correction; the HOLD verdict is unaffected).

**Risks:**
- The 2026-08-08 regime check's H1/decompound-style cells will read slightly worse than their 2026-06 counterparts partly for semantic reasons; mis-reading that as fresh regime deterioration is the main operational risk. Mitigation: §10 hook + the mc_anchor_history entry landed with this ADR.

**Downstream artifacts updated (this PR):**
- `core/portfolio_mc.py` — the hoist (comment cites this ADR).
- `tests/test_mc_bustday_maxdd.py` — 4 new regression tests (bust_daily day-1, bust_static grind, bust_trailing, surviving-path invariance), authored failing-first.
- `docs/mc_anchor_history.md` — 2026-07-06 semantic-correction entry with the Δ table.
- `docs/ltm/briefs/Q-DDTRIG-1-finding1-daily-loss-denominator-closure.md` — companion closure (same audit pass, same file surface).

---

## §7 — Implementation plan

Executed in-session (TDD order):

- **Phase 0** — Rule 0 reads per §0; runtime falsifiers reproduced the defect pre-edit.
- **Phase 1** — `tests/test_mc_bustday_maxdd.py` authored first: 3 failing (breach-day) + 1 passing (invariance guard) confirmed against pre-fix code.
- **Phase 2** — hoist landed in `_simulate_path`; all 4 new tests + Rule 0-T direct-call test + trailing/inactivity boundary suites green (23/23).
- **Phase 3** — anchor re-run (`python core/portfolio_mc.py --panel pepperstone`) + full-precision pre/post probe (§2 table) + `tests/core/test_mc_anchors.py` full suite green (6/6, pins intact).
- **Phase 4** — this ADR + mc_anchor_history entry + Finding #1 companion closure; status `Accepted` on downstream-sweep completion.

---

## §10 — Audit hooks (runnable)

```bash
# The hoist is in place and cites this ADR:
grep -n "bust-day-maxdd-inclusion" core/portfolio_mc.py
# Expected: 1 hit inside _simulate_path, above the bust checks

# Regression tests present and green:
python -m pytest tests/test_mc_bustday_maxdd.py -q
# Expected: 4 passed

# Anchor pins intact (no re-pin happened):
python -m pytest tests/core/test_mc_anchors.py -q
# Expected: 6 passed (skips on clones without vendor data)

# §4 coupling trigger — at each quarterly regime check:
python lab/analysis/time_to_pass.py --regime-check
# If any evaluated cell shows bust_rate >= 0.01 AND its p99_dd is cited as an
# independent gate confirmation, apply §4 (survivor-only p99 as DD diagnostic);
# two consecutive quarterly firings => supersede per §4.

# Cross-semantic comparison guard (any new MC vs pre-2026-07-06 published figures):
grep -n "2026-07-06 semantic correction" docs/mc_anchor_history.md
# Expected: the entry exists; cite it in any such comparison.
```

---

## Verification

```bash
# Production-source verification (Rule 0 confirmation)
git log -1 --format='%h %ci' -- core/portfolio_mc.py     # 5bd5f31 pre-change
python -m pytest tests/test_mc_bustday_maxdd.py tests/core/test_mc_anchors.py -q

# Downstream artifact update verification
grep -n "2026-07-06" docs/mc_anchor_history.md
test -f docs/ltm/briefs/Q-DDTRIG-1-finding1-daily-loss-denominator-closure.md && echo OK
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-06 | Initial authoring + acceptance (implementation, re-run, and downstream sweep completed same session) | Joshua + Claude Code |
