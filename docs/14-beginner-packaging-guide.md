# 14 — The Beginner Packaging Guide (Distilled, with Modern Corrections)

The original PortableApps.com "Beginner's Development and Packaging Guide"
(a self-described *unfinished* guide, preserved in the Wayback Machine) laid
out the seven steps every packager still follows. They are reproduced here
in substance, each followed by how the step works with today's tools
(Format 3.9, PAL 2.2, Installer 3.9).

## Step 1 — The Idea

Pick an app that would be handy to carry portably. Good candidates do
**not** require Windows administrative rights, do not depend on Windows
services, and do not require internet access (antivirus and system tools
are typically poor candidates). **First check whether a portable version
already exists** — if it does, you're done.

*Today:* also check [`AppConfigs`](13-ecosystem-and-source-repositories.md)
— if PortableApps.com publishes it, its full configuration is there to
learn from.

## Step 2 — The Licensing

Every program is licensed somehow — commercial, shareware, freeware, or
open source. Before packaging, determine whether the licence allows you to
**redistribute** it, **modify** it, or **create a launcher** for it. If it
doesn't, contact the author/publisher and get permission first. Check the
PortableApps.com forums too: the developer may already have stated whether
a portable version is allowed.

*Today:* this is a hard gate, detailed in
[`09-licensing-permissions-submission.md`](09-licensing-permissions-submission.md).
Freeware needs the publisher's express consent and its unmodified official
installer.

## Step 3 — The Analysis

Determine what must change to make the program portable:

- Where does it store settings — registry, INI file, XML, plain text?
- What files does it write, and where? Does it create directories or write
  anywhere else on the local drive?
- Can where it stores settings be changed (command line, environment
  variable, config file)?

Some apps are portable out of the box "if you know where to look." For the
rest, use a monitoring tool — the guide names **RegShot**, **Process
Monitor**, and **RegFromApp**: snapshot the system, run the app, snapshot
again, and compare. The differences are exactly what your launcher must
redirect.

*Today:* do this in a clean VM or Windows Sandbox and record the results
as a trace table mapping every touch point to a launcher mechanism —
[`07-end-to-end-workflow.md`](07-end-to-end-workflow.md), phases 2 and 5.

## Step 4 — The Code

Create a launcher/wrapper that makes the necessary changes when the app
runs and **restores them when it closes**. The guide's era wrote raw NSIS
by hand and recommended studying the Sumatra Portable launcher as the
simplest example.

*Today:* you almost never write the launcher by hand. You write a
launcher INI ([`04-launcher-ini-reference.md`](04-launcher-ini-reference.md))
and the **PortableApps.com Launcher Generator** produces the NSIS launcher.
Hand-written NSIS survives only as `Custom.nsh` hooks for the cases the
INI cannot express ([`05-launcher-advanced-custom-code.md`](05-launcher-advanced-custom-code.md)).

## Step 5 — Compression

Smaller packages take less room on the device and launch faster. The guide
recommended compressing EXEs/DLLs with UPX and recompressing JARs (just
ZIP files with another name) at maximum level with 7-Zip.

*Today:* ⚠️ **Do not follow this step for official-style releases.**
AppCompactor/UPX is **no longer used** for official PortableApps.com
releases — it caused false-positive antivirus detections and breakage.
The `.paf.exe`'s own NSIS compression is sufficient. Skip compression of
the base app's binaries entirely.

## Step 6 — Hosting

The guide pointed open-source packagers at SourceForge free hosting.

*Today:* host source and releases wherever the project lives (GitHub is
typical for community packages). Official distribution is through the
PortableApps.com Platform's app directory after the review process in
[`09-licensing-permissions-submission.md`](09-licensing-permissions-submission.md).

## Step 7 — Testing

Post in the Beta Testing forum so others can test the app and give
feedback to work out bugs.

*Today:* test against the matrix in
[`08-testing-debugging-troubleshooting.md`](08-testing-debugging-troubleshooting.md)
first (first run, persistence, drive-letter change, exit cleanliness,
local-copy coexistence), then post a **Development Test** release in the
forums per [`09-licensing-permissions-submission.md`](09-licensing-permissions-submission.md).

---

*Source: "An Unfinished Beginner's Development and Packaging Guide",
portableapps.com/development/beginner_packaging, via the Wayback Machine
(capture of 2019-03-01). The guide's seven-step shape remains the standard
workflow; the annotations above bring each step up to Format 3.9 practice.*
