# 07 — End-to-End Workflow: From Local App to .paf.exe

This is the complete procedure for packaging an existing Windows
application as a PortableApps.com Format package. Follow it in order.

## Phase 0 — Legality and feasibility check

1. Confirm you may package the app (see
   `docs/09-licensing-permissions-submission.md`): open source → check the
   license; freeware → publisher or publisher's written consent only;
   commercial → do not proceed without an agreement.
2. Confirm the app *can* be portable: it must not require a kernel driver,
   a Windows service that cannot be started/stopped portably, or machine
   activation tied to hardware IDs. Apps needing admin rights must declare
   `RequiresAdmin=yes` in `appinfo.ini`.
3. Get the official tools (`docs/11-tools-and-versions.md`):
   PortableApps.com Launcher, PortableApps.com Installer, and the
   PortableApps.com Application Template (commented reference configs).

## Phase 1 — Analyse the base app (find every trace)

Work in a **clean** environment: a fresh Windows VM, Windows Sandbox, or a
snapshot you can revert. Never analyse on a machine where the app was
previously installed — leftover traces corrupt the results.

1. Snapshot the clean system: registry + file system. **RegShot** is the
   classic tool: take Shot 1.
2. Install the app the normal way (or, if it ships as an archive, extract
   it). Note the install directory and every option the installer offers.
3. Run the app. Change every setting. Create data. Use every major
   feature. Close the app.
4. Take Shot 2 and compare. Record:
   - Registry keys/values created or changed (usually under
     `HKCU\Software\<Publisher>\<App>`, sometimes `HKLM`).
   - Files/folders created or changed: `%APPDATA%`, `%LOCALAPPDATA%`,
     `%USERPROFILE%`, Documents, the install folder itself.
   - Any files written *outside* those (temp files are usually ignorable;
     settings are not).
5. Also test: does the app store paths inside its settings (absolute paths
   break when the drive letter changes)? Does it have a "portable mode"
   switch, a `-portable` flag, or a settings-file-next-to-exe mode? A
   native portable mode always beats launcher redirection.
6. Revert the snapshot. You now have the app's **trace inventory** — every
   item on it must be handled by the launcher or consciously accepted.

## Phase 2 — Lay out the package

1. Copy `templates/MinimalAppPortable/` and rename to `<AppName>Portable`.
2. Put the app's binaries in `App\<AppName>\` (from the local install or
   extracted archive). Remove uninstallers and anything that only serves
   the local installer.
