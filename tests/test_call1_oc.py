"""T4 Call-1 OC — synthetic PF paths. No lifecycle_state.json write."""

import numpy as np

from discovery.lifecycle_call1.oc import oc_from_pf_paths
from lifecycle import decay_breach


def test_known_decay_trips_decay_breach():
    assert decay_breach(rolling_pf=2.4, baseline_pf=3.0, pf_sigma=0.5) is True


def test_flat_series_does_not_trip_at_k1():
    paths = [np.full(20, 3.0) for _ in range(40)]
    oc = oc_from_pf_paths(paths, baseline_pf=3.0, pf_sigma=0.5, k_sigma=1.0)
    assert oc["false_kill_rate"] == 0.0
    assert oc["wrote_lifecycle_state"] is False


def test_decay_paths_detect_with_finite_lag():
    # Drop below floor 2.5 from window 3 onward.
    paths = [np.array([3.0, 3.0, 3.0, 2.2, 2.1, 2.0]) for _ in range(10)]
    oc = oc_from_pf_paths(paths, baseline_pf=3.0, pf_sigma=0.5, k_sigma=1.0, persist=2)
    assert oc["false_kill_rate"] == 1.0
    assert oc["mean_detection_lag"] == 5.0  # second consecutive breach at index 4
    assert oc["wrote_lifecycle_state"] is False
