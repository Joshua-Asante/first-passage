"""Synthetic builder acceptance; contract #752 b02c173e, §§B–D, F2–F9.

No private inputs. Literal expected values are derived from the cited clauses.
Independent Claude derivation/mutation verification is deliberately still owed.
"""
import copy
import csv
import hashlib
import io
import json
from dataclasses import replace
from datetime import date, timedelta
from fractions import Fraction

import numpy as np
import pytest

from discovery import sfgrowth_acceptance as s
from discovery.remc_series_builder import TRADE_LIST_COLUMNS


def encoded(value):
    return json.dumps(value).encode()


def digest(value):
    return hashlib.sha256(value).hexdigest()


def weekdays(n=63):
    start = date(2026, 1, 5)
    return tuple(start + timedelta(days=i) for i in range(n * 2)
                 if (start + timedelta(days=i)).weekday() < 5)[:n]


def export_bytes(*, net=96, commission=4, adverse=8, favorable=12, qty=1):
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=TRADE_LIST_COLUMNS)
    writer.writeheader()
    for kind, time in [('entry', '10:00'), ('exit', '11:00')]:
        row = dict.fromkeys(TRADE_LIST_COLUMNS, '0')
        row.update({'Trade number': '1', 'Type': kind + ' long',
                    'Date and time': '2026-01-05 ' + time, 'Size (qty)': str(qty),
                    'Net PnL USD': str(net), 'Commission USD': str(commission),
                    'Adverse excursion USD': str(adverse),
                    'Favorable excursion USD': str(favorable)})
        writer.writerow(row)
    return out.getvalue().encode()


def parsed(tmp_path, **kwargs):
    raw = export_bytes(**kwargs)
    path = tmp_path / 'synthetic.csv'
    path.write_bytes(raw)
    return s.read_export(path, expected_sha256=digest(raw), leg='synthetic',
                         export_tz='America/New_York', baseline=True)


def settings(**changes):
    value = {'Pyramiding': 2, 'commission': 4, 'slippage': 7,
             'backtestMode': False, 'soft_stop': True}
    value.update(changes)
    return value


def test_f9_fee_only_accounting_uses_parser_gross_once(tmp_path):
    trades = parsed(tmp_path)
    fees = dict(commission=1, exchange=1, clearing=.75, NFA=.25)
    # Two sides × 3 = 6; net 96 + export commission 4 = 100.
    # Reference slippage 7 stays in 96. MAE 8 and MFE 12 stay captured.
    before = copy.deepcopy(trades)
    a = s.daily_series(trades, weekdays(), fees, 1)
    b = s.daily_series(trades, weekdays(), fees, 1.5)
    assert a[0].tolist() == [94, -14, 12]
    assert b[0].tolist() == [91, -17, 12]
    np.testing.assert_array_equal(b[0] - a[0], [-3, -3, 0])
    assert not a[1:].any()  # no-trade weekdays are zero
    assert trades == before
    assert s.explore_quantity(trades, weekdays()) == 1  # paired rows counted once


@pytest.mark.parametrize('component', ['commission', 'exchange', 'clearing', 'NFA'])
def test_f9_missing_fee_component_void(tmp_path, component):
    fees = dict(commission=1, exchange=1, clearing=.75, NFA=.25)
    del fees[component]
    with pytest.raises(s.Void):
        s.daily_series(parsed(tmp_path), weekdays(), fees, 1)


@pytest.mark.parametrize('raw,baseline', [
    (b'', False), (b'not,a,trade', False),
    (export_bytes().replace(b'Favorable excursion USD', b'Absent column'), False),
    ((','.join(TRADE_LIST_COLUMNS) + '\n').encode(), True),
    (export_bytes(favorable=''), False), (export_bytes(favorable='nan'), False),
])
def test_f3_real_export_never_promoted_to_zero(tmp_path, raw, baseline):
    path = tmp_path / 'synthetic.csv'
    path.write_bytes(raw)
    with pytest.raises(s.Void):
        s.read_export(path, expected_sha256=digest(raw), leg='synthetic',
                      export_tz='America/New_York', baseline=baseline)


def test_b_empty_nonbaseline_is_valid_and_hash_is_checked(tmp_path):
    raw = (','.join(TRADE_LIST_COLUMNS) + '\n').encode()
    path = tmp_path / 'synthetic.csv'
    path.write_bytes(raw)
    assert s.read_export(path, expected_sha256=digest(raw), leg='synthetic',
                         export_tz='America/New_York', baseline=False) == ()
    with pytest.raises(s.Void):
        s.read_export(path, expected_sha256='0'*64, leg='synthetic',
                      export_tz='America/New_York', baseline=False)


