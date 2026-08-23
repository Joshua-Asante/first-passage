"""Phase C: Guardian/Aegis leave living BASE_RISK; historical book + Call-4 stay."""

from dd_protection import BASE_RISK, DD_SCALE, DD_TRIGGER
from firm_rules import _BASE_RISK
from historical_challenge import HISTORICAL_CHALLENGE_BASE_RISK
from lifecycle import STRATEGY_KEYS


def test_living_base_risk_is_striker_pair_only():
    assert set(_BASE_RISK) == {"striker", "striker_nas100"}
    assert set(BASE_RISK) == {"Striker", "Striker NAS100"}
    assert "Guardian" not in BASE_RISK
    assert "Aegis" not in BASE_RISK


def test_historical_book_bytes_match_pre_c_lock():
    assert HISTORICAL_CHALLENGE_BASE_RISK == {
        "guardian": 0.0034,
        "striker": 0.0070,
        "aegis": 0.0150,
        "striker_nas100": 0.0037,
    }
    for slug, value in _BASE_RISK.items():
        assert value == HISTORICAL_CHALLENGE_BASE_RISK[slug]


def test_call4_authorization_book_stays_four_leg():
    assert STRATEGY_KEYS == frozenset(
        {"Guardian", "Striker", "Aegis", "Striker NAS100"}
    )


def test_protection_literals_untouched():
    assert DD_TRIGGER == 0.015
    assert DD_SCALE == 0.40
