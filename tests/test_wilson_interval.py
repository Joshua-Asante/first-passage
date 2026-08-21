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
