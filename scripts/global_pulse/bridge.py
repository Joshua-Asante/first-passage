"""Versioned observation packets, immutable captures and editable Notice drafts.

Synthetic fixtures remain supported alongside an exact-revision adapter for
the separately owned production registry. No production definitions live here.
"""
from __future__ import annotations

from contextlib import contextmanager
from datetime import date, datetime
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import tempfile
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from scripts.research_asset_registry import ALLOWED_KINDS, validate_registry
from . import production

ID = re.compile(r"GP-\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*\Z")
HASH = re.compile(r"[a-f0-9]{64}\Z")
ROUTE_START = "<!-- global-pulse-routing:start -->"
ROUTE_END = "<!-- global-pulse-routing:end -->"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def finite_number(value):
    try:
        return type(value) in (int, float) and math.isfinite(value)
    except OverflowError:
        return False


def obj(value, fields, label):
    require(isinstance(value, dict), f"{label}: expected object")
    require(set(value) == set(fields.split()), f"{label}: expected fields {fields}")
    return value


def text(value, label):
    require(isinstance(value, str) and bool(value.strip()), f"{label}: expected nonempty text")
    require(not any(ord(c) < 32 or 127 <= ord(c) <= 159 for c in value),
            f"{label}: control characters are not permitted")
    return value


def strings(value, label):
    require(isinstance(value, list), f"{label}: expected array")
    for item in value:
        text(item, label)
    return value


def timestamp(value, label):
    text(value, label)
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{label}: invalid ISO timestamp") from exc
    require("T" in value and result.utcoffset() is not None,
            f"{label}: timezone-aware ISO timestamp required")
    return result


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()


def _unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def decode(data):
    try:
        return json.loads(data, object_pairs_hook=_unique,
                          parse_constant=lambda x: require(False, f"invalid JSON number: {x}"))
    except RecursionError as exc:
        raise ValueError("excessive JSON nesting") from exc


def relative_file_path(relative):
    text(relative, "local path")
    path = Path(relative)
    require(path.parts and not path.anchor and not any(p in {"..", "."} for p in path.parts)
            and "\\" not in relative and ":" not in relative, "unsafe local path")
    return path


def local_file(root, relative):
    path = relative_file_path(relative)
    resolved_root = root.resolve()
    current = resolved_root
    for part in path.parts:
        current = current / part
        require(not current.is_symlink(), f"symlink not permitted: {relative}")
        require(current.resolve().is_relative_to(resolved_root), f"path escapes input root: {relative}")
    require(current.is_file(), f"missing local file: {relative}")
    return current


def registry_rows(registry):
    obj(registry, "schema_version synthetic series", "registry")
    require(registry["schema_version"] == "global-pulse-synthetic-registry/v1"
            and registry["synthetic"] is True,
            "production registry adapter pending authoritative watchlist schema")
    require(isinstance(registry["series"], list) and registry["series"], "registry: series required")
    rows = {}
    for row in registry["series"]:
        obj(row, "id provider unit conventions proxy futures_roll max_age_seconds", "series")
        for field in ("id", "provider", "unit", "proxy", "futures_roll"):
            text(row[field], f"series.{field}")
        require(row["id"] not in rows, "duplicate registry series ID")
        require(isinstance(row["conventions"], dict) and row["conventions"], "conventions required")
        for key, convention in row["conventions"].items():
            text(key, "convention ID")
            obj(convention, "definition output_unit", "convention")
            text(convention["definition"], "convention.definition")
            text(convention["output_unit"], "convention.output_unit")
        age = row["max_age_seconds"]
        require(age is None or (finite_number(age) and age >= 0),
                "max_age_seconds must be null or a nonnegative finite number")
        rows[row["id"]] = row
    return rows


