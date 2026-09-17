"""Pure mapping of whole sampled blocks; no adapter is reset at a splice."""
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone

from .model import ET, PathBar, PathSession, positive_int


@dataclass(frozen=True)
class PathAssembler:
    start_date: date

    def __post_init__(self):
        if type(self.start_date) is not date or self.start_date.weekday() >= 5:
            raise ValueError('explicit weekday path start required')

    def assemble(self, blocks: tuple, *, horizon_sessions: int) -> tuple[PathSession, ...]:
        """Map already-selected blocks, refusing implicit shortening or redrawing.

        Path dates are an independent Mon-Fri account/week clock. Path bar
        timestamps form a contiguous grid and deliberately do not encode source
        calendar dates or the account session dates.
        """
        positive_int(horizon_sessions, 'horizon_sessions')
        if not blocks or not blocks[0] or any(len(b) != len(blocks[0]) for b in blocks):
            raise ValueError('nonempty equal-length whole blocks required')
        if sum(map(len, blocks)) != horizon_sessions:
            raise ValueError('horizon must contain exactly whole blocks')
        path_time = datetime.combine(self.start_date, time(), timezone.utc)
        path_date = self.start_date
        result = []
        for block in blocks:
            for index, source in enumerate(block):
                bars = []
                for original in source.bars:
                    bars.append(PathBar(path_time, original.source_bar_time, source.source_session_date,
                                        original.source_bar_time.astimezone(ET), original.bars))
                    path_time += timedelta(minutes=15)
                result.append(PathSession(len(result), path_date, source, tuple(bars), index == 0, index == len(block)-1))
                path_date += timedelta(days=1)
                while path_date.weekday() >= 5:
                    path_date += timedelta(days=1)
        return tuple(result)

    def sample(self, candidates: tuple, rng, *, horizon_sessions: int) -> tuple[PathSession, ...]:
        positive_int(horizon_sessions, 'horizon_sessions')
        if not candidates or not candidates[0] or any(len(b) != len(candidates[0]) for b in candidates):
            raise ValueError('nonempty equal-length candidates required')
        if horizon_sessions % len(candidates[0]):
            raise ValueError('horizon must contain whole blocks')
        blocks = tuple(rng.choice(candidates) for _ in range(horizon_sessions // len(candidates[0])))
        return self.assemble(blocks, horizon_sessions=horizon_sessions)
