# 05 — Launcher Advanced Topics: Segments and Custom Code

Most packages need **no** custom code. Write it only when the launcher
INI (docs/04) cannot express a behaviour — and check the Development
forum first, because there is usually an INI way.

Sources: PAL 2.2 manual, `advanced/custom.html`; PAL 2.1 release notes;
official PortableApps.com forum guidance from the PAL developers.

## The Custom.nsh file

| PAL version | Location |
|---|---|
| **2.1 and later (current)** | `App\AppInfo\Launcher\Custom.nsh` |
| 2.0 (legacy) | `Other\Source\PortableApps.comLauncherCustom.nsh` |

The Generator automatically upgrades the legacy path/name when it first
compiles a package that still uses it. The manual's custom-code page
still shows the old `Other\Source` location in one sentence — that is a
known documentation error (acknowledged by the developers in the forum);
the release notes and the Generator's actual behaviour put the file in
`App\AppInfo\Launcher\Custom.nsh`. After editing `Custom.nsh`, the
launcher must be **regenerated** — custom code is compiled in, not read
at runtime.

All non-debugging launcher modifications go in this one file. Do not edit
PAL's own segment files or the generated launcher.

## Segments and hooks

PAL is built from **segments** (one per feature: FilesMove, RegistryKeys,
Environment, …). Each segment runs code at defined points of the
launcher lifecycle through **hooks**. A custom segment adds your own
hooks to that lifecycle.

File structure:

```nsh
${SegmentFile}

; Optional: segment-specific macros/functions first, prefixed with
; _YourSegmentName_ by convention, then any Var declarations.

${SegmentInit}
    ; ... NSIS code ...
!macroend

${SegmentPrePrimary}
    ; ... NSIS code ...
!macroend
```

Rules:

- The **first line** of `Custom.nsh` is `${SegmentFile}`.
- Each hook is written as `${Segment<Hook>}` … `!macroend`.
- Custom macros/functions should be prefixed with the segment name
  (e.g. a "Start" macro in a FilesMove-like segment becomes
  `_FilesMove_Start`) and placed immediately after `${SegmentFile}`,
  before variable declarations.
- LogicLib is already included — `${If}` / `${ElseIf}` / `${EndIf}` and
  friends are available with no extra include.

### Hook names (lifecycle order)

Verified hook macros include:

| Hook | When it runs |
|---|---|
| `${Segment.onInit}` | In NSIS `.onInit` — earliest possible point |
| `${SegmentInit}` | Initialisation, before any Pre hooks |
| `${SegmentPre}` | Before the primary/secondary split |
| `${SegmentPrePrimary}` | Before the (first) app launch — the most common custom hook: register DLLs, rename files into place, set up extra redirection |
| `${SegmentPreExec}` | Immediately before execution (either instance kind). The manual advises preferring `Pre` |
| `${SegmentPreExecPrimary}` | Immediately before the primary executable is executed |
| `${SegmentPreExecSecondary}` | Immediately before a secondary executable is executed |
| `${SegmentPost}` | Cleanup/restoration for either instance kind |
| `${SegmentPostPrimary}` | After the primary app exits — undo what PrePrimary did (unregister DLLs, rename files back) |
| `${SegmentPreSecondary}` | Before a secondary launch (launcher invoked again while the app is already running) |
| `${SegmentPostSecondary}` | After a secondary launch |
| `${SegmentUnload}` | Final teardown, after all Post hooks |

There is no `PreUnload`/`PostUnload` hook. The execution step itself is
not a hook — it can only be replaced wholesale with `${OverrideExecute}`.

The built-in **segments** these hooks belong to (names used by
`${DisableSegment}`, `${DisableHook}`, and the `DEBUG_SEGMENT_…` flags
in [`08-testing-debugging-troubleshooting.md`](08-testing-debugging-troubleshooting.md)):
`Core`, `DirectoriesCleanup`, `DirectoriesMove`, `DirectoryMoving`,
`DriveLetter`, `Environment`, `ExecString`, `FileWrite`, `FilesMove`,
`InstanceManagement`, `Java`, `Language`, `OperatingSystem`, `Qt`,
`RefreshShellIcons`, `Registry`, `RegistryCleanup`, `RegistryKeys`,
`RegistryValueBackupDelete`, `RegistryValueWrite`, `RunAsAdmin`,
`RunLocally`, `Services` (currently not functional and disabled),
`Settings`, `SplashScreen`, `Temp`, `Variables`, `WorkingDirectory`.

The manual's custom-code page links the exhaustive hook list; if you
need a hook not listed here, look it up there rather than guessing a
name — an unknown `${Segment…}` macro fails the Generator compile, which
is your safety net.

