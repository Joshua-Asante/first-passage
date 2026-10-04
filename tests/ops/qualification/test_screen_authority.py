"""T00 screen authority: rows A1-A11, K1-K4, X2, X3 (design 2026-10-02 §2.2, §3; card §2.3).

TEST_ONLY keys are generated in-process. Only the pinned root (``SOURCE_SIGNING_KEYS`` and the
compiled source constants through ``build_source_case``, plus the compiled r3c digest) and the
validator's ``REPOSITORY_ROOT`` are replaced; the K rows also install a stand-in for the screen
bootstrap's recorder (``sys.p7_recorder``), the process state the real bootstrap sets (design
§13). The repository is a synthetic git repository whose #581 copy carries the tracked A5/A6
section bytes (public text). No test reads the real source. Each row test asserts its row's
code and has a passing twin; the module is imported inside each test, so a missing module fails
the row rather than erroring at collection.
"""
from __future__ import annotations

# Row-named tests (design §10), pytest fixtures and the stand-in recorder attribute on sys:
# pylint: disable=invalid-name,redefined-outer-name,no-member,missing-function-docstring

import base64
from contextlib import contextmanager
import hashlib
import importlib
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
from datetime import timedelta
from types import SimpleNamespace

import pytest

from c1_rail.qualification import p7_evidence
from c1_rail.qualification.contract import canonical_json_bytes as canonical
from c1_rail.qualification.t00_screen import journal, verdict
from test_source_contract import NOW, build_source_case

pytestmark = pytest.mark.skipif(shutil.which('git') is None, reason='git required for the repository bindings')
WINDOWS = pytest.mark.skipif(os.name != 'nt', reason='the run lock is a msvcrt byte-range lock (card §3.4)')

REPO = Path(__file__).resolve().parents[3]
PREREG = 'docs/briefs/pre-registration/2026-10-01-tradeify-t00-step2-screen-prereg.md'
ORB = 'docs/briefs/pre-registration/2026-10-02-tradeify-route-native-editions-successor-prereg.md'
VAN = 'docs/briefs/pre-registration/2026-10-02-tradeify-vanguard-fixed-stop-edition-successor-prereg.md'
MODULE = 'ops/c1_rail/qualification/t00_screen_fixture.py'  # the synthetic P7 record's one loaded module
SECTION3 = {1: ('depth_per_root', 'budget'), 2: ('pass_floor_halves',), 3: ('deadline_only_is_bust',),
            4: ('rng', 'block', 'path_start_date'), 5: ('run1_diagnostic',), 7: ('scenarios',), 8: ('a5_rule',)}
REFUSALS = ['QUALIFICATION_STAGES', 'PART_A', 'F1', 'DECISION_RULES', 'SEAL', 'ADMISSION', 'DEPLOYMENT', 'ARM',
            'FALSIFIER_EVIDENCE', 'PARAMETER_CHANGE']
BINARY = getattr(os, 'O_BINARY', 0)


def sa():
    return importlib.import_module('c1_rail.qualification.screen_authority')


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git(root, *args):
    return subprocess.run(['git', '-C', str(root), '-c', 'user.email=pa@test', '-c', 'user.name=pa-test',
                           '-c', 'core.autocrlf=false', '-c', 'commit.gpgsign=false', *args],
                          check=True, capture_output=True).stdout.decode('utf-8').strip()


def write(root: Path, relative: str, text: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode('utf-8'))


def refused(code, call, detail=''):
    with pytest.raises(ValueError) as error:
        call()
    message = str(error.value)
    assert message.startswith(code + ':') and detail in message, message


def cells(overrides=None):
    rows = {item: 'values block: ' + ', '.join(f'`{key}`' for key in keys) for item, keys in SECTION3.items()}
    rows.update(overrides or {})
    return rows


