"""Appendix-A JSON → CrossTrade key=value translator (P5 golden-path offline layer)."""
from __future__ import annotations

from typing import Any


def appendix_a_to_crosstrade(
    payload: dict[str, Any],
    *,
    account: str,
    secret_key: str,
) -> str:
    """Map validated Appendix-A object to CrossTrade semicolon payload."""
    leg = payload["leg"]
    action = payload["action"]
    instrument = payload["symbol"]
    qty = int(payload["qty"])
    order_id = payload["id"]

    parts = [
        f"key={secret_key}",
    ]

    if leg == "exit" and action == "close":
        parts.extend([
            "command=closeposition",
            f"account={account}",
            f"instrument={instrument}",
            f"quantity={qty}",
        ])
        return ";".join(parts) + ";"

    parts.append("command=place")
    parts.extend([
        f"account={account}",
        f"instrument={instrument}",
        f"action={action}",
        f"qty={qty}",
        "order_type=market",
        "tif=day",
        f"order_id={order_id}",
    ])
    if "sl" in payload:
        parts.append(f"stop_loss={payload['sl']}")
    if "tp" in payload:
        parts.append(f"take_profit={payload['tp']}")
    if leg == "entry":
        parts.append("flatten_first=true")
    return ";".join(parts) + ";"


def parse_crosstrade_payload(text: str) -> dict[str, str]:
    """Parse semicolon key=value payload to dict (lowercase keys)."""
    out: dict[str, str] = {}
    for chunk in text.split(";"):
        chunk = chunk.strip()
        if not chunk or chunk.startswith("//"):
            continue
        if "=" not in chunk:
            continue
        key, val = chunk.split("=", 1)
        out[key.strip().lower()] = val.strip()
    return out
