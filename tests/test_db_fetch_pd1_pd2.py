"""Tests for db_fetch.py PD-1 / PD-2 hygiene fixes, caught live during the
DISC-CAMP-0 first real Databento pull (docs/SESSIONS.md 2026-07-13 entry;
docs/ltm/briefs/pre-registration/DISC-CAMP-0-preregistration.md §5):

  PD-1 -- `estimate()` fetches and prints the dataset's available range but
    never compares the requested --start/--end against it, so a request
    outside the available window sails through to `client.metadata.get_cost`,
    which raises a raw `BentoClientError: 422 data_start_before_available_start`
    buried inside a metadata call instead of a clear, actionable message.

  PD-2 -- `pull()`'s `data.to_file(path)` writes directly to the FINAL cache
    path. A crash/interrupt mid-write can leave a partial/corrupt file at that
    exact path; the next invocation's `path.exists()` check then treats the
    corrupt file as a cache hit, silently serving bad data (no re-billing,
    but no correctness either).

Pure offline tests: `client` / `metadata` / `timeseries` are fully faked, no
network, no DATABENTO_API_KEY. `importorskip` matches the sibling
tests/test_db_fetch_datecap.py posture (databento absent on ops venv / CI).
"""
from __future__ import annotations

from argparse import Namespace
from pathlib import Path

import pytest

pytest.importorskip("databento")

# Canonical lab module (lab is on pytest pythonpath); see test_db_fetch_datecap.py.
from databento_fetch import db_fetch as dfetch  # noqa: E402


def _args(**kw) -> Namespace:
    base = dict(
        symbols="GC.FUT", stype="parent", schema="ohlcv-1h",
        start="2010-06-06", end="2010-06-08",
        campaign_id=None, phase=None, is_boundary=None,
        max_cost=5.0, force=False, out=None,
    )
    base.update(kw)
    return Namespace(**base)


# ============================================================================
# Fakes -- no real databento client / network / credentials anywhere below.
# ============================================================================

class _FakeData:
    """Stand-in for the object client.timeseries.get_range() returns. `to_file`
    writes straight to WHATEVER path it's handed, mirroring the real SDK's own
    `open(path, 'wb')` behavior -- so if the caller (pre-fix) hands it the
    FINAL cache path, a simulated mid-write crash corrupts that exact path,
    exactly like a real Ctrl-C / network drop would."""

    def __init__(self, content: bytes = b"FAKE-DBN-BYTES", fail_after: int | None = None):
        self.content = content
        self.fail_after = fail_after
        self.write_calls: list[str] = []

    def to_file(self, path, *a, **kw) -> None:
        self.write_calls.append(str(path))
        if self.fail_after is not None:
            with open(path, "wb") as f:
                f.write(self.content[: self.fail_after])
            raise OSError("simulated crash mid-write")
        with open(path, "wb") as f:
            f.write(self.content)


class _FakeMetadata:
    def __init__(self, cost=0.0, size=100, count=10, rng=None, range_exc=None):
        self.cost, self.size, self.count = cost, size, count
        self.rng = rng if rng is not None else {
            "start": "2010-06-06T00:00:00.000000000Z",
            "end": "2026-07-01T00:00:00.000000000Z",
            "schema": {},
        }
        self.range_exc = range_exc
        self.calls = {"get_dataset_range": 0, "get_cost": 0,
                      "get_billable_size": 0, "get_record_count": 0}

    def get_dataset_range(self, dataset):
        self.calls["get_dataset_range"] += 1
        if self.range_exc is not None:
            raise self.range_exc
        return self.rng

    def get_cost(self, **kw):
        self.calls["get_cost"] += 1
        return self.cost

    def get_billable_size(self, **kw):
        self.calls["get_billable_size"] += 1
        return self.size

    def get_record_count(self, **kw):
        self.calls["get_record_count"] += 1
        return self.count


class _FakeTimeseries:
    def __init__(self, data_factory):
        self.data_factory = data_factory
        self.calls = 0

    def get_range(self, **kw):
        self.calls += 1
        return self.data_factory()


