"""T00 screen driver: rows S4-S8, S11, S12, S15, B2-B5, X1, X4-X6, integration I1-I3, and the
P-F card note tests (design 2026-10-02 §2.2, §4-§5, §10; build card §2.9, notes 5, 11, 12, PF-1, PF-2).

Real subprocess workers run the real ``SCREEN_BOOTSTRAP`` against a TEST_ONLY code root: a copy of
``ops``/``core`` committed to a throwaway git repository whose module text carries the test pins,
as ``test_p7_evidence`` does (card note item 2): the TEST_ONLY source key and trust constants, the
synthetic case's contract digest in place of r3c's, and the install-tree digest stubbed (card-owner
ruling 2026-10-04 (4), as ``test_screen_authority``). The source is a real ``ProductionSource``
over synthetic ``composition_fixture`` artifacts; ``worker.py`` has no fake-source hook. In this
process only the pinned root and the validator's repository-root constant are replaced (design
§10), plus the same install-tree stub. No test reads the real source.

Crash windows (I1) are rebuilt from one uninterrupted run's own ledger and journals, cut where
the window leaves the durable record. The new modules are imported inside each test, so a missing
module fails the row rather than erroring at collection (card F7). The run machinery is
Windows-only (msvcrt locks, the Job Object); those tests skip elsewhere.
"""
from __future__ import annotations

# Row-named tests (design §10) and shared pytest fixtures:
# pylint: disable=invalid-name,redefined-outer-name,missing-function-docstring,protected-access
# pylint: disable=too-many-lines,import-outside-toplevel

import ast
import base64
from datetime import datetime, timedelta, timezone
import hashlib
import importlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import threading
import time

import pytest

from c1_rail.qualification import p7_evidence, screen_authority
from c1_rail.qualification.contract import canonical_json_bytes as canonical
from c1_rail.qualification.t00_screen import journal, state
from test_p7_evidence import make_code_root
from test_screen_authority import ORB, PREREG, REFUSALS, VAN, pinned_sections, prereg_text, successor
from test_source_contract import build_source_case

pytestmark = pytest.mark.skipif(shutil.which('git') is None, reason='git required for the code-root binding')
WINDOWS = pytest.mark.skipif(os.name != 'nt', reason='the run locks and the Job Object are Windows-only (card §3.4)')

REPO = Path(__file__).resolve().parents[3]
LABEL_SCRIPT = 'scripts/t00_screen_label_check.py'
ENTRY_SCRIPT = 'scripts/t00_screen.py'
FIXTURE_MODULE = 'ops/c1_rail/qualification/t00_screen/journal.py'  # the synthetic P7 record's one module
STUB_TREE = "\n# TEST_ONLY code root override\ndef install_tree_sha256(site, *, base=None):\n    return 'e' * 64\n"
BLOCK = 75
WORKERS = 2
BINARY = getattr(os, 'O_BINARY', 0)
PINNED = (('c1_rail.qualification.contract', 'SOURCE_SIGNING_KEYS'),
          ('c1_rail.qualification.trust_domain', 'SOURCE_TRUST_CONSTANTS'),
          ('c1_rail.qualification.screen_authority', 'REPOSITORY_ROOT'),
          ('c1_rail.qualification.screen_authority', 'R3C_CONTRACT_SHA256'))
_CACHE = {}  # the one uninterrupted run this module compares every window with


def drv():
    return importlib.import_module('c1_rail.qualification.t00_screen.coordinator')


def cli():
    return importlib.import_module('c1_rail.qualification.t00_screen.__main__')


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git(root, *args):
    return subprocess.run(['git', '-C', str(root), '-c', 'user.email=pf@test', '-c', 'user.name=pf-test',
                           '-c', 'core.autocrlf=false', '-c', 'commit.gpgsign=false', *args],
                          check=True, capture_output=True).stdout.decode('utf-8').strip()


def stamp(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def _repo_text(relative):
    path = REPO / relative
    return path.read_text(encoding='utf-8') if path.is_file() else '"""absent at this base"""\n'


class Env:  # pylint: disable=too-many-instance-attributes
    """One TEST_ONLY code root, synthetic source case, P7 record and signed screen authority."""

    def __init__(self, base: Path, monkeypatch, *, code_edits=None):
        self.base, self.monkeypatch = base, monkeypatch
        monkeypatch.setattr(p7_evidence, 'install_tree_sha256', lambda site, base=None: 'e' * 64, raising=False)
        self.artifact_root = base / 'private'
        self.case = build_source_case(self.artifact_root, monkeypatch)
        self.contract_sha256 = sha(self.case.contract_bytes())
        now = datetime.now(timezone.utc)
        self.issued, self.expires = stamp(now - timedelta(hours=1)), stamp(now + timedelta(days=2))
        self.source_approval = self.case.approval(issued_at=self.issued, expires_at=self.expires)
        self.params = {
            'expressions': 'DECLARED_BOOK', 'scenarios': ['S0'],
            'initial_state': dict(self.case.document['initial_state']), 'horizon_sessions': 1500,
            'rng': {'tag': 't00-screen-rng/v1', 'roots': ['root-a', 'root-b', 'root-c'], 'probe_root': 'probe'},
            'depth_per_root': {'FULL': 1, 'H1': 1, 'H2': 1},
            'block': {'family': 'JOINT_FLAT_BOTH_RUNS', 'length_sessions': BLOCK},
            'path_start_date': self.case.document['path_start_date'], 'pass_floor_halves': 'BINDING',
            'deadline_only_is_bust': True, 'run1_diagnostic': 'WAIVED', 'a5_rule': 'T00_A5/v1',
            'median_rule': 'LOWER_NEAREST_RANK_INF_INCLUDED',
            'budget': {'path_cpu_seconds': 1_000_000, 'overhead_cpu_seconds': 1_000_000,
                       'basis': 'TEST_ONLY basis'}}
        self.code = self._code_root(code_edits or {})
        monkeypatch.setattr(screen_authority, 'REPOSITORY_ROOT', self.code)
        monkeypatch.setattr(screen_authority, 'R3C_CONTRACT_SHA256', self.contract_sha256)
        self.record = self._record()
        self.authority = canonical(self._document())
        self.approval = self.screen_approval()
        self.inputs_dir = base / 'inputs'
        self._write_inputs()
        self.pins = {(module, name): getattr(importlib.import_module(module), name) for module, name in PINNED}

    def apply(self, monkeypatch):
        """This environment's in-process pins, for one test (two environments share this module)."""
        monkeypatch.setattr(p7_evidence, 'install_tree_sha256', lambda site, base=None: 'e' * 64, raising=False)
        for (module, name), value in self.pins.items():
            monkeypatch.setattr(importlib.import_module(module), name, value)
        return self

    def _code_root(self, code_edits):
        sections = pinned_sections()
        edits = {
            'ops/c1_rail/qualification/screen_authority.py':
                lambda text: text + f'\n# TEST_ONLY code root override\nR3C_CONTRACT_SHA256 = {self.contract_sha256!r}\n',
            'ops/c1_rail/qualification/p7_evidence.py': lambda text: text + STUB_TREE,
            **code_edits,
        }
        files = {LABEL_SCRIPT: _repo_text(LABEL_SCRIPT), ENTRY_SCRIPT: _repo_text(ENTRY_SCRIPT),
                 'scripts/layer_bootstrap.py': _repo_text('scripts/layer_bootstrap.py'),
                 '.gitignore': '__pycache__/\n',  # as the repository's: an operator launch caches bytecode
                 ORB: successor('| ORB-3 '), VAN: successor('| VAN-3 '),
                 PREREG: prereg_text(sections, self.params, status='DRAFT — NOT RATIFIED')}
        root = make_code_root(self.base / 'code', self.case, edits=edits, extra=files, commit=False)
        git(root, 'init', '-q')
        git(root, 'add', '-A')
        git(root, 'commit', '-q', '-m', 'TEST_ONLY draft')
        (root / PREREG).write_bytes(prereg_text(sections, self.params).encode('utf-8'))
        git(root, 'commit', '-q', '-am', 'TEST_ONLY ratify')
        self.ratifying = git(root, 'rev-parse', 'HEAD')
        (root / PREREG).write_bytes(prereg_text(sections, self.params, ratifying=f'`{self.ratifying}`').encode('utf-8'))
        git(root, 'commit', '-q', '-am', 'TEST_ONLY record the ratifying SHA')
        self.head = git(root, 'rev-parse', 'HEAD')
        git(root, 'update-ref', 'refs/remotes/origin/main', self.head)
        return root

    def _record(self) -> bytes:
        closure = {'first_party': {'c1_rail.qualification.t00_screen.journal': {
                       'path': FIXTURE_MODULE, 'sha256': sha((self.code / FIXTURE_MODULE).read_bytes())}},
                   'third_party': {}, 'distributions': {}, 'stdlib': [], 'ports': {}}
        record = {'schema': p7_evidence.RECORD_SCHEMA, 'contract_sha256': self.contract_sha256,
                  'code_head': self.head, 'bootstrap_sha256': p7_evidence.P7_BOOTSTRAP_SHA256,
                  'code_closure_sha256': sha(p7_evidence.canonical(closure)), 'loaded_closure': closure,
                  'interpreter': p7_evidence.current_interpreter_binding(self.code),
                  'contract_b64': base64.b64encode(self.case.contract_bytes()).decode('ascii'),
                  'approval_b64': base64.b64encode(self.source_approval).decode('ascii'),
                  'result': {'labels': []}}
        return p7_evidence.canonical(record)

    def _document(self) -> dict:
        record = json.loads(self.record)
        return {
            'schema': 't00_screen_authority/v1', 'authority_id': 'TEST_ONLY-screen-authority',
            'purpose': 'T00_STEP3_SELECTED_BOOK_SCREEN', 'grants': ['T00_STEP3_SCREEN_ONCE'], 'refusals': REFUSALS,
            'evidence_class': 'T00_STEP3_SCREEN', 'source': {'contract_sha256': self.contract_sha256},
            'run_root_sha256': sha(str((self.artifact_root / 't00-step3').resolve()).encode('utf-8')),
            'p7': {'record_sha256': sha(self.record), 'code_head': record['code_head'],
                   'code_closure_sha256': record['code_closure_sha256'],
                   'bootstrap_sha256': record['bootstrap_sha256'], 'interpreter': record['interpreter']},
            'prereg': {'path': PREREG, 'ratifying_commit': self.ratifying, 'commit': self.head,
                       'blob_sha256': sha((self.code / PREREG).read_bytes()),
                       'a5_text_sha256': screen_authority.verdict.A5_TEXT_SHA256,
                       'a6_text_sha256': screen_authority.verdict.A6_TEXT_SHA256},
            'a3_answers': [{'path': path, 'commit': self.head, 'blob_sha256': sha((self.code / path).read_bytes())}
                           for path in (ORB, VAN)],
            'parameters': self.params, 'source_trust': self.case.document['source_trust'],
        }

    def screen_approval(self, *, issued=None, expires=None) -> bytes:
        return self.case.approval(scope='APPROVE_T00_SCREEN_AUTHORITY', subject=self.authority,
                                  issued_at=issued or self.issued, expires_at=expires or self.expires)

    def _write_inputs(self):
        self.inputs_dir.mkdir(exist_ok=True)
        for name, raw in (('authority.json', self.authority), ('approval.json', self.approval),
                          ('contract.json', self.case.contract_bytes()), ('source-approval.json', self.source_approval),
                          ('p7-record.json', self.record)):
            (self.inputs_dir / name).write_bytes(raw)
        (self.inputs_dir / 'registry.json').write_text(json.dumps(
            {key: base64.b64encode(raw).decode('ascii') for key, raw in self.case.public_keys.items()}),
            encoding='utf-8')

    @property
    def authority_sha256(self) -> str:
        return sha(self.authority)

    @property
    def run_root(self) -> Path:
        return (self.artifact_root / 't00-step3').resolve()

    @property
    def run_dir(self) -> Path:
        return self.run_root / self.authority_sha256

    def inputs(self, *, approval=None):
        return drv().Inputs(authority=self.authority, approval=approval or self.approval,
                            source_contract=self.case.contract_bytes(), source_approval=self.source_approval,
                            public_keys=dict(self.case.public_keys), p7_record=self.record,
                            artifact_root=self.artifact_root)

    def argv(self, subcommand, *extra):
        names = {'--authority': 'authority.json', '--approval': 'approval.json', '--source-contract': 'contract.json',
                 '--source-approval': 'source-approval.json', '--registry': 'registry.json',
                 '--p7-record': 'p7-record.json'}
        argv = [subcommand]
        for option, name in names.items():
            argv += [option, str(self.inputs_dir / name)]
        return argv + ['--artifact-root', str(self.artifact_root), *extra]

    def act(self, kind, *, head=None):
        doc = {'schema': 't00_screen_act/v1', 'authority_sha256': self.authority_sha256, 'act': kind,
               'ledger_head_sha256': head or ledger_head(self.run_dir), 'statement': f'TEST_ONLY {kind}',
               'readers': [{'name': 'Joshua', 'exposure': 'not seen'}]}
        raw = canonical(doc)
        return raw, self.case.approval(scope='APPROVE_T00_SCREEN_ACT', subject=raw, issued_at=self.issued,
                                       expires_at=self.expires)

    def fresh(self):
        """Set the run root aside (the authority binds its path), so the next state starts empty."""
        if self.run_root.exists():
            os.rename(self.run_root, self.base / f'set-aside-{time.time_ns()}')
        if (self.artifact_root / 'p7_acceptance.json').exists():
            os.rename(self.artifact_root / 'p7_acceptance.json', self.base / f'acceptance-{time.time_ns()}.json')


@pytest.fixture(scope='module')
def built_env(tmp_path_factory):
    with pytest.MonkeyPatch.context() as monkeypatch:
        yield Env(tmp_path_factory.mktemp('t00-driver'), monkeypatch)


@pytest.fixture
def env(built_env, monkeypatch):
    return built_env.apply(monkeypatch)


# ---- run-record helpers ----------------------------------------------------------------------------

def ledger_records(run_dir: Path):
    return drv().read_ledger(run_dir)


def ledger_head(run_dir: Path):
    records = ledger_records(run_dir)
    return journal.record_sha256(records[-1]) if records else None


def ledger_bytes(run_dir: Path) -> bytes:
    return b''.join(path.read_bytes() for path in sorted((run_dir / 'ledger').glob('*.jsonl')))


def kinds(run_dir: Path):
    return [record['type'] for record in ledger_records(run_dir)]


def items(records):
    return [(record['type'], record['body']) for record in records]


def chain(entries):
    """(type, body) pairs as hash-chained records, in memory."""
    out, prev = [], None
    for kind, body in entries:
        record = {'body': body, 'prev_sha256': prev, 'type': kind}
        out.append(record)
        prev = journal.record_sha256(record)
    return out


def write_file(path: Path, entries, *, tail=b''):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | BINARY, 0o644)
    try:
        prev = None
        for kind, body in entries:
            prev = journal.append(fd, kind, body, prev_sha256=prev)
        os.write(fd, tail)
    finally:
        os.close(fd)


