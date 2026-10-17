"""Solo producer and clock-envelope checks, exclusively synthetic trade lists/paths."""
import csv
from dataclasses import replace
from datetime import date, datetime
import hashlib
import importlib
import importlib.util
import json
from pathlib import Path
import subprocess
from zoneinfo import ZoneInfo

import numpy as np
import pytest

from discovery.remc_series_builder import TRADE_LIST_COLUMNS, Trade, InputIdentityError

NY = ZoneInfo('America/New_York')
TIERS = ('Bulenox_100K', 'Tradeify_Select_100K', 'MFFU_Rapid_100K', 'BluSky_Premium_100K')


def test_solo_producer_available():
    assert importlib.util.find_spec('discovery.orb_solo_series') is not None


@pytest.fixture
def api():
    return importlib.import_module('discovery.orb_solo_series')


def trade(n=1, *, day='2024-01-08', entry='10:00', exit='11:00', gross=-20., mae=-30., qty=1):
    return Trade('orb_mnq_v7', n, datetime.fromisoformat(f'{day}T{entry}').replace(tzinfo=NY),
                 datetime.fromisoformat(f'{day}T{exit}').replace(tzinfo=NY), qty,
                 gross-2., 2., mae)


def write_export(path, rows, *, kind='long'):
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=TRADE_LIST_COLUMNS)
        writer.writeheader()
        for t in rows:
            for label, ts in (('Entry', t.entry_ny), ('Exit', t.exit_ny)):
                row = dict.fromkeys(TRADE_LIST_COLUMNS, '0')
                row.update({'Trade number': t.trade_number, 'Type': f'{label} {kind}',
                            'Date and time': ts.strftime('%Y-%m-%d %H:%M'), 'Size (qty)': t.qty,
                            'Net PnL USD': t.net_usd, 'Commission USD': t.commission_usd,
                            'Adverse excursion USD': t.adverse_excursion_usd})
                writer.writerow(row)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def week():
    return [trade(), trade(2, day='2024-01-12', gross=40, mae=-5)]


def build(api, trades=None):
    return api.build_solo_series(week() if trades is None else trades,
                                 expected_quantity=1, tier_keys=TIERS)


def test_hash_mismatch_precedes_parsing(api, tmp_path):
    p = tmp_path/'bad.csv'
    p.write_text('not CSV')
    with pytest.raises(InputIdentityError):
        api.load_solo_export(p, '0'*64, export_tz='America/New_York',
                             expected_quantity=1, capture_commission_per_side=1.)


def test_hash_bound_export_and_source_costs(api, tmp_path):
    p = tmp_path/'synthetic.csv'
    pin = write_export(p, week())
    loaded = api.load_solo_export(p, pin, export_tz='America/New_York',
                                  expected_quantity=1, capture_commission_per_side=1.)
    assert loaded == week()
    with pytest.raises(ValueError, match='commission'):
        api.load_solo_export(p, pin, export_tz='America/New_York',
                             expected_quantity=1, capture_commission_per_side=.5)


def test_short_side_rejected(api, tmp_path):
    p = tmp_path/'short.csv'
    pin = write_export(p, week(), kind='short')
    with pytest.raises(ValueError, match='long'):
        api.load_solo_export(p, pin, export_tz='America/New_York',
                             expected_quantity=1, capture_commission_per_side=1.)


def test_duplicate_partial_and_unpaired_rows_rejected(api, tmp_path):
    p = tmp_path/'duplicate.csv'
    pin = write_export(p, [trade(), trade()])
    with pytest.raises(ValueError, match='more than one'):
        api.load_solo_export(p, pin, export_tz='America/New_York',
                             expected_quantity=1, capture_commission_per_side=1.)
    p2 = tmp_path/'partial.csv'
    pin2 = write_export(p2, [replace(trade(), qty=.5)])
    with pytest.raises(ValueError, match='quantity'):
        api.load_solo_export(p2, pin2, export_tz='America/New_York',
                             expected_quantity=1, capture_commission_per_side=1.)
    lines = p2.read_text().splitlines()
    p2.write_text('\n'.join(lines[:2])+'\n')
    pin3 = hashlib.sha256(p2.read_bytes()).hexdigest()
    with pytest.raises(ValueError, match='no exit'):
        api.load_solo_export(p2, pin3, export_tz='America/New_York',
                             expected_quantity=1, capture_commission_per_side=1.)


@pytest.mark.parametrize('entry_qty,exit_qty', [('2', '1'), ('', '1'), ('1', ''), ('.5', '1')])
def test_both_raw_rows_must_establish_the_complete_lot(api, tmp_path, entry_qty, exit_qty):
    p = tmp_path/'paired-quantity.csv'
    write_export(p, week())
    with p.open(newline='') as handle:
        rows = list(csv.DictReader(handle))
    rows[0]['Size (qty)'] = entry_qty
    rows[1]['Size (qty)'] = exit_qty
    with p.open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=TRADE_LIST_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    pin = hashlib.sha256(p.read_bytes()).hexdigest()
    with pytest.raises(ValueError, match='quantity'):
        api.load_solo_export(p, pin, export_tz='America/New_York',
                             expected_quantity=1, capture_commission_per_side=1.)


