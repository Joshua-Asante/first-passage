from types import SimpleNamespace

import pytest

from c1_rail.qualification.blocks import JointFlatBlocks, partition_populations
from c1_rail.qualification.model import EdgeState, LEG_IDS


def edge(nonflat=False):
    zero = tuple((leg, 0) for leg in LEG_IDS)
    working = tuple((leg, int(nonflat and i == 0)) for i, leg in enumerate(LEG_IDS))
    return EdgeState(zero, working, zero)


def test_working_order_or_reservation_edge_is_not_flat():
    sessions = tuple(range(6))
    edges = tuple(edge(i == 5) for i in range(7))
    blocks = JointFlatBlocks(sessions, edges, block_sessions=5, adjacent=(True,) * 5)
    assert blocks.candidates() == (sessions[1:6],)


def test_gap_does_not_silently_compress_source_adjacency():
    blocks = JointFlatBlocks(tuple(range(6)), (edge(),) * 7,
                             block_sessions=5, adjacent=(True, True, False, True, True))
    assert blocks.candidates() == ()


def test_no_short_blocks_and_proof_length_is_exact():
    edges = (edge(),) * 4
    assert JointFlatBlocks((0, 1, 2), edges, block_sessions=5, adjacent=(True, True)).candidates() == ()
    with pytest.raises(ValueError):
        JointFlatBlocks((0, 1, 2), edges[:-1], block_sessions=5, adjacent=(True, True))


def test_odd_population_partition_is_disjoint_and_complete():
    pools = partition_populations(tuple(range(5)))
    assert pools == {'FULL': (0, 1, 2, 3, 4), 'H1': (0, 1, 2), 'H2': (3, 4)}


def test_incomplete_ledger_cannot_claim_flatness():
    with pytest.raises(ValueError, match='EdgeState'):
        JointFlatBlocks((0,), (SimpleNamespace(is_flat=True),) * 2, block_sessions=1, adjacent=())


def test_reservation_without_position_excludes_block():
    zero = tuple((leg, 0) for leg in LEG_IDS)
    reserved = tuple((leg, int(i == 0)) for i, leg in enumerate(LEG_IDS))
    assert JointFlatBlocks((0,), (edge(), EdgeState(zero, zero, reserved)), block_sessions=1, adjacent=()).candidates() == ()
