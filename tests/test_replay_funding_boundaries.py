from decimal import Decimal
import unittest
from unittest.mock import patch

from lab import replay_funding as funding


D = Decimal


def facts(**changes):
    values = {
        "cash_before": D("1000"),
        "point_value": D("5"),
        "execution_price": D("100"),
        "current_mark": D("99"),
        "execution_cost": D("3"),
        "margin_ratio": D("1"),
        "requested_quantity": 1,
        "open_quantity": 0,
        "competing_entry_count": 0,
        "direction": "LONG",
        "known_state": True,
        "execution_price_established": True,
    }
    values.update(changes)
    return funding.FundingFacts(**values)


class ConstructionPreflightTests(unittest.TestCase):
    def test_over_budget_add_rejects_before_coefficient_construction(self):
        with patch.object(
            funding, "_coefficient_from_digits",
            side_effect=AssertionError("coefficient construction reached"),
        ):
            with self.assertRaises(funding._ArithmeticLimit):
                funding._exact_add(D("99999"), D("1"), _budget=3)

    def test_over_budget_multiply_rejects_before_coefficient_construction(self):
        with patch.object(
            funding, "_coefficient_from_digits",
            side_effect=AssertionError("coefficient construction reached"),
        ):
            with self.assertRaises(funding._ArithmeticLimit):
                funding._exact_multiply(D("99999"), D("2"), _budget=3)

    def test_zero_and_exact_equality_shortcuts_precede_metadata_and_construction(self):
        with patch.object(
            funding, "_coefficient_from_digits",
            side_effect=AssertionError("coefficient construction reached"),
        ):
            self.assertEqual(
                funding._exact_add(D("1E+9999"), D("-1E+9999"), _budget=1),
                D("0"),
            )
            self.assertEqual(
                funding._exact_subtract(D("1E+9999"), D("1E+9999"), _budget=1),
                D("0"),
            )
            self.assertEqual(
                funding._exact_multiply(D("0"), D("99999"), _budget=1),
                D("0"),
            )

    def test_padded_but_normalized_compact_inputs_are_not_input_capped(self):
        self.assertEqual(
            funding._exact_multiply(D("1000.0000"), D("1"), _budget=1),
            D("1E+3"),
        )


class BorderlineProductTests(unittest.TestCase):
    def test_actual_one_scratch_digit_product_is_accepted_in_both_orders(self):
        self.assertEqual(funding._exact_multiply(D("16"), D("125"), _budget=3),
                         D("2E+3"))
        self.assertEqual(funding._exact_multiply(D("125"), D("16"), _budget=3),
                         D("2E+3"))
        self.assertEqual(
            funding._exact_multiply(D("1"), D("16"), D("125"), _budget=3),
            D("2E+3"),
        )

    def test_nearby_products_keep_actual_result_and_scratch_limits(self):
        for left, right in (("99", "99"), ("16", "124"), ("15", "125"),
                            ("16", "625")):
            with self.subTest(left=left, right=right):
                with self.assertRaises(funding._ArithmeticLimit):
                    funding._exact_multiply(D(left), D(right), _budget=3)
        self.assertEqual(funding._exact_multiply(D("12"), D("25"), _budget=3),
                         D("3E+2"))
        self.assertEqual(funding._exact_multiply(D("45"), D("22"), _budget=3),
                         D("9.9E+2"))
        self.assertEqual(funding._exact_multiply(D("1"), D("999"), _budget=3),
                         D("999"))


class ContractPreservationTests(unittest.TestCase):
    def test_base_witness_and_domain_precedence_are_unchanged(self):
        result = funding.assess_funding(facts())
        self.assertEqual(result.status, funding.FundingStatus.PROVEN_POSITIVE_CUSHION)
        self.assertEqual(result.reason, funding.FundingReason.POSITIVE_CUSHION)
        self.assertEqual(
            (result.cash_after_cost, result.funding_basis,
             result.required_at_basis, result.surplus,
             result.post_fill_margin_cushion),
            (D("997"), D("100"), D("500"), D("497"), D("497")),
        )
        unknown = funding.assess_funding(facts(
            known_state=False, execution_price_established=False,
            direction="SHORT", open_quantity=1, competing_entry_count=1,
        ))
        self.assertEqual(unknown.reason, funding.FundingReason.UNKNOWN_STATE)
        invalid = funding.assess_funding(facts(
            cash_before=1000, known_state=False,
        ))
        self.assertEqual(invalid.status, funding.FundingStatus.INVALID_INPUT)
        self.assertEqual(invalid.reason, funding.FundingReason.INVALID_INPUT)


if __name__ == "__main__":
    unittest.main()
