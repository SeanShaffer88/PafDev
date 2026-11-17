# Reference — Package Layout

The Format 3.9 tree at a glance. Full spec:
[`../docs/01-format-spec.md`](../docs/01-format-spec.md). Naming
rules: [`../AGENTS.md`](../AGENTS.md).

```
<AppID>/                              e.g. AppNamePortable/
  <AppID>.exe                         generated launcher (Launcher Generator)
  help.html                           package help page
  App/
    AppInfo/
      appinfo.ini                     name, AppID, versions, license, control
      appicon.ico                     icon set — exact contents in docs/01 §3
      appicon_16.png  appicon_32.png  appicon_75.png
      appicon_128.png  appicon_256.png
      installer.ini                   OPTIONAL — only the keys you need (docs/02)
      Launcher/
        <AppID>.ini                   launcher config — name matches the AppID
        Custom.nsh                    OPTIONAL launcher custom code (PAL 2.1+ home)
    <AppName>/                        the base app's binaries
    DefaultData/                      first-run defaults, copied to Data\ once
  Data/                               ALL user data and settings (runtime)
  Other/
    Help/Images/                      images referenced by help.html
    Source/
      Readme.txt                      launcher readme / licence notices
      <AppID>.ini                     example user configuration file
      PortableApps.comInstallerCustom.nsh   OPTIONAL installer custom code
```

## The rules the tree encodes

- **AppID = folder name**, and the launcher INI is named `<AppID>.ini`
  inside `App\AppInfo\Launcher\` — never a generic `launcher.ini`.
- **Binaries in `App\`, data in `Data\`, sources in `Other\Source\`.**
  Nothing user-specific is written into `App\` at runtime; no binaries
  live in `Data\`.
- `installer.ini` and `Custom.nsh` are **optional and usually absent**
  — create them only for a documented need (docs/02, docs/05).
- The generated `<AppID>.exe` is a build product of the Launcher
  Generator; `[Control] Start` in appinfo.ini names exactly it.
- Installer output: `<AppID>_<DisplayVersion>.paf.exe` (online
  installers end `_online.paf.exe`).
