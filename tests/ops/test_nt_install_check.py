"""Read-only NT install checks: install-vs-manifest, safety config, and the no-write surface.

All fixtures are synthetic. MARKER, ACCOUNT and CONN stand for private content that
must never reach the output.
"""
import ast
import hashlib
import io
import json
import os
from pathlib import Path

import pytest

import nt_install_check as check

SOURCE_FILE = Path(check.__file__)
MARKER = "SYNTHETIC_PARAM_31337"
ACCOUNT = "ACCT12345"
CONN = "MyFirmConnection"
FROZEN = {"AlphaStrategy-v1.cs": f"class Alpha : Strategy {{ int p = 1; // {MARKER}\r\n}}\r\n",
          "BetaEngine-v2.cs": "class Beta { }\r\n"}


def run(*argv):
    out = io.StringIO()
    code = check.main([str(a) for a in argv], stdout=out)
    text = out.getvalue()
    return code, json.loads(text), text


def age(path, seconds_ago):
    stamp = path.stat().st_mtime - seconds_ago
    os.utime(path, (stamp, stamp))


@pytest.fixture
def nt(tmp_path):
    root = tmp_path / "NinjaTrader 8"
    custom = root / "bin" / "Custom"
    (custom / "Strategies").mkdir(parents=True)
    (custom / "Indicators").mkdir()
    (custom / "AddOns").mkdir()
    (custom / "ExportNinjaScript").mkdir()
    (root / "trace").mkdir()
    (root / "workspaces").mkdir()
    frozen = tmp_path / "frozen"
    frozen.mkdir()
    lines = []
    for name, text in FROZEN.items():
        (frozen / name).write_bytes(text.encode())
        (custom / "Strategies" / name).write_bytes(text.encode())
        lines.append(f"{hashlib.sha256(text.encode()).hexdigest()} *{name}")
    (frozen / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (custom / "Strategies" / "@Strategy.cs").write_text("stock", encoding="utf-8")
    (custom / "Indicators" / "@SMA.cs").write_text("stock", encoding="utf-8")
    (custom / "AssemblyInfo.cs").write_text("stock", encoding="utf-8")
    (custom / "NinjaTrader.Custom.csproj").write_text(
        '<Project xmlns="http://schemas.microsoft.com/developer/msbuild/2003"><ItemGroup>'
        '<Compile Include="Indicators\\%40SMA.cs" /><Compile Include="Strategies\\%40Strategy.cs" />'
        '<Reference Include="System.Core" /><Reference Include="NinjaTrader.Core" />'
        '</ItemGroup></Project>', encoding="utf-8")
    for path in custom.rglob("*.cs"):
        age(path, 3600)
    (custom / "NinjaTrader.Custom.dll").write_bytes(b"MZ synthetic assembly System.Core")
    (custom / "NinjaTrader.Vendor.dll").write_bytes(b"MZ")
    (root / "trace" / "trace.20261106.00000.txt").write_text(
        "******************* Session Start (Version 8.1.8.4) *******************\n",
        encoding="utf-8")
    (root / "Config.xml").write_text(config_xml(), encoding="utf-8")
    (root / "workspaces" / "_Workspaces.xml").write_text(
        "<NinjaTrader><ActiveWorkspace>Blank</ActiveWorkspace></NinjaTrader>", encoding="utf-8")
    return root, frozen / "SHA256SUMS"


def config_xml(ati="false", entries="false", exits="false", tradovate="false",
               simulator="true"):
    return (
        "<NinjaTrader>"
        f"<CachedConnectionTokens><{ACCOUNT}><CachedTokenExpiration>x</CachedTokenExpiration>"
        f"</{ACCOUNT}></CachedConnectionTokens>"
        "<ConnectOptions>"
        f"<SimulatorOptions><Name>Simulated Data Feed</Name><ConnectOnStartup>{simulator}"
        "</ConnectOnStartup></SimulatorOptions>"
        f"<TradovateOptions><Name>{CONN}</Name><User>{ACCOUNT}</User>"
        f"<ConnectOnStartup>{tradovate}</ConnectOnStartup></TradovateOptions>"
        "</ConnectOptions>"
        f"<AtiOptions><AtiOptions><IsAtiEnabled>{ati}</IsAtiEnabled></AtiOptions></AtiOptions>"
        "<StrategiesOptions><StrategiesOptions>"
        f"<CancelEntriesOnStrategyDisable>{entries}</CancelEntriesOnStrategyDisable>"
        f"<CancelExitsOnStrategyDisable>{exits}</CancelExitsOnStrategyDisable>"
        "</StrategiesOptions></StrategiesOptions>"
        "</NinjaTrader>")


def install(root, manifest, *extra):
    return run("--nt-root", root, "install", "--manifest", manifest, *extra)


# --- install -------------------------------------------------------------------------

def test_matching_install_passes(nt):
    root, manifest = nt
    pin = hashlib.sha256(manifest.read_bytes()).hexdigest()
    code, result, text = install(root, manifest, "--manifest-sha256", pin)
    assert code == 0 and result["pass"], result
    assert result["files"] == {name: "match" for name in FROZEN}
    assert result["manifest_pin_ok"] is True
    assert result["extra"] == [] and result["dll_newer_than_sources"] is True
    assert result["nt_version"] == "8.1.8.4"
    assert MARKER not in text


def test_changed_and_missing_files_fail(nt):
    root, manifest = nt
    strategies = root / "bin" / "Custom" / "Strategies"
    (strategies / "AlphaStrategy-v1.cs").write_bytes(b"class Alpha : Strategy { int p = 2; }\r\n")
    (strategies / "BetaEngine-v2.cs").unlink()
    code, result, _ = install(root, manifest)
    assert code == 1 and not result["pass"]
    assert result["files"] == {"AlphaStrategy-v1.cs": "differ", "BetaEngine-v2.cs": "missing"}


def test_line_ending_only_difference_is_named_and_still_fails(nt):
    root, manifest = nt
    target = root / "bin" / "Custom" / "Strategies" / "BetaEngine-v2.cs"
    target.write_bytes(b"\xef\xbb\xbfclass Beta { }\n")
    age(target, 3600)
    code, result, _ = install(root, manifest)
    assert code == 1
    assert result["files"]["BetaEngine-v2.cs"] == "differ-eol-or-bom-only"


def test_extra_compiled_sources_fail_but_stock_and_export_do_not(nt):
    root, manifest = nt
    custom = root / "bin" / "Custom"
    (custom / "Indicators" / "Old").mkdir()
    (custom / "Indicators" / "Old" / "StaleCopy.cs").write_text("x", encoding="utf-8")
    (custom / "ExportNinjaScript" / "Staged.cs").write_text("x", encoding="utf-8")
    project = custom / "NinjaTrader.Custom.csproj"
    project.write_text(project.read_text(encoding="utf-8").replace(
        "</ItemGroup>", '<Compile Include="AddOns\\Ghost.cs" /></ItemGroup>'), encoding="utf-8")
    for path in custom.rglob("*.cs"):
        age(path, 3600)
    code, result, _ = install(root, manifest)
    assert code == 1
    assert result["extra"] == ["AddOns/Ghost.cs", "Indicators/Old/StaleCopy.cs"]


def test_stale_dll_fails(nt):
    root, manifest = nt
    dll = root / "bin" / "Custom" / "NinjaTrader.Custom.dll"
    age(dll, 7200)
    code, result, _ = install(root, manifest)
    assert code == 1 and result["dll_newer_than_sources"] is False
    assert "compiled DLL is older than a compiled source or the compile project" in result["failures"]


def test_project_newer_than_dll_fails(nt):
    """Dropping a source from the compile project changes what compiles: rebuild needed."""
    root, manifest = nt
    custom = root / "bin" / "Custom"
    age(custom / "NinjaTrader.Custom.dll", 1800)
    code, result, _ = install(root, manifest)
    assert code == 1 and result["dll_newer_than_sources"] is False
    assert result["files"] == {name: "match" for name in FROZEN} and result["extra"] == []


def test_wrong_manifest_pin_fails(nt):
    root, manifest = nt
    code, result, _ = install(root, manifest, "--manifest-sha256", "0" * 64)
    assert code == 1 and result["manifest_pin_ok"] is False


@pytest.mark.parametrize("line", ["../escape.cs", "C:/abs.cs", "sub\\name.cs"])
def test_unsafe_manifest_names_are_errors(nt, line):
    root, manifest = nt
    manifest.write_text(f"{'a' * 64} *{line}\n", encoding="utf-8")
    code, result, _ = install(root, manifest)
    assert code == 2 and "unsafe" in result["error"]


@pytest.mark.parametrize("argv", [["--manifest-sha256", "xyz"], ["--folder", "../x"]])
def test_bad_arguments_are_errors(nt, argv):
    root, manifest = nt
    code, result, _ = install(root, manifest, *argv)
    assert code == 2 and "error" in result


def test_link_under_custom_fails(nt, tmp_path):
    root, manifest = nt
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "Hidden.cs").write_text("x", encoding="utf-8")
    try:
        (root / "bin" / "Custom" / "Indicators" / "linked").symlink_to(outside, target_is_directory=True)
    except OSError:
        pytest.skip("symlinks need privileges on this host")
    code, result, _ = install(root, manifest)
    assert code == 1 and "link under bin/Custom: Indicators/linked" in result["failures"]
    assert result["extra"] == []


