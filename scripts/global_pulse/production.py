"""Exact-revision adapter for the registry owned by PR #787.

This module reads public metadata, never imports the ops layer. A new registry
revision needs an explicitly reviewed pin and compatibility tests.
"""
import hashlib
import json

REVISION = "107fe97cdba6f2b6b5c0f1939bfe93b3924b3ceb"
SHA256 = "ae0af9795931524faecc53d00ac63864caf41e68949d28f83d719970783b2b9c"
PATH = "ops/global_market_map/registry.json"
REPOSITORY = "Joshua-Asante/first-passage"
SCHEMA = "global-market-map/v1"


def project(registry, raw, revision):
    if (revision != REVISION or hashlib.sha256(raw).hexdigest() != SHA256
            or registry.get("schema_version") != SCHEMA
            or registry.get("registry_id") != "global-market-map"):
        raise ValueError("unrecognized production registry revision/content; reviewed exact pin required")
    rows = {}
    for source in registry["series"]:
        rows[source["series_id"]] = {
            "id": source["series_id"],
            "provider": source["instrument"]["provider"],
            "unit": source["instrument"]["unit"],
            "conventions": {c["id"]: dict(c) for c in source["measurement_conventions"]},
            "proxy": ("none" if source["proxy"]["kind"] == "none"
                      else json.dumps(source["proxy"], sort_keys=True)),
            "futures_roll": ("none" if source["futures"] is None
                             else json.dumps(source["futures"], sort_keys=True)),
            "max_age_seconds": source["observation"]["max_age_seconds"],
            "production": source,
        }
    return rows


def context(registry, revision):
    return {
        "repository": REPOSITORY, "path": PATH, "revision": revision, "sha256": SHA256,
        "verification": registry["verification"], "chart_settings": registry["chart_settings"],
        "sources": registry["sources"], "series": registry["series"],
        "watchlist": registry["watchlist"],
    }


def limitations(row):
    source = row["production"]
    sid = row["id"]
    return [f"{sid}: {field}: {json.dumps(source[field], sort_keys=True)}"
            for field in ("instrument", "entitlement", "observation", "limitations", "evidence_refs")]
