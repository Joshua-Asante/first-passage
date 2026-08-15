# ADR 2026-06-22 — Cost-geometry pre-gate for instrument-ledger Phase-0

**Status:** `Accepted`
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Decision date:** 2026-06-22
**Authors:** Joshua + Claude Code
**Supersedes:** none (additive — extends Rule 10 / ADR 2026-06-11)
**Related:** [`docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md`](2026-06-11-instrument-ledger-and-cfg-fingerprint.md) (the instrument-ledger rule this extends) · [`docs/adr/2026-06-14-reject-usoil-rdm-spike-fader.md`](2026-06-14-reject-usoil-rdm-spike-fader.md) + [`docs/adr/2026-06-14-rejected-candidate-patterns.md`](2026-06-14-rejected-candidate-patterns.md) (the paid-for failure + the venue/cost add-back condition this mechanizes) · [`docs/ltm/briefs/Q-5LEG-DATA-instrument-regime-public-data.md`](../ltm/briefs/Q-5LEG-DATA-instrument-regime-public-data.md) (the search that motivates it)
**Layer:** methodology / infrastructure (R&D session governance) — **does not touch strategy code, allocations, dd_protection, or MC calibration.** Locked config untouched.

---

## §0 — Rule 0 reads (production-source verification)

Read **before** authoring, this session, at worktree HEAD `21c009f` (currency verified `git log HEAD..origin/main` empty for the branch base):

- [`docs/operational_rules.md`](../operational_rules.md) — anchor `5baf01f` (2026-06-11). Rule 10 (instrument-ledger) is the rule this extends; its maintenance clause ("rules earn their place by being paid for"; "edits to existing rules must be logged with a dated entry") binds this change. Rule 10's Phase-0 obligation today is read-at-start / append-at-end only — no pre-flight before the first backtest.
- [`docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md`](2026-06-11-instrument-ledger-and-cfg-fingerprint.md) — anchor `2b171fc` (2026-06-12). §2a ratifies Rule 10; §5 forbids ledger restating locked constants — this pre-gate links out, never restates.
- [`docs/adr/2026-06-14-reject-usoil-rdm-spike-fader.md`](2026-06-14-reject-usoil-rdm-spike-fader.md) + [`lab/archive/usoil_rdm/RESULTS.md`](../../lab/archive/usoil_rdm/RESULTS.md) + [`lab/archive/usoil_rdm/costlaw.py`](../../lab/archive/usoil_rdm/costlaw.py) — anchor `88e11dc` (2026-06-14). The worked failure: realized round-trip cost **0.090R** on a sub-ATR confirmation stop, gross-negative at every target cell; the L-COST-GEOMETRY firing (assumed k·ATR reads comfortable, realized spike-high stop is sub-ATR → ~8× the assumed hurdle).
- [`docs/adr/2026-06-14-rejected-candidate-patterns.md`](2026-06-14-rejected-candidate-patterns.md) — anchor `88e11dc` (2026-06-14). §A names the **venue/cost-constraint** class whose add-back condition is "a geometry that **clears the cost-law pre-flight with margin (from the realized stop, not assumed k·ATR)**." §5 explicitly endorses "adopt the *gates* now (near-free); keep the *lessons* candidate-status." This ADR is that gate, made runnable.
- [`ops/instruments/USDCAD.md`](../../ops/instruments/USDCAD.md) — anchor `5f9231d` (2026-06-15). Durable finding #1 (COST LAW): "cost-in-R ∝ price/stop_dist under risk sizing. Measured **0.097R RT at 1.42×ATR(15m)**; 0.055–0.072R at 2.5×ATR … compute the hurdle pre-flight." The pre-gate operationalizes that last sentence.
- [`lab/archive/ict_cascade_2026-06-18/harness_1m.py`](../../lab/archive/ict_cascade_2026-06-18/harness_1m.py) — anchor `bcf2160` (2026-06-18). The standing `cost_r = (2·comm·entry + 2·slip·tick)/stop_dist` convention + the 4×-median-cost hurdle (`MIN_RMULT = 4.0`); the pre-gate reuses this geometry pre-trade.
- [`docs/ltm/briefs/Q-5LEG-DATA-instrument-regime-public-data.md`](../ltm/briefs/Q-5LEG-DATA-instrument-regime-public-data.md) — anchor `20903db` (2026-06-21). The 5th-leg discovery brief; T1 surfaces tight-RANGE mean-reversion crosses (EURGBP/EURCHF-class) whose edge-style fits chop but whose cost geometry is the live risk.
- [`core/bar_export_loader.py`](../../core/bar_export_loader.py) — anchor `5cba8af` (2026-06-17) — canonical M15 OHLC schema (`time,open,high,low,close,volume`) + BAR EXPORT v0.1 `Signal` format the gate parses; [`docs/adr/2026-06-12-tv-csv-canonical-feed-policy.md`](2026-06-12-tv-csv-canonical-feed-policy.md) — anchor `6f2f468` — TV-export/Pepperstone series is canonical (other symbols staging-only); the gate's ATR15m must be feed-sourced from it.

