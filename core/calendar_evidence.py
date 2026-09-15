"""Pure capture identity and date-scoped halt evidence for calendar authoring/loading."""
from datetime import date, datetime, timezone
from hashlib import sha256
import json
from zoneinfo import ZoneInfo


# The immutable v1 capture's quoted wall-date events, converted from CT to UTC.
# This compatibility mapping belongs only to these exact bytes, never to an ID alone.
_LEGACY_DIGEST = "56951e1527af20966dea64130bf8d0a1dccb9bc011bd6e0501282faa549fcba5"
_LEGACY_HALTS = {"6J": "21:00", "MGC": "18:30", "MYM": "17:00", "MNQ": "17:00"}


def read_json_object(data: bytes) -> dict:
    """Reject ambiguous objects before JSON normalization can erase duplicate keys."""
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    payload = json.loads(data, object_pairs_hook=unique_object)
    if not isinstance(payload, dict):
        raise ValueError("expected a JSON object")
    return payload


def index_captures(evidence: dict) -> dict[str, dict]:
    captures = evidence.get("captures")
    if not isinstance(captures, list) or not captures or any(
            not isinstance(c, dict) or not isinstance(c.get("id"), str) or not c["id"].strip()
            for c in captures):
        raise ValueError("calendar: evidence captures")
    ids = [c["id"] for c in captures]
    if len(set(ids)) != len(ids):
        raise ValueError("calendar: duplicate evidence capture ids")
    return dict(zip(ids, captures))


def halt_evidence(evidence_bytes: bytes, captures: dict[str, dict]) -> dict:
    """Index explicit matching halts by capture, account date and product.

    Each optional capture.matching_halts entry has exactly account_date,
    product and matching_close_utc. The date is the Tradeify account date, not
    a CME business trade date. Ordinary schedule captures may omit this list.
    """
    result = {}
    for sid, capture in captures.items():
        events = capture.get("matching_halts", [])
        if not isinstance(events, list):
            raise ValueError(f"halt evidence: {sid}.matching_halts must be a list")
        indexed = {}
        for event in events:
            if not isinstance(event, dict) or set(event) != {"account_date", "product", "matching_close_utc"}:
                raise ValueError(f"halt evidence: {sid} event keys")
            try:
                day = date.fromisoformat(event["account_date"])
                close = datetime.strptime(event["matching_close_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            except (TypeError, ValueError) as exc:
                raise ValueError(f"halt evidence: {sid} invalid date/time") from exc
            code = event["product"]
            if not isinstance(code, str) or code not in _LEGACY_HALTS:
                raise ValueError(f"halt evidence: {sid} invalid product")
            if "products" in capture and (not isinstance(capture["products"], list) or code not in capture["products"]):
                raise ValueError(f"halt evidence: {sid} product outside capture coverage")
            if close.second or close.astimezone(ZoneInfo("America/New_York")).date() != day:
                raise ValueError(f"halt evidence: {sid} clock/date mismatch")
            key = (day.isoformat(), code)
            if key in indexed:
                raise ValueError(f"halt evidence: {sid} duplicate date/product event")
            indexed[key] = close
        result[sid] = indexed
    if sha256(evidence_bytes).hexdigest() == _LEGACY_DIGEST:
        result["cme-ui-labor-2026"] = {
            ("2026-09-07", code): datetime.fromisoformat(f"2026-09-07T{clock}:00+00:00")
            for code, clock in _LEGACY_HALTS.items()
        }
    return result


def require_halt_evidence(halts: dict, source_ids, day: date, product: str, close: datetime) -> None:
    key = (day.isoformat(), product)
    cited = {halts[sid][key] for sid in source_ids if sid in halts and key in halts[sid]}
    if cited != {close}:
        raise ValueError(f"halt evidence: {day} {product} needs a cited, unambiguous matching halt at {close.isoformat()}")
