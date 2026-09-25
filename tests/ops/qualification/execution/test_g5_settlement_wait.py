"""The committing qg5 unit is settled only after it has left its cgroup.

Regression for the intermittent Linux failure of
``test_s3_genuine_pass_reaches_n2_ready`` (``BUDGET_UNCERTAIN`` instead of
``N2_READY``): the assessment commit lands while the g5 driver is still
returning, and ``_run_n1_g5`` used to break out of its supervision loop on the
progression state and observe at once. A populated slice yields no final CPU
sample (``LinuxCampaignRuntime.observation``), and since the settlement rule
of #455 an uncertain settlement ends authority even from ``N2_READY``.

The fakes stand in for the store, the Linux runtime and the unit bus; the
kernel is reduced to the unit cgroup's ``cgroup.events`` file.
"""
import base64
import json
import shutil
from contextlib import contextmanager
from pathlib import PurePosixPath
from types import SimpleNamespace

import pytest

from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution import campaign_supervisor as supervisor
from c1_rail.qualification.execution import runtime

BOOT_ID = 'boot0'
LINUX_INTERPRETER = '/opt/ops/bin/python'
LINUX_CODE_ROOT = '/opt/qualification'
PAYLOAD_SLICE = 'fpq-camp-work.slice'
UNIT = 'fpq-camp-work-g5.service'
START_NS = 10**12
WALL_NS = 60 * 10**9


class Kernel:
    """Wall time and the unit cgroup; the unit exits after ``exit_after`` sleeps."""

    def __init__(self, parent, exit_after, populated=1, remove_on_exit=False):
        self.now = START_NS
        self.sleeps = 0
        self.exit_after = exit_after
        self.remove_on_exit = remove_on_exit
        self.group = parent / 'fpq-camp.slice' / PAYLOAD_SLICE / UNIT
        self.group.mkdir(parents=True)
        (self.group / 'cgroup.procs').write_text('')
        self.set_populated(populated)

    def set_populated(self, value):
        (self.group / 'cgroup.events').write_text(f'populated {value}\nfrozen 0\n')

    def populated(self):
        if not self.group.exists():
            return 0
        text = (self.group / 'cgroup.events').read_text()
        return int(text.split('populated ')[1].split()[0])

    def clock(self):
        return encoded({'schema': 'qualification_campaign_clock/v1', 'boot_id': BOOT_ID,
                        'boottime_ns': self.now, 'utc': '2026-09-23T00:00:00Z'})

    def sleep(self, seconds):
        self.sleeps += 1
        self.now += int(seconds * 10**9)
        if self.exit_after is not None and self.sleeps >= self.exit_after:
            if self.remove_on_exit:
                # systemd removes a stopped transient unit's cgroup outright.
                shutil.rmtree(self.group, ignore_errors=True)
            else:
                self.set_populated(0)


class Campaigns:
    """The store surface ``_run_n1_g5`` uses. The commit has already landed."""

    def __init__(self, progression):
        self.progression = progression
        self.settled = []
        self.transitions = []

    def state(self):
        return {'attempt_id': 'att1', 'state': self.progression, 'validity': 'VALID',
                'authority_revision': 7, 'works': []}

    def budget_snapshot(self, attempt_id):
        return encoded(self.state())

    @contextmanager
    def launch_gate(self, attempt_id, work_id, clock, role):
        yield {'token': 'tok'}

    def acknowledge_dispatch(self, *args):
        pass

    def _work(self, state, work_id):
        return {'work_id': work_id, 'state': 'SIGNED'}

    def _retry_parent(self, work):
        return None

    def settle_work(self, attempt_id, work_id, observed):
        self.settled.append(observed)
        return encoded(self.state())

    def record_work_transition(self, attempt_id, work_id, raw, expected_revision):
        self.transitions.append(json.loads(raw)['state'])
        return encoded(self.state())

    def retain_supervision_event(self, raw):
        pass


class Store:
    @contextmanager
    def transaction(self):
        yield SimpleNamespace(execute=lambda *a: SimpleNamespace(fetchone=lambda: None))