def place(env, ledger, journals=None, *, manifest=True, tails=None):
    """A run directory holding exactly this durable record (one crash window)."""
    env.fresh()
    run_dir = env.run_dir
    for sub in ('ledger', 'journal', 'acts', 'errors'):
        (run_dir / sub).mkdir(parents=True, exist_ok=True)
    write_file(run_dir / 'ledger' / '0001.jsonl', ledger)
    for name, entries in (journals or {}).items():
        write_file(run_dir / 'journal' / name, entries, tail=(tails or {}).get(name, b''))
    if manifest:
        shutil.copyfile(full(env)['dir'] / 'manifest.json', run_dir / 'manifest.json')
    return run_dir


def full(env):
    """The uninterrupted run: run -> COMPLETE, finalize, verify, kept as this module's reference."""
    if 'dir' not in _CACHE:
        module = drv()
        env.fresh()
        lines = []
        stop = module.run(env.inputs(), workers=WORKERS, on_launch=lines.append)
        label, results_sha = module.finalize(env.inputs())
        verified = module.verify(env.inputs())
        kept = env.base / 'full-run'
        shutil.copytree(env.run_dir, kept)
        records = ledger_records(kept)
        _CACHE.update(dir=kept, stop=stop, lines=lines, label=label, results_sha=results_sha, verified=verified,
                      records=records, journals=module.read_journals(kept),
                      results=(kept / 'results.json').read_bytes())
    return _CACHE


def upto(env, kind, *, last=False):
    """The reference ledger's (type, body) entries through the first (or last) record of ``kind``."""
    entries = items(full(env)['records'])
    found = [i for i, (k, _) in enumerate(entries) if k == kind]
    return entries[:(found[-1] if last else found[0]) + 1]


def journal_entries(env, name):
    return items(full(env)['journals'][name])


def candidate_journal(env):
    return {'c1-w0.jsonl': journal_entries(env, 'c1-w0.jsonl')}


def segment_journals(env):
    return {name: journal_entries(env, name) for name in full(env)['journals'] if name.startswith('s1-')}


def finish(env, *, resume=True):
    """Resume to its stop (when asked), then finalize; the results bytes."""
    stop = drv().resume(env.inputs(), workers=WORKERS) if resume else None
    drv().finalize(env.inputs())
    return stop, (env.run_dir / 'results.json').read_bytes()


def refused(code, call):
    with pytest.raises(drv().ScreenRefusal) as error:
        call()
    assert error.value.code == code, str(error.value)


# ---- rows S4-S8 (coordinator.run / resume) ----------------------------------------------------------

def _attempt(env, name, prereg_path, *, final=False):
    """Another attempt's directory under the run root: AUTHORITY_BOUND for ``prereg_path``."""
    entries = [('AUTHORITY_BOUND', {'authority_sha256': name, 'prereg_path': prereg_path, 'approvals': [],
                                    'reused_directory': False})]
    if final:
        entries += [('TERMINAL', {'code': 'CORRUPTION'}), ('AGGREGATED', {'results_sha256': 'a' * 64}),
                    ('REPORTED', {'report_sha256': 'b' * 64}), ('FINAL', {'attestation_sha256': 'c' * 64})]
    write_file(env.run_root / name / 'ledger' / '0001.jsonl', entries)


def _scan(env):
    """The run-root scan of rows S6, S4 and S5 alone, with this run's validated authority."""
    module = drv()
    _, auth = module.launch_checks(env.inputs(), datetime.now(timezone.utc))
    module._scan_attempts(env.run_root, auth)


@WINDOWS
def test_S4(env):
    """A second authority after an interrupted first that named the same pre-registration: PREREG_CONSUMED."""
    env.fresh()
    _attempt(env, 'b' * 64, PREREG)
    refused('PREREG_CONSUMED', lambda: drv().run(env.inputs(), workers=WORKERS))
    assert not env.run_dir.exists()
    env.fresh()
    _attempt(env, 'b' * 64, 'docs/briefs/pre-registration/another.md', final=True)
    _scan(env)  # twin: a FINAL attempt under another path neither consumes nor blocks


@WINDOWS
def test_S5(env):
    """An open attempt under another pre-registration path: SCREEN_ATTEMPT_OPEN."""
    env.fresh()
    _attempt(env, 'c' * 64, 'docs/briefs/pre-registration/another.md')
    refused('SCREEN_ATTEMPT_OPEN', lambda: drv().run(env.inputs(), workers=WORKERS))
    assert not env.run_dir.exists()
    env.fresh()
    _attempt(env, 'c' * 64, 'docs/briefs/pre-registration/another.md', final=True)
    _scan(env)  # twin: once FINAL it no longer blocks


@WINDOWS
def test_S6(env):
    """``run`` twice: SCREEN_ALREADY_RUN and no ledger change; a directory without a durable
    AUTHORITY_BOUND is reused under the lock and records the reuse."""
    reference = full(env)
    assert reference['stop'].kind == 'COMPLETE' and 'AUTHORITY_BOUND' == reference['records'][0]['type']
    env.fresh()
    shutil.copytree(reference['dir'], env.run_dir)
    before = ledger_bytes(env.run_dir)
    refused('SCREEN_ALREADY_RUN', lambda: drv().run(env.inputs(), workers=WORKERS))
    assert ledger_bytes(env.run_dir) == before
    env.fresh()
    (env.run_dir / 'ledger').mkdir(parents=True)
    (env.run_dir / 'ledger' / '0001.jsonl').write_bytes(b'{"body":{"authority_sha')  # torn, never durable
    module = drv()
    receipt, auth = module.launch_checks(env.inputs(), datetime.now(timezone.utc))
    ledger, lock = module._bind(env.inputs(), auth, receipt)
    ledger.close()
    lock.release()
    bound = ledger_records(env.run_dir)
    assert [r['type'] for r in bound] == ['AUTHORITY_BOUND'] and bound[0]['body']['reused_directory'] is True


@WINDOWS
def test_S7(env):
    """An untracked file at resume refuses RESUME_LAUNCH_CHECK with the ledger bytes unchanged."""
    place(env, upto(env, 'SEGMENT_END'), {**candidate_journal(env), **segment_journals(env)})
    before = ledger_bytes(env.run_dir)
    stray = env.code / 'stray.txt'
    stray.write_bytes(b'untracked\n')
    try:
        refused('RESUME_LAUNCH_CHECK', lambda: drv().resume(env.inputs(), workers=WORKERS))
    finally:
        os.remove(stray)
    assert ledger_bytes(env.run_dir) == before
    assert drv().resume(env.inputs(), workers=WORKERS).kind == 'COMPLETE'  # twin: a clean tree resumes