def validate(packet, input_root, *, retained=None):
    """Read only. Return limitations and the exact verified input bytes."""
    require(isinstance(packet, dict), "packet: expected object")
    v2 = packet.get("schema_version") == 2
    obj(packet, "schema_version observation_id author source captured_at watchlist measurements "
        "evidence interpretation limitations prior_exposure lineage correction" +
        (" data_kind missing_inputs attendance" if v2 else ""), "packet")
    require(type(packet["schema_version"]) is int and packet["schema_version"] in (1, 2),
            "packet: unsupported schema_version")
    oid = text(packet["observation_id"], "observation_id")
    require(ID.fullmatch(oid), "observation_id must be GP-YYYY-MM-DD-slug")
    date.fromisoformat(oid[3:13])
    for field in ("author", "source"):
        text(packet[field], field)
    captured = timestamp(packet["captured_at"], "captured_at")
    binding = obj(packet["watchlist"], "path sha256" + (" revision" if v2 else ""), "watchlist")
    relative_file_path(binding["path"])
    require(isinstance(binding["sha256"], str) and HASH.fullmatch(binding["sha256"]),
            "watchlist.sha256: exact content hash required")
    registry_bytes = (local_file(input_root, binding["path"]).read_bytes() if retained is None
                      else (retained / "registry.json").read_bytes())
    require(digest(registry_bytes) == binding["sha256"], "unresolvable registry revision: hash mismatch")
    registry = decode(registry_bytes)
    is_production = isinstance(registry, dict) and registry.get("schema_version") == production.SCHEMA
    if is_production:
        require(v2, "production registry requires packet schema_version 2")
        rows = production.project(registry, registry_bytes, binding["revision"])
        warnings = ["Production registry audit: " + registry["verification"]["qualification"]]
    else:
        rows = registry_rows(registry)
        warnings = ["SYNTHETIC registry; production watchlist integration pending"]
        if v2:
            require(binding["revision"] is None, "synthetic registry has no production Git revision")
    attended = None
    if v2:
        require(packet["data_kind"] in ("synthetic", "real"), "data_kind must be synthetic or real")
        require(is_production or packet["data_kind"] == "synthetic", "real data requires identified production registry")
        if packet["data_kind"] == "synthetic":
            require(packet["attendance"] is None, "synthetic values must not claim real attendance")
            warnings.append("SYNTHETIC VALUES: demonstration only; registry definitions may be real")
        else:
            attendance = obj(packet["attendance"], "observer method attended_at evidence_ids", "attendance")
            text(attendance["observer"], "attendance.observer")
            text(attendance["method"], "attendance.method")
            attended = timestamp(attendance["attended_at"], "attendance.attended_at")
            require(attended <= captured,
                    "attendance cannot follow capture")
            require(strings(attendance["evidence_ids"], "attendance.evidence_ids"), "attendance evidence required")
    warnings.extend(strings(packet["limitations"], "limitations"))
    interpretation = obj(packet["interpretation"],
                         "observation baseline departure why_stands_out candidate_explanations", "interpretation")
    for field in ("observation", "baseline", "departure", "why_stands_out"):
        text(interpretation[field], f"interpretation.{field}")
    strings(interpretation["candidate_explanations"], "candidate_explanations")
    lineage = obj(packet["lineage"], "observations notices investigations", "lineage")
    for field, value in lineage.items():
        strings(value, f"lineage.{field}")
    exposure = obj(packet["prior_exposure"], "status windows note", "prior_exposure")
    require(exposure["status"] in ("unknown", "none", "declared"), "invalid prior exposure status")
    text(exposure["note"], "prior_exposure.note")
    require(isinstance(exposure["windows"], list), "exposure windows must be array")
    require(bool(exposure["windows"]) == (exposure["status"] == "declared"),
            "declared exposure requires windows; none/unknown must not claim known windows")
    for window in exposure["windows"]:
        obj(window, "start end activity series_ids", "exposure window")
        require(timestamp(window["start"], "exposure.start") <= timestamp(window["end"], "exposure.end")
                <= captured, "impossible exposure window")
        text(window["activity"], "exposure.activity")
        require(strings(window["series_ids"], "exposure.series_ids")
                and all(s in rows for s in window["series_ids"]), "unknown exposure series ID")
    if exposure["status"] == "unknown":
        warnings.append("Prior data exposure is unknown; confirmation-data eligibility unresolved")
    correction = packet["correction"]
    if correction is not None:
        obj(correction, "predecessor_id predecessor_sha256 changes", "correction")
        require(isinstance(correction["predecessor_id"], str)
                and ID.fullmatch(correction["predecessor_id"])
                and correction["predecessor_id"] != oid, "invalid correction predecessor ID")
        require(isinstance(correction["predecessor_sha256"], str)
                and HASH.fullmatch(correction["predecessor_sha256"]), "invalid predecessor hash")
        require(strings(correction["changes"], "correction.changes"), "correction must identify changes")
    require(isinstance(packet["evidence"], list) and packet["evidence"], "evidence required")
    evidence = {}
    for index, item in enumerate(packet["evidence"]):
        obj(item, "id kind path sha256 provider source_reference evidence_store_version", "evidence")
        relative_file_path(item["path"])
        eid = text(item["id"], "evidence.id")
        require(text(item["kind"], "evidence.kind") in ALLOWED_KINDS, "unknown evidence asset kind")
        require(eid not in evidence, "duplicate evidence ID")
        for field in ("provider", "source_reference"):
            text(item[field], f"evidence.{field}")
        if item["evidence_store_version"] is not None:
            text(item["evidence_store_version"], "evidence_store_version")
            warnings.append(f"{eid}: supplied evidence-store reference is unverified; use store source to inspect")
        body = (local_file(input_root, item["path"]).read_bytes() if retained is None
                else (retained / f"artifact-{index}.bin").read_bytes())
        require(digest(body) == item["sha256"], f"{eid}: evidence hash mismatch")
        evidence[eid] = body
    require(isinstance(packet["measurements"], list) and packet["measurements"], "measurements required")
    if v2:
        if packet["attendance"] is not None:
            require(all(e in evidence for e in packet["attendance"]["evidence_ids"]), "unknown attendance evidence")
        require(isinstance(packet["missing_inputs"], list), "missing_inputs must be array")
        missing = set()
        for item in packet["missing_inputs"]:
            obj(item, "series_id reason", "missing input")
            sid = text(item["series_id"], "missing series_id")
            require(sid in rows and sid not in missing, "unknown/duplicate missing series ID")
            text(item["reason"], "missing input reason")
            missing.add(sid)
            warnings.append(f"{sid}: UNAVAILABLE / missing input: {item['reason']}")
        if is_production:
            require(set(registry["watchlist"]["unavailable_series_ids"]) <= missing,
                    "explicit missing funding_basis entry required")
    seen = set()
    for m in packet["measurements"]:
        obj(m, "id series_id value unit convention_id definition window_start window_end "
            "observed_at published_at available_at evidence_ids" +
            (" delivery observation_date bar_time timing_basis source_timezone contract_ids" if v2 else ""), "measurement")
        mid = text(m["id"], "measurement.id")
        require(mid not in seen, "duplicate measurement ID")
        seen.add(mid)
        sid = text(m["series_id"], "series_id")
        require(sid in rows, f"unknown series ID: {sid}")
        row = rows[sid]
        if v2:
            require(sid not in missing, f"{sid}: unavailable input cannot be measured")
            text(m["timing_basis"], "timing_basis")
            if m["observation_date"] is not None:
                date.fromisoformat(text(m["observation_date"], "observation_date"))
            if m["bar_time"] is not None:
                require(timestamp(m["bar_time"], "bar_time") <= captured, "future bar label is not a realized input")
            if m["source_timezone"] is not None:
                text(m["source_timezone"], "source_timezone")
            strings(m["contract_ids"], "contract_ids")
            if is_production:
                source = row["production"]
                require(source["availability"] == "available", f"{sid}: unavailable registry target")
                expected = {"delayed": "delayed", "daily_publication": "daily",
                            "live_label_observed_closed_market": "live_label"}[source["entitlement"]["status"]]
                require(m["delivery"] == expected, f"{sid}: delivery classification must preserve registry status {expected}")
                warnings.extend(production.limitations(row))
                if source["futures"] is None:
                    require(not m["contract_ids"], f"{sid}: non-futures input cannot specify contract IDs")
                if source["futures"] is not None and not m["contract_ids"]:
                    warnings.append(f"{sid}: actual contract IDs unknown; continuous-series roll mapping unresolved")
            else:
                require(m["delivery"] in ("live_label", "delayed", "daily", "unknown"), "invalid delivery")
        cid = text(m["convention_id"], "convention_id")
        require(cid in row["conventions"], f"{mid}: unknown measurement convention")
        convention = row["conventions"][cid]
        require(m["unit"] == convention["output_unit"], f"{mid}: incorrect units")
        require(m["definition"] == convention["definition"], f"{mid}: ambiguous measurement definition")
        require(finite_number(m["value"]), f"{mid}: finite value required")
        unknown_clock = v2 and m["observed_at"] is None
        source_zone = None
        observation_date = None
        if v2:
            if m["source_timezone"] is not None:
                try:
                    source_zone = ZoneInfo(m["source_timezone"])
                except (ValueError, ZoneInfoNotFoundError) as exc:
                    raise ValueError(f"{mid}: source timezone must be a resolvable IANA zone") from exc
            if m["observation_date"] is not None:
                observation_date = date.fromisoformat(m["observation_date"])
                capture_date = captured.astimezone(source_zone).date() if source_zone else captured.date()
                require(observation_date <= capture_date, "future observation date")
                if attended is not None:
                    attendance_date = attended.astimezone(source_zone).date() if source_zone else attended.date()
                    require(observation_date <= attendance_date, f"{mid}: attendance predates observation date")
                if source_zone is None:
                    warnings.append(f"{mid}: source timezone unknown; date bounds use capture/attendance offsets, "
                                    "not a verified source calendar")
        if unknown_clock:
            require(m["delivery"] == "daily", "unknown observation clocks require daily delivery")
            require(m["observation_date"] is not None and m["window_start"] is None and m["window_end"] is None,
                    f"{mid}: unknown observation clock needs observation_date and null window timestamps")
            require(cid == "level", "unknown measurement-window clocks permit only a dated level")
            observed = None
            warnings.append(f"{mid}: exact observation/window clock unknown; date/bar label is not availability")
        else:
            start = timestamp(m["window_start"], f"{mid}.window_start")
            end = timestamp(m["window_end"], f"{mid}.window_end")
            observed = timestamp(m["observed_at"], f"{mid}.observed_at")
            require(start <= end <= observed <= captured, f"{mid}: impossible measurement timing")
        times = {}
        for field in ("published_at", "available_at"):
            if m[field] is None:
                warnings.append(f"{mid}: {field} unknown; capture time does not establish historical availability")
            else:
                times[field] = timestamp(m[field], f"{mid}.{field}")
                if unknown_clock:
                    require(source_zone is not None,
                            f"{mid}: known daily release requires a comparable source timezone")
                    require(times[field].astimezone(source_zone).date() >= observation_date,
                            f"{mid}: {field} predates observation date")
                require(times[field] <= captured and (observed is None or observed <= times[field]),
                        f"{mid}: impossible {field}")
        if len(times) == 2:
            require(times["published_at"] <= times["available_at"], f"{mid}: availability precedes publication")
        if attended is not None:
            known_times = list(times.values()) + ([observed] if observed is not None else [])
            require(all(value <= attended for value in known_times), f"{mid}: attendance predates measured data")
        require(strings(m["evidence_ids"], "measurement.evidence_ids")
                and all(eid in evidence for eid in m["evidence_ids"]), f"{mid}: unknown/missing evidence IDs")
        providers = {item["provider"] for item in packet["evidence"] if item["id"] in m["evidence_ids"]}
        require(row["provider"] in providers, f"{mid}: series provider not represented in evidence")
        age = (captured - observed).total_seconds() if observed is not None else None
        policy = row["max_age_seconds"]
        warnings.append(f"{mid}: observation age " + (f"{age:g}s; " if age is not None else "unknown; ") +
                        ("no declared age policy" if policy is None else
                         f"declared maximum {policy:g}s" + (" EXCEEDED" if age is not None and age > policy else "")))
        for field in ("proxy", "futures_roll"):
            if row[field] != "none":
                warnings.append(f"{mid}: {field}: {row[field]}")
    return {"limitations": warnings, "registry": registry_bytes, "evidence": evidence,
            "registry_context": production.context(registry, binding["revision"]) if is_production else None}


