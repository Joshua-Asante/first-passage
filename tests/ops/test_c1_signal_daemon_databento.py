"""Synthetic SDK-shaped records, strictly offline; not M1 evidence."""
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest

from c1_signal_daemon import daemon
from test_c1_signal_daemon_m1 import prepared, manifest, cfg, NOW, TARGET


class SDK:
    def __init__(self):
        self.callback = None
        self.up = True
        self.subscriptions = []
    def add_callback(self, callback, exception_callback=None):
        self.callback = callback
    def subscribe(self, **kwargs):
        self.subscriptions.append(kwargs)
    def start(self):
        pass
    def is_connected(self):
        return self.up
    def terminate(self):
        self.up = False


class SymbolMappingMsg(SimpleNamespace):
    pass


class OHLCVMsg(SimpleNamespace):
    pass


def mapping(**overrides):
    values = dict(publisher_id=1, instrument_id=123, ts_event=int(NOW.timestamp()) * 10**9,
                  stype_in="raw_symbol", stype_in_symbol="MYMU6", stype_out="raw_symbol",
                  stype_out_symbol="MYMU6", start_ts=int(NOW.timestamp()) * 10**9,
                  end_ts=int((NOW + timedelta(days=1)).timestamp()) * 10**9)
    values.update(overrides)
    return SymbolMappingMsg(**values)


def record(**overrides):
    values = dict(publisher_id=1, instrument_id=123, ts_event=int(TARGET.timestamp()) * 10**9,
                  rtype=33, open=41000 * 10**9, high=41002 * 10**9, low=40999 * 10**9,
                  close=41001 * 10**9, volume=3)
    values.update(overrides)
    return OHLCVMsg(**values)


def source_fixture(tmp_path):
    from c1_signal_daemon.databento_live_source import DatabentoLiveBarSource
    m, store, path = prepared(tmp_path)
    sdk = SDK()
    now = [TARGET + timedelta(seconds=61)]
    calls = []
    def factory():
        calls.append(True)
        return sdk
    source = DatabentoLiveBarSource(store, sdk_factory=factory, clock=lambda: now[0])
    return source, sdk, calls, now, store


def test_lazy_source_maps_finalized_bar_and_durably_deduplicates(tmp_path):
    source, sdk, calls, now, store = source_fixture(tmp_path)
    assert source.poll() is None
    assert calls == []
    assert source.connected is False
    source.activate(manifest()["source"])
    assert sdk.subscriptions == [dict(dataset="GLBX.MDP3", schema="ohlcv-1m",
                                       symbols=["MYMU6"], stype_in="raw_symbol")]
    sdk.callback(record())
    assert source.poll() is None
    sdk.callback(mapping())
    sdk.callback(record())
    bar = source.poll()
    assert bar.ts == TARGET
    assert bar.close == 41001
    assert bar.volume == 3
    sdk.callback(record())
    assert source.poll() is None
    assert len(store.read()["watermarks"]) == 1
    source.deactivate()
    assert source.poll() is None


@pytest.mark.parametrize("changes", [dict(close=float("nan")), dict(volume=0),
                                       dict(low=42000 * 10**9), dict(instrument_id=999),
                                       dict(publisher_id=99), dict(rtype=32),
                                       dict(ts_event=int((TARGET + timedelta(minutes=2)).timestamp()) * 10**9),
                                       dict(ts_event=int((TARGET - timedelta(minutes=3)).timestamp()) * 10**9)])
def test_bad_bars_never_reach_strategy(tmp_path, changes):
    source, sdk, calls, now, store = source_fixture(tmp_path)
    source.activate(manifest()["source"])
    sdk.callback(mapping())
    sdk.callback(record(**changes))
    assert source.poll() is None
    assert store.read()["watermarks"] == {}


def test_conflicting_or_expired_mapping_rejected(tmp_path):
    source, sdk, calls, now, store = source_fixture(tmp_path)
    source.activate(manifest()["source"])
    sdk.callback(mapping(stype_out_symbol="MYMZ6"))
    sdk.callback(record())
    assert source.poll() is None
    sdk.callback(mapping(end_ts=int(TARGET.timestamp()) * 10**9))
    sdk.callback(record())
    assert source.poll() is None


def test_reconnect_uses_backoff_and_no_historical_replay(tmp_path):
    source, sdk, calls, now, store = source_fixture(tmp_path)
    source.activate(manifest()["source"])
    sdk.up = False
    source.poll()
    source.activate(manifest()["source"])
    assert len(calls) == 1
    now[0] += timedelta(seconds=3)
    sdk.up = True
    source.activate(manifest()["source"])
    assert len(calls) == 2
    assert all("start" not in sub for sub in sdk.subscriptions)


def test_runtime_activation_order_backs_off_established_disconnect(tmp_path):
    source, sdk, calls, now, store = source_fixture(tmp_path)
    source.activate(manifest()["source"])
    sdk.up = False
    # EvaluateLoop calls coordinator activation before source.poll every cycle.
    source.activate(manifest()["source"])
    source.poll()
    source.activate(manifest()["source"])
    assert len(calls) == 1
    now[0] += timedelta(seconds=2)
    sdk.up = True
    source.activate(manifest()["source"])
    assert len(calls) == 2


@pytest.mark.parametrize("changes", [dict(stype_in="instrument_id", stype_in_symbol="123"),
                                      dict(stype_in_symbol="MYMZ6"),
                                      dict(stype_out_symbol="MYMZ6"),
                                      dict(stype_out="instrument_id", stype_out_symbol="123"),
                                      dict(instrument_id=999), dict(publisher_id=2)])
def test_mapping_requires_both_elected_raw_symbols_and_header_identity(tmp_path, changes):
    source, sdk, calls, now, store = source_fixture(tmp_path)
    source.activate(manifest()["source"])
    sdk.callback(mapping(**changes))
    sdk.callback(record())
    assert source.poll() is None
    assert source.binding is None


def test_runtime_build_is_network_free_and_exposes_boot(tmp_path):
    import json
    path = tmp_path / "config.json"
    value = cfg()
    value["strategy"] = "null"
    value["m1_test"]["state_path"] = str(tmp_path / "runtime.json")
    path.write_text(json.dumps(value))
    calls = []
    loop = daemon.build_loop(path, boot_id="runtime-boot", sdk_factory=lambda: calls.append(True))
    loop.step(NOW)
    heartbeat = loop.heartbeat(NOW).as_json_dict()
    assert calls == []
    assert heartbeat["boot_id"] == "runtime-boot"
    assert heartbeat["strategy"] == "NullStrategy"
    assert heartbeat["effective_emit"] is False
    assert "path_token" not in str(heartbeat)
