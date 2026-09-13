"""One durable dispatch boundary. The broker owns execution, the kernel owns outcomes."""
from .broker import Outcome


def dispatch(kernel, effect):
    """Execute planned work once; a crash after the boundary leaves an unknown attempt."""
    if effect.status != "planned":
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
