#!/usr/bin/env python3
"""check-package.py — static checks for a PortableApps.com package tree.

Usage: python3 check-package.py path/to/AppNamePortable

Checks (rules from AGENTS.md, docs/01, docs/02, docs/04 of the PafDev
repo; the same inventories live in paf-data.json next to this script):

  appinfo.ini
    - App\\AppInfo\\appinfo.ini exists and parses as INI.
    - [Format] Type=PortableApps.comFormat, Version=3.9.
    - [Details] Name, AppID, Publisher, Homepage, Category,
      Description, Language present; AppID equals the folder name;
      Category is one of the 10 fixed values; Description <= 512
      chars; no double quotes in any value.
    - [Version] PackageVersion is exactly 4 numeric parts;
      DisplayVersion present.
    - [Control] Start names <AppID>.exe; Icons count matches the
      appicon PNG set (warning only — icons are binary and are often
      added after the config).
  Launcher INI
    - App\\AppInfo\\Launcher\\<AppID>.ini exists (a file named
      launcher.ini, or an INI whose name does not match the AppID,
      is a failure).
    - Every section name is a documented PAL section (unknown INI
      sections/keys fail SILENTLY in the Launcher — that is why this
      check exists). Numbered families FileWriteN / ServiceN allowed.
    - [Launch] ProgramExecutable present, and its target exists under
      App\\ (warning only — binaries may not be copied in yet).
    - [Launch] and [Activate] keys are from the documented key lists.
  installer.ini (optional)
    - If present, every section is a documented installer section.
  Layout
    - help.html in the package root (warning), Data\\ directory
      present, Other\\Source\\Readme.txt present (warning).

Exit code: 0 = no failures, 1 = at least one FAIL. Warnings do not
fail the run. Python 3, standard library only.
"""

import configparser
import os
import re
import sys

FAIL = "FAIL"
WARN = "WARN"
OK = "OK  "

FORMAT_VERSION = "3.9"
CATEGORIES = [
    "Accessibility", "Development", "Education", "Games",
    "Graphics & Pictures", "Internet", "Music & Video", "Office",
    "Security", "Utilities",
]
LAUNCHER_SECTIONS = {
    "Activate", "DirectoriesCleanupForce", "DirectoriesCleanupIfEmpty",
    "DirectoriesMove", "Environment", "FilesMove", "Language",
    "LanguageFile", "LanguageStrings", "Launch", "LiveMode",
    "QtKeysCleanup", "RegistryCleanupForce", "RegistryCleanupIfEmpty",
    "RegistryKeys", "RegistryValueBackupDelete", "RegistryValueWrite",
}
LAUNCHER_NUMBERED = ("FileWrite", "Service")  # FileWrite1, Service2, ...
LAUNCH_KEYS = {
    "AdditionalParameters", "CleanTemp", "CloseEXE",
    "CommandLineArguments", "DirectoryMoveOK", "DisableSplashScreen",
    "HideCommandLineWindow", "LaunchAppAfterSplash", "MaxOS", "MinOS",
    "NoSpacesInPath", "ProgramExecutable",
    "ProgramExecutableWhenParameters", "RefreshShellIcons",
    "RunAsAdmin", "RunAsAdminVista", "RunAsAdminXP", "RunLocally",
    "SingleAppInstance", "SinglePortableAppInstance", "SplashTime",
    "SupportsUNC", "WaitForOtherInstances", "WaitForProgram",
    "WorkingDirectory",
}
ACTIVATE_KEYS = {"INI", "Java", "Registry", "XML"}
INSTALLER_SECTIONS = {
    "CheckRunning", "CopyLocalFiles", "DirectoriesToPreserve",
    "DownloadFiles", "FilesToPreserve", "Languages", "LegacyVersions",
    "MainDirectories", "OptionalComponents", "Source",
}


def read_ini(path):
    parser = configparser.ConfigParser(strict=False)
    parser.optionxform = str  # preserve key case
    with open(path, encoding="utf-8-sig", errors="replace") as fh:
        parser.read_file(fh)
    return parser


def section_of(parser, name):
    for s in parser.sections():
        if s.lower() == name.lower():
            return s
    return None


