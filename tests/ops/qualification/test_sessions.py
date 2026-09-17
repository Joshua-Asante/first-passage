from datetime import date,timedelta
import pytest
from c1_rail.qualification.model import LEG_IDS,EdgeState,SessionRecord
from c1_rail.qualification.sessions import WeekClock,session_arrays


def rows():
    zero=tuple((leg,0) for leg in LEG_IDS);edge=EdgeState(zero,zero,zero)
    return tuple(SessionRecord(i,date(2020,1,6)+timedelta(days=(i//5)*7+i%5),str(i),0.,0.,int(i==0),True,edge,edge) for i in range(10))


def test_idle_week_is_descriptive_not_failure():
    assert WeekClock().count_idle(rows()) == 1
    pnl,low=session_arrays(rows())
    assert pnl.shape==(10,1) and low.shape==(10,)


def test_duplicate_or_gapped_path_session_refused():
    records=rows()
    with pytest.raises(ValueError):
        session_arrays((records[0],records[0]))
    with pytest.raises(ValueError):
        session_arrays((records[0],records[2]))