# --- config --------------------------------------------------------------------------

def config(root):
    return run("--nt-root", root, "config")


def test_safe_config_passes_and_never_prints_names(nt):
    root, _ = nt
    code, result, text = config(root)
    assert code == 0 and result["pass"], result
    assert result["ati_enabled"] is False
    assert result["cancel_entries_on_disable"] is False
    assert result["cancel_exits_on_disable"] is False
    assert (result["connections"], result["live_connect_on_startup"],
            result["simulated_connect_on_startup"]) == (2, 0, 1)
    for private in (ACCOUNT, CONN, MARKER, "<"):
        assert private not in text


@pytest.mark.parametrize("change, failure", [
    ({"ati": "true"}, "ATI enabled: on"),
    ({"entries": "true"}, "cancel entries on strategy disable: on"),
    ({"exits": "true"}, "cancel exits on strategy disable: on"),
    ({"tradovate": "true"}, "1 non-simulated connection(s) connect on startup"),
])
def test_unsafe_settings_fail(nt, change, failure):
    root, _ = nt
    (root / "Config.xml").write_text(config_xml(**change), encoding="utf-8")
    code, result, text = config(root)
    assert code == 1 and failure in result["failures"]
    assert ACCOUNT not in text and CONN not in text


def test_missing_setting_fails(nt):
    root, _ = nt
    (root / "Config.xml").write_text("<NinjaTrader />", encoding="utf-8")
    code, result, _ = config(root)
    assert code == 1 and "ATI enabled: setting not found" in result["failures"]


