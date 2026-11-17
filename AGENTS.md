# AGENTS.md — Instructions for AI agents building PortableApps.com packages

You are using this repository as your knowledge base for creating
PortableApps.com Format packages (`.paf.exe` installers with a
PortableApps.com Launcher). Follow these rules exactly.

## Non-negotiable rules

1. **Never invent INI keys, section names, or values.** Every key you write
   in `appinfo.ini`, `installer.ini`, or a launcher INI must appear in
   `docs/01-format-spec.md`, `docs/02-installer-and-installer-ini.md`, or
   `docs/04-launcher-ini-reference.md`. Two documented exception classes
   live elsewhere: the production-verified environment variables in
   `docs/06-environment-variables.md`, and patterns in the mirrored
   production configs under `examples/real-world/` (borrow patterns
   only — reconcile every value against docs/01–04). If a behaviour you
   need is not covered by a documented key, the correct tool is custom
   NSIS code (`docs/05-launcher-advanced-custom-code.md`) — say so
   explicitly instead of guessing a key name.
2. **Case and spelling matter.** Section names and keys are matched by the
   tools as written in the references. Paths inside the package use Windows
   backslashes (`App\AppName\AppName.exe`).
3. **Versions:**
   - `[Format] Version` in `appinfo.ini` is the Format version: `3.9`.
   - `[Version] PackageVersion` is always exactly four numeric parts:
     `x.x.x.x` (for example `2.4.0.1`). No letters, no suffixes.
   - `[Version] DisplayVersion` is the human version (for example
     `2.4 Revision 1`). It never drives upgrade comparisons.
4. **Naming:**
   - Package folder: `AppNamePortable` (no spaces).
   - `AppID` equals the folder name for official-style packages.
   - Launcher INI file: `App\AppInfo\Launcher\<AppID>.ini` — the file name
     matches the AppID, for example `AppNamePortable.ini`. (Older packages
     used a single `launcher.ini`; the per-app named file inside the
     `Launcher` folder is the current convention.)
   - Generated launcher: `<AppID>.exe` in the package root, and
     `[Control] Start` in `appinfo.ini` must name exactly that file.
   - Installer output file: `<AppID>_<DisplayVersion>.paf.exe`, for example
     `AppNamePortable_1.2.paf.exe`. Online installers end in
     `_online.paf.exe`.
5. **Data separation is the whole point.** Binaries go in `App\`, all user
   data and settings go in `Data\`, sources/licences/readmes go in
   `Other\Source\`. Nothing user-specific may be written into `App\` at
   runtime, and no binaries may live in `Data\`.
6. **Leave no trace.** A package may touch the host registry/files while
   running only if it restores the host to its exact pre-run state on exit
   (back up a local copy's settings, restore them afterwards). See the
   Format's host-modification rule in `docs/01-format-spec.md`.
7. **Use the current tools.** Every release must be built with the current
   PortableApps.com Installer; a package built with an installer version
   more than 30 days superseded may not be released as current. Current
   versions are recorded in `docs/11-tools-and-versions.md`.
8. **Licensing is a hard gate, not a detail.** Check
   `docs/09-licensing-permissions-submission.md` before packaging anything
   you did not write. Freeware may only be packaged by its publisher or
   with the publisher's express consent, and only with the unmodified
   official installer.
9. **Start from the templates.** Copy `templates/MinimalAppPortable/` and
   the closest file in `examples/` — the mirrored production configs in
   `examples/real-world/` outrank the synthetic examples — then edit.
   Do not write configuration files from scratch from memory.
10. **Verify before declaring done.** Run every applicable item in
    `checklists/package-checklist.md` and
    `checklists/pre-release-checklist.md`. State plainly which checks were
    run and which could not be run (for example Windows-only runtime
    behaviour when working from a non-Windows machine) — label those
    **Unverified** rather than claiming success.

## Security rules (full treatment: `docs/18-security-privacy-and-abuse.md`)

- **Verify the base app before bundling it**: publisher's canonical URL,
  signature/published hash checked, source URL + SHA-256 recorded.
- **Online installers: HTTPS + `DownloadSHA256`, always.** A hash proves
  the payload is the file the packager chose, not that it is safe.
- **Custom code is code.** Read every line of any `.nsh` file before
  generating — never copy one unread from AppConfigs, a forum, or a
  template repo.
- **Least elevation**: `RunAsAdmin=none` by default; `try` before
  `force`; `compile-force` only with a written justification.
- **Never route around the services boundary**: services are disabled in
  PAL 2.2; do not implement them in custom code.
- **Scope the Force cleanup sections** to trees your trace inventory
  proved; they delete unconditionally on every exit and can destroy a
  local install's data.
- **No code through `Data`** — never move DLLs/scripts through it.
- **Never ship `Debug.nsh`** or a `Data\debug.log` in a release.

## Build order (always in this sequence)

1. Analyse the base app: where does it store settings (registry, `%APPDATA%`,
   `%LOCALAPPDATA%`, its own folder, documents folder)? Does it write
   anywhere else? Use a clean VM / Windows Sandbox + RegShot-style
   before/after comparison (`docs/07-end-to-end-workflow.md`).
2. Lay out the package tree from the template.
3. Write `appinfo.ini`.
4. Write the launcher INI to redirect/move/backup everything found in
   step 1.
5. Generate the launcher with the PortableApps.com Launcher Generator.
6. Test the extracted package (never only the installed one): first run,
   settings persistence, drive-letter change, second run, exit cleanliness,
   local-copy coexistence (`docs/08-testing-debugging-troubleshooting.md`).
7. Write `installer.ini` only if defaults are not enough (online download,
   optional components, upgrade preservation, etc.).
8. Build the `.paf.exe` with the PortableApps.com Installer wizard.
9. Install the built `.paf.exe` to a fresh location and repeat step 6
   against the installed copy.
10. Complete the pre-release checklist.

## Things that are always wrong

- `PackageVersion` with fewer/more than 4 parts, or containing text.
- A category that is not one of the 10 fixed values (Accessibility,
  Development, Education, Games, Graphics & Pictures, Internet,
  Music & Video, Office, Security, Utilities).
- A description longer than 512 characters in `appinfo.ini`.
- Double quotes inside `appinfo.ini` / `installer.ini` field values.
- Settings left in `%APPDATA%` or the registry after the app exits.
- Hard-coded drive letters or absolute paths in launcher configuration —
  use PAL variables (`%PAL:DataDir%`, `%PAL:AppDir%`, …) from
  `docs/06-environment-variables.md`.
- Including the generated `pac_installer_log.ini` in a source repository
  (add it to `.gitignore`).
- Copying the specification's full example `installer.ini` into a project —
  it is illustrative only. Build `installer.ini` from scratch with only
  the features the package needs.
- Modifying the PortableApps.com Installer's own code inside a package.
  Installer customisation goes in
  `Other\Source\PortableApps.comInstallerCustom.nsh` only.
