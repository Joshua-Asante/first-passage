"""S8 integrated full-E1 acceptance on the canonical host (TEST_ONLY), prepared
before the integrated candidate exists (ticket G; plan
2026-09-18-full-e1-execution-slices.md section S8).

Selection: ``--s8`` only (FP_QUALIFICATION_S8=1 on top of the S5 environment,
which the integrated installation seam must honour); ``--test-only`` ignores
this file. Location: beside the boundary harness, because the installed-route
cases share its session-scoped ``real_boundary`` (one install per host); the
plan named tests/ops/qualification/execution/.

Declarations precede any admission and never change after a campaign is
observed: ``EXPECTED_VERDICTS`` (per actual synthetic source scenario: stage
statuses in result-aggregate vocabulary, Part A facts and the admitted ORB
port identity) and ``COVERAGE`` (one proposed invariant-manifest row per
E01-E12; not registered until these cases exist and pass on the integrated
candidate).

Interface policy: a case whose route needs an interface absent from this
checkout (the T05 result/seal modules, operations and the result_g5 role) is
``xfail(strict=True, raises=IntegrationAbsent, reason='awaits integrated
candidate')``. The absence check runs first, before any host fixture, so the
xfail is decided on every platform and an unexpected pass fails. Installed-
route and OS-property cases need the disposable Linux host; no mock substitutes.

Disclosures carried from S5: on the (2, 4, 2) depth-60 fixture prescribed
expansion and p5-above-FULL are unreachable, so E04's above-FULL leg and E05's
expansion/tolerance legs stand on the named arithmetic boundary nodes, which
are never called full-route witnesses. The frozen-engine establishment runs
only in the S8 selection (the N2 compute is minutes per scenario). No qseal
diagnostic hold exists, so E10/E12's seal-side windows are not barrier-exact.

Known conflict (E03, n2_full_fails): the frozen T05 aggregate (6cf2732
``_row_outcome``/``parse_receipt_row``) admits a failure only on the last stage
of a prefix and puts the joint batch's decision on PART_B, while the canonical
policy (``required_output_roles``: LEGALITY..PART_B COMPLETE/FAIL) and spec E03
admit FULL failing with both halves passing. This file asserts the canonical
split; the integrated candidate fails it until that is ruled.
"""
# Linux-only route helpers and the engine load at call time; the T05 interface
# probe reads the protocol's closed operation table.
# pylint: disable=import-outside-toplevel,protected-access
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

_QUALIFICATION = str(Path(__file__).resolve().parents[2] / 'ops' / 'qualification')
if _QUALIFICATION not in sys.path:
    sys.path.insert(0, _QUALIFICATION)

import campaign_sources  # noqa: E402  pylint: disable=wrong-import-position
from campaign_driver import (  # noqa: E402  pylint: disable=wrong-import-position
    RESULT_RECEIPT_FIELDS, RESULT_RECEIPT_SCHEMA, RESULT_WORK, SEAL_RECEIPT_FIELDS,
    SEAL_RECEIPT_SCHEMA, SEAL_WORK, CampaignDriver, accepted_prefix, expected_launch_counts,
    launch_counts, plan, result_outcome, terminal_state)

REPO = Path(__file__).resolve().parents[3]
HERE = 'tests/integration/qualification_boundary/test_full_campaign_boundary.py'
AWAITING = 'awaits integrated candidate'


# ---- Declarations (before any admission) -----------------------------------

_ALL_PASS = {'LEGALITY': 'PASS', 'N1': 'PASS', 'N2': 'PASS', 'PART_B': 'PASS', 'PART_A': 'PASS'}
EXPECTED_VERDICTS = {
    'trading': {
        'stages': _ALL_PASS,
        'part_a': {'expansion_required': False, 'final_panels': 2, 'failure_reason': None,
                   'prefix_preserved': True},
        'orb_port_sha256': '63ae31e1289ac17eb5dac2f9ecc46023a6a2f670d099214c603e2e95fbe53039'},
    'idle': {
        'stages': {'LEGALITY': 'PASS', 'N1': 'FAIL'},
        'part_a': None,
        'orb_port_sha256': '581ebff568ec2d797cbf28ed18323f89315b96a9132f3aa77be8b506e1db4175'},
    'n2_full_fails': {
        'stages': {'LEGALITY': 'PASS', 'N1': 'PASS', 'N2': 'FAIL', 'PART_B': 'PASS'},
        'part_a': None,
        'orb_port_sha256': 'be0940642565c4c4c32e8440b4063013b57a291e1c303a323f0bdb875e6676e3'},
    'n2_halves_fail': {
        'stages': {'LEGALITY': 'PASS', 'N1': 'PASS', 'N2': 'PASS', 'PART_B': 'FAIL'},
        'part_a': None,
        'orb_port_sha256': 'cbc1b2fc4aea4c61bb82077b02f830015de23abd1d187496883cce476470f425'},
    'part_a_below_floor': {
        'stages': {**_ALL_PASS, 'PART_A': 'FAIL'},
        'part_a': {'expansion_required': False, 'final_panels': 2,
                   'failure_reason': 'below_floor', 'prefix_preserved': True},
        'orb_port_sha256': 'b1d880c35685a08a2d9ed7c399856ad6961f9106ce647deedd93a955cdb50856'},
}
# E11: exact-depth approval lifetime for the idle (N1-only) route; long enough
# for admission plus N1, short enough to expire before the result commit.
EXPIRY_SECONDS = 300
# Paths containing both idle dates, per (stage, population); every other count is 0.
IDLE_PAIR_PLACEMENT = {
    'n2_full_fails': {('n2', 'FULL'): 1},
    'n2_halves_fail': {('n2', 'H1'): 1},
    'part_a_below_floor': {},
}


