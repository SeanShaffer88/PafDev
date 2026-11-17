# 06 — PAL Environment Variable Substitution (envsub)

Source: official PAL 2.2 manual, `ref/envsub.html` and
`topics/languages.html`. Verified 2026-11-16.

Substitution applies to almost every path/string value in the launcher
INI (`[Launch]`, `[Environment]`, `[FileWriteN]`, `[FilesMove]`,
`[DirectoriesMove]`, cleanup sections, `[Language*]`,
`[RegistryValueWrite]`, …). Ordinary Windows environment variables
(`%TEMP%`, `%PATH%`, `%APPDATA%`, …) may also be used; the variables below
are the PAL-provided ones.

## Alternative forms for directory variables

Every **directory** variable below exists in four forms:

| Form | Example |
|---|---|
| `%VAR%` | `X:\PortableApps\AppNamePortable\App` |
| `%VAR:ForwardSlash%` | `X:/PortableApps/AppNamePortable/App` |
| `%VAR:DoubleBackslash%` | `X:\\PortableApps\\AppNamePortable\\App` |
| `%VAR:java.util.prefs%` | java.util.prefs escaping: forward-slash separated, characters other than colon and lower-case letters escaped with `/` |

Partial-directory variables get the same forms. Drive variables do not.
The case of drive/partial-dir variables is not guaranteed (may be upper
or lower case) — never do case-sensitive matching against them.

## Drive variables