def get(parser, section, key):
    s = section_of(parser, section)
    if s is None:
        return None
    for k, v in parser.items(s):
        if k.lower() == key.lower():
            return v.strip()
    return None


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    root = sys.argv[1].rstrip("/\\")
    folder = os.path.basename(root)
    failures = 0

    def report(level, msg):
        nonlocal failures
        if level == FAIL:
            failures += 1
        print(f"{level} {msg}")

    if not os.path.isdir(root):
        report(FAIL, f"not a directory: {root}")
        return 1

    # ---------- appinfo.ini ----------
    appinfo_path = os.path.join(root, "App", "AppInfo", "appinfo.ini")
    appid = None
    if not os.path.exists(appinfo_path):
        report(FAIL, "App/AppInfo/appinfo.ini missing")
    else:
        try:
            info = read_ini(appinfo_path)
        except configparser.Error as exc:
            report(FAIL, f"appinfo.ini does not parse: {exc}")
            info = None
        if info is not None:
            if get(info, "Format", "Type") != "PortableApps.comFormat":
                report(FAIL, "[Format] Type must be PortableApps.comFormat")
            if get(info, "Format", "Version") != FORMAT_VERSION:
                report(FAIL, f"[Format] Version must be {FORMAT_VERSION} "
                             f"(found: {get(info, 'Format', 'Version')!r})")
            else:
                report(OK, "appinfo.ini [Format] Type/Version correct")

            for key in ("Name", "AppID", "Publisher", "Homepage",
                        "Category", "Description", "Language"):
                if not get(info, "Details", key):
                    report(FAIL, f"[Details] {key} missing or empty")
            appid = get(info, "Details", "AppID")
            if appid and appid != folder:
                report(FAIL, f"AppID {appid!r} does not equal the folder "
                             f"name {folder!r}")
            elif appid:
                report(OK, f"AppID matches folder name ({appid})")
            cat = get(info, "Details", "Category")
            if cat and cat not in CATEGORIES:
                report(FAIL, f"Category {cat!r} is not one of the 10 fixed values")
            desc = get(info, "Details", "Description") or ""
            if len(desc) > 512:
                report(FAIL, f"Description is {len(desc)} chars (max 512)")
            for s in info.sections():
                for k, v in info.items(s):
                    if '"' in v:
                        report(FAIL, f"double quote in appinfo value [{s}] {k}")
            pv = get(info, "Version", "PackageVersion") or ""
            if re.fullmatch(r"\d+\.\d+\.\d+\.\d+", pv):
                report(OK, f"PackageVersion {pv} (4 numeric parts)")
            else:
                report(FAIL, f"PackageVersion {pv!r} is not exactly 4 numeric parts")
            if not get(info, "Version", "DisplayVersion"):
                report(FAIL, "[Version] DisplayVersion missing")
            start = get(info, "Control", "Start")
            if appid and start != f"{appid}.exe":
                report(FAIL, f"[Control] Start must be {appid}.exe (found: {start!r})")
            elif start:
                report(OK, f"[Control] Start = {start}")
            icons = get(info, "Control", "Icons")
            if icons and icons.isdigit():
                appinfo_dir = os.path.dirname(appinfo_path)
                have = [f for f in os.listdir(appinfo_dir)
                        if f.startswith("appicon_") and f.endswith(".png")]
                if not os.path.exists(os.path.join(appinfo_dir, "appicon.ico")):
                    report(WARN, "appicon.ico missing (binary — add before release)")
                if len(have) < int(icons):
                    report(WARN, f"appicon PNG set incomplete ({len(have)} found) — "
                                 "see docs/01 for the required sizes")

    # ---------- Launcher INI ----------
    launcher_dir = os.path.join(root, "App", "AppInfo", "Launcher")
    if appid:
        launcher_path = os.path.join(launcher_dir, appid + ".ini")
        if os.path.isdir(launcher_dir):
            inis = [f for f in os.listdir(launcher_dir) if f.endswith(".ini")]
            if os.path.exists(launcher_path):
                report(OK, f"launcher INI named for the AppID ({appid}.ini)")
            else:
                report(FAIL, f"App/AppInfo/Launcher/{appid}.ini missing "
                             f"(found: {inis or 'none'}) — the file name must match the AppID")
                launcher_path = None
        else:
            report(FAIL, "App/AppInfo/Launcher directory missing")
            launcher_path = None
        if launcher_path:
            try:
                lc = read_ini(launcher_path)
            except configparser.Error as exc:
                report(FAIL, f"launcher INI does not parse: {exc}")
                lc = None
            if lc is not None:
                for s in lc.sections():
                    base = re.match(r"^([A-Za-z]+?)(\d+)$", s)
                    if s in LAUNCHER_SECTIONS:
                        continue
                    if base and base.group(1) in LAUNCHER_NUMBERED:
                        continue
                    report(FAIL, f"launcher INI section [{s}] is not a documented "
                                 "PAL section — unknown sections fail silently (docs/04)")
                ls = section_of(lc, "Launch")
                if ls is None:
                    report(FAIL, "launcher INI has no [Launch] section")
                else:
                    for k, _v in lc.items(ls):
                        if k not in LAUNCH_KEYS:
                            report(FAIL, f"[Launch] key {k!r} is not a documented "
                                         "key — unknown keys fail silently (docs/04)")
                    prog = get(lc, "Launch", "ProgramExecutable")
                    if not prog:
                        report(FAIL, "[Launch] ProgramExecutable missing")
                    else:
                        target = os.path.join(root, "App", prog.replace("\\", os.sep))
                        if os.path.exists(target):
                            report(OK, f"ProgramExecutable target exists: {prog}")
                        else:
                            report(WARN, f"ProgramExecutable target not in the tree "
                                         f"yet: {prog}")
                act = section_of(lc, "Activate")
                if act is not None:
                    for k, _v in lc.items(act):
                        if k not in ACTIVATE_KEYS:
                            report(FAIL, f"[Activate] key {k!r} is not a documented "
                                         "key (docs/04)")

    # ---------- installer.ini ----------
    inst_path = os.path.join(root, "App", "AppInfo", "installer.ini")
    if os.path.exists(inst_path):
        try:
            inst = read_ini(inst_path)
            for s in inst.sections():
                if s not in INSTALLER_SECTIONS:
                    report(FAIL, f"installer.ini section [{s}] is not a documented "
                                 "section (docs/02)")
            else:
                report(OK, "installer.ini sections all documented")
        except configparser.Error as exc:
            report(FAIL, f"installer.ini does not parse: {exc}")

    # ---------- Layout ----------
    if not os.path.exists(os.path.join(root, "help.html")):
        report(WARN, "help.html missing from the package root")
    if not os.path.isdir(os.path.join(root, "Data")):
        report(FAIL, "Data directory missing")
    if not os.path.exists(os.path.join(root, "Other", "Source", "Readme.txt")):
        report(WARN, "Other/Source/Readme.txt missing")

    print()
    print("RESULT:", "FAIL — fix the FAIL lines above" if failures
          else "PASS (warnings are advisory)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
