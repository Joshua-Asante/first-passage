import pytest

from c1_rail.qualification.benchmark_part_a import benchmark_part_a


def test_representative_part_a_small_horizon_measures_real_panel_pipeline():
    output = benchmark_part_a(horizon_sessions=5, seed=771)
    assert output['synthetic'] is True and output['processes'] == 1
    assert output['source_sessions'] >= 150
    assert output['proof_sessions'] == output['source_sessions']
    assert output['path_sessions'] == 5
    assert output['inner_candidates'] > 0
    assert output['path_bars'] == 5 * 92
    assert output['serialized_bytes'] > 0
    assert len(output['equivalence_sha256']) == 64
    assert set(output['timings']) == {'source_build', 'outer_selection', 'proof_rebuild', 'path_replay_kernel', 'serialization', 'total'}
    assert all(value >= 0 for value in output['timings'].values())
    assert 'verdict' not in output and 'outcomes' not in output


def test_benchmark_requires_whole_inner_horizon_and_long_source():
    with pytest.raises(ValueError):
        benchmark_part_a(horizon_sessions=4, seed=1)
    with pytest.raises(ValueError):
        benchmark_part_a(horizon_sessions=5, seed=1, source_months=6)
