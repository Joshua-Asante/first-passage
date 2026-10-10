"""T00 screen authority: rows A1-A11, K1-K4, X2, X3 (design 2026-10-02 §2.2, §3; card §2.3).

TEST_ONLY keys are generated in-process. Only the pinned root (``SOURCE_SIGNING_KEYS`` and the
compiled source constants through ``build_source_case``, plus the compiled r3c digest) and the
validator's ``REPOSITORY_ROOT`` are replaced; the K rows also install a stand-in for the screen
bootstrap's recorder (``sys.p7_recorder``), the process state the real bootstrap sets (design
§13). The repository is a synthetic git repository whose #581 copy carries the A5/A6 section
bytes of #581's Git blob at HEAD (public text; never the checkout, whose EOLs may differ). No test reads the real source. Each row test asserts its row's
code and has a passing twin; the module is imported inside each test, so a missing module fails
the row rather than erroring at collection.
"""
from __future__ import annotations

# Row-named tests (design §10), pytest fixtures and the stand-in recorder attribute on sys:
# pylint: disable=invalid-name,redefined-outer-name,no-member,missing-function-docstring

import base64
from contextlib import contextmanager
import dataclasses
import errno
import hashlib
import importlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
from datetime import timedelta
from types import SimpleNamespace

import pytest

from c1_rail.book_policy import IDENTITY_SIZE_VECTOR
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
# The successor purpose (build card 2026-10-10 §2.5, S-3 to S-7): #733's path, step 12's compiled
# RNG roots, and a TEST_ONLY non-identity size vector (Aegis base 7). It is not the frozen vector.
SUCCESSOR_PREREG = 'docs/briefs/pre-registration/2026-10-08-tradeify-book-successor-screen-prereg-DRAFT.md'
STARTUP_V2 = 'qualification-source-startup/v2'
TEST_SIZING = dict(IDENTITY_SIZE_VECTOR.as_mapping(), aegis_6j={'base': 7, 'adds': 'UNCHANGED'})
ORIGINAL = ('T00_STEP3_SELECTED_BOOK_SCREEN', ['T00_STEP3_SCREEN_ONCE'], 'T00_STEP3_SCREEN')
SUCCESSOR = ('T00_SUCCESSOR_SCREEN', ['T00_SUCCESSOR_SCREEN_ONCE'], 'T00_SUCCESSOR_SCREEN')


def sa():
    return importlib.import_module('c1_rail.qualification.screen_authority')


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git(root, *args, env=None):
    return subprocess.run(['git', '-C', str(root), '-c', 'user.email=pa@test', '-c', 'user.name=pa-test',
                           '-c', 'core.autocrlf=false', '-c', 'commit.gpgsign=false', *args],
                          check=True, capture_output=True, env=None if env is None else {**os.environ, **env},
                          ).stdout.decode('utf-8').strip()


def tracked_blob(relative: str, root: Path = REPO, rev: str = 'HEAD') -> bytes:
    """Git blob bytes, independent of the checkout's EOL conversion (a CRLF clone changes A6's digest)."""
    return subprocess.run(['git', '-C', str(root), 'cat-file', 'blob', f'{rev}:{relative}'],
                          check=True, capture_output=True).stdout


