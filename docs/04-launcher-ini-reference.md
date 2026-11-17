# 04 — Launcher INI Complete Reference (PAL 2.2)

Source: official PortableApps.com Launcher 2.2 manual,
https://portableapps.com/manuals/PortableApps.comLauncher/ (`ref/launcher.ini/*`).
Verified against the manual on 2026-11-16.

## File identity

- The file is **never** literally named `launcher.ini` in a package. It is
  `App\AppInfo\Launcher\<AppID>.ini` — the base name matches the launcher
  executable (`AppNamePortable.exe` → `AppNamePortable.ini`). "launcher.ini"
  is the manual's shorthand.
- INI syntax: `[Section]` headers (CamelCase by convention), `Key=value`,
  comment lines start with `;`. **Inline comments are NOT permitted.**
- Quoting: if a value's first and last characters are the same quote (`'`
  or `"`), the quotes are stripped — a pure character check, no escaping.
  This matters for `CommandLineArguments` containing paths with spaces.
- **There is no safety net for INI keys.** A misspelled or invented key
  is not an error — PAL simply never acts on it, and the feature it was
  meant to enable silently does not happen. (Custom code is the opposite:
  an unknown `${Segment…}` macro fails the Generator compile —
  `docs/05-launcher-advanced-custom-code.md`.) Diff every key against
  this file before generating.

## Definitive section list (PAL 2.2)

`[Launch]`, `[Activate]`, `[LiveMode]`, `[Environment]`, `[RegistryKeys]`,
`[RegistryValueWrite]`, `[RegistryCleanupIfEmpty]`,
`[RegistryCleanupForce]`, `[RegistryValueBackupDelete]`,
`[QtKeysCleanup]`, `[FileWriteN]`, `[FilesMove]`, `[DirectoriesMove]`,
`[DirectoriesCleanupIfEmpty]`, `[DirectoriesCleanupForce]`, `[Language]`,
`[LanguageStrings]`, `[LanguageFile]`, `[ServiceN]`

**Do not use** (commonly guessed, but **not** in PAL 2.2): a `[Qt]`
section (it is `[QtKeysCleanup]`), a `[Services]` section (it is
`[ServiceN]`), `[FileExtensions]`/`[URIProtocols]`/`[ProtocolExtensions]`
sections, `[Launch] AdditionalParametersAllowed`, `[Launch] DosName`,
`[Activate] VB6RunTime`, a `[Dependencies]` section, or a `[Control]`
section (that belongs to `appinfo.ini`). File associations are handled via
registry sections or custom code.

## [Launch]

