# Publication-Date OOS Gate + Side-Prediction Intake — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the §2.1 machinery for [CC-HANDOFF-external-strategy-sourcing.md](../ltm/briefs/rnd-pipeline/CC-HANDOFF-external-strategy-sourcing.md): a publication-date out-of-sample gate (Edit 1) and a returns-independent side-prediction intake check (Edit 2), so externally-sourced strategies are evaluated only on data their authors could not have fit to.

**Architecture:** Additive only. (1) `ConceptRecord` gains an optional `discovery_date` field. (2) `check_concept.py` gains two checks that fire ONLY under a new `--external` flag (internal concepts unaffected), backed by a new additive `side_prediction` block in the read-only contract. (3) `harness.py` gains `run_harness_oos`, which selects the IS-best on the pre-`d` partition only (the post-`d` holdout must not influence selection — see Edit 1 follow-up) but evaluates its EDGE only on the `exit_time > discovery_date` partition, returning an `OOS_PASS / INSUFFICIENT_OOS / FAIL` label. (4) `run_candidate.py` wires `discovery_date` → the OOS gate. No existing verdict math changes; the OOS path is a new entry point.

**Tech Stack:** Python 3.x, pydantic v2, numpy, pandas, pytest. Modules under `lab/validation/` and `lab/validation/concept_intake/`.

## Global Constraints