def pinned_sections(root: Path = REPO) -> str:
    """#581's A5 and A6 section bytes from its blob, checked against the compiled pins."""
    blob = tracked_blob(PREREG, root)
    a5, a6 = verdict.section_text(blob, 'A5'), verdict.section_text(blob, 'A6')
    assert (sha(a5), sha(a6)) == (verdict.A5_TEXT_SHA256, verdict.A6_TEXT_SHA256)
    return (a5 + a6).decode('utf-8')


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
                 a3_unanswered=False, crlf=False, param_changes=None, side_ratified=None, extra_files=None,
                 install_tree=None, r3d=False, purpose=None, startup=None, r3d_edit=None):
        self.monkeypatch = monkeypatch
        # Card-owner ruling 2026-10-04 (4): the install-tree digest is stubbed here, as the
        # interpreter binding is synthetic; test_p7_rrec.py computes the real digest once.
        monkeypatch.setattr(p7_evidence, 'install_tree_sha256',
                            install_tree or (lambda site, base=None: 'e' * 64), raising=False)
        self.ledger = None
        self.artifact_root = root / 'private'
        self.case = build_source_case(self.artifact_root, monkeypatch)
        self.r3d = r3d
        self.purpose = (SUCCESSOR if r3d else ORIGINAL) if purpose is None else purpose
        self.prereg_path = SUCCESSOR_PREREG if self.purpose == SUCCESSOR else PREREG
        if r3d:
            self._derive_r3d(startup, r3d_edit)
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
        if self.purpose == SUCCESSOR:
            self.params.update(expressions={'base': 'DECLARED_BOOK', 'size_vector_sha256': sha(canonical(TEST_SIZING))},
                               rng=dict(self.params['rng'], probe_root='probe-successor'))
        self.params.update(param_changes or {})
        sections = pinned_sections()
        if crlf:
            sections = sections.replace('\n', '\r\n')
        if a6_byte:
            head, tail = sections.split('### A6', 1)
            sections = head + '### A6' + tail.replace(' the ', ' thE ', 1)
        self.repo = repo = root / 'repo'
        repo.mkdir()
        git(repo, 'init', '-q')
        write(repo, MODULE, '"""TEST_ONLY loaded module."""\n')
        for relative, content in (extra_files or {}).items():
            write(repo, relative, content)
        write(repo, ORB, successor('| ORB-3 ', answered=not a3_unanswered, mapping_marker=a3_unanswered))
        write(repo, VAN, successor('| VAN-3 '))
        write(repo, self.prereg_path, prereg_text(sections, self.params, status='DRAFT — NOT RATIFIED'))
        git(repo, 'add', '-A')
        git(repo, 'commit', '-q', '-m', 'TEST_ONLY draft')
        self.side = None
        if side_ratified is not None:
            # A side branch ratifies first (env: its commit dates), main ratifies with the same
            # bytes, and the merge is TREESAME to both parents, so path-limited history drops it.
            main = git(repo, 'rev-parse', '--abbrev-ref', 'HEAD')
            git(repo, 'checkout', '-q', '-b', 'side')
            write(repo, self.prereg_path, prereg_text(sections, self.params))
            git(repo, 'commit', '-q', '-am', 'TEST_ONLY side ratify', env=side_ratified)
            self.side = git(repo, 'rev-parse', 'HEAD')
            git(repo, 'checkout', '-q', main)
        write(repo, self.prereg_path, prereg_text(sections, self.params))
        git(repo, 'commit', '-q', '-am', 'TEST_ONLY ratify')
        self.ratifying = git(repo, 'rev-parse', 'HEAD')
        if self.side is not None:
            git(repo, 'merge', '-q', '--no-ff', '-m', 'TEST_ONLY merge side', 'side')
        later = cells({2: 'values block: `pass_floor_halves` (edited)'}) if cprime_cell else None
        write(repo, self.prereg_path, prereg_text(sections, self.params, ratifying=f'`{self.ratifying}`', row_cells=later))
        git(repo, 'commit', '-q', '-am', 'TEST_ONLY record the ratifying SHA')
        self.head = git(repo, 'rev-parse', 'HEAD')
        git(repo, 'update-ref', 'refs/remotes/origin/main', self.head)
        self.interpreter = p7_evidence.current_interpreter_binding(repo)
        self.record = self._record(p7_evidence.P7_BOOTSTRAP_SHA256)
        self.authority = self.document(self.record)

    def _derive_r3d(self, startup, r3d_edit):
        """The synthetic case is r3c; r3d is r3c with only ``contract_id`` and the startup-policy row
        changed (card §7 step 2), over a v2 startup policy whose fields other than ``sizing`` are r3c's."""
        r3c = self.case.document
        self.r3c_sha256, self.r3c_id = sha(self.case.contract_bytes()), r3c['contract_id']
        self.r3c_row = next(row for row in r3c['artifacts'] if row['role'] == 'source_startup_policy')
        v1 = json.loads(self.case.payloads['source_startup_policy'])
        raw = canonical(dict(v1, schema=STARTUP_V2, sizing=TEST_SIZING)) if startup is None else startup(v1)
        self.startup_path = 'retained/source_startup_policy_v2.bin'
        (self.artifact_root / self.startup_path).write_bytes(raw)
        row = dict(self.r3c_row, path=self.startup_path, sha256=sha(raw))
        doc = dict(r3c, contract_id='TEST_ONLY-r3d',
                   artifacts=[row if old is self.r3c_row else old for old in r3c['artifacts']])
        self.r3c_case = self.case
        self.case = dataclasses.replace(self.case, document=doc if r3d_edit is None else r3d_edit(doc, self))

    def _record(self, bootstrap_sha256, contract_sha256=None, contract_bytes=None):
        closure = {'first_party': {'c1_rail.qualification.t00_screen_fixture': {
                       'path': MODULE, 'sha256': sha((self.repo / MODULE).read_bytes())}},
                   'third_party': {}, 'distributions': {}, 'stdlib': [], 'ports': {}}
        record = {'schema': p7_evidence.RECORD_SCHEMA,
                  'contract_sha256': contract_sha256 or self.receipt.contract_sha256,
                  'code_head': self.head, 'bootstrap_sha256': bootstrap_sha256,
                  'code_closure_sha256': sha(p7_evidence.canonical(closure)), 'loaded_closure': closure,
                  'interpreter': self.interpreter,
                  'contract_b64': base64.b64encode(contract_bytes or self.case.contract_bytes()).decode('ascii'),
                  'approval_b64': base64.b64encode(self.receipt.approval_bytes).decode('ascii'),
                  'result': {'labels': []}}
        return p7_evidence.canonical(record)

    def document(self, record_bytes):
        record = p7_evidence.parse_record(record_bytes)
        blob = (self.repo / self.prereg_path).read_bytes()
        purpose, grants, evidence_class = self.purpose
        return {
            'schema': 't00_screen_authority/v1', 'authority_id': 'TEST_ONLY-screen-authority',
            'purpose': purpose, 'grants': grants, 'refusals': REFUSALS,
            'evidence_class': evidence_class, 'source': {'contract_sha256': self.receipt.contract_sha256},
            'run_root_sha256': sha(str((self.artifact_root / 't00-step3').resolve()).encode('utf-8')),
            'p7': {'record_sha256': sha(record_bytes), 'code_head': record['code_head'],
                   'code_closure_sha256': record['code_closure_sha256'],
                   'bootstrap_sha256': record['bootstrap_sha256'], 'interpreter': record['interpreter']},
            'prereg': {'path': self.prereg_path, 'ratifying_commit': self.ratifying, 'commit': self.head,
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
        if not self.r3d:
            self.monkeypatch.setattr(module, 'R3C_CONTRACT_SHA256', self.receipt.contract_sha256)
            return module
        # The successor counterparts of the compiled r3c digest (card §2.2): r3c's id and startup row.
        self.monkeypatch.setattr(module, 'R3C_CONTRACT_SHA256', self.r3c_sha256)
        self.monkeypatch.setattr(module, 'R3C_CONTRACT_ID', self.r3c_id, raising=False)
        self.monkeypatch.setattr(module, 'R3C_STARTUP_POLICY_ROW', dict(self.r3c_row), raising=False)
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


# ---- W. the successor purpose (build card 2026-10-10 §2.5) ------------------------------------

@pytest.fixture
def successor_screen(tmp_path, monkeypatch):
    return Screen(tmp_path / 'successor', monkeypatch, r3d=True)


def with_purpose(doc, purpose, grants, evidence_class):
    return dict(doc, purpose=purpose, grants=grants, evidence_class=evidence_class)


def test_W1(successor_screen):
    """Successor constants and closed document; a mixed purpose, grant or evidence class is refused."""
    module = sa()
    assert (module.SUCCESSOR_PURPOSE, list(module.SUCCESSOR_GRANTS), module.SUCCESSOR_EVIDENCE_CLASS) == SUCCESSOR
    assert module.PREREG_CHAIN == (PREREG, SUCCESSOR_PREREG)
    assert module.STEP12_RNG_ROOTS == ('42', '123', '2026', 'probe')
    profile = module.PURPOSE_PROFILES[module.SUCCESSOR_PURPOSE]
    assert (list(profile.grants), profile.evidence_class, profile.chain_entry) == (*SUCCESSOR[1:], 1)
    assert module.PURPOSE_PROFILES[module.SCREEN_PURPOSE].chain_entry == 0
    doc = successor_screen.authority
    for mixed in (with_purpose(doc, SUCCESSOR[0], ORIGINAL[1], SUCCESSOR[2]),
                  with_purpose(doc, SUCCESSOR[0], SUCCESSOR[1], ORIGINAL[2]),
                  with_purpose(doc, ORIGINAL[0], SUCCESSOR[1], SUCCESSOR[2]),
                  dict(doc, size_vector_sha256='a' * 64)):
        refused('SCREEN_AUTHORITY_FIELDS', lambda mixed=mixed: successor_screen.validate(doc=mixed))
    auth = successor_screen.validate()
    assert auth.evidence_class == SUCCESSOR[2] and auth.prereg['path'] == SUCCESSOR_PREREG


def test_W2(screen):
    """Regression: a #581 authority under the original purpose validates exactly as at base, and
    the original refuses the successor's chain entry and expressions as before."""
    auth = screen.validate()
    assert (auth.evidence_class, auth.prereg['path'], auth.parameters['expressions']) == \
        ('T00_STEP3_SCREEN', PREREG, 'DECLARED_BOOK')
    assert auth.authority_sha256 == sha(canonical(screen.authority))
    refused('SCREEN_AUTHORITY_FIELDS', lambda: screen.validate(
        doc=dict(screen.authority, prereg=dict(screen.authority['prereg'], path=SUCCESSOR_PREREG))),
        'compiled constant')
    expressions = {'base': 'DECLARED_BOOK', 'size_vector_sha256': sha(canonical(TEST_SIZING))}
    refused('SCREEN_PARAMETER_UNSUPPORTED', lambda: screen.validate(
        doc=dict(screen.authority, parameters=dict(screen.params, expressions=expressions))), 'expressions')


def test_W3(successor_screen, tmp_path, monkeypatch):
    """Under the successor, receipt, authority and P7 record carry one contract digest; r3c's digest is
    refused under the successor and a successor digest under the original."""
    s = successor_screen
    auth = s.validate()
    assert auth.source_receipt.contract_sha256 == s.receipt.contract_sha256 != s.r3c_sha256
    refused('SCREEN_SOURCE_MISMATCH', lambda: s.validate(
        doc=dict(s.authority, source={'contract_sha256': s.r3c_sha256})))
    r3c_record = s._record(p7_evidence.P7_BOOTSTRAP_SHA256, contract_sha256=s.r3c_sha256)  # pylint: disable=protected-access
    refused('SCREEN_P7_MISMATCH', lambda: s.validate(doc=s.document(r3c_record), record=r3c_record), 'not over')
    r3c_receipt = s.r3c_case.validate()
    r3c_doc = dict(s.document(r3c_record), source={'contract_sha256': s.r3c_sha256})
    refused('SCREEN_SOURCE_MISMATCH', lambda: s.validate(doc=r3c_doc, receipt=r3c_receipt, record=r3c_record))
    original = Screen(tmp_path / 'original', monkeypatch, r3d=True, purpose=ORIGINAL)
    refused('SCREEN_SOURCE_MISMATCH', original.validate, 'compiled r3c digest')


def test_W3_p7_payload_binds_the_successor_contract(successor_screen):
    """Codex P1 on #764: a P7 record whose payload is r3c's contract, with only its contract_sha256
    field set to r3d's digest, is refused under the successor; the record over r3d is accepted."""
    s = successor_screen
    forged = s._record(p7_evidence.P7_BOOTSTRAP_SHA256,  # pylint: disable=protected-access
                       contract_bytes=s.r3c_case.contract_bytes())
    refused('SCREEN_P7_MISMATCH', lambda: s.validate(doc=s.document(forged), record=forged), 'contract_b64')
    s.validate()


def test_W4(tmp_path, monkeypatch):
    """An r3d with one other role changed (cost_model) fails the derivation check."""
    def other_cost_model(doc, screen):
        raw = b'TEST_ONLY another cost model'
        (screen.artifact_root / 'retained/cost_model_other.bin').write_bytes(raw)
        return dict(doc, artifacts=[dict(row, path='retained/cost_model_other.bin', sha256=sha(raw))
                                    if row['role'] == 'cost_model' else row for row in doc['artifacts']])
    bad = Screen(tmp_path / 'bad', monkeypatch, r3d=True, r3d_edit=other_cost_model)
    refused('SCREEN_SOURCE_MISMATCH', bad.validate, 'derivation')
    Screen(tmp_path / 'good', monkeypatch, r3d=True).validate()


def test_W5(tmp_path, monkeypatch):
    """The size vector binding: a size_vector_sha256 mismatch, a v1 policy, the identity v2 vector,
    startup bytes off the receipt digest, a v2 policy differing from r3c's v1 outside ``sizing``, and
    r3c's startup bytes missing. Each refused."""
    identity = IDENTITY_SIZE_VECTOR.as_mapping()

    def case(name, **kwargs):
        return Screen(tmp_path / name, monkeypatch, r3d=True, **kwargs)
    refused('SCREEN_PARAMETER_UNSUPPORTED', case('sha', param_changes={'expressions': {
        'base': 'DECLARED_BOOK', 'size_vector_sha256': 'f' * 64}}).validate, 'size_vector_sha256')
    refused('SCREEN_PARAMETER_UNSUPPORTED', case('v1', startup=lambda v1: json.dumps(v1, indent=1).encode()).validate,
            'v2')
    refused('SCREEN_PARAMETER_UNSUPPORTED', case(
        'identity', startup=lambda v1: canonical(dict(v1, schema=STARTUP_V2, sizing=identity)),
        param_changes={'expressions': {'base': 'DECLARED_BOOK', 'size_vector_sha256': sha(canonical(identity))}},
    ).validate, 'identity')
    drifted = case('bytes')
    (drifted.artifact_root / drifted.startup_path).write_bytes(b'{}')
    refused('SCREEN_SOURCE_MISMATCH', drifted.validate, 'startup')

    def richer(v1):
        legs = dict(v1['legs'], aegis_6j=dict(v1['legs']['aegis_6j'], paper_initial_capital='90000'))
        return canonical(dict(v1, schema=STARTUP_V2, sizing=TEST_SIZING, legs=legs))
    refused('SCREEN_SOURCE_MISMATCH', case('fields', startup=richer).validate, "r3c's")
    missing = case('missing')
    (missing.artifact_root / missing.r3c_row['path']).unlink()
    refused('SCREEN_SOURCE_MISMATCH', missing.validate, 'startup')
    case('good').validate()


def test_W6(successor_screen, tmp_path, monkeypatch):
    """A step-12 root, or the step-12 probe root, is refused under the successor."""
    s = successor_screen
    for rng in (dict(s.params['rng'], roots=['42', 'root-b', 'root-c']), dict(s.params['rng'], probe_root='probe')):
        refused('SCREEN_PARAMETER_UNSUPPORTED', lambda rng=rng: s.validate(
            doc=dict(s.authority, parameters=dict(s.params, rng=rng))), 'rng')
    s.validate()
    step12 = {'tag': 't00-screen-rng/v1', 'roots': ['42', '123', '2026'], 'probe_root': 'probe'}
    Screen(tmp_path / 'original', monkeypatch, param_changes={'rng': step12}).validate()  # the original keeps them


def test_W7(successor_screen):
    """Cross-binding of purpose and chain entry is refused both ways."""
    s = successor_screen
    for doc in (with_purpose(s.authority, *ORIGINAL), s.authority):
        path = PREREG if doc is s.authority else SUCCESSOR_PREREG
        crossed = dict(doc, prereg=dict(doc['prereg'], path=path))
        refused('SCREEN_AUTHORITY_FIELDS', lambda crossed=crossed: s.validate(doc=crossed), 'compiled constant')
    s.validate()


def test_W8(tmp_path, monkeypatch):
    """A successor pre-registration with one byte changed in A6 is refused (A9 under the new purpose)."""
    bad = Screen(tmp_path / 'bad', monkeypatch, r3d=True, a6_byte=True)
    refused('SCREEN_PREREG_MISMATCH', bad.validate, 'A5/A6')
    Screen(tmp_path / 'good', monkeypatch, r3d=True).validate()


@WINDOWS
def test_W10(successor_screen):
    """``require_validated_screen_authority`` refuses a source contract other than the authority's
    bound digest under the successor, and serves the bound r3d receipt."""
    s = successor_screen
    auth = s.validate()
    r3c_receipt = s.r3c_case.validate()
    with s.ready(auth):
        refused('SCREEN_SOURCE_MISMATCH', lambda: require(auth, receipt=r3c_receipt))
        assert require(auth) is auth


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
    assert module.PREREG_CHAIN[0] == PREREG and set(module.A3_SUCCESSORS) == {ORB, VAN}
    pinned_sections()
    for path, (prefix, exposure, owed) in module.A3_SUCCESSORS.items():
        lines = tracked_blob(path).decode('utf-8').split('\n')
        rows = [i for i, line in enumerate(lines) if line.startswith(prefix)]
        assert rows and [i for i, line in enumerate(lines) if exposure.search(line)] == [rows[0]]
        assert owed.search(lines[rows[0]]) is None


def test_compiled_r3c_successor_constants_are_r3c_shaped_and_derive_their_own_restoration(tmp_path):
    """The compiled r3c id and startup row are r3c-contract-shaped (validate_source_contract's row
    rules), and the derivation check restores exactly them. Their agreement with the compiled r3c
    digest needs r3c's private bytes, so it is checked at r3d assembly (card §7 step 2), not here."""
    module = sa()
    row = dict(module.R3C_STARTUP_POLICY_ROW)
    assert module.R3C_CONTRACT_SHA256 == 'a526b50fa75e68451bdd2b5b57fa7a04e6ee08e61f96865c915ae8116a848d97'
    assert module.R3C_CONTRACT_ID == 't00-p7-source-contract-r3c'
    assert set(row) == {'role', 'path', 'sha256', 'producer', 'authority_class'}
    assert (row['role'], row['authority_class']) == ('source_startup_policy', 'PRODUCTION_REVIEWED')
    assert module._hex(row['sha256']) and all(type(v) is str and v for v in row.values())  # pylint: disable=protected-access
    # A synthetic r3c-shaped document over the compiled row: an r3d with another id and startup
    # row derives back to it exactly when R3C_CONTRACT_SHA256 is that document's digest.
    other = {'role': 'cost_model', 'path': 'x', 'sha256': 'b' * 64, 'producer': 'p',
             'authority_class': 'PRODUCTION_REVIEWED'}
    r3c = {'contract_id': module.R3C_CONTRACT_ID, 'artifacts': [other, row]}
    r3d = dict(r3c, contract_id='TEST_ONLY-r3d', artifacts=[other, dict(row, path='y', sha256='c' * 64)])
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(module, 'R3C_CONTRACT_SHA256', sha(canonical(r3c)))
        assert module._derived_from_r3c(r3d)  # pylint: disable=protected-access
        assert not module._derived_from_r3c(dict(r3d, artifacts=[dict(other, sha256='d' * 64), r3d['artifacts'][1]]))  # pylint: disable=protected-access


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
    recorder = SimpleNamespace(first_party={}, third_party={}, ports={}, stdlib=set())
    screen.monkeypatch.setattr(sys, 'p7_recorder', recorder, raising=False)
    cover_loaded(recorder)
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


def test_crlf_checkout_keeps_the_pinned_fixture_and_validation_refuses_crlf_sections(tmp_path, monkeypatch):
    """A CRLF working file (a Windows autocrlf clone) leaves the fixture's blob-derived A5/A6
    digests pinned, and production validation stays byte-exact: CRLF section bytes are refused."""
    tree = tmp_path / 'checkout'
    tree.mkdir()
    git(tree, 'init', '-q')
    lf = tracked_blob(PREREG)
    write(tree, PREREG, lf.decode('utf-8'))
    git(tree, 'add', '-A')
    git(tree, 'commit', '-q', '-m', 'TEST_ONLY #581 blob')
    (tree / PREREG).write_bytes(lf.replace(b'\n', b'\r\n'))
    assert sha(verdict.section_text((tree / PREREG).read_bytes(), 'A6')) != verdict.A6_TEXT_SHA256
    assert pinned_sections(tree) == pinned_sections()
    refused('SCREEN_PREREG_MISMATCH', Screen(tmp_path / 'crlf', monkeypatch, crlf=True).validate, 'A5/A6')


# ---- epoch close over the recorder's full loaded closure (card ruling 2026-10-04) ------------

class FakeSource:  # pylint: disable=too-few-public-methods
    """Stands in for ProductionSource at close; its full integrity check passes."""

    def _verify_integrity(self):
        return None


SOURCE = FakeSource()  # epochs hold their source weakly; the worker keeps it alive


def cover_loaded(recorder):
    """Synthetic only: every module already in this process counts as a stdlib name (no bytes),
    so a test's own unrecorded module is the only one without a load digest."""
    recorder.stdlib |= set(sys.modules) - set(recorder.first_party) - set(recorder.third_party)


def closure_case(screen, tmp_path):
    """A validated authority and a recorder with one stable dependency in every family."""
    module = sa()
    auth = screen.validate()
    site = tmp_path / 'site'
    site.mkdir()
    (site / 'dep.py').write_bytes(b'VALUE = 1\n')
    port = auth.source_receipt.artifacts[0]  # synthetic file; port keys are compile filenames (artifact paths)
    recorder = SimpleNamespace(
        first_party={'c1_rail.qualification.t00_screen_fixture': {
            'path': MODULE, 'sha256': sha((screen.repo / MODULE).read_bytes())}},
        third_party={'dep': {'path': 'dep.py', 'sha256': sha(b'VALUE = 1\n')}},
        ports={port.path: port.sha256}, stdlib={'t00_screen_stdlib_name'}, site_packages_path=str(site))
    screen.monkeypatch.setattr(sys, 'p7_recorder', recorder, raising=False)
    files = {'first_party': screen.repo / MODULE, 'third_party': site / 'dep.py',
             'ports': screen.artifact_root / port.path}
    return module, auth, recorder, files


def closes(module, auth, recorder, change=None):
    epoch = module.open_screen_epoch(SOURCE, auth)
    if change is not None:
        change()
    cover_loaded(recorder)
    return module.close_screen_epoch(epoch)


def load_unrecorded(screen, path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    screen.monkeypatch.setitem(sys.modules, name, loaded)
    spec.loader.exec_module(loaded)


def test_epoch_close_passes_stable_dependencies_in_every_family(screen, tmp_path):
    module, auth, recorder, _ = closure_case(screen, tmp_path)
    closed = closes(module, auth, recorder)
    assert closed.closure_match
    assert closed.closure_sha256 == sha(canonical({
        'first_party': recorder.first_party, 'third_party': recorder.third_party, 'ports': recorder.ports,
        'stdlib': sorted(recorder.stdlib)}))


@pytest.mark.parametrize('family', ['first_party', 'third_party', 'ports'])
def test_epoch_close_refuses_a_changed_recorded_dependency(screen, tmp_path, family):
    """A replaced file in a recorded family closes closure_match=False (CODE_OR_ARTIFACT_DRIFT)."""
    module, auth, recorder, files = closure_case(screen, tmp_path)
    assert closes(module, auth, recorder).closure_match
    changed = closes(module, auth, recorder,
                     lambda: files[family].write_bytes(files[family].read_bytes() + b'# replaced\n'))
    assert not changed.closure_match


@pytest.mark.parametrize('family', ['first_party', 'third_party', 'ports', 'stdlib', 'third_party_file'])
def test_epoch_close_refuses_a_disappeared_recorded_dependency(screen, tmp_path, family):
    """A dependency recorded at open that is gone at close (from the record, or from disk) is drift."""
    module, auth, recorder, files = closure_case(screen, tmp_path)
    assert closes(module, auth, recorder).closure_match
    gone = {'first_party': recorder.first_party.clear, 'third_party': recorder.third_party.clear,
            'ports': recorder.ports.clear, 'stdlib': lambda: recorder.stdlib.discard('t00_screen_stdlib_name'),
            'third_party_file': lambda: os.replace(files['third_party'], files['third_party'].with_suffix('.gone'))}
    assert not closes(module, auth, recorder, gone[family]).closure_match


def test_epoch_close_accepts_a_lazy_import_recorded_mid_epoch_with_its_digest(screen, tmp_path):
    module, auth, recorder, files = closure_case(screen, tmp_path)
    late = files['third_party'].parent / 't00_screen_lazy_dep.py'
    late.write_bytes(b'LATE = 1\n')

    def lazy_import():
        recorder.third_party['t00_screen_lazy_dep'] = {'path': late.name, 'sha256': sha(late.read_bytes())}
        load_unrecorded(screen, late, 't00_screen_lazy_dep')
    epoch = module.open_screen_epoch(SOURCE, auth)
    lazy_import()
    cover_loaded(recorder)
    closed = module.close_screen_epoch(epoch)
    assert closed.closure_match and closed.closure_sha256 != epoch.closure_sha256
    recorder.third_party['t00_screen_lazy_dep']['sha256'] = sha(b'OTHER = 1\n')
    assert not closes(module, auth, recorder).closure_match


def test_epoch_close_refuses_a_loaded_but_unrecorded_executable(screen, tmp_path):
    module, auth, recorder, files = closure_case(screen, tmp_path)
    assert closes(module, auth, recorder).closure_match
    stray = files['third_party'].parent / 't00_screen_unrecorded_dep.py'
    stray.write_bytes(b'STRAY = 1\n')
    epoch = module.open_screen_epoch(SOURCE, auth)
    cover_loaded(recorder)
    load_unrecorded(screen, stray, 't00_screen_unrecorded_dep')
    assert not module.close_screen_epoch(epoch).closure_match


@pytest.mark.parametrize('family', ['third_party', 'ports'])
def test_epoch_close_refuses_a_recorded_digest_replaced_by_a_reload(screen, tmp_path, family):
    """The recorder overwrites a third-party or port entry when it is found or compiled again;
    a reload with changed bytes mid-epoch is drift, and a reload with identical bytes is not."""
    module, auth, recorder, files = closure_case(screen, tmp_path)
    path = files[family]
    key = 'dep' if family == 'third_party' else next(iter(recorder.ports))

    def reload(raw):
        def change():
            path.write_bytes(raw)
            if family == 'third_party':
                recorder.third_party[key] = dict(recorder.third_party[key], sha256=sha(raw))
            else:
                recorder.ports[key] = sha(raw)
        return change
    assert closes(module, auth, recorder, reload(path.read_bytes())).closure_match
    assert not closes(module, auth, recorder, reload(path.read_bytes() + b'# reloaded\n')).closure_match


SCREEN_WORKER = """import json
import sys
from c1_rail.qualification import p7_evidence, screen_authority
closure = screen_authority._closure()
named = {n for f in ('first_party', 'third_party') for n in closure[f]} | set(closure['stdlib'])
rooted = sorted(n for n, m in list(sys.modules.items()) if n not in named and isinstance(
    getattr(getattr(m, '__spec__', None), 'origin', None) or getattr(m, '__file__', None), str)
    and (getattr(getattr(m, '__spec__', None), 'origin', None) or '') not in ('built-in', 'frozen'))
print(json.dumps({'screen_bootstrap': sys.p7_recorder.bootstrap_sha256 == p7_evidence.SCREEN_BOOTSTRAP_SHA256,
                  'unrecorded': list(screen_authority._unrecorded(closure)), 'unnamed_with_origin': rooted,
                  'recorded': {family: len(rows) for family, rows in closure.items()},
                  'refusals': list(sys.p7_recorder.refusals)}))
"""


def test_a_real_screen_bootstrap_process_has_no_unrecorded_loaded_module(screen, tmp_path):
    """The real SCREEN_BOOTSTRAP and recorder, in a child interpreter over a TEST_ONLY copy of
    ops/core with a synthetic worker: every loaded module is recorded or interpreter-rooted."""
    from test_p7_evidence import make_code_root  # pylint: disable=import-outside-toplevel
    root = make_code_root(tmp_path / 'code', screen.case,
                          extra={'ops/c1_rail/qualification/t00_screen/worker.py': SCREEN_WORKER})
    run_dir = tmp_path / 'run'
    (run_dir / 'journal').mkdir(parents=True)
    done = subprocess.run([sys.executable, '-I', '-S', '-B', '-c', p7_evidence.SCREEN_BOOTSTRAP, str(root),
                           str(run_dir), 'a' * 64, 'c1-w0.jsonl'], capture_output=True, text=True, timeout=300,
                          cwd=tmp_path, check=False)
    assert done.returncode == 0, done.stderr[-2000:]
    report = json.loads(done.stdout.strip().splitlines()[-1])
    assert report['screen_bootstrap'] and not report['refusals'], report
    assert report['recorded']['first_party'] and report['recorded']['third_party'], report
    assert report['unrecorded'] == [], report
    print('UNNAMED_WITH_ORIGIN', report['unnamed_with_origin'])


def test_an_unrecorded_file_under_a_site_nested_in_a_stdlib_root_is_unrecorded(screen, tmp_path):
    """Site-first: a stdlib root that is an ancestor of site-packages does not cover an unrecorded
    installed executable; a true stdlib file under the same root is interpreter-rooted."""
    module = sa()
    stdlib_root = tmp_path / 'lib' / 'python3.x'
    site = stdlib_root / 'site-packages'
    site.mkdir(parents=True)
    (site / 't00_screen_site_unrecorded.py').write_bytes(b'SITE = 1\n')
    (stdlib_root / 't00_screen_true_stdlib.py').write_bytes(b'STDLIB = 1\n')
    recorder = SimpleNamespace(first_party={}, third_party={}, ports={}, stdlib=set(), site_packages_path=str(site),
                               installed_roots=[str(site), str(stdlib_root)])
    screen.monkeypatch.setattr(sys, 'p7_recorder', recorder, raising=False)
    cover_loaded(recorder)
    load_unrecorded(screen, stdlib_root / 't00_screen_true_stdlib.py', 't00_screen_true_stdlib')
    assert module._unrecorded(module._closure()) == ()  # pylint: disable=protected-access
    load_unrecorded(screen, site / 't00_screen_site_unrecorded.py', 't00_screen_site_unrecorded')
    assert module._unrecorded(module._closure()) == ('t00_screen_site_unrecorded',)  # pylint: disable=protected-access


# ---- review 5407704640 at ccfeba4 ------------------------------------------------------------

def test_ratified_requires_one_canonical_complete_status_field():
    """r4178909765: one Status field, in its canonical place (the line after the title and a
    blank line), whose whole backticked field is RATIFIED <valid date>."""
    module = sa()
    draft = '**Status:** `DRAFT — NOT RATIFIED.` TEST_ONLY'.encode('utf-8')
    ratified = b'**Status:** `RATIFIED 2026-10-10.` TEST_ONLY'
    assert module._ratified(b'# Title\n\n' + ratified + b'\n\nbody\n')  # pylint: disable=protected-access
    for blob in (ratified + b'\n# Title\n\n' + draft + b'\n',               # an earlier RATIFIED line
                 b'# Title\n\n' + draft + b'\n\n' + ratified + b'\n',       # an embedded later one
                 b'# Title\n\n**Status:** `RATIFIED 2026-10-10 pending` x\n',  # an incomplete field
                 b'# Title\n\n**Status:** `RATIFIED 2026-13-40.` x\n'):       # an invalid date
        assert not module._ratified(blob), blob  # pylint: disable=protected-access


@WINDOWS
def test_run_lock_is_held_only_on_the_msvcrt_lock_conflict_errno(tmp_path, monkeypatch):
    """r4178909774: msvcrt.locking(LK_NBLCK) raises EACCES on a conflict (CRT _locking: "Locking
    violation"; measured 2026-10-04); every other OSError is refused, never read as held."""
    module, msvcrt = sa(), importlib.import_module('msvcrt')
    lock = tmp_path / 'lock'
    lock.write_bytes(b'{}')
    assert not module._lock_held(lock)  # pylint: disable=protected-access
    holder = os.open(lock, os.O_RDWR | BINARY)
    try:
        os.lseek(holder, journal.LOCK_OFFSET, os.SEEK_SET)
        msvcrt.locking(holder, msvcrt.LK_NBLCK, 1)
        assert module._lock_held(lock)  # pylint: disable=protected-access
        os.lseek(holder, journal.LOCK_OFFSET, os.SEEK_SET)
        msvcrt.locking(holder, msvcrt.LK_UNLCK, 1)
    finally:
        os.close(holder)
    real = msvcrt.locking

    def failing(fd, mode, count):
        if mode == msvcrt.LK_NBLCK:
            raise OSError(errno.EBADF, os.strerror(errno.EBADF))
        return real(fd, mode, count)
    monkeypatch.setattr(msvcrt, 'locking', failing)
    refused('SCREEN_RUN_UNBOUND', lambda: module._lock_held(lock), 'lock')  # pylint: disable=protected-access


def test_epoch_close_turns_a_failed_dependency_read_into_drift(screen, tmp_path):
    """r4178909777: a recorded dependency unreadable between its existence check and its read
    closes closure_match=False (CODE_OR_ARTIFACT_DRIFT); no OSError escapes."""
    module, auth, recorder, files = closure_case(screen, tmp_path)
    assert closes(module, auth, recorder).closure_match
    target, real = files['third_party'], Path.read_bytes

    def racing(self):
        if self == target:
            raise PermissionError(errno.EACCES, 'unreadable', str(self))
        return real(self)
    unreadable = closes(module, auth, recorder, lambda: screen.monkeypatch.setattr(Path, 'read_bytes', racing))
    assert not unreadable.closure_match


def test_epoch_close_final_closure_digest_is_deterministic(screen, tmp_path):
    """Row K6 (design :151, "all epochs record the same closure"): the same loaded set gives the
    same final closure_sha256, whatever the recorder's insertion order."""
    module, auth, recorder, _ = closure_case(screen, tmp_path)
    first = closes(module, auth, recorder)
    for family in ('first_party', 'third_party', 'ports'):
        setattr(recorder, family, dict(reversed(list(getattr(recorder, family).items()))))
    recorder.stdlib = set(sorted(recorder.stdlib, reverse=True))
    second = closes(module, auth, recorder)
    assert first.closure_match and second.closure_match
    assert first.closure_sha256 == second.closure_sha256


# ---- review at ac7681e (round 3) -------------------------------------------------------------

def test_cpu_budgets_accept_finite_positive_fractions(tmp_path, monkeypatch):
    """r4179039941: budget fields are CPU seconds, "finite and positive" (design :260)."""
    budget = {'path_cpu_seconds': 1000.5, 'overhead_cpu_seconds': 100.25, 'basis': 'TEST_ONLY fractional'}
    screen = Screen(tmp_path, monkeypatch, param_changes={'budget': budget})
    assert dict(screen.validate().parameters['budget']) == budget


def test_budget_and_count_predicates_stay_separate(screen):
    """Budgets: finite positive int or float, never bool, NaN, +-inf or <= 0. Counts
    (depth_per_root, design :252; block length, :253): positive integers only."""
    module = sa()

    def params(**budget):
        return dict(screen.params, budget=dict(screen.params['budget'], **budget))
    for bad in (float('nan'), float('inf'), float('-inf'), 0, 0.0, -1.5, True):
        refused('SCREEN_PARAMETER_UNSUPPORTED', lambda b=bad: module._check_parameters(  # pylint: disable=protected-access
            params(path_cpu_seconds=b)), 'budget')
    module._check_parameters(params(path_cpu_seconds=0.5))  # pylint: disable=protected-access
    for counts in ({'depth_per_root': dict(screen.params['depth_per_root'], FULL=2.5)},
                   {'block': dict(screen.params['block'], length_sessions=1.0)}):
        name = next(iter(counts))
        refused('SCREEN_PARAMETER_UNSUPPORTED', lambda c=counts: module._check_parameters(  # pylint: disable=protected-access
            dict(screen.params, **c)), name)


@pytest.mark.parametrize('bad', [None, ['a'], {'p': 1}, 1])
def test_a3_answer_paths_are_typed_before_sorting_and_before_git(screen, bad):
    """r4179039945: a non-string a3 path refuses with SCREEN_AUTHORITY_FIELDS, never TypeError,
    and no git call runs."""
    answers = [dict(screen.authority['a3_answers'][0], path=bad), screen.authority['a3_answers'][1]]
    calls = spy_git(screen)
    refused('SCREEN_AUTHORITY_FIELDS', lambda: screen.validate(doc=dict(screen.authority, a3_answers=answers)),
            'path')
    assert not calls
    screen.validate()


SKEWED = {'GIT_AUTHOR_DATE': '2030-01-01T00:00:00+0000', 'GIT_COMMITTER_DATE': '2030-01-01T00:00:00+0000'}


@pytest.mark.parametrize('side_dates', [{}, SKEWED], ids=['in-order', 'skewed-dates'])
def test_a8_finds_a_ratified_status_on_a_merged_away_side_branch(tmp_path, monkeypatch, side_dates):
    """r4179039949, design :137 ("C is the oldest commit reachable from origin/main at which
    #581's Status reads RATIFIED"): a side-branch RATIFIED commit that is not a descendant of C,
    merged so that default path-limited history drops it, refuses; the order is topological,
    so dates that put the side commit after C change nothing."""
    bad = Screen(tmp_path / 'bad', monkeypatch, side_ratified=side_dates)
    default = git(bad.repo, 'rev-list', 'refs/remotes/origin/main', '--', PREREG).split()
    assert bad.side not in default  # the merge is TREESAME to its first parent: history simplified away
    refused('SCREEN_PREREG_MISMATCH', bad.validate, 'oldest')
    Screen(tmp_path / 'good', monkeypatch).validate()  # linear history: C is the oldest RATIFIED


def test_a_large_integer_cpu_budget_is_accepted_without_overflow(screen):
    """The design sets no budget maximum (:260), so 10**400 CPU seconds is a valid positive int;
    it never reaches a float conversion (no OverflowError)."""
    params = dict(screen.params, budget=dict(screen.params['budget'], path_cpu_seconds=10 ** 400))
    sa()._check_parameters(params)  # pylint: disable=protected-access


@WINDOWS
def test_a_fractional_budget_authority_is_issued_used_and_acted_on(tmp_path, monkeypatch):
    """End to end: issued with a fractional CPU budget, then required on use (snapshot of its
    float parameters), an epoch opened and closed, and an act over its bytes validated."""
    module = sa()
    budget = {'path_cpu_seconds': 1000.5, 'overhead_cpu_seconds': 100.25, 'basis': 'TEST_ONLY fractional'}
    screen = Screen(tmp_path, monkeypatch, param_changes={'budget': budget})
    auth = screen.validate()
    with screen.ready(auth):
        assert require(auth) is auth
        assert require(auth) is auth
    recorder = SimpleNamespace(first_party={}, third_party={}, ports={}, stdlib=set())
    monkeypatch.setattr(sys, 'p7_recorder', recorder, raising=False)
    cover_loaded(recorder)
    epoch = module.open_screen_epoch(SOURCE, auth)
    assert module.close_screen_epoch(epoch).closure_match
    assert validate_act(screen, *act(screen)).authority_sha256 == auth.authority_sha256


OUTSIDE_OPS_CORE = {'lab/t00_lab_fixture.py': 'LAB = 1\n', 't00_root_fixture.py': 'ROOT = 1\n'}


@pytest.mark.parametrize('relative', sorted(OUTSIDE_OPS_CORE))
def test_stat_guard_covers_first_party_import_roots_outside_ops_and_core(tmp_path, monkeypatch, relative):
    """r4179201913: the bootstrap permits first-party imports from core, lab, ops, ops/c1_rail,
    ops/c1_signal_daemon and the code root (p7_evidence.py:241-242; any tracked *.py under the
    code root, :228-230, :338). A recorded module there that changes after open stops the next
    guarded call (SCREEN_EPOCH_STALE) and fails the close; unchanged, both pass."""
    screen = Screen(tmp_path, monkeypatch, extra_files=OUTSIDE_OPS_CORE)
    module, auth, recorder, _ = closure_case(screen, tmp_path)
    target = screen.repo / relative
    recorder.first_party['t00_outside_fixture'] = {'path': relative, 'sha256': sha(target.read_bytes())}
    assert closes(module, auth, recorder).closure_match
    epoch = module.open_screen_epoch(SOURCE, auth)
    module.require_open_screen_epoch(epoch, source=SOURCE, authority=auth)
    target.write_bytes(target.read_bytes() + b'# changed\n')
    stat = target.stat()
    os.utime(target, ns=(stat.st_atime_ns, stat.st_mtime_ns + 1_000_000_000))
    refused('SCREEN_EPOCH_STALE', lambda: module.require_open_screen_epoch(epoch, source=SOURCE, authority=auth))
    cover_loaded(recorder)
    assert not module.close_screen_epoch(epoch).closure_match


# ---- R-REC packet classes (2) and (4): the install-tree digest at launch and every close -------

def install_case(tmp_path, monkeypatch, layout):
    """A Screen whose bound install tree is a synthetic install (test_p7_rrec.fake_install) in
    ``layout``, digested for real in that layout; the closure case's recorder is unchanged."""
    from test_p7_rrec import fake_install, tree_digest  # pylint: disable=import-outside-toplevel
    base, site, paths = fake_install(tmp_path / 'install', layout)
    real = getattr(p7_evidence, 'install_tree_sha256', None)

    def tree(_site, base=None):  # pylint: disable=unused-argument
        return tree_digest(layout, site, install_base, real) if real is not None else 'e' * 64
    install_base = base
    (tmp_path / 'screen').mkdir()
    screen = Screen(tmp_path / 'screen', monkeypatch, install_tree=tree)
    return screen, paths


INSTALL_CHANGES = {
    'stdlib': lambda paths: paths['stdlib'].write_bytes(b'STDLIB = 2\n'),
    'pycache': lambda paths: (paths['pycache'].parent / 'planted.cpython.pyc').write_bytes(b'pyc'),
    'dll': lambda paths: paths['runtime'].write_bytes(b'changed'),
    # Class (4): a site-packages file with no recorded row (never imported yet) changed after launch.
    'venv_site_unimported': lambda paths: paths['site_dep'].write_bytes(b'DEP = 2\n'),
}


@pytest.mark.parametrize('layout', ['nt', 'posix'])
@pytest.mark.parametrize('change', [None, *INSTALL_CHANGES])
def test_rrec_install_tree_changed_after_epoch_open_fails_the_close(tmp_path, monkeypatch, change, layout):
    """Classes (2) and (4): a stdlib, __pycache__, DLL or not-yet-imported venv site-packages
    file changed after the epoch opens closes closure_match=False; unchanged (twin) closes True."""
    screen, paths = install_case(tmp_path, monkeypatch, layout)
    module, auth, recorder, _ = closure_case(screen, tmp_path)
    closed = closes(module, auth, recorder, None if change is None else lambda: INSTALL_CHANGES[change](paths))
    assert closed.closure_match is (change is None)


@pytest.mark.parametrize('layout', ['nt', 'posix'])
def test_rrec_launch_refuses_a_changed_install_tree_or_a_reachable_base_site(tmp_path, monkeypatch, layout):
    """At launch (row A5's interpreter-binding check): the bound tree digest must hold, and the
    base install's site-packages must be unreachable (card-owner ruling 2026-10-04 (1))."""
    screen, paths = install_case(tmp_path, monkeypatch, layout)
    assert screen.validate().authority_sha256  # twin
    base_site = os.path.join(sys.base_prefix, *p7_evidence.site_packages_relative().split('/'))
    if os.path.normcase(os.path.realpath(base_site)) != os.path.normcase(screen.interpreter['site_packages_path']):
        with monkeypatch.context() as patch:
            patch.setattr(sys, 'path', [*sys.path, base_site])
            refused('SCREEN_P7_MISMATCH', screen.validate, 'interpreter')
    INSTALL_CHANGES['stdlib'](paths)
    refused('SCREEN_P7_MISMATCH', screen.validate, 'interpreter')


def test_epoch_close_exposes_the_full_final_closure(screen, tmp_path):
    """P-D follow-up ruling (K6 amendment): the close carries the full final closure for the
    EPOCH_CLOSE writer, with closure_sha256 its canonical digest."""
    module, auth, recorder, _ = closure_case(screen, tmp_path)
    closed = closes(module, auth, recorder)
    assert closed.closure_match
    assert closed.closure == {'first_party': recorder.first_party, 'third_party': recorder.third_party,
                              'ports': recorder.ports, 'stdlib': sorted(recorder.stdlib)}
    assert closed.closure_sha256 == sha(canonical(closed.closure))
    recorder.third_party['dep']['sha256'] = 'f' * 64
    assert closed.closure['third_party']['dep']['sha256'] != 'f' * 64, 'the close holds a copy'
