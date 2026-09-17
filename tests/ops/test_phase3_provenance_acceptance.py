"""Independent source identity vectors; synthetic bytes, no qualification draws."""
from dataclasses import replace
from datetime import date, datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import py_compile
from types import SimpleNamespace

import pytest

from c1_signal_daemon import book_adapters


def _digest(data):
    return hashlib.sha256(data).hexdigest()


def _port(tmp_path, monkeypatch, *, value="NEW", suffix=""):
    leg_id = "dj30_mym_p250"
    original = book_adapters.ADAPTER_BY_LEG[leg_id]
    source = (
        f"LEG_ID = {leg_id!r}\n"
        f"PINE_SHA256 = {original.pine_sha256!r}\n"
        f"VALUE = {value!r}\n" + suffix
    ).encode()
    path = tmp_path / f"{original.module}.py"
    path.write_bytes(source)
    monkeypatch.setenv("FP_PORT_ROOT", str(tmp_path))
    monkeypatch.setitem(book_adapters.ADAPTER_BY_LEG, leg_id,
                        replace(original, runtime_sha256=_digest(source)))
    return leg_id, path, source


def test_unaccepted_port_bytes_are_refused_before_execution(tmp_path, monkeypatch):
    marker = tmp_path / "executed.txt"
    leg_id, path, accepted = _port(tmp_path, monkeypatch)
    path.write_bytes(accepted +
                     f"from pathlib import Path\nPath({str(marker)!r}).write_text('ran')\n".encode())

    with pytest.raises(ValueError):
        book_adapters.load_port(leg_id)

    assert not marker.exists(), "unaccepted source executed before its digest refusal"


def test_accepted_source_cannot_execute_stale_timestamp_pyc(tmp_path, monkeypatch):
    leg_id, path, accepted = _port(tmp_path, monkeypatch, value="NEW")
    old = accepted.replace(b"'NEW'", b"'OLD'")
    assert len(old) == len(accepted)
    path.write_bytes(old)
    py_compile.compile(str(path), doraise=True,
                       invalidation_mode=py_compile.PycInvalidationMode.TIMESTAMP)
    previous = path.stat()
    path.write_bytes(accepted)
    os.utime(path, ns=(previous.st_atime_ns, previous.st_mtime_ns))

    loaded = book_adapters.load_port(leg_id)

    assert loaded.VALUE == "NEW", "loader hashed accepted source but executed stale cached code"


def test_effective_inputs_are_parsed_from_the_verified_bytes(tmp_path, monkeypatch):
    path = tmp_path / "effective_inputs.json"
    accepted = {"_note": "synthetic source identity fixture"}
    for row in book_adapters.ADAPTERS:
        accepted[row.leg_id] = {
            "adapter": {"sentinel": "accepted"}, "emulator": {}, "qty_scale": 1,
        }
    accepted_bytes = json.dumps(accepted).encode()
    changed = json.loads(accepted_bytes)
    for row in book_adapters.ADAPTERS:
        changed[row.leg_id]["adapter"]["sentinel"] = "changed"
    changed_bytes = json.dumps(changed).encode()
    path.write_bytes(accepted_bytes)
    monkeypatch.setenv("FP_PORT_ROOT", str(tmp_path))
    monkeypatch.setattr(book_adapters, "EFFECTIVE_INPUTS_SHA256", _digest(accepted_bytes))

    original_read = Path.read_bytes

    def read_then_change(source):
        data = original_read(source)
        if source == path:
            source.write_bytes(changed_bytes)
        return data

    monkeypatch.setattr(Path, "read_bytes", read_then_change)
    monkeypatch.setattr(book_adapters, "load_port", lambda leg_id: SimpleNamespace(
        build=lambda **values: SimpleNamespace(leg_id=leg_id, **values)))

    runtime_values = json.loads(accepted_bytes)
    runtime_values["orb_mnq_v7"]["adapter"]["qty"] = 1
    runtime_bytes = json.dumps(
        runtime_values, sort_keys=True, separators=(",", ":"), allow_nan=False,
    ).encode()
    monkeypatch.setattr(
        book_adapters, "RUNTIME_EFFECTIVE_INPUTS_SHA256", _digest(runtime_bytes))

    loaded = book_adapters.load_book_adapters()

    assert all(adapter.sentinel == "accepted" for adapter in loaded.values()), (
        "effective inputs were reread after verification; the receipt names different bytes"
    )


