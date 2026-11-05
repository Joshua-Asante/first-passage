"""One fixed M6E exploratory expression. No parameter search or holdout scoring."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'fp.ps1').exists())
sys.path.insert(0, str(ROOT / 'core'))
from bar_export_loader import decode_bar_meta, decode_bar_signal

LDN = ZoneInfo('Europe/London')
START, END = date(2016, 1, 4), date(2024, 12, 31)
TICK, POINT_VALUE, TICK_VALUE, COST = 0.0001, 12500.0, 1.25, 6.60
REQUIRED = frozenset(range(420, 601, 15))


@dataclass(frozen=True)
class Bar:
    o: int
    h: int
    l: int
    c: int


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def london_day_minute(epoch):
    t = datetime.fromtimestamp(epoch / 1000, timezone.utc).astimezone(LDN)
    return t.date(), t.hour * 60 + t.minute


def validate_input_years(years):
    if sorted(years) != list(range(2016, 2025)):
        raise ValueError('Only the nine frozen 2016-2024 input files may be decoded')


def load_days(reg, data_root):
    """Verify the allowlist and hashes before decoding any prices; no broad data glob."""
    validate_input_years([f['year'] for f in reg['scored_files']])
    files = [(f, Path(data_root) / f['name']) for f in reg['scored_files']]
    for f, path in files:
        if path.name != f['name'] or sha(path) != f['sha256']:
            raise ValueError(f'Input hash/path mismatch: {f["name"]}')
    days, seen, volume_zero, bars = defaultdict(dict), set(), 0, 0
    for f, path in files:
        with path.open(encoding='utf-8-sig', newline='') as stream:
            for row in csv.DictReader(stream):
                if not str(row.get('Type', '')).startswith('Entry'):
                    continue
                # Check timestamp and sample fence BEFORE decoding any OHLC values.
                epoch = int(row['Signal'].split('|', 1)[0])
                dt = datetime.fromtimestamp(epoch / 1000, timezone.utc)
                d, minute = london_day_minute(epoch)
                if dt.year != f['year'] or d.year > 2024:
                    raise ValueError('Unexpected year in an allowed input file')
                if epoch in seen:
                    raise ValueError('Duplicate bar-open timestamp')
                seen.add(epoch)
                if not START <= d <= END:
                    continue
                decoded, meta = decode_bar_signal(row['Signal']), decode_bar_meta(row['Signal'])
                expected = {'ticker': 'M6E1!', 'type': 'futures', 'quote_currency': 'USD',
                            'base_currency': 'EUR', 'mintick': TICK, 'pointvalue': POINT_VALUE,
                            'timezone': 'America/Chicago', 'timeframe': '15'}
                if not meta or {k:v for k,v in meta.items() if k != '_bar'} != expected:
                    raise ValueError('Unexpected instrument metadata')
                if epoch % 900000 or meta['_bar']['time_close_ms'] - epoch != 900000:
                    raise ValueError('Unexpected bar clock/duration')
                prices = [decoded[k] for k in ('o', 'h', 'l', 'c')]
                if not all(math.isfinite(x) and x > 0 for x in prices):
                    raise ValueError('Invalid price')
                ticks = [round(x / TICK) for x in prices]
                if any(abs(x / TICK - t) > 1e-6 for x,t in zip(prices, ticks)):
                    raise ValueError('Price not on declared M6E tick grid')
                b = Bar(*ticks)
                if b.l > min(b.o, b.c) or b.h < max(b.o, b.c) or b.h < b.l:
                    raise ValueError('Invalid OHLC shape')
                if abs(float(row['Price USD']) - decoded['c']) > TICK / 2:
                    raise ValueError('Transport price disagrees with encoded close')
                if not math.isfinite(decoded['v']) or decoded['v'] < 0:
                    raise ValueError('Invalid volume')
                bars += 1
                if d.weekday() < 5:
                    days[d][minute] = b
                    volume_zero += int(minute in REQUIRED and decoded['v'] == 0)
    return days, {'decoded_bars': bars, 'zero_volume_window_bars': volume_zero}


def simulate_day(bars):
    if not REQUIRED <= bars.keys():
        return {'status': 'incomplete'}
    high = max(bars[m].h for m in range(420, 480, 15))
    low = min(bars[m].l for m in range(420, 480, 15))
    if high == low:
        return {'status': 'zero_range'}
    for signal_minute in range(480, 540, 15):
        close = bars[signal_minute].c
        sign = 1 if close > high else -1 if close < low else 0
        if not sign:
            continue
        entry_minute = signal_minute + 15
        entry = bars[entry_minute].o
        stop = low if sign == 1 else high
        risk_ticks = sign * (entry - stop)
        if risk_ticks <= 0:
            return {'status': 'entry_gap_skip'}
        exit_price, exit_minute, reason = bars[600].o, 600, 'time'
        for m in range(entry_minute, 600, 15):
            b = bars[m]
            if sign * (b.o - stop) <= 0:
                exit_price, exit_minute, reason = b.o, m, 'gap_stop'
                break
            if (sign == 1 and b.l <= stop) or (sign == -1 and b.h >= stop):
                exit_price, exit_minute, reason = stop, m, 'stop'
                break
        # 10:00 open is both the scheduled exit and any boundary gap fill;
        # its later high/low cannot affect a position already flattened.
        favorable = [sign * ((bars[m].h if sign == 1 else bars[m].l) - entry)
                     for m in range(entry_minute, 600, 15)] + [sign * (bars[600].o - entry), 0]
        gross = sign * (exit_price - entry) * TICK_VALUE
        return {'status': 'trade', 'direction': 'long' if sign == 1 else 'short',
                'entry_minute': entry_minute, 'entry_ticks': entry, 'stop_ticks': stop,
                'exit_minute': exit_minute, 'exit_ticks': exit_price, 'exit_reason': reason,
                'gross': gross, 'net': gross - COST, 'risk_ticks': risk_ticks,
                'reachable_r_before_1000_ignoring_stop': max(favorable) / risk_ticks}
    return {'status': 'no_signal'}


def bootstrap_ci(pnl, count, reps=10000, seed=20261104):
    """Circular moving blocks, 20 eligible mornings; ratio mean over traded mornings."""
    pnl, count = np.asarray(pnl, float), np.asarray(count, int)
    n = len(pnl)
    if n == 0 or count.sum() == 0:
        return [None, None]
    rng, block = np.random.default_rng(seed), min(20, n)
    full, rem = divmod(n, block)
    starts = rng.integers(0, n, size=(reps, full + int(rem > 0)))
    sums = []
    for values in (pnl, count):
        cs = np.concatenate(([0], np.cumsum(np.tile(values, 2))))
        totals = (cs[starts[:, :full] + block] - cs[starts[:, :full]]).sum(axis=1)
        if rem:
            totals += cs[starts[:, -1] + rem] - cs[starts[:, -1]]
        sums.append(totals)
    valid = sums[1] > 0
    return np.quantile(sums[0][valid] / sums[1][valid], [0.025, 0.975]).tolist()


def summarize(days, direction=None, reps=10000):
    def selected(d):
        return d['status'] == 'trade' and (direction is None or d['direction'] == direction)
    trades = [d for d in days if selected(d)]
    pnl = np.array([d['net'] if selected(d) else 0 for d in days], dtype=float)
    count = np.array([int(selected(d)) for d in days])
    n, gross, net = len(trades), sum(d['gross'] for d in trades), float(pnl.sum())
    wins = sum(d['net'] > 0 for d in trades)
    gains, losses = sum(max(d['net'], 0) for d in trades), -sum(min(d['net'], 0) for d in trades)
    curve = np.concatenate(([0], np.cumsum(pnl)))
    return {'eligible_days': len(days), 'trades': n, 'gross_total': gross, 'cost_total': COST * n,
            'net_total': net, 'net_mean': net / n if n else None,
            'net_mean_95pct_block_ci': bootstrap_ci(pnl, count, reps=reps),
            'net_win_rate': wins / n if n else None,
            'net_profit_factor': gains / losses if losses else None,
            'closed_trade_max_drawdown': float(np.max(np.maximum.accumulate(curve) - curve))}


def run(registration, data_root, output):
    reg = json.loads(Path(registration).read_text(encoding='utf-8'))
    # Literal rule and sample parameters live in this file; registration identifies them,
    # not a configuration surface for testing variants.
    if reg['sample_start'] != START.isoformat() or reg['sample_end'] != END.isoformat() or reg['round_trip_cost'] != COST:
        raise ValueError('Registration contradicts fixed implementation')
    for relative, digest in reg['pre_outcome_sha256'].items():
        if sha(ROOT / relative) != digest:
            raise ValueError('Source differs from pre-outcome registration')
    source_files = [HERE / 'experiment.py', HERE / 'test_experiment.py', Path(registration), ROOT / 'core/bar_export_loader.py']
    before = {str(p): sha(p) for p in source_files}
    days, audit = load_days(reg, data_root)
    outcomes, exclusions = [], []
    d = START
    while d <= END:
        if d.weekday() < 5:
            result = {'date': d.isoformat(), **simulate_day(days.get(d, {}))}
            if result['status'] == 'incomplete':
                exclusions.append(result)
            else:
                outcomes.append(result)
        d += timedelta(days=1)
    trades = [x for x in outcomes if x['status'] == 'trade']
    summary = {'scope': 'one fixed exploratory expression; no holdout or builder acceptance',
               'sample_start': START.isoformat(), 'sample_end': END.isoformat(),
               'round_trip_cost': COST, 'audit': audit,
               'calendar_weekdays': len(outcomes) + len(exclusions),
               'incomplete_days': len(exclusions), 'excluded_dates': [x['date'] for x in exclusions],
               'status_counts': dict(Counter(x['status'] for x in outcomes)),
               'all': summarize(outcomes),
               'direction': {s: summarize(outcomes, s) for s in ('long', 'short')},
               'year': {str(y): summarize([x for x in outcomes if x['date'].startswith(str(y))]) for y in range(2016, 2025)},
               'year_direction': {str(y): {s: summarize([x for x in outcomes if x['date'].startswith(str(y))], s)
                                          for s in ('long', 'short')} for y in range(2016, 2025)},
               'exit_counts': dict(Counter(x['exit_reason'] for x in trades)),
               'entry_clock_counts': dict(Counter(str(x['entry_minute']) for x in trades)),
               'geometry': {'median_initial_stop_dollars': float(np.median([x['risk_ticks'] * TICK_VALUE for x in trades])),
                            'median_reachable_r_ignoring_stop': float(np.median([x['reachable_r_before_1000_ignoring_stop'] for x in trades])),
                            'fraction_reaching_1r_ignoring_stop': float(np.mean([x['reachable_r_before_1000_ignoring_stop'] >= 1 for x in trades]))},
               'uncertainty': {'method': 'circular moving-block percentile bootstrap of eligible daily outcomes',
                               'block_days': 20, 'replicates': 10000, 'seed': 20261104,
                               'scope': 'descriptive, conditional on model/sample; no selection or execution-error adjustment'}}
    if any(sha(p) != h for p,h in before.items()):
        raise ValueError('Source changed during run')
    for f in reg['scored_files']:
        if sha(Path(data_root) / f['name']) != f['sha256']:
            raise ValueError('Input changed during run')
    if not math.isclose(summary['all']['net_total'], sum(s['net_total'] for s in summary['year'].values()), abs_tol=1e-7):
        raise ValueError('Year reconciliation failed')
    if not math.isclose(summary['all']['net_total'], sum(s['net_total'] for s in summary['direction'].values()), abs_tol=1e-7):
        raise ValueError('Direction reconciliation failed')
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    (output / 'summary.json').write_text(json.dumps(summary, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    (output / 'daily_private.json').write_text(json.dumps(outcomes, indent=2) + '\n', encoding='utf-8')
    record = {'status': 'completed', 'created_at_utc': datetime.now(timezone.utc).isoformat(),
              'interpreter': sys.executable, 'python_version': sys.version,
              'source_sha256': before, 'source_stable': True, 'input_hashes_stable': True,
              'scored_files': reg['scored_files'], 'summary_sha256': sha(output / 'summary.json'),
              'prices_loaded_outside_scored_years': False}
    (output / 'run_record.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: summary[k] for k in ('calendar_weekdays', 'incomplete_days', 'status_counts', 'all', 'direction', 'year', 'geometry')}, indent=2))
    print('Saved:', output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--registration', type=Path, required=True)
    parser.add_argument('--data-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    run(args.registration, args.data_root, args.output)
