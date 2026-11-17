# 09 — Licensing, Permissions, and Submitting to PortableApps.com

## The Format's permissions rule (§7 of the Format specification)

> Applications packaged in PortableApps.com Format using our tools must
> be done in accordance with local and international law. **Freeware may
> be packaged using the PortableApps.com Installer but only if the
> installer is unmodified and in its original form** as distributed by
> PortableApps.com. **Freeware may only be packaged by the original
> publisher or with the express consent of the publisher.** Commercial
> software may be packaged by contacting PortableApps.com.

Practical consequences:

- **Open source apps** (OSI-approved license): packaging is permitted by
  the license; still honour trademark rules (below) and include the
  license + source offer in `Other\Source` as the license requires.
- **Freeware (closed source, free of charge)**: you need to *be* the
  publisher or have the publisher's express consent. "It's free" is not
  consent to redistribute. If consent covers distribution but not
  modification/repackaging of the download, use an **online installer**
  (`[DownloadFiles]`) so the bits come from the publisher at install time.
- **Commercial/shareware**: do not package without an agreement with the
  publisher / PortableApps.com.
- **Your own app**: no restriction beyond the tool licenses.

## License metadata must match reality

The `[License]` section of `appinfo.ini` (`Shareable`, `OpenSource`,
`Freeware`, `CommercialUse`) is shown to users in the Platform and drives
distribution decisions. Setting `OpenSource=true` for a freeware binary,
or `Shareable=true` for an app whose license forbids redistribution, is a
defect as real as a broken launcher.

## Trademarks and naming

- The `AppID`/name rules in `docs/01-format-spec.md` exist partly for
  trademark safety: third-party packages carry a suffix
  (`AppNamePortable-example.com` / `AppNamePortable-username`) so they are
  not mistaken for official releases.
- Record trademark notices in `[Details] Trademarks`.
- `BaseAppName` / `ExtractIcon` / `ExtractName` exist for cases where the
  law requires the base app's own name/icon to be used — only then.

## What goes in the package

- The base app's license file(s) and any required notices — normally in
  `App\<AppName>` (as shipped) and/or `Other\Source`.
- If the app is open source, the corresponding source code or a written
  offer/link per its license; PortableApps.com packages conventionally
  note source availability in `Other\Source\Readme.txt` and `help.html`.
- The launcher's own readme (`Other\Source\Readme.txt`, from the
  template) states that the installer and launcher are GPL and where
  their source is available — keep that text intact in derived packages.
- A EULA that must be accepted at install time goes in
  `App\AppInfo\EULA.txt` (see `docs/02-installer-and-installer-ini.md`).

## Development Test releases and official publication

PortableApps.com's community process (via the Portable App Development
forum at portableapps.com):

1. Build and self-test the package thoroughly first
   (`docs/08-testing-debugging-troubleshooting.md`). Do not post a
   package you have not run.
2. Post it as a **Development Test (DT)** release in the Beta Testing
   forum (per the forum's Development Test posting layout): subject
   pattern is the app name + version + "Development Test" revision
   (e.g. "AppName Portable 1.2 Development Test 1"). Include:
   what the app is, its license status and your permission to package it,
   the download link to the `.paf.exe`, its MD5/SHA hash, and known
   issues. Then note the release on the Development Test Releases page,
   and edit the original post for updates rather than starting new
   threads. DT-specific rules:
   - The DT installer file is named with the Dev Test pattern:
     `AppNamePortable_1.2_Dev_Test_1_English.paf.exe`.
   - Compile the **Development Test splash screen** (from the
     Application Template) into the launcher, so testers can see the
     build is not a final release.
   - Follow the current Format specification and build with the current
     Installer — DTs are held to the same format rules as releases.
3. Community members test on varied Windows versions and report leaks,
   leftovers, and bugs. Fix, increment the DT number, repost.
4. When a DT is clean, it becomes a candidate for an official release
   ("Apps Ready For Official Release" tracking). Posting there is a
   commitment: only the app's author/packager may post it, and you must
   be willing to **support the app on an ongoing basis (at least
   6 months)**. Official releases are
   published by PortableApps.com under the app's page, are built with the
   then-current Installer, and thereafter updated through the Platform's
   app store.
5. Keep `PackageVersion` discipline through DTs: DTs are still public
   releases of the package, so `PackageVersion` must increase
   monotonically and stay 4-part numeric (encode test builds in the 4th
   part and in `DisplayVersion`, e.g. DisplayVersion `1.2 Development
   Test 1`).

Rules of thumb from the community process:

- One app per thread; update the first post as DTs progress.
- Respond to tester reports — an unmaintained DT is abandoned, not
  promoted.
- If the base app updates, the portable package is expected to follow;
  stale packages get flagged in the "Outdated Official Apps" tracking.

## Downstream redistribution

Others will copy your package — mirror sites, USB-stick images,
friends. The Format's signals for that are the `[License]` booleans in
`appinfo.ini` (`docs/01-format-spec.md`): `Shareable=true` is the
redistribution signal, and redistributors rely on the booleans being
*accurate* — one more reason false license metadata is a release
defect, not a detail.

- A redistributed copy should be the **unmodified `.paf.exe`**. Anyone
  who re-zips an extracted folder and re-shares it has broken the chain
  of custody the hash discipline depends on
  (`docs/18-security-privacy-and-abuse.md`).
- Copying a package drive-to-drive means copying it **without** the
  `Data` folder — `Data` is the previous user's settings and possibly
  credentials, never part of the distribution.
- Where redistribution of the app itself is not permitted, the online
  installer form is what keeps the publisher's bits out of the
  redistributed file entirely: the `.paf.exe` carries only the downloader
  and the pinned hash.