def _halted_idle(env):
    """IDLE with every key done (a STOPPED segment), then HALT{UNCLASSIFIED_ERROR, from IDLE}."""
    entries = upto(env, 'SEGMENT_START')
    end = dict(dict(upto(env, 'SEGMENT_END'))['SEGMENT_END'], **{'class': 'STOPPED', 'cause': 'WORKER_LOST'})
    entries += [('SEGMENT_END', end), ('HALT', {'code': 'UNCLASSIFIED_ERROR', 'from': 'IDLE'})]
    return place(env, entries, {**candidate_journal(env), **segment_journals(env)})


@WINDOWS
def test_S8(env):
    """``resume`` refuses from HALTED without CONTINUE, while a lock is held and while an act file
    has no ledger record; after a recorded CONTINUE it resumes."""
    run_dir = _halted_idle(env)
    before = ledger_bytes(run_dir)
    refused('SCREEN_HALTED', lambda: drv().resume(env.inputs(), workers=WORKERS))
    held = drv()._Lock(run_dir / 'lock')
    try:
        refused('SCREEN_WORKERS_ALIVE', lambda: drv().resume(env.inputs(), workers=WORKERS))
    finally:
        held.release()
    raw, approval = env.act('CONTINUE', head='d' * 64)  # binds a stale head: never recordable
    (run_dir / 'acts' / f'{sha(raw)}.json').write_bytes(canonical(
        {'act_b64': base64.b64encode(raw).decode('ascii'), 'approval_b64': base64.b64encode(approval).decode('ascii')}))
    refused('SCREEN_ACT_PENDING', lambda: drv().resume(env.inputs(), workers=WORKERS))
    os.remove(run_dir / 'acts' / f'{sha(raw)}.json')
    assert ledger_bytes(run_dir) == before
    raw, approval = env.act('CONTINUE')  # twin
    assert drv().act(env.inputs(), raw, approval) == ('CONTINUE', sha(raw))
    assert drv().resume(env.inputs(), workers=WORKERS).kind == 'COMPLETE'
    assert kinds(run_dir)[-3:] == ['HALT', 'ACT', 'ALL_DONE']


# ---- rows S11, S12, S15; PF-1 --------------------------------------------------------------------

@WINDOWS
def test_S11(env):
    """A crash between SEGMENT_START and the first spawn: SEGMENT_START (heartbeat 0) is durable, and
    resume charges it one heartbeat interval of wall and interval x W of job CPU, with no loss."""
    module = drv()
    run_dir = place(env, upto(env, 'SEGMENT_START'), candidate_journal(env))
    stop, results = finish(env)
    crashed = next(r['body'] for r in ledger_records(run_dir) if r['type'] == 'SEGMENT_CRASHED')
    start = next(r['body'] for r in ledger_records(run_dir) if r['type'] == 'SEGMENT_START')
    assert crashed == {'k': 1, 'losses': [], 'cap': None,
                       'charge': {'cpu_s': float(module.HEARTBEAT_S * start['w']),
                                  'wall_s': float(module.HEARTBEAT_S)}}
    assert stop.kind == 'COMPLETE' and results == full(env)['results']  # twin: the run completes unchanged


def _process_table():
    """{pid: parent pid} for every process (Toolhelp32)."""
    import ctypes
    from ctypes import wintypes

    class Entry(ctypes.Structure):  # PROCESSENTRY32W
        _fields_ = [('dwSize', wintypes.DWORD), ('cntUsage', wintypes.DWORD), ('th32ProcessID', wintypes.DWORD),
                    ('th32DefaultHeapID', ctypes.c_size_t), ('th32ModuleID', wintypes.DWORD),
                    ('cntThreads', wintypes.DWORD), ('th32ParentProcessID', wintypes.DWORD),
                    ('pcPriClassBase', wintypes.LONG), ('dwFlags', wintypes.DWORD), ('szExeFile', wintypes.WCHAR * 260)]
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    kernel.Process32FirstW.argtypes = kernel.Process32NextW.argtypes = (wintypes.HANDLE, ctypes.c_void_p)
    kernel.CloseHandle.argtypes = (wintypes.HANDLE,)
    snapshot = kernel.CreateToolhelp32Snapshot(0x2, 0)
    entry = Entry()
    entry.dwSize = ctypes.sizeof(entry)
    table = {}
    try:
        found = kernel.Process32FirstW(snapshot, ctypes.byref(entry))
        while found:
            table[entry.th32ProcessID] = entry.th32ParentProcessID
            found = kernel.Process32NextW(snapshot, ctypes.byref(entry))
    finally:
        kernel.CloseHandle(snapshot)
    return table


def _coordinator_process(env, subcommand):
    """The coordinator through the PF-2 entry point at the code root, as its own interpreter process
    (the same base-interpreter launch as PF-1, so the Popen pid is the coordinator itself)."""
    executable, pinned = drv().worker_launch()
    child = {name: value for name, value in os.environ.items() if name != 'PYTHONPATH'}
    child.update({name: value for name, value in pinned.items() if name == '__PYVENV_LAUNCHER__'})
    command = [executable, '-B', str(env.code / ENTRY_SCRIPT), *env.argv(subcommand, '--workers', str(WORKERS))]
    return subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=child, cwd=env.base)


def _await_key_start(run_dir, process, timeout=600):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        folder = run_dir / 'journal'
        if any(b'KEY_START' in path.read_bytes() for path in folder.glob('s*.jsonl')) if folder.is_dir() else False:
            return
        assert process.poll() is None, process.communicate()
        time.sleep(0.2)
    raise AssertionError('no worker started a key')


def _idle(env):
    return place(env, upto(env, 'PROBE'), candidate_journal(env))


@WINDOWS
def test_S12(env):
    """Kill the coordinator: no worker survives (Job Object, kill on close); resume then records the
    crash and the results equal the uninterrupted run's (W22)."""
    run_dir = _idle(env)
    coordinator = _coordinator_process(env, 'resume')
    try:
        _await_key_start(run_dir, coordinator)
        workers = [pid for pid, parent in _process_table().items() if parent == coordinator.pid]
        assert len(workers) == WORKERS
    finally:
        coordinator.kill()
        coordinator.communicate()
    deadline = time.monotonic() + 15
    while set(workers) & set(_process_table()) and time.monotonic() < deadline:
        time.sleep(0.2)
    assert not set(workers) & set(_process_table()), 'a worker outlived the coordinator'
    assert state.fold(ledger_records(run_dir)).name == 'RUNNING'
    stop, results = finish(env)
    assert 'SEGMENT_CRASHED' in kinds(run_dir) and stop.kind == 'COMPLETE'
    assert results == full(env)['results']  # twin: the same run, resumed


@WINDOWS
def test_PF1_worker_parent_is_the_coordinator(env):
    """Amendment PF-1: a worker interpreter's parent (its ``os.getppid()``, row K4) is the
    coordinator's own pid, not a venv redirector; the redirector stays the worker's ``sys.executable``."""
    executable, pinned = drv().worker_launch()
    base = getattr(sys, '_base_executable', sys.executable)
    if os.path.normcase(base) != os.path.normcase(sys.executable):
        assert (executable, pinned['__PYVENV_LAUNCHER__']) == (base, sys.executable)
    run_dir = _idle(env)
    coordinator = _coordinator_process(env, 'resume')
    try:
        _await_key_start(run_dir, coordinator)
        table = _process_table()
        workers = [pid for pid, parent in table.items() if parent == coordinator.pid]
        probe = subprocess.run([executable, '-I', '-S', '-c', 'import os, sys; print(os.getppid(), sys.executable)'],
                               env={**os.environ, **pinned}, capture_output=True, text=True, check=True)
    finally:
        coordinator.kill()
        coordinator.communicate()
    assert len(workers) == WORKERS and all(table[pid] == coordinator.pid for pid in workers)
    parent, child_executable = probe.stdout.split(' ', 1)
    assert int(parent) == os.getpid() and child_executable.strip() == sys.executable


@WINDOWS
def test_S15(env):
    """``finalize`` from STOPPED refuses FINALIZE_NOT_COMPLETE with the ledger bytes unchanged."""
    entries = upto(env, 'SEGMENT_START')
    end = dict(dict(upto(env, 'SEGMENT_END'))['SEGMENT_END'], **{'class': 'STOPPED', 'cause': 'WORKER_LOST'})
    run_dir = place(env, entries + [('SEGMENT_END', end)], {**candidate_journal(env), **segment_journals(env)})
    before = ledger_bytes(run_dir)
    refused('FINALIZE_NOT_COMPLETE', lambda: drv().finalize(env.inputs()))
    assert ledger_bytes(run_dir) == before
    place(env, upto(env, 'SEGMENT_END'), {**candidate_journal(env), **segment_journals(env)})  # twin: COMPLETE
    assert drv().finalize(env.inputs()) == (full(env)['label'], full(env)['results_sha'])


@WINDOWS
def test_finalize_refuses_a_journal_the_ledger_does_not_name(env):
    """Card note item 12: an extra file under journal/ is CORRUPTION at finalize (TERMINAL, so the
    verdict is INSUFFICIENT), even when its own chain is valid."""
    planted = {'s9-w0.jsonl': [('WORKER_STOP', {'reason': 'DONE', 'key': None})]}
    run_dir = place(env, upto(env, 'SEGMENT_END'), {**candidate_journal(env), **segment_journals(env), **planted})
    label, _ = drv().finalize(env.inputs())
    assert label == 'INSUFFICIENT' and {'type': 'TERMINAL', 'body': {'code': 'CORRUPTION'}}.items() <= \
        next(r for r in ledger_records(run_dir) if r['type'] == 'TERMINAL').items()
    place(env, upto(env, 'SEGMENT_END'), {**candidate_journal(env), **segment_journals(env)})  # twin
    assert drv().finalize(env.inputs())[0] == full(env)['label']


# ---- rows B2-B5 ----------------------------------------------------------------------------------

@WINDOWS
def test_B2(env):
    """A crash between PROBE_START and PROBE HALTs PROBE_INTERRUPTED; CONTINUE returns it to PREPARED,
    from which the probe is timed again (never scored)."""
    entries = upto(env, 'PROBE_START')
    cut = journal_entries(env, 'c1-w0.jsonl')[:4]  # the probe epoch opened, no PROBE_RESULT
    run_dir = place(env, entries, {'c1-w0.jsonl': cut})
    stop = drv().resume(env.inputs(), workers=WORKERS)
    assert (stop.kind, stop.code) == ('HALTED', 'PROBE_INTERRUPTED')
    assert ledger_records(run_dir)[-1]['body'] == {'code': 'PROBE_INTERRUPTED', 'from': 'PROBING'}
    raw, approval = env.act('CONTINUE')
    drv().act(env.inputs(), raw, approval)
    assert state.fold(ledger_records(run_dir)).name == 'PREPARED'  # twin: the probe re-times from here


