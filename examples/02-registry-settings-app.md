# Example 2 — Registry-settings app

**Shape:** the base app stores all settings under
`HKCU\Software\Publisher\AppName`, writes a few values under
`HKCU\Software\Publisher` as well, and leaves an empty `Publisher` key
behind when uninstalled. It also caches thumbnails in a `Temp` subkey
that should never be saved.

## launcher INI — `App\AppInfo\Launcher\PixelToolPortable.ini`

```ini
[Launch]
ProgramExecutable=PixelTool\PixelTool.exe
DirectoryMoveOK=yes
SupportsUNC=yes

[Activate]
Registry=true

[RegistryKeys]
PixelTool=HKCU\Software\Publisher\PixelTool

[RegistryCleanupForce]
1=HKCU\Software\Publisher\PixelTool\Temp

[RegistryCleanupIfEmpty]
1=HKCU\Software\Publisher
```

How it works:

- `[RegistryKeys]` exports the app's key to
  `Data\settings\PixelTool.reg` at exit and re-imports it at start. If a
  local install of PixelTool exists, its key is backed up before the
  portable run and restored afterwards.
- `[RegistryCleanupForce]` deletes the `Temp` cache subkey after the run
  instead of saving it (it is recreated by the app; saving it would bloat
  `Data` and could carry host-specific paths).
- `[RegistryCleanupIfEmpty]` removes the `Publisher` parent if the run
  left it empty, so no trace remains in the host registry.

Order note: numbering in the cleanup sections must be consecutive
starting at 1.

## appinfo.ini (key lines)

```ini
[Details]
Name=PixelTool Portable
AppID=PixelToolPortable
Category=Graphics & Pictures
[Version]
PackageVersion=5.0.0.1
DisplayVersion=5.0
[Control]
Icons=1
Start=PixelToolPortable.exe
```

## Testing focus

Run the leak test (docs/08) twice: once on a machine with no local
PixelTool (expect zero leftovers), and once with a local PixelTool whose
settings you changed first (expect the local settings intact afterwards).
