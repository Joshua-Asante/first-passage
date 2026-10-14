"""Card E score composition: hand-derived synthetic cases, no private reads."""
import copy
from datetime import date, timedelta
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import numpy as np
import pytest

SOURCE = Path(__file__).resolve().parents[2] / 'lab/analysis/c1/sfclear_2026-10/score_r1.py'
LEGS = ('aegis_6j', 'dj30_mym_p250', 'vanguard_mgc', 'orb_mnq_v7')
SYMBOLS = ('6J', 'MYM', 'MGC', 'MNQ')
HEAD = 'a' * 40


def raw(doc):
    return json.dumps(doc).encode()


def sha(blob):
    return hashlib.sha256(blob).hexdigest()


@pytest.fixture
def s():
    assert SOURCE.exists(), 'E scoring implementation absent'
    spec = importlib.util.spec_from_file_location('sfclear_score_r1', SOURCE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def days(n=61):
    start = date(2026, 1, 5)
    return tuple(start + timedelta(days=i) for i in range(n * 2)
                 if (start + timedelta(days=i)).weekday() < 5)[:n]


def freeze():
    return dict(schema='sfclear2_freeze_record/v1', nonce='1' * 64,
                calculator_sha256='2' * 64,
                G1={leg: dict(p95=.1, max=999) for leg in LEGS[:3]},
                G3=dict(p95=.5, max=999), margin_snapshot=dict(sha256='3' * 64),
                fee_snapshot=dict(sha256='4' * 64))


def score_inputs():
    return dict(schema='sfclear_score_inputs/v1', monthly_debited_fixed_costs_usd=0.0,
                f_basis='prescreen_debited_case', f_source_sha256='5' * 64,
                fee_snapshot_v1_sha256='6' * 64, vanguard_paper_capital_usd=1000.0)


def port_state():
    return dict(schema='sfclear_port_state/v1', run_head=HEAD, legs={
        LEGS[1]: dict(daily_dd_trips_utc=[], total_dd_trips_utc=[]),
        LEGS[2]: dict(e_p=[['2026-01-05T15:00:00Z', 1200.0]])})


def fee_raw():
    return raw(dict(schema='sfclear_tradovate_fees/v1', venue='Tradovate', plan='Free',
        unit='USD_per_side_per_contract', captured_utc='2026-01-01T00:00:00Z', source_sha256='4' * 64,
        rows=[dict(instrument=symbol, commission='1', exchange='0', clearing='0', NFA='0')
              for symbol in SYMBOLS]))


def trade(day='2026-01-05', leg=LEGS[0], **changes):
    value = dict(leg=leg, instrument=SYMBOLS[LEGS.index(leg)], contract='2026-03',
        entry_utc=day+'T15:00:00Z', exit_utc=day+'T16:00:00Z', side='buy', quantity=1,
        tranche_index=0, entry_price=100.0, initial_stop_level=99.0, delta_0=1.0,
        exit_price=110.0, exit_kind='close', stop_fill_distance_b=0.0,
        net_pnl_usd=8.0, commission_usd=2.0, mae_usd=-1.0, mfe_usd=11.0)
    value.update(changes)
    return value


def route():
    return dict(schema='sfclear_route_output/v1', trades=[trade()],
                refusals={leg: [] for leg in LEGS},
                days=[dict(account_date=d.isoformat(), net_pnl_usd=8.0 if i == 0 else 0.0,
                           fills=2 if i == 0 else 0) for i, d in enumerate(days())],
                input_identities={key: '7' * 64 for key in ('tuple','size_vector','source_bundle',
                    'schedule','roll_list','generator','calendar','reference_friction','e0')}, latch=None)


def test_e9_half_split_and_short_void(s):
    result = s.windows(days())
    assert [len(result[k]) for k in ('FULL','H1','H2')] == [61, 30, 31]
    with pytest.raises(s.Void):
        s.windows(days(39))


def test_e17_off_empty_leg_still_sets_span(s):
    spans = dict(zip(LEGS, [('2026-01-01','2026-05-01'), ('2026-01-02','2026-04-30'),
                           ('2026-01-05','2026-04-29'), ('2026-01-06','2026-04-28')]))
    result = s.panel_calendar(spans)
    assert result[0] == date(2026,1,6) and result[-1] == date(2026,4,28)
    with pytest.raises(s.Void):
        s.panel_calendar({k:v for k,v in spans.items() if k != LEGS[3]})


def test_e16_fee_gross_once_and_account_debit_once(s):
    doc = route()
    doc['trades'].append(trade(leg=LEGS[1]))
    frozen, inputs = freeze(), score_inputs()
    inputs['fee_snapshot_v1_sha256'] = sha(fee_raw())
    fees = s.read_fees(fee_raw(), frozen, inputs)
    base = s.series(doc, days(), fees, 1.5)
    # Each leg: net 8 + commission 2 - 2 sides * 1 * 1.5 = 7.
    np.testing.assert_array_equal(base[0], [14, -8, 22])
    np.testing.assert_array_equal(s.series(doc, days(), fees, 1.5, debits={}), base)
    debit = {days()[0]: 3.0}
    with pytest.raises(s.Void):
        s.series(doc, days(), fees, 1.5, debits=debit)
    changed = s.series(doc, days(), fees, 1.5, debits=debit, ruling='synthetic-ruling')
    np.testing.assert_array_equal(changed[0], [11,-11,22])
    np.testing.assert_array_equal(changed[1:], base[1:])


def test_e10_real_bootstrap_cells_and_growth(s):
    result = s.score_cells({c: np.tile([1., 0., 1.], (40,1)) for c in (1,1.5)}, 1000.)
    assert len(result['drawdown']) == 18 and len(result['growth']) == 3
    assert all(cell['hits'] == 0 and cell['pass'] for cell in result['drawdown'].values())
    assert all(cell['terminal_median'] == 1252. and cell['pass'] for cell in result['growth'].values())


def passing_cells():
    return dict(drawdown={f'{w}/{c}/{seed}': dict(hits=0, **{'pass':True})
                         for w in ('FULL','H1','H2') for c in (1,1.5) for seed in (42,123,2026)},
                growth={w: dict(terminal_median=1252., **{'pass':True}) for w in ('FULL','H1','H2')})


@pytest.mark.parametrize('kind,index', [('drawdown',i) for i in range(18)] + [('growth',i) for i in range(3)])
def test_e10_every_binding_cell_binds(s, kind, index):
    cells = passing_cells()
    assert s.verdict(cells, gates=dict.fromkeys(('G1','G3','G1_D','G3_D'),True), margin='PASS', total_trip=False) == 'RESOLVED'
    cells[kind][list(cells[kind])[index]]['pass'] = False
    assert s.verdict(cells, gates=dict.fromkeys(('G1','G3','G1_D','G3_D'),True), margin='PASS', total_trip=False) == 'NOT CLEARED'


def test_e11_e12_verdict_order_trip_and_e14_reports(s):
    args = dict(gates=dict.fromkeys(('G1','G3','G1_D','G3_D'),True), margin='PASS', total_trip=True)
    assert s.verdict(passing_cells(), **args) == 'NOT CLEARED'
    assert s.verdict(passing_cells(), **args, void=True) == 'VOID'
    assert s.verdict(passing_cells(), **args, void=True, freeze_invalid=True) == 'FREEZE INVALID'
    args['total_trip'] = False
    cells = passing_cells()
    cells['residuals'] = {'bad':float('inf')}
    cells['sensitivities'] = {'bad':False}
    assert s.verdict(cells, **args) == 'RESOLVED'


@pytest.mark.parametrize('peak,band', [(100,'PASS'), (500,'PASS'), (501,'MARGINAL'), (600,'MARGINAL'), (601,'FAIL')])
def test_e13_exact_margin_bands(s, peak, band):
    # E0=1500, G3=1, f=150/1500: u_max=(.85-.15-.1)/1.5=.4.
    result = s.b2(peak, 1500, 1., 150., 100.)
    assert result['headroom_usd'] == 600 - peak
    assert result['status'] == band
    if band != 'PASS':
        assert s.verdict(passing_cells(), gates=dict.fromkeys(('G1','G3','G1_D','G3_D'),True),
                         margin=band, total_trip=False) == 'NOT CLEARED'


def test_e13a_each_b2_term(s):
    assert s.b2(100,1500,1.,150.,100.)['headroom_usd'] == 500
    assert s.b2(130,1500,1.,150.,100.)['headroom_usd'] == 470
    assert s.b2(100,1500,2.,150.,100.)['headroom_usd'] == 350
    assert s.b2(100,1500,1.,180.,100.)['headroom_usd'] == 480


def margins():
    return ('## Margins per contract (USD, synthetic)\n'
            '| Symbol | Contract | Exchange | Intraday ("Day") margin |\n'
            '|---|---|---|---|\n' + ''.join(f'| **{symbol}** | test | CME | 100.00 |\n' for symbol in SYMBOLS)).encode()


def test_e13b_margin_hash_and_table(s):
    blob = margins()
    assert s.read_margins(blob, sha(blob)) == dict.fromkeys(SYMBOLS,100.)
    with pytest.raises(s.Void):
        s.read_margins(blob, '0'*64)
    for bad in (blob.replace(b'100.00',b'$100.00'), blob + b'| 6J | t | CME | 100.00 |\n',
                blob.replace(b'| **MNQ** | test | CME | 100.00 |\n',b'')):
        with pytest.raises(s.Void):
            s.read_margins(bad, sha(bad))


def test_added_port_head_trip_and_m_star(s):
    state = port_state()
    assert s.read_port_state(raw(state), HEAD, 1000.)['m_star'] == 1.2
    state['legs'][LEGS[1]]['total_dd_trips_utc'] = ['2026-01-05T15:00:00Z']
    assert s.read_port_state(raw(state), HEAD, 1000.)['total_trip']
    with pytest.raises(s.Void):
        s.read_port_state(raw(state), 'b'*40, 1000.)


def test_added_score_inputs_closed_and_manifest_bound(s):
    blob = raw(score_inputs())
    assert s.read_score_inputs(blob, {'score.json':sha(blob)}, 'score.json')['f_basis'] == 'prescreen_debited_case'
    with pytest.raises(s.Void):
        s.read_score_inputs(blob, {}, 'score.json')
    bad = raw(dict(score_inputs(), extra=1))
    with pytest.raises(s.Void):
        s.read_score_inputs(bad, {'score.json':sha(bad)}, 'score.json')


def test_added_fee_both_identities(s):
    frozen, inputs = freeze(), score_inputs()
    blob = fee_raw()
    inputs['fee_snapshot_v1_sha256'] = sha(blob)
    assert s.read_fees(blob, frozen, inputs).rates_for('6J')['commission'] == 1
    with pytest.raises(s.Void):
        s.read_fees(blob+b' ', frozen, inputs)
    frozen['fee_snapshot']['sha256'] = 'f'*64
    with pytest.raises(s.Void):
        s.read_fees(blob, frozen, inputs)


def test_e18_latch_is_not_a_verdict_input_and_zero_days_remain(s):
    doc = route()
    frozen, inputs = freeze(), score_inputs()
    inputs['fee_snapshot_v1_sha256'] = sha(fee_raw())
    fees = s.read_fees(fee_raw(), frozen, inputs)
    base = s.series(doc, days(), fees, 1)
    doc['latch'] = dict(utc='2026-01-05T16:00:00Z', kind='personal_halt_latched')
    np.testing.assert_array_equal(s.series(doc, days(), fees, 1), base)
    assert len(base) == 61 and np.count_nonzero(base[1:]) == 0


def test_freeze_identity_and_finite_required_cells(s):
    blob = raw(freeze())
    assert s.read_freeze(blob, sha(blob), '2'*64)['G3']['p95'] == .5
    with pytest.raises(s.FreezeInvalid):
        s.read_freeze(blob, 'f'*64, '2'*64)
    bad = freeze()
    del bad['G1'][LEGS[0]]['p95']
    blob = raw(bad)
    with pytest.raises(s.FreezeInvalid):
        s.read_freeze(blob, sha(blob), '2'*64)


def test_e10_actual_bad_drawdown_and_growth_cells(s):
    hit = s.score_cells({c:np.tile([0.,-150.,0.],(40,1)) for c in (1,1.5)},1000.)
    assert all(cell['hits'] == 10000 and not cell['pass'] for cell in hit['drawdown'].values())
    flat = s.score_cells({c:np.zeros((40,3)) for c in (1,1.5)},1000.)
    assert all(not cell['pass'] for cell in flat['growth'].values())


def test_margin_uses_concurrent_tranches_once(s):
    doc = route()
    doc['trades'] += [trade(quantity=2), trade(leg=LEGS[1])]
    result = s.margin_from_route(doc,dict.fromkeys(SYMBOLS,100.),1500.,freeze(),score_inputs())
    # 3 concurrent 6J contracts + 1 MYM = 400, irrespective of paired exits.
    assert result['u'] == pytest.approx(400/1500)


def schedule():
    return {'header':{'schema':'sfclear_historical_schedule/v1'},'sessions':[
        dict(account_date=d.isoformat(),permission='PERMITTED',
             opens_utc=d.isoformat()+'T14:00:00Z',risk_add_cutoff_utc=d.isoformat()+'T20:45:00Z',
             flatten_start_utc=d.isoformat()+'T20:55:00Z',own_flat_deadline_utc=d.isoformat()+'T21:00:00Z')
        for d in days()]}


def rolls():
    return dict(contracts=[dict(product=sym,contract_month='2026-03',
                              g4_start_open_utc='2026-06-01T22:00:00Z') for sym in ('6J','MGC')],seams=[])


@pytest.mark.parametrize('damage', ['denied','late_entry','late_exit','g4','mae','missing_day'])
def test_route_defects_void_before_score(s, damage):
    doc, sched, roll = route(), schedule(), rolls()
    if damage == 'denied':
        sched['sessions'][0] = dict(account_date='2026-01-05',permission='DENIED')
    elif damage == 'late_entry':
        doc['trades'][0].update(entry_utc='2026-01-05T20:45:00Z',exit_utc='2026-01-05T20:50:00Z')
    elif damage == 'late_exit':
        doc['trades'][0]['exit_utc'] = '2026-01-05T21:00:00Z'
    elif damage == 'g4':
        roll['contracts'][0]['g4_start_open_utc'] = '2026-01-05T15:30:00Z'
    elif damage == 'mae':
        del doc['trades'][0]['mae_usd']
    else:
        doc['days'].pop()
    with pytest.raises(s.Void):
        s.check_route_gates(doc,days(),sched,roll)


def test_route_gates_accept_latch_zero_days(s):
    doc = route()
    doc['latch'] = dict(utc='2026-01-05T16:00:00Z',kind='personal_halt_latched')
    s.check_route_gates(doc,days(),schedule(),rolls())


def test_residual_measured_for_every_trade_nonbinding(s):
    doc = route()
    doc['trades'][0].update(mae_usd=-8.,quantity=2,stop_fill_distance_b=.5)
    # pv=2: 2*max(0,.5,8/(2*2)-1)=2 dollars/contract.
    report = s.residual_report(doc,dict.fromkeys(SYMBOLS,2.),dict.fromkeys(LEGS[:3],2),freeze(),1000.)
    assert report['per_leg'][LEGS[0]] == {'p95':2.,'max':2.}
    assert report['G1']['p95'][LEGS[0]] == pytest.approx(.1+2/150)
    assert report['G3']['p95'] == pytest.approx(.5+4/150)


def test_calculator_process_binds_hash_m_star_and_inputs(s,tmp_path):
    # Stub is an external executable, not a mock of the scorer.
    script = tmp_path/'calc.py'
    script.write_text('''import argparse,hashlib,json,pathlib
p=argparse.ArgumentParser()
p.add_argument('--repo-root');p.add_argument('--out-root');p.add_argument('--m-star',type=float)
p.add_argument('--input',nargs=3,action='append');a=p.parse_args()
legs=['aegis_6j','dj30_mym_p250','vanguard_mgc']
h=lambda b:hashlib.sha256(b).hexdigest()
d={'schema':'sfclear2_g1g3/v1','calculator_sha256':h(pathlib.Path(__file__).read_bytes()),
'created_utc':'2026-01-01T00:00:00Z','nonce':'a'*64,'m_star':a.m_star,'on_legs':legs,
'window_et':['2026-01-01','2026-01-31'],'units':'rope','statistics':['p95','max'],
'pine_ta_sha256':'b'*64,'inputs':{n:{'path':f,'sha256':s} for n,f,s in a.input},
'G1':{k:{'p95':.1,'max':.2} for k in legs},'G3':{'p95':.5,'max':.6},
'G1_D':{k:{'p95':.1*a.m_star,'max':.2*a.m_star} for k in legs},
'G3_D':{'p95':.5*a.m_star,'max':.6*a.m_star},
 'terms_rope':{k:{t:{'p95':.01,'max':.02} for t in ['T1','T3','gap']} for k in legs}}
b=json.dumps(d).encode();(pathlib.Path(a.out_root)/'g1g3_20260101T000000Z_12345678.json').write_bytes(b)
print(h(b))
''')
    inp=tmp_path/'input';inp.write_bytes(b'synthetic')
    inputs={key:dict(path=str(inp),sha256=sha(inp.read_bytes())) for key in s.CALCULATOR_INPUTS}
    kwargs=dict(expected_sha256=sha(script.read_bytes()),repo=tmp_path,inputs=inputs,m_star=1.2)
    doc=s.calculator_cells(script,output_root=tmp_path/'out',**kwargs)
    assert doc['G3_D']['p95'] == .6
    with pytest.raises(s.Void):
        s.calculator_cells(script,output_root=tmp_path/'out2',**dict(kwargs,expected_sha256='f'*64))
    inp.write_bytes(b'changed')
    with pytest.raises(s.Void):
        s.calculator_cells(script,output_root=tmp_path/'out3',**kwargs)


@pytest.mark.parametrize('required,b3,news', [(100.,237.5,500.), (200.,137.5,100.), (300.,37.5,-300.)])
def test_b3_news_formulas_are_nonbinding(s, required, b3, news):
    reports = s.margin_sensitivities(required,1500.,1.,150.,100.)
    assert reports['B3']['headroom_usd'] == b3
    assert reports['news']['headroom_usd'] == news
    assert reports['B3']['status'] == ('PASS' if b3 >= 100 else 'MARGINAL')
    assert reports['news']['status'] == ('PASS' if news >= 100 else 'FAIL')
    cells = passing_cells()
    cells['sensitivities'] = reports
    assert s.verdict(cells,gates=dict.fromkeys(('G1','G3','G1_D','G3_D'),True),
                     margin='PASS',total_trip=False) == 'RESOLVED'


def test_seam_removes_trades_not_days_and_never_binds(s):
    doc = route()
    doc['trades'] = [trade(d.isoformat()) for d in days()]
    frozen, inputs = freeze(),score_inputs()
    inputs['fee_snapshot_v1_sha256'] = sha(fee_raw())
    fees = s.read_fees(fee_raw(),frozen,inputs)
    empty = {symbol:() for symbol in SYMBOLS}
    baseline = s.seam_sensitivity(doc,days(),fees,1000.,empty)
    # A seam on every session excludes all trades while retaining every day.
    removed = s.seam_sensitivity(doc,days(),fees,1000.,dict(empty, **{'6J':days()}))
    assert baseline['windows']['FULL']['terminal_median'] == 3016.
    assert removed['windows']['FULL']['terminal_median'] == 1000.
    assert removed['removed_trades'] == 61 and removed['calendar_days'] == 61
    for report in (baseline,removed):
        cells = passing_cells()
        cells['sensitivities'] = {'seams':report}
        assert s.verdict(cells,gates=dict.fromkeys(('G1','G3','G1_D','G3_D'),True),
                         margin='PASS',total_trip=False) == 'RESOLVED'


def test_seam_inclusive_ten_weekday_boundary(s):
    calendar=days()
    doc=route()
    doc['trades']=[trade(calendar[i].isoformat()) for i in (9,10,30,31)]
    frozen,inputs=freeze(),score_inputs()
    inputs['fee_snapshot_v1_sha256']=sha(fee_raw())
    fees=s.read_fees(fee_raw(),frozen,inputs)
    report=s.seam_sensitivity(doc,calendar,fees,1000.,
        {'6J':(calendar[20],),'MYM':(),'MGC':(),'MNQ':()})
    assert report['removed_trades'] == 2
    assert report['calendar_days'] == 61


def test_maximum_changes_residual_only(s):
    doc=route()
    doc['trades']=[trade(leg=leg) for leg in LEGS[:3]]
    frozen=freeze()
    changed=copy.deepcopy(frozen)
    changed['G1'][LEGS[0]]['max']=1001.
    changed['G3']['max']=1002.
    args=(doc,dict.fromkeys(SYMBOLS,2.),dict.fromkeys(LEGS[:3],1))
    first=s.residual_report(*args,frozen,1000.)
    second=s.residual_report(*args,changed,1000.)
    assert second['G1']['max'][LEGS[0]]-first['G1']['max'][LEGS[0]] == 2.
    assert second['G3']['max']-first['G3']['max'] == 3.
    assert second['G1']['p95'] == first['G1']['p95']
    for reports in (first,second):
        cells=passing_cells()
        cells['residuals']=reports
        assert s.verdict(cells,gates=dict.fromkeys(('G1','G3','G1_D','G3_D'),True),
                         margin='PASS',total_trip=False) == 'RESOLVED'


def test_composition_binds_all_cells_and_residuals(s):
    doc=route()
    doc['latch']=dict(utc=days()[-1].isoformat()+'T16:00:00Z',kind='personal_halt_latched')
    doc['trades']=[trade(d.isoformat(),leg=leg) for d in days() for leg in LEGS[:3]]
    frozen,inputs=freeze(),score_inputs()
    inputs['fee_snapshot_v1_sha256']=sha(fee_raw())
    fees=s.read_fees(fee_raw(),frozen,inputs)
    drift={'G1_D':{leg:{'p95':.1,'max':.3} for leg in LEGS[:3]},'G3_D':{'p95':.5,'max':.8}}
    result=s.compose(doc,calendar=days(),fees=fees,equity=1000.,frozen=frozen,
        inputs=inputs,margins=dict.fromkeys(SYMBOLS,10.),port=s.read_port_state(raw(port_state()),HEAD,1000.),
        drift=drift,schedule=schedule(),rolls=rolls(),pointvalues=dict.fromkeys(SYMBOLS,1.),
        rule_max=dict.fromkeys(LEGS[:3],1),roll_dates=dict.fromkeys(SYMBOLS,()))
    assert result['verdict']=='RESOLVED'
    assert len(result['cells']['drawdown'])==18 and len(result['cells']['growth'])==3
    assert set(result['residuals'])=={'slippage','drift_slippage','port_state','sensitivities'}
    assert set(result['residuals']['sensitivities'])=={'B3','news','seams'}
    assert result['gates']==dict.fromkeys(('G1','G3','G1_D','G3_D'),True)


@pytest.fixture
def artifact_request(tmp_path):
    root=tmp_path/'private';root.mkdir()
    calculator=tmp_path/'calculator.py'
    calculator.write_text('''import argparse,hashlib,json,pathlib
p=argparse.ArgumentParser();p.add_argument('--repo-root');p.add_argument('--out-root');p.add_argument('--m-star',type=float);p.add_argument('--input',nargs=3,action='append');a=p.parse_args()
legs=['aegis_6j','dj30_mym_p250','vanguard_mgc'];h=lambda b:hashlib.sha256(b).hexdigest()
d={'schema':'sfclear2_g1g3/v1','calculator_sha256':h(pathlib.Path(__file__).read_bytes()),'created_utc':'2026-01-01T00:00:00Z','nonce':'a'*64,'m_star':a.m_star,'on_legs':legs,'window_et':['2026-01-01','2026-03-31'],'units':'rope','statistics':['p95','max'],'pine_ta_sha256':'b'*64,'inputs':{n:{'path':f,'sha256':s} for n,f,s in a.input},'G1':{k:{'p95':.1,'max':.2} for k in legs},'G3':{'p95':.5,'max':.6},'G1_D':{k:{'p95':.1*a.m_star,'max':.2*a.m_star} for k in legs},'G3_D':{'p95':.5*a.m_star,'max':.6*a.m_star},'terms_rope':{k:{t:{'p95':.01,'max':.02} for t in ['T1','T3','gap']} for k in legs}}
b=json.dumps(d).encode();(pathlib.Path(a.out_root)/'g1g3_20260101T000000Z_12345678.json').write_bytes(b);print(h(b))
''')
    inputs=score_inputs();inputs['fee_snapshot_v1_sha256']=sha(fee_raw())
    frozen=freeze();frozen['calculator_sha256']=sha(calculator.read_bytes());frozen['margin_snapshot']['sha256']=sha(margins())
    tuple_doc={'capital_anchor':{'file_sha256':sha(b'1000\n')},'size_vector_sha256':sha(b'{}'),
               'rule_max_contracts':dict(zip(LEGS,(1,1,1,0)))}
    blobs={'freeze':raw(frozen),'fees':fee_raw(),'margin':margins(),'score_inputs':raw(inputs),'e0':b'1000\n',
           'tuple':raw(tuple_doc),'size_vector':b'{}','source_bundle':b'{}','schedule':raw(schedule()),
           'roll_list':raw(rolls()),'generator':b'synthetic','calendar':b'synthetic',
           'reference_friction':raw({'instruments':{leg:{'pointvalue':1.} for leg in LEGS}})}
    for role,blob in blobs.items():
        (root/(role+'.bin')).write_bytes(blob)
    calc_inputs={name:{'path':str(root/'calendar.bin'),'sha256':sha(blobs['calendar'])}
                 for name in ('book_sources','effective_inputs','meta:6J','meta:MGC','meta:MYM','panel:6J','panel:MGC','panel:MYM')}
    for name in ('e0','tuple','schedule'):
        calc_inputs[name]={'path':str(root/(name+'.bin')),'sha256':sha(blobs[name])}
    panel_refs={}
    for leg in LEGS:
        panel=root/(leg+'.csv')
        panel.write_text('time,open,high,low,close,volume\n'+''.join(
            d.isoformat()+'T14:00:00Z,1,1,1,1,1\n' for d in days()))
        panel_refs[leg]={'path':str(panel),'sha256':sha(panel.read_bytes())}
    for leg,symbol in zip(LEGS[:3],('6J','MYM','MGC')):
        calc_inputs['panel:'+symbol]=panel_refs[leg]
    request={'schema':'sfclear_score_request/v1','repo':str(SOURCE.parents[4]),'root':str(root),
             'run_head':HEAD,'pins':{key:sha(blobs[key]) for key in ('freeze','tuple','schedule','roll_list')},
             'inputs':{key:key+'.bin' for key in blobs},'calculator':{'path':str(calculator),'inputs':calc_inputs},
             'panels':panel_refs}
    request['pins']['calculator']=sha(calculator.read_bytes())
    doc=route();doc['trades']=[trade(d.isoformat(),leg=leg) for d in days() for leg in LEGS[:3]]
    doc['input_identities']={key:sha(blobs[key]) for key in doc['input_identities']}
    (root/'route.json').write_bytes(raw(doc));(root/'port_state.json').write_bytes(raw(port_state()))
    (root/'nonce').write_bytes(b'n'*32);(root/'request.json').write_bytes(raw(request))
    def seal():
        manifest=''.join(sha(path.read_bytes())+'  '+path.name+'\n' for path in sorted(root.iterdir())
                         if path.is_file() and path.name!='INPUT_SHA256SUMS').encode()
        (root/'INPUT_SHA256SUMS').write_bytes(manifest)
        return sha(manifest)
    return root,request,seal


def test_artifacts_to_private_verdict_with_real_calculator_process(s,artifact_request):
    root,request,seal=artifact_request
    result=s.score_request(request,manifest_sha256=seal())
    assert result['verdict']=='RESOLVED'
    assert (root/'cells.json').is_file() and (root/'residuals.json').is_file()
    assert json.loads((root/'cells.json').read_bytes())['run_head']==HEAD
    assert len(list((root/'calculator-output').glob('*.json')))==1


def test_score_cli_no_private_output(artifact_request):
    import subprocess
    root,request,seal=artifact_request
    proc=subprocess.run([sys.executable,str(SOURCE),'--request',str(root/'request.json'),
                         '--manifest-sha256',seal()],capture_output=True,text=True)
    assert proc.returncode==0,proc.stderr
    assert proc.stdout=='' and proc.stderr==''
    assert json.loads((root/'cells.json').read_bytes())['verdict']=='RESOLVED'


def test_manifest_mismatch_refuses_before_calculator(s,artifact_request):
    root,request,seal=artifact_request
    expected=seal();(root/'score_inputs.bin').write_bytes(b'{}')
    with pytest.raises(s.Void):
        s.score_request(request,manifest_sha256=expected)
    assert not (root/'calculator-output').exists()


def test_panel_endpoints_cannot_be_narrowed(s,artifact_request):
    root,request,seal=artifact_request
    request['panel_spans']={leg:[days()[10].isoformat(),days()[-1].isoformat()] for leg in LEGS}
    with pytest.raises(s.Void):
        s.score_request(request,manifest_sha256=seal(),preflight=True)


def test_panel_content_must_match_inventory(s,artifact_request):
    root,request,seal=artifact_request
    expected=seal()
    Path(request['panels'][LEGS[3]]['path']).write_text('time,open,high,low,close,volume\n')
    with pytest.raises(s.Void):
        s.score_request(request,manifest_sha256=expected,preflight=True)


SCORE_MUTANTS = {
    'M-E2': [('cut = len(calendar) // 2', 'cut = 2*len(calendar)//3')],
    'M-E5': [('and not total_trip)', 'and True)')],
    'M-E6': [("'PASS' if headroom >= step", "'PASS' if headroom >= 0")],
    'M-E8': [('for pair in spans.values():', 'for pair in list(spans.values())[:3]:')],
    'M-E9': [("maximum = (Fraction('0.85')-g-f)/Fraction('1.5')", "maximum = (Fraction('0.85')-g-f)/Fraction('2')")],
    'M-E10': [("if _sha(raw) != _hex(expected_sha256):\n        raise Void('margin identity mismatch')", 'if False:\n        pass')],
    'M-E11': [('result[i,:2] -= debits.get(day,0)', 'result[i,:2] -= 4*debits.get(day,0)')],
    'M-E12': [("if any(debits.values()) and (type(ruling) is not str or not ruling.strip()):", 'if False:')],
    'M-E13': [("total_trip=port['total_trip'])", "total_trip=port['total_trip'] or route['latch'] is not None)")],
}


@pytest.mark.parametrize('name', SCORE_MUTANTS)
def test_named_score_mutant_is_killed(name):
    import types
    source=SOURCE.read_text()
    for old,new in SCORE_MUTANTS[name]:
        assert source.count(old)==1, (name,old)
        source=source.replace(old,new)
    mutant=types.ModuleType('sfclear_score_mutant')
    mutant.__file__=str(SOURCE)
    sys.modules[mutant.__name__]=mutant
    exec(compile(source,str(SOURCE),'exec'),mutant.__dict__)
    checks={'M-E2':test_e9_half_split_and_short_void,
            'M-E5':test_e11_e12_verdict_order_trip_and_e14_reports,
            'M-E8':test_e17_off_empty_leg_still_sets_span,
            'M-E9':test_e13a_each_b2_term,'M-E10':test_e13b_margin_hash_and_table,
            'M-E11':test_e16_fee_gross_once_and_account_debit_once,
            'M-E12':test_e16_fee_gross_once_and_account_debit_once,
            'M-E13':test_composition_binds_all_cells_and_residuals}
    with pytest.raises((AssertionError,pytest.fail.Exception)):
        if name=='M-E6':
            test_e13_exact_margin_bands(mutant,501,'MARGINAL')
        else:
            checks[name](mutant)


def test_full_synthetic_job_to_sealed_candidate(artifact_request,tmp_path,monkeypatch):
    import importlib
    import subprocess
    records=importlib.import_module('analysis.c1.sfclear_2026-10.run_record')
    root,request,_=artifact_request
    repo=tmp_path/'checkout';repo.mkdir()
    def git(*args):
        return subprocess.run(['git','-C',str(repo),*args],check=True,capture_output=True,text=True).stdout.strip()
    git('init');git('config','user.name','Synthetic');git('config','user.email','synthetic@example.invalid')
    git('config','core.hooksPath',str(tmp_path/'absent-hooks'))
    module_root=repo/'lab/analysis/c1/sfclear_2026-10';module_root.mkdir(parents=True)
    for name in ('run_record.py','score_r1.py'):
        (module_root/name).write_bytes(SOURCE.with_name(name).read_bytes())
    (repo/'scripts').mkdir()
    (repo/'scripts/fp.py').write_text('import subprocess,sys\nraise SystemExit(subprocess.call([sys.executable,*sys.argv[2:]]))\n')
    (repo/'frozen').write_text('synthetic freeze')
    git('add','.');git('commit','-m','synthetic source')
    head=git('rev-parse','HEAD')
    fg=tmp_path/'fg.json';fg.write_bytes(b'{"status":"PASS"}')
    driver=tmp_path/'driver.py'
    port=json.loads((root/'port_state.json').read_bytes());port['run_head']=head
    driver.write_text('import pathlib,sys,json\nr=pathlib.Path(sys.argv[1])\n'
        +"assert (r/'provenance.json').is_file()\n"
        +"assert 'provenance.json' in (r/'INPUT_SHA256SUMS').read_text()\n"
        +"(r/'route.json').write_bytes("+repr((root/'route.json').read_bytes())+")\n"
        +"(r/'port_state.json').write_bytes("+repr(raw(port))+")\n")
    monkeypatch.setattr(records,'__file__',str(module_root/'run_record.py'))
    monkeypatch.setattr(records,'freeze_bindings',lambda repo:request['pins'])
    original_begin=records.begin
    monkeypatch.setattr(records,'begin',lambda **kwargs:original_begin(**kwargs,freeze=head,frozen_paths=('frozen',)))
    output=tmp_path/'sfclear2-run-20260101T000000Z'
    candidate=records.run_job({'repo':str(repo),'private_root':str(output),
        'fg':{'path':str(fg),'sha256':sha(fg.read_bytes())},
        'driver':{'path':str(driver),'sha256':sha(driver.read_bytes()),'args':['{private_root}']},
        'inputs':{role:{'path':str(root/name),'sha256':sha((root/name).read_bytes())}
                  for role,name in request['inputs'].items()},
        'calculator':request['calculator'],'panels':request['panels']})
    assert candidate.record['run_head']==head
    assert json.loads((output/'cells.json').read_bytes())['verdict']=='RESOLVED'
    _,manifest=records.read_manifest(output)
    assert {'provenance.json','route.json','port_state.json','cells.json','residuals.json'}<=set(manifest)
    assert git('status','--porcelain')==''
