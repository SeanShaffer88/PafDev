# Reference — installer.ini Quick Sections

`installer.ini` is **optional** — most packages need none. Create it
from scratch with only the sections your package needs; never copy a
full option list into a project (AGENTS.md). Full reference:
[`../docs/02-installer-and-installer-ini.md`](../docs/02-installer-and-installer-ini.md).
[`../tools/check-package.py`](../tools/) validates section names
against this inventory.

| Section | Use it when |
|---|---|
| `[DownloadFiles]` | Online installer: the `.paf.exe` downloads the app at install time. HTTPS + `DownloadSHA256` always (docs/18). Worked example: [`../templates/online-installer.ini`](../templates/online-installer.ini) |
| `[DirectoriesToPreserve]` | A directory under `App\` (e.g. user plugins) must survive upgrades even though `App\` is replaced |
| `[FilesToPreserve]` | Same, for individual files |
| `[OptionalComponents]` | The package offers optional parts at install time |
| `[LegacyVersions]` | Upgrading from pre-Format or older package layouts |
| `[MainDirectories]` | Non-standard main directory handling |
| `[CopyLocalFiles]` | Copying files from a local installed copy during install |
| `[CheckRunning]` | The installer must detect/close a running instance |
| `[Languages]` | Installer language behaviour beyond the appinfo default |
| `[Source]` | Source-availability information for open-source packages |

Defaults without any `installer.ini`: `App\` and `Other\` are replaced
on upgrade, `Data\` is preserved, and the installer language follows
`appinfo.ini`.
