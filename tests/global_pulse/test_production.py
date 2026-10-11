"""Compatibility with exact #787 bytes; all measurement values are invented."""
from copy import deepcopy
from pathlib import Path
import shutil

import pytest

from scripts.global_pulse import bridge as b, production as prod

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def case(tmp_path):
    root = tmp_path / "input"
    shutil.copytree(FIXTURES, root)
    return b.decode((root / "production-packet.json").read_bytes()), root, tmp_path / "captures"


def test_exact_revision_and_complete_metadata(case):
    p, root, output = case
    raw = (root / p["watchlist"]["path"]).read_bytes()
    assert p["watchlist"]["revision"] == "107fe97cdba6f2b6b5c0f1939bfe93b3924b3ceb"
    assert b.digest(raw) == prod.SHA256 == "ae0af9795931524faecc53d00ac63864caf41e68949d28f83d719970783b2b9c"
    registry = b.decode(raw)
    rows = prod.project(registry, raw, prod.REVISION)
    assert set(rows) == {
        "spx", "sxxp", "topix", "mchi", "eem", "us02y", "us10y", "dfii10",
        "de10y", "jp10y", "dxy", "usdjpy", "usdcnh", "oas", "brent", "copper",
        "gold", "vix", "move", "funding_basis",
    }
    assert rows["funding_basis"]["conventions"] == {}
    assert rows["mchi"]["production"]["instrument"]["loaded_feed_alias"] == "BATS:MCHI"
    assert rows["brent"]["production"]["futures"]["back_adjustment"] is False
    assert rows["brent"]["production"]["futures"]["daily_close"] == "settlement"
    assert rows["brent"]["production"]["futures"]["contract_mapping"] is None
    assert rows["dfii10"]["conventions"]["change_bp"]["scale"] == 100
    bundle = b.capture(p, root, output)
    assert (bundle / "registry.json").read_bytes() == raw
    context = b.decode((bundle / "registry-context.json").read_bytes())
    assert context["verification"] == registry["verification"]
    assert context["series"] == registry["series"]
    assert context["verification"]["moving_tick_test_performed"] is False
    assert b.verify_bundle(bundle) == p


def test_mixed_demonstration_remains_synthetic_and_open(case):
    p, root, output = case
    bundle = b.capture(p, root, output)
    warnings = b.validate(p, root)["limitations"]
    assert not any("SYNTHETIC registry" in w for w in warnings)
    assert any("SYNTHETIC VALUES" in w for w in warnings)
    retained = b.verify_bundle(bundle)
    assert {m["delivery"] for m in retained["measurements"]} == {"live_label", "delayed", "daily"}
    assert retained["missing_inputs"][0]["series_id"] == "funding_basis"
    assert all(m["published_at"] is m["available_at"] is None for m in retained["measurements"])
    daily = next(m for m in retained["measurements"] if m["series_id"] == "dfii10")
    assert daily["observed_at"] is daily["bar_time"] is daily["window_end"] is None
    assert daily["observation_date"] == "2026-10-08"
    notice = b.draft(bundle).read_text(encoding="utf-8")
    for expected in ("SYNTHETIC VALUES", "Decision: PENDING", "funding_basis", "BATS:MCHI",
                     "delay_minutes", "settlement", "contract_mapping", "live_label_observed_closed_market",
                     prod.REVISION, "published_at unknown"):
        assert expected in notice
    assert "GRADUATED to" not in notice
    assert not (bundle / "notice-finalization.json").exists()


@pytest.mark.parametrize("mutation", ["revision", "content", "schema", "identity"])
def test_production_identity_cannot_be_forged(case, mutation):
    p, root, _ = case
    if mutation == "revision":
        p["watchlist"]["revision"] = "0" * 40
    else:
        r = b.decode((root / p["watchlist"]["path"]).read_bytes())
        if mutation == "schema":
            r["schema_version"] = "global-market-map/v2"
        elif mutation == "identity":
            r["registry_id"] = "impostor"
        else:
            r["series"][0]["entitlement"]["delay_minutes"] = 0
        raw = b.encoded(r)
        (root / p["watchlist"]["path"]).write_bytes(raw)
        p["watchlist"]["sha256"] = b.digest(raw)
    with pytest.raises(ValueError):
        b.validate(p, root)


