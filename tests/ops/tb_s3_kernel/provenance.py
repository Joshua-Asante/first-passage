"""Evidence-side order identity checks against the durable, originally authorized send."""
from .broker import Evidence, Execution


def order_matches(facts: dict, authority: dict) -> bool:
    """A familiar reference alone cannot authorize different broker risk fields."""
    fields = {k: authority[k] for k in ("ref", "sym", "leg_id", "kind", "side", "qty")}
    fields.update(type=authority["order_type"], price=authority.get("price"), attached_to=None)
    return all(k in facts and facts[k] == value for k, value in fields.items())


def entry_evidence_matches(ev: Evidence, authority: dict, seen: dict[int, Execution],
                           reserved: int, sent_seq: int, history_acquired: int) -> bool:
    """Full immutable history and per-order capacity must agree before crediting any fill."""
    ref = authority["ref"]
    if ev.order_symbols is None or ev.order_symbols.get(ref, ev.sym) != authority["sym"]:
        return False
    facts = ev.order_facts.get(ref)
    status = ev.order_status.get(ref)
    executions = [e for e in ev.executions if e.ref == ref]
    indexed = {e.execution_id: e for e in executions}
    filled = ev.fills.get(ref, 0)
    if (len(indexed) != len(executions) or any(indexed.get(i) != e for i, e in seen.items())
            or sum(e.qty for e in executions) != filled
            or sum(e.qty for e in executions if e.execution_id not in seen) > reserved):
        return False
    if (facts is not None or status is not None or executions) and sent_seq == 0:
        return False
    if facts is not None:
        if (not order_matches(facts, authority) or facts.get("filled_qty") != filled
                or not 0 <= filled <= authority["qty"]
                or facts.get("remaining") != authority["qty"] - filled):
            return False
    elif status is not None or executions:
        return False
    working = [w for w in ev.working if w["ref"] == ref]
    if status in ("working", "partial"):
        if len(working) != 1 or facts != working[0] or filled >= authority["qty"]:
            return False
    elif working or (status == "filled" and filled != authority["qty"]):
        return False
    for execution in executions:
        fields = dict(ref=execution.ref, sym=execution.sym, leg_id=execution.leg_id,
                      kind=execution.kind, side=execution.side, qty=execution.order_qty,
                      type=execution.order_type, price=execution.order_price,
                      attached_to=execution.attached_to)
        if (not order_matches(fields, authority) or type(execution.qty) is not int
                or execution.qty <= 0 or not sent_seq < execution.execution_id < ev.acquired
                or (execution.execution_id not in seen and execution.execution_id <= history_acquired)
                or not execution.fill_id
                or ev.lot_facts.get(execution.fill_id, {}).get("entry_ref") != ref
                or any(e.fill_id == execution.fill_id and e.ref != ref for e in ev.executions)):
            return False
    return True