| Key | Values / default | Meaning |
|---|---|---|
| `ProgramExecutable` | Path, **mandatory** | Program to launch, **relative to the package's `App` directory**. `App\AppName\AppName.exe` → `ProgramExecutable=AppName\AppName.exe`. With `[Activate] Java=require`, `java.exe`/`javaw.exe` is rewritten to the found JRE binary |
| `ProgramExecutable64` | Path, optional (2.1+) | Override on 64-bit Windows. Only ship 64-bit builds when there is significant benefit or a requirement |
| `ProgramExecutableWhenParameters` | Path, optional | Override used **only when arguments are passed** to the launcher (e.g. menu exe normally, compiler exe when a file is passed) |
| `ProgramExecutableWhenParameters64` | Path, optional (2.1+) | 64-bit override of the above. Lookup order: WhenParameters64 → 64 → WhenParameters → base |
| `CommandLineArguments` | String, optional | Arguments **always** passed to the app (e.g. to point it at portable data). Quote paths with spaces: `CommandLineArguments='-d "%PAL:DataDir%\settings"'`. Envsub applies. Arguments the *user* passes to the launcher exe are forwarded separately |
| `WorkingDirectory` | Path, optional | Launch working directory. **Avoid when possible** — it breaks passing multiple relative files; a single file is auto-corrected. Prefer adding the app dir to `PATH` via `[Environment]` |
| `MinOS` | `none`/`2000`/`XP`/`2003`/`Vista`/`2008`/`7`/`2008 R2`; default `none` (2.1+) | Minimum Windows version; lower versions get a message and the app does not run |
| `MaxOS` | Same values; default `none` (2.1+) | Maximum Windows version. Use cautiously |
| `RunAsAdmin` | `force`/`try`/`compile-force`/`none`; default `none` (`compile-force` 2.1+) | `force`: UAC prompt; failure/cancel = exit with a message. `try`: prompt; if not elevated, warn and continue. `compile-force`: bakes `RequestExecutionLevel admin` into the exe (requires regenerating the launcher; OS handles elevation, no friendly message) |
| `RunAsAdmin2000` / `RunAsAdminXP` / `RunAsAdmin2003` / `RunAsAdminVista` / `RunAsAdmin2008` / `RunAsAdmin7` / `RunAsAdmin2008R2` | `force`/`try`/`none` (2.1+) | Per-OS overrides of `RunAsAdmin`. Pattern: `RunAsAdmin=force` + `RunAsAdminXP=none` for apps needing admin only on Vista+ |
| `CleanTemp` | `true`/`false`; default `true` | When true, the app gets a contained temp dir `%TEMP%\AppNamePortableTemp`, deleted on exit. With `WaitForProgram=false`, temp goes to `Data\temp` and is deleted on next start instead. Set `false` only if the app provably leaves nothing in TEMP |
| `SinglePortableAppInstance` | `true`/`false`; default `false` | `true`: only one instance of the **portable** copy; a second portable launch aborts silently |
| `SingleAppInstance` | `true`/`false`; default `true` | If a **local** copy is already running, abort with an error. Does not affect a second portable instance. Set `false` only if local+portable may run together safely (never when settings live in `%APPDATA%`/registry). For Launch4J Java apps, set `false` and use `CloseEXE` |
| `CloseEXE` | File name only, optional | A **different** exe that must be closed before starting (mainly Java/Launch4J apps whose real process differs from `ProgramExecutable`) |
| `SplashTime` | Milliseconds; default `1500` | Splash screen duration. Do not inflate it. Users can disable the splash entirely (user config) |
| `LaunchAppAfterSplash` | `true`/`false`; default `false` | Wait for the splash to finish before launching (for full-screen/resolution-changing apps) |
| `WaitForProgram` | `true`/`false`; default `true` | `false`: launcher does not wait for exit. **Only** safe when no registry handling and no file moves are used (all settings redirected by args/env vars). Ignored in Live mode |
| `WaitForOtherInstances` | `true`/`false`; default `true` | May be `false` for single-instance apps that forward to the first instance **and cannot restart themselves**. Never `false` for self-restarting apps (e.g. Firefox) — cleanup would run while the app still runs |
| `WaitForEXE1`, `WaitForEXE2`, … | File name | Extra executables to wait for when `ProgramExecutable` is a stub that spawns the real app. Number sequentially from 1 |
| `RefreshShellIcons` | `before`/`after`/`both`/`none`; default `none` | Refresh Explorer icons around launch, for apps whose file-type registrations PAL handles/cleans. With `[RegistryKeys]` handling, use `both` |
| `HideCommandLineWindow` | `true`/`false`; default `false` | Hide a console window produced by the app |
| `DirectoryMoveOK` | `yes`/`warn`/`no`; default `warn` (2.1+) | Whether the **package folder itself** may be moved (drive-letter changes must always work regardless). Set `yes` only after designing for moves, typically with `[FileWriteN]` + `%PAL:LastPackagePartialDir%`/`%PAL:PackagePartialDir%` |
| `NoSpacesInPath` | `true`/`false`; default `false` | `true`: show a clear error if the package path contains spaces instead of letting the app fail obscurely |
| `SupportsUNC` | `yes`/`warn`/`no`; default `warn` (2.2+) | Running from a UNC path `\\server\share\…`. Only `yes` after actually testing UNC — some apps corrupt data on UNC |
| `AppName` | String, **deprecated** | Non-portable app name for the "already running" error. Derived from `appinfo.ini` when unset; leave unset |

## [Activate]

Tells PAL which subsystems to compile in. Changing a value that adds a
plug-in **requires regenerating the launcher**.

| Key | Values / default | Meaning |
|---|---|---|
| `Registry` | `true`/`false`; default `false` | **Must be `true` for ANY registry section to be parsed at all** (`[RegistryKeys]`, `[RegistryValueWrite]`, `[RegistryCleanup*]`, `[RegistryValueBackupDelete]`, `[QtKeysCleanup]`) |
| `Java` | `none`/`find`/`require`; default `none` | `find`: locate a JRE if present and set `%JAVA_HOME%` (path may not exist). `require`: abort if no Java found; `ProgramExecutable=javaw.exe`/`java.exe` is rewritten to the JRE binary. With `require`, consider `WaitForProgram=false`/`WaitForOtherInstances=false` or cleanup may match other apps' `javaw.exe` |
| `XML` | `true`/`false`; default `false` | Required for `[FileWriteN]`/`[LanguageFile]` types `XML attribute`/`XML text`. Adds the NSIS XML plug-in (~60 KB). PAL warns at generation time if XML features are used without it |