def test_funding_cannot_disappear_or_be_measured(case):
    p, root, output = case
    copy = deepcopy(p)
    copy["missing_inputs"] = []
    with pytest.raises(ValueError, match="missing funding_basis"):
        b.capture(copy, root, output)
    assert not output.exists()
    p["measurements"][0]["series_id"] = "funding_basis"
    with pytest.raises(ValueError, match="unavailable input"):
        b.capture(p, root, output)
    assert not output.exists()


@pytest.mark.parametrize("sid,delay", [("spx", 10), ("sxxp", 15), ("topix", 20), ("dxy", 10),
                                      ("brent", 10), ("copper", 10), ("vix", 15), ("move", 15)])
def test_all_declared_delays_survive(case, sid, delay):
    p, root, _ = case
    raw = (root / p["watchlist"]["path"]).read_bytes()
    row = prod.project(b.decode(raw), raw, prod.REVISION)[sid]
    m = p["measurements"][1]
    m.update(series_id=sid, unit=row["unit"], definition=row["conventions"]["level"]["definition"])
    p["evidence"][1]["provider"] = row["provider"]
    warnings = b.validate(p, root)["limitations"]
    assert any(f'"delay_minutes": {delay}' in w and w.startswith(sid + ": entitlement") for w in warnings)
    m["delivery"] = "live_label"
    with pytest.raises(ValueError, match="delivery classification"):
        b.validate(p, root)


def test_units_conventions_and_provider_fail_closed(case):
    p, root, _ = case
    daily = p["measurements"][2]
    daily["unit"] = "basis_points"
    with pytest.raises(ValueError, match="incorrect units"):
        b.validate(p, root)
    daily["unit"] = "percent"
    daily["definition"] = "100 * daily value"
    with pytest.raises(ValueError, match="ambiguous measurement"):
        b.validate(p, root)
    daily["definition"] = "Source level at window_end, without rebasing or currency conversion."
    p["evidence"][0]["provider"] = "NASDAQ"
    with pytest.raises(ValueError, match="provider not represented"):
        b.validate(p, root)


def test_v1_synthetic_support_survives(case):
    _, root, output = case
    p = b.decode((root / "packet.json").read_bytes())
    bundle = b.capture(p, root, output)
    assert b.verify_bundle(bundle) == p
    assert "SYNTHETIC registry" in b.draft(bundle).read_text(encoding="utf-8")
    assert not (bundle / "registry-context.json").exists()


def test_real_capture_requires_attendance_evidence(case):
    p, root, _ = case
    p["data_kind"] = "real"
    with pytest.raises(ValueError, match="attendance"):
        b.validate(p, root)
    # Validation of attestation mechanics only: still invented test values.
    p["attendance"] = dict(observer="Test observer", method="Synthetic test of manual attestation shape",
                            attended_at=p["captured_at"], evidence_ids=["missing"])
    with pytest.raises(ValueError, match="unknown attendance evidence"):
        b.validate(p, root)


def test_unknown_daily_clock_cannot_become_a_change_window(case):
    p, root, _ = case
    m = p["measurements"][2]
    m.update(convention_id="change_bp", unit="basis_points",
             definition="100 * (source level at window_end - source level at window_start); source levels expressed in percent.")
    with pytest.raises(ValueError, match="permit only a dated level"):
        b.validate(p, root)


def test_persisted_context_is_verified(case):
    p, root, output = case
    bundle = b.capture(p, root, output)
    (bundle / "registry-context.json").write_text('{}')
    with pytest.raises(ValueError, match="integrity failure"):
        b.verify_bundle(bundle)

@pytest.mark.parametrize("index", [0, 1, 3])
def test_intraday_inputs_require_observation_clock(case, index):
    p, root, _ = case
    p["measurements"][index].update(observed_at=None, window_start=None, window_end=None)
    with pytest.raises(ValueError, match="daily delivery"):
        b.validate(p, root)


@pytest.mark.parametrize("index", [0, 1, 2])
def test_non_futures_reject_contract_ids(case, index):
    p, root, _ = case
    p["measurements"][index]["contract_ids"] = ["invented-contract"]
    with pytest.raises(ValueError, match="non-futures"):
        b.validate(p, root)