@pytest.mark.parametrize('active', [True, False])
def test_f7_native_guards_and_f9_properties_preserved(active):
    reference = settings(backtestMode=active)
    s.validate_settings(reference, reference.copy())
    for key in reference:
        changed = reference.copy()
        changed[key] = not active if key == 'backtestMode' else 999
        with pytest.raises(s.Void):
            s.validate_settings(reference, changed)
        missing = reference.copy()
        del missing[key]
        with pytest.raises(s.Void):
            s.validate_settings(reference, missing)
    with pytest.raises(s.Void):
        s.validate_settings(settings(Pyramiding=None), settings(Pyramiding=None))
    with pytest.raises(s.Void):
        s.validate_settings(reference, {**reference, 'add_size_percentage': 2})


def test_f7_size_specific_sample_is_not_rescaled_or_reconstructed(tmp_path):
    small = parsed(tmp_path, net=2, commission=0, qty=1)
    large = parsed(tmp_path, net=9, commission=0, qty=3)
    fees = dict(commission=0, exchange=0, clearing=0, NFA=0)
    assert s.daily_series(small, weekdays(), fees, 1)[0, 0] == 2
    assert s.daily_series(large, weekdays(), fees, 1)[0, 0] == 9
    assert s.explore_quantity(small, weekdays()[1:]) == 0


def test_c_worked_example_and_halt_stops_future_recovery():
    assert s.path_terminal([(2, -3, 4), (-14, -16, 0), (1000, 0, 1000)], 100) == (86, True)


@pytest.mark.parametrize('low,expected', [(-14.999, (100, False)), (-15, (85, True)),
                                         (-15.001, (84.999, True))])
def test_c_inclusive_fifteen_percent(low, expected):
    terminal, hit = s.path_terminal([(0, low, 0)], 100)
    assert terminal == pytest.approx(expected[0])
    assert hit is expected[1]


def test_c_high_before_low_prior_peak_and_close_peak():
    assert s.path_terminal([(0, -7, 10)], 100) == (93, True)  # 17/110
    assert s.path_terminal([(10, 0, 0), (0, -7, 0)], 100) == (110, False)
    assert s.path_terminal([(10, 0, 0), (0, -17, 0)], 100) == (93, True)
    assert s.path_terminal([(0, 0, 10), (0, -7, 0)], 100) == (93, True)


def summary(growth=110, hits=(0, 0, 0)):
    return s.Summary(growth, hits)


@pytest.mark.parametrize('hits,clear', [((100,100,100), True), ((101,0,0), False),
                                       ((0,101,0), False), ((0,0,101), False)])
def test_c_clearance_is_per_seed_not_pooled(hits, clear):
    assert summary(hits=hits).clears is clear


def test_c_growth_is_pooled_even_median_not_median_of_seed_medians():
    terminals = np.array([[90]*6000 + [110]*4000,
                          [100]*6000 + [120]*4000,
                          [130]*10000], dtype=float)
    # Sorted pooled positions 14999 and 15000 are both 110; seed medians median=100.
    result = s.summarize(terminals, np.zeros((3,10000), dtype=bool))
    assert result.growth == 110
    terminals = np.array([[90]*10000, [100]*5000 + [104]*5000, [130]*10000])
    assert s.summarize(terminals, np.zeros((3,10000), dtype=bool)).growth == 102


def candidate(vector, growth=110, hits=(0,0,0), quantity=1, excluded=False):
    return s.Candidate(vector, summary(growth, hits), quantity, excluded)


def test_c_maximum_growth_precedes_safety_and_quantity():
    high = candidate((2,), 120, (99,99,99), 100)
    low = candidate((1,), 110, (0,0,0), 1)
    assert s.rank([low, high], 100) == [high, low]


def test_c_all_tiebreaks_in_order_and_strict_positive_growth():
    a = candidate((2,0), hits=(0,0,1), quantity=99)
    b = candidate((1,0), hits=(0,1,1), quantity=1)
    c = candidate((0,2), hits=(0,1,1), quantity=2)
    d = candidate((0,1), hits=(0,1,1), quantity=2)
    rejected = [candidate((3,0), growth=100), candidate((4,0), hits=(101,0,0)),
                candidate((5,0), growth=999, excluded=True)]
    assert s.rank([c,b,d,a,*rejected], 100) == [a,b,d,c]


