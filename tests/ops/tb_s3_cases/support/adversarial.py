"""Explicit malformed broker facts for consumer quarantine/recovery tests.

These events deliberately bypass normal route validation. They are not claimed
producer capabilities and never supply the consumer's expected outcome.
"""
from tests.ops.tb_s3_kernel.broker import Execution, Lot


def inject_unlinked_execution(route, ref):
    """An invalid/unlinked order really executed; preserve its actual immutable identity."""
    order = route.orders[ref]
    qty = order.qty - order.filled_qty
    assert qty > 0
    execution_id = route.clock.tick()
    fill_id = f"{ref}#injected:{execution_id}"
    order.filled_qty += qty
    order.status = "filled"
    route.positions[order.sym] = route.positions.get(order.sym, 0) + (
        qty if order.side == "buy" else -qty)
    route.lots[fill_id] = Lot(fill_id, order.sym, order.leg_id, order.side, qty, ref)
    route.executions.append(Execution(execution_id, ref, fill_id, order.sym, order.leg_id,
                                      order.kind, order.side, qty, order.qty, order.order_type,
                                      order.price, order.attached_to))
    return fill_id
