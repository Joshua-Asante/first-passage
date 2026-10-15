"""Public metadata contract: identity, evidence, availability and layout integrity."""
import json
from pathlib import Path

REGISTRY = Path(__file__).resolve().parents[2] / "ops/global_market_map/registry.json"
EXPECTED_IDS = {
    "spx", "sxxp", "topix", "mchi", "eem", "us02y", "us10y", "dfii10",
    "de10y", "jp10y", "dxy", "usdjpy", "usdcnh", "oas", "brent", "copper",
    "gold", "vix", "move", "funding_basis",
}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        assert key not in result, f"duplicate JSON key: {key}"
        result[key] = value
    return result


def registry():
    assert REGISTRY.is_file(), "authoritative registry has not been published"
    return json.loads(REGISTRY.read_text(encoding="utf-8"), object_pairs_hook=unique_object)


def test_stable_conceptual_identity_and_schema():
    data = registry()
    assert data["schema_version"] == "global-market-map/v1"
    rows = data["series"]
    assert len(rows) == 20
    assert {r["series_id"] for r in rows} == EXPECTED_IDS
    assert len({r["series_id"] for r in rows}) == len(rows)
    assert "synthetic" not in data
    assert data["verification"]["markets_closed"] is True
    assert data["verification"]["moving_tick_test_performed"] is False


def test_funding_gap_is_retained_without_a_measurable_proxy():
    row = next(r for r in registry()["series"] if r["series_id"] == "funding_basis")
    assert row["availability"] == "unavailable"
    assert row["instrument"]["symbol"] is None
    assert row["instrument"]["provider"] is None
    assert row["instrument"]["unit"] is None
    assert row["measurement_conventions"] == []
    assert row["proxy"]["kind"] == "none"
    assert row["observation"]["published_at"] is None


def test_evidence_and_explicit_unknowns_survive_handoff():
    data = registry()
    evidence_ids = {e["id"] for e in data["verification"]["evidence"]}
    for row in data["series"]:
        assert row["concept"] and row["definition"] and row["limitations"]
        assert row["evidence_refs"]
        assert set(row["evidence_refs"]) <= evidence_ids
        assert all(ref in data["sources"] for ref in row["source_refs"])
        assert row["observation"]["published_at"] is None
        assert row["observation"]["available_at"] is None
        assert row["observation"]["max_age_seconds"] is None
        assert row["observation"]["timezone"]["exact_vendor_session_zone"] is None
        assert row["history"]["complete_daily_history_verified"] is False
        if row["availability"] == "available":
            assert row["instrument"]["symbol"] and row["instrument"]["provider"]
            assert row["instrument"]["unit"] and row["measurement_conventions"]


def test_entitlement_delay_and_proxy_distinctions():
    rows = {r["series_id"]: r for r in registry()["series"]}
    for sid, minutes in {"spx": 10, "sxxp": 15, "topix": 20, "dxy": 10,
                         "brent": 10, "copper": 10, "vix": 15, "move": 15}.items():
        assert rows[sid]["entitlement"]["delay_minutes"] == minutes
        assert rows[sid]["entitlement"]["realtime_exchange_entitlement"] == "not_present"
    for sid in ("mchi", "eem"):
        assert rows[sid]["proxy"]["kind"] == "etf"
        assert rows[sid]["instrument"]["loaded_feed_alias"].startswith("BATS:")
        assert rows[sid]["entitlement"]["realtime_exchange_entitlement"] == "not_verified"
    assert rows["copper"]["proxy"]["kind"] == "different_futures_market"
    assert rows["dxy"]["proxy"]["kind"] == "different_index"
    assert rows["oas"]["instrument"]["symbol"] == "FRED:BAMLH0A0HYM2"
    assert rows["oas"]["proxy"]["kind"] == "different_oas_index"


def test_measurement_units_and_futures_settings():
    rows = {r["series_id"]: r for r in registry()["series"]}
    for row in rows.values():
        conventions = row["measurement_conventions"]
        assert len({c["id"] for c in conventions}) == len(conventions)
        for c in conventions:
            assert c["definition"] and c["output_unit"]
    for sid in ("us02y", "us10y", "dfii10", "de10y", "jp10y", "oas"):
        c = {c["id"]: c for c in rows[sid]["measurement_conventions"]}
        assert c["change_bp"]["output_unit"] == "basis_points"
        assert c["change_bp"]["scale"] == 100
    for sid in ("vix", "move"):
        assert "change_bp" not in {c["id"] for c in rows[sid]["measurement_conventions"]}
    for sid in ("brent", "copper"):
        f = rows[sid]["futures"]
        assert f["back_adjustment"] is False
        assert f["daily_close"] == "settlement"
        assert f["exact_roll_schedule"] is None
    assert rows["gold"]["futures"] is None


def test_layouts_use_concepts_and_keep_derived_panels_separate():
    data = registry()
    derived = {v["view_id"]: v for v in data["derived_views"]}
    assert set(derived) == {"t10y2y", "t10yie", "regional_comparison", "brent_spread"}
    assert not (set(derived) & EXPECTED_IDS)
    layouts = data["layouts"]
    assert [len(x["panels"]) for x in layouts] == [8, 8, 8]
    for layout in layouts:
        assert layout["interval"] == "1D"
        assert layout["url"].startswith("https://www.tradingview.com/chart/")
        for panel in layout["panels"]:
            assert panel["ref"] in EXPECTED_IDS | set(derived)
    missing = [p for p in layouts[1]["panels"] if p["state"] == "unavailable"]
    assert missing == [{"ref": "funding_basis", "state": "unavailable"}]
    assert layouts[1]["populated_chart_count"] == 7
    assert derived["regional_comparison"]["currency_basis"] == "mixed_USD_EUR_JPY"


def test_public_handoff_excludes_private_exports_and_account_identifiers():
    raw = REGISTRY.read_text(encoding="utf-8")
    for forbidden in ("C:\\", "C:/Users/", "history-audit/", "account_id"):
        assert forbidden not in raw
    assert not list(REGISTRY.parent.glob("*.csv"))
