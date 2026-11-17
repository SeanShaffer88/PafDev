${SegmentFile}

; PortableApps.com Launcher custom code for AppName Portable.
; Location: App\AppInfo\Launcher\Custom.nsh  (PAL 2.1+)
; Delete this file if the package needs no custom code -- most don't.
; After ANY edit here, regenerate the launcher or the change does nothing.
; Reference: docs/05-launcher-advanced-custom-code.md in the PafDev repo.

; Example: register a bundled DLL only while the app runs.
;${SegmentPrePrimary}
;	RegDLL $AppDirectory\AppName\Example.dll
;!macroend
;
;${SegmentPostPrimary}
;	UnRegDLL $AppDirectory\AppName\Example.dll
;!macroend