---

## §1 — Context

The 5th-leg search ([`Q-5LEG-DATA`](../ltm/briefs/Q-5LEG-DATA-instrument-regime-public-data.md), T1) repeatedly surfaces tight-RANGE mean-reversion candidates — range FX crosses like EURGBP/EURCHF — whose *edge-style* is correct for the 2020-2023 chop regime the portfolio needs relief in, but whose **cost geometry is the live risk**: a small 15m ATR relative to the spread can swamp the mean-reversion edge before any directional signal is tested. This is the **same failure mode that killed the USOIL spike-fader** (`CONCEPT-USOIL-RDM-001`): a ~0.09R round-trip cost hurdle, a sub-ATR stop on a wide-spread instrument, gross-negative at every target cell on the canonical feed.

L-COST-GEOMETRY is already named methodology — it is the add-back condition for the `venue/cost-constraint` rejection class (ADR 2026-06-14-rejected-candidate-patterns §A) — but it has been a **post-hoc finding**: discovered by running a probe (and, when the instrument is ledgered, spending an anti-SNAG slot) and *then* computing the realized cost. For a candidate stream that generates range-cross mean-reverters at the current rate, rediscovering the same cost wall per candidate is wasteful. The USDCAD ledger's own durable finding #1 already prescribes the remedy in words — "compute the hurdle pre-flight" — but there was no runnable pre-flight bound to the Phase-0 step.

**Decision driver (one sentence):** make the cheapest correct kill (cost geometry from the realized stop) a mechanical pre-flight that runs *before* the first backtest, so a cost-infeasible mechanism is caught by `median(spread)/median(ATR15m)` arithmetic, not by a spent probe.

---

## §2 — Decision

Add a runnable **cost-geometry pre-gate** to the instrument-ledger **Phase-0** validation step (operational rule 10). It is **additive** — Rule 10's read-at-start / append-at-end obligation is unchanged; this inserts one pre-flight before the first backtest of a new candidate mechanism.

**§2a — The gate.** Before any backtest on a *new candidate entry mechanism* on an instrument, compute from the **canonical TV/Pepperstone 15m series**:

```
cost_ratio@1xATR = median(spread) / median(ATR15m)
cost_R           = round_trip_cost_price / realized_stop_distance
```

with `realized_stop_distance = stop_atr · median(ATR15m)` (or an explicit realized stop in price units for confirmation/structural-stop designs), and `round_trip_cost_price = spread + 2·slippage + 2·commission`. **PASS iff `cost_R < 0.05R`** (the default ceiling). The 0.05R ceiling is the round-trip cost a PF~2.0 after-cost leg absorbs with margin and is consistent with the standing 4×-median-cost hurdle (0.05R cost ⇒ a 0.20R post-cost hurdle, comfortable against a ≥0.2R gross edge). The ceiling is a config arg (`--ceiling`), set once per investigation — not re-tuned per candidate.

**§2b — The realized-stop rule (load-bearing).** The stop fed to the gate **must be the stop the strategy actually uses, computed from its realized geometry** — not an assumed comfortable k·ATR. This is the exact USOIL trap: an assumed 2.5×ATR stop reads "comfortable" while the realized spike-high confirmation stop is sub-ATR, ~8× the assumed cost. The gate echoes the implied stop-in-ATR and flags any sub-ATR stop.

**§2c — Disposition.** The Phase-0 ledger disposition for a new-mechanism session records `cost_R`, the ceiling, and the verdict. A **FAIL** means the mechanism *as specified* is cost-infeasible and does not proceed to backtest without a stop-geometry change (wider stop, higher execution TF) or a lower-cost venue — mirroring the §A venue/cost add-back. A **PASS is necessary-not-sufficient**: the pre-registered backtest still runs.