@contextmanager
def writer(root):
    root.mkdir(parents=True, exist_ok=True)
    lock = root / "writer.lock"
    # Exclusive creation owns the lock; close before unlinking on Windows.
    handle = lock.open("x")
    try:
        with handle:
            yield
    finally:
        lock.unlink()


def write_new(path, body):
    with path.open("xb") as handle:
        handle.write(body)
        handle.flush()
        os.fsync(handle.fileno())


def capture_files(packet, checked):
    files = [("packet.json", encoded(packet), "evidence"),
             ("registry.json", checked["registry"], "configuration"),
             ("validation.json", encoded({"limitations": checked["limitations"]}), "evidence")]
    if checked["registry_context"] is not None:
        files.append(("registry-context.json", encoded(checked["registry_context"]), "configuration"))
    for i, item in enumerate(packet["evidence"]):
        files.append((f"artifact-{i}.bin", checked["evidence"][item["id"]], item["kind"]))
    return files


def capture_inventory(packet, files):
    assets, locations = [], []
    for name, data, kind in files:
        aid = f"{packet['observation_id']}:{name}"
        assets.append(dict(id=aid, kind=kind, label=name, privacy="private",
                           members=[dict(key="file", sha256=digest(data))], parents=[],
                           supersedes=[], claims=[], limitations=[]))
        locations.append(dict(asset_id=aid, member_key="file", root="capture", relative_path=name))
    return dict(schema_version=1, assets=assets), locations


