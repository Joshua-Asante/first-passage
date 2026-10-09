from datetime import datetime, timezone
from pathlib import Path
import pytest
from scripts.azure_jobs import control

MONDAY = datetime(2026, 10, 5, tzinfo=timezone.utc).timestamp()


def test_reservation_refuses_over_budget_without_starting(tmp_path):
    ledger = control.Ledger(tmp_path / 'ledger.json', initial_seconds=42 * 3600, initial_week=MONDAY)
    with pytest.raises(ValueError, match='weekly'):
        ledger.reserve('job', 7200, MONDAY + 100)
    assert ledger.read()['active'] is None


def test_reservation_persists_and_second_controller_cannot_start(tmp_path):
    path = tmp_path / 'ledger.json'
    first = control.Ledger(path, initial_seconds=0, initial_week=MONDAY)
    first.reserve('job', 100, MONDAY + 100)
    second = control.Ledger(path)
    with pytest.raises(ValueError, match='active'):
        second.reserve('other', 100, MONDAY + 110)
    assert second.read()['active']['job_id'] == 'job'


def test_missing_ledger_requires_explicit_seed(tmp_path):
    with pytest.raises(ValueError, match='seed'):
        control.Ledger(tmp_path / 'ledger.json').read()


def test_week_boundary_refused_and_old_usage_not_reused(tmp_path):
    ledger = control.Ledger(tmp_path / 'ledger.json', initial_seconds=40 * 3600, initial_week=MONDAY)
    with pytest.raises(ValueError, match='boundary'):
        ledger.reserve('late', 100, MONDAY + 7 * 86400 - 50)
    ledger.reserve('next', 3600, MONDAY + 7 * 86400 + 100)
    assert ledger.read()['active']['job_id'] == 'next'


class FakeAzure:
    def __init__(self, states):
        self.states = iter(states)
        self.calls = []
    def deallocate(self):
        self.calls.append('deallocate')
    def power(self):
        return next(self.states)


def test_idle_deallocate_verifies_before_releasing_reservation(tmp_path):
    ledger = control.Ledger(tmp_path / 'ledger.json', initial_seconds=0, initial_week=MONDAY)
    ledger.reserve('job', 3600, MONDAY + 100)
    azure = FakeAzure(['VM deallocating', 'VM deallocated'])
    clock = iter([MONDAY + 200, MONDAY + 210, MONDAY + 220])
    control.retire(azure, ledger, clock=lambda: next(clock), sleep=lambda _: None, attempts=2)
    assert azure.calls == ['deallocate', 'deallocate']
    assert ledger.read()['active'] is None
    assert ledger.read()['sessions'][0]['end'] >= MONDAY + 200


def test_unconfirmed_deallocation_keeps_charging_and_blocks_new_job(tmp_path):
    ledger = control.Ledger(tmp_path / 'ledger.json', initial_seconds=0, initial_week=MONDAY)
    ledger.reserve('job', 3600, MONDAY + 100)
    azure = FakeAzure(['VM stopped', 'VM running'])
    with pytest.raises(RuntimeError, match='unconfirmed'):
        control.retire(azure, ledger, sleep=lambda _: None, attempts=2)
    assert ledger.read()['active'] is not None
    with pytest.raises(ValueError, match='active'):
        ledger.reserve('second', 1, MONDAY + 200)


def test_elapsed_session_split_across_weeks(tmp_path):
    ledger = control.Ledger(tmp_path / 'ledger.json', initial_seconds=0, initial_week=MONDAY)
    ledger.reserve('job', 30, MONDAY + 7 * 86400 - 60)
    ledger.finish(MONDAY + 7 * 86400 + 60)
    assert ledger.week_seconds(MONDAY + 7 * 86400 + 70) == 60
    assert ledger.week_seconds(MONDAY + 7 * 86400 - 70) == 60


@pytest.mark.parametrize('seconds', [0, -1, float('nan'), float('inf'), True])
def test_invalid_duration_fails_closed(tmp_path, seconds):
    ledger = control.Ledger(tmp_path / 'ledger.json', initial_seconds=0, initial_week=MONDAY)
    with pytest.raises(ValueError):
        ledger.reserve('job', seconds, MONDAY)


def test_clock_reversal_not_negative_credit(tmp_path):
    ledger = control.Ledger(tmp_path / 'ledger.json', initial_seconds=0, initial_week=MONDAY)
    ledger.reserve('job', 100, MONDAY + 100)
    with pytest.raises(ValueError):
        ledger.finish(MONDAY)
    assert ledger.read()['active'] is not None



def test_managed_submission_uses_private_json_file_not_batch_command_line(tmp_path):
    from types import SimpleNamespace
    calls = []
    def execute(args, **kwargs):
        calls.append(args)
        return SimpleNamespace(returncode=0,stdout='{}',stderr='')
    config = dict(az='az.cmd',subscription='subscription-placeholder',resource_group='group',vm='vm',location='eastus',state_dir=str(tmp_path))
    azure = control.Azure(config,execute=execute)
    azure.submit('test-job', 'Write-Output '+('x'*20000), timeout=3600)
    assert calls[0][1:3] == ['rest','--method']
    body_arg = calls[0][calls[0].index('--body')+1]
    import json
    body = json.loads(Path(body_arg[1:]).read_text())
    assert body['properties']['timeoutInSeconds'] == 3600
    assert body['properties']['asyncExecution'] is True
    assert len(body['properties']['source']['script']) > 20000


def test_stale_retirement_cannot_deallocate_successor(tmp_path):
    ledger = control.Ledger(tmp_path / "ledger.json", initial_seconds=0, initial_week=MONDAY)
    ledger.reserve("old", 100, MONDAY + 100)
    ledger.finish(MONDAY + 110)
    ledger.reserve("new", 100, MONDAY + 120)
    azure = FakeAzure([])
    control.retire(azure, ledger, expected_job="old", sleep=lambda _: None)
    assert azure.calls == []
    assert ledger.read()["active"]["job_id"] == "new"


def test_malformed_azure_response_does_not_abandon_shutdown(tmp_path):
    import json
    ledger = control.Ledger(tmp_path / "ledger.json", initial_seconds=0, initial_week=MONDAY)
    ledger.reserve("job", 100, MONDAY + 100)
    class Flaky(FakeAzure):
        def power(self):
            if len(self.calls) == 1:
                raise json.JSONDecodeError("bad", "", 0)
            return "VM deallocated"
    azure = Flaky([])
    control.retire(azure, ledger, clock=lambda: MONDAY+110, sleep=lambda _:None, attempts=2)
    assert ledger.read()["active"] is None


def test_lease_adds_tags_on_bare_vm_without_replacing_other_tags():
    from types import SimpleNamespace
    calls = []
    def execute(args, **kwargs):
        calls.append(args)
        if args[1:3] == ["vm", "update"]:
            return SimpleNamespace(returncode=1, stdout="", stderr="Couldn't find tags")
        return SimpleNamespace(returncode=0, stdout="{}", stderr="")
    azure = control.Azure(dict(az="az.cmd", subscription="placeholder", resource_group="group", vm="vm"), execute=execute)
    azure.set_lease("job", 1234)
    assert calls[0][1:3] == ["tag", "update"]
    assert calls[0][calls[0].index("--operation") + 1] == "Merge"