def _row(identity, requirement, producer, consumer, evidence, nodes):
    return {'id': identity, 'requirement': requirement,
            'owner': 'full-E1 S8 (coordinator acceptance)', 'producer': producer,
            'consumer': consumer, 'evidence_kind': evidence, 'test_nodeids': list(nodes)}


def _here(*names):
    return [HERE + '::' + name for name in names]


_PART_A_UNIT = 'tests/ops/qualification/execution/test_campaign_part_a.py::'
_ESTABLISH = 'test_frozen_engine_establishes_the_declared_verdict'
_ROUTE = ('qexec service, Docker workers, qg5/result-G5 units and qseal on the integrated '
          'installation')
_LINUX = 'real disposable Linux host: JUnit, retained journal/objects, receipts and cleanup'
COVERAGE = [
    _row('E01', 'Genuine PASS: protected N1, joint N2/Part B and Part A launches, G5 '
         'reconstruction, one full PASS result receipt and a separate qseal receipt, all '
         'TEST_ONLY', _ROUTE, 'CampaignStore/ResultStore/SealStore', _LINUX,
         _here(_ESTABLISH + '[trading]', 'test_e01_genuine_pass_commits_and_is_sealed_separately')),
    _row('E02', 'Genuine N1 failure: authenticated FAIL result, no N2/Part A launch, no seal',
         _ROUTE, 'ResultStore/SealStore eligibility', _LINUX,
         _here(_ESTABLISH + '[idle]', 'test_e02_n1_failure_commits_fail_without_successors')),
    _row('E03', 'FULL fails with halves passing and halves fail with FULL passing: one joint '
         'batch, both decisions, no Part A launch, authenticated FAIL, no seal', _ROUTE,
         'ResultStore/SealStore eligibility', _LINUX,
         _here(_ESTABLISH + '[n2_full_fails]', _ESTABLISH + '[n2_halves_fail]',
               'test_e03_asymmetric_joint_failure_is_one_batch[n2_full_fails]',
               'test_e03_asymmetric_joint_failure_is_one_batch[n2_halves_fail]')),
    _row('E04', 'Part A below floor and above FULL are final FAIL; the FULL sanity comparison '
         'applies after any prescribed expansion (arithmetic witness: unreachable on the '
         'depth-60 fixture)', _ROUTE, 'part_a_g5 adjudicator, ResultStore',
         _LINUX + '; above-FULL by the arithmetic boundary test',
         _here(_ESTABLISH + '[part_a_below_floor]', 'test_e04_part_a_below_floor_commits_fail')
         + [_PART_A_UNIT + 'test_above_full_failure_is_refused']),
    _row('E05', 'No expansion, required expansion and the inclusive tolerance boundary give '
         'correct counts and an unchanged prefix with one disjoint pilot; equal limits and '
         'duplicate PART_A depths reject before planning (expansion legs are arithmetic '
         'witnesses on this fixture)', 'part_a_worker compute adapter',
         'part_a_g5 reconstruction; canonical workload validator',
         _LINUX + '; arithmetic boundary tests',
         ['tests/integration/qualification_boundary/test_campaign_part_a_linux.py::'
          'test_s5_genuine_part_a_without_expansion_reaches_full_pass_ready',
          _PART_A_UNIT + 'test_required_expansion_appends_panels_after_the_unchanged_prefix',
          _PART_A_UNIT + 'test_exact_tolerance_equality_expands_as_decimal',
          _PART_A_UNIT + 'test_initial_prefix_bytes_survive_expansion_unchanged',
          _PART_A_UNIT + 'test_adapter_parity_with_exact_decimal_recomputation',
          'tests/ops/qualification/execution/test_campaign_plan.py::'
          'test_invalid_workload_counts_rejected_by_canonical_validator']),
    _row('E06', 'Crash between the result signing intent and commit, and lost reply after '
         'commit: exact candidate and receipt recovery, launch history proves no redraw',
         _ROUTE, 'ResultStore T1/T2', _LINUX,
         _here('test_e06_result_signing_crash_recovers_exact_bytes_without_redraw')),
    _row('E07', 'Concurrent duplicate seal requests and lost replies: one seal receipt, '
         'identical bytes on inspection, no second publication', _ROUTE, 'SealStore T1/T2',
         _LINUX, _here('test_e07_duplicate_seal_requests_publish_one_receipt')),
    _row('E08', 'Service restarts between stages and with a reservation open never reset the '
         'allowance or mint authority', _ROUTE, 'campaign budget ledger and STATUS', _LINUX,
         _here('test_e08_restarts_between_stages_never_reset_the_allowance')),
    _row('E09', 'Fabricated or altered result candidates and unauthorized result/seal callers '
         'reject; the client principal reads no credential or store and drives no Docker',
         _ROUTE, 'campaign protocol ACL, ResultStore T2, host permissions', _LINUX,
         _here('test_e09_fabricated_or_unauthorized_finalization_rejects')),
    _row('E10', 'VOID before the result or seal publication refuses it; publication before '
         'VOID keeps the historical receipts with no current authority', _ROUTE,
         'ResultStore/SealStore under the VOID lock', _LINUX,
         _here(*('test_e10_void_orderings_against_result_and_seal[' + ordering + ']'
                 for ordering in ('void_before_result', 'void_before_seal',
                                  'publish_before_void')))),
    _row('E11', 'Approval expiry before the result commit mints no result or seal authority; '
         'the committed checkpoint receipt stays exact', _ROUTE,
         'ResultStore T2 approval recheck, SealStore eligibility', _LINUX,
         _here('test_e11_expired_approval_blocks_new_authority_but_not_history')),
    _row('E12', 'qseal death mid-signing and owned cleanup: durable intent, no late '
         'publication, no unit left, historical inspection available', _ROUTE,
         'SealStore, campaign_host cleanup', _LINUX,
         _here('test_e12_qseal_death_and_cleanup_publish_nothing_late')),
]