def test_b_nominal_grid_no_dedup_zero_contribution_retains_vector():
    grid = s.nominal_grid(('x','y'), forbidden_pairs=())
    assert len(grid) == 35  # 6²−1, synthetic two-leg contract only
    assert (Fraction(1,8), 0) in grid and (Fraction(1,4), 0) in grid
    tied = [candidate(v, quantity=0) for v in grid]
    assert len(s.rank(tied, 100)) == 35
    assert s.rank(tied, 100)[0].vector == (0, Fraction(1,8))
    restricted = s.nominal_grid(('x','y'), forbidden_pairs=(('x','y'),))
    assert len(restricted) == 10  # nominal positives excluded even if contributions zero
    assert all(not (x and y) for x,y in restricted)
    excluded = [replace(c, excluded=True) for c in tied]
    assert len(excluded) == 35 and s.rank(excluded, 100) == []


@pytest.mark.parametrize('failure', ['base_hits', 'stress_hits', 'base_growth',
                                    'stress_growth', 'seam_hits', None])
def test_d_confirm_only_top_and_no_second_pick(failure):
    top, second = candidate((2,), 120), candidate((1,), 110)
    calls = []
    def confirm(vector, cost, seam):
        calls.append((vector, cost, seam))
        limb = 'seam' if seam else 'base' if cost == 1 else 'stress'
        return summary(100 if failure == limb+'_growth' else 110,
                       (101,0,0) if failure == limb+'_hits' else (0,0,0))
    assert s.verdict([second, top], 100, confirm) == (
        'RESOLVED' if failure is None else 'AMBIGUOUS-HOLD')
    assert calls == [((2,),1,False), ((2,),1.5,False), ((2,),1,True)]


def test_d_void_before_payoffs_and_falsified_without_confirm():
    def forbidden(*args):
        pytest.fail('Confirm must not be read')
    assert s.verdict([], 100, forbidden) == 'FALSIFIED'
    assert s.verdict([candidate((1,))], 100, forbidden, input_error='bad binding') == 'VOID'
    def invalid(*args):
        raise s.Void('missing evidence')
    assert s.verdict([candidate((1,))], 100, invalid) == 'VOID'


def test_c_calendar_common_weekdays_and_floor_split():
    dates = weekdays()
    calendar = s.common_calendar([(dates[0], dates[-1]), (dates[1], dates[-2])])
    assert calendar == dates[1:-1]
    explore, confirm = s.split_calendar(calendar)
    assert explore == calendar[:40] and confirm == calendar[40:]
    with pytest.raises(s.Void):
        s.split_calendar(weekdays(57))
    assert tuple(map(len, s.split_calendar(weekdays(58)))) == (38, 20)
    with pytest.raises(s.Void):
        s.common_calendar([])


def test_c_bootstrap_exact_draw_contract_shared_and_252_truncation():
    draws = s.bootstrap_indices(27)
    assert draws.shape == (3,10000,252)
    # Independent oracle of the specified one-call PCG64 draw law.
    for seed_index, seed in enumerate((42,123,2026)):
        starts = np.random.Generator(np.random.PCG64(seed)).integers(0,8,size=(10000,13))
        expected = np.concatenate([starts[:,:,None] + np.arange(20)], axis=2).reshape(10000,260)[:,:252]
        np.testing.assert_array_equal(draws[seed_index], expected)
    assert draws.min() == 0 and draws.max() == 26
    assert not draws.flags.writeable
    with pytest.raises(s.Void):
        s.bootstrap_indices(19)
    # Same immutable draws reused for both costs and every vector.
    days = np.tile([1,0,0], (27,1))
    assert s.score(days, 100, draws) == summary(352)
    assert s.score(days*0, 100, draws) == summary(100)


def test_c_roll_seam_inclusive_ten_weekdays_both_sides():
    dates = weekdays(30)
    retained = s.outside_roll_seams(dates, [dates[15]])
    assert retained == dates[:5] + dates[26:]
    assert s.outside_roll_seams(dates, []) == dates


def archive_fixture():
    blob = b'{"synthetic":true}\r\n'
    sha = digest(blob)
    ref = dict(schema_version=1, archive_repository='Joshua-Asante/first-passage-archive',
               archive_commit='a'*40, archive_path=f'evidence/sha256/{sha[:2]}/{sha}',
               manifest_sha256=sha)
    archive = {(ref['archive_repository'], 'a'*40, ref['archive_path']): blob}
    def retrieve(repo, commit, path):
        return archive[repo, commit, path]
    return ref, blob, retrieve


