# 01 — PortableApps.com Format 3.9 Specification

Based on the official PortableApps.com Format™ 3.9 specification
(2026-03-02), https://portableapps.com/development/portableapps.com_format

The Format governs the file/directory layout and operating behaviour of
portable apps. Packages are distributed as `.paf.exe` installer files built
by the PortableApps.com Installer.

## 1. Directory and file layout

```
AppNamePortable
+ App
   + AppInfo            configuration for the Platform + icons
      + FileTypeIcons   custom file-type icons (optional)
      + Launcher        launcher INI (+ custom.nsh) for PAL
   + AppName            the application binaries (usually)
   + DefaultData        first-run defaults copied into Data
+ Data                  ALL user data/settings; no binaries
+ Other
   + Help
      + Images          images used by help.html
   + Source             source, licenses, launcher readme, custom code
AppNamePortable.exe     the generated launcher (package root)
help.html               main help file (package root)
```

Rules:

- **Package root** contains only the launcher executable
  (`AppNamePortable.exe`) and `help.html` by default.
- **App** holds everything that makes up the application itself, usually in
  `App\AppName`. `AppInfo` holds configuration + icons and may hold the
  Launcher folder. `DefaultData` holds the default files that belong in
  `Data`; the launcher copies them into `Data` on first run when `Data`
  has no files yet.
- **Data** holds all user data — settings, configuration, profiles
  (Mozilla-style apps use `Data\profiles`, most apps use `Data\settings`).
  No application components (binaries) may be in `Data`. The launcher/app
  must be able to recreate `Data` and everything required in it if it is
  deleted.
- **Other** holds everything else: help images under `Other\Help\Images`,
  and source code, source licensing, installer source (if included), the
  launcher source/readme and license files under `Other\Source`.

## 2. appinfo.ini — complete reference

Location: `App\AppInfo\appinfo.ini`. INI format; do **not** put double
quotes inside field values.

### [Format]

| Key | Value |
|---|---|
| `Type` | Always `PortableApps.comFormat` (the only valid value) |
| `Version` | Format version the file follows; currently `3.9` |

### [Details]

| Key | Meaning |
|---|---|
| `Name` | Display name in the PortableApps.com Menu, e.g. `AppName Portable` |
| `AppID` | Globally unique ID. Official/publisher packages: the app name without spaces (`AppNamePortable`). Third-party packages must be suffixed: `AppNamePortable-example.com` (publisher domain) or `AppNamePortable-username` (PortableApps.com username, for individuals not working toward an official release). Allowed characters: letters, numbers, `.` `-` `+` `_` |
| `BaseAppName` | (Optional) Base app name when it differs from the launcher name. Only when legally required; otherwise omit |
| `Publisher` | Publisher name shown in hover tips and the app details screen. If repackaging someone else's app, list them too, e.g. `App Developer & PortableApps.com` |
| `Homepage` | Homepage of the **portable** app (not the base app) |
| `Donate` | (Optional) URL of a donations page |
| `Category` | Exactly one of: `Accessibility`, `Development`, `Education`, `Games`, `Graphics & Pictures`, `Internet`, `Music & Video`, `Office`, `Security`, `Utilities`. Use the English string even for non-English apps |
| `Description` | Brief description, **maximum 512 characters** |
| `Language` | `Multilingual`, or one of the fixed language strings: Afrikaans, Albanian, Arabic, Armenian, Basque, Belarusian, Bosnian, Breton, Bulgarian, Catalan, Cibemba, Croatian, Czech, Danish, Dutch, Efik, English, EnglishGB, Esperanto, Estonian, Farsi, Finnish, French, Galician, Georgian, German, Greek, Hebrew, Hindi, Hungarian, Icelandic, Igbo, Indonesian, Irish, Italian, Japanese, Khmer, Korean, Kurdish, Latvian, Lithuanian, Luxembourgish, Macedonian, Malagasy, Malay, Mongolian, Norwegian, NorwegianNynorsk, Pashto, Polish, Portuguese, PortugueseBR, Romanian, Russian, Serbian, SerbianLatin, SimpChinese, Slovak, Slovenian, Spanish, SpanishInternational, Swahili, Swedish, Thai, TradChinese, Turkish, Ukrainian, Uzbek, Valencian, Vietnamese, Welsh, Yoruba |
| `Trademarks` | (Optional) Trademark notices. Double quotes are converted to single quotes |
| `InstallType` | (Optional) Specific install type shown in the Platform (e.g. a language edition). With optional installer components, the installer updates this automatically from `installer.ini` |

### [License] — all values `true`/`false`

| Key | Meaning |
|---|---|
| `Shareable` | App may be copied drive-to-drive (without the `Data` directory) |
| `OpenSource` | Fully open source under an OSI-approved license |
| `Freeware` | Free of cost |
| `CommercialUse` | May be used in a business environment (does **not** grant commercial distribution) |
| `EULAVersion` | (Optional) Version of the EULA shown from `EULA.txt` at install time; defaults to `1` when a EULA is used |