def test_calendar_is_actual_monday_to_friday_with_zero_days(api):
    b = build(api)
    assert b.dates == tuple(date(2024, 1, d) for d in range(8, 13))
    np.testing.assert_array_equal(b.tiers['Tradeify_Select_100K']['pnl'], [-21.82, 0, 0, 0, 38.18])
    np.testing.assert_array_equal(b.tiers['Tradeify_Select_100K']['low'], [-31.82, 0, 0, 0, -6.82])
    assert b.manifest['scored'] is False
    assert b.manifest['clock_kind'] == 'conservative_mae_envelope'


def test_complete_week_boundary_rule_does_not_relabel_or_pad(api):
    ts = [trade(1, day='2024-01-04'), trade(2, day='2024-01-09'),
          trade(3, day='2024-01-15')]
    b = build(api, ts)
    assert (b.dates[0], b.dates[-1]) == (date(2024, 1, 8), date(2024, 1, 12))
    assert b.manifest['boundary_excluded_trade_numbers'] == [1, 3]
    assert len(b.dates) == 5


def test_envelope_covers_overlap_and_previously_realized_losses(api):
    # At an actual sampled instant: one closed lot -20, two overlapping lots -30/-10;
    # full-day fee6: actual excursion -66, below-opening envelope is -95-6=-101.
    ts = [trade(1, gross=-20, mae=-25), trade(2, entry='10:30', exit='12:00', gross=50, mae=-40),
          trade(3, entry='10:45', exit='12:30', gross=10, mae=-30),
          trade(4, day='2024-01-12', gross=0, mae=0)]
    b = build(api, ts)
    low = b.tiers['Tradeify_Select_100K']['low'][0]
    assert low == pytest.approx(-95 - 6*.91)
    actual_marks = [-20, -30, -10]
    assert low <= sum(actual_marks)-6*.91


def test_every_admissible_mark_combination_above_envelope(api):
    # Enumerated independent hand-set paths include not-yet-open, open and closed lots.
    from itertools import product
    ts = [trade(1, gross=-20, mae=-25), trade(2, gross=50, mae=-40),
          trade(3, day='2024-01-12', gross=0, mae=0)]
    low = build(api, ts).tiers['Tradeify_Select_100K']['low'][0]
    for a, b, paid_cost in product((0, -25, -20), (0, -40, 50), (0, .91, 1.82, 3.64)):
        assert low <= a+b-paid_cost


def test_mae_that_misses_realized_loss_is_rejected_not_repaired(api):
    with pytest.raises(ValueError, match='realized gross loss'):
        build(api, [trade(gross=-100, mae=-10), week()[1]])


def test_even_a_small_uncovered_loss_is_not_waived(api):
    with pytest.raises(ValueError, match='realized gross loss'):
        build(api, [trade(gross=-1e-9, mae=0), week()[1]])


def test_export_ingestion_also_rejects_uncovered_loss(api, tmp_path):
    p = tmp_path/'uncovered.csv'
    pin = write_export(p, [trade(gross=-1e-9, mae=0), week()[1]])
    with pytest.raises(ValueError, match='realized gross loss'):
        api.load_solo_export(p, pin, export_tz='America/New_York', expected_quantity=1,
                             capture_commission_per_side=1.)


def test_dst_and_utc_timestamps_keep_the_actual_ny_session(api, tmp_path):
    from datetime import timezone
    ts = [trade(1, day='2024-03-08'), trade(2, day='2024-03-15')]
    utc = [replace(t, entry_ny=t.entry_ny.astimezone(timezone.utc),
                   exit_ny=t.exit_ny.astimezone(timezone.utc)) for t in ts]
    p = tmp_path/'utc.csv'
    pin = write_export(p, utc)
    loaded = api.load_solo_export(p, pin, export_tz='UTC', expected_quantity=1,
                                  capture_commission_per_side=1.)
    assert loaded == ts
    assert loaded[0].entry_ny.utcoffset().total_seconds() == -5*3600
    assert loaded[1].entry_ny.utcoffset().total_seconds() == -4*3600


def test_ambiguous_dst_and_wrong_cme_session_rejected(api, tmp_path):
    p = tmp_path/'ambiguous.csv'
    pin = write_export(p, [trade(day='2024-11-03', entry='01:30', exit='02:30')])
    with pytest.raises(ValueError, match='ambiguous'):
        api.load_solo_export(p, pin, export_tz='America/New_York', expected_quantity=1,
                             capture_commission_per_side=1.)
    pin = write_export(p, [replace(trade(), entry_ny=datetime(2024, 1, 7, 17, tzinfo=NY))])
    with pytest.raises(ValueError, match='different CME'):
        api.load_solo_export(p, pin, export_tz='America/New_York', expected_quantity=1,
                             capture_commission_per_side=1.)


