from c1_rail.qualification.benchmark import benchmark


def test_representative_synthetic_workload_is_deterministic():
    one=benchmark(horizon_sessions=5,seed=791946211)
    two=benchmark(horizon_sessions=5,seed=791946211)
    assert one['equivalence_sha256']==two['equivalence_sha256']
    assert one['sessions']==5 and one['adapter_bars']==1840
    assert one['fills']>=40 and one['synthetic'] is True
