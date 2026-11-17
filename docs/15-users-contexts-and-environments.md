# 15 — Who Uses These Packages, Where, and What That Obliges You to Do

The rest of this knowledge base is written from the packager's chair.
This file is the other side: the people who will run your package, the
places they will run it, and the packaging decisions those facts force.
Items marked *(analysis)* are reasoning about the environment, not
PortableApps.com Format rules. Behaviour marked **Unverified** is not
documented by PortableApps.com — test it yourself before relying on it.

## The jobs you are actually serving

People run portable apps to: use their own apps, settings, and data on a
machine they cannot or may not install software on; try software without
installing it (deleting the folder removes it completely); run an older
version beside a current local install; carry a known-good toolkit
between machines (the IT tech's repair stick); run an app in a language
the host PC is not set to; and keep their data on media they control.
If your package only works on the machine you built it on, it serves
none of these.

People *package* apps to: make a favourite app usable where they can't
install software; ship an official portable edition as the app's
publisher; distribute freeware legally without redistributing it (the
online installer, [`02-installer-and-installer-ini.md`](02-installer-and-installer-ini.md));
portable-ize an existing local install (`[CopyLocalFiles]`); keep an old
app version alive after the new one drops their OS or bitness
(`[LegacyVersions]`); add plugins or locales to an existing package
(plugin installers); or learn how the format works by packaging
something real.

## Who is on the other end — and what breaks for them

| User / situation | What they need | What breaks if you ignore them |
|---|---|---|
| USB roamer (own stick, foreign PCs) | Drive-letter independence, no admin, no traces | The core promise — covered by the migration triple ([`04`](04-launcher-ini-reference.md)) and the leak test ([`08`](08-testing-debugging-troubleshooting.md)) |
| Cloud-drive user (OneDrive/Dropbox/Google Drive, 2+ PCs) | Package survives sync clients | See the cloud row in the environments table — the biggest untested environment |
| Local-disk portable user (folder on C:, prefers no-install) | Same package from a fixed path | Works by design; still test it — "path never changes but the user profile does" is a different case from the stick |
| Shared / family PC user | Their `Data` must not bleed into another Windows user's session; backup/restore must be per-user safe | One user's run restores *another* user's local settings. Test with two accounts ([`08`](08-testing-debugging-troubleshooting.md)) |
| School / library / kiosk user | Runs as guest/standard user; profile may be wiped at logoff | Data "vanishes" — because it was never on the stick. help.html must say data lives in the package folder, not on the PC |
| Locked-down corporate user | No HKLM writes, no elevation available | See the policy row below |
| User with poor / no connectivity | Full installers that work air-gapped; online installers that fail clearly | A half-installed package and no explanation |
| Privacy-conscious user | Zero host leftovers — and honesty about OS-level traces no launcher can remove ([`18-security-privacy-and-abuse.md`](18-security-privacy-and-abuse.md)) | Over-trusting "no trace" |
| User who also has the app locally | Both copies' settings untouched | Covered thoroughly in [`03`](03-launcher-overview.md)/[`08`](08-testing-debugging-troubleshooting.md) |
| User on old hardware / old Windows | Honest `MinOS`; a legacy spin-off when support is dropped | Covered: [`04`](04-launcher-ini-reference.md) `MinOS`/`MaxOS`, [`02`](02-installer-and-installer-ini.md) `[LegacyVersions]` |
| User with a huge profile (browser/mail archives) | Startup not dominated by moving gigabytes | Prefer in-place redirection over moves ([`08`](08-testing-debugging-troubleshooting.md), Performance sanity) |
| User who loses the stick | Knowing the folder copy *is* the backup, and `Data` is the irreplaceable part | The template help.html now says this explicitly |

## Environments beyond the happy path

| Environment | What to do |
|---|---|
| Cloud-synced folder (OneDrive, Dropbox, Google Drive) | *(analysis)* Sync clients lock files and may deliver placeholder (not-yet-downloaded) files, and two PCs can sync `Data` between runs, producing conflict copies of settings and `.reg` files. Prefer in-place redirection (environment variables, the app's own portable mode) over `[FilesMove]`/`[DirectoriesMove]` copy-back, which multiplies lock conflicts. Never claim cloud-folder support you have not tested with the sync client running, on two machines. PAL behaviour under sync clients is **Unverified**. |
| Policy-managed PC (school, library, employer) | *(analysis)* Group Policy / AppLocker can block executables from removable media and writes to HKLM; no package setting overrides policy. Design HKCU-only where the app allows it, use `RunAsAdmin=try` rather than `force` so a refusal degrades instead of dead-ending, and do not promise these machines in help.html. |
| Windows Server / multi-session hosts, Fast User Switching | **Unverified** — PAL behaviour when two users run the same portable copy concurrently is not documented. Do not claim it. |
| Slow removable media (USB 2, cheap flash) | Minimise move-in/move-out volume. A browser-sized profile shuttled over USB 2 is a failed package even if it is a correct one. |
| Nearly-full drives | The installer checks free space using `AdditionalInstallSize` — keep it honest ([`02`](02-installer-and-installer-ini.md)). *(analysis)* Also consider the host drive: Live mode and the contained temp dir need room on the host, not just the stick. |
| Long and deep paths | *(analysis)* Path-length limits bite in three places: where the user puts the package, how deep `Data` grows, and the Live-mode temp copy. Keep package-internal paths short, avoid deep `DefaultData` trees, and test from a deliberately deep folder (200+ characters). |
| Filesystem of the medium | *(analysis)* FAT32 cannot hold a single file over 4 GB and has no ACLs; exFAT/NTFS differ again. If the base app creates large single files, say so in help.html rather than letting it fail on a FAT32 stick. |
| Non-English Windows | Test on a non-English Windows image if you claim multilingual support: installer `[Languages]`, the `[Language]`/`[LanguageFile]` chain, and `FileWrite` `Encoding` are separate systems and each can fail alone. *(analysis)* Apps that store settings in the system ANSI code page can corrupt non-ASCII data when the package moves between differently-localed PCs — if your trace shows ANSI settings files, note it in help.html. |
| Stored window positions | *(analysis)* Settings files often store window geometry. A position saved on a dual-monitor or high-DPI machine can open off-screen on the next PC. This is a portability trace like any other: if the app stores geometry, test first run on a single small display. |
| Offline machines | An online installer is a promise of network. If the app must work air-gapped, ship a full (non-online) installer and say the online one needs internet in its description. A failed download must never be "fixed" by removing `DownloadSHA256` ([`02`](02-installer-and-installer-ini.md)). |
| Antivirus-heavy environments | On-access scanning can slow first runs, lock files during move-back, or quarantine a generated launcher. See [`18-security-privacy-and-abuse.md`](18-security-privacy-and-abuse.md) — and never "fix" false positives with UPX/AppCompactor ([`14`](14-beginner-packaging-guide.md)). |
| Wine as a *run* target | Only the uroesch build route is documented ([`13`](13-ecosystem-and-source-repositories.md)). PAL-on-Wine runtime support is **Unverified**; an optional Wine run is in the [`08`](08-testing-debugging-troubleshooting.md) matrix. |
| ReactOS | Never claimed by any source this repo is built on. **Unverified** — do not claim it. |
| 32-bit app on 64-bit Windows (WoW64) | *(analysis)* A 32-bit base app's registry/file writes may be redirected by WoW64 on 64-bit Windows, so a RegShot trace taken on one bitness can mislead on the other. Trace on the bitness you ship for, or on both. |

## Inputs are wider than the base app

Every input a package consumes is a place it can break — or be broken:

- **Base app in every shape**: Inno installer, ZIP/7z archive, MSI,
  NSIS/other EXE installer, plain folder, existing local install
  (`[CopyLocalFiles]`), single EXE/JAR/.NET assembly. Extraction
  mechanics are in [`02`](02-installer-and-installer-ini.md); the worked
  examples cover Inno and ZIP. MSI is listed among the formats the
  Installer's online mode can extract, but this repo has no worked MSI
  example — verify your exact input format with a test build
  (**Unverified** beyond the Inno/ZIP cases).
- **The online download**: direct URL, redirect chain, knock page
  (`DownloadKnockURL`), publisher re-issue under the same URL, an
  interrupted download. There is **no mirror/fallback key** —
  `Download2*` is a *second file*, not an alternative source for the
  first. If `DownloadURL` dies, the install fails; the fix is a new
  package release, never a removed hash.
- **The user's own documents**, opened via the app (Open With,
  drag-and-drop, Platform associations, Send To). These are untrusted
  input forwarded *through the launcher* — quoting bugs become
  argument-injection bugs ([`18`](18-security-privacy-and-abuse.md)).
- **Command-line arguments to the launcher exe**, forwarded to the app
  in addition to `CommandLineArguments` — including the quote-stripping
  surprise in [`04`](04-launcher-ini-reference.md).
- **The user config INI** next to the exe — runtime-read, user-writable,
  therefore untrusted ([`18`](18-security-privacy-and-abuse.md)).
- **Host state**: environment variables (a broken/hostile `PATH`
  affects DLL loading), a local install's registry state, and `Data`
  written by an *older package version* — the input nobody re-tests.
  Settings migrations across versions are a maintainer task:
  [`16-updating-a-package.md`](16-updating-a-package.md).
- **Language signals that can disagree**: Platform variables, Windows
  locale, installer UI language, the app's own language files. The
  chain and its fallback order are in
  [`04`](04-launcher-ini-reference.md)/[`06`](06-environment-variables.md)/[`10`](10-platform-integration.md);
  wire it end-to-end or the app silently runs in its default language.
