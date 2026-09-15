"""Synthetic state regressions; direct provider observations are retained privately."""
from datetime import datetime, timezone

import pytest

from c1_signal_daemon.book_adapters import load_port, port_available
from c1_signal_daemon.pine_ta import tv_daily_key


def test_daily_key_keeps_observed_january_2025_reset():
    before = datetime(2025, 1, 9, 21, 45, tzinfo=timezone.utc)
    after = datetime(2025, 1, 9, 23, 0, tzinfo=timezone.utc)
    assert tv_daily_key(before) != tv_daily_key(after)


def test_daily_key_retains_observed_holiday_merge():
    before = datetime(2022, 9, 5, 16, 45, tzinfo=timezone.utc)
    after = datetime(2022, 9, 5, 22, 0, tzinfo=timezone.utc)
    assert tv_daily_key(before) == tv_daily_key(after)


@pytest.mark.parametrize('before,after', [
    ('2023-04-07T13:15:00+00:00', '2023-04-09T22:00:00+00:00'),
    ('2026-04-03T13:15:00+00:00', '2026-04-05T22:00:00+00:00'),
])
def test_daily_key_keeps_observed_sunday_reopen(before, after):
    assert tv_daily_key(datetime.fromisoformat(before)) != tv_daily_key(datetime.fromisoformat(after))


def test_striker_does_not_reset_on_merged_provider_day():
    leg = 'dj30_mym_p250'
    if not port_available(leg):
        pytest.skip('private Striker adapter absent')
    from c1_signal_daemon.feed import Bar
    adapter = load_port(leg).build(force_flat=False)
    def bar(hour, minute):
        return Bar(ts=datetime(2022, 9, 5, hour, minute, tzinfo=timezone.utc),
                   open=100.0, high=101.0, low=99.0, close=100.0, volume=10.0)
    adapter.on_bar(bar(16, 45))
    adapter.daily_trade_count = 1
    adapter.on_bar(bar(22, 0))
    assert adapter.daily_trade_count == 1


def test_striker_open_entry_fees_reduce_equity_at_loss_boundary():
    leg = 'dj30_mym_p250'
    if not port_available(leg):
        pytest.skip('private Striker adapter absent')
    module = load_port(leg)
    adapter = module.build(max_total_dd_pct=0.0015, force_flat=False)
    # One flat-price synthetic lot: its paid entry commission is already a loss.
    adapter._lots = {'synthetic': (1, 100.0, 2.0)}
    adapter.realized_net = 0.0
    assert adapter._equity(100.0) == adapter.params.initial_capital - 2.0
    from c1_signal_daemon.feed import Bar
    actions = adapter.on_bar(Bar(ts=datetime(2024, 2, 6, 15, tzinfo=timezone.utc),
                                open=100.0, high=100.0, low=100.0, close=100.0, volume=1.0))
    assert any(getattr(action, 'reason', None) == 'DD Limit' for action in actions)


def test_striker_partial_close_preserves_unspent_entry_fee_allocation():
    leg = 'dj30_mym_p250'
    if not port_available(leg):
        pytest.skip('private Striker adapter absent')
    from c1_signal_daemon.book_protocol import ExecutionEvent, Fill, Side
    adapter = load_port(leg).build()
    now = datetime(2024, 2, 6, 15, tzinfo=timezone.utc)
    entry = Fill('entry', 'order', leg, 'entry', Side.BUY, 2, 100.0, now, commission=4.0)
    adapter.on_execution(ExecutionEvent('fill', leg, now, fill=entry))
    partial = Fill('partial', 'close', leg, 'exit', Side.SELL, 1, 100.0, now,
                   entry_fill_id='entry', commission=2.0)
    adapter.on_execution(ExecutionEvent('fill', leg, now, fill=partial))
    assert adapter._position() == 1
    assert adapter.realized_net == -4.0
    assert adapter._equity(100.0) == adapter.params.initial_capital - 6.0