def test_f6_committed_identity_exact_bytes_no_public_values():
    ref, blob, retrieve = archive_fixture()
    assert s.resolve_manifest(encoded(ref), retrieve, local_bytes=blob) == blob
    assert set(ref) == {'schema_version','archive_repository','archive_commit',
                        'archive_path','manifest_sha256'}
    with pytest.raises(s.Void):
        s.resolve_manifest(encoded(ref), retrieve, local_bytes=blob.replace(b'\r\n',b'\n'))


@pytest.mark.parametrize('field,value', [
    ('schema_version',True), ('schema_version',2), ('archive_repository','other/repo'),
    ('archive_commit','main'), ('archive_commit','A'*40), ('archive_commit','b'*40),
    ('archive_path','local.json'), ('manifest_sha256','0'*64),
    ('private_value',123),
])
def test_f6_bad_reference_void(field,value):
    ref, _, retrieve = archive_fixture()
    ref[field] = value
    with pytest.raises(s.Void):
        s.resolve_manifest(encoded(ref), retrieve)


@pytest.mark.parametrize('raw', [b'[]', b'null', b'{}', b'\xef\xbb\xbf{}', b'{',
                                b'{"schema_version":1,"schema_version":1}'])
def test_f6_malformed_reference_void(raw):
    with pytest.raises(s.Void):
        s.resolve_manifest(raw, lambda *args: pytest.fail('must validate before retrieval'))


@pytest.mark.parametrize('failure', ['unavailable','altered','local_only'])
def test_f6_archive_required_no_local_fallback(failure):
    ref, blob, _ = archive_fixture()
    def retrieve(*args):
        if failure == 'altered':
            return blob.replace(b'\r\n', b'\n')
        raise FileNotFoundError('synthetic absent archive')
    with pytest.raises(s.Void):
        s.resolve_manifest(encoded(ref), retrieve, local_bytes=blob)


@pytest.mark.parametrize('defect', ['missing','duplicate','hash','source','freeze','kind'])
def test_f2_f6_generic_slot_and_binding_integrity(defect):
    raw = b'synthetic export'
    binding = dict(kind='EXPORT', pine_sha256='1'*64, reference_evidence_sha256='2'*64,
                   classification_sha256='3'*64, preregistration_sha256='4'*64)
    expected = {('synthetic','1'):binding}
    row = dict(slot=('synthetic','1'), sha256=digest(raw), **binding)
    rows = [row]
    if defect == 'missing': rows = []
    if defect == 'duplicate': rows = [row,row]
    if defect == 'hash': row['sha256'] = '0'*64
    if defect == 'source': row['pine_sha256'] = '0'*64
    if defect == 'freeze': row['preregistration_sha256'] = '0'*64
    if defect == 'kind': row['kind'] = 'ZERO_BY_INTEGER_SIZING'
    with pytest.raises(s.Void):
        s.validate_slots(rows, expected, lambda slot: raw)


def test_f6_generic_complete_slot_inventory_passes():
    binding = dict(kind='EXPORT', pine_sha256='1'*64, reference_evidence_sha256='2'*64,
                   classification_sha256='3'*64, preregistration_sha256='4'*64)
    row = dict(slot=('synthetic','1'), sha256=digest(b'fixture'), **binding)
    s.validate_slots([row], {('synthetic','1'):binding}, lambda slot: b'fixture')


# F8 supersedes the five historical zero slots and cosmetic exemption. No active
# pool or eligible zero schema binding can be invented while blocker 2 is open.
POOL_CASES = [
    'F2-F5_each_admitted_zero_slot_both_costs_sensitivity_calendar_draws',
    'F2-F5_other_positive_k0_wrong_leg_input_fraction_added_slot_VOID',
    'F2-F5_nonzero_floor_bound_inconsistency_VOID',
    'F2-F5_zero_schema_missing_extra_duplicate_keys_version_type_reason_BOM_JSON_VOID',
    'F3-F5_zero_quantity_margin_lexicographic_nominal_vector',
    'F4-F5_two_cosmetic_unknowns_only_with_explicit_status',
    'F5-F6_final_full_manifest_export_zero_counts',
    'F8_final_nominal_grid_K_exclusions_no_dedup',
    'F8_reject_excluded_legs_and_unadmitted_replacements',
    'F8_genuine_nonempty_final_pool_baseline_calendar',
    'F8_reject_zero_outside_final_frozen_eligible_slots',
    'F7-F8_final_native_settings_size_dependent_soft_stop_bindings',
]


