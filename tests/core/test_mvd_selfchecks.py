"""MVD self-check confirmation.

dd_protection._validate_protection_rule() runs at module import. If the
boundary check fails or the spec pin literal drifts past DD_TRIGGER=0.015 /
DD_SCALE=0.40, the import raises AssertionError. This test makes the
import-time guard visible at the test layer so it cannot be silently disabled.

Constants relocked 2026-05-08 from C0 (0.010, 0.40) to C2 (0.015, 0.40)
after bust_attribution_flip closed broker-feed-confirmed; see Q-DDP-1
recommendation.md OVERRIDE section.
"""
import pytest


def test_dd_protection_self_check_passes_at_import():
    import dd_protection

    assert callable(dd_protection._validate_protection_rule)
    # Spec-pinned constants — duplicated here so a constant drift fails this
    # test even if the spec pin in dd_protection.py is also drifted.
    assert dd_protection.DD_TRIGGER == 0.015
    assert dd_protection.DD_SCALE == 0.40


# ----------------------------------------------------------------------
# lib.mvd assert-helper coverage (added 2026-06-24).
# The Family-2/4/5 helpers below are a documented public MVD-discipline API
# (docs/adr/2026-04-24-mvd-discipline.md + docs/templates/*) prescribed for
# future calibration / lock-decision scripts. They had no live caller and no
# coverage; these self-checks lock the API so a behavior change can't land
# silently (the rationale for keeping rather than deleting them).
# ----------------------------------------------------------------------

def test_mvd_identity_asserts_pass_on_match_and_raise_on_mismatch():
    from lib.mvd import assert_symbol, assert_broker, assert_version

    # Equal -> no raise (returns None).
    assert assert_symbol("USDJPY", "USDJPY") is None
    assert assert_broker("Pepperstone", "Pepperstone") is None
    assert assert_version("v5.5", "v5.5") is None

    # Unequal -> AssertionError (the USDJPY-vs-USDJPY_X / panel-source mislabel class).
    with pytest.raises(AssertionError):
        assert_symbol("USDJPY", "USDJPY_X")
    with pytest.raises(AssertionError):
        assert_broker("Pepperstone", "OANDA")
    with pytest.raises(AssertionError):
        assert_version("v5.4", "v5.5")


def test_mvd_assert_reconciled_tolerance_and_zero_expected():
    from lib.mvd import assert_reconciled

    assert_reconciled(104.0, 100.0, 0.05)          # 4% gap < 5% tol -> OK
    with pytest.raises(AssertionError):
        assert_reconciled(106.0, 100.0, 0.05)      # 6% gap > 5% tol -> fail
    assert_reconciled(0.0, 0.0, 0.05)              # expected==0 branch, gap=0 -> OK
    with pytest.raises(AssertionError):
        assert_reconciled(1.0, 0.0, 0.05)          # expected==0, gap=|actual|>tol -> fail


def test_mvd_assert_file_contains(tmp_path):
    from lib.mvd import assert_file_contains

    f = tmp_path / "rule.txt"
    f.write_text("dayofmonth >= 29\n", encoding="utf-8")
    assert_file_contains(str(f), "dayofmonth >= 29")          # present -> OK
    with pytest.raises(AssertionError):
        assert_file_contains(str(f), "dayofmonth >= 28")      # text absent -> fail
    with pytest.raises(AssertionError):
        assert_file_contains(str(tmp_path / "nope.txt"), "x")  # file missing -> fail
