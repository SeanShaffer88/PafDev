# Templates

Copy-and-rename starting points. Do not write configuration files from
memory — start here or from `../examples/`.

## MinimalAppPortable/

A complete minimal package skeleton:

```
MinimalAppPortable/
  help.html
  App/
    AppInfo/
      appinfo.ini
      installer.ini            (optional-file example: preserve plugins dir)
      Launcher/
        AppNamePortable.ini    (rename to your AppID)
        Custom.nsh             (custom-code skeleton; delete if unused)
    DefaultData/
      README.txt               (explains DefaultData; replace with real defaults)
    AppName/                   (put the base app's binaries here)
  Data/                        (created on first run; do not ship user data)
  Other/
    Help/Images/               (images referenced by help.html)
    Source/
      Readme.txt               (launcher readme — keep the GPL notice text)
      AppNamePortable.ini      (example user configuration file)
```

What you must add yourself (binary files cannot be provided as text):

- `App\AppInfo\appicon.ico` and `appicon_16.png`, `appicon_32.png`,
  `appicon_75.png`, `appicon_128.png`, `appicon_256.png` — see
  `../docs/01-format-spec.md` §3 for the exact ICO contents.
- The base application's binaries in `App\AppName\`.
- The generated launcher `AppNamePortable.exe` in the package root
  (produced by the PortableApps.com Launcher Generator).

What you must rename/replace:

- Every occurrence of `AppName` / `AppNamePortable` (folder names, AppID,
  file names, `ProgramExecutable`, registry paths).
- The placeholder `appinfo.ini` metadata (Publisher, Homepage, Category,
  Description, versions, license booleans — set them to the *true* values
  for your app).
- The launcher INI's registry key and `%APPDATA%` paths — these must match
  your app's actual traces (see `../docs/07-end-to-end-workflow.md`).

## online-installer.ini

A complete `[DownloadFiles]` example for an online installer
(`..._online.paf.exe`), placed as `App\AppInfo\installer.ini`. The
SHA-256 value is a placeholder of zeros — replace it with the real hash
of the publisher's file before building.

## PortableApps.comInstallerCustom.nsh

Skeleton for installer custom code with the three supported macros
(`CustomCodePreInstall`, `CustomCodePostInstall`,
`CustomCodeOptionalCleanup`). Goes in `Other\Source\`.

## Launcher custom code (Custom.nsh)

A skeleton `Custom.nsh` is included inside the skeleton package at
`MinimalAppPortable/App/AppInfo/Launcher/Custom.nsh` — its correct home
in PAL 2.1+. Delete it if the package needs no custom code (most don't).
See `../docs/05-launcher-advanced-custom-code.md` for when custom
launcher code is appropriate.