def test_B3():
    """A probe projection one second over the path budget is PROBE_OVER_BUDGET; at the budget it passes."""
    module = drv()
    assert module.probe_refusal(10.0, 100, 999) == 'PROBE_OVER_BUDGET'
    assert module.probe_refusal(10.0, 100, 1000) is None
    assert state.classify('PROBE_OVER_BUDGET') == ('TERMINAL', 'PROBE_OVER_BUDGET')


def _path_body(key, cpu):
    run = {'digest': 'a' * 64, 'sessions': 1500, 'fills': 0, 'events_sha256': 'b' * 64, 'deadline_failure': False,
           'consumed_intrabar_split_count': 0, 'consumed_intrabar_splits_sha256': 'c' * 64, 'status': 'PASS',
           'sessions_to_pass': 4, 'failure_reason': None, 'kernel_outcome': 'pass'}
    return {'key': list(key), 'seed': 1, 'path_sha256': 'd' * 64, 'bracket_status': 'PASS',
            'runs': {'r1': run, 'r2': dict(run)}, 'wall_s': cpu, 'cpu_s': cpu}


def test_B4():
    """The gate books the first PATH of each plan key only; with a budget equal to the sum of every
    path but the last, the last key is never dispatched and the segment ends BUDGET_EXHAUSTED."""
    module = drv()
    keys = [('r', 'FULL', i) for i in range(4)]
    cpu = [3.0, 5.0, 7.0, 11.0]
    shares, _ = module.assignment(keys, 1)

    def drive(budget):
        gate = module.Dispatcher(shares, [], booked=0.0, budget=budget, completed=set())
        sent = []
        while (key := gate.next(0)) is not None:
            sent.append(key)
            gate.report(key, cpu[key[2]])
        return gate, sent
    gate, sent = drive(sum(cpu[:-1]))
    assert sent == keys[:-1] and gate.refused
    assert module.provisional_cause(['DONE'], interrupted=False, refused=gate.refused, complete=False) == \
        'BUDGET_EXHAUSTED'
    gate, sent = drive(sum(cpu[:-1]) + 1)  # twin: one second more and the run is scored, overrun recorded
    assert sent == keys and not gate.refused and gate.booked > sum(cpu[:-1]) + 1
    journals = {'s1-w0.jsonl': chain([('KEY_START', {'key': list(keys[0])}), ('PATH', _path_body(keys[0], 3.0))]),
                's2-w0.jsonl': chain([('KEY_START', {'key': list(keys[0])}), ('PATH', _path_body(keys[0], 99.0)),
                                      ('KEY_START', {'key': list(keys[1])}), ('PATH', _path_body(keys[1], 5.0))])}
    assert module.booked_path_cpu(journals, keys) == 8.0  # the witness duplicate is overhead


def test_B5():
    """Repeated kills exhaust the overhead reserve; it HALTs (never TERMINAL) and a CONTINUE that
    answers OVERHEAD_EXHAUSTED resets it."""
    module = drv()
    entries = [('PROBE', {'path_cpu_s': 10.0, 'path_wall_s': 10.0, 'peak_memory_bytes': 1})]
    for k in range(1, 4):
        entries += [('SEGMENT_START', {'k': k, 'w': 2, 'assignment_sha256': 'a' * 64, 'witness_keys': [],
                                       'approvals': []})]
        charge = module.crash_charge(chain(entries), {}, k=k, w=2)
        assert charge == {'cpu_s': 2.0 * module.HEARTBEAT_S, 'wall_s': float(module.HEARTBEAT_S)}
        entries += [('SEGMENT_CRASHED', {'k': k, 'charge': charge, 'losses': [], 'cap': None})]
    used = module.overhead_used(chain(entries), {})
    assert used == 10.0 + 6 * module.HEARTBEAT_S
    assert used >= used - 1 and state.classify('OVERHEAD_EXHAUSTED') == ('HALTED', 'OVERHEAD_EXHAUSTED')
    halted = entries + [('HALT', {'code': 'OVERHEAD_EXHAUSTED', 'from': 'IDLE'}),
                        ('ACT', {'act_sha256': 'e' * 64, 'act': 'CONTINUE'})]
    assert module.overhead_used(chain(halted), {}) == 0.0  # twin: the answered reserve starts again


# ---- card note item 5: caps at SEGMENT_END ------------------------------------------------------

def _cap_record(cause_of_last):
    """One key, two STOPPED IO_ERROR segments that each lost it, and an open third that lost it again."""
    key = ('r', 'FULL', 0)
    populations = {'FULL': {'indices': [0], 'candidates_sha256': 'a' * 64},
                   'H1': {'indices': [0], 'candidates_sha256': 'a' * 64},
                   'H2': {'indices': [0], 'candidates_sha256': 'a' * 64}}
    manifest = {'authority_sha256': 'f' * 64, 'contract_sha256': 'f' * 64, 'p7_record_sha256': 'f' * 64,
                'code_head': '0' * 40, 'populations': populations, 'plan_sha256': 'f' * 64}
    cost = {'cpu_s': 1.0, 'wall_s': 1.0}
    entries = [('AUTHORITY_BOUND', {'authority_sha256': 'f' * 64, 'prereg_path': PREREG, 'approvals': [],
                                    'reused_directory': False}),
               ('PREPARED', {'manifest_sha256': sha(canonical(manifest)), 'build': cost, 'integrity': cost}),
               ('PROBE_START', {}), ('PROBE', {'path_cpu_s': 1.0, 'path_wall_s': 1.0, 'peak_memory_bytes': 1})]
    _, digest = drv().assignment([key], 1)
    end = {'class': 'STOPPED', 'cause': 'IO_ERROR', 'workers': [{'worker': 'w', 'reason': 'IO_ERROR'}], 'wall_s': 1.0,
           'job_cpu_s': 1.0, 'path_cpu_s': 0.0, 'overhead_cpu_s': 1.0, 'peak_memory_bytes': 1}
    journals = {}
    for k in (1, 2, 3):
        entries.append(('SEGMENT_START', {'k': k, 'w': 1, 'assignment_sha256': digest, 'witness_keys': [],
                                          'approvals': []}))
        journals[f's{k}-w0.jsonl'] = chain([('KEY_START', {'key': list(key)}),
                                            ('WORKER_STOP', {'reason': 'IO_ERROR', 'key': None})])
        if k < 3:
            entries.append(('SEGMENT_END', end))
    return entries, journals, manifest, [key], cause_of_last


def test_segment_end_caps_iterate_to_a_fixed_point():
    """Note item 5: an INTERRUPTED segment whose first cap call gives IO_EXHAUSTED reaches
    RESOURCE_EXHAUSTED once its losses count; the coordinator writes the fixed point, which
    check_record accepts, while the single-call answer is CORRUPTION."""
    module = drv()
    entries, journals, manifest, keys, cause = _cap_record('INTERRUPTED')
    ledger = chain(entries)
    assert state.cap_finding(ledger, journals, keys=keys, cause=cause, reasons=['IO_ERROR']) == 'IO_EXHAUSTED'
    cls, written = module.segment_cause(ledger, journals, keys, cause, ['IO_ERROR'])
    assert (cls, written) == ('HALTED', 'RESOURCE_EXHAUSTED')

    def check(code):
        end = {'class': 'HALTED', 'cause': code, 'workers': [{'worker': 'w', 'reason': 'IO_ERROR'}], 'wall_s': 1.0,
               'job_cpu_s': 1.0, 'path_cpu_s': 0.0, 'overhead_cpu_s': 1.0, 'peak_memory_bytes': 1}
        return state.check_record(chain(entries + [('SEGMENT_END', end)]), journals, manifest, {}, keys=keys,
                                  trusted_keys={}, now=datetime.now(timezone.utc)).code
    assert check(written) == 'RESOURCE_EXHAUSTED'
    assert check('IO_EXHAUSTED') == 'CORRUPTION'


def test_segment_end_terminal_cause_at_a_cap_stays_terminal():
    """Note item 5: a TERMINAL provisional cause at a reached cap is written unchanged."""
    entries, journals, _, keys, _ = _cap_record('CONTEXT_REFUSAL')
    assert drv().segment_cause(chain(entries), journals, keys, 'CONTEXT_REFUSAL', ['IO_ERROR']) == \
        ('TERMINAL', 'CONTEXT_REFUSAL')
    assert state.cap_finding(chain(entries), journals, keys=keys, cause='CONTEXT_REFUSAL', reasons=['IO_ERROR'])


# ---- rows X1, X4-X6 --------------------------------------------------------------------------------

def _main(argv):
    out, err = io.StringIO(), io.StringIO()
    status = cli().main(argv, stdout=out, stderr=err)
    return status, out.getvalue().splitlines(), err.getvalue().splitlines()


@WINDOWS
def test_X1(env, tmp_path):
    """Each subcommand prints only its fixed lines (design §5.6); stderr carries one code only."""
    digest = env.authority_sha256
    reference = full(env)
    assert _main(env.argv('preflight')) == (0, [f'T00_SCREEN_PREFLIGHT OK authority_sha256={digest}'], [])
    place(env, upto(env, 'SEGMENT_END'), {**candidate_journal(env), **segment_journals(env)})
    assert _main(env.argv('resume')) == (0, [f'T00_SCREEN_RUN authority_sha256={digest}', 'T00_SCREEN_COMPLETE'], [])
    assert _main(env.argv('run')) == (3, [], ['SCREEN_ALREADY_RUN'])
    assert _main(env.argv('finalize')) == (
        0, [f"T00_SCREEN_VERDICT {reference['label']} results_sha256={reference['results_sha']}"], [])
    assert _main(env.argv('verify')) == (0, ['T00_SCREEN_VERIFY VERIFIED'], [])
    _halted_idle(env)
    raw, approval = env.act('TERMINATE')
    (tmp_path / 'act.json').write_bytes(raw)
    (tmp_path / 'act-approval.json').write_bytes(approval)
    assert _main(env.argv('act', '--act', str(tmp_path / 'act.json'), '--act-approval',
                          str(tmp_path / 'act-approval.json'))) == (
        0, [f'T00_SCREEN_ACT_RECORDED TERMINATE act_sha256={sha(raw)}'], [])
    assert _main(env.argv('resume')) == (
        0, [f'T00_SCREEN_RUN authority_sha256={digest}', 'T00_SCREEN_TERMINAL OPERATOR_TERMINATED'], [])
    assert _main(['finalize']) == (2, [], ['USAGE'])
    # accept-p7: a real P7 record at the code root, accepted by re-execution; a non-canonical one refused.
    record = _p7_record(env, tmp_path)
    registry = str(env.inputs_dir / 'registry.json')
    common = ['--artifact-root', str(env.artifact_root), '--registry', registry]
    (tmp_path / 'bad-record.json').write_bytes(record + b' ')
    assert _main(['accept-p7', '--p7-record', str(tmp_path / 'bad-record.json'), *common]) == (
        3, [], ['P7_RECORD_NOT_CANONICAL'])
    status, out, err = _main(['accept-p7', '--p7-record', str(tmp_path / 'p7-record.json'), *common])
    acceptance = (env.artifact_root / 'p7_acceptance.json').read_bytes()
    assert (status, out, err) == (0, [f'T00_SCREEN_P7_ACCEPTED acceptance_sha256={sha(acceptance)}'], [])


