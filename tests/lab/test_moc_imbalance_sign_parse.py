"""Regression guard on the MOC-imbalance sign rules.

The load-bearing defect this pins (found 2026-09-02): FinancialJuice publishes the
imbalance in two formats -- one with the sign inline, one with bare absolute
magnitudes whose side lives in a red/green marker. The Telegram mirror renders that
marker as a plain exclamation mark, so for those posts the sign is UNRECOVERABLE. An
earlier pass inferred "bare => buy-side" and was falsified by the X original for
2025-04-30, which is red (sell-side) with digits identical to the row stored as
buy-side.

These tests fail if anyone re-promotes bare magnitudes to a trusted sign, or lets a
non-verified row reach the tradeable table.

Home of the parser: lab/analysis/c1/tradeify_book_composition_2026-09/scrape/.
Imported by path because the campaign slug is hyphenated (not a package name).
"""
from __future__ import annotations

import importlib.util
import pathlib

import pytest

_PARSER = (pathlib.Path(__file__).resolve().parents[2] / "lab" / "analysis" / "c1"
           / "tradeify_book_composition_2026-09" / "scrape" / "build_moc_table.py")


def _load():
    spec = importlib.util.spec_from_file_location("moc_build", _PARSER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def parser():
    if not _PARSER.exists():
        pytest.skip(f"parser absent: {_PARSER}")
    return _load()


# The exclamation-mark family marks negatives inline and leaves positives bare, so a
# post carrying any '-' is self-consistently signed and trustworthy.
def test_inline_negative_family_is_trusted(parser):
    p = parser.parse_post(
        "❗ MOC IMBALANCE\nS&P 500: 619.2 MLN\nNASDAQ 100: -269.0 MLN\n"
        "DOW 30: 180.9 MLN\nMAG 7: -58.0 MLN $MACRO|FJ")
    assert p["sign_source"] == "explicit"
    assert p["sp500"] == pytest.approx(619.2)
    assert p["ndx"] == pytest.approx(-269.0)
    assert p["mag7"] == pytest.approx(-58.0)


def test_explicit_plus_minus_format_is_trusted(parser):
    p = parser.parse_post(
        "MOC Imbalance\n\nS&P 500: +197 mln\nNasdaq 100: -6.5 mln\n"
        "Dow 30: 78.4 mln\nMag 7: -22.1 mln|FJ")
    assert p["sign_source"] == "explicit"
    assert p["sp500"] == pytest.approx(197.0)
    assert p["ndx"] == pytest.approx(-6.5)


def test_bln_units_scale_to_mln(parser):
    p = parser.parse_post(
        "MOC Imbalance\n\nS&P 500: +6.8 bln\nNasdaq 100: +2.8 bln\n"
        "Dow 30: +2.6 bln\nMag 7: +1.9 bln|FJ")
    assert p["sign_source"] == "explicit"
    assert p["sp500"] == pytest.approx(6800.0)


# THE REGRESSION GUARD. This is the real 2025-04-30 post as the Telegram mirror
# rendered it. The X original carries a red (sell-side) marker; the mirror dropped it.
# The parser must NOT report this as trusted, and must not claim a buy-side sign.
def test_all_bare_post_is_flagged_not_trusted(parser):
    p = parser.parse_post(
        "❗ MOC IMBALANCE\nS&P 500: 2787.9 MLN\nNASDAQ 100: 1281.8 MLN\n"
        "DOW 30: 999.8 MLN\nMAG 7: 1013.6 MLN $MACRO|FJ")
    assert p["sign_source"] != "explicit", (
        "all-bare posts carry their side in a colour marker the mirror drops; "
        "they must never be classified as explicitly signed")
    assert p["sign_source"] == "bare-positive"
    # magnitude is still correct and usable
    assert abs(p["sp500"]) == pytest.approx(2787.9)


def test_colour_marked_sell_side_is_signed_when_the_marker_survives(parser):
    """If the red marker DOES reach us (scraped from X, not the mirror), use it."""
    p = parser.parse_post(
        "\U0001F534 MOC IMBALANCE\nS&P 500: 2787.9 MLN\nNASDAQ 100: 1281.8 MLN\n"
        "DOW 30: 999.8 MLN\nMAG 7: 1013.6 MLN $MACRO|FJ")
    assert p["sign_source"] == "emoji/word-sell"
    assert p["sp500"] == pytest.approx(-2787.9)
    assert p["ndx"] == pytest.approx(-1281.8)


def test_single_figure_word_format(parser):
    p = parser.parse_post("MOC imbalance 4.1 bln buy-side.")
    assert p["sp500"] == pytest.approx(4100.0)
    p = parser.parse_post("MOC IMBALANCE 2.1 BLN SELL-SIDE.")
    assert p["sp500"] == pytest.approx(-2100.0)


def test_early_prints_are_flagged(parser):
    p = parser.parse_post("1. Early MOC imbalance 528 mln sell-side.")
    assert p["early"] is True


def test_only_verified_sign_rows_reach_the_pine_table(parser):
    """The splice must filter on == 'explicit', not merely exclude a sentinel."""
    src = _PARSER.read_text(encoding="utf-8")
    assert 'p["sign_source"] == "explicit"' in src, (
        "the Pine splice must whitelist verified-sign rows; a blacklist lets a new "
        "unverifiable sign class through silently")
