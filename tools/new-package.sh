#!/usr/bin/env bash
# new-package.sh — scaffold a new PortableApps.com package from the
# PafDev template (templates/MinimalAppPortable).
#
# Usage:
#   ./new-package.sh <AppName> [destination-dir]
#
# Creates <destination>/<AppName>Portable/ with the folder, the App
# subfolder, and both AppNamePortable.ini files renamed, and the app
# name substituted throughout appinfo.ini, the launcher INI, and
# help.html. You still must: add the base app's binaries, the icons
# (docs/01 §3), fix the metadata (Publisher/Homepage/Category/
# Description/license) and the launcher INI's registry/%APPDATA%
# paths to match your app's real traces (docs/07).
#
# Example:
#   ./new-package.sh MyApp ~/portable-dev
set -euo pipefail

NAME="${1:-}"
DEST="${2:-.}"
if [ -z "$NAME" ]; then
    echo "Usage: $0 <AppName> [destination-dir]" >&2
    exit 2
fi
case "$NAME" in
    *[!A-Za-z0-9]*)
        echo "AppName must be alphanumeric (it becomes the AppID prefix): $NAME" >&2
        exit 2 ;;
esac

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$SCRIPT_DIR/../templates/MinimalAppPortable"
OUT="$DEST/${NAME}Portable"

if [ -e "$OUT" ]; then
    echo "Refusing to overwrite existing folder: $OUT" >&2
    exit 1
fi

mkdir -p "$OUT"
cp -R "$SRC"/. "$OUT"/

# Renames: App subfolder, launcher INI, user-config example INI.
[ -d "$OUT/App/AppName" ] && mv "$OUT/App/AppName" "$OUT/App/$NAME"
[ -f "$OUT/App/AppInfo/Launcher/AppNamePortable.ini" ] && \
    mv "$OUT/App/AppInfo/Launcher/AppNamePortable.ini" \
       "$OUT/App/AppInfo/Launcher/${NAME}Portable.ini"
[ -f "$OUT/Other/Source/AppNamePortable.ini" ] && \
    mv "$OUT/Other/Source/AppNamePortable.ini" \
       "$OUT/Other/Source/${NAME}Portable.ini"

# Substitute the name in text files. Longer token first.
find "$OUT" -type f \( -name '*.ini' -o -name '*.html' -o -name '*.txt' -o -name '*.nsh' \) -print0 |
while IFS= read -r -d '' f; do
    sed -i \
        -e "s/AppNamePortable/${NAME}Portable/g" \
        -e "s/AppName/$NAME/g" \
        "$f"
done

echo "Created $OUT"
echo "Next: add binaries to App/$NAME/, add icons to App/AppInfo/ (docs/01 §3),"
echo "fix appinfo.ini metadata, and set the launcher INI's registry and"
echo "%APPDATA% paths from your trace of the real app (docs/07)."
echo "Validate any time with: python3 tools/check-package.py \"$OUT\""