def _source_session():
    from c1_rail.qualification.model import LEG_IDS, SessionSchedule, SourceBar, SourceSession
    from c1_signal_daemon.feed import Bar

    source_time = datetime(2026, 9, 15, 19, 30, tzinfo=timezone.utc)
    bars = tuple((leg_id, Bar(source_time, 100, 101, 99, 100, 1)) for leg_id in LEG_IDS)
    schedule = SessionSchedule(source_time + timedelta(minutes=15),
                               source_time + timedelta(minutes=25),
                               source_time + timedelta(minutes=30))
    return SourceSession("source:2026-09-15", date(2026, 9, 15),
                         (SourceBar(source_time, bars),), schedule)


@pytest.mark.parametrize("field", ["positions", "working_orders", "reservations"])
@pytest.mark.parametrize("defect", ["missing", "duplicate", "negative", "boolean"])
def test_joint_flat_proof_rejects_incomplete_or_non_gross_counts(field, defect):
    from c1_rail.qualification.model import EdgeState, LEG_IDS

    zeros = tuple((leg_id, 0) for leg_id in LEG_IDS)
    values = {name: zeros for name in ("positions", "working_orders", "reservations")}
    if defect == "missing":
        values[field] = zeros[:-1]
    elif defect == "duplicate":
        values[field] = zeros[:-1] + zeros[:1]
    else:
        values[field] = ((LEG_IDS[0], -1 if defect == "negative" else False),) + zeros[1:]
    with pytest.raises(ValueError):
        EdgeState(**values)


@pytest.mark.parametrize("field", ["positions", "working_orders", "reservations"])
def test_joint_flat_requires_all_three_categories_to_be_zero(field):
    from c1_rail.qualification.model import EdgeState, LEG_IDS

    zeros = tuple((leg_id, 0) for leg_id in LEG_IDS)
    values = {name: zeros for name in ("positions", "working_orders", "reservations")}
    values[field] = zeros[:-1] + ((LEG_IDS[-1], 1),)
    assert not EdgeState(**values).is_flat


def test_source_schedule_cannot_be_borrowed_from_another_session():
    source = _source_session()
    foreign = replace(source.schedule,
                      cutoff=source.schedule.cutoff + timedelta(days=1),
                      flatten_start=source.schedule.flatten_start + timedelta(days=1),
                      own_flat_deadline=source.schedule.own_flat_deadline + timedelta(days=1))
    with pytest.raises(ValueError):
        replace(source, schedule=foreign)


def test_path_mapping_preserves_source_identity_and_immutable_bar_collection():
    from c1_rail.qualification.model import ET, PathBar, PathSession

    source = _source_session()
    original = source.bars[0]
    mapped = PathBar(datetime(2030, 1, 1, tzinfo=timezone.utc),
                     original.source_bar_time, source.source_session_date,
                     original.source_bar_time.astimezone(ET), original.bars)
    accepted = PathSession(0, date(2030, 1, 1), source, (mapped,), True, True)
    assert accepted.bars[0].source_bar_time == original.source_bar_time
    assert accepted.bars[0].path_time != original.source_bar_time
    with pytest.raises(ValueError):
        replace(accepted, bars=[mapped])


def test_path_mapping_rejects_relabelled_source_date():
    from c1_rail.qualification.model import ET, PathBar, PathSession

    source = _source_session()
    original = source.bars[0]
    mapped = PathBar(datetime(2030, 1, 1, tzinfo=timezone.utc),
                     original.source_bar_time, source.source_session_date + timedelta(days=1),
                     original.source_bar_time.astimezone(ET), original.bars)
    with pytest.raises(ValueError):
        PathSession(0, date(2030, 1, 1), source, (mapped,), True, True)


def test_outcome_diagnostics_cannot_mutate_after_construction():
    from c1_rail.qualification.model import PathOutcome

    with pytest.raises(ValueError):
        PathOutcome("PASS", 1, None, (["stage", "n2"],))


