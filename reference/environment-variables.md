# Reference — Environment Variables

Variables the Launcher substitutes in INI values, and the standard
Windows variables packages use. Full treatment, including which are
production-verified:
[`../docs/06-environment-variables.md`](../docs/06-environment-variables.md).
**Never hard-code a drive letter or absolute path in launcher
configuration** — that is what these exist to prevent.

## %PAL:% variables (set by the Launcher)

| Variable | Expands to |
|---|---|
| `%PAL:AppDir%` | The package's `App` directory |
| `%PAL:DataDir%` | The package's `Data` directory |
| `%PAL:BinDir%` | The directory containing the launcher exe (package root) |
| `%PAL:FullAppDir%` | Full path of the app directory |
| `%PAL:PortableAppsDir%` | The PortableApps directory (the one containing the package) |
| `%PAL:PortableAppsBaseDir%` / `%PAL:PortableAppsBaseDirectory%` | The base directory above the PortableApps directory |
| `%PAL:PackagePartialDir%` | The package's path relative to the base directory |
| `%PAL:LastPackagePartialDir%` | Same, for the previous run's location (drive-change detection) |
| `%PAL:Drive%` / `%PAL:CurrentDrive%` | Current drive (with colon and backslash form per docs/06) |
| `%PAL:DriveLetter%` | Current drive letter only |
| `%PAL:DriveHex%` | Current drive in hex form |
| `%PAL:LastDrive%` / `%PAL:LastDriveLetter%` / `%PAL:LastDriveHex%` | The previous run's drive equivalents |
| `%PAL:LastPortableAppsBaseDir%` | Previous run's base directory |
| `%PAL:Bits%` | OS bitness (32/64) |
| `%PAL:LanguageCustom%` | The Platform's custom language value |

The `Last*` family is how `[FileWriteN]` sections fix paths stored by
the app when the drive letter changed between runs — see docs/04 and
docs/06 before using them.

## Standard Windows variables (as the app sees them)

`%APPDATA%`, `%LOCALAPPDATA%`, `%USERPROFILE%`, `%DOCUMENTS%`,
`%TEMP%`, `%PATH%`, `%ALLUSERSPROFILE%` — used in
`[DirectoriesMove]`/`[FilesMove]` targets and `[Environment]`
overrides. The Launcher redirects the app's view of some of these
when the corresponding sections say so; the exact semantics are in
docs/04/docs/06.