| Variable | Meaning |
|---|---|
| `%PAL:Drive%` | Drive letter **with colon** the app runs from, e.g. `X:`. In Live mode this is the portable device location, not the temp copy |
| `%PAL:LastDrive%` | Drive letter with colon from the **previous** run, e.g. `W:` |
| `%PAL:DriveLetter%` | Drive letter **without colon**, e.g. `X`. For patterns like `file:////%PAL:DriveLetter%/`. **Do not use when supporting UNC** — for UNC paths this is `\` |
| `%PAL:LastDriveLetter%` | Previous drive letter without colon. Same UNC caveat |

## Directory variables

| Variable | Meaning |
|---|---|
| `%PAL:AppDir%` | The package's `App` directory, normally `X:\PortableApps\AppNamePortable\App`. In Live mode: `%TEMP%\AppNamePortableLive\App` unless `[LiveMode] CopyApp=false` |
| `%PAL:DataDir%` | The package's `Data` directory, normally `X:\PortableApps\AppNamePortable\Data`. In Live mode: `%TEMP%\AppNamePortableLive\Data` |
| `%JAVA_HOME%` | Only with `[Activate] Java=find` or `require`. The found JRE/JDK root (no trailing `\bin`). With `find` the path may not exist; with `require` the launcher aborts if Java is not found |
| `%PortableApps.comDocuments%` | PortableApps Documents folder, normally `X:\Documents`. Existence not guaranteed |
| `%PortableApps.comPictures%` | Normally `X:\Documents\Pictures`. Existence not guaranteed |
| `%PortableApps.comMusic%` | Normally `X:\Documents\Music`. Existence not guaranteed |
| `%PortableApps.comVideos%` | Normally `X:\Documents\Videos`. Existence not guaranteed |
| `%PAL:PortableAppsDir%` | The `PortableApps` directory — exactly: **the parent directory of the package**, normally `X:\PortableApps` |
| `%PAL:PortableAppsBaseDir%` | Base of the PortableApps hierarchy — the directory that normally contains `PortableAppsDir` and the Documents folder. Note the spelling: `BaseDir`, **not** `BaseDirectory` |
| `%PAL:LastPortableAppsBaseDir%` | Previous run's `%PAL:PortableAppsBaseDir%` |
| `%USERPROFILE%` | Host user profile, e.g. `C:\Users\Username` |
| `%ALLUSERSPROFILE%` | All-users profile, e.g. `C:\ProgramData` (Vista+). See `%ALLUSERSAPPDATA%` below — most apps should use that instead |
| `%ALLUSERSAPPDATA%` | **Invented by PAL** (does not exist in Windows itself; new in 2.1). Like `ALLUSERSPROFILE` but on 2000/XP it appends `\Application Data`. On Vista+: `C:\ProgramData` |
| `%LOCALAPPDATA%` | e.g. `C:\Users\Username\AppData\Local` |
| `%APPDATA%` | e.g. `C:\Users\Username\AppData\Roaming` |
| `%DOCUMENTS%` | The **host** Documents folder, e.g. `C:\Users\Username\Documents` — distinct from `%PortableApps.comDocuments%` |
| `%TEMP%` | The temp directory the app will see — if `[Launch] CleanTemp` assigned a contained temp dir, this is that dir |

## Partial directory variables

For updating paths stored inside settings files when the package moves
(used with `[FileWriteN] Type=Replace`):

| Variable | Meaning |
|---|---|
| `%PAL:PackagePartialDir%` | Current package path **minus drive letter and colon**, e.g. `\PortableApps\AppNamePortable` |
| `%PAL:LastPackagePartialDir%` | Same, for the previous run, e.g. `\Apps\AppNamePortable`. On first run it equals `PackagePartialDir`, so a Find/Replace pair using both is skipped |

Typical use:

```ini
[FileWrite1]
Type=Replace
File=%PAL:DataDir%\settings\app.conf
Find=%PAL:LastPackagePartialDir%
Replace=%PAL:PackagePartialDir%
```

## Language variables

Set by the PortableApps.com Platform when it launches the app (values
shown for English / Portuguese / Brazilian Portuguese):

| Variable | Examples |
|---|---|
| `%PortableApps.comLanguageCode%` | `en`, `pt`, `pt-br` |
| `%PortableApps.comLocaleCode2%` | `en`, `pt`, `pt` |
| `%PortableApps.comLocaleCode3%` | `eng`, `por`, `por` |
| `%PortableApps.comLocaleglibc%` | `en_US`, `pt`, `pt_BR` (exact spelling: `Localeglibc`) |
| `%PortableApps.comLocaleID%` | `1033`, `2070`, `1046` |
| `%PortableApps.comLocaleWinName%` | `LANG_ENGLISH`, `LANG_PORTUGUESE`, `LANG_PORTUGUESEBR` |
| `%PortableApps.comLocaleName%` | `English`, `Portuguese`, `PortugueseBR` |
| `%PAL:LanguageCustom%` | Custom value built by `[Language]` + `[LanguageStrings]` (+ `[LanguageFile]`) in the launcher INI |

## Production-verified, but missing from the manual's envsub page

These do **not** appear in the PAL 2.2 manual's `envsub` page, but are used
by official production packages in
[AppConfigs](../examples/real-world/README.md) — treat them as real:

- `%PAL:FullAppDir%` — the directory of the running `ProgramExecutable`
  under `App\` (32/64-bit aware). Used by 7-Zip Portable, e.g.
  `CheckIfExists=%PAL:FullAppDir%\Lang\%PAL:LanguageCustom%.txt`.
- `%PAL:DriveHex%` / `%PAL:LastDriveHex%` — the drive letter in the hex
  form used inside `REG_BINARY` data in `.reg` files. 7-Zip Portable
  patches them with a `[FileWriteN]` pair:
  `Find=%PAL:LastDriveHex%,00,3a,00` → `Replace=%PAL:DriveHex%,00,3a,00`.

Related trap: `%FullAppDir%` **without** the `PAL:` prefix is **not** a
built-in. Notepad++ Portable defines its own in `Custom.nsh`
(`${SetEnvironmentVariablesPath} FullAppDir …` in `${SegmentInit}`,
choosing the 32/64-bit folder via `$Bits`). If you see `%FullAppDir%` in a
config, check its `Custom.nsh` for the definition — and if you copy the
pattern, copy the definition too
([05-launcher-advanced-custom-code.md](05-launcher-advanced-custom-code.md)).

## Not real (do not use)

Verified **absent** from the PAL 2.2 manual — commonly hallucinated or
from forum proposals:

- `%PAL:BinDir%` — does not exist in 2.2.
- `%PAL:PortableAppsBaseDirectory%` — wrong name; use `%PAL:PortableAppsBaseDir%`.
- `%PortableApps.comLanguage%` — not a variable; use the `…LanguageCode%` / locale variables above.
- `%PAL:Bits%` — not an envsub variable; `$Bits` is an NSIS variable for
  custom code only.
- `%PAL:CurrentDrive%` — appears once in a manual example but is not
  defined; use `%PAL:Drive%`.