def test_saved_strategies_in_workspaces_are_counted(nt):
    root, _ = nt
    (root / "workspaces" / "recovery").mkdir()
    (root / "workspaces" / "recovery" / "ws.xml").write_text(
        '<NinjaTrader xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        "<Item><Type>NinjaTrader.NinjaScript.Strategies.SampleMACrossOver</Type></Item>"
        '<Item xsi:type="Alpha"><Account>' + ACCOUNT + "</Account></Item>"
        "</NinjaTrader>", encoding="utf-8")
    code, result, text = config(root)
    assert code == 1 and result["workspace_strategy_entries"] == 2
    assert ACCOUNT not in text


def test_addons_and_non_stock_assemblies_fail(nt):
    root, _ = nt
    custom = root / "bin" / "Custom"
    (custom / "AddOns" / "Bridge.cs").write_text("x", encoding="utf-8")
    (custom / "SomeBridge.dll").write_bytes(b"MZ")
    code, result, _ = config(root)
    assert code == 1
    assert result["addon_source_files"] == 1 and result["non_stock_dlls"] == ["SomeBridge.dll"]


def test_non_stock_reference_fails_when_compiled_in_and_warns_when_dangling(nt):
    root, _ = nt
    custom = root / "bin" / "Custom"
    project = custom / "NinjaTrader.Custom.csproj"
    project.write_text(project.read_text(encoding="utf-8").replace(
        "</ItemGroup>", '<Reference Include="Vendor_AddOn_v1, Version=1.0" /></ItemGroup>'),
        encoding="utf-8")
    code, result, _ = config(root)
    assert code == 0 and result["warnings"]
    assert result["non_stock_references"] == [
        {"name": "Vendor_AddOn_v1", "file_present": False, "in_compiled_dll": False}]
    (custom / "NinjaTrader.Custom.dll").write_bytes(b"MZ refs Vendor_AddOn_v1 System.Core")
    code, result, _ = config(root)
    assert code == 1 and "non-stock reference in use: Vendor_AddOn_v1" in result["failures"]