def _p7_record(env, tmp_path) -> bytes:
    """One real P7 run at the code root over three FULL sessions (the P7 procedure's own launcher)."""
    sessions = json.loads(env.case.payloads['population_index'])['populations']['FULL'][:3]
    (tmp_path / 'path.json').write_text(json.dumps({'sessions': sessions}), encoding='utf-8')
    out = tmp_path / 'p7-record.json'
    done = p7_evidence.run_p7(code_root=env.code, contract_path=env.inputs_dir / 'contract.json',
                              approval_path=env.inputs_dir / 'source-approval.json',
                              registry_path=env.inputs_dir / 'registry.json', artifact_root=env.artifact_root,
                              path_spec_path=tmp_path / 'path.json', out_path=out)
    assert out.exists(), done.stderr[-3000:]
    return out.read_bytes()


@WINDOWS
def test_X4(env):
    """``verify`` under an expired screen approval is VERIFY_BLOCKED_APPROVAL_EXPIRED, never VERIFIED."""
    reference = full(env)
    assert reference['verified'] == 'VERIFIED'  # twin, inside the gate with k hash-derived keys
    verify_start = next(r['body'] for r in reference['records'] if r['type'] == 'VERIFY_START')
    assert len(verify_start['keys']) == 9
    env.fresh()
    shutil.copytree(reference['dir'], env.run_dir)
    before = ledger_bytes(env.run_dir)
    now = datetime.now(timezone.utc)
    expired = env.screen_approval(issued=stamp(now - timedelta(hours=3)), expires=stamp(now - timedelta(hours=1)))
    assert drv().verify(env.inputs(approval=expired)) == 'VERIFY_BLOCKED_APPROVAL_EXPIRED'
    assert ledger_bytes(env.run_dir) == before


def _imports(tree):
    names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names += [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            names += [(node.module or '')] + [f'{node.module}.{alias.name}' for alias in node.names]
    return names


def verdict_imports(source: str):
    return [name for name in _imports(ast.parse(source))
            if name.startswith('c1_rail') or 't00_screen' in name or name.endswith('verdict')]


def test_X5(tmp_path):
    """The label recompute imports nothing from ``t00_screen.verdict`` (nor any c1_rail module), and
    labels from #581 A5/A6 alone."""
    source = (REPO / LABEL_SCRIPT).read_text(encoding='utf-8')
    assert verdict_imports(source) == []
    planted = source + '\nfrom c1_rail.qualification.t00_screen import verdict\n'
    assert verdict_imports(planted)
    spec = importlib.util.spec_from_file_location('t00_label_check', REPO / LABEL_SCRIPT)
    label = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(label)
    params = {'depth_per_root': {'FULL': 1, 'H1': 1, 'H2': 1}, 'rng': {'roots': ['a']}, 'horizon_sessions': 1500,
              'deadline_only_is_bust': True, 'pass_floor_halves': 'BINDING'}

    def run(status, stp=None, reason=None, kernel='pass'):
        return {'status': status, 'sessions_to_pass': stp, 'failure_reason': reason, 'kernel_outcome': kernel}
    passing = run('PASS', 4)
    split = {'r1': passing, 'r2': run('UNRESOLVED', None, 'horizon_cap', 'horizon_cap')}
    outcomes = [{'key': ['a', p, 0], 'runs': {'r1': passing, 'r2': passing}} for p in ('FULL', 'H1', 'H2')]
    assert label.label(outcomes, params, []) == 'GO-evidence'
    assert label.label(outcomes, params, ['BUDGET_EXHAUSTED']) == 'INSUFFICIENT'
    undetermined = [dict(outcomes[0], runs=split)] + outcomes[1:]
    assert label.label(undetermined, params, []) == 'NO-GO-evidence-UNDETERMINED-dependent'
    bust = run('FAILURE', None, 'bust_daily', 'bust_daily')
    assert label.label([dict(outcomes[0], runs={'r1': bust, 'r2': bust})] + outcomes[1:], params, []) == \
        'NO-GO-evidence-robust'
    assert label.label(outcomes[:2], params, []) == 'INSUFFICIENT'  # H2 short of its depth


SCREEN_SCAN = ('ops/c1_rail/qualification/screen_authority.py', 'ops/c1_rail/qualification/t00_screen')


def result_reads(source: str):
    """Reads of a ``result`` key: ``x['result']`` or ``x.get('result')`` (row X6)."""
    found = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Constant) and node.slice.value == 'result':
            found.append(node.lineno)
        elif (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == 'get'
              and node.args and isinstance(node.args[0], ast.Constant) and node.args[0].value == 'result'):
            found.append(node.lineno)
    return found


def test_X6():
    """P7 enters only as a precondition: nothing in the screen package or screen_authority reads a
    P7 record's ``result`` field."""
    paths = [REPO / SCREEN_SCAN[0]] + sorted((REPO / SCREEN_SCAN[1]).glob('*.py'))
    assert REPO / SCREEN_SCAN[1] / 'coordinator.py' in paths
    assert {str(path): result_reads(path.read_text(encoding='utf-8')) for path in paths} == \
        {str(path): [] for path in paths}
    planted = (REPO / SCREEN_SCAN[1] / 'coordinator.py').read_text(encoding='utf-8') + \
        '\n\ndef leak(record):\n    return record["result"], record.get("result")\n'
    assert len(result_reads(planted)) == 2


# ---- card note item 12: the worker's write-path hook ------------------------------------------------

PLANTED_WRITES = '''

# TEST_ONLY planted write (card note item 12): runs at import, inside the worker, swallowed.
def _t00_planted():
    import os, shutil, sys
    case = os.path.join(sys.argv[2], 'case') if len(sys.argv) > 2 else ''
    if not os.path.isfile(case):
        return
    with open(case, encoding='utf-8') as handle:
        event, target = handle.read().split('\\n', 1)
    actions = {'os.rename': lambda: os.replace(target, target + '.moved'),
               'os.link': lambda: os.link(target, target + '.link'),
               'os.symlink': lambda: os.symlink(target, target + '.sym'),
               'os.truncate': lambda: os.truncate(target, 0),
               'os.remove': lambda: os.remove(target),
               'os.rmdir': lambda: os.rmdir(target + '.dir'),
               'os.mkdir': lambda: os.mkdir(target + '.new'),
               'shutil.rmtree': lambda: shutil.rmtree(target + '.dir')}
    try:
        actions[event]()
    except Exception:
        pass


_t00_planted()
'''
WRITE_EVENTS = ('os.rename', 'os.link', 'os.symlink', 'os.truncate', 'os.remove', 'os.rmdir', 'os.mkdir',
                'shutil.rmtree')


@pytest.fixture(scope='module')
def planted_root(tmp_path_factory):
    base = tmp_path_factory.mktemp('t00-writes')
    with pytest.MonkeyPatch.context() as monkeypatch:  # its in-process pins are undone at once
        case = build_source_case(base / 'private', monkeypatch)
    plan = 'ops/c1_rail/qualification/t00_screen/plan.py'
    return make_code_root(base / 'code', case, edits={plan: lambda text: text + PLANTED_WRITES}), base


def _write_case(planted_root, event):
    """One worker under the real bootstrap whose import chain attempts ``event`` and swallows it."""
    root, base = planted_root
    work = base / f'{event}-{time.time_ns()}'
    run_dir, target = work / 'run', work / 'target'
    (run_dir / 'journal').mkdir(parents=True)
    target.write_bytes(b'kept\n')
    (work / 'target.dir').mkdir()
    if event is not None:
        (run_dir / 'case').write_text(f'{event}\n{target}', encoding='utf-8')
    executable, env = drv().worker_launch()
    done = subprocess.run([executable, '-I', '-S', '-B', '-c', p7_evidence.SCREEN_BOOTSTRAP, str(root),
                           str(run_dir), 'a' * 64, 's1-w0.jsonl'], input=b'', capture_output=True, env=env,
                          cwd=run_dir, timeout=600, check=False)
    records = journal.read(run_dir / 'journal' / 's1-w0.jsonl', prev_sha256=None) \
        if (run_dir / 'journal' / 's1-w0.jsonl').exists() else ()
    untouched = (target.read_bytes() == b'kept\n' and (work / 'target.dir').is_dir()
                 and not any((work / f'target{suffix}').exists() for suffix in ('.moved', '.link', '.sym', '.new')))
    return done, records, untouched


def _write_path_test(event):
    @WINDOWS
    def test(planted_root):
        done, records, untouched = _write_case(planted_root, event)
        assert untouched, f'{event} reached the file system'
        assert done.returncode != 0
        assert records and records[-1]['type'] == 'WORKER_STOP', done.stderr[-3000:]
        assert records[-1]['body'] == {'reason': 'SCREEN_WRITE_REFUSED', 'key': None}
        assert 'PATH' not in [r['type'] for r in records]
        if event == WRITE_EVENTS[0]:  # twin: without the planted write the same worker stops for its own reason
            done, records, untouched = _write_case(planted_root, None)
            assert untouched and records[-1]['body'] == {'reason': 'INTERRUPTED', 'key': None}, done.stderr[-3000:]
    test.__name__ = 'test_worker_write_path_' + event.replace('.', '_')
    test.__doc__ = f'Card note item 12: {event} inside the worker is refused and recorded, so the worker ' \
                   'appends no PATH and stops SCREEN_WRITE_REFUSED with key null.'
    return test


for _event in WRITE_EVENTS:
    globals()['test_worker_write_path_' + _event.replace('.', '_')] = _write_path_test(_event)


@WINDOWS
def test_worker_real_import_smoke(env):
    """The full worker import chain (candidate pass, probe, segment and verify keys) runs under the
    write-path hook with no refusal: every worker stops DONE."""
    reference = full(env)
    stops = {name: records[-1]['body'] for name, records in reference['journals'].items()}
    assert set(stops) == {'c1-w0.jsonl', 's1-w0.jsonl', 's1-w1.jsonl', 'v1-w0.jsonl'}
    assert all(body == {'reason': 'DONE', 'key': None} for body in stops.values()), stops


# ---- integration I1-I3 -----------------------------------------------------------------------------

