"""Personal Tradovate micro cap (Q-SFCLEAR-2 run-path card A, step A0; D6)."""
import firm_rules

TIER = "Personal_Tradovate"


def test_personal_cap_is_the_existing_80_micro_source():
    cap = firm_rules.FIRM_RULES[TIER]["micro_contract_cap"]
    assert type(cap) is int and cap == 80


def test_personal_cap_matches_the_tradeify_book_cap_it_reuses():
    # D6 keeps the existing cap source; the two rows must not drift apart.
    assert (firm_rules.FIRM_RULES[TIER]["micro_contract_cap"]
            == firm_rules.FIRM_RULES["Tradeify_Select_100K"]["micro_contract_cap"])
