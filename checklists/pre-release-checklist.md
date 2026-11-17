# Pre-Release Checklist

Run against the **built `.paf.exe`**, installed fresh — not against the
build tree.

## Build

- [ ] Built with the current PortableApps.com Installer (version
      recorded; not superseded by more than 30 days).
- [ ] Launcher generated with the current PortableApps.com Launcher
      from the exact INI in the package.
- [ ] Output file named `<AppID>_<DisplayVersion>.paf.exe`
      (or `..._online.paf.exe` for online installers).
- [ ] `pac_installer_log.ini` is not committed to the source repo
      (`.gitignore` covers it).

## Install + run (fresh VM or clean snapshot)

- [ ] Fresh install completes to a new `PortableApps` folder.
- [ ] App starts from the Platform menu and directly via the launcher exe.
- [ ] First run creates `Data` from `DefaultData`; defaults are sane.
- [ ] Settings persist across close/reopen.
- [ ] Package copied to a different drive letter and a path with spaces:
      works, settings and MRU intact.
- [ ] Limited (non-admin) user: works (unless admin is declared).
- [ ] Local copy coexistence: with the same app locally installed and
      configured distinctively, the portable run neither reads nor
      alters the local settings, and the local copy is unaffected after.
- [ ] Leak test: registry + filesystem snapshot compare after a full
      run-and-exit shows no leftovers outside the package folder.
- [ ] Exit paths: normal quit, and quit while a document is open, both
      clean up. Crash recovery: kill the app mid-run; next launch
      recovers without losing portable or local settings.
- [ ] File opening: double-clicking an associated file type (or Open
      With → launcher) opens the file in the app.

## Upgrade

- [ ] Previous version installed + settings created; new `.paf.exe`
      installed over it: settings preserved, binaries replaced, files
      scheduled for removal are gone, preserved directories intact.
- [ ] Installer detects the running app and offers to close it.
- [ ] Online installer only: hash verification passes with the real
      publisher file; a corrupted download fails with a clear error.

## Metadata and docs

- [ ] `PackageVersion` increased vs the last release; `DisplayVersion`
      and the file name agree.
- [ ] `help.html` renders, links work, and the user-configuration
      section matches the shipped example INI.
- [ ] `Other\Source\Readme.txt` present with the launcher GPL notice
      intact; base app license(s) included as required.
- [ ] EULA (if any) is `App\AppInfo\EULA.txt`, Unicode, and
      `EULAVersion` is correct.
- [ ] Changelog/release notes state the base app version and the
      packaging revision.

## Security pass

- [ ] Base app binaries verified against the publisher's signature or
      published hash for this exact version.
- [ ] Hostile-filename test: opening files whose names contain spaces,
      embedded quotes, and a leading dash via Open With / drag-and-drop
      opens the file and nothing else (no extra app behaviour).
- [ ] User-config test: a pre-existing `<AppID>.ini` in the package root
      with unexpected `AdditionalParameters` does not change behaviour
      beyond what help.html documents.
- [ ] `Debug.nsh` is absent from the tree and `Data\debug.log` does not
      exist in the built package.
- [ ] help.html carries the honesty statements: `Data` is plaintext
      (drive encryption recommended for sensitive apps), Live mode
      copies `Data` to the host temporarily, OS-level traces (Prefetch,
      recent-items) are outside the launcher's control, and the
      extracted folder is program files — re-install from the original
      `.paf.exe` if its provenance is in doubt.

## Accessibility pass

- [ ] Keyboard-only pass completed (install, first run, exit) and one
      run under Windows high contrast (`docs/19-accessibility.md`).
- [ ] App starts in the Platform's language; icon recognisable at
      16×16.

## Honesty check

- [ ] Anything not actually tested above is listed as **Unverified** in
      the release notes / handoff — not silently implied as tested.