def _verify_snapshot(bundle):
    locations = decode(local_file(bundle, "locations.json").read_bytes())
    obj(locations, "schema_version roots locations", "capture locations")
    obj(locations["roots"], "capture", "capture root")
    declared_root = Path(text(locations["roots"]["capture"], "capture root"))
    require(declared_root.is_absolute() and declared_root.resolve() == bundle.resolve(),
            "capture root does not match bundle being verified")
    findings = validate_registry(bundle / "assets.json", bundle / "locations.json")
    require(not findings, f"retained asset integrity failure: {findings}")
    packet = decode((bundle / "packet.json").read_bytes())
    require(packet["observation_id"] == bundle.name, "capture directory identity mismatch")
    checked = validate(packet, bundle, retained=bundle)
    expected_assets, expected_locations = capture_inventory(packet, capture_files(packet, checked))
    require(locations["locations"] == expected_locations, "capture locations do not bind retained files")
    require(decode((bundle / "validation.json").read_bytes()) == {"limitations": checked["limitations"]},
            "retained limitations differ from packet/registry")
    if checked["registry_context"] is not None:
        require(decode((bundle / "registry-context.json").read_bytes()) == checked["registry_context"],
                "retained production registry context differs")
    require(decode((bundle / "assets.json").read_bytes()) == expected_assets,
            "retained inventory differs from generated capture metadata")
    return packet


