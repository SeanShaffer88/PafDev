# Example 5 — Qt application

**Shape:** a Qt-based app. Qt apps typically store settings under
`HKCU\Software\<Org>\<App>` **and** write Qt framework cache keys under
`HKCU\Software\Trolltech\OrganizationDefaults\…` that embed the app's
absolute path. Those cache keys break (or leak) when the package moves,
so PAL has a dedicated cleanup section for them.

## launcher INI — `App\AppInfo\Launcher\HexViewPortable.ini`

```ini
[Launch]
ProgramExecutable=HexView\HexView.exe
DirectoryMoveOK=yes
SupportsUNC=yes

[Activate]
Registry=true

[RegistryKeys]
HexView=HKCU\Software\HexWorks\HexView

[RegistryCleanupIfEmpty]
1=HKCU\Software\HexWorks

[QtKeysCleanup]
1=Qt Factory Cache 4.8\com.trolltech.Qt.QImageIOHandlerFactoryInterface:
2=Qt Plugin Cache 4.8.false
```

How the Qt entries are built (from the manual):

- Find the offending keys under
  `HKCU\Software\Trolltech\OrganizationDefaults\` after a test run
  (RegShot shows them).
- Strip that prefix, and strip the trailing portable path from the key
  name. What remains is the `[QtKeysCleanup]` entry.
- The Qt version in the entry (`4.8` above) must match the Qt version
  the base app was built with — check the app's DLLs/about dialog.

Notes:

- `[QtKeysCleanup]` requires `[Activate] Registry=true` like every other
  registry section.
- If the app also uses Qt's `QSettings` with a custom organisation name,
  that still lands under `HKCU\Software\<Org>\<App>` and is handled by
  the ordinary `[RegistryKeys]` entry — there is no separate Qt settings
  mechanism.
- Newer Qt versions (Qt 5+) use the organisation name directly under
  `HKCU\Software` in many builds; the Trolltech cache keys are the
  Qt 4-era pattern. Verify with RegShot which pattern *your* app
  actually writes instead of copying these entries blindly — the entries
  above are the documented format, with the versions as an example.
