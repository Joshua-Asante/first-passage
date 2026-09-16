"""Pure structural checks for the fixed-book feed and adapter boundary."""
from dataclasses import dataclass
from datetime import datetime
import math

from c1_signal_daemon.book_adapters import ADAPTER_BY_LEG
from c1_signal_daemon.book_protocol import Action, Bracket, BracketAmend, Cancel, FillTiming, OrderIntent, Side
from c1_signal_daemon.feed import Bar


@dataclass(frozen=True)
class InputViolation:
    code: str
    field: str


def _number(value):
    return type(value) is int or (type(value) is float and math.isfinite(value))


def _identity(value):
    return type(value) is str and bool(value.strip())


def _aware(value):
    if not isinstance(value, datetime):
        return False
    try:
        return value.utcoffset() is not None
    except (ValueError, TypeError, OverflowError):
        return False


def validate_bar(bar: Bar) -> InputViolation | None:
    if type(bar) is not Bar:
        return InputViolation("type", "bar")
    if not _aware(bar.ts):
        return InputViolation("aware_time", "ts")
    for field in ("open", "high", "low", "close", "volume"):
        if not _number(getattr(bar, field)):
            return InputViolation("finite_number", field)
    if bar.volume < 0:
        return InputViolation("nonnegative", "volume")
    if not (bar.low <= bar.open <= bar.high and bar.low <= bar.close <= bar.high):
        return InputViolation("ohlc_order", "bar")
    return None


def validate_action(action: Action) -> InputViolation | None:
    if type(action) not in (OrderIntent, BracketAmend, Cancel):
        return InputViolation("type", "action")
    if not _identity(action.leg_id) or action.leg_id not in ADAPTER_BY_LEG:
        return InputViolation("known_identity", "leg_id")
    if isinstance(action, Cancel):
        if action.order_id is not None and not _identity(action.order_id):
            return InputViolation("identity", "order_id")
        return None
    scope = action.scope_fill_ids
    if scope is not None and (type(scope) is not tuple or
            any(not _identity(item) for item in scope) or len(set(scope)) != len(scope)):
        return InputViolation("scope", "scope_fill_ids")
    bracket = action.bracket
    if bracket is None and isinstance(action, BracketAmend):
        return InputViolation("type", "bracket")
    if bracket is not None:
        if type(bracket) is not Bracket:
            return InputViolation("type", "bracket")
        for field in ("stop", "limit"):
            value = getattr(bracket, field)
            if value is not None and (not _number(value) or value <= 0):
                return InputViolation("positive_price", "bracket." + field)
        activation, offset = bracket.trail_activation_ticks, bracket.trail_offset_ticks
        if activation is not None or offset is not None:
            if type(activation) is not int or activation < 0:
                return InputViolation("trailing_pair", "bracket.trail_activation_ticks")
            if type(offset) is not int or offset <= 0:
                return InputViolation("trailing_pair", "bracket.trail_offset_ticks")
    if isinstance(action, BracketAmend):
        return None
    if not _identity(action.order_id):
        return InputViolation("identity", "order_id")
    if type(action.kind) is not str or action.kind not in ("entry", "add", "exit", "flat"):
        return InputViolation("kind", "kind")
    if type(action.side) is not Side:
        return InputViolation("type", "side")
    if type(action.timing) is not FillTiming:
        return InputViolation("type", "timing")
    if type(action.order_type) is not str or action.order_type not in ("market", "stop"):
        return InputViolation("order_type", "order_type")
    if not (action.qty is None and action.kind in ("exit", "flat")):
        if type(action.qty) is not int or action.qty <= 0:
            return InputViolation("quantity", "qty")
    if action.price is not None or action.order_type == "stop":
        if not _number(action.price) or action.price <= 0:
            return InputViolation("positive_price", "price")
    if action.oca_group is not None and not _identity(action.oca_group):
        return InputViolation("identity", "oca_group")
    if type(action.reason) is not str:
        return InputViolation("type", "reason")
    if not _number(action.stop_dist_pts) or action.stop_dist_pts < 0:
        return InputViolation("nonnegative", "stop_dist_pts")
    if action.bar_time is not None and not _aware(action.bar_time):
        return InputViolation("aware_time", "bar_time")
    return None