class _FakeClient:
    def __init__(self, metadata=None, data_factory=None):
        self.metadata = metadata or _FakeMetadata()
        self.timeseries = _FakeTimeseries(data_factory or (lambda: _FakeData()))


class _FakeStore:
    """Stand-in for db.DBNStore -- avoids needing real DBN binary bytes to
    exercise the cache-lifecycle logic in pull()."""

    def __init__(self, rows=3):
        self._rows = rows

    def to_df(self):
        return list(range(self._rows))

    def to_parquet(self, out):
        Path(out).write_bytes(b"parquet")


@pytest.fixture
def cache_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(dfetch, "CACHE_DIR", tmp_path)
    return tmp_path


# ============================================================================
# PD-2 -- atomic cache write
# ============================================================================

def test_midwrite_failure_leaves_no_file_at_final_cache_path(cache_dir, monkeypatch):
    data = _FakeData(fail_after=4)
    fake_client = _FakeClient(data_factory=lambda: data)
    monkeypatch.setattr(dfetch, "_client", lambda: fake_client)

    args = _args()
    path = dfetch._cache_path(args)

    with pytest.raises(OSError, match="simulated crash"):
        dfetch.pull(args)

    assert not path.exists(), (
        "PD-2: a mid-write crash must not leave a (partial/corrupt) file at "
        "the real cache path -- the next run's `path.exists()` cache-hit "
        "check would otherwise silently serve it."
    )
    leftovers = list(cache_dir.iterdir())
    assert leftovers == [], f"tmp file(s) not cleaned up on failure: {leftovers}"
    assert data.write_calls, "to_file() was never called"
    assert path not in {Path(p) for p in data.write_calls}, (
        "to_file() was called with the FINAL cache path directly -- write "
        "must go through a same-directory tmp path first (PD-2 unfixed)."
    )


def test_subsequent_successful_pull_produces_valid_cache_hit(cache_dir, monkeypatch):
    data = _FakeData()
    fake_client = _FakeClient(data_factory=lambda: data)
    monkeypatch.setattr(dfetch, "_client", lambda: fake_client)
    monkeypatch.setattr(dfetch.db.DBNStore, "from_file", lambda p: _FakeStore())

    args = _args()
    path = dfetch._cache_path(args)

    dfetch.pull(args)  # first: real (fake) write
    assert path.exists()
    assert path.read_bytes() == data.content

    calls_before = fake_client.timeseries.calls
    dfetch.pull(args)  # second: must be a cache hit
    assert fake_client.timeseries.calls == calls_before, (
        "a valid cached file must short-circuit to the cache-hit branch, "
        "never re-invoking client.timeseries.get_range()"
    )


def test_failure_then_retry_recovers_cleanly(cache_dir, monkeypatch):
    """A crash on attempt 1, then a clean attempt 2 for the SAME args, must
    succeed and leave a valid cache entry (no residue from attempt 1 blocks
    or corrupts attempt 2)."""
    failing_data = _FakeData(fail_after=2)
    good_data = _FakeData()
    calls = {"n": 0}

    def factory():
        calls["n"] += 1
        return failing_data if calls["n"] == 1 else good_data

    fake_client = _FakeClient(data_factory=factory)
    monkeypatch.setattr(dfetch, "_client", lambda: fake_client)
    monkeypatch.setattr(dfetch.db.DBNStore, "from_file", lambda p: _FakeStore())

    args = _args()
    path = dfetch._cache_path(args)

    with pytest.raises(OSError):
        dfetch.pull(args)
    assert not path.exists()

    dfetch.pull(args)  # retry
    assert path.exists()
    assert path.read_bytes() == good_data.content


# ============================================================================
# PD-1 -- dataset-range fail-fast pre-check
# ============================================================================

