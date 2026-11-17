# Sources

Everything in this repository is drawn from the official PortableApps.com
documentation, checked on **2026-11-16**. If this repo and an official
page disagree, the official page is correct and this repo should be fixed.

## Primary sources

| Topic | Official source |
|---|---|
| Development hub (tool versions) | https://portableapps.com/development |
| Format 3.9 specification (layout, appinfo.ini, installer.ini, icons, plugin installers, permissions) | https://portableapps.com/development/portableapps.com_format |
| Launcher manual (2.2) — index | https://portableapps.com/manuals/PortableApps.comLauncher/ |
| Launcher INI reference | https://portableapps.com/manuals/PortableApps.comLauncher/ref/launcher.ini/ (pages: launch, activate, livemode, environment, registry, filesystem, filewriten, language, qt, services) |
| Environment variable substitution | https://portableapps.com/manuals/PortableApps.comLauncher/ref/envsub.html |
| Language variable values | https://portableapps.com/manuals/PortableApps.comLauncher/topics/languages.html |
| INI file syntax | https://portableapps.com/manuals/PortableApps.comLauncher/ini.html |
| Custom code | https://portableapps.com/manuals/PortableApps.comLauncher/advanced/custom.html |
| PAL 2.1 changes (Custom.nsh / Debug.nsh locations) | https://portableapps.com/manuals/PortableApps.comLauncher/releases/2.1.html |
| Format spec as reproduced in the Launcher manual | https://portableapps.com/manuals/PortableApps.comLauncher/ref/paf/ (appinfo.html, installer.html) |
| Launcher app page (download) | https://portableapps.com/apps/development/portableapps.com_launcher |
| Installer app page (download) | https://portableapps.com/apps/development/portableapps.com_installer |

## Community and archival sources

Mined on 2026-11-16; the durable content is mirrored or distilled inside
this repo (see `docs/13-ecosystem-and-source-repositories.md` and
`docs/14-beginner-packaging-guide.md`), so readers do not need to visit
them.

| Source | What was taken from it |
|---|---|
| https://github.com/PortableApps/AppConfigs | Production configs for every published app; Notepad++ and 7-Zip sets mirrored verbatim in `examples/real-world/` |
| https://github.com/PortableApps/Launcher | Launcher source + bundled manual source. ⚠️ Its `Other/Source/Manual/ref/paf/installer.rst` is an **outdated snapshot** (still shows `DownloadMD5`, `Extract1To`) — the live Format 3.9 page wins |
| http://hg.code.sf.net/p/portableapps/installer | The Installer's own source (Mercurial) — how `installer.ini` is interpreted |
| https://sourceforge.net/projects/portableapps/files/PortableApps.com%20Template/ | Official Application Template downloads (3.9.2) |
| https://github.com/uroesch/PortableAppsTemplate | Community cookiecutter template + PowerShell/Docker build pipeline (unofficial) |
| https://sourceforge.net/projects/paf-assistant/ | "PAF Assistant" — note the live project slug is `pafassistant` (https://sourceforge.net/projects/pafassistant/); unmaintained since 2015 |
| https://web.archive.org/web/20191011180434/https://portableapps.com/development/beginner_packaging | The beginner packaging guide (Wayback served the 2019-03-01 capture); distilled in `docs/14-beginner-packaging-guide.md` |
| http://web.archive.org/web/20191011180434/https://portableapps.com/development | Historical development hub — superseded by the live page for versions/downloads |
| https://portableapps.com/comment/5280#comment-5280 | "A basic NSIS tutorial" — the pre-PAL hand-written launcher skeleton |
| https://portableapps.com/node/21546 | Forum thread: why a ZIP/tarball cannot be compiled into a `.paf.exe` directly (must be in Format first) |
| https://portableapps.com/forums/development/portable_app_development | Portable App Development forum — process and community practice |

## Versions verified

- Format 3.9 (2026-03-02)
- Launcher 2.2.9 (2024-05-25); manual version 2.2
- Installer 3.9.18 (2026-07-20)
- Application Template 3.9.2 (2026-07-11)

## Prior project knowledge

Terminology and workflow conventions (RegShot-based analysis, clean-VM
testing, Development Test process) follow the long-standing PortableApps.com
community practice as documented on portableapps.com forums and the
development pages above.
