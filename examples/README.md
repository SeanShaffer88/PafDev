# Examples

Worked, annotated packages by app shape. Each example shows the launcher
INI (the part that differs most), the relevant `appinfo.ini` lines, and
the testing focus. All keys used are documented in
`../docs/04-launcher-ini-reference.md`.

| # | Example | Shape |
|---|---|---|
| 1 | [01-natively-portable-app.md](01-natively-portable-app.md) | App already keeps settings next to its exe — one `[FilesMove]` |
| 2 | [02-registry-settings-app.md](02-registry-settings-app.md) | All settings in the registry — `[RegistryKeys]` + cleanup |
| 3 | [03-appdata-filesmove-app.md](03-appdata-filesmove-app.md) | `%APPDATA%` profile + stored absolute paths — `[DirectoriesMove]` + `[FileWriteN]` |
| 4 | [04-java-app.md](04-java-app.md) | Java/JAR app — `[Activate] Java=require`, JVM instance handling |
| 5 | [05-qt-app.md](05-qt-app.md) | Qt app — `[QtKeysCleanup]` for Trolltech cache keys |
| 6 | [06-online-installer-app.md](06-online-installer-app.md) | Freeware without redistribution rights — `[DownloadFiles]` online installer |
| — | [real-world/](real-world/) | **Actual production configs** mirrored from PortableApps AppConfigs (Notepad++ complete set, 7-Zip launcher INI) with commentary |

Pick the example closest to your app's **trace inventory** (from the
analysis phase in `../docs/07-end-to-end-workflow.md`), not the one
closest to your app's category — two apps in the same category can need
completely different launchers. When a real-world config exists for your
app or a similar one, study it first — it outranks the synthetic examples.
