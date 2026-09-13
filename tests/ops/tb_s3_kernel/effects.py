"""One durable dispatch boundary. The broker owns execution, the kernel owns outcomes."""
from functools import wraps

from .broker import Outcome


def planned_command(method=None, *, drain=True):
    """Commit a complete command before dispatch; nested planning cannot publish a prefix."""
    if method is None:
        return lambda func: planned_command(func, drain=drain)
    @wraps(method)
    def run(kernel, *args, **kwargs):
        kernel._plan_depth += 1  # pylint: disable=protected-access
        try:
            result = method(kernel, *args, **kwargs)
        finally:
            kernel._plan_depth -= 1  # pylint: disable=protected-access
        # An interrupted planning phase publishes nothing. After the one atomic write,
        # a crash can recover every owner and effect using the normal dispatch journal.
        if not kernel._plan_depth:  # pylint: disable=protected-access
            kernel.persist()
            if drain:
                kernel._drain_effects()  # pylint: disable=protected-access
        return result
    return run


def dispatch(kernel, effect):
    """Execute planned work once; a crash after the boundary leaves an unknown attempt."""
    if effect.status != "planned":
        return
    op = kernel.operations.get(effect.owner)
    if op and op.status == "complete":
        effect.status = "cancelled"
        if effect.kind == "modify":
            op.components[effect.payload["component"]].status = "cancelled"
        kernel.persist()
        return
    kernel.persist()
    if kernel.effect_hook:
        kernel.effect_hook("planned", effect)
    effect.status = "dispatching"
    effect.boundary = kernel.clock.tick()
    effect.sent_at = kernel.clock.now
    kernel._mark_dispatch(effect)  # pylint: disable=protected-access
    kernel.persist()
    if kernel.effect_hook:
        kernel.effect_hook("dispatching", effect)
    payload = dict(effect.payload)
    payload.pop("component", None)
    if effect.kind == "disarm":
        outcome = Outcome("accepted")
    else:
        outcome = kernel.broker.request(effect.kind, effect.effect_id, **payload)
    if kernel.effect_hook:
        kernel.effect_hook("executed", effect)
    kernel._effect_outcome(effect, outcome)  # pylint: disable=protected-access
    kernel.persist()
    if kernel.effect_hook:
        kernel.effect_hook("recorded", effect)
