# 20 — Common Recipes

The recurring app shapes and the configuration each one needs. Every
recipe points at its full worked example or reference — this page is
the index of patterns, not a substitute for them. All keys named here
are documented in [`04-launcher-ini-reference.md`](04-launcher-ini-reference.md);
if a shape needs a behaviour no key provides, the answer is custom
code ([`05-launcher-advanced-custom-code.md`](05-launcher-advanced-custom-code.md)),
never an invented key.

## Recipe 1 — The app is already portable

**Shape:** settings in its own folder or a file beside the exe, no
registry, no `%APPDATA%`.
**Config:** a `[Launch]` section and little else. Point
`ProgramExecutable` at the exe; move the app's settings folder into
`Data\` with `[FilesMove]`/`[DirectoriesMove]` only if it writes
beside the exe (that folder is under `App\`, which upgrades replace).
**Trap:** "already portable" apps that still drop a registry key or a
`%TEMP%` file — trace before believing (docs/07).
**Full example:** [`../examples/01-natively-portable-app.md`](../examples/01-natively-portable-app.md).

## Recipe 2 — Settings in the registry

**Shape:** the app keeps settings under `HKCU\Software\Publisher\App`.
**Config:** `[Activate] Registry=true` (required), `[RegistryKeys]`
mapping a save-file name to the key, `[RegistryCleanupIfEmpty]` for
the publisher parent. PAL saves the key to `Data\settings\` while
running and backs up/restores a local copy's key automatically.
**Trap:** forgetting `[Activate]` — the registry sections are then
silently inert. Second trap: the app writes values under a *second*
key (recent-files, window state) that the trace missed.
**Full example:** [`../examples/02-registry-settings-app.md`](../examples/02-registry-settings-app.md);
the template package ([`../templates/MinimalAppPortable/`](../templates/))
is this recipe as a tree; Notepad++'s production set is in
[`../examples/real-world/notepadplusplus/`](../examples/real-world/notepadplusplus/).

## Recipe 3 — Settings in %APPDATA%

**Shape:** the app writes `%APPDATA%\Publisher\App`.
**Config:** `[DirectoriesMove]` mapping a `Data\` folder to the
`%APPDATA%` path, plus `[DirectoriesCleanupIfEmpty]` for the parent.
**Trap:** the app *also* uses `%LOCALAPPDATA%` (caches, crash dumps) —
decide per folder: move it, or leave it and accept the trace
(docs/15's user/context analysis decides which).
**Full example:** [`../examples/03-appdata-filesmove-app.md`](../examples/03-appdata-filesmove-app.md).

## Recipe 4 — Java app

**Shape:** a `.jar` or a Java-dependent exe; needs a JRE (portable
jPortable or a local install).
**Config:** `[Activate] Java=yes` — the documented values are
`yes`/`find`/`require` per docs/04 (Java discovery/requirement is an
Activate concern, not a `[Launch]` key).
**Trap:** hard-coding a Java path. Let PAL find it.
**Full example:** [`../examples/04-java-app.md`](../examples/04-java-app.md).

## Recipe 5 — Qt app

**Shape:** Qt-based; leaves Qt's own registry traces and may read
`qt.conf`.
**Config:** the app's own recipes above, **plus** `[QtKeysCleanup]`
(exact name — `[Qt]` is not a section) for Qt's registry keys.
**Trap:** shipping a `qt.conf` with absolute paths — use
`[FileWriteN]` to rewrite them per run.
**Full example:** [`../examples/05-qt-app.md`](../examples/05-qt-app.md).

## Recipe 6 — Online installer

**Shape:** the `.paf.exe` must stay small; the app downloads at
install time.
**Config:** `installer.ini` with `[DownloadFiles]`: the publisher's
canonical URL over **HTTPS**, `DownloadSHA256` set, filename/advanced
extract keys per docs/02. The launcher INI is unchanged.
**Trap:** a hash proves the payload is the file you chose, not that
it is safe — verify the publisher's file first (docs/18). Never
download over HTTP.
**Full example:** [`../examples/06-online-installer-app.md`](../examples/06-online-installer-app.md)
and [`../templates/online-installer.ini`](../templates/online-installer.ini).

## Recipe 7 — The app stores absolute paths in its config

**Shape:** the app writes `D:\path\to\file` into its own INI/XML
settings, which break when the drive letter changes.
**Config:** `[FileWrite1]`, `[FileWrite2]`, … sections rewriting the
stored paths at launch, using the `%PAL:Last*%` variables to find the
old location (reference/environment-variables.md).
**Trap:** rewriting on exit as well as entry, or a Find string that
can match user content — scope the rewrite to the exact keys the app
writes (docs/04's FileWrite semantics).

## Recipe 8 — The app needs admin (rare, justify it)

**Shape:** genuinely cannot run unelevated.
**Config:** `[Launch] RunAsAdmin=try` first; `force` only when `try`
provably fails; `compile-force` only with a written justification in
the package notes (docs/18, least elevation).
**Trap:** reaching for admin to paper over a data-redirection problem
— that problem is Recipes 2/3, not elevation.

## Recipe 9 — Single-instance app

**Shape:** the app refuses or misbehaves on a second launch, or a
second *portable* instance must not fight the first over `Data\`.
**Config:** `[Launch] SingleAppInstance` / `SinglePortableAppInstance`
per docs/04, with `WaitForOtherInstances` when cleanup must wait for
the other instance to exit.
**Trap:** enabling single-instance to hide a data-locking bug — two
instances sharing one `Data\` is the bug; the keys are the guardrail,
not the fix.
