# Example 6 — Online installer (freeware, no redistribution)

**Shape:** a freeware app whose publisher consents to PortableApps.com
packaging but not to third parties mirroring the binaries. The package
therefore ships **without** the app's binaries: the `.paf.exe` downloads
the publisher's own installer at install time and extracts the app from
it. The launcher side is identical to a normal package.

## Package tree difference

`App\AppName\` is **empty** (or nearly) in the source tree — the files
arrive at install time. Everything else (`appinfo.ini`, launcher INI,
icons, `help.html`, `Other\Source`) is present as usual, and the
generated launcher is built into the root as usual.

## installer.ini — `App\AppInfo\installer.ini`

Publisher ships an Inno Setup installer; we extract the `{app}` content:

```ini
[DownloadFiles]
DownloadURL=https://example-publisher.com/files/DrawToolSetup.exe
DownloadName=DrawTool Setup Files
DownloadFilename=DrawToolSetup.exe
DownloadSHA256=PASTE_THE_REAL_64_CHAR_HEX_HASH_HERE
AdditionalInstallSize=62000
DownloadInnoExtractTo=App\DrawTool
DownloadInnoExtractFrom={app}
```

For a plain ZIP download instead:

```ini
[DownloadFiles]
DownloadURL=https://example-publisher.com/files/DrawTool.zip
DownloadName=DrawTool Program Files
DownloadFilename=DrawTool.zip
DownloadSHA256=PASTE_THE_REAL_64_CHAR_HEX_HASH_HERE
AdditionalInstallSize=58000
AdvancedExtract1To=App\DrawTool
AdvancedExtract1Filter=**
```

Rules that matter here:

- **Always** set `DownloadSHA256`. Get it by downloading the file
  yourself from the publisher and hashing it. If the publisher later
  changes the file under the same URL, installs will fail the hash
  check — that is the protection working; update the hash deliberately
  after verifying the new file.
- `AdditionalInstallSize` is in KB and covers the extracted size beyond
  what's inside the `.paf.exe`, so the installer can check free space.
- `AdvancedExtract1Filter=**` means "everything, recursively" in 7-Zip
  filter syntax. Narrow it (e.g. `DrawTool\**`) when the archive
  contains wrapper folders or files the portable package must not ship.
- The built file is named `DrawToolPortable_2.0_online.paf.exe` — the
  `_online` suffix is how users and the Platform know a network download
  happens at install time.

## appinfo.ini (key lines)

```ini
[License]
Shareable=true
OpenSource=false
Freeware=true
CommercialUse=true
```

`OpenSource=false` — freeware is not open source; the `[License]`
booleans must describe the base app truthfully.

## Launcher INI

Unchanged from a normal package for this app shape (registry +
`%APPDATA%` handling as in Examples 2–3). The launcher does not care
whether the binaries arrived via the installer payload or via a
download — by the time it runs, `App\DrawTool` is populated either way.
