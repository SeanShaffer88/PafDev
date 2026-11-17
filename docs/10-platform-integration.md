# 10 — PortableApps.com Platform Integration

How the PortableApps.com Platform (the menu/app store that users run from
`StartPortableApps.exe`) interacts with a package — i.e. what your
`appinfo.ini` values actually *do* on a user's machine.

## Discovery

- The Platform scans its `PortableApps` directory for folders containing
  `App\AppInfo\appinfo.ini`. A package that is not under a `PortableApps`
  folder, or whose `appinfo.ini` is malformed, simply does not appear.
- The menu entry shows `[Details] Name`, the icon set from `App\AppInfo`,
  and `[Control] Start` is what gets executed. Multi-icon apps
  (`Icons=2` + `Start1`/`Name1`…) get multiple menu entries.
- "Refresh App Icons" in the Platform re-scans after manual changes.

## App Store, installs, and updates

- The built-in App Store installs `.paf.exe` files silently through the
  PortableApps.com Installer: the user picks a parent location, the
  package lands in `<PortableApps>\<AppID>`.
- Updates are driven **solely** by comparing the installed
  `[Version] PackageVersion` (4-part numeric) with the store's — a
  package whose `PackageVersion` did not increase will never be offered
  as an update, and a malformed one breaks comparison.
- `InstallType` (and the installer's optional-components writing of it)
  is displayed in the app details so users can tell editions apart
  (e.g. Multilingual vs English).
- `[Dependencies]` values are surfaced/enforced by the Platform:
  `UsesJava=yes` ties the app to Java Portable (jPortable, installed
  under `CommonFiles\Java`); `UsesDotNetVersion` warns/blocks on machines
  lacking the framework; `Requires64bitOS=yes` hides/blocks the app on
  32-bit systems; `RequiresAdmin=yes` marks the app as needing elevation.
- Cached online-installer downloads: when `[DownloadFiles]
  DownloadCachedByPAc` is set, the Platform's store can serve the
  publisher download from the PortableApps.com cache during installs and
  updates.

## Launching from the Platform

- The Platform sets the language environment variables
  (`%PortableApps.comLanguageCode%`, `%PortableApps.comLocale*%` — see
  `docs/06-environment-variables.md`) before starting the launcher, which
  is how `[Language]`/`[LanguageStrings]` in the launcher INI and
  multilingual apps pick their UI language. Outside the Platform those
  variables are absent — that is what `[LanguageFile]` is for.
- File-association features (the Platform's file associations /
  "open with" integration) use `[Associations]` and `[FileTypeIcons]`
  from `appinfo.ini`: `FileTypes`, `Protocols`, and the command-line
  patterns tell the Platform how to pass a file/URL to your launcher.
- A well-behaved package does **not** permanently register file
  associations on the host: association is a Platform feature, and when
  the app itself registers associations, PAL's registry backup/restore
  is the mechanism — the host must end the run as it began (the
  host-modification rule, `docs/01-format-spec.md`).
- `BaseAppID`/`BaseAppID64`/`BaseAppIDARM64` let Platform 16+ create a
  correctly-pinnable taskbar shortcut for the running base app.
- The Platform's "disable splash screens" option works because PAL
  honours it (same mechanism as the user config's `DisableSplashScreen`).

## PortableApps directory conventions

A standard portable drive layout:

```
X:\
  StartPortableApps.exe        (Platform launcher, at drive root)
  PortableApps\
    PortableApps.com\          (the Platform itself)
    CommonFiles\               (shared components: Java, etc.)
    AppNamePortable\           (your package)
  Documents\                   (PortableApps Documents: Music/Pictures/Videos)
```

This is why `%PAL:PortableAppsDir%` is defined as the package's parent
directory and `%PAL:PortableAppsBaseDir%` as the drive-level root, and
why packages must never assume a drive letter or that the parent folder
is literally named `PortableApps` on every machine — use the variables.

## Plugin and CommonFiles installs

Plugin installers (see `docs/02-installer-and-installer-ini.md`) install
*into* an existing package folder from the Platform/manual install flow.
CommonFiles installers target `PortableApps\CommonFiles\<AppID>` and are
reserved for shared components designated by PortableApps.com (Java is
the canonical example).