def prereg_text(sections, params, *, status='RATIFIED 2026-10-10', ratifying='—', row_cells=None):
    rows = row_cells or cells()
    table = '\n'.join(f'| {item} | item {item} | — | TEST_ONLY | {rows[item]} |' for item in sorted(rows))
    return (f'# Pre-registration — TEST_ONLY copy of #581\n\n**Status:** `{status}.` TEST_ONLY.\n\n'
            f'## §2 — The additions\n\n{sections}'
            '## §3 — OPERATOR TO SET\n\n| # | Item | Candidates | Why | Ratified value |\n|---|---|---|---|---|\n'
            f'{table}\n| 6 | *Withdrawn* | — | — | — |\n\n'
            '## §6 — Ratification\n\n- **Ruling:** TEST_ONLY ruling\n- **OD-1 / OD-2:** TEST_ONLY rulings\n'
            f'- **Ratifying commit SHA:** {ratifying}\n\n```t00-step2-values/v1\n'
            f'{canonical(params).decode("utf-8")}\n```\n\n## Audit hooks\n\nnone\n')


def successor(prefix, *, answered=True, mapping_marker=False):
    status = ('**Answered** (TEST_ONLY).<br>Answerer exposure: seen — Tester |' if answered
              else '**OWED (operator)** |')
    mapping = 'mapped. Answerer exposure: seen — Tester |' if mapping_marker else 'mapped |'
    return '\n'.join([
        '# TEST_ONLY successor', '',
        'Write the statement as `Answerer exposure: seen — <answerer name>`.', '',
        '## §3', '', '| ID | Rule | Status |', '|---|---|---|', f'{prefix}*(CF)* | What replaces the trail. | {status}',
        '', '## §3a', '', '| ID | Mapping |', '|---|---|', f'{prefix}*(CF)* | {mapping}', ''])