No other `[Activate]` keys exist in 2.2.

## [LiveMode]

Behaviour when the package is on read-only media ("running locally"):
needed parts are copied to a writable temp location, run, then deleted.

| Key | Values / default | Meaning |
|---|---|---|
| `CopyApp` | `true`/`false`; default `true` | Whether the app itself must be copied to run in Live mode. Affects `%PAL:AppDir%` in Live mode |
| `CopyData` | **Obsolete** | Removed; data is always copied in Live mode. Do not use |

## [Environment]

Arbitrary `NAME=value` pairs — no fixed keys. Each sets an environment
variable **for the launched app and its children only**. Parsed in file
order, **before** all other active sections, so variables defined here can
be reused later in the file. Envsub applies to values.

```ini
[Environment]
PATH=%PATH%;%PAL:AppDir%\AppName
APPNAME_HOME=%PAL:DataDir%\settings
```

Long paths can be defined once as pseudo-variables (including transformed
forms such as `%PAL:DataDir:DoubleBackslash%`) and referenced elsewhere.

## Registry sections — all require `[Activate] Registry=true`

Roots are written short: `HKCU`, `HKLM`, `HKCR`, `HKU`, …

### [RegistryKeys]

Format: `filename=HKCU\Software\AppName`

- The key subtree is imported from / saved to `Data\settings\<filename>.reg`.
- A pre-existing local key is backed up before the run and restored after.
- Special filename `-`: `-=HKCU\Software\AppName` protects the local key
  and **discards** the portable app's changes (nothing saved).
- To fix drive letters inside a saved `.reg`, add a `[FileWriteN]`
  `Type=Replace` targeting that `.reg` file.

### [RegistryValueWrite]

Format: the **key name is the full path including the value name**;
the value is `REG_TYPE:value` (prefix optional, defaults to `REG_SZ` —
write it explicitly if the value itself could contain a colon).

```ini
[RegistryValueWrite]
HKCU\Software\AppName\Settings\SavePath=REG_SZ:%PAL:DataDir%
HKCU\Software\AppName\Settings\Count=REG_DWORD:16
```

Use it to set values only for the portable run (e.g. pointing the app at
portable paths, disabling association writes).

### [RegistryValueBackupDelete]

Format: consecutive integers from 1: `1=HKCU\Software\Publisher\AppName\SomeValue`

Each listed **value** is backed up before and restored after the run, but
any value the portable app sets is **deleted** (for values not worth saving).

### [RegistryCleanupIfEmpty]

Format: consecutive integers from 1: `1=HKCU\Software\Publisher`

Listed keys are deleted after the run **only if empty** — for parent trees
left behind empty.

### [RegistryCleanupForce]

Format: consecutive integers from 1. Listed keys are **unconditionally
removed with contents** after the run — for trees of useless/temp data.

