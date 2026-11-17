# Tools

Standalone utilities that speed up PortableApps.com package
development. None of them need Windows or the official tools.

| Tool | What it does |
|---|---|
| [`new-package.sh`](new-package.sh) / [`new-package.ps1`](new-package.ps1) | Scaffolds a new package from [`../templates/MinimalAppPortable/`](../templates/): copies the tree, renames the folder/files to `<App>Portable`, and substitutes the app name throughout the INI files and help page. |
| [`check-package.py`](check-package.py) | Static validator for a package tree: layout, `appinfo.ini` rules (Format 3.9, 4-part PackageVersion, the 10 categories, 512-char description, no double quotes), launcher INI naming and section names (unknown sections fail **silently** in PAL — this catches them), installer.ini sections, icon/help warnings. Python 3, standard library only. |
| [`paf-data.json`](paf-data.json) | The Format data the validator uses, in machine-readable form: current tool versions, the 10 categories, launcher/installer section inventories, `[Launch]`/`[Activate]` keys, and the `%PAL:%` environment variables. |
| [`package.gitignore`](package.gitignore) | `.gitignore` for a package source repo — keeps the generated `pac_installer_log.ini` and build outputs out (AGENTS.md rule). |
| [`build-ai-bundle.py`](build-ai-bundle.py) | Regenerates the repo-root `manifest.json` (machine-readable file map + reading order) and `ai-bundle.md` (the whole knowledge base as one file) so AI tools that download the repo — ChatGPT included — can ingest it locally. Run after any content change. |

Usage examples are in each file's header. The validator's inventories
come from `docs/01`, `docs/02`, `docs/04`, and `AGENTS.md` of this
repo; when the Format's documentation changes, update
`paf-data.json` and `check-package.py` together.