### [Version]

| Key | Meaning |
|---|---|
| `PackageVersion` | Package version, **exactly `x.x.x.x`** numeric format, incremented with every public release. This is what the Platform compares for updates |
| `DisplayVersion` | Human-friendly version, e.g. `2.4 Revision 2` for PackageVersion `2.4.0.2` |

Versioning convention: `PackageVersion` is normally the base app's version
padded to four parts; the 4th part is the portable-package revision
(`2.4.4.1` = app 2.4.4, first portable packaging; `2.4.4.2` = packaging
fix revision 2 of the same app version).

### [SpecialPaths] (optional)

| Key | Meaning |
|---|---|
| `Plugins` | Path (inside the package) of a user-added plugins directory inside `App` (e.g. Firefox-style). Excluded from the free-space calculation on upgrade. Omit entirely if there is no plugins directory |

### [Dependencies] (optional)

| Key | Values / meaning |
|---|---|
| `UsesGhostscript` | `yes` / `no` / `optional` (optional = Ghostscript Portable adds features but is not required) |
| `UsesJava` | `yes` / `no` / `optional` — same pattern for Java Portable (jPortable). Deprecated `true`/`false` are read as `yes`/`no` |
| `UsesDotNetVersion` | Minimum .NET requirement. Bundled-runtime values: `5bundle`…`10bundle` (.NET 5–10 included with the app). Framework ranges: `4or3.5`, `4or3`, `4or2`. Specific Framework: `4.8`, `4.7.2`, `4.7.1`, `4.7`, `4.6.2`, `4.6.1`, `4.6`, `4.5.2`, `4.5.1`, `4.5`, `4`, `3.5`, `3`, `2`, `1.1`, `1`. Specific Core/.NET (install required, not yet Platform-supported): `7`, `6`, `5`, `3.1core`, `3core`, `2.2core`, `2.1core`, `2core`, `1.1core`, `1core`. Omit when the app needs no .NET |
| `Requires64bitOS` | `yes` if the app requires a 64-bit OS; default `no` |
| `RequiresPortableApp` | AppID of another portable app this one requires (not yet Platform-supported) |
| `RequiresAdmin` | `yes` if the app requires admin rights; default `no` |

### [Control]

| Key | Meaning |
|---|---|
| `Icons` | Number of icons (launch entries) the app has in the menu |
| `Start` | Command to start the app, relative to the package root — normally `AppNamePortable.exe` |
| `ExtractIcon` | (Optional, single-icon apps only) Extract the menu icon from this file instead of using `appicon.ico`. Only when legally required; slows menu access; omit normally |
| `ExtractName` | (Optional, single-icon apps only) Extract the app name from this file. Same restrictions as `ExtractIcon` |
| `BaseAppID` | Windows AppUserModelID of the base app, used for taskbar pinning (Platform 16+). Use `NOT-NEEDED` for apps with no taskbar icon |
| `BaseAppID64` | Same, for the 64-bit build on 64-bit Windows |
| `BaseAppIDARM64` | Same, for ARM64 builds (Platform 24+) |
| `ExitEXE` / `ExitParameters` | (Optional) Command + parameters to cleanly exit the app, relative to package root. Not yet used by the Platform |

Multiple icons (e.g. a suite): set `Icons=2` and add `Start1`/`Name1`,
`Start2`/`Name2`, … `Start` remains the main entry. `ExtractIcon1`,
`ExtractIcon2`, … exist under the same legal-requirement restriction.

### [Associations] (optional — omit if the app opens no file types/protocols)

| Key | Meaning |
|---|---|
| `FileTypes` | Comma-delimited extensions the app can open: `txt,html,doc` |
| `FileTypeCommandLine` | Parameter pattern passed to the launcher to open a file; `%1` marks where the file goes. Omit if passing the file directly works |
| `FileTypeCommandLine-<ext>` | Per-extension override of the above |
| `Protocols` | Comma-delimited protocols the app handles: `http,https,mailto,torrent` |
| `ProtocolCommandLine` | Parameter pattern for protocols; `%1` marks the URL/string position |
| `ProtocolCommandLine-<protocol>` | Per-protocol override |
| `SendTo` | `true` only for the small set of apps that belong in the Windows Send To menu (e.g. antivirus); generally omit |
| `SendToCommandLine` | Parameter pattern for Send To; `%1` = sent file(s) |
| `Shell` | `true` only for apps acting as a Windows shell; generally omit |
| `ShellCommand` | Shell command pattern using `%I` and `%L` |

### [FileTypeIcons] (optional)

Maps extensions from `[Associations]` to icon handling. Needed only for
types the Platform does not already know. Each value is either a built-in
category name, `app` (use the app's main icon), or `custom` (icons supplied
in `App\AppInfo\FileTypeIcons`). Built-in categories and their default
extensions:

