"""Explicit ledger and source-adjacency proofs for whole session blocks."""
from dataclasses import dataclass
from typing import Generic, TypeVar
from .model import EdgeState

T = TypeVar('T')


@dataclass(frozen=True)
class JointFlatBlocks(Generic[T]):
    sessions: tuple[T, ...]
    edges: tuple
    block_sessions: int
    adjacent: tuple[bool, ...]

    def __post_init__(self):
        if any(type(items) is not tuple for items in (self.sessions, self.edges, self.adjacent)):
            raise ValueError('immutable tuple inputs required')
        if any(not isinstance(edge, EdgeState) for edge in self.edges):
            raise ValueError('complete EdgeState ledger proofs required')
        if type(self.block_sessions) is not int or self.block_sessions <= 0:
            raise ValueError('block_sessions must be a positive integer')
        if len(self.edges) != len(self.sessions) + 1:
            raise ValueError('one ledger proof required at every session edge')
        if len(self.adjacent) != max(0, len(self.sessions) - 1) or any(type(x) is not bool for x in self.adjacent):
            raise ValueError('explicit source adjacency proof required for every join')

    def candidates(self) -> tuple[tuple[T, ...], ...]:
        n = self.block_sessions
        return tuple(self.sessions[i:i+n] for i in range(len(self.sessions)-n+1)
                     if self.edges[i].is_flat and self.edges[i+n].is_flat
                     and all(self.adjacent[i:i+n-1]))


def partition_populations(sessions: tuple[T, ...]) -> dict[str, tuple[T, ...]]:
    """Input is the already-covered chronological panel; depths are unrelated."""
    middle = (len(sessions) + 1) // 2
    return {'FULL': sessions, 'H1': sessions[:middle], 'H2': sessions[middle:]}
