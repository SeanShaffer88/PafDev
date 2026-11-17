# Real-World Configurations (Mirrored)

These are **actual production configuration files** from official PortableApps.com
packages, mirrored from the PortableApps **AppConfigs** repository
(https://github.com/PortableApps/AppConfigs) so this knowledge base is
self-contained. AppConfigs holds the `App\AppInfo` configuration for every app
PortableApps.com publishes, organized by first letter of the app name
(`A\…`, `B\…`, `#\…` for names starting with a digit). Each app folder is flat and
contains some or all of:

| File | What it is |
|---|---|
| `appinfo.ini` | The package metadata ([`../../docs/01-format-spec.md`](../../docs/01-format-spec.md)) |
| `installer.ini` | The Installer configuration ([`../../docs/02-installer-and-installer-ini.md`](../../docs/02-installer-and-installer-ini.md)) |
| `<AppID>.ini` | The Launcher INI, e.g. `Notepad++Portable.ini` ([`../../docs/04-launcher-ini-reference.md`](../../docs/04-launcher-ini-reference.md)) |
| `Custom.nsh` | Launcher custom code ([`../../docs/05-launcher-advanced-custom-code.md`](../../docs/05-launcher-advanced-custom-code.md)) |
| `PortableApps.comInstallerCustom.nsh` | Installer custom code ([`../../docs/02-installer-and-installer-ini.md`](../../docs/02-installer-and-installer-ini.md)) |

**Study these before writing your own configs.** They are the ground truth for
how the format is used in practice — including a few things the manuals do not
document (below). Files are mirrored verbatim; they are the work of
PortableApps.com and the respective app publishers, distributed under the same
open-source terms as the packages they ship in.

## Included here

### `notepadplusplus/` — a complete config set

All five file types for Notepad++ Portable. Study especially:

- **The path-migration triple.** Every config file that stores absolute paths
  gets **three** `[FileWriteN]` `Replace` sections, most specific first:
  1. `%PAL:LastDrive%%PAL:LastPackagePartialDir%\` → `%PAL:Drive%%PAL:PackagePartialDir%\`
  2. `%PAL:LastPortableAppsBaseDir%\` → `%PAL:PortableAppsBaseDir%\`
  3. `%PAL:LastDrive%\` → `%PAL:Drive%\`

  Notepad++ repeats the triple for each of its five path-storing files
  (FileWrite1–15). Never write just one — a file can contain any of the three
  path forms. See [`../../docs/04-launcher-ini-reference.md`](../../docs/04-launcher-ini-reference.md).
- **`%FullAppDir%` is a custom variable, not a built-in.** The launcher INI uses
  `%FullAppDir%` as the `[FilesMove]`/`[DirectoriesMove]` target, and
  `Custom.nsh` defines it in `${SegmentInit}` with
  `${SetEnvironmentVariablesPath} FullAppDir $strCustomFullAppDir`, choosing the
  32-bit or 64-bit app folder based on `$Bits`. This is the standard pattern
  when the real app folder differs between 32/64-bit builds.
- **`-=HKLM\...` in `[RegistryKeys]`** — the `-` filename discards changes to a
  file-association key the app touches, protecting the host.
- **Installer custom code doing a settings migration**: the
  `PortableApps.comInstallerCustom.nsh` moves a legacy `Data\settings` layout to
  `Data\Config` during upgrade (backup first, in `CustomCodePreInstall`;
  finishing touches in `CustomCodePostInstall`). This is how shipped packages
  survive their own layout changes.
- `appinfo.ini` shows `[Control] BaseAppID`/`BaseAppID64` with the
  `%BASELAUNCHERPATH%` token and a long `[Associations] FileTypes` list.

### `7zip/7-ZipPortable.ini` — launcher INI only

7-Zip Portable's launcher INI demonstrates techniques Notepad++ doesn't:

- **`[FileWriteN]` on the saved registry file itself.** FileWrite1 uses
  `Type=INI` against `Data\settings\7zip_portable.reg` to rewrite the `Lang`
  value inside the exported `.reg` before it is imported — the way to inject
  the Platform language into registry-based settings.
- **The migration triple in `:DoubleBackslash` form**, because paths inside a
  `.reg` file are stored with doubled backslashes — plus a **fourth** replace
  for hex-encoded paths in `REG_BINARY` values using
  `%PAL:LastDriveHex%` / `%PAL:DriveHex%` (the drive letter as hex bytes,
  e.g. `X,00,3a,00` in the file appears as the literal text of the hex data).
- **The full language chain**: `[Language]` with
  `CheckIfExists=%PAL:FullAppDir%\Lang\%PAL:LanguageCustom%.txt` and
  `DefaultIfNotExists=en`, a `[LanguageStrings]` mapping, and a
  `[LanguageFile]` `ConfigRead` that reads the current language back out of the
  saved `.reg` data (`Entry='"Lang"="'`, `TrimRight="`) when the app was not
  launched from the Platform.
- **`%PAL:FullAppDir%`** (with the `PAL:` prefix) is used here as a built-in —
  the directory of the running `ProgramExecutable` under `App\`. It is absent
  from the PAL 2.2 manual's envsub page but is used by official production
  configs; treat it as real. Do not confuse it with a package-defined
  `%FullAppDir%` (Notepad++, above).

## How to use AppConfigs yourself

1. Find the app (or a similar app) in the letter folder.
2. Read its launcher INI and map every section back to the behavior it
   produces, using the trace method in
   [`../../docs/07-end-to-end-workflow.md`](../../docs/07-end-to-end-workflow.md).
3. Borrow patterns, not whole files — versions in AppConfigs may target older
   format versions (e.g. Notepad++'s `appinfo.ini` still declares
   `[Format] Version=3.5`); always reconcile against the current Format
   specification in [`../../docs/01-format-spec.md`](../../docs/01-format-spec.md).