### Worked example — register a DLL only while the app runs

From official forum guidance for a VB6-era app shipping `ccrpbds6.dll`:

```nsh
${SegmentFile}

${SegmentPrePrimary}
    RegDLL $AppDirectory\PIXResizer\ccrpbds6.dll
!macroend

${SegmentPostPrimary}
    UnRegDLL $AppDirectory\PIXResizer\ccrpbds6.dll
!macroend
```

(`$AppDirectory` is a PAL-provided NSIS variable holding the package's
`App` directory path; `$Bits` similarly holds 32/64 for bitness checks in
custom code. These are NSIS variables for custom code — not `%…%` envsub
variables; see docs/06 for the distinction.)

### Worked example — an extra user-config option

Custom code can define new keys for the user configuration file
(`<AppID>.ini` next to the exe) with `${ReadUserConfig}`:

```nsh
${SegmentFile}

${SegmentInit}
    ${ReadUserConfig} $1 AlwaysUse32Bit
    ${If} $1 == true
        StrCpy $Bits 32
    ${EndIf}
!macroend
```

Any key you introduce this way **must be documented in the package's
`help.html`**, and boolean keys use `true`/`false` by convention.

## Reading configuration from custom code

| Macro | Purpose |
|---|---|
| `${ReadLauncherConfig} $0 Section Key` | Read a value from the launcher INI (wraps `ReadINIStr`; check `${Errors}` after `ClearErrors` to distinguish missing from empty) |
| `${ReadLauncherConfigWithDefault} $0 Section Key Default` | Same, with a fallback value when the key does not exist |
| `${ReadUserConfig} $0 KeyName` | Read a value from the user config file next to the exe (renamed from `${ReadUserOverrideConfig}` in 2.1; the Generator upgrades the old name) |

## Defining your own environment variables

```nsh
${SetEnvironmentVariablesPath} VarName $value
```

Defines (or overrides) an environment variable that the rest of the
launcher — including envsub in the launcher INI — can then use as
`%VarName%`. The production pattern (Notepad++ Portable, mirrored in
[`../examples/real-world/notepadplusplus/`](../examples/real-world/notepadplusplus/)):
define a `FullAppDir` variable in `${SegmentInit}` that points at the
32-bit or 64-bit app folder depending on `$Bits`, then use `%FullAppDir%`
as the target throughout `[FilesMove]`/`[DirectoriesMove]`. Remember:
`%FullAppDir%` without a definition like this does nothing — it is not a
built-in (the built-in is `%PAL:FullAppDir%`, the folder of the running
`ProgramExecutable`; see
[`06-environment-variables.md`](06-environment-variables.md)).

## Disabling built-in behaviour (last resort)

```nsh
${DisableHook} Segment Hook     ; disable one hook of a built-in segment
${DisableSegment} Segment        ; disable a whole built-in segment
```

The manual's warning stands: disabling segments very easily breaks the
launcher's backup/restore symmetry and strands user data or host
settings. Ask in the Development forum before doing this.

## Overriding the execute step (last resort)

```nsh
${OverrideExecute}
    ; ... complete replacement for the app-launch step ...
!macroend
```

Only when the standard execution genuinely cannot run the app. Read
PAL's own Execute function first (`Other\Source\PortableApps.comLauncher.nsi`
in the Launcher's source) — an override that forgets argument forwarding
or exit-code handling will fail testing in ways that look like app bugs.

## Debugging custom code and launchers

- **Debug.nsh:** since PAL 2.1, debugging code lives in
  `App\AppInfo\Launcher\Debug.nsh` (previously
  `Other\Source\PortableApps.comLauncherDebug.nsh`; the Generator
  upgrades the path). Debug builds log what each segment does, which is
  how you prove a hook fired and in what order. Regenerate the launcher
  after changing debug code, and do not ship a debug build as a release.
- **MessageBox probes:** the low-tech standard — temporary
  `MessageBox MB_OK "..."` lines in a hook confirm execution and show
  variable values during development.
- **Generator output is the compiler log:** a failed generation prints
  the NSIS error with the file/line of the offending macro or include;
  fix that first error, not the cascade after it.
- A missing `Custom.nsh` include warning at generation time
  (`could not find: "...App\AppInfo\Launcher\Custom.nsh"`) simply means
  the package has no custom code — it is a warning, not a failure, in
  template-based packages that reference the file optionally.

## When custom code is the wrong answer

- The behaviour is expressible in the INI (moves, writes, environment,
  registry) — INI wins: it is validated, documented, and survives PAL
  upgrades.
- You are tempted to write a whole separate NSIS launcher — don't, for
  anything intended for official release; PAL is more powerful, more
  stable, and far easier to maintain (the developers' own guidance).
