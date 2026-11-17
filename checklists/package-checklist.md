# Package Structure Checklist

Run against the package **source tree** before generating the launcher
and building the installer.

## Layout

- [ ] Folder is named `<AppID>` (e.g. `AppNamePortable`), no spaces.
- [ ] Package root contains only the launcher exe (once generated),
      `help.html`, and the `App` / `Data` / `Other` folders.
- [ ] Binaries are under `App\<AppName>\`; no binaries in `Data`.
- [ ] `Data` ships empty (or with only a placeholder) — no developer
      machine user data in the distributed tree.
- [ ] First-run defaults, if any, are in `App\DefaultData` mirroring the
      `Data` structure.
- [ ] Help images are in `Other\Help\Images`; sources, licenses and the
      launcher readme are in `Other\Source`.

## appinfo.ini

- [ ] `[Format] Type=PortableApps.comFormat`, `Version=3.9`.
- [ ] `AppID` equals the folder name (or correctly suffixed for
      third-party packages).
- [ ] `Category` is one of the 10 fixed values, spelled exactly.
- [ ] `Description` ≤ 512 characters; no double quotes in any field.
- [ ] `[License]` booleans are true **for this app**.
- [ ] `PackageVersion` is exactly 4 numeric parts and higher than the
      last public release.
- [ ] `DisplayVersion` matches the file name you will ship.
- [ ] `[Dependencies]` declares Java/.NET/Ghostscript/64-bit/admin
      requirements that actually apply — and none that don't.
- [ ] `[Control] Start` names the generated launcher exe exactly.
- [ ] `BaseAppID` set, or explicitly `NOT-NEEDED`.

## Icons

- [ ] `App\AppInfo\appicon.ico` contains 16/32/48 px 8-bit, 16/32/48 px
      32-bit, and 256 px PNG-compressed entries.
- [ ] `appicon_16.png`, `appicon_32.png`, `appicon_75.png`,
      `appicon_128.png`, `appicon_256.png` present, true colour + alpha.
- [ ] Multi-icon apps: `appicon1…`, `appicon2…` match `Start1`, `Start2`.
- [ ] Custom file-type icons (if `[FileTypeIcons]` uses `custom`) are in
      `App\AppInfo\FileTypeIcons` with all required sizes.

## Launcher

- [ ] Launcher INI is at `App\AppInfo\Launcher\<AppID>.ini` and its base
      name matches the launcher exe.
- [ ] Every key in the INI exists in
      `docs/04-launcher-ini-reference.md` (no invented keys).
- [ ] `[Launch] ProgramExecutable` is relative to `App\` and points at a
      file that exists in the tree.
- [ ] `[Activate] Registry=true` is present iff registry sections exist.
- [ ] `[Activate] XML=true` is present iff XML FileWrite/LanguageFile
      types are used.
- [ ] Every item in the app's trace inventory maps to a launcher
      mechanism (move, registry, FileWrite, environment, custom code).
- [ ] Numbered sections (`[FileWriteN]`, cleanup lists,
      `[RegistryValueBackupDelete]`) are consecutive starting at 1.
- [ ] No `settings` directory move (would clobber `Data\settings\*.reg`).
- [ ] Launcher has been **regenerated** after the last INI edit.
- [ ] Example user config in `Other\Source\<AppID>.ini` matches the
      keys `help.html` documents.

## installer.ini (if present)

- [ ] Contains only the features this package needs (not a copied
      full-option example).
- [ ] Online installers: `DownloadSHA256` is the real current hash of
      the publisher's file.
- [ ] `[MainDirectories] RemoveDataDirectory` is not `true`.
- [ ] Optional components actually list their directories/files.

## Security (see `docs/18-security-privacy-and-abuse.md`)

- [ ] Base app was downloaded from the publisher's canonical URL and
      verified against the publisher's signature/published hash; source
      URL and SHA-256 recorded in the project notes (bundled packages
      too, not just online installers).
- [ ] Online installers: `DownloadURL`/`DownloadKnockURL` are the
      publisher's own HTTPS addresses; `DownloadSHA256` is set.
- [ ] `RunAsAdmin` is `none`, or the value used is justified in the
      package notes and `RequiresAdmin=yes` is set in appinfo.ini.
- [ ] `[RegistryCleanupForce]` / `[DirectoriesCleanupForce]` entries are
      scoped to trees the trace inventory proved the app creates;
      `IfEmpty` variants used where they suffice.
- [ ] `[CopyLocalFiles]`, if present, copies only the documented paths,
      and help.html states what local data is imported.
- [ ] Every `.nsh` file in the tree (Custom.nsh, installer custom code,
      Debug.nsh, Legacy launchers) has been read line-by-line — none
      copied unread from AppConfigs, forums, or templates.
- [ ] No `[FilesMove]`/`[DirectoriesMove]` entry moves DLLs or scripts
      through `Data\`; `[SpecialPaths] Plugins` declared iff a real
      user-plugins folder exists.
- [ ] `DirectoryMoveOK` / `SupportsUNC` are `yes` only if the matching
      tests in `docs/08` actually passed — otherwise `warn`.