class Screen:  # pylint: disable=too-many-instance-attributes
    """One synthetic source case, repository, P7 record and screen authority."""

    def __init__(self, root: Path, monkeypatch, *, a6_byte=False, cprime_cell=False,  # pylint: disable=too-many-arguments
                 a3_unanswered=False):
        self.monkeypatch = monkeypatch
        self.ledger = None
        self.artifact_root = root / 'private'
        self.case = build_source_case(self.artifact_root, monkeypatch)
        self.receipt = self.case.validate()
        smallest = min(len(values) for values in self.case.document['populations'].values())
        self.params = {
            'expressions': 'DECLARED_BOOK', 'scenarios': ['S0'],
            'initial_state': dict(self.case.document['initial_state']), 'horizon_sessions': 1500,
            'rng': {'tag': 't00-screen-rng/v1', 'roots': ['root-a', 'root-b', 'root-c'], 'probe_root': 'probe'},
            'depth_per_root': {'FULL': 2, 'H1': 2, 'H2': 2},
            'block': {'family': 'JOINT_FLAT_BOTH_RUNS',
                      'length_sessions': max(d for d in range(1, smallest + 1) if 1500 % d == 0)},
            'path_start_date': self.case.document['path_start_date'], 'pass_floor_halves': 'BINDING',
            'deadline_only_is_bust': True, 'run1_diagnostic': 'WAIVED', 'a5_rule': 'T00_A5/v1',
            'median_rule': 'LOWER_NEAREST_RANK_INF_INCLUDED',
            'budget': {'path_cpu_seconds': 1000, 'overhead_cpu_seconds': 100, 'basis': 'TEST_ONLY basis'},
        }
        tracked = (REPO / PREREG).read_bytes()
        sections = (verdict.section_text(tracked, 'A5') + verdict.section_text(tracked, 'A6')).decode('utf-8')
        if a6_byte:
            head, tail = sections.split('### A6', 1)
            sections = head + '### A6' + tail.replace(' the ', ' thE ', 1)
        self.repo = repo = root / 'repo'
        repo.mkdir()
        git(repo, 'init', '-q')
        write(repo, MODULE, '"""TEST_ONLY loaded module."""\n')
        write(repo, ORB, successor('| ORB-3 ', answered=not a3_unanswered, mapping_marker=a3_unanswered))
        write(repo, VAN, successor('| VAN-3 '))
        write(repo, PREREG, prereg_text(sections, self.params, status='DRAFT — NOT RATIFIED'))
        git(repo, 'add', '-A')
        git(repo, 'commit', '-q', '-m', 'TEST_ONLY draft')
        write(repo, PREREG, prereg_text(sections, self.params))
        git(repo, 'commit', '-q', '-am', 'TEST_ONLY ratify')
        self.ratifying = git(repo, 'rev-parse', 'HEAD')
        later = cells({2: 'values block: `pass_floor_halves` (edited)'}) if cprime_cell else None
        write(repo, PREREG, prereg_text(sections, self.params, ratifying=f'`{self.ratifying}`', row_cells=later))
        git(repo, 'commit', '-q', '-am', 'TEST_ONLY record the ratifying SHA')
        self.head = git(repo, 'rev-parse', 'HEAD')
        git(repo, 'update-ref', 'refs/remotes/origin/main', self.head)
        self.interpreter = p7_evidence.current_interpreter_binding(repo)
        self.record = self._record(p7_evidence.P7_BOOTSTRAP_SHA256)
        self.authority = self.document(self.record)

    def _record(self, bootstrap_sha256):
        closure = {'first_party': {'c1_rail.qualification.t00_screen_fixture': {
                       'path': MODULE, 'sha256': sha((self.repo / MODULE).read_bytes())}},
                   'third_party': {}, 'distributions': {}, 'stdlib': [], 'ports': {}}
        record = {'schema': p7_evidence.RECORD_SCHEMA, 'contract_sha256': self.receipt.contract_sha256,
                  'code_head': self.head, 'bootstrap_sha256': bootstrap_sha256,
                  'code_closure_sha256': sha(p7_evidence.canonical(closure)), 'loaded_closure': closure,
                  'interpreter': self.interpreter,
                  'contract_b64': base64.b64encode(self.case.contract_bytes()).decode('ascii'),
                  'approval_b64': base64.b64encode(self.receipt.approval_bytes).decode('ascii'),
                  'result': {'labels': []}}
        return p7_evidence.canonical(record)

    def document(self, record_bytes):
        record = p7_evidence.parse_record(record_bytes)
        blob = (self.repo / PREREG).read_bytes()
        return {
            'schema': 't00_screen_authority/v1', 'authority_id': 'TEST_ONLY-screen-authority',
            'purpose': 'T00_STEP3_SELECTED_BOOK_SCREEN', 'grants': ['T00_STEP3_SCREEN_ONCE'], 'refusals': REFUSALS,
            'evidence_class': 'T00_STEP3_SCREEN', 'source': {'contract_sha256': self.receipt.contract_sha256},
            'run_root_sha256': sha(str((self.artifact_root / 't00-step3').resolve()).encode('utf-8')),
            'p7': {'record_sha256': sha(record_bytes), 'code_head': record['code_head'],
                   'code_closure_sha256': record['code_closure_sha256'],
                   'bootstrap_sha256': record['bootstrap_sha256'], 'interpreter': record['interpreter']},
            'prereg': {'path': PREREG, 'ratifying_commit': self.ratifying, 'commit': self.head,
                       'blob_sha256': sha(blob), 'a5_text_sha256': verdict.A5_TEXT_SHA256,
                       'a6_text_sha256': verdict.A6_TEXT_SHA256},
            'a3_answers': [{'path': path, 'commit': self.head, 'blob_sha256': sha((self.repo / path).read_bytes())}
                           for path in (ORB, VAN)],
            'parameters': self.params, 'source_trust': self.case.document['source_trust'],
        }

    def approval(self, raw, *, scope='APPROVE_T00_SCREEN_AUTHORITY', authority='OPERATOR',
                 expires_at='2026-09-16T19:00:00Z'):
        return self.case.approval(scope=scope, authority=authority, expires_at=expires_at, subject=raw)

    def patch(self):
        module = sa()
        self.monkeypatch.setattr(module, 'REPOSITORY_ROOT', self.repo)
        self.monkeypatch.setattr(module, 'R3C_CONTRACT_SHA256', self.receipt.contract_sha256)
        return module

    def validate(self, *, doc=None, approval=None, record=None, receipt=None,  # pylint: disable=too-many-arguments
                 artifact_root=None, now=NOW):
        module = self.patch()
        raw = canonical(self.authority if doc is None else doc)
        return module.validate_screen_authority(
            raw, self.approval(raw) if approval is None else approval, self.case.public_keys,
            source_receipt=self.receipt if receipt is None else receipt,
            p7_record_bytes=self.record if record is None else record,
            artifact_root=self.artifact_root if artifact_root is None else artifact_root, now=now)

    @contextmanager
    def ready(self, auth, *, bound=True):
        """A screen-bootstrap recorder, a run directory with its ledger and a held run lock whose
        content names this process's parent, and the write-once binding."""
        msvcrt = importlib.import_module('msvcrt')
        run_dir = Path(auth.run_root) / auth.authority_sha256
        (run_dir / 'ledger').mkdir(parents=True)
        self.ledger = run_dir / 'ledger' / '0001.jsonl'
        self.ledger.write_bytes(b'')
        if bound:
            self.bind_ledger(auth)
        lock = os.open(run_dir / 'lock', os.O_RDWR | os.O_CREAT | BINARY, 0o644)
        try:
            os.write(lock, canonical({'host': socket.gethostname(), 'pid': os.getppid(),
                                      'schema': 't00_screen_lock/v1'}))
            os.lseek(lock, journal.LOCK_OFFSET, os.SEEK_SET)
            msvcrt.locking(lock, msvcrt.LK_NBLCK, 1)
            self.monkeypatch.setattr(sys, 'p7_recorder', SimpleNamespace(
                bootstrap_sha256=p7_evidence.SCREEN_BOOTSTRAP_SHA256), raising=False)
            sa().bind_screen_run(run_dir, auth.authority_sha256)
            yield run_dir
            os.lseek(lock, journal.LOCK_OFFSET, os.SEEK_SET)
            msvcrt.locking(lock, msvcrt.LK_UNLCK, 1)
        finally:
            os.close(lock)

    def bind_ledger(self, auth):
        fd = os.open(self.ledger, os.O_WRONLY | os.O_APPEND | BINARY)
        try:
            journal.append(fd, 'AUTHORITY_BOUND', {
                'authority_sha256': auth.authority_sha256, 'prereg_path': PREREG,
                'approvals': [auth.approval.approval_sha256], 'reused_directory': False}, prev_sha256=None)
        finally:
            os.close(fd)


