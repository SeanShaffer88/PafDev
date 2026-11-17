# 08 — Testing, Debugging, and Troubleshooting

## The test matrix

Test the **extracted/installed package**, never just the build tree, and
test a fresh copy for each "first run" item (delete `Data` contents
between first-run tests).

### First run and persistence

- [ ] First launch: `Data` is populated from `App\DefaultData`; the app
      starts with sane defaults.
- [ ] Change every category of setting (options, window size, recent
      files, language); close; relaunch: all persist.
- [ ] Create user data inside the app (documents, profiles, playlists):
      it lands inside `Data`, not in `App` and not on the host.
- [ ] Delete the `Data` folder entirely: the app recreates it and starts
      cleanly (Format requirement).

### Portability

- [ ] Copy the package to a different drive letter: settings, MRU lists,
      and language survive; no "file not found" for internal paths.
- [ ] Run from a path containing spaces and from a path containing
      non-ASCII characters.
- [ ] Run from a read-only location with `RunLocally` (user config): the
      launcher copies to a temp folder and runs from there.
- [ ] Run via UNC path if `[Launch] SupportsUNC` is claimed.
- [ ] Limited (non-admin) Windows user account: full functionality unless
      the app itself needs admin.

### Host cleanliness (the leak test)

1. On a clean VM/snapshot, record registry + file state (RegShot Shot 1).
2. Run the portable app, use it, close it, wait for the launcher to exit
   fully (check Task Manager — the launcher waits for child processes).
3. Shot 2 + compare: **zero** new/changed keys or files attributable to
   the app outside the package folder. Temp files the app creates and
   Windows itself creates (Prefetch, etc.) are OS noise; settings,
   caches with user data, and registry keys are leaks.
4. Repeat with a **locally installed copy of the same app present**:
   before the portable run, set a distinctive value in the local copy's
   settings; after the portable run, the local value must be intact and
   the portable run must not have read it.

### Lifecycle

- [ ] Launch while the app is already running: behaviour matches
      `[Launch] SingleAppInstance` / `SinglePortableAppInstance` intent
      (second launch passes the file/argument to the running instance or
      is refused cleanly — never a corrupted settings file).
- [ ] Open a file via the Platform / Explorer "Open With" / drag-and-drop
      onto the launcher exe: the app opens that file (argument passing).
- [ ] Close the app via its own exit path and via closing the launcher's
      watched EXE: cleanup still happens.
- [ ] Crash the app (kill the process): on next launch the launcher
      recovers (it detects the unclean exit and restores backups).
- [ ] Eject/remove the drive while running is *not* a supported scenario;
      but a forced launcher kill must not corrupt `Data`.

### Installer

- [ ] Fresh install of the `.paf.exe` to an empty `PortableApps` folder.
- [ ] Install while the app is running: installer detects it
      (`[CheckRunning]`) and offers to close it.
- [ ] Upgrade over the previous version: settings preserved, replaced
      binaries actually replaced, removed files actually removed
      (`[FilesToRemove]`/preservation rules honoured).
- [ ] Online installer: download verifies against `DownloadSHA256`;
      a tampered/wrong download fails loudly, not silently.
- [ ] Install to a path with spaces; install when the target drive is
      nearly full (installer must refuse cleanly).

### Contexts (add the rows that match what help.html claims)

- [ ] Cloud folder: package inside a synced folder (OneDrive/Dropbox/
      Google Drive), sync client running; run on machine A, let it sync,
      run on machine B: settings intact, no sync-conflict copies inside
      `Data`. (PAL behaviour under sync clients is **Unverified** —
      record what you observe.)
- [ ] Second Windows user account on the same PC: the portable run does
      not read or alter the other account's local settings.
- [ ] Deep path: install under a folder path of 200+ characters; first
      run, persistence, and Live mode all work.
- [ ] Non-English Windows image (if multilingual is claimed): installer
      language, app language via the Platform, and the `[LanguageFile]`
      fallback when launched directly all behave.
- [ ] Policy-realistic account: standard user, no elevation available;
      every non-admin feature works, admin features refuse cleanly.
- [ ] Offline: with networking disabled, a full installer installs and
      runs; an online installer fails with a clear message and leaves no
      half-installed package. (Expected online-installer failure
      behaviour: **Unverified** — record what you actually observe.)
- [ ] Keyboard-only pass: installer, splash dismissal, and first run
      completed without a mouse (`docs/19-accessibility.md`).
- [ ] (Optional, community packages) Wine: the package installs and runs
      under Wine. Not an official-format requirement.

## Debugging the launcher