def _w0(env):
    run_dir = place(env, upto(env, 'AUTHORITY_BOUND'), {'c1-w0.jsonl': journal_entries(env, 'c1-w0.jsonl')[:1]},
                    manifest=False)
    stop = drv().resume(env.inputs(), workers=WORKERS)
    assert (stop.kind, stop.code) == ('HALTED', 'UNCLASSIFIED_ERROR')
    raw, approval = env.act('CONTINUE')
    drv().act(env.inputs(), raw, approval)
    assert state.fold(ledger_records(run_dir)).name == 'BOUND'
    result = finish(env)
    crashed = drv().read_journals(run_dir)['c1-w0.jsonl'][0]['body']  # its EPOCH_OPEN, never PREPARED
    charged = drv().HEARTBEAT_S + crashed['build']['cpu_s'] + crashed['integrity']['cpu_s']
    assert drv().overhead_used(ledger_records(run_dir), drv().read_journals(run_dir)) >= charged
    return run_dir, result


def _w1(env):
    cut = journal_entries(env, 'c1-w0.jsonl')
    cut = cut[:next(i for i, (k, _) in enumerate(cut) if k == 'EPOCH_CLOSE') + 1]
    return place(env, upto(env, 'PREPARED'), {'c1-w0.jsonl': cut}), finish(env)


def _cut_segment(env, *, ended):
    """Segment 1 cut mid-path: worker 0 has one PATH and its next key in flight; worker 1 three
    PATHs and a torn final line (W3)."""
    first, second = (journal_entries(env, f's1-w{i}.jsonl') for i in (0, 1))
    starts0 = [i for i, (k, _) in enumerate(first) if k == 'KEY_START']
    paths1 = [i for i, (k, _) in enumerate(second) if k == 'PATH']
    journals = {**candidate_journal(env), 's1-w0.jsonl': first[:starts0[1] + 1], 's1-w1.jsonl': second[:paths1[2] + 1]}
    entries = upto(env, 'SEGMENT_START')
    if ended:  # W2: the live coordinator saw both workers lost
        end = dict(dict(upto(env, 'SEGMENT_END'))['SEGMENT_END'],
                   **{'class': 'STOPPED', 'cause': 'WORKER_LOST',
                      'workers': [{'worker': 's1-w0.jsonl', 'reason': 'WORKER_LOST'},
                                  {'worker': 's1-w1.jsonl', 'reason': 'WORKER_LOST'}]})
        entries = entries + [('SEGMENT_END', end)]
    else:  # W22: the coordinator itself died after one heartbeat
        entries = entries + [('HEARTBEAT', {'wall_s': 5.0, 'job_cpu_s': 9.0})]
    return place(env, entries, journals, tails={'s1-w1.jsonl': b'{"body":{"key":["root-'})


def _w2(env):
    run_dir = _cut_segment(env, ended=True)
    return run_dir, finish(env)


def _w22(env):
    run_dir = _cut_segment(env, ended=False)
    result = finish(env)
    crashed = next(r['body'] for r in ledger_records(run_dir) if r['type'] == 'SEGMENT_CRASHED')
    in_flight = journal_entries(env, 's1-w0.jsonl')[[i for i, (k, _) in enumerate(journal_entries(
        env, 's1-w0.jsonl')) if k == 'KEY_START'][1]][1]['key']
    assert crashed['losses'] == [in_flight] and crashed['charge']['wall_s'] == 5.0 + drv().HEARTBEAT_S
    return run_dir, result


def _w5(env):
    """Every completed PATH altered (re-chained): the resume witness re-executes one and diverges."""
    def altered(entries):
        out = []
        for kind, body in entries:
            if kind == 'PATH':
                body = dict(body, runs=dict(body['runs'], r1=dict(body['runs']['r1'], fills=body['runs']['r1']['fills'] + 1)))
            out.append((kind, body))
        return out
    run_dir = _cut_segment(env, ended=True)
    for name in ('s1-w0.jsonl', 's1-w1.jsonl'):
        entries = items(journal.read(run_dir / 'journal' / name, prev_sha256=None))
        write_file(run_dir / 'journal' / name, altered(entries))
    return run_dir, finish(env)


def _w6(env):
    entries = upto(env, 'AGGREGATED')
    return place(env, entries, {**candidate_journal(env), **segment_journals(env)}), finish(env, resume=False)


def _w7(env):
    entries = upto(env, 'REPORTED')
    run_dir = place(env, entries, {**candidate_journal(env), **segment_journals(env)})
    shutil.copyfile(full(env)['dir'] / 'results.json', run_dir / 'results.json')
    return run_dir, finish(env, resume=False)


def _w16(env):
    run_dir = _idle(env)
    raw, approval = env.act('TERMINATE')
    drv().act(env.inputs(), raw, approval)
    return run_dir, finish(env, resume=False)


def _w17(env):
    run_dir = _cut_segment(env, ended=True)
    entries = items(journal.read(run_dir / 'journal' / 's1-w1.jsonl', prev_sha256=None))
    outside = ['root-z', 'FULL', 0]
    write_file(run_dir / 'journal' / 's1-w1.jsonl',
               entries + [('KEY_START', {'key': outside}), ('PATH', _path_body(outside, 1.0))])
    return run_dir, finish(env)


def _w9(env):
    """The dispatch gate mid-segment: the booked path CPU sits just under the budget, so each worker
    is sent one more key and the next dispatch is refused with keys left."""
    run_dir = _cut_segment(env, ended=True)
    journals = drv().read_journals(run_dir)
    others = drv().booked_path_cpu(journals, drv().plan_keys(env.params))
    entries = items(journals['s1-w0.jsonl'])
    first = next(i for i, (kind, _) in enumerate(entries) if kind == 'PATH')
    body = entries[first][1]
    budget = env.params['budget']['path_cpu_seconds']
    entries[first] = ('PATH', dict(body, cpu_s=budget - (others - body['cpu_s']) - 0.01))
    write_file(run_dir / 'journal' / 's1-w0.jsonl', entries)
    stop, results = finish(env)
    end = [r['body'] for r in ledger_records(run_dir) if r['type'] == 'SEGMENT_END'][-1]
    assert (end['class'], end['cause']) == ('TERMINAL', 'BUDGET_EXHAUSTED')
    done = {tuple(o['key']) for o in journal.outcomes(drv().read_journals(run_dir), drv().plan_keys(env.params))}
    assert done != set(drv().plan_keys(env.params))  # refused with keys left: never scored
    return run_dir, (stop, results)


# window -> (builder, the stop class and code the run reaches, whether the results equal the reference)
WINDOWS_I1 = {
    'W0': (_w0, ('COMPLETE', None), True),
    'W1': (_w1, ('COMPLETE', None), True),
    'W2': (_w2, ('COMPLETE', None), True),
    'W5': (_w5, ('COMPLETE', None), 'NONDETERMINISM'),
    'W6': (_w6, None, True),
    'W7': (_w7, None, True),
    'W9': (_w9, ('TERMINAL', 'BUDGET_EXHAUSTED'), 'BUDGET_EXHAUSTED'),
    'W16': (_w16, None, 'OPERATOR_TERMINATED'),
    'W17': (_w17, ('TERMINAL', 'CORRUPTION'), 'CORRUPTION'),
    'W22': (_w22, ('COMPLETE', None), True),
}


@WINDOWS
@pytest.mark.parametrize('window', sorted(WINDOWS_I1))
def test_I1(env, window):
    """Every crash window of design §4.4 rebuilt from its own durable prefix (W3 inside W2/W22, W4
    and W13/W23 in rows S13/S10/B5, W8 in X4, W11 in S7, W14 in S8, W21 in B2): the final
    results.json equals the uninterrupted run's bytes, or the stated class is reached."""
    builder, expected_stop, results_equal = WINDOWS_I1[window]
    run_dir, (stop, results) = builder(env)
    if expected_stop is not None:
        assert (stop.kind, stop.code) == expected_stop
    if results_equal is True:
        assert results == full(env)['results']
    else:
        codes = drv().terminal_codes(ledger_records(run_dir))
        assert results_equal in codes and json.loads(results)['verdict']['kind'] == 'INSUFFICIENT'
    assert state.fold(ledger_records(run_dir)).name == 'FINAL'


@WINDOWS
@pytest.mark.skipif(sys.prefix == sys.base_prefix, reason='fp.py runs only a virtual environment')
def test_I2(env):
    """Ctrl-C through the launcher (``fp.py python scripts/t00_screen.py resume``, PF-2), then resume
    (card amendment PF-3, as refined: on a Windows venv fp.py's kill reaches the venv redirector,
    not the coordinator interpreter, which stops on the same Ctrl-C; W22 stays with test_S12 and
    I1[W22]). Asserts: (1) the ledger ends in SEGMENT_END STOPPED ``INTERRUPTED``; (2) once that is
    written and the run lock released, none of the coordinator's or workers' PIDs, recorded before
    the interrupt, is alive; (3) resume completes with the same results."""
    run_dir = _idle(env)
    venv = sys.prefix
    # A console's Ctrl-C reaches only processes that have not inherited "ignore Ctrl-C"; this
    # wrapper re-enables it for the launcher it starts (and ignores the interrupt itself).
    wrap = ('import ctypes, signal, subprocess, sys\nctypes.windll.kernel32.SetConsoleCtrlHandler(None, False)\n'
            'signal.signal(signal.SIGINT, signal.SIG_IGN)\nraise SystemExit(subprocess.call(sys.argv[1:]))')
    command = [sys.executable, '-c', wrap, sys.executable, '-I', str(REPO / 'scripts' / 'fp.py'), '--env', venv,
               'python', str(env.code / ENTRY_SCRIPT), *env.argv('resume', '--workers', str(WORKERS))]
    child = {name: value for name, value in os.environ.items() if name != 'PYTHONPATH'}
    launcher = subprocess.Popen(command, cwd=REPO, env=child, creationflags=subprocess.CREATE_NEW_CONSOLE)
    try:
        _await_key_start(run_dir, launcher)
        table = _process_table()
        run_pids, frontier = {}, {launcher.pid}
        while frontier:  # every process the launcher started, recorded before the interrupt
            frontier = {pid for pid, parent in table.items() if parent in frontier and pid not in run_pids}
            run_pids.update({pid: table[pid] for pid in frontier})
        children = {pid: [c for c, parent in run_pids.items() if parent == pid] for pid in run_pids}
        coordinator = max(run_pids, key=lambda pid: len(children[pid]))
        assert len(children[coordinator]) == WORKERS  # PF-1: the workers' parent is the coordinator
        signal = ('import ctypes, sys\nk = ctypes.windll.kernel32\nk.FreeConsole()\n'
                  'assert k.AttachConsole(int(sys.argv[1]))\nk.SetConsoleCtrlHandler(None, True)\n'
                  'assert k.GenerateConsoleCtrlEvent(0, 0)\n')
        subprocess.run([sys.executable, '-c', signal, str(launcher.pid)], check=True, timeout=60,
                       creationflags=subprocess.CREATE_NO_WINDOW)
        launcher.wait(timeout=120)
    finally:
        if launcher.poll() is None:
            launcher.kill()
    deadline = time.monotonic() + 300  # the coordinator outlives the launcher until its segment ends
    while time.monotonic() < deadline:
        try:
            drv()._Lock(run_dir / 'lock').release()
            break
        except drv().ScreenRefusal:
            time.sleep(0.5)
    end = ledger_records(run_dir)[-1]
    deadline = time.monotonic() + 10  # the coordinator releases its lock just before it exits
    while True:
        alive = _process_table()
        survivors = [pid for pid, parent in run_pids.items() if alive.get(pid) == parent]
        if not survivors or time.monotonic() > deadline:
            break
    assert survivors == [], f'run processes outlived SEGMENT_END and the lock: {survivors}'
    assert end['type'] == 'SEGMENT_END' and (end['body']['class'], end['body']['cause']) == ('STOPPED', 'INTERRUPTED')
    assert 'INTERRUPTED' in {w['reason'] for w in end['body']['workers']} <= {'INTERRUPTED', 'DONE'}
    stop, results = finish(env)
    assert stop.kind == 'COMPLETE' and results == full(env)['results']


