"""Contract tests for the qualification child's local hang-bound override."""

import pytest


def _timeout(record_property):
    # Import only the helper: importing the bridge test would collect it here.
    from test_qualification_isolation import qualification_child_timeout

    return qualification_child_timeout(record_property)


@pytest.mark.parametrize("raw, expected, overridden", [
    (None, 3600, False),
    ("3600", 3600, True),
    ("7200", 7200, True),
    ("14400", 14400, True),
])
def test_timeout_value_and_recorded_source(monkeypatch, raw, expected, overridden):
    if raw is None:
        monkeypatch.delenv("FP_QUALIFICATION_CHILD_TIMEOUT_S", raising=False)
    else:
        monkeypatch.setenv("FP_QUALIFICATION_CHILD_TIMEOUT_S", raw)
    properties = []

    actual = _timeout(lambda name, value: properties.append((name, value)))

    assert actual == expected
    assert properties == [
        ("qualification_child_timeout_s", expected),
        ("qualification_child_timeout_overridden", overridden),
    ]


@pytest.mark.parametrize("raw", ["3599", "14401", "abc", "", "1e4"])
def test_invalid_timeout_refuses_without_recording_a_value(monkeypatch, raw):
    monkeypatch.setenv("FP_QUALIFICATION_CHILD_TIMEOUT_S", raw)
    properties = []

    with pytest.raises(pytest.fail.Exception, match="FP_QUALIFICATION_CHILD_TIMEOUT_S"):
        _timeout(lambda name, value: properties.append((name, value)))

    assert properties == []
