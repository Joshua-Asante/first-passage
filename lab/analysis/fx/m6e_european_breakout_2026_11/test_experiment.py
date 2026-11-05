"""Hand-calculated execution and data-boundary regressions, independent of vendor data."""
from datetime import datetime, timezone
import csv
import hashlib

import numpy as np
import pytest

from .experiment import Bar, bootstrap_ci, load_days, london_day_minute, simulate_day, summarize, validate_input_years


def morning():
    return {m: Bar(11000, 11005, 10995, 11000) for m in range(420, 601, 15)}


def long_morning():
    b = morning()
    b[480] = Bar(11000, 11008, 10990, 11006)  # stop touched before entry: irrelevant
    for m in range(495, 600, 15):
        b[m] = Bar(11008, 11014, 11000, 11010)
    b[600] = Bar(11012, 11020, 10900, 11000)  # post-exit low: irrelevant
    return b


def test_next_open_not_signal_close_and_no_signal_bar_or_post_exit_stop():
    t = simulate_day(long_morning())
    assert (t['entry_minute'], t['entry_ticks'], t['exit_ticks'], t['exit_reason']) == (495, 11008, 11012, 'time')
    assert t['gross'] == 5.0
    assert t['net'] == pytest.approx(-1.60)


@pytest.mark.parametrize('bar,exit_ticks,reason', [
    (Bar(11008, 11014, 10995, 11010), 10995, 'stop'),
    (Bar(10990, 11014, 10985, 11010), 10990, 'gap_stop'),
])
def test_stop_touch_and_gap_use_worse_price(bar, exit_ticks, reason):
    b = long_morning()
    b[510] = bar
    t = simulate_day(b)
    assert (t['exit_ticks'], t['exit_reason']) == (exit_ticks, reason)
    assert t['net'] == pytest.approx((exit_ticks - 11008) * 1.25 - 6.60)


def test_entry_bar_stop_active_and_no_reentry():
    b = long_morning()
    b[495] = Bar(11008, 11014, 10995, 11010)
    t = simulate_day(b)
    assert (t['exit_minute'], t['exit_reason'], t['net']) == (495, 'stop', -22.85)


def test_short_sign_and_gap_loss():
    b = morning()
    b[480] = Bar(11000, 11010, 10990, 10994)
    for m in range(495, 600, 15):
        b[m] = Bar(10992, 11000, 10980, 10990)
    b[600] = Bar(10988, 11030, 10970, 11000)
    t = simulate_day(b)
    assert (t['direction'], t['gross'], t['net']) == ('short', 5.0, -1.5999999999999996)
    b[510] = Bar(11010, 11015, 11000, 11010)
    t = simulate_day(b)
    assert (t['exit_reason'], t['net']) == ('gap_stop', -29.1)


def test_first_gap_signal_consumed_and_zero_range_and_no_signal():
    b = long_morning()
    b[495] = Bar(10995, 11010, 10990, 11008)
    assert simulate_day(b)['status'] == 'entry_gap_skip'
    assert simulate_day(morning())['status'] == 'no_signal'
    b = morning()
    for m in range(420, 480, 15):
        b[m] = Bar(11000, 11000, 11000, 11000)
    assert simulate_day(b)['status'] == 'zero_range'


def test_strict_break_and_last_0900_signal_but_none_after():
    b = morning()
    b[480] = Bar(11000, 11005, 10995, 11005)
    assert simulate_day(b)['status'] == 'no_signal'
    b[525] = Bar(11000, 11008, 10995, 11006)
    b[540] = Bar(11007, 11010, 11000, 11008)
    t = simulate_day(b)
    assert t['entry_minute'] == 540
    b = morning()
    b[540] = Bar(11000, 11008, 10995, 11006)
    assert simulate_day(b)['status'] == 'no_signal'


def test_missing_holding_or_exit_bar_excluded_not_forward_filled():
    for minute in (420, 495, 570, 600):
        b = long_morning()
        del b[minute]
        assert simulate_day(b)['status'] == 'incomplete'


def test_london_clock_tracks_dst_not_fixed_new_york_offset():
    for stamp, minute in [('2024-03-29T07:00:00+00:00', 420), ('2024-04-01T06:00:00+00:00', 420), ('2024-10-28T07:00:00+00:00', 420)]:
        epoch = int(datetime.fromisoformat(stamp).timestamp() * 1000)
        assert london_day_minute(epoch)[1] == minute


def test_reserved_or_out_of_sample_file_rejected_before_loading():
    validate_input_years([2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024])
    with pytest.raises(ValueError):
        validate_input_years([2016, 2025])


def test_block_uncertainty_resamples_flat_days_with_trade_count_denominator():
    pnl = np.array([0.0, 2.0] * 20)
    count = np.array([0, 1] * 20)
    assert bootstrap_ci(pnl, count, reps=100, seed=1) == [2.0, 2.0]


def test_summary_reconciles_costs_and_counts():
    days = [dict(date='2020-01-02', status='trade', direction='long', gross=10.0, net=3.4),
            dict(date='2020-01-03', status='trade', direction='short', gross=-5.0, net=-11.6),
            dict(date='2020-01-06', status='no_signal')]
    s = summarize(days, reps=100)
    assert s['trades'] == 2
    assert s['net_total'] == pytest.approx(-8.2)
    assert s['cost_total'] == 13.2
    assert s['net_mean'] == pytest.approx(-4.1)


def export_fixture(tmp_path):
    files = []
    for year in range(2016, 2025):
        epoch = int(datetime(year, 1, 4, 7, tzinfo=timezone.utc).timestamp() * 1000)
        signal = f'{epoch}|1.1000|1.1005|1.0995|1.1000|1|{epoch+900000}|2|M|M6E1!|futures|USD|EUR|0.0001|12500|America/Chicago|15'
        p = tmp_path / f'{year}.csv'
        with p.open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=['Type', 'Signal', 'Price USD'])
            writer.writeheader()
            writer.writerow({'Type': 'Entry long', 'Signal': signal, 'Price USD': '1.1000'})
        files.append({'name': p.name, 'year': year, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
    return {'scored_files': files}


def test_loader_rejects_tamper_before_price_decode(tmp_path):
    reg = export_fixture(tmp_path)
    days, audit = load_days(reg, tmp_path)
    assert audit['decoded_bars'] == 9
    assert max(days).year == 2024
    (tmp_path / '2016.csv').write_text('not a CSV', encoding='utf-8')
    with pytest.raises(ValueError, match='hash/path'):
        load_days(reg, tmp_path)


def test_loader_fails_reserved_timestamp_even_inside_renamed_allowed_file(tmp_path):
    reg = export_fixture(tmp_path)
    p = tmp_path / '2024.csv'
    old = int(datetime(2024, 1, 4, 7, tzinfo=timezone.utc).timestamp() * 1000)
    new = int(datetime(2025, 1, 4, 7, tzinfo=timezone.utc).timestamp() * 1000)
    p.write_text(p.read_text().replace(str(old), str(new)), encoding='utf-8')
    reg['scored_files'][-1]['sha256'] = hashlib.sha256(p.read_bytes()).hexdigest()
    with pytest.raises(ValueError, match='Unexpected year'):
        load_days(reg, tmp_path)
