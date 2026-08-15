"""Regression tests for strict numeric and JSON state boundaries."""

import json

import pytest

from lib.validation import dump_strict_json, load_strict_json, require_finite_number


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_require_finite_number_rejects_non_finite_values(value):
    with pytest.raises(ValueError, match="must be finite"):
        require_finite_number(value, field="equity")


def test_require_finite_number_rejects_boolean():
    with pytest.raises(ValueError, match="must be a number"):
        require_finite_number(True, field="equity")


@pytest.mark.parametrize("token", ["NaN", "Infinity", "-Infinity"])
def test_load_strict_json_rejects_non_standard_constants(tmp_path, token):
    path = tmp_path / "state.json"
    path.write_text(f'{{"equity": {token}}}', encoding="utf-8")

    with pytest.raises(ValueError, match="not strict JSON"):
        load_strict_json(path)


def test_dump_strict_json_rejects_non_finite_values():
    with pytest.raises(ValueError, match="non-JSON value"):
        dump_strict_json({"equity": float("nan")})


def test_strict_json_round_trip(tmp_path):
    state = {"equity": 200_000.0, "history": []}
    path = tmp_path / "state.json"
    path.write_text(dump_strict_json(state), encoding="utf-8")

    assert load_strict_json(path) == json.loads(path.read_text(encoding="utf-8"))
