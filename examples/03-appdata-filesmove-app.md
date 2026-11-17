# Example 3 — %APPDATA% app with stored absolute paths

**Shape:** the base app keeps its profile in
`%APPDATA%\Publisher\MailTool`, and inside `profile.ini` in that folder
it stores the absolute path of its data store
(`storepath=X:\...`). When the drive letter changes, the app loses its
mail store unless the path is rewritten at launch.

Two mechanisms combine:

1. `[DirectoriesMove]` shuttles the profile folder between
   `Data\MailToolConfig` and `%APPDATA%\Publisher\MailTool`.
2. `[FileWriteN]` sections with `Type=Replace` rewrite the stored path
   inside `profile.ini` before launch. Production packages use the
   **path-migration triple** (see
   [`../docs/04-launcher-ini-reference.md`](../docs/04-launcher-ini-reference.md)):
   one replace for the package path, one for the PortableApps base path,
   one for the bare drive — because a stored path can take any of those
   forms. This example uses all three.

## launcher INI — `App\AppInfo\Launcher\MailToolPortable.ini`

```ini
[Launch]
ProgramExecutable=MailTool\MailTool.exe
DirectoryMoveOK=yes
SupportsUNC=warn

[DirectoriesMove]
MailToolConfig=%APPDATA%\Publisher\MailTool

[DirectoriesCleanupIfEmpty]
1=%APPDATA%\Publisher

[FileWrite1]
Type=Replace
File=%PAL:DataDir%\MailToolConfig\profile.ini
Find=%PAL:LastDrive%%PAL:LastPackagePartialDir%\
Replace=%PAL:Drive%%PAL:PackagePartialDir%\

[FileWrite2]
Type=Replace
File=%PAL:DataDir%\MailToolConfig\profile.ini
Find=%PAL:LastPortableAppsBaseDir%\
Replace=%PAL:PortableAppsBaseDir%\

[FileWrite3]
Type=Replace
File=%PAL:DataDir%\MailToolConfig\profile.ini
Find=%PAL:LastDrive%\
Replace=%PAL:Drive%\
```

How it works:

- `[FileWriteN]` runs before launch, against the file **in `Data`** —
  the path above points at the Data copy, which is then moved into
  `%APPDATA%` by `[DirectoriesMove]` for the run.
- On the first run, each `Last…` variable equals its current counterpart,
  so the replaces are skipped automatically.
- Order matters: most specific (full package path) first, bare drive
  last — otherwise the bare-drive replace would corrupt the longer
  matches before they run.
- `DirectoryMoveOK=yes` is justified precisely because these FileWrites
  handle every move-sensitive stored path — that is the pattern the
  manual prescribes.
- If this app stored paths *without* a drive letter (partial-dir form
  only), the first and third replaces simply never match and are
  harmless. Keep the triple anyway: an app update can change the stored
  form without warning. Note the drive replaces mean UNC runs get
  `SupportsUNC=warn` unless you have actually tested UNC paths.

## DefaultData

Ship `App\DefaultData\MailToolConfig\profile.ini` with a
`storepath` pointing at a placeholder under the package partial dir, so
first-run FileWrite and the app both find a valid file.

## Testing focus

The drive-letter test is the whole point of this example: run once from
`E:`, create data, move the package to `F:` (and to a different folder
depth), run again — the store must open with all data intact.