3. Put first-run default settings in `App\DefaultData\` (mirroring the
   structure they should have in `Data\`).
4. Leave `Data\` empty in the distributed package (a placeholder file is
   fine); the launcher populates it from `DefaultData` on first run.
5. Write `help.html` and `Other\Source\Readme.txt` (launcher readme —
   model it on the template in `templates/`).

## Phase 3 — appinfo.ini

Fill in `App\AppInfo\appinfo.ini` from `docs/01-format-spec.md`:

- `[Format] Version=3.9`
- `AppID` = folder name; `Category` from the fixed list of 10;
  `Description` ≤ 512 chars; no double quotes anywhere.
- `[License]` booleans that are *true for this app*.
- `PackageVersion` = app version padded to 4 parts, 4th part = packaging
  revision starting at 1 for a first packaging of that app version
  (convention: app `2.4.4` → `2.4.4.1`).
- `[Dependencies]` for Java/.NET/Ghostscript/64-bit/admin requirements.
- `[Control] Start=<AppID>.exe`; `BaseAppID` (or `NOT-NEEDED`).
- Add the icon set (`appicon.ico` + 5 PNGs) to `App\AppInfo`.

## Phase 4 — launcher.ini

Write `App\AppInfo\Launcher\<AppID>.ini` using
`docs/04-launcher-ini-reference.md`. Map every item from the trace
inventory:

| Trace found | Launcher mechanism |
|---|---|
| Settings in `HKCU\Software\...` | `[Activate] Registry=true` + `[RegistryKeys]` (+ cleanup sections) |
| Settings in `%APPDATA%\App` | `[DirectoriesMove]` or `[FilesMove]` to `%PAL:DataDir%` |
| Single settings file anywhere | `[FilesMove]` |
| App reads a path from a config file | `[FileWriteN]` to rewrite it each launch with `%PAL:DataDir%` |
| App needs an environment variable | `[Environment]` |
| App stores settings in its own folder | Point it at `Data` via its own portable switch if any; otherwise move the settings file with `[FilesMove]` |
| App is Java-based | `[Activate] Java=find` or `Java=require` (finds Java Portable / local Java; `yes` is not a valid value) |
| App is a Qt app writing to registry | `[QtKeysCleanup]` + `[RegistryKeys]` (there is no `[Qt]` section in PAL 2.2 — see `docs/04-launcher-ini-reference.md`) |
| Local copy of same app exists on host | PAL backs up host settings and restores them on exit automatically for the keys/files it manages — verify in testing |

Start from the closest file in `examples/`. Keep the INI minimal: only
sections the app actually needs.

## Phase 5 — Generate the launcher

1. Install/extract the PortableApps.com Launcher package; run
   `PortableApps.comLauncherGenerator.exe` (the Generator).
2. Point it at the package folder (`<AppName>Portable`).
3. It reads `App\AppInfo\Launcher\<AppID>.ini`, validates it, and compiles
   `<AppID>.exe` into the package root using NSIS. Prerequisite
   (`docs/03-launcher-overview.md`): NSIS Portable (**Unicode** variant)
   installed as the sibling folder `NSISPortable` next to
   `PortableApps.comLauncher` — the ANSI variant is not used.
4. Fix every Generator error before continuing. The
   `!include: could not find` warnings for the optional `Custom.nsh` /
   `Debug.nsh` files are harmless when those files are intentionally
   absent (`docs/08-testing-debugging-troubleshooting.md`); any other
   warning about missing files or bad keys means the launcher is not
   done.

## Phase 6 — Test the package folder (before building the installer)

Run the full test matrix in
`docs/08-testing-debugging-troubleshooting.md`. Minimum:

- First run from the folder: defaults appear, app works.
- Change settings, close, reopen: settings persist.
- Copy the folder to a different drive letter / path with spaces and a
  non-ASCII folder name: still works, settings intact.
- Run on a machine (VM) with a **local install of the same app**: local
  settings are untouched after the portable run; portable settings are
  untouched by the local app.
- Exit cleanliness: snapshot registry + file system before/after a full
  run — no leftovers outside the package folder.
- Run as a limited (non-admin) user.
- Run twice / run while already running (single-instance behaviour).

## Phase 7 — installer.ini (only if needed)

Defaults cover most apps. Write `App\AppInfo\installer.ini` only for:
online downloads (`[DownloadFiles]`), optional components, upgrade
preservation/removal tweaks, local-copy import (`[CopyLocalFiles]`), or
legacy-version handling. See `docs/02-installer-and-installer-ini.md`.

## Phase 8 — Build the .paf.exe

1. Run `PortableApps.comInstaller.exe`, point it at the package folder.
2. Output: `<AppID>_<DisplayVersion>.paf.exe` next to the package folder
   (online: `..._online.paf.exe`).
3. Record the Installer version used; confirm it is current (≤30 days
   superseded rule).

## Phase 9 — Test the built installer

1. Install the `.paf.exe` to a **fresh** `PortableApps` folder (ideally a
   different VM/drive than the build tree).
2. Repeat the Phase 6 matrix against the *installed* copy.
3. Upgrade test: install the previous package version, create settings,
   install the new `.paf.exe` over it — settings survive, old binaries
   are gone, `Data` intact.
4. Uninstall expectation: deleting the folder removes everything (there
   is no separate uninstaller; the folder *is* the app).

## Phase 10 — Release

1. Complete `checklists/pre-release-checklist.md`.
2. Name the file exactly `<AppID>_<DisplayVersion>.paf.exe`.
3. Publish with a changelog entry stating the base app version and the
   packaging revision (DisplayVersion), e.g. "2.4 Revision 1".
4. For PortableApps.com publication, post a Development Test release in
   the Portable App Development forum and iterate; see
   `docs/09-licensing-permissions-submission.md`.