- **archive**: 7z, bzip2, cab, gz, gzip, rar, tar, zip, wim, xz, z
- **audio**: aac, aif, iff, flac, m3u, m3u8, m4a, mid, midi, mp3, mpa, ogg, pls, ra, wav, wv
- **calendar**: ical, icalendar, ics, ifb, vcs
- **chart**: (none by default)
- **code**: ada, ads, adb, asm, asp, aspx, au3, bas, c, cmake, h, hpp, hxx, cpp, cc, cs, css, d, diff, patch, es, iss, java, js, jsp, lua, m, mak, nsi, nsh, pas, inc, pl, pm, plx, php, php3, phtml, pro, ps1, py, pyw, r, rb, rbw, rc, sql, vb, vbs, xml, xsml, xsl, xsd, wsdl
- **contact**: vcard, vcf
- **database**: db, odb, sqlite
- **diskimage**: cue, img, iso
- **drawing**: ai, eps, odg, otp, sda, sdd, sgv, std, svg, svgz, sxd
- **document**: abw, djvu, doc, docm, docx, dotx, dotm, fodt, odt, ott, pdf, rtf, stw, sxw, uot, ps
- **ebook**: azw, cbr, cbz, epub, lrf, lrx, lit, mobi
- **font**: fnt, otf, ttf
- **image**: ani, bmp, cur, ico, jpg, jpeg, gif, ora, pcx, png, psd, tif, tiff, xcf
- **java**: jar
- **presentation**: odp, otp, sxi, sti, sxd, pps, ppsx, ppt, pptm, pptx, pot, sdd, sdp
- **spreadsheet**: gnumeric, ods, ots, sxc, stc, xls, xlc, xlm, xlw, xlk, sdc, csv, xlsx, xlsm
- **text**: cfg, inf, ini, log, nfo, txt, text
- **torrent**: torrent
- **video**: 3gp, asf, avi, flv, mp4, m4v, mpe, mpeg, mpg, mkv, mov, ogm, qt, rm, rmvb, webm, wmv
- **webpage**: html, htm, mht, mhtml, shtml, xhtml, xhtm, xht

`AllOtherIcons=<category|app|custom>` is a catch-all for associated types
not otherwise listed. Associated types with no entry default to `app`.

### Complete example

See `templates/MinimalAppPortable/App/AppInfo/appinfo.ini`.

## 3. Icons

In `App\AppInfo`:

- Main icon: `appicon.ico` plus PNGs `appicon_16.png`, `appicon_32.png`,
  `appicon_75.png`, `appicon_128.png`, `appicon_256.png` (true colour with
  alpha; sizes match the suffixes).
- Extra icons for multi-icon apps: `appicon1.ico` / `appicon1_16.png` /
  `appicon1_32.png` / …, numbered to match `Start1`, `Start2`, …
- `appicon.ico` must contain: 16/32/48 px at 256 colours (8-bit),
  16/32/48 px at true colour + alpha (32-bit), and 256 px true colour +
  alpha as PNG.
- Custom file-type icons go in `App\AppInfo\FileTypeIcons` named after the
  extension: for `swf=custom`, provide `swf.ico`, `swf_16.png`,
  `swf_32.png`, `swf_128.png`. For `AllOtherIcons=custom`, the files are
  `AllOtherIcons.ico`, `AllOtherIcons_16.png`, etc.
- With `ExtractIcon` in use, `appicon.ico`/PNGs are unused and may be
  omitted; a generic `appicon.ico` is included for backwards compatibility.

## 4. Host PC modifications & portability (Format §5)

- A portable app **may** modify registry entries and local files while
  running, but must return them to their exact pre-run state on exit —
  including backing up and restoring a locally installed copy's settings.
- The app must keep working (settings, preferences, language, MRU file
  lists) as the drive letter changes between computers.
- This is the rule the Launcher exists to enforce; see
  `docs/03-launcher-overview.md`.

## 5. Format version history (recent)

- **3.9 (2026-03-02)** — custom legacy App ID in installer Legacy sections;
  multiple-EXE and Source copying in Legacy sections; more .NET directives;
  `ExitEXE`/`ExitParameters`; LegacyVersions handling.
- **3.8 (2024)** — `UseLightweight7Zip`; `RequiresAdmin`;
  `OptionalSectionPreSelectedIfLessThanWindows`; Inno Setup extraction;
  32/64-bit optional components; MD5 removed (SHA256 only).
- **3.7 (2023)** — `BaseAppIDARM64`; `DownloadSHA256`.
- **3.6 (2022)** — `Requires64bitOS`, `RequiresPortableApp`, 256 px PNG
  icon, full .NET Framework/Core value set, AppCompactor section removed
  (AppCompactor is no longer used for official releases).
