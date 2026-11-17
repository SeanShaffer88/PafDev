# 16 — Updating an Existing Package (the Maintainer's Workflow)

Most packaging work is not new packages; it is new versions of the base
app in an existing package. The greenfield workflow
([`07-end-to-end-workflow.md`](07-end-to-end-workflow.md)) still applies,
with these deltas:

1. **Re-run the trace analysis on the NEW base-app build** in a clean VM
   ([`07`](07-end-to-end-workflow.md) Phase 1). New versions add settings
   locations and retire old ones; last version's trace inventory is a
   hypothesis, not a fact. Pay attention to bitness: a trace taken on
   64-bit Windows can mislead for a 32-bit build under WoW64
   ([`15`](15-users-contexts-and-environments.md)).
2. **Decide what happens to existing users' `Data`.** The installer's
   preservation rules ([`02-installer-and-installer-ini.md`](02-installer-and-installer-ini.md))
   decide which folders survive an upgrade. If the base app changed its
   settings format or location, an upgrade can strand the old settings
   in place, unread. The production pattern for a real migration is
   installer custom code that copies the old layout forward on upgrade,
   backing up first — see the Notepad++ set in
   [`../examples/real-world/`](../examples/real-world/) (its
   `PortableApps.comInstallerCustom.nsh` moves a legacy `Data\settings`
   layout to `Data\Config` in `CustomCodePreInstall` and finishes in
   `CustomCodePostInstall`).
3. **`DefaultData` only populates an EMPTY `Data` folder.** Changing
   `DefaultData` in a new release does nothing for existing users. If a
   new default must reach them, that is a `[FileWriteN]` or custom-code
   job, not a `DefaultData` edit — a mistake maintainers make routinely.
4. **Re-verify the payload deliberately.** For online installers,
   re-download the `[DownloadFiles]` target and re-pin `DownloadSHA256`
   ([`02`](02-installer-and-installer-ini.md)). For bundled packages,
   verify the new base-app download against the publisher's signature or
   published hash before bundling it
   ([`18-security-privacy-and-abuse.md`](18-security-privacy-and-abuse.md)).
   A hash change you did not make is a stop sign, not a nuisance.
5. **Bump versions per [`01`](01-format-spec.md)**: new app version in
   the first `PackageVersion` parts, packaging revision in the last;
   `DisplayVersion` states the new base-app version honestly.
6. **Run the upgrade test, checking specifics**
   ([`08`](08-testing-debugging-troubleshooting.md) +
   pre-release checklist): install the *previous* package, create real
   settings, install the new `.paf.exe` over it — then verify the
   specific preserve/remove entries did what they say, the migrated
   settings open in the new version, and files scheduled for removal are
   actually gone. "Settings survived" in general is not the test.
7. **Check the legacy cutoffs.** If this release drops 32-bit Windows or
   an old Windows version, the `[LegacyVersions]` cutoff versions must
   name *this* release, and the legacy launcher files must be present in
   `Other\Source\Legacy\<SuffixFolder>`
   ([`02`](02-installer-and-installer-ini.md),
   [`17-failure-mode-reference.md`](17-failure-mode-reference.md)).
8. **Audit `Data\settings` drift.** If you removed a `[RegistryKeys]`
   entry, existing users still carry its old `.reg` file. Note stale
   files in the release notes; an obsolete key can be re-imported if the
   entry ever returns.