def test_range_precheck_exits_before_get_cost_when_start_before_floor(monkeypatch):
    rng = {
        "start": "2010-06-06T00:00:00.000000000Z",
        "end": "2026-07-01T00:00:00.000000000Z",
        "schema": {},
    }
    fake_meta = _FakeMetadata(rng=rng)
    monkeypatch.setattr(dfetch, "_client", lambda: _FakeClient(metadata=fake_meta))

    # Mirrors the real PD-1 catch: frozen IS start 2010-01-01 predates the
    # GLBX.MDP3 floor 2010-06-06.
    args = _args(start="2010-01-01", end="2010-06-08")

    with pytest.raises(SystemExit):
        dfetch.estimate(args)

    assert fake_meta.calls["get_cost"] == 0, "get_cost must not be reached (fail-fast)"
    assert fake_meta.calls["get_billable_size"] == 0
    assert fake_meta.calls["get_record_count"] == 0


def test_range_precheck_exits_when_end_past_ceiling(monkeypatch):
    rng = {"start": "2010-06-06", "end": "2020-01-01", "schema": {}}
    fake_meta = _FakeMetadata(rng=rng)
    monkeypatch.setattr(dfetch, "_client", lambda: _FakeClient(metadata=fake_meta))

    args = _args(start="2015-01-01", end="2025-01-01")

    with pytest.raises(SystemExit):
        dfetch.estimate(args)

    assert fake_meta.calls["get_cost"] == 0
    assert fake_meta.calls["get_billable_size"] == 0
    assert fake_meta.calls["get_record_count"] == 0


def test_range_precheck_prefers_per_schema_range_over_dataset_wide(monkeypatch):
    """The dataset-wide range covers the request, but THIS schema's own range
    (which can differ -- e.g. mbo starting later than ohlcv) does not; the
    schema-specific range must win, per the pre-registration note."""
    rng = {
        "start": "2000-01-01",
        "end": "2030-01-01",
        "schema": {"ohlcv-1h": {"start": "2015-01-01", "end": "2030-01-01"}},
    }
    fake_meta = _FakeMetadata(rng=rng)
    monkeypatch.setattr(dfetch, "_client", lambda: _FakeClient(metadata=fake_meta))

    args = _args(schema="ohlcv-1h", start="2010-06-06", end="2010-06-08")

    with pytest.raises(SystemExit):
        dfetch.estimate(args)

    assert fake_meta.calls["get_cost"] == 0


def test_range_precheck_passes_through_when_request_is_covered(monkeypatch):
    rng = {
        "start": "2010-06-06", "end": "2026-07-01",
        "schema": {"ohlcv-1h": {"start": "2010-06-06", "end": "2026-07-01"}},
    }
    fake_meta = _FakeMetadata(rng=rng, cost=1.23, size=555, count=77)
    monkeypatch.setattr(dfetch, "_client", lambda: _FakeClient(metadata=fake_meta))

    args = _args(schema="ohlcv-1h", start="2011-01-01", end="2012-01-01")

    cost = dfetch.estimate(args)  # must NOT raise

    assert cost == 1.23
    assert fake_meta.calls["get_cost"] == 1
    assert fake_meta.calls["get_billable_size"] == 1
    assert fake_meta.calls["get_record_count"] == 1


def test_range_precheck_skipped_when_get_dataset_range_raises(monkeypatch):
    """Existing non-fatal handling of a get_dataset_range failure is
    untouched: the pre-check must not run (and must not block) when the
    range fetch itself failed."""
    fake_meta = _FakeMetadata(range_exc=RuntimeError("network blip"))
    monkeypatch.setattr(dfetch, "_client", lambda: _FakeClient(metadata=fake_meta))

    # This window WOULD fail the pre-check if it ran -- proves the skip, not
    # just a lucky pass-through.
    args = _args(start="2010-01-01", end="2010-06-08")

    cost = dfetch.estimate(args)  # must NOT raise/exit

    assert cost == 0.0
    assert fake_meta.calls["get_cost"] == 1
    assert fake_meta.calls["get_billable_size"] == 1
    assert fake_meta.calls["get_record_count"] == 1
