# Cross-campaign Mechanism Prior Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a disclosure-only tool that reads First Passage's closed-campaign history and reports a small-N-honest survival-rate prior by mechanism tier, sourcing channel, and instrument — so future sourcing decisions are informed by measured history instead of nothing.

**Architecture:** Four layers, each independently testable: (1) a validated, append-only JSON-Lines tag store; (2) pure-arithmetic Wilson-interval aggregation + Markdown report generation; (3) a batch validator/ingest CLI that gates what enters the store; (4) a one-time (then incremental) LLM tagging pass over `docs/rejected_candidates.md` (117 entries) and `discovery_manifests/*.json` (15 entries), run via the Workflow tool, whose output is validated by layer 3 before it ever touches the store.

**Tech Stack:** Python 3.11+ (matching this repo's floor), `pytest`, stdlib only (`json`, `argparse`, `re`, `math`, `dataclasses`) — no new dependencies.

## Global Constraints

- Never gates, blocks, or auto-selects anything — every output is disclosure-only, consumed by a human. [design spec §4/§5]
- Every reported rate carries its N and a 95% Wilson score interval — never a bare percentage. [design spec §3]
- Storage is append-only — corrections are new records with a `supersedes` pointer; nothing is ever edited or deleted in place. [design spec §6]
- Reuses `strategy_harvest.md`'s existing `mechanism_tier` (A/B/C) and `sourcing_channel_rank` (1–6, 1-tie) vocabulary verbatim — no new taxonomy. [design spec §3]
- The LLM only classifies already-*closed*, already-verdicted history — it never scores or judges anything live or in-flight. [design spec §5]
- No cross-tabs (tier × channel × instrument) — reported univariate only, one dimension at a time. [design spec §4]
- No new standing automation or hooks — tagging a new closure is a manual step at closure time. [design spec §4]

---

## Phase 1: Schema & storage infrastructure

### Task 1: Shared test fixture + tag schema/validation

**Files:**
- Create: `tests/conftest.py`
- Create: `lab/research_utils/mechanism_prior_schema.py`
- Test: `tests/test_mechanism_prior_schema.py`

**Interfaces:**
- Produces: `validate_tag_record(record: dict) -> None` (raises `TagValidationError` on any violation), `TagValidationError`, `MECHANISM_TIERS`, `SOURCING_CHANNEL_RANKS`, `OUTCOMES` (all `set[str]`) — consumed by Tasks 2 and 5.
- Produces (fixture): a `valid_tag_record` pytest fixture — a factory function `(**overrides) -> dict` returning a valid 5-field tag record — consumed by every test file in this plan (Tasks 1, 2, 4, 5) instead of each defining its own local `_record`/`_valid` helper.

**Note:** this task starts with `tests/conftest.py` (not test code for this task's own module) because every later test file needs the shared fixture from its first test onward — creating it once here, before any test file is written, avoids a later find-and-replace across 4 files.

- [ ] **Step 1: Create the shared fixture (no test — this is fixture infrastructure, exercised implicitly by every test that uses it below)**

```python
# tests/conftest.py
"""Shared pytest fixtures for mechanism-prior tests."""

import pytest


@pytest.fixture
def valid_tag_record():
    """Factory fixture: call with field overrides to build a valid tag record dict.

    `valid_tag_record()` returns a record that passes validate_tag_record()
    unmodified; `valid_tag_record(mechanism_tier="B")` overrides one field.
    Overriding "provenance" replaces the whole sub-dict (pass a complete one).
    """

    def _make(**overrides):
        record = {
            "mechanism_tier": "A",
            "sourcing_channel_rank": "3",
            "target_instrument_family": "MNQ",
            "outcome": "SURVIVED",
            "provenance": {
                "source_path": "docs/rejected_candidates.md",
                "source_ref": "entry-1",
                "tagged_at": "2026-08-20",
            },
        }
        record.update(overrides)
        return record

    return _make
```

- [ ] **Step 2: Write the failing tests**

```python
# tests/test_mechanism_prior_schema.py
import pytest

from lab.research_utils.mechanism_prior_schema import (
    TagValidationError,
    validate_tag_record,
)


def test_valid_record_passes(valid_tag_record):
    validate_tag_record(valid_tag_record())  # must not raise


def test_missing_field_rejected(valid_tag_record):
    record = valid_tag_record()
    del record["outcome"]
    with pytest.raises(TagValidationError, match="missing required fields"):
        validate_tag_record(record)


def test_bad_mechanism_tier_rejected(valid_tag_record):
    with pytest.raises(TagValidationError, match="mechanism_tier"):
        validate_tag_record(valid_tag_record(mechanism_tier="Z"))


def test_bad_sourcing_channel_rank_rejected(valid_tag_record):
    with pytest.raises(TagValidationError, match="sourcing_channel_rank"):
        validate_tag_record(valid_tag_record(sourcing_channel_rank="7"))


def test_bad_outcome_rejected(valid_tag_record):
    with pytest.raises(TagValidationError, match="outcome"):
        validate_tag_record(valid_tag_record(outcome="MAYBE"))


def test_empty_instrument_family_rejected(valid_tag_record):
    with pytest.raises(TagValidationError, match="target_instrument_family"):
        validate_tag_record(valid_tag_record(target_instrument_family="  "))


def test_provenance_must_be_object(valid_tag_record):
    with pytest.raises(TagValidationError, match="provenance must be an object"):
        validate_tag_record(valid_tag_record(provenance="not-a-dict"))


def test_provenance_missing_subfield_rejected(valid_tag_record):
    record = valid_tag_record()
    del record["provenance"]["tagged_at"]
    with pytest.raises(TagValidationError, match="provenance missing fields"):
        validate_tag_record(record)


def test_n_a_sourcing_channel_allowed_for_mined_entries(valid_tag_record):
    validate_tag_record(valid_tag_record(sourcing_channel_rank="n/a"))  # must not raise


def test_extra_provenance_fields_allowed(valid_tag_record):
    record = valid_tag_record()
    record["provenance"]["reasoning"] = "cites the closure's own FALSIFIED verdict"
    validate_tag_record(record)  # must not raise -- extra fields are fine
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `pytest tests/test_mechanism_prior_schema.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'lab.research_utils.mechanism_prior_schema'` (the fixture itself loads fine; it's the module under test that doesn't exist yet)

- [ ] **Step 4: Write the implementation**

```python
# lab/research_utils/mechanism_prior_schema.py
"""Schema and validation for cross-campaign mechanism-prior tag records.

See docs/superpowers/specs/2026-08-20-cross-campaign-mechanism-prior-design.md.
"""

from __future__ import annotations

MECHANISM_TIERS = {"A", "B", "C", "unclear"}
SOURCING_CHANNEL_RANKS = {"1", "2", "3", "4", "5", "6", "1-tie", "n/a"}
OUTCOMES = {"SURVIVED", "KILLED_AT_ADMISSION", "KILLED_AT_TEST", "AMBIGUOUS"}

REQUIRED_FIELDS = {
    "mechanism_tier",
    "sourcing_channel_rank",
    "target_instrument_family",
    "outcome",
    "provenance",
}

PROVENANCE_REQUIRED_FIELDS = {"source_path", "source_ref", "tagged_at"}


class TagValidationError(ValueError):
    """Raised when a proposed tag record fails schema validation."""


def validate_tag_record(record: dict) -> None:
    """Raise TagValidationError if `record` does not conform to the schema.

    Does not mutate `record`. Safe to call before appending. Extra keys
    (e.g. provenance.reasoning) are always allowed -- this validates the
    required shape, not a closed schema.
    """
    missing = REQUIRED_FIELDS - record.keys()
    if missing:
        raise TagValidationError(f"missing required fields: {sorted(missing)}")

    if record["mechanism_tier"] not in MECHANISM_TIERS:
        raise TagValidationError(
            f"mechanism_tier {record['mechanism_tier']!r} not in {sorted(MECHANISM_TIERS)}"
        )
    if record["sourcing_channel_rank"] not in SOURCING_CHANNEL_RANKS:
        raise TagValidationError(
            f"sourcing_channel_rank {record['sourcing_channel_rank']!r} "
            f"not in {sorted(SOURCING_CHANNEL_RANKS)}"
        )
    if record["outcome"] not in OUTCOMES:
        raise TagValidationError(f"outcome {record['outcome']!r} not in {sorted(OUTCOMES)}")

    instrument = record["target_instrument_family"]
    if not isinstance(instrument, str) or not instrument.strip():
        raise TagValidationError("target_instrument_family must be a non-empty string")

    provenance = record["provenance"]
    if not isinstance(provenance, dict):
        raise TagValidationError("provenance must be an object")
    missing_prov = PROVENANCE_REQUIRED_FIELDS - provenance.keys()
    if missing_prov:
        raise TagValidationError(f"provenance missing fields: {sorted(missing_prov)}")

    if "supersedes" in record and not isinstance(record["supersedes"], dict):
        raise TagValidationError("supersedes, if present, must be an object with source_path/source_ref")
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/test_mechanism_prior_schema.py -v`
Expected: 10 passed

- [ ] **Step 6: Commit**

```bash
git add tests/conftest.py lab/research_utils/mechanism_prior_schema.py tests/test_mechanism_prior_schema.py
git commit -m "feat(research_utils): mechanism-prior tag schema + validation + shared test fixture"
```

---

### Task 2: Append-only tag store

**Files:**
- Create: `lab/research_utils/mechanism_prior_store.py`
- Test: `tests/test_mechanism_prior_store.py`

**Interfaces:**
- Consumes: `validate_tag_record`, `TagValidationError` (Task 1); the `valid_tag_record` pytest fixture (Task 1, from `tests/conftest.py`) in this task's own tests.
- Produces: `DEFAULT_STORE_PATH: Path`, `load_all_records(store_path) -> list[dict]`, `load_latest_records(store_path) -> list[dict]`, `append_record(record, store_path) -> None` — consumed by Tasks 4 and 5.

**Storage format:** JSON Lines (one JSON object per line) inside the file named in the design spec (`lab/research_utils/mechanism_prior_tags.json`) — genuinely append-only (a new line never touches existing bytes), unlike a single JSON array which would require rewriting the whole file on every append.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_mechanism_prior_store.py
import json

import pytest

from lab.research_utils.mechanism_prior_schema import TagValidationError
from lab.research_utils.mechanism_prior_store import (
    append_record,
    load_all_records,
    load_latest_records,
)


def test_load_all_records_missing_file_returns_empty(tmp_path):
    assert load_all_records(tmp_path / "nope.json") == []


def test_append_then_load_round_trips(tmp_path, valid_tag_record):
    store = tmp_path / "tags.json"
    append_record(valid_tag_record(), store_path=store)
    records = load_all_records(store)
    assert len(records) == 1
    assert records[0]["mechanism_tier"] == "A"


def test_append_is_one_line_per_record(tmp_path, valid_tag_record):
    store = tmp_path / "tags.json"
    append_record(
        valid_tag_record(provenance={"source_path": "x", "source_ref": "1", "tagged_at": "d"}), store_path=store
    )
    append_record(
        valid_tag_record(provenance={"source_path": "x", "source_ref": "2", "tagged_at": "d"}), store_path=store
    )
    lines = store.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2
    json.loads(lines[0])
    json.loads(lines[1])


def test_append_rejects_invalid_record(tmp_path, valid_tag_record):
    store = tmp_path / "tags.json"
    with pytest.raises(TagValidationError):
        append_record(valid_tag_record(mechanism_tier="nope"), store_path=store)
    assert not store.exists()


def test_append_never_truncates_existing_content(tmp_path, valid_tag_record):
    store = tmp_path / "tags.json"
    append_record(
        valid_tag_record(provenance={"source_path": "x", "source_ref": "1", "tagged_at": "d"}), store_path=store
    )
    append_record(
        valid_tag_record(provenance={"source_path": "x", "source_ref": "2", "tagged_at": "d"}), store_path=store
    )
    assert len(load_all_records(store)) == 2


def test_load_latest_prefers_superseding_record(tmp_path, valid_tag_record):
    store = tmp_path / "tags.json"
    original = valid_tag_record(
        mechanism_tier="B",
        provenance={"source_path": "docs/rejected_candidates.md", "source_ref": "entry-9", "tagged_at": "2026-08-18"},
    )
    append_record(original, store_path=store)

    correction = valid_tag_record(
        mechanism_tier="A",
        provenance={
            "source_path": "docs/rejected_candidates.md",
            "source_ref": "entry-9-correction",
            "tagged_at": "2026-08-20",
        },
        supersedes={"source_path": "docs/rejected_candidates.md", "source_ref": "entry-9"},
    )
    append_record(correction, store_path=store)

    latest = load_latest_records(store)
    assert len(latest) == 1
    assert latest[0]["mechanism_tier"] == "A"


def test_load_latest_keeps_unrelated_records(tmp_path, valid_tag_record):
    store = tmp_path / "tags.json"
    append_record(
        valid_tag_record(provenance={"source_path": "x", "source_ref": "1", "tagged_at": "d"}), store_path=store
    )
    append_record(
        valid_tag_record(provenance={"source_path": "x", "source_ref": "2", "tagged_at": "d"}), store_path=store
    )
    assert len(load_latest_records(store)) == 2
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_mechanism_prior_store.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'lab.research_utils.mechanism_prior_store'` (the `valid_tag_record` fixture loads fine — it comes from `tests/conftest.py`, created in Task 1)

- [ ] **Step 3: Write the implementation**

```python
# lab/research_utils/mechanism_prior_store.py
"""Append-only storage for mechanism-prior tag records.

JSON-Lines format -- one record per line, genuinely append-only. See
docs/superpowers/specs/2026-08-20-cross-campaign-mechanism-prior-design.md
§4/§6.
"""

from __future__ import annotations

import json
from pathlib import Path

from lab.research_utils.mechanism_prior_schema import validate_tag_record

DEFAULT_STORE_PATH = Path("lab/research_utils/mechanism_prior_tags.json")


def load_all_records(store_path: Path = DEFAULT_STORE_PATH) -> list[dict]:
    """Return every record in the store, in file order. Empty list if missing/empty."""
    if not store_path.exists():
        return []
    text = store_path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def _record_key(record: dict) -> tuple[str, str]:
    prov = record["provenance"]
    return (prov["source_path"], prov["source_ref"])


def load_latest_records(store_path: Path = DEFAULT_STORE_PATH) -> list[dict]:
    """Return one record per (source_path, source_ref), dropping any record
    a later record's `supersedes` pointer names. The superseded record still
    exists on disk (append-only) -- it is only excluded from this view.
    """
    all_records = load_all_records(store_path)
    latest: dict[tuple[str, str], dict] = {}
    superseded_keys: set[tuple[str, str]] = set()

    for record in all_records:
        key = _record_key(record)
        latest[key] = record
        if "supersedes" in record:
            sup = record["supersedes"]
            superseded_keys.add((sup["source_path"], sup["source_ref"]))

    return [rec for key, rec in latest.items() if key not in superseded_keys]


def append_record(record: dict, store_path: Path = DEFAULT_STORE_PATH) -> None:
    """Validate and append one record as a new line. Never overwrites."""
    validate_tag_record(record)
    store_path.parent.mkdir(parents=True, exist_ok=True)
    with store_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_mechanism_prior_store.py -v`
Expected: 7 passed

- [ ] **Step 5: Commit**

```bash
git add lab/research_utils/mechanism_prior_store.py tests/test_mechanism_prior_store.py
git commit -m "feat(research_utils): append-only mechanism-prior tag store"
```

---

## Phase 2: Weight computation & reporting

### Task 3: Wilson score interval

**Files:**
- Create: `lab/research_utils/wilson_interval.py`
- Test: `tests/test_wilson_interval.py`

**Interfaces:**
- Produces: `wilson_interval(successes: int, n: int, z: float = Z_95) -> tuple[float, float]` — consumed by Task 4.

- [ ] **Step 1: Write the failing tests**

Reference values below were computed directly from the formula (not eyeballed) — verify by running the formula yourself if you doubt them:

```python
# tests/test_wilson_interval.py
import pytest

from lab.research_utils.wilson_interval import wilson_interval


def test_reference_value_8_of_10():
    lower, upper = wilson_interval(8, 10)
    assert lower == pytest.approx(0.4901624715366418, abs=1e-9)
    assert upper == pytest.approx(0.9433178485456247, abs=1e-9)


def test_reference_value_0_of_20():
    lower, upper = wilson_interval(0, 20)
    assert lower == pytest.approx(0.0, abs=1e-9)
    assert upper == pytest.approx(0.16112515805281938, abs=1e-9)


def test_reference_value_20_of_20():
    lower, upper = wilson_interval(20, 20)
    assert lower == pytest.approx(0.8388748419471806, abs=1e-9)
    assert upper == pytest.approx(1.0, abs=1e-9)


def test_reference_value_5_of_10():
    lower, upper = wilson_interval(5, 10)
    assert lower == pytest.approx(0.236593090512564, abs=1e-9)
    assert upper == pytest.approx(0.763406909487436, abs=1e-9)


def test_larger_n_gives_narrower_interval_at_same_proportion():
    lo_small, hi_small = wilson_interval(5, 10)
    lo_big, hi_big = wilson_interval(50, 100)
    assert (hi_big - lo_big) < (hi_small - lo_small)


def test_rejects_zero_n():
    with pytest.raises(ValueError, match="n must be positive"):
        wilson_interval(0, 0)


def test_rejects_negative_n():
    with pytest.raises(ValueError, match="n must be positive"):
        wilson_interval(0, -1)


def test_rejects_successes_greater_than_n():
    with pytest.raises(ValueError, match="successes must be within"):
        wilson_interval(11, 10)


def test_rejects_negative_successes():
    with pytest.raises(ValueError, match="successes must be within"):
        wilson_interval(-1, 10)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_wilson_interval.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'lab.research_utils.wilson_interval'`

- [ ] **Step 3: Write the implementation**

```python
# lab/research_utils/wilson_interval.py
"""95% Wilson score confidence interval for a binomial proportion.

Used by mechanism_prior.py so every reported rate carries an N-aware
interval instead of a bare percentage (this repo's Rule 1 -- small-cell
variance prior).
"""

from __future__ import annotations

import math

Z_95 = 1.959963984540054  # two-sided 95% normal quantile


def wilson_interval(successes: int, n: int, z: float = Z_95) -> tuple[float, float]:
    """Return (lower, upper) Wilson score bounds for successes/n.

    Raises ValueError if n <= 0 or successes is out of [0, n].
    """
    if n <= 0:
        raise ValueError("n must be positive")
    if not (0 <= successes <= n):
        raise ValueError("successes must be within [0, n]")

    p_hat = successes / n
    denom = 1 + z ** 2 / n
    center = p_hat + z ** 2 / (2 * n)
    margin = z * math.sqrt((p_hat * (1 - p_hat) + z ** 2 / (4 * n)) / n)
    lower = (center - margin) / denom
    upper = (center + margin) / denom
    return max(0.0, lower), min(1.0, upper)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_wilson_interval.py -v`
Expected: 9 passed

- [ ] **Step 5: Commit**

```bash
git add lab/research_utils/wilson_interval.py tests/test_wilson_interval.py
git commit -m "feat(research_utils): Wilson score interval for small-N rates"
```

---

### Task 4: Aggregation, report rendering, and CLI

**Files:**
- Create: `lab/research_utils/mechanism_prior.py`
- Test: `tests/test_mechanism_prior.py`

**Interfaces:**
- Consumes: `wilson_interval` (Task 3); `DEFAULT_STORE_PATH`, `load_latest_records` (Task 2); the `valid_tag_record` pytest fixture (Task 1) in this task's own tests.
- Produces: `aggregate_by_field(records, field) -> dict[str, tuple[int, int, float, float]]`, `render_report(records, store_path, now) -> str`, `main(argv=None) -> int` — this is the script named in the design spec, run via `python lab/research_utils/mechanism_prior.py`.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_mechanism_prior.py
import json
from datetime import datetime, timezone
from pathlib import Path

from lab.research_utils.mechanism_prior import aggregate_by_field, main, render_report


def test_aggregate_counts_survivors_and_n(valid_tag_record):
    records = [
        valid_tag_record(mechanism_tier="A", outcome="SURVIVED"),
        valid_tag_record(mechanism_tier="A", outcome="KILLED_AT_TEST"),
        valid_tag_record(mechanism_tier="B", outcome="SURVIVED"),
    ]
    table = aggregate_by_field(records, "mechanism_tier")
    assert table["A"][0] == 1  # successes
    assert table["A"][1] == 2  # n
    assert table["B"][0] == 1
    assert table["B"][1] == 1


def test_aggregate_returns_wilson_bounds_within_unit_interval(valid_tag_record):
    records = [valid_tag_record(outcome="SURVIVED"), valid_tag_record(outcome="KILLED_AT_TEST")]
    table = aggregate_by_field(records, "mechanism_tier")
    successes, n, lo, hi = table["A"]
    assert 0.0 <= lo <= hi <= 1.0


def test_aggregate_of_empty_records_is_empty():
    assert aggregate_by_field([], "mechanism_tier") == {}


def test_render_report_contains_all_three_field_sections(valid_tag_record):
    report = render_report([valid_tag_record()], Path("fake/path.json"), datetime(2026, 8, 20, tzinfo=timezone.utc))
    assert "By mechanism tier" in report
    assert "By sourcing channel rank" in report
    assert "By target instrument family" in report


def test_render_report_every_data_row_has_bracketed_interval(valid_tag_record):
    records = [valid_tag_record(), valid_tag_record(outcome="KILLED_AT_TEST")]
    report = render_report(records, Path("fake/path.json"), datetime(2026, 8, 20, tzinfo=timezone.utc))
    data_rows = [line for line in report.splitlines() if line.startswith("| A |")]
    assert data_rows
    for line in data_rows:
        assert "[" in line and "]" in line


def test_render_report_shows_entry_count_and_timestamp(valid_tag_record):
    now = datetime(2026, 8, 20, 12, 0, 0, tzinfo=timezone.utc)
    report = render_report(
        [valid_tag_record(), valid_tag_record()], Path("lab/research_utils/mechanism_prior_tags.json"), now
    )
    assert "2 current records" in report
    assert "2026-08-20T12:00:00" in report


def test_cli_writes_report_to_out_file(tmp_path, valid_tag_record):
    store = tmp_path / "tags.json"
    store.write_text(json.dumps(valid_tag_record()) + "\n", encoding="utf-8")
    out = tmp_path / "report.md"

    exit_code = main(["--store", str(store), "--out", str(out)])

    assert exit_code == 0
    assert out.exists()
    assert "By mechanism tier" in out.read_text(encoding="utf-8")


def test_cli_prints_to_stdout_when_no_out_given(tmp_path, capsys, valid_tag_record):
    store = tmp_path / "tags.json"
    store.write_text(json.dumps(valid_tag_record()) + "\n", encoding="utf-8")

    exit_code = main(["--store", str(store)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "By mechanism tier" in captured.out
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_mechanism_prior.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'lab.research_utils.mechanism_prior'` (the `valid_tag_record` fixture loads fine — it comes from `tests/conftest.py`, created in Task 1)

- [ ] **Step 3: Write the implementation**

```python
# lab/research_utils/mechanism_prior.py
"""Cross-campaign mechanism prior -- computes and reports univariate
survival rates by mechanism_tier, sourcing_channel_rank, and
target_instrument_family.

See docs/superpowers/specs/2026-08-20-cross-campaign-mechanism-prior-design.md.
Pure arithmetic over lab/research_utils/mechanism_prior_tags.json -- never
calls an LLM, never gates anything. Run on demand:

    python lab/research_utils/mechanism_prior.py
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from lab.research_utils.mechanism_prior_store import DEFAULT_STORE_PATH, load_latest_records
from lab.research_utils.wilson_interval import wilson_interval

SURVIVED = "SURVIVED"
FIELDS_TO_REPORT = ("mechanism_tier", "sourcing_channel_rank", "target_instrument_family")
FIELD_TITLES = {
    "mechanism_tier": "By mechanism tier",
    "sourcing_channel_rank": "By sourcing channel rank",
    "target_instrument_family": "By target instrument family",
}


def aggregate_by_field(records: list[dict], field: str) -> dict[str, tuple[int, int, float, float]]:
    """Group records by `field`, return {value: (successes, n, lo, hi)}.

    "successes" counts outcome == SURVIVED. A value with n == 0 never
    appears (nothing to divide by). Requires n >= 1 per group -- callers
    must not pass an empty `records` list expecting per-value output.
    """
    counts: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for record in records:
        value = record[field]
        counts[value][1] += 1
        if record["outcome"] == SURVIVED:
            counts[value][0] += 1

    result = {}
    for value, (successes, n) in counts.items():
        lo, hi = wilson_interval(successes, n)
        result[value] = (successes, n, lo, hi)
    return result


def render_report(records: list[dict], store_path: Path, now: datetime) -> str:
    """Render the full Markdown report for the given records."""
    lines = [
        "# Cross-campaign mechanism prior",
        "",
        f"Generated: {now.isoformat()}",
        f"Tag store: `{store_path}` -- {len(records)} current records "
        "(superseded records excluded from this count; see `supersedes` "
        "chains in the raw file for the full history).",
        "",
        "Every rate below is 95% Wilson-interval bounded, not a bare "
        "percentage. Small cells (single-digit N) are expected in this "
        "corpus by design -- read the interval width, not just the center.",
        "",
    ]
    for field in FIELDS_TO_REPORT:
        table = aggregate_by_field(records, field)
        lines.append(f"## {FIELD_TITLES[field]}")
        lines.append("")
        lines.append("| Value | Survived / N | 95% Wilson interval |")
        lines.append("|---|---|---|")
        for value in sorted(table):
            successes, n, lo, hi = table[value]
            lines.append(f"| {value} | {successes}/{n} | [{lo:.3f}, {hi:.3f}] |")
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store", type=Path, default=DEFAULT_STORE_PATH)
    parser.add_argument("--out", type=Path, default=None, help="write report here instead of stdout")
    args = parser.parse_args(argv)

    records = load_latest_records(args.store)
    report = render_report(records, args.store, datetime.now(timezone.utc))

    if args.out:
        args.out.write_text(report, encoding="utf-8")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_mechanism_prior.py -v`
Expected: 8 passed

- [ ] **Step 5: Commit**

```bash
git add lab/research_utils/mechanism_prior.py tests/test_mechanism_prior.py
git commit -m "feat(research_utils): mechanism-prior aggregation, report, CLI"
```

---

## Phase 3: Tagging pipeline & the one-time historical pass

### Task 5: Batch validator/ingest CLI

**Files:**
- Create: `lab/research_utils/mechanism_prior_ingest.py`
- Test: `tests/test_mechanism_prior_ingest.py`

**Interfaces:**
- Consumes: `validate_tag_record`, `TagValidationError` (Task 1); `append_record` (Task 2); the `valid_tag_record` pytest fixture (Task 1) in this task's own tests.
- Produces: `load_proposed_records(path) -> list[dict]`, `validate_batch(records) -> list[str]`, `ingest(proposed_path, store_path) -> int`, `main(argv=None) -> int` — this is what Task 7's tagging pass runs its output through before anything reaches the real store.

- [ ] **Step 1: Write the failing tests**

Every record below uses `valid_tag_record(provenance={... "source_ref": ref ...})` rather than a
locally-defined helper, so `source_ref` is the only thing that varies call to call — the shared
fixture (Task 1) is the single place the 5-field shape is defined.

```python
# tests/test_mechanism_prior_ingest.py
import json
from pathlib import Path

import pytest

from lab.research_utils.mechanism_prior_ingest import ingest, main, validate_batch
from lab.research_utils.mechanism_prior_schema import TagValidationError
from lab.research_utils.mechanism_prior_store import load_all_records


def _write_proposed(path: Path, records: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(r) for r in records) + "\n", encoding="utf-8")


def _prov(ref: str) -> dict:
    return {"source_path": "docs/rejected_candidates.md", "source_ref": ref, "tagged_at": "2026-08-20"}


def test_validate_batch_all_valid_returns_no_errors(valid_tag_record):
    records = [valid_tag_record(provenance=_prov("1")), valid_tag_record(provenance=_prov("2"))]
    assert validate_batch(records) == []


def test_validate_batch_reports_each_bad_record_with_locator(valid_tag_record):
    bad = valid_tag_record(mechanism_tier="nope", provenance=_prov("3"))
    good = valid_tag_record(provenance=_prov("1"))
    errors = validate_batch([good, bad])
    assert len(errors) == 1
    assert "record 1" in errors[0]
    assert "3" in errors[0]


def test_ingest_appends_full_valid_batch(tmp_path, valid_tag_record):
    proposed = tmp_path / "proposed.jsonl"
    store = tmp_path / "tags.json"
    records = [valid_tag_record(provenance=_prov(ref)) for ref in ("1", "2", "3")]
    _write_proposed(proposed, records)

    count = ingest(proposed, store_path=store)

    assert count == 3
    assert len(load_all_records(store)) == 3


def test_ingest_rejects_whole_batch_on_any_invalid_record(tmp_path, valid_tag_record):
    proposed = tmp_path / "proposed.jsonl"
    store = tmp_path / "tags.json"
    bad = valid_tag_record(outcome="MAYBE", provenance=_prov("2"))
    records = [valid_tag_record(provenance=_prov("1")), bad, valid_tag_record(provenance=_prov("3"))]
    _write_proposed(proposed, records)

    with pytest.raises(TagValidationError, match="0 records appended"):
        ingest(proposed, store_path=store)

    assert not store.exists()


def test_cli_exit_code_1_on_bad_batch(tmp_path, capsys, valid_tag_record):
    proposed = tmp_path / "proposed.jsonl"
    store = tmp_path / "tags.json"
    bad = valid_tag_record(mechanism_tier="nope", provenance=_prov("1"))
    _write_proposed(proposed, [bad])

    exit_code = main([str(proposed), "--store", str(store)])

    assert exit_code == 1
    assert "batch rejected" in capsys.readouterr().err


def test_cli_exit_code_0_and_message_on_success(tmp_path, capsys, valid_tag_record):
    proposed = tmp_path / "proposed.jsonl"
    store = tmp_path / "tags.json"
    _write_proposed(proposed, [valid_tag_record(provenance=_prov("1"))])

    exit_code = main([str(proposed), "--store", str(store)])

    assert exit_code == 0
    assert "appended 1 records" in capsys.readouterr().out
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_mechanism_prior_ingest.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'lab.research_utils.mechanism_prior_ingest'` (the `valid_tag_record` fixture loads fine — it comes from `tests/conftest.py`, created in Task 1)

- [ ] **Step 3: Write the implementation**

```python
# lab/research_utils/mechanism_prior_ingest.py
"""Batch-validate and append proposed mechanism-prior tag records.

Used by the one-time tagging pass (design spec §3/§4, Task 7 of this
plan). Reads a JSON-Lines file of PROPOSED records, validates every one
against the schema, and only appends to the store if the WHOLE batch is
valid -- never a partial append, so a malformed batch can be fixed and
re-run without hand-auditing what already landed.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from lab.research_utils.mechanism_prior_schema import TagValidationError, validate_tag_record
from lab.research_utils.mechanism_prior_store import DEFAULT_STORE_PATH, append_record


def load_proposed_records(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def validate_batch(records: list[dict]) -> list[str]:
    """Return one error string per invalid record (empty list if all valid)."""
    errors = []
    for i, record in enumerate(records):
        try:
            validate_tag_record(record)
        except TagValidationError as exc:
            ref = record.get("provenance", {}).get("source_ref", "?")
            errors.append(f"record {i} ({ref}): {exc}")
    return errors


def ingest(proposed_path: Path, store_path: Path = DEFAULT_STORE_PATH) -> int:
    """Validate then append every record in `proposed_path` to `store_path`.

    Returns the count appended. Raises TagValidationError (all failures
    joined) if any record is invalid -- nothing is appended in that case.
    """
    records = load_proposed_records(proposed_path)
    errors = validate_batch(records)
    if errors:
        raise TagValidationError("batch rejected, 0 records appended:\n" + "\n".join(errors))
    for record in records:
        append_record(record, store_path=store_path)
    return len(records)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("proposed", type=Path, help="JSON-Lines file of proposed tag records")
    parser.add_argument("--store", type=Path, default=DEFAULT_STORE_PATH)
    args = parser.parse_args(argv)

    try:
        count = ingest(args.proposed, args.store)
    except TagValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"appended {count} records to {args.store}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_mechanism_prior_ingest.py -v`
Expected: 6 passed

- [ ] **Step 5: Commit**

```bash
git add lab/research_utils/mechanism_prior_ingest.py tests/test_mechanism_prior_ingest.py
git commit -m "feat(research_utils): batch validator/ingest CLI for proposed tags"
```

---

### Task 6: Split `rejected_candidates.md` into taggable entries

**Files:**
- Create: `lab/research_utils/mechanism_prior_extract.py`
- Test: `tests/test_mechanism_prior_extract.py`

**Interfaces:**
- Produces: `RawEntry` (dataclass: `title: str`, `body: str`, `source_ref: str`), `split_entries(markdown_text: str) -> list[RawEntry]`, `load_entries(path: Path) -> list[RawEntry]` — consumed by Task 7's driver step.

**Rule-0 note (RE-VERIFIED 2026-08-21 — supersedes this task's original 2026-08-20 note, which
is now stale):** `docs/rejected_candidates.md` was reorganized upstream between this task's
original authoring and dispatch — a real drift a Cursor-fleet dispatch of the *original* version
of this task correctly caught and bounced `NEEDS_CONTEXT` on, rather than guessing (see
`docs/briefs/handoffs/2026-08-21-cursor-fleet-mechanism-prior-tasks-5-6.md` Packet B's return).
Verified directly against the file at `origin/main`@1b53833: it now has **6 `##` sections**, not
one flat `## Entries` list:

| `##` section | `###` count | Per-candidate entries? |
|---|---|---|
| Entries | 17 | Yes |
| Queryable index (concept-intake gate, added 2026-06-05) | 15 | Yes — same prose-field shape as Entries, confirmed by direct read (Rejection scope / Closure date / Class / Authoritative artifact); historically served a since-retired machine dedup consumer, but the records themselves are real per-candidate closures, not duplicates of the Entries section |
| Harness-fed rejections (auto-appended) | 0 (currently empty) | Yes, by name/design — future auto-appended per-candidate records |
| Domain-level SNAG closures | 1 | **No** — explicitly "distinct from the per-direction entries above": a whole research *domain* closed on SNAG-budget exhaustion, spanning many instruments as one roll-up record (verified: the one entry cites XAGUSD/USOIL/EURGBP/EURUSD/GEX/T10Y3M/Friday/rates-MR/dispersion as its object-level instances) — does not fit the schema's one-`target_instrument_family`-per-record assumption |
| Domain-level tail-exhaustion raised bars | 2 | **No** — same reasoning: a domain-level re-proposal-bar record, not a per-candidate outcome |
| Audit hooks | 0 (currently empty) | No — mechanical/process content, never per-candidate entries |

Design: `split_entries` parses `### ` headings from every `##` section **except** a named
denylist (`Domain-level SNAG closures`, `Domain-level tail-exhaustion raised bars`, `Audit
hooks`) — a denylist rather than an allowlist so a future new per-candidate section (like
`Harness-fed rejections` once it's populated) is picked up automatically without a further code
change, while the two structurally-different domain-rollup sections stay permanently excluded
by name. Current real yield: 17 + 15 + 0 = **32 per-candidate entries** (not the 117 this task
originally assumed, and not the 35 total `###` headings in the file — 3 of those are domain-
level rollups, correctly excluded).

~31 of the per-candidate entries additionally carry a structured
`<!-- concept-intake-entry ... -->` HTML comment (instrument, class, date attributes), but this
coverage is partial and the attribute vocabulary heterogeneous — it's useful *context* handed to
the tagging pass in Task 7, not a shortcut around it.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_mechanism_prior_extract.py
from pathlib import Path

from lab.research_utils.mechanism_prior_extract import load_entries, split_entries

SAMPLE = """# Rejected portfolio candidates

Some preamble text that is not an entry.

## Entries

### First entry title -- FALSIFIED

**Rejection scope:** blah blah.
**Closure date:** 2026-08-13

<!-- concept-intake-entry instrument="MNQ" -->

### Second entry title -- STAGE-1 FAIL

**Rejection scope:** other blah.

## Domain-level SNAG closures

### A domain rollup that must be excluded

**Scope:** spans many instruments -- not a per-candidate entry.

## Queryable index (concept-intake gate, added 2026-06-05)

### Third entry title -- from the index section

**Rejection scope:** index-section blah.

## Audit hooks

### Not a candidate either

Mechanical check text, also excluded.
"""


def test_split_entries_ignores_preamble_before_first_section():
    entries = split_entries(SAMPLE)
    titles = [e.title for e in entries]
    assert "First entry title -- FALSIFIED" in titles
    assert all("not an entry" not in e.body for e in entries)


def test_split_entries_captures_title_and_body():
    entries = split_entries(SAMPLE)
    first = entries[0]
    assert first.title == "First entry title -- FALSIFIED"
    assert "Rejection scope" in first.body
    assert "concept-intake-entry" in first.body


def test_split_entries_excludes_domain_level_and_audit_sections():
    entries = split_entries(SAMPLE)
    titles = [e.title for e in entries]
    assert "A domain rollup that must be excluded" not in titles
    assert "Not a candidate either" not in titles


def test_split_entries_includes_queryable_index_section():
    entries = split_entries(SAMPLE)
    titles = [e.title for e in entries]
    assert "Third entry title -- from the index section" in titles


def test_split_entries_assigns_stable_source_refs_across_included_sections_only():
    entries = split_entries(SAMPLE)
    # 3 included entries total (Entries x2 + Queryable index x1); excluded
    # sections never consume a source_ref, so numbering has no gaps.
    assert [e.source_ref for e in entries] == ["entry-1", "entry-2", "entry-3"]


def test_split_entries_last_entry_in_a_section_runs_to_next_section_boundary():
    entries = split_entries(SAMPLE)
    first = entries[0]
    assert "Second entry title" not in first.body


def test_split_entries_empty_text_returns_empty_list():
    assert split_entries("# Rejected portfolio candidates\n\nNo entries here.") == []


def test_load_entries_reads_real_file(tmp_path):
    p = tmp_path / "rejected.md"
    p.write_text(SAMPLE, encoding="utf-8")
    entries = load_entries(p)
    assert len(entries) == 3
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_mechanism_prior_extract.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'lab.research_utils.mechanism_prior_extract'`

- [ ] **Step 3: Write the implementation**

```python
# lab/research_utils/mechanism_prior_extract.py
"""Split docs/rejected_candidates.md into individually-taggable entries.

The file is organized into several `##` sections. Most contain individual
per-candidate closure records (in a shared prose-field shape); two are
DOMAIN-LEVEL rollups (a whole research theme closed or bar-raised,
spanning many instruments as one record) rather than per-candidate
entries, and are excluded by name -- see the Rule-0 note in Task 6 of the
implementation plan for the verified current section list and why a
denylist (not an allowlist) is used. This module does no classification --
only splitting and locating -- see mechanism_prior_ingest.py and Task 7 of
the implementation plan for the LLM tagging step that consumes this output.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

SECTION_HEADING_RE = re.compile(r"^## (.+)$", re.MULTILINE)
ENTRY_HEADING_RE = re.compile(r"^### (.+)$", re.MULTILINE)

# Domain-level rollups and meta/process sections are NOT per-candidate
# entries. Denylist, not allowlist, so a future new per-candidate section
# (e.g. "Harness-fed rejections" once populated) is picked up automatically.
EXCLUDED_SECTIONS = {
    "Domain-level SNAG closures",
    "Domain-level tail-exhaustion raised bars",
    "Audit hooks",
}


@dataclass(frozen=True)
class RawEntry:
    title: str
    body: str
    source_ref: str  # e.g. "entry-1" -- stable, order-based identifier


def split_entries(markdown_text: str) -> list[RawEntry]:
    """Return one RawEntry per `### ` heading, across every `##` section
    except EXCLUDED_SECTIONS.

    Text before the first `## ` section (front-matter, registry preamble)
    is never treated as an entry. source_ref numbering is continuous
    across included sections only -- an excluded section never consumes
    a number, so there are no gaps.
    """
    sections = [(m.start(), m.group(1).strip()) for m in SECTION_HEADING_RE.finditer(markdown_text)]
    sections.append((len(markdown_text), None))  # sentinel end boundary

    entries: list[RawEntry] = []
    counter = 0
    for (start, name), (end, _) in zip(sections, sections[1:]):
        if name in EXCLUDED_SECTIONS:
            continue
        section_text = markdown_text[start:end]
        headings = list(ENTRY_HEADING_RE.finditer(section_text))
        for i, match in enumerate(headings):
            counter += 1
            title = match.group(1).strip()
            body_start = match.end()
            body_end = headings[i + 1].start() if i + 1 < len(headings) else len(section_text)
            body = section_text[body_start:body_end].strip()
            entries.append(RawEntry(title=title, body=body, source_ref=f"entry-{counter}"))
    return entries


def load_entries(path: Path) -> list[RawEntry]:
    return split_entries(path.read_text(encoding="utf-8"))
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_mechanism_prior_extract.py -v`
Expected: 8 passed

- [ ] **Step 5: Commit**

```bash
git add lab/research_utils/mechanism_prior_extract.py tests/test_mechanism_prior_extract.py
git commit -m "feat(research_utils): split rejected_candidates.md into taggable entries"
```

---

### Task 7: Run the one-time tagging pass over real history

This task has no unit tests of its own — Tasks 1–6 already cover every piece of code it calls. Its own "test" is the reconciliation check in Step 5: every historical entry produces exactly one accepted tag record.

**Files:**
- No new source files. Uses Tasks 1–6 plus one Workflow script (given in full below, saved as a scratch file, not committed to the repo).
- Populates: `lab/research_utils/mechanism_prior_tags.json` (117 + 15 = 132 records expected).

- [ ] **Step 1: Build the raw-entries batch**

Run this from the repo root (adjust the scratch path if your environment's temp directory differs):

```python
# scratch: build_entries.py -- not committed, delete after Task 7 completes
import json
from pathlib import Path

from lab.research_utils.mechanism_prior_extract import load_entries

entries = load_entries(Path("docs/rejected_candidates.md"))

manifest_entries = []
for p in sorted(Path("discovery_manifests").glob("*.json")):
    data = json.loads(p.read_text(encoding="utf-8"))
    manifest_entries.append({
        "title": data.get("hypothesis", p.stem),
        "body": json.dumps(data, indent=2),
        "source_ref": f"manifest:{p.name}",
    })

all_entries = (
    [{"title": e.title, "body": e.body, "source_ref": e.source_ref} for e in entries]
    + manifest_entries
)
Path("mechanism_prior_entries.json").write_text(json.dumps(all_entries), encoding="utf-8")
print(f"wrote {len(all_entries)} entries to mechanism_prior_entries.json")
```

Run: `python build_entries.py`
Expected: `wrote 132 entries to mechanism_prior_entries.json` (117 from `rejected_candidates.md` + 15 from `discovery_manifests/`; if the real count differs when this task is actually run, that's expected — the corpus grows over time — just carry the real number into Step 5's reconciliation check instead of 132).

- [ ] **Step 2: Run the tagging Workflow**

Call the `Workflow` tool with this script, passing `mechanism_prior_entries.json`'s contents (parsed) as `args`:

```javascript
export const meta = {
  name: 'mechanism-prior-tagging-pass',
  description: 'One-time LLM-assisted tagging pass over closed-campaign history for the cross-campaign mechanism prior',
  phases: [{ title: 'Tag' }],
}

const CANDIDATE_TIERS = 'A (fund-first, low-frequency, large-per-event-delta, futures-native) / B (conditional -- announcement/auction drift, seasonality, index-rebalance) / C (graveyard-watch -- intraday microstructure, dealer-gamma) / unclear'
const OUTCOME_DEFS = 'SURVIVED (the candidate reached deployment/authorization) / KILLED_AT_ADMISSION (died at an admission/screen requirement before any statistical test of the mechanism itself ran) / KILLED_AT_TEST (died at explore/confirm statistical scoring) / AMBIGUOUS (genuinely unclear from the entry which of the above applies)'

const TAG_SCHEMA = {
  type: 'object',
  properties: {
    tags: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          source_ref: { type: 'string' },
          mechanism_tier: { type: 'string', enum: ['A', 'B', 'C', 'unclear'] },
          sourcing_channel_rank: { type: 'string', enum: ['1', '2', '3', '4', '5', '6', '1-tie', 'n/a'] },
          target_instrument_family: { type: 'string' },
          outcome: { type: 'string', enum: ['SURVIVED', 'KILLED_AT_ADMISSION', 'KILLED_AT_TEST', 'AMBIGUOUS'] },
          reasoning: { type: 'string', description: 'one sentence: which part of the entry text supports this classification' },
        },
        required: ['source_ref', 'mechanism_tier', 'sourcing_channel_rank', 'target_instrument_family', 'outcome', 'reasoning'],
      },
    },
  },
  required: ['tags'],
}

function chunk(items, size) {
  const out = []
  for (let i = 0; i < items.length; i += size) out.push(items.slice(i, i + size))
  return out
}

phase('Tag')
const batches = chunk(args.entries, 15)
log(`Tagging ${args.entries.length} historical entries in ${batches.length} batches of up to 15.`)

const results = await parallel(
  batches.map((batch, i) => () => agent(
    `You are classifying ALREADY-CLOSED, already-verdicted historical strategy-research entries for a cross-campaign prior. You are NOT judging anything live or in-flight -- every entry below already has a final, settled outcome; your job is only to describe it consistently, using the fixed vocabulary given. If an entry carries a <!-- concept-intake-entry ... --> comment, treat its attributes as a hint to weigh, not an answer to copy verbatim -- its instrument/class vocabulary is inconsistent across the corpus.\n\nMechanism tiers: ${CANDIDATE_TIERS}\nOutcome categories: ${OUTCOME_DEFS}\nsourcing_channel_rank: 1=citation-graph traversal, 2=survey/replication meta-studies, 3=futures-native journals, 4=CFTC positioning data, 5=strategy encyclopedias, 6=practitioner blogs, 1-tie=structural flow census, n/a=mechanically mined (not harvested from a published source).\n\nFor each entry below, return one tag object with your classification and a one-sentence reasoning citing the specific text that supports it. If the entry's own text is genuinely ambiguous on any field, use "unclear" (mechanism_tier) or "AMBIGUOUS" (outcome) rather than guessing.\n\nEntries:\n${batch.map((e) => `--- ${e.source_ref} ---\nTitle: ${e.title}\n${e.body}`).join('\n\n')}`,
    { label: `tag-batch-${i}`, phase: 'Tag', schema: TAG_SCHEMA }
  ))
)

const allTags = results.filter(Boolean).flatMap((r) => r.tags)
log(`Tagged ${allTags.length} of ${args.entries.length} entries.`)
return { tags: allTags, total_entries: args.entries.length }
```

- [ ] **Step 3: Convert the Workflow's output into proposed tag records**

The Workflow's `tags` array is missing `provenance` (it only knows `source_ref`, not the full record shape Task 1's schema requires). Convert it:

```python
# scratch: convert_tags.py -- not committed, delete after Task 7 completes
import json
from datetime import date, timezone, datetime
from pathlib import Path

entries_by_ref = {e["source_ref"]: e for e in json.loads(Path("mechanism_prior_entries.json").read_text())}
raw_tags = json.loads(Path("mechanism_prior_workflow_result.json").read_text())["tags"]  # paste the Workflow's returned `tags` array here

proposed = []
for tag in raw_tags:
    ref = tag["source_ref"]
    source_path = (
        f"discovery_manifests/{ref.split('manifest:')[1]}"
        if ref.startswith("manifest:")
        else "docs/rejected_candidates.md"
    )
    proposed.append({
        "mechanism_tier": tag["mechanism_tier"],
        "sourcing_channel_rank": tag["sourcing_channel_rank"],
        "target_instrument_family": tag["target_instrument_family"],
        "outcome": tag["outcome"],
        "provenance": {
            "source_path": source_path,
            "source_ref": ref,
            "tagged_at": date.today().isoformat(),
            "reasoning": tag["reasoning"],
        },
    })

with open("mechanism_prior_proposed.jsonl", "w", encoding="utf-8") as f:
    for p in proposed:
        f.write(json.dumps(p) + "\n")
print(f"wrote {len(proposed)} proposed records")
```

Run: `python convert_tags.py`

- [ ] **Step 4: Ingest the proposed batch**

Run: `python lab/research_utils/mechanism_prior_ingest.py mechanism_prior_proposed.jsonl`
Expected: `appended <N> records to lab/research_utils/mechanism_prior_tags.json`

If this instead prints `batch rejected` with a list of `record N (source_ref): reason` lines, the Workflow produced a record outside the enum vocabulary (schema-constrained structured output makes this unlikely, but not impossible if a batch's `args` got malformed). Fix the specific bad line(s) in `mechanism_prior_proposed.jsonl` by hand and re-run — do not weaken the ingest validator to make a bad record pass.

- [ ] **Step 5: Reconcile — every entry produced exactly one accepted tag**

```bash
python -c "
import json
from pathlib import Path
from lab.research_utils.mechanism_prior_store import load_all_records

entries = json.loads(Path('mechanism_prior_entries.json').read_text())
tagged_refs = {r['provenance']['source_ref'] for r in load_all_records()}
missing = [e['source_ref'] for e in entries if e['source_ref'] not in tagged_refs]
print(f'{len(entries)} entries, {len(tagged_refs)} tagged, {len(missing)} missing')
if missing:
    print('missing:', missing)
"
```

Expected: `<N> entries, <N> tagged, 0 missing` where both counts match. If `missing` is non-empty, re-run Step 2's Workflow for just those `source_ref`s (pass a filtered `args.entries`) and repeat Steps 3–5.

- [ ] **Step 6: Delete scratch files, commit the populated store**

```bash
rm -f build_entries.py convert_tags.py mechanism_prior_entries.json mechanism_prior_workflow_result.json mechanism_prior_proposed.jsonl
git add lab/research_utils/mechanism_prior_tags.json
git commit -m "data(research_utils): one-time tagging pass over closed-campaign history"
```

---

## Phase 4: First real report

### Task 8: Generate and sanity-check the first real report

**Files:**
- Modify: none (all code already exists from Tasks 1–7).

- [ ] **Step 1: Generate the report**

Run: `python lab/research_utils/mechanism_prior.py --out lab/research_utils/mechanism_prior_report.md`

- [ ] **Step 2: Sanity-check the output by hand**

Open `lab/research_utils/mechanism_prior_report.md` and verify:
- The entry count in the header matches Task 7 Step 5's reconciled total.
- Every data row has a bracketed `[lo, hi]` interval — grep for any row missing one: `grep -E "^\| [^|]+ \| [0-9]+/[0-9]+ \|" lab/research_utils/mechanism_prior_report.md | grep -v "\["` should print nothing.
- At least one `mechanism_tier` cell has single-digit N with a visibly wide interval (the small-N-honesty property working as designed, not a bug).

- [ ] **Step 3: Commit the first report**

```bash
git add lab/research_utils/mechanism_prior_report.md
git commit -m "docs(research_utils): first generated cross-campaign mechanism prior report"
```

- [ ] **Step 4: Done — hand back to the design spec's consumption model**

Per the design spec §4/§5, this report is read by a human (or a future GENERATE-stage scoping session) before deciding what to source next. Nothing in this pipeline automatically re-reads it — regenerating it (Task 8 Step 1) after future closures get tagged (a manual step at each closure, per Global Constraints) is the standing operating procedure, not a new automation this plan builds.