@pytest.mark.parametrize('change,match', [
    ({'qty': 2}, 'quantity'), ({'commission_usd': -1}, 'commission'),
    ({'adverse_excursion_usd': float('nan')}, 'finite'),
    ({'net_usd': float('inf')}, 'finite'), ({'leg': 'foreign'}, 'leg'),
    ({'entry_ny': datetime(2024, 1, 8, 10)}, 'timezone'),
    ({'exit_ny': datetime(2024, 1, 8, 9, tzinfo=NY)}, 'chronology'),
    ({'entry_ny': datetime(2024, 1, 7, 18, tzinfo=NY)}, 'same NY'),
])
def test_invalid_trade_context_rejected(api, change, match):
    with pytest.raises(ValueError, match=match):
        build(api, [replace(trade(), **change), week()[1]])


def test_single_partial_week_and_duplicate_trade_rejected(api):
    with pytest.raises(ValueError, match='complete week'):
        build(api, [trade(day='2024-01-09')])
    with pytest.raises(ValueError, match='duplicate'):
        build(api, [trade(), trade(), week()[1]])


@pytest.mark.parametrize('exit,match', [('18:15', 'CME'), ('16:45', 'session close')])
def test_direct_builder_cannot_bypass_loader_session_rules(api, exit, match):
    with pytest.raises(ValueError, match=match):
        build(api, [trade(exit=exit), week()[1]])


def test_each_tier_cost_is_applied_once_and_signed_mae_supported(api):
    b = build(api, [trade(mae=30), week()[1]])
    for tier, cps in zip(TIERS, (.61, .91, .95, .95)):
        assert b.tiers[tier]['pnl'][0] == pytest.approx(-20-2*cps)
        assert b.tiers[tier]['low'][0] == pytest.approx(-30-2*cps)


def test_existing_block_consumer_gets_correct_real_weekdays(api):
    from discovery.prop_survivor_scoring import paired_blocks_from_daily
    b = build(api)
    pnl = b.tiers['Tradeify_Select_100K']['pnl']
    low = b.tiers['Tradeify_Select_100K']['low']
    blocks, lows = paired_blocks_from_daily(pnl, low)
    np.testing.assert_array_equal(blocks[0, :, 0], pnl)
    np.testing.assert_array_equal(lows[0, :, 0], low)


def test_no_unknown_or_duplicate_tier(api):
    with pytest.raises(ValueError, match='tier'):
        api.build_solo_series(week(), expected_quantity=1, tier_keys=('FXIFY',))
    with pytest.raises(ValueError, match='duplicate'):
        api.build_solo_series(week(), expected_quantity=1, tier_keys=(TIERS[0], TIERS[0]))


def test_produced_envelope_reaches_engine_barrier_not_only_close(api):
    from mc.simulation import simulate_path
    b = build(api, [trade(gross=5, mae=-40), trade(2, day='2024-01-12', gross=0, mae=0)])
    channel = b.tiers['Tradeify_Select_100K']
    path = channel['pnl'][:, None]
    kwargs = dict(dd_trigger=1., dd_scale=1., horizon=5, starting_equity=100.,
                  daily_loss_pct=None, profit_target=106., min_trading_days=0,
                  inactivity_limit=1501, dd_type='trailing_locking', trailing_dd_pct=-.3,
                  dd_lock_offset_usd=1000000., consistency_frac=None)
    assert simulate_path(path, **kwargs)[0] == 'horizon_cap'
    assert simulate_path(path, intraday_low=channel['low'], **kwargs)[:2] == ('bust_trailing', 1)


def test_output_custody_manifest_hashes_and_no_overwrite(api, tmp_path):
    root = tmp_path/'repo'
    root.mkdir()
    subprocess.run(['git', 'init', str(root)], check=True, capture_output=True)
    (root/'.gitignore').write_text('.cache/\n')
    b = build(api)
    out = root/'.cache/orb-mnq-v7-s4-2026-10/synthetic'
    manifest = api.write_solo_bundle(b, out, repo_root=root,
                                     input_sha256='1'*64, configuration_sha256='2'*64)
    data = json.loads(manifest.read_text())
    assert data['configuration_sha256'] == '2'*64
    assert data['scored'] is False
    for name, pin in data['series_files'].items():
        assert hashlib.sha256((out/name).read_bytes()).hexdigest() == pin
    with pytest.raises(FileExistsError):
        api.write_solo_bundle(b, out, repo_root=root,
                              input_sha256='1'*64, configuration_sha256='2'*64)
    with pytest.raises(ValueError, match='custody'):
        api.write_solo_bundle(b, tmp_path/'elsewhere', repo_root=root,
                              input_sha256='1'*64, configuration_sha256='2'*64)
    with pytest.raises(ValueError, match='digest'):
        api.write_solo_bundle(b, out/'bad', repo_root=root,
                              input_sha256='', configuration_sha256='2'*64)