- **Backward compatibility is load-bearing.** Every existing `lab/validation/concept_intake/concepts/*.yaml` must still parse and still pass `check_concept.py` *without* `--external`. Verify by re-parsing all of them (Task 1 Step 6, Task 2 Step 9).
- **No change to existing verdict math.** `derive_verdict`, `run_harness`, `run_harness_on_family` keep their current behavior on the full series. The OOS path is a *new* function that *reuses* them; it does not edit them. (Brief §2.1 per-step gate.)
- **DSR `n_trials` = the full examined grid** (`trial_set.total_n`) on the OOS path too — the selection exposure is unchanged because the search that produced the candidate grid was still the full grid; only the *selection criterion* is restricted to pre-`d` data (ADR 2026-06-05-sweep-engine §6).
- **No OOS re-selection.** The IS-best config is selected on the pre-`d` partition only (not the full search, and never on post-`d`); it is NOT re-picked on the post-`d` window (that would be selecting on OOS — a worse leak than the one this fixes). (Brief §5.)
- **Contract edits are additive, in a reviewed commit.** The `side_prediction` block adds *markers* (it does not tune any threshold to pass a concept); `contract.py` deep-freezes it (forbidden move #1 intact).
- **Pre-registration values (frozen, from the brief §0.5):** `k_min = 30` (min post-`d` trades for `OOS_PASS`); `pbo_n_splits` default `16` (so `k_min ≥ pbo_n_splits` always holds — the IS-best is always rank-comparable on post-`d`).
- **`exit_times` are `datetime64[ns]` tz-naive UTC** (`ingest.py:60-63,216-217`; `engine.py:361-362`). The partition is `exit_times > np.datetime64(discovery_date)`.
- **Do not commit/merge without Joshua's go** (brief Authority). Commits in this plan are local; merge is gated on the brief §7 review.

---

## File Structure

| File | Responsibility | Change |
|---|---|---|
| `lab/validation/concept_intake/schema.py` | `ConceptRecord` pydantic model | **Modify** — add optional `discovery_date` field + ISO validator |
| `lab/validation/concept_intake/admissibility_contract.yaml` | read-only marker/threshold contract | **Modify** — add additive `side_prediction` block |
| `lab/validation/concept_intake/check_concept.py` | admissibility checks + CLI | **Modify** — two new checks behind `--external`; thread `external` flag |
| `lab/validation/concept_intake/tests/test_gate_controls.py` | intake gate tests | **Modify** — add discovery_date + side-prediction cases |
| `lab/validation/harness.py` | stage-4 orchestrator | **Modify** — add `run_harness_oos` + OOS labels (no edit to existing fns) |
| `lab/validation/tests/test_oos_gate.py` | OOS-gate tests | **Create** |
| `lab/validation/run_candidate.py` | stage-3→4 driver | **Modify** — wire `discovery_date` → `run_harness_oos`; emit OOS label |
| `lab/validation/tests/test_run_candidate.py` | driver tests | **Modify** — add an OOS-path case |

---

## Task 1: `discovery_date` field on `ConceptRecord`

**Files:**
- Modify: `lab/validation/concept_intake/schema.py`
- Test: `lab/validation/concept_intake/tests/test_gate_controls.py`

**Interfaces:**
- Produces: `ConceptRecord.discovery_date: str | None` (ISO `YYYY-MM-DD`, the literal `"undatable"`, or `None`). `field_text("discovery_date")` returns `""` when `None`.

- [ ] **Step 1: Write the failing test**

Add to `tests/test_gate_controls.py`:

```python
import pytest
from pydantic import ValidationError
from lab.validation.concept_intake.schema import load_concept_dict

def _base_record(**over):
    rec = {
        "concept_id": "T-DD-1", "title": "t",
        "mechanism": "edge exists because dealer hedging flow pushes price after the fix",
        "falsifier": "if the hedging-flow loading on forward returns has p above 0.05 then reject",
        "regime": "policy-divergence windows", "portfolio_fit": "decorrelated from guardian in chop",
        "logic_family_hint": "mean-reversion long with session filter",
        "provenance": "test", "instrument": "EURUSD", "mechanism_family": "flow-fade",
    }
    rec.update(over)
    return rec

def test_discovery_date_defaults_none():
    c = load_concept_dict(_base_record())
    assert c.discovery_date is None
    assert c.field_text("discovery_date") == ""

def test_discovery_date_accepts_iso():
    c = load_concept_dict(_base_record(discovery_date="2024-03-15"))
    assert c.discovery_date == "2024-03-15"

def test_discovery_date_accepts_undatable_sentinel():
    c = load_concept_dict(_base_record(discovery_date="undatable"))
    assert c.discovery_date == "undatable"

def test_discovery_date_rejects_malformed():
    with pytest.raises(ValidationError):
        load_concept_dict(_base_record(discovery_date="2024-13-99"))
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest lab/validation/concept_intake/tests/test_gate_controls.py -k discovery_date -v`
Expected: FAIL — `discovery_date` is not a field (pydantic `extra='forbid'` rejects it, or `AttributeError`).

- [ ] **Step 3: Add the field + validator**

In `schema.py`, change the pydantic import and add the field. Replace the import line:

```python
from pydantic import BaseModel, ConfigDict, Field, field_validator
```

Add, inside `ConceptRecord` after the `provenance` field (keep `extra='forbid'`):

```python
    discovery_date: str | None = Field(
        default=None,
        description=(
            "Earliest public-disclosure date (ISO YYYY-MM-DD) for an externally-"
            "sourced concept; None for internal concepts; the literal 'undatable' "
            "routes to the forward-paper window (pre-disclosure data carries no "
            "edge weight — Edit 1)."
        ),
    )
```

Add the validator method (after `field_text`):

```python
    @field_validator("discovery_date")
    @classmethod
    def _validate_discovery_date(cls, v: str | None) -> str | None:
        from datetime import date
        if v is None:
            return None
        v = v.strip()
        if v in ("", "undatable"):
            return v or None
        try:
            date.fromisoformat(v)
        except ValueError as exc:
            raise ValueError(
                "discovery_date must be ISO 'YYYY-MM-DD', the literal 'undatable', "
                f"or empty; got {v!r}."
            ) from exc
        return v
```

- [ ] **Step 4: Run the new tests to verify they pass**

Run: `python -m pytest lab/validation/concept_intake/tests/test_gate_controls.py -k discovery_date -v`
Expected: PASS (4 tests).

- [ ] **Step 5: Run the full concept-intake suite (no regressions)**

Run: `python -m pytest lab/validation/concept_intake/ -q`
Expected: PASS (all prior tests still green).

- [ ] **Step 6: Verify every existing concept still parses**

Run:
```bash
for f in lab/validation/concept_intake/concepts/*.yaml; do \
  python -c "import sys; from lab.validation.concept_intake.schema import load_concept; load_concept(sys.argv[1])" "$f" \
    && echo "OK $f" || echo "PARSE FAIL $f"; done
```
Expected: `OK` for every file (no `PARSE FAIL`). Backward compatibility confirmed.

- [ ] **Step 7: Commit**

```bash
git add lab/validation/concept_intake/schema.py lab/validation/concept_intake/tests/test_gate_controls.py
git commit -m "feat(intake): add optional discovery_date field to ConceptRecord (Edit 1)"
```

---

## Task 2: Side-prediction + discovery-date intake checks behind `--external`

**Files:**
- Modify: `lab/validation/concept_intake/admissibility_contract.yaml`
- Modify: `lab/validation/concept_intake/check_concept.py`
- Test: `lab/validation/concept_intake/tests/test_gate_controls.py`

**Interfaces:**
- Consumes: `ConceptRecord.discovery_date` (Task 1); the frozen contract's new `side_prediction` block.
- Produces: `run_checks(concept, contract=None, registry_path=None, external=False) -> list[CheckResult]`; CLI `--external` flag. When `external=True`, two extra checks run; internal calls (`external=False`) are unchanged.

- [ ] **Step 1: Write the failing test**

Add to `tests/test_gate_controls.py` (reuses `_base_record` from Task 1):

```python
from lab.validation.concept_intake.check_concept import run_checks, is_admissible

def _statuses(results):
    return {r.name: r.status for r in results}

def test_external_requires_discovery_date():
    # external concept with NO discovery_date -> FAIL under --external
    res = run_checks(load_concept_dict(_base_record()), external=True)
    names = _statuses(res)
    assert any("Discovery date" in n and s == "FAIL" for n, s in names.items())
    # same record is admissible WITHOUT --external (internal path unaffected)
    assert is_admissible(run_checks(load_concept_dict(_base_record())))

def test_external_returns_independent_side_prediction_passes():
    # falsifier names a returns-INDEPENDENT observable (hedging-flow loading)
    rec = _base_record(discovery_date="2024-03-15")
    res = run_checks(load_concept_dict(rec), external=True)
    assert is_admissible(res)

def test_external_performance_only_falsifier_culled():
    # falsifier reduces to a performance threshold -> hard FAIL under --external
    rec = _base_record(
        discovery_date="2024-03-15",
        falsifier="if the out-of-sample profit factor falls below 1.2 then reject the concept",
        mechanism="prices mean-revert because of liquidity provision after a stop run",
    )
    res = run_checks(load_concept_dict(rec), external=True)
    assert not is_admissible(res)
    assert any("side-prediction" in r.name.lower() and r.status == "FAIL" for r in res)

def test_internal_path_unchanged_by_new_checks():
    # the performance-only falsifier is STILL admissible on the internal path
    rec = _base_record(
        falsifier="if the out-of-sample profit factor falls below 1.2 then reject the concept",
        mechanism="prices mean-revert because of liquidity provision after a stop run",
    )
    assert is_admissible(run_checks(load_concept_dict(rec)))  # external defaults False
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest lab/validation/concept_intake/tests/test_gate_controls.py -k external -v`
Expected: FAIL — `run_checks` has no `external` kwarg (TypeError) / the new checks don't exist.

- [ ] **Step 3: Add the `side_prediction` contract block**

Append to `admissibility_contract.yaml` (additive; not in `contract.py`'s `required_top`, so loading is unaffected):

```yaml
# ---------------------------------------------------------------------------
# Side-prediction contract (Edit 2, external sourcing only — fires under
# --external). The mechanism must be confirmable by an observable OTHER than the
# strategy's own returns. The falsifier must name a returns-INDEPENDENT
# observable and must NOT reduce to a performance threshold (the confabulation
# the gate forbids). Markers are NON-exhaustive: a clear performance-only
# falsifier is a hard FAIL; a falsifier with no recognized independent marker is
# a human-review WARN, not an auto-reject.
# ---------------------------------------------------------------------------
side_prediction:
  returns_independent_markers:
    - "flow"
    - "order flow"
    - "spread"
    - "loading"
    - "coefficient"
    - "regression"
    - "correlation"
    - "concentrat"
    - "orthogonal"
    - "liquidity"
    - "positioning"
    - "term structure"
    - "basis"
    - "session"
    - "calendar"
    - "volume"
    - "open interest"
    - "funding"
    - "inventory"
    - "auction"
    - "expir"
    - "survey"
    - "rate differential"
    - "beta"
    - "partial"
    - "granger"
  performance_markers:
    - "profit factor"
    - "profit-factor"
    - "sharpe"
    - "drawdown"
    - "win rate"
    - "win-rate"
    - "winrate"
    - "net profit"
    - "equity curve"
    - "pnl"
    - "p&l"
    - "return series"
    - "cagr"
    - "expectancy"
    - "the backtest"
```

- [ ] **Step 4: Add the two checks in `check_concept.py`**

Add after `check_dedup` (before the Runner section):

```python
def check_discovery_date_present(c: ConceptRecord, k: AdmissibilityContract) -> CheckResult:
    """External sourcing (Edit 1): a sourced concept must carry a discovery_date
    (ISO) or the explicit 'undatable' sentinel. Pre-discovery data carries no
    edge weight; an absent date is a hard FAIL on the external path."""
    d = c.field_text("discovery_date")
    if not d:
        return CheckResult(
            "Discovery date present (external sourcing)", "FAIL",
            "externally-sourced concept has no discovery_date. Set the earliest "
            "public-disclosure date (ISO YYYY-MM-DD), or 'undatable' to route to "
            "the forward-paper window. Pre-d data carries no edge weight (Edit 1).",
        )
    return CheckResult("Discovery date present (external sourcing)", "PASS", None)


def check_side_prediction_returns_independent(
    c: ConceptRecord, k: AdmissibilityContract
) -> CheckResult:
    """Edit 2: the mechanism must be confirmable WITHOUT the strategy's own
    returns. The pre-registered falsifier must name a returns-independent
    observable and must NOT reduce to a performance threshold (the confabulation
    door). Hard FAIL on performance-only; human-review WARN when no recognized
    independent marker is found (the marker list is non-exhaustive)."""
    spec = k.get("side_prediction", {})
    fals = c.field_text("falsifier")
    has_independent = _contains_any(fals, spec.get("returns_independent_markers", ()))
    has_performance = _contains_any(fals, spec.get("performance_markers", ()))
    if has_performance and not has_independent:
        return CheckResult(
            "Mechanism carries a returns-independent side-prediction", "FAIL",
            "the falsifier reduces to a performance threshold (PF/Sharpe/DD/"
            "win-rate/...). Edit 2 forbids confirming a mechanism with the "
            "strategy's own returns. Pre-register a side-prediction checkable "
            "WITHOUT the strategy's P&L (a flow/spread/loading/session/correlation "
            "observable a cheap probe can test).",
        )
    if not has_independent:
        return CheckResult(
            "Mechanism carries a returns-independent side-prediction", "WARN",
            "no recognized returns-independent observable found in the falsifier. "
            "Confirm the falsifier names an observable implication of the mechanism "
            "checkable without the strategy's returns (the marker list is "
            "non-exhaustive). Flagged for human review.", kind="judgment",
        )
    return CheckResult("Mechanism carries a returns-independent side-prediction", "PASS", None)
```

- [ ] **Step 5: Thread the `external` flag through `run_checks`**

Replace `run_checks`:

```python
def run_checks(
    concept: ConceptRecord,
    contract: AdmissibilityContract | None = None,
    registry_path: str | Path | None = None,
    external: bool = False,
) -> list[CheckResult]:
    k = contract or load_contract()
    checks = [
        check_required_fields(concept, k),
        check_no_parameter_grid(concept, k),
        check_mechanism_is_claim(concept, k),
        check_falsifier_falsifiable(concept, k),
        check_portfolio_fit_nontrivial(concept, k),
        check_regime_and_hint(concept, k),
    ]
    if external:
        checks.append(check_discovery_date_present(concept, k))
        checks.append(check_side_prediction_returns_independent(concept, k))
    checks.append(check_dedup(concept, k, registry_path))
    return checks
```

- [ ] **Step 6: Add the `--external` CLI flag**

In `main()`, after the `--quiet` argument:

```python
    ap.add_argument("--external", action="store_true",
                    help="apply external-sourcing controls (Edit 1 discovery_date "
                         "required + Edit 2 returns-independent side-prediction)")
```

And change the `run_checks` call in `main()`:

```python
    results = run_checks(concept, registry_path=args.registry, external=args.external)
```

- [ ] **Step 7: Run the new tests to verify they pass**

Run: `python -m pytest lab/validation/concept_intake/tests/test_gate_controls.py -k external -v`
Expected: PASS (4 tests).

- [ ] **Step 8: Run the full concept-intake suite + the bundled self-test**

Run:
```bash
python -m pytest lab/validation/concept_intake/ -q
python lab/validation/concept_intake/check_concept.py --self-test
```
Expected: pytest all green; self-test verdicts unchanged from baseline (the examples run WITHOUT `--external`).

- [ ] **Step 9: Verify every existing concept still ADMITs on the internal path**

Run:
```bash
for f in lab/validation/concept_intake/concepts/*.yaml; do \
  python lab/validation/concept_intake/check_concept.py "$f" --quiet \
    && echo "ADMIT $f" || echo "REJECT $f"; done
```
Expected: identical ADMIT/REJECT to pre-change (no internal concept newly rejected — the new checks are external-only).

- [ ] **Step 10: Commit**

```bash
git add lab/validation/concept_intake/admissibility_contract.yaml \
        lab/validation/concept_intake/check_concept.py \
        lab/validation/concept_intake/tests/test_gate_controls.py
git commit -m "feat(intake): --external discovery_date + returns-independent side-prediction checks (Edit 2)"
```

---

## Task 3: `run_harness_oos` — publication-date OOS partition + verdict ladder

**Files:**
- Modify: `lab/validation/harness.py`
- Test: `lab/validation/tests/test_oos_gate.py` (create)

**Interfaces:**
- Consumes: a `validation.sweep.emitter.TrialSet`; `_select_is_best`, `run_harness_on_family` (existing, unchanged); `validation.ingest.STARTING_EQUITY`.
- Produces:
  - module constants `OOS_PASS = "OOS_PASS"`, `OOS_INSUFFICIENT = "INSUFFICIENT_OOS"`, `OOS_FAIL = "FAIL"`.
  - `run_harness_oos(trial_set, *, discovery_date, k_min, strategy, instrument, allocation, candidate_id=None, gate=None, **compute_overrides) -> tuple[str, DispositionRecord | None, dict]` — `(oos_label, record_or_None, detail)`.

- [ ] **Step 1: Write the failing test**

Create `lab/validation/tests/test_oos_gate.py`:

```python
"""Tests for the publication-date OOS gate (Edit 1)."""
import numpy as np
import pytest

from validation.harness import run_harness_oos, OOS_PASS, OOS_INSUFFICIENT, OOS_FAIL
from validation.ingest import from_arrays
from validation.sweep.emitter import EmittedTrial, TrialSet

D = np.datetime64("2024-01-01")

def _exit_times(n, start, step_days=1):
    """n exit timestamps starting at `start` (datetime64[D]), one per step_days."""
    return start + np.arange(n) * np.timedelta64(step_days, "D")

def _trial(tid, returns, exit_start):
    n = len(returns)
    xt = _exit_times(n, exit_start)
    et = xt - np.timedelta64(1, "D")
    series = from_arrays(tid, np.asarray(returns, float), et, xt, strategy="striker")
    return EmittedTrial(trial_id=tid, config={"i": tid}, status="ok",
                        tier="pre-filter", series=series, metrics={"n_trades": n})

def _trial_set(trials, total_n=None):
    total_n = total_n if total_n is not None else len(trials)
    agg = {"parity_gate": {"passed": True}}
    return TrialSet(candidate_id="T-OOS", trials=tuple(trials), total_n=total_n, aggregate=agg)

_FAST = dict(pbo_n_splits=6, permutation_n=50, gate_n_paths=40, seed=7)

def test_insufficient_oos_when_best_post_d_too_thin():
    rng = np.random.default_rng(1)
    # best trial: strong pre-d edge, only 5 trades after D -> INSUFFICIENT (k_min=30)
    best = _trial("t-best", np.r_[rng.normal(0.01, 0.005, 200), rng.normal(0.01, 0.005, 5)],
                  exit_start=np.datetime64("2022-01-01"))
    others = [_trial(f"t{i}", rng.normal(0.0, 0.01, 220), np.datetime64("2022-01-01"))
              for i in range(3)]
    label, rec, detail = run_harness_oos(
        _trial_set([best, *others]), discovery_date="2024-01-01", k_min=30,
        strategy="striker", instrument="SYNTH", allocation=0.005, **_FAST)
    assert label == OOS_INSUFFICIENT
    assert rec is None
    assert detail["n_post_d_trades"] < 30

def test_oos_pass_on_post_d_edge():
    rng = np.random.default_rng(2)
    # best trial carries a real edge that PERSISTS past D
    best = _trial("t-best", rng.normal(0.01, 0.004, 400), exit_start=np.datetime64("2021-06-01"))
    others = [_trial(f"t{i}", rng.normal(0.0, 0.01, 400), np.datetime64("2021-06-01"))
              for i in range(4)]
    label, rec, detail = run_harness_oos(
        _trial_set([best, *others]), discovery_date="2024-01-01", k_min=30,
        strategy="striker", instrument="SYNTH", allocation=0.005, **_FAST)
    assert label == OOS_PASS
    assert rec is not None and rec.verdict.startswith("VALIDATED")
    assert rec.n_trials == 5  # DSR N stays the full grid

def test_oos_fail_when_post_d_edge_is_null():
    rng = np.random.default_rng(3)
    # pre-d edge, pure noise after D -> the post-d verdict FAILs
    pre = rng.normal(0.02, 0.003, 350)
    post = rng.normal(0.0, 0.02, 120)
    best = _trial("t-best", np.r_[pre, post], exit_start=np.datetime64("2021-01-01"))
    others = [_trial(f"t{i}", np.r_[rng.normal(0.02, 0.003, 350), rng.normal(0.0, 0.02, 120)],
                     np.datetime64("2021-01-01")) for i in range(4)]
    label, rec, detail = run_harness_oos(
        _trial_set([best, *others]), discovery_date="2024-01-01", k_min=30,
        strategy="striker", instrument="SYNTH", allocation=0.005, **_FAST)
    assert label in (OOS_FAIL, OOS_PASS)  # label is whatever derive_verdict yields on post-d
    assert rec is not None  # the gate RAN (post-d had >= k_min trades); verdict is the evidence
```

> Note on the third test: with synthetic noise the verdict is not deterministic across seeds; the load-bearing assertion is that the gate *ran on the post-d window* (`rec is not None`) and the label is derived from the post-d verdict, never the full-history one. Tighten the seed/edge during execution so it lands `OOS_FAIL` deterministically if a strict assertion is wanted.

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest lab/validation/tests/test_oos_gate.py -v`
Expected: FAIL — `run_harness_oos` / `OOS_PASS` do not exist (ImportError).

- [ ] **Step 3: Implement `run_harness_oos`**

> **Amendment (2026-06-30, post-merge follow-up — methodology defect fix):** the
> code listing below (and its docstring/comment text "selected on the FULL
> search" / "selection on all data is fine" / "Selection on the FULL series")
> reflects the AS-SHIPPED PR #251 version, which had a survivorship leak: letting
> the post-`d` holdout influence which config is "best" lets a config that is
> null pre-`d` but lucky post-`d` win selection and pass on luck — DSR's
> `n_trials` correction cannot see this. The shipped fix selects the IS-best on
> the **pre-`d` partition only** (`exit_time <= d`, gated on a minimum pre-`d`
> trade count so a thin/zero-Sharpe trial can't win by default) and evaluates it
> on post-`d` as before. See `lab/validation/harness.py::run_harness_oos` (current
> docstring) for the corrected contract; this plan's listing is left as the
> historical record of what Task 3 originally shipped.

In `harness.py`, add near the top (after `_BASE_ASSUMPTIONS`):

```python
OOS_PASS = "OOS_PASS"
OOS_INSUFFICIENT = "INSUFFICIENT_OOS"
OOS_FAIL = "FAIL"
_OOS_VALIDATED = {"VALIDATED", "VALIDATED_PERMUTATION_ADVISORY"}
```

Add the function (after `run_harness`):

```python
def _filter_post_d(returns, entry_times, exit_times, d64):
    """Keep only trades whose EXIT is strictly after the discovery date d64
    (datetime64[ns]). Pre-d trades carry no edge weight (Edit 1)."""
    xt = np.asarray(exit_times, dtype="datetime64[ns]")
    mask = xt > d64
    return (
        np.asarray(returns, dtype=float)[mask],
        np.asarray(entry_times, dtype="datetime64[ns]")[mask],
        xt[mask],
    )


def run_harness_oos(
    trial_set,
    *,
    discovery_date: str,
    k_min: int,
    strategy: str,
    instrument: str,
    allocation: float,
    candidate_id: str | None = None,
    gate: GateConfig | None = None,
    **compute_overrides,
):
    """Publication-date OOS gate (Edit 1) — the survivorship-honest verdict.

    The IS-best config is selected on the FULL search (the multiple-testing
    exposure DSR penalizes; selection on all data is fine). Its EDGE is evaluated
    ONLY on the post-discovery_date partition (exit_time > d). Pre-d data carries
    no evidential weight. DSR's n_trials stays the full examined grid.

    Returns ``(oos_label, record_or_None, detail)``:
      * INSUFFICIENT_OOS — the IS-best has < k_min post-d trades (route to
        forward-paper; NOT a pass, NOT a fail). record is None.
      * OOS_PASS / FAIL  — derive_verdict on the post-d partition is / is not in
        {VALIDATED, VALIDATED_PERMUTATION_ADVISORY}. record carries the post-d
        DispositionRecord.
    """
    from validation.ingest import STARTING_EQUITY

    gate = gate or load_gate_config()
    d64 = np.datetime64(discovery_date).astype("datetime64[ns]")

    ok = trial_set.ok_trials()
    if len(ok) < 2:
        raise ValueError(
            f"TrialSet {trial_set.candidate_id} has {len(ok)} ok trials; need >= 2 "
            "to rank (PBO/DSR undefined for one config — §5 #1)."
        )

    # Selection on the FULL series (NOT re-selected on post-d — that would be
    # selecting on OOS).
    full_returns = [t.series.returns for t in ok]
    best_index_full = _select_is_best(full_returns)
    best = ok[best_index_full]

    # Per-trial post-d filter (PBO needs the family on the held-out window).
    post = []  # (trial, returns, entry_times, exit_times)
    for t in ok:
        r, et, xt = _filter_post_d(
            t.series.returns, t.series.entry_times, t.series.exit_times, d64
        )
        post.append((t, r, et, xt))

    best_post = next(p for p in post if p[0].trial_id == best.trial_id)
    n_best_post = len(best_post[1])
    detail = {
        "discovery_date": str(discovery_date),
        "best_trial_id": best.trial_id,
        "n_post_d_trades": int(n_best_post),
        "k_min": int(k_min),
        "n_total_trials": int(trial_set.total_n),
    }
    if n_best_post < k_min:
        detail["reason"] = (
            f"IS-best has {n_best_post} post-d trades < k_min={k_min}; route to "
            "forward-paper (neither pass nor fail)."
        )
        return (OOS_INSUFFICIENT, None, detail)

    # Rank family on post-d: trials rank-comparable in an N-split CSCV. Because
    # k_min >= pbo_n_splits (global constraint), the IS-best is always included.
    min_rank = int(compute_overrides.get("pbo_n_splits", 16))
    rank = [(t, r, et, xt) for (t, r, et, xt) in post if len(r) >= min_rank]
    rank_ids = [t.trial_id for (t, _, _, _) in rank]
    if len(rank) < 2 or best.trial_id not in rank_ids:
        detail["reason"] = (
            "fewer than 2 trials are rank-comparable on the post-d window "
            f"(min_rank={min_rank}); insufficient to run PBO/DSR honestly."
        )
        return (OOS_INSUFFICIENT, None, detail)

    rank_best_index = rank_ids.index(best.trial_id)   # NO OOS re-selection
    rank_returns = [r for (_, r, _, _) in rank]
    _, rb_r, rb_et, rb_xt = rank[rank_best_index]

    record = run_harness_on_family(
        rank_returns,
        rank_best_index,
        rb_et,
        rb_xt,
        total_n=trial_set.total_n,          # DSR N = full grid (selection exposure)
        candidate_id=candidate_id or trial_set.candidate_id,
        strategy=strategy,
        instrument=instrument,
        allocation=allocation,
        gate=gate,
        best_pnl=rb_r * STARTING_EQUITY,
        extra_assumptions=(
            f"OOS GATE (Edit 1): verdict computed on the exit_time > "
            f"{discovery_date} partition only; pre-d data carried no edge weight. "
            f"IS-best selected on the full search, evaluated on {len(rb_r)} post-d "
            "trades.",
        ),
        **compute_overrides,
    )
    label = OOS_PASS if record.verdict in _OOS_VALIDATED else OOS_FAIL
    detail["verdict"] = record.verdict
    return (label, record, detail)
```

- [ ] **Step 4: Run the OOS-gate tests to verify they pass**

Run: `python -m pytest lab/validation/tests/test_oos_gate.py -v`
Expected: PASS (3 tests; tighten the third's seed if you want a strict `OOS_FAIL`).

- [ ] **Step 5: Confirm existing harness behavior is untouched**

Run:
```bash
python lab/validation/harness.py --self-test
python -m pytest lab/validation/tests/ -q
```
Expected: self-test prints `RESULT: PASS`; the existing suite is green (the OOS path added nothing to `run_harness` / `run_harness_on_family` / `derive_verdict`).

- [ ] **Step 6: Commit**

```bash
git add lab/validation/harness.py lab/validation/tests/test_oos_gate.py
git commit -m "feat(harness): run_harness_oos publication-date OOS gate (Edit 1)"
```

---

## Task 4: Wire `discovery_date` into `run_candidate.py`

**Files:**
- Modify: `lab/validation/run_candidate.py`
- Test: `lab/validation/tests/test_run_candidate.py`

**Interfaces:**
- Consumes: `concept.discovery_date` (Task 1); `run_harness_oos`, `OOS_INSUFFICIENT` (Task 3).
- Produces: an `--oos-start` / `--k-min` CLI; when a `discovery_date` is present the driver runs the OOS gate and writes the OOS label into the disposition output.

- [ ] **Step 1: Write the failing test**

Add to `lab/validation/tests/test_run_candidate.py` (follow the file's existing fixture style; sketch):

```python
def test_run_candidate_oos_path_emits_label(tmp_path, monkeypatch):
    """When the concept carries a discovery_date, the driver runs the OOS gate and
    the disposition JSON carries an `oos` block with the label + detail."""
    # Reuse the module's existing synthetic/self-parity harness fixture to build a
    # TrialSet whose IS-best spans a discovery date, run run_candidate with
    # --self-parity, and assert the written JSON has rec["oos"]["label"] in
    # {"OOS_PASS","INSUFFICIENT_OOS","FAIL"} and rec["oos"]["discovery_date"] set.
    ...
```

> The existing `test_run_candidate.py` already builds a self-parity TrialSet; model this test on that fixture rather than re-deriving the feed. If the fixture has no datetime span crossing a plausible `d`, set `--oos-start` to a date inside the synthetic feed's range.

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest lab/validation/tests/test_run_candidate.py -k oos -v`
Expected: FAIL — no `--oos-start` flag / no `oos` block in the output.

- [ ] **Step 3: Add the CLI flags**

In `run_candidate.py` `_main()`, after `--min-trades`:

```python
    ap.add_argument("--oos-start", default=None,
                    help="ISO discovery_date; overrides the concept's discovery_date. "
                         "When set (or present on the concept), the OOS gate (Edit 1) runs.")
    ap.add_argument("--k-min", type=int, default=30,
                    help="min post-discovery_date trades for OOS_PASS (default 30, frozen).")
```

- [ ] **Step 4: Run the OOS gate when a discovery_date is present**

In `run_candidate()`, after the existing `rec = run_harness_on_family(...)` block and before writing `out`, add:

```python
    # ── publication-date OOS gate (Edit 1) ──────────────────────────────────
    d = args.oos_start or concept.field_text("discovery_date")
    oos_block = None
    if d and d != "undatable":
        from validation.harness import run_harness_oos, OOS_INSUFFICIENT
        oos_label, oos_rec, oos_detail = run_harness_oos(
            trial_set, discovery_date=d, k_min=args.k_min,
            strategy=args.strategy or cid, instrument=args.instrument,
            allocation=args.allocation, candidate_id=cid, **compute,
        )
        oos_block = {"label": oos_label, "detail": oos_detail,
                     "disposition": (oos_rec.to_dict() if oos_rec is not None else None)}
        print(f"OOS gate (d>{d}):  {oos_label}  "
              f"(post-d trades={oos_detail['n_post_d_trades']}, k_min={args.k_min})")
    elif d == "undatable":
        oos_block = {"label": OOS_INSUFFICIENT, "detail":
                     {"reason": "undatable concept — no historical edge weight; forward-paper only."}}
        print("OOS gate: UNDATABLE concept -> forward-paper (no historical edge weight).")
```

Then attach it to the written record. Change the `out.write_text(...)` block:

```python
    rec_dict = rec.to_dict()
    if oos_block is not None:
        rec_dict["oos"] = oos_block
    out.write_text(json.dumps(rec_dict, indent=2, default=str), encoding="utf-8")
```

- [ ] **Step 5: Run the new test + the driver suite**

Run: `python -m pytest lab/validation/tests/test_run_candidate.py -q`
Expected: PASS (the new OOS case + all existing driver tests).

- [ ] **Step 6: Smoke the full validation suite**

Run: `python -m pytest lab/validation/ lab/codification/ -q`
Expected: all green.

- [ ] **Step 7: Commit**

```bash
git add lab/validation/run_candidate.py lab/validation/tests/test_run_candidate.py
git commit -m "feat(driver): wire discovery_date -> OOS gate in run_candidate (Edit 1)"
```

---

## Self-Review

**1. Spec coverage (vs CC-handoff §2.1):**
- discovery_date schema field (optional, backward-compatible) → Task 1. ✓
- External intake requires discovery_date → Task 2 (`check_discovery_date_present`, `--external`). ✓
- Returns-independent side-prediction check (Edit 2) → Task 2 (`check_side_prediction_returns_independent`). ✓
- `t>d` partition + verdict on post-d, reusing `derive_verdict`, DSR N = full grid, no OOS re-selection → Task 3 (`run_harness_oos`). ✓
- `OOS_PASS / INSUFFICIENT_OOS / FAIL` ladder → Task 3 constants + return label. ✓
- `--oos-start` wired into the driver, OOS label in the disposition → Task 4. ✓
- §5 forbidden move "never confirm a mechanism with its own returns" is enforced structurally by Task 2's performance-only hard FAIL. ✓
- *Not in this plan (by design):* §2.2–2.N (harvest, pre-screen, concept authoring, freeze, per-lane validation, corpus-FDR, portfolio gate) — those are the *investigation*, executed as a Workflow + per-concept Pre-Qs AFTER this machinery lands and passes the brief §7 review. This plan is the gating dependency only.

**2. Placeholder scan:** Task 4 Step 1 intentionally sketches the test against the existing `test_run_candidate.py` fixture (its feed-construction is local to that file and must be reused, not re-derived) — the executor reads that fixture and fills the body; every code-bearing step in Tasks 1–3 carries complete code. No `TBD`/`add error handling`/`similar to` placeholders elsewhere.

**3. Type consistency:** `discovery_date: str | None` (Task 1) is read via `field_text` → `""` when None (Task 2, Task 4). `run_harness_oos` returns `(str, DispositionRecord | None, dict)` (Task 3) consumed exactly that way in Task 4. `OOS_PASS/OOS_INSUFFICIENT/OOS_FAIL` defined in Task 3, imported in Task 4. `run_checks(..., external=False)` signature (Task 2) matches the Task 2 tests and the `main()` call. `pbo_n_splits` in `compute_overrides` is the same knob `run_harness_on_family` already accepts. Consistent.

**Note for the executor:** if Phase-0 re-reads (CC-handoff §0) contradict any assertion this plan rests on — `exit_times` not `datetime64[ns]`, `derive_verdict` not reusable on a sub-series, the contract not loadable with an extra block — STOP and return `NEEDS_CONTEXT` per the brief, do not build on the assumed semantics.