def verify_bundle(bundle):
    packet = _verify_snapshot(bundle)
    current = packet
    seen = {packet["observation_id"]}
    while current["correction"] is not None:
        correction = current["correction"]
        predecessor_id = correction["predecessor_id"]
        require(predecessor_id not in seen, "cyclic correction lineage")
        seen.add(predecessor_id)
        predecessor = bundle.parent / predecessor_id
        prior = _verify_snapshot(predecessor)
        require(digest((predecessor / "packet.json").read_bytes()) == correction["predecessor_sha256"],
                "correction predecessor hash mismatch")
        require(timestamp(prior["captured_at"], "predecessor.captured_at") <=
                timestamp(current["captured_at"], "captured_at"), "correction predates predecessor")
        current = prior
    return packet


def capture(packet, input_root, root):
    checked = validate(packet, input_root)
    body = encoded(packet)
    destination = root / packet["observation_id"]
    with writer(root):
        if destination.exists():
            verify_bundle(destination)
            require((destination / "packet.json").read_bytes() == body,
                    "observation ID already captured with different content; create a correction")
            return destination
        correction = packet["correction"]
        if correction:
            predecessor = root / correction["predecessor_id"]
            prior = verify_bundle(predecessor)
            require(digest((predecessor / "packet.json").read_bytes()) == correction["predecessor_sha256"],
                    "correction predecessor hash mismatch")
            require(timestamp(prior["captured_at"], "predecessor.captured_at") <=
                    timestamp(packet["captured_at"], "captured_at"), "correction predates predecessor")
        temporary = Path(tempfile.mkdtemp(prefix=".capture-", dir=root))
        try:
            files = capture_files(packet, checked)
            assets, locations = capture_inventory(packet, files)
            for name, data, kind in files:
                write_new(temporary / name, data)
            write_new(temporary / "assets.json", encoded(assets))
            write_new(temporary / "locations.json", encoded(dict(schema_version=1,
                      roots={"capture": str(destination.resolve())}, locations=locations)))
            # Atomic directory publication; the writer lock prevents competing captures.
            temporary.rename(destination)
        finally:
            if temporary.exists():
                shutil.rmtree(temporary)
    verify_bundle(destination)
    return destination


