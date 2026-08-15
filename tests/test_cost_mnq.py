"""cost_mnq firm_key is required (gate-stack audit R6)."""
from __future__ import annotations

import pytest

from discovery import cost_mnq


def test_default_firm_key_retired():
    assert not hasattr(cost_mnq, "DEFAULT_FIRM_KEY")


def test_hurdle_requires_firm_key():
    with pytest.raises(TypeError):
        cost_mnq.hurdle_from_price(15000.0)  # type: ignore[misc]


def test_hurdle_explicit_firm_key():
    h = cost_mnq.hurdle_from_price(14769.25, firm_key="Bulenox_100K")
    assert h.firm_key == "Bulenox_100K"
    assert h.commission_per_side_usd == pytest.approx(0.61)
    assert h.hurdle_4x_frac > 0