@pytest.mark.parametrize("status", ["FAILURE", "UNRESOLVED"])
def test_nonpass_cannot_supply_finite_pass_time(status):
    from c1_rail.qualification.model import PathOutcome

    with pytest.raises(ValueError):
        PathOutcome(status, 1, "not passed", ())


@pytest.mark.parametrize("mutation", ["verdict", "completion", "canonical_bytes", "stage_digest"])
def test_result_authentication_rejects_receipt_fields_changed_after_validation(mutation, monkeypatch):
    """A real signature over an envelope cannot authenticate altered receipt fields."""
    import importlib.util
    from c1_rail.qualification import seal

    root = Path(seal.__file__).resolve().parents[3]
    helper_path = root / "tests/ops/qualification/test_seal.py"
    monkeypatch.syspath_prepend(str(helper_path.parent))
    spec = importlib.util.spec_from_file_location("independent_seal_fixture", helper_path)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    result = helper.validate(helper.result_case())
    fixture = helper.context(result)
    domain = fixture.domain
    private = fixture.private_keys["test-producer"]
    attestation = helper.signed_record(
        result, private, schema="qualification_result_authentication/v1",
        scope="ATTEST_E1_RESULT", subject=result.result_sha256, authority="test-producer")
    keys = {"test-producer": helper.key(private, "test-producer", "TEST_ONLY", "ATTEST_E1_RESULT")}
    seal.authenticate_result(result, attestation, trusted_keys=keys, now=helper.NOW, trust_domain=domain)
    changes = {
        "verdict": {"verdict": "FAIL"},
        "completion": {"completion": "PARTIAL"},
        "canonical_bytes": {"canonical_bytes": b"{}"},
        "stage_digest": {"stage_output_sha256": {**result.stage_output_sha256, "PART_A": "f" * 64}},
    }
    altered = replace(result, **changes[mutation])
    with pytest.raises(seal.ResultValidationError):
        seal.authenticate_result(altered, attestation, trusted_keys=keys, now=helper.NOW, trust_domain=domain)


def _exact_binomial_cdf(n, count, probability):
    from fractions import Fraction
    from math import comb
    return sum((Fraction(comb(n, k)) * probability**k * (1 - probability)**(n-k)
                for k in range(count + 1)), Fraction(0))


def _statistical_case(n=100):
    from decimal import Decimal
    from c1_rail.qualification.model import PathOutcome
    passed = PathOutcome("PASS", 200, None, ())
    rows = (passed,) * n
    rules = SimpleNamespace(failure_ceiling=Decimal(".05"), alpha=Decimal(".05"),
                            speed_target=Decimal(".5"), speed_horizon_sessions=200)
    contract = SimpleNamespace(replay=SimpleNamespace(decision_rules=rules))
    outcomes = {"LEGALITY": {}, "N1": {p: rows for p in ("FULL", "H1", "H2")},
                "N2": {"FULL": rows}, "PART_B": {"H1": rows, "H2": rows}}
    return contract, outcomes


@pytest.mark.parametrize("population", ["FULL", "H1", "H2"])
@pytest.mark.parametrize("adjacent", [0, 1])
def test_confirmation_failure_boundary_matches_exact_rational_oracle(population, adjacent):
    from fractions import Fraction
    from c1_rail.qualification.model import PathOutcome
    from c1_rail.qualification.result_adjudication import adjudicate_e1_outcomes
    contract, outcomes = _statistical_case()
    cutoff = max(k for k in range(101)
                 if _exact_binomial_cdf(100, k, Fraction(1, 20)) <= Fraction(1, 20))
    count = cutoff + adjacent
    stage = "N2" if population == "FULL" else "PART_B"
    outcomes[stage][population] = ((PathOutcome("UNRESOLVED", None, "horizon_cap", ()),) * count
                                   + outcomes[stage][population][count:])
    decisions = adjudicate_e1_outcomes(contract, outcomes, {"records": []})
    assert decisions[stage] == ("PASS" if adjacent == 0 else "FAIL")


