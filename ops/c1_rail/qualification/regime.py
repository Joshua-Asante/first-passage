"""Source-panel resampling and deterministic isolated RNG domain identities."""
from calendar import monthrange
from datetime import date
import hashlib
import json

from .blocks import JointFlatBlocks


def domain_seed(*, root: str, stage: str, population: str, panel_index: int | None,
                path_index: int, synthetic: bool = True, purpose: str = 'path') -> int:
    if not root or stage not in ('n1', 'n2', 'n3', 'probe') or population not in ('FULL', 'H1', 'H2'):
        raise ValueError('explicit root, stage and population domain required')
    if type(path_index) is not int or path_index < 0 or (panel_index is not None and (type(panel_index) is not int or panel_index < 0)):
        raise ValueError('nonnegative integer stream indices required')
    if type(synthetic) is not bool:
        raise ValueError('synthetic discriminator must be boolean')
    if purpose not in ('path', 'outer', 'probe'):
        raise ValueError('unknown RNG purpose')
    if purpose == 'outer' and (stage != 'n2' or population != 'FULL' or panel_index is None):
        raise ValueError('outer panels require n2 FULL and explicit panel index')
    payload = ['tb-s2-rng-v2', purpose, 'synthetic' if synthetic else 'qualification', root,
               stage, population, panel_index, path_index]
    return int.from_bytes(hashlib.sha256(json.dumps(payload, separators=(',', ':')).encode()).digest()[:8], 'big')


def _add_months(day: date, months: int) -> date:
    year, month0 = divmod(day.year * 12 + day.month - 1 + months, 12)
    return date(year, month0 + 1, min(day.day, monthrange(year, month0 + 1)[1]))


def outer_ranges(sessions: tuple, *, months: int, adjacent: tuple[bool, ...],
                 covered_until: date | None = None, tail_covered: bool = False) -> tuple[tuple, ...]:
    """Half-open calendar ranges; only ranges fully inside attested coverage.

    Without an explicit coverage end, the last source date is the conservative
    exclusive boundary. A calendar or missing session cannot be invented here.
    """
    if type(months) is not int or months <= 0 or not sessions:
        raise ValueError('positive months and nonempty source required')
    if type(tail_covered) is not bool or (tail_covered and covered_until is None):
        raise ValueError('tail coverage requires explicit exclusive coverage end')
    if type(adjacent) is not tuple or len(adjacent) != len(sessions) - 1 or any(type(x) is not bool for x in adjacent):
        raise ValueError('explicit coverage adjacency required at every source join')
    dates = tuple(s.source_session_date for s in sessions)
    if any(a >= b for a, b in zip(dates, dates[1:])):
        raise ValueError('outer source must have strictly increasing source dates')
    end = dates[-1] if covered_until is None else covered_until
    if end < dates[-1]:
        raise ValueError('coverage ends before source panel')
    result = []
    for i, start in enumerate(dates):
        stop = _add_months(start, months)
        if stop <= end:
            j = i
            while j < len(dates) and dates[j] < stop:
                j += 1
            # The last included -> first excluded join proves no omitted
            # session immediately before the half-open calendar boundary.
            # Without a following source observation, require explicit tail
            # coverage through the supplied end, never infer it from dates.
            boundary_proven = adjacent[j-1] if j < len(dates) else tail_covered
            if all(adjacent[i:j-1]) and boundary_proven:
                result.append(sessions[i:j])
    return tuple(result)


def sample_outer_panel(sessions: tuple, rng, *, months: int, adjacent: tuple[bool, ...],
                       covered_until: date | None = None, tail_covered: bool = False) -> tuple:
    candidates = outer_ranges(sessions, months=months, adjacent=adjacent,
                              covered_until=covered_until, tail_covered=tail_covered)
    if not candidates:
        raise ValueError('no fully covered calendar outer block')
    panel = []
    while len(panel) < len(sessions):
        selected = rng.choice(candidates)
        panel.extend(selected[:len(sessions) - len(panel)])
    return tuple(panel)


def rebuild_inner_blocks(panel: tuple, proof_provider, *, block_sessions: int) -> JointFlatBlocks:
    """Provider must continuously prove THIS occurrence panel, never old ids."""
    edges, adjacent = proof_provider(panel)
    return JointFlatBlocks(panel, tuple(edges), block_sessions, tuple(adjacent))
