"""A licensed bounded test signal using the unchanged Strategy/Signal interface."""
from c1_rail.m1_stage1_contract import LEG_ID, STOP_DIST_PTS
from c1_signal_daemon.m1_stage1_control import digest, utc
from c1_signal_daemon.strategy_protocol import Signal


class M1Stage1TestStrategy:
    def __init__(self, coordinator):
        self.coordinator = coordinator

    def on_bar(self, bar):
        manifest = self.coordinator.current_manifest
        if manifest is None or bar.ts != utc(manifest["target"]):
            return None
        event = "m1-" + digest({key: manifest[key] for key in
                              ("ceremony_id", "target", "contract_sha256", "source")})
        return Signal(LEG_ID, "entry", bar.close, STOP_DIST_PTS, event)