def _expected_states(records):
    """The state each record leaves, from the run's own transitions (the reference flow)."""
    names = {'AUTHORITY_BOUND': 'BOUND', 'PREPARED': 'PREPARED', 'PROBE_START': 'PROBING', 'PROBE': 'IDLE',
             'SEGMENT_START': 'RUNNING', 'HEARTBEAT': 'RUNNING', 'AGGREGATED': 'AGGREGATED',
             'REPORTED': 'REPORTED', 'FINAL': 'FINAL', 'VERIFY_START': 'FINAL', 'VERIFY': 'FINAL',
             'ALL_DONE': 'COMPLETE', 'SEGMENT_CRASHED': 'IDLE', 'TERMINAL': 'TERMINAL'}
    out = ['NONE']
    for record in records:
        kind, body = record['type'], record['body']
        if kind == 'SEGMENT_END':
            out.append({'COMPLETE': 'COMPLETE', 'STOPPED': 'IDLE', 'HALTED': 'HALTED',
                        'TERMINAL': 'TERMINAL'}[body['class']])
        else:
            out.append(names[kind])
    return out


@WINDOWS
def test_I3(env):
    """Every prefix of a recorded ledger, cut at each record and inside each record (a torn tail),
    folds through ``advance`` to the state the run was in when that prefix was durable."""
    recorded = [full(env)['records']]
    window = env.base / 'i3'
    for _, path in drv()._ledger_files(full(env)['dir']):
        assert path.exists()
    sources = [full(env)['dir']]
    for run_dir in sources:
        records = ledger_records(run_dir)
        recorded.append(records)
    for records in recorded:
        expected = _expected_states(records)
        raw = b''.join(canonical(dict(record)) + b'\n' for record in records)
        ends = [0] + [i + 1 for i, byte in enumerate(raw) if byte == 0x0A]
        for index, end in enumerate(ends):
            for cut in (end, end + 7) if index < len(records) else (end,):
                (window / 'ledger').mkdir(parents=True, exist_ok=True)
                (window / 'ledger' / '0001.jsonl').write_bytes(raw[:cut])
                assert state.fold(drv().read_ledger(window)).name == expected[index], (index, cut)
    assert _expected_states(full(env)['records'])[-1] == 'FINAL'


# ---- I1 windows injected at the coordinator/worker boundary (card-owner review of #705) ------------

PLAN = 'ops/c1_rail/qualification/t00_screen/plan.py'
FAULTS = """

# TEST_ONLY fault seam (driver I1 W10, W19, W20): the fault named in <private root>/t00-fault, read at
# call time inside a worker (its argv[2] is <private root>/t00-step3/<authority>).
def _t00_fault():
    import os, sys
    run_dir = sys.argv[2] if len(sys.argv) > 2 else ''
    path = os.path.join(os.path.dirname(os.path.dirname(run_dir)), 't00-fault')
    if not run_dir or not os.path.isfile(path):
        return ''
    with open(path, encoding='utf-8') as handle:
        return handle.read().strip()


_t00_candidates, _t00_seed = candidates, seed


def candidates(*args, **kwargs):
    if _t00_fault() == 'CANDIDATES_UNAVAILABLE':
        raise PlanRefusal('CANDIDATES_UNAVAILABLE')
    return _t00_candidates(*args, **kwargs)


def seed(*, purpose, **kwargs):
    if (_t00_fault(), purpose) in (('CONTEXT_REFUSAL', 'path'), ('PROBE_INCOMPLETE', 'probe')):
        raise PlanRefusal('CONTEXT_REFUSAL')
    return _t00_seed(purpose=purpose, **kwargs)
"""


@pytest.fixture(scope='module')
def built_fault_env(tmp_path_factory):
    with pytest.MonkeyPatch.context() as monkeypatch:
        yield Env(tmp_path_factory.mktemp('t00-faults'), monkeypatch,
                  code_edits={PLAN: lambda text: text + FAULTS})


@pytest.fixture
def fault_env(built_fault_env, monkeypatch):
    return built_fault_env.apply(monkeypatch)


# window -> (fault, the ledger's record types, the TERMINAL code)
FAULT_WINDOWS = {
    'W20': ('CANDIDATES_UNAVAILABLE', ['AUTHORITY_BOUND', 'TERMINAL'], 'CANDIDATES_UNAVAILABLE'),
    'W19': ('PROBE_INCOMPLETE', ['AUTHORITY_BOUND', 'PREPARED', 'PROBE_START', 'TERMINAL'], 'PROBE_INCOMPLETE'),
    'W10': ('CONTEXT_REFUSAL', ['AUTHORITY_BOUND', 'PREPARED', 'PROBE_START', 'PROBE', 'SEGMENT_START',
                                'SEGMENT_END'], 'CONTEXT_REFUSAL'),
}


@WINDOWS
@pytest.mark.parametrize('window', sorted(FAULT_WINDOWS))
def test_I1_injected(fault_env, window):
    """W10 (a context refusal on a path key), W19 (a probe that cannot complete) and W20 (candidates
    unavailable), each injected inside the worker through the TEST_ONLY code root: the run stops
    TERMINAL with that code, and finalize labels it INSUFFICIENT with that reason."""
    fault, kinds_expected, code = FAULT_WINDOWS[window]
    fault_env.fresh()
    marker = fault_env.artifact_root / 't00-fault'
    marker.write_text(fault, encoding='utf-8')
    try:
        stop = drv().run(fault_env.inputs(), workers=WORKERS)
    finally:
        marker.write_text('', encoding='utf-8')
    run_dir = fault_env.run_dir
    assert (stop.kind, stop.code) == ('TERMINAL', code)
    assert kinds(run_dir) == kinds_expected
    if window == 'W10':
        end = ledger_records(run_dir)[-1]['body']
        assert (end['class'], end['cause']) == ('TERMINAL', 'CONTEXT_REFUSAL')
    label, _ = drv().finalize(fault_env.inputs())
    results = json.loads((run_dir / 'results.json').read_bytes())
    assert label == 'INSUFFICIENT' and code in results['verdict']['reasons']
    assert state.fold(ledger_records(run_dir)).name == 'FINAL'


def _resume_in_background(env, workers=WORKERS):
    found = {}

    def resume():
        try:
            found['stop'] = drv().resume(env.inputs(), workers=workers)
        except BaseException as exc:  # pylint: disable=broad-exception-caught  # asserted by the caller
            found['error'] = exc
    thread = threading.Thread(target=resume)
    thread.start()
    return thread, found


def _await_path(run_dir, thread, timeout=600):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        folder = run_dir / 'journal'
        if folder.is_dir() and any(b'"PATH"' in path.read_bytes() for path in folder.glob('s*.jsonl')):
            return
        assert thread.is_alive(), 'the segment ended before a path completed'
        time.sleep(0.1)
    raise AssertionError('no path completed')


@WINDOWS
def test_I1_W12_tree_changed(env):
    """W12, drift that nothing loaded: an r3c artifact's mtime changes mid-segment. The stat guard stops
    each worker before its next KEY_START, the epoch still closes matching, and the segment ends
    STOPPED TREE_CHANGED; restored, resume completes with the uninterrupted run's results."""
    run_dir = _idle(env)
    artifact = env.artifact_root / next(iter(env.case.paths.values()))
    stat = artifact.stat()
    thread, found = _resume_in_background(env)
    try:
        _await_path(run_dir, thread)
        os.utime(artifact, ns=(stat.st_atime_ns, stat.st_mtime_ns + 5_000_000_000))
    finally:
        thread.join(timeout=900)
        os.utime(artifact, ns=(stat.st_atime_ns, stat.st_mtime_ns))
    assert 'error' not in found, found.get('error')
    assert (found['stop'].kind, found['stop'].code) == ('STOPPED', 'TREE_CHANGED')
    end = ledger_records(run_dir)[-1]['body']
    assert (end['class'], end['cause']) == ('STOPPED', 'TREE_CHANGED')
    closes = [r['body']['closure_match'] for records in drv().read_journals(run_dir).values() for r in records
              if r['type'] == 'EPOCH_CLOSE']
    assert closes and all(closes)
    stop, results = finish(env)
    assert stop.kind == 'COMPLETE' and results == full(env)['results']


@WINDOWS
def test_I1_W12_drift(env):
    """W12, drift that may have run: a loaded first-party module changes mid-segment. The stat guard
    stops the worker, its epoch close fails, and the segment ends TERMINAL CODE_OR_ARTIFACT_DRIFT;
    finalize labels the run INSUFFICIENT with that reason. A stop for its own reason (here the stale
    stat guard) whose close fails is drift, not the lower-class reason."""
    run_dir = _idle(env)
    module = env.code / PLAN
    original = module.read_bytes()
    thread, found = _resume_in_background(env, workers=1)  # one worker: its own stop reason decides
    try:
        _await_path(run_dir, thread)
        module.write_bytes(original + b'\n# TEST_ONLY drift\n')
    finally:
        thread.join(timeout=900)
        module.write_bytes(original)
    assert 'error' not in found, found.get('error')
    assert (found['stop'].kind, found['stop'].code) == ('TERMINAL', 'CODE_OR_ARTIFACT_DRIFT')
    end = ledger_records(run_dir)[-1]['body']
    assert (end['class'], end['cause']) == ('TERMINAL', 'CODE_OR_ARTIFACT_DRIFT')
    assert not all(r['body']['closure_match'] for records in drv().read_journals(run_dir).values() for r in records
                   if r['type'] == 'EPOCH_CLOSE')
    label, _ = drv().finalize(env.inputs())
    results = json.loads((run_dir / 'results.json').read_bytes())
    assert label == 'INSUFFICIENT' and 'CODE_OR_ARTIFACT_DRIFT' in results['verdict']['reasons']