# ---- Interface presence (decided before any host fixture) ------------------

class IntegrationAbsent(AssertionError):
    """The route needs an interface this checkout does not have."""


INTEGRATED_MODULES = ('campaign_result', 'g5_result', 'campaign_seal', 'seal_service')
INTEGRATED_OPERATIONS = ('RESULT_SNAPSHOT', 'COMMIT_E1_RESULT', 'REQUEST_SEAL', 'INSPECT_SEAL')
INTEGRATED_ROLES = (RESULT_WORK[1],)
AWAITS = pytest.mark.xfail(strict=True, raises=IntegrationAbsent, reason=AWAITING)


def absent_interfaces():
    """The integrated (T05) interfaces this checkout lacks."""
    import importlib.util
    from c1_rail.qualification.execution import campaign_funding, campaign_protocol
    missing = [name for name in INTEGRATED_MODULES
               if importlib.util.find_spec('c1_rail.qualification.execution.' + name) is None]
    missing += [name for name in INTEGRATED_OPERATIONS
                if name not in campaign_protocol._OPERATION_FIELDS]
    missing += [name for name in INTEGRATED_ROLES if name not in campaign_funding.PHASE_BY_ROLE]
    return missing


def s8_driver(request):
    """The driver on the integrated installation; absence fails first."""
    missing = absent_interfaces()
    if missing:
        raise IntegrationAbsent(AWAITING + ': ' + ', '.join(missing))
    if os.environ.get('FP_QUALIFICATION_S8') != '1':
        pytest.skip('FP_QUALIFICATION_S8=1 required: the integrated installation (--s8)')
    return CampaignDriver(request.getfixturevalue('real_boundary'))


# ---- Portable harness checks ------------------------------------------------

def test_declared_verdicts_are_legal_and_cover_the_source_registry():
    assert set(EXPECTED_VERDICTS) == set(campaign_sources.SCENARIOS)
    for name, declared in EXPECTED_VERDICTS.items():
        assert set(declared) == {'stages', 'part_a', 'orb_port_sha256'}, name
        plan(declared['stages'])
        assert (declared['part_a'] is not None) == ('PART_A' in declared['stages']), name
    assert set(IDLE_PAIR_PLACEMENT) == {
        name for name, row in campaign_sources.SCENARIOS.items() if row.idle_dates}