def notice_id(packet):
    return "N-" + packet["observation_id"][3:]


def draft_binding(packet, bundle):
    return {"- **Source:**": str(bundle.resolve() / "packet.json"),
            "- Packet:": f"{packet['observation_id']}; SHA-256 {digest(encoded(packet))}"}


def render(packet, bundle):
    p = packet
    interp = p["interpretation"]
    limitations = decode((bundle / "validation.json").read_bytes())["limitations"]
    measurements = "\n".join("- " + json.dumps(m, sort_keys=True) for m in p["measurements"])
    mechanisms = "\n".join("- " + item for item in interp["candidate_explanations"]) or "None supplied."
    related = json.dumps(p["lineage"], sort_keys=True)
    binding = "\n".join(f"{prefix} {value}" for prefix, value in draft_binding(p, bundle).items())
    return f"""# Notice — {p['observation_id']}

**Notice ID:** {notice_id(p)}
**Observed:** {', '.join(m['observed_at'] or (m.get('observation_date', '') + ' (clock unknown)') for m in p['measurements'])}
**Author:** {p['author']}
**Source:** {p['source']}
**Status:** OPEN (draft; routing pending)
**Lives in:** PENDING explicit finalization destination

## §0 — Source anchor

{binding}
- **Observed at:** per-series timestamps below; captured {p['captured_at']}
- Watchlist: {p['watchlist']['path']}; SHA-256 {p['watchlist']['sha256']}; retained registry.json
- Registry Git revision: {p['watchlist'].get('revision') or 'synthetic fixture; no production revision'}
- Input data: {p.get('data_kind', 'synthetic')}; attendance: {json.dumps(p.get('attendance'))}

## §1 — The observation

{interp['observation']}

Raw measurements (separate from interpretation):
{measurements}

Explicit missing inputs: {json.dumps(p.get('missing_inputs', []), sort_keys=True)}

## §2 — Why it stands out (the N signal)

- **Baseline:** {interp['baseline']}
- **Delta:** {interp['departure']}
- **Why it stands out:** {interp['why_stands_out']}
- **Frequency check / known related records:** {related}

## §3 — Candidate mechanisms (informal)

Not pre-registered hypotheses.

{mechanisms}

{ROUTE_START}
## §4 — Routing decision

Decision: PENDING. Explicit GRADUATE / DROP / HOLD required to finalize.
Reason: awaiting supplied routing decision.

## §5 — If HOLD: re-check trigger

No reconsideration condition or date supplied. No reminder scheduled.
{ROUTE_END}

## §10 — Audit hooks

```text
python -I scripts/fp.py python -m scripts.global_pulse verify --bundle {bundle.resolve()}
```

Evidence locators and hashes: assets.json + locations.json in the capture directory.
Original evidence references: {json.dumps(p['evidence'], sort_keys=True)}
Prior exposure: {json.dumps(p['prior_exposure'], sort_keys=True)}
Correction: {json.dumps(p['correction'], sort_keys=True)}

Material limitations:
{chr(10).join('- ' + item for item in limitations)}

Hashes establish identity, not correctness or statistical independence. This
capture does not determine trial counts or confirmation-data eligibility.
"""


def draft(bundle):
    packet = verify_bundle(bundle)
    path = bundle / "notice-draft.md"
    with writer(bundle):
        if not path.exists():
            write_new(path, render(packet, bundle).encode())
    return path


