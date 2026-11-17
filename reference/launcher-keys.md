# Reference — Launcher INI Quick Keys

The sections and keys reached for most often. **The full reference is
[`../docs/04-launcher-ini-reference.md`](../docs/04-launcher-ini-reference.md) —
never write a key from this quick list alone into a package without
checking its documented values there.** Unknown sections and keys
fail **silently** in PAL; [`../tools/check-package.py`](../tools/)
validates names against the full inventory.

## Sections

| Section | Purpose |
|---|---|
| `[Launch]` | The executable and how it is launched (below) |
| `[Activate]` | Feature switches: `Registry`, `Java`, `XML`, `INI` — required companions to the sections they enable (e.g. `[RegistryKeys]` needs `Registry=true`) |
| `[RegistryKeys]` | Registry keys saved to `Data\settings\` while running, restored/removed on exit |
| `[RegistryValueWrite]` / `[RegistryValueBackupDelete]` | Individual registry values written, or backed up and deleted |
| `[RegistryCleanupIfEmpty]` / `[RegistryCleanupForce]` | Parent keys cleaned up on exit (Force deletes unconditionally — scope it narrowly, AGENTS.md) |
| `[FilesMove]` | Files (e.g. in the app's own folder or profile) redirected to `Data\` |
| `[DirectoriesMove]` | Whole directories (typically `%APPDATA%\Publisher\App`) redirected to `Data\` |
| `[DirectoriesCleanupIfEmpty]` / `[DirectoriesCleanupForce]` | Directory cleanup on exit |
| `[FileWriteN]` | Rewrites inside text config files (paths made portable) — numbered: `[FileWrite1]`, `[FileWrite2]`, … |
| `[Environment]` | Environment variables set for the app process (values use `%PAL:%` variables) |
| `[Language]` / `[LanguageFile]` / `[LanguageStrings]` | Passing the Platform language to the app |
| `[LiveMode]` | Behaviour when running from a local (non-portable) copy |
| `[QtKeysCleanup]` | Qt's registry traces (this exact name — `[Qt]` does not exist) |
| `[ServiceN]` | Services — **disabled in PAL 2.2**; do not build on it |

## [Launch] keys (the common set)

| Key | Meaning in one line |
|---|---|
| `ProgramExecutable` | Path of the real exe, relative to `App\` (backslashes) |
| `ProgramExecutableWhenParameters` | Alternate exe used when arguments are passed |
| `CommandLineArguments` / `AdditionalParameters` | Fixed arguments for the app |
| `WorkingDirectory` | Working directory for the process |
| `DirectoryMoveOK` | `yes` / `no` / `warn` — may the package folder move? Leave `warn` until move-tested |
| `SupportsUNC` | `yes` / `no` / `warn` — UNC path support; same rule |
| `SingleAppInstance` / `SinglePortableAppInstance` | Second-launch behaviour |
| `WaitForProgram` / `WaitForOtherInstances` | Launcher waits before cleanup |
| `CloseEXE` | Companion exe the launcher also waits for/closes |
| `RunAsAdmin` | `none` (default) / `try` / `force` / `compile-force` — least elevation wins (docs/18) |
| `MinOS` / `MaxOS` | Windows version window (`none`, `2000`, `XP`, `Vista`, … per docs/04) |
| `DisableSplashScreen` / `SplashTime` / `LaunchAppAfterSplash` | Splash behaviour |
| `CleanTemp` | Clean the app's `%TEMP%` traces on exit |
| `RefreshShellIcons` | Refresh shell icons after exit (file-association apps) |
| `NoSpacesInPath` | App breaks on paths containing spaces |
| `HideCommandLineWindow` | Hide the console of a command-line child |
| `RunLocally` | Live Mode: run from a local copy instead |