@pytest.mark.parametrize('name', sorted(campaign_sources.SCENARIOS))
def test_declared_source_identity_is_the_scenario_port(tmp_path, name):
    identity = campaign_sources.source_identity(name, tmp_path)
    assert identity == EXPECTED_VERDICTS[name]['orb_port_sha256']


def test_shared_scenario_is_byte_identical_to_the_s5_producer(tmp_path):
    import fixture_producer
    from composition_fixture import build_artifacts, PORT_ROLES
    shared = campaign_sources.SCENARIOS['part_a_below_floor']
    assert shared.idle_dates == fixture_producer.PART_A_BELOW_FLOOR_IDLE_DATES
    ours = build_artifacts(tmp_path / 'ours',
                           port_transform=campaign_sources.port_transform('part_a_below_floor'))
    theirs = build_artifacts(
        tmp_path / 'theirs',
        port_transform=fixture_producer.scenario_port_transform('part_a_below_floor'))
    for role in PORT_ROLES.values():
        assert ours.payloads[role] == theirs.payloads[role], role


def test_idle_pairs_land_only_where_declared(tmp_path):
    """The derivation record: the real samplers place each pair exactly as
    declared (no path is replayed). The candidate blocks are the trading
    source's; establish_verdict replays each actual scenario source."""
    setup = campaign_sources.build_scenario_composition(tmp_path, 'trading')
    inventory = campaign_sources.path_inventory(setup.contract, setup.source)
    for name, expected in IDLE_PAIR_PLACEMENT.items():
        pair = campaign_sources.SCENARIOS[name].idle_dates
        counts = campaign_sources.co_occurrences(inventory, pair)
        assert counts == {key: expected.get(key, 0) for key in counts}, (name, counts)
    n1 = [('n1', population) for population in ('FULL', 'H1', 'H2')]
    assert ('2024-01-16', '2024-01-19') in campaign_sources.isolated_pairs(
        inventory, inside=[('n2', 'FULL')], outside=n1 + [('n2', 'H1'), ('n2', 'H2')])
    assert ('2024-01-08', '2024-01-12') in campaign_sources.isolated_pairs(
        inventory, inside=[('n2', 'H1')], outside=n1 + [('n2', 'FULL'), ('n2', 'H2')])


def test_driver_plan_follows_each_declared_verdict():
    expected = {
        'trading': ('FULL_PASS_READY', 'PASS', {'N1': 1, 'N2': 1, 'PART_A': 1}),
        'idle': ('N1_FAILED', 'FAIL', {'N1': 1, 'N2': 0, 'PART_A': 0}),
        'n2_full_fails': ('N2_FAILED', 'FAIL', {'N1': 1, 'N2': 1, 'PART_A': 0}),
        'n2_halves_fail': ('N2_FAILED', 'FAIL', {'N1': 1, 'N2': 1, 'PART_A': 0}),
        'part_a_below_floor': ('PART_A_FAILED', 'FAIL', {'N1': 1, 'N2': 1, 'PART_A': 1}),
    }
    for name, (terminal, outcome, launches) in expected.items():
        stages = EXPECTED_VERDICTS[name]['stages']
        observed = (terminal_state(stages), result_outcome(stages), expected_launch_counts(stages))
        assert observed == (terminal, outcome, launches), name
        assert accepted_prefix(stages) == list(stages)
    works = [{'phase': phase} for phase in ('ADMISSION', 'N1', 'N1_G5', 'N2', 'N2_G5', 'N2')]
    assert launch_counts({'works': works}) == {'N1': 1, 'N2': 2, 'PART_A': 0}


_ILLEGAL = {
    'legality_fail': {'LEGALITY': 'FAIL', 'N1': 'FAIL'},
    'passing_n1_stop': {'LEGALITY': 'PASS', 'N1': 'PASS'},
    'after_n1_fail': {'LEGALITY': 'PASS', 'N1': 'FAIL', 'N2': 'FAIL', 'PART_B': 'FAIL'},
    'passing_joint_stop': {'LEGALITY': 'PASS', 'N1': 'PASS', 'N2': 'PASS', 'PART_B': 'PASS'},
    'after_joint_fail': {**_ALL_PASS, 'N2': 'FAIL', 'PART_A': 'FAIL'},
    'reordered': {'LEGALITY': 'PASS', 'N1': 'PASS', 'PART_B': 'PASS', 'N2': 'PASS',
                  'PART_A': 'PASS'},
    'unknown_status': {'LEGALITY': 'PASS', 'N1': 'SKIP'},
}


