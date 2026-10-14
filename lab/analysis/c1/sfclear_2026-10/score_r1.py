"""Fixed R1 scoring composition. All values and reports stay in private artifacts.

Uses the shared scorer and margin engine unchanged. Serialized route output is
validated here without importing ops. No grid, ranking, or alternative portfolio.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta
from fractions import Fraction
import hashlib
import math
from pathlib import Path
import re
import subprocess
import sys
from zoneinfo import ZoneInfo

import numpy as np

from discovery.sfgrowth_acceptance import (Void, ExportTrade, strict_object, daily_series,
                                           common_calendar, bootstrap_indices, score)
from discovery.remc_series_builder import Trade
from discovery.sfclear_tradovate_fees import parse_snapshot
from research_utils.sfgrowth_margin import MarginFill, check_concurrent_margin

LEGS = ('aegis_6j', 'dj30_mym_p250', 'vanguard_mgc', 'orb_mnq_v7')
SYMBOLS = dict(zip(LEGS, ('6J', 'MYM', 'MGC', 'MNQ')))
ON_LEGS = LEGS[:3]
ET = ZoneInfo('America/New_York')
SEEDS = (42, 123, 2026)
COSTS = (1, 1.5)
CALCULATOR_HASH = '2333844dd2a9342239812baa38a119b55f4b8a65841165740a9a39633f2297bf'
CALCULATOR_INPUTS = {'book_sources', 'e0', 'effective_inputs', 'meta:6J', 'meta:MGC',
                     'meta:MYM', 'panel:6J', 'panel:MGC', 'panel:MYM', 'schedule', 'tuple'}
TRADE_FIELDS = {'leg', 'instrument', 'contract', 'entry_utc', 'exit_utc', 'side', 'quantity',
    'tranche_index', 'entry_price', 'initial_stop_level', 'delta_0', 'exit_price',
    'exit_kind', 'stop_fill_distance_b', 'net_pnl_usd', 'commission_usd', 'mae_usd', 'mfe_usd'}
ROUTE_INPUTS = {'tuple', 'size_vector', 'source_bundle', 'schedule', 'roll_list',
                'generator', 'calendar', 'reference_friction', 'e0'}


class FreezeInvalid(ValueError):
    """Freeze defect; precedes runtime VOID."""


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _hex(value, length=64):
    if type(value) is not str or re.fullmatch('[0-9a-f]{%d}' % length, value) is None:
        raise Void('invalid digest')
    return value


def _finite(value, *, minimum=None, positive=False):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise Void('finite number required')
    if (minimum is not None and value < minimum) or (positive and value <= 0):
        raise Void('numeric range')
    return value


def _closed(doc, fields):
    if type(doc) is not dict or set(doc) != set(fields):
        raise Void('closed fields required')


def _utc(value):
    try:
        result = datetime.fromisoformat(value)
        if result.utcoffset() != timedelta(0):
            raise ValueError
        return result
    except (ValueError, TypeError):
        raise Void('aware UTC time required') from None


def _p95(doc, key, per_leg=False):
    try:
        if per_leg:
            if set(doc[key]) != set(ON_LEGS):
                raise Void('ON leg cells required')
            return {leg: _finite(doc[key][leg]['p95'], minimum=0) for leg in ON_LEGS}
        return _finite(doc[key]['p95'], minimum=0)
    except (KeyError, TypeError):
        raise Void('binding cell absent') from None


def read_freeze(raw, expected_sha256, calculator_sha256=CALCULATOR_HASH):
    try:
        if _sha(raw) != _hex(expected_sha256):
            raise Void('freeze identity mismatch')
        doc = strict_object(raw)
        if doc['schema'] != 'sfclear3_freeze/v1':
            raise Void('freeze schema')
        _hex(doc['nonce'])
        if _hex(doc['calculator_sha256']) != _hex(calculator_sha256):
            raise Void('calculator identity differs')
        _p95(doc, 'G1', True)
        _p95(doc, 'G3')
        for key in ('margin_snapshot_sha256','fee_snapshot_sha256',
                    'effective_schedule_sha256','roll_list_sha256','source_build_sha256sums_sha256'):
            _hex(doc[key])
        return doc
    except (ValueError, KeyError, TypeError):
        raise FreezeInvalid('invalid frozen record') from None


def read_score_inputs(raw, manifest, name):
    if manifest.get(name) != _sha(raw):
        raise Void('scoring inputs absent or mismatched in manifest')
    doc = strict_object(raw)
    _closed(doc, ('schema', 'monthly_debited_fixed_costs_usd', 'f_basis', 'f_source_sha256',
                  'fee_snapshot_v1_sha256', 'vanguard_paper_capital_usd'))
    if doc['schema'] != 'sfclear_score_inputs/v1':
        raise Void('scoring inputs schema')
    _finite(doc['monthly_debited_fixed_costs_usd'], minimum=0)
    _finite(doc['vanguard_paper_capital_usd'], positive=True)
    _hex(doc['f_source_sha256'])
    _hex(doc['fee_snapshot_v1_sha256'])
    basis = doc['f_basis']
    if type(basis) is not str or (basis != 'prescreen_debited_case'
                                  and not re.fullmatch(r'ruling:\S.*', basis)):
        raise Void('fixed cost basis required')
    return doc


def read_fees(raw, frozen, inputs):
    try:
        return parse_snapshot(raw, expected_sha256=inputs['fee_snapshot_v1_sha256'],
                              expected_source_sha256=frozen['fee_snapshot_sha256'])
    except (ValueError, KeyError, TypeError):
        raise Void('fee identity or schema mismatch') from None


def read_margins(raw, expected_sha256):
    if _sha(raw) != _hex(expected_sha256):
        raise Void('margin identity mismatch')
    try:
        lines = raw.decode('utf-8').splitlines()
        headers = [i for i,line in enumerate(lines) if line.startswith('## Margins per contract (USD,')]
        if len(headers) != 1:
            raise Void('margin heading required')
        result, table = {}, False
        for line in lines[headers[0]+1:]:
            if line.startswith('#'):
                break
            if line.startswith('| Symbol | Contract | Exchange | Intraday ("Day") margin |'):
                if table:
                    raise Void('duplicate margin table')
                table = True
                continue
            if not table or not line.startswith('|'):
                continue
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            if cells and all(re.fullmatch(r':?-+:?', cell) for cell in cells):
                continue
            if len(cells) < 4:
                raise Void('margin row shape')
            symbol = cells[0]
            if symbol.startswith('**') and symbol.endswith('**'):
                symbol = symbol[2:-2]
            if symbol not in SYMBOLS.values():
                continue
            if symbol in result or not re.fullmatch(r'(?:\d+|\d{1,3}(?:,\d{3})+)\.\d{2}', cells[3]):
                raise Void('margin cell or duplicate symbol')
            result[symbol] = _finite(float(cells[3].replace(',','')), positive=True)
        if set(result) != set(SYMBOLS.values()):
            raise Void('incomplete margins')
        return result
    except UnicodeError:
        raise Void('margin encoding') from None


def read_port_state(raw, run_head, paper_capital):
    doc = strict_object(raw)
    _closed(doc, ('schema','run_head','legs'))
    if doc['schema'] != 'sfclear_port_state/v1' or _hex(doc['run_head'],40) != _hex(run_head,40):
        raise Void('port-state identity')
    _closed(doc['legs'], (LEGS[1],LEGS[2]))
    striker = doc['legs'][LEGS[1]]
    _closed(striker, ('daily_dd_trips_utc','total_dd_trips_utc'))
    for times in striker.values():
        if type(times) is not list:
            raise Void('trip list required')
        for time in times:
            _utc(time)
    _closed(doc['legs'][LEGS[2]], ('e_p',))
    path = doc['legs'][LEGS[2]]['e_p']
    if type(path) is not list or not path:
        raise Void('nonempty paper equity path required')
    stamps, values = [], []
    for row in path:
        if type(row) is not list or len(row) != 2:
            raise Void('paper equity row')
        stamps.append(_utc(row[0]))
        values.append(_finite(row[1]))
    if stamps != sorted(set(stamps)):
        raise Void('paper equity chronology')
    return dict(m_star=max(1., max(values)/_finite(paper_capital,positive=True)),
                total_trip=bool(striker['total_dd_trips_utc']), record=doc)


def panel_calendar(spans):
    _closed(spans, LEGS)
    try:
        ranges = []
        for pair in spans.values():
            if len(pair) != 2:
                raise Void('panel endpoints')
            start, end = map(date.fromisoformat, pair)
            if start > end:
                raise Void('panel endpoints')
            ranges.append((start,end))
        return common_calendar(ranges)
    except (TypeError, ValueError):
        raise Void('invalid four-panel calendar') from None


def admitted_panel_calendar(panels, calc_inputs):
    """Derive endpoints from exact retained CSV bytes, including the OFF leg.

    References are supplied by the coordinator from the admitted panel inventory.
    No panel bytes are copied and no caller-provided endpoint can trim history.
    """
    import csv
    import io
    _closed(panels, LEGS)
    spans={}
    for leg,ref in panels.items():
        _closed(ref, ('path','sha256'))
        blob=Path(ref['path']).read_bytes()
        if _sha(blob)!=_hex(ref['sha256']):
            raise Void('panel source identity')
        if leg in ON_LEGS and calc_inputs['panel:'+SYMBOLS[leg]]['sha256']!=ref['sha256']:
            raise Void('calculator panel differs')
        rows=csv.DictReader(io.StringIO(blob.decode('utf-8-sig')))
        if rows.fieldnames!=['time','open','high','low','close','volume']:
            raise Void('admitted panel columns')
        first=last=previous=None
        for row in rows:
            instant=datetime.fromisoformat(row['time'].replace('Z','+00:00'))
            if instant.utcoffset() is None or previous is not None and instant<=previous:
                raise Void('panel chronology')
            local=instant.astimezone(ET)
            day=local.date()+timedelta(days=int(local.hour>=18))
            first=day if first is None else first
            last=day
            previous=instant
        if first is None:
            raise Void('empty panel')
        spans[leg]=(first.isoformat(),last.isoformat())
    return panel_calendar(spans)


def windows(calendar):
    cut = len(calendar) // 2
    if min(cut, len(calendar)-cut) < 20:
        raise Void('window shorter than 20 weekdays')
    return dict(FULL=calendar, H1=calendar[:cut], H2=calendar[cut:])


def validate_route(doc):
    _closed(doc, ('schema','trades','refusals','days','input_identities','latch'))
    if doc['schema'] != 'sfclear_route_output/v1':
        raise Void('route schema')
    _closed(doc['input_identities'], ROUTE_INPUTS)
    for value in doc['input_identities'].values():
        _hex(value)
    _closed(doc['refusals'], LEGS)
    for rows in doc['refusals'].values():
        if type(rows) is not list:
            raise Void('refusal rows')
        for row in rows:
            _closed(row, ('utc','reason'))
            _utc(row['utc'])
            if type(row['reason']) is not str or not row['reason']:
                raise Void('refusal reason')
    if type(doc['days']) is not list or not doc['days']:
        raise Void('route days required')
    dates = []
    for row in doc['days']:
        _closed(row, ('account_date','net_pnl_usd','fills'))
        dates.append(date.fromisoformat(row['account_date']))
        _finite(row['net_pnl_usd'])
        if type(row['fills']) is not int or row['fills'] < 0:
            raise Void('day fill count')
    if dates != sorted(set(dates)):
        raise Void('day chronology')
    if doc['latch'] is not None:
        _closed(doc['latch'], ('utc','kind'))
        _utc(doc['latch']['utc'])
        if doc['latch']['kind'] != 'personal_halt_latched':
            raise Void('latch kind')
    if type(doc['trades']) is not list:
        raise Void('trade rows')
    for row in doc['trades']:
        _closed(row, TRADE_FIELDS)
        if row['leg'] not in LEGS or row['instrument'] != SYMBOLS[row['leg']]:
            raise Void('trade leg')
        if _utc(row['entry_utc']) > _utc(row['exit_utc']):
            raise Void('trade time order')
        if row['side'] not in ('buy','sell') or type(row['quantity']) is not int or row['quantity'] <= 0:
            raise Void('trade side/quantity')
        if type(row['tranche_index']) is not int or row['tranche_index'] != 0:
            raise Void('R1 tranche')
        for key in ('contract','exit_kind'):
            if type(row[key]) is not str or not row[key]:
                raise Void('trade text')
        for key in ('entry_price','initial_stop_level','delta_0','exit_price','stop_fill_distance_b',
                    'net_pnl_usd','commission_usd','mae_usd','mfe_usd'):
            _finite(row[key])
        if (row['mae_usd'] > 0 or min(row[k] for k in ('mfe_usd','commission_usd','delta_0','stop_fill_distance_b')) < 0
                or row['delta_0'] != abs(row['entry_price']-row['initial_stop_level'])):
            raise Void('trade values')
    return doc


def series(route, calendar, fees, cost, *, debits=None, ruling=None):
    validate_route(route)
    result = np.zeros((len(calendar),3))
    for leg in LEGS:
        captured = []
        for i, row in enumerate(route['trades']):
            if row['leg'] != leg:
                continue
            trade = Trade(leg, i, _utc(row['entry_utc']).astimezone(ET),
                _utc(row['exit_utc']).astimezone(ET), row['quantity'], row['net_pnl_usd'],
                row['commission_usd'], row['mae_usd'])
            captured.append(ExportTrade(trade,row['mfe_usd']))
        result += daily_series(captured,calendar,fees.rates_for(SYMBOLS[leg]),cost)
    debits = {} if debits is None else debits
    if not set(debits) <= set(calendar):
        raise Void('debit outside calendar')
    for value in debits.values():
        _finite(value,minimum=0)
    if any(debits.values()) and (type(ruling) is not str or not ruling.strip()):
        raise Void('nonzero debit requires operator ruling')
    for i, day in enumerate(calendar):
        result[i,:2] -= debits.get(day,0)
    return result


def score_cells(series_by_cost, equity):
    if set(series_by_cost) != set(COSTS):
        raise Void('both cost channels required')
    length = len(series_by_cost[1])
    if len(series_by_cost[1.5]) != length:
        raise Void('cost calendars differ')
    slices = windows(tuple(range(length)))
    result = dict(drawdown={},growth={})
    for window, indices in slices.items():
        draws = bootstrap_indices(len(indices))
        for cost in COSTS:
            summary = score(series_by_cost[cost][list(indices)],equity,draws)
            for seed, hits in zip(SEEDS, summary.hits):
                result['drawdown'][f'{window}/{cost}/{seed}'] = {'hits':hits,'pass':hits <= 100}
            if cost == 1.5:
                result['growth'][window] = {'terminal_median':summary.growth,'pass':summary.growth > equity}
    return result


def b2(required_margin, equity, g3, monthly_costs, six_j_margin):
    values = (required_margin,equity,g3,monthly_costs,six_j_margin)
    for value in values:
        _finite(value,minimum=0)
    if equity <= 0 or six_j_margin <= 0:
        raise Void('positive equity and margin required')
    required, e0, g3, fixed, step = map(lambda v: Fraction(str(v)),values)
    u = required/e0
    g, f = Fraction('0.15')*g3, fixed/e0
    maximum = (Fraction('0.85')-g-f)/Fraction('1.5')
    headroom = (maximum-u)*e0
    status = 'PASS' if headroom >= step else 'MARGINAL' if headroom >= 0 else 'FAIL'
    return dict(status=status,u=float(u),g=float(g),f=float(f),u_max=float(maximum),headroom_usd=float(headroom))


def margin_from_route(route, margins, equity, frozen, inputs):
    validate_route(route)
    fills = {leg:[] for leg in LEGS}
    expected = {leg:[] for leg in LEGS}
    for i,row in enumerate(route['trades']):
        leg = row['leg']
        for kind,key in (('entry','entry_utc'),('exit','exit_utc')):
            identity = f'{i}:{kind}'
            fills[leg].append(MarginFill(identity,str(i),_utc(row[key]),kind,row['quantity']))
            expected[leg].append(identity)
    result = check_concurrent_margin(fills,initial_margin_by_leg={leg:margins[SYMBOLS[leg]] for leg in LEGS},
                                     equity_limit=equity,expected_fill_ids_by_leg=expected)
    if result.status == 'VOID':
        raise Void('margin ledger invalid')
    return b2(float(result.required_margin),equity,_p95(frozen,'G3'),
              inputs['monthly_debited_fixed_costs_usd'],margins['6J'])


def verdict(cells, *, gates, margin, total_trip, freeze_invalid=False, void=False):
    if freeze_invalid:
        return 'FREEZE INVALID'
    if void:
        return 'VOID'
    expected = {f'{w}/{c}/{seed}' for w in ('FULL','H1','H2') for c in COSTS for seed in SEEDS}
    if (set(cells.get('drawdown',{})) != expected or set(cells.get('growth',{})) != {'FULL','H1','H2'}
            or set(gates) != {'G1','G3','G1_D','G3_D'}):
        return 'VOID'
    clear = (all(cell.get('pass') is True for group in ('drawdown','growth') for cell in cells[group].values())
             and all(value is True for value in gates.values()) and margin == 'PASS' and not total_trip)
    return 'RESOLVED' if clear else 'NOT CLEARED'


def calculator_cells(calculator, *, expected_sha256, repo, output_root, inputs, m_star):
    """Hash-bind executable, all input bytes, and exact returned file bytes."""
    if set(inputs) != CALCULATOR_INPUTS:
        raise Void('calculator input inventory')
    _finite(m_star,minimum=1)
    calculator, output = Path(calculator).resolve(), Path(output_root).resolve()
    if output.exists():
        raise Void('fresh calculator directory required')
    for parent in (output,*output.parents):
        if (parent/'.git').exists():
            raise Void('calculator output inside repository')
    try:
        if _sha(calculator.read_bytes()) != _hex(expected_sha256):
            raise Void('calculator identity')
        args = [sys.executable,'-I',str(calculator),'--repo-root',str(repo),
                '--out-root',str(output),'--m-star',str(m_star)]
        for name,row in sorted(inputs.items()):
            _closed(row,('path','sha256'))
            if _sha(Path(row['path']).read_bytes()) != _hex(row['sha256']):
                raise Void('calculator input mismatch')
            args.extend(('--input',name,str(row['path']),row['sha256']))
        output.mkdir(parents=True)
        proc = subprocess.run(args,capture_output=True)
        files = list(output.iterdir())
        if proc.returncode or proc.stderr or len(files) != 1 or not re.fullmatch(r'g1g3_[0-9TZ]+_[0-9a-f]{8}\.json',files[0].name):
            raise Void('calculator output failure')
        blob = files[0].read_bytes()
        if proc.stdout.strip().decode('ascii') != _sha(blob):
            raise Void('calculator output hash')
        doc = strict_object(blob)
        if (doc['schema'] != 'sfclear2_g1g3/v1' or doc['m_star'] != m_star
                or doc['calculator_sha256'] != expected_sha256):
            raise Void('calculator output binding')
        _hex(doc['nonce'])
        _p95(doc,'G1_D',True)
        _p95(doc,'G3_D')
        if _sha(calculator.read_bytes()) != expected_sha256:
            raise Void('calculator changed')
        for row in inputs.values():
            if _sha(Path(row['path']).read_bytes()) != row['sha256']:
                raise Void('calculator input changed')
        return doc
    except (OSError, UnicodeError, KeyError, TypeError):
        raise Void('calculator unavailable or malformed') from None


def check_route_gates(route, calendar, schedule, rolls):
    validate_route(route)
    try:
        sessions = {date.fromisoformat(row['account_date']):row for row in schedule['sessions']}
        if len(sessions) != len(schedule['sessions']):
            raise Void('duplicate schedule day')
        actual_days = {date.fromisoformat(row['account_date']):row for row in route['days']}
        if not set(calendar) <= set(actual_days) or not set(actual_days) <= set(sessions):
            raise Void('route calendar incomplete')
        boundaries = {}
        for row in rolls['contracts']:
            key = (row['product'],row['contract_month'])
            if key in boundaries:
                raise Void('duplicate roll contract')
            boundaries[key] = _utc(row['g4_start_open_utc'])
        for day,row in actual_days.items():
            if sessions[day]['permission'] == 'DENIED' and (row['fills'] or row['net_pnl_usd']):
                raise Void('DENIED day not zero')
        for row in route['trades']:
            entry, end = _utc(row['entry_utc']), _utc(row['exit_utc'])
            local = entry.astimezone(ET)
            day = local.date()+timedelta(days=int(local.hour >= 18))
            session = sessions[day]
            if (session['permission'] != 'PERMITTED'
                    or not _utc(session['opens_utc']) <= entry < _utc(session['risk_add_cutoff_utc'])
                    or end >= _utc(session['own_flat_deadline_utc'])):
                raise Void('G0 route breach')
            if row['instrument'] in ('6J','MGC'):
                boundary = boundaries[(row['instrument'],row['contract'])]
                if end >= boundary:
                    raise Void('G4 route breach')
    except (KeyError,TypeError,ValueError) as exc:
        raise Void('route gate validation failed') from exc


def residual_report(route, pointvalues, rule_max, frozen, equity):
    """Nonbinding per-contract slippage report, including non-stop exits."""
    validate_route(route)
    _closed(pointvalues,SYMBOLS.values())
    _closed(rule_max,ON_LEGS)
    for value in pointvalues.values():
        _finite(value,positive=True)
    for value in rule_max.values():
        if type(value) is not int or value < 0:
            raise Void('rule maximum must be integer')
    rope = .15*_finite(equity,positive=True)
    observed = {leg:[] for leg in ON_LEGS}
    for row in route['trades']:
        if row['leg'] not in observed:
            raise Void('OFF leg produced trade')
        pv = pointvalues[row['instrument']]
        value = pv*max(0,row['stop_fill_distance_b'],
                       abs(row['mae_usd'])/(row['quantity']*pv)-row['delta_0'])
        observed[row['leg']].append(value)
    per_leg = {leg:({'p95':float(np.percentile(values,95)), 'max':max(values)} if values
                    else {'p95':None,'max':None}) for leg,values in observed.items()}
    # No trade is not a measured zero residual. Keep incomplete re-checks null.
    g1,g3 = {},{}
    for statistic in ('p95','max'):
        g1[statistic] = {leg:(None if per_leg[leg][statistic] is None else
            _finite(frozen['G1'][leg][statistic],minimum=0)+per_leg[leg][statistic]/rope) for leg in ON_LEGS}
        terms = [rule_max[leg]*per_leg[leg][statistic]/rope for leg in ON_LEGS
                 if per_leg[leg][statistic] is not None]
        g3[statistic] = _finite(frozen['G3'][statistic],minimum=0)+sum(terms) if terms else None
    return dict(per_leg=per_leg,G1=g1,G3=g3)


def margin_sensitivities(required_margin, equity, g3, monthly_costs, six_j_margin):
    """D-1 nonbinding B3 and all-contract 4x news-rate reports."""
    # Reuse B2 validation, but calculate from exact inputs rather than its floats.
    b2(required_margin,equity,g3,monthly_costs,six_j_margin)
    required,e0,g3,fixed,step = map(lambda v:Fraction(str(v)),
        (required_margin,equity,g3,monthly_costs,six_j_margin))
    u,g,f = required/e0,Fraction('0.15')*g3,fixed/e0
    headrooms = {'B3':((Fraction('0.85')-2*g-f)/2-u)*e0,
                 'news':(Fraction('0.85')-g-f-4*u)*e0}
    return {name:{'headroom_usd':float(value),
                  'status':'PASS' if value >= step else 'MARGINAL' if value >= 0 else 'FAIL'}
            for name,value in headrooms.items()}


def seam_sensitivity(route, calendar, fees, equity, roll_dates_by_symbol, *, debits=None, ruling=None):
    """Remove affected trades at c=1; retain the fixed calendar and zero days.

    Q-SFCLEAR-2 replaces Explore/Confirm with FULL/H1/H2. Report each of those
    fixed windows without selecting a portfolio or making this a verdict input.
    """
    from discovery.sfgrowth_acceptance import outside_roll_seams

    validate_route(route)
    _closed(roll_dates_by_symbol,SYMBOLS.values())
    keep = {symbol:set(outside_roll_seams(calendar,dates))
            for symbol,dates in roll_dates_by_symbol.items()}
    trades = []
    for row in route['trades']:
        local = _utc(row['exit_utc']).astimezone(ET)
        session = local.date()+timedelta(days=int(local.hour >= 18))
        if session in keep[row['instrument']]:
            trades.append(row)
    filtered = dict(route,trades=trades)
    channels = series(filtered,calendar,fees,1,debits=debits,ruling=ruling)
    reports = {}
    for name,indices in windows(tuple(range(len(calendar)))).items():
        summary = score(channels[list(indices)],equity,bootstrap_indices(len(indices)))
        reports[name] = {'hits':dict(zip(SEEDS,summary.hits)), 'terminal_median':summary.growth}
    return {'windows':reports,'removed_trades':len(route['trades'])-len(trades),
            'calendar_days':len(calendar)}


def compose(route, *, calendar, fees, equity, frozen, inputs, margins, port, drift,
            schedule, rolls, pointvalues, rule_max, roll_dates, debits=None, ruling=None):
    """Complete fixed R1 result; return private data, never print it."""
    check_route_gates(route,calendar,schedule,rolls)
    windows(calendar)
    channels = {cost:series(route,calendar,fees,cost,debits=debits,ruling=ruling) for cost in COSTS}
    margin = margin_from_route(route,margins,equity,frozen,inputs)
    gates = {'G1':all(value <= .20 for value in _p95(frozen,'G1',True).values()),
             'G3':_p95(frozen,'G3') <= 1.,
             'G1_D':all(value <= .20 for value in _p95(drift,'G1_D',True).values()),
             'G3_D':_p95(drift,'G3_D') <= 1.}
    cells = score_cells(channels,equity)
    label = verdict(cells,gates=gates,margin=margin['status'],total_trip=port['total_trip'])
    # Reports are computed only after the binding decision and never fed back.
    drift_base = {'G1':drift['G1_D'],'G3':drift['G3_D']}
    residuals = {'slippage':residual_report(route,pointvalues,rule_max,frozen,equity),
                 'drift_slippage':residual_report(route,pointvalues,rule_max,drift_base,equity),
                 'port_state':port['record'],
                 'sensitivities':margin_sensitivities(margin['u']*equity,equity,_p95(frozen,'G3'),
                                        inputs['monthly_debited_fixed_costs_usd'],margins['6J'])}
    residuals['sensitivities']['seams'] = seam_sensitivity(route,calendar,fees,equity,roll_dates,
                                                         debits=debits,ruling=ruling)
    description = ('clears on exposed history (model-fitted; 15:55 flatten at the R1 adverse intrabar placement)'
                   if label == 'RESOLVED' else label)
    return {'verdict':label,'label':description,'cells':cells,'gates':gates,'B2':margin,'residuals':residuals}


def source_build_inputs(binding, frozen, blobs, roll_sha256):
    """Verify the independent source-build folder without modifying its bytes."""
    import importlib
    records=importlib.import_module('analysis.c1.sfclear_2026-10.run_record')
    _closed(binding,('path','sha256','inputs'))
    root=records.outside_git(binding['path'])
    manifest=(root/'SHA256SUMS').read_bytes()
    if _sha(manifest)!=_hex(binding['sha256']) or binding['sha256']!=frozen['source_build_sha256sums_sha256']:
        raise Void('source-build manifest identity')
    rows={}
    for line in manifest.decode('utf-8').splitlines():
        match=re.fullmatch(r'([0-9a-f]{64})  (.+)',line)
        if match is None:
            raise Void('source-build manifest encoding')
        expected,name=match.groups()
        if name in rows or name=='SHA256SUMS':
            raise Void('source-build manifest inventory')
        path=records._within(root,name)
        if _sha(path.read_bytes())!=expected:
            raise Void('source-build file identity')
        rows[name]=expected
    _closed(binding['inputs'],('source_bundle','reference_friction','effective_schedule'))
    result={}
    for role,ref in binding['inputs'].items():
        _closed(ref,('path','sha256'))
        path=Path(ref['path']).resolve()
        if not path.is_relative_to(root):
            raise Void('source-build input outside folder')
        if rows.get(path.relative_to(root).as_posix())!=_hex(ref['sha256']):
            raise Void('source-build input absent from manifest')
        result[role]=path.read_bytes()
        if _sha(result[role])!=ref['sha256']:
            raise Void('source-build input changed')
    if any(result[role]!=blobs[role] for role in ('source_bundle','reference_friction')):
        raise Void('source-build differs from replay input')
    if _sha(result['effective_schedule'])!=frozen['effective_schedule_sha256']:
        raise Void('effective schedule identity')
    if frozen['roll_list_sha256']!=roll_sha256 or _sha(blobs['roll_list'])!=roll_sha256:
        raise Void('roll list differs from F2')
    return result


def score_request(request, *, manifest_sha256, preflight=False):
    """Consume the wrapper's retained request and hashed private inventory.

    The coordinator supplies exact admitted panel references in the request. run_job binds
    that request before replay and supplies pins verified from F, not from input
    files. Standalone callers must establish the same chronology with run_record.
    """
    import importlib
    import json
    import secrets
    records=importlib.import_module('analysis.c1.sfclear_2026-10.run_record')
    try:
        _closed(request,('schema','repo','root','run_head','pins','inputs','calculator','panels','source_build'))
        if request['schema']!='sfclear_score_request/v1':
            raise Void('score request schema')
        _hex(request['run_head'],40)
        root=records.outside_git(request['root'])
        _closed(request['pins'],('freeze','calculator','tuple','schedule','roll_list'))
        for value in request['pins'].values():
            _hex(value)
        roles={'freeze','fees','margin','score_inputs',*ROUTE_INPUTS}
        _closed(request['inputs'],roles)
        # Freeze defects precede runtime VOID failures, including manifest errors.
        freeze_blob=records._within(root,request['inputs']['freeze']).read_bytes()
        frozen=read_freeze(freeze_blob,request['pins']['freeze'],request['pins']['calculator'])
        manifest_blob,manifest=records.read_manifest(root,required=tuple(request['inputs'].values()),
                                                      filename='INPUT_SHA256SUMS')
        if _sha(manifest_blob)!=_hex(manifest_sha256):
            raise Void('input manifest identity')
        blobs={role:records._within(root,name).read_bytes() for role,name in request['inputs'].items()}
        if any(_sha(blob)!=manifest[request['inputs'][role]] for role,blob in blobs.items()):
            raise Void('input changed during read')
        for role in ('freeze','tuple','schedule','roll_list'):
            if _sha(blobs[role])!=request['pins'][role]:
                raise Void('frozen input differs')
        source=source_build_inputs(request['source_build'],frozen,blobs,request['pins']['roll_list'])
        inputs=read_score_inputs(blobs['score_inputs'],manifest,request['inputs']['score_inputs'])
        fees=read_fees(blobs['fees'],frozen,inputs)
        margins=read_margins(blobs['margin'],frozen['margin_snapshot_sha256'])
        tuple_doc=strict_object(blobs['tuple'])
        if (re.fullmatch(rb'[0-9]+\n',blobs['e0']) is None
                or _sha(blobs['e0'])!=tuple_doc['capital_anchor']['file_sha256']):
            raise Void('equity identity')
        equity=_finite(float(int(blobs['e0'])),positive=True)
        if int(equity)!=int(blobs['e0']):
            raise Void('equity precision')
        schedule=strict_object(source['effective_schedule'])
        roll_list=strict_object(blobs['roll_list'])
        friction=strict_object(blobs['reference_friction'])
        pointvalues={SYMBOLS[leg]:friction['instruments'][leg]['pointvalue'] for leg in LEGS}
        rule_max={leg:tuple_doc['rule_max_contracts'][leg] for leg in ON_LEGS}
        if tuple_doc['rule_max_contracts'][LEGS[3]]!=0:
            raise Void('OFF leg rule maximum')
        _closed(request['calculator'],('path','inputs'))
        calc_inputs=request['calculator']['inputs']
        if set(calc_inputs)!=CALCULATOR_INPUTS:
            raise Void('calculator inputs incomplete')
        for name in ('e0','tuple','schedule'):
            expected_blob=source['effective_schedule'] if name=='schedule' else blobs[name]
            if calc_inputs[name]['sha256']!=_sha(expected_blob):
                raise Void('calculator source differs from score source')
        for ref in calc_inputs.values():
            _closed(ref,('path','sha256'))
            if _sha(Path(ref['path']).read_bytes())!=_hex(ref['sha256']):
                raise Void('calculator source mismatch')
        if _sha(Path(request['calculator']['path']).read_bytes())!=request['pins']['calculator']:
            raise Void('calculator source identity')
        calendar=admitted_panel_calendar(request['panels'],calc_inputs)
        windows(calendar)
        if preflight:
            return None
        if (root/'cells.json').exists() or (root/'residuals.json').exists():
            raise Void('refuse scoring overwrite')
        for name in ('route.json','port_state.json'):
            if name not in manifest:
                raise Void('replay output absent from manifest')
        route=strict_object((root/'route.json').read_bytes())
        expected={role:_sha(blobs[role]) for role in ROUTE_INPUTS}
        expected['size_vector']=tuple_doc['size_vector_sha256']
        if route['input_identities']!=expected:
            raise Void('route input identity differs')
        check_route_gates(route,calendar,schedule,roll_list)
        port=read_port_state((root/'port_state.json').read_bytes(),request['run_head'],inputs['vanguard_paper_capital_usd'])
        drift=calculator_cells(request['calculator']['path'],expected_sha256=request['pins']['calculator'],
            repo=request['repo'],output_root=root/'calculator-output',inputs=calc_inputs,m_star=port['m_star'])
        roll_dates={symbol:[] for symbol in SYMBOLS.values()}
        for row in roll_list['seams']:
            roll_dates[row['product']].append(date.fromisoformat(row['switch_trade_date']))
        result=compose(route,calendar=calendar,fees=fees,equity=equity,frozen=frozen,inputs=inputs,
            margins=margins,port=port,drift=drift,schedule=schedule,rolls=roll_list,
            pointvalues=pointvalues,rule_max=rule_max,roll_dates=roll_dates)
        if admitted_panel_calendar(request['panels'],calc_inputs)!=calendar:
            raise Void('panel calendar changed')
        # Check immutable snapshots again before making output available.
        after,_=records.read_manifest(root,filename='INPUT_SHA256SUMS')
        if after!=manifest_blob:
            raise Void('input manifest changed')
        source_build_inputs(request['source_build'],frozen,blobs,request['pins']['roll_list'])
        cells={key:value for key,value in result.items() if key!='residuals'}
        cells.update(schema='sfclear_cells/v1',run_head=request['run_head'],nonce=secrets.token_hex(32))
        residuals={'schema':'sfclear_residuals/v1','run_head':request['run_head'],
                   'nonce':secrets.token_hex(32),**result['residuals']}
        for name,doc in (('cells.json',cells),('residuals.json',residuals)):
            with (root/name).open('xb') as stream:
                stream.write((json.dumps(doc,sort_keys=True,allow_nan=False)+'\n').encode())
        return result
    except FreezeInvalid:
        raise
    except (OSError,KeyError,TypeError,ValueError,OverflowError):
        raise Void('scoring input or output invalid') from None


def main(argv=None):
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--request',type=Path,required=True)
    parser.add_argument('--manifest-sha256',required=True)
    parser.add_argument('--preflight',action='store_true')
    args=parser.parse_args(argv)
    try:
        score_request(strict_object(args.request.read_bytes()),manifest_sha256=args.manifest_sha256,
                      preflight=args.preflight)
        return 0
    except FreezeInvalid:
        print('FREEZE INVALID',file=sys.stderr)
        return 2
    except (OSError,ValueError):
        print('VOID',file=sys.stderr)
        return 1


if __name__=='__main__':
    raise SystemExit(main())