def test_reference_resolved_through_hint_path_fails(nt, tmp_path):
    root, _ = nt
    external = tmp_path / "elsewhere"
    external.mkdir()
    (external / "Bridge.dll").write_bytes(b"MZ")
    project = root / "bin" / "Custom" / "NinjaTrader.Custom.csproj"
    project.write_text(project.read_text(encoding="utf-8").replace(
        "</ItemGroup>", '<Reference Include="Bridge"><HintPath>'
        + str(external / "Bridge.dll") + "</HintPath></Reference></ItemGroup>"), encoding="utf-8")
    code, result, _ = config(root)
    assert code == 1 and "non-stock reference in use: Bridge" in result["failures"]
    assert result["non_stock_references"][0]["file_present"] is True


def test_linked_workspace_fails_instead_of_counting_zero(nt, tmp_path):
    root, _ = nt
    outside = tmp_path / "outside.xml"
    outside.write_text("<NinjaTrader><T>NinjaTrader.NinjaScript.Strategies.X</T></NinjaTrader>",
                       encoding="utf-8")
    try:
        (root / "workspaces" / "linked.xml").symlink_to(outside)
    except OSError:
        pytest.skip("symlinks need privileges on this host")
    code, result, _ = config(root)
    assert code == 1
    assert "link under workspaces, not inspected: linked.xml" in result["failures"]


def test_malformed_xml_is_an_error_without_content(nt):
    root, _ = nt
    (root / "Config.xml").write_text(f"<NinjaTrader><User>{ACCOUNT}</NinjaTrader", encoding="utf-8")
    code, result, text = config(root)
    assert code == 2 and ACCOUNT not in text


# --- surface -------------------------------------------------------------------------

def test_module_has_no_write_or_network_surface():
    tree = ast.parse(SOURCE_FILE.read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported |= {alias.name.split(".")[0] for alias in node.names}
        elif isinstance(node, ast.ImportFrom):
            imported.add((node.module or "").split(".")[0])
    forbidden = {"socket", "http", "urllib", "requests", "subprocess", "ctypes", "asyncio",
                 "shutil", "tempfile", "ssl", "multiprocessing", "os"}
    assert not imported & forbidden
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", None)
            assert name not in {"write_text", "write_bytes", "unlink", "rename", "replace",
                                "mkdir", "rmdir", "touch", "symlink_to", "chmod", "utime"} or (
                isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name)
                and func.value.id == "stdout"), ast.unparse(node)
            if name == "open":
                assert len(node.args) >= 2 and isinstance(node.args[1], ast.Constant)
                assert node.args[1].value == "rb"