@pytest.mark.parametrize('kind', list(_ILLEGAL))
def test_illegal_declared_verdicts_refuse(kind):
    with pytest.raises(ValueError):
        plan(_ILLEGAL[kind])


def test_coverage_map_is_one_row_per_e_case(tmp_path):
    from scripts.check_qualification_invariants import validate_coverage_map
    files = sorted({node.split('::')[0] for row in COVERAGE for node in row['test_nodeids']})
    collection = tmp_path / 'collected.json'
    env = {key: value for key, value in os.environ.items() if key != 'PYTEST_ADDOPTS'}
    completed = subprocess.run(
        [sys.executable, '-m', 'pytest', '--collect-only', '-q', '-n', '0',
         '-p', 'scripts.pytest_qualification_collection',
         f'--qualification-collection={collection}', '-p', 'no:cacheprovider', *files],
        cwd=REPO, env=env, capture_output=True, text=True, timeout=600, check=False)
    assert completed.returncode == 0, completed.stdout[-4000:] + completed.stderr[-4000:]
    collected = set(json.loads(collection.read_bytes()))
    owner = validate_coverage_map(COVERAGE, collected_nodeids=collected)
    # Every E-case and establishment node of this file belongs to exactly one row,
    # and an E-case node to its own row.
    own = {node for node in collected if node.startswith(HERE + '::test_e')
           or node.startswith(HERE + '::' + _ESTABLISH)}
    assert own == {node for node in owner if node.startswith(HERE)}
    for node in own:
        name = node.split('::')[1]
        if name.startswith('test_e'):
            assert owner[node] == 'E' + name[6:8], node


def test_awaiting_cases_name_only_absent_interfaces():
    """Strict xfail backs the claim: an awaiting case may only exist while an
    integrated interface is absent. Once all are present, remove the markers
    (and register E01-E12) rather than letting the cases pass unexpectedly."""
    awaiting = sorted(name for name, value in globals().items() if name.startswith('test_')
                      and any(mark.name == 'xfail' and mark.kwargs.get('reason') == AWAITING
                              for mark in getattr(value, 'pytestmark', ())))
    assert awaiting
    assert absent_interfaces(), ('integrated candidate present: remove the awaiting markers '
                                 'from ' + ', '.join(awaiting))


# ---- Frozen-engine establishment (S8 selection; minutes per scenario) ------

@pytest.mark.parametrize('name', list(campaign_sources.SCENARIOS))
def test_frozen_engine_establishes_the_declared_verdict(request, tmp_path, name):
    if os.environ.get('FP_QUALIFICATION_S8') != '1':
        pytest.skip('frozen-engine establishment runs in the S8 selection (FP_QUALIFICATION_S8=1)')
    established = campaign_sources.establish_verdict(tmp_path / 'engine', name)
    if os.environ.get('FP_QUALIFICATION_HOST_MANIFEST'):
        from tools.qualification_verification import host
        identity = campaign_sources.source_identity(name, tmp_path / 'identity')
        host.save(request.getfixturevalue('real_boundary').output / f's8-established-{name}.json',
                  {**established, 'orb_port_sha256': identity})
    declared = EXPECTED_VERDICTS[name]
    assert list(established['stages'].items()) == list(declared['stages'].items())
    assert established['part_a'] == declared['part_a']


# ---- Installed route (integrated candidate, disposable Linux host) ---------

def _route(driver, name):
    """Admission, the declared source identity and every checkpoint the
    declared verdict runs, with the launch history and stage split checked."""
    declared = EXPECTED_VERDICTS[name]
    stages = declared['stages']
    attempt = driver.admit(name)
    assert driver.source_identity(attempt) == declared['orb_port_sha256']
    state = driver.run_to_terminal(attempt, stages)
    assert state['state'] == terminal_state(stages), state
    assert launch_counts(state) == expected_launch_counts(stages), state['works']
    if 'N2' in stages:
        split = {'N2': stages['N2'], 'PART_B': stages['PART_B']}
        assert driver.stage_decisions(attempt, 'N2') == split
    if 'PART_A' in stages:
        from test_campaign_part_a_linux import captured_part_a_payload, staged_part_a
        facts = captured_part_a_payload(driver.boundary, attempt)['part_a']
        staged = staged_part_a(driver.boundary, attempt)
        assert (facts['expansion_required'], facts['final_panels']) == (
            declared['part_a']['expansion_required'], declared['part_a']['final_panels'])
        prefix = staged['part_a_initial_prefix']
        assert staged['part_a_final'][:len(prefix)] == prefix
    return attempt, state


