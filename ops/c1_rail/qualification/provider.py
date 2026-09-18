"""Synthetic source-to-path integration. No loader or production authority."""
from random import Random
from types import MappingProxyType

from .blocks import JointFlatBlocks, partition_populations
from .paths import PathAssembler
from .runner import NeedsContext
from .model import ReplayResult
from .replay import ReplayDeadlineFailure


class _ReplayProvider:
    """Build pool-specific indices once, then rerun fresh continuous path state.

    Initial source proof is necessary but not sufficient: the replay checks the
    actual sampled block edges again under its own changing account/paper state.
    The supplied replay callable must construct fresh adapters for every call.
    """

    def __init__(self,sessions,adjacent,*,block_sessions,path_start_date,replay):
        if type(sessions) is not tuple or not sessions:
            raise ValueError('immutable chronological synthetic source required')
        dates=tuple(s.source_session_date for s in sessions)
        if len(set(s.session_id for s in sessions))!=len(sessions) or any(a>=b for a,b in zip(dates,dates[1:])):
            raise ValueError('unique ordered source identities required')
        if type(adjacent) is not tuple or len(adjacent)!=len(sessions)-1 or any(type(x) is not bool for x in adjacent):
            raise ValueError('explicit covered source adjacency required')
        self.populations=MappingProxyType(partition_populations(sessions))
        self.assembler=PathAssembler(path_start_date)
        self.replay=replay
        self.candidates={}
        middle=(len(sessions)+1)//2
        spans={'FULL':(0,len(sessions)),'H1':(0,middle),'H2':(middle,len(sessions))}
        for name,pool in self.populations.items():
            if not pool:
                raise NeedsContext('empty independent source population')
            proof_path=self.assembler.assemble(tuple((s,) for s in pool),horizon_sessions=len(pool))
            try:
                proof=replay(proof_path)
            except ReplayDeadlineFailure as exc:
                raise NeedsContext('source proof failed own-flat deadline') from exc
            self._match(proof_path,proof)
            if len(proof.sessions)!=len(pool) or any(not row.flat_before_deadline for row in proof.sessions):
                raise NeedsContext('source proof failed schedule or length')
            # Preserve both observed sides of every internal boundary. A mismatch
            # cannot be hidden by choosing one side of the ledger.
            if any(a.end_edge!=b.start_edge for a,b in zip(proof.sessions,proof.sessions[1:])):
                raise NeedsContext('source proof has discontinuous account edges')
            edges=(proof.sessions[0].start_edge,)+tuple(row.end_edge for row in proof.sessions)
            start,end=spans[name]
            builder=JointFlatBlocks(pool,edges,block_sessions,adjacent[start:end-1])
            candidates=builder.candidates()
            if not candidates:
                raise NeedsContext('no whole joint-flat blocks in independent population')
            self.candidates[name]=candidates
        self.candidates=MappingProxyType(self.candidates)

    @staticmethod
    def _match(path,result):
        if type(result) is not ReplayResult:
            raise ValueError('typed replay result required')
        if len(path)!=len(result.sessions):
            raise ValueError('replay result does not match path length')
        for expected,actual in zip(path,result.sessions):
            if (actual.occurrence,actual.path_session_date,actual.source_session_id)!=(
                    expected.occurrence,expected.path_session_date,expected.source.session_id):
                raise ValueError('replay did not consume designated source occurrences')

    def __call__(self,*,stage,population,path_index,seed,horizon_sessions):
        if stage not in ('probe','n1','n2','n3') or population not in self.candidates:
            raise ValueError('unknown stage or population')
        path=self.assembler.sample(self.candidates[population],Random(seed),horizon_sessions=horizon_sessions)
        try:
            result=self.replay(path)
        except ReplayDeadlineFailure as exc:
            result=exc.result
            if (type(result) is not ReplayResult or not 0<len(result.sessions)<=len(path)
                    or result.sessions[-1].flat_before_deadline
                    or any(not row.flat_before_deadline for row in result.sessions[:-1])):
                raise ValueError('deadline exception requires a terminal failed path prefix') from exc
            self._match(path[:len(result.sessions)],result)
            raise
        self._match(path,result)
        return result


class SyntheticReplayProvider(_ReplayProvider):
    """Explicit test surface; production construction belongs to its driver."""
    synthetic = True
