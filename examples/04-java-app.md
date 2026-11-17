# Example 4 — Java application

**Shape:** the base app is a Java program shipped as a JAR (or a
Launch4J-wrapped exe). It needs a JRE at runtime and stores settings in
`%APPDATA%\ChartTool`.

PAL finds Java for you: `[Activate] Java=require` makes the launcher
locate Java Portable (jPortable, in `CommonFiles\Java`) or a locally
installed JRE/JDK, set `%JAVA_HOME%`, and — because
`ProgramExecutable` is `javaw.exe` — rewrite it to the found JRE binary.

## launcher INI — `App\AppInfo\Launcher\ChartToolPortable.ini`

```ini
[Launch]
ProgramExecutable=javaw.exe
CommandLineArguments='-jar "%PAL:AppDir%\ChartTool\charttool.jar"'
SingleAppInstance=false
CloseEXE=javaw.exe
DirectoryMoveOK=yes
SupportsUNC=yes

[Activate]
Java=require

[DirectoriesMove]
ChartToolConfig=%APPDATA%\ChartTool
```

Key points:

- `SingleAppInstance=false` + `CloseEXE=javaw.exe`: the standard
  Launch4J/JVM pattern from the manual — instance detection against
  `javaw.exe` is unreliable (every Java app looks the same), so the
  launcher is told not to block on a "local copy running" check based on
  the stub, and to close by the JVM exe name.
- Quoting: the whole `CommandLineArguments` value is single-quoted so
  PAL strips the outer quotes, leaving `-jar "X:\...\charttool.jar"`
  with the path safely double-quoted (see the INI quoting rule in
  `docs/04-launcher-ini-reference.md`).
- No cleanup section is needed for `%APPDATA%\ChartTool` itself: it is
  the move target and is restored by `[DirectoriesMove]`. Add
  `[DirectoriesCleanupIfEmpty]` only when the app creates an
  *intermediate* folder (e.g. `%APPDATA%\Publisher\`) that would
  otherwise be left behind empty.
- Declare the dependency in `appinfo.ini` too, so the Platform knows:

```ini
[Dependencies]
UsesJava=yes
```

- If the app can *optionally* use Java but does not require it, use
  `Java=find` instead, and `UsesJava=optional`.

## Alternative: Launch4J exe shipped

If the app ships `ChartTool.exe` (a Launch4J stub) instead of a raw JAR,
set `ProgramExecutable=ChartTool\ChartTool.exe`, keep `Java=require`
(so `%JAVA_HOME%` is set for the stub to find), keep
`SingleAppInstance=false`, and set `CloseEXE` to the real JVM-side exe
name if the stub detaches from the process that does the work.