def _epoch(build, integrity, *, close=None):
    opened = ('EPOCH_OPEN', {'build': {'cpu_s': build, 'wall_s': build},
                             'integrity': {'cpu_s': integrity, 'wall_s': integrity},
                             'closure_sha256': 'a' * 64, 'guard_sha256': 'b' * 64})
    if close is None:
        return [opened]
    closure = {'first_party': {}, 'third_party': {}, 'ports': {}, 'stdlib': []}
    return [opened, ('EPOCH_CLOSE', {'integrity': {'cpu_s': close, 'wall_s': close}, 'closure_match': True,
                                     'closure': closure})]


def test_B5_crashed_candidate_attempt_is_charged():
    """Design §5.4, a crash can only overcharge: a candidate attempt that never reached PREPARED is
    charged as a crash (one heartbeat interval for its one worker, heartbeat 0 being its start) plus
    every epoch cost its journal recorded; the attempt PREPARED carries is not charged twice."""
    module = drv()
    populations = {p: {'indices': [0], 'candidates_sha256': 'c' * 64} for p in ('FULL', 'H1', 'H2')}
    bound = ('AUTHORITY_BOUND', {'authority_sha256': 'f' * 64, 'prereg_path': PREREG, 'approvals': [],
                                 'reused_directory': False})
    crashed = chain(_epoch(7.0, 11.0))
    candidate_epoch, probe_epoch = _epoch(5.0, 1.5, close=1.5), _epoch(0.0, 2.0, close=3.0)
    accepted = chain(candidate_epoch[:1] + [('CANDIDATES', {'populations': populations})] + candidate_epoch[1:]
                     + probe_epoch[:1]
                     + [('PROBE_RESULT', {'path_cpu_s': 4.0, 'path_wall_s': 4.0, 'peak_memory_bytes': 1})]
                     + probe_epoch[1:] + [('WORKER_STOP', {'reason': 'DONE', 'key': None})])
    ledger = chain([bound, ('HALT', {'code': 'UNCLASSIFIED_ERROR', 'from': 'BOUND'}),
                    ('ACT', {'act_sha256': 'e' * 64, 'act': 'CONTINUE'}),
                    ('PREPARED', {'manifest_sha256': 'd' * 64, 'build': {'cpu_s': 5.0, 'wall_s': 5.0},
                                  'integrity': {'cpu_s': 3.0, 'wall_s': 3.0}}),
                    ('PROBE_START', {}), ('PROBE', {'path_cpu_s': 4.0, 'path_wall_s': 4.0, 'peak_memory_bytes': 1})])
    charge = module.HEARTBEAT_S + 7.0 + 11.0
    assert module.overhead_used(ledger, {'c1-w0.jsonl': crashed, 'c2-w0.jsonl': accepted}) == \
        (5.0 + 3.0) + 4.0 + (2.0 + 3.0) + charge
    assert module.overhead_used(chain([bound]), {'c1-w0.jsonl': crashed}) == charge
    assert module.overhead_used(ledger, {'c2-w0.jsonl': accepted}) == 8.0 + 4.0 + 5.0  # twin: no crash, no charge


# ---- the segment loop's accounting under load (Codex r4189920841, r4189920851 on #705) --------------
# A stand-in Job and stand-in workers drive the real ``_Run.segment`` loop: no process starts, so the
# timing of messages and interrupts is the test's own.

class _Job:
    """A stand-in Job Object: ``cpu`` CPU seconds while open; a closed job cannot be queried."""

    def __init__(self, cpu=200.0, readable=True):
        self.cpu, self.readable, self.handle = cpu, readable, 1

    def cpu_s(self):
        if not self.readable:
            raise OSError('job accounting unreadable')
        return self.cpu if self.handle else 0.0  # a closed job reads as no CPU at all

    def peak_memory(self):
        return 1 << 20 if self.handle else 0

    def close(self):
        self.handle = None


class _Interrupting(dict):
    """A worker message whose first read raises KeyboardInterrupt (a Ctrl-C inside the loop)."""

    def get(self, *args):
        raise KeyboardInterrupt


class _Worker:
    """A stand-in worker: ``noise`` seconds of chatter before 'ready', then one 'done' per key."""

    def __init__(self, name, inbox, index, *, noise=0.0, interrupts=0):
        self.name, self.inbox, self.index, self.noise, self.interrupts = name, inbox, index, noise, interrupts
        self.key, self.exited, self.stopped = None, False, 'DONE'
        self.process = type('Process', (), {'wait': staticmethod(lambda: 0)})()

    def send(self, message):
        if message.get('type') == 'init':
            threading.Thread(target=self._start, daemon=True).start()
        elif message.get('cmd') == 'key':
            self.inbox.put((self.index, {'type': 'done', 'key': message['key'], 'cpu_s': 1.0}))
        elif message.get('cmd') == 'stop':
            self.stopped = message.get('reason') or 'DONE'
            self.inbox.put((self.index, None))

    def _start(self):
        for _ in range(self.interrupts):
            self.inbox.put((self.index, _Interrupting()))
        until = time.perf_counter() + self.noise
        while time.perf_counter() < until:  # sustained traffic: the inbox never runs dry
            self.inbox.put((self.index, {'type': 'noise'}))
            time.sleep(0.001)
        self.inbox.put((self.index, {'type': 'ready'}))

    def reason(self):
        return self.stopped

    def keep_stderr(self):
        return None


def _segment_run(tmp_path, monkeypatch, *, job, **worker):
    """An IDLE run record and a ``_Run`` whose Job and workers are stand-ins; the segment's records."""
    module = drv()
    run_dir = tmp_path / 'run'
    (run_dir / 'journal').mkdir(parents=True)
    cost = {'cpu_s': 1.0, 'wall_s': 1.0}
    write_file(run_dir / 'ledger' / '0001.jsonl', [
        ('AUTHORITY_BOUND', {'authority_sha256': 'f' * 64, 'prereg_path': PREREG, 'approvals': [],
                             'reused_directory': False}),
        ('PREPARED', {'manifest_sha256': 'd' * 64, 'build': cost, 'integrity': cost}), ('PROBE_START', {}),
        ('PROBE', {'path_cpu_s': 1.0, 'path_wall_s': 1.0, 'peak_memory_bytes': 1})])
    monkeypatch.setattr(module, 'Job', lambda: job)
    run = object.__new__(module._Run)
    approval = type('Approval', (), {'approval_sha256': 'a' * 64})()
    run.inputs = type('Inputs', (), {'message': staticmethod(lambda: {})})()
    run.receipt = run.auth = type('Bound', (), {'approval': approval})()
    run.ledger, run.lock, run.run_dir, run.requested_workers = module.Ledger(run_dir), None, run_dir, 2
    run.params = {'budget': {'path_cpu_seconds': 1_000_000, 'overhead_cpu_seconds': 1_000_000}}
    run.keys = tuple(('r', population, 0) for population in ('FULL', 'H1', 'H2'))
    run.now, run.candidate, run.job = None, None, None
    run._start = lambda name, inbox, index=0: _Worker(name, inbox, index, **worker)
    stop = run.segment(sorted(run.keys), set(), 0.0)
    run.ledger.close()
    return stop, ledger_records(run_dir)


def test_heartbeats_keep_their_cadence_under_sustained_traffic(tmp_path, monkeypatch):
    """Codex r4189920841: the heartbeat deadline is checked on every loop iteration, so workers that
    keep the inbox busy for 20 intervals still see a heartbeat about every interval (design §4.2: every
    60 s while RUNNING)."""
    monkeypatch.setattr(drv(), 'HEARTBEAT_S', 0.05)
    stop, records = _segment_run(tmp_path, monkeypatch, job=_Job(), noise=1.0)
    beats = [r['body']['wall_s'] for r in records if r['type'] == 'HEARTBEAT']
    assert stop.kind == 'COMPLETE' and len(beats) >= 10, beats
    assert all(later - earlier < 0.5 for earlier, later in zip([0.0] + beats, beats)), beats
    assert all(r['body']['job_cpu_s'] == 200.0 for r in records if r['type'] == 'HEARTBEAT')


def test_second_interrupt_records_the_job_cpu(tmp_path, monkeypatch):
    """Codex r4189920851: a second Ctrl-C closes the job, and its CPU is read before the handle closes,
    so SEGMENT_END is not undercharged (200 CPU seconds, nothing booked: 200 of overhead)."""
    stop, records = _segment_run(tmp_path, monkeypatch, job=_Job(cpu=200.0), interrupts=2)
    end = records[-1]['body']
    assert (stop.kind, stop.code) == ('STOPPED', 'INTERRUPTED') and records[-1]['type'] == 'SEGMENT_END'
    assert (end['job_cpu_s'], end['path_cpu_s'], end['overhead_cpu_s']) == (200.0, 0.0, 200.0)


def test_unreadable_job_cpu_is_charged_conservatively(tmp_path, monkeypatch):
    """When the job's CPU cannot be read, SEGMENT_END carries the crash charge (the last heartbeat,
    here heartbeat 0, plus one interval per worker) as overhead, never 0."""
    stop, records = _segment_run(tmp_path, monkeypatch, job=_Job(readable=False), interrupts=2)
    end = records[-1]['body']
    floor = drv().HEARTBEAT_S * 2
    assert stop.kind == 'STOPPED' and end['job_cpu_s'] >= floor and end['overhead_cpu_s'] >= floor


def _failing_job():
    """A real ``Job`` whose kernel stand-in fails every QueryInformationJobObject (returns FALSE)."""
    import ctypes

    class Accounting(ctypes.Structure):
        _fields_ = [('TotalUserTime', ctypes.c_int64), ('TotalKernelTime', ctypes.c_int64)]

    class Extended(ctypes.Structure):
        _fields_ = [('PeakProcessMemoryUsed', ctypes.c_size_t)]

    class Kernel:
        @staticmethod
        def QueryInformationJobObject(*_args):
            return 0  # FALSE; the out-structure is left zeroed

        @staticmethod
        def CloseHandle(_handle):
            return 1

    job = object.__new__(drv().Job)
    job.ctypes, job.kernel, job.accounting_type, job.extended, job.handle = ctypes, Kernel(), Accounting, Extended, 1
    return job


def test_failed_job_query_is_unreadable_not_zero(tmp_path, monkeypatch):
    """Codex r2 on #705 (review 5423080976): a FALSE QueryInformationJobObject is an unreadable job,
    never a read of 0 CPU, so SEGMENT_END takes the conservative crash charge; peak memory alike."""
    job = _failing_job()
    with pytest.raises(OSError):
        job.cpu_s()
    with pytest.raises(OSError):
        job.peak_memory()
    stop, records = _segment_run(tmp_path, monkeypatch, job=job, interrupts=2)
    end = records[-1]['body']
    floor = drv().HEARTBEAT_S * 2
    assert stop.kind == 'STOPPED' and end['job_cpu_s'] >= floor and end['overhead_cpu_s'] >= floor
