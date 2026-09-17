from datetime import date, datetime, timedelta, timezone
from random import Random

import pytest

from c1_signal_daemon.feed import Bar
from c1_rail.qualification.model import SourceBar, SourceSession, SessionSchedule
from c1_rail.qualification.paths import PathAssembler


def source(day):
    ts = datetime(2024, 2, day, 15, tzinfo=timezone.utc)
    deadline = ts.replace(hour=21)
    bars = tuple(SourceBar(ts + timedelta(minutes=15*i),
                          (('aegis_6j', Bar(ts + timedelta(minutes=15*i), 1, 1, 1, 1)),)) for i in range(2))
    return SourceSession(str(day), ts.date(), bars,
                         SessionSchedule(deadline-timedelta(minutes=15), deadline-timedelta(minutes=5), deadline))


def test_repeated_reverse_blocks_keep_source_but_unique_contiguous_path_grid():
    a, b = source(9), source(8)
    result = PathAssembler(date(2030, 1, 4)).assemble(((a,), (a,), (b,)), horizon_sessions=3)
    assert [s.source for s in result] == [a, a, b]
    assert [s.path_session_date for s in result] == [date(2030, 1, 4), date(2030, 1, 7), date(2030, 1, 8)]
    times = [bar.path_time for s in result for bar in s.bars]
    assert all(b-a == timedelta(minutes=15) for a, b in zip(times, times[1:]))
    assert [s.occurrence for s in result] == [0, 1, 2]
    assert result[0].bars[0].bars is a.bars[0].bars
    assert all(s.block_start and s.block_end for s in result)


def test_inner_block_truncation_and_mixed_lengths_refused():
    a = source(9)
    with pytest.raises(ValueError, match='whole'):
        PathAssembler(date(2030, 1, 4)).assemble(((a, a),), horizon_sessions=1)
    with pytest.raises(ValueError):
        PathAssembler(date(2030, 1, 4)).assemble(((a,), (a, a)), horizon_sessions=3)


def test_sample_preserves_complete_block_edges_and_is_repeatable():
    a, b = source(9), source(8)
    assembler = PathAssembler(date(2030, 1, 4))
    result = assembler.sample(((a, b), (b, a)), Random(22), horizon_sessions=6)
    assert result == assembler.sample(((a, b), (b, a)), Random(22), horizon_sessions=6)
    assert [s.block_start for s in result] == [True, False] * 3
    assert [s.block_end for s in result] == [False, True] * 3
    with pytest.raises(ValueError, match='whole'):
        assembler.sample(((a, b),), Random(22), horizon_sessions=5)