def _committed_result(driver, attempt, stages):
    receipt = driver.commit_result(attempt)
    assert receipt is not None, 'no committed campaign result'
    assert set(receipt) == RESULT_RECEIPT_FIELDS, receipt
    assert receipt['schema'] == RESULT_RECEIPT_SCHEMA, receipt
    outcome = result_outcome(stages)
    assert receipt['outcome'] == outcome, receipt
    assert receipt['campaign_state'] == 'RESULT_COMMITTED_' + outcome, receipt
    assert receipt['accepted_prefix'] == accepted_prefix(stages)
    aggregate = json.loads(driver.result_row(attempt)[1])
    assert {row['stage']: row['status'] for row in aggregate['stages']} == stages, aggregate
    return receipt


def _sealed(driver, attempt, label='seal-request'):
    reply, error = driver.request_seal(attempt, label=label)
    assert error is None and reply is not None, error
    seal = json.loads(driver.seal_row(attempt)[2])
    assert set(seal) == SEAL_RECEIPT_FIELDS and seal['schema'] == SEAL_RECEIPT_SCHEMA, seal
    assert seal['campaign_state'] == 'SEALED_PASS'
    return seal


def _no_seal(driver, attempt, reason):
    reply, error = driver.request_seal(attempt)
    assert reply is None and reason in error, error
    assert driver.seal_row(attempt) is None
    inspection = driver.inspect_seal(attempt)
    assert inspection['receipt'] is None, inspection
    assert inspection['eligibility']['eligible'] is False, inspection


def _failure_prefix(request, name):
    driver = s8_driver(request)
    attempt, _ = _route(driver, name)
    _committed_result(driver, attempt, EXPECTED_VERDICTS[name]['stages'])
    _no_seal(driver, attempt, 'committed FAIL outcome is never sealed')


def _kill_payload_units(driver, attempt, work_id):
    """SIGKILL every unit in the work's payload namespace (the G5/qseal unit)."""
    from tools.qualification_verification.container_ownership import campaign_scopes
    scopes = campaign_scopes(driver.boundary.manifest['run_id'], attempt, work_id)
    subprocess.run(['/usr/bin/systemctl', '--system', '--no-ask-password', 'kill',
                    '--signal=KILL', scopes['payload_slice'][:-6] + '*.service'],
                   capture_output=True, check=False)


def _campaign_units(driver, attempt):
    """Active services under the campaign's own slice prefix, as listed text."""
    from tools.qualification_verification.container_ownership import campaign_scopes
    scopes = campaign_scopes(driver.boundary.manifest['run_id'], attempt, SEAL_WORK)
    pattern = scopes['campaign_slice'][:-6] + '*.service'
    listed = subprocess.run(['/usr/bin/systemctl', 'list-units', '--all', '--no-legend',
                             '--plain', '--state=active', pattern],
                            capture_output=True, text=True, check=False)
    return listed.stdout.strip()


def _held_result_intent(driver, attempt):
    """The result T1 intent made durable under the held diagnostic fault, then
    the result unit killed before T2: (intent, candidate) bytes."""
    driver.commit_result(attempt, fault='hold_after_intent')
    driver.until(attempt, lambda s: (driver.result_row(attempt) or (None,))[0] is not None,
                 seconds=120)
    _kill_payload_units(driver, attempt, RESULT_WORK[0])
    intent, candidate, _, receipt = driver.result_row(attempt)
    assert receipt is None, 'no receipt may exist between T1 and T2'
    return intent, candidate


@AWAITS
def test_e01_genuine_pass_commits_and_is_sealed_separately(request):
    from c1_rail.qualification.execution.protocol import sha256
    driver = s8_driver(request)
    release = json.loads((driver.boundary.installation / 'release.json').read_bytes())
    assert release['authority_class'] == 'TEST_ONLY' and release['production_execution'] is False
    attempt, _ = _route(driver, 'trading')
    result = _committed_result(driver, attempt, EXPECTED_VERDICTS['trading']['stages'])
    seal = _sealed(driver, attempt)
    assert seal['result_receipt_sha256'] == sha256(driver.result_row(attempt)[3])
    assert seal['work_id'] != result['work_id']
    inspection = driver.inspect_seal(attempt)
    observed = (inspection['receipt'], inspection['historical'], inspection['current_validity'])
    assert observed == (seal, True, 'VALID')


@AWAITS
def test_e02_n1_failure_commits_fail_without_successors(request):
    _failure_prefix(request, 'idle')


@AWAITS
@pytest.mark.parametrize('name', ['n2_full_fails', 'n2_halves_fail'])
def test_e03_asymmetric_joint_failure_is_one_batch(request, name):
    _failure_prefix(request, name)