@pytest.fixture
def screen(tmp_path, monkeypatch):
    return Screen(tmp_path, monkeypatch)


def spy_git(screen):
    module = screen.patch()
    calls, real = [], module._git  # pylint: disable=protected-access

    def spy(*args):
        calls.append(args)
        return real(*args)
    screen.monkeypatch.setattr(module, '_git', spy)
    return calls


def require(auth, now=NOW, receipt=None):
    return sa().require_validated_screen_authority(
        auth, source_contract=auth.source_receipt if receipt is None else receipt, now=now)


def act(screen, *, readers=None, head='a' * 64, scope='APPROVE_T00_SCREEN_ACT'):
    doc = {'schema': 't00_screen_act/v1', 'authority_sha256': sha(canonical(screen.authority)), 'act': 'CONTINUE',
           'ledger_head_sha256': head, 'statement': 'TEST_ONLY continue after a HALT',
           'readers': [{'name': 'Joshua', 'exposure': 'not seen'}] if readers is None else readers}
    raw = canonical(doc)
    return raw, screen.approval(raw, scope=scope)


def validate_act(screen, raw, approval, *, ledger_head='a' * 64):
    return sa().validate_screen_act(raw, approval, screen.case.public_keys, authority=canonical(screen.authority),
                                    ledger_head=ledger_head, now=NOW)


# ---- A. authority validation -----------------------------------------------------------------

def test_A1(screen):
    """An excluded field (an expiry) is refused by the closed field set."""
    refused('SCREEN_AUTHORITY_FIELDS', lambda: screen.validate(doc=dict(screen.authority, expires_at=NOW.isoformat())))
    assert screen.validate().authority_sha256 == sha(canonical(screen.authority))


def test_A2(screen):
    """A TEST_ONLY signer is refused at the signature step, before any git call."""
    raw = canonical(screen.authority)
    calls = spy_git(screen)
    refused('SCREEN_TRUST_ROOT_MISMATCH', lambda: screen.validate(approval=screen.approval(raw, authority='TEST_ONLY')),
            'TEST_ONLY')
    assert not calls
    screen.validate()
    assert calls


def test_A3(screen):
    """Scopes are exclusive: a source-scope approval over the authority digest verifies as nothing."""
    raw = canonical(screen.authority)
    refused('SCREEN_APPROVAL_INVALID', lambda: screen.validate(
        approval=screen.approval(raw, scope='APPROVE_T00_SOURCE_CONTRACT')), 'scope')
    refused('SCREEN_APPROVAL_INVALID', lambda: screen.validate(
        approval=screen.approval(raw, scope='APPROVE_T00_SCREEN_ACT')), 'scope')
    with pytest.raises(ValueError, match='approval scope does not match'):
        screen.case.validate(approval=screen.case.approval(scope='APPROVE_T00_SCREEN_AUTHORITY'))
    screen.validate()