def run(tmp_path, monkeypatch, *, progression, exit_after, populated=1, remove_on_exit=False,
        checkpoint='N1'):
    parent = tmp_path / 'fpq.slice'
    kernel = Kernel(parent, exit_after, populated, remove_on_exit)
    observed_populated = []

    class Runtime:
        def __init__(self):
            self.parent = parent

        def observation(self, state, work, enrollment):
            observed_populated.append(kernel.populated())
            return b'{}'

    monkeypatch.setattr(supervisor, 'observe_campaign_clock', kernel.clock)
    monkeypatch.setattr(supervisor.time, 'sleep', kernel.sleep)
    monkeypatch.setattr(supervisor, '_guardian_bus_call', lambda *a: None)
    # g5_unit_spec requires the installed Linux runtime's absolute POSIX paths;
    # pin them so the host's own interpreter and checkout (C:\... on Windows)
    # never reach the unit spec.
    monkeypatch.setattr(supervisor.sys, 'executable', LINUX_INTERPRETER)
    monkeypatch.setattr(runtime, 'installed_code_root', lambda: PurePosixPath(LINUX_CODE_ROOT))
    reservation = base64.b64encode(encoded({'clock': json.loads(kernel.clock())})).decode()
    state = {'attempt_id': 'att1', 'deadline_boottime_ns': START_NS + WALL_NS,
             'profile': {'orchestration_cpu_ns': {'N1_G5': 10**9}}}
    work = {'work_id': 'g5work', 'phase': 'N1_G5', 'reservation_bytes_b64': reservation,
            'limits': {'cpu_ns': 30 * 10**9, 'wall_ns': WALL_NS}}
    enrollment = {'scopes': {'payload_slice': PAYLOAD_SLICE,
                             'guardian_unit': 'fpq-guardian.service'}}
    context = SimpleNamespace(config={'g5_uid': 1234}, store=Store())
    campaigns = Campaigns(progression)
    supervisor._run_n1_g5(context, campaigns, Runtime(), state, work, enrollment, manifest={},
                          checkpoint=checkpoint)
    return kernel, campaigns, observed_populated


@pytest.mark.parametrize('progression', ['N2_READY', 'N1_FAILED'])
def test_commit_before_unit_exit_settles_only_after_the_cgroup_empties(
        tmp_path, monkeypatch, progression):
    kernel, campaigns, observed = run(tmp_path, monkeypatch, progression=progression,
                                      exit_after=3)
    assert observed == [0], 'the settlement observation sampled a still-populated g5 unit'
    assert len(campaigns.settled) == 1
    assert campaigns.transitions == ['COMPLETED']
    assert kernel.sleeps == 3


@pytest.mark.parametrize('progression', ['PART_A_READY', 'N2_FAILED'])
def test_joint_n2_commit_before_unit_exit_settles_only_after_the_cgroup_empties(
        tmp_path, monkeypatch, progression):
    # S4 drives the joint N2 assessment through the same qg5 loop; its commit
    # lands in PART_A_READY/N2_FAILED while the driver is still returning.
    kernel, campaigns, observed = run(tmp_path, monkeypatch, progression=progression,
                                      exit_after=3, checkpoint='N2')
    assert observed == [0], 'the settlement observation sampled a still-populated g5 unit'
    assert len(campaigns.settled) == 1
    assert campaigns.transitions == ['COMPLETED']
    assert kernel.sleeps == 3


def test_a_unit_that_never_exits_is_observed_at_the_bound_not_awaited_forever(
        tmp_path, monkeypatch):
    kernel, campaigns, observed = run(tmp_path, monkeypatch, progression='N2_READY',
                                      exit_after=None)
    # Past RuntimeMax plus the stop grace the observation reports what it sees:
    # a live unit, which settlement records as uncertain. Nothing is waited on
    # beyond the unit's own bound.
    assert observed == [1]
    assert kernel.now >= START_NS + WALL_NS + supervisor.G5_UNIT_STOP_GRACE_NS
    assert kernel.now < START_NS + WALL_NS + supervisor.G5_UNIT_STOP_GRACE_NS + 10**9


def test_a_unit_that_exits_before_any_commit_settles_without_waiting(tmp_path, monkeypatch):
    # The pre-commit exit path is unchanged: an already-empty cgroup ends the
    # loop on its first pass, with no sleep and no wait for a commit.
    kernel, campaigns, observed = run(tmp_path, monkeypatch, progression='BOUND',
                                      exit_after=None, populated=0)
    assert observed == [0]
    assert kernel.sleeps == 0
    assert len(campaigns.settled) == 1


def test_a_removed_unit_cgroup_after_the_commit_is_the_exit(tmp_path, monkeypatch):
    # The realistic Linux shape: the stopped transient unit's cgroup directory
    # disappears. The wait ends on the removal and settles once, never raising.
    kernel, campaigns, observed = run(tmp_path, monkeypatch, progression='N2_READY',
                                      exit_after=2, remove_on_exit=True)
    assert not kernel.group.exists()
    assert observed == [0]
    assert campaigns.transitions == ['COMPLETED']
