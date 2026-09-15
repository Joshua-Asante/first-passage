"""Synthetic state regressions; direct provider observations are retained privately.

The Striker cases run only against the reviewed corrected candidate port (Step 3
acceptance, ``corrected-ports/`` generation, digest below). With ``FP_PORT_ROOT``
unset the loader resolves the preserved original port, which lacks the reset and
fee corrections; running the regressions against it would fail for the wrong
reason, so they skip with the digest they expect instead.
"""
from datetime import datetime, timezone

import pytest

from c1_signal_daemon.book_adapters import load_port, port_available, port_sha256
from c1_signal_daemon.pine_ta import tv_daily_key

STRIKER = 'dj30_mym_p250'
CORRECTED_STRIKER_SHA256 = 'efd479b6b4c7eeaa7d8df3f40f36593f87d96b9d5f512dc79c4dd9b0520211f4'


def corrected_striker():
    """Load the reviewed corrected Striker candidate or skip; never the original port."""
    if not port_available(STRIKER):
        pytest.skip('private Striker adapter absent')
    actual = port_sha256(STRIKER)
    if actual != CORRECTED_STRIKER_SHA256:
        pytest.skip(f'loaded Striker port {actual[:12]} is not the reviewed corrected candidate '
                    f'{CORRECTED_STRIKER_SHA256[:12]}; point FP_PORT_ROOT at the corrected-ports generation')
    return load_port(STRIKER)


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
    from c1_signal_daemon.feed import Bar
    adapter = corrected_striker().build(force_flat=False)
    def bar(hour, minute):
        return Bar(ts=datetime(2022, 9, 5, hour, minute, tzinfo=timezone.utc),
                   open=100.0, high=101.0, low=99.0, close=100.0, volume=10.0)
    adapter.on_bar(bar(16, 45))
    adapter.daily_trade_count = 1
    adapter.on_bar(bar(22, 0))
    assert adapter.daily_trade_count == 1


def test_striker_open_entry_fees_reduce_equity_at_loss_boundary():
    module = corrected_striker()
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
    from c1_signal_daemon.book_protocol import ExecutionEvent, Fill, Side
    leg = STRIKER
    adapter = corrected_striker().build()
    now = datetime(2024, 2, 6, 15, tzinfo=timezone.utc)
    entry = Fill('entry', 'order', leg, 'entry', Side.BUY, 2, 100.0, now, commission=4.0)
    adapter.on_execution(ExecutionEvent('fill', leg, now, fill=entry))
    partial = Fill('partial', 'close', leg, 'exit', Side.SELL, 1, 100.0, now,
                   entry_fill_id='entry', commission=2.0)
    adapter.on_execution(ExecutionEvent('fill', leg, now, fill=partial))
    assert adapter._position() == 1
    assert adapter.realized_net == -4.0
    assert adapter._equity(100.0) == adapter.params.initial_capital - 6.0
