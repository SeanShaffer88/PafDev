; PortableApps.com Installer custom code example.
; Location in a package: Other\Source\PortableApps.comInstallerCustom.nsh
; Encoding: Unicode (not ANSI/DOS).
;
; Only these three macros are called by the PortableApps.com Installer.
; Available helpers beyond stock NSIS: ConfigRead, ConfigReadS,
; ConfigWrite, ConfigWriteS, GetParent, GetRoot, VersionCompare, and
; LogicLib. If your code calls 7z.exe, set CustomCodeUses7zip=true in
; installer.ini's [DownloadFiles] section.

!macro CustomCodePreInstall
	; Runs before installation. Example: abort if a prerequisite is absent.
	; IfFileExists "$WINDIR\System32\example.dll" +3 0
	;	MessageBox MB_OK|MB_ICONSTOP "Example prerequisite is missing."
	;	Abort
!macroend

!macro CustomCodePostInstall
	; Runs after installation. Example: remove a file the upstream
	; installer layout includes but the portable package must not ship.
	; Delete "$INSTDIR\App\AppName\Uninstall.exe"
!macroend

!macro CustomCodeOptionalCleanup
	; Runs at the start of installation when the installer's optional
	; section is NOT selected. Intended for upgrades where the previous
	; install had the optional section: clean up its leftovers here.
!macroend
