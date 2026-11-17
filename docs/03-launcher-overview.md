# 03 — PortableApps.com Launcher (PAL) Overview

The PortableApps.com Launcher makes an ordinary Windows application
portable **without modifying the application's code**. Current version:
**2.2.9 (2024-05-25)**; the manual documents PAL 2.2.

## What it is

PAL is a **generator**, not a runtime library:

1. You write one configuration file:
   `App\AppInfo\Launcher\<AppID>.ini` (see
   `docs/04-launcher-ini-reference.md`).
2. You run the **PortableApps.com Launcher Generator**
   (`PortableApps.comLauncherGenerator.exe` from the Launcher package)
   and point it at your package folder.
3. The Generator validates the INI and **compiles** a small native
   launcher, `<AppID>.exe`, into the package root, using NSIS. Only the
   subsystems you activated (`[Activate]`) are compiled in, which keeps
   the launcher small and fast.
4. End users run `<AppID>.exe`. There is no separate PAL runtime to
   install.

Changing the INI — especially `[Activate]` values that add plug-ins —
requires **regenerating** the launcher. The generated exe and the INI must
always be kept in sync; ship the INI in the package (in
`App\AppInfo\Launcher`) so the package can be rebuilt.

**Generator prerequisites (manual, quickstart):** install the Launcher
and **NSIS Portable, the Unicode variant** — for automatic detection,
NSIS Portable must sit in a **sibling directory named `NSISPortable`**
next to the Launcher (recommended layout: `X:\PortableApps\PortableApps.comLauncher`
and `X:\PortableApps\NSISPortable`). The ANSI NSIS variant is not used.
Run the Generator from its install directory or from the Platform, pass
it the package's main folder (`AppNamePortable`), and it compiles
`<AppID>.exe` into that folder. Re-run it after **any** change to the
launcher INI, `Custom.nsh`, or `Debug.nsh` — all three are compiled in.
(The current Launcher release notes also describe an NSIS core bundled
with the builder; the manual's sibling-install instruction above is the
documented 2.2 route — if your Generator finds NSIS by itself, that is
the bundled core at work.)

## What the generated launcher does at runtime

In order, roughly:

1. **Pre-flight checks** — OS version (`MinOS`/`MaxOS`), single-instance
   rules, UNC/spaces-in-path policies, admin elevation (`RunAsAdmin`),
   Java discovery (`[Activate] Java`).
2. **First-run setup** — if `Data` is empty/missing, populate it from
   `App\DefaultData`.
3. **Live mode decision** — if the package is on read-only media (or the
   user set `RunLocally=true`), copy app/data to a temp folder and run
   from there (`[LiveMode]`).
4. **Backup of local state** — for every registry key, file, and directory
   PAL manages, any pre-existing **local** copy's data is backed up (e.g.
   `<name>-BackupBy<AppID>`), so a locally installed copy of the same app
   is never harmed.
5. **Redirection in** — portable registry keys are imported from
   `Data\settings\*.reg`; portable files/directories are copied/moved to
   the locations the app expects (`%APPDATA%`, etc.); `[FileWriteN]`
   rewrites stored paths for the current drive/location; `[Environment]`
   variables are set; `[RegistryValueWrite]` values are applied;
   a contained TEMP directory is assigned (`CleanTemp`).
6. **Splash screen** (unless disabled) and **launch** of
   `ProgramExecutable` with `CommandLineArguments` plus any arguments the
   user passed to the launcher.
7. **Waiting** — the launcher waits for the app (and any `WaitForEXE`
   children) to exit, so cleanup cannot run early.
8. **Redirection back out** — changed registry keys are exported back to
   `Data\settings\*.reg`; files/directories are moved back into `Data`;
   values written only for the run are removed; cleanup sections delete
   leftovers (`[RegistryCleanup*]`, `[DirectoriesCleanup*]`,
   `[QtKeysCleanup]`).
9. **Restore of local state** — the backups from step 4 are restored, so
   the host PC is exactly as it was before the run. This is how PAL
   satisfies the Format's host-modification rule.

If the launcher detects an unclean previous exit (crash, power loss), it
recovers on the next launch: it restores the local backups and re-saves
the portable state rather than losing either.

## The portability techniques (choose per trace)

From least to most invasive — prefer the earliest that works:

1. **The app's own portable mode** — a command-line switch, a
   settings-next-to-exe mode, or an official portable build. Use
   `CommandLineArguments` / `[Environment]` to engage it.
2. **Environment redirection** — many apps honour variables like
   `%APPDATA%`-style overrides or their own `*_HOME` variable; set them in
   `[Environment]` to point inside `Data`.
3. **File/directory moves** — `[FilesMove]` / `[DirectoriesMove]` shuttle
   settings between `Data` and the expected location around the run.
4. **Registry save/restore** — `[RegistryKeys]` (+ cleanup sections).
5. **Path rewriting** — `[FileWriteN]` fixes absolute paths stored inside
   settings files when the drive letter or folder changes.
6. **Value writes** — `[RegistryValueWrite]` forces individual values for
   the portable run.
7. **Custom NSIS code** — for anything the INI cannot express; see
   `docs/05-launcher-advanced-custom-code.md`.

## User configuration

End users can place `<AppID>.ini` next to the launcher exe to set
`AdditionalParameters`, `DisableSplashScreen`, and `RunLocally` — see the
end of `docs/04-launcher-ini-reference.md`. Packages ship an example of
this file in `Other\Source`.

## Hard limits to know

- PAL cannot make an app portable if it requires a kernel driver or a
  permanently installed Windows service — `[ServiceN]` exists in the INI
  reference but **services are currently disabled** in PAL 2.2.
- PAL launchers are Windows executables compiled with NSIS; there is no
  macOS/Linux variant.
- The launcher can only clean up what it knows about: every trace the app
  leaves must be covered by the INI (or custom code), which is why the
  analysis phase in `docs/07-end-to-end-workflow.md` matters.
