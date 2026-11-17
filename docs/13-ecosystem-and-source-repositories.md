# 13 — Ecosystem, Source Repositories, and Community Resources

Everything around the core tools: where the official source code lives, where
real production configurations live, the templates, and the community tooling.
The most useful content from each is mirrored into this repository (see
[`../examples/real-world/`](../examples/real-world/)), so you rarely need to
leave it.

## AppConfigs — the production configuration library

**https://github.com/PortableApps/AppConfigs**

The single most valuable learning resource after the manuals. It contains the
`App\AppInfo` configuration of essentially every app PortableApps.com
publishes, organized by first letter (`#` for digit-leading names, then
`A`–`Z`). Each app folder is flat: `appinfo.ini`, `installer.ini`,
`<AppID>.ini` (launcher INI), `Custom.nsh`, and
`PortableApps.comInstallerCustom.nsh`, as applicable.

How to use it:

- Building a package for an app that already has an official portable
  version? Start from its AppConfigs folder.
- Facing a behaviour you don't know how to express? Find an app with the
  same trait (Java, Qt, .NET, online installer, 32/64-bit split) and read
  how its config solves it.
- Caveat: configs accumulate history. Some declare older format versions
  (Notepad++'s `appinfo.ini` still says `[Format] Version=3.5`) and use
  patterns that predate current manual guidance. Reconcile everything
  against [`01-format-spec.md`](01-format-spec.md) before reusing it.
- Selected complete sets are mirrored in
  [`../examples/real-world/`](../examples/real-world/) with commentary.

## Launcher source and its manual — with a warning

**https://github.com/PortableApps/Launcher** — the PortableApps.com Launcher
source (NSIS), including the manual source under `Other\Source\Manual`.

> ⚠️ **Source-conflict warning.** The manual source bundled in that
> repository is an **old snapshot**. Its installer reference
> (`Other/Source/Manual/ref/paf/installer.rst`) still documents
> `DownloadMD5` and the deprecated `Extract1To`/`Extract1File` keys, both
> removed from the current format. The **live Format 3.9 specification**
> (mirrored in [`01-format-spec.md`](01-format-spec.md) and
> [`02-installer-and-installer-ini.md`](02-installer-and-installer-ini.md))
> wins wherever they disagree. The launcher-INI portion of the manual is
> current for PAL 2.2 and is the basis of
> [`04-launcher-ini-reference.md`](04-launcher-ini-reference.md).

## Installer source (Mercurial)

**http://hg.code.sf.net/p/portableapps/installer** — the PortableApps.com
Installer's own source repository (Mercurial, hosted on SourceForge under
the portableapps project). Read it to understand exactly how `installer.ini`
is interpreted; do not copy its code into a package — installer
customisation belongs in `PortableApps.comInstallerCustom.nsh` only
([`02-installer-and-installer-ini.md`](02-installer-and-installer-ini.md)).

## Templates

### Official Application Template

**https://sourceforge.net/projects/portableapps/files/PortableApps.com%20Template/**
(also linked from https://portableapps.com/development)

The official starting skeleton, current version **3.9.2** (2026-07-11):
the full directory layout with placeholder `appinfo.ini`, launcher INI,
`help.html`, icons, and source readmes. A cleaned, annotated equivalent
lives in [`../templates/MinimalAppPortable/`](../templates/MinimalAppPortable/).
The template's launcher-INI patterns are ground truth — notably the
**path-migration triple** for `[FileWriteN]`
([`04-launcher-ini-reference.md`](04-launcher-ini-reference.md)).

### uroesch/PortableAppsTemplate (community, unofficial)

**https://github.com/uroesch/PortableAppsTemplate**

A cookiecutter-style template used by a large family of unofficial
portable apps. You fill in placeholders (`{{ AppName }}`, `{{ AppNameSpaced }}`,
`{{ UpstreamName }}`, `{{ GitHubUser }}`, …) and get a complete project
whose build is a PowerShell script, `Other/Update/Update.ps1`, which
downloads the upstream release and builds the `.paf.exe` using local clones
of the PortableApps.com Installer and a *patched* PortableApps.com Launcher.
It also documents building on Linux with Wine (or Docker) — the only
maintained Linux build route for `.paf.exe` files. Useful as a project
layout and automation reference; its packages are unofficial and its
patched launcher differs from stock PAL, so do not treat its outputs as
official-format ground truth.

## PAF Assistant (community, unmaintained)

**https://sourceforge.net/projects/pafassistant/** (project slug
`pafassistant`; the `/projects/paf-assistant/` URL does not exist)

A 2014–2015 Windows Forms tool (VB.NET, .NET Framework 4, CC BY-SA 3.0,
last release 1.2, 2015-11-26) that generates the folder structure,
`appinfo.ini`, launcher INI, `help.html`, and icon set from a wizard, then
hands off to the Launcher Generator and Installer. It targets the format
as of 2015, so **anything it generates must be reconciled against Format
3.9** before use. Historical interest and a quick scaffolding aid only.

## The forums

**https://portableapps.com/forums/development/portable_app_development** —
the Portable App Development forum. Where packaging questions are asked,
permissions are sometimes recorded, and Development Test releases are
discussed ([`09-licensing-permissions-submission.md`](09-licensing-permissions-submission.md)).

Two classic threads worth knowing:

- **"How to compile *.paf installer from zip or tarball?"**
  (https://portableapps.com/node/21546, 2009). John T. Haller's answer is
  still the rule: **you can't, directly.** A `.paf.exe` is an installer for
  an app already laid out in PortableApps.com Format; a random ZIP of a
  non-portable app must be analysed and portablized first
  ([`07-end-to-end-workflow.md`](07-end-to-end-workflow.md)). A `.paf.exe`
  is itself just a specialized self-extracting NSIS executable.
- **"A basic NSIS tutorial"** (https://portableapps.com/comment/5280) — the
  pre-PAL way: a hand-written NSIS launcher skeleton. Every launcher was
  once written like this; PAL exists so you almost never have to. The
  skeleton's shape (defines, `Name`/`OutFile`, version information, one
  `Section` doing the work, `$EXEDIR`/`$OUTDIR`, `Exec` vs `ExecWait`) is
  still the mental model underneath PAL's generated launchers and
  `Custom.nsh`.

## Archived pages

The old development hub (https://portableapps.com/development) and the
beginner guide survive in the Wayback Machine; their still-valid content
is distilled in [`14-beginner-packaging-guide.md`](14-beginner-packaging-guide.md).
The current development page supersedes them for versions and downloads.
