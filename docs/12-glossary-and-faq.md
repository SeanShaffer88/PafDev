# 12 — Glossary and FAQ

## Glossary

- **AppID** — Globally unique identifier of a package; also its folder
  name (`AppNamePortable`).
- **appinfo.ini** — `App\AppInfo\appinfo.ini`; metadata the Platform and
  Installer read (name, version, category, license, dependencies).
- **Application Template** — Official skeleton package with commented
  configuration files; the canonical starting point.
- **Base app** — The original, non-portable application being packaged.
- **CommonFiles** — `PortableApps\CommonFiles`; shared components (Java)
  used by multiple packages; also a plugin-installer type.
- **Data directory** — The package's `Data\` folder; the only place user
  data and settings may live.
- **DefaultData** — `App\DefaultData`; first-run defaults copied into
  `Data` by the launcher.
- **Development Test (DT)** — A public test build posted in the Portable
  App Development forum before official release.
- **DisplayVersion** — Human version string (`2.4 Revision 2`); never
  used for update comparison.
- **envsub** — PAL's environment-variable substitution (`%PAL:DataDir%`
  etc.) applied to launcher INI values.
- **Format** — PortableApps.com Format, the layout/behaviour
  specification (current: 3.9).
- **help.html** — The package's help file, in the package root.
- **installer.ini** — Optional `App\AppInfo\installer.ini` configuring
  the PortableApps.com Installer (downloads, optional components,
  upgrade rules).
- **Launcher (PAL)** — PortableApps.com Launcher; the generator + the
  generated `<AppID>.exe` that makes the base app portable.
- **launcher.ini** — Shorthand for `App\AppInfo\Launcher\<AppID>.ini`,
  PAL's configuration file. (The file is never actually named
  `launcher.ini`.)
- **Live mode** — Running from read-only media by copying app/data to a
  temp folder first; forced by the user config `RunLocally=true`.
- **Online installer** — A `.paf.exe` (named `..._online.paf.exe`) that
  downloads the base app at install time via `[DownloadFiles]`.
- **PackageVersion** — 4-part numeric package version (`x.x.x.x`) in
  `appinfo.ini`; drives update checks.
- **.paf.exe** — A compiled PortableApps.com Format installer file.
- **PAL** — PortableApps.com Launcher.
- **Platform** — The PortableApps.com Platform: menu, App Store, updater.
- **Plugin installer** — A `.paf.exe` built from `plugininstaller.ini`
  that adds files to an existing package.
- **RegShot** — Snapshot/compare tool used to discover an app's traces.
- **Segment** — A named hook block in PAL custom NSIS code that runs at a
  specific point in the launcher lifecycle.
- **Trace inventory** — The complete list of registry keys/files an app
  touches, gathered during analysis; every item must be handled by the
  launcher.

## Easily confused — five different things called "portable"

| Thing | What it actually is |
|---|---|
| A Format package (folder) | The extracted `AppNamePortable` tree: `App\`, `Data\`, `Other\`, the generated launcher exe, help.html. What the packager authors and what actually runs |
| A `.paf.exe` | The compiled installer that *delivers* a Format package. It is an artifact of the package, not the package itself |
| A ZIP of the package folder | The same tree in an archive. Works when extracted by hand, but no App Store install/update, no validation — not a Format release (see the FAQ below) |
| A "portable by design" app | A base app that natively keeps its settings beside its exe. It still needs a Format package (metadata, launcher, installer) to be a PortableApps.com release |
| The Platform | The menu/App Store program that discovers, installs, updates, and launches packages. Packages must also work launched directly, without it |

## FAQ

**Do I need to write code to make a portable app?**
Usually not. Most apps are made portable with only the launcher INI.
NSIS custom code is the escape hatch for the rest.

**Can I just zip the folder instead of building a .paf.exe?**
A zipped package folder works when extracted manually, but it is not a
PortableApps.com Format *release*: no App Store install/update, no
upgrade preservation rules, no online-download mechanism. Official-style
distribution is the `.paf.exe` built by the current Installer.

**Why four version parts?**
Windows version resources and the Platform's comparison are 4-part
numeric. `PackageVersion` follows that; the human version lives in
`DisplayVersion`.

**My app is already portable (settings next to the exe). Do I still need
a launcher?**
Yes — a thin one. Point the app at `Data` (its own portable switch, an
environment variable, or `[FilesMove]` for its settings file), and you
still need the generated launcher as `[Control] Start`, for splash,
single-instance handling, and Platform integration.

**The app is .NET/Java. Anything special?**
Declare it: `UsesDotNetVersion` in `appinfo.ini` for .NET; for Java use
`[Activate] Java=find|require` in the launcher INI so Java Portable or a
local JRE is located and `%JAVA_HOME%` set.

**Can a portable app require admin rights?**
Yes, but declare it in both places that apply: `RequiresAdmin=yes` in
`appinfo.ini` and `[Launch] RunAsAdmin` in the launcher INI. Prefer
`try` over `force` when only some features need elevation.

**Can I package this freeware app I like?**
Only if you are its publisher or have the publisher's express consent
(see `docs/09-licensing-permissions-submission.md`). Otherwise, build the
package for your own use and do not distribute it — or ask the publisher.

**Where do I get help?**
The Portable App Development forum at portableapps.com, and the Launcher
manual. Search existing Development Test threads for your app first —
someone may already maintain a package of it.
