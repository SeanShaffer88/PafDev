# 18 — Security, Privacy, and Abuse

The rest of this knowledge base is about correctness. This file is the
threat side: who can attack a package, a packager, or a user, and what
the format does — and does not — do about it. Items marked *(analysis)*
are security reasoning applied to documented behaviour; items marked
**Unverified** are not established by the sources this repo is built on.

## Threat model in one page

**Assets at risk**

- **The host PC's integrity.** The launcher deliberately writes to the
  host registry, `%APPDATA%`, and TEMP, then restores them
  ([`03`](03-launcher-overview.md)). Anything that breaks the
  backup/restore symmetry — or a package that never intended to
  restore — leaves persistent changes. With `RunAsAdmin`, the package
  runs elevated.
- **The user's portable data.** All settings, profiles, and saved
  credentials live in `Data\`, in the clear, on removable media.
- **The publisher's reputation.** A trojanized repack is distributed
  under the publisher's name and icon.
- **The format's trust.** Users are trained that `.paf.exe` means safe
  and vetted. That trust attaches to the *format*, so any `.paf.exe`
  from any site borrows it.
- **The packager's build machine.** Packaging executes untrusted code by
  design: the base app runs during analysis, custom code is compiled
  into the launcher and runs at install/launch time.
- **The host user's data (reverse direction).** The launcher reads and
  copies a local install's settings to back them up, and
  `[CopyLocalFiles]` imports local files into the package. A hostile
  package can walk away with host data inside its `Data\`.

**Attackers**: a malicious packager; a compromised upstream publisher;
a network attacker on the install-time download path; a malicious
document opened in the app; a hostile host machine the stick is plugged
into; a co-user with write access to the package folder; and fake
"portable apps" download sites.

## Security rules for packagers

1. **Licensing is a security control, not paperwork.** The
   publisher/consent rule ([`09`](09-licensing-permissions-submission.md))
   is what separates an official package from a trojanized one. Never
   package what you cannot account for.
2. **Verify the base app before you bundle it.** Download only from the
   publisher's canonical URL; check the publisher's signature or hash
   where offered; record the source URL and the SHA-256 of what you
   bundled. A compromised upstream download becomes a compromised
   package that passes every format check.
3. **Online installers: HTTPS + pinned hash, always.** `DownloadURL`
   (and `DownloadKnockURL`, if unavoidable) must be the publisher's own
   HTTPS address, and `DownloadSHA256` must always be set. A hash proves
   the payload is the file the *packager chose* — it does not prove the
   file is safe or that the publisher made it. Never delete or blank a
   hash to fix a failed install; re-verify the new file and update the
   hash deliberately ([`02`](02-installer-and-installer-ini.md)).
   Whether the downloader enforces HTTPS is **Unverified** — require it
   by policy.
4. **Custom code is code.** `Custom.nsh`,
   `PortableApps.comInstallerCustom.nsh`, and `Debug.nsh` are arbitrary
   NSIS that run at launch/install time — possibly elevated. Read every
   line of any file you copy from AppConfigs, a forum, or a template
   repo before generating. Prefer INI over custom code; justify any
   `${DisableSegment}` / `${OverrideExecute}` in writing.
5. **Least elevation.** Default `RunAsAdmin=none`. Use `try` before
   `force`; use `compile-force` only with a written justification (it
   removes the explanatory message and gets a conditioned UAC click).
   Declare `RequiresAdmin=yes` in appinfo.ini whenever elevation is
   used, so the Platform can surface it before install.
6. **A package that installs a service or driver is not a PAL
   package.** Services are disabled in PAL 2.2
   ([`04`](04-launcher-ini-reference.md)). Do not route around that with
   custom code; treat any third-party package that does as untrusted
   until manually reviewed. This disablement is a load-bearing safety
   property of the format.
7. **Scope destructive sections like a loaded tool.**
   `[RegistryCleanupForce]` and `[DirectoriesCleanupForce]` delete
   unconditionally on every exit. List only trees your trace inventory
   proved the app creates; prefer the `IfEmpty` variants; use the `-`
   discard form for keys the app must never persist
   ([`17`](17-failure-mode-reference.md) §E).
8. **Treat `[CopyLocalFiles]` and broad `[RegistryKeys]` lists as
   data-access declarations** — the portable equivalent of app
   permissions. They copy host files/registry data into the package.
   Include them only when the feature needs them, scope them to exact
   paths/keys, and say in help.html what is copied.
9. **No code through `Data`.** Binaries belong in `App\` (Format rule).
   Never use `[FilesMove]`/`[DirectoriesMove]` to shuttle DLLs or
   scripts through `Data\`. Declare real plugin folders with
   `[SpecialPaths] Plugins` and tell users that folder is code.
10. **Keep `CleanTemp=true`** and `SupportsUNC` at `warn`/`no` unless
    UNC operation is a tested requirement. Do not add `PATH` entries or
    `WorkingDirectory` overrides pointing outside the package.
11. **Mind what `Data` contains.** Settings and `Data\settings\*.reg`
    files are plaintext and may hold credentials (see Privacy below).
12. **Truthful metadata is a security property.** `[License]` booleans,
    `DisplayVersion`, `Homepage`, and `Donate` are rendered in the
    Platform and drive update decisions ([`10`](10-platform-integration.md)).
    A `PackageVersion` bump that does not match the stated release is a
    release-blocking defect — version comparison is not authenticity.
13. **Get the tools only from portableapps.com** and record their
    versions ([`11`](11-tools-and-versions.md)). A patched or
    third-party Generator/Installer changes the trust base of
    everything it builds; label such builds unofficial.
14. **Do not ship debug builds.** Remove `Debug.nsh` before release
    ([`08`](08-testing-debugging-troubleshooting.md)): a shipped
    `Data\debug.log` leaks full paths and segment traces to anyone who
    later holds the stick.

## The risks behind the rules (summary)

| Risk | Mechanism in one line | Covered by |
|---|---|---|
| Trojanized repackaging | Anyone can build a `.paf.exe`; provenance and review are the only separators | Rule 1; [`09`](09-licensing-permissions-submission.md) |
| Compromised upstream (bundled) | Packager bundles a poisoned download once; no downstream check exists | Rule 2 |
| Online-installer substitution | MITM/mirror serves a bad file; hash stops it only if the installer itself is genuine | Rule 3 |
| DLL search-order hijacking *(analysis)* | Windows loads DLLs from the app's own folder first; that folder is on writable removable media | Rule 9/10; treat the package folder as trusted-code territory |
| No runtime integrity check *(analysis)* | The launcher INI is compiled in, but nothing verifies the *files*: replace `App\…\App.exe` or a DLL beside it and the genuine launcher runs the replacement | Tell users (help.html note below) to re-install from the original `.paf.exe` if a folder's provenance is doubtful |
| User config INI injection *(analysis)* | `<AppID>.ini` next to the exe is runtime-read and writable: `AdditionalParameters` and custom `${ReadUserConfig}` keys can change what runs | Rule 4 applies to custom keys too: validate values in `Custom.nsh`, document them in help.html |
| Argument injection via opened files *(analysis)* | Crafted filenames/URLs pass through `[Associations]` patterns and PAL's weak quote-stripping into the app's command line | Quote `%1` in patterns; run the hostile-filename test in the pre-release checklist |
| UNC attacks *(analysis)* | Running from `\\server\share` loads binaries over the network from that server and can expose the user's NTLM credential material to it | Rule 10 |
| Temp races / Live-mode exposure *(analysis)* | Temp names are fixed (`…PortableTemp`, `…PortableLive`); Live mode copies all of `Data` onto the host disk for the run. Whether PAL fails safe if the temp path already exists with hostile contents is **Unverified** | Rule 10; warn users in help.html |
| Update channel abuse *(analysis)* | Updates compare `PackageVersion` only; `DisplayVersion` never gates anything; `Homepage`/`Donate` are packager-controlled links in a trusted UI | Rule 12 |
| Extraction reaching outside the target *(partly Unverified)* | `[CopyLocalFiles]`, `<ROOT>` extract targets, `[LegacyVersions]`, and plugin installers deliberately write outside `<parent>\<AppID>`; 7-Zip path-traversal protection on hostile archives is **Unverified** | Review any installer.ini using them as privileged configuration |
| Java resolution *(Unverified)* | PAL's search order for `[Activate] Java=find` is not documented in this repo; prefer `require` + Java Portable for sensitive apps | Rule 13's spirit: know your toolchain |

## Privacy

- **Leave-no-trace is the format's core privacy control**, and it is
  only as good as the trace inventory
  ([`01`](01-format-spec.md) §4, [`08`](08-testing-debugging-troubleshooting.md)
  leak test). Done wrong, the traces are: registry keys and `%APPDATA%`
  leftovers (covered), Qt per-path cache keys (`[QtKeysCleanup]`), and
  crash dumps written by the app or Windows Error Reporting to host
  locations outside every move/cleanup section *(analysis)*.
- **What portability cannot hide** *(analysis)*: OS-level traces no
  launcher can remove — Prefetch records (exe name, path, run times),
  recent-items/jump-list entries for files you opened, thumbnail
  caches, and the host registry's USB device history. Never advertise a
  package as forensic-proof; state the limit instead.
- **`Data` is plaintext.** Settings files and the
  `Data\settings\*.reg` exports may contain credentials, tokens, and
  private keys in clear text. **A lost or stolen stick is a full
  profile compromise** for browsers, mail clients, and FTP/SSH tools.
  If the base app has a master-password or encrypted-vault option,
  enable or recommend it in help.html, and advise users carrying
  sensitive apps to encrypt the drive itself (e.g. BitLocker To Go).
  Never describe a package as "private" without these caveats.
- **Sync is silent replication.** If the PortableApps folder sits inside
  OneDrive/Dropbox/Google Drive, `Data` — including the plaintext
  `.reg` files — is copied to third-party servers and every synced
  machine ([`15`](15-users-contexts-and-environments.md)).
- **Metadata travels with the folder.** Settings files contain absolute
  paths from every machine the package has run on (that is why the
  migration triple exists); `pac_installer_log.ini` records install
  times and versions; `Data\debug.log` can contain full paths. Users
  sharing a `Data` folder for bug reports should inspect it first.
- **The base app's network behaviour is unchanged.** Packaging moves
  where an app stores data, not what it sends. Telemetry and cloud
  features still phone home — now from every host the stick visits.
  Where the app has an offline mode or a telemetry opt-out settable via
  `[RegistryValueWrite]`/`[FileWriteN]`, using it is a privacy
  improvement worth documenting in help.html.

## Abuse cases (know them; don't build for them)

- **Policy bypass.** "No installation, no admin" is indistinguishable
  from a tool for evading workplace/school software policy. That is the
  user's legal/disciplinary risk, and packagers should not market
  packages as policy-evasion tools.
- **Portable malware toolkits.** Password-recovery and network tools are
  legitimate `Security`/`Utilities` apps and standard attacker kit. The
  format is neutral; official-distribution review
  ([`09`](09-licensing-permissions-submission.md)) is the only gate, and
  it binds only official distribution.
- **License circumvention.** Packaging commercial software to defeat
  its installation/activation is forbidden by the Format
  ([`09`](09-licensing-permissions-submission.md)). False `[License]`
  booleans that make redistribution look authorised are the soft form
  of the same abuse.
- **Fake "portable" download sites.** The highest-volume real-world
  abuse: SEO-poisoned sites offering "AppName Portable" downloads that
  are adware/malware wearing the format's name, icon, and
  `.paf.exe` naming convention — a convention anyone can copy. The
  anti-impersonation controls (official distribution, third-party
  `AppID` suffixing) bind only honest packagers.
- **Anti-forensic use.** Leave-no-trace plus Live mode's
  copy-run-delete cycle is a privacy feature and an anti-forensic
  feature. Document its limits (above) rather than letting users
  over-trust it.
- **Online installers as scan evasion.** A small clean downloader whose
  payload arrives at install time defeats static scanning of the
  distributed file. `DownloadSHA256` does not help here — a malicious
  packager pins the hash of a malicious payload. Reviewers of online
  installers must fetch and inspect the *payload*, not just the
  installer.ini.

## Suggested help.html wording (trust and privacy note)

> Download this package only from PortableApps.com or the app
> publisher's own site. Other sites offering "portable" versions of
> well-known apps are a common malware channel, whatever the file is
> named. Third-party (non-PortableApps.com) packages are unsigned;
> Windows may warn the first time you run one — check where the file
> came from instead of dismissing the warning by habit. Your settings
> live in the `Data` folder in plain form, like most apps' settings; if
> you carry accounts or credentials in this app, encrypt the drive (for
> example with BitLocker To Go). The extracted package folder is
> program files: if anyone else could have changed files in it, delete
> it and re-install from the original `.paf.exe`. Running from a
> network share (`\\server\share`) loads the program over the network
> and can expose your Windows credentials to that server — copy the
> package to a drive you control first.
