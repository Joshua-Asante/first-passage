"""Read-only checks of the local NinjaTrader 8 install (standard library only).

Two checks, each printing one JSON object and exiting 0 on pass, 1 on fail, 2 on a
usage or read error:

``install``  Does the NinjaScript installed in NT match a frozen SHA256SUMS manifest?
             Per manifest file: ``match``, ``differ``, ``differ-eol-or-bom-only`` or
             ``missing``. ``differ-eol-or-bom-only`` (still a fail) needs the frozen
             file beside the manifest, read in place. Every other non-stock ``.cs`` that NT compiles into the same
             assembly is ``extra`` (a fail). Also: is the compiled DLL newer than every
             compiled source (a failed compile leaves the old DLL), and the NT version.
``config``   Safety booleans and counts from Config.xml, the saved workspaces, the
             compile project and ``bin/Custom``: ATI, the two cancel-on-disable options
             (spec B8), connections set to connect on startup, strategies saved in
             workspaces, add-on sources and non-stock assemblies (AGENTS.md money
             control 3, spec B1).

What it never does: write, delete, connect, start a process or talk to NinjaTrader.
It opens files for reading only and does not follow links. Output holds hashes,
booleans, counts, NT version strings, file names under ``bin/Custom`` and assembly
names. It never prints file contents, raw XML, XML text values, connection names,
account names or strategy parameters, so its output is Open data that Codex may see.
It reads the installed private sources in place to hash them and to collect strategy
class names for the workspace count; neither leaves the process.

Run from anywhere::

    python -I ops/nt_install_check.py install --manifest <SHA256SUMS> --manifest-sha256 <hex>
    python -I ops/nt_install_check.py config

``--nt-root`` defaults to ``~/Documents/NinjaTrader 8``.

Known limits: stock ``@*.cs`` files are trusted by name, not hashed; the PDB carries no
source checksums, so the DLL is tied to its sources by file time only, and a copy that
keeps the frozen files' old times can defeat that (recompile after every copy), and NT's
trace does not log every compile, so it is not used; ``ati_enabled`` false
does not prove the ATI port is closed (10-17 canary); the workspace count recognises a
saved strategy by its type name, a format not yet seen with a strategy saved.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

MAX_XML_BYTES = 64 * 1024 * 1024
READ_BLOCK = 64 * 1024

# NinjaTrader's own files at the root of bin/Custom; every other stock file is @-prefixed.
STOCK_ROOT_SOURCES = {"AssemblyInfo.cs", "NinjaTrader.Vendor.cs", "Resource.Designer.cs",
                      "ResourceEnumConverter.cs"}
# Not compiled: NT's export staging folder.
NOT_COMPILED_DIRS = {"ExportNinjaScript"}
STOCK_DLLS = {"NinjaTrader.Custom.dll", "NinjaTrader.Vendor.dll"}
STOCK_REFERENCES = {
    "InfragisticsWPF.DataPresenter", "Infralution.Localization.Wpf", "Microsoft.CSharp",
    "Newtonsoft.Json", "NinjaTrader.Core", "NinjaTrader.Gui", "NinjaTrader.Vendor",
    "PresentationCore", "PresentationFramework", "SharpDX", "SharpDX.Direct2D1", "System",
    "System.ComponentModel.DataAnnotations", "System.Core", "System.Data",
    "System.Data.SQLite", "System.Management", "System.Net.Http", "System.Numerics",
    "System.Web.Extensions", "System.Windows.Forms", "System.Xaml", "System.Xml",
    "System.Xml.Linq", "UIAutomationProvider", "WindowsBase", "mscorlib",
}
# Simulated connections; any other connection set to connect on startup fails.
SIMULATED_CONNECTIONS = {"SimulatorOptions", "PlaybackOptions"}
ESCAPE = re.compile(r"%([0-9A-Fa-f]{2})")
VERSION = re.compile(r"Session Start \(Version ([0-9][0-9.]{0,30})\)")
SHA_LINE = re.compile(r"^([0-9a-fA-F]{64}) [ *](.+)$")
STRATEGY_CLASS = re.compile(r"\bclass\s+([A-Za-z_]\w*)\s*:\s*Strategy\b")
XSI_TYPE = "{http://www.w3.org/2001/XMLSchema-instance}type"
SAFE_NAME = re.compile(r"^[A-Za-z0-9_.@ /-]{1,200}$")


class CheckError(Exception):
    """A usage or read error: exit 2."""


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while block := handle.read(READ_BLOCK):
            digest.update(block)
    return digest.hexdigest()


def _normalised(path: Path) -> bytes:
    with open(path, "rb") as handle:
        data = handle.read()
    if data.startswith(b"\xef\xbb\xbf"):
        data = data[3:]
    return b"\n".join(data.split(b"\r\n"))


def _changed(path: Path) -> float:
    """Latest of modified and (where the OS keeps it) creation time."""
    info = path.stat()
    return max(info.st_mtime, getattr(info, "st_birthtime", 0.0))


def _is_link(path: Path) -> bool:
    return path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction())


def _walk(root: Path, links: list[str], skip_dirs: set[str] = frozenset()) -> list[Path]:
    """Files under root, never following links; links are recorded, not entered."""
    files: list[Path] = []
    stack = [root]
    while stack:
        current = stack.pop()
        for entry in sorted(current.iterdir()):
            if _is_link(entry):
                links.append(entry.relative_to(root).as_posix())
            elif entry.is_dir():
                if not (current == root and entry.name in skip_dirs):
                    stack.append(entry)
            elif entry.is_file():
                files.append(entry)
    return files


def _shown(name: str) -> str:
    return name if SAFE_NAME.match(name) else "[unprintable name]"


def _parse_xml(path: Path) -> ET.Element:
    if path.stat().st_size > MAX_XML_BYTES:
        raise CheckError(f"{path.name} is over {MAX_XML_BYTES} bytes")
    try:
        return ET.parse(path).getroot()
    except ET.ParseError as exc:
        raise CheckError(f"{path.name} is not well-formed XML (line {exc.position[0]})") from None


def _bool_text(element: ET.Element | None) -> bool | None:
    if element is None:
        return None
    text = (element.text or "").strip().lower()
    return {"true": True, "false": False}.get(text)


def _trace_files(nt_root: Path) -> list[Path]:
    trace = nt_root / "trace"
    if not trace.is_dir():
        return []
    files = [p for p in trace.iterdir() if p.is_file() and not _is_link(p)
             and p.name.startswith("trace.") and p.suffix == ".txt"]
    return sorted(files, key=lambda p: p.stat().st_mtime)


def _nt_version(nt_root: Path) -> str | None:
    files = _trace_files(nt_root)
    if not files:
        return None
    with open(files[-1], "rb") as handle:
        first = handle.readline(4096).decode("utf-8", "replace")
    match = VERSION.search(first)
    return match.group(1) if match else None



def _read_manifest(path: Path) -> dict[str, str]:
    entries: dict[str, str] = {}
    with open(path, "rb") as handle:
        lines = handle.read().decode("utf-8").splitlines()
    for number, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        match = SHA_LINE.match(line)
        if not match:
            raise CheckError(f"manifest line {number} is not '<sha256> <name>'")
        name = match.group(2).strip()
        parts = Path(name).parts
        if Path(name).is_absolute() or ".." in parts or "\\" in name or not SAFE_NAME.match(name):
            raise CheckError(f"manifest line {number} names an unsafe path")
        if name in entries:
            raise CheckError(f"manifest line {number} repeats a name")
        entries[name] = match.group(1).lower()
    if not entries:
        raise CheckError("manifest has no entries")
    return entries


def _csproj_items(custom: Path, kind: str) -> list[str]:
    project = custom / "NinjaTrader.Custom.csproj"
    if not project.is_file():
        return []
    root = _parse_xml(project)
    items = []
    for element in root.iter():
        if element.tag.rsplit("}", 1)[-1] == kind and element.get("Include"):
            items.append(element.get("Include"))
    return items


def _is_stock_source(relative: str) -> bool:
    name = relative.rsplit("/", 1)[-1]
    return name.startswith("@") or ("/" not in relative and name in STOCK_ROOT_SOURCES)


def check_install(nt_root: Path, manifest: Path, manifest_sha256: str | None,
                  folder: str) -> dict:
    custom = nt_root / "bin" / "Custom"
    target = custom / folder
    if not custom.is_dir():
        raise CheckError("bin/Custom not found under --nt-root")
    if not manifest.is_file():
        raise CheckError("--manifest not found")
    failures: list[str] = []
    manifest_hash = _sha256(manifest)
    pin_ok = None
    if manifest_sha256 is not None:
        pin_ok = manifest_hash == manifest_sha256.lower()
        if not pin_ok:
            failures.append("manifest sha256 differs from --manifest-sha256")
    entries = _read_manifest(manifest)

    links: list[str] = []
    compiled = {p.relative_to(custom).as_posix(): p
                for p in _walk(custom, links, NOT_COMPILED_DIRS) if p.suffix.lower() == ".cs"}
    for item in _csproj_items(custom, "Compile"):
        relative = "/".join(ESCAPE.sub(lambda m: chr(int(m.group(1), 16)), item).split("\\"))
        compiled.setdefault(relative, custom / relative)

    expected = {f"{folder}/{name}" if folder else name: name for name in entries}
    files: dict[str, str] = {}
    for relative, name in expected.items():
        path = custom / relative
        if not path.is_file() or _is_link(path):
            files[name] = "missing"
        elif _sha256(path) == entries[name]:
            files[name] = "match"
        else:
            reference = manifest.parent / name
            same_text = (reference.is_file() and not _is_link(reference)
                         and _sha256(reference) == entries[name]
                         and _normalised(reference) == _normalised(path))
            files[name] = "differ-eol-or-bom-only" if same_text else "differ"
    failures += [f"{name}: {state}" for name, state in files.items() if state != "match"]

    extra = sorted(_shown(rel) for rel in compiled
                   if rel not in expected and not _is_stock_source(rel))
    failures += [f"extra compiled source: {rel}" for rel in extra]
    failures += [f"link under bin/Custom: {_shown(rel)}" for rel in links]

    dll = custom / "NinjaTrader.Custom.dll"
    present = [p for p in compiled.values() if p.is_file() and not _is_link(p)]
    newest = max((_changed(p) for p in present), default=None)
    dll_newer = dll.is_file() and newest is not None and dll.stat().st_mtime >= newest
    if not dll.is_file():
        failures.append("NinjaTrader.Custom.dll missing")
    elif not dll_newer:
        failures.append("compiled DLL is older than a compiled source")
    return {
        "check": "install",
        "nt_version": _nt_version(nt_root),
        "folder": folder,
        "manifest_sha256": manifest_hash,
        "manifest_pin_ok": pin_ok,
        "files": files,
        "extra": extra,
        "dll_present": dll.is_file(),
        "dll_newer_than_sources": dll_newer,
        "pass": not failures,
        "failures": failures,
    }


def _strategy_classes(custom: Path) -> set[str]:
    names: set[str] = set()
    strategies = custom / "Strategies"
    if not strategies.is_dir():
        return names
    for path in _walk(strategies, []):
        if path.suffix.lower() == ".cs" and not path.name.startswith("@"):
            with open(path, "rb") as handle:
                names |= set(STRATEGY_CLASS.findall(handle.read().decode("utf-8", "replace")))
    return names


def _workspace_strategy_entries(nt_root: Path, classes: set[str]) -> int:
    workspaces = nt_root / "workspaces"
    if not workspaces.is_dir():
        return 0
    count = 0
    for path in _walk(workspaces, []):
        if path.suffix.lower() != ".xml":
            continue
        for element in _parse_xml(path).iter():
            values = [element.text or ""] + list(element.attrib.values())
            if (any("NinjaScript.Strategies." in value for value in values)
                    or element.get(XSI_TYPE) in classes):
                count += 1
    return count


def check_config(nt_root: Path) -> dict:
    config_file = nt_root / "Config.xml"
    custom = nt_root / "bin" / "Custom"
    if not config_file.is_file():
        raise CheckError("Config.xml not found under --nt-root")
    root = _parse_xml(config_file)
    failures: list[str] = []
    warnings: list[str] = []

    ati = _bool_text(root.find("AtiOptions/AtiOptions/IsAtiEnabled"))
    cancel_entries = _bool_text(
        root.find("StrategiesOptions/StrategiesOptions/CancelEntriesOnStrategyDisable"))
    cancel_exits = _bool_text(
        root.find("StrategiesOptions/StrategiesOptions/CancelExitsOnStrategyDisable"))
    for label, value in (("ATI enabled", ati),
                         ("cancel entries on strategy disable", cancel_entries),
                         ("cancel exits on strategy disable", cancel_exits)):
        if value is None:
            failures.append(f"{label}: setting not found")
        elif value:
            failures.append(f"{label}: on")

    connections = live_on_startup = sim_on_startup = 0
    options = root.find("ConnectOptions")
    for connection in (list(options) if options is not None else []):
        connections += 1
        if _bool_text(connection.find("ConnectOnStartup")):
            if connection.tag in SIMULATED_CONNECTIONS:
                sim_on_startup += 1
            else:
                live_on_startup += 1
    if live_on_startup:
        failures.append(f"{live_on_startup} non-simulated connection(s) connect on startup")

    workspace_entries = _workspace_strategy_entries(nt_root, _strategy_classes(custom))
    if workspace_entries:
        failures.append(f"{workspace_entries} strategy entr(y/ies) in saved workspaces")

    links: list[str] = []
    addons = custom / "AddOns"
    addon_sources = 0
    if addons.is_dir():
        addon_sources = sum(1 for p in _walk(addons, links)
                            if p.suffix.lower() == ".cs" and not p.name.startswith("@"))
    if addon_sources:
        failures.append(f"{addon_sources} add-on source file(s)")

    non_stock_dlls = []
    if custom.is_dir():
        non_stock_dlls = sorted(_shown(p.name) for p in custom.iterdir()
                                if p.suffix.lower() == ".dll" and p.name not in STOCK_DLLS)
    failures += [f"non-stock assembly in bin/Custom: {name}" for name in non_stock_dlls]

    dll = custom / "NinjaTrader.Custom.dll"
    dll_bytes = b""
    if dll.is_file():
        with open(dll, "rb") as handle:
            dll_bytes = handle.read()
    references = []
    for item in _csproj_items(custom, "Reference"):
        name = item.split(",", 1)[0].strip()
        if name in STOCK_REFERENCES:
            continue
        file_present = any(p.is_file() for p in (custom / f"{name}.dll",
                                                 nt_root / "bin" / f"{name}.dll"))
        in_dll = bool(name) and name.encode("utf-8") in dll_bytes
        references.append({"name": _shown(name), "file_present": file_present,
                           "in_compiled_dll": in_dll})
        if file_present or in_dll:
            failures.append(f"non-stock reference in use: {_shown(name)}")
        else:
            warnings.append(f"dangling non-stock reference in the compile project: {_shown(name)}")
    failures += [f"link under bin/Custom/AddOns: {_shown(rel)}" for rel in links]

    return {
        "check": "config",
        "nt_version": _nt_version(nt_root),
        "ati_enabled": ati,
        "cancel_entries_on_disable": cancel_entries,
        "cancel_exits_on_disable": cancel_exits,
        "connections": connections,
        "live_connect_on_startup": live_on_startup,
        "simulated_connect_on_startup": sim_on_startup,
        "workspace_strategy_entries": workspace_entries,
        "addon_source_files": addon_sources,
        "non_stock_dlls": non_stock_dlls,
        "non_stock_references": references,
        "pass": not failures,
        "failures": failures,
        "warnings": warnings,
    }


def main(argv: list[str] | None = None, stdout=None) -> int:
    stdout = stdout or sys.stdout
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument("--nt-root", type=Path,
                        default=Path.home() / "Documents" / "NinjaTrader 8")
    commands = parser.add_subparsers(dest="command", required=True)
    install = commands.add_parser("install", help="installed NinjaScript vs a SHA256SUMS manifest")
    install.add_argument("--manifest", type=Path, required=True)
    install.add_argument("--manifest-sha256", help="expected sha256 of the manifest file itself")
    install.add_argument("--folder", default="Strategies",
                         help="folder under bin/Custom the manifest names are relative to")
    commands.add_parser("config", help="safety booleans and counts")
    options = parser.parse_args(argv)
    try:
        if options.command == "install":
            if options.manifest_sha256 is not None and not re.fullmatch(
                    r"[0-9a-fA-F]{64}", options.manifest_sha256):
                raise CheckError("--manifest-sha256 must be 64 hex characters")
            if ".." in Path(options.folder).parts or Path(options.folder).is_absolute():
                raise CheckError("--folder must be a relative path inside bin/Custom")
            folder = Path(options.folder).as_posix().strip("/")
            result = check_install(options.nt_root, options.manifest, options.manifest_sha256,
                                   "" if folder == "." else folder)
        else:
            result = check_config(options.nt_root)
    except (CheckError, OSError, UnicodeDecodeError) as exc:
        detail = str(exc) if isinstance(exc, CheckError) else type(exc).__name__
        stdout.write(json.dumps({"check": options.command, "error": detail}) + "\n")
        return 2
    stdout.write(json.dumps(result, indent=2) + "\n")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
