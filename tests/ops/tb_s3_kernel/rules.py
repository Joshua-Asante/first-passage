"""Shared evidence and protection predicates; no transport or listener mutation."""


def covers(ev, at, boundary, now):
    """Rev 5.6 freshness plus acquisition after the exact command/dispatch boundary."""
    from .broker import BAR  # avoid a broker/state import cycle
    return (ev.order_level and ev.request_fence and ev.acquired > boundary and ev.as_of > at
            and ev.as_of <= now and now - ev.as_of <= BAR)


def protection_consumed(ev, fill_id):
    """A protection owner is consumed independently of FIFO accounting quantity."""
    return (ev.order_level and ev.protection_owners.get(fill_id, {}).get("consumed") is True
            and not any(w.get("attached_to") == fill_id for w in ev.working))


def scope_quiescent(ev, scope_kind, scope_id, pending):
    """No position, executable order, or unreconciled future exposure in scope."""
    if not ev.order_level:
        return False
    if scope_kind == "fill":
        entries = [o for o in pending.values() if scope_id in o.lot_ids]
        lots = {scope_id} | {i for o in entries for i in o.lot_ids}
        return (all(ev.lots.get(i) == 0 for i in lots)
                and all(ev.protection_owners.get(i, {}).get("qty") == 0 for i in lots)
                and not any(w.get("attached_to") in lots for w in ev.working)
                and not any(any(w["ref"] == o.ref for o in entries) for w in ev.working)
                and all(o.status in ("filled", "cancelled", "rejected", "not_sent")
                        for o in entries))
    if ev.position != 0 or ev.working or any(qty != 0 for qty in ev.lots.values()):
        return False
    return not any(o.sym == ev.sym and o.status not in
                   ("filled", "cancelled", "rejected", "not_sent") for o in pending.values())


def matches(order, fields):
    """Every static field matches, including None; a trail anchor is dynamic."""
    return all(order.get(k) == v for k, v in fields.items())


def valid_component(order, component, fields, fill_id, qty, side):
    """Protection includes linkage, direction, type and the entire residual quantity."""
    if component == "trail" and (order.get("trail_activation") is None
                                 or order.get("trail_offset") is None):
        return False
    return (order.get("kind") == component and order.get("type") == component
            and order.get("attached_to") == fill_id and order.get("qty") == qty
            and order.get("side") == ("sell" if side == "buy" else "buy")
            and matches(order, fields))