@AWAITS
def test_e04_part_a_below_floor_commits_fail(request):
    _failure_prefix(request, 'part_a_below_floor')


@AWAITS
def test_e06_result_signing_crash_recovers_exact_bytes_without_redraw(request):
    """Crash between the result T1 intent and T2 (the held unit killed), then an
    exact signing retry; a restart afterwards stands in for the lost reply."""
    driver = s8_driver(request)
    attempt, state = _route(driver, 'idle')
    launches = launch_counts(state)
    intent, candidate = _held_result_intent(driver, attempt)
    retried = driver.commit_result(attempt, work_id='rretry', signing_retry_of=RESULT_WORK[0])
    assert retried is not None, 'the exact signing retry committed nothing'
    assert retried['signing_at_utc'] == json.loads(intent)['signing_at_utc'], retried
    committed = driver.result_row(attempt)
    assert committed[:2] == (intent, candidate)
    assert launch_counts(driver.ledger(attempt)) == launches
    driver.boundary.restart()
    assert driver.result_row(attempt) == committed


@AWAITS
def test_e07_duplicate_seal_requests_publish_one_receipt(request):
    from concurrent.futures import ThreadPoolExecutor
    driver = s8_driver(request)
    attempt, _ = _route(driver, 'trading')
    _committed_result(driver, attempt, EXPECTED_VERDICTS['trading']['stages'])
    with ThreadPoolExecutor(max_workers=2) as pool:
        replies = list(pool.map(
            lambda index: driver.request_seal(attempt, label=f'seal-request-{index}'), range(2)))
    successes = [reply for reply, error in replies if error is None]
    assert successes and all(reply == successes[0] for reply in successes), replies
    sealed = driver.seal_row(attempt)
    assert sealed is not None and sealed[2] is not None
    driver.request_seal(attempt, label='seal-request-late')
    assert driver.seal_row(attempt) == sealed
    assert driver.inspect_seal(attempt)['receipt'] == json.loads(sealed[2])


@AWAITS
def test_e08_restarts_between_stages_never_reset_the_allowance(request):
    """A restart after every checkpoint and one with the RESULT reservation open
    (held T1): the allowance never resets and the campaign still seals once."""
    driver = s8_driver(request)
    stages = EXPECTED_VERDICTS['trading']['stages']
    attempt = driver.admit('trading')

    def restarted():
        before = driver.status(attempt)
        driver.boundary.restart()
        after = driver.status(attempt)
        assert after['settled_cpu_ns'] >= before['settled_cpu_ns'], (before, after)
        assert after['remaining_cpu_ns'] <= before['remaining_cpu_ns'], (before, after)
    for step in plan(stages):
        driver.run_step(attempt, step)
        restarted()
    _held_result_intent(driver, attempt)
    restarted()
    retried = driver.commit_result(attempt, work_id='rretry', signing_retry_of=RESULT_WORK[0])
    assert retried is not None and retried['outcome'] == 'PASS', retried
    _sealed(driver, attempt)
    driver.settled(attempt)
    final = driver.status(attempt)
    assert final['reserved_cpu_ns'] == 0 and final['remaining_cpu_ns'] >= 0, final


@AWAITS
def test_e09_fabricated_or_unauthorized_finalization_rejects(request):
    import base64
    from tools.qualification_verification import host
    driver = s8_driver(request)
    attempt, _ = _route(driver, 'idle')
    receipt = _committed_result(driver, attempt, EXPECTED_VERDICTS['idle']['stages'])
    row = driver.result_row(attempt)
    altered = base64.b64encode(json.dumps({**json.loads(row[1]), 'outcome': 'PASS'}).encode())
    for role in ('qclient', 'qg5'):
        with pytest.raises(subprocess.CalledProcessError):
            driver.boundary.request(
                'COMMIT_E1_RESULT', role=role, schema='qualification_campaign_request/v2',
                attempt_id=attempt, work_id=RESULT_WORK[0], candidate_bytes_b64=altered.decode(),
                authentication_sha256='0' * 64, expected_revision=receipt['campaign_revision'],
                artifacts=[])
        with pytest.raises(subprocess.CalledProcessError):
            driver.boundary.request('REQUEST_SEAL', role=role,
                                    schema='qualification_campaign_request/v2', attempt_id=attempt)
    # The client principal reads no credential or store, and drives no Docker.
    root = driver.boundary.root
    docker = driver.boundary.manifest['host_config']['docker']
    for probe in (['/usr/bin/cat', str(root / 'keys/qg5/credential.json')],
                  ['/usr/bin/cat', str(root / 'keys/qexec/credential.json')],
                  ['/usr/bin/cat', str(root / 'data/journal.sqlite')],
                  [docker, '--host', 'unix:///var/run/docker.sock', 'ps']):
        with pytest.raises(subprocess.CalledProcessError):
            host.run_owned(driver.boundary.group, driver.boundary.identity('qclient', probe),
                           interpreter=driver.boundary.python, timeout=60)
    assert driver.result_row(attempt) == row and driver.seal_row(attempt) is None


