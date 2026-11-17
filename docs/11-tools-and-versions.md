# 11 — Official Tools and Versions

All tools are from https://portableapps.com/development (checked
2026-11-16).

| Tool | Current version | Role |
|---|---|---|
| PortableApps.com Format | 3.9 (2026-03-02) | The specification (`docs/01-format-spec.md`) |
| PortableApps.com Launcher | 2.2.9 (2024-05-25) | Generator that compiles `<AppID>.exe` from the launcher INI (`docs/03`–`06`) |
| PortableApps.com Installer | 3.9.18 (2026-07-20) | Wizard that compiles the `.paf.exe` (`docs/02-installer-and-installer-ini.md`) |
| PortableApps.com Application Template | 3.9.2 (2026-07-11) | Commented reference `appinfo.ini` / `installer.ini` / launcher INI + a default launcher — the official starting skeleton. The templates in this repo mirror its structure |
| PortableApps.com AppCompactor | — | Historically compressed app binaries (UPX-style). **No longer used for official releases** (noted in Format 3.6, 2022). Do not add an `appcompactor.ini` to new packages |
| PortableApps.com Platform | (rolling) | Menu + App Store end users run; see `docs/10-platform-integration.md` |

## Tool-by-tool notes

### PortableApps.com Launcher (Generator)

- Download: the Launcher app page,
  https://portableapps.com/apps/development/portableapps.com_launcher
- Manual: https://portableapps.com/manuals/PortableApps.comLauncher/
- It is itself a portable app: extract/install it anywhere, run
  `PortableApps.comLauncherGenerator.exe`, choose your package folder,
  generate.
- It compiles with NSIS (Unicode variant): install NSIS Portable as the
  sibling folder `NSISPortable` next to `PortableApps.comLauncher` first
  (`docs/03-launcher-overview.md`). If generation fails with a makensis
  error, the full NSIS error is the diagnostic — the INI key or custom
  code it names is the problem.
- Regenerate the launcher after **any** launcher-INI change before
  testing; testing a stale exe against a new INI is a classic false pass.

### PortableApps.com Installer

- Download: https://portableapps.com/apps/development/portableapps.com_installer
- Wizard flow: select the package folder → it validates
  `appinfo.ini`/`installer.ini` → compiles the `.paf.exe` beside the
  folder.
- **Currency rule:** every release must use the current Installer; an
  Installer superseded for more than 30 days on release day is not
  acceptable for a current release.
- The generated installer supports silent operation (used by the
  Platform), a `/DESTINATION=`-style target override, and writes
  `pac_installer_log.ini` into installed packages (exclude from source
  control).

### NSIS

Both tools are built on NSIS (Unicode). You only need NSIS knowledge
directly when writing custom code:

- Launcher: `App\AppInfo\Launcher\Custom.nsh` (PAL 2.1+; in PAL 2.0 it
  was `Other\Source\PortableApps.comLauncherCustom.nsh`)
- Installer: `Other\Source\PortableApps.comInstallerCustom.nsh`

See `docs/05-launcher-advanced-custom-code.md` and
`docs/02-installer-and-installer-ini.md`.

### Analysis tools (not PortableApps.com products)

- **RegShot** — registry/filesystem before-after snapshots; the standard
  trace-inventory tool.
- **Process Monitor (ProcMon)**, Sysinternals — live file/registry
  tracing for traces RegShot misses.
- **7-Zip** — used by the Installer itself for AdvancedExtract; also the
  manual way to inspect what an upstream installer/archive contains.
- A clean **Windows VM or Windows Sandbox** (Pro/Enterprise/Education;
  not Home) — the analysis environment. Snapshot before, revert after.

## Driving the tools non-interactively

- Both the Generator and the Installer accept the portable app's main
  directory as their target (command line or Windows Send To) — that is
  how you point them at `X:\PortableApps\FileZillaPortable` without
  browsing.
- The scriptable surface for *testing* is the built `.paf.exe`: silent
  installs and the `/DESTINATION=`-style override
  ([`02-installer-and-installer-ini.md`](02-installer-and-installer-ini.md))
  are what the Platform itself uses. Exact switch syntax is
  tool-version-specific — verify against the installed tool's own
  documentation before scripting against it (**Unverified** in this
  repo).

## Automation reality check

- There is **no documented headless mode** for the stock Generator or
  Installer wizard in the sources this repo is built on. Treat launcher
  generation and `.paf.exe` compilation as interactive Windows steps
  unless you have verified otherwise on your exact tool version.
- What *is* automatable today: silent `.paf.exe` install testing;
  INI linting against [`01`](01-format-spec.md) /
  [`02`](02-installer-and-installer-ini.md) /
  [`04`](04-launcher-ini-reference.md) (unknown key, bad `PackageVersion`
  shape, missing required sections); and the unofficial uroesch
  Wine/Docker pipeline for community packages
  ([`13`](13-ecosystem-and-source-repositories.md)).
- A pragmatic CI shape: lint the INIs on any runner, build on a Windows
  runner with a human-triggered release step, and never let CI publish a
  `.paf.exe` no human has installed once.