@pytest.mark.parametrize('case', POOL_CASES)
@pytest.mark.skip(reason='PENDING blocker 2: F8 final pool, K, slots and reconciled freeze unset')
def test_pending_pool_contract(case):
    raise AssertionError(case)  # removing skip alone cannot manufacture acceptance


@pytest.mark.parametrize('case', ['overlap_base_add', 'separated_trades', 'entry_before_exit_ties',
                                 'partial_exits_closed_tranches', 'malformed_exposure_VOID',
                                 'margin_above_E0_excluded_still_in_K'])
@pytest.mark.skip(reason='PENDING blocker 4: F9 margin PR #782 open/unmerged at build')
def test_pending_f9_margin_integration(case):
    raise AssertionError(case)


def test_c_vectorized_halt_matches_worked_path_and_never_recovers():
    draws = np.full((3,10000,252), 2, dtype=int)
    draws[:,:,0] = 0
    draws[:,:,1] = 1
    result = s.score([(2,-3,4), (-14,-16,0), (1000,0,1000)], 100, draws)
    assert result == summary(86, (10000,10000,10000))


def zero_schema():
    # Historical schema fixture only, never an admission into the F8 pool.
    return dict(schema_version=1, artifact_type='ZERO_BY_INTEGER_SIZING', leg=3,
                multiplier='1/8', input_id='maxContracts', reason='FLOORED_COUNT_BELOW_INPUT_MIN',
                pine_sha256='1'*64, reference_evidence_sha256='2'*64,
                classification_sha256='3'*64, preregistration_sha256='4'*64)


@pytest.mark.parametrize('field,value', [
    ('schema_version', True), ('schema_version', 2), ('artifact_type','EXPORT'),
    ('leg',True), ('leg',5), ('multiplier','0'), ('multiplier','0.125'),
    ('multiplier','2/16'), ('multiplier','1'), ('input_id','qty'),
    ('reason','empty CSV'), ('pine_sha256','A'*64), ('reference_evidence_sha256','bad'),
    ('classification_sha256',None), ('preregistration_sha256','0'*63),
    ('trade',[]), ('date','2026-01-05'), ('cash',0),
])
def test_f2_schema_rejects_malformed_historical_zero(field, value):
    obj = zero_schema()
    obj[field] = value
    with pytest.raises(s.Void):
        s.validate_zero_schema(encoded(obj))


@pytest.mark.parametrize('field', list(zero_schema()))
def test_f2_schema_requires_every_key(field):
    obj = zero_schema()
    del obj[field]
    with pytest.raises(s.Void):
        s.validate_zero_schema(encoded(obj))


@pytest.mark.parametrize('raw', [b'[]', b'null', b'{}', b'\xef\xbb\xbf{}', b'{',
                                b'{"schema_version":1,"schema_version":1}'])
def test_f2_zero_invalid_json_void(raw):
    with pytest.raises(s.Void):
        s.validate_zero_schema(raw)


def test_f2_schema_validation_does_not_admit_excluded_historical_slots():
    # Schema inspection is pool-independent; admission requires final frozen bindings.
    for leg, multiplier, input_id in [(3,'1/8','maxContracts'), (3,'1/4','maxContracts'),
                                     (4,'1/8','qty'), (4,'1/4','qty'), (4,'1/2','qty')]:
        obj = dict(zero_schema(), leg=leg, multiplier=multiplier, input_id=input_id)
        assert s.validate_zero_schema(encoded(obj)) == obj
        with pytest.raises(s.Void):
            s.require_zero_slot(obj, eligible_slots=frozenset())


@pytest.mark.parametrize('defect', ['missing','hash','freeze'])
def test_f6_required_source_evidence_checked_against_frozen_bindings(defect):
    sources = {'pine':b'synthetic source', 'freeze':b'synthetic contract'}
    expected = {name:digest(raw) for name,raw in sources.items()}
    if defect == 'missing': del sources['pine']
    if defect == 'hash': sources['pine'] += b'changed'
    if defect == 'freeze': sources['freeze'] += b'changed'
    with pytest.raises(s.Void):
        s.validate_evidence(expected, sources.__getitem__)


def test_f6_required_evidence_exact_bytes_pass():
    sources = {'reference':b'synthetic original\r\n', 'recapture':b'synthetic recapture\n'}
    expected = {name:digest(raw) for name,raw in sources.items()}
    s.validate_evidence(expected, sources.__getitem__)
    sources['reference'] = sources['recapture']
    with pytest.raises(s.Void):
        s.validate_evidence(expected, sources.__getitem__)
