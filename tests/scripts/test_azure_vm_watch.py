"""Behavior of scripts/azure_vm_watch.py against a fake VM and clock."""
from __future__ import annotations

import importlib.util
import json
import subprocess
from pathlib import Path

import pytest

_SPEC = importlib.util.spec_from_file_location(
    "azure_vm_watch", Path(__file__).resolve().parents[2] / "scripts" / "azure_vm_watch.py")
w = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(w)

RUN = "VM running"
MONDAY = 1792800000.0 - (1792800000.0 % 604800) + 4 * 86400  # a UTC Monday 00:00


class Clock:
    def __init__(self):
        self.t = MONDAY + 3600

    def __call__(self):
        return self.t

    def sleep(self, s):
        self.t += s


class FakeVm:
    """Power states come from ``script`` (one per read; last repeats); deallocate sets deallocated."""

    def __init__(self, script, deallocate_works=True):
        self.script, self.works, self.deallocations, self.forced = list(script), deallocate_works, 0, None

    def power(self):
        if self.forced:
            return self.forced
        state = self.script.pop(0) if len(self.script) > 1 else self.script[0]
        if isinstance(state, Exception):
            raise state
        return state

    def deallocate(self):
        self.deallocations += 1
        if self.works:
            self.forced = w.DEALLOCATED


def run(vm, tmp_path, clock=None, **kw):
    clock = clock or Clock()
    opts = dict(hours=1, poll=60, grace=900, rate=2.90, cap=125.0, max_unreadable=600)
    opts.update(kw)
    ledger = w.Ledger(tmp_path / "ledger.json")
    return w.watch(vm, ledger, tmp_path, clock=clock, sleep=clock.sleep, **opts), ledger, clock


def test_deadline_deallocates_and_verifies(tmp_path):
    vm = FakeVm([RUN])
    rc, ledger, clock = run(vm, tmp_path, hours=1)
    assert rc == 0 and vm.deallocations == 1
    assert ledger.seconds(clock()) == pytest.approx(3600)


def test_run_ending_deallocated_exits_without_deallocating(tmp_path):
    vm = FakeVm([RUN, RUN, w.DEALLOCATING, w.DEALLOCATED])
    rc, _, _ = run(vm, tmp_path)
    assert rc == 0 and vm.deallocations == 0


def test_never_started_exits_after_grace(tmp_path):
    vm = FakeVm([w.DEALLOCATED])
    rc, _, clock = run(vm, tmp_path, grace=900)
    assert rc == 0 and vm.deallocations == 0 and clock() - (MONDAY + 3600) >= 900


def test_waits_for_start_then_watches(tmp_path):
    vm = FakeVm([w.DEALLOCATED, w.DEALLOCATED, "VM starting", RUN])
    rc, _, _ = run(vm, tmp_path, hours=1)
    assert rc == 0 and vm.deallocations == 1


def test_stopped_but_allocated_is_deallocated(tmp_path):
    vm = FakeVm([RUN, w.STOPPED])
    rc, _, _ = run(vm, tmp_path, hours=12)
    assert rc == 0 and vm.deallocations == 1


def test_weekly_cap_counts_prior_watched_time(tmp_path):
    clock = Clock()
    w.Ledger(tmp_path / "ledger.json").add(clock(), 125 / 2.90 * 3600 - 120)
    vm = FakeVm([RUN])
    rc, _, _ = run(vm, tmp_path, clock=clock, hours=12)
    assert rc == 0 and vm.deallocations == 1 and clock() - (MONDAY + 3600) < 600


def test_prior_week_does_not_count(tmp_path):
    clock = Clock()
    w.Ledger(tmp_path / "ledger.json").add(clock() - 7 * 86400, 10**6)
    vm = FakeVm([RUN, RUN, w.DEALLOCATED])
    rc, _, _ = run(vm, tmp_path, clock=clock, hours=12)
    assert rc == 0 and vm.deallocations == 0


def test_unreadable_power_state_deallocates(tmp_path):
    vm = FakeVm([RUN, RuntimeError("network")])
    rc, _, clock = run(vm, tmp_path, hours=12, max_unreadable=600)
    assert rc == 0 and vm.deallocations == 1 and clock() - (MONDAY + 3600) < 3600


def test_unverified_deallocation_alarms(tmp_path):
    vm = FakeVm([RUN], deallocate_works=False)
    rc, _, _ = run(vm, tmp_path, hours=1)
    assert rc == 2 and vm.deallocations == 3 and (tmp_path / "ALARM.txt").exists()


def test_hours_capped_at_twelve():
    with pytest.raises(SystemExit):
        w.main(["--hours", "12.5"])


def test_az_calls_are_read_or_deallocate_and_redacted(monkeypatch):
    calls = []
    view = {"instanceView": {"statuses": [{"code": "ProvisioningState/succeeded", "displayStatus": "x"},
                                          {"code": "PowerState/running", "displayStatus": RUN}]}}

    def fake_run(cmd, **_):
        calls.append(cmd[1:3])
        if cmd[2] == "deallocate":
            return subprocess.CompletedProcess(cmd, 1, "", "denied /subscriptions/12345678-0000-4000-8000-000000000000/x")
        return subprocess.CompletedProcess(cmd, 0, json.dumps(view), "")

    monkeypatch.setattr(w.subprocess, "run", fake_run)
    vm = w.Vm("az", "g", "n")
    assert vm.power() == RUN
    with pytest.raises(RuntimeError) as e:
        vm.deallocate()
    assert "12345678" not in str(e.value) and "<redacted>" in str(e.value)
    assert calls == [["vm", "get-instance-view"], ["vm", "deallocate"]]


def test_slow_read_cannot_defer_the_deadline(tmp_path):
    clock = Clock()

    class SlowVm(FakeVm):
        def power(self):
            if not self.forced:
                clock.t += 1800  # one read blocks past the 15-minute deadline
            return super().power()

    vm = SlowVm([RUN])
    rc, _, _ = run(vm, tmp_path, clock=clock, hours=0.25)
    assert rc == 0 and vm.deallocations == 1 and clock() - (MONDAY + 3600) < 1900


def test_unwritable_ledger_deallocates(tmp_path):
    (tmp_path / "ledger.json").mkdir()  # reading a directory raises OSError
    vm = FakeVm([RUN])
    rc, _, _ = run(vm, tmp_path, hours=12)
    assert rc == 0 and vm.deallocations == 1


def test_power_read_timeout_is_short(monkeypatch):
    seen = {}

    def fake_run(cmd, timeout, **_):
        seen[cmd[2]] = timeout
        raise subprocess.TimeoutExpired(cmd, timeout)

    monkeypatch.setattr(w.subprocess, "run", fake_run)
    with pytest.raises(subprocess.TimeoutExpired):
        w.Vm("az", "g", "n").power()
    assert seen["get-instance-view"] <= 120


def test_deallocation_retries_are_billed(tmp_path):
    vm = FakeVm([RUN], deallocate_works=False)
    rc, ledger, clock = run(vm, tmp_path, hours=1)
    assert rc == 2 and ledger.seconds(clock()) == pytest.approx(3600 + 3 * 60)


def test_external_deallocation_bills_the_final_interval(tmp_path):
    vm = FakeVm([RUN, RUN, w.DEALLOCATING, w.DEALLOCATED])
    rc, ledger, clock = run(vm, tmp_path)
    assert rc == 0 and ledger.seconds(clock()) == pytest.approx(180)
