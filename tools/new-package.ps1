# new-package.ps1 — scaffold a new PortableApps.com package from the
# PafDev template (templates/MinimalAppPortable).
#
# Usage:
#   .\new-package.ps1 <AppName> [destination-dir]
#
# Creates <destination>\<AppName>Portable\ with the folder, the App
# subfolder, and both AppNamePortable.ini files renamed, and the app
# name substituted throughout appinfo.ini, the launcher INI, and
# help.html. You still must: add the base app's binaries, the icons
# (docs/01 §3), fix the metadata (Publisher/Homepage/Category/
# Description/license) and the launcher INI's registry/%APPDATA%
# paths to match your app's real traces (docs/07).
#
# Example:
#   .\new-package.ps1 MyApp C:\portable-dev
param(
    [Parameter(Mandatory = $true, Position = 0)] [string] $Name,
    [Parameter(Position = 1)] [string] $Destination = "."
)

if ($Name -notmatch '^[A-Za-z0-9]+$') {
    Write-Error "AppName must be alphanumeric (it becomes the AppID prefix): $Name"
    exit 2
}

$src = Join-Path $PSScriptRoot "..\templates\MinimalAppPortable"
$out = Join-Path $Destination "${Name}Portable"
if (Test-Path $out) {
    Write-Error "Refusing to overwrite existing folder: $out"
    exit 1
}

Copy-Item -Recurse $src $out

# Renames: App subfolder, launcher INI, user-config example INI.
if (Test-Path "$out\App\AppName") { Rename-Item "$out\App\AppName" $Name }
if (Test-Path "$out\App\AppInfo\Launcher\AppNamePortable.ini") {
    Rename-Item "$out\App\AppInfo\Launcher\AppNamePortable.ini" "${Name}Portable.ini"
}
if (Test-Path "$out\Other\Source\AppNamePortable.ini") {
    Rename-Item "$out\Other\Source\AppNamePortable.ini" "${Name}Portable.ini"
}

# Substitute the name in text files. Longer token first.
Get-ChildItem -Recurse -File $out |
    Where-Object { $_.Extension -in ".ini", ".html", ".txt", ".nsh" } |
    ForEach-Object {
        $text = Get-Content -Raw $_.FullName
        $text = $text.Replace("AppNamePortable", "${Name}Portable")
        $text = $text.Replace("AppName", $Name)
        Set-Content -NoNewline $_.FullName $text
    }

Write-Host "Created $out"
Write-Host "Next: add binaries to App\$Name\, add icons to App\AppInfo (docs/01 §3),"
Write-Host "fix appinfo.ini metadata, and set the launcher INI's registry and"
Write-Host "%APPDATA% paths from your trace of the real app (docs/07)."
Write-Host "Validate any time with: python3 tools/check-package.py `"$out`""