def test_A4(screen):
    """An unsigned commit field shaped as a git option is refused before any git call."""
    doc = dict(screen.authority, prereg=dict(screen.authority['prereg'], commit='--output=x'))
    calls = spy_git(screen)
    refused('SCREEN_AUTHORITY_FIELDS', lambda: screen.validate(doc=doc), 'commit')
    assert not calls
    screen.validate()


def test_A5(screen):
    """One untracked file at the repository root is an unclean tree."""
    screen.validate()
    (screen.repo / 'stray.txt').write_bytes(b'untracked\n')
    refused('SCREEN_P7_MISMATCH', screen.validate, 'clean')


def test_A6(screen, tmp_path):
    """The same authority presented with a copied private root refuses on the bound run root."""
    copy = tmp_path / 'copied-private'
    shutil.copytree(screen.artifact_root, copy)
    refused('SCREEN_RUN_ROOT_MISMATCH', lambda: screen.validate(artifact_root=copy))
    screen.validate()


def test_A7(screen):
    """A record listing the true current hashes under another bootstrap digest is refused."""
    record = screen._record('f' * 64)  # pylint: disable=protected-access
    refused('SCREEN_P7_MISMATCH', lambda: screen.validate(doc=screen.document(record), record=record), 'bootstrap')
    screen.validate()


def test_A8(tmp_path, monkeypatch):
    """C′ also edits one §3 cell: C→C′ changes more than the Ratifying commit SHA line."""
    bad = Screen(tmp_path / 'bad', monkeypatch, cprime_cell=True)
    refused('SCREEN_PREREG_MISMATCH', bad.validate, 'Ratifying commit SHA')
    Screen(tmp_path / 'good', monkeypatch).validate()


def test_A9(tmp_path, monkeypatch):
    """One byte changed inside A6 breaks the compiled section hash."""
    bad = Screen(tmp_path / 'bad', monkeypatch, a6_byte=True)
    refused('SCREEN_PREREG_MISMATCH', bad.validate, 'A5/A6')
    Screen(tmp_path / 'good', monkeypatch).validate()


def test_A10(tmp_path, monkeypatch):
    """The §3a mapping row carries the exposure marker while the §3 row still reads OWED."""
    bad = Screen(tmp_path / 'bad', monkeypatch, a3_unanswered=True)
    refused('SCREEN_A3_UNANSWERED', bad.validate, 'ORB-3')
    Screen(tmp_path / 'good', monkeypatch).validate()


def test_A11(screen):
    """A second scenario is unsupported."""
    doc = dict(screen.authority, parameters=dict(screen.params, scenarios=['S0', 'S1']))
    refused('SCREEN_PARAMETER_UNSUPPORTED', lambda: screen.validate(doc=doc), 'scenarios')
    screen.validate()


# ---- K. capability gate (every use) ----------------------------------------------------------

@WINDOWS
def test_K1(screen):
    """Same SHA-256, a different receipt object."""
    auth = screen.validate()
    other = screen.case.validate()
    assert other.contract_sha256 == auth.source_receipt.contract_sha256 and other is not auth.source_receipt
    with screen.ready(auth):
        refused('SCREEN_SOURCE_MISMATCH', lambda: require(auth, receipt=other))
        assert require(auth) is auth


@WINDOWS
def test_K2(screen):
    """The screen approval expires between two calls and is named as the screen's."""
    raw = canonical(screen.authority)
    auth = screen.validate(approval=screen.approval(raw, expires_at='2026-09-15T21:00:00Z'))
    with screen.ready(auth):
        assert require(auth) is auth
        refused('SCREEN_APPROVAL_EXPIRED', lambda: require(auth, now=NOW + timedelta(minutes=90)))


@WINDOWS
def test_K3(screen):
    """A valid authority in a plain interpreter (no screen-bootstrap recorder)."""
    auth = screen.validate()
    with screen.ready(auth):
        recorder = sys.p7_recorder
        screen.monkeypatch.delattr(sys, 'p7_recorder')
        refused('SCREEN_BOOTSTRAP_MISMATCH', lambda: require(auth))
        screen.monkeypatch.setattr(sys, 'p7_recorder', recorder, raising=False)
        assert require(auth) is auth


