# 02 — PortableApps.com Installer and installer.ini

The PortableApps.com Installer is the only permitted builder for
`.paf.exe` packages. Current version: **3.9.18 (2026-07-20)**. Every
release of an app in PortableApps.com Format must use the current
Installer; if a new Installer ships during a long test cycle, the older
one may be kept only if it is less than 30 days old on release day.

The installer is configured by `appinfo.ini` (see
`docs/01-format-spec.md`) plus the optional `installer.ini`, both in
`App\AppInfo`. **The whole `installer.ini` is optional.** Without it: the
`App` and `Other` directories are replaced on upgrade, `Data` is
preserved, the installer is single-language (per `appinfo.ini`) or
multilingual with all languages, and the installer source is not included.

> ⚠️ The full example `installer.ini` in the specification illustrates
> every option at once. **Never copy it into a project.** Create each
> project's `installer.ini` from scratch with only the features it needs.

## How building works

1. Lay out the complete package tree (`AppNamePortable\` with `App`,
   `Data`, `Other`, launcher exe, `help.html`).
2. Run `PortableApps.comInstaller.exe` (the Installer wizard) and point it
   at the package folder.
3. The wizard reads `appinfo.ini` + `installer.ini`, validates, and
   compiles `<AppID>_<DisplayVersion>.paf.exe` (online installers:
   `..._online.paf.exe`).
4. Test the produced `.paf.exe` by installing it to a **fresh** directory
   and running the installed copy — not the build tree.

The installer itself must not be modified. Customisation is only via
`installer.ini` and the custom-code file described below.

## installer.ini — complete reference

### [CheckRunning]

| Key | Meaning |
|---|---|
| `CloseEXE` | Custom EXE to check for/close when upgrading. Omit if it is the same as `[Control] Start` in `appinfo.ini`. `CloseEXE=NONE` (uppercase) disables the running check — use with caution |
| `CloseName` | Different display name for what will be closed. Omit if same as the app name in `appinfo.ini` |

### [Source]

| Key | Meaning |
|---|---|
| `IncludeInstallerSource` | `true` includes the PortableApps.com Installer source in the installed package |

### [MainDirectories]

Defaults: `App` removed, `Other` removed, `Data` preserved on upgrade.
Omit the section to keep defaults.

| Key | Meaning |
|---|---|
| `RemoveAppDirectory` | `true`/`false` — replace `App` on upgrade |
| `RemoveDataDirectory` | `true`/`false` — replace `Data` on upgrade (almost always `false`/omitted; removing user data on upgrade is destructive) |
| `RemoveOtherDirectory` | `true`/`false` — replace `Other` on upgrade |

### [OptionalComponents]

Enables a second, optional installer section (typically extra languages,
or 32-bit vs 64-bit components).

| Key | Meaning |
|---|---|
| `OptionalComponents` | `true` enables the optional section |
| `MainSectionTitle` | Default: `AppName Portable (English) [Required]`. Omit if happy with default |
| `MainSectionDescription` | Default: `Install the portable app` |
| `OptionalSectionTitle` | Default: `Additional Languages` |
| `OptionalSectionDescription` | Default: `Add multilingual support for this app` |
| `OptionalSectionSelectedInstallType` | `InstallType` written to `appinfo.ini` when the optional section is chosen. Default `Multilingual` |
| `OptionalSectionNotSelectedInstallType` | `InstallType` when not chosen. Default `English` |
| `OptionalSectionPreSelectedIfNonEnglishInstall` | Pre-select optional section if the installer runs in a non-English language. Default `true` |
| `OptionalSectionPreSelectedIfWindows32Bit` | Pre-select on 32-bit Windows. Default `false` |
| `OptionalSectionPreSelectedIfLessThanWindows` | Pre-select when Windows version is less than the integer given: XP=5, Vista=6, 7=7, 8=8, 8.1=9, 10=10, 11=11 |
| `OptionalSectionInstalledWhenSilent` | Install the optional section in silent (Platform-driven) installs. Default `true` when the optional components are not additional languages. Ignored when `OptionalSectionPreSelectedIfWindows32Bit=true` |
| `OptionalDirectory1`, `OptionalDirectory2`, … | Relative paths placed in the optional section, e.g. `OptionalDirectory1=App\AppName\locales` |
| `OptionalFile1`, `OptionalFile2`, … | Relative file patterns in the optional section, e.g. `OptionalFile1=App\AppName\*.lang` |

You **must** list the optional content with `OptionalDirectory#` and/or
`OptionalFile#` when an optional section exists.

### [CopyLocalFiles]

Copies files in from an existing local installation of the app at install
time (used by "portable-izer" style packages).

| Key | Meaning |
|---|---|
| `CopyLocalFiles` | `true` enables the section |
| `CopyFromRegPath` | Registry key holding the local install path, e.g. `HKLM\Software\AppName` |
| `CopyFromRegKey` | Value name within that key holding the path |
| `CopyFromRegRemoveDirectories` | Number of trailing path components to strip from the registry value to reach the folder to copy. If the value points at a file, count the file name as one. Example: value `C:\Program Files\AppName\bin\AppName.exe`, copy from `C:\Program Files\AppName` → `2` |
| `CopyFromDirectory` | Local directory to copy from, e.g. `%PROGRAMFILES%\AppName`. Also used as fallback when the registry lookup fails. Available variables: `%PROGRAMFILES%`, `%COMMONFILES%`, `%DESKTOP%`, `%WINDIR%`, `%SYSDIR%`, `%APPDATA%`, `%LOCALAPPDATA%`, `%TEMP%` |
| `CopyToDirectory` | Destination inside the package, usually `App\AppName`. Created if missing |

### [DownloadFiles] — online installers

Downloads file(s) at install time and optionally extracts them. This is
how legally non-redistributable apps are packaged: the `.paf.exe` is
small and fetches the real app from the publisher during install. The
resulting file name ends in `_online.paf.exe`.

| Key | Meaning |
|---|---|
| `AdditionalInstallSize` | Size (KB, number only) the downloaded content adds beyond what is inside the installer |
| `DownloadURL` | URL of the file to download |
| `DownloadKnockURL` | URL that must be fetched **before** `DownloadURL` (e.g. a page that sets a cookie/token) |
| `DownloadName` | Display name shown while downloading. Must be a valid DOS name — no `: " \` etc. |
| `DownloadFilename` | Local working file name; normally the same file name as in `DownloadURL` |
| `DownloadSHA256` | SHA-256 hash of the downloaded file; the installer verifies it. **Highly recommended** — an unverified download is a supply-chain hole. (MD5 support was removed in Format 3.8.) |
| `DownloadTo` | Copy the downloaded file into the package as-is at this relative path (e.g. `App\AppName`). Do not combine with extraction keys |
| `DownloadInnoExtractTo` | Extract a downloaded **Inno Setup** installer into this relative path (e.g. `App\AppName`) |
| `DownloadInnoExtractFrom` | With the above: sub-directory inside the Inno package to take, e.g. `{app}` |
| `DownloadCachedByPAc` | Marks that PortableApps.com caches this download for Platform App Store installs/updates (the standalone installer does not use the cache) |
| `AdvancedExtract1To` / `AdvancedExtract1Filter` | Extract from a ZIP or many installer EXEs with 7-Zip semantics. `…To` = relative destination (typically `App\AppName`); supports `<ROOT>` for the package root. `…Filter` = 7-Zip-style filter: `*` all files in root, `**` all files recursively, `*.txt`, `Src\*.cpp`, etc. Up to **10** numbered entries (`AdvancedExtract1…` … `AdvancedExtract10…`) |
| `DoubleExtractFilename` | For an archive inside the downloaded archive: the inner archive's file name (e.g. download `setup.exe` contains `data.zip`) |
| `DoubleExtract1To` / `DoubleExtract1Filter` | Same as AdvancedExtract, applied to the inner archive. Up to 10 entries. `…To` supports `<ROOT>` |
| `Download2URL` … `Download2DoubleExtract1Filter` | A complete second set of the above keys prefixed `Download2` (including `Download2AdvancedExtract…` and `Download2DoubleExtract…`) for a second downloadable file |
| `CustomCodeUses7zip` | `true` if installer custom code calls `7z.exe` itself. 7-Zip is auto-included when any Advanced/DoubleExtract key is used |
| `UseLightweight7Zip` | `true` to use the smaller `7za.exe` (7-Zip Extras) instead of `7z.exe`+`7z.dll`; saves a few hundred KB in minimal online installers. Default `false` |

Notes:

- Deprecated `Extract1To`-style keys are auto-converted to
  `AdvancedExtract` keys when an old package is compiled.
- Downloads generally do not work on Windows 2000; SHA-256 verification
  also requires post-2000 Windows.
- Always pin `DownloadSHA256`. If the publisher re-issues the file under
  the same URL with a different hash, the install will (correctly) fail —
  update the hash deliberately, never delete it to "fix" the failure.
- There is **no mirror/fallback download key**. `Download2*` describes a
  *second* downloadable file, not an alternative source for the first.
  If `DownloadURL` dies, the install fails; the fix is a new package
  release with a corrected URL and hash.
- What the Installer does with an interrupted download is not documented
  here (**Unverified**). Test it once for your package (start an online
  install, cut the network, observe) and record the result in your
  release notes.
- MSI and RAR inputs: the Installer lists MSI among the formats its
  online mode can extract, and `AdvancedExtract` uses 7-Zip semantics,
  but this knowledge base has no worked MSI example and does not
  enumerate every archive format 7-Zip accepts. Verify your exact input
  format with a test build before relying on it (**Unverified** beyond
  the Inno/ZIP cases in `examples/06-online-installer/`).

### [Languages]

Which installer UI languages are offered. Only applies when
`appinfo.ini`'s `Language` is `Multilingual`. If the section is omitted,
all languages are included. If included, `ENGLISH=true` is **required**;
all others default to `false`. Keys are uppercase language names:
`ENGLISH`, `ENGLISHGB`, `AFRIKAANS`, `ALBANIAN`, `ARABIC`, `ARMENIAN`,
`ASTURIAN`, `BASQUE`, `BELARUSIAN`, `BENGALI`, `BOSNIAN`, `BRETON`,
`BULGARIAN`, `CATALAN`, `CIBEMBA`, `CORSICAN`, `CROATIAN`, `CZECH`,
`DANISH`, `DUTCH`, `EFIK`, `ESPERANTO`, `ESTONIAN`, `FARSI`, `FILIPINO`,
`FINNISH`, `FRENCH`, `GALICIAN`, `GEORGIAN`, `GERMAN`, `GREEK`, `HEBREW`,
`HINDI`, `HUNGARIAN`, `ICELANDIC`, `IGBO`, `INDONESIAN`, `IRISH`,
`ITALIAN`, `JAPANESE`, `KHMER`, `KOREAN`, `KURDISH`, `LATVIAN`,
`LITHUANIAN`, `LUXEMBOURGISH`, `MACEDONIAN`, `MALAGASY`, `MALAY`,
`MONGOLIAN`, `NORWEGIAN`, `NORWEGIANNYNORSK`, `PASHTO`, `POLISH`,
`PORTUGUESE`, `PORTUGUESEBR`, `ROMANIAN`, `RUSSIAN`, `SCOTSGAELIC`,
`SERBIAN`, `SERBIANLATIN`, `SESOTHO`, `SIMPCHINESE`, `SLOVAK`,
`SLOVENIAN`, `SPANISH`, `SPANISHINTERNATIONAL`, `SUNDANESE`, `SWAHILI`,
`SWEDISH`, `TAMIL`, `TATAR`, `THAI`, `TRADCHINESE`, `TURKISH`, `TWI`,
`UKRAINIAN`, `UYGHUR`, `UZBEK`, `VIETNAMESE`, `WELSH`, `YORUBA`, `ZULU`.

### [DirectoriesToPreserve] / [DirectoriesToRemove]

Up to 10 entries each: `PreserveDirectory1=` / `RemoveDirectory1=` with
relative paths (e.g. `App\AppName\plugins`). Preserve wins over a
`[MainDirectories]` removal; Remove wins over a preservation. Omit when
unused.

### [FilesToPreserve] / [FilesToRemove]

Same pattern for files (wildcards allowed): `PreserveFile1=App\AppName\*.hlp`,
`RemoveFile1=App\AppName\*.lang`. Up to 10 entries each.

### [LegacyVersions]

Lets an upgrade automatically spin off a **legacy copy** of the existing
install (e.g. `AppNamePortableLegacyWin7`) when the new version drops
support for the user's OS or for 32-bit Windows.

| Key | Meaning |
|---|---|
| `Legacy32AppIDSuffix` / `Legacy32AppNameSuffix` | Suffixes for the legacy package's AppID / display name for 32-bit Windows (e.g. `Legacy32bit` / `(Legacy 32-bit)`) |
| `Legacy32CutoffAppVersion` | App version (`x.x.x.x`) that ended 32-bit support; a legacy package is not created from an install already at/past it |
| `Legacy32RemoveAppSubDirectory` | Sub-directory to remove from the legacy copy (e.g. the 64-bit `AppName64` folder) |
| `Legacy32CustomLegacyAppID` | Custom legacy AppID (destination folder + launcher EXE/INI names) instead of the suffix-derived one |
| `LegacyOSAppIDSuffix` / `LegacyOSAppNameSuffix` | Same, for pre-cutoff Windows versions (e.g. `LegacyWin7` / `(Legacy Win7)`) |
| `LegacyOSCutoffOSVersion` | Windows version the new app requires: `XP`, `Vista`, `7`, `8.0`, `8.1`, `10`, `11` |
| `LegacyOSCutoffAppVersion` | App version (`x.x.x.x`) that dropped the legacy OS |
| `LegacyOSCustomLegacyAppID` | Custom legacy AppID for the OS-legacy package |

The installer looks for replacement launcher files in
`Other\Source\Legacy\<SuffixFolder>` of the **installing** package
(launcher EXE(s), INI, `custom.nsh`, plus a `Source` subfolder that
replaces the legacy copy's `Other\Source`).

## EULA display

Put `EULA.txt` (Unicode, not ANSI) in `App\AppInfo`. The installer finds
it automatically and shows it during install. Set `EULAVersion` in
`appinfo.ini`'s `[License]` when the EULA changes.

## Installer custom code (NSIS)

File: `Other\Source\PortableApps.comInstallerCustom.nsh` (Unicode, not
ANSI). It may define three macros:

| Macro | When it runs |
|---|---|
| `CustomCodePreInstall` | Before installation |
| `CustomCodePostInstall` | After installation |
| `CustomCodeOptionalCleanup` | At the start of installation when the optional section is **not** selected (for upgrades where the old install had it) |

Available beyond stock NSIS: `ConfigRead`, `ConfigReadS`, `ConfigWrite`,
`ConfigWriteS`, `GetParent`, `GetRoot`, `VersionCompare`, and LogicLib.
Set `CustomCodeUses7zip=true` in `[DownloadFiles]` if the code shells out
to 7-Zip.

## Installer logging

The installer writes `pac_installer_log.ini` into the installed
`App\AppInfo` directory, recording installer generation, installs,
wizard/installer versions and times. Do not alter or delete it (other
than via the official installer). **Exclude it from source control**
(`.gitignore`). Apps may read it to learn install time/method.

## Plugin installers

The Installer can also build **plugin installers** that add files to an
existing portable app:

- Configuration is a single `plugininstaller.ini` in `App\AppInfo`,
  combining everything that would be in `appinfo.ini` + `installer.ini`.
- `[Details]` gains `PluginName=` (e.g. `Adobe Flash for Firefox Portable`).
- All `[MainDirectories]` removal options default to `false`.
- EULA file is `PluginEULA.txt` instead of `EULA.txt`.
- Custom code file is `PortableApps.comInstallerPluginCustom.nsh` in
  `Other\Source`.
- Build a normal-looking package tree containing **only** the plugin's
  files; `App\AppInfo` contains only `plugininstaller.ini`.
- **CommonFiles installers** (install into `X:\PortableApps\CommonFiles`,
  for shared components like Java, designated by PortableApps.com): add
  `PluginType=CommonFiles` to `[Details]`. For these, `App` removal
  defaults to `true` (the whole `CommonFiles\<AppID>` folder is replaced).

## Installer behaviour worth knowing

- Installing into `C:\Program Files` (or equivalent) is **not supported**
  — portable apps install to a user-chosen folder, normally under a
  `PortableApps` directory on a portable drive or local disk.
- On upgrade, the installer checks whether the app is running
  (`[CheckRunning]`) and offers to close it before replacing files.
- In silent mode (driven by the Platform's app store/updater), prompts
  are suppressed and `[OptionalComponents]` silent rules apply.
- The installer appends the app folder name to a `/DESTINATION=`-style
  target: the user picks the **parent** (e.g. `X:\PortableApps`), the
  package installs to `X:\PortableApps\AppNamePortable`.