- **PAL debug builds:** put debug flags in
  `App\AppInfo\Launcher\Debug.nsh` (PAL 2.1+ location; see
  `docs/05-launcher-advanced-custom-code.md`) and regenerate — the
  Generator finds the file and compiles debugging in. Debug output goes
  to message boxes **and to `Data\debug.log`** in the package. Debugging
  is compile-time only; there is no runtime debug switch. **Remove
  `Debug.nsh` for release builds** or users get a debug build.

  | Flag in Debug.nsh | Effect |
  |---|---|
  | `!define DEBUG_ALL` | Debug almost everything (`DEBUG_GLOBAL` + all segment flags; segment announcements still need `DEBUG_SEGWRAP`) |
  | `!define DEBUG_GLOBAL` | Debug code outside all segments |
  | `!define DEBUG_SEGMENT_<SegmentName>` | Debug one segment, e.g. `DEBUG_SEGMENT_RunAsAdmin` (segment names in `docs/05…`) |
  | `!define DEBUG_SEGWRAP` | Announce each segment as it starts/finishes ("About to execute segment" / "Finished executing segment") |
  | `!define DEBUG_OUTPUT file` | Output to `Data\debug.log` only. `messagebox` = boxes only. Default (unset) = both; any other value silences output |

- **Harmless Generator warnings:** `!include: could not find:
  "…\Other\Source\PortableApps.comLauncherCustom.nsh"` (and the same for
  `…LauncherDebug.nsh`) are **warnings, not errors** — they simply mean
  the package has no custom code / no debug code. Do not create empty
  files to silence them.
- **Bisect the INI:** comment out half the move/registry entries, retest,
  narrow down. Launcher problems are almost always one bad entry.
- **Watch live:** Process Monitor (ProcMon) filtered to the app process
  shows every file/registry access in real time — the fastest way to find
  a settings location the RegShot pass missed (e.g. writes that only
  happen on a specific feature).
- **Check the wait chain:** if cleanup does not happen, the app probably
  spawned a child process that outlives the main EXE. Use
  `[Launch] WaitForEXE1`… (see the launcher reference) so the launcher
  waits for the real worker process.

## Common problems and fixes

| Symptom | Likely cause | Fix |
|---|---|---|
| Settings reset every run | Settings location not captured; app writes to `%APPDATA%` or registry that is never moved | Find the real location (ProcMon/RegShot), add `[FilesMove]`/`[DirectoriesMove]`/`[RegistryKeys]` |
| Settings reset only when drive letter changes | App stores absolute paths in its settings file | `[FileWriteN]` to rewrite the path on each launch with `%PAL:DataDir%` etc. |
| Local install's settings changed after portable run | Launcher key/file overlaps the local app's, backup/restore missing or the app was already running locally | Ensure the same entries are in the backup-managed sections; never run both copies at once |
| Registry key left behind after exit | Key created by the app but not listed, or a parent key not cleaned | Add the key to `[RegistryKeys]`; add empty parents to `[RegistryCleanupIfEmpty]` |
| Empty folders left in `%APPDATA%` | Directory moved back but source shell left | `[DirectoriesCleanupIfEmpty]` / `[DirectoriesCleanupForce]` |
| "Another instance is running" on first launch | Stale lock from a crashed run, or `SingleAppInstance` mismatch | Check the app's lock file location (move it to `Data`); verify `[Launch]` instance settings |
| Launcher exits immediately, app never starts | Wrong `ProgramExecutable` path (relative to `App\`), or missing runtime (Java/.NET) | Verify the path; add `[Activate] Java` / `UsesDotNetVersion` as applicable; check debug log |
| "*…Portable did not close properly last time it was run and will now clean up*" on launch | Previous run ended without cleanup (crash, unsafe USB eject, Windows shutdown with the app open) — the launcher could not restore local data then | Expected recovery behaviour, not a package bug; launch again after cleanup. If it recurs every run, the app is crashing or a child process holds files open |
| "*…Cannot be started… (ERROR: App\<path>.exe could not be found)*" | `ProgramExecutable` names a file that is not in the package at that relative path | Fix `[Launch] ProgramExecutable` (it is relative to `App\`) and regenerate |
| App starts but can't find its DLLs/plugins | Working directory wrong, or plugin dir moved | Set `[Launch] WorkingDirectory` (sparingly) or keep plugins in `App` and exclude via `[SpecialPaths] Plugins` |
| Second launch loses the file it was asked to open | App's single-instance forwarding + launcher argument order | Review `CommandLineArguments` and the app's own forwarding; test open-with explicitly |
| Installer refuses / hash mismatch on online install | Publisher changed the download, or wrong hash recorded | Re-download from the publisher, verify manually, update `DownloadSHA256` deliberately |
| Upgrade wipes user settings | `installer.ini` removes `Data`, or `DefaultData` overwrites on upgrade | `RemoveDataDirectory` must stay false/omitted; check `[DirectoriesToPreserve]` |
| Menu shows wrong/no icon | Missing PNG size or malformed ICO | Provide the full icon set per `docs/01-format-spec.md` §3 |
| Platform offers no update | `PackageVersion` not increased, or not 4-part numeric | Fix `[Version] PackageVersion` |
| App fails on Windows XP/7-era system | MinOS not declared / runtime too new | Set `[Launch] MinOS` in the launcher INI and test on the oldest claimed OS |

## Performance sanity

- Launcher startup should add well under a second for typical apps.
  Registry/file moves of huge directories (browser profiles) are the
  usual cost — prefer in-place redirection (environment variables,
  command-line switches, the app's own portable mode) over moving large
  trees when the app supports it.
- Avoid `WaitForProgram=false` unless the app truly forks and exits;
  cleanup correctness beats shaving milliseconds.
