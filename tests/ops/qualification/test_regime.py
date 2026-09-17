from datetime import date
from random import Random
from types import SimpleNamespace

import pytest

from c1_rail.qualification.regime import domain_seed, outer_ranges, sample_outer_panel, rebuild_inner_blocks
from c1_rail.qualification.model import EdgeState, LEG_IDS


def monthly():
    return tuple(SimpleNamespace(source_session_date=date(2024, m, 1), session_id=str(m)) for m in range(1, 13))


def test_six_calendar_month_ranges_are_complete_not_six_sessions():
    ranges = outer_ranges(monthly(), months=6, adjacent=(True,) * 11)
    assert [s.session_id for s in ranges[0]] == ['1', '2', '3', '4', '5', '6']
    assert [s.session_id for s in ranges[-1]] == ['6', '7', '8', '9', '10', '11']


def test_outer_replacement_truncates_only_final_range_to_exact_length():
    panel = sample_outer_panel(monthly(), Random(23), months=6, adjacent=(True,) * 11)
    assert len(panel) == 12
    source = monthly()
    panel = sample_outer_panel(source, Random(23), months=6, adjacent=(True,) * 11)
    assert all(any(s is original for original in source) for s in panel)


def test_every_alternate_panel_rebuild_calls_its_own_proof_provider():
    panels = [monthly(), monthly()[::-1]]
    seen = []
    def prove(panel):
        seen.append(panel)
        zero = tuple((leg, 0) for leg in LEG_IDS)
        return ((EdgeState(zero, zero, zero),) * (len(panel) + 1), (True,) * (len(panel) - 1))
    results = [rebuild_inner_blocks(p, prove, block_sessions=5) for p in panels]
    assert seen == panels
    assert results[0].candidates()[0] != results[1].candidates()[0]


def test_seed_domains_isolate_stage_population_panel_path_and_synthetic():
    common = dict(root='root', stage='n2', population='FULL', panel_index=None, path_index=0)
    base = domain_seed(**common)
    variants = [dict(stage='n3'), dict(population='H1'), dict(panel_index=0), dict(path_index=1), dict(synthetic=False)]
    assert len({base, *(domain_seed(**(common | v)) for v in variants)}) == 6
    assert base == domain_seed(**common)
    with pytest.raises(ValueError):
        domain_seed(**(common | {'path_index': -1}))


def test_calendar_month_end_clips_day_and_refuses_incomplete_outer_range():
    sessions = tuple(SimpleNamespace(source_session_date=d, session_id=str(d)) for d in
                     (date(2024, 8, 31), date(2024, 9, 30), date(2025, 1, 31), date(2025, 2, 27), date(2025, 2, 28)))
    ranges = outer_ranges(sessions, months=6, adjacent=(True,) * 4, covered_until=date(2025, 2, 28))
    assert ranges == (sessions[:-1],)
    assert outer_ranges(sessions[:-1], months=6, adjacent=(True,) * 3) == ()


def test_outer_final_truncation_and_expansion_preserve_prior_panels():
    source = monthly() + (SimpleNamespace(source_session_date=date(2025, 1, 1), session_id='13'),)
    def panels(count):
        return tuple(sample_outer_panel(source, Random(domain_seed(root='test', stage='n2', population='FULL',
                                                                  panel_index=i, path_index=0, purpose='outer')), months=6, adjacent=(True,) * 12)
                     for i in range(count))
    initial = panels(100)
    expanded = panels(200)
    assert expanded[:100] == initial
    assert all(len(panel) == 13 for panel in expanded)


def test_outer_and_inner_seed_domains_never_share_first_path_address():
    common = dict(root='test', stage='n2', population='FULL', panel_index=0, path_index=0)
    assert domain_seed(**common, purpose='outer') != domain_seed(**common, purpose='path')
    assert len({domain_seed(**common, purpose=purpose) for purpose in ('outer', 'path', 'probe')}) == 3
    for invalid in ({'stage': 'n3'}, {'panel_index': None}, {'population': 'H1'}):
        with pytest.raises(ValueError):
            domain_seed(**(common | invalid), purpose='outer')


def test_outer_ranges_cannot_bridge_a_coverage_exclusion():
    source = monthly()
    adjacent = (True, True, False) + (True,) * 8
    ranges = outer_ranges(source, months=6, adjacent=adjacent)
    assert ranges == (source[3:9], source[4:10], source[5:11])
    with pytest.raises(ValueError):
        outer_ranges(source, months=6, adjacent=(True,))
    with pytest.raises(ValueError):
        sample_outer_panel(source, Random(1), months=6, adjacent=(False,) * 11)


def test_outer_right_boundary_does_not_hide_excluded_tail_session():
    source = tuple(SimpleNamespace(source_session_date=d, session_id=str(d)) for d in
                   (date(2024, 1, 2), date(2024, 1, 3), date(2024, 6, 28), date(2024, 7, 2)))
    assert outer_ranges(source, months=6, adjacent=(True, True, False)) == ()


def test_outer_end_after_last_source_requires_explicit_tail_coverage():
    source = tuple(SimpleNamespace(source_session_date=d, session_id=str(d)) for d in
                   (date(2024, 1, 2), date(2024, 6, 28)))
    args = dict(months=6, adjacent=(True,), covered_until=date(2024, 7, 2))
    assert outer_ranges(source, **args) == ()
    assert outer_ranges(source, **args, tail_covered=True) == (source,)