@pytest.mark.parametrize("below", [0, 1])
def test_speed_boundary_uses_all_paths_and_inclusive_day_200(below):
    from fractions import Fraction
    from c1_rail.qualification.model import PathOutcome
    from c1_rail.qualification.result_adjudication import adjudicate_e1_outcomes
    n = 101
    contract, outcomes = _statistical_case(n)
    minimum = min(k for k in range(n + 1)
                  if 1 - _exact_binomial_cdf(n, k - 1, Fraction(1, 2)) <= Fraction(1, 20))
    dropped_failure_minimum = min(k for k in range(n)
        if 1 - _exact_binomial_cdf(n - 1, k - 1, Fraction(1, 2)) <= Fraction(1, 20))
    assert minimum == dropped_failure_minimum + 1, "fixture must detect denominator shrinkage"
    fast = minimum - below
    outcomes["N2"]["FULL"] = ((PathOutcome("PASS", 200, None, ()),) * fast
                                + (PathOutcome("PASS", 201, None, ()),) * (n-1-fast)
                                + (PathOutcome("FAILURE", None, "bust_trailing", ()),))
    decisions = adjudicate_e1_outcomes(contract, outcomes, {"records": []})
    assert decisions["N2"] == ("PASS" if below == 0 else "FAIL")


@pytest.mark.parametrize("boundary", ["claim", "seal"])
@pytest.mark.parametrize("field", ["verdict", "completion", "canonical_bytes", "stage_output_sha256"])
def test_authenticated_consumers_recheck_canonical_receipt_fields(boundary, field, monkeypatch):
    """Exercise field binding independently of rejecting a replacement object."""
    import importlib.util
    from c1_rail.qualification import seal
    from c1_rail.qualification.attempt import AttemptStore

    root = Path(seal.__file__).resolve().parents[3]
    helper_path = root / "tests/ops/qualification/test_seal.py"
    monkeypatch.syspath_prepend(str(helper_path.parent))
    spec = importlib.util.spec_from_file_location(
        "independent_consumer_fixture", helper_path)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    result = helper.validate(helper.result_case())
    fixture = helper.context(result)
    domain = fixture.domain
    private = fixture.private_keys["test-producer"]
    attestation = helper.signed_record(result, private, schema="qualification_result_authentication/v1",
        scope="ATTEST_E1_RESULT", subject=result.result_sha256, authority="test-producer")
    keys = {"test-producer": helper.key(private, "test-producer", "TEST_ONLY", "ATTEST_E1_RESULT")}
    authenticated = seal.authenticate_result(result, attestation, trusted_keys=keys, now=helper.NOW, trust_domain=domain)
    store = AttemptStore(Path(result.attempt_journal_path), result.attempt_id,
                         result.contract_sha256, "boot-1", domain.sha256)
    seal.commit_authenticated_result(store, authenticated, trusted_keys=keys, now=helper.NOW, trust_domain=domain)
    signing_key = fixture.private_keys["test-seal"]
    record = helper.signed_record(result, signing_key, schema="e1_qualification_seal/v1",
        scope="SEAL_E1_PASS", subject=_digest(seal.e1_seal_payload(authenticated, sealed_utc=helper.NOW)),
        authority="test-seal")
    seal_keys = {"test-seal": helper.key(signing_key, "test-seal", "TEST_ONLY", "SEAL_E1_PASS")}

    def consume():
        if boundary == "claim":
            return seal.authenticated_result_claim(authenticated, trusted_keys=keys, now=helper.NOW, trust_domain=domain)
        return seal.seal_e1_pass(authenticated, record, sealed_utc=helper.NOW,
            trusted_keys=seal_keys, now=helper.NOW, result_trusted_keys=keys, attempt_store=store,
            trust_domain=domain)

    consume()  # A valid unchanged committed result reaches this exact boundary.
    changed = {"verdict": "FAIL", "completion": "PARTIAL", "canonical_bytes": b"{}",
               "stage_output_sha256": {**result.stage_output_sha256, "PART_A": "f" * 64}}
    previous = getattr(result, field)
    try:
        object.__setattr__(result, field, changed[field])
        with pytest.raises(seal.ResultValidationError, match="canonical|receipt"):
            consume()
    finally:
        object.__setattr__(result, field, previous)