@WINDOWS
def test_K4(screen):
    """The right bootstrap and binding, but a run directory without AUTHORITY_BOUND."""
    auth = screen.validate()
    with screen.ready(auth, bound=False):
        refused('SCREEN_RUN_UNBOUND', lambda: require(auth), 'AUTHORITY_BOUND')
        screen.bind_ledger(auth)
        assert require(auth) is auth


# ---- X. acts ---------------------------------------------------------------------------------

def test_X2(screen):
    """An act with an empty readers list."""
    refused('SCREEN_ACT_FIELDS', lambda: validate_act(screen, *act(screen, readers=[])), 'reader')
    assert validate_act(screen, *act(screen)).act == 'CONTINUE'


def test_X3(screen):
    """A valid act presented after a later ledger record is stale; an act not signed under the
    act scope is unsigned."""
    raw, approval = act(screen)
    refused('SCREEN_ACT_STALE', lambda: validate_act(screen, raw, approval, ledger_head='b' * 64))
    refused('SCREEN_ACT_UNSIGNED', lambda: validate_act(screen, *act(screen, scope='APPROVE_T00_SCREEN_AUTHORITY')))
    assert validate_act(screen, raw, approval).act_sha256 == sha(raw)


# ---- non-row: compiled constants, epochs, binding --------------------------------------------

def test_compiled_constants_name_the_tracked_files_and_patterns_accept_the_tracked_successors():
    module = sa()
    assert module.PREREG_CHAIN[-1] == PREREG and set(module.A3_SUCCESSORS) == {ORB, VAN}
    assert sha(verdict.section_text((REPO / PREREG).read_bytes(), 'A6')) == verdict.A6_TEXT_SHA256
    for path, (prefix, exposure, owed) in module.A3_SUCCESSORS.items():
        lines = (REPO / path).read_text(encoding='utf-8').split('\n')
        rows = [i for i, line in enumerate(lines) if line.startswith(prefix)]
        assert rows and [i for i, line in enumerate(lines) if exposure.search(line)] == [rows[0]]
        assert owed.search(lines[rows[0]]) is None


def test_bind_screen_run_is_write_once_and_needs_the_screen_bootstrap(screen, tmp_path):
    module = sa()
    refused('SCREEN_BOOTSTRAP_MISMATCH', lambda: module.bind_screen_run(tmp_path, 'a' * 64))
    screen.monkeypatch.setattr(sys, 'p7_recorder', SimpleNamespace(
        bootstrap_sha256=p7_evidence.SCREEN_BOOTSTRAP_SHA256), raising=False)
    module.bind_screen_run(tmp_path, 'a' * 64)
    refused('SCREEN_RUN_UNBOUND', lambda: module.bind_screen_run(tmp_path, 'a' * 64), 'write-once')


def test_epoch_opens_guards_and_closes_once(screen):
    module = sa()
    auth = screen.validate()

    class Source:  # pylint: disable=too-few-public-methods
        """Stands in for ProductionSource; only the full integrity check is called."""
        checks = 0

        def _verify_integrity(self):
            Source.checks += 1
    source = Source()
    epoch = module.open_screen_epoch(source, auth)
    module.require_open_screen_epoch(epoch, source=source, authority=auth)
    refused('SCREEN_EPOCH_REQUIRED', lambda: module.require_open_screen_epoch(epoch, source=Source(), authority=auth))
    artifact = screen.artifact_root / auth.source_receipt.artifacts[0].path
    stat = artifact.stat()
    os.utime(artifact, ns=(stat.st_atime_ns, stat.st_mtime_ns + 1_000_000_000))
    refused('SCREEN_EPOCH_STALE', lambda: module.require_open_screen_epoch(epoch, source=source, authority=auth))
    closed = module.close_screen_epoch(epoch)
    assert closed.closure_match and Source.checks == 1
    refused('SCREEN_EPOCH_REQUIRED', lambda: module.close_screen_epoch(epoch))


def test_screen_bracket_requires_a_bracket_result():
    with pytest.raises(ValueError, match='BracketReplayResult'):
        sa().ScreenBracket(None, (False, False), ((), ()))