def routing(decision):
    obj(decision, "decision reason reconsider_on reconsider_when investigation", "routing")
    choice = decision["decision"]
    require(choice in ("HOLD", "DROP", "GRADUATE"), "explicit routing decision required")
    text(decision["reason"], "routing.reason")
    if choice == "HOLD":
        require(decision["investigation"] is None, "HOLD must not specify investigation")
        require(decision["reconsider_on"] is not None or decision["reconsider_when"] is not None,
                "HOLD needs an explicit reconsideration condition/date")
        if decision["reconsider_on"] is not None:
            date.fromisoformat(text(decision["reconsider_on"], "reconsider_on"))
        if decision["reconsider_when"] is not None:
            text(decision["reconsider_when"], "reconsider_when")
        status = f"HELD until {decision['reconsider_on'] or 'supplied condition'}"
    else:
        require(decision["reconsider_on"] is None and decision["reconsider_when"] is None,
                "reconsideration applies only to HOLD")
        if choice == "GRADUATE":
            reference = text(decision["investigation"], "investigation reference or PENDING required")
            require(reference == "PENDING" or bool(re.fullmatch(r"Q-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*", reference)),
                    "investigation must be specific Q-ID or PENDING")
            status = "GRADUATED to " + ("investigation creation PENDING" if reference == "PENDING" else reference)
        else:
            require(decision["investigation"] is None, "DROP must not specify investigation")
            status = "DROPPED"
    body = f"## §4 — Routing decision\n\nDecision: {choice}\nReason: {decision['reason']}\n"
    if choice == "GRADUATE":
        body += f"Investigation: {decision['investigation']} (creation is manual).\n"
    if choice == "HOLD":
        body += (f"\n## §5 — If HOLD: re-check trigger\n\n"
                 f"- **Re-check date:** {decision['reconsider_on'] or 'not supplied; condition-based'}\n"
                 f"- **Trigger condition:** {decision['reconsider_when'] or 'reconsider on supplied date'}\n"
                 "- **Calendar entry:** not scheduled by this bridge.\n")
    return status, body


def finalize(bundle, decision, notice_dir):
    packet = verify_bundle(bundle)
    status, route = routing(decision)
    source = (bundle / "notice-draft.md").read_text(encoding="utf-8")
    require(source.count(f"**Notice ID:** {notice_id(packet)}\n") == 1,
            "draft Notice identity was edited; reconcile before finalizing")
    for prefix, value in draft_binding(packet, bundle).items():
        require([line for line in source.splitlines() if line.startswith(prefix)] == [f"{prefix} {value}"],
                "draft provenance differs from selected capture; reconcile before finalizing")
    require(source.count(ROUTE_START) == source.count(ROUTE_END) == 1,
            "edited draft lost routing markers; restore markers before finalizing")
    before, remainder = source.split(ROUTE_START)
    _, after = remainder.split(ROUTE_END)
    require(before.count("**Status:** OPEN (draft; routing pending)") == 1,
            "draft status was edited; reconcile it before finalizing")
    result = before.replace("**Status:** OPEN (draft; routing pending)", f"**Status:** {status}") + route + after
    path = notice_dir / f"{notice_id(packet)}.md"
    destination_header = r"(?m)^\*\*Lives in:\*\*[^\n]*$"
    require(len(re.findall(destination_header, result)) == 1,
            "draft must retain exactly one Lives in header")
    result = re.sub(destination_header, lambda _: f"**Lives in:** {path.resolve().as_posix()}", result)
    with writer(bundle):
        receipt = bundle / "notice-finalization.json"
        intent = encoded({"notice": str(path.resolve()), "routing": decision})
        if receipt.exists():
            require(receipt.read_bytes() == intent,
                    "Notice finalization already bound to a different destination/decision")
        with writer(notice_dir):
            # Reserve destination before publication, so a retry after interruption
            # cannot route the same packet into a second Notice directory.
            require(not path.exists(), f"Notice already exists; preserved: {path}")
            if not receipt.exists():
                write_new(receipt, intent)
            write_new(path, result.encode())
    return path