> **Warning — this can destroy a local install's data.** If a listed key
> is one the locally installed copy of the app also uses, force cleanup
> deletes the *local* settings on every exit. The safe alternatives:
> `[RegistryKeys]` (the local key is backed up and restored) or the `-`
> filename form in `[RegistryKeys]` (protects the local key and discards
> the portable app's changes). Reserve force cleanup for keys only the
> portable app creates. See `docs/17-failure-mode-reference.md` §E.

### [QtKeysCleanup]

Cleans Qt's per-path cache keys under
`HKCU\Software\Trolltech\OrganizationDefaults\`. Entries (integers from 1)
are the offending key with that prefix **and** the trailing portable path
stripped:

```ini
[QtKeysCleanup]
1=Qt Factory Cache 4.6\com.trolltech.Qt.QImageIOHandlerFactoryInterface:
2=Qt Plugin Cache 4.6.false
```

## [FileWriteN] — `[FileWrite1]`, `[FileWrite2]`, …

Writes into files **before launch** (typically updating stored paths when
the package moved). The target file **must already exist** or the section
is silently skipped.

| Key | Required for | Meaning |
|---|---|---|
| `Type` | Always (mandatory) | `ConfigWrite` / `INI` / `Replace` / `XML attribute` / `XML text` (XML types need `[Activate] XML=true`) |
| `File` | Always | File to modify. Envsub applies |
| `Entry` | `ConfigWrite` | Line prefix to find; `Value` is written onto that line, or appended at end of file if not found. Include all leading whitespace; quote the string if it has leading/trailing whitespace |
| `Section` + `Key` + `Value` | `INI` | Write `Value` into an INI file's `Section`/`Key` |
| `Value` | `ConfigWrite`, `INI`, XML types | Value to write. For `ConfigWrite` into XML-like files, include closing markup yourself (e.g. `%PAL:DataDir%\settings</config>`) or use the XML types |
| `Find` + `Replace` | `Replace` | Find-and-replace in the file (the drive-letter/path update mechanism). If after envsub `Replace` == `Find`, the replacement is skipped |
| `Attribute` + `XPath` | XML types | Attribute to set / XPath locating the node |
| `CaseSensitive` | Optional, `ConfigWrite`/`Replace` | Default `false`. Case-sensitive search is faster |
| `Encoding` | Optional, `Replace` only | `auto` (default, detect from BOM) / `ANSI` / `UTF-16LE`. Set `UTF-16LE` for a UTF-16LE file missing its BOM. `ConfigWrite`/`INI` auto-detect encoding themselves |

### The path-migration triple (required pattern)

Any stored file that can contain an absolute path needs **three** `Replace`
sections per file, in this order — most specific first. A stored path can
take any of the three forms, and missing one leaves stale paths behind
(the classic symptom: the app works on the first machine and breaks, or
points at the old drive, after the package moves). This is the pattern the
official Application Template teaches and production packages use
(Notepad++ Portable repeats it for five files, `[FileWrite1]`–`[FileWrite15]`):

```ini
[FileWrite1]
Type=Replace
File=%PAL:DataDir%\Config\config.xml
Find=%PAL:LastDrive%%PAL:LastPackagePartialDir%\
Replace=%PAL:Drive%%PAL:PackagePartialDir%\

[FileWrite2]
Type=Replace
File=%PAL:DataDir%\Config\config.xml
Find=%PAL:LastPortableAppsBaseDir%\
Replace=%PAL:PortableAppsBaseDir%\

[FileWrite3]
Type=Replace
File=%PAL:DataDir%\Config\config.xml
Find=%PAL:LastDrive%\
Replace=%PAL:Drive%\
```

Variants used by production packages:

- **Inside a saved `.reg` file**, paths are stored with doubled
  backslashes, so use the `:DoubleBackslash` forms and a doubled trailing
  backslash (`Find=%PAL:LastDrive%%PAL:LastPackagePartialDir:DoubleBackslash%\\`).
- **`REG_BINARY` values** in a `.reg` store the drive as hex bytes; add a
  fourth replace: `Find=%PAL:LastDriveHex%,00,3a,00` →
  `Replace=%PAL:DriveHex%,00,3a,00`.
- Set `DirectoryMoveOK=yes` in `[Launch]` only once every path-storing
  file has its triple.

### Working on the saved `.reg` file itself

`[FileWriteN]` may target the `.reg` files that `[RegistryKeys]` saves
into `Data\settings\` — they are plain files before import. Two production
uses (7-Zip Portable, mirrored in
[`../examples/real-world/7zip/`](../examples/real-world/7zip/)):

- `Type=INI` with `Section=HKEY_CURRENT_USER\Software\…` to rewrite a
  single value inside the `.reg` (there: injecting `%PAL:LanguageCustom%`
  as the app's `Lang` value).
- The migration triple in `:DoubleBackslash` form (above) to fix paths
  the app stored in its registry keys.

## Filesystem sections (wildcards supported since 2.1; envsub applies)

### [FilesMove]

Format: `filename=target directory`

```ini
[FilesMove]
settings\file.txt=%PAL:AppDir%\AppName
```

- `filename` is **relative to `Data\`**. The target is the **directory**
  the file is copied into while running — do **not** include the file name.
- An existing local target file is backed up (to
  `<filename>-BackupBy<AppID>`) and restored at exit; the portable file
  moves back to `Data\` at exit.
- The folder containing the file **inside `Data\` must already exist** or
  the file will not be saved — keep files at `Data\` root or in
  `Data\settings`, or create the folder via `DefaultData`.

### [DirectoriesMove]

Format: `directory=target location`

```ini
[DirectoriesMove]
AppNameConfig=%APPDATA%\Publisher\AppName
```

- `directory` is relative to `Data\`; the target **includes the directory
  name itself** (`Data\<directory>\*.*` → `<target>\*.*`).
- A pre-existing target is backed up (to `<target>-BackupBy<AppID>`) and
  restored at exit.
- Special source `-`: `-=<target>` protects the local directory and
  **discards** changes.
- The **parent** folder inside `Data\` must exist — use a top-level
  directory name. **Never use `settings` as the key**: `Data\settings`
  holds the registry `.reg` files; moving it loses data.

### [DirectoriesCleanupIfEmpty]

Format: integers from 1 (`1=%APPDATA%\Publisher`). Listed directories are
removed after the run **only if empty**.

### [DirectoriesCleanupForce]

Format: integers from 1. Listed directories are **unconditionally
removed** after the run. To protect local data instead of destroying it,
use `[DirectoriesMove]` with key `-`.

## Language sections

These build the custom variable `%PAL:LanguageCustom%` (usable anywhere
envsub applies) from the Platform language plus app-specific mappings.

### [Language]

| Key | Meaning |
|---|---|
| `Base` | **Mandatory if the section is used.** Base string to derive from — normally exactly one language variable, e.g. `Base=%PortableApps.comLanguageCode%` |
| `Default` | Optional. Value used when the base value is not a key in `[LanguageStrings]`; if unset, the base value itself is used |
| `CheckIfExists` | Optional. File to test (append `\*.*` to test a directory); may use `%PAL:LanguageCustom%`. If it does not exist, fall back to `DefaultIfNotExists` |
| `DefaultIfNotExists` | Optional. Fallback value when the `CheckIfExists` test fails |

### [LanguageStrings]

Arbitrary pairs: the `[Language] Base` value is looked up **as a key name**
here, and the matching value (after envsub) becomes `%PAL:LanguageCustom%`.

```ini
[LanguageStrings]
en=English
pt-br=PortugueseBR
```

### [LanguageFile]

Reads `%PAL:LanguageCustom%` **from a file** — for launches outside the
Platform, where no Platform language variables exist. Keys mirror
`[FileWriteN]` reading: `Type` (`ConfigRead`/`INI`/`XML attribute`/`XML text`,
mandatory), `File` (mandatory), `Entry` (for `ConfigRead`), `Section`/`Key`
(for `INI`), `Attribute`/`XPath` (XML types; need `[Activate] XML=true`),
`CaseSensitive` (for `ConfigRead`), and `TrimRight` (strip this suffix from
the read string, e.g. a file extension or closing tag). `ConfigRead`/`INI`
auto-detect encoding from the BOM.

## [ServiceN] — `[Service1]`, `[Service2]`, …

> ⚠️ **Services are currently disabled in the PortableApps.com Launcher.**
> This section is documented but non-functional in PAL 2.2.

Keys: `Name` (mandatory), `Path` (mandatory), `Type`
(`service`/`driver-kernel`/`driver-file-system`, default `service`),
`User` (`none`/`LocalService`/`NetworkService`, default `none` =
LocalSystem), `Display`, `Dependencies` (comma-separated), `Description`,
`IfExists` (`skip`/`replace`, default `skip`; currently no effect except a
warning for `replace`).

## User configuration file (`<AppID>.ini` next to the exe)

A **different file** from the launcher INI: it sits in the package root
next to `<AppID>.exe` with the same base name, and lets the *end user*
override behaviour. Packages ship an example as
`Other\Source\<AppID>.ini`; the user copies it to the root and renames it.
No section header is required.

| Key | Values / default | Meaning |
|---|---|---|
| `AdditionalParameters` | String; default empty | Extra command-line parameters passed to the app, in addition to `[Launch] CommandLineArguments` and parameters given to the launcher exe |
| `DisableSplashScreen` | `true`/`false`; default `false` | Suppresses the splash screen |
| `RunLocally` | `true`/`false`; default `false` | Forces Live mode: copy needed app/data to a temp folder on the host, run, delete afterwards |

Custom code can define **additional** app-specific user keys via
`${ReadUserConfig}` — those are documented in that app's `help.html`, are
not standard PAL keys, and booleans use `true`/`false` by convention.
There is no standard user key named `LiveMode`; the key is `RunLocally`.

## Minimal valid example (verified keys only)

```ini
[Launch]
ProgramExecutable=AppName\AppName.exe
DirectoryMoveOK=yes
SupportsUNC=yes

[Activate]
Registry=true

[RegistryKeys]
AppName=HKCU\Software\AppName

[DirectoriesMove]
AppNameConfig=%APPDATA%\AppName
```
