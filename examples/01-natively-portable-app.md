# Example 1 — Natively portable app

**Shape:** the base app already stores its settings in a file next to its
exe (or has a portable mode). The launcher's job is to redirect that one
settings location into `Data` and provide Platform integration.

Technique: `[FilesMove]` for the settings file. The file lives in
`Data\settings.ini` between runs and is copied next to the exe while the
app runs. Any pre-existing file next to a *local* copy is not involved —
the move target is inside the package's own `App` folder, which only the
portable copy uses.

## launcher INI — `App\AppInfo\Launcher\NoteToolPortable.ini`

```ini
[Launch]
ProgramExecutable=NoteTool\NoteTool.exe
DirectoryMoveOK=yes
SupportsUNC=yes

[FilesMove]
settings.ini=%PAL:AppDir%\NoteTool
```

Notes:

- No `[Activate] Registry=true` — the app never touches the registry, so
  the registry subsystem is not compiled in at all.
- `settings.ini` sits at the root of `Data`, which satisfies the rule
  that a moved file's containing folder inside `Data` must already exist.
- Ship a default `settings.ini` in `App\DefaultData\` if the app needs
  one to exist on first run; otherwise let the app create it (it will be
  moved back to `Data` at exit and kept).

## appinfo.ini (key lines)

```ini
[Details]
Name=NoteTool Portable
AppID=NoteToolPortable
Category=Office
[Version]
PackageVersion=3.1.0.1
DisplayVersion=3.1
[Control]
Icons=1
Start=NoteToolPortable.exe
```

## installer.ini

None needed — defaults are correct.