@AWAITS
@pytest.mark.parametrize('ordering', ['void_before_result', 'void_before_seal',
                                      'publish_before_void'])
def test_e10_void_orderings_against_result_and_seal(request, ordering):
    """VOID inside the result T1/T2 window (barrier: the held unit), VOID after
    the result and before the seal, and VOID after both publications."""
    driver = s8_driver(request)
    attempt, _ = _route(driver, 'trading')
    result = seal = None
    if ordering == 'void_before_result':
        _held_result_intent(driver, attempt)
    else:
        result = _committed_result(driver, attempt, EXPECTED_VERDICTS['trading']['stages'])
    if ordering == 'publish_before_void':
        seal = _sealed(driver, attempt)
    reply, error = driver.void(attempt, 'S8 E10 ' + ordering)
    assert error is None and reply['validity'] == 'VOID', error
    if ordering == 'void_before_result':
        driver.schedule(attempt, 'rretry', RESULT_WORK[1], signing_retry_of=RESULT_WORK[0])
        driver.settled(attempt)
        assert driver.result_row(attempt)[3] is None, 'VOID-first result publication refuses'
        _no_seal(driver, attempt, 'no committed campaign result')
        return
    assert json.loads(driver.result_row(attempt)[3]) == result
    if seal is None:
        _no_seal(driver, attempt, 'VOID campaign')
        return
    inspection = driver.inspect_seal(attempt)
    observed = (inspection['receipt'], inspection['historical'], inspection['current_validity'])
    assert observed == (seal, True, 'VOID')
    assert inspection['eligibility']['eligible'] is False


@AWAITS
def test_e11_expired_approval_blocks_new_authority_but_not_history(request):
    """The exact-depth approval expires between the committed N1 receipt and the
    result commit: no result authority is minted and the N1 receipt stays exact."""
    import time
    from datetime import datetime, timezone
    driver = s8_driver(request)
    stages = EXPECTED_VERDICTS['idle']['stages']
    attempt = driver.admit('idle', depth_valid_seconds=EXPIRY_SECONDS)
    driver.run_to_terminal(attempt, stages)
    receipt = driver.checkpoint_row(attempt, 'N1')
    expires = datetime.fromisoformat(
        driver.bundles[attempt]['depth_expires_at'].replace('Z', '+00:00'))
    remaining = (expires - datetime.now(timezone.utc)).total_seconds()
    assert remaining > 0, 'the N1 route outlasted the approval; raise EXPIRY_SECONDS'
    time.sleep(remaining + 1)
    driver.schedule(attempt, RESULT_WORK[0], RESULT_WORK[1])
    driver.settled(attempt)
    assert (driver.result_row(attempt) or (None,) * 4)[3] is None, 'expiry mints no result'
    assert driver.checkpoint_row(attempt, 'N1') == receipt
    _no_seal(driver, attempt, 'no committed campaign result')


@AWAITS
def test_e12_qseal_death_and_cleanup_publish_nothing_late(request):
    """qseal killed once the seal intent is durable: a restart keeps the intent,
    publishes nothing late, inspection stays historical and no unit of the
    campaign survives settlement. Without a qseal hold the kill can land after
    publication; the case then still proves the single, unchanged receipt."""
    import threading
    driver = s8_driver(request)
    attempt, _ = _route(driver, 'trading')
    _committed_result(driver, attempt, EXPECTED_VERDICTS['trading']['stages'])
    worker = threading.Thread(target=driver.request_seal, args=(attempt,), daemon=True)
    worker.start()
    driver.until(attempt, lambda s: driver.seal_row(attempt) is not None, seconds=120)
    _kill_payload_units(driver, attempt, SEAL_WORK)
    worker.join(timeout=330)
    intent, _, receipt = driver.seal_row(attempt)
    driver.save(attempt, 'e12-kill', {'published_before_kill_settled': receipt is not None})
    driver.boundary.restart()
    driver.settled(attempt)
    assert driver.seal_row(attempt)[0] == intent and driver.seal_row(attempt)[2] == receipt
    inspection = driver.inspect_seal(attempt)
    assert inspection['receipt'] == (None if receipt is None else json.loads(receipt))
    assert not _campaign_units(driver, attempt), 'owned campaign units survived settlement'