**Effective:** immediately, all surfaces (CC, claude.ai, cursor). **Implementation:** [`scripts/cost_geometry_pregate.py`](../../scripts/cost_geometry_pregate.py) (stdlib-only, runnable on a public clone) + [`tests/test_cost_geometry_pregate.py`](../../tests/test_cost_geometry_pregate.py) (pins the USOIL/USDCAD anchors); Rule 10 amended with a dated maintenance-log entry pointing here.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Status quo — keep L-COST-GEOMETRY a post-hoc finding | Costs a probe (and, on ledgered instruments, an anti-SNAG slot) per rediscovery. The 5th-leg search generates range-cross mean-reverters at a rate that makes per-candidate rediscovery the dominant waste. USDCAD finding #1 already asked for a pre-flight in words. |
| Fold into the concept-intake gate (`lab/validation/concept_intake`) | Intake is **mechanism** dedup/admissibility and runs *before* an instrument + feed are chosen; cost geometry is **instrument + feed specific** and belongs at Phase-0 (after the ledger read, before the backtest). Wrong stage, wrong inputs. |
| A hard CI gate | CI cannot hash gitignored vendor feeds (the M-9 class — same reason `check_data_manifests` can't re-hash on runners). The gate runs locally at Phase-0, like the data-manifest pre-commit hook. |
| Reuse `harness_1m.median_hurdle` directly | That is a **post-hoc**, trade-population metric (needs realized trades). The pre-gate is **pre-trade** geometry computed from the bar feed + the design's stop alone — zero backtest days spent. It deliberately reuses the same `cost_r` arithmetic so the two reads agree. |
| Select on the headline `spread/ATR` ratio only | The ratio is at a 1×ATR stop; the binding number is `cost_R` at the **realized** stop. Reporting only the ratio would hide the sub-ATR trap (the whole USOIL lesson). |

---

## §4 — Falsifiable hypothesis (revert trigger)

**Hypothesis (H, falsifiable):** a mechanical Phase-0 cost-geometry pre-gate prevents the rediscover-by-backtest of cost-infeasible candidates at sustainable cost — concretely, it catches the USOIL/USDCAD-class kill from `median(spread)/median(ATR15m)` + the realized stop, *before* a probe is spent, without producing false kills of genuinely cost-feasible mechanisms.

**Verdict mapping (evaluated 2026-08-08 programme audit, co-scheduled):**
- **RESOLVED** (load-bearing, gate stands) iff: every post-2026-06-22 `venue/cost-constraint` rejection whose inputs (spread / ATR15m / realized stop) were knowable pre-backtest was caught at Phase-0 with no probe spent, **and** no gate **PASS** was later rejected on realized round-trip cost the gate's inputs already covered.
- **FALSIFIED** iff either limb fails: (a) a candidate the gate **PASSED** is later killed on realized round-trip cost the gate's inputs should have surfaced (ceiling/spread-sourcing miscalibrated), **or** (b) the gate **FAILED** a candidate that a faithful realized-geometry backtest then showed cost-feasible (a false kill). → **Revert action:** recalibrate the ceiling / spread-sourcing, or downgrade the gate to advisory; do not silently keep a miscalibrated gate. Supersede with a fresh ADR.
- **AMBIGUOUS** iff <1 new cost-sensitive candidate reached Phase-0 by 2026-08-08 → carry the evaluation to 2026-11-08 unchanged (insufficient exposure).

**Trigger check schedule:** quarterly programme-audit slate, **2026-08-08** (first look) and **2026-11-08**, alongside the standing regime + instrument-ledger triggers.

---

## §5 — Forbidden moves (under this ADR)

- **Running the gate on the *assumed* k·ATR stop when the design's realized stop is sub-ATR.** The exact USOIL trap. The realized stop (`--realized-stop`) governs for confirmation/structural-stop designs; the gate flags sub-ATR stops precisely so this move is visible.
- **Sourcing ATR15m from a non-canonical feed** (the `FX_USOIL`/`TVC:USOIL` corruption class). Canonical TV-export / Pepperstone series only (2026-06-12 policy). A new execution feed clears the feed-equivalence pre-flight first.
- **Treating a PASS as edge validation.** The pre-gate is necessary-not-sufficient; it spends zero forward days and makes zero edge claim. The pre-registered, placebo-controlled backtest still runs.
- **Loosening `--ceiling` per candidate to manufacture a PASS.** The design-layer analogue of "widen the stop post-hoc to cut cost" (ADR 2026-06-14-reject-usoil-rdm §5c). The ceiling is set once per investigation; a candidate clears it or changes its geometry/venue.
- **Citing one feed's spread/ATR as a proxy for another's** (the feed-equivalence + XAGUSD instrument-vs-strategy-correlation belt). Geometry is feed-specific.

---

## §6 — Gate (binary)

**Verdict: ACCEPTED — additive Phase-0 pre-gate adopted.** The §4 hypothesis is open and re-tested 2026-08-08: **RESOLVED** if it catches cost-infeasible candidates pre-backtest with no false kills, **FALSIFIED** if a PASS is later cost-killed on covered inputs or a FAIL is shown to be a false kill, **AMBIGUOUS** if exposure is insufficient by then. Adoption gates met: script runnable + tested (USOIL 0.090R and USDCAD 0.097R/0.055R anchors reproduce), Rule 10 amended with a dated log entry, no locked config touched (`check_boundaries` OK).

---

## §7 — Implementation plan (executed)

- **Phase 0** ✅ — §0 anchors verified current at `21c009f`.
- **Phase 1** ✅ — [`scripts/cost_geometry_pregate.py`](../../scripts/cost_geometry_pregate.py) authored (stdlib-only; canonical-M15 + BAR-EXPORT-v0.1 parsing; Wilder ATR; realized-stop rule + sub-ATR flag; PASS/FAIL exit codes; `--json`).
- **Phase 2** ✅ — [`tests/test_cost_geometry_pregate.py`](../../tests/test_cost_geometry_pregate.py) pins the geometry primitives, the band thresholds (≡ `costlaw.py`), and the **USOIL (0.090R, sub-ATR FAIL)** + **USDCAD (0.097R @1.42×ATR, 0.055R @2.5×ATR, both FAIL @0.05)** anchors + the EURGBP-class flag + a passing case. 11/11 green.
- **Phase 3** ✅ — [`docs/operational_rules.md`](../operational_rules.md) Rule 10 amended (Phase-0 cost-geometry pre-gate sub-step + maintenance-log entry pointing here).
- **Phase 4** ✅ — verification block run; status `Accepted`.

Not implemented (deliberately): no CI gate (§3 — vendor-feed hashing class); no ledger-file edits (Rule 10 link suffices; ledgers stay append-only); no change to any locked constant.

---

## §10 — Audit hooks (runnable)

```bash
# 1. Rule 10 carries the Phase-0 cost-geometry pre-gate provision + the dated log entry
grep -n "cost-geometry pre-gate\|cost_geometry_pregate" docs/operational_rules.md

# 2. The gate is runnable and reproduces the documented anchors (11/11)
python tests/test_cost_geometry_pregate.py        # stdlib runner; or: pytest tests/test_cost_geometry_pregate.py

# 3. CLI smoke: a sub-ATR confirmation stop FAILs and flags the USOIL trap (exit 1)
python scripts/cost_geometry_pregate.py --help | head -1

# 4. No locked config touched by this change
python scripts/check_boundaries.py                # expect: OK
git diff --name-only HEAD~1 | grep -E "dd_protection|firm_rules|portfolio_mc|\.pine$" || echo "no locked-config files touched"

# 5. The cost_r arithmetic agrees with the standing harness convention
grep -n "def cost_r" lab/archive/ict_cascade_2026-06-18/harness_1m.py scripts/cost_geometry_pregate.py
```

---

## Verification

```bash
# Discipline checks (mechanical)
python scripts/check_brief.py docs/adr/2026-06-22-cost-geometry-pregate.md --type adr
# Expected: all checks PASS

# Production-source verification (Rule-0 anchors)
git log -1 -- docs/operational_rules.md docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md

# The gate reproduces the USOIL/USDCAD anchors and Rule 10 references it
python tests/test_cost_geometry_pregate.py
grep -q "cost_geometry_pregate" docs/operational_rules.md && echo "Rule 10 wired"
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-06-22 | Initial authoring — runnable cost-geometry pre-gate added to instrument-ledger Phase-0 (Rule 10); script + test + Rule 10 amendment; additive, no locked config touched | Joshua + Claude Code |
